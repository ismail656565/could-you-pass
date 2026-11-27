"""Myth Dug Up #013 (news) — Nvidia agrees to pay $290 million to settle the 2018 crypto-mining shareholder lawsuit.
Plates: a cut-and-paste collage with a halftone graphics card and ransom letters (newscollage), and a case file with the
2018 share drop and the eight-year court timeline (blueprint). No logos, no likeness.
Facts (Reuters 25 Nov 2026; The Block 25 Nov 2026; Dataconomy 26 Nov 2026; earlier coverage of the class certification
in March 2026):
- Nvidia agreed to pay $290 million in cash to settle a securities class action in the U.S. District Court for the
  Northern District of California; filed 24 Nov 2026; still requires court approval.
- Investors alleged Nvidia understated how much of its gaming GPU revenue in 2017-2018 came from crypto miners
  (plaintiffs' estimate: about $1.1 billion understated). Class period 10 Aug 2017 - 15 Nov 2018.
- Shares fell about 28% (The Block: 28.5%) over two trading sessions in November 2018 after a forecast cut.
- Nvidia denies wrongdoing and admits no liability; Nvidia says insurers fund the majority of the settlement.
- History: suit filed 2018, dismissed 2021, revived by the Ninth Circuit 2023, U.S. Supreme Court dismissed Nvidia's
  appeal Dec 2024, class certified Mar 2026. Nvidia paid $5.5M to the SEC in 2022 over similar disclosures.
- Plaintiffs' lawyers will seek up to $62 million in fees.
Facts as of 27 Nov 2026."""
from pathlib import Path
from newscollage import NewsCollage, Photo, RED, INK, MUSTARD
from blueprint import Blueprint

W, H = 1440, 2560


def gpu_photo():
    p = Photo(1100, 640, seed=13)
    p.poly([(40, 120), (1060, 120), (1060, 470), (40, 470)], height=10, bevel=4, albedo=0.18, metal=0.5, gloss=0.6)
    for cx in (300, 800):
        p.disc(cx, 295, 150, z=10, height=6, bevel=3, albedo=0.1, metal=0.3, gloss=0.5)
        p.gear(cx, 295, 128, teeth=11, z=14, height=4, spokes=0, albedo=0.35, metal=0.6, gloss=0.5)
        p.disc(cx, 295, 36, z=18, height=4, albedo=0.8, metal=0.4)
    p.poly([(120, 470), (760, 470), (760, 530), (120, 530)], height=4, bevel=1, albedo=0.75, metal=1.0, gloss=0.6)
    for k in range(24):
        x = 140 + k * 25
        p.lines([[(x, 478), (x, 524)]], 6, tone=0.35)
    p.text('GAMING?', 550, 590, 60, font='didone', tone=0.1)
    p.glare(300, 200, 140, 360, 200, 250, strength=0.4)
    return p


def coin_photo():
    p = Photo(420, 420, seed=14)
    p.disc(210, 210, 190, height=12, bevel=5, albedo=0.7, metal=1.0, gloss=0.6)
    p.ring(210, 210, 150, 165, z=12, albedo=0.7, metal=1.0)
    p.text('B', 210, 215, 170, font='didone', tone=0.15)
    p.glare(160, 140, 60, 160, 200, 250, strength=0.5)
    return p


def paint_collage(out):
    nc = NewsCollage(W, H, seed=131)
    nc.board()
    for (w, h, x, y, r, sides) in ((980, 1300, 470, 760, -4, 'rb'), (900, 1200, 1010, 1650, 5, 'lt'), (820, 900, 430, 2160, -2, 'rt')):
        s = nc.newsprint(w, h, columns=3); s.tear(sides); nc.paste(s, x, y, rot=r)
    nc.stage('board')
    nc.disc(720, 1230, 520, RED)
    s = nc.print_photo(gpu_photo()); s.cutout(14); nc.paste(s, 720, 1200, rot=-7)
    nc.stage('gpu')
    nc.ransom('NVIDIA PAYS', 170, 300, 84, rot=2)
    nc.ransom('$290,000,000', 160, 560, 76, rot=-2)
    nc.tape(220, 220, 200, rot=-12); nc.tape(1250, 200, 200, rot=10)
    nc.stage('ransom')
    s = nc.print_photo(coin_photo()); s.cutout(10); nc.paste(s, 1140, 1640, rot=12)
    nc.label('CRYPTO SALES 2017-18', 150, 1900, 62, face='typewriter_bold', rot=3)
    nc.stage('crypto')
    nc.label('8 YEARS IN COURT', 210, 2290, 70, face='typewriter_bold', block=MUSTARD, rot=-2)
    nc.tape(220, 2280, 160, rot=70)
    nc.stage('years')
    nc.stamp(1020, 2140, ['NO', 'ADMISSION'], rot=-10)
    nc.stage('stamp')
    nc.save(str(out / 'collage.png'), stages_dir=str(out / 'collage'))


