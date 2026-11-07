# Plan – 2026-11-07

## TECHNIK-PROBLEM
1. **Gunpowder-Short mit 0 Views:** "4 Gunpowder Plot Questions – Can You Get 4/4? 💥" ist laut report.json (06.11. 11:47) **public, aber 0 öffentliche Views nach ~15,7 h**. Andere Shorts hatten nach dieser Zeit 50–950 Views. Zweiter 0-View-Short nach "4 Questions Almost Everyone Gets Wrong". Bitte im nächsten Analytics-Lauf prüfen: status/ytRating/regionRestriction/rejectionReason + Studio-Hinweis "eingeschränkt". Mögliche Ursache: Themenfilter (Sprengstoff/„36 Fässer Schießpulver“, 💥). **Ab sofort keine Sprengstoff-, Waffen- oder Anschlags-Themen in Shorts.** Wenn morgen immer noch < 20 Views → Besitzer informieren (Studio-Prüfung) und den Short nicht noch einmal hochladen.
2. Kein Lauf-Fehler im Log (06.11.: Uploads, Kommentare 16:06 / 21:04 mit Long-Link, Konkurrenz 25 Kanäle / 131 Gewinner). Queue 07.11. + 08.11. vollständig (je 3 Items) → **nur 09.11. neu anlegen.**
3. Analytics-Stand weiter **06.11. 11:47** (nächster Lauf ~08:30). Scoreboard-Dedupe (videoId) wirkt: "#2"-Duplikat ist weg.
4. Risiko GitHub-Actions-Minuten (≈2.100 min/Monat hochgerechnet, Limit 2.000) bleibt – bei "spending limit"/"minutes"-Fehlern Besitzer informieren.

## Zusammenfassung (Deutsch)
- **VS bleibt das stärkste Short-Format:** "Which Has More People?" jetzt **1.102 Views** (bester Short seit 01.11.); VS 873 / 555 / 1.102 → VS-Median 873 ≈ 1,8× Shorts-Median (480). 21:00 = VS jeden Tag; am 09.11. neues VS-Thema **Gewicht** mit Fangrunde „Wolke vs. Blauwal“.
- **6-Q mit Suchthema:** Geography 6/6 **969 n. 1,9 T**, Trivia 6/6 1.217. Aber **Vocabulary (E5) nur 115 n. ~20 h** (Geo hatte nach 21 h 769) → Wortschatz-Thema vorläufig Flop, Verdict 08.11. Das Thema entscheidet über die Reichweite, nicht nur das Format → 6-Q-Themen nur noch aus Geo/Trivia/Geschichte/Wissenschaft/Hauptstädte.
- **Longs weiter tot** (Geography-50 final 3, Emoji-50 1 View n. 1 T). E8 (30 Fragen, enges Thema) läuft wie geplant bis zum Verdict 12.11.; 09.11. E8 #3 **Flag Quiz** (stärkster Konkurrenz-Short-Trend: "Only 5% can name these flags" 189k bei 1,5k Abos).
- 09.11. = 37. Jahrestag Mauerfall → 6-Q "Berlin Wall Quiz" als Themen-Experiment E10 (DE = Publikum Nr. 2, History-4-Trap 1.081 Views).
- Abos 14 (unverändert seit 05.11.).

## Konkurrenz-Gewinner heute (letzte 30 Tage, competitors.md + outliers.md 06.11.)

