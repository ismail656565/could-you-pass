"""Zuschauer-Kommentare lesen + Antworten posten (seit 22.11.2026, Besitzer: „Liest du die Comments? … interagiere“).

fetch(ap)  → autopilot/analytics/comments.json + comments.md
             alle Kommentare der letzten 21 Tage auf dem Kanal (auch Antworten unter unserem Erst-Kommentar),
             grob sortiert: FEHLER-HINWEIS / WUNSCH / SCORE / FRAGE / SONSTIGES, Flag „unbeantwortet“.
post_replies(ap) → liest autopilot/replies.json (vom Research-Agenten geschrieben):
             [{"commentId": "<id des Kommentars, auf den wir antworten>", "text": "…"}]
             Antwort wird immer an den Top-Level-Thread gehängt (YouTube kennt nur eine Ebene).
             Erledigte bekommen "posted": "<Zeit>" bzw. "error"; max. 40 pro Lauf.
Wir löschen/verstecken nie etwas und liken nichts (API kann kein Herz)."""
import datetime as dt
import json
import re

DAYS = 21
MAX_REPLIES = 40

FIX = re.compile(r"\b(wrong|incorrect|not correct|isn'?t correct|actually|mistake|error|false|not true|that'?s not|it'?s not|should be|typo|misspel)", re.I)
WISH = re.compile(r"\b(do an?|make an?|can you (do|make)|next (one|time|quiz)|please (do|make)|more of|part 2|another one|i want|we want)", re.I)
FRAC = re.compile(r"\b(\d{1,2})\s*(/|out of)\s*(\d{1,2})\b", re.I)
SCORE = re.compile(r"\b(\d{1,2})\s*(/|out of|of)\s*(\d{1,2})\b|\bgot (all|\d+)\b|\b(\d{1,2}) right\b", re.I)


def _kind(text):
    if FIX.search(text):
        return 'FEHLER-HINWEIS'
    if WISH.search(text):
        return 'WUNSCH'
    if SCORE.search(text):
        return 'SCORE'
    if '?' in text:
        return 'FRAGE'
    return 'SONSTIGES'


def fetch(ap):
    y = ap.yt()
    me = y.channels().list(part='id', mine=True).execute()['items'][0]['id']
    since = dt.datetime.now(dt.timezone.utc) - dt.timedelta(days=DAYS)
    titles = {}
    for d in ap.DONE.glob('*.json'):
        try:
            it = json.loads(d.read_text(encoding='utf-8'))
            vid = (it.get('uploaded') or {}).get('videoId')
            if vid:
                titles[vid] = (it.get('youtube') or {}).get('title', it.get('id'))
        except Exception:
            pass
    out, token, pages = [], None, 0
    while pages < 8:
        r = y.commentThreads().list(part='snippet,replies', allThreadsRelatedToChannelId=me, maxResults=100, order='time',
                                    textFormat='plainText', pageToken=token).execute()
        pages += 1
        stop = False
        for th in r.get('items', []):
            top = th['snippet']['topLevelComment']
            ts = top['snippet']
            pub = dt.datetime.fromisoformat(ts['publishedAt'].replace('Z', '+00:00'))
            last = dt.datetime.fromisoformat(th['snippet'].get('updatedAt', ts['publishedAt']).replace('Z', '+00:00')) if th['snippet'].get('updatedAt') else pub
            if pub < since and last < since:
                stop = True
                continue
            vid = th['snippet'].get('videoId') or ts.get('videoId')
            reps = list((th.get('replies') or {}).get('comments', []))
            if th['snippet'].get('totalReplyCount', 0) > len(reps):
                try:
                    reps = y.comments().list(part='snippet', parentId=top['id'], maxResults=100, textFormat='plainText').execute().get('items', [])
                except Exception:
                    pass
            def author(s):
                return (s.get('authorChannelId') or {}).get('value')
            items = [(top['id'], ts)] + [(c['id'], c['snippet']) for c in reps]
            mine_after = [dt.datetime.fromisoformat(s['publishedAt'].replace('Z', '+00:00')) for _, s in items if author(s) == me]
            for cid, s in items:
                if author(s) == me:
                    continue
                p = dt.datetime.fromisoformat(s['publishedAt'].replace('Z', '+00:00'))
                if p < since:
                    continue
                text = s.get('textDisplay') or s.get('textOriginal') or ''
                out.append({
                    'commentId': cid, 'threadId': top['id'], 'videoId': vid, 'video': titles.get(vid, vid),
                    'author': s.get('authorDisplayName'), 'text': text[:600], 'likes': s.get('likeCount', 0),
                    'published': s['publishedAt'], 'kind': _kind(text),
                    'answered': any(m > p for m in mine_after),
                    'underOurComment': cid != top['id'] and author(ts) == me,
                })
        token = r.get('nextPageToken')
        if stop or not token:
            break
    out.sort(key=lambda c: c['published'], reverse=True)
    (ap.ANALYTICS / 'comments.json').write_text(json.dumps({'fetched': dt.datetime.now().isoformat(timespec='minutes'), 'comments': out}, indent=1, ensure_ascii=False), encoding='utf-8')
    write_md(ap, out)
    open_n = sum(1 for c in out if not c['answered'])
    ap.log(f'Kommentare: {len(out)} Zuschauer-Kommentare ({DAYS} T), {open_n} unbeantwortet, {sum(1 for c in out if c["kind"] == "FEHLER-HINWEIS")} Fehler-Hinweise')
    return out


