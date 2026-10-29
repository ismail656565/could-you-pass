"""Kostenloser vidIQ-Ersatz für Keyword-Recherche (läuft in der GitHub Action).

1) YouTube-Autocomplete (dieselben Vorschläge wie im YouTube-Suchfeld):
   für jeden Seed + Buchstaben a–z. Häufigkeit + Position = Nachfrage-Signal
   (je öfter und weiter oben ein Begriff vorgeschlagen wird, desto mehr wird er gesucht).
2) Google Trends, Suchbereich "YouTube": steigende ("rising") und Top-Suchanfragen
   der letzten 30 Tage je Seed. Google blockt Cloud-IPs manchmal (429) – dann fehlt
   nur dieser Teil, der Rest läuft weiter.

Ergebnis: autopilot/analytics/keywords.md (+ keywords.json). Keine API-Schlüssel nötig.
"""
import datetime as dt
import json
import string
import sys
import time
from collections import defaultdict
from pathlib import Path

import requests

AP = Path(__file__).resolve().parent
OUT_MD = AP / "analytics" / "keywords.md"
OUT_JSON = AP / "analytics" / "keywords.json"

SEEDS = [
    "quiz", "trivia", "general knowledge quiz", "animal quiz", "geography quiz",
    "history quiz", "science quiz", "which is bigger", "guess the", "can you pass",
    "memory test", "emoji quiz", "true or false quiz", "country quiz",
]
TREND_SEEDS = ["quiz", "trivia", "general knowledge quiz", "guess the", "which is bigger"]

S = requests.Session()
S.headers["User-Agent"] = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                           "(KHTML, like Gecko) Chrome/124.0 Safari/537.36")


def suggest(q):
    r = S.get("https://suggestqueries.google.com/complete/search",
              params={"client": "firefox", "ds": "yt", "hl": "en", "gl": "us", "q": q}, timeout=15)
    r.raise_for_status()
    data = json.loads(r.content.decode("utf-8", "replace"))
    return [s for s in data[1] if isinstance(s, str)]


def autocomplete():
    score = defaultdict(float)
    hits = defaultdict(int)
    per_seed = {}
    for seed in SEEDS:
        found = []
        for suffix in [""] + [f" {c}" for c in string.ascii_lowercase]:
            try:
                sugg = suggest(seed + suffix)
            except Exception as ex:  # einzelne Fehlschläge ignorieren
                print("autocomplete", seed + suffix, ex, file=sys.stderr)
                time.sleep(2)
                continue
            for pos, s in enumerate(sugg[:10]):
                score[s] += (10 - pos) / 10
                hits[s] += 1
                if suffix == "":
                    found.append(s)
            time.sleep(0.25)
        per_seed[seed] = found
    ranked = sorted(score.items(), key=lambda kv: -kv[1])
    return per_seed, [{"keyword": k, "score": round(v, 2), "hits": hits[k]} for k, v in ranked[:120]]


def _trends_json(text):
    return json.loads(text[text.index("{"):])


def trends(seed):
    """Rising/Top-Suchanfragen auf YouTube (Google Trends, gprop=youtube), 30 Tage, weltweit."""
    S.get("https://trends.google.com/trends/explore", params={"q": seed, "gprop": "youtube"}, timeout=20)
    req = {"comparisonItem": [{"keyword": seed, "geo": "", "time": "today 1-m"}], "category": 0, "property": "youtube"}
    r = S.get("https://trends.google.com/trends/api/explore",
              params={"hl": "en-US", "tz": "0", "req": json.dumps(req)}, timeout=20)
    r.raise_for_status()
    widgets = _trends_json(r.text)["widgets"]
    w = next(x for x in widgets if x.get("id") == "RELATED_QUERIES")
    r = S.get("https://trends.google.com/trends/api/widgetdata/relatedsearches",
              params={"hl": "en-US", "tz": "0", "req": json.dumps(w["request"]), "token": w["token"]}, timeout=20)
    r.raise_for_status()
    lists = _trends_json(r.text)["default"]["rankedList"]
    top = [(k["query"], k.get("formattedValue", "")) for k in lists[0]["rankedKeyword"]] if lists else []
    rising = [(k["query"], k.get("formattedValue", "")) for k in lists[1]["rankedKeyword"]] if len(lists) > 1 else []
    return {"top": top[:15], "rising": rising[:15]}


def main():
    today = dt.date.today().isoformat()
    per_seed, ranked = autocomplete()
    tr, tr_err = {}, None
    for seed in TREND_SEEDS:
        try:
            tr[seed] = trends(seed)
        except Exception as ex:
            tr_err = f"{type(ex).__name__}: {str(ex)[:150]}"
            print("trends", seed, tr_err, file=sys.stderr)
            if "429" in str(ex):
                break
        time.sleep(4)

    OUT_JSON.write_text(json.dumps({"date": today, "autocomplete": per_seed, "ranked": ranked, "trends": tr,
                                    "trendsError": tr_err}, ensure_ascii=False, indent=1), encoding="utf-8")
    md = [f"# Keyword-Recherche (kostenlos, vidIQ-Ersatz) – {today}", "",
          "Quelle 1: YouTube-Autocomplete (Seed + a–z). Score = Summe (10 − Position)/10 über alle Abfragen → höher = häufiger gesucht.",
          "Quelle 2: Google Trends, Suchbereich YouTube, letzte 30 Tage (rising = stark wachsend, 'Breakout' = >5000 %).", "",
          "## Top-Suchbegriffe (Autocomplete-Score)", "", "| # | Suchbegriff | Score | Treffer |", "|---|---|---|---|"]
    md += [f"| {i} | {r['keyword']} | {r['score']} | {r['hits']} |" for i, r in enumerate(ranked[:60], 1)]
    md += ["", "## Direkte Vorschläge je Seed", ""]
    md += [f"- **{seed}**: " + ", ".join(found) for seed, found in per_seed.items()]
    md += ["", "## Google Trends (YouTube) – rising / top", ""]
    if not tr:
        md.append(f"_nicht verfügbar ({tr_err})_")
    for seed, d in tr.items():
        md.append(f"- **{seed}** – rising: " + (", ".join(f"{q} ({v})" for q, v in d["rising"]) or "–"))
        md.append(f"  - top: " + (", ".join(f"{q} ({v})" for q, v in d["top"]) or "–"))
    OUT_MD.write_text("\n".join(md) + "\n", encoding="utf-8")
    print(f"Keywords: {len(ranked)} Begriffe, Trends für {len(tr)} Seeds" + (f" (Fehler: {tr_err})" if tr_err else ""))


if __name__ == "__main__":
    main()
