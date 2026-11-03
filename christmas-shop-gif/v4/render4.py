import sys, os, math, random, numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from scipy import ndimage as nd
sys.path.insert(0, os.path.dirname(__file__)); from stands import stand_mask
S = sys.argv[1]; OUT = sys.argv[2]; ONLY = sys.argv[3] if len(sys.argv) > 3 else None
W, H = 600, 830
FPS, DUR = 20, 7.4
RED = (128, 24, 34); CREAM = (247, 241, 232)
F = S + '/fonts/'
def inter(sz, w='SemiBold'):
    f = ImageFont.truetype(F + 'Inter.ttf', int(sz)); f.set_variation_by_name(w); return f
cardo = lambda sz: ImageFont.truetype(F + 'Cardo-Regular.ttf', int(sz))
clamp = lambda v: max(0.0, min(1.0, v))
def ease_out_back(t, s=1.3):
    t -= 1; return t * t * ((s + 1) * t + s) + 1
smooth = lambda t: t * t * (3 - 2 * t)

# ---- scene geometry: photo crop -> page ---------------------------------
CX0, CY0, CX1, CY1 = 50, 160, 1950, 1940
SC = W / (CX1 - CX0)
TOP = 100                                    # scene top on page
SH = round((CY1 - CY0) * SC)
def P(x, y): return ((x - CX0) * SC, TOP + (y - CY0) * SC)
photo = Image.open(f'{S}/v3/photo.png').convert('RGB')
cut = Image.open(f'{S}/v3/cut.png')
al = np.clip((np.array(cut)[..., 3].astype(np.float32) - 20) * 255 / 200, 0, 255)
bgp = Image.open(f'{S}/v3/bgplate.png').convert('RGB')
def to_scene(img, resample=Image.LANCZOS):
    return img.crop((CX0, CY0, CX1, CY1)).resize((W, SH), resample)

# background: studio gradient, gently cooled/darkened at the top so snow reads
bg_scene = np.array(to_scene(bgp), np.float32)
top_col = bg_scene[:6].mean((0, 1))
canvas = np.zeros((H, W, 3), np.float32); canvas[:] = top_col
canvas[TOP:TOP + SH] = bg_scene
yy = np.arange(H)[:, None]
shade = np.where(yy < TOP, 0.93 + 0.07 * yy / TOP, 1.0)
canvas *= shade[..., None]
BG = Image.fromarray(np.clip(canvas, 0, 255).astype(np.uint8))

# stands layer (photo pixels inside traced stand shapes)
# product groups
GROUPS = [
 ('diffuser', [(596, 336, 862, 640), (618, 620, 842, 892), (826, 224, 1032, 882)]),
 ('pillar',   [(1056, 596, 1274, 884), (1296, 436, 1598, 968), (1610, 600, 1730, 964)]),
 ('minis',    [(266, 426, 338, 704), (421, 436, 496, 704), (196, 696, 552, 1040), (490, 784, 560, 1004), (256, 962, 552, 1078)]),
 ('candle',   [(696, 1010, 948, 1398), (910, 1030, 1190, 1368)]),
 ('bodywash', [(1376, 1156, 1640, 1664), (1636, 1090, 1870, 1650)]),
 ('oilperf',  [(512, 1210, 608, 1474), (1180, 1198, 1354, 1518)]),
 ('cracker',  [(104, 1250, 424, 1756)]),
 ('soapcream',[(450, 1540, 856, 1836), (914, 1494, 1196, 1796)]),
 ('wax',      [(1244, 1644, 1836, 1876)]),
]
import cv2
from stands import STANDS as STAND_SHAPES
sm = stand_mask().filter(ImageFilter.GaussianBlur(2))
prod = np.zeros(al.shape, bool)
for _n, _rects in GROUPS:
    for x0, y0, x1, y1 in _rects: prod[y0:y1, x0:x1] |= al[y0:y1, x0:x1] > 3