| # | Video (Kanal, Abos) | Views | × Median | Länge | Titel-Muster | Was wir übernehmen → Slot |
|---|---|---|---|---|---|---|
| 1 | "10 Tricky IQ Riddles / Test Your Intelligence!" (Quiz World, 1.090) – 22.10. | 516.408 | 276× | 6:48 | Zahl + "Tricky" + IQ | Je Runde 1 Fangfrage in jedem Quiz (09.11. VS-Runde 2 Wolke > Blauwal); Riddles-Long im Backlog #5 |
| 2 | "Test Your IQ Level in just 8 Min (Part 2)" (Clear Think, 6.560) – 13.10. | 233.067 | 295× | 8:09 | Zeitversprechen + Serie | Länge 7–8 min = E8 bestätigt; „in just X minutes“ als Titel-Test nach E8-Verdict (12.11.) |
| 3 | "Name These F1 Tracks from Google Earth! Part 2" + Part 3 (Dopamine Quiz, 417) – 08./31.10. | 215.550 / 29.243 | 308× / 42× | 15:06 / 8:50 | enge Nische + Suchbegriff + Serie | E8 = enges Suchthema vorn im Titel → 09.11. "Flag Quiz: 30 Questions…" |
| 4 | "Only 5% can name these flags" (Question Time, 1.550) – Shorts-Ausreißer | 188.509 | 122× (Views/Abos) | 1:15 | Prozent-Ego-Hook + Flaggen | Flaggen als Thema: 09.11. Long (E8 #3) + 10.11. 6-Q "Only Geniuses Get 6/6 🧠 Flag Quiz" (Backlog #1) – Flaggen per Text-Hinweis + unsere 10 lizenzierten Flaggenfotos |
| 5 | "Which Animal Lives for Only One Day?" (GK QuizCast, 483) – Shorts-Ausreißer | 99.493 | 199× | 1:10 | Tier-Frage als Titel | Tier-Fakten mit Überraschung → VS "Which Is Heavier?" 09.11.; 1-Frage-Format selbst bleibt gestoppt (bei uns Median 378) |

Nicht übernommen: Chauncey Asks (Straßen-Interviews, Playbills/Airline-Livery = Markenrechte), comicnutz (Comic-Figuren), Clue Senpai (Anime-Zeichnungen), QuizNova "Score More Than 2 / Ages 70-95" (= unser gestopptes E1, 0/0/1 Views), "Which US President ranking…" (Politik).

## 3-Tage-Plan

Layout überall **tvshow**. Fakten vor dem Schreiben prüfen (Britannica, Smithsonian, USGS, NOAA, Stiftung Berliner Mauer / berlin.de). Gegen `queue/done/*` greppen. **07.11. + 08.11. liegen fertig in der Queue → nur 09.11. neu anlegen.**

| Datum / Slot | Format | Thema | Arbeitstitel (YouTube) | Fragen + timing | Hook / Frage 1 | Musik | cardColors | Thumbnail A/B/C + Foto | Warum | Erfolgskriterium |
|---|---|---|---|---|---|---|---|---|---|---|
| 07.11. Long 14:00 | E8 #1 (Queue) | Hauptstädte | Capital Cities Quiz: 30 Questions From Easy to Legend 🌍 | 30, 5.0/1.2 | Queue | world-trip | #0F766E/#042F2E | Queue | E8 | Median ≥10 Views n. 3 T (12.11.) |
| 07.11. Short 16:00 | 6-Q (Queue) | Hauptstädte | Only Geniuses Get 6/6 🧠 Capital Cities Quiz | 6, Queue | Queue | game-show | – | – | Exploit | ≥1.000 |
| 07.11. Short 21:00 | VS #5 (Queue) | Einwohner R2 | Which Country Has More People? 4 Rounds 90% Fail 👥 | 4, Queue | Queue | brain-pulse | – | – | Exploit VS (1.102) | ≥800 |
| 08.11. Long 14:00 | E8 #2 (Queue) | Sonnensystem | Solar System Quiz: 30 Questions From Easy to Legend 🪐 | 30, 5.0/1.2 | Queue | brain-pulse | #1E2A5A/#0B1026 | Queue | E8 | wie E8 |
| 08.11. Short 16:00 | 6-Q E9 (Queue) | Weltraum | Only Geniuses Get 6/6 🧠 Space Quiz | 6, Queue | Queue | game-show | – | – | Thema-Test | ≥800; <400 → Space raus |
| 08.11. Short 21:00 | VS #6 (Queue) | Planeten & Monde | Which Is Bigger? Planets & Moons – 90% Get #2 Wrong 🪐 | 4, Queue | Queue | world-trip | – | – | Exploit VS | ≥700 |
| **09.11. Long 14:00** | **E8 #3**: QuizLong 30 Q, 5 Runden à 6 EASY→MEDIUM→HARD→VERY HARD→LEGEND, Ziel 7–8 min | Flaggen (Text-Hinweise: Farben, Symbole, Form; Reveal mit Flaggenfoto, wo vorhanden) | **Flag Quiz: 30 Questions From Easy to Legend 🚩** (48 Z.) | 30, count 5.0 / tail 1.2, midCtaIndex 14, `fact` bei allen 30 | Hook "CAN YOU GET 25/30? 🧠"; Q1 leicht: "Which country's flag has a red maple leaf?" → Canada. Weiter z. B. Japan (roter Kreis), Brasilien („Ordem e Progresso“), Schweiz (quadratisch), Nepal (einzige nicht-rechteckige Nationalflagge – nur wenn nicht in done, sonst Mosambik = Flagge mit Gewehr ✗ (Waffe) → stattdessen Zypern = Landkarte auf der Flagge), Libanon (Zeder), Kasachstan (Adler + Sonne), Paraguay (Vorder-/Rückseite verschieden), Bhutan (Drache), LEGEND: Dänemark = älteste durchgehend benutzte Nationalflagge. Je Runde 1 Fangfrage (Konkurrenz #1). **Keine** Flaggen mit Waffen-Motiv als Antwort-Thema | world-trip | ['#7F1D1D', '#FFF7ED'] (Weinrot/Creme) | A "FLAG **QUIZ**" + `bilder/cap-flag-brazil.jpg` · B "CAN YOU GET **25/30**?" · C "**LEGEND** LEVEL"; thumbEmoji 🚩, thumbBadge "30 Q · EASY → LEGEND" | E8 #3 + Konkurrenz #3/#4 (Flaggen-Ausreißer 189k), Autocomplete "country guess by flag" / "country guessing game flag" | E8 gesamt: Median ≥10 öffentl. Views n. 3 T UND Ø angesehen ≥40 % |
| **09.11. Short 16:00** | 6-Q (Exploit Format + Titel; **Thema = Experiment E10 Jahrestag**) ≤ 50 s | Berliner Mauer (37. Jahrestag Mauerfall) – nur Fakten, keine Wertung, keine Politiker-Fotos | **Only Geniuses Get 6/6 🧠 Berlin Wall Quiz** (+ #shorts, 39 Z.) | 6, count 2.5 / tail 0.8, leicht → schwer, schwerste an Platz 4, Antworten ≤ 6 Wörter, 4 Optionen | Q1 sehr leicht: "In which city did a famous wall fall in 1989?" → Berlin (Paris/Berlin/Rome/Vienna). Dann: Jahr des Mauerfalls (1989), Baujahr (1961), **#4 schwer: "How many years did the Berlin Wall stand?" → 28** (Fangoptionen 18/28/38/45), bekanntester Grenzübergang (Checkpoint Charlie), Wiedervereinigung (3 October 1990). Loop-Satz "Got all six? Go again!" | game-show | – | – (Shorts: Frame) | 6-Q = stärkstes Format nach VS (Median ~1.000 bei Trivia/Geo); History-4-Trap 1.081 = Geschichte funktioniert; Jahrestag 09.11. = Suchspitze | ≥800 Views n. 3 T; <400 → Jahrestags-Themen nur noch als Zusatz, nicht im 16:00-Slot |
| **09.11. Short 21:00** | VS #7 (Exploit) | Gewicht | **Which Is Heavier? 4 Rounds 90% Get #2 Wrong 🐘** (47 Z.) | 4, count 3.0 / tail 1.2, correctLabel "HEAVIER!", valueLabels "≈ … kg" bzw. "≈ … tonnes" | R1 leicht: African elephant (Bulle ≈6.000 kg) vs Hippo (≈1.500–1.800 kg); **R2 Haken: average cumulus cloud ≈500 t (USGS: ~1,1 Mio. lb) vs Blue whale ≈150 t** → die Wolke ist schwerer; R3: Giraffe (≈1.200 kg Bulle) vs Moose (≈600 kg); R4: Polar bear (Männchen ≈450 kg) vs Grizzly (≈300 kg). Werte vor dem Rendern gegen Smithsonian/NOAA/USGS prüfen; bei Spannen den Mittelwert ausgewachsener Männchen nehmen und in valueLabels „≈“ zeigen | world-trip | – | – (icons statt Fotos) | VS 3/3 Treffer, Median 873; Gewicht = neues VS-Thema, Fangrunde nach Konkurrenz #1 | ≥700 Views n. 3 T |

Bandit 07.–09.11.: 5 Exploit (VS ×3, 6-Q Capitals, 6-Q Format) / 4 Experiment (E8 ×3, E9/E10 nur als Themenvariable) ≈ 60/40 – akzeptiert, weil die Longs ohnehin nicht ausgespielt werden und alle Shorts im Gewinner-Format laufen.

## Ideen-Backlog (nach erwartetem Potenzial)
1. **6-Q "Only Geniuses Get 6/6 🧠 Flag Quiz" (10.11. 16:00)** – Konkurrenz "Only 5% can name these flags" 189k (122×); Autocomplete "country guess by flag"; verlinkt aufs Flag-Long 09.11.
2. **VS "Which Is Older?" (Bauwerke/Erfindungen, 10.11. 21:00)** – Which-Came-First R1 1.234 + VS-Format (Median 873); Haken: Oxford University älter als die Azteken-Hauptstadt Tenochtitlan.
3. **Veterans/Remembrance Day 11.11.: 6-Q "Only Geniuses Get 6/6 🧠 World War 1 Quiz" (16:00)** – US+UK ≈ 69 % Publikum; nur Fakten (Waffenstillstand 11 Uhr, 1918), keine Kriegs-B-Roll.
4. **GTA-VI-Woche (Release 19.11.2026 laut Take-Two bestätigt): 6-Q "Only Real Fans Get 6/6 🎮 GTA Quiz" 18.11. + E8-Long "GTA Quiz: 30 Questions" 17.11.** – riesige Suchspitze; nur Textfakten (Vice City = Miami-Vorbild, GTA V 2013), keine Spielbilder/Logos.
5. **"12 Tricky Riddles – Can You Solve 4?" (Long ~7 min)** – Quiz World 516k (276×), Quiz Guy 82k (71×); nach E8-Verdict, nur wenn Renderer Rätseltexte sauber zeigt.
6. **VS "Which Is Hotter / Colder?" (Orte & Planeten)** – VS-Variante, Fangrunde Venus vs. Merkur schon benutzt → Antarktis vs. Mars-Äquator am Tag.
7. **Emoji-Long "Guess the Movie by Emoji – 30 Rounds 🎬" (E8, 10.11.)** – einziges Long mit Reichweite (Emoji-15: 141), Konkurrenz Quiz Bunny / Again Quiz Emoji 357k (111×); nur Filmtitel als Text.
8. **"Human Body Quiz: 30 Questions" (E8) + VS "Which Organ Is Heavier?"** – Autocomplete "human body quiz"; Math Quiz "human body…" vorhanden.
9. **Thanksgiving 26.11.: 6-Q "Only Geniuses Get 6/6 🦃 Thanksgiving Quiz" + E8-Long** – saisonal US; Halloween-35 war bestes Fragen-Long (185).
10. **ATP Finals Turin (ab 08.11.) / Tennis 6-Q** – Ereignis der Woche, aber Sport-Longs bei uns 7–8 Views → nur als Short-Thema, niedrige Priorität.

## Für den Produktions-Agenten (gilt heute, überschreibt ältere Defaults)
- **3 Items für 09.11.** anlegen: `2026-11-09-flag-quiz-30-1.json` (Long, publishAt "14:00", E8-Format wie Capitals-30), `2026-11-09-six-q-genius-berlin-wall.json` (publishAt "16:00"), `2026-11-09-vs-heavier-1.json` (publishAt "21:00").
- Flaggen-Fotos nur aus image-credits.json (`bilder/cap-flag-*.jpg`, 10 Stück); übrige Flaggen per cardText-Hinweis (keine Fremdbilder). Gegen done greppen (Nepal-Flagge war in Quick-Fire-Geo → nicht als Frage wiederholen).
- **Keine Sprengstoff-/Waffen-/Anschlags-Themen und kein 💥 mehr in Shorts** (Technik 1). Keine Politik, kein Halloween, keine E1-Longs.
- Shorts-Kommentar 09.11. verlinkt aufs Flag-Long (sobald öffentlich).
- Im Analytics-Lauf: Gunpowder-Status prüfen + loggen; stayed/Ø angesehen der Videos ab 04.11. für E6- und Lautheits-Verdict (08.11.) notieren.
