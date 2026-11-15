"""WILDLY TRUE – Fakten-Shorts-Autopilot (eigener YouTube-Kanal, eigene Warteschlange)

Nutzt die Bausteine des Quiz-Autopiloten (Kokoro-Stimme, Wikimedia-B-Roll, QA, Upload),
aber mit eigenem Token, eigener Queue (autopilot/wildlytrue/queue) und eigenem Log.

  python autopilot/wildlytrue.py auth          einmalig LOKAL: Google-Anmeldung, Kanal "Wildly True" wählen
                                               -> Wert für das GitHub-Secret WT_GOOGLE_REFRESH_TOKEN
  python autopilot/wildlytrue.py check         Token + Kanalname prüfen (kein Upload)
  python autopilot/wildlytrue.py dryrun [ID]   ein Queue-Item vertonen + rendern, OHNE Upload (out/wt-<id>.mp4)
  python autopilot/wildlytrue.py analytics     Zahlen -> autopilot/wildlytrue/analytics/report.json
  python autopilot/wildlytrue.py comments      Erst-Kommentare unter veröffentlichte Videos
  python autopilot/wildlytrue.py all           analytics + 1 Short pro Tag produzieren/hochladen + Kommentare

Queue-Format (autopilot/wildlytrue/queue/<datum>-<id>.json):
  {"id": "...", "publishAt": "18:00", "youtube": {"title", "description", "tags", "comment"},
   "story": {"hookText": "400 YEARS OLD.", "music": "sfx/tension-loop.wav", "sources": [...],
             "beats": [{"text": "Ein Satz (3–5 s).", "broll": ["suchbegriff 1", "ersatz 2"]}, ...]}}
"""
import datetime as dt
import json
import os
import re
import shutil
import subprocess
import sys
import traceback
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import autopilot as A  # noqa: E402

WT = HERE / 'wildlytrue'
QUEUE = WT / 'queue'
DONE = QUEUE / 'done'
FAILED = QUEUE / 'failed'
# Alle Hilfsfunktionen des Quiz-Autopiloten schreiben ab hier in die Wildly-True-Ordner
A.QUEUE, A.DONE, A.FAILED, A.ANALYTICS, A.LOG = QUEUE, DONE, FAILED, WT / 'analytics', WT / 'log.txt'
log = A.log

_orig_candidates = A._commons_candidates


def _polite_candidates(query, sess):
    """Wikimedia-Suche mit Pause + Wiederholung bei 429 (viele Beats hintereinander)."""
    import time
    for attempt in range(4):
        time.sleep(1.5 + attempt * 6)
        try:
            return [c for c in _orig_candidates(query, sess) if _relevant(query, c['title'])]
        except Exception as ex:
            if '429' not in str(ex) or attempt == 3:
                raise


_STOP = {'with', 'from', 'over', 'into', 'slow', 'motion', 'close', 'video', 'footage', 'the', 'and'}


def _relevant(query, title):
    """Wikimedia-Suche ist unscharf (Probe 15.11.: "shrimp claw" → Dim-Sum-Kochvideo, "underwater bubbles" → Sternhaufen).
    Ein Clip zählt nur, wenn ein Kernwort der Suche im Dateinamen steht."""
    t = title.lower()
    # Studien-Begleitvideos (PLOS "pone.0077120.s0", Mikroskopie) haben Messbalken/Beschriftung im Bild → nicht nehmen
    if re.search(r'\b(pone|pbio|pcbi|ppat|journal|supplement|microscop|figure)\b|\.s\d{3}\b', t):
        return False
    words = [w for w in re.findall(r'[a-z]+', query.lower()) if len(w) > 3 and w not in _STOP]
    return any(w.rstrip('s') in t for w in words) if words else True


A._commons_candidates = _polite_candidates

