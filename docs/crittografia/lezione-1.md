# Lezione 1 – Introduzione e segretezza perfetta

## Info sul corso

- <b>Docente</b>: Prof. Daniele Venturi
- <b>Esame</b>: scritto, 3 parti. Ogni parte ha <b>1 esercizio + 1 domanda di teoria</b>
- <b>Libro di testo</b>: <i>Introduction to Modern Cryptography</i>, J. Katz e Y. Lindell

## Di cosa parla il corso

Il corso copre le basi della crittografia con un focus sulla <b>sicurezza dimostrabile</b> (<i>provable security</i>), che è l'approccio moderno.

- <b>Prima del 1950 circa</b>: la crittografia era <i>trial and error</i>. Si inventava un cifrario, qualcuno lo rompeva, se ne inventava un altro.
- <b>Dal 1950 in poi</b>: diventa una <b>scienza</b>.

<b>Sicurezza dimostrabile</b> significa due cose:

1. dare una <b>definizione precisa</b> di cosa vuol dire "sicuro"
2. fornire una <b>dimostrazione</b> che lo schema soddisfa quella definizione (eventualmente sotto alcune ipotesi)

### Obiettivo: comunicazione sicura

Scenario classico: <b>Alice</b> manda un messaggio $m$ a <b>Bob</b>, e <b>Eve</b> (l'avversaria, da <i>eavesdropper</i>) sta in mezzo al canale.

Due proprietà che vogliamo:

- <b>Confidenzialità</b>: Eve intercetta $m$ ma non deve capirne nulla.
- <b>Integrità</b>: Eve non deve poter modificare il messaggio. Se Bob riceve $m' \ne m$ deve accorgersene.

!!! note ""

    In questa lezione ci occupiamo solo di <b>confidenzialità</b>.

## Sicurezza incondizionata (Shannon)

!!! abstract "In breve"

    La sicurezza è "incondizionata" quando vale anche contro un avversario con potenza di calcolo infinita. Non si basa su problemi difficili da calcolare, ma sul fatto che l'informazione per rompere lo schema proprio non c'è.

È la trattazione dovuta a <b>Claude Shannon</b>. "Incondizionata" vuol dire che la sicurezza vale anche contro un avversario con <b>potenza di calcolo illimitata</b>.

### Schema di cifratura

Alice e Bob condividono una chiave segreta $k$. Alice cifra $m$ ottenendo il cifrato $c$, lo manda a Bob, e Bob decifra con la stessa chiave.

```text
         k                          k
         ↓                          ↓
Alice → [Enc] ──── c ────→ [Dec] → Bob
  m
```

Notazione:

- $\mathcal{K}$ = spazio delle chiavi, $\mathcal{M}$ = spazio dei messaggi, $\mathcal{C}$ = spazio dei cifrati
- Uno schema è una coppia $\Pi = (\text{Enc}, \text{Dec})$ con

$$
\text{Enc}: \mathcal{K} \times \mathcal{M} \to \mathcal{C} \qquad \text{Dec}: \mathcal{K} \times \mathcal{C} \to \mathcal{M}
$$

<b>Ipotesi</b>: la chiave $k \in \mathcal{K}$ è scelta in modo <b>uniformemente casuale</b> ed è <b>sconosciuta a Eve</b>.

### Correttezza

Decifrare quello che si è cifrato deve restituire il messaggio originale:

$$
\forall k \in \mathcal{K},\ \forall m \in \mathcal{M}: \quad \text{Dec}(k, \text{Enc}(k, m)) = m
$$

### Definizione: segretezza perfetta

!!! abstract "In breve"

    Uno schema è perfettamente segreto se vedere il cifrato non cambia nulla di quello che Eve sa sul messaggio: la sua stima prima e dopo aver visto il cifrato è la stessa.

Sia $M$ una <b>qualunque</b> distribuzione sui messaggi e $K$ la distribuzione uniforme sulle chiavi. Allora anche il cifrato $C = \text{Enc}(K, M)$ è una variabile aleatoria.

$\Pi$ è <b>perfettamente segreto</b> se per ogni distribuzione $M$, per ogni $m \in \mathcal{M}$ e per ogni $c \in \mathcal{C}$ (con $\Pr[C=c] > 0$):

$$
\Pr[M = m] = \Pr[M = m \mid C = c]
$$

<b>Intuizione</b>: $\Pr[M = m]$ è quello che Eve sa sul messaggio <i>prima</i> di vedere il cifrato (es. "Alice scrive 'sì' nel 70% dei casi"). $\Pr[M = m \mid C = c]$ è quello che sa <i>dopo</i> averlo visto. Se sono uguali, vedere il cifrato non le ha insegnato nulla.

!!! note ""

    <b>Perché "per ogni distribuzione </b>$M$<b>"?</b> Perché non sappiamo cosa Eve sappia già dei messaggi. La definizione deve funzionare qualunque sia la sua conoscenza a priori.

## Teorema: tre formulazioni equivalenti

!!! abstract "In breve"

    La segretezza perfetta si può dire in tre modi equivalenti: (i) a priori = a posteriori, (ii) messaggio e cifrato sono indipendenti, (iii) ogni messaggio produce i cifrati con la stessa distribuzione. Per dimostrare che uno schema è perfettamente segreto di solito si usa la (iii).

Le seguenti sono equivalenti:

1. <b>(i)</b> $\Pi$ è perfettamente segreto
2. <b>(ii)</b> $M$ e $C$ sono <b>indipendenti</b> (in termini di teoria dell'informazione: la mutua informazione è $I(M; C) = 0$)
3. <b>(iii)</b> $\forall m, m' \in \mathcal{M},\ \forall c \in \mathcal{C}$:

$$
\Pr[\text{Enc}(K, m) = c] = \Pr[\text{Enc}(K, m') = c]
$$

<b>Intuizione di (iii)</b>: la distribuzione del cifrato è <b>la stessa qualunque sia il messaggio</b>. Vedendo $c$ non puoi capire se veniva da $m$ o da $m'$. Nota che qui la probabilità è solo sulla scelta della chiave: il messaggio è fissato.

(iii) è la formulazione più comoda da verificare in pratica, ed è quella che si usa per dimostrare che uno schema è perfettamente segreto.

## One-Time Pad (OTP)

<b>Definizione</b>: il One-Time Pad è un cifrario a chiave simmetrica che cifra facendo lo <b>XOR bit a bit</b> tra messaggio e chiave. La chiave è scelta <b>uniformemente</b>, è <b>lunga quanto il messaggio</b> e va usata <b>una sola volta</b>.

$\mathcal{K} = \mathcal{M} = \mathcal{C} = \{0,1\}^\ell$ (stringhe di $\ell$ bit)

$$
\text{Enc}(k, m) = k \oplus m \qquad \text{Dec}(k, c) = k \oplus c
$$

<b>Correttezza</b>: $\text{Dec}(k, \text{Enc}(k, m)) = k \oplus (k \oplus m) = (k \oplus k) \oplus m = 0^\ell \oplus m = m$ ✓

!!! example ""

    <b>Esempio</b> con $\ell = 4$: $m = 1010$, $k = 0110$

    Cifratura: $c = 1010 \oplus 0110 = 1100$

    Decifratura: $1100 \oplus 0110 = 1010 = m$ ✓

### Corollario: l'OTP è perfettamente segreto

!!! abstract "In breve"

    Per ogni messaggio e ogni cifrato c'è esattamente una chiave che porta l'uno nell'altro. Siccome la chiave è casuale, visto il cifrato ogni messaggio resta ugualmente possibile.

<b>Dimostrazione</b> (usando la (iii)). Fissiamo un qualunque $m$ e un qualunque $c$:

$$
\Pr[\text{Enc}(K, m) = c] = \Pr[K \oplus m = c] = \Pr[K = c \oplus m] = 2^{-\ell}
$$

- Il secondo passaggio: "$K \oplus m = c$" equivale a "$K = c \oplus m$" (fai XOR con $m$ da entrambi i lati).

È come risolvere un'equazione normale. Se hai x + 3 = 5, per isolare x sottrai 3 da entrambi i lati. Con lo XOR si fa la stessa cosa, ma l'operazione "inversa" dello XOR è lo XOR stesso: per togliere m, fai di nuovo ⊕ m.

Passo per passo, partendo da

K ⊕ m = c

fai ⊕ m da entrambi i lati:

K ⊕ m ⊕ m = c ⊕ m

A sinistra m ⊕ m = 0 (una cosa XOR se stessa si annulla), quindi resta

K ⊕ 0 = c ⊕ m

e siccome K ⊕ 0 = K:

K = c ⊕ m

- L'ultimo: $c \oplus m$ è <b>una</b> stringa specifica, e $K$ è uniforme su $2^\ell$ stringhe, quindi la probabilità di beccarla è $2^{-\ell}$.

Lo stesso conto per un qualunque altro $m'$ dà $\Pr[\text{Enc}(K, m') = c] = 2^{-\ell}$. Le due probabilità sono uguali, quindi vale (iii) e per il teorema l'OTP è perfettamente segreto. ∎

<b>Intuizione</b>: per ogni coppia $(m, c)$ esiste <b>esattamente una</b> chiave che porta $m$ in $c$. Quindi, visto $c$, ogni messaggio è ugualmente plausibile: basta "supporre" la chiave giusta.

### Limiti dell'OTP

La segretezza perfetta è possibile, ma <b>a caro prezzo</b>:

1. <b>La chiave è lunga quanto il messaggio.</b> Per mandare 1 GB serve 1 GB di chiave condivisa in anticipo.
2. <b>La chiave si può usare una sola volta</b> (da cui <i>one-time</i>). Se cifri due messaggi con la stessa chiave:

$$
c_1 = k \oplus m_1, \quad c_2 = k \oplus m_2 \quad\Rightarrow\quad c_1 \oplus c_2 = m_1 \oplus m_2
$$

perché $k \oplus k = 0^\ell$. La chiave sparisce ed Eve ottiene lo XOR dei due messaggi.

!!! example ""

    <b>Esempio</b>: $m_1 \oplus m_2$ vale 0 esattamente nelle posizioni in cui i due messaggi coincidono. Eve scopre quindi dove sono uguali e dove no. E se conosce uno dei due messaggi, ricava l'altro: $m_2 = (c_1 \oplus c_2) \oplus m_1$.

<b>Perché la chiave sparisce</b>: lo XOR di un bit con se stesso fa sempre 0, quindi facendo $c_1 \oplus c_2$ le due $k$ si annullano:

$$
c_1 \oplus c_2 = (m_1 \oplus k) \oplus (m_2 \oplus k) = m_1 \oplus m_2 \oplus (k \oplus k) = m_1 \oplus m_2
$$

!!! example ""

    <b>Esempio numerico</b>: chiave $k = 0110$ usata due volte.

    - $m_1 = 1010$, quindi $c_1 = 1010 \oplus 0110 = 1100$

    - $m_2 = 1001$, quindi $c_2 = 1001 \oplus 0110 = 1111$

    Eve vede solo $c_1$ e $c_2$ e calcola $c_1 \oplus c_2 = 1100 \oplus 1111 = 0011$, che è proprio $m_1 \oplus m_2 = 1010 \oplus 1001 = 0011$, <b>senza conoscere la chiave</b>.

!!! note ""

    <b>Cosa ci legge</b>: 0011 vuol dire che i due messaggi hanno i primi due bit uguali e gli ultimi due diversi.

!!! note ""

    <b>Se conosce</b> $m_1 = 1010$: ricava $m_2 = 0011 \oplus 1010 = 1001$ e anche la chiave $k = c_1 \oplus m_1 = 1100 \oplus 1010 = 0110$. Nella realtà conoscere un pezzo di messaggio è facile: le email iniziano con "Ciao", i file hanno intestazioni standard.

<b>Il confronto</b>: con <b>un solo</b> cifrato ogni messaggio è compatibile con $c$ (basta cambiare chiave), quindi Eve non impara nulla. Con <b>due</b> cifrati e la stessa chiave, combinandoli elimina la chiave e ottiene informazioni vere sui messaggi.

## Dimostrazione del teorema

Schema: (i) ⇒ (ii) ⇒ (iii) ⇒ (i). Così basta dimostrare tre implicazioni per avere tutte le equivalenze.

### (i) ⇒ (ii)

Per la segretezza perfetta e la definizione di probabilità condizionata:

$$
\Pr[M = m] = \Pr[M = m \mid C = c] = \frac{\Pr[M = m \wedge C = c]}{\Pr[C = c]}
$$

Moltiplicando per $\Pr[C = c]$:

$$
\Pr[M = m \wedge C = c] = \Pr[M = m] \cdot \Pr[C = c]
$$

che è proprio la definizione di indipendenza tra $M$ e $C$.

### (ii) ⇒ (iii)

$$
\Pr[\text{Enc}(K, m) = c] = \Pr[\text{Enc}(K, M) = c \mid M = m] = \Pr[C = c \mid M = m] = \Pr[C = c]
$$

- <b>1° passaggio</b>: condizionare su $M = m$ equivale a fissare il messaggio a $m$. Funziona perché la chiave $K$ è scelta indipendentemente dal messaggio, quindi sapere $M = m$ non cambia la distribuzione di $K$.
- <b>2° passaggio</b>: $\text{Enc}(K, M)$ è per definizione $C$.
- <b>3° passaggio</b>: per (ii) $M$ e $C$ sono indipendenti, quindi il condizionamento sparisce.

Con gli stessi passaggi, $\Pr[\text{Enc}(K, m') = c] = \Pr[C = c]$. Entrambe valgono $\Pr[C = c]$, quindi sono uguali. ✓

### (iii) ⇒ (i)

<b>Passo 1</b>: mostriamo che $\Pr[C = c \mid M = m] = \Pr[C = c]$.

Partiamo da $\Pr[C = c]$ e usiamo la <b>probabilità totale</b> spezzando su tutti i possibili messaggi $m'$:

$$
\begin{aligned}
\Pr[C = c] &= \sum_{m'} \Pr[C = c \wedge M = m'] \\
&= \sum_{m'} \Pr[C = c \mid M = m'] \cdot \Pr[M = m'] \\
&= \sum_{m'} \Pr[\text{Enc}(K, M) = c \mid M = m'] \cdot \Pr[M = m'] \\
&= \sum_{m'} \Pr[\text{Enc}(K, m') = c] \cdot \Pr[M = m'] \\
&= \sum_{m'} \Pr[\text{Enc}(K, m) = c] \cdot \Pr[M = m'] \qquad \text{(qui usiamo (iii))} \\
&= \Pr[\text{Enc}(K, m) = c] \cdot \underbrace{\sum_{m'} \Pr[M = m']}_{=\,1} \\
&= \Pr[\text{Enc}(K, M) = c \mid M = m] = \Pr[C = c \mid M = m]
\end{aligned}
$$

<b>Il trucco</b>: grazie a (iii), $\Pr[\text{Enc}(K, m') = c]$ è lo stesso numero per ogni $m'$, quindi lo sostituiamo con quello di un $m$ fissato e lo portiamo fuori dalla somma. Quel che resta è la somma delle probabilità di tutti i messaggi, che fa 1.

<b>Passo 2</b>: applichiamo Bayes. Scriviamo $\Pr[M = m \wedge C = c]$ in due modi:

$$
\Pr[M = m \mid C = c] \cdot \Pr[C = c] = \Pr[M = m \wedge C = c] = \Pr[C = c \mid M = m] \cdot \Pr[M = m]
$$

Quindi

$$
\Pr[M = m] = \frac{\Pr[M = m \mid C = c] \cdot \Pr[C = c]}{\Pr[C = c \mid M = m]}
$$

Per il passo 1 il denominatore è uguale a $\Pr[C = c]$, che si semplifica con quello al numeratore:

$$
\Pr[M = m] = \Pr[M = m \mid C = c]
$$

che è la segretezza perfetta. ∎

## Riepilogo

- Sicurezza dimostrabile = definizione precisa + dimostrazione
- Confidenzialità (Eve non capisce) vs integrità (Eve non modifica)
- Segretezza perfetta: vedere il cifrato non cambia la conoscenza sul messaggio, $\Pr[M = m] = \Pr[M = m \mid C = c]$
- Equivale a $M$ e $C$ indipendenti, ed equivale a "ogni messaggio produce la stessa distribuzione di cifrati"
- L'OTP ($c = k \oplus m$) è perfettamente segreto
- Prezzo: chiave lunga quanto il messaggio e usabile una volta sola
