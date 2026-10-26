# Lezione 2 – Teorema di Shannon e MAC

## Teorema di Shannon: il prezzo della segretezza perfetta

Nella lezione 1 abbiamo visto che l'OTP è perfettamente segreto ma ha limiti pesanti. Shannon dimostra che non è colpa dell'OTP: <b>ogni</b> schema perfettamente segreto deve avere gli stessi limiti.

### Teorema

!!! abstract "In breve"

    Per avere segretezza perfetta servono almeno tante chiavi quanti messaggi, cioè una chiave lunga almeno quanto il messaggio. Vale per qualunque cifrario, non solo per l'OTP.

Per ogni SKE (schema di cifratura a chiave simmetrica) con segretezza perfetta:

$$
|\mathcal{K}| \ge |\mathcal{M}|
$$

Cioè servono almeno tante chiavi quanti sono i messaggi. Con chiavi e messaggi fatti di bit: la chiave deve essere lunga <b>almeno quanto il messaggio</b>.

### Dimostrazione (per assurdo)

!!! abstract "In breve"

    Se le chiavi sono meno dei messaggi, Eve prova a decifrare il cifrato con tutte le chiavi e ottiene meno candidati dei messaggi possibili. Qualche messaggio viene escluso, quindi Eve ha imparato qualcosa.

Sia $\Pi$ un qualunque SKE perfettamente segreto. Fissiamo la <b>distribuzione uniforme</b> su $\mathcal{M}$ (la definizione deve valere per ogni distribuzione, quindi possiamo sceglierne una comoda). Prendiamo un qualunque $c \in \mathcal{C}$ con $\Pr[C = c] > 0$.

Consideriamo l'insieme di tutti i messaggi che $c$ potrebbe nascondere:

$$
\mathcal{M}' = \{\text{Dec}(k, c) : k \in \mathcal{K}\}
$$

Supponiamo per assurdo che $|\mathcal{K}| < |\mathcal{M}|$.

- $|\mathcal{M}'| \le |\mathcal{K}|$: ogni chiave produce un solo messaggio (Dec è deterministica), quindi i messaggi diversi in $\mathcal{M}'$ sono al massimo quante le chiavi.
- Quindi $|\mathcal{M}'| \le |\mathcal{K}| < |\mathcal{M}|$, cioè $|\mathcal{M}'| < |\mathcal{M}|$.

Allora esiste un messaggio $m \in \mathcal{M} \setminus \mathcal{M}'$: un messaggio che $c$ non può nascondere con nessuna chiave.

!!! note ""

    <b>Attenzione alla notazione</b>: nelle formule compaiono tre simboli simili, con significati diversi.

    - $\mathcal{M}$ (corsiva) è l'<b>insieme</b> di tutti i messaggi possibili; $\mathcal{M}'$ è il suo sottoinsieme dei candidati per $c$.
    - $M$ (dritta), dentro $\Pr[M = m]$, <b>non è un insieme</b>: è "il messaggio che Alice manda davvero", che Eve non conosce (una variabile aleatoria, come "il risultato del dado").
    - $m$ (minuscola) è <b>un singolo messaggio</b>: quello escluso, che sta in $\mathcal{M}$ ma non in $\mathcal{M}'$.

    Quindi $\Pr[M = m]$ si legge "la probabilità che Alice abbia mandato proprio $m$", e riguarda solo quel messaggio, non tutto l'insieme.

```text
┌───────────────────────────┐
│ M            × m          │
│        ┌──────────┐       │
│        │    M'    │       │
│        └──────────┘       │
└───────────────────────────┘
```

Ora confrontiamo:

- <b>A priori</b>: $\Pr[M = m] = 1/|\mathcal{M}| > 0$ (distribuzione uniforme)
- <b>A posteriori</b>: $\Pr[M = m \mid C = c] = 0$. Infatti, se $c$ fosse la cifratura di $m$ con qualche chiave $k$, per correttezza $\text{Dec}(k, c) = m$, e quindi $m$ starebbe in $\mathcal{M}'$. Quindi <b>nessuna chiave</b> trasforma $m$ in $c$, e con la formula della probabilità condizionata:

$$
\Pr[M = m \mid C = c] = \frac{\Pr[M = m \wedge C = c]}{\Pr[C = c]} = \frac{0}{\Pr[C = c]} = 0
$$

Il numeratore è 0 perché "Alice manda $m$ <b>e</b> il cifrato è $c$" non succede mai; il denominatore è positivo perché abbiamo scelto un $c$ con $\Pr[C = c] > 0$.

A priori e a posteriori sono diversi: contraddizione con la segretezza perfetta. ∎

<b>Intuizione</b>: con meno chiavi che messaggi, Eve può prendere $c$ e decifrarlo con tutte le chiavi possibili. I messaggi che non escono mai sono esclusi: vedere $c$ le ha insegnato qualcosa.

### Takeaway

La segretezza perfetta costa troppo, quindi <b>faremo qualcosa di diverso</b>.

<b>Obiettivo</b>: Alice e Bob condividono <b>una</b> chiave di lunghezza <b>indipendente</b> dalla lunghezza del messaggio. <i>(Per riuscirci bisognerà rinunciare alla sicurezza contro avversari con potenza di calcolo illimitata.)</i>

## Esercizio: segretezza perfetta come gioco

!!! abstract "In breve"

    Un altro modo di definire la segretezza perfetta. Si sfida Eve a capire quale tra due messaggi è stato cifrato: lo schema è sicuro se nessuna strategia di Eve si comporta diversamente a seconda del messaggio cifrato.

Definizione alternativa di segretezza perfetta tramite un <b>gioco</b> (esperimento) tra un <b>avversario</b> $A$ e un <b>challenger</b> $C$.

$\text{GAME}_A(b, m_0, m_1)$ con $b \in \{0,1\}$ e $m_0, m_1 \in \mathcal{M}$:

1. $C$ sceglie $k \leftarrow \mathcal{K}$ uniformemente
2. $C$ manda ad $A$ il cifrato $c = \text{Enc}(k, m_b)$
3. $A$ risponde con $b' \in \{0,1\}$, il suo tentativo di indovinare quale messaggio è stato cifrato

```text
Avversario A                         Challenger C
                                     k ← K
      ←──────── c = Enc(k, m_b) ────────
      ──────── b' ∈ {0,1} ─────────→
```

<b>Definizione</b>: $\Pi$ è perfettamente segreto se $\forall A$, $\forall m_0, m_1 \in \mathcal{M}$:

$$
\Big| \Pr[b' = 1 : \text{GAME}_A(0, m_0, m_1)] - \Pr[b' = 1 : \text{GAME}_A(1, m_0, m_1)] \Big| = 0
$$

