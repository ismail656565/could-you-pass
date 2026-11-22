"""Myth Dug Up #001 — Troy. Plates: an Attic black-figure amphora with the wooden horse (blackfigure),
and Schliemann's section through Hisarlik in an 1870s field notebook (codex). Facts: Schliemann (German businessman)
began digging at Hisarlik in 1871; nine main settlement layers Troy I (c. 3000 BC) to IX (Roman);
Troy VI/VIIa are the usual candidates for Homer's Troy; most archaeologists accept Hisarlik = Troy, the war is debated."""
from pathlib import Path
import numpy as np
import blackfigure as B
from blackfigure import BlackFigure, _Fig, _horse, _ribbon, _circle, _closed, _runner
from codex import Codex
from core import fbm1d

STAND = {'nf': ([(0.33, -0.66), (0.35, -0.48), (0.36, -0.30), (0.37, -0.10), (0.40, -0.02)], [0.15, 0.11, 0.085, 0.075, 0.075]),
         'ff': ([(0.28, -0.66), (0.27, -0.48), (0.25, -0.30), (0.24, -0.10), (0.27, -0.02)], [0.14, 0.10, 0.08, 0.07, 0.07]),
         'nh': ([(-0.47, -0.67), (-0.42, -0.45), (-0.47, -0.28), (-0.46, -0.10), (-0.43, -0.02)], [0.22, 0.14, 0.085, 0.075, 0.075]),
         'fh': ([(-0.52, -0.65), (-0.56, -0.45), (-0.61, -0.28), (-0.60, -0.10), (-0.57, -0.02)], [0.2, 0.13, 0.08, 0.07, 0.07])}

def trojan_horse(zone, x, hw):
    f = _Fig()
    old = B._H_LEGS; B._H_LEGS = STAND
    _horse(f, bend=0.04, legs=(0, 0, 0, 0))
    B._H_LEGS = old
    for y in (-0.80, -0.70, -0.60, -0.50):                    # planks
        f.cut([(-0.55, y), (-0.2, y + 0.01), (0.15, y), (0.38, y - 0.01)], w=0.9)
    f.reserve([(-0.22, -0.68), (0.02, -0.68), (0.02, -0.52), (-0.22, -0.52)])   # the hatch
    f.cut([(-0.22, -0.68), (0.02, -0.68), (0.02, -0.52), (-0.22, -0.52), (-0.22, -0.68)], w=1.0)
    f.slip([(-0.80, 0.0), (0.72, 0.0), (0.72, 0.09), (-0.80, 0.09)])           # platform
    f.cut([(-0.78, 0.045), (0.70, 0.045)], w=0.9)
    for wx in (-0.62, -0.2, 0.25, 0.58):
        f.slip(_circle(wx, 0.19, 0.11, 18))
        f.cut(_circle(wx, 0.19, 0.035, 8), closed=True, w=0.9)
        f.red(_circle(wx, 0.19, 0.03, 8))
    zone.emit(f, x, zone.y1 - 0.30 * hw, hw)

def hoplite(zone, x, h, facing=1, phase=0):
    f = _Fig()
    _runner(f, phase, 1.0, True, 'down', zone.rng)
    f.line([(-0.30, -0.55), (0.55, -1.05)], w=2.0, taper=True)                  # spear
    f.slip(_circle(0.02, -0.64, 0.17, 28))                                       # round shield
    f.red(_circle(0.02, -0.64, 0.10, 20))
    f.cut(_circle(0.02, -0.64, 0.155, 26), closed=True, w=1.0)
    f.slip([(0.17, -0.925), (0.19, -1.0), (0.02, -1.035), (-0.07, -0.95)])         # helmet crest
    f.red([(0.15, -0.94), (0.17, -0.99), (0.03, -1.02), (-0.04, -0.955)])
    zone.emit(f, x, None, h, facing=facing)



