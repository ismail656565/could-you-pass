"""STUDIO – alle YouTube-Kanäle an einem Ort: Google-Zugang, Kanal-Schutz, täglicher Status.

  python autopilot/studio.py auth [kanal ...]   LOKAL, einmalig (kanaele-anmelden.bat): Kanäle mit Google verbinden.
                                                Ohne Angabe: alle Kanäle, die noch kein Token haben.
  python autopilot/studio.py secret             Wert für das GitHub-Secret YT_TOKENS_JSON erneut ausgeben/setzen
  python autopilot/studio.py check              jeden Kanal prüfen -> channels/status.md + channels/status.json

Tokens
  GitHub-Secret YT_TOKENS_JSON = {"wildlytrue": "<refresh-token>", "perceptlab": "...", ...}
  Alte Einzel-Secrets (GOOGLE_REFRESH_TOKEN, WT_GOOGLE_REFRESH_TOKEN) werden weiter erkannt.
  Lokal liegen die Tokens in autopilot/tokens.local.json (in .gitignore – niemals committen).
  GOOGLE_CLIENT_ID/GOOGLE_CLIENT_SECRET (bzw. autopilot/client_secret.json) teilen sich alle Kanäle.

Für Produktions-Skripte:  import studio;  y = studio.yt('perceptlab')   # bricht ab, wenn das Token zu einem anderen Kanal gehört
"""
import datetime as dt
import json
import os
import shutil
import subprocess
import sys
import webbrowser
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
AP = ROOT / 'autopilot'
REG = ROOT / 'channels' / 'channels.json'
STATUS_MD = ROOT / 'channels' / 'status.md'
STATUS_JSON = ROOT / 'channels' / 'status.json'
LOCAL = AP / 'tokens.local.json'
REPO = 'ismail656565/could-you-pass'
SECRET = 'YT_TOKENS_JSON'
SCOPES = [
    'https://www.googleapis.com/auth/youtube.upload',
    'https://www.googleapis.com/auth/youtube.readonly',
    'https://www.googleapis.com/auth/youtube.force-ssl',
    'https://www.googleapis.com/auth/yt-analytics.readonly',
]


# ---------------------------------------------------------------- Kanäle + Tokens
def registry():
    return json.loads(REG.read_text(encoding='utf-8'))['channels']


def channel(cid):
    for ch in registry():
        if ch['id'] == cid:
            return ch
    raise SystemExit(f'Unbekannter Kanal "{cid}" – bekannt: {", ".join(c["id"] for c in registry())}')


def matches(ch, title):
    return any(m in (title or '').lower() for m in ch['match'])


def local_tokens():
    if LOCAL.exists():
        return {k: v for k, v in json.loads(LOCAL.read_text(encoding='utf-8')).items() if v}
    return {}


def tokens():
    """Alle bekannten Refresh-Tokens: YT_TOKENS_JSON > alte Einzel-Secrets > lokale Datei."""
    toks = {}
    raw = os.environ.get(SECRET, '').strip()
    if raw:
        try:
            toks.update({k: v.strip() for k, v in json.loads(raw).items() if isinstance(v, str) and v.strip()})
        except json.JSONDecodeError:
            print(f'WARNUNG: {SECRET} ist kein gültiges JSON – wird ignoriert.')
    for ch in registry():
        leg = ch.get('legacy_secret')
        if ch['id'] not in toks and leg and os.environ.get(leg, '').strip():
            toks[ch['id']] = os.environ[leg].strip()
    for k, v in local_tokens().items():
        toks.setdefault(k, v)
    return toks


def client():
    if os.environ.get('GOOGLE_CLIENT_ID') and os.environ.get('GOOGLE_CLIENT_SECRET'):
        return os.environ['GOOGLE_CLIENT_ID'], os.environ['GOOGLE_CLIENT_SECRET']
    cs = AP / 'client_secret.json'
    if cs.exists():
        d = json.loads(cs.read_text(encoding='utf-8'))
        d = d.get('installed') or d.get('web') or {}
        return d['client_id'], d['client_secret']
    raise SystemExit('Kein Google-Client: GOOGLE_CLIENT_ID/GOOGLE_CLIENT_SECRET fehlen und autopilot/client_secret.json gibt es nicht.')


def creds(cid=None, refresh_token=None):
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    rt = refresh_token or tokens().get(cid)
    if not rt:
        raise SystemExit(f'Kein Token für "{cid}" – lokal "autopilot/kanaele-anmelden.bat" ausführen.')
    cl_id, cl_secret = client()
    c = Credentials(None, refresh_token=rt, token_uri='https://oauth2.googleapis.com/token',
                    client_id=cl_id, client_secret=cl_secret, scopes=SCOPES)
    c.refresh(Request())
    return c


def _build(api, ver, c):
    from googleapiclient.discovery import build
    return build(api, ver, credentials=c, cache_discovery=False)


