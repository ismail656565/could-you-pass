"""COULD YOU PASS? – Autopilot (läuft in GitHub Actions oder lokal)

  python autopilot/autopilot.py auth        einmalig: bei Google anmelden (öffnet Browser)
  python autopilot/autopilot.py analytics   Zahlen aller Videos holen -> autopilot/analytics/report.json
  python autopilot/autopilot.py produce     nächstes Quiz aus autopilot/queue/ vertonen, rendern, hochladen
  python autopilot/autopilot.py all         analytics + produce (das macht die tägliche Aufgabe)

Benötigt (setup.bat installiert alles):
  autopilot/.env               ELEVENLABS_API_KEY=...  (optional ELEVEN_VOICE=Roger, PRIVACY=public)
  autopilot/client_secret.json Google-OAuth-Client (Desktop-App)
"""
import datetime as dt
import json
import os
import re
import shutil
import subprocess
import sys
import time
import traceback
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent  # Projektordner wildly-true
AP = ROOT / 'autopilot'
QUEUE = AP / 'queue'
DONE = QUEUE / 'done'
FAILED = QUEUE / 'failed'
ANALYTICS = AP / 'analytics'
LOG = AP / 'log.txt'
SR = 44100

SCOPES = [
    'https://www.googleapis.com/auth/youtube.upload',
    'https://www.googleapis.com/auth/youtube.readonly',
    'https://www.googleapis.com/auth/youtube.force-ssl',
    'https://www.googleapis.com/auth/yt-analytics.readonly',
]

# Timing (wie bisher von Hand)
TEMPO = 1.07
GAP_Q = 0.15
COUNT = 2.5
GAP_A = 0.05
TAIL = 1.0


def log(*a):
    line = f"[{dt.datetime.now():%Y-%m-%d %H:%M:%S}] " + ' '.join(str(x) for x in a)
    print(line, flush=True)
    with open(LOG, 'a', encoding='utf-8') as f:
        f.write(line + '\n')


def env():
    e = {}
    p = AP / '.env'
    if p.exists():
        for line in p.read_text(encoding='utf-8').splitlines():
            if '=' in line and not line.strip().startswith('#'):
                k, v = line.split('=', 1)
                e[k.strip()] = v.strip().strip('"')
    return e


def ffmpeg_bin():
    try:
        import imageio_ffmpeg
        return imageio_ffmpeg.get_ffmpeg_exe()
    except Exception:
        return 'ffmpeg'


# ---------------------------------------------------------------- Google
def creds():
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    # Cloud (GitHub Actions): Zugang aus verschlüsselten Secrets
    if os.environ.get('GOOGLE_REFRESH_TOKEN'):
        c = Credentials(None, refresh_token=os.environ['GOOGLE_REFRESH_TOKEN'], token_uri='https://oauth2.googleapis.com/token',
                        client_id=os.environ['GOOGLE_CLIENT_ID'], client_secret=os.environ['GOOGLE_CLIENT_SECRET'], scopes=SCOPES)
        c.refresh(Request())
        return c
    tok = AP / 'token.json'
    c = None
    if tok.exists():
        c = Credentials.from_authorized_user_file(str(tok), SCOPES)
    if c and c.valid:
        return c
    if c and c.expired and c.refresh_token:
        c.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(str(AP / 'client_secret.json'), SCOPES)
        c = flow.run_local_server(port=0, access_type='offline', prompt='select_account consent')
    tok.write_text(c.to_json(), encoding='utf-8')
    return c


def yt():
    from googleapiclient.discovery import build
    return build('youtube', 'v3', credentials=creds(), cache_discovery=False)


def yta():
    from googleapiclient.discovery import build
    return build('youtubeAnalytics', 'v2', credentials=creds(), cache_discovery=False)


