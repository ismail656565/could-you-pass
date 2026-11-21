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
import statistics
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
        # Thumbnail-Impressions/CTR sind über die hier verwendete Analytics-Abfrage nicht zuverlässig verfügbar.
        # thumb_score() versucht CTR separat und fällt bei API-Fehlern auf Views/Tag zurück.
    # Länge der Videos
    for i in range(0, len(vids), 50):
        ids = ','.join(v['id'] for v in vids[i:i + 50])
        for it in y.videos().list(part='contentDetails,statistics,status', id=ids).execute().get('items', []):
            m = re.match(r'PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?', it['contentDetails']['duration'])
            by_id[it['id']]['durationSec'] = (int(m.group(1) or 0) * 3600 + int(m.group(2) or 0) * 60 + int(m.group(3) or 0)) if m else None
            by_id[it['id']]['publicViews'] = it['statistics'].get('viewCount')
            # Status-Check (Plan 02.11.): öffentlich? fälschlich "made for kids"? Altersbeschränkung?
            st = it.get('status', {})
            by_id[it['id']]['status'] = {k: st.get(k) for k in ('privacyStatus', 'madeForKids', 'selfDeclaredMadeForKids',
                                                                 'embeddable', 'publicStatsViewable', 'uploadStatus')}
            by_id[it['id']]['status']['ytRating'] = it['contentDetails'].get('contentRating', {}).get('ytRating')
            # Plan 04.11.: versteckte Einschränkungen sichtbar machen (Longs mit 0 Views)
            cd = it.get('contentDetails', {})
            by_id[it['id']]['status'].update({
                'regionRestriction': cd.get('regionRestriction'),
                'contentRating': cd.get('contentRating') or None,
                'licensedContent': cd.get('licensedContent'),
                'rejectionReason': st.get('rejectionReason'),
                'failureReason': st.get('failureReason'),
                'license': st.get('license')})
            rr_ = cd.get('regionRestriction') or {}
            if rr_.get('blocked') or rr_.get('allowed') or st.get('rejectionReason') or st.get('failureReason'):
                log(f"Status-Warnung {it['id']}: regionRestriction={rr_} rejection={st.get('rejectionReason')} failure={st.get('failureReason')}")
            if st.get('selfDeclaredMadeForKids'):
                try:
                    y.videos().update(part='status', body={'id': it['id'], 'status': {
                        'privacyStatus': st.get('privacyStatus'), 'selfDeclaredMadeForKids': False,
                        **({'publishAt': st['publishAt']} if st.get('publishAt') else {})}}).execute()
                    log(f"Status-Fix: {it['id']} war als 'made for kids' markiert → auf False gesetzt")
                except Exception as ex:
                    log(f"Status-Fix {it['id']} fehlgeschlagen:", str(ex)[:150])
            if st.get('madeForKids') or by_id[it['id']]['status']['ytRating'] or (
                    st.get('privacyStatus') not in ('public', 'private') and st.get('privacyStatus')):
                log(f"Status-Warnung {it['id']}: {by_id[it['id']]['status']}")
    for v in vids:
        if v.get('views') and v.get('engagedViews') is not None:
            v['engagedShare'] = round(v['engagedViews'] / max(1, v['views']), 3)
    # Kanal-Publikum (kostenlos über YouTube Analytics, letzte 28 Tage): Länder, Geräte, Alter
    audience = {}
    start28 = (dt.date.today() - dt.timedelta(days=28)).isoformat()
    for key, kw in (('countries', dict(metrics='views,engagedViews', dimensions='country', sort='-views', maxResults=15)),
                    ('devices', dict(metrics='views,engagedViews', dimensions='deviceType', sort='-views')),
                    ('ageGroups', dict(metrics='viewerPercentage', dimensions='ageGroup'))):
        try:
            rep = a.reports().query(ids='channel==MINE', startDate=start28, endDate=today, **kw).execute()
            cols = [h['name'] for h in rep['columnHeaders']]
            audience[key] = [dict(zip(cols, r)) for r in rep.get('rows', [])]
        except Exception as ex:
            audience[key + 'Error'] = str(ex)[:150]
    ANALYTICS.mkdir(parents=True, exist_ok=True)
    log(f"Kanal: {ch['snippet']['title']} | Kontrollnummer: {os.environ.get('GOOGLE_REFRESH_TOKEN', '')[-4:]}")
    report = {'fetched': dt.datetime.now().isoformat(timespec='minutes'), 'channel': ch['snippet']['title'],
              'subscribers': ch['statistics'].get('subscriberCount'), 'audience': audience, 'videos': vids}
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


def keyword_offset(q_text, spoken, dur):
    """Wann spricht die Stimme das **Schlüsselwort**? Kokoro liefert keine Wortzeiten → Schätzung über die
    Zeichenposition im gesprochenen Satz (±0,3 s; Pausen am Satzanfang/-ende abgezogen). None, wenn nicht gefunden."""
    import re as _re
    m = _re.search(r'\*\*([^*]+)\*\*', q_text or '')
    if not m or not spoken or dur <= 0:
        return None
    kw = m.group(1).strip().lower()
    sp = spoken.lower()
    i = sp.find(kw)
    if i < 0:  # z. B. "1492" im Bild, "fourteen ninety two" gesprochen → erstes Wort probieren
        first = _re.sub(r'[^a-z]', '', kw.split()[0]) if kw.split() else ''
        i = sp.find(first) if len(first) >= 4 else -1
    if i < 0:
        return None
    lead, trail = 0.08, 0.15  # typische Stille vor/nach Kokoro-Sätzen
    frac = i / max(1, len(sp))
    return max(0.0, lead + frac * max(0.1, dur - lead - trail))


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
        kw = keyword_offset(q.get('q', ''), ln['q'], len(qa) / SR)
        if kw is not None:
            q['keywordAt'] = round(t + kw, 3)
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
# Lange Videos nur noch an festen Tagen (0 = Montag): Di, Do, Sa. Grund (09.11.): 20 tägliche Longs seit 22.10.
# mit 0–14 Views – lieber 3 starke pro Woche als 7 gleichförmige; spart außerdem Action-Minuten.
LONG_DAYS = {1, 3, 5}