hole = cv2.dilate(prod.astype(np.uint8), np.ones((21, 21), np.uint8)) > 0
parr0 = np.array(photo).astype(np.float32)
stand_rgb = parr0.copy()
covered = np.zeros(al.shape, bool)
for name in ['step2', 'step1', 'rightcyl', 'leftcyl', 'block']:      # front to back
    m = Image.new('L', (2000, 2000), 0); STAND_SHAPES[name](ImageDraw.Draw(m)); m = np.array(m) > 128
    vis = m & ~covered
    ok = vis & ~hole
    need = vis & hole
    cols = np.where(need.any(0))[0]
    colval = np.full((2000, 3), np.nan, np.float32)
    for x in np.where(vis.any(0))[0]:
        idx = np.where(ok[:, x])[0]
        if len(idx) > 3: colval[x] = np.median(parr0[idx, x], 0)
    xs = np.arange(2000); good = ~np.isnan(colval[:, 0])
    if good.sum() > 1:
        for c in range(3): colval[:, c] = np.interp(xs, xs[good], colval[good, c])
        colval = cv2.GaussianBlur(colval[None], (0, 0), 3)[0]
        ys_, xs_ = np.where(need)
        stand_rgb[ys_, xs_] = colval[xs_]
    covered |= m
kk = cv2.GaussianBlur(hole.astype(np.float32), (0, 0), 3)[..., None]
stand_rgb = parr0 * (1 - kk) + stand_rgb * kk
st = Image.fromarray(np.clip(stand_rgb, 0, 255).astype(np.uint8)); st.putalpha(sm)
STANDS = to_scene(st)
reg = cv2.dilate(((np.array(sm) > 40) | prod).astype(np.uint8), np.ones((31, 31), np.uint8)).astype(np.float32)
reg = cv2.GaussianBlur(reg, (0, 0), 10)
so = photo.copy(); so.putalpha(Image.fromarray((reg * 255).astype(np.uint8)))
STANDS_ORIG = to_scene(so)
STANDS.save(f'{S}/v3/stands_scene.png')

parr = np.array(photo)
LAY = []
for gi, (n, rects) in enumerate(GROUPS):
    m = np.zeros(al.shape, np.float32)
    for x0, y0, x1, y1 in rects: m[y0:y1, x0:x1] = al[y0:y1, x0:x1]
    for _, r2 in GROUPS[gi + 1:]:
        for x0, y0, x1, y1 in r2:
            sub = m[y0:y1, x0:x1]; sub[al[y0:y1, x0:x1] > 128] = 0
    lay = Image.fromarray(np.dstack([parr, m.astype(np.uint8)]), 'RGBA')
    LAY.append((n, to_scene(lay)))

# garland + its bulbs
g = Image.open(f'{S}/v3/gen/garland_cut.png').convert('RGBA'); g = g.crop(g.split()[3].getbbox())
GW = 660; GH = round(g.height * GW / g.width * 0.72)
GARL = g.resize((GW, GH), Image.LANCZOS)
ga = np.array(g).astype(np.int32)
bulb = (ga[..., 0] > 235) & (ga[..., 1] > 205) & (ga[..., 2] < 215) & (ga[..., 3] > 200)
lab, nb = nd.label(nd.binary_dilation(bulb, iterations=3))
cents = nd.center_of_mass(bulb, lab, range(1, nb + 1)); sizes = nd.sum(bulb, lab, range(1, nb + 1))
BT = 712                                       # banner top
GX, GY = (W - GW) // 2, BT - GH // 2 - 6
BULBS = [(GX + c[1] * GW / g.width, GY + c[0] * GH / g.height, random.Random(i).uniform(0, 6.28))
         for i, (c, s_) in enumerate(zip(cents, sizes)) if s_ > 25]

random.seed(11)
# twinkle lights in the open background areas
def in_bg(x, y):
    if y < TOP + 6 or y > TOP + SH - 30: return False
    px = CX0 + (x) / SC; py = CY0 + (y - TOP) / SC
    if not (0 <= px < 2000 and 0 <= py < 2000): return False
    return al[int(py), int(px)] < 5 and sm.getpixel((int(px), int(py))) < 10
STARS = []
while len(STARS) < 30:
    x, y = random.uniform(8, W - 8), random.uniform(TOP + 8, TOP + SH - 40)
    if in_bg(x, y): STARS.append((x, y, random.uniform(4, 10), random.uniform(0, 6.28), random.uniform(1.4, 3.0)))
FLAKES = [(random.uniform(0, W), random.uniform(0, H), random.uniform(1.0, 2.6), random.uniform(16, 36),
           random.uniform(0, 6.28)) for _ in range(120)]

def static_ui():
    ui = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(ui)
    d.rectangle([0, BT, W, H], fill=RED)
    d.text((W / 2, BT + 44), 'Find the perfect gift this Christmas', font=cardo(30), fill=CREAM, anchor='ma')
    f = inter(11, 'SemiBold'); s = 'THE CHRISTMAS SHOP IS NOW OPEN'
    ws = [d.textlength(c, font=f) for c in s]; x = W / 2 - (sum(ws) + 3 * (len(s) - 1)) / 2
    for c, w_ in zip(s, ws): d.text((x, BT + 92), c, font=f, fill=(238, 205, 200)); x += w_ + 3
    return ui