# ---------------------------------------------------------------- Analytics
def analytics():
    y = yt()
    ch = y.channels().list(part='contentDetails,statistics,snippet', mine=True).execute()['items'][0]
    uploads = ch['contentDetails']['relatedPlaylists']['uploads']
    vids = []
    tok = None
    while True:
        r = y.playlistItems().list(part='contentDetails,snippet', playlistId=uploads, maxResults=50, pageToken=tok).execute()
        for it in r['items']:
            vids.append({'id': it['contentDetails']['videoId'], 'title': it['snippet']['title'], 'published': it['contentDetails'].get('videoPublishedAt')})
        tok = r.get('nextPageToken')
        if not tok or len(vids) >= 100:
            break
    a = yta()
    today = dt.date.today().isoformat()
    by_id = {v['id']: v for v in vids}
    for metrics in ('views,engagedViews,averageViewDuration,averageViewPercentage,likes,comments,subscribersGained',
                    'views,averageViewDuration,averageViewPercentage,likes,comments,subscribersGained'):
        try:
            rep = a.reports().query(ids='channel==MINE', startDate='2020-01-01', endDate=today, metrics=metrics,
                                    dimensions='video', sort='-views', maxResults=200).execute()
            cols = [h['name'] for h in rep['columnHeaders']]
            for row in rep.get('rows', []):
                d = dict(zip(cols, row))
                if d['video'] in by_id:
                    by_id[d['video']].update({k: v for k, v in d.items() if k != 'video'})
            break
        except Exception as ex:
            log('Analytics-Abfrage fehlgeschlagen, versuche einfachere:', ex)
    # Retention-Kurve für die 10 neuesten Videos
    for v in vids[:10]:
        try:
            rep = a.reports().query(ids='channel==MINE', startDate='2020-01-01', endDate=today,
                                    metrics='audienceWatchRatio,relativeRetentionPerformance',
                                    dimensions='elapsedVideoTimeRatio', filters=f"video=={v['id']}").execute()
            v['retention'] = [[round(r[0], 2), round(r[1], 3), round(r[2], 3)] for r in rep.get('rows', [])]
        except Exception as ex:
            v['retentionError'] = str(ex)[:200]
    # Woher kommen die Aufrufe? (Traffic-Quellen, v. a. für lange Videos wichtig)
    for v in vids[:15]:
        try:
            rep = a.reports().query(ids='channel==MINE', startDate='2020-01-01', endDate=today, metrics='views',
                                    dimensions='insightTrafficSourceType', filters=f"video=={v['id']}", sort='-views').execute()
            v['trafficSources'] = {r[0]: r[1] for r in rep.get('rows', [])}
        except Exception as ex:
            v['trafficError'] = str(ex)[:150]
        try:
            rep = a.reports().query(ids='channel==MINE', startDate='2020-01-01', endDate=today, filters=f"video=={v['id']}",
                                    metrics='videoThumbnailImpressions,videoThumbnailImpressionsClickRate').execute()
            row = (rep.get('rows') or [[None, None]])[0]
            v['impressions'], v['ctr'] = row[0], row[1]
        except Exception as ex:
            v['ctrError'] = str(ex)[:150]
    # Länge der Videos
    for i in range(0, len(vids), 50):
        ids = ','.join(v['id'] for v in vids[i:i + 50])
        for it in y.videos().list(part='contentDetails,statistics', id=ids).execute().get('items', []):
            m = re.match(r'PT(?:(\d+)M)?(?:(\d+)S)?', it['contentDetails']['duration'])
            by_id[it['id']]['durationSec'] = int(m.group(1) or 0) * 60 + int(m.group(2) or 0) if m else None
            by_id[it['id']]['publicViews'] = it['statistics'].get('viewCount')
    for v in vids:
        if v.get('views') and v.get('engagedViews') is not None:
            v['engagedShare'] = round(v['engagedViews'] / max(1, v['views']), 3)
    ANALYTICS.mkdir(parents=True, exist_ok=True)
    log(f"Kanal: {ch['snippet']['title']} | Kontrollnummer: {os.environ.get('GOOGLE_REFRESH_TOKEN', '')[-4:]}")
    report = {'fetched': dt.datetime.now().isoformat(timespec='minutes'), 'channel': ch['snippet']['title'],
              'subscribers': ch['statistics'].get('subscriberCount'), 'videos': vids}
    (ANALYTICS / 'report.json').write_text(json.dumps(report, indent=1, ensure_ascii=False), encoding='utf-8')
    (ANALYTICS / f'report-{today}.json').write_text(json.dumps(report, ensure_ascii=False), encoding='utf-8')
    log(f'Analytics gespeichert ({len(vids)} Videos)')


# ---------------------------------------------------------------- Stimme
def voice_id(key, name):
    import requests
    r = requests.get('https://api.elevenlabs.io/v1/voices', headers={'xi-api-key': key}, timeout=60)
    r.raise_for_status()
    for v in r.json().get('voices', []):
        if v['name'].lower().startswith(name.lower()):
            return v['voice_id']
    raise RuntimeError(f'Stimme "{name}" nicht gefunden')


def tts(key, vid, text, model):
    import requests
    for attempt in range(3):
        r = requests.post(f'https://api.elevenlabs.io/v1/text-to-speech/{vid}?output_format=mp3_44100_128',
                          headers={'xi-api-key': key, 'Content-Type': 'application/json'},
                          json={'text': text, 'model_id': model}, timeout=120)
        if r.ok:
            return r.content
        log('ElevenLabs-Fehler', r.status_code, r.text[:200])
        time.sleep(5)
    r.raise_for_status()


