# Lezione 5 – Failure detector e leader election

## Di cosa parliamo

Finora i crash erano solo un'ipotesi del modello: un processo può fermarsi e nessuno lo sa. Questa lezione introduce dei moduli che <b>danno informazioni sui crash</b>:

- i <b>failure detector</b> (FD): "secondo me $p$ è morto";
- la <b>leader election</b>: "questo processo è vivo, usalo come coordinatore".

L'idea chiave è che questi moduli <b>incapsulano le ipotesi sul tempo</b>. Invece di ragionare su timeout e ritardi dentro ogni algoritmo (complicato e facile da sbagliare nelle dimostrazioni), si scrive una volta sola un modulo che usa il tempo, e gli algoritmi sopra usano solo le sue proprietà. Alla fine si usano FD e leader election per rendere la mutua esclusione resistente ai crash.

Slide: versione 2026/27 ("Time III"), con in più gli esercizi della versione 2024/25.

## 1. L'astrazione failure detector

!!! abstract "In breve"

    Un failure detector è un modulo che, a ogni processo, segnala quali altri processi sono crashati. Funziona "a ping": se uno non risponde in tempo, lo considero morto. Più il sistema è sincrono, più le sue risposte sono affidabili.

- Funziona <b>solo per i crash</b> (crash-stop), non per i guasti bizantini: un processo bizantino può rispondere ai ping e intanto comportarsi male.
- Si descrive con due proprietà:
    - <b>Completeness</b> (completezza): la capacità di <b>accorgersi di tutti</b> i crash.
    - <b>Accuracy</b> (accuratezza): la capacità di <b>non sbagliare</b>, cioè non dichiarare morto un processo vivo.

Nota: soddisfare una sola delle due è banale. "Dichiaro tutti morti" ha completezza perfetta; "non dichiaro mai nessuno" ha accuratezza perfetta. Il difficile è averle insieme.

## 2. Perfect failure detector (P)

### Specifica

!!! abstract "In breve"

    P non sbaglia mai. Prima o poi tutti i processi corretti si accorgono di ogni crash, e se P dice che un processo è crashato, è davvero crashato.

Evento: $\langle \text{Crash} \mid p \rangle$, "ho rilevato che $p$ è crashato".

- <b>PFD1 – Strong completeness</b>: prima o poi ogni processo crashato viene rilevato, in modo permanente, da <b>ogni</b> processo corretto. → liveness
- <b>PFD2 – Strong accuracy</b>: se un processo viene rilevato da qualcuno, allora è davvero crashato. → safety

<b>Modello necessario</b>: sistema <b>sincrono</b>, crash, e link <i>perfect sincroni</i> (perfect link + se $p$ corretto manda $m$ al tempo $t$ e il destinatario non crasha entro $t + \text{max_delay}$, $m$ arriva entro $t + \text{max_delay}$).

<b>In asincrono non si può</b>: un processo lento e uno crashato sono indistinguibili (Lezione 2). Qualunque timeout scegli, prima o poi un processo vivo ma lento lo supera e lo dichiari morto per sbaglio, violando l'accuracy.

### Algoritmo "Exclude on Timeout"

Ogni $\Delta$ unità di tempo: chi non mi ha risposto dall'ultimo giro è morto; poi mando un nuovo ping a tutti.

```text
upon event ⟨P, Init⟩ do
    alive := Π; detected := ∅
    starttimer(Δ)

upon event ⟨Timeout⟩ do
    forall p ∈ Π do
        if p ∉ alive and p ∉ detected then    // non ha risposto
            detected := detected ∪ {p}
            trigger ⟨P, Crash | p⟩
        trigger ⟨pl, Send | p, HEARTBEAT_REQUEST⟩
    alive := ∅
    starttimer(Δ)

upon event ⟨pl, Deliver | q, HEARTBEAT_REQUEST⟩ do
    trigger ⟨pl, Send | q, HEARTBEAT_REPLY⟩

upon event ⟨pl, Deliver | p, HEARTBEAT_REPLY⟩ do
    alive := alive ∪ {p}
```

