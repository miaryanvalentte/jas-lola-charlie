"""Email 15-28 Variant B, transcribed section by section from Figma page 'Mia - Automations'."""
import lib
from lib import T, V, H, Cell, box, hosted, img, icon, cta, num, section, hero, gap, refer, SITE

U = {
    'best': SITE + '/best-sellers/', 'bundle': SITE + '/bundle-save/', 'gifts': SITE + '/all-gifts/',
    'free': SITE + '/free-gifts/', 'diff': SITE + '/home-fragrance/reed-diffusers/', 'cand': SITE + '/home-fragrance/candles/',
    'mist': SITE + '/home-fragrance/room-mist/', 'wax': SITE + '/home-fragrance/wax-melts/', 'wash': SITE + '/all-skincare/hand-wash/',
    'refill': SITE + '/home-fragrance/100ml-refill/', 'refill1l': SITE + '/home-fragrance/1l-reed-refill/',
    'reviews': SITE + '/about-us/customer-reviews/', 'giftbox': SITE + '/gift-boxes/', 'm12': SITE + '/organic/12-months-of-fragrance-offer/',
    'lr': SITE + '/shop-by-scent/lemongrass-and-rosemary/', 'wnl': SITE + '/shop-by-scent/white-neroli-and-lemon/',
    'lav': SITE + '/shop-by-scent/pure-lavender/', 'jr': SITE + '/shop-by-scent/jasmine-and-rosewood/',
    'vs': SITE + '/shop-by-scent/vanilla-sandalwood/', 'svl': SITE + '/shop-by-scent/spiced-vanilla-leather/',
    'pe': SITE + '/shop-by-scent/patchouli-and-eucalyptus/',
}

INK, BODY, TAUPE = '#212121', '#3a3633', '#8a7560'


def para(text, link, color=BODY, size=15.5):
    return T(text, 'MU', size, color, lh=1.65, link=link)


def eyebrow(text, color=TAUPE, link=None, align='center', size=11, lh=1.3, ls=0.22):
    return T(text, 'MU', size, color, 700, lh, align, ls=ls, upper=True, link=link)


def quote_block(q, who, link, qsize=21):
    return V([T(q, 'CG', qsize, INK, lh=1.32, italic=True, link=link), T(who, 'MU', 11.5, TAUPE, 700, 1.6, link=link)], 8)


def notes_row(label, value, w, link, vsize=17):
    return H([(w, T(label, 'MU', 10.5, TAUPE, 700, 1.6, 'left', ls=0.12, upper=True, link=link)),
              (w, T(value, 'CG', vsize, INK, 600, 1.12, 'right', link=link))], w * 2 + 6, 6, valign='middle')


def review_card(stars_size, q, qsize, who, bg, pad, link):
    return box(V([T('★★★★★', 'MU', stars_size, '#ffa222', lh=1.6, align='left', ls=0.1, link=link),
                  T(q, 'CG', qsize, INK, lh=1.3, align='left', italic=True, link=link),
                  T(who, 'MU', 11.5, TAUPE, 700, 1.6, 'left', link=link)], 6), bg, pad, 6)


EMAILS = {}


def email(n, subject, preheader):
    def deco(fn):
        EMAILS[n] = dict(subject=subject, preheader=preheader, build=fn)
        return fn
    return deco


@email(15, 'Team Lemongrass or Team Neroli? 🍋🍊', 'Our two longest-running best sellers, side by side.')
def e15():
    def card(bg, key, x, name, notes, quote, label, link):
        inner = V([eyebrow('Citrus family', size=10, lh=1.6, ls=0.18, link=link),
                   T(name, 'CG', 24, INK, 600, 1.05, link=link),
                   notes_row('Top', notes[0], 114, link), notes_row('Heart', notes[1], 114, link), notes_row('Base', notes[2], 114, link),
                   T(quote, 'MU', 11.5, '#6b625b', lh=1.4, link=link),
                   cta(label, link, 13, 12, 16)], 10)
        return Cell(V([img(key, x, 542, 270, 180, name + ' reed diffuser', link), box(inner, pad=(6, 18, 0, 18))], 10), bg, (0, 0, 22, 0), 6)
    return ''.join([
        hero(106, 400, 'Our two longest-running best sellers: Team Lemongrass or Team Neroli?', U['best']),
        section(H([(270, card('#eef1e2', 'sc_lr', 24, 'Lemongrass & Rosemary', ('Lemongrass', 'Rosemary', 'Garden Mint'),
                              '“Lots of lovely comments from visitors to the house & the scent is noticeable as soon as you open the front door.”  Lesley, verified buyer',
                              'I’m Team Lemongrass', U['lr'])),
                   (270, card('#fbf0e2', 'sc_wnl', 306, 'White Neroli & Lemon', ('Lemon', 'White Neroli', 'Bay'),
                              '“White Neroli and Lemon is one of my favourite fragrances in a reed diffuser. Everyone comments on how nice the house smells.”  Elaine, verified buyer',
                              'I’m Team Neroli', U['wnl']))], 552, 12, stack=True), pad=(36, 24, 40, 24)),
        section(V([T('Can’t pick a side? Have both.', 'CG', 28, INK, lh=1.12, italic=True, link=U['bundle']),
                   T('Mix Lemongrass & Rosemary and White Neroli & Lemon in one Bundle & Save. It starts at three diffusers:', 'MU', 15, BODY, lh=1.65, link=U['bundle']),
                   H([(140, V([T(n, 'CG', 46, '#b8892b', lh=1.21, link=U['bundle']),
                               T('DIFFUSERS', 'MU', 9.5, TAUPE, 700, 1.26, ls=0.14, link=U['bundle']),
                               T(s, 'CG', 18, INK, lh=1.21, italic=True, link=U['bundle'])], 2)) if n else ('rule', ('#d6c4a5', 64))
                      for n, s in (('3', 'Save'), (None, None), ('6', 'Save more'), (None, None), ('10', 'Best value'))], 422, 0, valign='middle', fixed=True),
                   T('Mix and match any scents. The more you add, the more you save.', 'MU', 13.5, '#4e4842', lh=1.26, link=U['bundle']),
                   gap(8) + cta('Bundle Both & Save', U['bundle'])], 18),
                bg='#faf7f3', pad=(34, 48, 40, 48), border_top='1px solid #e2d6c4'),
    ])