UI = static_ui()

def star(d, x, y, r, k):
    c = (255, 244, 214); g_ = int(255 * k)
    d.ellipse([x - r * .6, y - r * .6, x + r * .6, y + r * .6], fill=c + (int(g_ * .35),))
    d.line([x - r * 1.7, y, x + r * 1.7, y], fill=c + (g_,), width=1)
    d.line([x, y - r * 1.7, x, y + r * 1.7], fill=c + (g_,), width=1)
    d.ellipse([x - 1.8, y - 1.8, x + 1.8, y + 1.8], fill=(255, 255, 255, g_))

# ---------- realistic snow + bokeh fairy lights ----------
_SPR = {}
def sprite(sig, core=0.0):
    key = (round(sig, 1), core)
    if key not in _SPR:
        r = int(sig * 3.2) + 2
        y, x = np.mgrid[-r:r + 1, -r:r + 1].astype(np.float32)
        d2 = x * x + y * y
        g = np.exp(-d2 / (2 * sig * sig))
        if core: g = np.maximum(g, core * np.exp(-d2 / (2 * (sig * 0.28) ** 2)))
        _SPR[key] = (g / g.max(), r)
    return _SPR[key]
def screen_add(buf, x, y, spr, color, a):
    g, r = spr
    x0, y0 = int(round(x)) - r, int(round(y)) - r
    x1, y1 = x0 + g.shape[1], y0 + g.shape[0]
    cx0, cy0, cx1, cy1 = max(x0, 0), max(y0, 0), min(x1, W), min(y1, H)
    if cx0 >= cx1 or cy0 >= cy1: return
    k = g[cy0 - y0:cy1 - y0, cx0 - x0:cx1 - x0, None] * a
    reg = buf[cy0:cy1, cx0:cx1]
    reg += (np.array(color, np.float32) - reg) * k      # 'lighten towards colour'
rs = random.Random(21)
SNOW = []
for layer, n, rr, op, spd, sig in (('far', 130, (0.6, 1.0), (0.7, 0.95), (10, 18), 0.75),
                                   ('mid', 60, (1.2, 1.9), (0.9, 1.0), (22, 34), 1.05),
                                   ('near', 10, (4.0, 6.5), (0.45, 0.65), (55, 80), 3.0)):
    for _ in range(n):
        r_ = rs.uniform(*rr)
        SNOW.append(dict(x=rs.uniform(-20, W + 20), y=rs.uniform(0, H), sig=max(sig, r_ * (0.9 if layer == 'near' else 0.75)),
                         a=rs.uniform(*op), v=rs.uniform(*spd), wob=rs.uniform(0.4, 1.3), amp=rs.uniform(3, 10) * (2 if layer == 'near' else 1),
                         ph=rs.uniform(0, 6.28)))
LIGHTS = []
tries = 0
while len(LIGHTS) < 26 and tries < 5000:
    tries += 1
    x, y = rs.uniform(8, W - 8), rs.uniform(TOP + 6, TOP + SH - 40)
    if in_bg(x, y):
        LIGHTS.append(dict(x=x, y=y, sig=rs.uniform(1.8, 4.8), a=rs.uniform(0.7, 1.0),
                           f1=rs.uniform(0.7, 1.6), f2=rs.uniform(2.1, 3.7), ph=rs.uniform(0, 6.28),
                           col=rs.choice([(255, 220, 150), (255, 230, 180), (255, 206, 130)])))
def lights_fx(im, t):
    buf = np.array(im.convert('RGB'), np.float32)
    for L in LIGHTS:
        fl = 0.62 + 0.25 * math.sin(t * L['f1'] * 2 + L['ph']) + 0.13 * math.sin(t * L['f2'] * 2 + L['ph'] * 1.7)
        screen_add(buf, L['x'], L['y'], sprite(L['sig'] * 3.2), (255, 200, 120), L['a'] * 0.30 * fl)  # wide warm halo
        screen_add(buf, L['x'], L['y'], sprite(L['sig'] * 1.4), L['col'], L['a'] * 0.65 * fl)          # glow
        screen_add(buf, L['x'], L['y'], sprite(L['sig'] * 0.55, 0.0), (255, 248, 232), L['a'] * fl)  # bulb core
    return buf
