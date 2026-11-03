import sys, os, math, random
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
S = sys.argv[1]; OUT = sys.argv[2]; ONLY = sys.argv[3] if len(sys.argv) > 3 else None
W, H = 600, 830
FPS, DUR = 20, 6.9
RED = (128, 24, 34); INK = (33, 33, 33); CREAM = (247, 241, 232)
F = S + '/fonts/'
def inter(sz, w='SemiBold'):
    f = ImageFont.truetype(F + 'Inter.ttf', int(sz)); f.set_variation_by_name(w); return f
cardo = lambda sz: ImageFont.truetype(F + 'Cardo-Regular.ttf', int(sz))
clamp = lambda v: max(0.0, min(1.0, v))
def ease_out_back(t, s=1.4):
    t -= 1; return t * t * ((s + 1) * t + s) + 1
ease_in = lambda t: t ** 2

# ---------------- products: cut from the reference photo -----------------
cut = Image.open(f'{S}/v2/photo_cut.png').convert('RGBA')          # 2x of 1601x515
CS = cut.width / 1601
A = np.array(cut)
al = A[..., 3].astype(np.float32)
al = np.clip((al - 30) * 255 / 190, 0, 255)
# item rects in photo coords: name, x0,y0,x1,y1, z (higher = in front), tier
RECTS = [
 ('giftbox',   112, 18, 592, 352, 1, 'L'), ('handsoapbox', 220, 205, 348, 402, 2, 'L'),
 ('cube1',     398, 262, 572, 422, 2, 'L'), ('candle1',     428,  98, 552, 280, 3, 'L'),
 ('cream',     120, 312, 266, 455, 5, 'L'), ('soap',        294, 314, 468, 445, 5, 'L'),
 ('cube2',     592, 255, 752, 392, 2, 'L'), ('candle2',     604,  98, 724, 270, 3, 'L'),
 ('roommist',  552, 236, 618, 445, 6, 'L'), ('bathbox',     760, 178, 878, 402, 3, 'L'),
 ('wax',       650, 360, 882, 436, 6, 'L'),
 ('lotion',    876, 170, 964, 402, 4, 'R'), ('handwash',    962, 170, 1054, 398, 4, 'R'),
 ('diffbox',  1026,  50, 1140, 390, 2, 'R'), ('cube3',      1188, 272, 1465, 410, 2, 'R'),
 ('diffback', 1210,  22, 1372, 298, 3, 'R'), ('difffront', 1088, 118, 1245, 430, 5, 'R'),
 ('oil',      1050, 330, 1110, 455, 6, 'R'),
]
TIER = {'L': (108, 14, 880, 460), 'R': (879, 14, 1470, 460)}
hh, ww = al.shape
owner = np.full((hh, ww), -1, np.int32); best = np.full((hh, ww), -1e9)
for i, (n, x0, y0, x1, y1, z, t) in enumerate(RECTS):
    X0, Y0, X1, Y1 = [int(v * CS) for v in (x0, y0, x1, y1)]
    score = z * 1e7 - (x1 - x0) * (y1 - y0)
    sl = (slice(Y0, Y1), slice(X0, X1))
    m = best[sl] < score
    best[sl][m] = score; owner[sl][m] = i
# ribbon running behind candle1 belongs to the gift box
lum = A[..., :3].astype(np.float32).mean(2)
ci = [r[0] for r in RECTS].index('candle1')
yy_, xx_ = np.mgrid[0:hh, 0:ww]
rib = (owner == ci) & (lum < 135) & (yy_ < 190 * CS)
owner[rib] = 0
# leftovers inside a tier -> the biggest back item of that tier
for t, fb in (('L', 0), ('R', 14)):
    x0, y0, x1, y1 = [int(v * CS) for v in TIER[t]]
    sub = owner[y0:y1, x0:x1]; sub[sub < 0] = fb
rgb = A[..., :3]
SC = 0.68
def tier_box(t, top):
    x0, y0, x1, y1 = TIER[t]
    w, h = (x1 - x0) * SC, (y1 - y0) * SC
    return (round((W - w) / 2), top, round(w), round(h))
