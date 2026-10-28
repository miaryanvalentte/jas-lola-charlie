"""Helpers that render Figma 'Variant B' sections as email-safe HTML, wrapped in the Aiden Header and Zac Footer."""
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
    return ("https://www.valentte.com/refer-a-friend?email={{ (customer.email or '') | urlencode }}&firstname={{ (customer.first_name or '') | urlencode }}"
            "&surname={{ (customer.last_name or '') | urlencode }}&situation=Bloomreach-Emails-PP2x-E%d-TestB&locale=en_GB&segment=loyalty" % n).replace('&', '&amp;')


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


def H(cols, total, g=0, valign='top', bg=None, r=0, fixed=False, stack=False, rtl=False):
    """cols: list of (width, html); ('rule', (colour, height)) inserts a 1px vertical divider.
    fixed=True renders a centred table exactly `total` px wide instead of 100%.
    stack=True lets the columns stack full-width on phones (max-width 620px).
    rtl=True shows the columns right-to-left on desktop while keeping DOM order for the mobile stack."""
    colcls, gapcls = ('vb-col vb-stack', 'vb-gap vb-stackgap') if stack else ('vb-col', 'vb-gap')
    tds = []
    for i, (w, inner) in enumerate(cols):
        if i and g:
            tds.append('<td width="%d" class="%s" style="width:%.3f%%;font-size:1px;line-height:1px;">&nbsp;</td>' % (g, gapcls, g * 100.0 / total))
        if w == 'rule':
            col, h = inner
            tds.append('<td width="1" valign="middle" style="width:1px;"><div style="width:1px;height:%dpx;background-color:%s;font-size:1px;line-height:1px;">&nbsp;</div></td>' % (h, col))
            continue
        tds.append('<td width="%d" class="%s" valign="%s"%s style="width:%.3f%%;">%s</td>' % (w, colcls, valign, ' dir="ltr"' if rtl else '', w * 100.0 / total, inner))
    st = "border-collapse:separate;"
    bgattr = ' dir="rtl"' if rtl else ''
    if bg:
        st += "background-color:%s;" % bg
        bgattr += ' bgcolor="%s"' % bg
    if r: st += "border-radius:%dpx;" % r
    if fixed:
        return ('<table role="presentation" width="%d" align="center" cellpadding="0" cellspacing="0" border="0"%s style="width:100%%;max-width:%dpx;%s"><tr>%s</tr></table>'
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


AIDEN_HEADER = 'https://d2ol7oe51mr4n9.cloudfront.net/user_3J5VVo50uL70F327Y6AS8CqWwV6/84de175c-9db0-4b16-9a60-78f06518f4d0.png'
NAV = (('Offers', SITE + '/sale/'), ('Home Fragrance', SITE + '/about-home-fragrance/'), ('Best Sellers', SITE + '/best-sellers/'))
ALSO_LIKE = (('GIFTING', SITE + '/all-gifts/', 'CategoriesA11%401.5x.png'),
             ('REFILLS', SITE + '/home-fragrance/100ml-refill/', 'CategoriesA12%401.5x.png'),
             ('OFFERS', SITE + '/sale/', 'CategoriesA13%401.5x.png'))
BEE_IMG = 'https://d15k2d11r6t6rl.cloudfront.net/public/users/Integrators/ae52a6e2-ca6a-4d8e-8944-532f952aae85/2e25bbd8-55a8-11f0-9f79-9aae66778e25/'

HEAD = ('''{%- set fn = (customer.first_name or '') | trim | capitalize -%}
<!DOCTYPE html><html xmlns:v="urn:schemas-microsoft-com:vml" xmlns:o="urn:schemas-microsoft-com:office:office" lang="en"><head><title>Valentte</title>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<!--[if mso]><xml><o:OfficeDocumentSettings><o:PixelsPerInch>96</o:PixelsPerInch><o:AllowPNG/></o:OfficeDocumentSettings></xml><![endif]-->
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,600;0,700;1,400;1,600&family=Mulish:wght@400;600;700&display=swap" rel="stylesheet" type="text/css">
<style>*{box-sizing:border-box}body{margin:0;padding:0}a[x-apple-data-detectors]{color:inherit!important;text-decoration:inherit!important}#MessageViewBody a{color:inherit;text-decoration:none}
.vb-wrap{width:600px}
@media (max-width:620px){.vb-wrap{width:100%!important}.vb-pad{padding-left:20px!important;padding-right:20px!important}.vb-img{width:100%!important;height:auto!important}
.vb-stack{display:block!important;width:100%!important;max-width:100%!important}.vb-stack .vb-img{max-width:100%!important}.vb-stackgap{display:block!important;width:100%!important;height:14px!important}}
</style></head>
<body style="margin:0;padding:0;-webkit-text-size-adjust:none;text-size-adjust:none;background-color:#f7f7f7">''')


def header():
    logo = section(_a('<img src="%s" width="600" alt="Valentte London" class="vb-img" style="display:block;width:100%%;max-width:600px;height:auto;border:0;outline:none;">' % AIDEN_HEADER, SITE + '/'))
    nav = H([(200, T(t, 'MU', 14, '#333333', lh=1.2, link=u)) for t, u in NAV], 600)
    return logo + section(nav, pad=(0, 10, 12, 10))


def also_like():
    tiles = H([(200, _a('<img src="%s%s" width="200" alt="%s" class="vb-img" style="display:block;width:100%%;max-width:200px;height:auto;border:0;outline:none;">' % (BEE_IMG, f, t), u))
               for t, u, f in ALSO_LIKE], 600)
    rule = '<table role="presentation" width="75%" align="center" cellpadding="0" cellspacing="0" border="0"><tr><td style="font-size:1px;line-height:1px;border-top:2px solid #e5e1da;">&nbsp;</td></tr></table>'
    return section(V([rule, T('You may also like', 'CG', 38, '#212121', lh=1.5, link=SITE + '/best-sellers/')], 10), pad=(20, 30, 5, 30)) + section(tiles)


def zac_footer():
    zac = open(os.path.join(SHELL, 'zac-footer.html')).read().strip()
    return ('<table class="row vb" align="center" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation"><tbody><tr><td align="center">'
            '<table class="vb-wrap" align="center" width="600" border="0" cellpadding="0" cellspacing="0" role="presentation" style="width:600px;max-width:600px;background-color:#f1ece4;">'
            + zac + '</table></td></tr></tbody></table>')


def wrap(body, preheader, n):
    pre = ('<div style="display:none;font-size:1px;color:#ffffff;line-height:1px;max-height:0px;max-width:0px;opacity:0;overflow:hidden;mso-hide:all;">%s'
           "{%% for i in range(40) %%}&#847;&zwnj;&nbsp;{%% endfor %%}</div>" % _html.escape(preheader, quote=False))
    h = (HEAD + pre + '<table width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="background-color:#f7f7f7;"><tbody><tr><td>'
         + header() + body + also_like() + zac_footer() + '</td></tr></tbody></table></body></html>')
    h = h.replace(CG, "Cormorant Garamond,Georgia,Times New Roman,serif")
    # single-quote attributes and drop newlines so the blob needs almost no JSON escaping in the node payload
    h = re.sub(r'(\s[\w:-]+)="([^"\']*)"', lambda m: "%s='%s'" % (m.group(1), m.group(2)), h)
    return h.replace('\n', ' ').strip()
