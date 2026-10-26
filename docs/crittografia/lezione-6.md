# Lezione 6 – Goldreich-Levin e cifratura computazionale

*Segue gli appunti del prof. Le parti aggiunte per capire meglio sono segnate "non negli appunti del prof". Usa i concetti della [Lezione 4](lezione-4.md) (OWF, trascurabile) e della [Lezione 5](lezione-5.md) (PRG, hard-core bit, riduzioni, ≈c).*

## Fine lezione 5: perché f_BAD è comunque una OWF

!!! abstract "In breve"

    Nella lezione 5 abbiamo costruito $f_{\text{BAD}}(x) = f(x) \,\|\, h(x)$, che scrive in chiaro il bit $h(x)$: quindi $h$ non è hard-core per $f_{\text{BAD}}$. Qui il prof dimostra che $f_{\text{BAD}}$ resta comunque <b>one-way</b>, con una riduzione: chi inverte $f_{\text{BAD}}$ sa invertire anche $f$.

<b>Il problema</b>: $h(\cdot)$ chiaramente <b>non</b> è hard-core per $f_{\text{BAD}}$, perché è scritto nell'output. Perché $f_{\text{BAD}}$ è ancora una OWF?

<b>Supponiamo di no</b>: esiste un PPT $A$ che vince $\text{GAME}^{\text{owf}}_{f_{\text{BAD}}}(\lambda)$ con probabilità $\ge 1/\text{poly}(\lambda)$, cioè non trascurabile. Costruiamo un PPT $B$ che <b>rompe</b> $f$.

```text
A                              B                              C
                                                              x ← U_n
                               ←────────── y = f(x) ──────────
                               b̃ ← U_1   (bit tirato a caso)
  ←──────── y ‖ b̃ ─────────
  ────────── x' ───────────→
                               ────────────── x' ────────────→
```

1. $B$ riceve dal challenger $y = f(x)$, con $x$ casuale.
2. Ad $A$ serve una stringa della forma $f(x) \,\|\, h(x)$, ma $B$ non conosce $x$ e quindi non sa calcolare $h(x)$. Allora <b>tira a indovinare</b>: sceglie un bit casuale $\tilde{b}$ e dà ad $A$ la stringa $y \,\|\, \tilde{b}$.
3. $A$ risponde con un $x'$, e $B$ lo inoltra al challenger.

<b>Perché funziona</b> *(spiegazione non negli appunti del prof)*:

- Con probabilità $1/2$ il bit indovinato è giusto: $\tilde{b} = h(x)$. In quel caso $A$ riceve esattamente $f_{\text{BAD}}(x)$, cioè la stessa cosa che riceverebbe nel suo gioco, quindi vince con la sua solita probabilità.
- Se $A$ vince, ha trovato un $x'$ con $f(x') \,\|\, h(x') = y \,\|\, \tilde{b}$. Guardando solo i primi bit: $f(x') = y$. Quindi $x'$ è una controimmagine di $y$ e anche $B$ vince.

$$
\Pr[B \text{ vince}] \ \ge\ \frac{1}{2} \cdot \Pr[A \text{ vince}] \ \ge\ \frac{1}{2} \cdot \frac{1}{\text{poly}(\lambda)} = \frac{1}{\text{poly}(\lambda)}
$$

Quindi $B$ inverte $f$ con probabilità non trascurabile, ma $f$ è una OWF: <b>contraddizione</b>. ∎

!!! note ""

    <b>Il trucco da ricordare</b> *(non negli appunti del prof)*: quando la riduzione non sa calcolare un pezzo dell'input dell'avversario, può <b>tirare a indovinare</b>. Se indovina con probabilità $1/2$ (o $1/\text{poly}$), perde solo un fattore polinomiale, e poly · (1/poly) resta 1/poly.

## Teorema di Goldreich-Levin

!!! abstract "In breve"

    Abbiamo visto che nessun $h$ fissato è hard-core per <b>tutte</b> le OWF. La cosa migliore che si può avere è il contrario: <b>per ogni</b> OWF $f$ esiste un hard-core bit. Il teorema lo costruisce: si aggiunge all'input una stringa casuale $r$, la si pubblica, e l'hard-core bit è il <b>prodotto scalare modulo 2</b> tra $x$ e $r$.

