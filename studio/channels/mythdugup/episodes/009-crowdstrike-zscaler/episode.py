"""Myth Dug Up #009 (news) — CrowdStrike agrees to buy Zscaler in an all-stock deal.
Plates: a two-colour wood-type poster with two merging shields (letterpress), and a merger schematic with the exchange
ratio, a revenue bar chart and the open approvals (blueprint). No logos, generic shields only.
Facts (joint press release / SEC Form 8-K Ex. 99.1 and CrowdStrike Q3 FY2027 release, both 23 Nov 2026; business press):
- Announced Monday 23 Nov 2026; boards of both companies approved unanimously; all-stock.
- Values Zscaler at about $43.9 billion; 1.135 CrowdStrike shares per Zscaler share = about $260.41 per share,
  about a 34% premium to Zscaler's 20 Nov close.
- Combined ARR expected above $10 billion at close (CrowdStrike ending ARR $6.26B; Zscaler $3.9B).
- Zscaler protects about 50% of the Fortune 500. Targets: ~$1B annual run-rate revenue synergies within 30 months,
  $500M cost synergies (company projections).
- Still needs Zscaler shareholder approval and regulatory approvals; expected close in 2H of CrowdStrike fiscal 2028.
Facts as of 25 Nov 2026."""
from pathlib import Path
import numpy as np
from letterpress import Letterpress, RED, BLACK
from blueprint import Blueprint

W, H = 1440, 2560


def shield(lp, cx, cy, w, h):
    pts = [(cx - w / 2, cy - h / 2), (cx + w / 2, cy - h / 2), (cx + w / 2, cy - h * 0.05)]
    for t in np.linspace(0, 1, 12)[1:]:
        pts.append((cx + w / 2 * (1 - t) ** 1.3, cy - h * 0.05 + h * 0.55 * np.sin(t * np.pi / 2)))
    for t in np.linspace(0, 1, 12)[1:]:
        pts.append((cx - w / 2 * t ** 1.3, cy + h / 2 - h * 0.55 * (1 - np.cos(t * np.pi / 2))))
    return lp.poly(pts)


def press(lp, name):
    lp.press(RED); lp.press(BLACK); lp.stage(name)


def paint_poster(out):
    lp = Letterpress(W, H, seed=91)
    lp.paper()
    lp.border(60, 60, W - 60, H - 60, weight=5)
    lp.stage('paper')
    lp.type_line('CROWDSTRIKE', 120, W - 120, 330, 170, face='clarendon', ink=BLACK, shade=(8, 6, RED, 3))
    lp.type_line('BUYS', 420, W - 420, 520, 130, face='gothic', ink=RED)
    lp.type_line('ZSCALER', 140, W - 140, 790, 220, face='clarendon', ink=BLACK, shade=(8, 6, RED, 3))
    press(lp, 'names')
    a = shield(lp, 560, 1330, 520, 640)
    b = shield(lp, 880, 1330, 520, 640)
    lp.tint(b, ink=RED)
    lp.key(a, width=5, heavy=10); lp.hatch(a, angle=35, spacing=11)
    lp.clear(a * 0 + b, ink=BLACK)
    lp.key(b, width=5, heavy=10)
    press(lp, 'shields')
    lp.rule(140, W - 140, 1820, kind='double', weight=4)
    lp.type_line('$43.9', 170, W - 170, 2150, 300, face='clarendon', ink=RED, shade=(10, 8, BLACK, 4))
    lp.type_line('BILLION', 200, W - 200, 2360, 170, face='gothic', ink=BLACK)
    press(lp, 'price')
    lp.type_line('ALL STOCK  ·  34% PREMIUM', 200, W - 200, 2460, 52, face='gothic', ink=BLACK)
    press(lp, 'terms')
    lp.fold('h', 1280, depth=0.7); lp.tone_edges(); lp.foxing(n=90); lp.tack(110, 110); lp.tack(W - 110, 110)
    lp.stage('aged')
    lp.save(str(out / 'poster.png'), stages_dir=str(out / 'poster'))


