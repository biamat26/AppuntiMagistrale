# Appunti Magistrale – Luiggi

Appunti di Luiggi per la magistrale in Cybersecurity (Sapienza), in LaTeX. Gli appunti di Matteo sono sul branch `main`.

| Materia | Cartella |
|---|---|
| Crittografia (Prof. Venturi) | [`crittografia/`](crittografia/) |
| Distributed Systems | [`sistemi-distribuiti/`](sistemi-distribuiti/) |
| Network Infrastructures (Prof. Cuomo) | [`network-infrastructures/`](network-infrastructures/) |

Preambolo comune (pacchetti, riquadri, macro): [`common/preamble.sty`](common/preamble.sty).

## Compilare

```bash
cd crittografia
latexmk -pdf main.tex
```

## Aggiungere una lezione

1. Crea `chapters/lezione-7.tex` che inizia con `\chapter{Lezione 7 – Titolo}`.
2. Aggiungi `\input{chapters/lezione-7}` in `main.tex`.

## Riquadri

- `\begin{inbreve} ... \end{inbreve}`: la definizione corta prima di ogni concetto importante.
- `\begin{esempio} ... \end{esempio}` e `\begin{nota} ... \end{nota}`.
- `\begin{approfondimento}{Titolo} ... \end{approfondimento}`: dimostrazioni, soluzioni, domande di ripasso.

Restano disponibili anche quelli numerati del preambolo (`frameddefn`, `framedthm`, …).
