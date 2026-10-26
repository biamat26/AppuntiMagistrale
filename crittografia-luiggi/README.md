# Crittografia – appunti di Luiggi

Appunti del corso di Crittografia (Prof. Daniele Venturi, Sapienza), in italiano, pubblicati come sito web:
**https://biamat26.github.io/AppuntiMagistrale/**

Seguono gli appunti scritti a mano dal prof; prima di ogni concetto importante c'è un riquadro **In breve**, e le parti aggiunte per capire meglio sono segnate *(non negli appunti del prof)*.

## Struttura

- `docs/` – le pagine (Markdown con formule LaTeX tra `$...$` e `$$...$$`)
- `mkdocs.yml` – configurazione del sito (MkDocs Material) e menu
- `tools/notion2mkdocs.py` – script usato per importare le pagine da Notion

## Aggiungere una lezione

1. Crea `docs/lezione-6.md`.
2. Aggiungila sotto `nav:` in `mkdocs.yml`.
3. Fai push: il sito si ricostruisce da solo (workflow `.github/workflows/sito-crittografia-luiggi.yml`).

## Vedere il sito in locale

```bash
pip install "mkdocs<2" mkdocs-material
mkdocs serve -f crittografia-luiggi/mkdocs.yml
```
