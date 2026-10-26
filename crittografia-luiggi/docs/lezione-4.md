# Lezione 4 – Sicurezza computazionale e OWF

<i>Segue gli appunti del prof. Le parti aggiunte per capire meglio sono segnate "non negli appunti del prof". PRG e indistinguibilità computazionale sono nella</i> [Lezione 5](lezione-5.md)

## Fine lezione 3: dimostrazione del lemma sulla collision probability

!!! abstract "In breve"

    Nella lezione 3, per dimostrare il Leftover Hash Lemma, avevamo usato un lemma senza dimostrarlo: <b>se una distribuzione collide quasi quanto l'uniforme, allora è quasi uniforme</b>. Il prof lo dimostra qui, usando la disuguaglianza di Cauchy-Schwarz.

### Promemoria: cosa dice il lemma

Sia $Y$ una variabile aleatoria che prende valori in un insieme $\mathcal{Y}$, e sia $U$ uniforme su $\mathcal{Y}$. Se

$$
\text{Col}(Y) \le \frac{1}{|\mathcal{Y}|}\,(1 + 4\varepsilon^2)
$$

allora $\text{SD}(Y; U) \le \varepsilon$.

!!! note ""

    <b>Cosa sono le cose</b>

    - $\mathcal{Y}$ = l'insieme dei valori possibili; $|\mathcal{Y}|$ = quanti sono.
    - $U$ = la distribuzione uniforme su $\mathcal{Y}$: ogni valore ha probabilità $1/|\mathcal{Y}|$.
    - $\text{Col}(Y) = \sum_{y} \Pr[Y = y]^2$ = probabilità di collisione: la probabilità che due estrazioni indipendenti di $Y$ diano lo stesso valore. L'uniforme ha la più bassa possibile, $1/|\mathcal{Y}|$.
    - $\text{SD}(Y; U)$ = distanza statistica tra $Y$ e l'uniforme (lezione 3).

### Strumento: prodotto scalare e Cauchy-Schwarz

<i>(Definizioni non negli appunti del prof, servono per seguire la dimostrazione.)</i>

<b>Prodotto scalare</b> di due vettori $\vec{u} = (u_1, \dots, u_N)$ e $\vec{v} = (v_1, \dots, v_N)$: si moltiplicano le componenti a coppie e si somma.

$$
\langle \vec{u}, \vec{v} \rangle = u_1 v_1 + u_2 v_2 + \dots + u_N v_N
$$

!!! example ""

    <b>Esempio</b>: $\langle (1, 2), (3, 4) \rangle = 1 \cdot 3 + 2 \cdot 4 = 11$. In particolare $\langle \vec{u}, \vec{u} \rangle = u_1^2 + \dots + u_N^2$.

<b>Disuguaglianza di Cauchy-Schwarz</b>: il prodotto scalare di due vettori non supera mai la radice del prodotto dei loro "quadrati":

$$
\langle \vec{u}, \vec{v} \rangle \le \sqrt{\langle \vec{u}, \vec{u} \rangle \cdot \langle \vec{v}, \vec{v} \rangle}
$$

!!! example ""

    <b>Esempio</b>: con $(1, 2)$ e $(3, 4)$: a sinistra 11; a destra $\sqrt{5 \cdot 25} = \sqrt{125} \approx 11{,}18$. Infatti $11 \le 11{,}18$.

### Dimostrazione (del prof)

<b>Passo 1: riscrivere la SD come prodotto scalare.</b> Per definizione:

$$
\text{SD}(Y; U) = \frac{1}{2} \sum_{y \in \mathcal{Y}} \Big| \Pr[Y = y] - \frac{1}{|\mathcal{Y}|} \Big|
$$

Il prof introduce due abbreviazioni, per ogni valore $y$:

- $q_y = \Pr[Y = y] - \frac{1}{|\mathcal{Y}|}$: di quanto la probabilità di $y$ si scosta da quella uniforme (può essere positivo o negativo)
- $s_y = +1$ se $q_y \ge 0$, $s_y = -1$ altrimenti: il <b>segno</b> di $q_y$

Siccome un numero moltiplicato per il suo segno dà il suo valore assoluto ($q_y \cdot s_y = |q_y|$):