@email(16, 'Autumn favourites: 4 scents for shorter days 🍂', 'Woods, vanilla and florals. Find your autumn favourite.')
def e16():
    def card(key, x, y, eb, name, notes, formats, link, pic=None):
        inner = V([T(eb, 'MU', 10, '#a0623a', 700, 1.6, 'left', ls=0.18, upper=True, link=link),
                   T(name, 'CG', 21, INK, 600, 1.08, 'left', link=link),
                   T(notes, 'MU', 12.5, BODY, lh=1.45, align='left', link=link),
                   T(formats, 'MU', 11.5, TAUPE, 600, 1.45, 'left', link=link)], 4)
        return Cell((pic or img(key, x, y, 263, 170, name, link)) + box(inner, pad=(14, 16, 18, 16)), '#f7f1ea', r=6)

    def fmt(key, x, label, link, pic=None):
        return V([pic or img(key, x, 1423, 128, 120, label, link),
                  T(label, 'MU', 10.5, '#e7c89a', 700, 1.6, ls=0.14, upper=True, link=link)], 6)
    return ''.join([
        hero(106, 420, 'Autumn favourites: four scents for shorter days', U['best']),
        section(para('As the evenings draw in, these are the scents we’re reaching for. Each one comes in more than one format, so you can scent the whole house for the season.', U['best']), pad=(40, 60, 28, 60)),
        # Patchouli & Eucalyptus replaces Spiced Vanilla & Leather (requested after the Figma build); notes/formats from product knowledge + live scent page
        section(V([H([(263, card('sc_pe', 0, 0, 'Woody · Fresh', 'Patchouli & Eucalyptus', 'Eucalyptus · Patchouli · Cedarwood', 'Diffuser · Candle · Room Mist · Fragrance Oil', U['pe'],
                                 pic=hosted('sc_pe', 263, 'Patchouli & Eucalyptus', U['pe']))),
                      (263, card('sc_vs', 307, 672, 'Woody', 'Vanilla & Sandalwood', 'Vanilla · Tonka · Sandalwood', 'Diffuser · Candle · Fragrance Oil', U['vs']))], 540, 14, stack=True),
                   H([(263, card('sc_lav', 30, 997, 'Floral', 'Pure Lavender', 'Lavender · Herbal · Powdery', 'Diffuser · Candle · Room Mist · Wax Melts', U['lav'])),
                      (263, card('sc_jr', 307, 997, 'Floral · Woody', 'Jasmine & Rosewood', 'Rosewood · Jasmine · Cedarwood', 'Diffuser · Fragrance Oil', U['jr']))], 540, 14, stack=True)], 14),
                pad=(0, 30, 36, 30)),
        section(V([T('Start with a favourite', 'CG', 26, '#f4ede3', lh=1.12, italic=True, link=U['best']),
                   H([(128, fmt('dif_pe', 30, 'Diffuser', U['diff'], pic=hosted('dif_pe', 128, 'Diffuser', U['diff']))), (127, fmt('can_vs', 168, 'Candle', U['cand'])),
                      (128, fmt('e16_mist', 305, 'Room Mist', U['mist'])), (127, fmt('e16_wash', 443, 'Hand Wash', U['wash']))], 540, 10),
                   gap(8) + cta('Shop Best Sellers', U['best'])], 16), bg='#6e4e3a', pad=(34, 30, 40, 30)),
    ])