def paint_schematic(out):
    bp = Blueprint(W, H, seed=92)
    bp.border(50, 50, W - 50, H - 50, zones=(4, 8), size=18)
    bp.text('MERGER SCHEMATIC', W / 2, 190, 56, 'ms', pen=2.2, spacing=0.2)
    bp.text('ANNOUNCED 23 NOV 2026 · ALL-STOCK', W / 2, 250, 28, 'ms')
    bp.stage('sheet')
    o = 520                                     # vertical offset of the ratio block
    bp.box(170, 340 + o, 540, 590 + o, 'heavy'); bp.text('1 ZS', 355, 460 + o, 54, 'ms', pen=2.0); bp.text('SHARE', 355, 530 + o, 30, 'ms')
    bp.line([(560, 465 + o), (870, 465 + o)], 'thick'); bp.arrowhead((880, 465 + o), (1, 0), 18)
    bp.text('× 1.135', 715, 430 + o, 40, 'ms', pen=1.8)
    bp.box(900, 340 + o, 1270, 590 + o, 'heavy'); bp.text('1.135', 1085, 460 + o, 54, 'ms', pen=2.0); bp.text('CRWD SHARES', 1085, 530 + o, 30, 'ms')
    bp.text('ABOUT USD 260 PER ZS SHARE  ·  +34%', W / 2, 690 + o, 34, 'ms', pen=1.6)
    bp.stage('ratio')
    bp.view_title(720, 1340, 'ANNUAL RECURRING REVENUE', size=32)
    base, k = 2250, 70
    bars = ((260, 520, 6.26, 'CRWD', 'USD 6.3B'), (590, 850, 3.9, 'ZS', 'USD 3.9B'))
    for x0, x1, v, lab, val in bars:
        bp.box(x0, base - v * k, x1, base, 'thick')
        bp.hatch([[(x0, base - v * k), (x1, base - v * k), (x1, base), (x0, base)]], angle=45, spacing=12)
        bp.text(lab, (x0 + x1) / 2, base + 50, 30, 'ms'); bp.text(val, (x0 + x1) / 2, base - v * k - 20, 32, 'ms', pen=1.6)
    bp.ground([(200, base), (1260, base)])
    bp.stage('bars')
    x0, x1 = 940, 1200
    bp.box(x0, base - 6.26 * k, x1, base, 'thick'); bp.box(x0, base - 10.16 * k, x1, base - 6.26 * k, 'thick')
    bp.hatch([[(x0, base - 10.16 * k), (x1, base - 10.16 * k), (x1, base - 6.26 * k), (x0, base - 6.26 * k)]], angle=-45, spacing=10)
    bp.text('COMBINED', (x0 + x1) / 2, base + 50, 30, 'ms')
    bp.red_text('> $10B', 980, base - 10.16 * k - 30, 50, rot=3)
    bp.stage('combined')
    bx, by = 150, 330
    bp.table(bx, by, [700, 440], [100, 100, 100], pen='thin', outer='heavy')
    rows = (('FORTUNE 500 USING ZS', 'ABOUT 50%'), ('REVENUE TARGET / YR', 'USD 1B'), ('STILL NEEDED', 'VOTE + REGULATORS'))
    for i, (a, v) in enumerate(rows):
        yy = by + i * 100 + 64
        bp.text(a, bx + 24, yy, 32, 'ls', pen=1.6)
        bp.text(v, bx + 720, yy, 28 if i == 2 else 38, 'ls', pen=2.0)
        bp.stage('row%d' % i)
    bp.cloud([(bx + 705, by + 210), (bx + 1135, by + 210), (bx + 1135, by + 296), (bx + 705, by + 296)])
    bp.red_text('CLOSE: 2H FISCAL 2028', 760, 710, 40, rot=2)
    bp.stage('open')
    bp.fold(xs=(720,), ys=(1280,), wear=0.7)
    bp.stain(260, 2420, 70, 0.6)
    bp.save(str(out / 'schematic.png'), str(out / 'schematic'))


def paint(work):
    out = Path(work); out.mkdir(parents=True, exist_ok=True)
    paint_poster(out)
    paint_schematic(out)


PH = 2560
A = ['poster/%s.png' % n for n in ('00_paper', '01_names', '02_shields', '03_price', '04_terms', '05_aged', '06_final')]
B = ['schematic/%s.png' % n for n in ('00_sheet', '01_ratio', '02_bars', '03_combined', '04_row0', '05_row1', '06_row2', '07_open', '08_final')]