def decode(mp3_bytes, tmp, tempo=None):
    import numpy as np
    p = tmp / 'x.audio'
    p.write_bytes(mp3_bytes)
    raw = subprocess.run([ffmpeg_bin(), '-v', 'error', '-i', str(p), '-af', f'atempo={tempo or TEMPO}', '-f', 'f32le', '-ac', '1', '-ar', str(SR), '-'],
                         capture_output=True, check=True).stdout
    a = np.frombuffer(raw, dtype=np.float32).copy()
    # Stille am Anfang/Ende abschneiden
    thr = 0.012
    idx = np.where(np.abs(a) > thr)[0]
    if len(idx):
        a = a[max(0, idx[0] - int(0.03 * SR)): min(len(a), idx[-1] + int(0.06 * SR))]
    return a


_KOKORO = None
# Kanalstimme: Mischung zweier britischer Kokoro-Stimmen (klingt nicht wie die Standard-KI-Stimme af_heart)
DEFAULT_VOICE = 'bf_emma:70+bf_isabella:30'


def kokoro_voice(voice):
    """'bf_emma' oder Mischung 'bf_emma:70+bf_isabella:30' (eigene Stimme, die es so nirgends gibt)"""
    if '+' not in voice and ':' not in voice:
        return voice
    import numpy as np
    vs = np.load(str(ROOT / 'models' / 'voices-v1.0.bin'))
    parts = [(p.split(':')[0].strip(), float(p.split(':')[1]) if ':' in p else 1.0) for p in voice.split('+')]
    tot = sum(w for _, w in parts)
    return sum(vs[n].astype('float32') * (w / tot) for n, w in parts)


def kokoro_wav(text, voice, speed=1.0):
    """Kostenlose Stimme (Kokoro, Apache-2.0) – Modell liegt in models/ (vom Workflow geladen)"""
    global _KOKORO
    import io
    import soundfile as sf
    if _KOKORO is None:
        from kokoro_onnx import Kokoro
        m = ROOT / 'models'
        _KOKORO = Kokoro(str(m / 'kokoro-v1.0.onnx'), str(m / 'voices-v1.0.bin'))
    samples, sr = _KOKORO.create(text, voice=kokoro_voice(voice), speed=speed, lang='en-gb' if voice.startswith('b') else 'en-us')
    buf = io.BytesIO()
    sf.write(buf, samples, sr, format='WAV')
    return buf.getvalue()


def make_speaker(item):
    """liefert speak(text) -> Audiodaten; Standard Kokoro (kostenlos), ElevenLabs nur wenn item/Umgebung "elevenlabs" sagt"""
    e = env()
    engine = item.get('tts') or e.get('TTS') or os.environ.get('TTS') or 'kokoro'
    if engine == 'kokoro':
        voice = item.get('voice') or e.get('KOKORO_VOICE') or os.environ.get('KOKORO_VOICE') or DEFAULT_VOICE
        log(f'Stimme: Kokoro {voice}')
        speed = float(item.get('voiceSpeed') or e.get('KOKORO_SPEED') or os.environ.get('KOKORO_SPEED') or 1.0)
        return lambda text: kokoro_wav(text, voice, speed)
    key = e.get('ELEVENLABS_API_KEY') or os.environ.get('ELEVENLABS_API_KEY')
    if not key:
        raise RuntimeError('ELEVENLABS_API_KEY fehlt')
    vid = e.get('ELEVEN_VOICE_ID') or voice_id(key, e.get('ELEVEN_VOICE', 'Roger'))
    model = e.get('ELEVEN_MODEL', 'eleven_multilingual_v2')
    log('Stimme: ElevenLabs')
    return lambda text: tts(key, vid, text, model)


def build_audio(item, out_mp3):
    import numpy as np
    speak = make_speaker(item)
    tmp = AP / 'tmp'
    tmp.mkdir(exist_ok=True)
    story = item['story']
    qs = story['questions']
    lines = item['lines']
    assert len(lines) == len(qs), 'lines und questions passen nicht zusammen'
    tm = item.get('timing', {})
    count, tail = tm.get('count', COUNT), tm.get('tail', TAIL)
    tempo = tm.get('tempo', TEMPO)
    out, t = [], 0.0

    def put(x):
        nonlocal t
        out.append(x)
        t += len(x) / SR

    z = lambda s: np.zeros(int(round(s * SR)), np.float32)
    for q, ln in zip(qs, lines):
        qa = decode(speak(ln['q']), tmp, tempo)
        aa = decode(speak(ln['a']), tmp, tempo)
        q['start'] = round(t, 3)
        put(qa)
        put(z(GAP_Q))
        q['countdownStart'] = round(t, 3)
        put(z(count))
        q['reveal'] = round(t, 3)
        put(z(GAP_A))
        put(aa)
        put(z(tail))
        q['end'] = round(t, 3)
    story['outroStart'] = round(t, 3)
    if item.get('outroLine'):  # Abspann mit Abo-Aufruf (lange Videos)
        put(z(0.4))
        put(decode(speak(item['outroLine']), tmp, tempo))
        put(z(item.get('outroHold', 4.0)))
    story['durationInSeconds'] = round(t, 3)  # ohne outroLine kein Abspann -> Video loopt
    full = np.concatenate(out)
    full = full / (np.max(np.abs(full)) or 1) * 0.95
    subprocess.run([ffmpeg_bin(), '-v', 'error', '-y', '-f', 'f32le', '-ar', str(SR), '-ac', '1', '-i', '-', '-ar', '44100', '-b:a', '160k', str(out_mp3)],
                   input=full.tobytes(), check=True)
    shutil.rmtree(tmp, ignore_errors=True)
    log(f'Ton fertig: {t:.1f} s')


