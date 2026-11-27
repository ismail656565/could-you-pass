# Plan – 2026-11-27 (Fr)

Kanal **61 Abos** (report.json 26.11. 20:02; +6 seit 25.11.). Analytics gesamt (2–3 T Verzug): 43.797 Views → 59 Abos = **1,35 Abos/1.000** (Vortag 1,23). Ziel 2,0 bis 15.12., 100 Abos bis 31.12. (noch 39 in 34 T ≈ 1,1/Tag – Kurs der letzten 4 T ≈ 5/Tag ✓).
Flag Duel trägt weiter: #1 3.836/+20, #2 2.754/+12, #3 1.122/+1, #4 1.516 n. ≈1 T; Real or Fake #1 2.464 (Studio +2). Christmas-Long 3 Views n. ≈17 h (Zähler-Verzug wie immer).
Kommentare: 42 (21 T), **2 offen → 1 beantwortet, 1 Spam („uhijh“) übersprungen**, dazu 1 Nachfass-Antwort an @Pirl1776 (Lithuania-Wunsch erfüllt). Kein Faktenfehler.
Änderungen heute: **Bug gefixt (Queue-Kaskade, s. TECHNIK)** → Flag-Duel-Dateien rücken einen Tag vor, neues Flag Duel #8 für So 29.11.; erster Tag mit 3 Shorts (Missing Symbol #1 12:00).

