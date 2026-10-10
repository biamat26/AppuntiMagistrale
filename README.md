# Appunti Magistrale

LaTeX lecture notes for my Master's degree in Cybersecurity (Sapienza).

| Course | Folder |
|---|---|
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

- `definition`, `theorem`, `lemma`, `proposition`, `example` — numbered boxes:
  `\begin{definition}{Title}{label} ... \end{definition}` (reference with `\cref{def:label}`)
- `note`, `warning`, `summary` — unnumbered boxes
- `proof`, `algorithm` + `algorithmic`, `lstlisting`
