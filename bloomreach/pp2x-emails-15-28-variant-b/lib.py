"""Helpers that render Figma 'Variant B' sections as email-safe HTML (vb-* style, matching Emails 8-14 Test B)."""
import html as _html, json, os, re

S = os.path.dirname(os.path.abspath(__file__))
SHELL = os.path.join(S, 'shell')
CG = "'Cormorant Garamond',Georgia,'Times New Roman',serif"
MU = "Mulish,Arial,Helvetica,sans-serif"
SITE = "https://valentte.com"
URLS = json.load(open(os.path.join(S, 'urls.json'))) if os.path.exists(os.path.join(S, 'urls.json')) else {}
CROPS = []  # (email, key, x, y, w, h, fmt) registered while building

EMAIL = None


def refer(n):
    return ("https://www.valentte.com/refer-a-friend?email={{ customer.email }}&firstname={{ customer.first_name }}"
            "&surname={{ customer.last_name }}&situation=Bloomreach-Emails-PP2x-E%d-TestB&locale=en_GB&segment=loyalty" % n)


def esc(s):
    s = _html.escape(s, quote=False)
    s = s.replace('[First name]', "{{ fn if fn else 'there' }}")
    return s.replace('\n', '<br>')


def _a(inner, link, color='inherit'):
    if not link:
        return inner
    return '<a href="%s" target="_blank" style="display:block;text-decoration:none;color:%s;">%s</a>' % (link, color, inner)


def T(text, fam, size, color, weight=400, lh=1.2, align='center', ls=None, upper=False, italic=False, link=None, nowrap=False):
    """Text block. lh is a multiplier (Figma % / 100)."""
    f = CG if fam == 'CG' else MU
    st = ["margin:0", "font-family:%s" % f, "font-size:%spx" % size, "color:%s" % color, "font-weight:%d" % weight,
          "line-height:%spx" % round(size * lh, 2), "text-align:%s" % align, "mso-line-height-rule:exactly"]
    if italic: st.append("font-style:italic")
    if ls: st.append("letter-spacing:%sem" % ls)
    if upper: st.append("text-transform:uppercase")
    if nowrap: st.append("white-space:nowrap")
    div = '<div style="%s;">%s</div>' % (';'.join(st), esc(text))
    return _a(div, link)


def gap(h):
    return '<div style="height:%dpx;line-height:%dpx;font-size:1px;mso-line-height-rule:exactly;">&nbsp;</div>' % (h, h)


def V(children, g=0):
    out = []
    for i, c in enumerate(children):
        if i and g: out.append(gap(g))
        out.append(c)
    return ''.join(out)


def center(inner, align='center'):
    return ('<table role="presentation" width="100%%" cellpadding="0" cellspacing="0" border="0"><tr><td align="%s">'
            '<table role="presentation" cellpadding="0" cellspacing="0" border="0" align="%s"><tr><td>%s</td></tr></table></td></tr></table>'
            % (align, align, inner))


def box(inner, bg=None, pad=(0, 0, 0, 0), r=0, border=None, valign='top', align='left'):
    st = ["padding:%dpx %dpx %dpx %dpx" % pad]
    if bg: st.append("background-color:%s" % bg)
    if r: st.append("border-radius:%dpx" % r)
    if border: st.append("border:%s" % border)
    bgattr = ' bgcolor="%s"' % bg if bg else ''
    return ('<table role="presentation" width="100%%" cellpadding="0" cellspacing="0" border="0" style="border-collapse:separate;">'
            '<tr><td%s align="%s" valign="%s" style="%s;">%s</td></tr></table>' % (bgattr, align, valign, ';'.join(st), inner))


def H(cols, total, g=0, valign='top', bg=None, r=0, fixed=False):
    """cols: list of (width, html); ('rule', (colour, height)) inserts a 1px vertical divider.
    fixed=True renders a centred table exactly `total` px wide instead of 100%."""
    tds = []
    for i, (w, inner) in enumerate(cols):
        if i and g:
            tds.append('<td width="%d" class="vb-gap" style="width:%.3f%%;font-size:1px;line-height:1px;">&nbsp;</td>' % (g, g * 100.0 / total))
        if w == 'rule':
            col, h = inner
            tds.append('<td width="1" valign="middle" style="width:1px;"><div style="width:1px;height:%dpx;background-color:%s;font-size:1px;line-height:1px;">&nbsp;</div></td>' % (h, col))
            continue
        tds.append('<td width="%d" class="vb-col" valign="%s" style="width:%.3f%%;">%s</td>' % (w, valign, w * 100.0 / total, inner))
    st = "border-collapse:separate;"
    bgattr = ''
    if bg:
        st += "background-color:%s;" % bg
        bgattr = ' bgcolor="%s"' % bg
    if r: st += "border-radius:%dpx;" % r
    if fixed:
        return ('<table role="presentation" width="%d" align="center" cellpadding="0" cellspacing="0" border="0"%s style="width:%dpx;max-width:100%%;%s"><tr>%s</tr></table>'
                % (total, bgattr, total, st, ''.join(tds)))
    return ('<table role="presentation" width="100%%" cellpadding="0" cellspacing="0" border="0"%s style="%s"><tr>%s</tr></table>'
            % (bgattr, st, ''.join(tds)))