<b>Perché funziona</b> (con $\Delta \ge 2 \cdot \text{max_delay}$):

- <i>Strong completeness</i>: se $p_1$ crasha al tempo $t$, entro $t + \Delta$ ricevo un nuovo giro di ping, $p_1$ non risponde, e al timeout successivo lo rilevo. Il ritardo di rilevamento è quindi limitato (circa $2\Delta$).
- <i>Strong accuracy</i> (per assurdo): se rilevo $p$ ma era vivo, o la mia richiesta non gli è arrivata entro il timeout, o la sua risposta non è arrivata a me. Ma andata + ritorno durano al massimo $2 \cdot \text{max_delay} \le \Delta$. Contraddizione.

<b>Trade-off su</b> $\Delta$: più è piccolo, più in fretta rilevo i crash, ma mando più messaggi. Non può scendere sotto $2 \cdot \text{max_delay}$, altrimenti perdo l'accuracy.

### Domande tipiche sulle slide

- <b>Processi diversi possono rilevare lo stesso crash in momenti diversi?</b> Sì. La specifica dice solo "prima o poi": in un certo istante $p_0$ e $p_2$ possono già avere $p_3$ in <code>detected</code> e gli altri no. Quanto prima è "prima o poi" lo dice l'algoritmo, non la specifica (con Exclude on Timeout, entro circa $2\Delta$).
- <b>Se al tempo</b> $t$ <b>p non è in</b> <code>detected</code><b>, posso dire che è vivo al tempo</b> $t$<b>?</b> No. Un processo conosce il mondo solo tramite messaggi, che impiegano tempo: al tempo $t$ sa com'era il mondo un po' prima. Nessun FD può dire se qualcuno è vivo <b>adesso</b>: può essere crashato un istante fa.

### Migliorare P: il P a round

!!! abstract "In breve"

    Se gli orologi sono sincronizzati, non serve chiedere "sei vivo?". Basta che ognuno mandi "sono vivo" all'inizio di ogni turno: chi tace in un turno è morto. Si dimezzano i messaggi.

Citazione nelle slide: "nelle reti sincrone, <b>i silenzi parlano</b>" (N. Santoro). Exclude on Timeout usa 2 messaggi per coppia (richiesta + risposta). Se tutti hanno un orologio sincronizzato, basta 1 messaggio.

Ipotesi: sincronizzatore di clock con skew massimo $\delta$, link con ritardo massimo $\text{max_delay}$ e ritardo <b>minimo</b> $\text{min_delay} > \delta$.

Il tempo viene diviso in <b>round</b> di lunghezza $T$, con $T > 2(\text{max_delay} + \delta)$ nella slide. All'inizio di ogni round ogni processo:

1. dichiara crashati quelli da cui <b>non</b> ha ricevuto il BEAT nel round precedente;
2. manda BEAT a tutti quelli che considera ancora corretti.

<b>Perché funziona.</b> Bisogna mostrare che un BEAT spedito quando il mio round è $r$ arriva a $p$ quando anche $p$ è al round $r$:

- se entro nel round $r$ al tempo $t$, per lo skew $p$ ci entra tra $t - \delta$ e $t + \delta$;
- $p$ resta nel round $r$ almeno fino a $t - \delta + T$, che è maggiore di $t + \delta + \text{max_delay}$;
- il mio BEAT arriva nell'intervallo $(t + \text{min_delay}, t + \text{max_delay}]$; poiché $\text{min_delay} > \delta$, non arriva prima che $p$ sia entrato nel round $r$.

Quindi: se ho mandato il BEAT ero vivo, e il BEAT arriva nel round giusto. Se $p$ non riceve il mio BEAT, l'unico motivo è che non l'ho mandato, cioè sono crashato. Da qui completeness e accuracy.

