"""Scoreboard für den Research-Agenten: welche Formate, Themen, Layouts und Musik funktionieren?

Verknüpft jedes hochgeladene Video (autopilot/queue/done/*.json) mit seinen Zahlen aus
autopilot/analytics/report.json und schreibt autopilot/analytics/scoreboard.md (+ .json).
Läuft nach jedem Analytics-Abruf in der Action; braucht kein Netz.
"""
import datetime as dt
import json
import re
import statistics
from collections import defaultdict
from pathlib import Path

AP = Path(__file__).resolve().parent
DONE = AP / "queue" / "done"
REPORT = AP / "analytics" / "report.json"
OUT_MD = AP / "analytics" / "scoreboard.md"
OUT_JSON = AP / "analytics" / "scoreboard.json"


def num(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return None


def short_format(item_id, n):
    if item_id.startswith("auto-"):
        return "Ersatz-Generator (1 Frage)"
    if "one-q" in item_id:
        return "1-Frage-Ego-Hook"
    if item_id.startswith("vs-") or "-vs-" in item_id:
        return "VS-Vergleich"
    if "tf-" in item_id or "true-false" in item_id:
        return "Wahr/Falsch"
    if n <= 3:
        return "3 Fragen"
    if n == 4:
        return "4-Fragen-Trap"
    return "6+ Fragen"


LONG_TOPICS = [
    (r"halloween", "Halloween"), (r"emoji", "Emoji-Raten"), (r"citizenship|can you pass", "Can-You-Pass-Test"),
    (r"over 6|over 7|around 6|memory", "Memory/Alters-Titel"), (r"\biq\b", "IQ-Titel"), (r"19[5-9]0s|decade", "Jahrzehnt"),
    (r"league|football|soccer", "Fußball"), (r"animal", "Tiere"), (r"true or false", "Wahr/Falsch"),
    (r"guess the country|flag|geograph", "Geografie"), (r"general knowledge", "Allgemeinwissen"),
]


def long_topic(title):
    t = title.lower()
    for pat, name in LONG_TOPICS:
        if re.search(pat, t):
            return name
    return "Sonstiges"


def agg(rows):
    pv = [r["publicViews"] for r in rows if r["publicViews"] is not None]
    es = [r["engagedShare"] for r in rows if r["engagedShare"] is not None]
    ap = [r["avgPct"] for r in rows if r["avgPct"] is not None]
    subs = sum(r["subs"] or 0 for r in rows)
    return {
        "n": len(rows),
        "avgViews": round(statistics.mean(pv)) if pv else None,
        "medianViews": round(statistics.median(pv)) if pv else None,
        "bestViews": int(max(pv)) if pv else None,
        "stayed": round(100 * statistics.mean(es), 1) if es else None,
        "avgPct": round(statistics.mean(ap), 1) if ap else None,
        "subs": subs,
    }


def table(title, groups, note=""):
    lines = [f"### {title}", ""]
    if note:
        lines += [note, ""]
    lines += ["| Gruppe | Videos | Ø Views | Median | Bestes | Ø stayed % | Ø angesehen % | Abos |", "|---|---|---|---|---|---|---|---|"]
    for name, a in sorted(groups.items(), key=lambda kv: -(kv[1]["medianViews"] or 0)):
        f = lambda v: "–" if v is None else v
        lines.append(f"| {name} | {a['n']} | {f(a['avgViews'])} | {f(a['medianViews'])} | {f(a['bestViews'])} | "
                     f"{f(a['stayed'])} | {f(a['avgPct'])} | {a['subs']} |")
    return lines + [""]


def main():
    report = json.loads(REPORT.read_text(encoding="utf-8")) if REPORT.exists() else {"videos": []}
    stats = {v["id"]: v for v in report.get("videos", [])}
    now = dt.datetime.now(dt.timezone.utc)
    rows = []
    for path in sorted(DONE.glob("*.json")):
        try:
            item = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        vid = item.get("uploaded", {}).get("videoId")
        if not vid or vid not in stats:
            continue
        s = stats[vid]
        story = item.get("story", {})
        kind = "long" if story.get("format") == "long" else "short"
        n = len(story.get("questions", []))
        pub = s.get("published")
        try:
            age = (now - dt.datetime.fromisoformat(pub.replace("Z", "+00:00"))).total_seconds() / 86400 if pub else None
        except ValueError:
            age = None
        if age is not None and age < 2:
            continue  # zu frisch für einen fairen Vergleich
        title = s.get("title") or item.get("youtube", {}).get("title", "")
        rows.append({
            "file": path.name, "id": item.get("id"), "videoId": vid, "kind": kind, "title": title,
            "format": short_format(item.get("id", ""), n) if kind == "short" else f"{n} Fragen",
            "topic": long_topic(title) if kind == "long" else (story.get("header") or "–").upper(),
            "layout": story.get("layout") or "comic", "music": (story.get("music") or "–").replace("sfx/", ""),
            "slot": (item.get("scheduledFor") or item.get("publishAt") or "")[-11:-6] or item.get("publishAt") or "–",
            "publicViews": num(s.get("publicViews")), "engagedShare": num(s.get("engagedShare")),
            "avgPct": num(s.get("averageViewPercentage")), "subs": num(s.get("subscribersGained")),
            "durationSec": s.get("durationSec"), "ageDays": round(age, 1) if age is not None else None,
            "search": (s.get("trafficSources") or {}).get("YT_SEARCH"),
        })

    md = [f"# Scoreboard – Stand {report.get('fetched', '?')} ({report.get('subscribers', '?')} Abos)", "",
          "Automatisch aus queue/done + report.json (nur Videos, die ≥ 2 Tage online sind). "
          "Views = öffentliche Aufrufe (live); stayed/angesehen/Abos aus YouTube Analytics (2–3 Tage Verzug).", ""]
    out = {"fetched": report.get("fetched"), "groups": {}, "videos": rows}
    for kind, label in (("short", "Shorts"), ("long", "Lange Videos")):
        sub = [r for r in rows if r["kind"] == kind]
        md += [f"## {label} ({len(sub)} Videos)", ""]
        for key, name in (("format", "Format"), ("topic", "Thema/Titeltyp"), ("layout", "Layout"), ("music", "Musik"), ("slot", "Sendezeit")):
            groups = defaultdict(list)
            for r in sub:
                groups[r[key]].append(r)
            g = {k: agg(v) for k, v in groups.items()}
            out["groups"][f"{kind}.{key}"] = g
            md += table(f"{label} nach {name}", g)
        top = sorted(sub, key=lambda r: -(r["publicViews"] or 0))
        md += [f"### Top 8 {label}", ""] + [
            f"- {int(r['publicViews'] or 0)} Views · stayed {r['engagedShare'] if r['engagedShare'] is not None else '–'} · "
            f"{r['format']} · {r['layout']} · {r['music']} · {r['title']}" for r in top[:8]] + [""]
        md += [f"### Flop 5 {label}", ""] + [
            f"- {int(r['publicViews'] or 0)} Views · {r['format']} · {r['title']}" for r in top[-5:]] + [""]
    OUT_MD.write_text("\n".join(md), encoding="utf-8")
    OUT_JSON.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"Scoreboard: {len(rows)} Videos ausgewertet")


if __name__ == "__main__":
    main()