$$
\text{SD}(Y; U) = \frac{1}{2} \sum_{y \in \mathcal{Y}} q_y\, s_y = \frac{1}{2} \langle \vec{q}, \vec{s} \rangle
$$

dove $\vec{q} = (q_y)_{y \in \mathcal{Y}}$ e $\vec{s} = (s_y)_{y \in \mathcal{Y}}$ sono i vettori con una componente per ogni valore $y$.

<b>Passo 2: Cauchy-Schwarz.</b>

$$
\text{SD}(Y; U) = \frac{1}{2} \langle \vec{q}, \vec{s} \rangle \le \frac{1}{2} \sqrt{\langle \vec{q}, \vec{q} \rangle \cdot \langle \vec{s}, \vec{s} \rangle} = \frac{1}{2} \sqrt{\sum_{y \in \mathcal{Y}} q_y^2 \cdot |\mathcal{Y}|}
$$

Infatti $\langle \vec{s}, \vec{s} \rangle = \sum_y s_y^2 = |\mathcal{Y}|$, perché ogni $s_y$ vale $\pm 1$, quindi $s_y^2 = 1$, e ce n'è uno per ogni valore.

<b>Passo 3: calcolare</b> $\sum_y q_y^2$. Si sviluppa il quadrato $(a - b)^2 = a^2 + b^2 - 2ab$:

$$
\sum_{y} q_y^2 = \sum_{y} \Big( \Pr[Y = y] - \frac{1}{|\mathcal{Y}|} \Big)^2 = \sum_{y} \Big( \Pr[Y = y]^2 + \frac{1}{|\mathcal{Y}|^2} - 2\,\frac{\Pr[Y = y]}{|\mathcal{Y}|} \Big)
$$

Si sommano i tre pezzi separatamente:

- $\sum_y \Pr[Y = y]^2 = \text{Col}(Y)$, per definizione
- $\sum_y \frac{1}{|\mathcal{Y}|^2} = |\mathcal{Y}| \cdot \frac{1}{|\mathcal{Y}|^2} = \frac{1}{|\mathcal{Y}|}$, perché è lo stesso numero sommato $|\mathcal{Y}|$ volte
- $\sum_y 2\,\frac{\Pr[Y = y]}{|\mathcal{Y}|} = \frac{2}{|\mathcal{Y}|} \sum_y \Pr[Y = y] = \frac{2}{|\mathcal{Y}|}$, perché le probabilità sommano a 1

Quindi, usando l'ipotesi su $\text{Col}(Y)$:

$$
\sum_{y} q_y^2 = \text{Col}(Y) + \frac{1}{|\mathcal{Y}|} - \frac{2}{|\mathcal{Y}|} \le \frac{1 + 4\varepsilon^2}{|\mathcal{Y}|} - \frac{1}{|\mathcal{Y}|} = \frac{4\varepsilon^2}{|\mathcal{Y}|}
$$

<b>Passo 4: rimettere insieme.</b>

$$
\text{SD}(Y; U) \le \frac{1}{2} \sqrt{\frac{4\varepsilon^2}{|\mathcal{Y}|} \cdot |\mathcal{Y}|} = \frac{1}{2} \sqrt{4\varepsilon^2} = \frac{1}{2} \cdot 2\varepsilon = \varepsilon
$$

∎

<b>Intuizione</b>: $\sum_y q_y^2$ misura quanto $Y$ si scosta dall'uniforme "al quadrato", ed è esattamente l'<b>eccesso di collisioni</b> $\text{Col}(Y) - 1/|\mathcal{Y}|$. Se l'eccesso è piccolo, Cauchy-Schwarz garantisce che anche la distanza statistica è piccola.

## Sicurezza computazionale