@email(17, 'A new scent for every month 🌿', '12 mini room mists, curated by us, for a year of new favourites.')
def e17():
    L = U['m12']

    def bullet(y, text):
        return H([(18, icon('spark%d' % y, 310, y, 18)), (226, T(text, 'MU', 14.5, INK, lh=1.4, align='left', link=L))], 254, 10, valign='middle')

    def step(d, title, body):
        return V([num(d, '#b8892b'), T(title, 'CG', 20, INK, 600, 1.12, link=L), T(body, 'MU', 13, BODY, lh=1.5, link=L)], 8)
    return ''.join([
        hero(106, 400, 'A new scent for every month: 12 Months of Fragrance', L),
        section(para('Hi [First name], can’t decide on your next scent? Our 12 Months of Fragrance set brings you 12 mini room mists: a curated mix of bestsellers and seasonal favourites, one for every month of the year. Find the one you love, then bring it home in your favourite format.', L), pad=(40, 60, 30, 60)),
        section(H([(250, img('e15_life', 36, 706, 250, 250, '12 Months of Fragrance mini room mists', L)),
                   (254, V([bullet(736, '12 mini room mists, one for every month'),
                            bullet(788, 'A curated mix of bestsellers and seasonal favourites'),
                            bullet(840, 'The easiest way to find your next favourite'),
                            gap(8) + cta('Shop Mini Mists', L, align='left')], 12))], 528, 24, valign='middle', stack=True), pad=(0, 36, 36, 36)),
        section(quote_block('“Love these mini sprays. Handy for the bathroom, car, bedroom - or anywhere! Great way to trial a new scent.”', 'Lisa D. · Verified buyer · ★★★★★', L),
                bg='#f4ede3', pad=(30, 56, 30, 56)),
        section(V([T('How it works', 'CG', 34, INK, lh=1.08, link=L),
                   H([(172, step('1', 'Unbox 12 scents', 'Twelve mini room mists, curated by us.')),
                      (172, step('2', 'One a month', 'Spritz a new scent onto fabrics and around your home.')),
                      (172, step('3', 'Fall for one', 'Bring your favourite home as a diffuser, candle or wax melt.'))], 540, 12),
                   H([(173, img('dif_cc', 30, 1383, 173, 150, 'Reed diffuser', U['diff'])), (173, img('can_wnl', 213, 1383, 173, 150, 'Candle', U['cand'])),
                      (174, img('wax_lr', 397, 1383, 173, 150, 'Wax melts', U['wax']))], 540, 10),
                   gap(4) + cta('Shop 12 Months of Fragrance', L)], 20), pad=(40, 30, 44, 30)),
    ])


@email(18, 'A gift for them, a gift for you 🎁', 'Spend over £60 and get a free candle or diffuser.')
def e18():
    def prod(key, x, y, name, alt, link):
        return V([img(key, x, y, 263, 220, alt, link), T(name, 'CG', 19, INK, 600, 1.1, link=link),
                  T('Shop  ›', 'MU', 11, INK, 700, 1.6, ls=0.1, upper=True, link=link)], 7)

    def perk(key, x, label):
        return V([lib.center(icon(key, x, 1477, 24)), T(label, 'MU', 12.5, INK, 600, 1.6, link=U['gifts'])], 6)
    return ''.join([
        hero(106, 400, 'For them, and for you: a gift for them, a gift for you', U['gifts']),
        section(V([eyebrow('Spend over £60', '#c9a46a', U['best']), T('Get a free candle or diffuser', 'CG', 40, '#f4ede3', lh=1.05, link=U['best']),
                   T('See website for full terms.', 'MU', 11.5, '#bdb3a8', lh=1.6, link=U['best'])], 6), bg='#212121', pad=(30, 40, 32, 40)),
        section(para('Hi [First name], with the gifting season coming up, it’s a lovely time to tick a few names off your list, and treat yourself while you’re at it.', U['gifts']), pad=(36, 60, 24, 60)),
        section(V([T('Gifts our customers love', 'CG', 34, INK, lh=1.08, link=U['gifts']),
                   H([(263, prod('e17_bsgb', 30, 855, 'Best Selling Gift Box', 'Best Selling Gift Box', SITE + '/gift-boxes/best-selling-gift-box/')),
                      (263, prod('e17_bath', 307, 855, 'The Bathroom Best Sellers', 'The Bathroom Best Sellers', SITE + '/organic/the-bathroom-best-sellers/'))], 540, 14),
                   H([(263, prod('e17_melted', 30, 1146, 'The Melted Moments Collection', 'The Melted Moments Collection', SITE + '/organic/the-melted-moments-collection/')),
                      (263, prod('e17_perf', 307, 1146, 'The Perfume Duo', 'The Perfume Duo', SITE + '/organic/the-perfume-duo/'))], 540, 14)], 18),
                pad=(8, 30, 36, 30)),
        section(H([(177, perk('gift', 101, 'Arrives gift-ready')), (177, perk('truck', 288, 'Fast delivery')), (178, perk('spark', 475, 'Made in Cheshire'))], 552, 10),
                bg='#f4ede3', pad=(22, 24, 22, 24)),
        section(quote_block('“Great gift box for presents my friends love theirs and tell me their homes smell beautiful all the time. Would highly recommend.”',
                            'Helen · Best Selling Gift Box · ★★★★★', SITE + '/gift-boxes/best-selling-gift-box/'), pad=(34, 60, 10, 60)),
        section(gap(4) + cta('Shop Gifts', U['gifts']), pad=(22, 40, 44, 40)),
    ])