TB = {'R': tier_box('R', 112), 'L': tier_box('L', 404)}
SCALED = {}
for t in ('L', 'R'):
    x0, y0, x1, y1 = [int(v * CS) for v in TIER[t]]
    tim = Image.fromarray(np.dstack([rgb[y0:y1, x0:x1], al[y0:y1, x0:x1].astype(np.uint8)]), 'RGBA')
    bx, by, bw, bh = TB[t]
    tim = tim.resize((bw, bh), Image.LANCZOS)
    own = Image.fromarray(owner[y0:y1, x0:x1].astype(np.int32)).resize((bw, bh), Image.NEAREST)
    own = np.array(own); ta = np.array(tim)
    for i, (n, *_r, z, tt) in enumerate(RECTS):
        if tt != t: continue
        la = ta.copy(); la[..., 3] = np.where(own == i, ta[..., 3], 0)
        SCALED[n] = (Image.fromarray(la, 'RGBA'), t, z)
# per-item visual centre (for the pop anchor)
CENT = {}
for n, x0, y0, x1, y1, z, t in RECTS:
    tx0, ty0 = TIER[t][:2]; bx, by = TB[t][:2]
    CENT[n] = (bx + ((x0 + x1) / 2 - tx0) * SC, by + (y1 - ty0) * SC)
# reveal order: front first, then left to right
ORDER = sorted(RECTS, key=lambda r: (-r[5], r[7] if False else 0, r[1] + (0 if r[6] == 'L' else 2000)))
ORDER = [r[0] for r in ORDER]
DRAW = [r[0] for r in sorted(RECTS, key=lambda r: (0 if r[6] == 'R' else 1, r[5]))]  # back tier first, then z

# ---------------- background: silver, bokeh, ledges ----------------------
random.seed(3)
BT = 716    # banner top
def background():
    g = np.zeros((H, W, 3), np.float32)
    yy = np.linspace(0, 1, H)[:, None]
    xx = np.linspace(-1, 1, W)[None, :]
    base = 188 + 40 * np.exp(-((yy - 0.45) ** 2) / 0.08) - 10 * xx ** 2
    g[..., 0] = base; g[..., 1] = base - 1; g[..., 2] = base + 3
    bg = Image.fromarray(np.clip(g, 0, 255).astype(np.uint8))
    # warm bokeh
    bok = Image.new('RGB', (W, H), 0); d = ImageDraw.Draw(bok)
    for _ in range(70):
        x, y = random.uniform(0, W), random.uniform(0, BT); r = random.uniform(3, 16)
        c = random.choice([(255, 236, 190), (255, 248, 230), (255, 225, 160)])
        k = random.uniform(0.25, 0.8)
        d.ellipse([x - r, y - r, x + r, y + r], fill=tuple(int(v * k) for v in c))
    bok = bok.filter(ImageFilter.GaussianBlur(3))
    bg = Image.fromarray(np.clip(np.array(bg, np.int32) + np.array(bok, np.int32) * 0.55, 0, 255).astype(np.uint8))
    # fine glitter dust
    d = ImageDraw.Draw(bg)
    for _ in range(900):
        x, y = random.uniform(0, W), random.uniform(0, BT)
        v = random.randint(225, 255); d.point((x, y), fill=(v, v, v - 8))
    # snowy ledges under each tier
    for t in ('R', 'L'):
        x, y, w, h = TB[t]
        ly = y + h - 34
        sn = Image.new('L', (W, H), 0); ds = ImageDraw.Draw(sn)
        ds.rounded_rectangle([x - 30, ly, x + w + 30, ly + 46], radius=22, fill=255)
        sn = sn.filter(ImageFilter.GaussianBlur(9))
        bg.paste((246, 246, 250), (0, 0), sn)
        d = ImageDraw.Draw(bg)
        for _ in range(260):
            px, py = random.uniform(x - 10, x + w + 10), random.uniform(ly + 6, ly + 38)
            d.point((px, py), fill=random.choice([(255, 255, 255), (214, 218, 228), (200, 205, 218)]))
    # banner
    d.rectangle([0, BT, W, H], fill=RED)
    d.text((W / 2, BT + 26), 'Find the perfect gift this Christmas', font=cardo(31), fill=CREAM, anchor='ma')
    f = inter(11, 'SemiBold'); s = 'THE CHRISTMAS SHOP IS NOW OPEN'
    ws = [d.textlength(c, font=f) for c in s]; x = W / 2 - (sum(ws) + 3 * (len(s) - 1)) / 2
    for c, w_ in zip(s, ws): d.text((x, BT + 76), c, font=f, fill=(238, 205, 200)); x += w_ + 3
    return bg
BG = background()

# twinkle stars (positions avoid nothing in particular; they sit behind products)
STARS = [(random.uniform(10, W - 10), random.uniform(110, BT - 20), random.uniform(5, 13),
          random.uniform(0, 6.28), random.uniform(1.5, 3.2)) for _ in range(26)]