EPISODE = dict(
    chapter='CrowdStrike + Zscaler',
    title="CrowdStrike Is Buying Its Rival Zscaler for $43.9 Billion #shorts",
    description=("On Monday, 23 November, cybersecurity company CrowdStrike agreed to buy its rival Zscaler in an all-stock deal "
                 "that values Zscaler at about $43.9 billion (nearly $44 billion). Each Zscaler share becomes 1.135 CrowdStrike shares - about $260.41, "
                 "a 34% premium. Together the companies expect more than $10 billion in annual recurring revenue at closing. "
                 "Zscaler says it protects about half of the Fortune 500; CrowdStrike targets about $1 billion a year in revenue "
                 "synergies.\n\n"
                 "Proven: both boards unanimously approved the deal (joint announcement, SEC filing).\n"
                 "Debated: whether Zscaler shareholders and regulators sign off (closing expected in the second half of "
                 "CrowdStrike's fiscal 2028), and whether the promised synergies materialise.\n\n"
                 "Sources: CrowdStrike/Zscaler joint press release and SEC Form 8-K (23 Nov 2026), business press coverage.\n"
                 "Illustrations painted with code (no photos), narration is synthetic. Facts as of 25 Nov 2026. Not financial advice."),
    tags=['crowdstrike', 'zscaler', 'merger', 'acquisition', 'cybersecurity', 'tech news', 'business news', 'stocks', 'news'],
    voice='bm_george',
    lines=["Two cyber rivals just became one.",
           "On Monday, CrowdStrike agreed to buy Zscaler, in a stock deal worth nearly forty-four billion dollars.",
           "Zscaler holders get about a third more than Friday's price. Together, they expect over ten billion dollars in yearly recurring revenue.",
           "Zscaler says it protects half the Fortune five hundred. CrowdStrike is targeting a billion a year in extra sales.",
           "Proven: both boards approved it. Debated: whether shareholders and regulators will, and whether those gains are real."],
    gaps=[0.15, 0.35, 0.4, 0.4, 0.45],
    display=[(1, 'forty-four', '$44'), (1, 'dollars.', ''), (2, 'ten', '$10'), (2, 'dollars', ''), (3, 'five', '500.'), (3, 'hundred.', '')],
    plates=[dict(stages=A, show=[(0, 3), ('L1:crowdstrike', 4), ('L1.end', 6)]),
            dict(stages=B, show=[(0, 1), ('L2:together-0.2', 2), ('L2:together+0.4', 3), ('L3-0.2', 4),
                                 ('L3:crowdstrike', 5), ('L4:debated', 6), ('L4:shareholders', 7), ('L4:gains', 8)])],
    camera=[(0, 720, 1180, 2300), ('L0.end', 720, 1250, 2350), ('L1+0.2', 720, 1400, 2300), ('L1:worth', 720, 1900, 1300),
            ('L1.end', 720, 1900, 1250), ('L2-0.1', 720, PH + 1250, 2000), ('L2:together-0.3', 720, PH + 1250, 2050),
            ('L2:together+0.2', 720, PH + 1500, 2100), ('L2.end', 720, PH + 1480, 2140), ('L3-0.1', 720, PH + 1150, 2300),
            ('L4', 720, PH + 1150, 2300), ('END', 720, PH + 1280, 2500)],
    cards=[dict(at=0, until='L1-0.1', text='RIVALS MERGE', font='AlfaSlabOne-400', size=100, ink=(160, 32, 24), x=540, y=720, rot=-3),
           dict(at='L1:worth', until='L2-0.1', text='$43.9 BILLION', font='AlfaSlabOne-400', size=88, x=540, y=330, rot=2),
           dict(at='L2', until='L2:together-0.3', text='+34% PREMIUM', font='AlfaSlabOne-400', size=88, ink=(160, 32, 24), x=540, y=1770, rot=-2),
           dict(at='L3:zscaler', until='L3:crowdstrike', text='HALF THE FORTUNE 500', size=64, x=540, y=1770, rot=-2),
           dict(at='L3:crowdstrike', until='L4-0.1', text='TARGET: $1B / YEAR', size=64, x=540, y=1770, rot=2)],
    stamps=[dict(at='L4:proven', text='PROVEN', size=100, color=(30, 70, 52), x=540, y=1000, rot=-6),
            dict(at='L4:debated', text='DEBATED', size=100, color=(160, 32, 24), x=560, y=1210, rot=5)],
    music=dict(sections=[(0, 'L1', ['Dm9', 'Am9'], dict(bright=(0.3, 0.45), pulse=True)),
                         ('L1', 'L2', ['Esus', 'Dm9'], dict(bright=(0.45, 0.6), pulse=True, ticks=True)),
                         ('L2', 'L4', ['Fmaj7', 'Esus'], dict(bright=(0.5, 0.65), gain=(1, 1.1), pulse=True, ticks=True)),
                         ('L4', 'END', ['Am9', 'Fmaj7'], dict(bright=(0.5, 0.3), gain=(1, 0.0), plucks=0.4))]),
)