@email(19, 'We wrote the message for you 💌', 'Share Valentte with a friend, and you both get 15% off.')
def e19():
    R = refer(19)

    def msg(label, text):
        return box(V([T(label, 'MU', 11, TAUPE, 700, 1.6, 'left', ls=0.16, upper=True, link=R),
                       T(text, 'CG', 23, INK, lh=1.3, align='left', italic=True, link=R)], 8), '#fbf8f3', (22, 26, 20, 26), 6, '1px dashed #c9b49e')
    return ''.join([
        hero(106, 400, 'Refer a friend', R),
        section(V([eyebrow('Refer a friend', link=R), T('We wrote the message for you', 'CG', 40, INK, lh=1.08, link=R),
                   para('Hi [First name], recommending something you love shouldn’t feel awkward. Pick a message, share it with a friend, and you’ll both get 15% off.', R)], 12),
                pad=(40, 56, 28, 56)),
        section(V([msg('For the friend who’s just moved', '“New home? This is the diffuser everyone asks me about. Here’s 15% off your first order.”'),
                   msg('For your mum', '“I think you’d love this. It’s all made in Cheshire. Here’s 15% off your first order.”'),
                   msg('For the friend who’s always gifting', '“You always find the perfect present. Valentte arrives gift-ready, beautifully wrapped. Here’s 15% off your first order.”')], 14),
                pad=(8, 36, 36, 36)),
        section(V([T('They get 15% off their first order.\nYou get 15% off too.', 'CG', 26, INK, 600, 1.2, link=R),
                   gap(8) + cta('Share Valentte', R),
                   T('*See website for full terms.', 'MU', 11.5, '#4e5b45', lh=1.6, link=R)], 10), bg='#c9d3bc', pad=(30, 48, 34, 48)),
    ])


@email(20, 'Your words could help someone find their scent 💛', 'Share a quick review of your latest order.')
def e20():
    L = U['reviews']

    def prompt(t):
        return Cell(T(t, 'CG', 18, INK, 600, 1.15, link=L), '#f4ede3', (18, 12, 18, 12), 6, valign='middle')
    return ''.join([
        hero(106, 400, 'Your words matter: help someone find their scent', L),
        section(para('Hi [First name], so many of our customers find their next favourite by reading what people like you have to say. If you have a moment, we’d love you to share yours.', L), pad=(40, 60, 28, 60)),
        section(V([eyebrow('Reviews like these help people choose', link=L),
                   review_card(14, '“Really nice fresh smell, and lasts a lot longer than other diffusers.”', 20, 'Dawn · White Neroli & Lemon Reed Diffuser', '#ffffff', (20, 24, 20, 24), L),
                   review_card(14, '“Beautiful scent, long lasting & packaged with care & attention.”', 20, 'Koré · Vanilla & Sandalwood Reed Diffuser', '#ffffff', (20, 24, 20, 24), L),
                   review_card(14, '“These are honestly the best diffusers EVER! The whole house smells wonderful, thank you x”', 20, 'Jo · Ready, Set, Scent Pack', '#ffffff', (20, 24, 20, 24), L)], 14),
                bg='#f7f5f2', pad=(36, 36, 36, 36)),
        section(V([T('Not sure what to write?', 'CG', 32, INK, lh=1.08, link=L),
                   H([(161, prompt('Which room is it in?')), (161, prompt('How would you describe the scent?')), (162, prompt('Would you buy it again?'))], 504, 10),
                   gap(10) + cta('Write My Review', L)], 14), pad=(36, 48, 44, 48)),
    ])