FLAKES = [(random.uniform(0, W), random.uniform(0, H), random.uniform(0.9, 2.4),
           random.uniform(18, 40), random.uniform(0, 6.28)) for _ in range(110)]

def star(d, x, y, r, k):
    c = (255, 246, 222)
    g = int(255 * k)
    for rr, a in ((r * 0.55, 0.35), (r * 0.3, 0.7)):
        d.ellipse([x - rr, y - rr, x + rr, y + rr], fill=c + (int(g * a),))
    d.line([x - r * 1.6, y, x + r * 1.6, y], fill=c + (g,), width=1)
    d.line([x, y - r * 1.6, x, y + r * 1.6], fill=c + (g,), width=1)
    d.ellipse([x - 1.6, y - 1.6, x + 1.6, y + 1.6], fill=(255, 255, 255, g))

TYPED = 'valentte christmas shop'
def frame(t):
    im = BG.copy().convert('RGBA')
    # twinkles behind products
    ov = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(ov)
    for x, y, r, ph, sp in STARS:
        k = 0.5 + 0.5 * math.sin(t * sp * 2 + ph); k = k ** 2
        star(d, x, y, r * (0.7 + 0.5 * k), k)
    ov = ov.filter(ImageFilter.GaussianBlur(0.6)); im.alpha_composite(ov)
    # products
    for n in DRAW:
        sp, tr, z = SCALED[n]
        i = ORDER.index(n)
        t0 = 0.45 + 0.16 * i
        p = clamp((t - t0) / 0.42)
        q = clamp((t - (5.55 + 0.02 * (len(ORDER) - 1 - i))) / 0.35)
        if p <= 0 or q >= 1: continue
        alpha = clamp(p * 2.2) * (1 - ease_in(q))
        sc = 0.80 + 0.20 * ease_out_back(p)
        x, y, w, h = TB[tr]
        layer = sp
        if alpha < 1:
            layer = sp.copy(); layer.putalpha(sp.split()[3].point(lambda v: int(v * alpha)))
        if abs(sc - 1) > 0.002:
            cx, cy = CENT[n]
            lw, lh = round(w * sc), round(h * sc)
            layer = layer.resize((lw, lh), Image.BILINEAR)
            px = round(cx - (cx - x) * sc); py = round(cy - (cy - y) * sc)
            im.alpha_composite(layer, (px, py)) if px >= 0 and py >= 0 else im.paste(layer, (px, py), layer)
        else:
            im.alpha_composite(layer, (x, y))
    # falling snow in front of everything
    d = ImageDraw.Draw(im)
    for fx, fy, r, sp_, ph in FLAKES:
        yy = (fy + t * sp_) % H; xx = fx + 7 * math.sin(t * 1.2 + ph)
        d.ellipse([xx - r, yy - r, xx + r, yy + r], fill=(255, 255, 255, 230))
    # big search bar on top
    x0, y0, x1, y1 = 30, 26, 570, 96
    shd = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(shd).rounded_rectangle([x0, y0 + 5, x1, y1 + 5], radius=35, fill=(60, 40, 40, 70))
    im.alpha_composite(shd.filter(ImageFilter.GaussianBlur(8)))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([x0, y0, x1, y1], radius=35, fill=(255, 255, 255), outline=(222, 214, 214), width=1)
    cy = (y0 + y1) / 2; mx = x0 + 38
    d.ellipse([mx - 11, cy - 13, mx + 9, cy + 7], outline=RED, width=3)
    d.line([mx + 6, cy + 4, mx + 15, cy + 13], fill=RED, width=4)
    cx_ = x1 - 38
    for s in (1, -1): d.line([cx_ - 9, cy - 9 * s, cx_ + 9, cy + 9 * s], fill=RED, width=3)
    n = int(clamp((t - 0.3) / 2.1) * len(TYPED)); txt = TYPED[:n].upper()
    f = inter(22, 'SemiBold'); x = mx + 32
    for c in txt:
        d.text((x, cy), c, font=f, fill=RED, anchor='lm'); x += d.textlength(c, font=f) + 1.5
    if n < len(TYPED) or int(t * 2.4) % 2 == 0:
        d.line([x + 3, cy - 14, x + 3, cy + 14], fill=RED, width=2)
    return im.convert('RGB')

os.makedirs(OUT, exist_ok=True)
N = int(DUR * FPS)
for k in ([int(ONLY)] if ONLY else range(N)):
    frame(k / FPS).save(f'{OUT}/f{k:04d}.png')
print('frames', N)