CHANNEL_MATCH = 'wildly true'
PUBLISH_AT = '18:00'          # deutsche Zeit (US-Mittag)
PER_DAY = 1
DEFAULT_VOICE = 'am_michael:60+am_onyx:40'  # ruhige Doku-Männerstimme, eigene Mischung
PLAYLIST = 'Wildly True Facts 🌍'
# Eigenes Musikbett (scripts/make_wt_sounds.py): 120 BPM, Beat 1 bei 0,0 s → Schnitte rasten auf dieses Raster ein
MUSIC, BPM = 'sfx/wt-pulse.wav', 120
SNAP_MAX = 0.3      # Schnitt darf höchstens so weit vom Satzanfang auf den Takt rutschen
SPLIT_OVER = 3.4    # längere Einstellungen bekommen einen zusätzlichen Schnitt auf dem Takt (Tempo)
SENT = re.compile(r'(?<=[.!?])\s+')


# ---------------------------------------------------------------- Zugang
def use_wt_token():
    """Nie versehentlich mit dem Quiz-Token arbeiten: ohne WT-Token kein Google-Zugriff."""
    tok = os.environ.get('WT_GOOGLE_REFRESH_TOKEN', '').strip()
    if not tok:
        raise SystemExit('WT_GOOGLE_REFRESH_TOKEN fehlt – erst "python autopilot/wildlytrue.py auth" lokal ausführen '
                         'und den Wert als GitHub-Secret eintragen.')
    os.environ['GOOGLE_REFRESH_TOKEN'] = tok
    for k in ('CLIENT_ID', 'CLIENT_SECRET'):
        if os.environ.get(f'WT_GOOGLE_{k}'):
            os.environ[f'GOOGLE_{k}'] = os.environ[f'WT_GOOGLE_{k}']


def guard():
    """Bricht ab, wenn das Token nicht zum Kanal Wildly True gehört (Schutz vor Upload auf COULD YOU PASS?)."""
    items = A.yt().channels().list(part='snippet,statistics', mine=True).execute().get('items', [])
    titles = [i['snippet']['title'] for i in items]
    if not any(CHANNEL_MATCH in t.lower() for t in titles):
        raise SystemExit(f'FALSCHER KANAL: Token gehört zu {titles or "keinem Kanal"} – erwartet "Wildly True". Abbruch.')
    log(f"Kanal ok: {titles[0]} ({items[0]['statistics'].get('subscriberCount')} Abos)")


def auth():
    from google_auth_oauthlib.flow import InstalledAppFlow
    cs_path = HERE / 'client_secret.json'
    if not cs_path.exists():
        raise SystemExit('autopilot/client_secret.json fehlt (dieselbe Datei wie beim Quiz-Kanal).')
    print('Browser öffnet sich: Google-Konto wählen und dann den Kanal "WILDLY TRUE" auswählen!')
    flow = InstalledAppFlow.from_client_secrets_file(str(cs_path), A.SCOPES)
    c = flow.run_local_server(port=0, access_type='offline', prompt='select_account consent')
    from googleapiclient.discovery import build
    ch = build('youtube', 'v3', credentials=c, cache_discovery=False).channels().list(part='snippet', mine=True).execute()
    titles = [i['snippet']['title'] for i in ch.get('items', [])]
    print('\n>>> Angemeldeter Kanal:', ', '.join(titles) or 'KEINER')
    if not any(CHANNEL_MATCH in t.lower() for t in titles):
        print('!!! Das ist NICHT Wildly True. Bitte nochmal starten und beim Kanal-Auswahlschritt Wildly True wählen.')
        return
    print('\n=== Diesen Wert bei GitHub als Secret eintragen (Settings → Secrets and variables → Actions) ===')
    print('WT_GOOGLE_REFRESH_TOKEN =', c.refresh_token)
    print('(GOOGLE_CLIENT_ID / GOOGLE_CLIENT_SECRET vom Quiz-Kanal werden mitbenutzt.)')


# ---------------------------------------------------------------- Ton + Wortzeiten
def _trim(a, sr):
    import numpy as np
    idx = np.where(np.abs(a) > 0.012)[0]
    return a[max(0, idx[0] - int(0.03 * sr)): idx[-1] + int(0.08 * sr)] if len(idx) else a


