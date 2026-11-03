import sys, numpy as np, cv2, pickle
from PIL import Image
S = sys.argv[1]
photo = np.array(Image.open(f'{S}/v3/photo.png').convert('RGB')).astype(np.float32)
H, W = photo.shape[:2]
al = np.array(Image.open(f'{S}/v3/cut.png'))[..., 3]
# known-background samples: top band, side bands, bottom band
yy, xx = np.mgrid[0:H:8, 0:W:8]
keep = (yy < 210) | (xx < 90) | (xx > 1885) | (yy > 1905) | ((xx > 1800) & (yy < 1050))
keep &= al[::8, ::8] < 5
X = xx[keep] / W; Y = yy[keep] / H
def basis(X, Y):
    return np.stack([X**i * Y**j for i in range(4) for j in range(4 - i)], 1)
B = basis(X, Y)
gx, gy = np.mgrid[0:H, 0:W]
Bf = basis((gy / W).ravel(), (gx / H).ravel())
bg = np.zeros_like(photo)
for c in range(3):
    coef, *_ = np.linalg.lstsq(B, photo[::8, ::8, c][keep], rcond=None)
    bg[..., c] = (Bf @ coef).reshape(H, W)
bg = np.clip(bg, 0, 255)
Image.fromarray(bg.astype(np.uint8)).save(f'{S}/v3/bgplate.png')
diff = np.abs(cv2.GaussianBlur(photo, (0, 0), 2) - bg).max(2)
stand = np.clip((diff - 5) * 255 / 10, 0, 255)
stand = cv2.morphologyEx(stand.astype(np.uint8), cv2.MORPH_CLOSE, np.ones((25, 25), np.uint8))
stand = cv2.GaussianBlur(stand, (0, 0), 1.5)
Image.fromarray(stand).save(f'{S}/v3/standmask.png')
print('resid', np.abs(photo[::8, ::8][keep] - bg[::8, ::8][keep]).mean())
