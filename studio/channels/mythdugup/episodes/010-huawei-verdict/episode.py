"""Myth Dug Up #010 (news) — A U.S. federal jury convicts Huawei on 10 of 12 counts.
Plates: a two-colour wood-type poster with a generic judge's gavel (letterpress), and a verdict sheet with the charge
list and a timeline (blueprint). No logos, no likeness.
Facts (CNN, CNBC, Time, Fox Business with Reuters, The Next Web, 24-25 Nov 2026; Huawei statement; Chinese foreign ministry):
- Verdict Tuesday 24 Nov 2026, U.S. District Court for the Eastern District of New York (Brooklyn), after a ~3-month trial.
- Huawei Technologies and three subsidiaries convicted on 10 of 12 counts: bank fraud, wire fraud, money-laundering
  conspiracy, conspiracy to steal trade secrets, IEEPA (Iran sanctions) violations.
- Acquitted of racketeering conspiracy and conspiracy to obstruct justice.
- Prosecutors: Huawei hid its Iran business (via Skycom) from banks; targeted technology at T-Mobile, Cisco, CNEX,
  Quintel, Fujitsu.
- Huawei: remaining convictions "equally without legal or factual merit", will take all necessary legal actions.
  China's foreign ministry "firmly opposes" U.S. suppression of Chinese companies.
- Sentencing scheduled for 14 Sept 2027; fines, forfeiture, restitution possible. Case public since CFO's Dec 2018
  arrest in Canada; charges unsealed Jan 2019.
Facts as of 26 Nov 2026."""
from pathlib import Path
import math
from letterpress import Letterpress, RED, BLACK
from blueprint import Blueprint

W, H = 1440, 2560


def rrect(cx, cy, L, h, ang):
    c, s = math.cos(math.radians(ang)), math.sin(math.radians(ang))
    pts = []
    for dx, dy in ((-L / 2, -h / 2), (L / 2, -h / 2), (L / 2, h / 2), (-L / 2, h / 2)):
        pts.append((cx + dx * c - dy * s, cy + dx * s + dy * c))
    return pts


def press(lp, name):
    lp.press(RED); lp.press(BLACK); lp.stage(name)


def paint_poster(out):
    lp = Letterpress(W, H, seed=101)
    lp.paper()
    lp.border(60, 60, W - 60, H - 60, weight=5)
    lp.stage('paper')
    lp.type_line('U.S. JURY VERDICT', 300, W - 300, 250, 80, face='gothic', ink=RED)
    lp.type_line('HUAWEI', 140, W - 140, 560, 260, face='clarendon', ink=BLACK, shade=(8, 6, RED, 3))
    lp.rule(140, W - 140, 650, kind='double', weight=4)
    lp.type_line('10 OF 12', 170, W - 170, 940, 250, face='clarendon', ink=RED, shade=(10, 8, BLACK, 4))
    lp.type_line('COUNTS: GUILTY', 180, W - 180, 1100, 110, face='gothic', ink=BLACK)
    press(lp, 'names')
    # sound block
    blk = lp.rect(330, 1960, 1110, 2080)
    lp.tint(blk, ink=RED)
    lp.key(blk, width=5, heavy=10)
    # gavel: handle, then head
    ang = -28
    hx, hy = 640, 1520
    c, s = math.cos(math.radians(ang)), math.sin(math.radians(ang))
    # handle runs perpendicular to the head, down-right
    px, py = -s, c
    hc = (hx + px * 360, hy + py * 360)
    handle = lp.poly(rrect(hc[0], hc[1], 70, 640, ang + 0))
    lp.key(handle, width=5, heavy=10); lp.hatch(handle, angle=60, spacing=10)
    head = lp.poly(rrect(hx, hy, 620, 250, ang))
    lp.clear(head, ink=BLACK)
    lp.key(head, width=5, heavy=11); lp.hatch(head, angle=35, spacing=11)
    for d in (-230, 230):
        band = lp.poly(rrect(hx + c * d, hy + s * d, 40, 270, ang))
        lp.solid(band, ink=BLACK)
    press(lp, 'gavel')
    lp.rule(140, W - 140, 2250, kind='double', weight=4)
    press(lp, 'counts')
    lp.type_line('BROOKLYN  ·  24 NOV 2026', 260, W - 260, 2390, 54, face='gothic', ink=BLACK)
    press(lp, 'terms')
    lp.fold('h', 1280, depth=0.7); lp.tone_edges(); lp.foxing(n=90); lp.tack(110, 110); lp.tack(W - 110, 110)
    lp.stage('aged')
    lp.save(str(out / 'poster.png'), stages_dir=str(out / 'poster'))


