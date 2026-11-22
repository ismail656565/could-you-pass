"""Myth Dug Up — the archaeologist's field notebook (codex style, 1440x2560), in three layouts.
Each function paints draw-on stages into out/<name>/NN_stage.png + out/<name>.png and returns the list of
stage paths (relative to out), in order — use them as a plate in EPISODE['plates'].

  section(...)  a cut through a mound/site: stacked layers, a trench, labels per layer
  plan(...)     a site plan: walls of rooms drawn from rectangles, a scale bar, a north arrow, labels
  chart(...)    a coastal map: coastline, sea contour lines, places, an X where the find is
"""
from pathlib import Path
import numpy as np
from codex import Codex
from core import fbm1d

W, H = 1440, 2560


def _save(c, out, name):
    out = Path(out)
    c.save(str(out / f'{name}.png'), stages_dir=str(out / name))
    return [f'{name}/{i:02d}_{n}.png' for i, (n, _) in enumerate(c.stages)] + [f'{name}.png']


def _sheet(seed, title, subtitle, stain=(1250, 2300, 160), corner='bl'):
    c = Codex(W, H, seed=seed)
    c.sheet(stains=[stain] if stain else None, lost_corner=corner, foxing=0.8)
    c.stage('sheet')
    c.write([title], 120, 140, size=96 if len(title) < 12 else 76, mirror=False, ink=1.0)
    if subtitle:
        c.write([subtitle], 125, 205, size=34, mirror=False, ink=0.8)
    c.stage('title')
    return c


def section(out, name, title, subtitle, layers, seed=21, trench=None, note=None, highlight=(), hump=260):
    """layers: [(label, date)] from the top down. trench: (x0, x1, depth_layer_index, text, year_text) or None.
    highlight: indices of layers rubbed with red chalk; note: (text, layer_index)."""
    c = _sheet(seed, title, subtitle)
    X0, X1 = 110, 1130
    xs = np.linspace(X0, X1, 120)
    n = len(layers)
    surf = 560 - hump * np.exp(-((xs - 640) / 330) ** 2) + fbm1d(120, 20, 3, seed)[:120] * 10
    bounds = [surf]
    top, bottom = 620, 2330
    ys = np.linspace(top, bottom, n + 1)
    for i, y in enumerate(ys[1:]):
        h = max(0, (hump * 0.58 - i * hump * 0.055)) * np.exp(-((xs - 640) / (340 + 25 * i)) ** 2)
        b = y - h + fbm1d(120, 14, 3, seed + 30 + i)[:120] * 14
        bounds.append(np.maximum(b, bounds[-1] + 40))
    c.contour(np.stack([xs, bounds[0]], 1), width=3.2)
    for g in np.linspace(X0 + 10, X1 - 10, 70):
        yb = np.interp(g, xs, bounds[0])
        c.quill([(g, yb), (g + c.rng.uniform(-6, 6), yb - c.rng.uniform(10, 22))], width=1.2, ink=0.7)
    c.stage('surface')
    tm = np.zeros((H, W), np.float32)
    if trench:
        x0, x1, k, text, yr = trench
        yb = float(np.interp((x0 + x1) / 2, xs, bounds[min(n, k + 1)]))
        poly = np.array([(x0, 250), (x1, 250), (x1 - 30, yb), (x0 + 30, yb)], np.float32)
        tm = c.poly_mask(poly)
        c.dotted(poly[[0, 3, 2, 1]], width=1.8)
        c.arrow([(x1 + 140, 330), (x1 + 60, 360), (x1 - 8, 420)], width=1.8)
        c.write([text, yr], x1 + 150, 320, size=30, mirror=False, ink=0.9)
        c.stage('trench')
    masks, mids = [], []
    for i, (lab, date) in enumerate(layers):
        a, b = bounds[i], bounds[i + 1]
        poly = np.vstack([np.stack([xs, a], 1), np.stack([xs[::-1], b[::-1]], 1)])
        m = c.poly_mask(poly) * (1 - tm)
        masks.append(m)
        c.contour(np.stack([xs, b], 1), width=2.4 if i < n - 1 else 3.0, searching=1)
        c.hatch(m, shade=0.25 + 0.5 * i / max(1, n), angle=55 if i % 2 else 35, spacing=6.2 - 2.0 * i / max(1, n))
        yc = float((a[-1] + b[-1]) / 2)
        mids.append(float((a[60] + b[60]) / 2))
        c.write([lab], 1165, yc + 4, size=38 if len(lab) < 11 else 30, mirror=False, ink=1.0)
        if date:
            c.write([date], 1165, yc + 44, size=24, mirror=False, ink=0.75)
        for k in range(4 + i % 4):                               # stones and sherds
            x = c.rng.uniform(X0 + 60, X1 - 60)
            if trench and trench[0] - 40 < x < trench[1] + 40: continue
            yt, yb2 = np.interp(x, xs, a), np.interp(x, xs, b)
            if yb2 - yt < 50: continue
            y = c.rng.uniform(yt + 18, yb2 - 26)
            if c.rng.random() < 0.6:
                for s in range(3):
                    bw = c.rng.uniform(26, 44)
                    c.contour([(x + s * bw, y), (x + (s + 1) * bw - 4, y), (x + (s + 1) * bw - 4, y + 16), (x + s * bw, y + 16)],
                              width=1.6, closed=True, searching=0)
            else:
                c.quill(Codex.arc(x, y, 16, 200, 340), width=2.0)
        c.stage(f'layer_{i:02d}')
    if highlight:
        c.rub(sum(masks[i] for i in highlight), amount=0.32)
    if note:
        text, k = note
        c.write([text], 1165, float((bounds[k][-1] + bounds[k + 1][-1]) / 2) + 84, size=26, mirror=False, ink=0.9)
    for yy in range(top, bottom, 100):
        c.ruled((70, yy), (92, yy), width=1.4)
    c.ruled((80, top), (80, bottom), width=1.4)
    c.stage('notes')
    stages = _save(c, out, name)
    return stages, mids


