# Lezione 3 – Il tempo nei sistemi distribuiti (I)

## Di cosa parliamo

In un sistema distribuito non esiste un orologio comune: ogni macchina ha il suo, e gli orologi non vanno tutti alla stessa velocità. Questa lezione affronta due domande:

1. <b>Che ipotesi facciamo sul tempo?</b> Si introduce un terzo modello, quello <i>eventualmente sincrono</i>, a metà tra asincrono e sincrono.
2. <b>Come si tengono allineati gli orologi fisici?</b> Si vedono i problemi degli orologi reali e tre soluzioni: l'algoritmo di Cristian, quello di Berkeley e NTP. Alla fine si vede il loro limite: per quanto bene li sincronizzi, non bastano a ordinare con certezza tutti gli eventi.

Asincrono e sincrono sono già definiti nella [Lezione 2](lezione-2.md); qui c'è solo quello che si aggiunge.

## 1. Il modello eventualmente sincrono

### Perché serve un terzo modello

!!! abstract "In breve"

    L'asincrono è troppo pessimista (troppe cose diventano impossibili), il sincrono troppo ottimista (le reti vere non lo rispettano sempre). L'eventualmente sincrono descrive le reti reali: quasi sempre puntuali, ma con ritardi imprevisti ogni tanto.

Confronto veloce:

|  | Asincrono | Sincrono |
| --- | --- | --- |
| Ritardi dei messaggi | Nessun limite | Limite noto $\delta$: spedito al tempo $t$, arriva entro $t + \delta$ |
| Orologi | Solo locali, utili per ordinare gli eventi dello stesso processo | Sincronizzabili (con una certa precisione) |
| Passi dei processi | Avvengono quando decide lo scheduler | A intervalli prestabiliti e di durata limitata |
| Pro | Descrive qualunque rete | Quasi tutto è risolvibile |
| Contro | Molti problemi sono impossibili (es. mettersi d'accordo, il <i>consenso</i>) | Descrive solo reti molto controllate |

L'esempio del prof è un <code>ping google.com</code>: le risposte arrivano tutte in circa 40 ms, poi all'improvviso una ci mette 739 ms, poi si torna a 40. La rete è "sincrona quasi sempre", con brevi periodi asincroni.

### Definizione

!!! abstract "In breve"

    All'inizio il sistema può comportarsi in modo asincrono, ma da un certo istante in poi diventa sincrono per sempre. Quell'istante esiste, ma nessuno sa quando sia.

- Il sistema è inizialmente <b>asincrono</b>.
- Esiste un tempo $T$, <b>sconosciuto</b>, dopo il quale il sistema è <b>sincrono per sempre</b>.

Perché "per sempre" se le reti vere alternano fasi buone e cattive? È una semplificazione: nella pratica basta che il periodo sincrono duri <b>abbastanza</b> perché l'algoritmo finisca. Dire "per sempre" rende le dimostrazioni più semplici.

<b>Come si usa con safety e liveness</b> (collegamento con la Lezione 2):

- La <b>safety</b> (es. mutua esclusione) deve valere <b>sempre</b>, anche nei periodi asincroni: non puoi permettere che due processi entrino insieme in sezione critica solo perché la rete è lenta.
- La <b>liveness</b> (es. no-starvation) può contare sui periodi sincroni: "prima o poi" il sistema diventa puntuale e allora il progresso arriva.

### Relazione tra i tre modelli

Attenzione, ci sono due inclusioni che vanno in <b>versi opposti</b>:

- <b>Esecuzioni possibili</b>: Sincrono $\subset$ Eventualmente sincrono $\subset$ Asincrono. Ogni esecuzione sincrona è anche eventualmente sincrona (con $T = 0$), e ogni esecuzione eventualmente sincrona è anche asincrona.
- <b>Problemi risolvibili</b>: Asincrono $\subset$ Eventualmente sincrono $\subset$ Sincrono.

Il motivo: più esecuzioni il modello ammette, più scenari cattivi l'algoritmo deve sopportare, quindi meno problemi si riescono a risolvere. L'asincrono ammette di tutto ed è il più difficile; il sincrono ammette poco ed è il più facile.

## 2. Perché il tempo è importante

Molte applicazioni hanno bisogno di <b>ordinare gli eventi</b>: controllo del traffico aereo, ordini di acquisto e vendita in borsa, monitoraggio di rete. Esempi di algoritmi che dipendono dal tempo:

- <b>consistenza dei dati</b> (quale scrittura è l'ultima?);
- <b>autenticazione</b> (certificati e ticket hanno una scadenza);
- <b>evitare lavoro doppio</b>: <code>make</code> decide se ricompilare un file confrontando gli orari di modifica;
- <b>reti di sensori con TDMA</b>: ogni sensore trasmette solo nel suo intervallo di tempo, quindi tutti devono essere d'accordo sull'ora.

Nella Lezione 2 abbiamo visto che in asincrono due esecuzioni diverse possono essere indistinguibili. Se ogni processo potesse attaccare a ogni evento l'ora esatta (<b>timestamp</b>), potremmo ricostruire la storia globale.

<b>Soluzione ingenua</b>: ogni processo mette sugli eventi l'ora del proprio orologio fisico. Funziona solo se gli orologi sono d'accordo tra loro, e il resto della lezione mostra quanto è difficile.

## 3. Orologi fisici

### Come funziona l'orologio di un computer

!!! abstract "In breve"

    Dentro il computer c'è un cristallo di quarzo che oscilla e un contatore che conta le oscillazioni. Il sistema operativo trasforma il contatore in un'ora leggibile.

- <b>Orologio hardware</b> $H_i(t)$: un oscillatore più un registro che si incrementa a ogni oscillazione (<i>tick</i>).
- <b>Orologio software</b> (quello che usano i programmi): il sistema operativo lo calcola dall'hardware come

$$
C_i(t) = \alpha H_i(t) + \beta
$$

I parametri $\alpha$ (velocità) e $\beta$ (spostamento) servono a correggere l'orologio.

### Skew e drift

!!! abstract "In breve"

    Lo <b>skew</b> è quanto due orologi segnano ore diverse in un certo istante. Il <b>drift</b> è quanto un orologio va più veloce o più lento del tempo vero. Il drift fa crescere lo skew col passare del tempo.

- <b>Skew</b> tra due orologi: $\text{Skew}_{i,j}(t) = |C_i(t) - C_j(t)|$.
- <b>Drift rate</b>: di quanto l'orologio sbaglia per ogni secondo reale. Si guarda la velocità $dH/dt$:
    - $dH/dt = 1$: orologio perfetto;
    - $dH/dt > 1$: orologio veloce;
    - $dH/dt < 1$: orologio lento.

Numeri utili:

- un drift di 2 μs/s significa che per ogni secondo reale l'orologio avanza di 1 s + 2 μs;
- un quarzo normale ha drift circa $10^{-5}$ s/s, cioè sbaglia di circa 1 secondo ogni 11-12 giorni;
- un quarzo di alta precisione arriva a $10^{-7}$–$10^{-8}$ s/s.

Il drift non è costante: dipende anche dalla temperatura del cristallo.

### Orologio corretto

Un orologio hardware è <b>corretto</b> se il suo drift resta entro un limite noto $\rho > 0$ (es. $10^{-5}$):

$$
1 - \rho \le \frac{dH}{dt} \le 1 + \rho
$$

Con un orologio corretto si possono misurare intervalli di tempo commettendo un errore limitato.

### Ogni quanto risincronizzare

!!! abstract "In breve"

    Anche partendo perfettamente allineati, due orologi si allontanano. Se so quanto velocemente si allontanano, so ogni quanto devo risincronizzarli per restare entro una tolleranza.

Caso peggiore: due orologi partono allineati al tempo 0, uno va veloce al massimo ($1+\rho$), l'altro lento al massimo ($1-\rho$). Dopo un tempo $t$:

$$
|C_1(t) - C_2(t)| = (1+\rho)t - (1-\rho)t = 2\rho t
$$

Se voglio che lo skew non superi mai $\Delta$, devo risincronizzarli almeno ogni

$$
t = \frac{\Delta}{2\rho}
$$

Esempio: $\rho = 10^{-5}$ e tolleranza $\Delta = 1$ ms. Allora $t = 10^{-3} / (2 \cdot 10^{-5}) = 50$ s: bisogna risincronizzare ogni 50 secondi.

Al momento della risincronizzazione l'orologio veloce è avanti di $\Delta/2$ e quello lento indietro di $\Delta/2$; la correzione riporta l'orologio veloce indietro di $\Delta$ per allinearlo all'altro. Ma "riportare indietro" va fatto con attenzione, come spiega la sezione seguente.

### Monotonia: l'orologio non può tornare indietro

!!! abstract "In breve"

    Un orologio non deve mai segnare un'ora precedente a una già segnata. Se è avanti, non lo si riporta indietro di colpo: lo si fa andare un po' più piano finché l'ora giusta lo raggiunge.

L'orologio software deve essere <b>monotono</b>:

$$
t' > t \Rightarrow C(t') > C(t)
$$

Se lo spostassi indietro di colpo, due eventi dello stesso processo potrebbero ricevere timestamp nell'ordine sbagliato (l'effetto prima della causa), e un programma come <code>make</code> si confonderebbe.

