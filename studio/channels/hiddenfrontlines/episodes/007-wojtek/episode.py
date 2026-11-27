"""HiddenFrontlines #007 — One Soldier, One Decision: the bear who was enlisted (painted battlefield + unit badge,
numpy + Pillow). Facts (Wikipedia 'Wojtek (bear)'; Britannica 'Wojtek the Bear'; IPN 'On 15 November 1947 Wojtek the
bear was moved … to the Edinburgh Zoo'; British Library blog 'Wojtek the soldier bear'): a Syrian brown bear cub
adopted in Iran in 1942 by soldiers of the Polish II Corps (22nd Artillery Supply Company); officially enlisted so he
could be shipped with the unit to Italy; at the Battle of Monte Cassino (1944) soldiers said he carried crates of
ammunition; the company adopted a badge showing a bear carrying an artillery shell; promoted to corporal; full grown
about 220 kg; after the war he lived at Edinburgh Zoo from 1947 until his death in December 1963. Shell carrying is
told as 'soldiers said'. Generic silhouettes, no insignia beyond the bear badge, no gore."""
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

W, H = 1440, 2560
FD = Path(__file__).resolve().parents[4] / 'fonts'
SIL = (24, 20, 18)


def F(name, px):
    return ImageFont.truetype(str(FD / name), px)