def img(key, x, y, w, h, alt, link=None, fmt='jpg', disp_w=None):
    CROPS.append((EMAIL, key, x, y, w, h, fmt))
    src = URLS.get('%s_%s' % (EMAIL, key), 'PENDING:%s_%s' % (EMAIL, key))
    dw = disp_w or w
    tag = ('<img src="%s" width="%d" alt="%s" class="vb-img" style="display:block;width:100%%;max-width:%dpx;height:auto;border:0;outline:none;">'
           % (src, dw, _html.escape(alt), dw))
    return _a(tag, link)


def icon(key, x, y, size, alt=''):
    CROPS.append((EMAIL, key, x, y, size, size, 'png'))
    src = URLS.get('%s_%s' % (EMAIL, key), 'PENDING:%s_%s' % (EMAIL, key))
    return ('<img src="%s" width="%d" height="%d" alt="%s" style="display:block;width:%dpx;height:%dpx;border:0;outline:none;">'
            % (src, size, size, _html.escape(alt), size, size))


def cta(label, link, size=15, pv=15, ph=32, align='center'):
    btn = ('<table role="presentation" cellpadding="0" cellspacing="0" border="0" align="%s" style="border-collapse:separate;border-radius:3px;">'
           '<tr><td bgcolor="#ffa220" align="center" valign="middle" style="padding:%dpx %dpx %dpx %dpx;background-color:#ffa220;border-radius:3px;">'
           '<a href="%s" target="_blank" style="display:block;text-decoration:none;color:#212121;">'
           '<div style="margin:0;font-family:%s;font-size:%spx;color:#212121;font-weight:700;line-height:%spx;text-align:center;mso-line-height-rule:exactly;white-space:nowrap;">%s&nbsp;&#8594;</div>'
           '</a></td></tr></table>') % (align, pv, ph, pv, ph, link, MU, size, round(size * 1.2, 2), esc(label))
    return ('<table role="presentation" width="100%%" cellpadding="0" cellspacing="0" border="0"><tr><td align="%s">%s</td></tr></table>'
            % (align, btn))


def num(d, bg, color='#ffffff', size=34, fs=16, align='center'):
    c = ('<table role="presentation" cellpadding="0" cellspacing="0" border="0" align="%s" style="border-collapse:separate;"><tr>'
         '<td width="%d" height="%d" bgcolor="%s" align="center" valign="middle" style="width:%dpx;height:%dpx;background-color:%s;border-radius:%dpx;'
         'font-family:%s;font-size:%dpx;font-weight:600;color:%s;line-height:%dpx;text-align:center;mso-line-height-rule:exactly;">%s</td></tr></table>'
         % (align, size, size, bg, size, size, bg, size // 2, CG, fs, color, size, d))
    return ('<table role="presentation" width="100%%" cellpadding="0" cellspacing="0" border="0"><tr><td align="%s">%s</td></tr></table>' % (align, c))


def section(inner, bg='#ffffff', pad=(0, 0, 0, 0), border_top=None):
    st = "padding:%dpx %dpx %dpx %dpx;" % pad
    if border_top: st += "border-top:%s;" % border_top
    return ('<table class="row vb" align="center" width="100%%" border="0" cellpadding="0" cellspacing="0" role="presentation"><tbody><tr><td align="center">'
            '<table class="vb-wrap" align="center" width="600" border="0" cellpadding="0" cellspacing="0" role="presentation" style="width:600px;max-width:600px;background-color:%s;">'
            '<tr><td class="%s" align="center" valign="top" bgcolor="%s" style="%sbackground-color:%s;">%s</td></tr></table></td></tr></tbody></table>'
            % (bg, 'vb-pad' if pad[1] or pad[3] else '', bg, st, bg, inner))


def hero(y, h, alt, link):
    """Flattened hero image (photo + scrim + overlay copy, exactly as Figma renders it)."""
    return section(img('hero', 0, y, 600, h, alt, link))


def wrap(body, preheader, n):
    pre = open(os.path.join(SHELL, 'n3.html.pre')).read().replace('PREHEADER', _html.escape(preheader, quote=False))
    suf = open(os.path.join(SHELL, 'n3.html.suf')).read().replace('situation=X', 'situation=Bloomreach-Emails-PP2x-E%d-TestB' % n)
    h = (pre + body + suf).replace(CG, "Cormorant Garamond,Georgia,Times New Roman,serif")
    # single-quote attributes and drop newlines so the blob needs almost no JSON escaping in the node payload
    h = re.sub(r'(\s[\w:-]+)="([^"\']*)"', lambda m: "%s='%s'" % (m.group(1), m.group(2)), h)
    return h.replace('\n', ' ').strip()