def box_lines(c, a, b, cc, d, w):
    for p, q in (((a, b), (cc, b)), ((cc, b), (cc, d)), ((cc, d), (a, d)), ((a, d), (a, b))):
        c.ruled(p, q, width=w, overshoot=3.0)


def plan(out, name, title, subtitle, rooms, labels=(), seed=31, hatch_rooms=(), red=(), scale_text='0      10      20 m',
         box=(150, 420, 1290, 2250), extra=None):
    """rooms: [(x0, y0, x1, y1)] in sheet px (walls are drawn as double lines); hatch_rooms: indices drawn as walls of
    stone (hatched); red: indices rubbed with red chalk; labels: [(text, x, y, size)]. extra(c) may draw more."""
    c = _sheet(seed, title, subtitle)
    x0, y0, x1, y1 = box
    c.dotted([(x0 - 30, y0 - 30), (x1 + 30, y0 - 30), (x1 + 30, y1 + 30), (x0 - 30, y1 + 30), (x0 - 30, y0 - 30)], width=1.2, smooth=False)
    c.stage('grid')
    order = np.argsort([r[1] * 3 + r[0] for r in rooms])
    chunk = max(1, len(rooms) // 4)
    for k, i in enumerate(order):
        a, b, cc, d = rooms[i]
        box_lines(c, a, b, cc, d, 2.4)
        if cc - a > 40 and d - b > 40:
            box_lines(c, a + 12, b + 12, cc - 12, d - 12, 1.3)
            ring = c.poly_mask([(a, b), (cc, b), (cc, d), (a, d)]) - c.poly_mask([(a + 12, b + 12), (cc - 12, b + 12), (cc - 12, d - 12), (a + 12, d - 12)])
            c.hatch(np.clip(ring, 0, 1), shade=0.8, angle=45, spacing=4.0, levels=(0.2,), cross=None)
        if i in hatch_rooms:
            c.hatch(c.poly_mask([(a + 12, b + 12), (cc - 12, b + 12), (cc - 12, d - 12), (a + 12, d - 12)]), shade=0.35, angle=35, spacing=7)
        if (k + 1) % chunk == 0:
            c.stage(f'rooms_{k:02d}')
    for i in red:
        a, b, cc, d = rooms[i]
        c.rub(c.poly_mask([(a, b), (cc, b), (cc, d), (a, d)]), amount=0.35)
    if extra:
        extra(c)
    for text, x, y, size in labels:
        c.write([text], x, y, size=size, mirror=False, ink=0.95)
    # scale bar + north arrow
    c.ruled((x0, y1 + 120), (x0 + 400, y1 + 120), width=2.2)
    for k in range(5):
        c.ruled((x0 + k * 100, y1 + 108), (x0 + k * 100, y1 + 132), width=1.6)
    c.write([scale_text], x0 - 6, y1 + 175, size=24, mirror=False, ink=0.8)
    c.arrow([(x1 - 40, y1 + 190), (x1 - 40, y1 + 70)], width=2.2, head=18)
    c.write(['N'], x1 - 52, y1 + 50, size=34, mirror=False)
    c.stage('notes')
    return _save(c, out, name)


def chart(out, name, title, subtitle, seed=41, land='left', places=(), find=None, contours=5, coast_x=720, amp=180,
          islands=(), extra=None):
    """a coastal chart. land: 'left' / 'right' / 'top' / 'bottom' side of the coastline. places: [(text, x, y)] dots
    with names on land; find: (x, y, text) — the X of the find, red-chalk ring, and a hand-written note."""
    c = _sheet(seed, title, subtitle)
    ys = np.linspace(300, 2450, 220)
    xs = coast_x + amp * fbm1d(220, 30, 4, seed) + 60 * fbm1d(220, 6, 3, seed + 1)
    coast = np.stack([xs, ys], 1)
    c.contour(coast, width=2.8, searching=1)
    c.stage('coast')
    if land == 'left':
        lpoly = np.vstack([[[90, 300]], coast, [[90, 2450]]])
        sea_dir = 1
    else:
        lpoly = np.vstack([[[1350, 300]], coast, [[1350, 2450]]])
        sea_dir = -1
    c.hatch(c.poly_mask(lpoly), shade=0.3, angle=55, spacing=7.5, levels=(0.2,), cross=None)
    for (cx, cy, r) in islands:
        pts = Codex.arc(cx, cy, r, 0, 360)
        c.contour(pts, width=2.0, closed=True)
        c.hatch(c.disc_mask(cx, cy, r), shade=0.3, angle=55, spacing=7.5, levels=(0.2,), cross=None)
    c.stage('land')
    for k in range(1, contours + 1):                       # depth lines off the coast
        off = sea_dir * k * 46 + 8 * fbm1d(220, 25, 2, seed + 10 + k)
        c.dotted(np.stack([xs + off, ys], 1), width=1.0, ink=0.6 - 0.07 * k, dash=5, gap=7)
    c.stage('sea')
    for text, x, y in places:
        c.quill(Codex.arc(x, y, 7, 0, 360), width=2.0)
        c.write([text], x + 18, y + 10, size=30, mirror=False, ink=0.9)
    if extra:
        extra(c)
    c.stage('places')
    if find:
        x, y, text = find
        c.quill([(x - 30, y - 30), (x + 30, y + 30)], width=4.5)
        c.quill([(x + 30, y - 30), (x - 30, y + 30)], width=4.5)
        c.sanguines([Codex.arc(x, y, 70 + 6 * k, 0, 350) for k in range(2)], width=4.0)
        c.write([text], x - 160 if x > 900 else x + 90, y + 120, size=32, mirror=False, ink=1.0)
    c.stage('find')
    c.arrow([(1250, 2380), (1250, 2250)], width=2.2, head=18)
    c.write(['N'], 1238, 2230, size=34, mirror=False)
    return _save(c, out, name)
