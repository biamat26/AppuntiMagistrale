# Lezione 3 – MAC da hash ed estrazione di casualità

## Esempio di famiglia pairwise independent

$$
h_{a,b}(m) = a \cdot m + b \bmod p
$$

- $p$ è un <b>primo grande</b> (di $\lambda$ bit)
- Chiave: $(a, b) \in \mathbb{Z}_p^2 = \mathcal{K}$
- Messaggi e tag: $m \in \mathbb{Z}_p = \mathcal{M} = \mathcal{T}$

### Lemma

!!! abstract "In breve"

    Dimostriamo che $a \cdot m + b \bmod p$ è pairwise independent, cioè che i tag di due messaggi diversi si comportano come due numeri casuali indipendenti.

La famiglia $\mathcal{H} = \{h_{a,b}\}$ qui sopra è <b>pairwise independent</b>.

### Dimostrazione

!!! abstract "In breve"

    Si contano le chiavi $(a, b)$ che danno una certa coppia di tag. È un sistema di 2 equazioni in 2 incognite, quindi c'è una sola chiave: ogni coppia di tag ha probabilità $1/p^2$.

Fissiamo $m, m' \in \mathbb{Z}_p$ con $m \ne m'$ e $\tau, \tau' \in \mathbb{Z}_p$. Vogliamo calcolare

$$
\Pr_{a,b}[h_{a,b}(m) = \tau \wedge h_{a,b}(m') = \tau']
$$

Le due condizioni $a m + b = \tau$ e $a m' + b = \tau'$ formano un <b>sistema lineare</b> nelle incognite $a, b$. In forma matriciale:

$$
\Pr_{a,b}\left[ \begin{pmatrix} m & 1 \\ m' & 1 \end{pmatrix} \begin{pmatrix} a \\ b \end{pmatrix} = \begin{pmatrix} \tau \\ \tau' \end{pmatrix} \right] = \Pr_{a,b}\left[ \begin{pmatrix} a \\ b \end{pmatrix} = \begin{pmatrix} m & 1 \\ m' & 1 \end{pmatrix}^{-1} \begin{pmatrix} \tau \\ \tau' \end{pmatrix} \right] = \frac{1}{p^2}
$$

- <b>L'inversa esiste</b> perché $m \ne m'$: il determinante è $m - m' \ne 0 \bmod p$, e modulo un primo ogni numero non nullo è invertibile.
- Quindi c'è <b>una sola</b> coppia $(a, b)$ che soddisfa il sistema. Siccome $(a, b)$ è uniforme su $p^2$ coppie, la probabilità di beccarla è $1/p^2$. ∎

<b>Intuizione</b>: ogni coppia di tag $(\tau, \tau')$ corrisponde a esattamente una chiave, quindi la coppia di tag è uniforme su $\mathbb{Z}_p^2$.

## MAC da hash pairwise independent

### Teorema

!!! abstract "In breve"

    Se come tag usi una hash pairwise independent, Eve, anche dopo aver visto un messaggio con il suo tag, ha probabilità al massimo $1/|\mathcal{T}|$ di produrre il tag giusto per un altro messaggio.
    Eve conosce l'<b>insieme dei tag possibili</b> $\mathcal{T}$ (fa parte dello schema, che è pubblico: es. "i numeri da 0 a $p-1$"), ma non sa <b>quale</b> di questi è il tag giusto per il suo messaggio $m'$, perché dipende dalla chiave. Può usare qualunque strategia (riciclare $\tau$, fare calcoli, …), ma nessuna funziona meglio che sceglierne uno a caso tra i $|\mathcal{T}|$ possibili.

Ogni famiglia pairwise independent $\mathcal{H} = \{h_k : \mathcal{M} \to \mathcal{T}\}$ definisce un MAC <b>ε-statisticamente sicuro</b> con

$$
\varepsilon = \frac{1}{|\mathcal{T}|}
$$

### Dimostrazione

Per ogni $m \ne m'$ e ogni $\tau, \tau'$, per definizione di probabilità condizionata:

$$
\Pr[\tau' = h_K(m') \mid \tau = h_K(m)] = \frac{\Pr[\tau' = h_K(m') \wedge \tau = h_K(m)]}{\Pr[h_K(m) = \tau]} = \frac{1/|\mathcal{T}|^2}{1/|\mathcal{T}|} = \frac{1}{|\mathcal{T}|}
$$