## TECHNIK-PROBLEM (behoben, Commit 57dec2d)
- **Ursache:** Seit SHORT_SLOTS = 3 (26.11.) nahm `produce()` die Queue nur sortiert nach Namen, ohne Datum. Der Abendlauf 26.11. 17:46 sah „erst 2 Shorts heute“ und produzierte `2026-11-27-flag-duel-5` vorzeitig; da 16:00 vorbei war, ging es **sofort öffentlich (26.11. 17:47)**. Folge: Fr 27.11. 16:00 wäre leer gewesen, und der heutige Lauf hätte `2026-11-28-flag-duel-6` vorgezogen (Kaskade jeden Tag).
- **Fix:** `queue_due()` in autopilot.py – Dateien mit Datum im Namen werden erst an diesem Tag produziert; generate_queue.py zählt nur heute fällige Dateien (sonst kein Ersatz-Short). Syntax + Logik getestet.
- **Daher heute für den Produktions-Agenten (vor dem 08:15-Lauf!):** `git mv queue/2026-11-28-flag-duel-6.json queue/2026-11-27-flag-duel-6.json` und `git mv queue/2026-11-29-flag-duel-7.json queue/2026-11-28-flag-duel-7.json`, dann `2026-11-29-flag-duel-8.json` neu (s. Tabelle). Ohne den Umzug füllt der Ersatz-Generator 16:00 mit einem exam-Short.
- Sonst: alle Läufe 26.11. grün (4 Uploads: Christmas-Long, Flag Duel #4, Real or Fake #2, Flag Duel #5), Kommentar-Läufe ok. CTR per API weiter HttpError 400 (bekannt). Christmas-Long QA-Warnung Standbild 8,6 s (unkritisch).

## Zuschauer
- Beantwortet (replies.json, 26 Einträge, 2 neu): @JellieMaeLopez „4/4“ (Flag Duel #5) · Nachfass @Pirl1776: „You asked, so Lithuania is in Flag Duel #5 …“. Übersprungen: @michaeltomassi5202 „uhijh“ (Kauderwelsch).
- FEHLER-HINWEIS (1, alt): @s_1keb – Mercator-Missverständnis, kein Fehler, am 25.11. beantwortet.
- Scores: 18 gemeldet, 14× 4/4, 1× 0/4 → Flag Duel weiter zu leicht → LEGEND-Runden nur noch echte Doppelgänger (#7 Cuba/Puerto Rico, #8 Andorra/Moldova).
- Wünsche: Science (@Jo-wl5fj) → exam-Long Di 1.12.; Art/Klassik im Backlog. Keine neuen Länderwünsche.

## Diagnose (Videos ≥ 3 T unter Format-Median)
| Video | Views | Ursache | Fix |
|---|---|---|---|
| Rätsel-Long #2 exam (24.11., 3 T) | 29, Ø angesehen 24,8 %, 0 Abos | Titel „12 Hard Riddles“ ohne Suchsog, textlastig, 13–22 s pro Frage → Absprung | **E14b ✗** – keine Text-Rätsel-Longs mehr bis Referenz-Regeln (≤ 10 s/Frage, Bild) umgesetzt; Flag Blitz Sa ist der Test |
| Flag Duel #3 Qatar (24.11., 2,7 T) | 1.122 / +1 Abo (Format-Median ≈2.100) | zu leichte Paare (alle Kommentare 4/4) + erfundener „90%“-Titel; kein zweiter Push | Land im Titel (seit #5), LEGEND = echte Doppelgänger, Like-CTA |
| Karten-VS #8 (24.11.) | 988 / 0 Abos | Format-Ermüdung | eingestellt |
| Thanksgiving T/F tvshow (25.11.) | 136 | Layout + 44 s | gelöscht (Code-Sperre) |
- **KPI Abos/1.000 (Analytics):** Flag Duel #1–#3 **4,4** (33/7.475) · Longs ≈ 3 (wenige Views) · Karten-VS 0,25 · übrige Shorts ≈ 0,6 · gesamt **1,35**. Real or Fake / Missing Symbol noch ohne Analytics.
- Flag Duel #5 lief 26.11. 17:47 ungeplant (Abend, gleicher Tag wie #4) → 880 Views n. ≈9 h; als Kannibalisierungs-Datenpunkt markieren, nicht als Format-Flop werten.

## Konkurrenz-Gewinner heute (competitors.md 26.11.; vidIQ heute nicht abgefragt – 4 Credits)
| # | Video (Kanal, Abos) | Views / × | Länge | Muster | → Slot |
|---|---|---|---|---|---|
| 1 | „Can You Identify These 50 Old Items in Just 7 Seconds?“ (The Quiz Magnet, 8,3k) | 1,18 Mio / 142× | 9:51 | Zeitlimit im Titel + große Zahl, 1 Bild pro Frage | Flag Blitz #1 Sa (3-s-Versprechen) |
| 2 | „Can You Pass the U.S. Citizenship Test? 50 Questions“ (Trivia Square, 4,6k) | 2,82 Mio / 167× | 15:49 | Prüfung = Kanalname, 44 % US-Publikum | Backlog #3 (exam-Long) |
| 3 | „Test Your iQ in just 7 minutes“ (Clear Think, 7,9k) | 1,89 Mio / 1.348× | 6:48 | kurze Zeitangabe statt Fragenzahl | Titelmuster für Science-Long Di |
| 4 | „Christmas Quiz for Adults 🎄 Can You Get 40 Out of 45?“ (Still Sharp Trivia) | 85k / 138× | 18:37 | „for Adults“ + Hürde (passt zu 40 % 65+) | Christmas-Long #2 Do 3.12. |
| 5 | „First To Connect The Words Wins 🚨“ (Studio Seven, 1,5k) | 101k / 19,5× | 1:57 | Duell zu zweit | Backlog #7 („Play with a friend“-Zeile in Flag Duel) |
- Events nächste 7 T: **Albanien + Mauretanien + Panama 28.11.**, 1. Advent 29.11., Barbados + St Andrew's Day 30.11., Rumänien 1.12., **UAE 2.12.**, Laos 2.12., Finnland 6.12.

## 3-Tage-Plan
| Datum / Slot | Format | Thema | Titel (YouTube) | Fragen + timing | Hook / Fragen | Musik | cardColors | Thumbnail | Warum | Erfolg |
|---|---|---|---|---|---|---|---|---|---|---|
| 27.11. 12:00 (Queue) | Missing Symbol #1 (flagduel) | PT/KE/KH/KZ | Queue | 4, outro 0.6 | ohne Vorrede | game-show | – | – | **E27** 3. Slot / Ballandia 95k | ≥ 700 n. 3 T; Median 3-Shorts-Woche ≥ 70 % der 2-Shorts-Woche |
| **27.11. 16:00 – UMZUG** | Flag Duel #6 | DK/CH · GH/CM · EG/YE · NE/IN | Flag Quiz #6: Which One Is Niger? The Last One Is Brutal 🌍 #shorts | 4, think 2.6/move 0.7/tail 0.2/outro 0.6 | Datei `2026-11-28-…` → `2026-11-27-flag-duel-6.json`, Inhalt unverändert | game-show | – | – | Exploit | ≥ 1.500 n. 3 T, ≥ 3 Abos/1k |
| 27.11. 21:00 (Queue) | Real or Fake #3 | DK/AT/FI/NO | Queue | 4 | Queue | game-show | – | – | E24 | Likes ≥ 2 %, stayed ≥ 65 % |
| 28.11. 12:00 (Queue) | Missing Symbol #2 | UG/BB/CY/MT | Queue | 4 | Queue | game-show | – | – | E27 | s. o. |
| 28.11. 14:00 (Queue) | Flag Blitz #1 (Long) | 100 Flaggen | Guess the Flag in 3 Seconds 🌍 100 Flags – Easy to Impossible | 100, think 3.0 | Queue | Queue | – | „80/100?“ / „IMPOSSIBLE?“ | **E26** (Quiz Blitz / Quiz Magnet) | ≥ 150 n. 3 T, Ø angesehen ≥ 25 %, ≥ 1 Abo |
| **28.11. 16:00 – UMZUG** | Flag Duel #7 | JP/BD · PE/CA · GR/UY · CU/PR | Flag Quiz #7: Which One Is Cuba? The Last One Is Brutal 🌍 #shorts | 4, s. o. | `2026-11-29-…` → `2026-11-28-flag-duel-7.json` | game-show | – | – | Exploit, härtere LEGEND | ≥ 1.500 n. 3 T |
| 28.11. 21:00 (Queue) | Real or Fake #4 | USA/BR/TR/GB | Queue | 4 | Queue | game-show | – | – | E24/E25 | > Ø(#1–#3) n. 24 h |
| 29.11. 12:00 (Queue) | Missing Symbol #3 | BT/PG/MN/SZ | Queue | 4 | Queue | game-show | – | – | E27 | s. o. |
| **29.11. 16:00 – NEU** (1. Advent) | Flag Duel #8 | EASY **Ireland/Italy** · MEDIUM **Slovenia/Russia** · HARD **Venezuela/Ecuador** · LEGEND **Andorra/Moldova** | Flag Quiz #8: Which One Is Moldova? The Last One Is Brutal 🌍 #shorts | 4, s. o. | hookLine "" · Q1 „Who is Ireland? Left, or right?“ · Gewinner a/b/a/b · letzte Zeile „Got all four? Hit like, and follow!“ · Schlusskarte „Follow for number nine“ | game-show | – | – | Exploit + echte Doppelgänger (14/18 Scores 4/4) | ≥ 1.500 n. 3 T, Score-Kommentare < 70 % 4/4 |
| 29.11. 21:00 (Queue) | Real or Fake #5 | KR/GR/ES/CL | Queue | 4 | Queue | game-show | – | – | E24/E25 | s. o. |

Vorschau: Mo 30.11. Flag Duel #9 + Real or Fake #6 (Barbados-Nationalfeiertag 30.11.: Barbados nur, wenn nicht schon in Missing Symbol #2 → stattdessen Romania für 1.12.). **Di 1.12. 14:00 Long = science-quiz-30-1 (exam, Wunsch @Jo-wl5fj)**, Titel „Science Quiz: 30 Questions – Can You Get 25? 🔬“, B „CAN YOU GET **25/30**?“, Kommentar „You asked for it – science!“. **Mi 2.12. Real or Fake: „Can You Spot the Real UAE Flag?“** (Nationalfeiertag).
Bandit 27.–29.11. (10 Slots): 6 Exploit (Flag Duel/Real or Fake), 4 Experiment (E27 Missing Symbol ×3, E26 Flag Blitz).

## Ideen-Backlog
1. Flag Duel + Real or Fake täglich – einziges Format über 2 Abos/1k (Flag Duel 4,4).
2. Science-Long Di 1.12. (Zuschauer-Wunsch) – Bindung + Long-Abos.
3. „Can You Pass the U.S. Citizenship Test?“ exam-Long – Trivia Square 2,8 Mio, Kanalname-Match, 44 % US.
4. Flag Blitz #2 „Guess the Country by Its Shape in 3 Seconds“ – falls #1 ≥ 150 n. 3 T.
5. Christmas Quiz #2 „for Adults – Can You Get 40/45?“ (Still Sharp 85k) Do 3.12., Bilder statt Text.
6. Nationaltags-Folgen mit Land im Titel (UAE 2.12., Finnland 6.12., Kenia 12.12.).
7. „Play with a friend – first to 4/4 wins“ als Zusatz in Flag-Duel-Beschreibung/Kommentar (Studio Seven 101k).
8. „Brain Test“-Long für 65+-Publikum (40 %) ohne Altersangabe im Titel, 10–15 Fragen, großes Bild.
9. Flaggen-Gitter „One Flag Is Wrong“ (Flag Pals 18k) – neuer Renderer nötig.
10. Art-Trivia-Short im exam-Hochformat (≤ 4 Fragen) – Wunsch @Jo-wl5fj.

## Für den Produktions-Agenten (heute)
1. **ZUERST (vor 08:15-Lauf):** `git mv autopilot/queue/2026-11-28-flag-duel-6.json autopilot/queue/2026-11-27-flag-duel-6.json` und `git mv autopilot/queue/2026-11-29-flag-duel-7.json autopilot/queue/2026-11-28-flag-duel-7.json` (publishAt 16:00 bleibt), sofort pushen. Titel auf „Flag Quiz #6: Which One Is Niger? The Last One Is Brutal 🌍 #shorts“ bzw. „#7: Which One Is Cuba? …“ setzen, falls noch anders.
2. **Anlegen:** `2026-11-29-flag-duel-8.json` (16:00) exakt wie Tabelle; alle 8 SVGs prüfen (ie, it, si, ru, ve, ec, ad, md); fehlt eines → LEGEND Ersatz Romania/Chad ist verbraucht, dann Senegal/Cameroon nehmen (gegen Paare-Liste prüfen).
3. Flag-Serien: hookLine "", timing {think 2.6, move 0.7, tail 0.2, outro 0.6}, Antworten ≤ 3 Wörter, ≤ 27 s, Like-CTA, angepinnter Kommentar „Comment your score AND your country – we pick countries from the comments for the next episodes!“.
4. Benutzte Paare nie wiederholen: pl/id, ie/ci, au/nz, td/ro, is/no, ml/sn, nl/lu, si/sk, lv/at, ec/co, ht/li, qa/bh, it/mx, bg/hu, ni/hn, gn/ml, us/lr, be/de, lt/bo, kw/ae, dk/ch, gh/cm, eg/ye, ne/in, jp/bd, pe/ca, gr/uy, cu/pr (+ #8 heute: ie/it, si/ru, ve/ec, ad/md).
5. Queue-Dateien mit Zukunftsdatum werden ab jetzt erst an ihrem Tag produziert (Fix 57dec2d) – Dateiname = Sendetag ist jetzt Pflicht.
6. Titel ohne erfundene Prozente. Keine Halloween-/Alters-/Politik-Themen, Longs nur Di/Do/Sa, Shorts 12:00/16:00/21:00.