def snow_fx(buf, t):
    wind = 6 * math.sin(t * 0.35)
    for f in SNOW:
        y = (f['y'] + t * f['v']) % (H + 40) - 20
        x = f['x'] + wind * (f['v'] / 30) + f['amp'] * math.sin(t * f['wob'] + f['ph'])
        screen_add(buf, x + 0.6, y + 0.9, sprite(f['sig'] * 1.25), (150, 158, 172), f['a'] * 0.22)
        screen_add(buf, x, y, sprite(f['sig']), (255, 255, 255), f['a'])
    return buf

TYPED = 'valentte christmas shop'
STAND_IN, EXIT = (0.15, 0.65), 6.0
def frame(t):
    im = BG.copy().convert('RGBA')
    out = 1 - smooth(clamp((t - EXIT) / 0.5))
    def put(layer, a, dy=0):
        if a <= 0: return
        if a < 1:
            layer = layer.copy(); layer.putalpha(layer.split()[3].point(lambda v: int(v * a)))
        y = TOP + round(dy)
        if y >= 0: im.alpha_composite(layer, (0, y))
        else: im.alpha_composite(layer.crop((0, -y, W, SH)), (0, 0))
    sa = smooth(clamp((t - STAND_IN[0]) / (STAND_IN[1] - STAND_IN[0]))) * out
    xf = smooth(clamp((t - 3.3) / 0.4))
    if xf < 1: put(STANDS, sa)
    LATE = xf
    for i, (n, lay) in enumerate(LAY):
        p = clamp((t - (0.55 + 0.27 * i)) / 0.5)
        if p <= 0: continue
        put(lay, clamp(p * 2.5) * out, (1 - ease_out_back(p)) * -70)
    if LATE > 0: put(STANDS_ORIG, LATE * out)
    im = Image.fromarray(np.clip(lights_fx(im, t), 0, 255).astype(np.uint8)).convert('RGBA')
    im.alpha_composite(UI)
    im.alpha_composite(GARL, (GX, GY))
    gl = Image.new('RGBA', (W, H), (0, 0, 0, 0)); dg = ImageDraw.Draw(gl)
    for bx, by, ph in BULBS:
        k = 0.35 + 0.65 * (0.5 + 0.5 * math.sin(t * 4.2 + ph)) ** 2
        rr = 5 + 4 * k
        dg.ellipse([bx - rr, by - rr, bx + rr, by + rr], fill=(255, 214, 120, int(150 * k)))
        dg.ellipse([bx - 2, by - 2, bx + 2, by + 2], fill=(255, 250, 225, int(255 * k)))
    im.alpha_composite(gl.filter(ImageFilter.GaussianBlur(2.2)))
    im = Image.fromarray(np.clip(snow_fx(np.array(im.convert('RGB'), np.float32), t), 0, 255).astype(np.uint8)).convert('RGBA')
    d = ImageDraw.Draw(im)
    # search bar
    x0, y0, x1, y1 = 30, 22, 570, 90
    shd = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(shd).rounded_rectangle([x0, y0 + 5, x1, y1 + 5], radius=34, fill=(40, 40, 60, 60))
    im.alpha_composite(shd.filter(ImageFilter.GaussianBlur(8))); d = ImageDraw.Draw(im)
    d.rounded_rectangle([x0, y0, x1, y1], radius=34, fill=(255, 255, 255))
    cy = (y0 + y1) / 2; mx = x0 + 38
    d.ellipse([mx - 11, cy - 13, mx + 9, cy + 7], outline=RED, width=3)
    d.line([mx + 6, cy + 4, mx + 15, cy + 13], fill=RED, width=4)
    cx_ = x1 - 38
    for s in (1, -1): d.line([cx_ - 9, cy - 9 * s, cx_ + 9, cy + 9 * s], fill=RED, width=3)
    n = int(clamp((t - 0.3) / 2.0) * len(TYPED)); txt = TYPED[:n].upper()
    f = inter(22, 'SemiBold'); x = mx + 32
    for c in txt: d.text((x, cy), c, font=f, fill=RED, anchor='lm'); x += d.textlength(c, font=f) + 1.5
    if n < len(TYPED) or int(t * 2.4) % 2 == 0: d.line([x + 3, cy - 14, x + 3, cy + 14], fill=RED, width=2)
    return im.convert('RGB')

os.makedirs(OUT, exist_ok=True)
N = int(DUR * FPS)
for k in ([int(ONLY)] if ONLY else range(N)): frame(k / FPS).save(f'{OUT}/f{k:04d}.png')
print('frames', N, 'bulbs', len(BULBS))