!!! abstract "In breve"

    Finora la sicurezza valeva contro avversari con potenza di calcolo <b>infinita</b>, e il prezzo erano limiti pesantissimi (chiavi lunghe quanto i messaggi, chiavi che crescono con l'uso). Per avere crittografia <b>dimostrabilmente sicura ed efficiente</b> bisogna cambiare qualcosa: si fanno <b>due ipotesi</b> in più.

I limiti visti finora:

- <b>Cifratura (Shannon)</b>: la chiave deve essere lunga almeno quanto il messaggio e va usata una volta sola.
- <b>MAC</b>: per autenticare $t$ messaggi servono chiavi di $(t+1)\lambda$ bit.
- <b>Casualità</b>: da una fonte con min-entropia $k$ non si estraggono più di circa $k$ bit puliti.

Le due ipotesi del prof:

1. <b>L'avversario gira su una macchina "efficiente"</b>: non ha potenza infinita.
2. <b>Esistono problemi che sembrano "difficili"</b>, cioè che nessuna macchina efficiente sa risolvere.

## Ipotesi (i): l'avversario è PPT

!!! abstract "In breve"

    L'avversario è un programma (una macchina di Turing) che lavora in <b>tempo polinomiale</b> e può usare <b>bit casuali</b>. Si chiama <b>PPT</b>: <i>Probabilistic Polynomial Time</i>.

<b>Macchina di Turing (TM)</b> <i>(definizione non negli appunti del prof)</i>: il modello matematico di un computer. In pratica: <b>un algoritmo</b>. Dire "l'avversario è una TM" vuol dire "l'avversario è un programma".

<b>Tempo polinomiale</b>: si conta il numero di passi in funzione della lunghezza dell'input $n$. Il programma è efficiente se fa $O(n^c)$ passi per qualche costante $c \in \mathbb{N}$.

!!! note ""

    <b>Cosa vuol dire</b> $O(n^c)$: "al massimo una costante per $n^c$". Esempi: $n^2$, $5n^3 + n$, $n^{100}$ sono polinomiali, cioè efficienti. $2^n$ <b>non</b> lo è: con $n = 128$ sono $2^{128}$ passi, impossibili in pratica. Quindi l'avversario può fare tutto tranne i calcoli esponenziali, come provare tutte le chiavi possibili.

<b>In più</b>: l'avversario può generare una quantità (polinomiale) di <b>bit casuali</b>, cioè può "tirare monete" durante il calcolo.

$$
\text{Adv} \equiv \text{PPT TM} \quad (\text{Probabilistic Polynomial Time Turing Machine})
$$

## Ipotesi (ii): esistono problemi difficili

!!! abstract "In breve"

    Idealmente vorremmo basare la sicurezza su $P \neq NP$. Nessuno sa farlo; quello che si sa fare è basarla su problemi specifici che si credono difficili, come la <b>fattorizzazione</b>.

### P e NP

!!! abstract "In breve"

    <b>P</b> = problemi che si sanno <b>risolvere</b> velocemente. <b>NP</b> = problemi in cui una soluzione, se qualcuno te la dà, si sa <b>controllare</b> velocemente. Ogni problema in P sta anche in NP.

- $P$ = tutti i problemi risolvibili da una TM in tempo polinomiale.
- $NP$ = tutti i problemi tali che una soluzione si può <b>verificare</b> da una TM in tempo polinomiale.

Esempi del prof di problemi in NP:

- <b>FACTORING</b>: dato $n = p \cdot q$, trovare $p$ e $q$. Se qualcuno ti dà $p$ e $q$, controlli subito che $p \cdot q = n$; trovarli da solo invece è difficile.
- <b>3COL</b>: dato un grafo $G$, trovare una <b>3-colorazione</b> $\varphi$ di $G$. <i>(Definizione non negli appunti del prof: un grafo è un insieme di punti collegati da linee; una 3-colorazione assegna a ogni punto uno di 3 colori in modo che due punti collegati non abbiano mai lo stesso colore.)</i> Data una colorazione, controllare che sia giusta è facile (si guarda ogni linea); trovarla è difficile.

!!! example ""

    <b>Esempio intuitivo</b> <i>(non negli appunti del prof)</i>: il sudoku. Controllare un sudoku compilato è facile, risolverlo da zero no.

<b>La domanda P = NP?</b> È "tutto ciò che si <b>controlla</b> facilmente si può anche <b>trovare</b> facilmente?". Nessuno lo sa, ma quasi tutti credono di no ($P \neq NP$). P e NP sono <b>insiemi di problemi</b>, non problemi.

??? note "Approfondimento (non negli appunti del prof): perché le domande sì/no"

    Formalmente P e NP parlano di problemi <b>sì/no</b>: "3233 ha un divisore minore di 60?". Se la risposta è sì, una <b>prova</b> (es. "53") si controlla in fretta. NP = domande in cui la prova del sì si controlla velocemente; P = domande a cui si risponde velocemente da soli. $P = NP$ vorrebbe dire che non serve mai qualcuno che ti suggerisca la prova: c'è sempre un metodo veloce per arrivarci da solo.

### Il teorema ideale

$$
\textbf{Teorema (ideale)}: \text{ se } P \neq NP, \text{ allora } \Pi \text{ è sicuro.}
$$

<b>Perché sarebbe bellissimo</b>: restano solo due possibilità:

1. $\Pi$ è sicuro, oppure
2. $P = NP$, che quasi nessuno crede

Rompere $\Pi$ vorrebbe dire risolvere il problema più famoso dell'informatica.

<b>Bad news</b>: <b>nessuno sa dimostrare teoremi di questo tipo.</b>

### Quello che si sa fare

$$
\textbf{Teorema (esempio reale)}: \text{ se FACTORING è difficile, allora } \Pi \text{ è sicuro.}
$$

<b>È ancora utile?</b> Sì, leggendolo al contrario (<b>contronominale</b>): <i>se</i> $\Pi$ <i>non fosse sicuro, allora FACTORING non sarebbe difficile, cioè esisterebbe una PPT TM che fattorizza.</i> E siccome da decenni nessuno ha trovato un algoritmo veloce per fattorizzare, è molto improbabile che qualcuno rompa $\Pi$.

!!! note ""

    <b>Contronominale</b> <i>(definizione non negli appunti del prof)</i>: "se A allora B" è equivalente a "se non B allora non A". Es. "se piove, la strada è bagnata" equivale a "se la strada non è bagnata, non piove".

## One-way function (OWF)

!!! abstract "In breve"

    Una <b>funzione one-way</b> è facile da calcolare ma difficile da invertire: dato $x$ si calcola $f(x)$ in un attimo, ma dato $f(x)$ nessun algoritmo efficiente riesce a trovare un input che dia quel risultato. Per il prof è <b>"la madre di tutte le ipotesi"</b>: è l'<b>ipotesi minima</b> per fare crittografia interessante.

### Spiegazione semplice: la moltiplicazione

<i>(Non negli appunti del prof.)</i>

<b>Andata.</b> Ti do due numeri primi, 61 e 53: moltiplicarli è immediato, $61 \times 53 = 3233$.

<b>Ritorno.</b> Ti do solo <b>3233</b> e ti chiedo quali due numeri ho moltiplicato. Non c'è un trucco: devi provare a dividere per 2, 3, 5, 7, 11, … finché trovi un divisore.

<b>Con numeri enormi</b> (primi da 300 cifre) moltiplicare resta istantaneo, tornare indietro richiederebbe più tempo dell'età dell'universo.

- $x$ = l'input (i due primi), $f$ = la funzione (moltiplicarli), $f(x)$ = il risultato (3233)
- <b>invertire</b> = dato $f(x)$, trovare $x$

!!! note ""

    <b>Funzione che NON è one-way</b>: $f(x) = x + 5$. Da 15 si torna a 10 togliendo 5, istantaneo.

<b>Perché serve</b>: serve qualcosa che <b>tu</b> sai fare e <b>Eve</b> no. Chi conosce l'input (es. la chiave) calcola tutto facilmente; Eve, che vede solo il risultato, non riesce a tornare indietro.

### Definizione (del prof)

Una funzione <b>deterministica</b> $f : \mathcal{X} \to \mathcal{Y}$ è <b>one-way</b> se per ogni avversario PPT $A$:

$$
\Pr\big[\text{GAME}^{\text{owf}}_{A,f}(\lambda) = 1\big] \le \text{negl}(\lambda)
$$

cioè la probabilità che $A$ <b>vinca</b> il gioco qui sotto è <b>trascurabile</b>.

!!! note ""

    <b>Cosa sono le cose</b>

    - <b>deterministica</b> = stesso input, stesso output sempre (niente casualità dentro $f$).
    - $\mathcal{X}$ = insieme degli input, $\mathcal{Y}$ = insieme degli output. Tipicamente $f : \{0,1\}^\lambda \to \{0,1\}^\lambda$: stringhe di $\lambda$ bit in, stringhe di $\lambda$ bit out.
    - $\lambda$ = il <b>parametro di sicurezza</b>: la lunghezza dell'input in bit. Più è grande, più il problema è difficile.
    - $\text{GAME}^{\text{owf}}_{A,f}(\lambda)$ = il gioco tra l'avversario $A$ e il challenger, per la funzione $f$, con parametro $\lambda$. Vale 1 se $A$ vince.
    - $\text{negl}(\lambda)$ = una funzione <b>trascurabile</b> (vedi sotto).

### Il gioco della one-way function

```text
Avversario A                          Challenger C
                                      x ← X      (x scelto a caso)
      ←──────────── y ─────────────   y = f(x)
      ──────────── x' ─────────────→
                                      Output 1 (WIN) se f(x') = y
```

1. Il challenger sceglie $x$ <b>a caso</b> in $\mathcal{X}$ (la freccia $x \leftarrow \mathcal{X}$ vuol dire "scelto uniformemente a caso").
2. Calcola $y = f(x)$ e lo dà ad $A$.
3. $A$ risponde con un $x'$.
4. $A$ <b>vince</b> se $f(x') = y$.

<b>Dettagli importanti</b> <i>(non negli appunti del prof)</i>:

- <b>Basta una qualunque controimmagine</b>: $A$ vince anche se $x' \neq x$, purché $f(x') = y$.
- <b>L'input è casuale</b>: la difficoltà è richiesta <b>in media</b>, su input casuali, non solo per qualche input particolare.

### Esempi di OWF (candidate)

Nessuno ha mai <b>dimostrato</b> che le OWF esistono: sono un'<b>ipotesi</b>. Questi sono i candidati del prof, cioè problemi che si credono difficili:

- <b>FACTORING</b>: $f(p, q) = p \cdot q$; invertire = fattorizzare.
- <b>DISCRETE LOG</b> (logaritmo discreto): $f(x) = g^x \bmod p$; invertire = trovare l'esponente $x$ dato $g^x \bmod p$.
- <b>LATTICES</b> (reticoli) e <b>DECODING RANDOM CODES</b> (decodificare codici casuali): problemi di algebra lineare "rumorosa". <i>(Non negli appunti del prof: sono importanti perché si crede che resistano anche ai computer quantistici.)</i>

### OWF e P vs NP

<i>(Non negli appunti del prof: approfondimento per capire perché le OWF sono un'ipotesi più forte di P ≠ NP.)</i>

!!! abstract "In breve"

    Se le OWF esistono, allora $P \neq NP$. Il viceversa non è garantito: anche se $P \neq NP$ le OWF potrebbero non esistere.

??? note "Dimostrazione: OWF ⇒ P ≠ NP"

    Si dimostra al contrario: <b>se P = NP, allora nessuna funzione è one-way</b>.

    P e NP parlano di domande sì/no, ma a noi serve <b>trovare</b> $x$. Si fa come nel gioco delle 20 domande: si scopre $x$ <b>un bit alla volta</b>, con domande del tipo "esiste un $x'$ che inizia con $p$ e tale che $f(x') = y$?".

    Questa domanda sta in NP: se qualcuno propone $x'$, si controlla velocemente (si guarda come inizia e si calcola $f(x')$). Se $P = NP$, c'è un algoritmo veloce che risponde.

    <b>L'invertitore</b>: parte dal prefisso vuoto; a ogni passo chiede "esiste una controimmagine che continua con 0?"; se sì aggiunge 0, altrimenti aggiunge 1. Resta sempre vero che esiste una controimmagine con quel prefisso, quindi dopo $\lambda$ passi ha una controimmagine completa.

    <b>Esempio</b> con $x = 101$: inizia con 0? No → 1. Inizia con 10? Sì → 10. Inizia con 100? No → 101 ✓.

    Sono $\lambda$ domande veloci, quindi tempo polinomiale, e successo con probabilità 1: $f$ non è one-way. ∎

