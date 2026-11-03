from PIL import Image, ImageDraw
def cyl(d, x0, x1, ytop, ybot, ry, fill=255):
    cx = (x0 + x1) / 2
    d.rectangle([x0, ytop, x1, ybot], fill=fill)
    d.ellipse([x0, ytop - ry, x1, ytop + ry], fill=fill)
    d.ellipse([x0, ybot - ry, x1, ybot + ry], fill=fill)
STANDS = {
  'leftcyl':  lambda d: cyl(d, 106, 606, 1060, 1560, 24),
  'block':    lambda d: d.rectangle([572, 884, 1262, 1470], fill=255),
  'rightcyl': lambda d: cyl(d, 1258, 1792, 962, 1560, 26),
  'step2':    lambda d: cyl(d, 612, 1198, 1342, 1396, 44),
  'step1':    lambda d: cyl(d, 450, 1342, 1478, 1596, 68),
}
def stand_mask(size=(2000, 2000)):
    m = Image.new('L', size, 0); d = ImageDraw.Draw(m)
    for f in STANDS.values(): f(d)
    return m