@email(21, 'Fancy a refill? 🍋', 'Keep your silver cap, swap the oil, add new reeds.')
def e21():
    L = U['refill']

    def step(d, title, body):
        return Cell(V([num(d, '#4e5b45'), T(title, 'CG', 19, INK, 600, 1.12, link=L), T(body, 'MU', 13, BODY, lh=1.5, link=L)], 8), '#f7f5f2', (20, 12, 20, 12), 6)

    def prod(key, x, y, name, link):
        return V([img(key, x, y, 264, 200, name + ' 100ml Diffuser Refill', link), T(name, 'CG', 19, INK, 600, 1.1, link=link),
                  T('100ml Diffuser Refill', 'MU', 12.5, '#6b625b', lh=1.45, link=link)], 7)
    o = SITE + '/organic/'
    return ''.join([
        hero(106, 400, 'Running low... Fancy a refill?', L),
        section(para('Hi [First name], when your diffuser starts to run low, there’s no need to start from scratch. Our 100ml refills come in the same stylish bottle, ready for the silver cap you already have.', L), pad=(40, 60, 30, 60)),
        section(V([T('Three steps. That’s it.', 'CG', 32, INK, lh=1.08, link=L),
                   H([(172, step('1', 'Remove the lid', 'Take the lid off your new refill.')),
                      (172, step('2', 'Reuse your silver cap', 'Pop on the silver cap from your old diffuser.')),
                      (172, step('3', 'Add new reeds', 'Insert your new reeds, and voilà.'))], 540, 12),
                   gap(8) + cta('Shop Refills', L)], 18), pad=(0, 30, 36, 30)),
        section(H([(179, T(t, 'CG', 24, '#f4ede3', lh=1.12, italic=True, link=L)) for t in ('No spills', 'Less waste', 'More savings')], 553, 8, valign='middle'),
                bg='#4e5b45', pad=(22, 24, 22, 24)),
        section(V([eyebrow('Top up your favourites', link=L),
                   H([(264, prod('e21_lr', 30, 1132, 'Lemongrass & Rosemary', o + 'lemongrass-and-rosemary-100ml-diffuser-refill/')),
                      (264, prod('e21_wnl', 306, 1132, 'White Neroli & Lemon', o + 'white-neroli-and-lemon-100ml-diffuser-refill/'))], 540, 12),
                   H([(264, prod('e21_jr', 30, 1403, 'Jasmine & Rosewood', o + 'jasmine-and-rosewood-100ml-diffuser-refill/')),
                      (264, prod('e21_lav', 306, 1403, 'Pure Lavender', o + 'lavender-refill-100ml-diffuser-refill/'))], 540, 12)], 18),
                pad=(40, 30, 24, 30)),
        section(quote_block('“Amazing fragrance have them all around the house so I needed the refill bottle. Love these products good value and amazing smell”',
                            'Annabelle · 1L Diffuser Refill · ★★★★★', U['refill1l'], 19), bg='#f4ede3', pad=(28, 56, 28, 56)),
        section(V([T('Diffusers in every room? Our 1L refills are here too.', 'CG', 19, INK, lh=1.12, italic=True, link=U['refill1l']),
                   gap(4) + cta('Shop Refills', U['refill1l'])], 8), pad=(30, 40, 44, 40)),
    ])


@email(22, '3 perks you can use on your next order ✨', 'Bundle & Save, a free gift over £60, and 15% for you and a friend.')
def e22():
    R = refer(22)

    def perk(bg, key, y, n, ncol, title, tcol, body, label, link):
        col = V([T(n, 'CG', 24, ncol, lh=1.12, align='left', italic=True, link=link),
                 T(title, 'CG', 27, tcol, 600, 1.05, 'left', link=link),
                 T(body, 'MU', 13.5, tcol, lh=1.5, align='left', link=link),
                 cta(label, link, 13, 11, 18, align='left')], 8)
        return H([(190, img(key, 30, y, 190, 230, title, link)), (350, box(col, pad=(22, 24, 22, 24)))], 540, 0, valign='middle', bg=bg, r=6, stack=True)
    return ''.join([
        hero(106, 400, 'Your perks: three ways to get more from your next order', U['bundle']),
        section(para('As one of our regulars, here’s everything you can use on your next order, all in one place.', U['bundle']), pad=(36, 60, 24, 60)),
        section(V([perk('#c9d3bc', 'dif_bundle', 622, '01', TAUPE, 'Bundle & Save', INK, 'Choose 3, 6 or 10 diffusers, mix your favourite scents, and the savings take care of themselves.', 'Start Building', U['bundle']),
                   perk('#212121', 'can_wnl', 866, '02', '#c9a46a', 'A free gift over £60', '#f4ede3', 'Spend over £60 and get a free candle or diffuser.', 'Shop Now', U['best']),
                   perk('#eadfd1', 'gift_bsgb_lr', 1110, '03', TAUPE, 'Refer a friend', INK, 'They get 15% off their first order, and you get 15% off too.', 'Refer A Friend', R),
                   T('See website for full terms on each offer.', 'MU', 11.5, '#8a817a', lh=1.6)], 14), pad=(4, 30, 36, 30)),
    ])