<b>Perché P ≠ NP non basta</b>: $P \neq NP$ garantisce solo che esiste <b>almeno qualche</b> caso difficile (caso peggiore). In crittografia la chiave è scelta <b>a caso</b>, quindi serve che il problema sia difficile <b>quasi sempre</b> (caso medio). È come un produttore che garantisce che almeno uno su 1000 lucchetti è impossibile da scassinare: se ne prendi uno a caso, quasi sicuramente è facile.

## Funzioni trascurabili (negligible)

!!! abstract "In breve"

    "piccolo" in crittografia si definisce in modo <b>asintotico</b>: una funzione è <b>trascurabile</b> se diventa più piccola dell'inverso di <b>qualunque</b> polinomio. È il modo formale di dire "probabilità così piccola che si può ignorare".

### Definizione (del prof)

Una funzione $\varepsilon(\lambda)$ è <b>trascurabile</b> (<i>negligible</i>) in $\lambda$ se

$$
\varepsilon(\lambda) = O\Big(\frac{1}{p(\lambda)}\Big) \quad \text{per } \textbf{ogni} \text{ polinomio } p(\lambda) = \text{poly}(\lambda)
$$

Si scrive $\varepsilon(\lambda) = \text{negl}(\lambda)$.

<b>Come leggerla</b> <i>(non negli appunti del prof)</i>: per ogni polinomio, anche enorme come $\lambda^{100}$, da un certo punto in poi $\varepsilon(\lambda)$ sta sotto $1/p(\lambda)$ e ci resta. Basta <b>un solo</b> polinomio per cui non succede e la funzione non è trascurabile.