def build_voice(item, name):
    """Satz für Satz mit Kokoro sprechen; Wortzeiten aus Satzlängen (Whisper wird nicht gebraucht).
    Setzt story.audio, story.captions, Start/Ende jedes Beats und story.durationInSeconds."""
    import io
    import numpy as np
    import soundfile as sf
    story = item['story']
    voice = item.get('voice') or DEFAULT_VOICE
    speed = float(item.get('voiceSpeed') or 1.05)
    log(f'Stimme: Kokoro {voice} ×{speed}')
    sr = None
    chunks, words, t = [], [], 0.25
    lead = np.zeros(int(0.25 * 24000), dtype=np.float32)
    chunks.append(lead)
    for b in story['beats']:
        b['start'] = round(t, 2)
        for s in [x for x in SENT.split(b['text'].strip()) if x]:
            a, sr = sf.read(io.BytesIO(A.kokoro_wav(s, voice, speed)), dtype='float32')
            a = _trim(a, sr)
            dur = len(a) / sr
            toks = s.split()
            weights = [len(re.sub(r'\W', '', w)) + 2 for w in toks]
            tot, acc = sum(weights), 0.0
            for w, wt in zip(toks, weights):
                d = dur * wt / tot
                words.append({'word': w, 'start': round(t + acc, 3), 'end': round(t + acc + d * 0.92, 3)})
                acc += d
            chunks.append(a)
            pause = 0.18 if s.rstrip().endswith(('.', '!', '?')) else 0.08
            chunks.append(np.zeros(int(pause * sr), dtype=np.float32))
            t += dur + pause
        b['end'] = round(t, 2)
    item['_voice'] = (np.concatenate(chunks), sr)
    story['audio'] = f'audio/{name}.mp3'
    story['captions'] = words
    story['durationInSeconds'] = round(t + 0.5, 2)
    story['beats'][-1]['end'] = story['durationInSeconds']
    log(f"Ton: {story['durationInSeconds']} s, {len(words)} Wörter, {len(story['beats'])} Beats")


