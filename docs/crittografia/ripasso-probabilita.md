# Ripasso di probabilità di base

## 1. Le basi

<b>Spazio campionario</b> $\Omega$: l'insieme di tutti i risultati possibili di un esperimento casuale.

<b>Evento</b> $A$: un sottoinsieme di $\Omega$, cioè un gruppo di risultati che ci interessa.

!!! example ""

    Esempio: lanci un dado. $\Omega = \{1,2,3,4,5,6\}$. L'evento "esce pari" è $A = \{2,4,6\}$.

### Assiomi

- $0 \le \Pr[A] \le 1$: una probabilità sta sempre tra 0 (impossibile) e 1 (certo)
- $\Pr[\Omega] = 1$: qualcosa succede di sicuro
- se $A$ e $B$ sono <b>disgiunti</b> (non possono succedere insieme): $\Pr[A \cup B] = \Pr[A] + \Pr[B]$

!!! example ""

    Esempio: dado. "Esce 1" e "esce 2" sono disgiunti, quindi $\Pr[\text{1 o 2}] = 1/6 + 1/6 = 1/3$.

### Distribuzione uniforme

Tutti i risultati hanno la stessa probabilità. Allora:

$$
\Pr[A] = \frac{|A|}{|\Omega|} = \frac{\text{casi favorevoli}}{\text{casi possibili}}
$$

!!! example ""

    Esempio: pesco una carta da un mazzo da 52. $\Pr[\text{asso}] = 4/52 = 1/13$.

### Complementare

$$
\Pr[\neg A] = 1 - \Pr[A]
$$

Utilissimo quando "almeno una volta" è difficile da contare ma "mai" è facile.

!!! example ""

    Esempio: lanci un dado 4 volte. Probabilità di almeno un 6?

    Contare direttamente è scomodo (un 6, due 6, ...). Il complementare è "nessun 6": ogni lancio non dà 6 con prob. $5/6$, quindi

    $\Pr[\text{almeno un 6}] = 1 - (5/6)^4 = 1 - 625/1296 \approx 0{,}518$

### Unione di eventi non disgiunti

$$
\Pr[A \cup B] = \Pr[A] + \Pr[B] - \Pr[A \cap B]
$$

Si sottrae l'intersezione perché altrimenti la conti due volte.

!!! example ""

    Esempio: pesco una carta. Probabilità che sia di cuori <b>o</b> una figura (J, Q, K)?

    $\Pr[\text{cuori}] = 13/52$, $\Pr[\text{figura}] = 12/52$, $\Pr[\text{figura di cuori}] = 3/52$

    $\Pr = 13/52 + 12/52 - 3/52 = 22/52 \approx 0{,}42$

## 2. Union bound

$$
\Pr[A_1 \cup \dots \cup A_m] \le \sum_{i=1}^{m} \Pr[A_i]
$$

Vale <b>sempre</b>, anche se gli eventi non sono disgiunti: sommare le probabilità al massimo sovrastima (perché conti più volte le intersezioni). Si usa quando il valore esatto è difficile ma basta un limite superiore.

!!! example ""

    Esempio: hai 3 lampadine, ognuna si brucia entro l'anno con probabilità 1%. La probabilità che <b>almeno una</b> si bruci è al più $3 \times 1\% = 3\%$.

    Il valore esatto (se sono indipendenti) è $1 - 0{,}99^3 \approx 2{,}97\%$: il bound è molto vicino.

## 3. Probabilità condizionata e indipendenza

### Probabilità condizionata

Con $\Pr[B] > 0$:

$$
\Pr[A \mid B] = \frac{\Pr[A \cap B]}{\Pr[B]}
$$

Si legge "probabilità di $A$ sapendo che è successo $B$". In pratica: restringi il mondo ai soli casi in cui vale $B$, e guardi quanti di quelli soddisfano anche $A$.

!!! example ""

    Esempio: lanci un dado e un amico ti dice "è uscito un numero pari". Probabilità che sia 6?

    $\Pr[6 \mid \text{pari}] = \dfrac{\Pr[6]}{\Pr[\text{pari}]} = \dfrac{1/6}{1/2} = \dfrac{1}{3}$

    Ha senso: i casi possibili sono ora solo $\{2,4,6\}$, e uno su tre è il 6.

### Indipendenza

$A$ e $B$ sono <b>indipendenti</b> se

$$
\Pr[A \cap B] = \Pr[A] \cdot \Pr[B]
$$

che equivale a $\Pr[A \mid B] = \Pr[A]$: sapere che è successo $B$ non cambia nulla su $A$.

!!! example ""

    Esempio sì: lanci due monete. "Prima testa" e "seconda testa" sono indipendenti: $\Pr[\text{TT}] = 1/2 \cdot 1/2 = 1/4$.

    Esempio no: peschi due carte <b>senza rimetterle</b>. $\Pr[\text{1ª asso}] = 4/52$, ma $\Pr[\text{2ª asso} \mid \text{1ª asso}] = 3/51$: la prima pescata cambia la seconda.

    Esempio sorprendente: dado, $A$ = "pari" $= \{2,4,6\}$, $B$ = "al massimo 4" $= \{1,2,3,4\}$.

    $\Pr[A \cap B] = \Pr[\{2,4\}] = 2/6 = 1/3$ e $\Pr[A]\Pr[B] = 1/2 \cdot 2/3 = 1/3$. Sono indipendenti anche se riguardano lo stesso dado!

<b>Attenzione</b>: disgiunti ≠ indipendenti. Due eventi disgiunti con probabilità positiva sono anzi <b>dipendenti</b>: se succede uno, l'altro è impossibile.

### Probabilità totale