# ---------------------------------------------------------------- Upload
PUBLISH_AT = {'short': '16:00', 'long': '14:00'}  # deutsche Uhrzeit
SHORT_SLOTS = ['16:00', '21:00']  # bis zu 2 Shorts pro Tag (UK-Nachmittag / US-Nachmittag)
PER_DAY = {'short': len(SHORT_SLOTS), 'long': 1}


def publish_time(item):
    """Veröffentlichungszeit heute (Europe/Berlin) – None, wenn schon (fast) vorbei → sofort öffentlich"""
    from zoneinfo import ZoneInfo
    at = item.get('publishAt') or PUBLISH_AT.get(fmt_of(item))
    if not at:
        return None
    tz = ZoneInfo('Europe/Berlin')
    now = dt.datetime.now(tz)
    h, m = map(int, at.split(':'))
    when = now.replace(hour=h, minute=m, second=0, microsecond=0)
    return when if when - now > dt.timedelta(minutes=10) else None


def post_pending_comments():
    """Erst-Kommentar posten, sobald ein geplantes Video öffentlich ist"""
    y = None
    for d in sorted(DONE.glob('*.json')):
        item = json.loads(d.read_text(encoding='utf-8'))
        vid = item.get('uploaded', {}).get('videoId')
        if not item.get('pendingComment') or not vid:
            continue
        y = y or yt()
        st = (y.videos().list(part='status', id=vid).execute().get('items') or [{}])[0].get('status', {})
        if st.get('privacyStatus') != 'public':
            log(f"{item['id']}: noch nicht öffentlich – Kommentar später")
            continue
        try:
            y.commentThreads().insert(part='snippet', body={'snippet': {'videoId': vid, 'topLevelComment': {'snippet': {'textOriginal': item['youtube']['comment']}}}}).execute()
            log(f"{item['id']}: Kommentar gepostet")
            item.pop('pendingComment', None)
            d.write_text(json.dumps(item, indent=1, ensure_ascii=False), encoding='utf-8')
        except Exception as ex:
            log('Kommentar nicht möglich:', str(ex)[:200])


def with_chapters(item, desc):
    """Lange Videos: Kapitel (0:00 Easy, … Legend, Ergebnis) automatisch in die Beschreibung – hilft Suche & Zuschauern"""
    story = item.get('story', {})
    if story.get('format') != 'long' or '0:00' in desc:
        return desc
    fmt = lambda t: f"{int(t // 60)}:{int(t % 60):02d}"
    ch, last = [], None
    for i, q in enumerate(story.get('questions', [])):
        lv = (q.get('level') or '').strip()
        if lv and lv != last:
            ch.append((0 if not ch else q.get('start', 0), f"{lv.title()} (Question {i + 1})"))
            last = lv
    if story.get('outroStart') and story.get('durationInSeconds', 0) - story['outroStart'] > 10:
        ch.append((story['outroStart'], 'Your score'))
    ch = [c for j, c in enumerate(ch) if j == 0 or c[0] - ch[j - 1][0] >= 10]
    if len(ch) < 3:
        return desc
    return desc.rstrip() + '\n\nChapters:\n' + '\n'.join(f'{fmt(t)} {n}' for t, n in ch)


def playlist_name(item):
    if item.get('playlist'):
        return item['playlist']
    st = item.get('story', {})
    text = (st.get('header', '') + ' ' + item.get('youtube', {}).get('title', '')).lower()
    if st.get('format') != 'long':
        return 'Quiz Shorts – New Quiz Every Day 🧠'
    if 'halloween' in text:
        return 'Halloween Quizzes 🎃'
    if any(k in text for k in ('football', 'soccer', 'league', 'world cup', 'nba', 'sport')):
        return 'Football & Sports Quizzes ⚽'
    if 'emoji' in text:
        return 'Emoji Quizzes 🤔'
    return 'General Knowledge & Memory Quizzes 🧠'


_PLAYLISTS = None