def long_day(day=None):
    return (day or dt.date.today()).weekday() in LONG_DAYS


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


def viewer_interaction():
    """Zuschauer-Kommentare holen (analytics/comments.md) und vorbereitete Antworten aus replies.json posten – Fehler stoppen nichts"""
    import viewer_comments as vc
    for step in (vc.post_replies, vc.fetch):
        try:
            step(sys.modules[__name__])
        except Exception:
            log(f'Zuschauer-Kommentare ({step.__name__}) FEHLER:', traceback.format_exc()[-600:])


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
        text = item['youtube']['comment']
        # Manager-Entscheid 04.11.: Shorts-Zuschauer per Erst-Kommentar zum Long führen (nur wenn der Long schon öffentlich ist)
        lid = item.get('linkedLong')
        if lid and fmt_of(item) != 'long' and 'youtu.be/' not in text:
            try:
                lst = (y.videos().list(part='status', id=lid).execute().get('items') or [{}])[0].get('status', {})
                if lst.get('privacyStatus') == 'public':
                    text += f"\n\n▶ Want more? Try today's full quiz: https://youtu.be/{lid}"
            except Exception as ex:
                log('Long-Status für Kommentar-Link nicht lesbar:', str(ex)[:120])
        try:
            y.commentThreads().insert(part='snippet', body={'snippet': {'videoId': vid, 'topLevelComment': {'snippet': {'textOriginal': text}}}}).execute()
            log(f"{item['id']}: Kommentar gepostet" + (' (mit Long-Link)' if 'youtu.be/' in text else ''))
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
    unit = 'Round' if story.get('type') == 'truesize' else 'Question'
    for i, q in enumerate(story.get('questions') or story.get('rounds') or []):
        lv = (q.get('level') or '').strip()
        if lv and lv != last:
            ch.append((0 if not ch else q.get('start', 0), f"{lv.title()} ({unit} {i + 1})"))
            last = lv
    outro_at = story.get('outroStart') or (story.get('outro') or {}).get('start')
    if outro_at and story.get('durationInSeconds', 0) - outro_at > (5 if story.get('type') == 'truesize' else 10):
        ch.append((outro_at, 'Your score'))
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
    """Nur gleiche Titel von heute blockieren; alte Tagesvideos dürfen den neuen Upload nicht verhindern."""
    from zoneinfo import ZoneInfo
    today = dt.datetime.now(ZoneInfo('Europe/Berlin')).date().isoformat()
    ch = y.channels().list(part='contentDetails', mine=True).execute()['items'][0]
    up = ch['contentDetails']['relatedPlaylists']['uploads']
    r = y.playlistItems().list(part='snippet', playlistId=up, maxResults=50).execute()
    for it in r.get('items', []):
        snippet = it.get('snippet', {})
        if snippet.get('title', '').strip() != title.strip()[:100]:
            continue
        # YouTube's publishedAt is the best available timestamp for an upload,
        # including scheduled/private videos. Do not mistake yesterday's title for today's upload.
        published = snippet.get('publishedAt', '')
        if published[:10] == today:
            return it.get('snippet', {}).get('resourceId', {}).get('videoId')
    return None


def upload(item, mp4):
    from googleapiclient.http import MediaFileUpload
    meta = item['youtube']
    dup = already_uploaded(yt(), meta['title'])
    if dup:
        raise RuntimeError(
            f'Doppelter Titel bereits heute hochgeladen ({dup}); '
            'dieser Queue-Eintrag wird nicht fälschlich als neuer Upload markiert.'
        )
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
    """3 Vorschaubild-Varianten für den automatischen Thumbnail-Test (tvshow: Design v2 ab 12.11. – A gelb/Suchphrase, B lila/Punkt-Hürde, C rot/\"Only 1%\")"""
    THUMBS.mkdir(parents=True, exist_ok=True)
    out = []
    # exam-Layout: Variante B (rotes „F“, Besitzer-Favorit 22.11.) startet als erstes Vorschaubild
    order = ('B', 'A', 'C') if story.get('layout') == 'exam' else ('A', 'B', 'C')
    for v in order:
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


_CTR_API_OK = True


