"""Erzeugt die Texturen fürs Long-Layout "exam" (Holztisch + Papier) einmalig als Bilder.
Aufruf: python scripts/make_exam_textures.py  → public/exam/desk.jpg, public/exam/paper.jpg"""
from pathlib import Path
from playwright.sync_api import sync_playwright

OUT = Path(__file__).resolve().parent.parent / 'public' / 'exam'
DESK = '''<svg xmlns="http://www.w3.org/2000/svg" width="1920" height="1080">
<filter id="w" x="0" y="0" width="100%" height="100%">
 <feTurbulence type="fractalNoise" baseFrequency="0.004 0.09" numOctaves="4" seed="7"/>
 <feColorMatrix type="matrix" values="0 0 0 0 0.36  0 0 0 0 0.21  0 0 0 0 0.11  0 0 0 -2.2 1.35"/>
</filter>
<filter id="g" x="0" y="0" width="100%" height="100%">
 <feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="2" seed="3"/>
 <feColorMatrix type="saturate" values="0"/><feComponentTransfer><feFuncA type="linear" slope="0.10"/></feComponentTransfer>
</filter>
<rect width="1920" height="1080" fill="#B07A4A"/>
<rect width="1920" height="1080" filter="url(#w)"/>
<rect width="1920" height="1080" filter="url(#g)"/>
<radialGradient id="v" cx="50%" cy="45%" r="75%"><stop offset="55%" stop-color="#000" stop-opacity="0"/><stop offset="100%" stop-color="#1a0d05" stop-opacity="0.55"/></radialGradient>
<rect width="1920" height="1080" fill="url(#v)"/>
</svg>'''
PAPER = '''<svg xmlns="http://www.w3.org/2000/svg" width="1300" height="1000">
<filter id="n" x="0" y="0" width="100%" height="100%">
 <feTurbulence type="fractalNoise" baseFrequency="0.65" numOctaves="3" seed="11"/>
 <feColorMatrix type="saturate" values="0"/><feComponentTransfer><feFuncA type="linear" slope="0.07"/></feComponentTransfer>
</filter>
<filter id="b" x="0" y="0" width="100%" height="100%">
 <feTurbulence type="fractalNoise" baseFrequency="0.006" numOctaves="2" seed="5"/>
 <feColorMatrix type="matrix" values="0 0 0 0 0.6  0 0 0 0 0.5  0 0 0 0 0.3  0 0 0 0.25 -0.08"/>
</filter>
<rect width="1300" height="1000" fill="#FBF8EF"/>
<rect width="1300" height="1000" filter="url(#b)"/>
<rect width="1300" height="1000" filter="url(#n)"/>
</svg>'''


def shot(page, svg, w, h, out):
    page.set_viewport_size({'width': w, 'height': h})
    page.set_content(f'<html><body style="margin:0">{svg}</body></html>')
    page.screenshot(path=str(out), type='jpeg', quality=88, clip={'x': 0, 'y': 0, 'width': w, 'height': h})


if __name__ == '__main__':
    OUT.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page()
        shot(pg, DESK, 1920, 1080, OUT / 'desk.jpg')
        shot(pg, PAPER, 1300, 1000, OUT / 'paper.jpg')
        b.close()
    print('ok')