def paint_vase(out):
    W, Hc = 1440, 2560
    bf = BlackFigure(W, Hc, seed=11)
    bf.museum(wall='#1a2124', plinth='#c9bfae')
    H = 1900
    pot = bf.throw(cx=720, foot=2330, height=H)
    Y = lambda f: f * H
    bf.stage('thrown')
    pot.paint_handles()
    for a, b in [(0, .062), (.062, .080), (.212, .244), (.320, .326), (.640, .646), (.671, .676), (.722, .745), (.751, .756), (.850, .928), (.940, .994)]:
        pot.band(Y(a), Y(b))
    bf.stage('bands')
    pot.palmettes(Y(.084), Y(.210), n=5)
    pot.tongues(Y(.247), Y(.316))
    pot.meander(Y(.648), Y(.670))
    pot.rays(Y(.756), Y(.850))
    bf.stage('ornament')
    z = pot.zone(Y(.326), Y(.640))
    q = z.C / 4                      # centre of the visible front
    zh = z.y1 - z.y0
    trojan_horse(z, q + 60, zh * 0.66)
    z.letters('ΙΠΠΟΣ', q - 120, z.y0 + 26, size=26)
    for dx, fc, ph in ((-800, 1, 0), (-590, 1, 1), (640, -1, 0), (840, -1, 1)):
        hoplite(z, q + dx, zh * 0.74, fc, ph)
    z.letters('ΙΛΙΟΣ', q + 420, z.y0 + 26, size=26)
    z.bird(q - 330, z.y0 + 60, size=60, facing=1, flap=0.2)
    pot.paint(); bf.stage('silhouettes')
    pot.incise(); bf.stage('incision')
    pot.add_colour(); bf.stage('colour')
    pot.fire(); bf.stage('fired')
    pot.age(chips=5, roots=10); bf.stage('aged')
    bf.save(str(out / 'vase.png'), stages_dir=str(out / 'vase'))


