"""Myth Dug Up #008 (news) — Senegal reinstated as 2025 Africa Cup of Nations champions by CAS.
Plates: a newspaper collage with a generic trophy, ransom letters and score labels (newscollage), and a blueprint of the
pitch with the walk-off and the three rulings as a timeline (blueprint).
Facts (BBC Sport Africa 24 Nov 2026, via Yahoo Sports; Reuters, The Athletic/NYT, Al Jazeera coverage):
- Final, Rabat, January 2026: Senegal beat Morocco 1-0 after extra time (Pape Gueye).
- At 0-0 in stoppage time Senegal walked off in protest at a penalty for Morocco; delay of more than 15 minutes; the penalty was saved.
- March 2026: CAF appeals board ruled Senegal forfeited and awarded Morocco a 3-0 win.
- 24 Nov 2026: CAS (three arbitrators, unanimous) upheld Senegal's appeal, restored the result: restarting play was within the
  referee's sole authority ("field of play"). CAF says it will implement the award.
- Morocco's federation (FRMF) says it will pursue all legal avenues; a challenge at the Swiss Federal Tribunal is possible.
Facts as of 25 Nov 2026."""
from pathlib import Path
import numpy as np
from newscollage import NewsCollage, Photo, RED, INK, MUSTARD
from blueprint import Blueprint

W, H = 1440, 2560


def trophy_photo():
    p = Photo(620, 900, seed=8)
    # base
    p.poly([(150, 820), (470, 820), (430, 700), (190, 700)], height=30, bevel=6, albedo=0.25, metal=0.2, gloss=0.5)
    p.poly([(200, 700), (420, 700), (390, 640), (230, 640)], z=20, height=20, bevel=5, albedo=0.7, metal=1.0, gloss=0.5)
    # stem
    p.rod((310, 640), (310, 470), 34, z=20, albedo=0.85, metal=1.0)
    p.disc(310, 520, 58, z=40, height=14, albedo=0.85, metal=1.0)
    # cup + handles
    p.ring(150, 260, 52, 82, z=30, albedo=0.85, metal=1.0)
    p.ring(470, 260, 52, 82, z=30, albedo=0.85, metal=1.0)
    p.dome(310, 260, 175, 210, z=40, height=80, cut=1.0, albedo=0.88, metal=1.0, gloss=0.5)
    p.poly([(120, 150), (500, 150), (500, 185), (120, 185)], z=60, height=26, bevel=8, albedo=0.88, metal=1.0)
    p.dome(310, 120, 60, 40, z=70, height=30, albedo=0.88, metal=1.0)
    p.glare(250, 300, 40, 140, 200, 260, strength=0.4)
    return p


def paint_collage(out):
    nc = NewsCollage(W, H, seed=81)
    nc.board()
    for (w, h, x, y, r, sides) in ((980, 1300, 470, 720, -4, 'rb'), (900, 1200, 1010, 1650, 5, 'lt'), (800, 900, 420, 2150, -2, 'rt')):
        s = nc.newsprint(w, h, columns=3); s.tear(sides); nc.paste(s, x, y, rot=r)
    nc.stage('board')
    nc.disc(720, 1020, 520, RED)
    s = nc.print_photo(trophy_photo()); s.cutout(14); nc.paste(s, 720, 1060, rot=-4)
    nc.stage('trophy')
    nc.ransom('CHAMPIONS?', 100, 300, 118, rot=2)
    nc.tape(240, 240, 200, rot=-12); nc.tape(1260, 210, 200, rot=10)
    nc.stage('ransom')
    nc.label('JAN · FINAL: SENEGAL 1–0', 170, 1640, 58, face='typewriter_bold', rot=3)
    nc.stage('jan')
    nc.label('MARCH · CAF: MOROCCO 3–0', 150, 1830, 58, face='typewriter_bold', fg='knock', block=INK, rot=-2)
    nc.stage('march')
    nc.label('NOV 24 · CAS: SENEGAL', 190, 2020, 64, face='typewriter_bold', block=MUSTARD, rot=2)
    nc.tape(220, 2010, 160, rot=70)
    nc.stage('nov')
    nc.save(str(out / 'collage.png'), stages_dir=str(out / 'collage'))


