import sys, os, math, random
from PIL import Image, ImageDraw, ImageFont, ImageFilter
S = sys.argv[1]; OUT = sys.argv[2]; ONLY = sys.argv[3] if len(sys.argv) > 3 else None
K = 2                      # supersample
W, H = 600, 750
FPS = 20
DUR = 6.4
CREAM = (247, 241, 232); CREAM2 = (240, 230, 216)
RED = (128, 24, 34); RED_D = (104, 17, 26); INK = (33, 33, 33); GOLD = (196, 150, 40)
F = S + '/fonts/'
def inter(sz, w='SemiBold'):
    f = ImageFont.truetype(F + 'Inter.ttf', sz * K); f.set_variation_by_name(w); return f
cardo = lambda sz: ImageFont.truetype(F + 'Cardo-Regular.ttf', sz * K)
cardo_i = lambda sz: ImageFont.truetype(F + 'Cardo-Italic.ttf', sz * K)

LO, HI = 25, 230
def load(name, h):
    im = Image.open(f'{S}/cut2/{name}.png').convert('RGBA')
    a = im.split()[3].point(lambda v: 0 if v < LO else min(255, int((v - LO) * 255 / (HI - LO))))
    import numpy as np, scipy.ndimage as nd
    arr = np.array(a); lab, n = nd.label(arr > 20)
    if n > 1:
        sizes = nd.sum(np.ones_like(arr), lab, range(1, n + 1))
        keep = np.isin(lab, [i + 1 for i, z in enumerate(sizes) if z > sizes.max() * 0.02])
        arr = np.where(keep, arr, 0).astype('uint8'); a = Image.fromarray(arr)
    im.putalpha(a)
    im = im.crop(a.point(lambda v: 255 if v > 20 else 0).getbbox())
    r = h * K / im.height
    return im.resize((round(im.width * r), round(im.height * r)), Image.LANCZOS)

FLOOR = 592
# (cutout, height, centre-x, bottom-y) in back-to-front draw order == entry order
ITEMS = [
    ('diffuser_ff', 330, 128, FLOOR - 26),
    ('roommist_ff', 290, 478, FLOOR - 26),
    ('candle_ff',   235, 322, FLOOR - 2),
    ('oil_ff',      175, 118, FLOOR + 24),
    ('minimist_ff', 200, 492, FLOOR + 24),
]
sprites = [load(n, h) for n, h, _, _ in ITEMS]

def ease_out_back(t, s=1.5):
    t -= 1; return t * t * ((s + 1) * t + s) + 1
def ease_out(t): return 1 - (1 - t) ** 3
def ease_in(t): return t ** 3
clamp = lambda v: max(0.0, min(1.0, v))

# ---- static background -------------------------------------------------
def background():
    bg = Image.new('RGB', (W * K, H * K), CREAM)
    # soft warm radial glow behind products
    glow = Image.new('L', (W * K, H * K), 0)
    ImageDraw.Draw(glow).ellipse([60 * K, 230 * K, 540 * K, 640 * K], fill=255)
    glow = glow.filter(ImageFilter.GaussianBlur(90 * K))
    bg.paste(Image.new('RGB', bg.size, (252, 248, 242)), (0, 0), glow)
    # floor tint
    fl = Image.new('L', (W * K, H * K), 0)
    ImageDraw.Draw(fl).rectangle([0, (FLOOR - 40) * K, W * K, H * K], fill=110)
    fl = fl.filter(ImageFilter.GaussianBlur(40 * K))
    bg.paste(Image.new('RGB', bg.size, CREAM2), (0, 0), fl)
    d = ImageDraw.Draw(bg)
    cx = W * K // 2
    def ctext(y, s, font, fill, spacing=0):
        if spacing:
            ws = [d.textlength(c, font=font) for c in s]
            tot = sum(ws) + spacing * K * (len(s) - 1); x = cx - tot / 2
            for c, w in zip(s, ws):
                d.text((x, y * K), c, font=font, fill=fill); x += w + spacing * K
        else:
            d.text((cx, y * K), s, font=font, fill=fill, anchor='ma')
    ctext(34, 'NOW OPEN', inter(11, 'SemiBold'), RED, spacing=4)
    # little sprigs either side of NOW OPEN
    for sx in (-1, 1):
        x0 = cx + sx * 70 * K
        d.line([x0, 41 * K, x0 + sx * 40 * K, 41 * K], fill=RED, width=K)
    ctext(56, 'The Christmas Shop', cardo(56), RED)
    ctext(126, 'FROSTED FIR  ·  SNOW & SAGE  ·  CRUSHED CANDY CANE', inter(10, 'Medium'), INK, spacing=1.2)
    # bottom banner
    BT = 628
    d.rectangle([0, BT * K, W * K, H * K], fill=RED)
    return bg, BT