### Esempi

<b>Esempio del prof</b>: $2^{-\lambda}$ è trascurabile. Confronto con $1/\lambda^{10}$:

| λ | 2^(−λ) | 1/λ^10 | Chi è più piccolo? |
| --- | --- | --- | --- |
| 10 | ≈ 0,001 | 0,0000000001 | 1/λ^10 |
| 50 | ≈ 9 · 10^(−16) | ≈ 1 · 10^(−17) | 1/λ^10 |
| 100 | ≈ 8 · 10^(−31) | 1 · 10^(−20) | <b>2^(−λ)</b> |
| 200 | ≈ 6 · 10^(−61) | ≈ 1 · 10^(−23) | <b>2^(−λ)</b> |

All'inizio $2^{-\lambda}$ è più grande, ma da $\lambda = 59$ in poi passa sotto e non risale più: si dimezza a ogni passo, mentre $1/\lambda^{10}$ scende sempre più lentamente. Con qualunque altro polinomio succede lo stesso, solo più tardi.

<b>Controesempio</b> <i>(non negli appunti del prof)</i>: $1/\lambda^{10}$ <b>non</b> è trascurabile. Con il polinomio $\lambda^{11}$ dovrebbe finire sotto $1/\lambda^{11}$, ma $1/\lambda^{10}$ è sempre più grande (es. con $\lambda = 10$: $10^{-10} > 10^{-11}$).

