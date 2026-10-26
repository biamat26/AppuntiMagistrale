# Lezione 2 – Modelli, astrazioni e link

## Di cosa parliamo

Un <b>sistema distribuito</b> è un insieme di computer (li chiameremo <b>processi</b>) che collaborano scambiandosi messaggi su una rete. Nessuno vede lo stato degli altri: ognuno sa solo cosa ha in memoria e quali messaggi ha ricevuto.

Il corso lavora su <b>modelli</b>: descrizioni matematiche semplificate del sistema, precise abbastanza da poter <b>dimostrare</b> che un algoritmo funziona. Questa lezione costruisce il modello di base (processi, esecuzioni, guasti), spiega come si scrivono le specifiche (safety e liveness) e chiude con i primi algoritmi: come costruire canali di comunicazione affidabili partendo da una rete inaffidabile.

## 1. Il sistema e i processi

### Il sistema

!!! abstract "In breve"

    Abbiamo $n$ processi, ognuno con un nome diverso, collegati da canali su cui si mandano messaggi.

- $\Pi = \{p_0, \dots, p_{n-1}\}$: l'insieme degli $n$ processi, con <b>identità distinte</b> (ognuno sa chi è e conosce i nomi degli altri).
- I processi sono collegati da un <b>grafo di comunicazione</b> $G$: i nodi sono i processi, gli archi sono i <b>link</b> (canali). Di solito $G$ è <b>completo</b>: tutti possono parlare direttamente con tutti.

### Il processo

!!! abstract "In breve"

    Un processo è una macchina a stati. Ha una memoria interna, una "casella di posta" in entrata e una in uscita, e ad ogni passo legge la posta, aggiorna la memoria e magari spedisce messaggi.

Formalmente un processo è un <b>automa</b> (I/O automaton, anche con infiniti stati):

- $Q$: insieme degli stati interni; $Q_{in} \subseteq Q$: stati iniziali possibili.
- $M$: insieme dei messaggi, nella forma $\langle \text{mittente}, \text{destinatario}, \text{payload} \rangle$.
- $\text{InBuf}_j$: messaggi <b>arrivati</b> a $p_j$ e non ancora letti. Vengono consumati al prossimo passo locale.
- $\text{OutBuf}_j$: messaggi <b>spediti</b> da $p_j$ ma non ancora consegnati ("in volo" sulla rete).

I buffer sono <b>multinsiemi</b>: lo stesso messaggio può comparire più volte e non c'è un ordine.

Lo <b>stato</b> completo di $p_j$ è la terna $(q_j, \text{InBuf}_j, \text{OutBuf}_j)$.

## 2. Esecuzioni asincrone

### Lo scheduler (avversario)

!!! abstract "In breve"

    Chi decide "cosa succede adesso" non è nessun processo, ma un avversario immaginario. Gli algoritmi devono funzionare <b>qualunque</b> cosa scelga.

Il sistema avanza un evento alla volta, e ogni volta un <b>avversario</b> (lo <i>scheduler</i>) sceglie quale evento far succedere. Gli eventi possibili sono due:

- $\text{Del}(i, j, m)$ (<i>delivery</i>): la rete consegna $m$, cioè lo sposta da $\text{OutBuf}_i$ a $\text{InBuf}_j$.
- $\text{Exec}(i)$: $p_i$ fa <b>un passo</b> del suo automa: legge l'InBuf, cambia stato, eventualmente mette nuovi messaggi nell'OutBuf.

Pensare a uno scheduler cattivo serve a modellare il fatto che nella realtà non controlliamo i tempi: la rete può essere lenta, un processo può essere rallentato, ecc. Se l'algoritmo resiste al peggior scheduler, resiste a tutto.

### Configurazione, eventi abilitati, esecuzione