<b>Due processi possono rilevare lo stesso crash in round diversi?</b> Sì: se $p_3$ crasha <b>a metà</b> del ciclo con cui manda i BEAT, alcuni lo ricevono e altri no. Chi non l'ha ricevuto lo rileva al round dopo; gli altri un round più tardi.

### Sincrono = a round

Un modo alternativo di vedere il sincrono: il tempo è diviso in <b>round</b> logici e

- tutti i processi cambiano round nello stesso momento;
- un messaggio mandato da un processo corretto all'inizio del round $r$ arriva a tutti i corretti entro la fine del round $r$.

I round sono lo strumento standard per progettare algoritmi sincroni e la misura standard del loro tempo (numero di round). Lettura opzionale: <i>The splendors and miseries of rounds</i>, A. Shimi, 2019.

## 3. Eventually perfect failure detector (◇P)

### L'idea

!!! abstract "In breve"

    Nel modello eventualmente sincrono non si può avere un FD che non sbaglia mai. Si accetta che sbagli per un po', purché sia pronto a correggersi. Non "rileva" più i crash: li <b>sospetta</b>.

Modello: <b>eventualmente sincrono</b>, crash, perfect link. Prima del tempo $T$ (ignoto) il sistema si comporta in modo asincrono e il FD può sospettare processi corretti. Per questo ci sono due eventi:

- $\langle \text{Suspect} \mid p \rangle$: sospetto che $p$ sia crashato;
- $\langle \text{Restore} \mid p \rangle$: mi sono sbagliato, $p$ non è più sospettato.

### Specifica

- <b>EPFD1 – Strong completeness</b>: prima o poi ogni processo crashato è sospettato <b>per sempre</b> da ogni processo corretto.
- <b>EPFD2 – Eventual strong accuracy</b>: prima o poi <b>nessun</b> processo corretto è sospettato da un processo corretto.

Differenza con P: l'accuracy vale solo "da un certo momento in poi". Prima, il FD può sbagliare quanto vuole.

### Algoritmo "Increasing Timeout"

Come Exclude on Timeout, con due differenze: se un processo sospettato si rifà vivo, lo <b>ripristino</b>; e siccome il mio timeout era troppo corto, lo <b>allungo</b>.

```text
upon event ⟨◇P, Init⟩ do
    alive := Π; suspected := ∅
    delay := Δ
    starttimer(delay)

upon event ⟨Timeout⟩ do
    if alive ∩ suspected ≠ ∅ then       // ho sospettato qualcuno che era vivo
        delay := delay + Δ               // il timeout era troppo corto
    forall p ∈ Π do
        if p ∉ alive and p ∉ suspected then
            suspected := suspected ∪ {p}
            trigger ⟨◇P, Suspect | p⟩
        else if p ∈ alive and p ∈ suspected then
            suspected := suspected \ {p}
            trigger ⟨◇P, Restore | p⟩
        trigger ⟨pl, Send | p, HEARTBEAT_REQUEST⟩
    alive := ∅
    starttimer(delay)

// le risposte ai ping sono identiche a Exclude on Timeout
```

<b>Perché funziona</b>

- <i>Strong completeness</i>: un processo crashato smette di rispondere, quindi viene sospettato e nessuno lo ripristinerà più.
- <i>Eventual strong accuracy</i>: dopo il tempo $T$ i messaggi arrivano entro un ritardo massimo, che esiste ma <b>non conosciamo</b>. Ogni volta che sospetto per sbaglio un processo vivo, prima o poi arriva la sua risposta, lo ripristino e allungo il timeout. Dopo un numero finito di errori il timeout supera il tempo di andata e ritorno (circa $2 \cdot \text{MAX_DELAY}$; la versione 2024/25 delle slide dice proprio così, quella nuova scrive $\text{MAX_DELAY}$) e non sbaglio più.

### Proprietà: gli insiemi dei sospettati si allineano

<b>Lemma</b>: per due processi corretti $p_1, p_2$ esiste un tempo (di <i>stabilizzazione</i>) dopo il quale $\text{suspected}_1 = \text{suspected}_2$.