*(Il nome "Goldreich-Levin" non è negli appunti del prof, che lo chiama solo THM.)*

<b>La cosa migliore possibile</b>: non "$\exists h\ \forall f$" (impossibile, per $f_{\text{BAD}}$), ma "$\forall f\ \exists h$".

### Prodotto scalare modulo 2

*(Definizione non negli appunti del prof.)*

Per due stringhe di bit $x = (x_1, \dots, x_n)$ e $r = (r_1, \dots, r_n)$:

$$
\langle x, r \rangle = \sum_{i=1}^{n} x_i r_i \bmod 2
$$

Si moltiplicano i bit a coppie (cioè si fa l'AND) e si guarda se il numero di 1 ottenuti è pari (risultato 0) o dispari (risultato 1). In pratica: è lo <b>XOR dei bit di</b> $x$ <b>nelle posizioni in cui</b> $r$ <b>vale 1</b>.

!!! example ""

    <b>Esempio</b>: $x = 1011$, $r = 0110$.

    - posizione 1: $1 \cdot 0 = 0$
    - posizione 2: $0 \cdot 1 = 0$
    - posizione 3: $1 \cdot 1 = 1$
    - posizione 4: $1 \cdot 0 = 0$

    Somma $= 1$, quindi $\langle x, r \rangle = 1$. Detto in altro modo: $r$ "seleziona" le posizioni 2 e 3 di $x$, cioè i bit 0 e 1, e $0 \oplus 1 = 1$.

### Enunciato (del prof)

Sia $f : \{0,1\}^n \to \{0,1\}^n$ una OWF. Consideriamo

$$
g : \{0,1\}^{2n} \to \{0,1\}^{2n} \qquad g(x, r) = f(x) \,\|\, r \qquad \forall\, x, r \in \{0,1\}^n
$$

Allora $g$ è una OWF e

$$
h(x, r) = \langle x, r \rangle = \sum_{i=1}^{n} x_i r_i \bmod 2
$$

è <b>hard-core</b> per $g$.

!!! note ""

    <b>Cosa sono le cose</b>

    - $x$ = l'input segreto della OWF $f$; $r$ = una stringa casuale in più, della stessa lunghezza.
    - $g(x, r) = f(x) \,\|\, r$: calcola $f(x)$ e poi scrive $r$ <b>in chiaro</b>. Quindi chi vede l'output di $g$ conosce $r$ ma non $x$.
    - $h(x, r) = \langle x, r \rangle$: lo XOR di un <b>sottoinsieme casuale</b> dei bit di $x$, quello scelto da $r$.
    - In parole: anche conoscendo $f(x)$ e $r$, il bit $\langle x, r \rangle$ sembra completamente casuale.

<b>Perché</b> $g$ <b>è una OWF</b> *(non negli appunti del prof)*: invertire $g$ vuol dire, dato $f(x) \,\|\, r$, trovare $(x', r')$ con $f(x') \,\|\, r' = f(x) \,\|\, r$. In particolare $f(x') = f(x)$: chi inverte $g$ inverte anche $f$. È la stessa riduzione di $f_{\text{BAD}}$, ma senza nemmeno dover indovinare ($r$ è già dato).

### Intuizione (del prof)

Supponiamo che esista un avversario <b>bravissimo</b> che, dato $g(x, r)$, calcola <b>sempre</b> $h(x, r)$, per ogni $r$. Allora si ricava facilmente tutto $x$, scegliendo come $r$ le stringhe con un solo 1 ($e_i$ = tutti 0 tranne un 1 in posizione $i$):

$$
h(x, e_1) = \langle x, 10\cdots0 \rangle = x_1 \qquad \cdots \qquad h(x, e_n) = \langle x, 0\cdots01 \rangle = x_n
$$

Con $r = e_i$ il prodotto scalare "seleziona" solo il bit $i$ di $x$. Facendo $n$ domande si ricostruisce $x$ bit per bit, cioè si inverte $f$: impossibile, perché $f$ è one-way.

!!! example ""

    <b>Esempio</b> *(non negli appunti del prof)*: $x = 101$. $\langle x, 100 \rangle = 1$, $\langle x, 010 \rangle = 0$, $\langle x, 001 \rangle = 1$: si legge $x = 101$.

<b>Perché la dimostrazione vera è più difficile</b>: un avversario reale indovina $h(x, r)$ solo con probabilità $\frac{1}{2} + \frac{1}{\text{poly}}$, e solo <b>in media su</b> $r$ <b>casuale</b>. Sulle stringhe speciali $e_i$ potrebbe sbagliare sempre. La dimostrazione completa deve "amplificare" questo piccolo vantaggio, e il prof non la fa.

## Usare i PRG per battere Shannon

!!! abstract "In breve"

    Shannon dice che con la segretezza perfetta la chiave deve essere lunga quanto il messaggio. Con un PRG si aggira il limite: si usa una chiave <b>corta</b>, la si allunga con il PRG e si usa il risultato come un One-Time Pad.

### Lo schema (del prof)

Con un PRG $G : \{0,1\}^n \to \{0,1\}^{2n}$, chiave $k \in \{0,1\}^n$ e messaggi $m, c \in \{0,1\}^{2n}$:

$$
\text{Enc}(k, m) = G(k) \oplus m \qquad \text{Dec}(k, c) = G(k) \oplus c
$$

È un OTP in cui la chiave $G(k)$ non è davvero casuale, ma <b>pseudocasuale</b>. La correttezza è la stessa dell'OTP: $G(k) \oplus (G(k) \oplus m) = m$.

<b>La chiave è corta</b>: $n$ bit per un messaggio di $2n$ bit, quindi <b>più corta del messaggio</b>! Shannon non viene contraddetto, perché lo schema non è perfettamente segreto: è sicuro solo contro avversari efficienti.

!!! example ""

    <b>Esempio</b> *(valori di* $G$ *inventati, non negli appunti del prof)*: $n = 3$, $k = 101$, e supponiamo $G(101) = 110010$. Per cifrare $m = 011011$: $c = 110010 \oplus 011011 = 101001$. Bob, che conosce $k$, ricalcola $G(101) = 110010$ e fa $101001 \oplus 110010 = 011011 = m$. Si è usata una chiave di 3 bit per un messaggio di 6.

### È ancora one-time

Come l'OTP, questo schema si può usare <b>una sola volta</b>. Dati $c_1 = G(k) \oplus m_1$ e $c_2 = G(k) \oplus m_2$:

$$
c_1 \oplus c_2 = m_1 \oplus m_2
$$

perché $G(k) \oplus G(k) = 0$: la chiave sparisce, esattamente come nella Lezione 1.

## Sicurezza computazionale per la cifratura

!!! abstract "In breve"

    La segretezza perfetta chiede che i cifrati di due messaggi qualunque siano <b>identici</b> come distribuzione: nessuno, nemmeno con potenza infinita, li distingue. La versione computazionale chiede solo che siano <b>indistinguibili per avversari efficienti</b> ($\approx_c$).

<b>Ripasso (segretezza perfetta)</b>: per ogni $m_0, m_1$,

$$
\text{Enc}(K, m_0) \equiv \text{Enc}(K, m_1)
$$

quindi nemmeno un avversario <b>illimitato</b> riesce a distinguerli.

### Definizione: sicurezza computazionale one-time (del prof)

Uno SKE $\Pi = (\text{Enc}, \text{Dec})$ è <b>one-time computazionalmente sicuro</b> se

$$
\text{GAME}^{\text{one-time}}_{\Pi, A}(\lambda, 0) \ \approx_c\ \text{GAME}^{\text{one-time}}_{\Pi, A}(\lambda, 1)
$$

dove $\text{GAME}^{\text{one-time}}_{\Pi, A}(\lambda, b)$, con $b \in \{0, 1\}$, è:

```text
A                                    C
  ────────── m0, m1 ∈ M ──────────→
                                     k ← K
                                     c = Enc(k, m_b)
  ←─────────────── c ──────────────
  ─────────────── b' ─────────────→
```

1. $A$ sceglie <b>due messaggi</b> $m_0, m_1$ e li manda al challenger.
2. Il challenger sceglie una chiave $k$ a caso e cifra $m_b$: $c = \text{Enc}(k, m_b)$.
3. $A$ vede $c$ e risponde $b'$, il suo tentativo di indovinare quale dei due è stato cifrato.

In parole: <b>nessun avversario PPT</b> si comporta in modo (non trascurabilmente) diverso a seconda che sia stato cifrato $m_0$ o $m_1$.

!!! note ""

    <b>Differenze con il gioco della Lezione 2</b> *(non negli appunti del prof)*:

    - lì l'avversario poteva essere <b>illimitato</b> e la differenza doveva essere <b>esattamente 0</b>; qui l'avversario è <b>PPT</b> e la differenza deve essere <b>trascurabile</b>;
    - qui è l'avversario a <b>scegliere</b> $m_0$ e $m_1$: la definizione deve reggere anche per i messaggi più comodi per lui.

### Sanity checks (del prof)

Una buona definizione deve implicare le cose che ci aspettiamo da un cifrario. Questa le implica:

- <b>È difficile calcolare la chiave</b> $k$.
    - <b>Attenzione</b>: non basta! $\text{Enc}(k, m) = m$ (non cifrare proprio) soddisfa anche lui la proprietà che $k$ è difficile da calcolare, perché il cifrato non dice niente della chiave. Ma è ovviamente insicuro.
- <b>È difficile calcolare il messaggio</b> $m$.
- <b>Ma anche</b> il primo bit di $m$, il secondo bit, … : nessuna informazione parziale sul messaggio.

*Perché la definizione implica tutto questo (non negli appunti del prof)*: se un avversario sapesse calcolare $k$ (o $m$, o il primo bit di $m$), vincerebbe il gioco. Basta scegliere $m_0$ e $m_1$ che differiscono proprio in quello che sa calcolare (es. $m_0$ che inizia con 0 e $m_1$ che inizia con 1), calcolarlo dal cifrato e rispondere di conseguenza.

## Teorema: il PRG dà cifratura one-time sicura

!!! abstract "In breve"

    Se $G$ è un PRG, lo schema $\text{Enc}(k, m) = G(k) \oplus m$ è one-time computazionalmente sicuro. La dimostrazione usa il <b>game hopping</b>: si passa dal gioco con $b = 0$ a quello con $b = 1$ attraverso giochi intermedi, mostrando che ogni salto è invisibile.

### Enunciato (del prof)

Assumendo che $G$ sia un PRG, lo SKE definito sopra è <b>one-time computazionalmente sicuro</b>.

### Game hopping

<b>Game hopping</b> (tecnica di dimostrazione molto comune): si parte dai due giochi da confrontare,

$$
G_0 \equiv \text{GAME}^{\text{one-time}}_{\Pi, A}(\lambda, 0) \qquad G_1 \equiv \text{GAME}^{\text{one-time}}_{\Pi, A}(\lambda, 1)
$$

e bisogna mostrare $G_0 \approx_c G_1$. Si introducono <b>due giochi in più</b>, $H_0$ e $H_1$:

```text
                 G_b  /  H_b
A                                    C
  ────────── m0, m1 ──────────────→
                                     k ← {0,1}^n ;   z ← U_2n
                                     G_b:  c_b = G(k) ⊕ m_b
                                     H_b:  c_b = z ⊕ m_b
  ←─────────────── c ──────────────
  ─────────────── b' ─────────────→
```

- In $G_b$ si cifra con il PRG: $c = G(k) \oplus m_b$ (lo schema vero).
- In $H_b$ si cifra con una stringa <b>davvero casuale</b> $z$ di $2n$ bit: $c = z \oplus m_b$. È un vero OTP.

È la stessa idea dell'argomento ibrido della Lezione 5 *(collegamento non negli appunti del prof)*: si sostituisce il pezzo pseudocasuale con uno davvero casuale.

### Il piano

1. $H_0 \equiv H_1$: segue dalla <b>segretezza perfetta dell'OTP</b> (Lezione 1). Con $z$ uniforme, $z \oplus m_0$ e $z \oplus m_1$ hanno la stessa distribuzione, quindi $A$ si comporta in modo identico.
2. Resta da mostrare $G_b \approx_c H_b$ (per ogni $b$). Allora:

$$
G_0 \ \approx_c\ H_0 \ \equiv\ H_1 \ \approx_c\ G_1
$$

*Perché la catena basta (non negli appunti del prof)*: il vantaggio di $A$ tra $G_0$ e $G_1$ è al più la somma dei vantaggi sui singoli passi (disuguaglianza triangolare): $\text{negl} + 0 + \text{negl} = \text{negl}$.

### La riduzione: G_b ≈c H_b

<b>Supponiamo di no</b>: esiste un PPT $A$ che distingue $G_b$ da $H_b$ (per qualche $b \in \{0, 1\}$) con probabilità $\ge 1/\text{poly}$. Costruiamo $B$ che rompe il PRG:

```text
A                         B                              C
                                                         z = G(k), k ← U_n
                                                         oppure  z ← U_2n
                          ←──────────── z ─────────────
  ←────── "START" ──────
  ─────── m0, m1 ───────→
  ←──── c = m_b ⊕ z ─────
  ────────── b' ────────→
                          ──────────── b' ─────────────→
```

1. $B$ riceve dal challenger del PRG una stringa $z$ di $2n$ bit: o $z = G(k)$ con $k$ casuale, o $z$ davvero casuale.
2. $B$ fa partire $A$ ("START") e riceve i suoi due messaggi $m_0, m_1$.
3. $B$ risponde con $c = m_b \oplus z$ (usa $z$ come se fosse la chiave dell'OTP).
4. Quando $A$ risponde $b'$, $B$ inoltra $b'$ al challenger.

<b>Riduzione perfetta</b>: $B$ simula esattamente uno dei due giochi.

$$
\Pr[B \Rightarrow 1 : z = G(k)] = \Pr[A \Rightarrow 1 : \text{in } G_b]
$$

$$
\Pr[B \Rightarrow 1 : z \leftarrow U_{2n}] = \Pr[A \Rightarrow 1 : \text{in } H_b]
$$

- Se $z = G(k)$, allora $c = G(k) \oplus m_b$: è esattamente $G_b$.
- Se $z$ è casuale, allora $c = z \oplus m_b$: è esattamente $H_b$.

Quindi il vantaggio di $B$ contro il PRG è uguale a quello di $A$ tra $G_b$ e $H_b$, cioè $\ge 1/\text{poly}$: $B$ rompe $G$. Ma $G$ è un PRG: <b>contraddizione</b>. Inoltre $B$ è PPT, perché fa solo uno XOR in più rispetto ad $A$. ∎

## Riepilogo

- <b>f_BAD è una OWF</b>: la riduzione $B$ non conosce $h(x)$ e lo <b>indovina</b> con un bit casuale; $\Pr[B \text{ vince}] \ge \frac{1}{2} \Pr[A \text{ vince}]$
- Nessun $h$ va bene per tutte le $f$, ma <b>per ogni</b> $f$ <b>esiste</b> un $h$ (<b>Goldreich-Levin</b>): $g(x, r) = f(x) \,\|\, r$ è una OWF e $h(x, r) = \langle x, r \rangle = \sum x_i r_i \bmod 2$ è hard-core per $g$
- Intuizione: un avversario perfetto con $r = e_i$ ricaverebbe $x$ bit per bit; la dimostrazione vera è difficile perché l'avversario ha solo un vantaggio $1/\text{poly}$ su $r$ casuale
- <b>Battere Shannon con un PRG</b>: $\text{Enc}(k, m) = G(k) \oplus m$ con $G : \{0,1\}^n \to \{0,1\}^{2n}$: chiave più corta del messaggio; ma è ancora <b>one-time</b> ($c_1 \oplus c_2 = m_1 \oplus m_2$)
- <b>Sicurezza one-time computazionale</b>: $A$ sceglie $m_0, m_1$, riceve $\text{Enc}(k, m_b)$; $\text{GAME}(\lambda, 0) \approx_c \text{GAME}(\lambda, 1)$. Implica che $k$, $m$ e ogni bit di $m$ sono difficili da calcolare ("$k$ difficile" da solo non basta: vedi $\text{Enc}(k, m) = m$)
- <b>Teorema</b>: $G$ PRG ⇒ lo schema è one-time computazionalmente sicuro. Prova con <b>game hopping</b>: $G_0 \approx_c H_0 \equiv H_1 \approx_c G_1$, dove $H_b$ usa un $z$ davvero casuale (OTP) e $G_b \approx_c H_b$ per riduzione perfetta al PRG
