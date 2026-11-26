"""PlotMelt #006 — 'When the dragon has ONE weakness' (original fiction, "When…" meme-caption experiment).
Plate 1: a huge smug green dragon in a field, a tiny knight with a torch; then arrows, a broken sword and a catapult
boulder that bounced off. Plate 2: the same dragon screaming on a tiny wooden chair, a small spider on the grass;
then the spider gets a crown. Top ~22 % of every plate is left plain for the caption. Hand-inked cartoon
(claude-drawing-skill: cartoon). No real brands or known characters."""
from pathlib import Path
import numpy as np
from cartoon import Cartoon, WHITE, RED, YELLOW

E, R, P = Cartoon.ellipse_pts, Cartoon.rrect_pts, Cartoon.place
W, PH = 1440, 2560
GRN, GRN_D, BELLY = '#5fae4e', '#3f8436', '#f2dc8a'
SKY, GRASS, GRASS_D = '#f6eed8', '#8cc66a', '#6aa24c'
STEEL, STEEL_D = '#b9c2cc', '#8a95a3'
WOOD, WOOD_D = '#a8743f', '#7d5429'


def scene(c):
    c.paper()
    c.fill(np.array([(0, 0), (W, 0), (W, PH), (0, PH)], np.float32), SKY, knock=False)
    c.shape(np.array([(0, 1880), (W, 1860), (W, PH), (0, PH)], np.float32), GRASS, shade=(GRASS_D, 0, 14))
    for x in (150, 420, 1180, 1330):
        c.line([(x, 2120), (x + 18, 2080)], 4, taper=(0, 0)); c.line([(x + 30, 2125), (x + 40, 2085)], 4, taper=(0, 0))


def dragon(c, x, y, mood, arms_up=False):
    """body centre (x, y); head up and to the right"""
    c.shape(np.array([(x + 60, y - 160), (x + 520, y - 760), (x + 470, y - 520), (x + 600, y - 560),
                      (x + 500, y - 330), (x + 590, y - 330), (x + 300, y - 60)], np.float32), GRN_D)      # wing
    c.shape(np.array([(x - 250, y + 120), (x - 520, y + 260), (x - 640, y + 140), (x - 600, y + 330),
                      (x - 460, y + 380), (x - 200, y + 260)], np.float32), GRN, shade=(GRN_D, 8, 10))     # tail
    for k in range(5):                                                                                       # back spikes
        sx, sy = x - 220 + k * 90, y - 230 - k * 18
        c.shape(np.array([(sx - 34, sy + 20), (sx, sy - 60), (sx + 34, sy + 20)], np.float32), YELLOW)
    c.shape(E(x, y, 330, 260), GRN, shade=(GRN_D, 12, 12))                                                   # body
    c.shape(E(x - 30, y + 60, 200, 170), BELLY)
    c.shape(np.array([(x + 90, y - 180), (x + 160, y - 560), (x + 320, y - 560), (x + 280, y - 150)], np.float32), GRN)
    hx, hy = x + 230, y - 640
    for dx in (-90, 60):                                                                                     # horns
        c.shape(np.array([(hx + dx - 26, hy - 100), (hx + dx + 10, hy - 230), (hx + dx + 40, hy - 100)], np.float32), BELLY)
    c.shape(E(hx, hy, 190, 150), GRN, shade=(GRN_D, 10, 10))
    c.shape(E(hx - 170, hy + 50, 120, 82), GRN, shade=(GRN_D, 8, 8))                                         # snout
    c.dot(hx - 230, hy + 30, 9); c.dot(hx - 180, hy + 22, 9)
    c.face(hx + 20, hy - 10, 170, mood)
    for dx in (-170, 130):                                                                                   # legs
        c.shape(E(x + dx, y + 250, 90, 70), GRN, shade=(GRN_D, 8, 8))
    if arms_up:
        c.arm((x - 140, y - 120), (x - 330, y - 420), width=7, hand=34, glove=GRN)
        c.arm((x + 160, y - 120), (x + 420, y - 330), width=7, hand=34, glove=GRN)
    else:
        c.arm((x - 160, y - 40), (x - 60, y + 40), width=7, hand=30, glove=GRN)