Dimostrazione (per assurdo): sia $p$ in $\text{suspected}_1$ ma non in $\text{suspected}_2$ per sempre. Se $p$ è corretto, $p_1$ viola l'eventual strong accuracy. Se $p$ è crashato, $p_2$ viola la strong completeness.

Da un certo punto in poi, quindi, i sospettati sono esattamente i crashati, uguali per tutti. Questo lemma serve per Ω.

## 4. Leader election

### Perché

!!! abstract "In breve"

    A volte non interessa sapere chi è morto, ma avere <b>un</b> processo vivo di riferimento, per esempio un coordinatore. La leader election è un modulo che indica quel processo.

### Leader election (LE), con P

Evento: $\langle \text{Leader} \mid p \rangle$, "$p$ è il leader". Solo per crash-stop.

- <b>LE1 – Eventual detection</b>: o non c'è nessun processo corretto, oppure prima o poi viene eletto leader un processo corretto.
- <b>LE2 – Accuracy</b>: se un processo diventa leader, tutti i leader eletti prima sono crashati.

In parole: non si cambia leader finché quello attuale è vivo.

<b>Algoritmo "Monarchical Leader Election"</b> (usa P). Ogni processo ha un <i>rank</i> (es. l'ID). Il leader è il processo di rank massimo tra quelli non crashati.

```text
upon event ⟨le, Init⟩ do
    suspected := ∅; leader := ⊥

upon event ⟨P, Crash | p⟩ do
    suspected := suspected ∪ {p}

upon leader ≠ maxrank(Π \ suspected) do
    leader := maxrank(Π \ suspected)
    trigger ⟨le, Leader | leader⟩
```

<b>Perché funziona</b>: <i>eventual detection</i> viene dalla strong completeness di P (prima o poi tutti i crashati sono esclusi e resta un corretto). <i>Accuracy</i> viene dalla strong accuracy di P (si esclude solo chi è davvero crashato) più l'ordine totale sui rank: il leader cambia solo quando quello attuale è crashato.

<b>Esempi "possibile?" nelle slide</b>

- Tutti hanno $p_0$ come leader. $p_0$ crasha; $p_1$ se ne accorge e si elegge, mentre $p_2$ ha ancora $p_0$. <b>Possibile</b>: $p_2$ non ha ancora rilevato il crash, e la specifica non chiede che succeda per tutti nello stesso momento.
- Poi $p_2$ elegge sé stesso mentre $p_1$ è vivo ed era già stato eletto. <b>Non possibile</b>: viola LE2, perché $p_1$, un leader precedente, non è crashato.

### Eventual leader election (Ω)

Se il FD non è perfetto (◇P) non si può garantire LE2. Si indebolisce la specifica.

Evento: $\langle \text{Trust} \mid p \rangle$, "mi fido di $p$ come leader".

- <b>ELD1 – Eventual accuracy</b>: da un certo momento ogni processo corretto si fida di un processo <b>corretto</b>.
- <b>ELD2 – Eventual agreement</b>: da un certo momento nessuna coppia di processi corretti si fida di processi corretti <b>diversi</b>.

Con Ω, per un periodo arbitrario, i leader possono cambiare a caso e ce ne possono essere <b>più d'uno contemporaneamente</b>. Quando il leader diventa unico e non cambia più si dice che si è <b>stabilizzato</b>.

Le due proprietà sono indipendenti. Esempi nelle slide: un'esecuzione in cui alla fine tutti si fidano dello stesso processo, ma crashato, soddisfa l'agreement ma non l'accuracy. Un'esecuzione in cui ognuno si fida di un corretto, ma diverso, soddisfa l'accuracy ma non l'agreement.

<b>Algoritmo "Monarchical Eventual Leader Detection"</b> (usa ◇P): uguale al monarchico, ma con $\langle \text{Suspect} \rangle$ si aggiunge a <code>suspected</code> e con $\langle \text{Restore} \rangle$ si toglie. Ci si fida del processo di rank massimo tra i non sospettati.

<b>Perché funziona</b>

- <i>ELD1</i>: per la strong completeness, prima o poi <code>suspected</code> contiene tutti i crashati, quindi $\Pi \setminus \text{suspected}$ contiene solo corretti.
- <i>ELD2</i>: per il lemma sopra, gli insiemi dei sospettati di due corretti diventano uguali, quindi <code>maxrank</code> restituisce lo stesso processo a entrambi.

## 5. Tre modelli di guasto e confronto col sincrono

### Fail-stop, fail-noisy, fail-silent

!!! abstract "In breve"

    Si classificano i modelli con crash in base al failure detector disponibile: P (fail-stop), ◇P (fail-noisy), nessuno (fail-silent).

| Modello | Cosa c'è |
| --- | --- |
| <b>Fail-stop</b> | crash + perfect link + <b>P</b> |
| <b>Fail-noisy</b> | crash + perfect link + <b>◇P</b> |
| <b>Fail-silent</b> | crash + perfect link, <b>nessun FD</b> |

- Fail-stop <b>implica</b> fail-noisy (P è anche un ◇P), e fail-noisy implica fail-silent (si può sempre ignorare il FD).
- <b>Esecuzioni</b>: fail-stop $\subset$ fail-noisy $\subset$ fail-silent.
- <b>Problemi risolvibili</b>: al contrario, fail-silent $\subset$ fail-noisy $\subset$ fail-stop. Più il modello dà, più problemi si risolvono. È lo stesso ragionamento della Lezione 3 su sincrono/asincrono.

### Fail-stop vs sincrono

Il sincrono è <b>più forte</b> del fail-stop. Nel sincrono si può costruire P (Exclude on Timeout), quindi tutto ciò che si risolve in fail-stop si risolve anche in sincrono. Il viceversa no: il fail-stop dà un FD perfetto, ma non dà limiti sui tempi.

Esempi di problemi risolvibili in sincrono ma non in fail-stop (risposta del prof): <b>sincronizzazione degli orologi</b> e <b>timed delivery</b> ("se $p$ manda $m$ a $q$, $q$ lo riceve entro $x$"). Problemi risolvibili in fail-stop ma non in sincrono: <b>nessuno</b>.

## 6. Applicazione: mutua esclusione tollerante ai crash

### Lamport ME + P

!!! abstract "In breve"

    Lamport ME (Lezione 4) si blocca se un processo crasha, perché aspetta il suo ACK o il suo RELEASE per sempre. Con P si può "dimenticare" chi è crashato.

Le proprietà vanno riscritte tenendo conto dei crash:

- <b>Mutua esclusione</b>: in ogni istante al massimo un processo <b>non crashato</b> è in CS.
- <b>Liveness</b>: se un processo <b>corretto</b> chiede la CS, prima o poi entra.
- <b>Fairness</b>: se un processo <b>corretto</b> $p$ chiede prima di $q$, $q$ non entra prima di $p$.

<b>Punti critici</b> dell'algoritmo originale: un processo crashato <b>non manda il RELEASE</b> (se era in CS, o in coda, blocca tutti) e <b>non manda l'ACK</b> (chi aspetta il suo ACK si blocca).

<b>Patch</b>, alla ricezione di $\langle \text{Crash} \mid p_j \rangle$ da P:

1. aggiungo $p_j$ a <code>Crashed</code>;
2. tolgo da <code>Requests</code> le richieste di $p_j$;
3. per entrare non aspetto più l'ACK dei processi in <code>Crashed</code>: la condizione diventa "ACK da ogni $p \in \Pi \setminus \text{Crashed}$".

<b>Non basta.</b> Una REQ di $p_0$ può essere ancora in viaggio quando $p_0$ crasha e io lo rilevo. Se arriva <b>dopo</b> il rilevamento, la metto in coda e non verrà mai tolta (nessun RELEASE arriverà, e il crash l'ho già gestito): blocca le mie richieste per sempre.

<b>Patch corretta</b>: in più, alla ricezione di una REQ, la si accetta <b>solo se il mittente non è in</b> <code>Crashed</code>.

### Un algoritmo più semplice: P + leader election

Idea:

- con LE si elegge un <b>leader</b> che fa da coordinatore;
- chi vuole la CS manda una richiesta al leader;
- il leader concede la CS una richiesta alla volta, in ordine FIFO;
- chi esce manda un RELEASE al leader;
- se il leader rileva il crash di $p$: se $p$ non era in CS toglie la sua richiesta, se era in CS fa come se avesse rilasciato.

<b>Problema: cambio di leader.</b> Solo il vecchio leader sapeva chi era in CS. Se quel processo è crashato va bene; se è vivo, risponderà. Quindi il nuovo leader fa una <b>fase new_leader</b>: chiede a tutti i processi non rilevati come crashati se sono in CS e aggiorna il suo stato. Solo dopo serve nuove richieste. I processi che avevano richieste pendenti le rimandano al nuovo leader.

## 7. Esercizi e homework

??? note "T minimo per il P a round (soluzione proposta)"

    Dalla dimostrazione, serve che $p$ sia ancora nel round $r$ quando arriva il BEAT, cioè $t - \delta + T > t + \delta + \text{max_delay}$, quindi

    $$
    T > \text{max_delay} + 2\delta
    $$

    Il valore della slide, $T > 2(\text{max_delay} + \delta)$, è sufficiente ma più grande del necessario. Serve inoltre $\text{min_delay} > \delta$, perché il BEAT non arrivi prima che $p$ sia entrato nel round $r$.

??? note "Timeout di ◇P con ritardo massimo sconosciuto: come aumentarlo e diminuirlo? (soluzione proposta)"

    <b>Stabilizzare il prima possibile</b>: invece di aggiungere $\Delta$ a ogni errore, <b>raddoppiare</b> il timeout. Se il valore giusto è $D$, con incrementi fissi servono circa $D/\Delta$ errori, raddoppiando solo $\log_2(D/\Delta)$.

    <b>Latenza bassa sui crash veri</b>: un timeout troppo grande fa accorgere tardi dei crash. Si può <b>diminuire lentamente</b> il timeout quando per molti giri non ci sono stati errori, e misurare gli RTT reali per tenerlo vicino al massimo osservato (più un margine). Il compromesso classico è <b>aumento veloce e diminuzione lenta</b>, come il controllo di congestione di TCP (al contrario).

??? note "Mutua esclusione tollerante ai guasti in fail-silent e fail-noisy? (considerazioni, non dimostrazioni)"

    <b>Fail-silent: no.</b> Se il processo in CS smette di rispondere, non c'è modo di sapere se è crashato o solo lento. Aspettarlo per sempre viola la liveness; dare la CS a un altro rischia di avere due processi vivi in CS e viola la mutua esclusione.

    <b>Fail-noisy: sembra di no.</b> ◇P può sbagliare per un tempo arbitrario. Se sospetta per errore il processo in CS e la CS viene data a un altro, la mutua esclusione (safety) è violata, e una violazione di safety non si recupera anche se poi ◇P si corregge. Servirebbe un FD che non sbaglia mai su chi è vivo, cioè P.

??? note "Esercizio 2.8 del libro: un FD che non è ◇P può far violare una safety? (soluzione proposta)"

    No. Le proprietà di ◇P sono tutte "prima o poi", quindi <b>qualunque comportamento finito</b> del FD (anche "non sospetto nessuno") può essere l'inizio di un'esecuzione in cui ◇P è corretto. Una violazione di safety si vede in un prefisso finito. Se A violasse la safety con un FD "sbagliato", la stessa violazione apparirebbe anche in un'esecuzione in cui il FD è un vero ◇P (stesso prefisso), contro l'ipotesi che A sia corretto. Il FD sbagliato può rompere solo la <b>liveness</b>.

??? note "Esercizio 2.9 del libro: abstraction la cui liveness si rompe se il FD non rispetta le proprietà (soluzione proposta)"

    Esempio già visto: <b>leader election monarchica con P</b>. Se il FD non rispetta la strong completeness (es. non rileva mai nessun crash) e il leader crasha, nessuno elegge un nuovo leader: viola LE1 (eventual detection), che è una proprietà di liveness.

??? note "Esercizio d'esame (settembre 2021): perfect link su un link con al più k perdite (soluzione del prof, slide 2024/25)"

    <b>Link "bounded k-loss"</b>: no duplication, no creation, e se $p$ manda $T > k$ messaggi, $q$ ne consegna almeno $T - k$. In pratica il link perde <b>al massimo k messaggi in tutto</b>. L'<i>overhead</i> $O$ è quanti messaggi in più servono: per far consegnare $X$ messaggi ne mando al massimo $X + O$. Lo stubborn ha overhead infinito.

    <b>Q4.1 – Perfect link con overhead finito.</b> Mando ogni messaggio $k+1$ volte (almeno una copia arriva, perché se ne perdono al massimo $k$). Il ricevente scarta i duplicati con l'insieme <code>delivered</code>. Per $X$ messaggi spedisco $(k+1)X$, quindi overhead $kX$.

    <b>Q4.2 – Overhead minimo.</b> Per <b>un</b> messaggio servono almeno $k+1$ invii (l'avversario può perderne $k$), quindi $O = k$. Per un <b>lotto</b> di $X > k$ messaggi si fa meglio con gli ACK:

    1. mando ognuno degli $X$ messaggi <b>una volta</b>;
    2. il ricevente, per ogni messaggio consegnato, manda un ACK $k+1$ volte (così arriva sicuramente);
    3. quando ho ricevuto ACK per $X - k$ messaggi (al massimo $k$ sono andati persi), rimando i non confermati, al massimo $k$, ognuno $k+1$ volte.

    Totale messaggi del mittente: $X + k(k+1)$. L'overhead $k(k+1)$ <b>non dipende da</b> $X$.

    <b>Q4.3 – Link unidirezionale</b> (il ricevente non può rispondere). Si può ancora fare il perfect link con $k+1$ copie per messaggio, ma senza ACK non si sa cosa è andato perso: overhead $kX$, come per i singoli messaggi.

## Riepilogo

- I <b>failure detector</b> incapsulano le ipotesi sul tempo e funzionano solo per i crash. Due proprietà: <b>completeness</b> (li becco tutti) e <b>accuracy</b> (non sbaglio).
- <b>P</b> (sincrono): strong completeness + strong accuracy. Si fa con <i>Exclude on Timeout</i> ($\Delta \ge 2 \cdot \text{max_delay}$), o con il <i>P a round</i> che usa la metà dei messaggi grazie agli orologi sincronizzati.
- <b>◇P</b> (eventualmente sincrono): strong completeness + <b>eventual</b> strong accuracy. <i>Increasing Timeout</i>: sospetta, ripristina se sbagliato e allunga il timeout. Gli insiemi dei sospettati dei corretti prima o poi coincidono.
- <b>Leader election</b> (con P): prima o poi un corretto è leader, e si cambia leader solo se quello vecchio è crashato. <b>Ω</b> (con ◇P): prima o poi tutti i corretti si fidano dello stesso processo corretto. Entrambi si fanno con <i>maxrank</i> dei non sospettati.
- <b>Modelli</b>: fail-stop (P) ⇒ fail-noisy (◇P) ⇒ fail-silent. I problemi risolvibili vanno al contrario. Il sincrono è più forte del fail-stop.
- <b>Lamport ME tollerante ai crash</b>: con P si ignorano i crashati, ma bisogna anche <b>scartare le REQ dei crashati che arrivano in ritardo</b>. In alternativa: un leader coordinatore, con una fase new_leader quando il leader cambia.