def thumb_score(a, vid, start, end):
    """Klickrate (CTR) des Vorschaubilds im Zeitraum; falls die API das nicht liefert: Aufrufe pro Tag.
    Die CTR-Abfrage liefert bisher HttpError 400 → nach dem ersten Fehler pro Lauf nicht erneut versuchen,
    und den Fehlertext nicht mehr in jedes Ergebnis/Log schreiben."""
    global _CTR_API_OK
    if _CTR_API_OK:
        try:
            rep = a.reports().query(ids='channel==MINE', startDate=start, endDate=end, filters=f'video=={vid}',
                                    dimensions='video',
                                    metrics='videoThumbnailImpressions,videoThumbnailImpressionsClickRate').execute()
            row = (rep.get('rows') or [[vid, 0, 0]])[0]
            return {'impressions': int(row[1] or 0), 'ctr': round(float(row[2] or 0), 4), 'metric': 'ctr'}
        except Exception as ex:
            _CTR_API_OK = False
            log('Thumbnail-Test: CTR über API nicht verfügbar – nutze Aufrufe/Tag', str(ex)[:80])
    rep = a.reports().query(ids='channel==MINE', startDate=start, endDate=end, filters=f'video=={vid}', metrics='views').execute()
    views = int(((rep.get('rows') or [[0]])[0])[0] or 0)
    days = max(1, (dt.date.fromisoformat(end) - dt.date.fromisoformat(start)).days)
    return {'views': views, 'ctr': round(views / days, 2), 'metric': 'views/day'}


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
        if t.get('refresh') and st_file.exists():
            # Vorschaubild-Neustart (z. B. neues Design v2): alle Varianten neu rendern, Test von vorn, Variante A sofort setzen
            variants = render_thumbs(item['id'], json.loads(st_file.read_text(encoding='utf-8')))
            if variants:
                y = y or yt()
                try:
                    y.thumbnails().set(videoId=vid, media_body=MediaFileUpload(variants[0][1])).execute()
                    t = {'order': [v for v, _ in variants], 'current': variants[0][0], 'since': today.isoformat(), 'results': {}, 'done': False, 'design': t.get('refresh')}
                    item['thumbTest'] = t
                    d.write_text(json.dumps(item, indent=1, ensure_ascii=False), encoding='utf-8')
                    log(f"Thumbnail-Neustart {item['id']}: Design {t['design']}, jetzt Variante {t['current']}")
                except Exception as ex:
                    log('Thumbnail-Neustart fehlgeschlagen:', str(ex)[:200])
            continue
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


# ---------------------------------------------------------------- B-Roll (echte Clips statt KI-Look)
BROLL_USED = AP / 'broll-used.json'
_OK_LICENSE = re.compile(r'^(cc0|public domain|pd\b|pd-|cc[ -]by(?![^ ]*n[cd]))', re.I)


def _strip_html(t):
    return re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', '', t or '')).strip()


_AI_CLIP = re.compile(r'\bsora\b|openai|midjourney|dall-?e|stable[ _-]?diffusion|runway ?ml|\bveo ?[23]?\b|ai[- _]generated|\bkling\b|\bpika\b|generative ai|text-to-video', re.I)
# Manager-Entscheid 04.11.: keine politischen/Konflikt-Clips (z. B. "No Kings march" im Geography-Long 03.11.)
_OFFTOPIC_CLIP = re.compile(r'protest|demonstrat|no kings|\brally\b|\briot|election|campaign|politic|parliament|\btrump\b|\bbiden\b|refugee|military|soldier|\bpolice\b|\bwar\b|funeral|accident|\bcrash', re.I)


def _commons_candidates(query, sess):
    r = sess.get('https://commons.wikimedia.org/w/api.php', timeout=30, params={
        'action': 'query', 'format': 'json', 'generator': 'search', 'gsrsearch': f'{query} filetype:video',
        'gsrnamespace': 6, 'gsrlimit': 15, 'prop': 'videoinfo',
        'viprop': 'url|size|mime|extmetadata|derivatives'})
    r.raise_for_status()
    pages = sorted((r.json().get('query') or {}).get('pages', {}).values(), key=lambda p: p.get('index', 99))
    out = []
    for pg in pages:
        vi = (pg.get('videoinfo') or [{}])[0]
        meta = vi.get('extmetadata') or {}
        lic = _strip_html(meta.get('LicenseShortName', {}).get('value', ''))
        if not _OK_LICENSE.match(lic):
            continue
        dur = float(vi.get('duration') or 0)
        if dur and (dur < 4 or dur > 1800):
            continue
        ders = [d for d in vi.get('derivatives', []) if 300 <= int(d.get('height') or 0) <= 720]
        ders.sort(key=lambda d: -int(d.get('height') or 0))
        src = ders[0]['src'] if ders else (vi.get('url') if int(vi.get('size') or 0) < 80_000_000 else None)
        if not src:
            continue
        title = pg['title'].replace('File:', '', 1)
        artist = _strip_html(meta.get('Artist', {}).get('value', ''))[:60] or 'unknown'
        # Plan 04.11.: keine KI-generierten Clips (Besitzer-Regel "kein AI-Look", Synthetic-Content-Kennzeichnung)
        blob = ' '.join([title, artist, _strip_html(meta.get('ImageDescription', {}).get('value', '')),
                         _strip_html(meta.get('Categories', {}).get('value', ''))])
        if _AI_CLIP.search(blob) or _OFFTOPIC_CLIP.search(blob):
            continue
        out.append({'title': title, 'src': src, 'dur': dur, 'credit': f'{title.rsplit(".", 1)[0][:70]} – {artist} ({lic})'})
    return out


