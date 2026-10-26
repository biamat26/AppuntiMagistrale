"""Convert Notion-flavoured markdown (from notion-fetch) into MkDocs Material markdown."""
import re, sys, pathlib

MENTIONS = {
    '3f5b1b09a64781cb8091fac690c93b9b': ('Lezione 5', 'lezione-5.md'),
    '3f4b1b09a64781769778d31d628a07de': ('Lezione 4', 'lezione-4.md'),
}


def indent(lines, n=4):
    return [(' ' * n + l) if l.strip() else '' for l in lines]


def quote_block_lines(text):
    """One Notion quote paragraph -> list of markdown lines (handles <br /> lists and '\\-' bullets)."""
    out = []
    parts = text.split('<br />')
    for i, p in enumerate(parts):
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
    res = []
    i = 0
    while i < len(lines):
        if not lines[i].startswith('> '):
            res.append(lines[i]); i += 1; continue
        # collect consecutive quote paragraphs (separated only by blank lines);
        # a new paragraph starting with <b> starts a new admonition
        blocks = [lines[i][2:]]
        j = i + 1
        while True:
            k = j
            while k < len(lines) and lines[k].strip() == '':
                k += 1
            if k < len(lines) and lines[k].startswith('> ') and not lines[k][2:].startswith('<b>'):
                blocks.append(lines[k][2:]); j = k + 1
            else:
                break
        first = blocks[0]
        if first.startswith('<b>In breve</b>'):
            head = '!!! abstract "In breve"'
            b0 = re.sub(r'^<b>In breve</b>\s*:?\s*', '', first)
            blocks[0] = b0[:1].upper() + b0[1:]
        elif re.match(r'^(<b>)?Esempi', first):
            head = '!!! example ""'
        else:
            head = '!!! note ""'
        body = []
        for b in blocks:
            bl = quote_block_lines(b)
            if body:
                body.append('')
            body.extend(bl)
        res.append(head)
        res.append('')
        res.extend(indent(body))
        res.append('')
        i = j
    return res


def convert_toggles(text):
    def rep(m):
        inner = m.group(1).strip('\n').split('\n')
        title = inner[0].strip().replace('"', "'")
        body = inner[1:]
        while body and not body[0].strip():
            body.pop(0)
        return '??? note "' + title + '"\n\n' + '\n'.join(indent(body)) + '\n'
    return re.sub(r'<toggle>\n(.*?)\n</toggle>', rep, text, flags=re.S)


def convert(raw):
    title_line, body = raw.split('\n', 1)
    title = title_line[len('TITLE: '):].strip()
    title = re.sub(r'^[^\w]+\s*', '', title)  # drop leading emoji
    text = body
    text = text.replace('```javascript', '```text')
    text = text.replace('\\^', '^').replace('\\_', '_')
    def mention(m):
        pid = m.group(1)
        name, href = MENTIONS.get(pid, ('pagina', '#'))
        return f'[{name}]({href})'
    text = re.sub(r'<mention url="https://app\.notion\.com/p/(\w+)"\s*/>', mention, text)
    lines = text.split('\n')
    # don't touch content of code fences
    out, buf, in_code = [], [], False
    for l in lines:
        if l.startswith('```'):
            if not in_code:
                out.extend(convert_quotes(buf)); buf = []
                in_code = True; out.append(l)
            else:
                in_code = False; out.append(l)
            continue
        (out if in_code else buf).append(l)
    out.extend(convert_quotes(buf))
    text = '\n'.join(out)
    text = convert_toggles(text)
    if not text.lstrip().startswith('# '):
        text = f'# {title}\n\n' + text
    text = re.sub(r'\n{3,}', '\n\n', text).strip() + '\n'
    return text


if __name__ == '__main__':
    src, dst = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])
    for f in sorted(src.glob('*.md')):
        (dst / f.name).write_text(convert(f.read_text()))
        print('converted', f.name)
