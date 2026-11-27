"""Percept Lab #007 — Stare Test #2: a black-and-white picture that turns colour (negative afterimage).
An own painted landscape (blue sky, yellow sun, green hills, red barn) is shown colour-INVERTED with a red fixation
dot for 20 s; then a hard cut to the same landscape in grayscale with the same dot. While staring, the eye's colour
channels adapt to the inverted colours; on the gray image the adapted channels respond less, so you briefly see the
opposite (i.e. the original) colours: a negative afterimage, explained by opponent-process colour vision
(Wikipedia 'Afterimage'; Britannica 'afterimage'). Static image on purpose (fixation needed); the countdown moves."""
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageOps

W, H = 1440, 2560
CX, CY = 720, 1240


def landscape():
    im = Image.new('RGB', (W, H), (70, 140, 230)); d = ImageDraw.Draw(im)
    for k in range(40):                                                    # sky gradient
        d.rectangle((0, k * 30, W, k * 30 + 30), fill=(60 + k, 130 + k, 225))
    d.ellipse((1000, 280, 1300, 580), fill=(255, 215, 40))                 # sun
    d.polygon([(0, 1500), (400, 1250), (800, 1420), (1150, 1200), (1440, 1350), (1440, H), (0, H)], fill=(40, 170, 60))
    d.polygon([(0, 1900), (500, 1700), (1000, 1850), (1440, 1700), (1440, H), (0, H)], fill=(30, 140, 45))
    d.rectangle((260, 1250, 760, 1700), fill=(210, 30, 30))                # red barn
    d.polygon([(220, 1260), (510, 1020), (800, 1260)], fill=(170, 20, 25))
    d.rectangle((420, 1430, 600, 1700), fill=(250, 250, 245))
    d.line([(420, 1430), (600, 1700)], fill=(210, 30, 30), width=18); d.line([(600, 1430), (420, 1700)], fill=(210, 30, 30), width=18)
    d.rectangle((300, 1300, 380, 1380), fill=(250, 250, 245)); d.rectangle((640, 1300, 720, 1380), fill=(250, 250, 245))
    for tx, ty in ((1000, 1500), (1220, 1560)):                            # trees
        d.rectangle((tx - 25, ty, tx + 25, ty + 220), fill=(110, 60, 20))
        d.ellipse((tx - 140, ty - 260, tx + 140, ty + 40), fill=(20, 120, 40))
    for fx in range(120, 1400, 140):                                       # flowers in the grass
        d.ellipse((fx - 26, 2150 + (fx % 3) * 60, fx + 26, 2202 + (fx % 3) * 60), fill=(255, 220, 30))
    return im.filter(ImageFilter.GaussianBlur(3))


def dot(im):
    d = ImageDraw.Draw(im)
    d.ellipse((CX - 34, CY - 34, CX + 34, CY + 34), fill=(255, 255, 255))
    d.ellipse((CX - 24, CY - 24, CX + 24, CY + 24), fill=(230, 0, 0))
    return im


def paint(work):
    out = Path(work) / 'stare'; out.mkdir(parents=True, exist_ok=True)
    base = landscape()
    dot(ImageOps.invert(base)).save(out / '00_inverted.png')
    dot(ImageOps.grayscale(base).convert('RGB')).save(out / '01_gray.png')


ST = ['stare/00_inverted.png', 'stare/01_gray.png']

EPISODE = dict(
    chapter='The Colour Afterimage',
    title="Stare 20 Seconds. This Black & White Picture Turns Colour 👁️ #shorts",
    description=("Stare Test #2. Keep your eyes on the red dot for 20 seconds while the colours look wrong. When the "
                 "picture turns black and white, you'll see it in colour for a moment. It's a negative afterimage: "
                 "while you stare, the colour channels in your eyes adapt to the strange colours, and on the gray image "
                 "your brain briefly shows you the opposite colours – which are the real ones.\n\n"
                 "Illustrations painted with code (no photos), narration is synthetic."),
    tags=['afterimage', 'optical illusion', 'stare at the dot', 'black and white to colour', 'brain test',
          'perception', 'illusions'],
    voice='af_nicole',
    lines=["Stare at the red dot. Don't move your eyes.",
           "Twenty seconds. These colours are wrong on purpose.",
           "Keep staring. Don't blink.",
           "Almost there.",
           "Now. It's in colour. Isn't it?",
           "Tired colour cells. Your brain paints the opposite. Blink, and it's gone."],
    gaps=[0.15, 1.0, 3.0, 3.0, 2.3, 0.5],
    display=[(1, 'twenty', '20')],
    fade=0, bg=(0, 0, 0), tail=1.4,
    plates=[dict(stages=ST, show=[(0, 0), ('L4', 1)])],
    camera=[(0, 720, 1280, 2560), ('END', 720, 1280, 2560)],
    cards=[dict(at=0, until='L1', text='STARE TEST #2', font='AlfaSlabOne-400', size=84, paper=(255, 255, 255),
                ink=(20, 20, 20), tape=False, x=540, y=1420, rot=-2)],
    counter=dict(start=0.3, full='L4-0.2', until='L4', n=20, fmt='{n}s', x=540, y=260, rot=-3, size=120),
    stamps=[dict(at='L5', text='YOUR BRAIN DID THAT', size=64, color=(200, 30, 30), x=540, y=300, rot=-5)],
    caption=dict(y=0.86),
    music=dict(sections=[(0, 'L4', ['Am9', 'Esus'], dict(bright=(0.15, 0.3), ticks=True)),
                         ('L4', 'END', ['Fmaj7', 'Cmaj9'], dict(bright=(0.5, 0.3), gain=(1, 0.0), plucks=0.4))],
               events=[('L4', 'chime', dict(f=880.0))]),
)