@email(23, 'Over 7 million diffusers, and counting 🏆', 'The UK’s most-rated diffuser, and what makes it work.')
def e23():
    L = U['diff']

    def stat(big, small):
        return V([T(big, 'CG', 30, '#f4ede3', 600, 1.1, link=L, nowrap=True), T(small, 'MU', 12, '#c9bbaa', lh=1.4, link=L)], 4)

    def feat(key, x, y, title, body):
        return Cell(V([lib.center(icon(key, x, y, 26)), T(title, 'CG', 21, INK, 600, 1.12, link=L), T(body, 'MU', 13, BODY, lh=1.5, link=L)], 8),
                   '#f7f5f2', (22, 18, 22, 18), 6)
    side = V([T('Ready to scent another room?', 'CG', 30, INK, lh=1.08, align='left', link=U['bundle']),
              T('Choose 3, 6 or 10 diffusers with Bundle & Save, and mix your favourite scents.', 'MU', 14, BODY, lh=1.65, align='left', link=U['bundle']),
              cta('Shop The Diffuser Bundle', U['bundle'], 13, 12, 18, align='left')], 10)
    return ''.join([
        hero(106, 420, 'Everyone who visits asks what it is. Over 7 million diffusers, and counting', L),
        section(H([(181, stat('350,000+', 'five-star reviews')), (181, stat('7 million', 'diffusers sold')),
                   (182, stat('18 seconds', 'that’s how often someone chooses Valentte'))], 560, 8, stack=True), bg='#212121', pad=(30, 20, 30, 20)),
        section(V([eyebrow('The UK’s most-rated diffuser', link=L), T('What makes it work', 'CG', 36, INK, lh=1.08, link=L),
                   H([(258, feat('spark', 152, 813, 'Fibre reeds', 'They absorb oil more efficiently than traditional rattan reeds, so you need fewer of them.')),
                      (258, feat('heart', 422, 813, 'Works 24/7', 'No plug, no batteries, no effort.'))], 528, 12),
                   H([(258, feat('star', 152, 1001, 'Up to 12 weeks', 'One diffuser, up to 12 weeks of scent.')),
                      (258, feat('gift', 422, 1001, 'Made with natural oils', 'Strong enough to fill the room, never strong enough to overwhelm.'))], 528, 12)], 18),
                pad=(44, 36, 36, 36)),
        section(quote_block('“The smell is absolutely amazing\nAll my friends comment how lovely my home smells”', 'Sandra · Verified buyer · ★★★★★', L),
                bg='#f4ede3', pad=(30, 56, 30, 56)),
        section(H([(280, img('e23_three', 0, 1327, 280, 280, 'Valentte reed diffusers', U['bundle'])), (320, box(side, pad=(24, 30, 24, 30)))], 600, 0, valign='middle', stack=True)),
    ])


@email(24, '“Fills the whole house” and other things you told us 💬', 'Real reviews, sorted by what matters most.')
def e24():
    def theme(bg, cardbg, n, title, linktext, key, y, link, reviews):
        head = H([(402, V([T(n, 'CG', 22, '#b8892b', lh=1.12, align='left', italic=True, link=link),
                           T(title, 'CG', 30, INK, 600, 1.12, 'left', link=link),
                           T(linktext, 'MU', 11, INK, 700, 1.6, 'left', ls=0.1, upper=True, link=link)], 2)),
                  (110, img(key, 454, y, 110, 110, title, link))], 528, 16, valign='middle')
        return section(V([head] + [review_card(13, q, 19, who, cardbg, (18, 22, 18, 22), link) for q, who in reviews], 14), bg=bg, pad=(34, 36, 34, 36))
    return ''.join([
        hero(106, 420, 'In your words: strong enough to reach the top of the stairs', U['best']),
        section(para('Hi [First name], we read every review. Here’s what our customers tell us, sorted by what matters most.', U['best']), pad=(40, 60, 24, 60)),
        theme('#f7f5f2', '#ffffff', '01', 'Fills every room', 'Shop Reed Diffusers  ›', 'dif_lr', 676, U['diff'],
              [('“I love these reed diffusers. I have a different one in every room of the house”', 'Lisa · Ready, Set, Scent Pack'),
               ('“Absolutely lovely gift set, the diffusers are long lasting and make the whole house smell wonderful.”', 'Marilyn · Ready, Set, Scent Pack')]),
        theme('#ffffff', '#f7f5f2', '02', 'Guests always ask', 'Shop Best sellers  ›', 'dif_wnl', 1156, U['best'],
              [('“Absolutely love valentte products everyone comments how lovely they smell when they come in my home”', 'C. · The Ultimate Scent Ritual Offer'),
               ('“Bergamot and lemon diffuser purchased many times, lovely long lasting smell, lots of comments from visitors”', 'Heather · Ready, Set, Scent Pack')]),
        theme('#f7f5f2', '#ffffff', '03', 'Lasts and lasts', 'Shop Vanilla & Sandalwood  ›', 'dif_vs', 1636, U['vs'],
              [('“Vanilla and Sandalwood is one of my favourite diffuser scents so far!\nLong lasting and a beautiful smell anywhere around the home.”', 'Lisa · Vanilla & Sandalwood Reed Diffuser')]),
        theme('#ffffff', '#f7f5f2', '04', 'Beautifully packaged', 'Shop Gift Boxes  ›', 'gift_bsgb_wnl', 1965, U['giftbox'],
              [('“Beautiful scent, long lasting & packaged with care & attention.”', 'Koré · Vanilla & Sandalwood Reed Diffuser')]),
        section(V([T('350,000+', 'CG', 50, INK, 600, 1.0, link=U['best']), T('five-star reviews', 'MU', 12, '#c9a46a', 700, 1.6, ls=0.22, upper=True, link=U['best']),
                   gap(14) + cta('Shop Customer Favourites', U['best'])], 6), bg='#f4ede3', pad=(30, 48, 36, 48)),
    ])