def paint_sheet(out):
    bp = Blueprint(W, H, seed=102)
    bp.border(50, 50, W - 50, H - 50, zones=(4, 8), size=18)
    bp.text('VERDICT SHEET', W / 2, 190, 58, 'ms', pen=2.2, spacing=0.2)
    bp.text('U.S. V. HUAWEI · BROOKLYN · 24 NOV 2026', W / 2, 250, 28, 'ms')
    bp.stage('sheet')
    bx, by, rh = 150, 330, 110
    rows = (('BANK FRAUD', 'GUILTY'), ('WIRE FRAUD', 'GUILTY'), ('MONEY LAUNDERING CONSP.', 'GUILTY'),
            ('TRADE SECRETS CONSP.', 'GUILTY'), ('IRAN SANCTIONS (IEEPA)', 'GUILTY'),
            ('RACKETEERING CONSP.', 'CLEARED'), ('OBSTRUCTION CONSP.', 'CLEARED'))
    bp.table(bx, by, [780, 360], [rh] * len(rows), pen='thin', outer='heavy')
    for i, (a, v) in enumerate(rows[:5]):
        yy = by + i * rh + 72
        bp.text(a, bx + 24, yy, 34, 'ls', pen=1.6)
        bp.text(v, bx + 800, yy, 40, 'ls', pen=2.2)
    bp.stage('guilty')
    bp.box(150, 1150, 1290, 1290, 'thick')
    bp.text('TECH TARGETED, PER PROSECUTORS:', W / 2, 1205, 30, 'ms')
    bp.text('T-MOBILE · CISCO · FUJITSU · OTHERS', W / 2, 1262, 38, 'ms', pen=1.8)
    bp.stage('targets')
    for i, (a, v) in enumerate(rows[5:], start=5):
        yy = by + i * rh + 72
        bp.text(a, bx + 24, yy, 34, 'ls', pen=1.6)
        bp.red_text(v, bx + 800, yy - 8, 40, rot=0)
    bp.cloud([(bx + 10, by + 5 * rh + 8), (bx + 1130, by + 5 * rh + 8), (bx + 1130, by + 7 * rh - 8), (bx + 10, by + 7 * rh - 8)])
    bp.stage('cleared')
    x = 300
    pts = ((1450, 'DEC 2018', 'CFO ARRESTED IN CANADA'), (1680, 'JAN 2019', 'U.S. CHARGES UNSEALED'),
           (1910, 'NOV 2026', 'JURY VERDICT'))
    bp.view_title(720, 1380, 'TIMELINE', size=32)
    bp.line([(x, 1420), (x, 2330)], 'thick')
    for k, (y, d, t) in enumerate(pts):
        bp.box(x - 18, y - 18, x + 18, y + 18, 'heavy')
        bp.text(d, x + 60, y - 6, 44, 'ls', pen=2.0)
        bp.text(t, x + 60, y + 46, 32, 'ls', pen=1.5)
        bp.stage('t%d' % k)
    y = 2170
    bp.box(x - 18, y - 18, x + 18, y + 18, 'heavy')
    bp.red_text('14 SEPT 2027', x + 60, y - 6, 52, rot=2)
    bp.text('SENTENCING (FINES, FORFEITURE)', x + 60, y + 52, 32, 'ls', pen=1.5)
    bp.stage('sentencing')
    bp.fold(xs=(720,), ys=(1280,), wear=0.7)
    bp.stain(1220, 2420, 70, 0.6)
    bp.save(str(out / 'sheet.png'), str(out / 'sheet'))


def paint(work):
    out = Path(work); out.mkdir(parents=True, exist_ok=True)
    paint_poster(out)
    paint_sheet(out)


PH = 2560
A = ['poster/%s.png' % n for n in ('00_paper', '01_names', '02_gavel', '03_counts', '04_terms', '05_aged', '06_final')]
B = ['sheet/%s.png' % n for n in ('00_sheet', '01_guilty', '02_targets', '03_cleared', '04_t0', '05_t1', '06_t2',
                                  '07_sentencing', '08_final')]

