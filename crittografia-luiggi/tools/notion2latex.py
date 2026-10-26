"""Converte le pagine Notion (markdown esportato da notion-fetch) in capitoli LaTeX.

Uso: python3 notion2latex.py <cartella_raw> <cartella_chapters>
Ogni file raw inizia con 'TITLE: <titolo>' seguito dal markdown Notion.
Richiede pandoc; usa il filtro boxes.lua nella stessa cartella.
"""
import pathlib
import re
import subprocess
import sys

HERE = pathlib.Path(__file__).parent

MENTIONS = {
    '3f5b1b09a64781cb8091fac690c93b9b': 'Lezione 5',
    '3f4b1b09a64781769778d31d628a07de': 'Lezione 4',
}


def html_inline(text):
    """<b>/<i> -> markdown, spostando gli spazi fuori dai marcatori."""
    for tag, mark in (('b', '**'), ('i', '*')):
        text = re.sub(
            rf'<{tag}>(\s*)(.*?)(\s*)</{tag}>',
            lambda m: f'{m.group(1)}{mark}{m.group(2)}{mark}{m.group(3)}' if m.group(2) else m.group(1) + m.group(3),
            text, flags=re.S)
    return text


def quote_block_lines(text):
    out = []
    for p in text.split('<br />'):
        p = p.rstrip()
        if p.startswith('\\- '):
            p = '- ' + p[3:]
        if p.startswith('- ') and out and not out[-1].startswith('- ') and out[-1] != '':
            out.append('')
        if not p.startswith('- ') and out and out[-1].startswith('- '):
            out.append('')
        out.append(p)
    return out


def convert_quotes(lines):
    res, i = [], 0
    while i < len(lines):
        if not lines[i].startswith('> '):
            res.append(lines[i]); i += 1; continue
        blocks, j = [lines[i][2:]], i + 1
        while True:
            k = j
            while k < len(lines) and not lines[k].strip():
                k += 1
            if k < len(lines) and lines[k].startswith('> ') and not lines[k][2:].startswith('<b>'):
                blocks.append(lines[k][2:]); j = k + 1
            else:
                break
        first = blocks[0]
        if first.startswith('<b>In breve</b>'):
            cls = 'inbreve'
            b0 = re.sub(r'^<b>In breve</b>\s*:?\s*', '', first)
            blocks[0] = b0[:1].upper() + b0[1:]
        elif re.match(r'^(<b>)?Esempi', first):
            cls = 'esempio'
        else:
            cls = 'nota'
        body = []
        for b in blocks:
            if body:
                body.append('')
            body.extend(quote_block_lines(b))
        res += ['', f'::: {{.{cls}}}', *body, ':::', '']
        i = j
    return res


def convert_toggles(text):
    def rep(m):
        inner = m.group(1).strip('\n').split('\n')
        title = inner[0].strip().replace('"', "'")
        return f'\n::: {{.approfondimento title="{title}"}}\n' + '\n'.join(inner[1:]).strip('\n') + '\n:::\n'
    return re.sub(r'<toggle>\n(.*?)\n</toggle>', rep, text, flags=re.S)


def to_markdown(raw):
    title_line, body = raw.split('\n', 1)
    title = re.sub(r'^[^\w]+\s*', '', title_line[len('TITLE: '):].strip())
    text = body.replace('```javascript', '```').replace('\\^', '^').replace('\\_', '_')
    text = re.sub(r'<mention url="https://app\.notion\.com/p/(\w+)"\s*/>',
                  lambda m: MENTIONS.get(m.group(1), 'pagina collegata'), text)
    out, buf, in_code = [], [], False
    for line in text.split('\n'):
        if line.startswith('```'):
            if not in_code:
                out.extend(convert_quotes(buf)); buf = []
            in_code = not in_code
            out.append(line)
            continue
        (out if in_code else buf).append(line)
    out.extend(convert_quotes(buf))
    text = convert_toggles('\n'.join(out))
    text = html_inline(text)
    if not text.lstrip().startswith('# '):
        text = f'# {title}\n\n' + text
    return text


def to_latex(md):
    return subprocess.run(
        ['pandoc', '-f', 'markdown-auto_identifiers', '-t', 'latex',
         '--top-level-division=chapter', '--no-highlight', '--wrap=preserve',
         '--lua-filter', str(HERE / 'boxes.lua')],
        input=md, capture_output=True, text=True, check=True).stdout


if __name__ == '__main__':
    src, dst = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])
    dst.mkdir(parents=True, exist_ok=True)
    for f in sorted(src.glob('*.md')):
        tex = to_latex(to_markdown(f.read_text()))
        header = f'% Generato da tools/notion2latex.py a partire dalla pagina Notion "{f.stem}".\n\n'
        (dst / (f.stem + '.tex')).write_text(header + tex)
        print('ok', f.stem)
