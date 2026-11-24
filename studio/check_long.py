"""Check a long-video project before it goes into the queue (no kit needed).

  python studio/check_long.py studio/channels/<channel>/longs/NNN-slug

Checks: every sentence covered once and in order, every word cue occurs in its shot's sentences,
no abbreviations with dots that break sentence splitting (U.S., Mr., Dr. ...), short icon labels,
icons/documents timed at the start of the shot, word count / estimated length, meta.json fields.
Exit code 1 on errors.
"""
import json, re, sys
from pathlib import Path

KINDS = {'wide', 'closeup', 'walk', 'icon', 'table', 'counter', 'crowd', 'title', 'list', 'versus', 'map', 'skyline'}
ICONS = {'book', 'brain', 'bulb', 'calendar', 'clock', 'gift', 'heart', 'hourglass', 'house', 'lock', 'phone',
         'shopping', 'target', 'trophy', 'warning', 'laptop'}


def sentences(script):
    out = []
    for l in script.splitlines():
        if l.strip() and not l.startswith('#'):
            out += [x for x in re.split(r'(?<=[.!?])\s+', l.strip()) if x]
    return out


def main(d):
    d = Path(d)
    err, warn = [], []
    script = (d / 'script.txt').read_text()
    st = json.loads((d / 'story.json').read_text())
    meta = json.loads((d / 'meta.json').read_text())
    for m in re.finditer(r'\b(?:[A-Z]\.){2,}|\b(?:Mr|Mrs|Ms|Dr|St|Jr|Sr|vs|etc|Inc|Co)\.', script):
        err.append(f'abbreviation with dots breaks sentence split: {m.group()!r}')
    if re.search(r'\d', '\n'.join(l for l in script.splitlines() if not l.startswith('#'))):
        warn.append('digits in script: write numbers as words')
    S = sentences(script)
    words = sum(len(x.split()) for x in S)
    cov = []
    for i, sh in enumerate(st['shots']):
        k = sh.get('kind')
        if k not in KINDS:
            err.append(f'shot {i}: unknown kind {k}')
        if 's' not in sh:
            if k != 'title':
                err.append(f'shot {i}: no "s"')
            continue
        a, b = sh['s'][0], sh['s'][-1]
        cov += list(range(a, b + 1))
        text = ' '.join(S[a:b + 1]).lower() if b < len(S) else ''

        def walk(o):
            if isinstance(o, dict):
                for kk, v in o.items():
                    if kk in ('at', 'ring_at') and isinstance(v, str) and v.lower() not in text:
                        err.append(f'shot {i} s{sh["s"]}: cue {v!r} not in its sentences')
                    else:
                        walk(v)
            elif isinstance(o, list):
                for v in o:
                    walk(v)
        walk(sh)
        if k == 'icon':
            n = len(sh.get('icons', []))
            for ic in sh.get('icons', []):
                if ic.get('name') not in ICONS:
                    err.append(f'shot {i}: unknown icon {ic.get("name")}')
                if n > 1 and len(ic.get('label', '')) > (14 if n >= 3 else 18):
                    err.append(f'shot {i}: icon label too long for {n} icons: {ic["label"]!r}')
                if not isinstance(ic.get('at'), (int, float)) or ic['at'] > 0.6:
                    warn.append(f'shot {i}: icon at {ic.get("at")!r} (use 0.04..0.55 so the screen is never empty)')
                if ic.get('name') == 'book' and ic.get('text'):
                    err.append(f'shot {i}: book icon with text overflows')
        if k == 'table':
            for it in sh.get('items', []):
                if not isinstance(it.get('at'), (int, float)):
                    warn.append(f'shot {i}: table item at {it.get("at")!r} (use 0.04)')
        if k == 'counter' and not isinstance(sh.get('value', {}).get('at'), (int, float)):
            warn.append(f'shot {i}: counter at should be a number (0.06)')
        if '→' in json.dumps(sh, ensure_ascii=False):
            err.append(f'shot {i}: arrow glyph not in font')
    if cov != list(range(len(S))):
        bad = [x for x in range(len(S)) if cov.count(x) != 1]
        err.append(f'sentence coverage broken at {bad[:10]} (need each 0..{len(S)-1} exactly once, in order)')
    for f in ('title', 'description', 'tags'):
        if not meta.get(f):
            err.append(f'meta.json: {f} missing')
    if meta.get('thumb') and 'shot' in meta['thumb'] and not (0 <= int(meta['thumb']['shot']) < len(st['shots'])):
        err.append('meta.json: thumb.shot out of range')
    print(f'{len(S)} sentences, {len(st["shots"])} shots, {words} words ≈ {words/150:.1f} min')
    for w in warn:
        print('WARN', w)
    for e in err:
        print('ERROR', e)
    print('OK' if not err else 'FAILED')
    sys.exit(1 if err else 0)


if __name__ == '__main__':
    main(sys.argv[1])
