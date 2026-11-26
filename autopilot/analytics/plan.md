# Plan – 2026-11-26 (Do)

Kanal **55 Abos** (report.json 25.11. 20:25; +2 seit 24.11. 21:03). Analytics gesamt (2–3 T Verzug): 40.795 Views → 50 Abos = **1,23 Abos/1.000** (Vortag 1,18). Ziel 2,0 bis 15.12., 100 Abos bis 31.12. (noch 45 in 35 T ≈ 1,3/Tag – Kurs der letzten 3 T ≈ 4/Tag).
Flaggen-Serien tragen den Kanal: Flag Duel #1 3.805 Views/+19 Abos, #2 2.649/+5 (Analytics noch unvollständig, Studio +12), #3 1.060 n. ≈1,2 T; Real or Fake #1 1.417 n. 1,5 h (Besitzer), 70–72 % stayed = Kanal-Rekord.
Kommentare: 39 (21 T), **0 offen** – alle beantwortet (24 Antworten gesamt), kein bestätigter Faktenfehler.
Änderungen heute: **Flag Duel ab Fr 27.11. täglich 16:00** (Datei-Umbenennung #5 → 27.11., neues #6 für 28.11.), neue Folgen #7 / Real or Fake #5 für So 29.11.; keine neuen Formate (Bandit: Flag Blitz Sa ist das laufende Experiment).

## TECHNIK-PROBLEM
- Keine Ausfälle. Log 25.11.: 2/2 Shorts hochgeladen (true-false-thanksgiving 16:00, real-fake-flag-1 21:00), Kommentare + 1 Antwort gepostet (23:41), Analytics 17:59 + 20:25 ok, QA ok.
- **Offener Auftrag aus Nachtrag 25.11. noch nicht erledigt:** Für **Fr 27.11. 16:00 liegt kein Short in der Queue** (nur real-fake-flag-3 21:00). → Produktions-Agent heute zuerst (s. unten). Ohne Fix fehlt morgen ein Slot.
- Rätsel-Long #2 (exam, 24.11.) 26 Views n. ≈1,7 T – kein Bug (Status public), aber Flop-Kurs → Verdict morgen.

## Zuschauer
- 39 Kommentare, 0 offen → nichts zu posten. replies.json unverändert (24 Einträge, alle gepostet).
- FEHLER-HINWEIS (2): @s_1keb (Karten-VS #8, Mercator-Verständnis – kein Fehler, am 25.11. erklärt beantwortet), @AdnanSadaqat-q7d (Score-Kommentar „1 wrong“, kein Fehler). Keine Korrektur nötig.
- Länder aus Kommentaren (Regel 26.11.): @Pirl1776 „lets go lithuania mentioned“ → Lithuania ist im Flag Duel #5 (Fr 27.11., Bolivia/Lithuania) → Beschreibung #5 „Requested by @Pirl1776“; Antwort nach Upload: „Lithuania is back in Flag Duel #5 – did you spot it?“ (Research-Agent 28.11.).
- Wünsche: Science (@Jo-wl5fj) → exam-Long Di 1.12.; Art/Klassik im Backlog.
- 13 von 14 gemeldeten Scores sind 4/4 → LEGEND-Runde härter machen (echte Doppelgänger, s. #7 Cuba/Puerto Rico).

## Diagnose (Videos ≥ 3 T unter Format-Median)
| Video | Views | Ursache | Fix |
|---|---|---|---|
| Thanksgiving-Long (21.11., 5 T) | 101 | zu spät für Saisonsuche, Ø angesehen 28 %, Textlastig | Feiertags-Longs ≥ 3 Wochen vorher; neue Longs nach Referenz-Regeln (≤ 10 s/Frage, Bild statt Text) – Flag Blitz Sa |
| Karten-VS #7 (23.11.) / #8 (24.11.) | 943 / 699 | Format-Ermüdung, 0,37 Abos/1k | eingestellt (Besitzer 24.11.) |
| Rätsel-Long #2 (24.11., 1,7 T) | 26 | Titel „12 Hard Riddles“ ohne Suchvolumen + textlastiger exam-Look, Zähler-Verzug | nicht wiederholen; Rätsel #3 im Backlog nur mit 10 Rätseln + neuer Titelformel. Verdict 27.11. |
| Thanksgiving T/F tvshow (25.11., 1 T) | 110 | Layout (Besitzer), 44 s zu lang | Layout gelöscht, Code-Sperre aktiv |
- **KPI Abos/1.000 (Analytics):** Flag Duel ≈ 5,0 (24/6.454) · Longs ≈ 3 · übrige Shorts ≈ 0,7 · Karten-VS 0,37 (eingestellt) · gesamt 1,23.
- Flag Duel #3 (Qatar) 1.060 n. 1,2 T liegt unter #2 (2.649) → Titel „90% Pick Wrong“ (erfunden, jetzt verboten) war bei #2/#3 gleich; Unterschied eher Paare (Austria/Latvia zu leicht). Verdict E22 morgen mit #4.

## Konkurrenz-Gewinner heute (competitors.md 25.11. + vidIQ-Outliers 24./25.11.; vidIQ heute nicht abgefragt – nur 4 Credits)
| # | Video (Kanal, Abos) | Views / × | Länge | Muster | → Slot |
|---|---|---|---|---|---|
| 1 | „Can You Find The Real Grenada Flag?“ (Globonk, 1,9k) | 48,8k | 0:25 | echte Flagge EINES Landes im Titel | Real or Fake #4 „Spot the Real USA“ (Sa), #5 „Spot the Real South Korea“ (So) |
| 2 | „Which One Is INDONESIA? Left or Right?! 4 Levels“ (ThinkBop!, 2,5k) | 14,6k / 14× | 0:26 | exakt Flag Duel, Zielland im Titel | Flag Duel #5–#7 Titel „Which One Is X?“ |
| 3 | „Guess the Flag by Its Missing Symbol Part 3“ (Ballandia, 27k) | 95,3k | 0:47 | Teil-Nummer, Symbol fehlt | Backlog #3 (Real or Fake Variante) |
| 4 | „First To Connect The Words Wins 🚨“ (Studio Seven, 1,5k) | 100,8k / 18× | 1:57 | Duell-Rahmen „first to … wins“, Mitspielen zu zweit | Backlog #8 (Titelmuster „First to Spot the Real Flag Wins“) |
| 5 | „Your Brain Is Ageless! 10-Question IQ Quiz“ (GK STUDIO PRO, 2k) | 46,8k / 50× | 7:14 | wenige Fragen, Senioren-Publikum (wir: 40 % 65+!) | Backlog #5 Long-Idee „Brain Test for Seniors“ (ohne Altersangabe im Titel) |
- Events nächste 7 T: Thanksgiving heute, Black Friday 27.11., **1. Advent So 29.11.**, St Andrew's Day 30.11. (Schottland), Barbados 30.11., Rumänien 1.12., **UAE 2.12.** (Kuwait/UAE schon in #5 → Kommentar-Hinweis), Finnland 6.12.

## 3-Tage-Plan
| Datum / Slot | Format | Thema | Titel (YouTube) | Fragen + timing | Hook / Fragen | Musik | cardColors | Thumbnail | Warum | Erfolg |
|---|---|---|---|---|---|---|---|---|---|---|
| 26.11. 14:00 (Queue) | QuizLong exam, 50 Q | Christmas | Christmas Quiz 2026 🎄 50 Questions – Can You Get 40? | 50 | Queue | brain-pulse | #B91C1C/#14532D | B „CAN YOU GET **40/50**?“ | Saison | ≥ 100 n. 3 T |
| 26.11. 16:00 (Queue) | Flag Duel #4 | IT/MX, BG/HU, NI/HN, GN/ML | Flag Quiz #4: Left or Right? Can You Get 4/4? 🌍 #shorts | 4, E23 | ohne Vorrede | game-show | – | – | E22 | > Ø(#2,#3) n. 24 h |
| 26.11. 21:00 (Queue) | Real or Fake #2 | CA/IT/CH/JP | Real or Fake Flag? #2 Can You Spot All 4? 🧐 #shorts | 4, E23 | ohne Vorrede, Like-CTA | game-show | – | – | E24 | Likes ≥ 2 %, stayed ≥ 65 % |
| **27.11. 16:00 – UMZUG** | Flag Duel #5 | USA/Liberia · Belgium/Germany · Lithuania/Bolivia · Kuwait/UAE | Flag Quiz #5: Which One Is Liberia? The Last One Is Brutal 🌍 #shorts | 4, E23, outro 0.6 | Datei `2026-11-28-flag-duel-5.json` → `2026-11-27-flag-duel-5.json`; Schluss „Follow for number six!“; Beschreibung „Requested by @Pirl1776 (Lithuania)“ | game-show | – | – | Exploit + E25 Land im Titel | ≥ 1.500 n. 3 T, ≥ 3 Abos/1k |
| 27.11. 21:00 (Queue) | Real or Fake #3 | DK/AT/FI/NO | Real or Fake Flag? #3 Can You Spot All 4? 🧐 #shorts | 4, E23 | Queue | game-show | – | – | E24 | s. o. |
| 28.11. 14:00 (Queue) | Flag Blitz #1 (Long, flagblitz) | 100 Flaggen | Guess the Flag in 3 Seconds 🌍 100 Flags – Easy to Impossible | 100, think 3.0 | Queue; Thumbnail „80/100?“ / „IMPOSSIBLE?“ | Queue | – | Collage | Experiment E26 (Referenz Quiz Blitz) | ≥ 150 n. 3 T, Ø angesehen ≥ 25 %, ≥ 1 Abo |
| **28.11. 16:00 – NEU** | Flag Duel #6 | EASY Denmark/Switzerland · MEDIUM Ghana/Cameroon · HARD Egypt/Yemen · LEGEND Niger/India | Flag Quiz #6: Which One Is Niger? The Last One Is Brutal 🌍 #shorts | 4, E23, outro 0.6 | Q1 „Who is Denmark? Left, or right?“ · Gewinner a/b/a/b · Schluss „Follow for number seven!“ | game-show | – | – | Exploit + E25 | ≥ 1.500 n. 3 T |
| 28.11. 21:00 (Queue) | Real or Fake #4 | USA/Brazil/Turkey/UK | Real or Fake Flag? #4 Can You Spot the Real USA? 🧐 #shorts | 4, E23 | Queue | game-show | – | – | E24/E25 | > Ø(#1–#3) n. 24 h |
| **29.11. 16:00 – NEU** (1. Advent) | Flag Duel #7 | EASY Japan/Bangladesh · MEDIUM Peru/Canada · HARD Greece/Uruguay · LEGEND **Cuba/Puerto Rico** (Farben vertauscht – härter, weil 13/14 Scores 4/4) | Flag Quiz #7: Which One Is Cuba? The Last One Is Brutal 🌍 #shorts | 4, E23, outro 0.6 | Gewinner b/a/b/a · Schluss „Follow for number eight!“ | game-show | – | – | Exploit, härtere LEGEND | ≥ 1.500 n. 3 T |
| **29.11. 21:00 – NEU** | Real or Fake #5 | **South Korea** (Trigramme vertauscht), **Greece** (Kanton unten links), **Spain** (3 gleich breite Streifen), **Chile** (blaues Feld mit Stern rechts statt links) | Real or Fake Flag? #5 Can You Spot the Real South Korea? 🧐 #shorts | 4, E23 | Fakes neu bauen (public/flags/fake/kr,gr,es,cl) · nicht Argentinien ohne Sonne (echte Variante) · Gewinner a/b/b/a · Schluss „Follow for number six!“ | game-show | – | – | E24/E25 | s. o. |

Vorschau: Mo 30.11. Flag Duel #8 (Vorschlag Slovenia/Russia, Romania/Andorra, Ireland/Italy, Venezuela/Ecuador – vorher gegen Paare-Liste prüfen) + Real or Fake #6 (St Andrew's Day: Fake-Saltire, falls `gb-sct.svg` existiert). **Di 1.12. Long 14:00 = science-quiz-30-1 (exam, Zuschauer-Wunsch)**, Titel „Science Quiz: 30 Questions – Can You Get 25?“, B „CAN YOU GET **25/30**?“, Kommentar „You asked for it – science! 🔬“.
Bandit 26.–29.11. (11 Slots): 8 Exploit (Flag Duel/Real or Fake/Christmas), 3 Experiment (E22 Titel, E25 Land im Titel, E26 Flag Blitz).

## Ideen-Backlog
1. Flag Duel + Real or Fake täglich – einziges Format über 2 Abos/1k (≈5,0).
2. Science-Long (Wunsch @Jo-wl5fj) Di 1.12. – Viewer-Bindung + Longs ≈3 Abos/1k.
3. „Missing Symbol“-Real-or-Fake (Wappen/Stern entfernt) – Ballandia 95k, gleicher Renderer.
4. Flag Blitz #2 „Guess the Country by Its Shape in 3 Seconds“ – falls Flag Blitz #1 ≥ 150 n. 3 T (Formen in truesize.json vorhanden).
5. „Brain Test“-Long für unser 65+-Publikum (40 %!) – GK STUDIO PRO 46,8k; nur 10–15 Fragen, großes Bild, ohne Alter im Titel.
6. Nationaltags-Folgen (UAE 2.12., Finnland 6.12.) mit Ländernamen im Titel.
7. „Can You Pass the U.S. Citizenship Test?“ exam-Long – Trivia Square 2,8 Mio, passt zum Kanalnamen, 44 % US-Publikum.
8. Titelmuster „First to Spot the Real Flag Wins“ für Real or Fake (Studio Seven 100k) – Duell-Gefühl für Paare/Familien.
9. Flaggen-Gitter „One Flag Is Wrong“ (Flag Pals 18k) – neuer Renderer nötig.
10. Art-Trivia-Short im exam-Hochformat (≤ 4 Fragen) – Wunsch @Jo-wl5fj.

## Für den Produktions-Agenten (heute)
1. **Zuerst:** `git mv autopilot/queue/2026-11-28-flag-duel-5.json autopilot/queue/2026-11-27-flag-duel-5.json` (publishAt 16:00 bleibt). Beschreibung ergänzen: „Lithuania requested by @Pirl1776 🇱🇹“.
2. **Anlegen:** `2026-11-28-flag-duel-6.json` (16:00), `2026-11-29-flag-duel-7.json` (16:00), `2026-11-29-real-fake-flag-5.json` (21:00) – Paare/Fakes/Titel exakt wie in der Tabelle.
3. Flag-Serien: hookLine "", timing {think 2.6, move 0.7, tail 0.2, outro 0.6}, Antworten ≤ 3 Wörter, ≤ 27 s, Schluss „Follow for number N+1!“, angepinnter Kommentar „Comment your score AND your country – we pick countries from the comments for the next episodes!“.
4. Benutzte Paare nie wiederholen: pl/id, ie/ci, au/nz, td/ro, is/no, ml/sn, nl/lu, si/sk, lv/at, ec/co, ht/li, qa/bh, it/mx, bg/hu, ni/hn, gn/ml, us/lr, be/de, lt/bo, kw/ae (+ #6/#7 heute). Fakes benutzt: fr/de/lt/se/ca/it/ch/jp/dk/at/fi/no/us/br/tr/gb.
5. Neue Fakes kr/gr/es/cl gegen alle 270 Flaggen prüfen (darf keiner echten gleichen), Probe-Still rendern. Keine politisch umstrittenen Flaggen.
6. Titel ohne erfundene Prozente („90%“, „1 in 10“, „99%“ verboten). Keine Halloween-/Alters-/Politik-Themen, keine Longs Mo/Mi/Fr/So, max. 2 Shorts/Tag.
