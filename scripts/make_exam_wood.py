"""Holztisch-Textur fürs Long-Layout "exam" (prozedural, kein Fremdbild). → public/exam/desk.jpg"""
import numpy as np
from PIL import Image, ImageFilter
from pathlib import Path

W, H = 1920, 1080
rng = np.random.default_rng(4)


def noise(sx, sy, oct=5):
    out = np.zeros((H, W))
    amp, tot = 1.0, 0
    for o in range(oct):
        gx, gy = max(2, int(W / sx * 2 ** o)), max(2, int(H / sy * 2 ** o))
        g = rng.random((gy + 1, gx + 1))
        im = Image.fromarray((g * 255).astype(np.uint8)).resize((W, H), Image.BICUBIC)
        out += amp * np.asarray(im) / 255
        tot += amp
        amp *= 0.5
    return out / tot


y = np.arange(H)[:, None] * np.ones((1, W))
x = np.ones((H, 1)) * np.arange(W)[None, :]
n1 = noise(900, 60)
n2 = noise(300, 14, 4)
plank_h = 216
plank = (y // plank_h).astype(int)
off = rng.random(10) * 1000
grain = np.sin((y + n1 * 90 + n2 * 14) * 0.21 + off[plank] ) * 0.5 + 0.5
grain = grain ** 3
fine = noise(500, 3, 3)
base = np.array([0.66, 0.43, 0.25])
dark = np.array([0.42, 0.25, 0.13])
tone = (rng.random(10) * 0.12 - 0.06)[plank]
mix = np.clip(0.55 * grain + 0.35 * fine + 0.25 * n1 - 0.1, 0, 1)
img = base[None, None, :] * (1 - mix[..., None]) + dark[None, None, :] * mix[..., None]
img = img * (1 + tone[..., None])
# Fugen zwischen den Brettern
seam = (y % plank_h) < 3
img[seam] *= 0.55
# Vignette
cx, cy = W / 2, H * 0.45
d = np.sqrt(((x - cx) / W) ** 2 + ((y - cy) / H) ** 2)
img *= np.clip(1.15 - d * 0.9, 0.45, 1)[..., None]
out = Image.fromarray(np.clip(img * 255, 0, 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(0.6))
p = Path(__file__).resolve().parent.parent / 'public' / 'exam' / 'desk.jpg'
out.save(p, quality=86)
print(p)