def fetch_broll(story, name, max_clips=12):
    """Lädt für Fragen mit "broll" (Suchbegriff) einen kurzen, stummen Clip aus Wikimedia Commons
    (nur CC0/PD/CC BY/CC BY-SA) nach public/broll/ und setzt q["video"]. Fehler → Frage bleibt bei Foto/Emoji.
    Gibt die Credit-Zeilen für die Beschreibung zurück."""
    qs = [q for q in story.get('questions', []) if q.get('broll') and not q.get('values')][:max_clips]
    if not qs:
        return []
    import requests
    ff = 'ffmpeg'
    try:
        import imageio_ffmpeg
        ff = imageio_ffmpeg.get_ffmpeg_exe()
    except Exception:
        pass
    sess = requests.Session()
    sess.headers['User-Agent'] = 'CouldYouPassQuizBot/1.0 (YouTube quiz channel; contact via GitHub ismail656565)'
    used = set(json.loads(BROLL_USED.read_text(encoding='utf-8'))) if BROLL_USED.exists() else set()
    outdir = ROOT / 'public' / 'broll'
    outdir.mkdir(parents=True, exist_ok=True)
    credits = []
    for i, q in enumerate(story['questions']):
        if q not in qs:
            continue
        try:
            cands = [c for c in _commons_candidates(q['broll'], sess) if c['title'] not in used]
        except Exception as ex:
            log('B-Roll Suche fehlgeschlagen', q['broll'], str(ex)[:120])
            continue
        need = max(4.0, float(q.get('end', 8)) - float(q.get('start', 0)) + 1.0)
        for c in cands[:3]:
            raw = outdir / f'{name}-{i}.src'
            out = outdir / f'{name}-{i}.mp4'
            try:
                time.sleep(3)  # Wikimedia drosselt schnelle Downloads (429)
                for attempt in range(3):
                    r = sess.get(c['src'], timeout=120, stream=True)
                    if r.status_code != 429:
                        break
                    r.close()
                    time.sleep(10 * (attempt + 1))
                with r:
                    r.raise_for_status()
                    with open(raw, 'wb') as fh:
                        for chunk in r.iter_content(1 << 20):
                            fh.write(chunk)
                start = min(3.0, c['dur'] / 4) if c['dur'] else 0
                cmd = [ff, '-y', '-loglevel', 'error', '-stream_loop', '-1', '-ss', f'{start:.1f}', '-i', str(raw),
                       '-t', f'{need:.1f}', '-an', '-vf', 'scale=-2:720,fps=30', '-c:v', 'libx264', '-preset', 'veryfast',
                       '-crf', '26', '-pix_fmt', 'yuv420p', str(out)]
                rr = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
                raw.unlink(missing_ok=True)
                if rr.returncode or not out.exists() or out.stat().st_size < 20_000:
                    raise RuntimeError(rr.stderr[-200:])
                q['video'] = f'broll/{out.name}'
                used.add(c['title'])
                credits.append(c['credit'])
                log(f'B-Roll Frage {i + 1} ("{q["broll"]}"): {c["title"][:60]}')
                break
            except Exception as ex:
                raw.unlink(missing_ok=True)
                log('B-Roll Clip übersprungen', c['title'][:60], str(ex)[:120])
        else:
            if 'video' not in q:
                log(f'B-Roll Frage {i + 1} ("{q["broll"]}"): kein passender Clip – bleibt bei Foto/Emoji')
    BROLL_USED.write_text(json.dumps(sorted(used), indent=0, ensure_ascii=False), encoding='utf-8')
    return credits


def add_broll_credits(item, credits):
    if not credits:
        return
    yt = item.setdefault('youtube', {})
    desc = yt.get('description', '')
    line = 'Footage via Wikimedia Commons: ' + '; '.join(credits)
    if 'Music: original.' in desc:
        desc = desc.replace('Music: original.', line + '\nMusic: original.')
    else:
        desc = desc.rstrip() + '\n' + line
    yt['description'] = desc[:4900]



def qa_check(mp4, item):
    """Messbare Qualitätsprüfung nach dem Rendern (aus echris6/motion-video-kit, quality-bar.md):
    Lautheit (Ziel −14 LUFS, True Peak ≤ −1 dBTP → sonst automatisch normalisieren), eingefrorene Strecken,
    erstes Bild fertig (nicht schwarz). Ergebnis in item['qa'] + Log. Bricht nie den Upload ab."""
    import re as _re
    ff = ffmpeg_bin()
    res = {}
    try:
        out = subprocess.run([ff, '-hide_banner', '-nostats', '-i', str(mp4), '-af', 'ebur128=peak=true', '-f', 'null', '-'],
                             capture_output=True, text=True, timeout=900).stderr
        summ = out[out.rfind('Summary:'):] if 'Summary:' in out else out
        gi = _re.search(r'I:\s*(-?[\d.]+) LUFS', summ)
        gp = _re.search(r'Peak:\s*(-?[\d.]+|-inf) dBFS', summ)
        lra = _re.search(r'LRA:\s*(-?[\d.]+) LU', summ)
        if gi:
            res['lufs'] = float(gi.group(1))
        if gp and gp.group(1) != '-inf':
            res['truePeak'] = float(gp.group(1))
        if lra:
            res['lra'] = float(lra.group(1))
        if 'lufs' in res and (abs(res['lufs'] + 14) > 1.5 or res.get('truePeak', -2) > -1.0):
            tmp = Path(str(mp4).replace('.mp4', '.norm.mp4'))
            r = subprocess.run([ff, '-v', 'error', '-y', '-i', str(mp4), '-c:v', 'copy', '-af', 'loudnorm=I=-14:TP=-1.5:LRA=11',
                                '-ar', '48000', '-c:a', 'aac', '-b:a', '192k', '-movflags', '+faststart', str(tmp)], timeout=900)
            if r.returncode == 0 and tmp.exists():
                shutil.move(str(tmp), str(mp4))
                res['normalized'] = True
        # eingefrorene Strecken (Bilddifferenz ~0) bei 5 fps; Countdown-Pausen zählen mit, daher nur Info + Grenzwert für lange Standbilder
        fz = subprocess.run([ff, '-hide_banner', '-i', str(mp4), '-vf', 'fps=5,scale=240:-1,format=gray,tblend=all_mode=difference,signalstats,metadata=print:key=lavfi.signalstats.YAVG',
                             '-an', '-f', 'null', '-'], capture_output=True, text=True, timeout=1800).stderr
        vals = [float(v) for v in _re.findall(r'YAVG=([\d.]+)', fz)]
        if vals:
            frozen = [v < 0.35 for v in vals]
            longest = cur = 0
            for f in frozen:
                cur = cur + 1 if f else 0
                longest = max(longest, cur)
            res['frozenShare'] = round(sum(frozen) / len(vals), 3)
            res['longestFreezeSec'] = round(longest / 5, 1)
        # erstes Bild: mittlere Helligkeit (schwarz/leer = schlechter Hook-Frame)
        f0 = subprocess.run([ff, '-hide_banner', '-i', str(mp4), '-frames:v', '1', '-vf', 'scale=240:-1,format=gray,signalstats,metadata=print:key=lavfi.signalstats.YAVG', '-f', 'null', '-'],
                            capture_output=True, text=True, timeout=120).stderr
        y0 = _re.search(r'YAVG=([\d.]+)', f0)
        if y0:
            res['frame0Luma'] = round(float(y0.group(1)), 1)
        warn = []
        if res.get('longestFreezeSec', 0) > 6:
            warn.append(f"Standbild {res['longestFreezeSec']} s")
        if res.get('frame0Luma', 100) < 12:
            warn.append('erstes Bild fast schwarz')
        res['warnings'] = warn
        log(f"QA: {res.get('lufs')} LUFS, TP {res.get('truePeak')} dBTP{' → normalisiert auf −14' if res.get('normalized') else ''}, "
            f"Standbild max {res.get('longestFreezeSec')} s, Frame0-Luma {res.get('frame0Luma')}" + (f" | WARNUNG: {'; '.join(warn)}" if warn else ''))
    except Exception as ex:
        log('QA übersprungen:', str(ex)[:200])
    item['qa'] = res
    return res


