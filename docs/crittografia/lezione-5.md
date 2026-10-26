# Lezione 5 – Pseudocasualità, PRG e hard-core bit

<i>Segue gli appunti del prof. Le parti aggiunte per capire meglio sono segnate "non negli appunti del prof". Usa i concetti della Lezione 4: avversario PPT, funzioni trascurabili, one-way function.</i>

## Pseudocasualità

!!! abstract "In breve"

    Una funzione <b>pseudocasuale</b> è una funzione <b>deterministica</b> che prende una stringa uniforme (corta) e restituisce <b>tanti bit</b> che "sembrano" casuali. "Sembrano" ha un significato preciso: <b>nessun avversario PPT riesce a distinguerli da bit davvero casuali</b>, se non con probabilità trascurabile.

<b>Il collegamento con la lezione 3</b> <i>(non negli appunti del prof)</i>: l'estrattore tira fuori pochi bit puliti da una fonte sporca; la funzione pseudocasuale li usa come seme e ne genera quanti ne servono. È il passo 2 ("espansione") visto nella lezione 3.

```text
fonte sporca → [Estrattore] → seme (pochi bit casuali) → [PRG] → tanti bit pseudocasuali
```

## Indistinguibilità computazionale

!!! abstract "In breve"

    Due distribuzioni sono <b>computazionalmente indistinguibili</b> ($\approx_c$) se nessun avversario PPT riesce a capire da quale delle due viene un campione, se non con vantaggio trascurabile. È la versione "per avversari efficienti" della distanza statistica della lezione 3.

### Ensemble di distribuzioni