EPISODE = dict(
    chapter='U.S. v. Huawei',
    title="Huawei Was Just Found Guilty in a U.S. Court. 10 of 12 Counts. #shorts",
    description=("On Tuesday, 24 November, a federal jury in Brooklyn convicted Huawei and three subsidiaries on 10 of 12 counts "
                 "after a roughly three-month trial - including bank fraud, wire fraud, money-laundering conspiracy, conspiracy "
                 "to steal trade secrets and Iran sanctions violations. Prosecutors said Huawei hid its Iran business from banks and "
                 "targeted technology at companies such as T-Mobile and Cisco. The jury acquitted Huawei of racketeering conspiracy "
                 "and obstruction conspiracy. Huawei called the remaining convictions without legal or factual merit; China's "
                 "foreign ministry said it firmly opposes the case. Sentencing is set for 14 September 2027.\n\n"
                 "Proven: a U.S. jury convicted Huawei on 10 of 12 counts (court verdict).\n"
                 "Debated: whether the verdict survives Huawei's legal challenges, and what penalty the court imposes.\n\n"
                 "Sources: CNN, CNBC, Reuters, Time, Fox Business; Huawei statement; Chinese foreign ministry.\n"
                 "Illustrations painted with code (no photos), narration is synthetic. Facts as of 26 Nov 2026."),
    tags=['huawei', 'huawei verdict', 'huawei trial', 'trade secrets', 'iran sanctions', 'china', 'us china', 'court',
          'tech news', 'news'],
    voice='bm_george',
    lines=["Tech giant Huawei was just found guilty.",
           "A jury in Brooklyn convicted the Chinese tech giant on ten of twelve counts, including bank fraud and conspiracy to steal trade secrets.",
           "Prosecutors said it hid its business in Iran from banks, and targeted technology at T-Mobile, Cisco and others.",
           "The jury cleared it of racketeering. Huawei calls the rest without merit, and China says it firmly opposes the case.",
           "Proven: a U.S. jury convicted the company. Debated: whether it holds up. Sentencing is set for September twenty twenty-seven."],
    gaps=[0.15, 0.35, 0.4, 0.4, 0.45],
    display=[(1, 'ten', '10'), (1, 'twelve', '12'), (4, 'twenty', '2027.'), (4, 'twenty-seven.', '')],
    plates=[dict(stages=A, show=[(0, 3), ('L1:ten', 4), ('L1.end', 6)]),
            dict(stages=B, show=[(0, 1), ('L2:targeted', 2), ('L3', 3), ('L3:huawei', 4), ('L3:china', 6),
                                 ('L4:sentencing', 7), ('L4:sentencing+0.4', 8)])],
    camera=[(0, 720, 1180, 2300), ('L0.end', 720, 1230, 2350), ('L1+0.2', 720, 1150, 2200), ('L1:ten', 720, 1050, 2100),
            ('L1.end', 720, 1080, 2160), ('L2-0.1', 720, PH + 1100, 2150), ('L2:targeted', 720, PH + 1120, 2180),
            ('L3', 720, PH + 1100, 2150), ('L3:huawei', 720, PH + 1460, 2150), ('L4', 720, PH + 1440, 2200),
            ('END', 720, PH + 1300, 2450)],
    cards=[dict(at=0, until='L1-0.1', text='FOUND GUILTY', font='AlfaSlabOne-400', size=100, ink=(160, 32, 24), x=540, y=1830, rot=-3),
           dict(at='L1:trade', until='L1.end', text='TRADE SECRETS', font='AlfaSlabOne-400', size=80, x=540, y=1240, rot=2),
           dict(at='L2:iran', until='L3-0.1', text='HIDDEN IRAN DEALS?', size=64, x=540, y=1660, rot=-2),
           dict(at='L3', until='L3:huawei-0.1', text='NOT RACKETEERING', size=64, x=540, y=1660, rot=2)],
    stamps=[dict(at='L4:proven', text='PROVEN', size=100, color=(30, 70, 52), x=540, y=560, rot=-6),
            dict(at='L4:debated', text='DEBATED', size=100, color=(160, 32, 24), x=560, y=780, rot=5)],
    music=dict(sections=[(0, 'L1', ['Dm9', 'Am9'], dict(bright=(0.3, 0.45), pulse=True)),
                         ('L1', 'L2', ['Esus', 'Dm9'], dict(bright=(0.45, 0.6), pulse=True, ticks=True)),
                         ('L2', 'L4', ['Fmaj7', 'Esus'], dict(bright=(0.5, 0.65), gain=(1, 1.1), pulse=True, ticks=True)),
                         ('L4', 'END', ['Am9', 'Fmaj7'], dict(bright=(0.5, 0.3), gain=(1, 0.0), plucks=0.4))]),
)