BG, BT = background()
PILL = (70, BT + 26, 530, BT + 72)
random.seed(7)
FLAKES = [(random.uniform(0, W), random.uniform(0, H - BT), random.uniform(0.8, 2.1),
           random.uniform(14, 30), random.uniform(0, 6.28)) for _ in range(46)]
TYPED = 'valentte christmas shop'

_SH = {}
def shadow(w, h):
    if (w, h) not in _SH:
        pad = h * 2
        sh = Image.new('L', (w + 2 * pad, h + 2 * pad), 0)
        ImageDraw.Draw(sh).ellipse([pad, pad, pad + w, pad + h], fill=70)
        _SH[(w, h)] = (sh.filter(ImageFilter.GaussianBlur(h / 2.5)), pad)
    return _SH[(w, h)]

def frame(t):
    im = BG.copy()
    for i, ((n, h, cx, by), sp) in enumerate(zip(ITEMS, sprites)):
        t0 = 0.35 + 0.42 * i
        p = clamp((t - t0) / 0.5)
        q = clamp((t - (4.9 + 0.08 * (len(ITEMS) - 1 - i))) / 0.3)  # exit, front first
        if p <= 0 or q >= 1: continue
        y_off = (1 - ease_out_back(p)) * -150
        alpha = clamp(p * 3) * (1 - ease_in(q))
        y_off -= ease_in(q) * 0  # vanish in place, like the reference
        sc = 0.94 + 0.06 * ease_out(p)
        s2 = sp.resize((max(1, round(sp.width * sc)), max(1, round(sp.height * sc))), Image.BILINEAR) if sc < 0.999 else sp
        x = round(cx * K - s2.width / 2); y = round(by * K - s2.height + y_off * K)
        # contact shadow, grows as item lands
        land = clamp(1 - abs(y_off) / 150)
        if land > 0:
            sw, shh = int(sp.width * 0.55), int(16 * K)
            sh, pad = shadow(sw, shh)
            sh = sh.point(lambda v: int(v * land * alpha))
            im.paste((110, 80, 55), (round(cx * K - sw / 2 - pad), round(by * K - 8 * K - shh / 2 - pad)), sh)
        if alpha < 1:
            a = s2.split()[3].point(lambda v: int(v * alpha)); s2 = s2.copy(); s2.putalpha(a)
        im.paste(s2, (x, y), s2)
    d = ImageDraw.Draw(im)
    # snow in banner
    for fx, fy, r, sp_, ph in FLAKES:
        yy = (fy + t * sp_) % (H - BT); xx = fx + 6 * math.sin(t * 1.3 + ph)
        d.ellipse([(xx - r) * K, (BT + yy - r) * K, (xx + r) * K, (BT + yy + r) * K], fill=(236, 200, 200))
    # search pill
    x0, y0, x1, y1 = PILL
    d.rounded_rectangle([x0 * K, y0 * K, x1 * K, y1 * K], radius=23 * K, fill=CREAM)
    # magnifier
    mx, my = x0 + 26, (y0 + y1) / 2 - 2
    d.ellipse([(mx - 7) * K, (my - 7) * K, (mx + 7) * K, (my + 7) * K], outline=RED, width=2 * K)
    d.line([(mx + 5) * K, (my + 5) * K, (mx + 11) * K, (my + 11) * K], fill=RED, width=3 * K)
    # close x
    cx_ = x1 - 26; cy_ = (y0 + y1) / 2
    for s in (1, -1):
        d.line([(cx_ - 6) * K, (cy_ - 6 * s) * K, (cx_ + 6) * K, (cy_ + 6 * s) * K], fill=RED, width=2 * K)
    # typed text
    n = int(clamp((t - 0.3) / 2.2) * len(TYPED))
    txt = TYPED[:n].upper()
    f = inter(15, 'SemiBold')
    tx = (mx + 22) * K; ty = cy_ * K
    # letter-spaced draw
    x = tx
    for c in txt:
        d.text((x, ty), c, font=f, fill=RED, anchor='lm'); x += d.textlength(c, font=f) + 1.5 * K
    if (n < len(TYPED)) or (int(t * 2.4) % 2 == 0):
        d.line([x + 2 * K, ty - 10 * K, x + 2 * K, ty + 10 * K], fill=RED, width=2 * K)
    # caption under pill
    d.text((W * K / 2, (y1 + 14) * K), 'CANDLES  ·  DIFFUSERS  ·  MISTS  ·  GIFTS', font=inter(10, 'Medium'),
           fill=(240, 214, 210), anchor='ma')
    return im.resize((W, H), Image.LANCZOS)

os.makedirs(OUT, exist_ok=True)
N = int(DUR * FPS)
rng = [int(ONLY)] if ONLY else range(N)
for k in rng:
    frame(k / FPS).save(f'{OUT}/f{k:04d}.png')
print('frames', N)
