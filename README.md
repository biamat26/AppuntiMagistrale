# Appunti Magistrale – Luiggi

Appunti di Luiggi per la magistrale in Cybersecurity (Sapienza), pubblicati come sito web:
**https://biamat26.github.io/AppuntiMagistrale/**

Gli appunti di Matteo sono sul branch `main`.

| Materia | Cartella |
|---|---|
| Crittografia | [`docs/crittografia/`](docs/crittografia/) |
| Distributed Systems | [`docs/sistemi-distribuiti/`](docs/sistemi-distribuiti/) |
| Network Infrastructures | [`docs/network-infrastructures/`](docs/network-infrastructures/) |

## Come funziona

- Le pagine sono file Markdown in `docs/`, con formule LaTeX tra `$...$` e `$$...$$`.
- `mkdocs.yml` contiene la configurazione del sito (MkDocs Material) e il menu (`nav:`).
- Ogni push su questo branch che tocca `docs/` o `mkdocs.yml` ricostruisce il sito (workflow `.github/workflows/sito.yml`, pubblica sul branch `gh-pages`).
- `tools/notion2mkdocs.py` è lo script usato per importare le pagine da Notion.

## Aggiungere una lezione

1. Crea il file, es. `docs/crittografia/lezione-6.md`.
2. Aggiungilo sotto la materia giusta in `nav:` in `mkdocs.yml`.
3. Fai push.

## Vedere il sito in locale

```bash
pip install "mkdocs<2" mkdocs-material
mkdocs serve
```