- <b>Numeratore</b>: per pairwise independence la coppia $(h_K(m), h_K(m'))$ è uniforme su $\mathcal{T}^2$, quindi ogni coppia ha probabilità $1/|\mathcal{T}|^2$.
- <b>Denominatore</b>: sommando il numeratore su tutti i $|\mathcal{T}|$ possibili $\tau'$ si ottiene $|\mathcal{T}| \cdot 1/|\mathcal{T}|^2 = 1/|\mathcal{T}|$. ∎

Per l'esercizio 1 della lezione 2, $1/|\mathcal{T}|$ è il <b>miglior</b> $\varepsilon$ possibile.

!!! note ""

    Con l'esempio $h_{a,b}$: $|\mathcal{T}| = p \approx 2^\lambda$, quindi $\varepsilon \approx 2^{-\lambda}$, con una chiave di $2\lambda$ bit.

### Da dove vengono questi numeri

!!! abstract "In breve"

    Con una chiave di $2\lambda$ bit, la costruzione $h_{a,b}$ dà sicurezza $2^{-\lambda}$. Sono quattro piccoli conti, a partire dal fatto che <b>λ è il numero di bit di</b> $p$ (il prof sceglie un primo "di λ bit").

<b>1. Perché</b> $p \approx 2^\lambda$. Un numero di λ bit sta tra $2^{\lambda-1}$ e $2^\lambda$. Per esempio, i numeri da 3 bit vanno da $100 = 4$ a $111 = 7$, tutti vicini a $2^3 = 8$. Quindi un primo di λ bit vale circa $2^\lambda$.

<b>2. Perché</b> $|\mathcal{T}| = p$. Il tag è $(a \cdot m + b) \bmod p$: il "mod p" si applica a <b>tutta</b> l'espressione (prima si calcola $a \cdot m + b$, poi si prende il resto della divisione per $p$). Il resto di una divisione per $p$ sta sempre tra $0$ e $p-1$, quindi i tag possibili sono $0, 1, \dots, p-1$: sono $p$ valori, e $|\mathcal{T}| = p \approx 2^\lambda$.

!!! example ""

    <b>Esempio</b> con $p = 7$, $a = 3$, $m = 2$, $b = 5$: $a \cdot m + b = 11$, e $11 \bmod 7 = 4$. Qualunque calcolo si faccia, il tag è sempre uno tra 0, 1, …, 6.

<b>3. Perché</b> $\varepsilon \approx 2^{-\lambda}$. Dal teorema, $\varepsilon = 1/|\mathcal{T}| = 1/p \approx 1/2^\lambda = 2^{-\lambda}$.

<b>4. Perché la chiave è di</b> $2\lambda$ <b>bit.</b> La chiave è la coppia $(a, b)$, e $a$ e $b$ sono numeri mod $p$, cioè tra $0$ e $p-1$. Per scrivere in binario qualunque numero fino a $p-1$ bastano λ bit, quindi $a$ e $b$ occupano λ bit ciascuno: in totale $\lambda + \lambda = 2\lambda$ bit.

!!! example ""

    <b>Esempio con λ = 3</b>:

    - $p = 7$ (in binario $111$, cioè 3 bit), e $7 \approx 2^3 = 8$
    - tag possibili: $0, \dots, 6$, cioè 7 valori
    - $\varepsilon = 1/7 \approx 1/8 = 2^{-3}$
    - $a$ e $b$ valgono da 0 a 6, cioè da $000$ a $110$ in binario: 3 bit ciascuno, chiave di $3 + 3 = 6 = 2 \cdot 3$ bit

!!! example ""

    <b>Esempio reale con λ = 128</b>: $p$ è un primo di 128 bit, $\varepsilon \approx 2^{-128}$ (Eve non falsifica praticamente mai), chiave di 256 bit.

<b>Il messaggio</b>: con una chiave di $2\lambda$ bit si ottiene sicurezza $2^{-\lambda}$. È proprio il minimo previsto dalla "bad news" qui sotto con $t = 1$: $(1 + 1) \cdot \lambda = 2\lambda$.

### Bad news

!!! abstract "In breve"

    Con la sicurezza statistica la chiave del MAC deve crescere con il numero di messaggi da autenticare. Lo stesso problema dell'OTP.

<b>Teorema</b>: ogni MAC <b>t-time</b> $2^{-\lambda}$-sicuro ha una chiave di dimensione (almeno) $(t+1) \cdot \lambda$.

<i>t-time</i> = sicuro anche se Eve vede $t$ coppie valide. Quindi, come per la segretezza perfetta, con la sicurezza statistica la chiave <b>cresce</b> con il numero di messaggi da autenticare. Con $t = 1$ servono $2\lambda$ bit, esattamente quelli di $h_{a,b}$.

## Randomness extraction

<b>Definizione</b>: la <i>randomness extraction</i> (estrazione di casualità) è il processo che, partendo da una sorgente di casualità <b>imperfetta</b> (in cui alcuni valori escono più spesso di altri), produce bit <b>perfettamente casuali</b>, cioè uniformi. La funzione che lo fa si chiama <b>estrattore</b> ($\text{Ext}$).

!!! example ""

    <b>Esempio</b>: hai solo una moneta truccata che fa testa il 70% delle volte. Se la usi così com'è per creare una chiave, Eve sa che i bit valgono più spesso 1 che 0: la chiave non è uniforme e i teoremi visti (OTP, MAC) non valgono più. L'estrattore prende i lanci della moneta truccata e tira fuori bit come quelli di una moneta onesta.

    Le sorgenti reali sono di questo tipo: un computer è deterministico, quindi la casualità la prende da misure fisiche (movimenti del mouse, tempi tra un tasto e l'altro, rumore elettrico), che sono imprevedibili solo in parte.

### Un estrattore in pratica (trucco di von Neumann)

<i>(Non negli appunti del prof: esempio per capire cosa fa un estrattore.)</i>

Hai una moneta piegata che fa testa il 60% delle volte e ti servono bit perfettamente 50/50. Lanci la moneta <b>due volte</b> e guardi la coppia:

- <b>Testa poi Croce</b> → scrivi <b>0</b>
- <b>Croce poi Testa</b> → scrivi <b>1</b>
- <b>Testa Testa</b> oppure <b>Croce Croce</b> → butti via e rilanci

<b>Perché funziona</b>: $\Pr[\text{TC}] = 0{,}6 \times 0{,}4 = 0{,}24$ e $\Pr[\text{CT}] = 0{,}4 \times 0{,}6 = 0{,}24$. Le due probabilità sono identiche, quindi 0 e 1 escono esattamente al 50%, anche se la moneta è truccata.

È questo che fa un estrattore: <b>entra roba sbilanciata, esce roba perfettamente bilanciata</b>. Il prezzo è che si butta via una parte dei lanci: si ottengono <b>meno bit</b> di quanti se ne sono raccolti.

!!! note ""

    Questo trucco funziona solo se i lanci sono indipendenti tra loro. L'estrattore del corso (hash + seme) funziona con fonti molto più generali, ma l'idea è la stessa.

Come fanno Alice e Bob a ottenere <b>bit casuali</b>? È cruciale in crittografia:

- le <b>chiavi</b> devono essere <b>uniformi</b>
- la casualità servirà anche più avanti per la sicurezza (es. sicurezza <b>CPA</b>)

Si può pensare come un processo a più passi:

1. <b>Randomness extraction</b>: partendo da una sorgente di casualità <b>imperfetta</b>, generare casualità "pura" (uniforme).
2. <b>Espansione</b>: espandere in modo <b>deterministico</b> quello che si è estratto, quanto serve (<b>pseudocasualità</b>).
3. In più, un modo per <b>rinfrescare</b> la casualità, da poter espandere di nuovo.

Oggi ci occupiamo del passo 1.

<b>La domanda</b>: abbiamo una sorgente $X$ e vogliamo progettare una funzione <b>deterministica</b> $\text{Ext}$ tale che $\text{Ext}(X)$ sia <b>uniforme</b>.

È <b>impossibile in generale</b>: se $X$ è costante, anche $\text{Ext}(X)$ lo è. Serve che $X$ sia <b>imprevedibile</b> almeno in parte.

### Definizione: min-entropia

!!! abstract "In breve"

    La min-entropia misura quanto è imprevedibile una fonte, in bit. Min-entropia $k$ vuol dire che la fonte è difficile da indovinare quanto $k$ lanci di una moneta onesta, e quindi che se ne possono estrarre circa $k$ bit casuali.

La <b>min-entropia</b> di $X$ è

$$
H_\infty(X) = -\log \max_x \Pr[X = x]
$$

(logaritmo in base 2)

<b>Intuizione</b>: $\max_x \Pr[X = x]$ è la probabilità di indovinare $X$ al primo colpo puntando sul valore più probabile. La min-entropia misura quanto è difficile questo "miglior tentativo": se $H_\infty(X) = k$, il miglior tentativo riesce con probabilità $2^{-k}$. Più min-entropia c'è, meglio è.

!!! example ""

    <b>Esempi</b>:

    - $X = 0^n$ (costante): $\max \Pr = 1$, quindi $H_\infty(X) = -\log 1 = 0$

    - $X \equiv U_n$, cioè $X \leftarrow \{0,1\}^n$ uniforme: $\max \Pr = 2^{-n}$, quindi $H_\infty(X) = n$

    - <i>(non negli appunti del prof)</i> $X$ su 2 bit con $\Pr[00] = 1/2$ e gli altri tre valori a $1/6$: $H_\infty(X) = -\log(1/2) = 1$. Due bit di lunghezza, ma solo 1 bit di min-entropia, perché la sorgente è sbilanciata verso 00.

### A cosa serve la min-entropia

L'estrattore butta via una parte dei bit. La domanda naturale è: <b>quanti bit puliti si possono ottenere, al massimo?</b>

La min-entropia risponde proprio a questo: misura <b>quanti "bit puliti" ci sono nascosti dentro la fonte sporca</b>. Da una fonte con min-entropia $k$ si possono estrarre al massimo circa $k$ bit perfetti.

- <b>Moneta onesta</b>: ogni lancio vale 1 bit pulito. Min-entropia <b>1</b>.
- <b>Moneta piegata (testa al 60%)</b>: ogni lancio vale <b>meno</b> di un bit pulito, perché è un po' prevedibile. Min-entropia circa <b>0,74</b>.
- <b>Moneta che fa sempre testa</b>: ogni lancio vale <b>0</b> bit puliti. Non c'è niente da estrarre.

Quindi la min-entropia è il <b>"contenuto di casualità vera"</b> della fonte, e dice quanta roba l'estrattore può tirarne fuori.

### Come si calcola

La formula $-\log_2(p)$ si può riscrivere in un modo più comodo:

$$
H_\infty(X) = \log_2\!\left(\frac{1}{p}\right) \qquad p = \text{probabilità del risultato più probabile}
$$

Cioè: si fa 1 diviso la probabilità, e poi ci si chiede "2 elevato a quanto fa questo numero?" (è proprio quello che fa $\log_2$: ad esempio $\log_2 8 = 3$ perché $2^3 = 8$).

!!! example ""

    <b>Esempi</b>:

    - <b>Moneta onesta</b>, $p = 1/2$: $1/p = 2$, e $2^1 = 2$, quindi min-entropia <b>1</b>.
    - <b>Due monete oneste</b>, $p = 1/4$: $1/p = 4$, e $2^2 = 4$, quindi min-entropia <b>2</b>.
    - <b>Moneta piegata</b>, $p = 0{,}6$: $1/p \approx 1{,}67$. Siccome $2^0 = 1$ e $2^1 = 2$, la risposta sta tra 0 e 1; il conto preciso dà <b>0,74</b> (infatti $2^{0{,}74} \approx 1{,}67$).

<b>Con la calcolatrice</b> (che di solito ha solo $\ln$): $\log_2(x) = \ln(x) / \ln(2)$. Per la moneta piegata: $\ln(1{,}67) / \ln(2) \approx 0{,}511 / 0{,}693 \approx 0{,}74$.

<b>Tipicamente</b> si sa solo che $H_\infty(X) \ge k$ per qualche $k < n$, e si vuole estrarre quanta più casualità possibile.

### Teorema: estrattori deterministici impossibili

!!! abstract "In breve"

    Un estrattore fissato in anticipo può sempre essere fregato da una fonte costruita apposta contro di lui, anche se quella fonte è quasi perfettamente casuale.

!!! note ""

    <b>Notazione: cosa è cosa</b>

    - $\{0,1\}$ = l'insieme dei due bit possibili, 0 oppure 1: cioè <b>un singolo bit</b>.
    - $\{0,1\}^n$ = le <b>stringhe di</b> $n$ <b>bit</b>. Es. $\{0,1\}^3$ contiene 000, 001, …, 111 (8 stringhe). L'esponente dice quanti bit; senza esponente è uno solo.
    - $\to$ = "restituisce": a sinistra cosa entra nella funzione, a destra cosa esce.
    - $\times$ = "e": la funzione prende <b>due</b> input insieme.

    Quindi $\text{Ext}: \{0,1\}^n \to \{0,1\}$ si legge: <i>"Ext prende una stringa di</i> $n$ <i>bit (quella della fonte) e restituisce un solo bit"</i>. Es. con $n = 3$ e Ext = "prendi il primo bit": $\text{Ext}(101) = 1$.
    Nella versione con il seme, $\text{Ext}: \{0,1\}^d \times \{0,1\}^n \to \{0,1\}^\ell$ si legge: <i>"entra un seme di</i> $d$ <i>bit e una stringa della fonte di</i> $n$ <i>bit, escono</i> $\ell$ <i>bit puliti"</i>.

<b>Perché un solo bit in output</b>: si sceglie l'obiettivo più facile possibile. Se non si riesce a estrarre nemmeno 1 bit pulito, a maggior ragione non si riesce con di più: così il risultato negativo è il più forte possibile.

Non esiste nessun $\text{Ext}: \{0,1\}^n \to \{0,1\}$ che funzioni per tutte le sorgenti con $H_\infty(X) \ge k$, <b>nemmeno</b> con $k = n - 1$ (e nemmeno per estrarre un solo bit).

### Dimostrazione

Prendiamo un qualunque $\text{Ext}: \{0,1\}^n \to \{0,1\}$.

Sia $b \in \{0,1\}$ il bit che <b>massimizza</b> $|\text{Ext}^{-1}(b)|$, cioè il bit con più preimmagini.

```text
 {0,1}^n
┌───────────────┐
│  x  x  x  x  │ ───→  0
│───────────────│
│  x  x  x     │ ───→  1
└───────────────┘
```

Le due preimmagini $\text{Ext}^{-1}(0)$ e $\text{Ext}^{-1}(1)$ si spartiscono tutte le $2^n$ stringhe, quindi la più grande ne contiene almeno metà:

$$
|\text{Ext}^{-1}(b)| \ge 2^{n-1}
$$

Sia $X_{\text{BAD}}$ uniforme su $\text{Ext}^{-1}(b)$.

- Ogni valore ha probabilità $1/|\text{Ext}^{-1}(b)| \le 2^{-(n-1)}$, quindi $H_\infty(X_{\text{BAD}}) \ge n - 1$
- <b>ma</b> $\text{Ext}(X_{\text{BAD}}) = b$ è <b>costante</b>! ∎

<b>Intuizione</b>: qualunque estrattore fissato ha un "punto debole". Basta una sorgente cattiva che peschi solo dagli input che finiscono nello stesso output.

### Takeaway

Nessun $\text{Ext}$ deterministico può funzionare per <b>tutte</b> le sorgenti con min-entropia. Approcci possibili:

- <b>Più sorgenti indipendenti</b>: <i>2-source extractors</i>.
- <b>Strumenti crittografici</b> (es. funzioni hash): ma servono ipotesi forti su queste funzioni.
- <b>Seeded extraction</b>: è quello che vediamo nel corso.

## Seeded extraction

!!! abstract "In breve"

    Invece di fissare l'estrattore, lo si sceglie a caso tra tantissimi usando un <b>seme</b> pubblico. Così nessuna fonte può essere costruita apposta contro l'estrattore che verrà usato.

<b>Idea</b>: invece di un solo estrattore, una <b>famiglia</b> di estrattori, indicizzata da un <b>seed</b> (seme):

$$
\text{Ext}: \underbrace{\{0,1\}^d}_{\text{seed}} \times \underbrace{\{0,1\}^n}_{\text{sorgente}} \to \underbrace{\{0,1\}^\ell}_{\text{output}}
$$

Il seed sarà <b>casuale</b>. Perché non è barare (usare casualità per produrre casualità)?

- Il seed è un <b>catalizzatore</b> corto: l'output può essere più lungo.
- Il seed è <b>pubblico</b> (l'avversario lo conosce!) e <b>riutilizzabile</b>.

### Definizione: estrattore con seed

!!! abstract "In breve"

    Un $(k, \varepsilon)$-estrattore trasforma <b>ogni</b> fonte con min-entropia almeno $k$ in bit che, presi insieme al seme, sono quasi indistinguibili da bit perfettamente casuali (a meno di un errore $\varepsilon$).

$\text{Ext}: \{0,1\}^d \times \{0,1\}^n \to \{0,1\}^\ell$ è un $(k, \varepsilon)$<b>-seeded extractor</b> se per ogni $X$ con $H_\infty(X) \ge k$:

$$
(S, \text{Ext}(S, X)) \approx_\varepsilon (S, U_\ell) \ \equiv U_{d+\ell}
$$

dove $S \leftarrow U_d$ (seed uniforme).

<b>Significato di</b> $\approx_\varepsilon$: ogni avversario $A$, anche con <b>potenza illimitata</b>, distingue $(S, \text{Ext}(S, X))$ da $U_{d+\ell}$ con probabilità (vantaggio) al più $\varepsilon$.

<b>Nota</b>: il seed $S$ compare <b>insieme</b> all'output. È questo che formalizza "il seed è pubblico": l'output deve sembrare uniforme anche a chi conosce il seed.

### Distanza statistica

!!! abstract "In breve"

    La distanza statistica è un numero tra 0 e 1 che dice quanto due distribuzioni sono diverse. È il massimo vantaggio con cui chiunque, anche con potenza infinita, riesce a distinguerle.

$$
X \approx_\varepsilon Y \iff \text{SD}(X; Y) \le \varepsilon
$$

$$
\text{SD}(X; Y) = \frac{1}{2} \sum_z \Big| \Pr[X = z] - \Pr[Y = z] \Big|
$$

!!! note ""

    <b>Cosa sono le variabili</b>

    - $X$, $Y$ = due <b>distribuzioni</b>, cioè due modi di generare valori a caso (es. due monete).
    - $z$ = <b>un valore possibile</b> (per una moneta: 1 o 0).
    - $\Pr[X = z]$ = la probabilità che $X$ dia il valore $z$; idem $\Pr[Y = z]$.
    - $|\dots - \dots|$ = di quanto differiscono le due probabilità su quel valore (sempre positivo).
    - $\sum_z$ = "somma su tutti i valori $z$ possibili": si fa il conto per ogni valore e si sommano i risultati.
    - $\frac{1}{2}$ = si divide per 2, perché quello che una distribuzione ha in più su un valore lo ha in meno su un altro (le probabilità sommano sempre a 1): senza il ½ la stessa differenza verrebbe contata due volte. Così la SD sta sempre tra 0 e 1.
    - $\text{SD}(X; Y)$ = la <b>distanza statistica</b>, il numero che esce dalla formula.
    - $\varepsilon$ = l'errore massimo che si accetta (un numero piccolo).
    - $X \approx_\varepsilon Y$ = "X e Y sono quasi uguali, con errore al massimo $\varepsilon$".
    - $\iff$ = "se e solo se", cioè "è la stessa cosa di". La prima formula è quindi solo la definizione del simbolo $\approx_\varepsilon$.

<b>Intuizione</b>: misura quanto due distribuzioni sono diverse. Vale 0 se sono identiche, 1 se non hanno valori in comune.

!!! example ""

    <b>Esempio</b> <i>(non negli appunti del prof)</i>: moneta truccata $X$ con $\Pr[1] = 0{,}6$ contro moneta onesta $Y$:
    $\text{SD} = \frac{1}{2}(|0{,}6 - 0{,}5| + |0{,}4 - 0{,}5|) = 0{,}1$

## Leftover Hash Lemma (LHL)

!!! abstract "In breve"

    Il <b>Leftover Hash Lemma</b> è il teorema che risponde alla domanda "come si costruisce un estrattore con seme?". La risposta: basta una famiglia di hash pairwise independent. Il seme sceglie la hash, la si applica alla fonte e si ottengono bit quasi perfettamente casuali, purché la fonte abbia un po' più min-entropia dei bit che si vogliono estrarre. Il nome viene da <i>leftover</i> (avanzo): la casualità che "avanza" in una fonte imperfetta si trasforma con una hash in bit puliti.

### Teorema

Sia $\mathcal{H} = \{h_s : \{0,1\}^n \to \{0,1\}^\ell\}_{s \in \{0,1\}^d}$ <b>pairwise independent</b>. Allora

$$
\text{Ext}(s, x) = h_s(x)
$$

è un $(k, \varepsilon)$-seeded extractor per

$$
k \ge \ell + \underbrace{2\log(1/\varepsilon) - 2}_{\text{min-entropy gap}}
$$

<b>Cosa vuol dire</b> $\text{Ext}(s, x) = h_s(x)$: il seme $s$ sceglie quale funzione hash usare, e la si applica al valore $x$ della fonte. L'output della hash sono i bit puliti.

!!! example ""

    <b>Esempio</b> con $h(x) = a \cdot x + b \bmod 7$: il seme è la coppia $s = (a, b)$, per esempio $(3, 5)$. Se la fonte dà $x = 2$, l'output è $3 \cdot 2 + 5 = 11 \bmod 7 = 4$. Nei MAC la coppia $(a, b)$ era la <b>chiave segreta</b>, qui è il <b>seme pubblico</b>: stesse funzioni, ruolo diverso.

<b>Intuizione</b>: per estrarre $\ell$ bit quasi uniformi servono un po' più di $\ell$ bit di min-entropia. Il "prezzo" è il <b>min-entropy gap</b>, che cresce se vogliamo $\varepsilon$ più piccolo.

!!! example ""

    <b>Esempio</b> <i>(non negli appunti del prof)</i>: per estrarre $\ell = 128$ bit con $\varepsilon = 2^{-64}$ serve $k \ge 128 + 128 - 2 = 254$ bit di min-entropia.

### Collision probability e lemma

!!! abstract "In breve"

    La collision probability è la probabilità che due estrazioni indipendenti diano lo stesso valore. L'uniforme è la distribuzione che collide di meno, e il lemma dice che se una distribuzione collide quasi quanto l'uniforme, allora è quasi uniforme.

La dimostrazione usa la <b>probabilità di collisione</b> di una variabile aleatoria $Y$ su un insieme $\mathcal{Y}$:

$$
\text{Col}(Y) = \sum_{y \in \mathcal{Y}} \Pr[Y = y]^2 = \Pr[Y = Y']
$$

dove $Y'$ è una <b>copia indipendente</b> di $Y$: è la probabilità che due estrazioni indipendenti diano lo stesso valore. La distribuzione uniforme ha la collision probability più bassa possibile, $1/|\mathcal{Y}|$.

<b>Lemma</b>: se

$$
\text{Col}(Y) \le \frac{1}{|\mathcal{Y}|}(1 + 4\varepsilon^2)
$$

allora $\text{SD}(Y; U) \le \varepsilon$, con $U$ uniforme su $\mathcal{Y}$.

<b>Intuizione</b>: se la collision probability è quasi quella dell'uniforme, allora $Y$ è quasi uniforme.

??? note "Dimostrazione del lemma (il prof la fa all'inizio della Lezione 4: lì c'è la versione completa, passo per passo)"

    Sia $N = |\mathcal{Y}|$ e $p_y = \Pr[Y = y]$. Per Cauchy-Schwarz ($\sum |a_y| \le \sqrt{N \sum a_y^2}$):

    $\text{SD}(Y; U) = \frac{1}{2}\sum_y |p_y - 1/N| \le \frac{1}{2}\sqrt{N \sum_y (p_y - 1/N)^2}$

    Sviluppando il quadrato: $\sum_y (p_y - 1/N)^2 = \sum_y p_y^2 - \frac{2}{N}\sum_y p_y + \frac{1}{N} = \text{Col}(Y) - \frac{1}{N} \le \frac{4\varepsilon^2}{N}$

    Quindi $\text{SD}(Y; U) \le \frac{1}{2}\sqrt{N \cdot 4\varepsilon^2 / N} = \varepsilon$. ∎

### Dimostrazione del LHL

!!! abstract "In breve"

    Si contano le collisioni dell'output. Ci sono quelle "per caso", che ci sono anche nell'uniforme, e quelle dovute alla fonte che ripete lo stesso valore, che sono poche grazie alla min-entropia. Quindi l'output collide quasi quanto l'uniforme e, per il lemma, è quasi uniforme.

Poniamo $Y = (S, h(S, X))$, e sia $Y' = (S', h(S', X'))$ una copia indipendente. Calcoliamo la collision probability:

$$
\begin{aligned}
\text{Col}(Y) &= \Pr[Y = Y'] \\
&= \Pr[S = S' \wedge h(S, X) = h(S', X')] \\
&= \Pr[S = S' \wedge h(S, X) = h(S, X')] \\
&= \underbrace{\Pr[S = S']}_{\text{Col}(S) \,=\, 2^{-d}} \cdot \Pr[h(S, X) = h(S, X')]
\end{aligned}
$$

- <b>3° passaggio</b>: se $S = S'$, possiamo sostituire $S'$ con $S$.
- <b>4° passaggio</b>: i seed sono indipendenti dalle sorgenti, quindi le due probabilità si separano. $S$ è uniforme su $2^d$ valori, quindi $\text{Col}(S) = 2^{-d}$.

Ora spezziamo in due casi, $X = X'$ oppure $X \ne X'$:

$$
\begin{aligned}
&= 2^{-d} \Big( \Pr[X = X'] \cdot 1 + \Pr[h(S, X) = h(S, X') \wedge X \ne X'] \Big) \\
&\le 2^{-d} \Big( 2^{-k} + \Pr[h(S, X) = h(S, X') \wedge X \ne X'] \Big) \\
&\le 2^{-d} \Big( 2^{-k} + 2^{-\ell} \Big)
\end{aligned}
$$

- <b>Primo termine</b>: se $X = X'$ gli hash coincidono sicuramente (probabilità 1). E $\Pr[X = X'] = \sum_x \Pr[X = x]^2 \le \max_x \Pr[X = x] \cdot \sum_x \Pr[X = x] \le 2^{-k}$, perché $H_\infty(X) \ge k$.
- <b>Secondo termine</b>: per input diversi $x \ne x'$, per pairwise independence $\Pr_S[h_S(x) = h_S(x')] = 2^\ell \cdot 2^{-2\ell} = 2^{-\ell}$ (le coppie $(t, t)$ con valori uguali sono $2^\ell$, ognuna con probabilità $2^{-2\ell}$).

Raccogliendo $2^{-\ell}$:

$$
\begin{aligned}
&= \frac{1}{2^{d+\ell}} \Big( 2^{\ell - k} + 1 \Big) \\
&\le \frac{1}{|\mathcal{Y}|} \Big( 2^{2 - 2\log(1/\varepsilon)} + 1 \Big) \\
&= \frac{1}{|\mathcal{Y}|} \Big( 1 + 4\varepsilon^2 \Big)
\end{aligned}
$$

- $|\mathcal{Y}| = 2^{d+\ell}$ perché $Y$ è una stringa di $d + \ell$ bit.
- Dall'ipotesi $k \ge \ell + 2\log(1/\varepsilon) - 2$ segue $\ell - k \le 2 - 2\log(1/\varepsilon)$.
- $2^{2 - 2\log(1/\varepsilon)} = 4 \cdot (2^{\log(1/\varepsilon)})^{-2} = 4\varepsilon^2$.

Per il lemma: $\text{SD}(Y; U) \le \varepsilon$, cioè $(S, h(S, X)) \approx_\varepsilon U_{d+\ell}$. ∎

## Riepilogo

- $h_{a,b}(m) = am + b \bmod p$ è pairwise independent: il sistema lineare ha una sola soluzione perché $m \ne m'$
- Ogni famiglia pairwise independent dà un MAC ε-sicuro con $\varepsilon = 1/|\mathcal{T}|$ (ottimo)
- <b>Bad news</b>: un MAC t-time $2^{-\lambda}$-sicuro richiede chiavi di $(t+1)\lambda$ bit
- <b>Min-entropia</b> $H_\infty(X) = -\log \max_x \Pr[X = x]$: quanto è difficile indovinare $X$ al primo colpo
- Nessun estrattore <b>deterministico</b> funziona per tutte le sorgenti, nemmeno con $k = n - 1$ e un solo bit di output
- <b>Seeded extractor</b>: con un seed casuale, corto e <b>pubblico</b>, $(S, \text{Ext}(S, X)) \approx_\varepsilon U_{d+\ell}$
- <b>Distanza statistica</b> $\text{SD}$: misura quanto due distribuzioni differiscono
- <b>Leftover Hash Lemma</b>: hash pairwise independent sono estrattori, se $k \ge \ell + 2\log(1/\varepsilon) - 2$
