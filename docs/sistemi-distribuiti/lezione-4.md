# Lezione 4 – Il tempo nei sistemi distribuiti (II): tempo logico

## Di cosa parliamo

La [Lezione 3](lezione-3.md) si chiudeva con un limite: gli orologi fisici, per quanto sincronizzati, non bastano a ordinare gli eventi. Qui si cambia approccio. Spesso non interessa <b>quando</b> è successo qualcosa, ma <b>in che ordine</b> e <b>cosa ha causato cosa</b>. Per questo bastano contatori, senza nessun orologio vero.

Percorso della lezione:

1. la relazione <b>happened-before</b>, che formalizza "questo evento può aver causato quello";
2. il <b>clock logico scalare</b> (di Lamport), un numero per evento;
3. il <b>vector clock</b>, un vettore per evento, che cattura la causalità in modo esatto;
4. un'applicazione: la <b>mutua esclusione di Lamport</b>.

Slide usate: versione A.A. 2024/25 ("Time II").

## 1. Perché serve il tempo logico

### L'esempio della chat

!!! abstract "In breve"

    Se i messaggi arrivano nell'ordine sbagliato, una risposta può arrivare prima della domanda e il significato cambia. Serve un modo per sapere che un messaggio "dipende" da un altro.

Scenario: una chat distribuita per un ambiente critico (nessun server centrale, niente copie dei messaggi su un server, deve funzionare anche se la rete perde la sincronia, quindi <b>modello asincrono</b>: niente orologi fisici affidabili).

Ordine reale:

1. Alice: "Se il prezzo di Apple scende, che facciamo?"
2. Mike: "Vendiamo Apple e compriamo Amazon."
3. Alice: "Chi lo fa?"
4. Il capo di Bob: "Lo fa Bob."

Se a Bob arrivano solo i messaggi 2 e 4, oppure il 3 dopo il 4, legge "Vendiamo Apple" seguito da "Lo fa Bob" e agisce <b>subito</b>, anche se la condizione ("se il prezzo scende") non l'ha mai vista.

Cosa serve: quando Bob riceve il messaggio di Mike, deve sapere che c'è qualcosa che l'ha <b>causato</b> (la domanda di Alice) e che lui non ha ancora visto.

<b>Obiettivo della lezione</b>: dare timestamp agli eventi in modo che rispettino l'idea intuitiva di causalità.

## 2. La relazione happened-before

!!! abstract "In breve"

    "$e$ è successo prima di $e'$" ($e \to e'$) vuol dire che $e$ <b>può aver influenzato</b> $e'$: o sono sullo stesso processo uno dopo l'altro, o c'è una catena di messaggi che porta da $e$ a $e'$. Se non c'è nessuna catena, i due eventi sono <b>concorrenti</b>: nessuno dei due può sapere dell'altro.

### Definizione (Lamport)

$e \to e'$ se vale una di queste regole:

1. <b>Ordine locale</b>: $e$ ed $e'$ sono sullo stesso processo $p_i$ ed $e$ viene prima ($e \to_i e'$).
2. <b>Invio-ricezione</b>: per ogni messaggio $m$, $\text{send}(m) \to \text{receive}(m)$.
3. <b>Transitività</b>: se $e \to e''$ ed $e'' \to e'$, allora $e \to e'$.

In pratica: $e \to e'$ se nel diagramma spazio-tempo si può andare da $e$ a $e'$ <b>seguendo le linee dei processi in avanti e le frecce dei messaggi</b>.

### Eventi concorrenti

Se né $e \to e'$ né $e' \to e$, gli eventi sono <b>concorrenti</b>: $e \parallel e'$.

Per due eventi qualsiasi vale sempre <b>esattamente una</b> di tre cose: $e \to e'$, oppure $e' \to e$, oppure $e \parallel e'$.