<b>Perché conta</b>: un attacco che riesce con probabilità $1/\lambda^{10}$ si può ripetere $\lambda^{10}$ volte (tempo ancora polinomiale) e alla fine riesce. Con probabilità $2^{-\lambda}$, anche ripetendolo $\lambda^{10}$ volte si arriva al massimo a $\lambda^{10} \cdot 2^{-\lambda}$, ancora minuscolo.

### Perché è comoda (proprietà del prof)

$$
\text{negl}(\lambda) + \text{negl}(\lambda) = \text{negl}(\lambda) \qquad \text{poly}(\lambda) \cdot \text{negl}(\lambda) = \text{negl}(\lambda)
$$

??? note "Dimostrazione delle due proprietà (non negli appunti del prof)"

    <b>Idea</b>: per battere $1/\lambda^c$ si usa la definizione con un esponente <b>più grande</b> di $c$, così c'è margine per assorbire il fattore 2 o il polinomio.

    <b>Somma.</b> Fissato $c$, si applica la definizione con $c+1$: da un certo punto $\varepsilon_1, \varepsilon_2 < 1/\lambda^{c+1}$. Allora per $\lambda \ge 2$: $\varepsilon_1 + \varepsilon_2 < 2/\lambda^{c+1} = (2/\lambda) \cdot 1/\lambda^c \le 1/\lambda^c$. ✓

    <b>Prodotto.</b> Un polinomio da un certo punto sta sotto $\lambda^d$ per qualche $d$. Fissato $c$, si applica la definizione con $c + d$: $\varepsilon < 1/\lambda^{c+d}$, quindi $p(\lambda) \cdot \varepsilon < \lambda^d / \lambda^{c+d} = 1/\lambda^c$. ∎