- <b>Configurazione</b> $C_t$: la "fotografia" del sistema al tempo $t$, cioè il vettore degli stati di tutti i processi: $C_t[j] = (q_j, \text{InBuf}_j, \text{OutBuf}_j)$.
- Un evento è <b>abilitato</b> in $C$ se può accadere in quella configurazione. $\text{Exec}(i)$ è sempre abilitato; $\text{Del}(i,j,m)$ è abilitato solo se $m$ si trova davvero in $\text{OutBuf}_i$ (non puoi consegnare un messaggio mai spedito).
- <b>Esecuzione</b>: sequenza <b>infinita</b> che alterna configurazioni ed eventi

$$
E = (C_0, e_0, C_1, e_1, C_2, e_2, \dots)
$$

dove ogni $e_t$ è abilitato in $C_t$ e $C_{t+1}$ è il risultato di applicare $e_t$ a $C_t$.

<b>Esempio</b>: $C_0 \xrightarrow{\text{Exec}(1)} C_1 \xrightarrow{\text{Del}(1,2,m')} C_2 \xrightarrow{\text{Exec}(2)} C_3 \dots$ significa: $p_1$ fa un passo e spedisce $m'$; la rete consegna $m'$ a $p_2$; $p_2$ fa un passo e lo legge.

<b>Asincrono</b> vuol dire che non c'è nessun limite di tempo: tra un evento e l'altro dello stesso processo, o tra l'invio e la consegna di un messaggio, possono passare quanti eventi si vuole.

### Esecuzione fair

!!! abstract "In breve"

    Un'esecuzione è fair (equa) se lo scheduler non "dimentica" nessuno per sempre: ogni processo prima o poi avanza, e ogni messaggio prima o poi arriva.

Un'esecuzione $E$ è <b>fair</b> se:

1. ogni processo esegue <b>infiniti</b> passi locali, e
2. ogni messaggio spedito viene <b>prima o poi</b> consegnato da un evento $\text{Del}$.

<b>Perché serve?</b> Senza fairness lo scheduler potrebbe scegliere sempre e solo $\text{Exec}(1)$: $p_2$ non farebbe mai niente e i messaggi non arriverebbero mai. Nessun algoritmo potrebbe garantire che qualcosa "prima o poi succede". La fairness è l'ipotesi minima per poter parlare di progresso.

<b>Fairness con i guasti.</b> La definizione sopra è pensata per un sistema <b>senza guasti</b>. Con i crash non funziona: un processo crashato non viene più schedulato, quindi non fa infiniti passi e l'esecuzione non sarebbe mai fair. Per questo, con i guasti, la definizione si restringe ai processi corretti. Un'esecuzione è fair se:

1. ogni processo <b>corretto</b> esegue infiniti passi locali, e
2. ogni messaggio spedito <b>da</b> un processo corretto <b>a</b> un processo corretto viene prima o poi consegnato.

## 3. Esecuzione locale e indistinguibilità

### Esecuzione locale (local view)

!!! abstract "In breve"

    È quello che un singolo processo "vede" dell'esecuzione: solo gli eventi che lo riguardano, nell'ordine in cui sono avvenuti.

$E|p_j$ è la sottosequenza degli eventi di $E$ che toccano $p_j$ (i suoi passi e le consegne di messaggi a lui), nell'ordine originale.

### Indistinguibilità

!!! abstract "In breve"

    Due esecuzioni diverse possono sembrare identiche a ogni processo. Se succede, nessun processo può capire in quale delle due si trova.

Esempio con 4 processi:

$$
E = (C_0,\ \text{Exec}(0),\ C_1,\ \text{Del}(0,1,m),\ C_2,\ \text{Exec}(3),\ C_3,\ \text{Del}(3,2,m'),\ \dots)
$$

$$
E' = (C_0,\ \text{Exec}(3),\ C'_1,\ \text{Del}(3,2,m'),\ C'_2,\ \text{Exec}(0),\ C'_3,\ \text{Del}(0,1,m),\ \dots)
$$

In $E$ prima comunicano $p_0 \to p_1$, poi $p_3 \to p_2$; in $E'$ al contrario. Ma le due coppie non interagiscono, quindi ogni processo vede esattamente la stessa storia: $E|p_j = E'|p_j$ per ogni $p_j$. Diciamo che $E$ ed $E'$ sono <b>indistinguibili</b>.

<b>Teorema</b>: in un sistema asincrono è impossibile ricostruire l'esecuzione esatta.

In parole: nessun processo sa davvero "in che ordine sono successe le cose" nel sistema globale. Questa idea (un processo non distingue due mondi diversi) è lo strumento principale per dimostrare che certi problemi sono <b>impossibili</b>.

## 4. Sincrono vs asincrono

Nel corso vedremo tre modelli di tempo:

- <b>Asincrono</b>: nessun limite sui tempi (quello visto sopra).
- <b>Eventualmente sincrono</b>: asincrono per un po', poi da un certo momento (ignoto) diventa sincrono. Si vedrà nel modulo M2.
- <b>Sincrono</b>: esistono limiti <b>fissi e noti</b> su (i) quanto ci mette un messaggio ad arrivare, (ii) quanto dura un'azione di un processo, (iii) quanto tempo passa tra due azioni.

Nel sincrono si può dire "se non ricevo risposta entro 5 secondi, l'altro è morto". Nell'asincrono no: un processo lento e uno guasto sono indistinguibili.

## 5. Guasti dei processi

### Crash-stop e bizantino

!!! abstract "In breve"

    Un processo si può rompere in due modi. <b>Crash</b>: si spegne e non fa più nulla. <b>Bizantino</b>: impazzisce o diventa malevolo e fa qualunque cosa, anche mentire.

- $\text{Crash}(p_j)$: da quel momento $p_j$ non esegue più passi (niente più $\text{Exec}(j)$). Semplicemente si ferma.
- $\text{Byz}(p_j)$: da quel momento $p_j$ si comporta in modo <b>arbitrario</b>: quando fa un passo non segue più il suo automa. Può mandare messaggi falsi, messaggi diversi a processi diversi, tacere, ecc. È il modello giusto per un attaccante che ha preso il controllo di una macchina.

I guasti bizantini <b>contengono</b> i crash: fermarsi è uno dei possibili comportamenti arbitrari. Quindi un algoritmo che tollera i bizantini tollera anche i crash, non viceversa.

### Processi corretti e il parametro f

- Un processo è <b>corretto</b> se non subisce mai guasti. Attenzione: durante l'esecuzione <b>nessuno sa</b> chi è corretto.
- $f$ = numero massimo di processi che possono guastarsi in un'esecuzione. Di solito lo si limita, ad esempio $f \le n-1$ (almeno uno sopravvive).
- Non si fanno <b>mai</b> ipotesi su <b>quando</b> avviene un guasto: può capitare in qualunque momento, anche a metà algoritmo.

## 6. Astrazioni e specifiche

### Come si costruisce un'astrazione distribuita

!!! abstract "In breve"

    Un'astrazione è un "oggetto" con un comportamento promesso (es. "un canale che non perde messaggi"). Prima si scrive cosa promette, poi si costruisce, poi si dimostra che mantiene la promessa.

Il metodo del corso in 4 passi:

1. Definire il <b>modello</b> del sistema (processi, tempi, guasti).
2. Definire il problema come <b>astrazione</b>: un'interfaccia più un elenco di <b>proprietà</b> scritte senza ambiguità.
3. <b>Implementare</b> l'astrazione con un protocollo distribuito.
4. <b>Dimostrare</b> che il protocollo soddisfa tutte le proprietà.

Ogni astrazione comunica con chi la usa tramite <b>eventi</b>:

- <b>Request</b>: chiamate dall'alto verso l'astrazione (es. $\langle \text{Send} \mid q, m \rangle$: "spedisci $m$ a $q$").
- <b>Indication</b>: notifiche dall'astrazione verso l'alto (es. $\langle \text{Deliver} \mid p, m \rangle$: "ti è arrivato $m$ da $p$").

### Safety e liveness

!!! abstract "In breve"

    Ogni proprietà è di uno di due tipi. <b>Safety</b>: "non succede mai niente di male". <b>Liveness</b>: "prima o poi succede qualcosa di buono".

<b>Safety</b>

- Informale: <i>qualcosa di cattivo non succede mai</i>.
- Se viene violata al tempo $t$, resta violata per sempre: non si può più rimediare.
- Formale: se $E$ viola la proprietà, esiste un <b>prefisso finito</b> $E'$ di $E$ tale che <b>ogni</b> estensione di $E'$ la viola.

<b>Liveness</b>

- Informale: <i>qualcosa di buono prima o poi succede</i>.
- Non può essere violata in tempo finito: c'è sempre speranza.
- Formale: ogni esecuzione <b>finita</b> che non la soddisfa si può <b>estendere</b> in una che la soddisfa.

<b>Trucco pratico</b> per classificarle: chiediti "posso indicare il momento esatto in cui la proprietà è stata rotta?". Se sì, è safety. Se la violazione si vede solo "all'infinito" (aspetti per sempre e non succede), è liveness.

<b>Esempi</b>

- <i>Mutua esclusione</i>: se $p$ ha la risorsa $r$ al tempo $t$, nessun altro ce l'ha al tempo $t$. → <b>safety</b> (il momento in cui due la tengono insieme è la violazione).
- <i>No-deadlock</i>: se $r$ è libera, prima o poi qualcuno la ottiene. → <b>liveness</b>.
- <i>No-starvation</i>: se $p$ chiede $r$, prima o poi la ottiene. → <b>liveness</b>.
- <i>"Al massimo 7 consegne"</i>: ogni messaggio viene consegnato al più 7 volte. → <b>safety</b>: all'ottava consegna è violata e nessuna estensione rimedia.

### Proprietà scritte male

Una buona specifica separa safety e liveness in proprietà distinte. Esempio scritto male:

!!! note ""

    "Se $p$ manda $m$ a $q$, allora $q$ prima o poi lo consegna e la consegna è unica."

Mescola due cose. Meglio:

- (liveness) Se $p$ manda $m$ a $q$, $q$ prima o poi consegna $m$.
- (safety) Se $p$ manda $m$ a $q$, $m$ è consegnato al più una volta.

## 7. I link: dalla rete inaffidabile al canale perfetto

L'obiettivo: partire da una rete realistica (che perde e duplica messaggi) e costruire, strato sopra strato, canali sempre più affidabili.

```text
FIFO perfect link      ← consegna tutto, una volta, in ordine
       ▲
Perfect link (pl)       ← consegna tutto, una volta
       ▲
Stubborn link (sl)      ← consegna tutto, infinite volte
       ▲
Fair-loss link (fll)    ← la rete reale
```

### Fair-loss link

!!! abstract "In breve"

    È il modello della rete vera. Può perdere messaggi, ma se insisti a rimandare lo stesso messaggio, prima o poi passa. Può duplicare, ma solo un numero finito di volte. Non inventa messaggi.

<b>Prima di tutto: cos'è un link come astrazione.</b> Pensalo come una scatola nera tra due processi, con un ingresso e un'uscita:

```text
  p                                             q
  │  ⟨Send | q, m⟩                ⟨Deliver | p, m⟩  ▲
  ▼                                                 │
┌───────────────────── LINK ──────────────────────┐
│  qui dentro la rete può perdere o copiare m      │
└─────────────────────────────────────────────────┘
```

- <b>Send</b> è la richiesta del mittente: "prova a far arrivare $m$ a $q$".
- <b>Deliver</b> è l'evento lato destinatario: "il link ti consegna $m$, arrivato da $p$".

Un Send <b>non garantisce</b> un Deliver. Tutte le proprietà del link sono regole su che rapporto c'è tra i Send fatti da una parte e i Deliver che escono dall'altra.

<b>Perché proprio questo modello.</b> È la rete reale vista dal basso (tipo UDP): i pacchetti si perdono (congestione, buffer pieni), a volte arrivano doppi (un router o un livello sotto ritrasmette), ma la rete non si inventa pacchetti dal nulla. L'analogia è un <b>postino distratto</b>: certe lettere le perde, certe le consegna due volte, ma non scrive lettere di suo pugno. E se continui a spedire la stessa lettera, prima o poi qualcuna arriva.

Proprietà, una per una:

<b>FL1 (Fair-loss)</b>: se un processo corretto $p$ manda $m$ <b>infinite volte</b> a un processo corretto $q$, allora $q$ consegna $m$ infinite volte.

- Dice cosa <b>non</b> può fare la rete: perdere <i>per sempre</i> un messaggio che continui a rispedire. Può perdere molte copie, ma non tutte.
- La formulazione con "infinite volte" sembra strana, ma è l'unica onesta: la rete non promette nulla su <b>un singolo</b> invio (ogni copia può andare persa). Se ogni copia si perde con probabilità $pr < 1$, insistendo all'infinito ne passano infinite.
- Perché "corretti"? Se $p$ crasha smette di rispedire; se $q$ crasha non consegna più nulla. La promessa vale solo se entrambi restano vivi.
- Tipo: <b>liveness</b> (promette che qualcosa di buono, le consegne, continuerà ad accadere).

<b>FL2 (Finite duplication)</b>: se $p$ manda $m$ un numero <b>finito</b> di volte, $q$ non può consegnarlo infinite volte.

- La rete può creare copie, ma un numero limitato: se mandi $m$ 3 volte, magari ne arrivano 5, ma non infinite.
- Senza FL2 la rete potrebbe "spammare" $q$ all'infinito con una sola spedizione, e soprattutto potrebbe far sembrare che $p$ stia ritrasmettendo quando invece si è fermato.
- Tipo: <b>liveness</b>, ed è il caso furbo. Dato un pezzo finito di esecuzione con, diciamo, 1000 consegne di $m$, non hai violato niente: 1000 è finito, e l'esecuzione si può sempre continuare senza altre consegne. La violazione ("infinite consegne") si vede solo all'infinito, quindi per definizione non è safety.

<b>FL3 (No creation)</b>: se $q$ consegna $m$ con mittente $p$, allora $p$ ha davvero spedito $m$ a $q$.

- La rete non inventa messaggi, non li modifica e non cambia il mittente.
- Tipo: <b>safety</b>. Se $q$ consegna un messaggio mai spedito, c'è un istante preciso in cui è successo, e da lì la proprietà è rotta per sempre.

<b>Esempio.</b> $p$ manda $m$ tre volte e poi si ferma.

- Consentito: nessuna consegna (tutte perse); 1 consegna; 4 consegne (una copia duplicata).
- Vietato: infinite consegne (viola FL2); una consegna di $m'$ che $p$ non ha mai mandato (viola FL3).

Se invece $p$ continua a mandare $m$ per sempre, "zero consegne" diventa vietato (viola FL1).

<b>Cosa il fair-loss NON garantisce</b>: che un singolo invio arrivi, che non ci siano duplicati, l'ordine di arrivo, i tempi. Il resto della lezione serve a costruire queste garanzie sopra il fair-loss: lo <b>stubborn</b> sfrutta FL1 rispedendo per sempre, il <b>perfect</b> elimina i duplicati, il <b>FIFO</b> sistema l'ordine.

### Come si scrivono gli algoritmi

Lo pseudocodice del corso è <b>a eventi</b>: un algoritmo è un insieme di <b>handler</b> del tipo <code>upon event ⟨...⟩ do ...</code>. Ogni handler reagisce a un evento (una richiesta dall'alto, una consegna dal basso, un timer) e può generare nuovi eventi con <code>trigger</code>.

Gli handler sono <b>atomici</b>: un handler, una volta iniziato, finisce senza essere interrotto (tranne da un crash). Questo è importante nelle dimostrazioni.

### Stubborn link

!!! abstract "In breve"

    Un canale "testardo": tutto quello che mandi arriva, anzi arriva infinite volte. Si ottiene rimandando ogni messaggio per sempre.

Proprietà:

- <b>SL1 (Stubborn delivery)</b>: se un processo corretto $p$ manda $m$ a un processo corretto $q$, $q$ consegna $m$ infinite volte.
- <b>FL3 (No creation)</b>: come sopra.

Algoritmo <i>Retransmit Forever</i> (usa un fair-loss link <code>fll</code>):

```text
upon event ⟨sl, Init⟩ do
    sent := ∅
    starttimer(Δ)

upon event ⟨Timeout⟩ do            // ogni Δ: rimanda tutto
    forall (q, m) ∈ sent do
        trigger ⟨fll, Send | q, m⟩
    starttimer(Δ)

upon event ⟨sl, Send | q, m⟩ do
    trigger ⟨fll, Send | q, m⟩
    sent := sent ∪ {(q, m)}

upon event ⟨fll, Deliver | p, m⟩ do
    trigger ⟨sl, Deliver | p, m⟩
```

<b>Perché funziona</b>

- <i>No creation</i>: lo stubborn consegna un messaggio solo quando il fair-loss sotto lo consegna. Se consegnasse un messaggio mai spedito, l'avrebbe inventato il fair-loss, che però per FL3 non lo fa.
- <i>Stubborn delivery</i>: $m$ resta in <code>sent</code> per sempre, quindi il timer lo rimanda <b>infinite volte</b>. Per FL1 il fair-loss lo consegna infinite volte, e ogni consegna del fair-loss diventa una consegna dello stubborn.

### Perfect link

!!! abstract "In breve"

    Il canale che vorremmo sempre: ogni messaggio arriva, arriva <b>una volta sola</b>, e non ne arrivano di inventati. Si ottiene dallo stubborn buttando via i duplicati.

Proprietà:

- <b>PL1 (Reliable delivery)</b>: se $p$ corretto manda $m$ a $q$ corretto, $q$ prima o poi consegna $m$. → liveness
- <b>PL2 (No duplication)</b>: ogni messaggio è consegnato al più una volta. → safety
- <b>FL3 (No creation)</b>. → safety

Algoritmo <i>Eliminate Duplicates</i> (usa uno stubborn link <code>sl</code>):

```text
upon event ⟨pl, Init⟩ do
    delivered := ∅

upon event ⟨pl, Send | q, m⟩ do
    trigger ⟨sl, Send | q, m⟩

upon event ⟨sl, Deliver | p, m⟩ do
    if m ∉ delivered then           // filtro anti-duplicati
        delivered := delivered ∪ {m}
        trigger ⟨pl, Deliver | p, m⟩
```

<b>Perché funziona</b>

- <i>No creation</i>: come prima, si eredita dallo stubborn.
- <i>No duplication</i>: supponiamo $m$ consegnato due volte, ai tempi $t < t'$. Al tempo $t$ l'handler (atomico) aggiunge $m$ a <code>delivered</code>. Al tempo $t'$ quindi $m \in$ <code>delivered</code> e l'<code>if</code> blocca la consegna. Contraddizione.
- <i>Reliable delivery</i>: lo stubborn consegna $m$ (anzi infinite volte). La prima volta $m$ non è in <code>delivered</code>, quindi viene consegnato.

<b>Attenzione (correzione nelle slide)</b>: una prima versione di PL1 diceva solo "se $p$ corretto manda $m$ a $q$, $q$ consegna $m$". Con i crash è sbagliata: se $q$ crasha non può consegnare niente. Serve che <b>anche</b> $q$ <b>sia corretto</b>. In generale, nelle proprietà di liveness bisogna sempre dire chi deve essere corretto.

### FIFO perfect link

!!! abstract "In breve"

    Un perfect link che in più rispetta l'ordine: i messaggi arrivano nello stesso ordine in cui sono stati spediti.

Proprietà: PL1, PL2, FL3 e in più

- <b>FIFO</b>: se $q$ consegna $m$ prima di $m'$ (entrambi da $p$), allora $p$ ha spedito $m$ prima di $m'$.

<b>Idea</b>: numerare i messaggi. Il mittente attacca a ogni messaggio un numero di sequenza crescente; il destinatario tiene da parte i messaggi arrivati "in anticipo" e li consegna solo quando arriva quello col numero atteso.

```text
upon event ⟨fpl, Init⟩ do
    pending := ∅
    forall q ∈ Π do
        seq[q]  := 0      // ultimo numero usato verso q
        next[q] := 1      // prossimo numero atteso da q

upon event ⟨fpl, Send | q, m⟩ do
    seq[q] := seq[q] + 1
    trigger ⟨pl, Send | q, [seq[q], m]⟩

upon event ⟨pl, Deliver | s, [k, m]⟩ do
    pending := pending ∪ {(s, k, m)}

upon exists (s, k, m) ∈ pending such that k = next[s] do
    pending := pending \ {(s, k, m)}
    next[s] := next[s] + 1
    trigger ⟨fpl, Deliver | s, m⟩
```

<b>Perché funziona</b>: PL1, PL2, FL3 vengono direttamente dal perfect link sotto. Per FIFO: <code>next[s]</code> cresce di 1 a ogni consegna, quindi i messaggi di $s$ vengono consegnati esattamente nell'ordine 1, 2, 3, ... dei loro numeri, che è l'ordine di invio. Se $m'$ (numero più alto) venisse consegnato prima di $m$, <code>next</code> avrebbe dovuto già passare per il numero di $m$, cioè $m$ sarebbe già stato consegnato. Contraddizione.

Nota: i numeri di sequenza risolvono anche un altro problema, cioè due messaggi con lo <b>stesso contenuto</b> (vedi l'esercizio del contatore sotto).

## 8. Esercizi e homework

??? note "Homework: safety o liveness? (soluzione proposta, non nelle slide)"

    - <b>Fairness di un'esecuzione</b> → liveness: qualunque prefisso finito si può estendere in un'esecuzione fair, non si può mai dire "ormai è rotta".
    - <b>Al più f guasti</b> → safety: al momento del guasto numero $f+1$ la proprietà è violata per sempre.
    - <b>Eventual recovery</b> (chi crasha prima o poi riparte) → liveness.
    - <b>Time-bounded recovery</b> (se c'è un recovery, avviene entro $k$ eventi dal guasto) → safety: un recovery arrivato dopo più di $k$ eventi è una violazione visibile in un prefisso finito.
    - <b>Time-bounded implica eventual?</b> No. Così come è scritta, se il processo crasha e <b>non</b> riparte mai, time-bounded è soddisfatta "a vuoto" (non c'è nessun recovery da controllare), mentre eventual è violata.
    - <b>Riscrivere la proprietà sugli insiemi</b>: separare in (liveness) "se un processo corretto produce un output, prima o poi ogni processo corretto produce un output" e (safety) "per due output qualunque $O_z, O_t$ vale $O_z \subseteq O_t$ oppure $O_t \subseteq O_z$".

??? note "Homework 1: stubborn senza 'corretto' (soluzione nelle slide)"

    Se SL1 dice solo "se $p$ manda $m$ a $q$, $q$ lo consegna infinite volte", senza richiedere che $p$ sia corretto, l'algoritmo non funziona. Se $p$ crasha smette di ritrasmettere, quindi manda $m$ sul fair-loss solo un numero finito di volte, e il fair-loss può perderle tutte. Lo stesso argomento mostra che <b>nessun</b> algoritmo sopra un fair-loss può soddisfare quella proprietà.

    <b>Domanda (\*)</b>: con memoria limitata a $k$ messaggi si può fare un perfect link sopra un fair-loss? <i>Idea (proposta, da verificare a lezione)</i>: sembra di no. Per non consegnare duplicati il destinatario deve ricordare quali messaggi ha già consegnato, e una copia vecchia può arrivare in ritardo arbitrario. Con memoria limitata prima o poi deve "dimenticare" qualcosa e non riesce più a riconoscere un duplicato.

??? note "Homework 2: l'algoritmo di Caio senza timer (soluzione nelle slide)"

    Caio propone uno stubborn senza timer: a ogni nuova richiesta di invio rimanda <b>tutti</b> i messaggi accumulati in <code>set</code>.

    ```text
    upon event ⟨sl, Send | m, q⟩ do
        set := set ∪ {(m, q)}
        forall (x, y) ∈ set do
            trigger ⟨fll, Send | x, y⟩

    upon event ⟨fll, Deliver | m, q⟩ do
        trigger ⟨sl, Deliver | m, q⟩
    ```

    <b>Cosa non va</b>: i messaggi vengono rimandati solo quando arriva una nuova richiesta di invio. Se $p$ manda $m$ e poi non manda più niente, $m$ va sul fair-loss una volta sola e può andare perso.

    <b>Quando funziona</b>: solo nelle esecuzioni in cui $p$ continua a mandare infiniti messaggi.

    <b>Perché è impossibile senza timer</b>: per garantire la consegna bisogna mandare $m$ sul fair-loss infinite volte. Senza timer (o ciclo infinito, che è la stessa cosa) e senza infiniti input dall'esterno, dopo un certo numero di passi $p$ non cambia più stato e non fa più nulla. Quindi esiste un'esecuzione in cui $m$ viene mandato un numero finito di volte, e il fair-loss può perderle tutte.

??? note "Esercizio: il server contatore (soluzione nelle slide + commento mio)"

    <b>Testo</b>: un server ha una variabile $v = 0$ e accetta INC, DEC e GET (risponde con $v$). Comunica col client tramite il perfect link visto sopra. Il client manda INC, INC, GET e riceve <b>1</b> invece di 2. Rimanda GET e non riceve più risposta. Perché?

    <b>Spiegazione 1: ordine.</b> Il perfect link non garantisce l'ordine: il server può ricevere INC, GET, INC e rispondere 1.

    <b>Spiegazione 2: duplicati.</b> Anche se l'ordine è giusto: il filtro <code>if m ∉ delivered</code> guarda il <b>contenuto</b> del messaggio. Il secondo INC è identico al primo, quindi viene scartato come duplicato, e $v$ vale 1. Il secondo GET è identico al primo, quindi viene scartato anche lui: ecco perché non arriva più nessuna risposta. (L'indizio "quanto aspetteresti?" punta a questo: nell'asincrono non puoi distinguere un messaggio lento da uno buttato via.)

    <b>Soluzione</b>: dare a ogni messaggio un <b>identificatore unico</b> (es. numero di sequenza), così due INC sono messaggi diversi; per l'ordine usare il FIFO link, che fa entrambe le cose.

## Riepilogo

- <b>Modello</b>: $n$ processi = automi con InBuf/OutBuf, collegati da link; uno <b>scheduler avversario</b> sceglie gli eventi $\text{Exec}(i)$ e $\text{Del}(i,j,m)$.
- <b>Esecuzione</b> = sequenza infinita configurazione/evento; <b>fair</b> = ogni processo avanza infinite volte e ogni messaggio arriva.
- <b>Indistinguibilità</b>: esecuzioni diverse possono sembrare uguali a tutti i processi → in asincrono non si ricostruisce l'esecuzione esatta.
- <b>Tempo</b>: asincrono / eventualmente sincrono / sincrono.
- <b>Guasti</b>: crash-stop (si ferma) ⊂ bizantino (fa di tutto); al più $f$ guasti, in momenti imprevedibili.
- <b>Safety</b> = niente di male, violazione visibile in tempo finito; <b>liveness</b> = prima o poi qualcosa di buono, mai violabile in tempo finito.
- <b>Link</b>: fair-loss → (ritrasmetti per sempre) → stubborn → (scarta duplicati) → perfect → (numeri di sequenza) → FIFO perfect.
