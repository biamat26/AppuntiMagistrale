# Appunti Magistrale

LaTeX lecture notes for my Master's degree in Cybersecurity (Sapienza).

| Course | Folder |
|---|---|
| Cryptography | [`cryptography/`](cryptography/) |
| Crittografia (appunti di Luiggi, sito web: [biamat26.github.io/AppuntiMagistrale](https://biamat26.github.io/AppuntiMagistrale/)) | [`crittografia-luiggi/`](crittografia-luiggi/) |
| Distributed Systems | [`distributed-systems/`](distributed-systems/) |
| Network Infrastructures | [`network-infrastructures/`](network-infrastructures/) |
| Statistics | [`statistics/`](statistics/) |

Shared packages, colored boxes and macros live in [`common/preamble.sty`](common/preamble.sty).

## Build

```bash
cd distributed-systems
latexmk -pdf main.tex
```

## Adding a chapter

1. Create `chapters/02-topic.tex` starting with `\chapter{Topic}`.
2. Add `\input{chapters/02-topic}` to `main.tex`.

## Available environments

Numbered framed boxes (per chapter): `frameddefn`, `framedthm`, `framedlem`, `framedprop`,
`framedcor`, `framedobs`, `framedex`, `framedprob`, `framedalgo`.

```latex
\begin{frameddefn}[label={def:cut}]{Cut}
  ...
\end{frameddefn}
% reference with \Cref{def:cut}
```

Space-time diagrams (TikZ): `\proc{y}{p_1}{x_end}` draws a process line,
`\node[ev] (a) at (x,y) {};` an event, `\draw[msg] (a) -- (b);` a message.