def paint_strata(out):
    W, H = 1440, 2560
    c = Codex(W, H, seed=21)
    c.sheet(stains=[(1250, 2300, 160)], lost_corner='bl', foxing=0.8)
    c.stage('sheet')
    X0, X1 = 110, 1130
    xs = np.linspace(X0, X1, 120)
    # mound surface
    surf = 560 - 260 * np.exp(-((xs - 640) / 330) ** 2) + fbm1d(120, 20, 3, 3)[:120] * 10
    bounds = [surf]
    tops = [620, 760, 900, 1060, 1230, 1400, 1600, 1830, 2060, 2330]
    for i, y in enumerate(tops[1:]):
        hump = (150 - i * 14) * np.exp(-((xs - 640) / (340 + 25 * i)) ** 2)
        b = y - hump + fbm1d(120, 14, 3, 30 + i)[:120] * 14
        bounds.append(np.maximum(b, bounds[-1] + 40))
    names = ['IX', 'VIII', 'VII', 'VI', 'V', 'IV', 'III', 'II', 'I']
    dates = ['Roman', 'Greek · c. 700 BC', 'c. 1300–950 BC', '1750–1300 BC', '1900–1750 BC', '2200–1900 BC', 'c. 2250 BC', '2550–2250 BC', 'c. 3000 BC']
    trench = np.array([(560, 250), (720, 250), (690, 1560), (590, 1560)], np.float32)
    tm = c.poly_mask(trench)
    c.write(['HISARLIK'], 120, 140, size=96, mirror=False, ink=1.0)
    c.write(['section through the mound · N — S'], 125, 205, size=34, mirror=False, ink=0.8)
    c.stage('title')
    c.contour(np.stack([xs, bounds[0]], 1), width=3.2)
    for g in np.linspace(X0 + 10, X1 - 10, 70):                  # grass on the surface
        yb = np.interp(g, xs, bounds[0])
        c.quill([(g, yb), (g + c.rng.uniform(-6, 6), yb - c.rng.uniform(10, 22))], width=1.2, ink=0.7)
    c.stage('surface')
    # the trench
    c.dotted(trench[[0, 3, 2, 1]], width=1.8)
    c.arrow([(860, 330), (780, 360), (712, 420)], width=1.8)
    c.write(["Schliemann's trench", '1871–73'], 870, 320, size=30, mirror=False, ink=0.9)
    c.stage('trench')
    masks = []
    for i in range(9):
        top, bot = bounds[i], bounds[i + 1]
        poly = np.vstack([np.stack([xs, top], 1), np.stack([xs[::-1], bot[::-1]], 1)])
        m = c.poly_mask(poly) * (1 - tm)
        masks.append(m)
        c.contour(np.stack([xs, bot], 1), width=2.4 if i < 8 else 3.0, searching=1)
        c.hatch(m, shade=0.25 + 0.06 * i, angle=55 if i % 2 else 35, spacing=6.2 - 0.25 * i)
        yc = float(np.interp(1180, xs, (top + bot) / 2)) if False else float((top[-1] + bot[-1]) / 2)
        c.write([f'TROY {names[i]}'], 1165, yc + 4, size=38, mirror=False, ink=1.0)
        c.write([dates[i]], 1165, yc + 44, size=24, mirror=False, ink=0.75)
        # walls and sherds inside the layer
        for k in range(5 + i):
            x = c.rng.uniform(X0 + 60, X1 - 60)
            if 520 < x < 760: continue
            yt, yb2 = np.interp(x, xs, top), np.interp(x, xs, bot)
            y = c.rng.uniform(yt + 18, yb2 - 26)
            if c.rng.random() < 0.6:
                for s in range(3):
                    bw = c.rng.uniform(26, 44)
                    c.contour([(x + s * bw, y), (x + (s + 1) * bw - 4, y), (x + (s + 1) * bw - 4, y + 16), (x + s * bw, y + 16)], width=1.6, closed=True, searching=0)
            else:
                c.quill(Codex.arc(x, y, 16, 200, 340), width=2.0)
        c.stage(f'layer_{names[i]}')
    # red chalk: Homer's candidates
    c.rub(masks[2] + masks[3], amount=0.32)
    c.write(["Homer's Troy?"], 1165, float((bounds[3][-1] + bounds[4][-1]) / 2) + 84, size=26, mirror=False, ink=0.9)
    for yy in range(int(tops[0]), 2330, 100):                     # depth scale
        c.ruled((70, yy), (92, yy), width=1.4)
    c.ruled((80, 620), (80, 2330), width=1.4)
    c.stage('final_notes')
    c.save(str(out / 'strata.png'), stages_dir=str(out / 'strata'))


def paint(work):
    out = Path(work)
    out.mkdir(parents=True, exist_ok=True)
    paint_vase(out)
    paint_strata(out)


PH = 2560
V = ['vase/03_silhouettes.png', 'vase/04_incision.png', 'vase/05_colour.png', 'vase/06_fired.png', 'vase/07_aged.png', 'vase.png']
S = ['strata/%s.png' % n for n in ('00_sheet', '01_title', '02_surface', '03_trench', '04_layer_IX', '05_layer_VIII', '06_layer_VII',
     '07_layer_VI', '08_layer_V', '09_layer_IV', '10_layer_III', '11_layer_II', '12_layer_I', '13_final_notes')] + ['strata.png']

