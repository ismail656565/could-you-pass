"""HiddenFrontlines #006 — One Soldier, One Decision #1: the D-Day piper (painted dusk beach + file card, numpy + Pillow).
Facts (Wikipedia 'Bill Millin'; History UK 'The bagpiper of D-Day'; British Army news 'Remembering again the stirring
sounds that accompanied D-Day landings'): Bill Millin (born 14 July 1922, so 21 on D-Day) was personal piper to Lord
Lovat, commander of the 1st Special Service Brigade; on 6 June 1944 at Sword Beach, Normandy, Lovat asked him to play,
and he piped up and down the beach under fire, armed only with his pipes and a sgian-dubh. Millin's own account:
captured German snipers later told him they had not shot at him because they thought he was mad. He survived the war
and died in 2010. Generic silhouette only, no likeness. No gore."""
from pathlib import Path
import math
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

W, H = 1440, 2560
FD = Path(__file__).resolve().parents[4] / 'fonts'
SIL = (14, 10, 16)


def F(name, px):
    return ImageFont.truetype(str(FD / name), px)


def blobs(im, rng, n, box, rmin, rmax, colour, blur, alpha=1.0):
    lay = Image.new('RGBA', im.size, (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    for _ in range(n):
        x = rng.uniform(box[0], box[2]); y = rng.uniform(box[1], box[3]); r = rng.uniform(rmin, rmax)
        d.ellipse((x - r, y - r * 0.8, x + r, y + r * 0.8), fill=colour + (int(255 * alpha),))
    im.alpha_composite(lay.filter(ImageFilter.GaussianBlur(blur)))


def piper(d, x, foot, h):
    u = h / 950.0
    P = lambda pts: [(x + px * u, foot - py * u) for px, py in pts]
    d.polygon(P([(-70, 0), (-20, 0), (-25, 250), (-60, 250)]), fill=SIL)              # legs
    d.polygon(P([(10, 0), (75, 0), (55, 250), (20, 250)]), fill=SIL)
    d.polygon(P([(-95, 230), (95, 230), (70, 430), (-70, 430)]), fill=SIL)            # kilt
    d.polygon(P([(-80, 420), (80, 420), (95, 720), (-85, 720)]), fill=SIL)            # torso
    d.ellipse(P([(-62, 860), (62, 720)])[0] + P([(-62, 860), (62, 720)])[1], fill=SIL)  # head
    d.ellipse(P([(-80, 900), (60, 830)])[0] + P([(-80, 900), (60, 830)])[1], fill=SIL)  # beret
    d.ellipse(P([(-30, 935), (10, 895)])[0] + P([(-30, 935), (10, 895)])[1], fill=SIL)  # toorie
    d.ellipse(P([(-200, 660), (-20, 500)])[0] + P([(-200, 660), (-20, 500)])[1], fill=SIL)  # the bag
    d.polygon(P([(-60, 690), (-150, 700), (-190, 620), (-120, 600)]), fill=SIL)       # arm on the bag
    d.line(P([(-160, 560), (-230, 330)]), fill=SIL, width=int(22 * u))                 # chanter
    d.polygon(P([(-250, 330), (-210, 330), (-215, 300), (-245, 300)]), fill=SIL)
    d.line(P([(40, 650), (-200, 470)]), fill=SIL, width=int(30 * u))                   # arm on the chanter
    d.line(P([(30, 640), (-40, 760), (-60, 560)]), fill=SIL, width=int(28 * u))
    d.line(P([(-80, 660), (-150, 590)]), fill=SIL, width=int(18 * u))                  # blowpipe
    for k, (dx, L) in enumerate(((0, 440), (40, 400), (80, 330))):                     # drones over the shoulder
        a = math.radians(62 - k * 9)
        p0 = (-120 + dx * 0.4, 620); p1 = (p0[0] + L * math.cos(a), p0[1] + L * math.sin(a))
        d.line(P([p0, p1]), fill=SIL, width=int((20 - k * 3) * u))
        cx, cy = P([p1])[0]
        d.ellipse((cx - 18 * u, cy - 18 * u, cx + 18 * u, cy + 18 * u), fill=SIL)
    for k in range(3):                                                                 # ribbons
        p = P([(60 + k * 25, 760 - k * 10)])[0]
        d.line([p, (p[0] + 40 * u, p[1] + 140 * u)], fill=SIL, width=int(8 * u))


def beach(seed=6):
    rng = np.random.default_rng(seed)
    y = np.linspace(0, 1, H)[:, None]
    top, mid, low = np.array([46, 30, 70]), np.array([214, 96, 52]), np.array([250, 180, 90])
    sky = np.where(y < 0.35, top + (mid - top) * (y / 0.35), mid + (low - mid) * np.clip((y - 0.35) / 0.17, 0, 1))
    arr = np.repeat(sky[:, None, :], W, axis=1).reshape(H, W, 3)
    im = Image.fromarray(arr.astype(np.uint8)).convert('RGBA')
    blobs(im, rng, 40, (-100, 500, 1540, 1300), 90, 220, (60, 50, 60), 40, 0.55)       # smoke
    blobs(im, rng, 10, (0, 1220, 1440, 1320), 20, 50, (255, 140, 40), 18, 0.9)          # distant fires
    d = ImageDraw.Draw(im)
    d.rectangle((0, 1320, W, 1620), fill=(70, 60, 80))                                 # sea
    for k in range(18):
        yy = 1340 + k * 16
        d.line([(rng.uniform(0, 600), yy), (rng.uniform(800, 1440), yy)], fill=(120, 90, 90), width=2)
    for bx, by, s in ((180, 1330, 1.0), (1080, 1345, 0.8)):                            # landing craft silhouettes
        d.polygon([(bx, by), (bx + 300 * s, by), (bx + 330 * s, by - 60 * s), (bx + 20 * s, by - 70 * s)], fill=(30, 24, 34))
    d.polygon([(0, 1600), (W, 1560), (W, H), (0, H)], fill=(92, 66, 52))                # sand
    for k in range(10):
        yy = 1700 + k * 85
        d.line([(0, yy), (W, yy - 20)], fill=(80, 56, 44), width=3)
    for hx, hy in ((150, 1820), (1290, 1760), (1180, 2010)):                            # beach obstacles
        d.line([(hx - 60, hy + 50), (hx + 60, hy - 50)], fill=(40, 30, 32), width=14)
        d.line([(hx - 60, hy - 50), (hx + 60, hy + 50)], fill=(40, 30, 32), width=14)
        d.line([(hx, hy - 70), (hx, hy + 70)], fill=(40, 30, 32), width=14)
    return im, rng


def paint(work):
    out = Path(work); (out / 'beach').mkdir(parents=True, exist_ok=True); (out / 'file').mkdir(exist_ok=True)
    im, rng = beach()
    glow = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ImageDraw.Draw(glow).ellipse((380, 1050, 1060, 1650), fill=(255, 190, 110, 150))
    im.alpha_composite(glow.filter(ImageFilter.GaussianBlur(90)))
    d = ImageDraw.Draw(im)
    piper(d, 760, 2160, 1000)
    d.ellipse((520, 2130, 1020, 2190), fill=(60, 42, 36))                             # shadow
    piper(d, 760, 2160, 1000)
    for nx, ny, r in ((420, 980, 34), (470, 900, 26), (1120, 1060, 30)):               # music notes in the smoke
        d.ellipse((nx - r, ny - r * 0.75, nx + r, ny + r * 0.75), fill=(255, 226, 170))
        d.line([(nx + r - 4, ny), (nx + r - 4, ny - 120)], fill=(255, 226, 170), width=8)
    im.convert('RGB').save(out / 'beach' / '00_piper.png')

    f = Image.new('RGB', (W, H), (52, 38, 30)); d = ImageDraw.Draw(f)
    for k in range(40):
        yy = k * 66 + rng.uniform(-10, 10)
        d.line([(0, yy), (W, yy + rng.uniform(-8, 8))], fill=(60, 44, 34), width=4)
    card = Image.new('RGBA', (1160, 1380), (232, 219, 186, 255)); c = ImageDraw.Draw(card)
    c.rectangle((0, 0, 1159, 1379), outline=(150, 120, 80), width=6)
    c.text((580, 110), 'PERSONNEL FILE', font=F('Anton-400.woff', 96), fill=(60, 40, 30), anchor='mm')
    c.line([(80, 190), (1080, 190)], fill=(120, 90, 60), width=4)
    rows = [('NAME', 'PIPER BILL MILLIN'), ('AGE', '21'), ('UNIT', '1st SPECIAL SERVICE BRIGADE'),
            ('COMMANDER', 'LORD LOVAT'), ('LANDED', 'SWORD BEACH, NORMANDY'), ('DATE', '6 JUNE 1944')]
    for i, (k, v) in enumerate(rows):
        yy = 290 + i * 150
        c.text((90, yy), k + ':', font=F('Poppins-800.woff', 44), fill=(110, 80, 60), anchor='lm')
        c.text((90, yy + 58), v, font=F('Poppins-800.woff', 56), fill=(30, 26, 30), anchor='lm')
    card = card.rotate(2.5, expand=True, resample=Image.BICUBIC)
    sh = Image.new('RGBA', card.size, (0, 0, 0, 0)); sh.paste((0, 0, 0, 140), mask=card.split()[3])
    f = f.convert('RGBA'); f.alpha_composite(sh.filter(ImageFilter.GaussianBlur(20)), (150, 640))
    f.alpha_composite(card, (120, 600))
    f.convert('RGB').save(out / 'file' / '00_file.png')
    d = ImageDraw.Draw(f)
    d.text((720, 2160), 'ARMED WITH: BAGPIPES', font=F('Kalam-700.woff', 92), fill=(180, 30, 26), anchor='mm')
    d.line([(250, 2230), (1190, 2215)], fill=(180, 30, 26), width=8)
    f.convert('RGB').save(out / 'file' / '01_armed.png')


A = ['beach/00_piper.png']
B = ['file/00_file.png', 'file/01_armed.png']
PH = 2560

EPISODE = dict(
    chapter='The D-Day Piper',
    title="The 21-Year-Old Who Played Bagpipes Through the D-Day Landing #shorts",
    description=("One Soldier, One Decision #1. On 6 June 1944, Piper Bill Millin, 21, landed on Sword Beach in Normandy "
                 "with the 1st Special Service Brigade. His commander, Lord Lovat, asked him to play – and he piped up and "
                 "down the beach under fire, armed only with his bagpipes and a small knife. Millin later said captured "
                 "German soldiers told him they hadn't shot at him because they thought he was mad. He survived the war "
                 "and lived until 2010.\n\n"
                 "Illustrations painted with code (no photos), narration is synthetic."),
    tags=['bill millin', 'd-day piper', 'd-day', 'sword beach', 'ww2 stories', 'bagpipes', 'military history'],
    voice='am_michael',
    lines=["He walked onto a beach under fire. Armed with bagpipes.",
           "His commander told him to play. So he did, marching up and down the sand.",
           "This was D-Day, on Sword Beach in Normandy.",
           "The young piper was twenty-one. His commander was a Scottish lord.",
           "He later said captured German soldiers told him why they never shot at him.",
           "They thought he'd gone mad. He survived the war."],
    gaps=[0.15, 0.35, 0.4, 0.4, 0.4, 0.4],
    display=[(3, 'twenty-one.', '21.')],
    plates=[dict(stages=A, show=[(0, 0)]), dict(stages=B, show=[(0, 0), ('L3', 1)])],
    camera=[(0, 760, 1640, 1900), ('L1', 760, 1600, 2000), ('L2', 720, 1300, 2440), ('L2@0.6', 720, 1300, 2440),
            ('L2.end', 720, PH + 1300, 2300), ('L3', 720, PH + 1450, 2200), ('L4', 720, PH + 1450, 2200), ('L5', 760, 1550, 2100), ('END', 760, 1500, 2200)],
    cards=[dict(at=0, until='L1-0.2', text='UNDER FIRE', font='AlfaSlabOne-400', size=100, ink=(150, 34, 26),
                x=540, y=1560, rot=-3)],
    caption=dict(y=0.9),
    stamps=[dict(at='L5:survived', text='SURVIVED', size=110, color=(170, 30, 24), x=540, y=520, rot=-7)],
    music=dict(sections=[(0, 'L2', ['Dm9', 'Am9'], dict(bright=(0.2, 0.35), pulse=True)),
                         ('L2', 'L4', ['Esus', 'Dm9'], dict(bright=(0.35, 0.5), pulse=True, ticks=True)),
                         ('L4', 'END', ['Am9', 'Fmaj7'], dict(bright=(0.4, 0.25), gain=(1, 0.0)))]),
)