<b>Ordine parziale</b>: happened-before è un ordine <b>parziale</b> (poset), non totale: ci sono coppie di eventi che non sono ordinate (quelle concorrenti). Di conseguenza le sequenze di eventi che rispettano la causalità possono essere <b>più d'una</b> (si possono scambiare tra loro gli eventi concorrenti).

## 3. Clock logico scalare (Lamport)

!!! abstract "In breve"

    Ogni processo tiene un contatore. Lo aumenta a ogni evento e lo allega ai messaggi; chi riceve un messaggio porta il suo contatore almeno al valore ricevuto. Così, se un evento causa un altro, il secondo ha sempre un numero più grande.

Un <b>clock logico</b> è un contatore software che cresce sempre e non ha niente a che fare con l'ora vera. Ogni processo $p_i$ ha il suo $L_i$ e lo usa per dare un timestamp $L(e)$ agli eventi.

### Le regole

- <b>Inizio</b>: $L_i = 0$.
- <b>Evento locale o invio di</b> $m$: $L_i = L_i + 1$; se è un invio, $m$ porta con sé il timestamp $t = L_i$.
- <b>Ricezione di</b> $m$ <b>con timestamp</b> $t$: $L_i = \max(t, L_i) + 1$.

Esempio minimo: $p_0$ manda un messaggio al suo primo evento ($L = 1$). $p_1$ ha già fatto un evento ($L = 1$) e riceve: $\max(1, 1) + 1 = 2$.

### Proprietà garantita

$$
e \to e' \Rightarrow L(e) < L(e')
$$

Perché: lungo ogni passo di una catena causale il contatore cresce di almeno 1. Sullo stesso processo per la regola dell'incremento; lungo un messaggio perché il ricevente prende il massimo e poi aggiunge 1.

### Il limite

Il viceversa <b>non vale</b>:

$$
L(e) < L(e') \not\Rightarrow e \to e'
$$

Esempio dalle slide: $e^1_2$ e $e^1_3$ sono concorrenti ma hanno timestamp diversi (2 e 1); $e^1_1$ e $e^1_3$ sono concorrenti e hanno lo stesso timestamp (1). Quindi, guardando solo due numeri, <b>non si capisce se due eventi sono concorrenti o causalmente legati</b>. Se $L(e) < L(e')$, sappiamo solo che $e'$ <b>non</b> può essere successo prima di $e$.

### Ordine totale con gli ID

A volte serve un ordine <b>totale</b> (tutti d'accordo su chi viene prima, anche per eventi concorrenti). Si usa la coppia (timestamp, ID del processo):

$$
(L, i) < (L', j) \iff L < L' \ \lor\ (L = L' \land i < j)
$$

A parità di timestamp vince l'ID più piccolo. È arbitrario per gli eventi concorrenti, ma rispetta la causalità e tutti lo calcolano allo stesso modo. Si usa nella mutua esclusione più sotto.

## 4. Vector clock

### L'idea: portarsi dietro la storia

!!! abstract "In breve"

    Invece di un solo numero, ogni evento si porta dietro "quanti eventi conosco di ciascun processo". Se il vettore di $e'$ contiene tutto quello che sa il vettore di $e$ (e qualcosa in più), allora $e$ ha causato $e'$, e vale anche il viceversa.

Le slide ci arrivano per gradi:

1. <b>Prima idea</b>: il timestamp di $e$ è l'intera <b>storia</b> degli eventi che sono successi prima di $e$ (incluso $e$), divisa per processo. All'invio aggiungo l'evento alla mia storia; alla ricezione prendo, per ogni processo, la versione più aggiornata della sua storia tra la mia e quella del messaggio.
2. <b>Confronto</b>: $e \to e'$ se e solo se la storia di $e'$ <b>contiene</b> quella di $e$. Infatti se $e$ compare nella storia di $e'$, l'informazione su $e$ è arrivata a $e'$ attraverso una catena di messaggi, cioè proprio un cammino causale.
3. <b>Ottimizzazione</b>: la storia di ogni processo cresce sempre "in coda" (è sempre un prefisso di quella successiva). Quindi invece di tutta la lista basta la sua <b>lunghezza</b>. La storia diventa un vettore di $n$ interi.

### Definizione e regole

Un <b>vector clock</b> per $n$ processi è un array di $n$ interi. $p_i$ tiene $V_i$:

- $V_i[i]$ = quanti eventi ha fatto $p_i$;
- $V_i[j]$ (con $j \neq i$) = quanti eventi di $p_j$ conosce $p_i$.

Regole:

- <b>Inizio</b>: $V_i[j] = 0$ per ogni $j$.
- <b>Evento locale o invio</b>: $V_i[i] = V_i[i] + 1$; l'invio allega al messaggio il vettore $V_i$.
- <b>Ricezione di</b> $m$ <b>con vettore</b> $V_t$: $V_i[j] = \max(V_t[j], V_i[j])$ per ogni $j$, poi $V_i[i] = V_i[i] + 1$.

### Confrontare due vettori

- $V \le V'$ se $V[j] \le V'[j]$ per <b>ogni</b> $j$.
- $V < V'$ se $V \le V'$ e $V \neq V'$ (almeno una componente strettamente minore).
- Se né $V \le V'$ né $V' \le V$ (ognuno ha una componente più grande dell'altro), i vettori sono <b>non confrontabili</b>.

La proprietà chiave, che lo scalare non aveva:

$$
e \to e' \iff V(e) < V(e')
$$

Quindi: $V(e) < V(e')$ significa $e \to e'$; vettori non confrontabili significano $e \parallel e'$.

<b>Esempio</b> (dalle slide): $[\text{-},\text{-},1] < [4,3,2]$, quindi $e^1_3 \to e^4_1$. Invece $[4,3,2]$ e $[3,\text{-},3]$ non sono confrontabili (4 > 3 ma 2 \< 3), quindi $e^4_1 \parallel e^3_3$. Il trattino "-" vale 0.

### Quale clock per cosa

- <b>Scalare</b> → quando basta un ordine totale coerente con la causalità. Esempio: mutua esclusione di Lamport.
- <b>Vettoriale</b> → quando bisogna sapere davvero se un evento dipende da un altro. Esempio: <i>causal broadcast</i> (che risolve il problema della chat).

## 5. Mutua esclusione di Lamport

### Il problema

!!! abstract "In breve"

    C'è una risorsa (la <i>sezione critica</i>, CS) che può usare un solo processo alla volta. I processi devono mettersi d'accordo, solo scambiandosi messaggi, su chi entra e in che ordine.

L'astrazione ha tre eventi:

- <b>Request</b> (dall'alto): voglio entrare in CS.
- <b>Grant</b> (verso l'alto): puoi entrare.
- <b>Release</b> (dall'alto): sono uscito.

Proprietà:

- <b>Mutua esclusione</b> (safety): in ogni istante al massimo un processo è in CS.
- <b>Liveness</b>: se un processo chiede di entrare, prima o poi entra.
- <b>Fairness</b>: se la richiesta di $p$ è <i>happened-before</i> quella di $q$, $q$ non entra prima di $p$.

Ipotesi dell'algoritmo: <b>nessun crash</b> ($f = 0$) e <b>link FIFO perfect</b> (dalla Lezione 2).

### L'idea

!!! abstract "In breve"

    Tutti tengono una coda delle richieste ordinata per (timestamp, ID). Entri quando la tua richiesta è in testa alla coda <b>e</b> hai sentito tutti gli altri dopo la tua richiesta: così sei sicuro che non esiste una richiesta più vecchia ancora in viaggio.

Come funziona:

- <b>Richiesta</b>: $p_i$ incrementa il clock, manda $\text{REQ}$ con timestamp $(ck, i)$ a tutti e la mette nella sua coda <code>Requests</code>.
- <b>Ricezione di una REQ da</b> $p_j$: $p_i$ la mette in <code>Requests</code> e risponde con un $\text{ACK}$ con il suo timestamp attuale.
- <b>Entrata in CS</b>, se valgono entrambe:
    1. la richiesta di $p_i$ ha il timestamp <b>più piccolo</b> in <code>Requests</code>;
    2. $p_i$ ha ricevuto da <b>ogni</b> altro processo un messaggio con timestamp <b>maggiore</b> di quello della sua richiesta.
- <b>Uscita</b>: $p_i$ toglie la sua richiesta dalla coda e manda $\text{RELEASE}$ a tutti.
- <b>Ricezione di una RELEASE da</b> $p_j$: $p_i$ toglie la richiesta di $p_j$ dalla coda.

Perché la condizione 2 + FIFO funziona: se $p_j$ mi ha mandato un ACK con timestamp maggiore del mio, ogni richiesta che $p_j$ ha fatto <b>prima</b> ha timestamp più piccolo e, per FIFO, mi è già arrivata. Ogni richiesta che fa <b>dopo</b> avrà timestamp più grande del mio. Quindi nessuna richiesta più vecchia della mia può "spuntare" in ritardo.

### Pseudocodice (ripulito)

Nella slide i nomi <code>Requests</code>/<code>Request_set</code> sono usati a caso e la richiesta propria non viene messa in coda; qui è sistemato secondo le regole della slide precedente.

```text
upon event Init do
    Requests := ∅; Acks := ∅
    clock := 0; my_req := ⊥

upon event Request do                          // voglio la CS
    clock := clock + 1
    my_req := (REQ, ts = ⟨clock, i⟩)
    Requests := Requests ∪ {my_req}
    forall p_j ∈ Π do send FIFO(p_j, my_req)

upon event Release do                          // esco dalla CS
    Requests := Requests \ {my_req}; my_req := ⊥
    clock := clock + 1
    forall p_j ∈ Π do send FIFO(p_j, (RLS, ts = ⟨clock, i⟩))

// ts(x) < ts(y): clock più piccolo, a parità ID più piccolo
upon my_req ≠ ⊥
     and no req ∈ Requests with ts(req) < ts(my_req)
     and for every p ∈ Π exists m ∈ Acks from p with ts(m) > ts(my_req) do
    trigger Granted

upon event Deliver(m) do
    clock := max(clock(m), clock) + 1
    if m is REQ then
        Requests := Requests ∪ {m}
        clock := clock + 1
        send FIFO(sender(m), (ACK, ts = ⟨clock, i⟩))
    else if m is ACK then
        Acks := Acks ∪ {m}
    else if m is RLS then
        remove from Requests the request of sender(m)
```

### Esempio (dalle slide, 3 processi)

1. $p_3$ chiede la CS con $ts = (3, 3)$. $p_1$ e $p_2$ la mettono in coda e rispondono con un ACK.
2. Poi anche $p_1$ chiede, con $ts = (6, 1)$. Riceve gli ACK di tutti, ma in coda c'è $(3, 3) < (6, 1)$: <b>aspetta</b>.
3. $p_3$ ha tutti gli ACK ed è in testa alla coda: <b>entra</b>. Quando esce manda RELEASE.
4. Ricevuta la RELEASE, $p_1$ toglie $(3,3)$ dalla coda: ora è in testa e ha gli ACK, quindi <b>entra</b>.

### Perché funziona

<b>Mutua esclusione</b> (per assurdo). Supponiamo che $p_i$ e $p_j$ siano in CS insieme. Entrambi hanno ricevuto l'ACK dell'altro ed entrambi hanno la propria richiesta in testa alla coda.

- Se $p_j$ avesse fatto la sua richiesta <b>dopo</b> aver mandato l'ACK a $p_i$, la richiesta di $p_j$ avrebbe timestamp maggiore di quella di $p_i$ (il clock di $p_j$ è già passato oltre). Allora $p_j$ vede in coda la richiesta di $p_i$, più piccola, e non entra. Contraddizione.
- Quindi $p_j$ ha fatto la richiesta <b>prima</b> di mandare l'ACK. Per <b>FIFO</b> la REQ di $p_j$ arriva a $p_i$ prima dell'ACK, quindi è nella coda di $p_i$. Simmetricamente la REQ di $p_i$ è nella coda di $p_j$.
- Entrambi hanno entrambe le richieste in coda, e l'ordine (ts, ID) è totale: solo una delle due è la più piccola, quindi solo uno dei due può essere in testa. Contraddizione.

<b>Fairness.</b> Supponiamo che la REQ di $p_j$ sia happened-before quella di $p_i$, ma $p_i$ entri prima. Allora $ts(\text{REQ}_j) < ts(\text{REQ}_i)$ (proprietà del clock scalare). $p_i$ entra solo dopo aver ricevuto l'ACK di $p_j$, e per FIFO la REQ di $p_j$ gli è già arrivata prima di quell'ACK. Quindi nella coda di $p_i$ c'è una richiesta più piccola della sua, e non può entrare. Contraddizione.

### Costo

- <b>Messaggi per ogni CS</b>: $3(N-1)$, cioè $N-1$ REQ, $N-1$ ACK e $N-1$ RELEASE.
- <b>Ritardo nel caso migliore</b> (nessuno in CS, uno solo chiede): 2 tempi di messaggio, la REQ all'andata e l'ACK al ritorno.
- <b>Limite</b>: se un solo processo crasha, gli altri aspettano per sempre il suo ACK. Non tollera nessun guasto.

## 6. Esercizi e homework

??? note "Esercizio vector clock 1 (soluzione mia, controlla i calcoli)"

    Vettori nell'ordine $[P_1, P_2, P_3, P_4]$, eventi da sinistra a destra.

    - $P_1$: invio a $P_2$ $[1,0,0,0]$; ricezione da $P_3$ $[2,0,1,0]$; invio a $P_2$ $[3,0,1,0]$; $e_3$ (ricezione da $P_2$) $[4,7,4,3]$.
    - $P_2$: ric. $[1,1,0,0]$; invio a $P_4$ $[1,2,0,0]$; ric. da $P_1$ $[3,3,1,0]$; invio a $P_3$ $[3,4,1,0]$; ric. da $P_3$ $[3,5,4,1]$; ric. da $P_4$ $[3,6,4,3]$; invio a $P_1$ $[3,7,4,3]$.
    - $P_3$: $e_1$ (invio a $P_1$) $[0,0,1,0]$; ric. da $P_4$ $[0,0,2,1]$; ric. da $P_2$ $[3,4,3,1]$; invio a $P_2$ $[3,4,4,1]$.
    - $P_4$: invio a $P_3$ $[0,0,0,1]$; ric. da $P_2$ $[1,2,0,2]$; $e_2$ (invio a $P_2$) $[1,2,0,3]$.

    Confronti:

    - $e_1 \to e_2$: $[0,0,1,0]$ vs $[1,2,0,3]$. La terza componente è 1 > 0: non confrontabili, quindi <b>concorrenti</b>. <b>FALSA</b>.
    - $e_1 \to e_3$: $[0,0,1,0] < [4,7,4,3]$. <b>Vera</b>.
    - $e_2 \to e_3$: $[1,2,0,3] < [4,7,4,3]$. <b>Vera</b>.

??? note "Esercizio vector clock 2 (soluzione mia, controlla i calcoli)"

    - $P_1$: invio a $P_2$ $[1,0,0,0]$; $e_1$ (invio a $P_4$) $[2,0,0,0]$; invio a $P_2$ $[3,0,0,0]$; $e_3$ (ric. da $P_3$) $[4,4,4,3]$.
    - $P_2$: $e_2$ (ric. da $P_1$) $[1,1,0,0]$; ric. da $P_4$ $[1,2,0,1]$; ric. da $P_3$ $[1,3,1,1]$; invio a $P_3$ $[1,4,1,1]$; invio a $P_4$ $[1,5,1,1]$; $e_4$ (ric. da $P_1$) $[3,6,1,1]$.
    - $P_3$: invio a $P_2$ $[0,0,1,0]$; ric. da $P_2$ $[1,4,2,1]$; ric. da $P_4$ $[2,4,3,3]$; invio a $P_1$ $[2,4,4,3]$.
    - $P_4$: invio a $P_2$ $[0,0,0,1]$; ric. $e_1$ $[2,0,0,2]$; invio a $P_3$ $[2,0,0,3]$; $e_5$ (ric. da $P_2$) $[2,5,1,4]$.

    Confronti:

    - $e_1 \to e_2$: $[2,0,0,0]$ vs $[1,1,0,0]$: non confrontabili. <b>FALSA</b> ($e_1 \parallel e_2$).
    - $e_1 \to e_3$: $[2,0,0,0] < [4,4,4,3]$. <b>Vera</b>.
    - $e_2 \to e_3$: $[1,1,0,0] < [4,4,4,3]$. <b>Vera</b>.
    - (versione italiana) $e_1 \to e_4$: $[2,0,0,0] < [3,6,1,1]$. <b>Vera</b>. $e_1 \to e_5$: $[2,0,0,0] < [2,5,1,4]$. <b>Vera</b>.

??? note "Break time: debugging di p1 con i vector clock (soluzione mia)"

    <b>Dati</b>: 4 processi, clock incrementato prima dell'invio. $p_1$ invia un messaggio con $(1,0,0,0)$ e poi riceve un messaggio con $(1,2,3,1)$.

    <b>Q3.1: un'esecuzione possibile.</b>

    1. $p_1$ manda a $p_2$: $(1,0,0,0)$.
    2. $p_4$ manda a $p_3$: $(0,0,0,1)$.
    3. $p_3$ riceve da $p_4$: $(0,0,1,1)$.
    4. $p_2$ riceve da $p_1$: $(1,1,0,0)$, poi manda a $p_3$: $(1,2,0,0)$.
    5. $p_3$ riceve da $p_2$: $(1,2,2,1)$, poi manda a $p_1$: $(1,2,3,1)$.

    <b>Non è unica</b>: ad esempio si possono scambiare l'ordine dei passi 2-3 e 4, oppure il messaggio di $p_4$ può passare da $p_2$ invece che arrivare direttamente a $p_3$.

    <b>Q3.2: un processo può non aver mandato nessun messaggio?</b> No. L'informazione su un processo arriva agli altri <b>solo</b> dentro i messaggi. Ogni componente del vettore ricevuto è diversa da 0, quindi chi ha mandato il messaggio conosce eventi di tutti e quattro i processi.

    - $p_1$ ha mandato il suo messaggio iniziale.
    - Il mittente finale non può essere $p_4$: con la componente $p_4 = 1$ il suo unico evento sarebbe l'invio stesso, ma allora non potrebbe conoscere gli eventi degli altri (ricevere è un evento e farebbe salire la sua componente).
    - Quindi il mittente è $p_2$ o $p_3$. L'altro dei due e $p_4$ hanno componente diversa da 0 nel vettore del mittente, quindi devono avergli fatto arrivare informazioni: hanno spedito almeno un messaggio. E il mittente ha spedito il messaggio finale. Tutti hanno spedito.

??? note "Homework: vector clock senza conoscere i processi (soluzione proposta, non nelle slide)"

    <b>Idea</b>: al posto di un array di $n$ posizioni si usa una <b>mappa</b> ID → contatore. Un ID assente vale 0.

    - Evento locale o invio: <code>V[my_id] := V[my_id] + 1</code>.
    - Ricezione di $V_t$: per ogni ID presente in $V$ o in $V_t$, <code>V[id] := max(V[id], V_t[id])</code> (gli ID nuovi vengono aggiunti); poi <code>V[my_id] := V[my_id] + 1</code>.
    - Confronto: come prima, ma sull'unione delle chiavi delle due mappe.

    <b>Eventi concorrenti</b>: ciascuna delle due mappe ha almeno un ID con valore più alto dell'altra, spesso un ID che nell'altra <b>non compare proprio</b> (un processo di cui l'altro evento non ha mai sentito parlare).

    <b>Due processi con lo stesso ID</b>: i loro eventi finiscono nello stesso contatore, come se fossero un solo processo. Si rompe il "⇐": due eventi concorrenti dei due processi possono sembrare ordinati (es. $\{X:1\}$ e $\{X:2\}$ sembrano causalmente legati anche se non lo sono). In più i contatori non contano più correttamente gli eventi di nessuno dei due.

??? note "Homework: Lamport ME senza link FIFO (soluzione proposta, non nelle slide)"

    <b>Mutua esclusione: violata.</b> La dimostrazione usa FIFO per dire che la REQ di $p_j$ arriva prima del suo ACK. Senza FIFO un ACK può superare la REQ.

    Controesempio con 2 processi:

    1. $p_1$ ha già fatto altri eventi (clock = 5) e chiede la CS: $\text{REQ}_1$ con $ts = (6, 1)$.
    2. $p_2$ (clock = 0) chiede la CS: $\text{REQ}_2$ con $ts = (1, 2)$, che verso $p_1$ viaggia lentissima.
    3. $p_2$ riceve $\text{REQ}_1$ e risponde con un ACK con timestamp 8. L'ACK <b>supera</b> $\text{REQ}_2$ e arriva a $p_1$ per primo.
    4. $p_1$: in coda ha solo la sua richiesta, e ha un ACK di $p_2$ con ts 8 > 6. <b>Entra</b>.
    5. Arriva $\text{REQ}_2$; $p_1$ risponde con un ACK (ts > 1). $p_2$ ha in coda $(1,2)$ e $(6,1)$: la sua è la più piccola e ha l'ACK. <b>Entra anche lui</b>. Due processi in CS: violazione.

    <b>Fairness: può essere violata</b> per lo stesso motivo: la sua dimostrazione usa FIFO per garantire che la richiesta più vecchia sia già in coda quando arriva l'ACK.

    <b>Liveness: sembra reggere.</b> I link sono comunque perfect, quindi tutti i messaggi arrivano. Una richiesta arrivata in ritardo può rimescolare l'ordine, ma prima o poi ogni processo riceve tutto e la richiesta più piccola rimasta può entrare. Da verificare a lezione.

## Riepilogo

- Spesso conta l'<b>ordine causale</b>, non l'ora. <b>Happened-before</b> ($\to$): ordine locale + invio prima di ricezione + transitività. È un ordine <b>parziale</b>; gli eventi non ordinati sono <b>concorrenti</b>.
- <b>Clock scalare</b> (Lamport): $+1$ a ogni evento, $\max + 1$ alla ricezione. Garantisce $e \to e' \Rightarrow L(e) < L(e')$ ma <b>non</b> il viceversa. Con (ts, ID) si ottiene un ordine totale.
- <b>Vector clock</b>: un contatore per processo, $\max$ componente per componente alla ricezione. Garantisce $e \to e' \iff V(e) < V(e')$; vettori non confrontabili = eventi concorrenti.
- <b>Mutua esclusione di Lamport</b>: coda ordinata per (ts, ID); entri se sei in testa e hai sentito tutti dopo la tua richiesta. Serve FIFO, nessun crash tollerato, $3(N-1)$ messaggi per CS.