def paint_sheet(out):
    bp = Blueprint(W, H, seed=132)
    bp.border(50, 50, W - 50, H - 50, zones=(4, 8), size=18)
    bp.text('CASE FILE: CRYPTO SALES', W / 2, 190, 58, 'ms', pen=2.2, spacing=0.2)
    bp.text('SECURITIES CLASS ACTION · N.D. CALIFORNIA', W / 2, 250, 28, 'ms')
    bp.stage('sheet')
    # share price, Nov 2018: two sessions, about -28%
    x0, y0, x1, y1 = 180, 380, 1260, 1060
    bp.line([(x0, y0), (x0, y1), (x1, y1)], 'heavy')
    pts = [(x0 + 20, 520), (300, 500), (420, 540), (540, 510), (660, 530), (780, 520), (860, 540)]
    bp.line(pts, 'thick')
    bp.text('NOV 2018', x0 + 40, y1 + 50, 30, 'ls')
    bp.text('SHARE PRICE', x0 + 20, y0 - 20, 30, 'ls')
    bp.stage('chart')
    drop = [(860, 540), (1000, 760), (1180, 880)]
    bp.red(drop, width=5)
    bp.dashed([(860, 540), (1180, 540)], 'thin')
    bp.red_text('-28%', 900, 1000, 110, rot=-3)
    bp.text('IN TWO TRADING DAYS', 940, 1110, 30, 'ms')
    bp.stage('drop')
    bp.view_title(720, 1240, 'EIGHT YEARS IN COURT', size=34)
    rows = (('2018', 'INVESTORS SUE'), ('2021', 'CASE DISMISSED'), ('2023', 'APPEALS COURT REVIVES IT'),
            ('2024', 'SUPREME COURT: NO HEARING'), ('2026', '290 MILLION SETTLEMENT'))
    bx, by, rh = 150, 1300, 140
    bp.table(bx, by, [260, 880], [rh] * 5, pen='thin', outer='heavy')
    for i, (a, v) in enumerate(rows):
        yy = by + i * rh + 90
        bp.text(a, bx + 40, yy, 48, 'ls', pen=2.2)
        bp.text(v, bx + 290, yy, 38, 'ls', pen=1.9)
        if i == 2:
            bp.stage('rows')
    bp.cloud([(bx + 270, by + 4 * rh + 10), (bx + 1130, by + 4 * rh + 10), (bx + 1130, by + 5 * rh - 10), (bx + 270, by + 5 * rh - 10)])
    bp.red_text('NO ADMISSION OF WRONGDOING', 720, 2160, 50, rot=2, anchor='ms')
    bp.text('JUDGE MUST STILL APPROVE', W / 2, 2260, 36, 'ms', pen=2.0)
    bp.stage('settle')
    bp.fold(xs=(720,), ys=(1280,), wear=0.7)
    bp.stain(1220, 2420, 70, 0.6)
    bp.save(str(out / 'sheet.png'), str(out / 'sheet'))


def paint(work):
    out = Path(work); out.mkdir(parents=True, exist_ok=True)
    paint_collage(out)
    paint_sheet(out)


PH = 2560
A = ['collage/%s.png' % n for n in ('00_board', '01_gpu', '02_ransom', '03_crypto', '04_years', '05_stamp', '06_final')]
B = ['sheet/%s.png' % n for n in ('00_sheet', '01_chart', '02_drop', '03_rows', '04_settle', '05_final')]