def paint_pitch(out):
    bp = Blueprint(W, H, seed=82)
    bp.border(50, 50, W - 50, H - 50, zones=(4, 8), size=18)
    bp.text('AFRICA CUP FINAL · RABAT', W / 2, 260, 52, 'ms', pen=2.2, spacing=0.2)
    bp.text('STOPPAGE TIME · SCORE 0–0', W / 2, 325, 28, 'ms')
    # half pitch, goal at top
    x0, x1, y0, y1 = 220, 1220, 420, 1250
    bp.box(x0, y0, x1, y1, 'heavy')
    bp.box(440, y0, 1000, 660, 'thick'); bp.box(580, y0, 860, 505, 'medium')
    bp.box(640, y0 - 40, 800, y0, 'thick')
    bp.dot(720, 580, 9)
    bp.arc(720, 580, 130, 40, 140, 'medium')
    bp.arc(720, y1, 130, 180, 360, 'medium')
    bp.stage('sheet')
    bp.leader([(728, 575), (980, 540), (1120, 540)], 'PENALTY', size=26)
    bp.stage('penalty')
    # players walking off to the tunnel (right side)
    pts = [(560, 760), (700, 830), (860, 800), (620, 950), (900, 990), (760, 1090)]
    for (x, y) in pts:
        bp.circle(x, y, 22, 'thick')
    bp.stage('players')
    for (x, y) in pts:
        bp.dashed([(x + 20, y), (1150, 1130), (1300, 1130)], 'thin')
    bp.box(1240, 1070, 1330, 1190, 'thick')
    bp.text('TUNNEL', 1285, 1235, 24, 'ms')
    bp.arrowhead((1300, 1130), (1, 0), 16)
    bp.dim((260, 1310), (1180, 1310), 0, 'WALK-OFF · 15+ MIN', size=30)
    bp.stage('walkoff')
    # timeline of rulings
    bp.view_title(720, 1450, 'THREE RULINGS', size=34)
    rows = (('JAN 2026', 'FINAL', 'SENEGAL 1–0'), ('MAR 2026', 'CAF APPEALS', 'MOROCCO 3–0'), ('24 NOV 2026', 'CAS · 3 JUDGES', 'SENEGAL'))
    bx, by = 150, 1510
    bp.table(bx, by, [360, 400, 380], [110, 110, 110], pen='thin', outer='heavy')
    for i, (a, b, c) in enumerate(rows):
        yy = by + i * 110 + 70
        bp.text(a, bx + 20, yy, 30, 'ls', pen=1.6)
        bp.text(b, bx + 380, yy, 30, 'ls', pen=1.6)
        bp.text(c, bx + 780, yy, 34, 'ls', pen=2.0)
        bp.stage('row%d' % i)
    bp.red([(bx + 770, by + 175), (bx + 1120, by + 160)], width=5)
    bp.cloud([(bx + 760, by + 230), (bx + 1130, by + 230), (bx + 1130, by + 325), (bx + 760, by + 325)])
    bp.red_text('UNANIMOUS', 860, 1930, 44, rot=3)
    bp.stage('ruling')
    bp.text('NEXT? SWISS FEDERAL TRIBUNAL', W / 2, 2060, 30, 'ms')
    bp.stage('next')
    bp.fold(xs=(720,), ys=(1280,), wear=0.7)
    bp.stain(1200, 2300, 80, 0.6)
    bp.save(str(out / 'pitch.png'), str(out / 'pitch'))


def paint(work):
    out = Path(work); out.mkdir(parents=True, exist_ok=True)
    paint_collage(out)
    paint_pitch(out)


PH = 2560
C = ['collage/%s.png' % n for n in ('00_board', '01_trophy', '02_ransom', '03_jan', '04_march', '05_nov', '06_final')]
P = ['pitch/%s.png' % n for n in ('00_sheet', '01_penalty', '02_players', '03_walkoff', '04_row0', '05_row1', '06_row2', '07_ruling', '08_next', '09_final')]