def add_to_playlist(y, vid, name):
    """Video in passende Playlist (wird bei Bedarf angelegt) – Playlists bringen 'Vorgeschlagen'-Aufrufe und längere Sitzungen"""
    global _PLAYLISTS
    if _PLAYLISTS is None:
        _PLAYLISTS, tok = {}, None
        while True:
            r = y.playlists().list(part='snippet', mine=True, maxResults=50, pageToken=tok).execute()
            for p in r.get('items', []):
                _PLAYLISTS[p['snippet']['title']] = p['id']
            tok = r.get('nextPageToken')
            if not tok:
                break
    if name not in _PLAYLISTS:
        p = y.playlists().insert(part='snippet,status', body={
            'snippet': {'title': name, 'description': 'A new quiz every day from COULD YOU PASS? – how many can you get right? Subscribe & turn on the bell 🔔',
                        'defaultLanguage': 'en'},
            'status': {'privacyStatus': 'public'}}).execute()
        _PLAYLISTS[name] = p['id']
        log('Playlist angelegt:', name)
    for attempt in range(4):  # frisch angelegte Playlists liefern anfangs 409 "aborted"
        try:
            y.playlistItems().insert(part='snippet', body={'snippet': {'playlistId': _PLAYLISTS[name],
                                                                      'resourceId': {'kind': 'youtube#video', 'videoId': vid}}}).execute()
            log(f'In Playlist "{name}"')
            return
        except Exception:
            if attempt == 3:
                raise
            time.sleep(5 * (attempt + 1))


def already_uploaded(y, title):
    """Schutz gegen Doppel-Uploads: gleicher Titel unter den letzten 15 Kanal-Uploads (inkl. geplante/private)?"""
    ch = y.channels().list(part='contentDetails', mine=True).execute()['items'][0]
    up = ch['contentDetails']['relatedPlaylists']['uploads']
    r = y.playlistItems().list(part='snippet', playlistId=up, maxResults=15).execute()
    for it in r.get('items', []):
        if it['snippet']['title'].strip() == title.strip()[:100]:
            return it['snippet']['resourceId']['videoId']
    return None