def knight(c, x, y, torch=True, s=1.0):
    c.shape(R(x - 70 * s, y - 60 * s, x + 70 * s, y + 140 * s, 30), STEEL, shade=(STEEL_D, 8, 8))
    c.shape(R(x - 50 * s, y + 130 * s, x - 15 * s, y + 220 * s, 10), STEEL_D)
    c.shape(R(x + 15 * s, y + 130 * s, x + 50 * s, y + 220 * s, 10), STEEL_D)
    c.shape(E(x, y - 120 * s, 72 * s, 80 * s), STEEL, shade=(STEEL_D, 6, 6))
    c.ink_fill(R(x - 10 * s, y - 140 * s, x + 60 * s, y - 118 * s, 6))                                       # visor slit
    c.shape(np.array([(x - 10 * s, y - 196 * s), (x + 20 * s, y - 290 * s), (x + 30 * s, y - 196 * s)], np.float32), RED)
    if torch:
        c.arm((x + 50 * s, y), (x + 150 * s, y - 60 * s), width=6, hand=22, glove=STEEL)
        c.line([(x + 150 * s, y - 40 * s), (x + 190 * s, y - 200 * s)], 10, taper=(0, 0))
        c.burst(x + 195 * s, y - 250 * s, 50 * s, 70 * s, colour='#f28c28', spikes=9, depth=0.35)


def paint(work):
    out = Path(work); out.mkdir(parents=True, exist_ok=True)
    c = Cartoon(W, PH, seed=61, boil=2.0)
    scene(c)
    dragon(c, 840, 1560, 'smile')
    knight(c, 260, 1720)
    c.stage('field')
    for ax, ay, rot in ((560, 1880, 0.3), (640, 1900, -0.2), (1220, 1890, 0.15), (470, 1920, -0.35)):        # arrows
        P0 = (ax, ay); P1 = (ax + 150 * np.sin(rot), ay - 150 * np.cos(rot))
        c.line([P0, P1], 6, taper=(0, 0))
        c.shape(np.array([(P1[0] - 18, P1[1]), (P1[0], P1[1] - 30), (P1[0] + 18, P1[1])], np.float32), WHITE, width=4)
    c.shape(R(900, 1980, 1060, 2005, 6), STEEL)                                                             # broken sword
    c.shape(np.array([(1080, 2010), (1230, 1960), (1240, 1985), (1090, 2030)], np.float32), STEEL)
    c.shape(R(1060, 1965, 1080, 2040, 4), WOOD_D)
    c.shape(E(1180, 1150, 70, 66), '#9a9a9a', shade=('#707070', 8, 8))                                      # boulder
    c.pop_lines(1180, 1150, 90, 150, [200, 240, 280, 320])
    c.note('BONK', 1220, 1020, 76, anchor='m', colour=RED, rot=8)
    c.stage('tried')
    c.save(str(out / 'field.png'), stages_dir=str(out / 'field'))

    k = Cartoon(W, PH, seed=62, boil=2.0)
    scene(k)
    k.shape(R(560, 1700, 1140, 1760, 10), WOOD, shade=(WOOD_D, 6, 6))                                       # tiny chair seat
    for lx in (590, 1090):
        k.shape(R(lx - 16, 1750, lx + 16, 1990, 6), WOOD_D)
    k.shape(R(1080, 1360, 1130, 1720, 8), WOOD_D)
    dragon(k, 840, 1430, 'wow', arms_up=True)
    for dx, dy in ((-60, -980), (380, -900), (420, -760)):                                                  # sweat drops
        k.shape(E(840 + dx, 1430 + dy, 18, 30), '#8fd3f4', width=4)
    k.pop_lines(1070, 790, 230, 320, [300, 330, 20, 50])
    k.letter('EEEK!', 360, 860, 120, fill=YELLOW, anchor='m', rot=-6)
    sx, sy = 330, 2020                                                                                      # the spider
    for i in range(4):
        for side in (-1, 1):
            a = side * (0.5 + i * 0.32)
            k.line([(sx, sy), (sx + side * 70, sy - 40 + i * 25), (sx + side * 110, sy + 10 + i * 22)], 5, taper=(0, 0))
    k.shape(E(sx, sy, 48, 40), '#2b2b33')
    k.shape(E(sx, sy - 44, 30, 26), '#2b2b33')
    k.dot(sx - 10, sy - 50, 6, kind='flat'); k.dot(sx + 10, sy - 50, 6, kind='flat')
    knight(k, 1250, 1950, torch=False, s=0.8)
    k.stage('spider')
    k.shape(np.array([(sx - 34, sy - 70), (sx - 34, sy - 120), (sx - 14, sy - 92), (sx, sy - 130), (sx + 14, sy - 92),
                      (sx + 34, sy - 120), (sx + 34, sy - 70)], np.float32), YELLOW, width=4)               # crown
    k.sparkle(sx - 80, sy - 150, 26); k.sparkle(sx + 90, sy - 130, 20)
    k.letter('NEW HERO', 760, 2250, 100, fill=YELLOW, anchor='m', rot=-3)
    k.stage('hero')
    k.save(str(out / 'chair.png'), stages_dir=str(out / 'chair'))