EPISODE = dict(
    chapter='Troy',
    title="Everyone Said Troy Was a Myth. Then Someone Dug. #shorts",
    description=("For centuries Troy was just Homer's story. In 1871 Heinrich Schliemann started digging into a hill called "
                 "Hisarlik in Turkey and found not one city, but nine, stacked on top of each other.\n\n"
                 "Proven: a real city at Hisarlik that most archaeologists identify as Troy.\n"
                 "Debated: whether the Trojan War happened the way Homer told it.\n\n"
                 "Illustrations painted with code (no photos), narration is synthetic."),
    tags=['troy', 'trojan war', 'archaeology', 'schliemann', 'hisarlik', 'homer', 'iliad', 'ancient history', 'myth', 'history shorts'],
    voice='bm_george',
    lines=["Everyone said this city never existed.",
           "Troy. The wooden horse. A ten-year war. For centuries, it was just a story from Homer.",
           "Then, in eighteen seventy-one, a German businessman named Heinrich Schliemann started digging into a hill in Turkey called Hisarlik.",
           "He didn't find one city. He found nine. Stacked on top of each other, over three thousand years deep.",
           "Today, most archaeologists agree: this hill is Troy. But the war? That's still debated."],
    gaps=[0.15, 0.30, 0.45, 0.40, 0.45],
    display=[(1, 'ten-year.', '10-YEAR.'), (2, 'eighteen', '1871,'), (2, 'seventy-one,', ''), (3, 'three', '3,000'), (3, 'thousand', '')],
    plates=[dict(stages=V, show=[(0, 0), (0.55, 1), (1.05, 2), (1.6, 3), (2.1, 4), (2.6, 5)]),
            dict(stages=S, show=[(0, 0), ('L2+0.25', 1), ('L2+0.75', 2), ('L2:digging', 3)] +
                 [('L3@%.3f' % (0.02 + i * 0.085), 4 + i) for i in range(9)] + [('L4:agree-0.2', 13), ('L4:debated', 14)])],
    camera=[(0, 715, 1330, 1150), ('L1-0.05', 712, 1320, 960), ('L1+2.55', 720, 1300, 2420), ('L2-0.25', 720, 1290, 2300),
            ('L2+0.5', 480, PH + 480, 1350), ('L2:digging-0.4', 540, PH + 580, 1450), ('L2:digging+0.6', 650, PH + 720, 1550),
            ('L3+0.2', 960, PH + 840, 1500), ('L3.end-0.2', 960, PH + 1790, 1500), ('L4+0.2', 930, PH + 1760, 1560),
            ('L4+2.2', 720, PH + 1300, 2500), ('END', 720, PH + 1260, 2420)],
    cards=[dict(at='L1', until='L2-0.15', text='TROY', font='Cinzel-700', size=150, paper=(24, 20, 18), ink=(214, 120, 64), x=540, y=210, rot=-3),
           dict(at='L2:eighteen-0.05', until='L3-0.1', text='1871', font='AlfaSlabOne-400', size=120, ink=(150, 34, 26), x=860, y=300, rot=4),
           dict(at='L2:heinrich-0.05', until='L2:digging+0.2', text='HEINRICH SCHLIEMANN', size=64, x=540, y=1060, rot=-2)],
    counter=dict(start='L3:found-0.05', full='L3.end-0.6', until='L4+0.6', n=9, fmt='CITY {n}', x=300, y=300),
    stamps=[dict(at='L4:agree', text='CITY: PROVEN', color=(30, 70, 52), x=540, y=700, rot=-6),
            dict(at='L4:debated', text='WAR: DEBATED', color=(160, 32, 24), x=540, y=900, rot=5)],
    music=dict(sections=[(0, 'L2-0.25', ['Dm9', 'Am9'], dict(bright=(0.2, 0.35), gain=(0.9, 1.0), plucks=0.35)),
                         ('L2-0.25', 'L3+0.2', ['Fmaj7', 'Esus'], dict(bright=(0.35, 0.45), pulse=True, plucks=0.3)),
                         ('L3+0.2', 'L4', ['Dm9', 'Esus'], dict(bright=(0.45, 0.65), gain=(1, 1.1), pulse=True, ticks=True)),
                         ('L4', 'END', ['Am9', 'Fmaj7'], dict(bright=(0.5, 0.3), gain=(1, 0.0), plucks=0.4))]),
)