Se $B_1, \dots, B_m$ partizionano $\Omega$ (coprono tutti i casi e non si sovrappongono):

$$
\Pr[A] = \sum_{i} \Pr[A \mid B_i]\,\Pr[B_i]
$$

Cioè: spezzi il problema in casi, calcoli ogni caso e fai la media pesata.

!!! example ""

    Esempio: hai due urne. Urna 1: 3 palline rosse e 2 blu. Urna 2: 1 rossa e 4 blu. Lanci una moneta per scegliere l'urna, poi peschi una pallina.

    $\Pr[\text{rossa}] = \Pr[\text{rossa} \mid U_1]\Pr[U_1] + \Pr[\text{rossa} \mid U_2]\Pr[U_2] = \tfrac{3}{5}\cdot\tfrac{1}{2} + \tfrac{1}{5}\cdot\tfrac{1}{2} = 0{,}4$

### Teorema di Bayes

$$
\Pr[A \mid B] = \frac{\Pr[B \mid A]\,\Pr[A]}{\Pr[B]}
$$

Serve a "invertire" la condizionata: conosci $\Pr[B \mid A]$ ma ti interessa $\Pr[A \mid B]$.

!!! example ""

    Esempio (il classico test medico): una malattia colpisce l'1% della popolazione. Il test è positivo nel 99% dei malati, ma dà anche un 5% di falsi positivi sui sani. Fai il test ed è positivo: che probabilità hai di essere malato?

    Prima $\Pr[\text{pos}]$ con la probabilità totale:

    $\Pr[\text{pos}] = 0{,}99 \cdot 0{,}01 + 0{,}05 \cdot 0{,}99 = 0{,}0099 + 0{,}0495 = 0{,}0594$

    Poi Bayes:

    $\Pr[\text{malato} \mid \text{pos}] = \dfrac{0{,}99 \cdot 0{,}01}{0{,}0594} \approx 0{,}167$

    Solo il 17% circa! Il motivo: i sani sono tantissimi, quindi anche un 5% di falsi positivi su di loro supera di molto i veri positivi.

## 4. Variabili aleatorie e valore atteso

### Variabile aleatoria

Una <b>variabile aleatoria</b> $X$ è una funzione $\Omega \to \mathbb{R}$: associa un numero a ogni risultato dell'esperimento.

!!! example ""

    Esempio: lanci due dadi, $X$ = somma dei due. Se esce (3, 5), $X = 8$. $\Pr[X = 2] = 1/36$ (solo (1,1)), $\Pr[X = 7] = 6/36$ (sei combinazioni).

### Valore atteso

$$
\mathbb{E}[X] = \sum_x x \cdot \Pr[X = x]
$$

È la media dei valori pesata con le loro probabilità: il risultato "medio" se ripeti l'esperimento tantissime volte.

!!! example ""

    Esempio: un dado. $\mathbb{E}[X] = (1+2+3+4+5+6)/6 = 3{,}5$. Non esce mai 3,5, ma è la media a lungo andare.

    Esempio (scommessa): paghi 1 € per giocare, se esce 6 vinci 5 €. Il guadagno netto $X$ vale $+4$ con prob. $1/6$ e $-1$ con prob. $5/6$.

    $\mathbb{E}[X] = 4 \cdot \tfrac{1}{6} - 1 \cdot \tfrac{5}{6} = -\tfrac{1}{6} \approx -0{,}17$ €. In media perdi 17 centesimi a giocata.

### Linearità del valore atteso

$$
\mathbb{E}[X + Y] = \mathbb{E}[X] + \mathbb{E}[Y] \qquad \mathbb{E}[aX] = a\,\mathbb{E}[X]
$$

Vale <b>sempre</b>, anche se $X$ e $Y$ non sono indipendenti.

!!! example ""

    Esempio: somma di due dadi. Invece di fare la tabella 6×6: $\mathbb{E}[X_1 + X_2] = 3{,}5 + 3{,}5 = 7$.

### Variabili indicatrici

$X_A = 1$ se l'evento $A$ succede, $0$ altrimenti. Allora $\mathbb{E}[X_A] = \Pr[A]$.

Combinate con la linearità servono a <b>contare</b> quante volte succede qualcosa in media: scrivi il conteggio come somma di indicatrici.

!!! example ""

    Esempio: lanci 10 monete. Numero medio di teste? $X = X_1 + \dots + X_{10}$ dove $X_i = 1$ se la moneta $i$ dà testa. $\mathbb{E}[X] = 10 \cdot 1/2 = 5$.

    Esempio (guardaroba): $n$ persone lasciano il cappello, che vengono restituiti a caso. Quante persone in media riavranno il proprio?

    $X_i = 1$ se la persona $i$ riprende il suo: $\Pr = 1/n$. Quindi $\mathbb{E}[X] = n \cdot 1/n = 1$, <b>qualunque sia</b> $n$. Le $X_i$ non sono indipendenti, ma la linearità funziona lo stesso.

### Variabili indipendenti

$X$ e $Y$ sono indipendenti se $\Pr[X=x \wedge Y=y] = \Pr[X=x]\Pr[Y=y]$ per ogni $x, y$. In tal caso vale (senza indipendenza in generale no):

$$
\mathbb{E}[XY] = \mathbb{E}[X]\,\mathbb{E}[Y]
$$

!!! example ""

    Esempio: prodotto di due dadi lanciati separatamente: $\mathbb{E}[X_1 X_2] = 3{,}5 \cdot 3{,}5 = 12{,}25$.

    Controesempio: $X$ = un dado, $Y = X$ (lo stesso dado). $\mathbb{E}[X \cdot X] = (1+4+9+16+25+36)/6 \approx 15{,}17 \ne 12{,}25$.