# ---------------------------------------------------------------- Schnitt auf den Takt + Sounddesign
def cut_plan(story):
    """Schnitte auf das Musikraster legen (≤ SNAP_MAX vom Satzanfang) und lange Einstellungen auf dem Takt teilen.
    Liefert [(beat_index, teil, start, ende, versatz_im_clip)]."""
    g = 60 / BPM
    snap = lambda x: round(x / g) * g
    beats, dur = story['beats'], story['durationInSeconds']
    cuts = [0.0]
    for b in beats[1:]:
        c = snap(b['start'])
        if abs(c - b['start']) > SNAP_MAX or c - cuts[-1] < 1.0:
            c = b['start']
        cuts.append(round(c, 3))
    cuts.append(dur)
    shots = []
    for i in range(len(beats)):
        a, e = cuts[i], cuts[i + 1]
        parts = [a]
        if e - a > SPLIT_OVER:
            extra = int((e - a) // 2.2)
            for k in range(1, extra + 1):
                m = snap(a + (e - a) * k / (extra + 1))
                if m - parts[-1] >= 1.1 and e - m >= 1.1:
                    parts.append(round(m, 3))
        parts.append(e)
        for j in range(len(parts) - 1):
            # Sprungschnitt: im selben Clip 0,5 s weiter springen – wirkt wie ein neuer Blickwinkel
            shots.append((i, j, parts[j], parts[j + 1], round(parts[j] - a + 0.5 * j, 3)))
    return shots


def _load_sfx(rel, sr):
    import numpy as np
    import soundfile as sf
    a, r = sf.read(str(A.ROOT / 'public' / rel), dtype='float32')
    a = a.mean(1) if a.ndim > 1 else a
    if r != sr:
        a = np.interp(np.arange(0, len(a), r / sr), np.arange(len(a)), a).astype('float32')
    return a


def mix_audio(item, name):
    """Stimme + Impact (Hook, Schlüsselfakt) + leiser Whoosh auf jedem Schnitt → public/audio/<name>.mp3"""
    import numpy as np
    import soundfile as sf
    voice, sr = item.pop('_voice')
    story = item['story']
    out = np.zeros(int((story['durationInSeconds'] + 1.5) * sr), dtype=np.float32)
    out[:len(voice)] += voice
    boom, swish = _load_sfx('sfx/wt-boom.wav', sr), _load_sfx('sfx/wt-swish.wav', sr)

    def put(x, at, vol):
        s = max(0, int(at * sr))
        e = min(len(out), s + len(x))
        out[s:e] += x[:e - s] * vol

    put(boom, 0.0, 0.55)
    first_cut = {}
    for sc in story['scenes']:
        first_cut.setdefault(sc['_beat'], sc['start'])
    for sc in story['scenes'][1:]:
        put(swish, sc['start'] - 0.12, 0.22)
    for i, b in enumerate(story['beats']):
        if b.get('impact') and i in first_cut:
            put(boom, first_cut[i], 0.4)
    out = out[:int(story['durationInSeconds'] * sr)]
    peak = np.max(np.abs(out)) or 1
    out *= min(1.0, 0.95 / peak)
    mp3 = A.ROOT / 'public' / 'audio' / f'{name}.mp3'
    mp3.parent.mkdir(parents=True, exist_ok=True)
    wav = mp3.with_suffix('.wav')
    sf.write(str(wav), out, sr)
    subprocess.run([A.ffmpeg_bin(), '-v', 'error', '-y', '-i', str(wav), '-ar', '44100', '-b:a', '160k', str(mp3)], check=True)
    wav.unlink(missing_ok=True)
    for sc in story['scenes']:
        sc.pop('_beat', None)


# ---------------------------------------------------------------- Bild
def build_scenes(item, name):
    """Pro Beat ein echter Wikimedia-Clip (CC0/PD/CC BY/BY-SA). Fehlt einer, übernimmt der Nachbar-Clip.
    Ohne einen einzigen Clip wird abgebrochen (nie Platzhalter hochladen)."""
    story = item['story']
    beats = story['beats']
    credits = []
    max_try = max(len(b['broll']) if isinstance(b.get('broll'), list) else 1 for b in beats)
    for k in range(max_try):
        pending = []
        for b in beats:
            if b.get('video'):
                continue
            qs = b.get('broll') or []
            qs = [qs] if isinstance(qs, str) else qs
            if k < len(qs):
                # Puffer: Schnitt kann bis 0,3 s früher liegen, Sprungschnitte springen je 0,5 s weiter
                pending.append({'broll': qs[k], 'start': b['start'] - 0.4, 'end': b['end'] + 1.4, '_beat': b})
        if not pending:
            continue
        fake = {'questions': pending}
        credits += A.fetch_broll(fake, f'{name}-t{k}', max_clips=len(pending))
        for q in pending:
            if q.get('video'):
                q['_beat']['video'] = q['video']
    have = [b for b in beats if b.get('video')]
    if not have:
        raise RuntimeError('Kein einziger B-Roll-Clip gefunden – Video wird nicht produziert.')
    scenes = []
    for i, j, a, e, off in cut_plan(story):
        b = beats[i]
        src = b.get('video')
        if not src:  # Nachbar-Clip, versetzt gestartet, damit es nicht identisch wirkt
            near = sorted(have, key=lambda h: abs(beats.index(h) - i))[0]
            src = near['video']
            off += 1.5
            if j == 0:
                log(f'Beat {i + 1}: kein Clip – nutze Clip von Beat {beats.index(near) + 1}')
        scenes.append({'start': round(a, 3), 'end': round(e, 3), 'kind': 'video', 'src': src, '_beat': i,
                       **({'trimStart': off} if off > 0 else {})})
    story['scenes'] = scenes
    A.add_broll_credits(item, credits)
    log(f'Szenen: {len(have)}/{len(beats)} Beats mit eigenem Clip, {len(scenes)} Schnitte auf {BPM}-BPM-Raster')


# ---------------------------------------------------------------- Ablauf
def render(item, name):
    story = item['story']
    story.setdefault('title', item['youtube']['title'])
    story['script'] = ' '.join(b['text'] for b in story['beats'])
    story.setdefault('energy', 'normal')
    story.setdefault('brand', 'WILDLY TRUE')
    # Remotion mischt sonst die Beispiel-Props (stories/beispiel.json: Dateline 1972, Höhenzähler) hinein
    story.setdefault('datelines', [])
    story.setdefault('counters', [])
    if story.get('music'):
        story.setdefault('musicVolume', 0.11 if story['music'] == MUSIC else 0.08)
    sp = A.ROOT / 'stories' / f'{name}.json'
    sp.write_text(json.dumps(story, indent=1, ensure_ascii=False), encoding='utf-8')
    r = subprocess.run(['node', 'scripts/render.mjs', f'stories/{name}.json'], cwd=A.ROOT, shell=(os.name == 'nt'),
                       capture_output=True, text=True)
    mp4 = A.ROOT / 'out' / f'{name}.mp4'
    if r.returncode != 0 or not mp4.exists():
        raise RuntimeError('Rendern fehlgeschlagen: ' + (r.stdout[-1500:] + r.stderr[-1500:]).replace('\n', ' | '))
    log('Gerendert')
    A.qa_check(mp4, item)
    return mp4


def make_video(item):
    name = 'wt-' + item['id']
    build_voice(item, name)
    build_scenes(item, name)
    item['story'].setdefault('music', MUSIC)
    mix_audio(item, name)
    return render(item, name)


def produce_one(p, upload=True):
    item = json.loads(p.read_text(encoding='utf-8'))
    log(f"Produziere {item['id']}")
    try:
        mp4 = make_video(item)
        if not upload:
            log(f'Testlauf fertig: {mp4}')
            return mp4
        item.setdefault('publishAt', PUBLISH_AT)
        item.setdefault('playlist', PLAYLIST)
        item['youtube'].setdefault('categoryId', '27')  # Education
        src = item['story'].get('sources') or []
        if src and 'Sources:' not in item['youtube'].get('description', ''):
            item['youtube']['description'] = item['youtube'].get('description', '').rstrip() + '\n\nSources:\n' + '\n'.join(src)
        vid = A.upload(item, mp4)
        item['uploaded'] = {'videoId': vid, 'at': dt.datetime.now().isoformat(timespec='minutes')}
        DONE.mkdir(parents=True, exist_ok=True)
        (DONE / p.name).write_text(json.dumps(item, indent=1, ensure_ascii=False), encoding='utf-8')
        p.unlink()
    except Exception:
        log('FEHLER:', traceback.format_exc())
        if upload:
            FAILED.mkdir(parents=True, exist_ok=True)
            shutil.move(str(p), str(FAILED / p.name))
        raise


def uploaded_today():
    today = dt.date.today().isoformat()
    n = 0
    for d in DONE.glob('*.json'):
        try:
            n += json.loads(d.read_text(encoding='utf-8')).get('uploaded', {}).get('at', '').startswith(today)
        except Exception:
            pass
    return n


def produce():
    QUEUE.mkdir(parents=True, exist_ok=True)
    items = sorted(QUEUE.glob('*.json'))
    if uploaded_today() >= PER_DAY:
        log('Heute schon hochgeladen – nächstes morgen.')
        return
    if not items:
        log('WARNUNG: Wildly-True-Warteschlange leer – kein Upload heute.')
        return
    produce_one(items[0])


def main():
    cmd = sys.argv[1] if len(sys.argv) > 1 else 'all'
    WT.mkdir(exist_ok=True)
    if cmd == 'auth':
        return auth()
    if cmd == 'dryrun':
        QUEUE.mkdir(parents=True, exist_ok=True)
        want = sys.argv[2] if len(sys.argv) > 2 else ''
        items = [p for p in sorted(QUEUE.glob('*.json')) if want in p.name]
        if not items:
            raise SystemExit('Kein passendes Queue-Item.')
        tmp = WT / 'tmp-dryrun.json'
        shutil.copy(items[0], tmp)
        try:
            produce_one(tmp, upload=False)
        finally:
            tmp.unlink(missing_ok=True)
        return
    use_wt_token()
    guard()
    if cmd == 'check':
        return
    if cmd in ('analytics', 'all'):
        try:
            A.analytics()
        except Exception as ex:
            log('Analytics fehlgeschlagen:', str(ex)[:300])
    if cmd in ('produce', 'all'):
        produce()
    if cmd in ('comments', 'all'):
        A.post_pending_comments()


if __name__ == '__main__':
    main()
