# Crittografia – appunti di Luiggi

Appunti del corso di Crittografia (Prof. Daniele Venturi, Sapienza), in italiano. Seguono gli appunti scritti a mano dal prof; prima di ogni concetto importante c'è un riquadro **In breve**, e le parti aggiunte per capire meglio sono segnate *(non negli appunti del prof)*.

È una sezione separata da [`cryptography/`](../cryptography/): usa lo stesso preambolo condiviso (`common/preamble.sty`) ma ha capitoli e riquadri propri.

| Capitolo | File |
|---|---|
| Lezione 1 – Introduzione e segretezza perfetta | `chapters/lezione-1.tex` |
| Lezione 2 – Teorema di Shannon e MAC | `chapters/lezione-2.tex` |
| Lezione 3 – MAC da hash ed estrazione di casualità | `chapters/lezione-3.tex` |
| Lezione 4 – Sicurezza computazionale e OWF | `chapters/lezione-4.tex` |
| Lezione 5 – Pseudocasualità, PRG e hard-core bit | `chapters/lezione-5.tex` |
| Appendice – Ripasso di probabilità | `chapters/ripasso-probabilita.tex` |

## Compilare

```bash
cd crittografia-luiggi
latexmk -pdf main.tex
```

## Riquadri

`inbreve` (definizione corta), `esempio`, `nota`, `approfondimento{Titolo}`: sono definiti in `main.tex`.

I capitoli sono stati generati dalle pagine Notion con `tools/notion2latex.py` (pandoc + `tools/boxes.lua`); da qui in poi si modificano direttamente i `.tex`.