def produce_one(p):
    item = json.loads(p.read_text(encoding='utf-8'))
    name = item['id']
    log(f'Produziere {name} ({fmt_of(item)})')
    try:
        story = item['story']
        if story.get('type') in ('truesize', 'flagduel'):
            # Karten-Short / Flaggen-Duell "The map is lying" (Komposition TrueSize): eigene Stimme/Zeitplan, keine Fragenliste
            import atlas_voice
            story['id'] = name
            sp = ROOT / 'stories' / f'{name}.json'
            sp.write_text(json.dumps(story, indent=1, ensure_ascii=False), encoding='utf-8')
            atlas_voice.main(sp, sys.modules[__name__])
            story = item['story'] = json.loads(sp.read_text(encoding='utf-8'))
        else:
            story['audio'] = f'audio/{name}.mp3'
            build_audio(item, ROOT / 'public' / 'audio' / f'{name}.mp3')
        if story.get('type') in ('truesize', 'flagduel'):
            pass
        elif story.get('layout') == 'stick':
            # 2D-Strichmännchen-Look: KI-Doodle-Clips von LTX statt echter B-Roll-Fotos
            try:
                from ltx import fetch_ltx
                n = fetch_ltx(story, ROOT)
                log(f'LTX: {n} neue Clip(s)')
            except Exception as ex:
                log('LTX übersprungen:', str(ex)[:200])
        else:
            try:
                add_broll_credits(item, fetch_broll(story, name))
            except Exception as ex:
                log('B-Roll übersprungen:', str(ex)[:200])
        (ROOT / 'stories' / f'{name}.json').write_text(json.dumps(story, indent=1, ensure_ascii=False), encoding='utf-8')
        r = subprocess.run(['node', 'scripts/render.mjs', f'stories/{name}.json'], cwd=ROOT, shell=(os.name == 'nt'), capture_output=True, text=True)
        mp4 = ROOT / 'out' / f'{name}.mp4'
        if r.returncode != 0 or not mp4.exists():
            raise RuntimeError('Rendern fehlgeschlagen: ' + (r.stdout[-1500:] + r.stderr[-1500:]).replace('\n', ' | '))
        log('Gerendert')
        qa_check(mp4, item)
        if story.get('type') == 'truesize' and story.get('format') == 'long':
            # Karten-Long: ein festes Vorschaubild (Grönland in echter Größe auf Afrika), kein A/B/C-Test
            THUMBS.mkdir(exist_ok=True)
            tf = THUMBS / f'{name}-A.jpg'
            cmd = ['npx', 'remotion', 'still', 'TrueSizeThumb', str(tf), f'--props=stories/{name}.json', '--jpeg-quality=90']
            if os.environ.get('BROWSER_EXECUTABLE'):
                cmd.append(f"--browser-executable={os.environ['BROWSER_EXECUTABLE']}")
            subprocess.run(cmd, cwd=ROOT, shell=(os.name == 'nt'), capture_output=True, text=True)
            if tf.exists():
                item['_thumb'] = str(tf)
        elif story.get('format') == 'long':
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
        error = traceback.format_exc()
        log('FEHLER:', error)
        FAILED.mkdir(exist_ok=True)
        shutil.move(str(p), str(FAILED / p.name))
        raise RuntimeError(f'Produktion fehlgeschlagen für {name}; Datei liegt in {FAILED / p.name}')


def produce():
    """pro Tag höchstens 1 Short und 1 langes Video (außer "force": true)"""
    QUEUE.mkdir(parents=True, exist_ok=True)
    items = sorted(p for p in QUEUE.glob('*.json'))
    today = dt.date.today().isoformat()
    if not items:
        # A scheduled backup run can happen after the main run already met
        # the daily target. Treat that as success, not as a broken workflow.
        done_counts = {'short': 0, 'long': 0}
        for d in DONE.glob('*.json'):
            try:
                di = json.loads(d.read_text(encoding='utf-8'))
                if di.get('uploaded', {}).get('at', '').startswith(today):
                    kind = fmt_of(di)
                    done_counts[kind] = done_counts.get(kind, 0) + 1
            except Exception:
                pass
        if done_counts.get('short', 0) >= PER_DAY['short'] and done_counts.get('long', 0) >= (PER_DAY['long'] if long_day() else 0):
            log(f"Daily target already completed (Shorts={done_counts['short']}, long={done_counts['long']}); nothing left to produce.")
            return
        message = (
            'FATAL: Warteschlange leer, obwohl das Tagesziel nicht erreicht ist. '
            'Der automatische Queue-Generator hat keine Quiz-Datei bereitgestellt. '
            'Prüfe den vorherigen Generierungsschritt und autopilot/queue/.'
        )
        log(message)
        raise RuntimeError(message)
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
            if f == 'long' and not long_day() and not item_force(cand[0]):
                log('Heute kein Long-Tag (Di/Do/Sa) – langes Video bleibt in der Warteschlange.')
                break
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
    """Beschreibung der Shorts von heute + gestern (Nachholen) um den Link zum langen Video desselben Tages ergänzen"""
    try:
        yday = (dt.date.fromisoformat(today[:10]) - dt.timedelta(days=1)).isoformat()
    except Exception:
        yday = None
    for day in [yday, today]:
        if day:
            _link_day(day)