@email(25, 'Three scents, three rooms 🍋', 'Our favourite trio, and the easiest way to start Bundle & Save.')
def e25():
    def card(key, img_x, y, name, quote, notes, also, link, img_left=True):
        col = V([T(name, 'MU', 10.5, '#a0623a', 700, 1.6, 'left', ls=0.14, upper=True, link=link),
                 T(quote, 'CG', 20, INK, lh=1.28, align='left', italic=True, link=link),
                 notes_row('Top', notes[0], 139, link, 18), notes_row('Heart', notes[1], 139, link, 18), notes_row('Base', notes[2], 139, link, 18),
                 T(also, 'MU', 13, BODY, lh=1.45, align='left', link=link)], 12)
        pic = (260, img(key, img_x, y, 260, 330, name.title(), link))
        txt = (340, box(col, pad=(26, 28, 26, 28)))
        return section(H([pic, txt], 600, 0, valign='middle', bg='#fbf3e6', stack=True, rtl=not img_left), pad=(0, 0, 16, 0))
    return ''.join([
        hero(106, 420, 'Bundle & Save: three scents, three rooms', U['bundle']),
        section(gap(32)),
        card('e25_wnl', 0, 558, 'WHITE NEROLI & LEMON', '“A radiant blend that evokes the effortless elegance and vitality of sunlit summer days.”',
             ('Lemon', 'White Neroli', 'Bay'), 'Also as a candle, room mist and wax melts.', U['wnl']),
        card('e25_lr', 340, 904, 'LEMONGRASS & ROSEMARY', '“Zesty lemongrass and fragrant rosemary swirl through golden sunlight, stirring memories of endless summer afternoons.”',
             ('Lemongrass', 'Rosemary', 'Garden Mint'), 'Also as a candle, room mist and wax melts.', U['lr'], img_left=False),
        card('e25_lav', 0, 1250, 'pure lavender', '“In the sun-drenched fields of Provence, endless lavender blooms fill the summer air with a sweet, floral scent.”',
             ('Lavender', 'Sweet floral', 'Soft herbal'), 'Also as a candle, room mist and refill.', U['lav']),
        section(V([T('Bring all three home', 'CG', 34, INK, lh=1.08, link=U['bundle']),
                   T('Three diffusers is where Bundle & Save begins. Pick these three, or swap in any scent you love: the savings take care of themselves.', 'MU', 15, BODY, lh=1.6, link=U['bundle'])], 12),
                pad=(40, 24, 8, 24)),
        section(gap(4) + cta('Bundle These Three & Save', U['bundle']), pad=(10, 40, 44, 40)),
    ])


@email(26, 'Three scents, one beautiful home 💛', 'Ready-made trios that start your Bundle & Save.')
def e26():
    L = U['bundle']

    def trio(bg, key, y, title, scents, desc):
        return box(V([img(key, 52, y, 496, 250, title, L), T(title, 'CG', 28, INK, 600, 1.12, link=L),
                      T(scents, 'MU', 11, TAUPE, 700, 1.5, ls=0.04, upper=True, link=L), T(desc, 'MU', 14, BODY, lh=1.5, link=L),
                      cta('Bundle This Trio', L, 13, 12, 22)], 12), bg, (22, 22, 24, 22), 6)

    def how(d, t):
        return V([num(d, '#ffa220', INK, 30, 16), T(t, 'MU', 13, INK, lh=1.4, link=L)], 6)
    return ''.join([
        hero(106, 400, 'Perfect trios: three scents, one beautiful home', L),
        section(para('Bundle & Save starts at three, so we’ve paired three scents that work beautifully together. Choose a trio, and the savings take care of themselves.', L), pad=(40, 60, 24, 60)),
        section(V([trio('#fbf0e2', 'e26_t1b', 674, 'Energising mornings', 'Lemongrass & Rosemary · Wild Mint & Sicilian Lemon · White Neroli & Lemon', 'Sparkling citrus for kitchens, hallways and bathrooms.'),
                   trio('#efedf4', 'e26_t2', 1162, 'Bright days, calm evenings', 'White Neroli & Lemon · Pure Lavender · Lemongrass & Rosemary', 'Radiant citrus by day, soft lavender for winding down.'),
                   trio('#f3e9e0', 'e26_t3b', 1633, 'Cosy nights in', 'Patchouli & Eucalyptus · Vanilla & Sandalwood · Jasmine & Rosewood', 'Warm woods and soft florals for living rooms and snugs.')], 16),
                pad=(4, 30, 30, 30)),
        section(V([T('How Bundle & Save works', 'CG', 28, INK, lh=1.12, italic=True, link=L),
                   H([(169, how('1', 'Choose 3, 6 or 10\ndiffusers')), (169, how('2', 'Mix your favourite\nscents')), (170, how('3', 'The savings take care\nof themselves'))], 528, 10),
                   gap(8) + cta('Build Your Own Bundle', L)], 16), bg='#f4ede3', pad=(34, 36, 40, 36)),
    ])