def guard(cid, y):
    """Bricht ab, wenn das Token nicht zum erwarteten Kanal gehört (nie auf den falschen Kanal hochladen)."""
    ch = channel(cid)
    items = y.channels().list(part='snippet,statistics,contentDetails', mine=True).execute().get('items', [])
    titles = [i['snippet']['title'] for i in items]
    if not any(matches(ch, t) for t in titles):
        raise SystemExit(f'FALSCHER KANAL: Token für "{cid}" gehört zu {titles or "keinem Kanal"} – erwartet "{ch["name"]}". Abbruch.')
    return items[0]


def yt(cid):
    """YouTube-Client für einen Kanal – mit Kanal-Schutz."""
    y = _build('youtube', 'v3', creds(cid))
    guard(cid, y)
    return y


def yta(cid):
    return _build('youtubeAnalytics', 'v2', creds(cid))


# ---------------------------------------------------------------- lokal: Kanäle verbinden
def _banner(text):
    print('\n' + '=' * 64 + f'\n  {text}\n' + '=' * 64)


def auth(ids):
    from google_auth_oauthlib.flow import InstalledAppFlow
    cs = AP / 'client_secret.json'
    if not cs.exists():
        raise SystemExit('autopilot/client_secret.json fehlt – dieselbe Datei wie beim Quiz-Kanal (google-anmelden.bat).')
    local = local_tokens()
    chans = [c for c in registry() if c.get('auth', True)]
    todo = [c for c in chans if c['id'] in ids] if ids else [c for c in chans if c['id'] not in local]
    if not todo:
        print('Alle Kanäle haben schon ein Token. (Einen Kanal neu verbinden: kanaele-anmelden.bat <kanal-id>)')
    for n, ch in enumerate(todo, 1):
        _banner(f'[{n}/{len(todo)}]  {ch["name"]}  ({ch["handle"]})')
        print(f'  1. Google-Konto wählen:   {ch["account"]}')
        print(f'  2. Kanal wählen:          {ch["name"]}')
        print('  3. Falls "Google hat diese App nicht überprüft": Erweitert -> Weiter zu ... -> alles erlauben')
        if input('\n  Enter = Browser öffnen   |   s + Enter = diesen Kanal überspringen: ').strip().lower() == 's':
            continue
        for attempt in range(3):
            flow = InstalledAppFlow.from_client_secrets_file(str(cs), SCOPES)
            c = flow.run_local_server(port=0, access_type='offline', prompt='select_account consent')
            items = _build('youtube', 'v3', c).channels().list(part='snippet', mine=True).execute().get('items', [])
            titles = [i['snippet']['title'] for i in items]
            if any(matches(ch, t) for t in titles) and c.refresh_token:
                local[ch['id']] = c.refresh_token
                LOCAL.write_text(json.dumps(local, indent=1), encoding='utf-8')
                print(f'  OK: verbunden mit "{titles[0]}"')
                break
            print(f'  !!! Angemeldet ist "{", ".join(titles) or "kein Kanal"}" – das ist nicht {ch["name"]}. Bitte nochmal, '
                  f'diesmal im Schritt "Kanal auswählen" {ch["name"]} anklicken.')
            if attempt < 2:
                input('  Enter = nochmal versuchen: ')
        else:
            print(f'  -> {ch["name"]} übersprungen (später: kanaele-anmelden.bat {ch["id"]})')
    publish(local)


def publish(local=None):
    local = local if local is not None else local_tokens()
    if not local:
        print('Keine Tokens gespeichert.')
        return
    value = json.dumps(local, separators=(',', ':'))
    _banner(f'{len(local)} Kanal/Kanäle verbunden: {", ".join(local)}')
    gh = shutil.which('gh')
    if gh and subprocess.run([gh, 'auth', 'status'], capture_output=True).returncode == 0:
        r = subprocess.run([gh, 'secret', 'set', SECRET, '-R', REPO, '--body', value], capture_output=True, text=True)
        if r.returncode == 0:
            print(f'  Fertig: GitHub-Secret {SECRET} wurde automatisch gesetzt.')
            return
        print('  (gh konnte das Secret nicht setzen:', r.stderr.strip()[:200], ')')
    copied = False
    try:
        if sys.platform.startswith('win'):
            copied = subprocess.run('clip', input=value.encode('utf-8'), shell=True).returncode == 0
        elif sys.platform == 'darwin':
            copied = subprocess.run(['pbcopy'], input=value.encode('utf-8')).returncode == 0
    except Exception:
        pass
    print('  Letzter Schritt (30 Sekunden):')
    print(f'  1. Im Browser öffnet sich GitHub -> "New repository secret"  (Name: {SECRET})')
    print('  2. Ins Feld "Secret" einfügen: ' + ('Strg+V (der Wert ist schon in der Zwischenablage)' if copied else 'den Wert unten'))
    print(f'     Gibt es {SECRET} schon: in der Liste auf den Stift bei {SECRET} klicken und den Wert ersetzen.')
    print('  3. "Add secret" klicken – fertig.')
    if not copied:
        print('\n' + value + '\n')
    try:
        webbrowser.open(f'https://github.com/{REPO}/settings/secrets/actions/new')
    except Exception:
        pass