def _long_label(long_item):
    st = long_item.get('story', {})
    if st.get('questions'):
        return f"▶ Full {len(st['questions'])}-question quiz"
    if st.get('rounds'):
        return f"▶ Full {len(st['rounds'])}-round map challenge"
    return "▶ Full video"


def _link_day(today):
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
        sn['description'] = f"{_long_label(long_item)}: https://youtu.be/{long_id}\n\n" + sn.get('description', '')
        y.videos().update(part='snippet', body={'id': v['id'], 'snippet': {k: sn[k] for k in ('title', 'description', 'tags', 'categoryId') if k in sn}}).execute()
        short['linkedLong'] = long_id
        d.write_text(json.dumps(short, indent=1, ensure_ascii=False), encoding='utf-8')
        log(f'Short-Beschreibung ({short["id"]}) verlinkt auf langes Video {long_id}')


# ---------------------------------------------------------------- Ausreißer-Scan (eigener vidIQ-Ersatz)
OUTLIER_KEYWORDS = ['general knowledge quiz', 'trivia quiz', 'memory test quiz', 'quiz for seniors', 'iq test quiz', 'guess the quiz']


def parse_dur(iso):
    m = re.match(r'P(?:(\d+)D)?T?(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?', iso or '')
    if not m:
        return 0
    d, h, mi, se = (int(x or 0) for x in m.groups())
    return d * 86400 + h * 3600 + mi * 60 + se


def outliers(days=30, max_subs=100000):
    """Sucht Quiz-Videos der letzten N Tage über die offizielle YouTube-API (~2.000 Quota-Einheiten)
    und schreibt die Ausreißer (Views im Verhältnis zu Abos, Views/Tag) nach analytics/outliers.json + .md"""
    y = yt()
    now = dt.datetime.now(dt.timezone.utc)
    after = (now - dt.timedelta(days=days)).strftime('%Y-%m-%dT%H:%M:%SZ')
    ids, hits = [], {}
    for kw in OUTLIER_KEYWORDS:
        for dur in ('short', 'medium', 'long'):
            try:
                r = y.search().list(part='id', q=kw, type='video', order='viewCount', publishedAfter=after,
                                    videoDuration=dur, relevanceLanguage='en', maxResults=50).execute()
            except Exception as e:
                log(f'Ausreißer-Suche "{kw}"/{dur} fehlgeschlagen: {e}')
                continue
            for it in r.get('items', []):
                vid = it['id'].get('videoId')
                if vid and vid not in hits:
                    hits[vid] = kw
                    ids.append(vid)
    vids = []
    for i in range(0, len(ids), 50):
        r = y.videos().list(part='snippet,statistics,contentDetails,liveStreamingDetails', id=','.join(ids[i:i + 50])).execute()
        vids += r.get('items', [])
    chans = {}
    cids = sorted({v['snippet']['channelId'] for v in vids})
    for i in range(0, len(cids), 50):
        r = y.channels().list(part='statistics', id=','.join(cids[i:i + 50])).execute()
        for c in r.get('items', []):
            chans[c['id']] = int(c['statistics'].get('subscriberCount') or 0)
    rows = []
    foreign = re.compile('[\u0400-\u04FF\u0590-\u06FF\u0900-\u0DFF\u0E00-\u0FFF\u1100-\u11FF\u3040-\u30FF\u3400-\u9FFF\uAC00-\uD7AF]')
    skipped = 0
    for v in vids:
        sn, stt = v['snippet'], v.get('statistics', {})
        if 'liveStreamingDetails' in v or foreign.search(sn['title']) or (sn.get('defaultAudioLanguage') or 'en')[:2] not in ('en', 'zx'):
            skipped += 1  # Livestreams und nicht-englische Videos auslassen
            continue
        views = int(stt.get('viewCount') or 0)
        subs = chans.get(sn['channelId'], 0)
        pub = dt.datetime.fromisoformat(sn['publishedAt'].replace('Z', '+00:00'))
        age = max((now - pub).total_seconds() / 86400, 0.5)
        sec = parse_dur(v['contentDetails'].get('duration'))
        rows.append({'id': v['id'], 'title': sn['title'], 'channel': sn['channelTitle'], 'subs': subs, 'views': views,
                     'viewsPerDay': round(views / age), 'ratio': round(views / max(subs, 500), 1),
                     'likes': int(stt.get('likeCount') or 0), 'comments': int(stt.get('commentCount') or 0),
                     'seconds': sec, 'format': 'short' if sec <= 180 else 'long', 'published': sn['publishedAt'][:10],
                     'keyword': hits.get(v['id']), 'url': f"https://youtube.com/watch?v={v['id']}"})
    small = [r for r in rows if r['subs'] <= max_subs and r['views'] >= 5000]
    out = {'fetched': now.isoformat(timespec='minutes'), 'days': days, 'maxSubs': max_subs, 'keywords': OUTLIER_KEYWORDS,
           'scanned': len(rows), 'skippedLiveOrForeign': skipped}
    md = [f"# Ausreißer-Scan {now:%Y-%m-%d} (letzte {days} Tage, Kanäle ≤ {max_subs:,} Abos, ≥ 5.000 Views)", '']
    for f in ('long', 'short'):
        top = sorted([r for r in small if r['format'] == f], key=lambda r: -r['ratio'])[:25]
        out[f] = top
        md += [f"## {'Lange Videos' if f == 'long' else 'Shorts'} – Top {len(top)} nach Views/Abos", '',
               '| Views | Views/Tag | Abos | × | Länge | Titel | Kanal |', '|---|---|---|---|---|---|---|']
        for r in top:
            md.append(f"| {r['views']:,} | {r['viewsPerDay']:,} | {r['subs']:,} | {r['ratio']} | {r['seconds'] // 60}:{r['seconds'] % 60:02d} "
                      f"| [{r['title'].replace('|', '/')}]({r['url']}) | {r['channel'].replace('|', '/')} |")
        md.append('')
    (AP / 'analytics' / 'outliers.json').write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding='utf-8')
    (AP / 'analytics' / 'outliers.md').write_text('\n'.join(md), encoding='utf-8')
    log(f"Ausreißer-Scan: {len(rows)} Videos geprüft, {len(out['long'])} lange + {len(out['short'])} Shorts gespeichert")