Quindi un orologio avanti si <b>rallenta</b>, scegliendo bene $\alpha$ e $\beta$ (che possono cambiare nel tempo). In pratica il sistema operativo "ignora" alcuni interrupt del timer, così l'ora avanza più lentamente finché non si riallinea.

## 4. UTC, sincronizzazione esterna e interna

### UTC

<b>UTC</b> (Universal Time Coordinated) è lo standard internazionale dell'ora, basato sugli orologi atomici: 1 secondo = tempo per 9.192.631.770 transizioni di un atomo di cesio. Gli orologi atomici hanno drift intorno a $10^{-13}$.

I segnali UTC arrivano via radio (precisione circa 1 ms) o via GPS (circa 1 μs), e un computer con un ricevitore può allineare il suo orologio all'ora vera.

### Esterna vs interna

!!! abstract "In breve"

    <b>esterna</b> = ogni orologio è vicino all'ora vera (UTC). <b>Interna</b> = gli orologi sono vicini tra loro, anche se magari tutti sbagliati rispetto all'ora vera.

Sia $D > 0$ il limite di sincronizzazione (la tolleranza) e $S$ la sorgente UTC.

- <b>Sincronizzazione esterna</b> (<i>accuracy</i>): per ogni processo $i$ e ogni istante $t$ nell'intervallo $I$,

$$
|S(t) - C_i(t)| < D
$$

- <b>Sincronizzazione interna</b> (<i>agreement</i>): per ogni coppia di processi $i, j$ e ogni istante $t$ in $I$,

$$
|C_i(t) - C_j(t)| < D
$$

Relazioni tra le due:

