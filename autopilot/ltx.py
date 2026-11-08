"""LTX-Video (https://ltx.io) für das Layout "stick": erzeugt pro Frage einen kurzen 2D-Doodle-Clip
für die Karte oben (q["video"]). Ohne LTX_API_KEY oder bei Fehlern bleibt die Frage bei Emoji/Foto.

Kosten (Stand 11/2026, ltx-2-3-fast, 1280x720): 0,03 $ pro Sekunde → 6-s-Clip = 0,18 $.
Budget pro Video: LTX_MAX_CLIPS (Standard 6). Bereits erzeugte Clips werden über den Prompt-Hash wiederverwendet.

Prompt-Quelle je Frage (darf die Antwort NIE verraten):
  q["ltx"]   – eigener Szenen-Prompt (bevorzugt), z. B. "a ladybug walking on a leaf"
  q["broll"] – sonst der B-Roll-Suchbegriff
  sonst      – das **Schlüsselwort** der Frage (ohne Zahlen)
"""
import hashlib
import json
import os
import re
import time
from pathlib import Path

import requests

API = 'https://api.ltx.io/v2/text-to-video'
STYLE = (
    '2D hand-drawn doodle animation, black ink line art on clean white paper, simple flat pastel color fills, '
    'cartoon notebook sketch style, smooth simple motion, centered subject, plain white background, '
    'no text, no letters, no numbers, no words, no watermark. Scene: '
)


def _log(*a):
    print('[LTX]', *a, flush=True)


def _generate(key, prompt, out, model, duration, resolution):
    h = {'Authorization': f'Bearer {key}', 'Content-Type': 'application/json'}
    body = {'prompt': prompt, 'model': model, 'duration': duration, 'resolution': resolution, 'generate_audio': False}
    r = requests.post(API, headers=h, json=body, timeout=60)
    if r.status_code >= 400:
        raise RuntimeError(f'Submit {r.status_code}: {r.text[:300]}')
    job = r.json()['id']
    deadline = time.time() + 600
    while time.time() < deadline:
        time.sleep(6)
        s = requests.get(f'{API}/{job}', headers=h, timeout=60).json()
        st = s.get('status')
        if st == 'completed':
            url = s['result']['video_url']
            v = requests.get(url, timeout=180)
            v.raise_for_status()
            out.write_bytes(v.content)
            return
        if st == 'failed':
            raise RuntimeError(f"Job fehlgeschlagen: {json.dumps(s.get('error'))[:300]}")
    raise RuntimeError('Zeitüberschreitung (10 min)')


def fetch_ltx(story, root: Path):
    """Setzt q["video"] = "ltx/<hash>.mp4" für Fragen mit Prompt. Gibt Anzahl neuer Clips zurück."""
    if story.get('layout') != 'stick':
        return 0
    key = os.environ.get('LTX_API_KEY')
    if not key:
        _log('kein LTX_API_KEY – Karten bleiben bei Emoji/Foto')
        return 0
    model = os.environ.get('LTX_MODEL', 'ltx-2-3-fast')
    duration = int(os.environ.get('LTX_DURATION', '6'))
    resolution = os.environ.get('LTX_RESOLUTION', '1280x720')
    budget = int(os.environ.get('LTX_MAX_CLIPS', '6'))
    outdir = root / 'public' / 'ltx'
    outdir.mkdir(parents=True, exist_ok=True)
    made = 0
    for i, q in enumerate(story.get('questions', [])):
        scene = (q.get('ltx') or q.get('broll') or '').strip()
        if not scene:  # Fallback: das **Schlüsselwort** der Frage als Motiv (verrät die Antwort nicht)
            m = re.search(r'\*\*([^*]+)\*\*', q.get('q', ''))
            kw = m.group(1).strip() if m else ''
            if kw and not re.search(r'\d', kw):
                scene = f'a cute friendly cartoon {kw}, gently moving, playful'
        if not scene or q.get('values') or q.get('image'):
            continue
        prompt = STYLE + scene
        h = hashlib.sha1(f'{model}|{duration}|{resolution}|{prompt}'.encode()).hexdigest()[:16]
        out = outdir / f'{h}.mp4'
        if not out.exists():
            if made >= budget:
                _log(f'Budget ({budget} Clips) erreicht – Frage {i + 1} bleibt bei Emoji')
                continue
            try:
                _generate(key, prompt, out, model, duration, resolution)
                made += 1
                _log(f'Frage {i + 1}: neuer Clip ({scene[:60]})')
            except Exception as ex:
                _log(f'Frage {i + 1} übersprungen:', str(ex)[:200])
                out.unlink(missing_ok=True)
                continue
        q['video'] = f'ltx/{out.name}'
    return made