A = ['field/00_field.png', 'field/01_tried.png']
B = ['chair/00_spider.png', 'chair/01_hero.png']

EPISODE = dict(
    chapter="The Dragon's Weakness",
    title="When the Dragon Has One Weird Weakness #shorts",
    description="Fire? Nothing. Swords? Nothing. A catapult? Bonk. Then the dragon saw it…\n\n"
                "An original animated story, drawn with code. Narration is synthetic.",
    tags=['animated story', 'funny story', 'dragon', 'knight', 'plot twist', 'cartoon', 'shorts'],
    voice='am_puck',
    lines=["The brave knight tried fire first.",
           "He tried swords. Arrows. A catapult.",
           "Nothing worked. The dragon just yawned.",
           "Then the dragon saw it, and screamed. A tiny spider.",
           "The kingdom has a new hero. It has eight legs.",
           "And the dragon? Still on the chair."],
    gaps=[0.15, 0.35, 0.4, 0.5, 0.5, 0.5],
    plates=[dict(stages=A, show=[(0, 0), ('L1:swords', 1)]),
            dict(stages=B, show=[(0, 0), ('L4', 1)])],
    camera=[(0, 720, 1300, 2440), ('L1', 720, 1300, 2440), ('L2', 720, 1290, 2400), ('L3', 720, PH + 1300, 2440),
            ('L4', 720, PH + 1300, 2440), ('END', 720, PH + 1290, 2400)],
    cards=[dict(at=0, until='END', text='When the dragon\nhas ONE weakness', font='AlfaSlabOne-400', size=78,
                paper=(255, 255, 255), ink=(20, 20, 20), tape=False, x=540, y=230, rot=0)],
    caption=dict(y=0.91),
    stamps=[dict(at='L3:spider', text='WEAKNESS FOUND', size=66, color=(200, 40, 30), x=470, y=1400, rot=-6)],
    music=dict(sections=[(0, 'L2', ['Dm9', 'Am9'], dict(bright=(0.25, 0.35), plucks=0.4)),
                         ('L2', 'L3', ['Esus', 'Am9'], dict(bright=(0.35, 0.45), pulse=True, ticks=True)),
                         ('L3', 'END', ['Fmaj7', 'Cmaj9'], dict(bright=(0.5, 0.3), gain=(1, 0.0), plucks=0.6))],
               events=[('L3:spider', 'impact', dict(level=0.5))]),
)