def write_md(ap, out):
    order = ['FEHLER-HINWEIS', 'WUNSCH', 'FRAGE', 'SCORE', 'SONSTIGES']
    scores = []
    for c in out:
        m = FRAC.search(c['text'])
        if m:
            try:
                a, b = int(m.group(1)), int(m.group(3))
                if 0 < b <= 60 and a <= b:
                    scores.append((c['video'], a, b))
            except ValueError:
                pass
    lines = [f'# Zuschauer-Kommentare – Stand {dt.datetime.now().strftime("%Y-%m-%d %H:%M")}', '',
             f'Letzte {DAYS} Tage, ohne unsere eigenen. {len(out)} Kommentare, {sum(1 for c in out if not c["answered"])} unbeantwortet.',
             'Antworten: Einträge in autopilot/replies.json ({"commentId": "…", "text": "…"}) – der nächste Kommentar-Lauf postet sie.', '']
    if scores:
        lines += ['## Gemeldete Ergebnisse', '', '| Video | Score |', '|---|---|'] + [f'| {v[:60]} | {a}/{b} |' for v, a, b in scores[:30]] + ['']
    for k in order:
        grp = [c for c in out if c['kind'] == k]
        if not grp:
            continue
        lines += [f'## {k} ({len(grp)})', '']
        for c in grp[:60]:
            flag = '' if c['answered'] else ' **[OFFEN]**'
            lines.append(f"- {c['published'][:10]} · {c['video'][:50]} · {c['author']}{flag} · id `{c['commentId']}`  \n  „{c['text'][:300].replace(chr(10), ' ')}“")
        lines.append('')
    (ap.ANALYTICS / 'comments.md').write_text('\n'.join(lines), encoding='utf-8')


def post_replies(ap):
    p = ap.AP / 'replies.json'
    if not p.exists():
        return 0
    try:
        todo = json.loads(p.read_text(encoding='utf-8'))
    except Exception as ex:
        ap.log('replies.json unlesbar:', str(ex)[:120])
        return 0
    known = {}
    cj = ap.ANALYTICS / 'comments.json'
    if cj.exists():
        try:
            known = {c['commentId']: c['threadId'] for c in json.loads(cj.read_text(encoding='utf-8')).get('comments', [])}
        except Exception:
            pass
    y, n = None, 0
    for r in todo:
        if r.get('posted') or r.get('error') or not (r.get('text') or '').strip() or not r.get('commentId'):
            continue
        if n >= MAX_REPLIES:
            break
        y = y or ap.yt()
        parent = r.get('threadId') or known.get(r['commentId']) or r['commentId']
        try:
            y.comments().insert(part='snippet', body={'snippet': {'parentId': parent, 'textOriginal': r['text'].strip()[:900]}}).execute()
            r['posted'] = dt.datetime.now().isoformat(timespec='minutes')
            n += 1
        except Exception as ex:
            r['error'] = str(ex)[:200]
    p.write_text(json.dumps(todo, indent=1, ensure_ascii=False), encoding='utf-8')
    if n:
        ap.log(f'Kommentar-Antworten gepostet: {n}')
    return n