def blobs(im, rng, n, box, rmin, rmax, colour, blur, alpha=1.0):
    lay = Image.new('RGBA', im.size, (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    for _ in range(n):
        x = rng.uniform(box[0], box[2]); y = rng.uniform(box[1], box[3]); r = rng.uniform(rmin, rmax)
        d.ellipse((x - r, y - r * 0.8, x + r, y + r * 0.8), fill=colour + (int(255 * alpha),))
    im.alpha_composite(lay.filter(ImageFilter.GaussianBlur(blur)))


def bear(d, x, foot, h, col=SIL, crate=True):
    """upright bear seen from the side-back, carrying a crate; (x, foot) = between the feet"""
    u = h / 1000.0
    E = lambda cx, cy, rx, ry: d.ellipse((x + (cx - rx) * u, foot - (cy + ry) * u, x + (cx + rx) * u, foot - (cy - ry) * u), fill=col)
    E(-60, 120, 70, 130); E(80, 120, 70, 130)                                          # legs
    E(0, 430, 200, 300)                                                                # body
    E(-20, 700, 190, 150)                                                              # shoulder hump
    E(70, 860, 120, 105)                                                               # head
    E(190, 830, 85, 50)                                                                # snout
    E(0, 970, 34, 34); E(110, 975, 34, 34)                                             # ears
    if crate:
        cx0, cy0 = x + 120 * u, foot - 820 * u
        d.polygon([(cx0 - 20 * u, cy0), (cx0 + 330 * u, cy0 - 40 * u), (cx0 + 350 * u, cy0 + 160 * u),
                   (cx0, cy0 + 200 * u)], fill=(96, 74, 46))                           # the crate
        for k in range(1, 3):
            t = k / 3
            d.line([(cx0 - 20 * u + 370 * u * t, cy0 - 40 * u * t), (cx0 + 350 * u * t, cy0 + 200 * u - 40 * u * t)],
                   fill=(70, 52, 30), width=int(10 * u))
        E(170, 690, 80, 50); E(250, 640, 60, 45)                                       # arm up to the crate


def landscape(seed=7):
    rng = np.random.default_rng(seed)
    y = np.linspace(0, 1, H)[:, None]
    top, low = np.array([96, 104, 96]), np.array([186, 176, 140])
    sky = top + (low - top) * np.clip(y / 0.5, 0, 1)
    im = Image.fromarray(np.repeat(sky[:, None, :], W, axis=1).astype(np.uint8)).convert('RGBA')
    d = ImageDraw.Draw(im)
    d.polygon([(0, 1200), (260, 900), (520, 1040), (760, 760), (1040, 980), (1300, 820), (1440, 900), (1440, 1500),
               (0, 1500)], fill=(92, 100, 84))                                         # mountains
    d.polygon([(0, 1400), (380, 1250), (820, 1380), (1180, 1240), (1440, 1330), (1440, 1700), (0, 1700)], fill=(74, 82, 64))
    blobs(im, rng, 36, (-100, 500, 1540, 1350), 90, 230, (70, 70, 66), 45, 0.5)        # smoke
    blobs(im, rng, 8, (900, 1150, 1400, 1300), 20, 50, (240, 150, 70), 20, 0.7)        # distant flashes
    d = ImageDraw.Draw(im)
    d.polygon([(0, 1650), (W, 1600), (W, H), (0, H)], fill=(110, 96, 70))              # dirt track
    for k in range(12):
        yy = 1720 + k * 70
        d.line([(0, yy + rng.uniform(-10, 10)), (W, yy - 30 + rng.uniform(-10, 10))], fill=(96, 82, 60), width=4)
    for bx in (140, 1250):                                                             # stacked crates
        for j in range(3):
            d.rectangle((bx - 90, 1900 - j * 110, bx + 90, 2000 - j * 110), fill=(84, 64, 40), outline=(50, 38, 24), width=6)
    return im, rng


def badge(size=900):
    im = Image.new('RGBA', (size, size), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.ellipse((0, 0, size - 1, size - 1), fill=(200, 160, 70), outline=(110, 80, 30), width=18)
    d.ellipse((60, 60, size - 61, size - 61), fill=(232, 219, 186))
    bear(d, size * 0.42, size * 0.86, size * 0.66, col=(60, 40, 26), crate=False)
    sx0, sx1 = size * 0.58, size * 0.68                                                 # brass shell held up
    d.rounded_rectangle((sx0, size * 0.22, sx1, size * 0.52), 12, fill=(214, 160, 60), outline=(60, 40, 26), width=8)
    d.polygon([(sx0, size * 0.23), ((sx0 + sx1) / 2, size * 0.1), (sx1, size * 0.23)], fill=(150, 110, 60),
              outline=(60, 40, 26))
    d.line([(sx0, size * 0.47), (sx1, size * 0.47)], fill=(60, 40, 26), width=8)
    return im


def paint(work):
    out = Path(work); (out / 'field').mkdir(parents=True, exist_ok=True); (out / 'file').mkdir(exist_ok=True)
    im, rng = landscape()
    glow = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ImageDraw.Draw(glow).ellipse((300, 900, 1140, 1800), fill=(250, 220, 160, 120))
    im.alpha_composite(glow.filter(ImageFilter.GaussianBlur(100)))
    d = ImageDraw.Draw(im)
    d.ellipse((420, 2180, 1100, 2250), fill=(70, 58, 40))                              # shadow
    bear(d, 720, 2210, 1250)
    for sx in (280, 1180):                                                             # small soldier silhouettes
        d.ellipse((sx - 26, 1540, sx + 26, 1592), fill=SIL)
        d.polygon([(sx - 40, 1590), (sx + 40, 1590), (sx + 30, 1740), (sx - 30, 1740)], fill=SIL)
        d.line([(sx - 20, 1740), (sx - 26, 1840)], fill=SIL, width=18); d.line([(sx + 20, 1740), (sx + 26, 1840)], fill=SIL, width=18)
    im.convert('RGB').save(out / 'field' / '00_bear.png')

    f = Image.new('RGB', (W, H), (52, 46, 38)); d = ImageDraw.Draw(f)
    for k in range(40):
        yy = k * 66 + rng.uniform(-10, 10)
        d.line([(0, yy), (W, yy + rng.uniform(-8, 8))], fill=(60, 53, 44), width=4)
    f = f.convert('RGBA')
    b = badge(820)
    f.alpha_composite(b, (310, 260))
    d = ImageDraw.Draw(f)
    d.text((720, 1170), 'THE COMPANY BADGE', font=F('Anton-400.woff', 84), fill=(232, 219, 186), anchor='mm')
    f.convert('RGB').save(out / 'file' / '00_badge.png')
    card = Image.new('RGBA', (1160, 1040), (232, 219, 186, 255)); c = ImageDraw.Draw(card)
    c.rectangle((0, 0, 1159, 1039), outline=(150, 120, 80), width=6)
    c.text((580, 100), 'SERVICE RECORD', font=F('Anton-400.woff', 92), fill=(60, 40, 30), anchor='mm')
    c.line([(80, 175), (1080, 175)], fill=(120, 90, 60), width=4)
    rows = [('NAME', 'WOJTEK'), ('SPECIES', 'SYRIAN BROWN BEAR'), ('RANK', 'CORPORAL'),
            ('UNIT', '22nd ARTILLERY SUPPLY CO.'), ('AFTER THE WAR', 'EDINBURGH ZOO')]
    for i, (k, v) in enumerate(rows):
        yy = 250 + i * 155
        c.text((90, yy), k + ':', font=F('Poppins-800.woff', 42), fill=(110, 80, 60), anchor='lm')
        c.text((90, yy + 56), v, font=F('Poppins-800.woff', 56), fill=(30, 26, 30), anchor='lm')
    card = card.rotate(-2, expand=True, resample=Image.BICUBIC)
    sh = Image.new('RGBA', card.size, (0, 0, 0, 0)); sh.paste((0, 0, 0, 140), mask=card.split()[3])
    f.alpha_composite(sh.filter(ImageFilter.GaussianBlur(20)), (150, 1330))
    f.alpha_composite(card, (120, 1290))
    f.convert('RGB').save(out / 'file' / '01_record.png')


A = ['field/00_bear.png']
B = ['file/00_badge.png', 'file/01_record.png']
PH = 2560

EPISODE = dict(
    chapter='The Soldier Bear',
    title="The Army Enlisted a Bear. He Carried Artillery Shells. #shorts",
    description=("One Soldier, One Decision. In 1942 soldiers of the Polish II Corps adopted a Syrian brown bear cub in "
                 "Iran and named him Wojtek. To take him on their ship to Italy, they officially enlisted him in the "
                 "22nd Artillery Supply Company. At the Battle of Monte Cassino in 1944, soldiers said he carried crates "
                 "of ammunition – and the company made a bear carrying an artillery shell its badge. He was promoted to "
                 "corporal, and after the war lived at Edinburgh Zoo until he died in 1963.\n"
                 "Sources: Britannica 'Wojtek the Bear'; Institute of National Remembrance (IPN); British Library.\n\n"
                 "Illustrations painted with code (no photos), narration is synthetic."),
    tags=['wojtek', 'soldier bear', 'wojtek the bear', 'monte cassino', 'ww2 stories', 'animals in war',
          'military history'],
    voice='am_michael',
    say={'Wojtek': 'Voytek'},
    lines=["This soldier was a bear. Officially.",
           "Over two hundred kilos. And soldiers said he carried crates of artillery shells in battle.",
           "His unit adopted him as a cub. To take him on their ship to Italy, they enlisted him.",
           "His company even changed its badge, to a bear carrying a shell.",
           "His name was Wojtek, and he rose to corporal in the Polish army.",
           "After the war, he lived at Edinburgh Zoo, until nineteen sixty-three."],
    gaps=[0.15, 0.35, 0.4, 0.4, 0.4, 0.4],
    display=[(5, 'nineteen', '1963.'), (5, 'sixty-three.', '')],
    plates=[dict(stages=A, show=[(0, 0)]), dict(stages=B, show=[(0, 0), ('L4', 1)])],
    camera=[(0, 740, 1450, 2150), ('L1', 730, 1420, 2250), ('L2', 720, 1300, 2440), ('L2.end', 720, 1300, 2440),
            ('L3', 720, PH + 950, 1900), ('L3.end', 720, PH + 950, 1900), ('L4', 720, PH + 1400, 2300),
            ('END', 720, PH + 1420, 2260)],
    cards=[dict(at=0, until='L1-0.2', text='A REAL SOLDIER', font='AlfaSlabOne-400', size=92, paper=(250, 248, 240),
                ink=(20, 20, 20), tape=False, x=540, y=1600, rot=0)],
    caption=dict(y=0.9),
    stamps=[dict(at='L2:enlisted', text='ENLISTED', size=110, color=(170, 30, 24), x=540, y=380, rot=-7, until='L3')],
    music=dict(sections=[(0, 'L2', ['Dm9', 'Am9'], dict(bright=(0.2, 0.35), pulse=True)),
                         ('L2', 'L4', ['Esus', 'Dm9'], dict(bright=(0.35, 0.5), pulse=True, ticks=True)),
                         ('L4', 'END', ['Am9', 'Fmaj7'], dict(bright=(0.4, 0.25), gain=(1, 0.0)))]),
)