def competitors(max_channels=25, days=60):
    """Konkurrenz-Beobachtung: verfolgt kleine/mittlere Quiz-Kanäle (aus dem Ausreißer-Scan + Liste
    analytics/competitors.json) und findet deren GEWINNER-Videos (Views im Verhältnis zum eigenen
    Kanal-Median). Ergebnis: analytics/competitors.md/.json. ~3 Quota-Einheiten pro Kanal."""
    y = yt()
    now = dt.datetime.now(dt.timezone.utc)
    cfile = AP / 'analytics' / 'competitors.json'
    conf = json.loads(cfile.read_text(encoding='utf-8')) if cfile.exists() else {}
    blocked = set(conf.get('blocked', []))  # vom Research-Agenten entfernte Kanäle (nie wieder aufnehmen)
    tracked = {c['id']: c for c in conf.get('channels', []) if c['id'] not in blocked}
    # neue Kandidaten aus dem Ausreißer-Scan (Video-IDs -> Kanal-IDs)
    of = AP / 'analytics' / 'outliers.json'
    if of.exists():
        o = json.loads(of.read_text(encoding='utf-8'))
        cand = sorted(o.get('long', []) + o.get('short', []), key=lambda r: -r.get('ratio', 0))[:40]
        ids = [r['id'] for r in cand]
        for i in range(0, len(ids), 50):
            for it in y.videos().list(part='snippet', id=','.join(ids[i:i + 50])).execute().get('items', []):
                cid = it['snippet']['channelId']
                if cid not in tracked and cid not in blocked and len(tracked) < max_channels:
                    tracked[cid] = {'id': cid, 'name': it['snippet']['channelTitle'], 'source': 'outlier-scan',
                                    'added': now.date().isoformat()}
    if not tracked:
        log('Konkurrenz: keine Kanäle bekannt (erst Ausreißer-Scan laufen lassen)')
        return
    cids = list(tracked)
    chans = {}
    for i in range(0, len(cids), 50):
        for c in y.channels().list(part='snippet,statistics,contentDetails', id=','.join(cids[i:i + 50])).execute().get('items', []):
            chans[c['id']] = c
    winners, summary = [], []
    for cid, c in chans.items():
        try:
            up = c['contentDetails']['relatedPlaylists']['uploads']
            items = y.playlistItems().list(part='contentDetails', playlistId=up, maxResults=50).execute().get('items', [])
            vids = [it['contentDetails']['videoId'] for it in items]
            data = y.videos().list(part='snippet,statistics,contentDetails', id=','.join(vids)).execute().get('items', []) if vids else []
        except Exception as ex:
            log(f"Konkurrenz {c['snippet']['title']}: {ex}")
            continue
        rows = []
        for v in data:
            sn, st = v['snippet'], v.get('statistics', {})
            pub = dt.datetime.fromisoformat(sn['publishedAt'].replace('Z', '+00:00'))
            age = (now - pub).total_seconds() / 86400
            sec = parse_dur(v['contentDetails'].get('duration'))
            rows.append({'id': v['id'], 'title': sn['title'], 'views': int(st.get('viewCount') or 0),
                         'likes': int(st.get('likeCount') or 0), 'comments': int(st.get('commentCount') or 0),
                         'seconds': sec, 'format': 'short' if sec <= 180 else 'long', 'ageDays': round(age, 1),
                         'published': sn['publishedAt'][:10], 'url': f"https://youtube.com/watch?v={v['id']}"})
        subs = int(c['statistics'].get('subscriberCount') or 0)
        name = c['snippet']['title']
        tracked[cid]['name'] = name
        hist = tracked[cid].setdefault('subsHistory', {})
        hist[now.date().isoformat()] = subs
        for f in ('short', 'long'):
            fr = [r for r in rows if r['format'] == f and r['ageDays'] >= 3]
            if not fr:
                continue
            med = statistics.median([r['views'] for r in fr]) or 1
            recent = [r for r in fr if r['ageDays'] <= days]
            per_week = round(len([r for r in rows if r['format'] == f and r['ageDays'] <= 28]) / 4, 1)
            summary.append({'channel': name, 'id': cid, 'subs': subs, 'format': f, 'median': int(med), 'perWeek': per_week,
                            'best': max(fr, key=lambda r: r['views'])['title']})
            for r in recent:
                score = r['views'] / max(med, 50)
                if score >= 2.5 and r['views'] >= 3000:
                    winners.append(dict(r, channel=name, subs=subs, score=round(score, 1), channelMedian=int(med)))
    winners.sort(key=lambda r: -r['score'])
    conf['channels'] = list(tracked.values())
    cfile.write_text(json.dumps(conf, indent=1, ensure_ascii=False), encoding='utf-8')
    out = {'fetched': now.isoformat(timespec='minutes'), 'summary': summary, 'winners': winners[:60]}
    (AP / 'analytics' / 'competitors-report.json').write_text(json.dumps(out, indent=1, ensure_ascii=False), encoding='utf-8')
    md = [f"# Konkurrenz-Beobachtung {now:%Y-%m-%d} ({len(chans)} Kanäle)", '',
          'Gewinner = Video mit ≥ 2,5 × Views des eigenen Kanal-Medians (gleiches Format, letzte ' + str(days) + ' Tage, ≥ 3.000 Views).',
          'Nutzen: IDEEN übernehmen (Thema, Format, Titel-Muster, Länge, Thumbnail-Prinzip) – nie Fragen, Skripte oder Bilder 1:1 kopieren.', '',
          '## Gewinner-Videos (höchster Faktor zuerst)', '', '| × Median | Views | Länge | Titel | Kanal (Abos) | Datum |', '|---|---|---|---|---|---|']
    for r in winners[:40]:
        md.append(f"| {r['score']} | {r['views']:,} | {r['seconds'] // 60}:{r['seconds'] % 60:02d} | "
                  f"[{r['title'].replace('|', '/')}]({r['url']}) | {r['channel'].replace('|', '/')} ({r['subs']:,}) | {r['published']} |")
    md += ['', '## Kanäle', '', '| Kanal | Abos | Format | Median-Views | Uploads/Woche | bestes Video |', '|---|---|---|---|---|---|']
    for s_ in sorted(summary, key=lambda s_: -s_['median']):
        md.append(f"| {s_['channel'].replace('|', '/')} | {s_['subs']:,} | {s_['format']} | {s_['median']:,} | {s_['perWeek']} | {s_['best'].replace('|', '/')[:70]} |")
    (AP / 'analytics' / 'competitors.md').write_text('\n'.join(md) + '\n', encoding='utf-8')
    log(f'Konkurrenz: {len(chans)} Kanäle, {len(winners)} Gewinner-Videos')


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
        viewer_interaction()
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
            try:
                log('Testlauf B-Roll-Credits:', fetch_broll(story, name))
            except Exception as ex:
                log('B-Roll übersprungen:', str(ex)[:200])
            (ROOT / 'stories' / f'{name}.json').write_text(json.dumps(story, indent=1, ensure_ascii=False), encoding='utf-8')
            r = subprocess.run(['node', 'scripts/render.mjs', f'stories/{name}.json'], cwd=ROOT, capture_output=True, text=True)
            if r.returncode:
                log('Render-Ausgabe:', (r.stdout[-1500:] + r.stderr[-1500:]).replace('\n', ' | '))
            log(f'Testlauf {name}: Render-Code {r.returncode}, Dauer {story["durationInSeconds"]} s')
            # Standbilder zum Begutachten (werden mit autopilot/ zurück ins Repo committet)
            mp4 = ROOT / 'out' / f'{name}.mp4'
            if mp4.exists():
                fr = AP / 'test' / 'frames'
                fr.mkdir(parents=True, exist_ok=True)
                qs = story.get('questions', [])
                times = []
                if qs:
                    times += [qs[0]['start'] + 1.0, qs[0]['reveal'] + 0.1, qs[0]['reveal'] + 0.8]
                    for i in range(1, len(qs)):
                        if qs[i].get('level') != qs[i - 1].get('level'):
                            times.append(qs[i]['start'] + 0.5)
                            break
                    mi = story.get('midCtaIndex')
                    if isinstance(mi, int) and mi < len(qs):
                        times.append(qs[mi]['reveal'] + 2.5)
                    times.append(qs[-1]['reveal'] + 0.8)
                    if story.get('durationInSeconds', 0) - story.get('outroStart', 0) > 1:
                        times.append(story['outroStart'] + 2.5)
                ff = 'ffmpeg'
                try:
                    import imageio_ffmpeg
                    ff = imageio_ffmpeg.get_ffmpeg_exe()
                except Exception:
                    pass
                for k, tt in enumerate(times):
                    subprocess.run([ff, '-y', '-loglevel', 'error', '-ss', f'{tt:.2f}', '-i', str(mp4), '-frames:v', '1', '-vf', 'scale=iw/2:-1', '-q:v', '4', str(fr / f'{name}-{k}.jpg')])
                if story.get('format') == 'long':
                    render_thumbs(f'test-{name}', story)
                log(f'Testlauf {name}: {len(times)} Standbilder in autopilot/test/frames')
    elif cmd == 'competitors':
        competitors()
    elif cmd == 'outliers':
        outliers(int(sys.argv[2]) if len(sys.argv) > 2 else 30)
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
        viewer_interaction()
        produce()
        # wöchentlicher Ausreißer-Scan (nach den Uploads, damit die Quota zuerst für Uploads reicht)
        if cmd == 'all':
            try:
                f = AP / 'analytics' / 'outliers.json'
                last = json.loads(f.read_text(encoding='utf-8')).get('fetched', '') if f.exists() else ''
                if not last or (dt.datetime.now(dt.timezone.utc) - dt.datetime.fromisoformat(last)).days >= 6:
                    outliers()
            except Exception:
                log('Ausreißer-Scan-FEHLER:', traceback.format_exc())
            try:
                competitors()
            except Exception:
                log('Konkurrenz-FEHLER:', traceback.format_exc())


if __name__ == '__main__':
    main()