Con la sicurezza computazionale tutto dipende dal parametro $\lambda$ (più è grande, più l'avversario fatica). Per questo non si confrontano due distribuzioni singole, ma due <b>famiglie</b> di distribuzioni, una per ogni valore di $\lambda$:

$$
X = \{X_\lambda\}_{\lambda \in \mathbb{N}} \qquad Y = \{Y_\lambda\}_{\lambda \in \mathbb{N}}
$$

!!! note ""

    <b>Cosa vuol dire</b> <i>(non negli appunti del prof)</i>: $X_\lambda$ è un modo di generare stringhe casuali che dipende da $\lambda$. Una famiglia così si chiama <b>ensemble</b>. Esempio: $\{U_\lambda\}$, dove $U_\lambda$ è la distribuzione <b>uniforme</b> su stringhe di $\lambda$ bit ($U_1$ su 1 bit, $U_2$ su 2 bit, …).

### Definizione (del prof)

$X \approx_c Y$ se per ogni avversario PPT $A$:

$$
\Big| \Pr[A(X_\lambda) = 1] - \Pr[A(Y_\lambda) = 1] \Big| \le \text{negl}(\lambda)
$$

dove $\Pr[A(X_\lambda) = 1]$ è un'abbreviazione per $\Pr[A(z) = 1 : z \leftarrow X_\lambda]$.

!!! note ""

    <b>Cosa sono le cose</b>

    - $A$ = un programma efficiente (il <b>distinguisher</b>) che riceve una stringa $z$ e risponde 1 ("secondo me viene da $Y$") o 0 ("secondo me viene da $X$"). È l'assaggiatore alla cieca.
    - $z \leftarrow X_\lambda$ = "$z$ è estratta dalla distribuzione $X_\lambda$".
    - $\Pr[A(z) = 1 : z \leftarrow X_\lambda]$ = quanto spesso $A$ risponde 1 quando la stringa viene da $X$. I due punti si leggono "nella situazione in cui".
    - La differenza in valore assoluto è il <b>vantaggio</b> di $A$: quanto cambia il suo comportamento a seconda della provenienza della stringa.
    - $\le \text{negl}(\lambda)$ = il vantaggio deve essere trascurabile, e questo per <b>ogni</b> $A$ PPT.

!!! example ""

    <b>Esempi di vantaggio</b> <i>(non negli appunti del prof)</i>: $A$ dice 1 il 50% delle volte con $X$ e il 50% con $Y$: vantaggio 0, non distingue. $A$ dice 1 il 10% con $X$ e il 90% con $Y$: vantaggio 0,8, distingue benissimo.

### La stessa cosa come gioco

$\text{GAME}(\lambda, b)$, con $b \in \{0, 1\}$:

```text
Avversario A                          Challenger C
                                      se b = 0: z ← X_λ
                                      se b = 1: z ← Y_λ
      ←──────────── z ─────────────
      ──────── b' ∈ {0,1} ─────────→
```

Il challenger estrae $z$ da $X_\lambda$ (se $b = 0$) o da $Y_\lambda$ (se $b = 1$) e lo dà ad $A$, che risponde con $b'$. La definizione diventa:

$$
\{\text{GAME}(\lambda, 0)\} \approx_c \{\text{GAME}(\lambda, 1)\}
$$

cioè la risposta di $A$ ha (quasi) la stessa distribuzione nei due giochi. È lo stesso schema di GAME(0)/GAME(1) della lezione 2.

### Esempio concreto: due macchine

<i>(Non negli appunti del prof.)</i>

<b>Lo scenario.</b> Ci sono due "macchine" che producono stringhe di bit: la macchina $X$ (es. l'uscita di un generatore pseudocasuale) e la macchina $Y$ (es. bit davvero casuali). Ad $A$ viene data <b>una</b> stringa e deve dire da quale macchina viene: risponde 1 ("viene da $Y$") o 0 ("viene da $X$"). La domanda è: <b>esiste un </b>$A$<b> che si comporta in modo diverso a seconda della macchina da cui arriva la stringa?</b>

<b>Caso 1: un generatore scarso.</b>

- Macchina $X$: produce 2 bit, ma sempre <b>uguali</b> tra loro: 00 oppure 11, metà e metà.
- Macchina $Y$: produce 2 bit davvero casuali: 00, 01, 10, 11, ognuno al 25%.
- Regola di $A$: <b>"rispondi 1 se i due bit sono diversi"</b>.

Quanto spesso $A$ risponde 1?

- Se la stringa viene da $X$: i bit sono sempre uguali, quindi <b>mai</b>: $\Pr[A(z) = 1 : z \leftarrow X] = 0$
- Se la stringa viene da $Y$: i bit sono diversi in 01 e 10, metà dei casi: $\Pr[A(z) = 1 : z \leftarrow Y] = 1/2$

<b>Vantaggio</b> $= |0 - 1/2| = 1/2$. $A$ si comporta in modo molto diverso nei due casi, quindi <b>distingue</b> le due macchine: questo generatore <b>non</b> è indistinguibile da bit casuali ($X \not\approx_c Y$).

<b>Caso 2: un generatore buono.</b> Ora $X$ è un buon PRG. Qualunque regola efficiente $A$ provi, risponde 1 <b>quasi con la stessa frequenza</b> nei due casi, ad esempio:

- $\Pr[A \text{ risponde } 1 \text{ con } X] = 0{,}5000000001$
- $\Pr[A \text{ risponde } 1 \text{ con } Y] = 0{,}5$

Il vantaggio è $0{,}0000000001$, trascurabile. Se questo vale per <b>ogni</b> $A$ efficiente, allora $X \approx_c Y$.

<b>La formula letta in italiano</b>: <i>"per ogni programma efficiente</i> $A$<i>, la frequenza con cui</i> $A$ <i>dice 1 sulle stringhe di</i> $X$ <i>e quella con cui dice 1 sulle stringhe di</i> $Y$ <i>differiscono di una quantità trascurabile"</i>. $\lambda$ è la lunghezza delle stringhe: il vantaggio deve diventare trascurabile al crescere di $\lambda$.

<b>Il gioco è la stessa cosa</b>: il challenger tira una moneta $b$; se $b = 0$ prende la stringa dalla macchina $X$, se $b = 1$ dalla macchina $Y$, e la dà ad $A$, che risponde $b'$ (il suo tentativo di indovinare $b$). "GAME(λ, 0) ≈c GAME(λ, 1)" vuol dire che $A$ dice 1 con quasi la stessa frequenza sia quando la stringa viene da $X$ sia quando viene da $Y$: è esattamente la formula. Nella Lezione 2 le due macchine erano "cifra $m_0$" e "cifra $m_1$".

### Statistica vs computazionale

<i>(Non negli appunti del prof.)</i>

|  | Statistica (lezione 3) | Computazionale |
| --- | --- | --- |
| Simbolo | $X \approx_\varepsilon Y$ | $X \approx_c Y$ |
| Chi prova a distinguere | Chiunque, anche con potenza infinita | Solo avversari PPT |
| Vantaggio ammesso | Al più un numero fissato ε | Una funzione trascurabile di λ |

L'indistinguibilità computazionale è <b>più debole</b>: due distribuzioni possono essere molto diverse statisticamente, ma nessun avversario efficiente riesce ad accorgersene. È proprio questo che rende possibili i PRG.

## Pseudorandom generator (PRG)

!!! abstract "In breve"

    Un <b>PRG</b> è una funzione deterministica che prende un seme casuale di $\lambda$ bit e restituisce $\lambda + \ell$ bit, cioè <b>più</b> bit di quanti ne ha ricevuti, in modo che l'uscita sia computazionalmente indistinguibile da bit davvero casuali.

### Definizione (del prof)

Una funzione $G : \{0,1\}^\lambda \to \{0,1\}^{\lambda + \ell}$, con $\ell > 0$, è un <b>PRG (sicuro)</b> se

$$
\{X_\lambda\} = \{G(U_\lambda)\}_\lambda \ \approx_c \ \{U_{\lambda + \ell}\}_\lambda = \{Y_\lambda\}
$$

!!! note ""

    <b>Cosa sono le cose</b>

    - $U_\lambda$ = un seme di $\lambda$ bit scelto <b>uniformemente a caso</b>.
    - $G(U_\lambda)$ = la distribuzione che si ottiene scegliendo un seme a caso e applicandogli $G$: escono $\lambda + \ell$ bit.
    - $U_{\lambda + \ell}$ = $\lambda + \ell$ bit davvero casuali.
    - $\ell$ = lo <b>stretch</b> ("allungamento"): quanti bit in più escono rispetto al seme.
    - In parole: nessun avversario PPT distingue l'uscita di $G$ da bit davvero casuali.
    - <i>(Non negli appunti del prof)</i>: si intende anche che $G$ sia calcolabile in tempo polinomiale, altrimenti non servirebbe a niente.

<b>Notare</b> <i>(non negli appunti del prof)</i>: $G$ è <b>deterministica</b> (stesso seme, stessa uscita). Tutta la casualità viene dal seme; $G$ la "stira" su più bit.

### Esercizio: nessun PRG è sicuro contro attaccanti illimitati

!!! abstract "In breve"

    Un PRG può essere sicuro <b>solo</b> contro avversari efficienti. Un avversario con potenza infinita lo rompe sempre, anche se il PRG allunga di un solo bit ($G : \{0,1\}^\lambda \to \{0,1\}^{\lambda+1}$).

<b>Soluzione del prof.</b> L'avversario $A$, dato $z \in \{0,1\}^{\lambda+1}$, cerca un seme $s \in \{0,1\}^\lambda$ tale che $z = G(s)$. Se lo trova risponde 1, altrimenti 0.

- <b>Se </b>$z$<b> viene dal PRG</b> ($z = G(s)$ con $s \leftarrow U_\lambda$): il seme esiste di sicuro, quindi $\Pr[A(z) = 1] = 1$.
- <b>Se </b>$z$<b> è uniforme</b> ($z \leftarrow U_{\lambda+1}$): $\Pr[A(z) = 1] \le 1/2$.

Quindi il vantaggio è almeno $1 - 1/2 = 1/2$, per niente trascurabile.

<b>Perché</b> $\le 1/2$ <i>(non negli appunti del prof)</i>: i semi sono $2^\lambda$, quindi $G$ produce al massimo $2^\lambda$ stringhe diverse. Le stringhe di $\lambda + 1$ bit sono $2^{\lambda+1}$, il doppio. Quindi una stringa uniforme cade tra le uscite di $G$ al massimo nella metà dei casi.

<b>Perché non funziona contro un avversario PPT</b> <i>(non negli appunti del prof)</i>: per cercare il seme $A$ deve provare tutti i $2^\lambda$ semi, cioè fare un numero <b>esponenziale</b> di passi. Un avversario PPT non può farlo. Un PRG è sicuro proprio perché nessun avversario efficiente sa fare di meglio.

## Come si costruisce un PRG?

!!! abstract "In breve"

    Se esistono le one-way function, esistono PRG che allungano di quanto si vuole (un numero polinomiale di bit). La dimostrazione completa è difficile; il prof ne vede i due ingredienti principali.

<b>Teorema</b>: se esistono le OWF, esistono PRG con stretch $\ell(\lambda) = \text{poly}(\lambda)$.

I due ingredienti:

1. <b>Stretch amplification</b>: passare da $\ell(\lambda) = 1$ a $\ell(\lambda) = \text{poly}(\lambda)$, cioè da un PRG che allunga di 1 bit a uno che allunga di quanto si vuole.
2. <b>Hard-core bit</b>: per costruire il PRG che allunga di 1 bit, partendo da una OWF.

## Ingrediente 1: stretch amplification

!!! abstract "In breve"

    Basta un PRG che aggiunge <b>un solo bit</b> per ottenerne uno che ne aggiunge quanti ne vogliamo. L'idea è applicare $G$ più volte di fila, tenendo da parte un bit a ogni passo.

### Teorema

Se $G : \{0,1\}^\lambda \to \{0,1\}^{\lambda+1}$ è un PRG, allora per ogni $\ell(\lambda) = \text{poly}(\lambda)$ esiste un PRG $G^\ell : \{0,1\}^\lambda \to \{0,1\}^{\lambda + \ell}$.

!!! note ""

    <b>Notazione</b> <i>(non negli appunti del prof)</i>: $G^\ell$ <b>non</b> è una potenza: è solo il nome del nuovo PRG, quello che allunga di $\ell$ bit.

### La costruzione (del prof)

```text
s0 ──→ [G] ──s1──→ [G] ──s2──→ ... ──s(ℓ-1)──→ [G] ──→ sℓ
        │           │                           │
        ↓           ↓                           ↓
        b1          b2                          bℓ
```

- $s_0 \leftarrow U_\lambda$: il seme iniziale, casuale
- per ogni $i \in [\ell]$ (cioè $i = 1, \dots, \ell$): $(s_i, b_i) = G(s_{i-1})$, con $s_i \in \{0,1\}^\lambda$ e $b_i \in \{0,1\}$
- <b>output</b>: $(b_1, \dots, b_\ell, s_\ell)$

In parole: $G$ prende $\lambda$ bit e ne restituisce $\lambda + 1$. Si spezza l'uscita in due: $\lambda$ bit diventano il <b>nuovo seme</b> $s_i$, l'ultimo bit $b_i$ si <b>mette da parte</b>. Si ripete $\ell$ volte e alla fine si restituiscono tutti i bit messi da parte più l'ultimo seme: $\ell + \lambda$ bit.

### Spiegazione semplice con un esempio

<i>(Non negli appunti del prof.)</i>

<b>L'idea: riusare l'uscita come nuovo seme.</b> $G$ prende 3 bit e ne restituisce 4. Li dividiamo: <b>3 bit</b> li <b>rimettiamo dentro</b> $G$ come nuovo seme (sembrano casuali, quindi vanno benissimo come seme), <b>1 bit</b> lo <b>teniamo da parte</b> come "guadagno". E ripetiamo: a ogni giro guadagniamo un bit.

!!! note ""

    <b>Analogia</b>: un distributore che, se metti una moneta, ti ridà <b>la moneta + una caramella</b>. Rimetti la moneta, ti ridà moneta + caramella. Dopo 3 giri hai <b>3 caramelle</b> e ancora la moneta in mano.

<b>Passo per passo</b> (valori di $G$ inventati, solo per vedere il meccanismo), seme iniziale <b>101</b>:

- <b>Giro 1</b>: $G(101) = 0110$ → tieni da parte l'ultimo bit <b>0</b>, rimetti dentro <b>011</b>
- <b>Giro 2</b>: $G(011) = 1101$ → tieni da parte <b>1</b>, rimetti dentro <b>110</b>
- <b>Giro 3</b>: $G(110) = 0001$ → tieni da parte <b>1</b>, rimane <b>000</b>

<b>Alla fine</b> si mettono insieme i bit messi da parte (0, 1, 1) e l'ultimo seme rimasto (000): <b>011 000</b> = 6 bit. Partiti da <b>3</b> bit, ne abbiamo ottenuti <b>6</b>. Con $\ell$ giri se ne ottengono $3 + \ell$.

<b>I nomi nella formula del prof</b>:

- $s_0$ = il seme iniziale (101)
- $s_i$ = il seme che si rimette dentro al giro $i$ (011, 110, 000)
- $b_i$ = il bit messo da parte al giro $i$ (0, 1, 1)
- $(s_i, b_i) = G(s_{i-1})$ = "al giro $i$, $G$ applicato al seme precedente dà il nuovo seme e un bit"
- output $(b_1, \dots, b_\ell, s_\ell)$ = tutti i bit messi da parte, più l'ultimo seme
- $G^\ell$ = il nome di questo nuovo generatore, quello che fa $\ell$ giri

### Come dimostrarlo: per riduzione

!!! abstract "In breve"

    Una <b>riduzione</b> dimostra "se qualcuno sa rompere A, allora sa rompere anche B", costruendo un attaccante per B che usa quello per A come sottoprogramma. Se B è sicuro per ipotesi, allora anche A lo è.

Il piano del prof: <b>supponiamo che esista un avversario PPT </b>$A$<b> che rompe </b>$G^\ell$<b>; costruiamo un avversario PPT </b>$B$<b> che rompe </b>$G$<b>.</b> Siccome $G$ è un PRG per ipotesi, $B$ non può esistere, quindi nemmeno $A$.

!!! note ""

    <b>"Rompere"</b> <i>(non negli appunti del prof)</i> = distinguere l'uscita dall'uniforme con vantaggio <b>non trascurabile</b>, cioè almeno $1/p(\lambda)$ per qualche polinomio $p$.

<b>Il problema</b> (i "???" del prof):

```text
A ←── z' ∈ {0,1}^(λ+ℓ) ─── B ←────── z ─────── C      z ← G(U_λ)  oppure  z ← U_(λ+1)
          ???
```

$B$ riceve dal challenger una stringa $z$ di $\lambda + 1$ bit, ma $A$ sa attaccare solo stringhe di $\lambda + \ell$ bit. Come fa $B$ a usare $A$? Per risolvere questo serve una tecnica nuova: l'argomento ibrido.

### Argomento ibrido (hybrid argument)

!!! abstract "In breve"

    Per dimostrare che due distribuzioni "lontane" $X$ e $Y$ sono indistinguibili, si costruisce una <b>catena di distribuzioni intermedie</b> (gli <b>ibridi</b>) in cui ogni anello differisce dal successivo per un dettaglio piccolissimo. Se nessun avversario nota i singoli passi, non nota nemmeno la differenza tra i due estremi.

<b>Definizione (del prof)</b>: per mostrare $X \approx_c Y$ si trovano ibridi $H_0, H_1, \dots, H_\ell$ tali che:

1. $H_0 \equiv X$ e $H_\ell \equiv Y$ (gli estremi sono le due distribuzioni da confrontare)
2. $H_0 \approx_c H_1$, $H_1 \approx_c H_2$, …, $H_{\ell-1} \approx_c H_\ell$ (ogni passo è indistinguibile)

Allora, per la <b>disuguaglianza triangolare</b>, $H_0 \approx_c H_\ell$, <b>purché</b> $\ell(\lambda) = \text{poly}(\lambda)$.

!!! note ""

    <b>Analogia</b> <i>(non negli appunti del prof)</i>: cambi una foto un pixel alla volta, finché diventa un'altra foto. Se a ogni passo nessuno nota la differenza con la versione precedente, e i passi sono "pochi" (polinomiali), nessuno distingue nemmeno la prima foto dall'ultima.

??? note "Perché funziona e perché serve ℓ polinomiale (non negli appunti del prof)"

    Chiamiamo $p_i = \Pr[A(z) = 1 : z \leftarrow H_i]$. La <b>disuguaglianza triangolare</b> dice che la distanza diretta tra due numeri non supera la somma delle distanze passando per numeri intermedi:

    $|p_0 - p_\ell| \le |p_0 - p_1| + |p_1 - p_2| + \dots + |p_{\ell-1} - p_\ell|$

    A sinistra c'è il vantaggio di $A$ sugli estremi; a destra la somma dei vantaggi sui singoli passi. Ogni passo ha vantaggio trascurabile, e i passi sono $\ell$: il totale è al più $\ell \cdot \text{negl}(\lambda)$. Se $\ell$ è polinomiale, poly · negl = negl (Lezione 4), quindi il totale è ancora trascurabile.

    Se invece i passi fossero esponenziali (es. $2^\lambda$), $2^\lambda \cdot 2^{-\lambda} = 1$: non sarebbe più trascurabile e l'argomento crollerebbe.

### Gli ibridi nel nostro caso

Gli estremi sono:

- $H_0 \equiv G^\ell(U_\lambda)$: tutto pseudocasuale
- $H_\ell \equiv U_{\ell + \lambda}$: tutto davvero casuale

L'ibrido $H_i$ (definizione del prof):

- $b_1, \dots, b_i \leftarrow \{0,1\}$: i primi $i$ bit sono <b>davvero casuali</b>
- $s_i \leftarrow U_\lambda$: il seme al passo $i$ è <b>davvero casuale</b>
- $(b_{i+1}, \dots, b_\ell, s_\ell) = G^{\ell - i}(s_i)$: il resto si calcola con la costruzione, facendo i rimanenti $\ell - i$ passi

Cioè: <b>si sostituisce un bit pseudocasuale alla volta con un bit davvero casuale</b>, partendo da sinistra.

!!! example ""

    <b>Esempio con </b>$\ell = 3$ <i>(non negli appunti del prof)</i>:

    - $H_0$: $s_0$ casuale, poi $b_1, b_2, b_3, s_3$ tutti calcolati con $G$ = $G^3(U_\lambda)$
    - $H_1$: $b_1$ casuale, $s_1$ casuale, poi $b_2, b_3, s_3$ calcolati con $G$
    - $H_2$: $b_1, b_2$ casuali, $s_2$ casuale, poi $b_3, s_3$ calcolati con $G$
    - $H_3$: $b_1, b_2, b_3$ casuali e $s_3$ casuale = $U_{3+\lambda}$

<b>Cosa cambia tra </b>$H_0$<b> e </b>$H_1$ <i>(non negli appunti del prof)</i>: solo il primo passo. In $H_0$ la coppia $(s_1, b_1) = G(s_0)$ è <b>pseudocasuale</b>; in $H_1$ è <b>davvero casuale</b>. Tutto il resto si calcola allo stesso modo a partire da $s_1$.

### La riduzione: H₀ ≈c H₁

Ora la riduzione funziona. Il prof la fa concretamente per $H_0 \approx_c H_1$.

<b>Supponiamo per assurdo</b> che esista un PPT $A$ che distingue $H_0$ da $H_1$. Costruiamo $B$ che rompe $G$:

```text
A ←── (b1, b2, ..., bℓ, sℓ) ─── B ←──── z ∈ {0,1}^(λ+1) ──── C     z ← G(U_λ)  oppure  z ← U_(λ+1)
  ──────────── b' ────────────→   ────────── b' ─────────→
```

$B$, ricevuto $z \in \{0,1\}^{\lambda+1}$:

1. spezza $z = (b_1, s_1)$, con $b_1 \in \{0,1\}$ e $s_1 \in \{0,1\}^\lambda$
2. calcola il resto con la costruzione: $(b_2, \dots, b_\ell, s_\ell) = G^{\ell-1}(s_1)$
3. dà ad $A$ la stringa $(b_1, b_2, \dots, b_\ell, s_\ell)$
4. quando $A$ risponde $b'$, $B$ risponde anche lui $b'$ al challenger

<b>Osservazione chiave (del prof)</b>:

- se $z \leftarrow G(U_\lambda)$, la coppia $(b_1, s_1)$ è un'uscita di $G$, quindi la stringa data ad $A$ è distribuita come $H_0$
- se $z \leftarrow U_{\lambda+1}$, la coppia $(b_1, s_1)$ è davvero casuale, quindi la stringa è distribuita come $H_1$

<b>Per ipotesi</b>, $A$ distingue $H_0$ da $H_1$:

$$
\Big| \Pr[A(b_1, \dots, b_\ell, s_\ell) = 1 : (b_1, \dots, s_\ell) \leftarrow \underbrace{G^\ell(U_\lambda)}_{= H_0}] - \Pr[A(b_1, \dots, b_\ell, s_\ell) = 1 : (b_1, \dots, s_\ell) \leftarrow H_1] \Big| \ge \frac{1}{p(\lambda)}
$$

per qualche polinomio $p(\lambda)$. E per l'osservazione chiave:

$$
\Pr[B(z) = 1 : z \leftarrow G(U_\lambda)] = \Pr[A(b_1, \dots, b_\ell, s_\ell) = 1 : (b_1, \dots, s_\ell) \leftarrow H_0]
$$

$$
\Pr[B(z) = 1 : z \leftarrow U_{\lambda+1}] = \Pr[A(b_1, \dots, b_\ell, s_\ell) = 1 : (b_1, \dots, s_\ell) \leftarrow H_1]
$$

Quindi $B$ distingue $G(U_\lambda)$ da $U_{\lambda+1}$ con vantaggio $\ge 1/p(\lambda)$, cioè <b>rompe </b>$G$. Ma $G$ è un PRG: <b>contraddizione</b>. Inoltre $B$ è PPT, perché chiama $G$ al più $\ell$ volte (polinomiale) e poi $A$.

Con una dimostrazione molto simile, <b>per ogni </b>$i$<b>: </b>$H_i \approx_c H_{i+1}$, e per l'argomento ibrido $G^\ell(U_\lambda) = H_0 \approx_c H_\ell = U_{\lambda+\ell}$. ∎

??? note "Il caso generale H_i ≈c H_(i+1) (non negli appunti del prof)"

    È uguale, ma $B$ inserisce $z$ al passo $i+1$ invece che al passo 1. Ricevuto $z$:

    1. sceglie $b_1, \dots, b_i$ <b>davvero casuali</b>
    2. spezza $z = (b_{i+1}, s_{i+1})$
    3. calcola $(b_{i+2}, \dots, b_\ell, s_\ell) = G^{\ell-i-1}(s_{i+1})$
    4. dà ad $A$ la stringa $(b_1, \dots, b_\ell, s_\ell)$ e ne inoltra la risposta

    Se $z \leftarrow G(U_\lambda)$, il passo $i+1$ è pseudocasuale (come se $s_i$ fosse uniforme e $(s_{i+1}, b_{i+1}) = G(s_i)$): la stringa è distribuita come $H_i$. Se $z$ è uniforme, il passo $i+1$ è davvero casuale: la stringa è distribuita come $H_{i+1}$. Stesso ragionamento di prima.

## Ingrediente 2: hard-core bit

<b>Da dove si prende il primo</b> $G : \{0,1\}^\lambda \to \{0,1\}^{\lambda+1}$? In teoria si può costruire partendo da <b>qualunque</b> OWF, ma non è molto efficiente. Più avanti si vedranno costruzioni efficienti basate su <b>teoria dei numeri</b>, <b>reticoli</b> (lattices), ecc.

L'ingrediente principale sono gli <b>hard-core bit</b>.

### Hard-core bit

!!! abstract "In breve"

    Una OWF nasconde il suo input $x$ "nel complesso", ma potrebbe lasciar trapelare qualche pezzo di $x$. Un <b>hard-core bit</b> è un bit $h(x)$, calcolato da $x$, che resta <b>impossibile da indovinare</b> anche conoscendo $f(x)$: sembra un bit completamente casuale.

Sia $f : \{0,1\}^n \to \{0,1\}^n$ una OWF. La domanda del prof: <b>possiamo dire che un particolare bit di </b>$x$<b> è difficile da calcolare?</b>

<b>Intuitivamente</b>: $h : \{0,1\}^n \to \{0,1\}$ è <b>hard-core</b> per $f$ se $h(x)$ è difficile da calcolare conoscendo $f(x)$.

<b>Formalmente (in alternativa)</b>:

$$
(f(x), h(x)) \approx_c (f(x), u) \qquad u \leftarrow \{0,1\}
$$

!!! note ""

    <b>Cosa sono le cose</b>

    - $x$ = l'input segreto, scelto a caso.
    - $h$ = una funzione che da $x$ calcola <b>un solo bit</b> (es. "il primo bit di $x$", o lo XOR di alcuni bit di $x$).
    - $(f(x), h(x))$ = l'output della OWF <b>insieme</b> al bit $h(x)$.
    - $(f(x), u)$ = l'output della OWF insieme a un bit $u$ <b>completamente casuale</b>, che non c'entra niente con $x$.
    - In parole: anche conoscendo $f(x)$, il bit $h(x)$ è indistinguibile da un bit tirato a caso.

<b>Perché serve questa nozione</b> <i>(non negli appunti del prof)</i>: essere one-way vuol dire solo che non si riesce a ricavare <b>tutto</b> $x$. Non garantisce che non si ricavi <b>qualche pezzo</b> di $x$. Ad esempio se $f$ è one-way, anche $f'(x) = f(x) \| x_1$ (che scrive in chiaro il primo bit di $x$) è one-way, ma il primo bit di $x$ ovviamente non è nascosto. Un hard-core bit è un bit che invece è <b>garantito</b> nascosto.

### Perché è utile: un PRG da una one-way permutation

Supponiamo che $f : \{0,1\}^n \to \{0,1\}^n$ sia una <b>one-way permutation (OWP)</b>.

!!! note ""

    <b>Permutazione</b> <i>(definizione non negli appunti del prof)</i>: una funzione da $\{0,1\}^n$ a $\{0,1\}^n$ in cui <b>ogni output viene da esattamente un input</b> (una biiezione). In pratica "rimescola" le stringhe senza perderne nessuna. Quindi: <b>se </b>$s$<b> è uniforme, anche </b>$f(s)$<b> è uniforme</b>. Una OWP è una OWF che è anche una permutazione.

Allora il prof definisce:

$$
G(s) = f(s) \,\|\, h(s) \qquad s \leftarrow U_n
$$

($\|$ = <b>concatenazione</b>: si attaccano le due stringhe una dopo l'altra. Es. $f(s) = 111$ e $h(s) = 1$ danno $f(s) \| h(s) = 1111$. Quindi gli $n$ bit di $f(s)$ più il bit $h(s)$ fanno $n+1$ bit: con $n = 128$, escono 129 bit.)

<b>Perché è un PRG</b>, passo per passo:

$$
G(s) = f(s) \,\|\, h(s) \ \approx_c \ f(s) \,\|\, b \ \equiv \ U_{n+1} \qquad b \leftarrow \{0,1\}
$$

1. $f(s) \| h(s) \approx_c f(s) \| b$: è esattamente la definizione di hard-core bit: $h(s)$ non si distingue da un bit casuale $b$, anche conoscendo $f(s)$.
2. $f(s) \| b \equiv U_{n+1}$: $f(s)$ è uniforme su $n$ bit (perché $f$ è una permutazione e $s$ è uniforme), e $b$ è un bit uniforme indipendente. Insieme fanno $n + 1$ bit uniformi.

Quindi $G : \{0,1\}^n \to \{0,1\}^{n+1}$ allunga di 1 bit ed è un PRG. Con l'ingrediente 1 si allunga poi di quanto si vuole.

### In generale

- Si riesce a far funzionare la stessa idea partendo da una qualunque <b>OWF</b> (non serve che sia una permutazione), ma è più complicato.
- <b>Ogni</b> OWF $f$ ammette un hard-core bit $h$. <i>(Non negli appunti del prof: è il teorema di Goldreich-Levin; l'hard-core bit è lo XOR di un sottoinsieme casuale dei bit di </i>$x$<i>.)</i>

### Domanda: esiste un unico h che funziona per ogni f?

<b>No.</b> L'idea del prof: preso un qualunque $h$, si costruisce una funzione $f_{\text{BAD}}$ tale che

- $h$ <b>non</b> è hard-core per $f_{\text{BAD}}$
- ma $f_{\text{BAD}}$ è comunque una OWF

Va bene se $f_{\text{BAD}}$ usa al suo interno un'altra OWF ausiliaria $f : \{0,1\}^n \to \{0,1\}^n$.

??? note "Come si costruisce f_BAD (non negli appunti del prof)"

    Si prende $f_{\text{BAD}}(x) = f(x) \,\|\, h(x)$, cioè si scrive $h(x)$ <b>in chiaro</b> nell'output.

    - $h$<b> non è hard-core per </b>$f_{\text{BAD}}$: chi vede $f_{\text{BAD}}(x)$ legge direttamente $h(x)$ nell'ultimo bit. Altro che difficile da calcolare.
    - $f_{\text{BAD}}$<b> è comunque one-way</b>: se qualcuno sapesse invertire $f_{\text{BAD}}$, cioè trovare $x'$ con $f(x') \| h(x') = f(x) \| h(x)$, avrebbe in particolare $f(x') = f(x)$, e quindi saprebbe invertire $f$. Ma $f$ è one-way. (È una riduzione!)

    Quindi nessun $h$ fissato funziona per tutte le OWF: l'hard-core bit va scelto in base alla funzione. È lo stesso schema del "nessun estrattore fisso funziona per tutte le fonti" della lezione 3.

## Riepilogo

- <b>Pseudocasuale</b> = bit generati in modo deterministico da un seme corto, che nessun avversario PPT distingue da bit casuali (se non con probabilità trascurabile)
- $X \approx_c Y$: per ogni PPT $A$, $|\Pr[A(X_\lambda) = 1] - \Pr[A(Y_\lambda) = 1]| \le \text{negl}(\lambda)$; equivalente al gioco GAME(λ, 0) ≈c GAME(λ, 1)
- <b>PRG</b>: $G : \{0,1\}^\lambda \to \{0,1\}^{\lambda+\ell}$ con $G(U_\lambda) \approx_c U_{\lambda+\ell}$
- <b>Nessun PRG è sicuro contro avversari illimitati</b>: basta cercare il seme (vantaggio ≥ 1/2), ma richiede tempo esponenziale
- <b>OWF ⇒ PRG</b> con stretch polinomiale; due ingredienti:
- <b>Stretch amplification</b>: da stretch 1 a stretch poly, applicando $G$ in catena; si dimostra per <b>riduzione</b> usando l'<b>argomento ibrido</b> (ibridi $H_i$: i primi $i$ bit davvero casuali)
- <b>Hard-core bit</b>: $(f(x), h(x)) \approx_c (f(x), u)$; con una OWP, $G(s) = f(s) \| h(s)$ è un PRG con stretch 1
- Ogni OWF ha un hard-core bit, ma nessun $h$ funziona per tutte le OWF ($f_{\text{BAD}}$)