Notazione: $\Pr[b' = 1 : \text{GAME}]$ è la probabilità che $A$ risponda 1 giocando quel gioco.

<b>Formulazione alternativa</b>: $\text{GAME}_A(0, m_0, m_1) \equiv \text{GAME}_A(1, m_0, m_1)$, cioè i due giochi sono <b>identicamente distribuiti</b>.

<b>Intuizione</b>: se la risposta di $A$ dipendesse da $b$, vorrebbe dire che $A$ riesce a distinguere la cifratura di $m_0$ da quella di $m_1$. La definizione chiede che nessun avversario ci riesca.

### Spiegazione semplice

<b>L'idea</b>: mettiamo alla prova Eve. Le facciamo vedere un cifrato e le chiediamo <b>quale di due messaggi</b> c'è dentro. Se il cifrario è sicuro, non deve riuscire a capirlo.

<b>Le regole</b>: si scelgono due messaggi, per esempio $m_0$ = "SÌ" e $m_1$ = "NO". Poi:

1. $C$ (l'arbitro) sceglie una chiave a caso.
2. $C$ cifra <b>uno dei due</b> messaggi e dà il cifrato $c$ ad $A$ (Eve).
3. $A$ guarda $c$ e risponde <b>0</b> ("secondo me era $m_0$") oppure <b>1</b> ("secondo me era $m_1$").

<b>GAME(0) e GAME(1)</b>: la $b$ dice quale messaggio viene cifrato. In <b>GAME(0)</b> $C$ cifra sempre $m_0$, in <b>GAME(1)</b> cifra sempre $m_1$. $A$ non sa in quale versione si trova.

<b>La condizione di sicurezza</b>: il cifrario è sicuro se $A$ si comporta <b>allo stesso modo</b> in entrambe le versioni, cioè risponde "1" con la stessa probabilità sia in GAME(0) sia in GAME(1). Se le sue risposte cambiano a seconda del messaggio cifrato, vuol dire che dal cifrato riesce a capire qualcosa.

!!! example ""

    <b>Esempio: cifrario rotto.</b> Chiave di 1 bit, messaggi di 2 bit: se $k = 1$ si invertono entrambi i bit, se $k = 0$ restano uguali. Prendiamo $m_0 = 00$ e $m_1 = 01$.

    - In <b>GAME(0)</b> si cifra 00, quindi $c$ è 00 oppure 11: bit sempre <b>uguali</b>.

    - In <b>GAME(1)</b> si cifra 01, quindi $c$ è 01 oppure 10: bit sempre <b>diversi</b>.

    $A$ usa la strategia "se i bit di $c$ sono uguali rispondo 0, se sono diversi rispondo 1". In GAME(0) risponde 1 con probabilità <b>0</b>, in GAME(1) con probabilità <b>1</b>. La differenza è 1: $A$ vince sempre, quindi il cifrario <b>non</b> è sicuro.

!!! example ""

    <b>Esempio: OTP.</b> Chiave di 2 bit, sempre $m_0 = 00$ e $m_1 = 01$.

    - In <b>GAME(0)</b> $c = 00 \oplus k$: uno qualsiasi tra 00, 01, 10, 11, ognuno con probabilità 1/4.

    - In <b>GAME(1)</b> $c = 01 \oplus k$: di nuovo uno qualsiasi tra 00, 01, 10, 11, ognuno con probabilità 1/4.

    $A$ vede cifrati distribuiti <b>esattamente allo stesso modo</b> nei due giochi, quindi qualunque strategia usi risponde 1 con la stessa probabilità in entrambi. La differenza è 0: l'OTP è sicuro.

<b>In una frase</b>: il gioco chiede "Eve, guardando il cifrato, riesce a distinguere se dentro c'era $m_0$ o $m_1$?". Se per ogni coppia di messaggi e per ogni strategia la risposta è no, il cifrario è perfettamente segreto. È la stessa idea di "a priori = a posteriori", detta in un altro modo.

<b>Esercizio</b>: dimostrare che questa definizione è equivalente alla segretezza perfetta.

??? note "Soluzione proposta (non negli appunti del prof)"

    <b>PS ⇒ gioco.</b> Per la (iii) della lezione 1, $\text{Enc}(K, m_0)$ e $\text{Enc}(K, m_1)$ hanno la stessa distribuzione. $A$ vede solo $c$, quindi nei due giochi riceve un input con la stessa distribuzione e la sua risposta $b'$ ha la stessa distribuzione. La differenza è 0.

    <b>Gioco ⇒ PS</b> (per contrapposizione). Se $\Pi$ non è perfettamente segreto, per la (iii) esistono $m_0, m_1, c$ con $\Pr[\text{Enc}(K, m_0) = c] \ne \Pr[\text{Enc}(K, m_1) = c]$. Costruiamo l'avversario $A$: "se ricevo $c$ rispondo 1, altrimenti 0". Allora $\Pr[b' = 1 : \text{GAME}_A(0)] = \Pr[\text{Enc}(K, m_0) = c]$ e $\Pr[b' = 1 : \text{GAME}_A(1)] = \Pr[\text{Enc}(K, m_1) = c]$, che sono diverse: la differenza non è 0 e la definizione col gioco è violata.

## Message Authentication Codes (MAC)

!!! abstract "In breve"

    Un MAC serve a <b>autenticare</b> un messaggio, cioè a garantire che venga davvero da chi conosce la chiave e che non sia stato modificato. Alice attacca al messaggio un <b>tag</b> che solo chi ha la chiave sa calcolare, e Bob lo ricalcola per verificarlo. Non nasconde il messaggio.

Nella lezione 1 ci siamo occupati di <b>confidenzialità</b>. Ora passiamo all'<b>integrità</b>: Eve non deve poter modificare il messaggio senza che Bob se ne accorga.

### Schema

Alice e Bob condividono una chiave $k \in \mathcal{K}$.

```text
Alice (k)                                       Bob (k)
m → [Tag] → τ                                   m → [Tag] → τ*
                ────── (m, τ) ──────→                  τ* = τ ?
```

- Alice calcola il <b>tag</b> $\tau = \text{Tag}(k, m)$ e manda la coppia $(m, \tau)$, <b>in chiaro</b>: il MAC non nasconde il messaggio, lo autentica.
- Bob ricalcola $\text{Tag}(k, m)$ e controlla che coincida con $\tau$.

$$
\text{Tag}: \mathcal{K} \times \mathcal{M} \to \mathcal{T}
$$

Tag è <b>deterministica</b>: stessa chiave e stesso messaggio danno sempre lo stesso tag. È quello che permette a Bob di ricalcolarlo e confrontarlo.

### Sicurezza: cosa vuole fare Eve

<b>Obiettivo di Eve</b>: produrre una coppia $(m', \tau')$, <b>senza conoscere</b> $k$, tale che $\tau' = \text{Tag}(k, m')$. Si chiama <i>forgery</i> (falsificazione).

Rendiamo Eve più forte: conosce già una coppia <b>valida</b> $(m, \tau)$, cioè con $\text{Tag}(k, m) = \tau$ (ad esempio perché l'ha intercettata). Deve comunque essere difficile falsificare un $\tau'$ valido per un $m' \ne m$.

!!! note ""

    Perché $m' \ne m$? Rimandare la stessa coppia $(m, \tau)$ è sempre possibile, quindi non conta come falsificazione.

### Definizione: sicurezza statistica (one-time)

!!! abstract "In breve"

    Un MAC è ε-sicuro se Eve, anche dopo aver visto un messaggio con il suo tag, riesce a indovinare il tag di un altro messaggio al massimo con probabilità $\varepsilon$, piccolissima.

Sia Tag un MAC su $\mathcal{K}, \mathcal{M}, \mathcal{T}$. Diciamo che è <b>ε-statisticamente sicuro</b> (<i>one-time</i>) se $\forall m, m' \in \mathcal{M}$ con $m \ne m'$ e $\forall \tau, \tau' \in \mathcal{T}$:

$$
\Pr[\text{Tag}(K, m') = \tau' \mid \text{Tag}(K, m) = \tau] \le \varepsilon
$$

con $K$ uniforme su $\mathcal{K}$.

<b>Intuizione</b>: anche sapendo il tag di $m$, indovinare il tag di un altro messaggio riesce al massimo con probabilità $\varepsilon$.

- <b>Statistica</b>: vale contro avversari con potenza di calcolo illimitata, come la segretezza perfetta di Shannon.
- <b>One-time</b>: Eve vede una sola coppia valida, quindi la chiave va usata per autenticare un solo messaggio.

Valori tipici di $\varepsilon$: $2^{-80}$, $2^{-128}$.

### Esercizi

<b>Esercizio 1.</b> La ε-sicurezza è impossibile per $\varepsilon = 0$.

??? note "Soluzione proposta (non negli appunti del prof)"

    Fissiamo $m \ne m'$ e un $\tau$ con $\Pr[\text{Tag}(K, m) = \tau] > 0$. Il tag di $m'$ sarà pur qualcosa, quindi sommando su tutti i $\tau' \in \mathcal{T}$ le probabilità condizionate $\Pr[\text{Tag}(K, m') = \tau' \mid \text{Tag}(K, m) = \tau]$ si ottiene 1. Sono $|\mathcal{T}|$ termini, quindi almeno uno vale $\ge 1/|\mathcal{T}| > 0$. Ne segue $\varepsilon \ge 1/|\mathcal{T}|$.

    In pratica: Eve può sempre tirare a indovinare un tag a caso.

<b>Esercizio 2.</b> L'OTP usato come MAC è insicuro: $\text{Tag}(k, m) = \tau = m \oplus k$.

??? note "Soluzione proposta (non negli appunti del prof)"

    Eve conosce $(m, \tau)$ e ricava la chiave: $k = m \oplus \tau$. Poi per qualunque $m' \ne m$ calcola $\tau' = m' \oplus k$. Riesce con probabilità 1, quindi lo schema non è ε-sicuro per nessun $\varepsilon < 1$.

    Esempio: $m = 1010$, $\tau = 0011$, quindi $k = 1001$. Per $m' = 1111$: $\tau' = 1111 \oplus 1001 = 0110$.

    Morale: l'OTP è perfetto per la confidenzialità ma inutile per l'integrità.

<b>Esercizio 3.</b> Consideriamo un gioco come prima:

1. $A$ manda un messaggio $m \in \mathcal{M}$ al challenger
2. Il challenger sceglie $k \leftarrow \mathcal{K}$ e risponde con $\tau = \text{Tag}(k, m)$
3. $A$ produce una coppia $(m', \tau')$

```text
Avversario A                         Challenger C
      ──────── m ∈ M ──────────→
                                     k ← K
      ←──────── τ = Tag(k, m) ───────
      ──────── (m', τ') ─────────→
```

$A$ <b>vince</b> (WIN) se: (i) $m' \ne m$ e (ii) $\text{Tag}(k, m') = \tau'$.

Richiesta: $\forall A$, $\Pr[\text{WIN}] \le \varepsilon$.

??? note "Soluzione proposta (non negli appunti del prof)"

    <b>Definizione ⇒ gioco.</b> Per un $A$ deterministico, $m$ è fissato e la coppia $(m', \tau')$ dipende solo dal $\tau$ ricevuto. Spezzando sui possibili $\tau$ (probabilità totale): $\Pr[\text{WIN}] = \sum_\tau \Pr[\text{Tag}(K, m) = \tau] \cdot \Pr[\text{Tag}(K, m') = \tau' \mid \text{Tag}(K, m) = \tau]$. Ogni probabilità condizionata è al più $\varepsilon$ e le altre sommano a 1, quindi $\Pr[\text{WIN}] \le \varepsilon$. Se $A$ è probabilistico, si fa la media sulle sue scelte casuali e il limite resta.

    <b>Il viceversa in generale no</b>: la definizione chiede il limite per <b>ogni</b> $\tau$, il gioco solo <b>in media</b> sui $\tau$. Un tag rarissimo che rende facile la falsificazione viola la definizione ma pesa pochissimo nel gioco.

## Costruire MAC: funzioni hash pairwise independent

!!! abstract "In breve"

    Si sceglie a caso una funzione da una famiglia (cioè si sceglie una chiave a caso). Ogni input dà <b>il suo</b> output. La famiglia è <b>pairwise independent</b> se, <b>conoscendo l'output su un input, non si sa nulla dell'output su un altro input</b>: può essere qualunque valore, compreso lo stesso, ognuno con la stessa probabilità. È come lanciare due dadi separati: a volte escono uguali, ma il primo non dice niente sul secondo. Nel MAC l'output è il tag: Eve vede il tag di un messaggio e non impara nulla sul tag di un altro.

!!! example ""

    <b>Esempio</b>: $h(m) = a \cdot m + b \bmod 3$. Se sai $h(0) = 2$, allora $b = 2$, ma $a$ resta ignoto: $h(1) = a + 2$ vale 2, 0 o 1 a seconda di $a$, ognuno con probabilità 1/3. Con $h(m) = m + k \bmod 3$ invece, da $h(0) = 2$ ricavi $k = 2$ e quindi $h(1) = 0$ con certezza: <b>non</b> è pairwise independent.

Costruiremo i MAC usando un particolare tipo di <b>funzioni hash</b>.

### Definizione

Una famiglia $\mathcal{H} = \{h_k : \mathcal{M} \to \mathcal{T}\}_{k \in \mathcal{K}}$ è <b>pairwise independent</b> se $\forall m, m' \in \mathcal{M}$ con $m \ne m'$, la coppia

$$
(h(K, m),\ h(K, m'))
$$

con $K$ uniforme su $\mathcal{K}$, è <b>uniforme</b> su $\mathcal{T}^2 = \mathcal{T} \times \mathcal{T}$.

Notazione: $h(k, m) = h_k(m)$.

<b>Intuizione</b>: i valori della funzione su due input diversi si comportano come due valori scelti a caso e indipendenti. Conoscere $h_K(m)$ non dice nulla su $h_K(m')$.

Questo suggerisce di usare:

$$
\text{Tag}(k, m) = h(k, m) = h_k(m)
$$

??? note "Perché funziona (anticipazione, non negli appunti del prof)"

    Se la coppia è uniforme su $\mathcal{T}^2$, ogni coppia $(\tau, \tau')$ ha probabilità $1/|\mathcal{T}|^2$, e da sola $h(K, m) = \tau$ ha probabilità $1/|\mathcal{T}|$. Quindi:

    $\Pr[h(K, m') = \tau' \mid h(K, m) = \tau] = \dfrac{1/|\mathcal{T}|^2}{1/|\mathcal{T}|} = \dfrac{1}{|\mathcal{T}|}$

    Il MAC è ε-sicuro con $\varepsilon = 1/|\mathcal{T}|$, il minimo possibile per l'esercizio 1. Con tag di 128 bit: $\varepsilon = 2^{-128}$.

    <b>Esempio di famiglia pairwise independent</b>: $p$ primo, $\mathcal{K} = \mathbb{Z}_p \times \mathbb{Z}_p$, $\mathcal{M} = \mathcal{T} = \mathbb{Z}_p$, $h_{a,b}(m) = a \cdot m + b \bmod p$. Per $m \ne m'$ e una qualunque coppia $(\tau, \tau')$, il sistema $a m + b = \tau$, $a m' + b = \tau'$ ha una sola soluzione $(a, b)$: sottraendo si ottiene $a(m - m') = \tau - \tau'$, e $m - m'$ è invertibile modulo $p$. Quindi ogni coppia esce con probabilità $1/p^2$.

## Riepilogo

- <b>Shannon</b>: ogni schema perfettamente segreto ha $|\mathcal{K}| \ge |\mathcal{M}|$, quindi chiavi lunghe almeno quanto i messaggi
- Obiettivo d'ora in poi: una chiave di lunghezza indipendente dal messaggio
- La segretezza perfetta si può definire con un gioco: nessun avversario distingue la cifratura di $m_0$ da quella di $m_1$
- <b>MAC</b>: Alice manda $(m, \tau)$ in chiaro con $\tau = \text{Tag}(k, m)$, Bob ricalcola e confronta
- <b>ε-sicurezza statistica one-time</b>: visto un tag valido, falsificarne un altro riesce al più con probabilità $\varepsilon$; $\varepsilon = 0$ è impossibile
- L'OTP come MAC è completamente insicuro
- Hash <b>pairwise independent</b> → MAC con $\text{Tag}(k, m) = h_k(m)$