@email(27, 'How many diffusers does your home need? 🏡', 'Choose 3, 6 or 10 diffusers, mix your favourite scents and save.')
def e27():
    L = U['bundle']

    def tier(bg, n, title, desc, label, mid_w, cta_w):
        row = H([(56, T(n, 'CG', 60, '#b8892b', 600, 0.9, link=L)),
                 (mid_w, V([T(title, 'CG', 24, INK, 600, 1.12, 'left', link=L, cls='vb-mcenter'),
                            T(desc, 'MU', 13.5, INK if n == '10' else BODY, lh=1.5, align='left', link=L, cls='vb-mcenter')], 3)),
                 (cta_w, cta(label, L, 12.5, 10, 16))], 492, 20, valign='middle', stack=True)
        return box(row, bg, (20, 24, 20, 24), 6)
    return ''.join([
        hero(106, 380, 'How many diffusers does your home need?', L),
        section(V([eyebrow('Bundle & Save', link=L), T('How many diffusers does your home need?', 'CG', 40, INK, lh=1.08, link=L),
                   para('Hi [First name], choose your number, mix your favourite scents, and the savings take care of themselves.', L)], 12), pad=(10, 56, 28, 56)),
        section(V([tier('#eef1e8', '3', 'The everyday trio', 'Hallway, living room and bathroom.', 'Choose 3', 281, 115),
                   tier('#f4ede3', '6', 'Upstairs and down', 'Every main room, with a scent for each.', 'Choose 6', 281, 115),
                   tier('#f6ece6', '10', 'The whole house', 'Every room covered, plus a few to gift.', 'Choose 10', 273, 123)], 12), pad=(4, 30, 36, 30)),
        section(img('e27_six', 0, 1046, 600, 330, 'Six Valentte reed diffusers', L)),
        section(V([T('Mix and match your favourite scents.', 'CG', 20, INK, lh=1.12, italic=True, link=L),
                   gap(4) + cta('Start Building Your Bundle', L)], 8), pad=(30, 40, 44, 40)),
    ])


@email(28, 'A little gift for a friend, from you 🎁', 'Give them 15% off their first order, and get 15% off too.')
def e28():
    R = refer(28)

    def pill(t):
        return Cell(T(t, 'MU', 12.5, INK, 600, 1.6, link=R), '#f4ede3', (12, 6, 12, 6), 20, valign='middle')
    return ''.join([
        hero(106, 400, 'Refer a friend: a little gift, from you', R),
        section(V([H([(392, img('gift_tag', 104, 550, 392, 251, 'To: someone lovely. 15% off their first order. From: you', R))], 392, fixed=True),
                   T('Know someone who’d love Valentte? Send them 15% off their first order, and we’ll say thank you with 15% off for you too.', 'MU', 15.5, '#2a3326', lh=1.65, link=R)], 22),
                bg='#c9d3bc', pad=(44, 40, 48, 40)),
        section(V([T('Who’s it for?', 'CG', 28, INK, lh=1.12, italic=True, link=R),
                   H([(129, pill('Your mum')), (129, pill('Your best friend')), (129, pill('A new neighbour')), (129, pill('Your work friend'))], 540, 8),
                   gap(10) + cta('Send Your Gift', R),
                   T('*See website for full terms.', 'MU', 11.5, '#8a817a', lh=1.6, link=R)], 16), pad=(38, 30, 44, 30)),
    ])


def build_all():
    out = {}
    lib.CROPS.clear()
    for n, e in sorted(EMAILS.items()):
        lib.EMAIL = n
        out[n] = dict(subject=e['subject'], preheader=e['preheader'], html=lib.wrap(e['build'](), e['preheader'], n))
    return out