## Conclusione: i mondi computazionali

!!! abstract "In breve"

    A seconda delle ipotesi che si fanno, si ottengono "mondi" diversi, cioè diverse cose che la crittografia riesce a costruire. Con le sole OWF si costruisce tutta la crittografia <b>simmetrica</b>; per quella <b>a chiave pubblica</b> sembra servire qualcosa in più.

| Mondo | Ipotesi | Cosa si può costruire |
| --- | --- | --- |
| <b>Minicrypt</b> | Esistono le OWF | SKE, MAC, PRNG |
| <b>Cryptomania</b> | Ipotesi più forti delle OWF | PKE, scambio di chiavi (TLS) |

!!! note ""

    <b>Le sigle</b> <i>(definizioni non negli appunti del prof)</i>

    - <b>SKE</b> (<i>Symmetric Key Encryption</i>): cifratura a chiave simmetrica, Alice e Bob hanno la stessa chiave (come l'OTP).
    - <b>MAC</b>: codici di autenticazione dei messaggi (lezioni 2-3).
    - <b>PRNG</b> (<i>Pseudo-Random Number Generator</i>): generatori di bit pseudocasuali, cioè che <i>sembrano</i> casuali (vedi Lezione 5).
    - <b>PKE</b> (<i>Public Key Encryption</i>): cifratura a chiave pubblica, una chiave pubblica per cifrare e una privata per decifrare (es. RSA).
    - <b>Scambio di chiavi</b> (<i>key exchange</i>): due persone che non si sono mai viste concordano una chiave segreta parlando su un canale pubblico. È quello che fa <b>TLS</b> ogni volta che apri un sito in HTTPS.

<b>La freccia sbarrata</b> nel disegno del prof: dalle sole OWF <b>non</b> si sa ottenere la crittografia a chiave pubblica. Minicrypt non porta automaticamente a Cryptomania.

??? note "I cinque mondi di Impagliazzo (dalle dispense, non negli appunti del prof)"

    Russell Impagliazzo (1995) ha descritto cinque mondi possibili. Non sappiamo in quale viviamo; si spera in uno degli ultimi due.

    - <b>Algorithmica</b>: $P = NP$, niente problemi difficili, niente crittografia computazionale.
    - <b>Heuristica</b>: $P \neq NP$, ma i problemi difficili sono facili <b>in media</b>: inutile per le chiavi casuali.
    - <b>Pessiland</b>: esistono problemi difficili in media, ma <b>non</b> le OWF. Il mondo peggiore.
    - <b>Minicrypt</b>: esistono le OWF, ma non la crittografia a chiave pubblica.
    - <b>Cryptomania</b>: esistono OWF <b>e</b> crittografia a chiave pubblica.

## Riepilogo

- <b>Lemma della collision probability</b>: si dimostra scrivendo la SD come prodotto scalare e usando <b>Cauchy-Schwarz</b>; l'eccesso di collisioni controlla la distanza dall'uniforme
- <b>Sicurezza computazionale</b>: due ipotesi in più, avversario efficiente e problemi difficili
- <b>Avversario = PPT TM</b>: tempo polinomiale $O(n^c)$ e bit casuali
- <b>P</b> = problemi che si risolvono velocemente; <b>NP</b> = problemi in cui una soluzione si controlla velocemente (es. FACTORING, 3COL)
- Ideale: "se P ≠ NP allora Π sicuro", ma nessuno sa farlo. Reale: "se FACTORING è difficile allora Π sicuro", e al contrario: rompere Π ⇒ fattorizzare
- <b>OWF</b>: facile da calcolare, difficile da invertire; nel gioco l'avversario vince con probabilità $\le \text{negl}(\lambda)$; è l'ipotesi minima della crittografia
- <b>Trascurabile</b>: $O(1/p(\lambda))$ per ogni polinomio; es. $2^{-\lambda}$; negl + negl = negl, poly · negl = negl
- Candidati OWF: FACTORING, DISCRETE LOG, LATTICES, DECODING RANDOM CODES
- <b>Minicrypt</b> (OWF): SKE, MAC, PRNG. <b>Cryptomania</b>: PKE, scambio di chiavi (TLS)