def upload(item, mp4):
    from googleapiclient.http import MediaFileUpload
    meta = item['youtube']
    dup = already_uploaded(yt(), meta['title'])
    if dup:
        log(f'Schon hochgeladen ({dup}) – kein zweiter Upload')
        return dup
    privacy = env().get('PRIVACY') or os.environ.get('PRIVACY', 'public')
    body = {
        'snippet': {'title': meta['title'][:100], 'description': with_chapters(item, meta.get('description', '')), 'tags': meta.get('tags', []),
                    'categoryId': meta.get('categoryId', '24'), 'defaultLanguage': 'en', 'defaultAudioLanguage': 'en'},
        'status': {'privacyStatus': privacy, 'selfDeclaredMadeForKids': False},
    }
    when = publish_time(item) if privacy == 'public' else None
    if when:
        body['status'].update({'privacyStatus': 'private', 'publishAt': when.astimezone(dt.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')})
        item['scheduledFor'] = when.isoformat(timespec='minutes')
    y = yt()
    req = y.videos().insert(part='snippet,status', body=body, media_body=MediaFileUpload(str(mp4), chunksize=-1, resumable=True))
    resp = None
    while resp is None:
        _, resp = req.next_chunk()
    vid = resp['id']
    log(f'Hochgeladen: https://youtube.com/watch?v={vid} ({resp["status"].get("privacyStatus")})')
    thumb = item.get('_thumb')
    if thumb and Path(thumb).exists():
        try:
            y.thumbnails().set(videoId=vid, media_body=MediaFileUpload(thumb)).execute()
            log('Vorschaubild gesetzt')
        except Exception as ex:
            log('Vorschaubild nicht möglich (Kanal evtl. nicht per Telefon bestätigt):', str(ex)[:200])
    try:
        add_to_playlist(y, vid, playlist_name(item))
        item['playlistAdded'] = True
    except Exception as ex:
        log('Playlist nicht möglich:', str(ex)[:200])
    if meta.get('comment') and when:
        item['pendingComment'] = True
        log(f"Geplant für {when:%d.%m. %H:%M} Uhr (Berlin) – Kommentar folgt nach Veröffentlichung")
    elif meta.get('comment'):
        try:
            y.commentThreads().insert(part='snippet', body={'snippet': {'videoId': vid, 'topLevelComment': {'snippet': {'textOriginal': meta['comment']}}}}).execute()
            log('Kommentar gepostet')
        except Exception as ex:
            log('Kommentar nicht möglich:', ex)
    return vid


# ---------------------------------------------------------------- Ablauf
def item_force(p):
    try:
        return bool(json.loads(p.read_text(encoding='utf-8')).get('force'))
    except Exception:
        return False


def fmt_of(item):
    return 'long' if item.get('story', {}).get('format') == 'long' else 'short'


THUMBS = AP / 'thumbs'


def render_thumbs(name, story):
    """3 Vorschaubild-Varianten (A neon, B gelb-comic, C rot-challenge) für den automatischen Thumbnail-Test"""
    THUMBS.mkdir(parents=True, exist_ok=True)
    out = []
    for v in ('A', 'B', 'C'):
        f = THUMBS / f'{name}-{v}.jpg'
        props = ROOT / 'out' / f'.thumb-{name}-{v}.json'
        props.parent.mkdir(exist_ok=True)
        props.write_text(json.dumps({**story, 'thumbVariant': v}, ensure_ascii=False), encoding='utf-8')
        subprocess.run(['npx', 'remotion', 'still', 'QuizThumb', str(f), f'--props={props}', '--jpeg-quality=90'], cwd=ROOT, shell=(os.name == 'nt'))
        if f.exists():
            out.append((v, str(f)))
        else:
            log(f'Vorschaubild {v} nicht gerendert')
    return out


def thumb_score(a, vid, start, end):
    """Klickrate (CTR) des Vorschaubilds im Zeitraum; falls die API das nicht liefert: Aufrufe pro Tag"""
    try:
        rep = a.reports().query(ids='channel==MINE', startDate=start, endDate=end, filters=f'video=={vid}',
                                metrics='videoThumbnailImpressions,videoThumbnailImpressionsClickRate').execute()
        row = (rep.get('rows') or [[0, 0]])[0]
        return {'impressions': int(row[0] or 0), 'ctr': round(float(row[1] or 0), 4), 'metric': 'ctr'}
    except Exception as ex:
        rep = a.reports().query(ids='channel==MINE', startDate=start, endDate=end, filters=f'video=={vid}', metrics='views').execute()
        views = int(((rep.get('rows') or [[0]])[0])[0] or 0)
        days = max(1, (dt.date.fromisoformat(end) - dt.date.fromisoformat(start)).days)
        return {'views': views, 'ctr': round(views / days, 2), 'metric': 'views/day', 'note': str(ex)[:120]}


def thumb_rotate():
    """Automatischer Thumbnail-Test für lange Videos: jede Variante ~3 Tage, danach die beste behalten"""
    from googleapiclient.http import MediaFileUpload
    TEST_DAYS, MIN_IMPR, MAX_DAYS = 4, 200, 8  # Analytics hängt 2–3 Tage hinterher
    today = dt.date.today()
    a = y = None
    for d in sorted(DONE.glob('*.json')):
        item = json.loads(d.read_text(encoding='utf-8'))
        t = item.get('thumbTest')
        vid = item.get('uploaded', {}).get('videoId')
        if not t or t.get('done') or not vid:
            continue
        st_file = ROOT / 'stories' / f"{item['id']}.json"
        if any(not (THUMBS / f"{item['id']}-{v}.jpg").exists() for v in t['order'] if v != 'O') and st_file.exists():
            render_thumbs(item['id'], json.loads(st_file.read_text(encoding='utf-8')))
        since = dt.date.fromisoformat(t['since'])
        age = (today - since).days
        if age < TEST_DAYS:
            continue
        a = a or yta()
        y = y or yt()
        try:
            sc = thumb_score(a, vid, t['since'], today.isoformat())
        except Exception as ex:
            log('Thumbnail-Test: Abfrage fehlgeschlagen', vid, str(ex)[:200])
            continue
        if sc.get('metric') == 'ctr' and sc['impressions'] < MIN_IMPR and age < MAX_DAYS:
            log(f"Thumbnail-Test {item['id']}: Variante {t['current']} erst {sc['impressions']} Impressionen – warte noch")
            continue
        t['results'][t['current']] = {**sc, 'from': t['since'], 'to': today.isoformat()}
        log(f"Thumbnail-Test {item['id']}: Variante {t['current']} → {sc}")
        rest = [v for v in t['order'] if v not in t['results']]
        if rest:
            nxt = rest[0]
        else:
            have = [v for v in t['results'] if (THUMBS / f"{item['id']}-{v}.jpg").exists() or v == t['current']]
            nxt = max(have, key=lambda v: t['results'][v]['ctr'])
            t['done'] = True
            t['winner'] = nxt
        f = THUMBS / f"{item['id']}-{nxt}.jpg"
        if f.exists() and (nxt != t['current'] or not t.get('done')):
            try:
                y.thumbnails().set(videoId=vid, media_body=MediaFileUpload(str(f))).execute()
                log(f"Thumbnail-Test {item['id']}: jetzt Variante {nxt}" + (' (Gewinner)' if t.get('done') else ''))
            except Exception as ex:
                log('Thumbnail setzen fehlgeschlagen:', str(ex)[:200])
                continue
        t['current'] = nxt
        t['since'] = today.isoformat()
        item['thumbTest'] = t
        d.write_text(json.dumps(item, indent=1, ensure_ascii=False), encoding='utf-8')


def produce_one(p):
    item = json.loads(p.read_text(encoding='utf-8'))
    name = item['id']
    log(f'Produziere {name} ({fmt_of(item)})')
    try:
        story = item['story']
        story['audio'] = f'audio/{name}.mp3'
        build_audio(item, ROOT / 'public' / 'audio' / f'{name}.mp3')
        (ROOT / 'stories' / f'{name}.json').write_text(json.dumps(story, indent=1, ensure_ascii=False), encoding='utf-8')
        r = subprocess.run(['node', 'scripts/render.mjs', f'stories/{name}.json'], cwd=ROOT, shell=(os.name == 'nt'), capture_output=True, text=True)
        mp4 = ROOT / 'out' / f'{name}.mp4'
        if r.returncode != 0 or not mp4.exists():
            raise RuntimeError('Rendern fehlgeschlagen: ' + (r.stdout[-1500:] + r.stderr[-1500:]).replace('\n', ' | '))
        log('Gerendert')
        if story.get('format') == 'long':
            variants = render_thumbs(name, story)
            if variants:
                item['_thumb'] = variants[0][1]
                item['thumbTest'] = {'order': [v for v, _ in variants], 'current': variants[0][0],
                                     'since': dt.date.today().isoformat(), 'results': {}, 'done': False}
        vid = upload(item, mp4)
        item['uploaded'] = {'videoId': vid, 'at': dt.datetime.now().isoformat(timespec='minutes')}
        DONE.mkdir(exist_ok=True)
        (DONE / p.name).write_text(json.dumps(item, indent=1, ensure_ascii=False), encoding='utf-8')
        p.unlink()
    except Exception:
        log('FEHLER:', traceback.format_exc())
        FAILED.mkdir(exist_ok=True)
        shutil.move(str(p), str(FAILED / p.name))


def produce():
    """pro Tag höchstens 1 Short und 1 langes Video (außer "force": true)"""
    QUEUE.mkdir(parents=True, exist_ok=True)
    items = sorted(p for p in QUEUE.glob('*.json'))
    if not items:
        log('Warteschlange leer – heute kein Video.')
        return
    today = dt.date.today().isoformat()
    done_today = {}
    for d in DONE.glob('*.json'):
        try:
            di = json.loads(d.read_text(encoding='utf-8'))
            if di.get('uploaded', {}).get('at', '').startswith(today):
                done_today[fmt_of(di)] = done_today.get(fmt_of(di), 0) + 1
        except Exception:
            pass
    for f in ('short', 'long'):
        while True:
            cand = [p for p in sorted(QUEUE.glob('*.json')) if fmt_of(json.loads(p.read_text(encoding='utf-8'))) == f]
            if not cand:
                log(f'Kein {f}-Video in der Warteschlange.')
                break
            n = done_today.get(f, 0)
            if n >= PER_DAY[f] and not item_force(cand[0]):
                log(f'Heute schon {n} {f}-Video(s) hochgeladen – nächstes morgen.')
                break
            if f == 'short' and n < len(SHORT_SLOTS):
                it = json.loads(cand[0].read_text(encoding='utf-8'))
                if not it.get('publishAt'):
                    it['publishAt'] = SHORT_SLOTS[n]
                    cand[0].write_text(json.dumps(it, ensure_ascii=False, indent=1), encoding='utf-8')
            produce_one(cand[0])
            done_today[f] = n + 1
            if cand[0].exists():  # nicht verschoben (Fehler) → nicht endlos wiederholen
                break
    try:
        link_short_to_long(today)
    except Exception as ex:
        log('Verlinkung Short → langes Video fehlgeschlagen:', str(ex)[:200])


def link_short_to_long(today):
    """Beschreibung der heutigen Shorts um den Link zum heutigen langen Video ergänzen (Shorts-Zuschauer → lange Videos → Abos)"""
    shorts, long_item = [], None
    for d in DONE.glob('*.json'):
        it = json.loads(d.read_text(encoding='utf-8'))
        if it.get('uploaded', {}).get('at', '').startswith(today):
            if fmt_of(it) == 'long':
                long_item = it
            elif not it.get('linkedLong'):
                shorts.append((d, it))
    if not long_item or not shorts:
        return
    long_id = long_item['uploaded']['videoId']
    y = yt()
    for d, short in shorts:
        v = y.videos().list(part='snippet', id=short['uploaded']['videoId']).execute()['items'][0]
        sn = v['snippet']
        sn['description'] = f"▶ Full {len(long_item['story']['questions'])}-question quiz: https://youtu.be/{long_id}\n\n" + sn.get('description', '')
        y.videos().update(part='snippet', body={'id': v['id'], 'snippet': {k: sn[k] for k in ('title', 'description', 'tags', 'categoryId') if k in sn}}).execute()
        short['linkedLong'] = long_id
        d.write_text(json.dumps(short, indent=1, ensure_ascii=False), encoding='utf-8')
        log(f'Short-Beschreibung ({short["id"]}) verlinkt auf langes Video {long_id}')


def main():
    cmd = sys.argv[1] if len(sys.argv) > 1 else 'all'
    AP.mkdir(exist_ok=True)
    if cmd == 'auth':
        creds()
        log('Google-Anmeldung gespeichert')
        tok = json.loads((AP / 'token.json').read_text(encoding='utf-8'))
        cs = json.loads((AP / 'client_secret.json').read_text(encoding='utf-8'))
        cs = cs.get('installed') or cs.get('web')
        print('\n=== Diese 3 Werte bei GitHub als Secrets eintragen ===')
        print('GOOGLE_CLIENT_ID     =', cs['client_id'])
        print('GOOGLE_CLIENT_SECRET =', cs['client_secret'])
        print('GOOGLE_REFRESH_TOKEN =', tok.get('refresh_token'))
        try:
            ch = yt().channels().list(part='snippet', mine=True).execute().get('items', [])
            print('\n>>> Angemeldeter YouTube-Kanal:', ', '.join(i['snippet']['title'] for i in ch) or 'KEINER')
        except Exception as ex:
            print('Kanal-Abfrage fehlgeschlagen:', ex)
        print('>>> Kontrollnummer (Ende des Tokens):', (tok.get('refresh_token') or '')[-4:])
    elif cmd == 'analytics':
        analytics()
    elif cmd == 'produce':
        produce()
    elif cmd == 'comments':
        post_pending_comments()
    elif cmd == 'private':
        # Videos auf privat stellen (z. B. versehentliche Doppel-Uploads): python autopilot.py private ID1 ID2
        y = yt()
        for vid in sys.argv[2:]:
            v = y.videos().list(part='status', id=vid).execute()['items'][0]
            st = v['status']
            st['privacyStatus'] = 'private'
            st.pop('publishAt', None)
            y.videos().update(part='status', body={'id': vid, 'status': st}).execute()
            log(f'{vid} auf privat gestellt')
    elif cmd == 'playlists':
        # bisherige Videos nachträglich in Playlists einsortieren
        y = yt()
        for d in sorted(DONE.glob('*.json')):
            it = json.loads(d.read_text(encoding='utf-8'))
            vid = it.get('uploaded', {}).get('videoId')
            if vid and not it.get('playlistAdded'):
                try:
                    add_to_playlist(y, vid, playlist_name(it))
                    it['playlistAdded'] = True
                    d.write_text(json.dumps(it, indent=1, ensure_ascii=False), encoding='utf-8')
                except Exception as ex:
                    log('Playlist-Fehler', vid, str(ex)[:200])
    elif cmd == 'dryrun':
        # Test ohne Upload: Ton + Video für alle Dateien in autopilot/test/
        for p in sorted((AP / 'test').glob('*.json')):
            item = json.loads(p.read_text(encoding='utf-8'))
            name = item['id']
            story = item['story']
            story['audio'] = f'audio/{name}.mp3'
            build_audio(item, ROOT / 'public' / 'audio' / f'{name}.mp3')
            (ROOT / 'stories' / f'{name}.json').write_text(json.dumps(story, indent=1, ensure_ascii=False), encoding='utf-8')
            r = subprocess.run(['node', 'scripts/render.mjs', f'stories/{name}.json'], cwd=ROOT, capture_output=True, text=True)
            if r.returncode:
                log('Render-Ausgabe:', (r.stdout[-1500:] + r.stderr[-1500:]).replace('\n', ' | '))
            log(f'Testlauf {name}: Render-Code {r.returncode}, Dauer {story["durationInSeconds"]} s')
    elif cmd == 'thumbs':
        # nur Vorschaubilder rendern: python autopilot.py thumbs stories/<id>.json
        st = json.loads(Path(sys.argv[2]).read_text(encoding='utf-8'))
        log('Thumbnails:', render_thumbs(Path(sys.argv[2]).stem, st))
    else:
        try:
            analytics()
        except Exception:
            log('Analytics-FEHLER:', traceback.format_exc())
        try:
            post_pending_comments()
        except Exception:
            log('Kommentar-FEHLER:', traceback.format_exc())
        try:
            thumb_rotate()
        except Exception:
            log('Thumbnail-Test-FEHLER:', traceback.format_exc())
        produce()


if __name__ == '__main__':
    main()