# ---------------------------------------------------------------- Status aller Kanäle
def _public(y, handle):
    r = y.channels().list(part='snippet,statistics,contentDetails', forHandle=handle).execute().get('items', [])
    return r[0] if r else None


def _latest(y, item, n=3):
    try:
        pl = item['contentDetails']['relatedPlaylists']['uploads']
        vids = y.playlistItems().list(part='snippet', playlistId=pl, maxResults=n).execute().get('items', [])
        return [{'title': v['snippet']['title'], 'at': v['snippet']['publishedAt'][:10]} for v in vids]
    except Exception:
        return []


def check():
    toks = tokens()
    reader = None   # irgendein gültiger Zugang für öffentliche Kanaldaten
    for cid in ['couldyoupass'] + list(toks):
        if cid in toks:
            try:
                reader = _build('youtube', 'v3', creds(refresh_token=toks[cid]))
                break
            except Exception as ex:
                print(f'(Leser-Token {cid} unbrauchbar: {str(ex)[:80]})')
    rows = []
    for ch in registry():
        row = {'id': ch['id'], 'name': ch['name'], 'handle': ch['handle'], 'account': ch['account'],
               'kind': ch.get('kind'), 'pipeline': ch.get('pipeline', ''), 'token': ch['id'] in toks}
        item = None
        try:
            if row['token']:
                y = _build('youtube', 'v3', creds(refresh_token=toks[ch['id']]))
                mine = y.channels().list(part='snippet,statistics,contentDetails', mine=True).execute().get('items', [])
                titles = [i['snippet']['title'] for i in mine]
                if any(matches(ch, t) for t in titles):
                    row['status'] = 'verbunden'
                    item = mine[0]
                else:
                    row['status'] = f'FALSCHER KANAL (Token gehört zu {", ".join(titles) or "keinem Kanal"})'
                reader = reader or y
            else:
                row['status'] = 'Token fehlt'
            if item is None and reader and ch['handle']:
                item = _public(reader, ch['handle'])
            if item:
                st = item.get('statistics', {})
                row.update(title=item['snippet']['title'], description=item['snippet'].get('description', '')[:240],
                           subs=int(st.get('subscriberCount', 0)), views=int(st.get('viewCount', 0)),
                           videos=int(st.get('videoCount', 0)), latest=_latest(reader or y, item))
        except SystemExit as ex:
            row['status'] = f'Fehler: {ex}'
        except Exception as ex:
            row['status'] = f'Fehler: {str(ex)[:160]}'
        rows.append(row)
        print(f"{row['name']:<18} {row['status']:<28} Abos={row.get('subs', '?'):<6} Videos={row.get('videos', '?')}")
    now = dt.datetime.now(dt.timezone.utc).strftime('%Y-%m-%d %H:%M UTC')
    STATUS_JSON.write_text(json.dumps({'checked': now, 'channels': rows}, ensure_ascii=False, indent=1), encoding='utf-8')
    ok = sum(1 for r in rows if r['status'] == 'verbunden')
    md = [f'# Studio – Status aller Kanäle', '', f'Stand: {now} · verbunden: **{ok}/{len(rows)}**', '',
          '| Kanal | Zugang | Abos | Videos | Views | Pipeline |', '|---|---|---:|---:|---:|---|']
    for r in rows:
        flag = '✅' if r['status'] == 'verbunden' else ('⏳' if r['status'] == 'Token fehlt' else '❌')
        md.append(f"| {r['name']} | {flag} {r['status']} | {r.get('subs', '–')} | {r.get('videos', '–')} | {r.get('views', '–')} | {r['pipeline']} |")
    md += ['', 'Token fehlt → einmalig lokal `autopilot/kanaele-anmelden.bat` (Windows) bzw. `kanaele-anmelden.command` (Mac).', '']
    for r in rows:
        md.append(f"## {r['name']} {r['handle']}")
        md.append(f"Konto: {r['account']} · Typ: {r.get('kind')}")
        if r.get('description'):
            md.append(f"> {r['description'].replace(chr(10), ' ')}")
        for v in r.get('latest', []):
            md.append(f"- {v['at']} · {v['title']}")
        md.append('')
    STATUS_MD.write_text('\n'.join(md), encoding='utf-8')
    print(f'\n{ok}/{len(rows)} Kanäle verbunden -> channels/{STATUS_MD.name}')


if __name__ == '__main__':
    cmd = sys.argv[1] if len(sys.argv) > 1 else 'check'
    if cmd == 'auth':
        auth(sys.argv[2:])
    elif cmd == 'secret':
        publish()
    elif cmd == 'check':
        check()
    else:
        print(__doc__)
