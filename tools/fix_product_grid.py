#!/usr/bin/env python3
"""Fix misaligned 2-column product grids in Valentte email HTML on mobile.

Problem: each product is one <td> holding image, title, prices and button
stacked together. When titles wrap to a different number of lines on a narrow
screen, the prices and "Shop Now" buttons below them drift out of line.

Fix: rebuild every two-product row as a 4-row table (image / title / price /
button) with one cell per product in each row. Cells in the same row always
share a height, so prices and buttons line up regardless of title length.
Also adds mobile CSS that shrinks titles and keeps "Shop Now ->" on one line.

Only rows whose two cells each contain image-link, title div, price div(s)
and a button link are touched; everything else is left byte-for-byte as is.
Running it twice is a no-op.

Usage: fix_product_grid.py in.html out.html
"""
import re
import sys

MARKER = 'class="pg-grid"'

CELL_RE = re.compile(
    r'(<td\b[^>]*class="stack-col"[^>]*>)(.*?)</td>', re.S)
ROW_RE = re.compile(
    r'<table\b[^>]*>\s*(?:<tbody>)?\s*<tr>\s*'
    r'(<td\b[^>]*class="stack-col"[^>]*>.*?</td>)\s*'
    r'(<td\b[^>]*width="1"[^>]*>.*?</td>)\s*'
    r'(<td\b[^>]*class="stack-col"[^>]*>.*?</td>)\s*'
    r'</tr>\s*(?:</tbody>)?\s*</table>', re.S)
CHILD_RE = re.compile(r'<a\b.*?</a>|<div\b.*?</div>', re.S)

MOBILE_CSS = (
    "    .pg-title div { font-size:18px !important; line-height:21px !important; }\n"
    "    .pg-btn a { padding:10px 12px !important; white-space:nowrap !important; }\n"
)


def split_cell(cell_html):
    m = CELL_RE.fullmatch(cell_html.strip())
    if not m:
        return None
    open_tag, inner = m.groups()
    kids = CHILD_RE.findall(inner)
    # Expect: image link, title div, one or more price divs, button link.
    if len(kids) < 4 or '<img' not in kids[0] or not kids[-1].startswith('<a'):
        return None
    if not all(k.startswith('<div') for k in kids[1:-1]):
        return None
    if '<img' in kids[-1]:
        return None
    # Make sure nothing else lives in the cell that we'd silently drop.
    leftover = CHILD_RE.sub('', inner).strip()
    if leftover:
        return None
    return open_tag, kids[0], kids[1], kids[2:-1], kids[-1]


def with_padding(open_tag, padding, extra_class=''):
    tag = re.sub(r'padding:\s*[^;"]+', 'padding:' + padding, open_tag, count=1)
    if 'padding:' not in tag:
        tag = tag.replace('style="', 'style="padding:%s;' % padding, 1)
    if extra_class:
        tag = tag.replace('class="stack-col"', 'class="stack-col %s"' % extra_class, 1)
    return tag


def nowrap(button):
    if 'white-space' in button:
        return button
    return re.sub(r'style="', 'style="white-space:nowrap;', button, count=1)


def rebuild(match):
    left, divider, right = match.groups()
    a, b = split_cell(left), split_cell(right)
    if not a or not b:
        return match.group(0)
    divider = divider.replace('<td ', '<td rowspan="4" ', 1)

    def row(parts, valign=None):
        cells = []
        for tag, body in parts:
            if valign:
                tag = re.sub(r'valign="[^"]*"', 'valign="%s"' % valign, tag, count=1)
            cells.append('            %s%s</td>' % (tag, body))
        return cells

    out = ['<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" class="pg-grid">',
           '          <tbody><tr>']
    img = row([(with_padding(a[0], '24px 10px 0'), a[1]),
               (with_padding(b[0], '24px 10px 0'), b[1])])
    out += [img[0], '            ' + divider, img[1], '          </tr>', '          <tr>']
    out += row([(with_padding(a[0], '0 10px', 'pg-title'), a[2]),
                (with_padding(b[0], '0 10px', 'pg-title'), b[2])], 'top')
    out += ['          </tr>', '          <tr>']
    out += row([(with_padding(a[0], '0 10px'), ''.join(a[3])),
                (with_padding(b[0], '0 10px'), ''.join(b[3]))], 'bottom')
    out += ['          </tr>', '          <tr>']
    out += row([(with_padding(a[0], '0 10px 26px', 'pg-btn'), nowrap(a[4])),
                (with_padding(b[0], '0 10px 26px', 'pg-btn'), nowrap(b[4]))], 'top')
    out += ['          </tr>', '        </tbody></table>']
    return '\n'.join(out)


STACK_RULE_RE = re.compile(r'(\.stack-col\s*\{)([^}]*display:\s*block[^}]*width:\s*100%[^}]*)\}')


def fix_stack_overflow(html):
    """Columns that stack on mobile get width:100% plus their own padding, which
    pushes them wider than the phone screen (the whole email then pans sideways).
    border-box keeps the padding inside the 100%."""
    def add(m):
        if 'box-sizing' in m.group(2):
            return m.group(0)
        return m.group(1) + m.group(2).rstrip() + ' box-sizing:border-box !important; }'
    return STACK_RULE_RE.sub(add, html)


def fix(html):
    html = fix_stack_overflow(html)
    if MARKER in html:
        return html, 0
    new, n = ROW_RE.subn(rebuild, html)
    changed = new.count(MARKER)
    if changed and '.pg-title' not in new:
        mq = re.search(r'@media[^{]*max-width[^{]*\{', new)
        if mq:
            new = new[:mq.end()] + '\n' + MOBILE_CSS.rstrip('\n') + new[mq.end():]
        else:
            new = new.replace('</head>', '<style>\n  @media only screen and (max-width:620px) {\n'
                              + MOBILE_CSS + '  }\n</style>\n</head>', 1)
    return new, changed


if __name__ == '__main__':
    src, dst = sys.argv[1], sys.argv[2]
    html = open(src, encoding='utf-8').read()
    new, changed = fix(html)
    open(dst, 'w', encoding='utf-8').write(new)
    print('%d product row(s) rebuilt' % changed)
    # Bloomreach's visual editor sometimes escapes pasted rows into visible text.
    if re.search(r'&lt;/?(tr|td|table|a|img)\b', new):
        print('WARNING: escaped HTML tags found (e.g. &lt;tr&gt;) - these render as raw code in the email')