EPISODE = dict(
    chapter='Senegal vs CAF',
    title="Senegal Lost Its Africa Cup Title. A Court Just Gave It Back. #shorts",
    description=("In January Senegal beat Morocco 1-0 in the Africa Cup of Nations final in Rabat - after walking off the pitch for "
                 "more than 15 minutes in protest at a penalty. In March, CAF's appeals board ruled Senegal had forfeited and "
                 "awarded Morocco a 3-0 win. On 24 November the Court of Arbitration for Sport (CAS) unanimously overturned that: "
                 "restarting the match was the referee's call alone. Morocco's federation says it will pursue all legal avenues.\n\n"
                 "Proven: CAS restored the 1-0 result - Senegal are the 2025 AFCON champions; CAF says it will implement the award.\n"
                 "Debated: whether Morocco can still overturn it, e.g. at the Swiss Federal Tribunal.\n\n"
                 "Sources: BBC Sport, Reuters, The Athletic (NYT), Al Jazeera, CAS statement.\n"
                 "Illustrations painted with code (no photos), narration is synthetic. Facts as of 25 Nov 2026."),
    tags=['senegal', 'morocco', 'afcon', 'africa cup of nations', 'cas', 'court of arbitration for sport', 'caf', 'football news',
          'sports news', 'news'],
    voice='bm_george',
    lines=["Senegal's trophy was taken away.",
           "In January, Senegal won the Africa Cup final, one-nil. Then African football's appeals board handed Morocco a three-nil win.",
           "On Tuesday, the Court of Arbitration for Sport overturned it. Unanimously.",
           "Senegal had walked off for over fifteen minutes. But restarting was the referee's call alone, the court ruled.",
           "Proven: Senegal are champions again. Debated: whether Morocco, which vows to fight on, can still overturn it in a Swiss court."],
    gaps=[0.15, 0.35, 0.4, 0.4, 0.45],
    display=[(1, 'one-nil.', '1–0.'), (1, 'three-nil', '3–0'), (3, 'fifteen', '15')],
    plates=[dict(stages=C, show=[(0, 2), ('L1:senegal', 3), ('L1:appeals', 4), ('L2:court', 5), ('L2.end', 6)]),
            dict(stages=P, show=[(0, 2), ('L3:walked', 3), ('L3.end-0.6', 4), ('L3.end-0.3', 5), ('L3.end', 6), ('L4:proven', 7),
                                 ('L4:morocco', 8), ('L4:swiss', 9)])],
    camera=[(0, 720, 1100, 2150), ('L0.end', 720, 1080, 2000), ('L1+0.3', 690, 1620, 1820), ('L1:appeals', 690, 1640, 1800),
            ('L2', 690, 1640, 1820), ('L2.end-0.2', 700, 1620, 1860),
            ('L3-0.1', 720, PH + 900, 1780), ('L3:referee', 720, PH + 960, 1900), ('L3.end-0.4', 720, PH + 1480, 2140),
            ('L4:debated', 720, PH + 1460, 2180), ('END', 720, PH + 1300, 2450)],
    cards=[dict(at=0, until='L1-0.1', text='TITLE STRIPPED', font='AlfaSlabOne-400', size=96, ink=(160, 32, 24), x=540, y=1770, rot=-3),
           dict(at='L1:three', until='L2-0.1', text='MOROCCO 3–0', font='AlfaSlabOne-400', size=84, x=540, y=320, rot=2),
           dict(at='L2:court', until='L3-0.1', text='CAS: OVERTURNED', font='AlfaSlabOne-400', size=84, ink=(30, 70, 52), x=540, y=330, rot=-2),
           dict(at='L3:walked', until='L3:referee', text='15+ MIN WALK-OFF', size=70, x=540, y=1770, rot=2),
           dict(at='L3:referee', until='L3.end-0.4', text="REFEREE'S CALL", size=78, x=540, y=1770, rot=-2)],
    stamps=[dict(at='L4:proven', text='PROVEN', size=100, color=(30, 70, 52), x=540, y=380, rot=-6),
            dict(at='L4:debated', text='DEBATED', size=100, color=(160, 32, 24), x=560, y=600, rot=5)],
    music=dict(sections=[(0, 'L1', ['Dm9', 'Am9'], dict(bright=(0.3, 0.4), pulse=True)),
                         ('L1', 'L2', ['Esus', 'Dm9'], dict(bright=(0.4, 0.55), pulse=True, ticks=True)),
                         ('L2', 'L4', ['Fmaj7', 'Esus'], dict(bright=(0.5, 0.65), gain=(1, 1.1), pulse=True, ticks=True)),
                         ('L4', 'END', ['Am9', 'Fmaj7'], dict(bright=(0.5, 0.3), gain=(1, 0.0), plucks=0.4))]),
)