EPISODE = dict(
    chapter='Nvidia crypto settlement',
    title="Nvidia Will Pay $290 Million Over Crypto. It Admits Nothing. #shorts",
    description=("Nvidia has agreed to pay $290 million to settle a shareholder class action filed in 2018. Investors alleged "
                 "that in 2017 and 2018 Nvidia understated how much of its gaming graphics-card sales came from crypto miners - "
                 "by about $1.1 billion, according to the plaintiffs. When crypto mining demand collapsed, the stock fell about "
                 "28% in two trading days in November 2018. The case was dismissed in 2021, revived on appeal in 2023, and the "
                 "Supreme Court dismissed Nvidia's appeal in 2024. Nvidia denies wrongdoing and says insurers fund most of the "
                 "payment. A federal judge in California still has to approve the deal. (Nvidia paid the SEC $5.5 million over "
                 "similar disclosures in 2022.)\n\n"
                 "Proven: the $290 million settlement was filed in court.\n"
                 "Debated: whether Nvidia misled investors - it admits no wrongdoing and the claims were never tried.\n\n"
                 "Sources: Reuters, The Block, Dataconomy, court filing.\n"
                 "Illustrations painted with code (no photos), narration is synthetic. Facts as of 27 Nov 2026. Not financial advice."),
    tags=['nvidia', 'nvidia lawsuit', 'nvidia settlement', 'crypto mining', 'class action', 'gpu', 'tech news', 'business news', 'news'],
    voice='bm_george',
    lines=["Nvidia is paying to end an eight-year fight.",
           "Investors claimed that in twenty seventeen and eighteen, it hid how much of its gaming chip sales came from crypto miners. Their estimate: over a billion dollars.",
           "When the crypto boom crashed, the stock fell about twenty-eight percent in two days.",
           "The case reached the Supreme Court. Now Nvidia settles for two hundred ninety million dollars. It admits no wrongdoing.",
           "Proven: the deal was filed in court. Debated: whether Nvidia really misled anyone."],
    gaps=[0.15, 0.35, 0.4, 0.4, 0.45],
    display=[(3, 'two', '$290'), (3, 'hundred', ''), (3, 'ninety', ''), (3, 'million', 'MILLION'), (3, 'dollars.', ''),
             (2, 'twenty-eight', '28%'), (2, 'percent', '')],
    plates=[dict(stages=A, show=[(0, 2), ('L1:crypto', 3), ('L3', 4), ('L3:it', 5)]),
            dict(stages=B, show=[(0, 1), ('L2:fell', 2), ('L3', 3), ('L3:it', 4), ('L4', 5)])],
    camera=[(0, 720, 1180, 2300), ('L0.end', 720, 1230, 2350), ('L1+0.2', 720, 1350, 2250), ('L1:crypto', 720, 1450, 2200),
            ('L1.end', 720, 1450, 2250),
            ('L2-0.1', 720, PH + 1150, 2300), ('L2.end', 720, PH + 1150, 2300),
            ('L3-0.1', 720, PH + 1500, 2000), ('L3:it', 720, PH + 1500, 1950), ('L4', 720, PH + 1300, 2450),
            ('END', 720, PH + 1300, 2500)],
    cards=[dict(at=0, until='L1-0.1', text='$290 MILLION', font='AlfaSlabOne-400', size=96, ink=(160, 32, 24), x=540, y=1780, rot=-3),
           dict(at='L1:their', until='L2-0.1', text='$1 BILLION+?', font='AlfaSlabOne-400', size=88, x=540, y=1720, rot=2),
           dict(at='L3:it', until='L4-0.1', text='NO ADMISSION', size=80, x=540, y=1720, rot=-2)],
    stamps=[dict(at='L4:proven', text='PROVEN', size=100, color=(30, 70, 52), x=540, y=560, rot=-6),
            dict(at='L4:debated', text='ALLEGED', size=100, color=(160, 32, 24), x=560, y=780, rot=5)],
    music=dict(sections=[(0, 'L1', ['Dm9', 'Am9'], dict(bright=(0.3, 0.45), pulse=True)),
                         ('L1', 'L2', ['Esus', 'Dm9'], dict(bright=(0.45, 0.6), pulse=True, ticks=True)),
                         ('L2', 'L4', ['Fmaj7', 'Esus'], dict(bright=(0.5, 0.65), gain=(1, 1.1), pulse=True, ticks=True)),
                         ('L4', 'END', ['Am9', 'Fmaj7'], dict(bright=(0.5, 0.3), gain=(1, 0.0), plucks=0.4))]),
)