- <b>Interna non implica esterna</b>: gli orologi possono essere d'accordo tra loro e derivare tutti insieme lontano dall'ora vera.
- <b>Esterna entro D implica interna entro 2D</b>: se ogni orologio dista meno di $D$ da UTC, due orologi distano meno di $2D$ tra loro (uno può essere $D$ avanti e l'altro $D$ indietro). Formalmente è la disuguaglianza triangolare: $|C_i - C_j| \le |C_i - S| + |S - C_j| < 2D$.

## 5. Algoritmi di sincronizzazione

Tre approcci:

- <b>Server centrale, su richiesta</b>: algoritmo di Cristian (esterna).
- <b>Server centrale che interroga tutti</b>: algoritmo di Berkeley (interna).
- <b>Servizio distribuito</b>: NTP.

### Algoritmo di Cristian

!!! abstract "In breve"

    Chiedo l'ora a un server che conosce l'ora esatta. Siccome la risposta impiega del tempo ad arrivarmi, all'ora ricevuta aggiungo una stima di quel ritardo: metà del tempo totale di andata e ritorno.

Nelle slide è scritto "Christian", ma l'autore è Flaviu <b>Cristian</b>.

Algoritmo di sincronizzazione <b>esterna</b>. C'è un time server $S$ collegato a una sorgente UTC.

1. Il processo $p$ manda a $S$ una richiesta $m_r$ e fa partire un cronometro.
2. $S$ risponde con un messaggio $m_t$ che contiene la sua ora $t$.
3. Alla ricezione $p$ misura il <b>round trip time</b> $RTT$ (tempo tra invio della richiesta e arrivo della risposta) e imposta

$$
C_p = t + \frac{RTT}{2}
$$

L'idea è che andata e ritorno durino uguale, quindi la risposta ha viaggiato circa $RTT/2$.

<b>Precisione.</b> Sia $min$ il tempo minimo possibile per un viaggio in un verso. Il viaggio della risposta è durato tra $min$ (se la risposta è stata velocissima) e $RTT - min$ (se è stata velocissima la richiesta). La stima $RTT/2$ sta in mezzo, quindi sbaglia al massimo di

$$
\pm \left( \frac{RTT}{2} - min \right)
$$

Funziona bene solo se l'RTT è piccolo rispetto alla precisione che vogliamo. Funziona "probabilisticamente" anche in asincrono: se una misura ha un RTT enorme la si scarta e si riprova.

<b>Problemi</b>

- Il server è un <b>single point of failure</b>: se crasha nessuno si sincronizza. Soluzione: chiedere a un gruppo di server sincronizzati.
- I server possono essere guasti in modo arbitrario o <b>attaccati</b> (un server malevolo può spostare l'ora di tutti). Soluzioni: ridondanza e <b>autenticazione</b> delle risposte.

### Algoritmo di Berkeley

!!! abstract "In breve"

    Non c'è un'ora "vera" di riferimento. Un coordinatore raccoglie le ore di tutti, ne fa la media scartando quelle assurde, e dice a ciascuno di quanto correggersi per arrivare alla media.

Algoritmo di sincronizzazione <b>interna</b> con struttura <b>master-slave</b>. (Nelle slide a volte è scritto "Berkley".)

<b>Passo 1: misurare le differenze.</b>

1. Il master $p_m$ manda a ogni processo (anche a sé stesso) un messaggio con la propria ora $t_1$.
2. Ogni processo $p_i$ risponde con la sua ora $t_2$.
3. Il master riceve la risposta, legge l'ora $t_3$ e stima la differenza $\Delta p_i$ tra l'orologio di $p_i$ e il suo (tenendo conto del tempo di viaggio, come in Cristian: in pratica $\Delta p_i \approx t_2 - \frac{t_1 + t_3}{2}$).

<b>Passo 2: calcolare le correzioni (master).</b>

1. Calcola la media $avg$ delle $\Delta p_i$, <b>escludendo i processi "guasti"</b>: quelli il cui orologio differisce da quello del master più di una soglia $\gamma$.
2. Per <b>ogni</b> processo (anche i guasti) calcola la correzione $adj_{p_i} = avg - \Delta p_i$ e gliela manda.

<b>Passo 3 (slave).</b> Ogni processo applica la correzione. Se è negativa <b>rallenta</b> il proprio orologio (monotonia), non lo porta indietro.

<b>Esempio.</b> Il master segna 3:05; $p_1$ segna 2:55, $p_2$ 3:00, $p_3$ 3:25.

- Differenze: $\Delta p_m = 0$, $\Delta p_1 = -10$, $\Delta p_2 = -5$, $\Delta p_3 = +20$. Nella slide c'è scritto "3:25 – 3:20 = 20", ma è un refuso: è 3:25 – 3:05.
- $p_3$ è troppo lontano, quindi è considerato guasto e non entra nella media: $avg = (0 - 10 - 5)/3 = -5$.
- Correzioni: master $-5$, $p_1$ $+5$, $p_2$ $0$, $p_3$ $-25$.

Verifica: dopo le correzioni tutti segnano 3:00. Anche $p_3$, pur escluso dalla media, viene riallineato.

<b>Precisione e tolleranza ai guasti</b>

- La precisione dipende dal massimo RTT: il master scarta le misure con RTT troppo grande.
- Se il master crasha se ne elegge un altro (in un tempo non prevedibile).
- Tollera comportamenti arbitrari degli slave (es. uno che manda valori sbagliati), perché i valori troppo lontani vengono scartati dalla media.

### NTP (Network Time Protocol)

!!! abstract "In breve"

    È il servizio che sincronizza davvero gli orologi su Internet. I server sono organizzati a livelli: in cima quelli collegati agli orologi atomici, sotto quelli che si sincronizzano con loro, e così via fino ai nostri computer.

- Sincronizza i client con <b>UTC</b> attraverso Internet.
- È organizzato ad albero, a livelli (<i>strati</i>):
    1. <b>server primari</b>: collegati direttamente a una sorgente UTC;
    2. <b>server secondari</b>: si sincronizzano con i primari;
    3. livelli più bassi, fino ai computer degli utenti.
- <b>Affidabile</b>: server e percorsi ridondanti, se un server cade ce ne sono altri.
- <b>Scalabile</b>: grazie alla gerarchia nessun server deve servire tutti.

## 6. Il limite della precisione limitata

!!! abstract "In breve"

    Anche con orologi ben sincronizzati, ogni timestamp ha un margine d'errore. Se due eventi su processi diversi capitano a distanza più piccola di quel margine, non si può sapere quale è venuto prima.

Con una sincronizzazione entro $D$, il timestamp di un evento non è un istante preciso ma un <b>intervallo di incertezza</b> intorno al valore letto (nelle slide disegnato come un cerchio attorno all'evento).

- Se gli intervalli di due eventi <b>non si sovrappongono</b>, l'ordine è certo.
- Se <b>si sovrappongono</b>, l'ordine reale non si può stabilire: l'evento con il timestamp più basso potrebbe essere avvenuto dopo.

Quindi gli orologi fisici, per quanto sincronizzati, non bastano per ordinare in modo affidabile tutti gli eventi di un sistema distribuito. Questo motiva la prossima parte del corso ("Time II"), che presumibilmente introdurrà tempi <i>logici</i> che non dipendono dagli orologi fisici.

## 7. Homework

??? note "Quale schema di messaggi è 'cattivo' per Cristian? (soluzione proposta; le slide 2024/25 riportano la domanda senza risposta scritta)"

    La slide mostra due schemi di richiesta/risposta. Nel primo andata e ritorno impiegano più o meno lo stesso tempo (frecce ugualmente inclinate). Nel secondo la richiesta è lenta (freccia molto inclinata) e la risposta istantanea (freccia verticale).

    Il cattivo è il <b>secondo</b>, cioè quello <b>asimmetrico</b>. Cristian assume che la risposta abbia viaggiato per $RTT/2$. Se la risposta in realtà è arrivata subito (ritardo ≈ $min$), $p$ aggiunge troppo e finisce avanti di circa $RTT/2 - min$: è proprio il caso peggiore dell'errore.

??? note "Fair-loss con consegna temporizzata: si può avere un perfect link con tempo di consegna limitato? (risposta confermata dalle slide 2024/25)"

    <b>Risposta del prof</b>: no. Supponiamo che esista un algoritmo A che garantisce la consegna entro X unità di tempo: l'avversario può far perdere tutte le copie spedite in quell'intervallo. Lo slogan della slide: <b>sincrono + perdite di messaggi illimitate = asincrono</b>.

    <b>Testo</b>: sistema sincrono, link fair-loss con in più la proprietà <i>timed delivery</i>: se $p$ manda $m$ al tempo $t$ e $m$ non va perso, $q$ lo consegna entro $t + 1$. Si può costruire un perfect link che garantisca anche un <b>limite</b> sul tempo di consegna?

    <b>Idea di risposta: no, non con un limite fisso.</b> Il fair-loss promette solo che, rispedendo all'infinito, prima o poi i messaggi passano. Non dice dopo quanti tentativi. L'avversario può far perdere le prime $k$ copie per qualunque $k$ scelto, quindi per qualunque limite $B$ che proponi esiste un'esecuzione in cui $m$ arriva dopo $B$.

    <b>Cosa si ottiene comunque</b>: ogni copia che arriva ci mette al massimo 1 unità di tempo. Ritrasmettendo ogni unità di tempo, il ritardo di consegna è al massimo "numero di copie perse + 1". Il limite diventa fisso solo aggiungendo un'ipotesi sul link, del tipo "al più $k$ perdite consecutive": allora $m$ arriva entro $k + 1$ unità di tempo.

??? note "Sincronizzazione completamente distribuita: media dei vicini (dalle slide 2024/25, soluzione proposta)"

    <b>Testo</b>: devi revisionare un algoritmo di sincronizzazione per grafi qualsiasi. Ogni processo legge gli orologi dei vicini, ne fa la media e imposta il proprio orologio a quel valore. C'è qualcosa che non va?

    Problemi:

    - <b>Monotonia</b>: "impostare" l'orologio alla media può spostarlo <b>indietro</b>. Va rallentato, non riportato indietro.
    - <b>Ritardi ignorati</b>: il valore letto da un vicino è già vecchio quando arriva. Senza compensare (come fa Cristian con RTT/2) si introduce un errore sistematico.
    - <b>Valori anomali</b>: un vicino guasto o malevolo con un orologio assurdo sposta la media di tutti, e l'errore si propaga nel grafo. Berkeley risolve scartando gli outlier oltre una soglia.
    - <b>Solo interna</b>: anche quando converge, gli orologi concordano tra loro ma possono derivare tutti insieme lontano da UTC.
    - <b>Convergenza lenta</b>: in un grafo sparso l'informazione si propaga solo tra vicini, quindi servono molti giri.

## Riepilogo

- <b>Eventualmente sincrono</b>: asincrono fino a un tempo $T$ ignoto, poi sincrono per sempre. Modella le reti reali; la safety deve valere sempre, la liveness può contare sulla fase sincrona.
- Esecuzioni: Sync $\subset$ E-Sync $\subset$ Async. Problemi risolvibili: al contrario.
- Orologio software $C = \alpha H + \beta$; <b>skew</b> = differenza tra due orologi, <b>drift</b> = errore di velocità. Due orologi corretti si allontanano al massimo di $2\rho t$, quindi per skew $\le \Delta$ si risincronizza ogni $\Delta / 2\rho$.
- Gli orologi devono essere <b>monotoni</b>: se sono avanti si rallentano, non si portano indietro.
- <b>Esterna</b> = vicino a UTC entro $D$; <b>interna</b> = vicini tra loro entro $D$. Esterna entro $D$ implica interna entro $2D$, non viceversa.
- <b>Cristian</b> (esterna): $C = t + RTT/2$, errore $\pm(RTT/2 - min)$.
- <b>Berkeley</b> (interna): il master fa la media delle differenze scartando gli outlier e manda a ognuno la sua correzione.
- <b>NTP</b>: gerarchia di server a strati, ridondante e scalabile.
- <b>Limite</b>: ogni timestamp ha un'incertezza, quindi eventi troppo vicini non si possono ordinare con gli orologi fisici.
