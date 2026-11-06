# Plan – 2026-11-06

## TECHNIK-PROBLEM
1. Keine Fehler: Läufe 05.11. alle grün, Soll 05.11. erfüllt (emoji-word-50-1, six-q-vocabulary-1, trap-4-gunpowder; Kommentare 13:13 / 16:23 / 21:10 mit Long-Link). competitors.md 05.11. ok (25 Kanäle, 134 Gewinner). Queue 06.11. + 07.11. vollständig (je 3 Items) → **nur 08.11. neu anlegen.**
2. Analytics-Stand weiter **05.11. 11:52** (nächster Lauf ~08:30) – Zahlen unten = dieser Stand; Videos vom 05.11. waren da noch privat (keine Werte).
3. **Kleiner Scoreboard-Fehler:** In "Top 8 Shorts" steht "Can You Answer This Quiz Question? 🤯 #2" (1.160 Views) **doppelt** (einmal brain-pulse, einmal game-show) → ein Video wird aus 2 done-Dateien mit derselben videoId gezählt (verfälscht Gruppe "Ersatz-Generator" und Musik-Tabelle). Im Scoreboard-Skript nach videoId deduplizieren (neueste done-Datei gewinnt).
4. Risiko GitHub-Actions-Minuten (≈2.100 min/Monat hochgerechnet, Limit 2.000) bleibt – bei "spending limit"/"minutes"-Fehlern Besitzer informieren.

## Zusammenfassung (Deutsch)
- **VS bestätigt sich:** VS #3 "Which Has More People?" jetzt **1.007 Views** (bester Short seit 01.11.), VS #1 873, VS #2 554 → VS-Median 873 = **~2× Shorts-Median (480)**. 21:00 bleibt täglich VS; 08.11. neues VS-Thema **Planeten & Monde** ("Which Is Bigger?" war Titel-Gewinner 873).
- **6-Q mit Suchthema trägt:** "Quick Fire Geography 6/6" **769 n. ~21 h** (auf Kurs ≥1.000); "Round 2"-Sequel blieb bei **140** (final ≈) → Sequel-Titel endgültig tot, Titelformel "Only Geniuses Get 6/6 🧠 <Thema>" ab 07.11.
- **Longs:** E1 (7-Min-Test, niedrige Hürde) #1 0 / #2 0 / #3 "Well Educated" **1 View n. 23 h** → **E1 gestoppt** (nichts mehr davon einplanen). Heute E7 (Long 19:00), morgen E8 #1 Capitals-30. 08.11. **E8 #2 "Solar System Quiz"** als "Weltraum-Tag" mit VS-Planeten + 6-Q-Space gekoppelt.
- Abos 14 (+7 in 7 Tagen). E6 (Editorial-Look) + Lautheits-Fix: stayed-Werte der Videos ab 04.11. fehlen noch (2–3 Tage Verzug) → Verdict 08.11.

## Konkurrenz-Gewinner heute (letzte 30 Tage, competitors.md 05.11.)

| # | Video (Kanal, Abos) | Views | × Median | Länge | Titel-Muster | Was wir übernehmen → Slot |
|---|---|---|---|---|---|---|
| 1 | "10 Tricky IQ Riddles / Test Your Intelligence!" (Quiz World, 1.080) – 22.10. | 510.053 (+3 %/Tag) | 274× | 6:48 | Zahl + "Tricky" + IQ-Versprechen | Pro Runde 1 Fangfrage im E8-Long (08.11.: "Saturn würde schwimmen", "Ganymed > Merkur"); Riddles-Long im Backlog (#4) |
| 2 | "Can You Score More Than 2? Test For Ages 70-95!" (QuizNova, 1.370) – 10.10. | 421.694 | 194× | 6:42 | extrem niedrige Score-Hürde + Altersgruppe | Bei uns als E1 getestet → 0/0/1 Views → **nicht mehr übernehmen** (Kanal hat kein Long-/Senioren-Publikum) |
| 3 | "Test Your IQ Level in just 8 Min (Part 2)" (Clear Think, 6.440) – 13.10. | 229.359 | 312× | 8:09 | Zeitversprechen + Serie | Länge 7–8 min für E8 bestätigt; Zeitangabe im Titel = Titel-Experiment nach E8-Verdict (12.11.) |
| 4 | "English Quizz IQ test time #learnanewwordtoday" (Math Quiz, 1.420) – 17.10. | 152.915 | 41× | 1:11 | Wortschatz-Short, Minimal-Titel | E5 Vocabulary-6-Q lief 05.11. (Verdict 08.11.) – bei ≥1.000 Wortschatz in 6-Q-Rotation |
| 5 | "Can You Guess 20 F1 Tracks From Above? – F1 Track Quiz Part 3" (Dopamine Quiz, 415) – 31.10. | 28.882 in 6 T | 41× | 8:50 | **enge Nische + Serie**, Suchbegriff "F1 Track Quiz" | Enge Suchthemen statt Oberbegriff → E8 #2 "Solar System Quiz" (08.11.); F1-Strecken selbst nicht (Google-Earth-Bilder) |

Ebenfalls stark: Quiz Guy "You're Not Smart Enough to Solve These 12 Puzzles!" 80k (70×, 8:15) → Backlog #4. Nicht übernommen: Chauncey Asks (Straßen-Interviews, Logos/Playbills = Markenrechte), FootyMind/QuizKoala (Spielerfotos), Quiz Phoenix (Disney-Songs).

## 3-Tage-Plan

Layout überall **tvshow**. Fakten vor dem Schreiben prüfen (NASA Planetary Fact Sheet, NASA Science "Solar System", Britannica). Gegen `queue/done/*` greppen (bereits benutzt: Sonnenlicht 8 min, Venus-Rotation 243 Tage, Merkur nächster/Venus heißester Planet, Saturn-Ringe, Mars). **06.11. + 07.11. liegen in der Queue → nur 08.11. neu anlegen.**

| Datum / Slot | Format | Thema | Arbeitstitel (YouTube) | Fragen + timing | Hook / Frage 1 | Musik | cardColors | Thumbnail A/B/C + Foto | Warum | Erfolgskriterium |
|---|---|---|---|---|---|---|---|---|---|---|
| 06.11. Long **19:00** | E7 Timing (Queue) | Geschichte | History Quiz: 50 Questions From Easy to Legend 🏛️ | 50, 5.0/1.2 | Queue | world-trip | weinrot/creme | Queue | E7 | ≥10 öffentliche Views n. 3 T |
| 06.11. Short 16:00 | 6-Q (Queue) | Wissenschaft | Quick Fire Science Quiz – Can You Get 6/6? 🔬 | 6, Queue | Queue | game-show | – | – | Exploit 6-Q | ≥1.000 |
| 06.11. Short 21:00 | VS #4 (Queue) | Bauwerkshöhen | Which Is Taller? 4 Rounds 90% Get Wrong 🏙️ | 4, Queue | Queue | world-trip | – | – | Exploit VS | ≥500 |
| 07.11. Long 14:00 | E8 #1 (Queue) | Hauptstädte | Capital Cities Quiz: 30 Questions From Easy to Legend 🌍 | 30, 5.0/1.2 | Queue | world-trip | #0F766E/#042F2E | Queue (Kanada-Flagge) | E8 | Median ≥10 Views n. 3 T (Verdict 12.11.) |
| 07.11. Short 16:00 | 6-Q (Queue) | Hauptstädte | Only Geniuses Get 6/6 🧠 Capital Cities Quiz | 6, Queue | Queue | game-show | – | – | Exploit Titel | ≥1.000 |
| 07.11. Short 21:00 | VS #5 (Queue) | Einwohner R2 | Which Country Has More People? 4 Rounds 90% Fail 👥 | 4, Queue | Queue | brain-pulse | – | – | Exploit VS | ≥800 |
| **08.11. Long 14:00** | **E8 #2**: QuizLong 30 Q, 5 Runden à 6 EASY→LEGEND, Ziel 7–8 min (Länge vor Render schätzen, Schätzer +5 %) | Sonnensystem (gekoppelt an VS + 6-Q des Tages = "Weltraum-Tag") | **Solar System Quiz: 30 Questions From Easy to Legend 🪐** (55 Z.) | 30, count 5.0 / tail 1.2, midCtaIndex 14, `fact` bei allen 30 | Hook "CAN YOU GET 25/30? 🧠"; Q1 leicht: "Which planet is called the Red Planet?" → Mars. Je Runde 1 Fangfrage (Konkurrenz #1): Saturn ist weniger dicht als Wasser; Uranus rotiert "auf der Seite" (~98°); Neptun per Rechnung gefunden (1846); Pluto 2006 Zwergplanet; Olympus Mons = höchster Vulkan; Finale LEGEND: größter Mond = Ganymed (Jupiter). **Nicht** Venus-Tag/heißester Planet/Sonnenlicht (benutzt) und **nicht** die VS-/6-Q-Fakten desselben Tages | brain-pulse | ['#1E2A5A', '#0B1026'] (Nachtblau) | A "SOLAR SYSTEM **QUIZ**" + `bilder/q2-sun.jpg` · B "CAN YOU GET **25/30**?" · C "**LEGEND** LEVEL"; thumbEmoji 🪐, thumbBadge "30 Q · EASY → LEGEND" | Experiment E8 (Konkurrenz #5 enge Nische; Studio: Longs bekommen nur "Vorgeschlagene" → Kopplung an Shorts) | E8 gesamt: Median ≥10 öffentl. Views n. 3 T UND Ø angesehen ≥40 % |
| **08.11. Short 16:00** | 6-Q (Exploit Format + Titel; **Thema = Experiment E9**) ≤ 50 s | Weltraum | **Only Geniuses Get 6/6 🧠 Space Quiz** (+ #shorts, 35 Z.) | 6, count 2.5 / tail 0.8, leicht → schwer, schwerste an Platz 4, Antworten ≤ 6 Wörter | Q1 sehr leicht: "In which year did humans first walk on the Moon?" → 1969 (Optionen 1959/1969/1979/1989); dann z. B. Anzahl Planeten (8), Planet mit den meisten bekannten Monden (Saturn – vorher NASA-Stand prüfen!), #4 schwer: "Which planet has the longest day?" → **nicht** Venus (benutzt) → stattdessen "What is the closest star to Earth?" → The Sun (Fangfrage), Erdmond-Entfernung ≈384.000 km, Ausklang "Who was the first person in space?" → Yuri Gagarin **nur wenn nicht in done** (sonst Valentina Tereshkova = erste Frau); Loop-Satz "Got all six? Go again!" | game-show | – | – (Shorts: Frame) | 6-Q = 2. stärkstes Format (Median 1.224); Space-Thema nur 1× im schwachen Ego-Hook (204) → Thema einzeln testen | ≥800 Views n. 3 T; <400 → Space aus 6-Q-Rotation |
| **08.11. Short 21:00** | VS #6 (Exploit) | Planeten & Monde Durchmesser | **Which Is Bigger? Planets & Moons – 90% Get #2 Wrong 🪐** (52 Z.) | 4, count 3.0 / tail 1.2, correctLabel "BIGGER!", valueLabels "≈ … km wide (NASA)" | R1 leicht: Jupiter ≈139.820 km vs Saturn ≈116.460 km; R2 (Haken): **Ganymed ≈5.268 km vs Merkur ≈4.879 km** → der Mond ist größer; R3: Erde ≈12.742 km vs Venus ≈12.104 km (knapp, 5 %); R4: Erdmond ≈3.474 km vs Pluto ≈2.377 km. Alle Werte gegen NASA Fact Sheet (mittlerer Durchmesser) prüfen; Uranus/Neptun nicht (3 % zu knapp) | world-trip | – | – | VS 3/3 Treffer, Titel "Which Is Bigger?" 873 (Median VS 873) | ≥700 Views n. 3 T |

Bandit 06.–08.11.: 6 Exploit / 3 Experiment (E7, E8 ×2) + E9 nur als Themenvariable im Exploit-Format ≈ 67/33.

## Ideen-Backlog (nach erwartetem Potenzial)
1. **VS "Which Is Heavier?" (Tiere, 09./10.11. 21:00)** – VS 3/3, Gewicht neues VS-Thema; Werte Smithsonian/NOAA (Blauwal, Elefant, Nilpferd, Giraffe).
2. **Veterans/Remembrance Day 11.11.: "Only Geniuses Get 6/6 🧠 World War 1 Quiz" (Short 16:00) + E8-Long "World War 1 Quiz: 30 Questions From Easy to Legend"** – US+UK = 69 % Publikum (US 12.376, GB 630 Views); nur Fakten, keine Kriegs-B-Roll.
3. **Fall der Berliner Mauer 09.11.: "Only Geniuses Get 6/6 🧠 Cold War Quiz" (Short 16:00)** – Jahrestag, DE = Nr. 2 Publikum (2.492 Views); Fakten ohne Wertung.
4. **"12 Tricky Riddles – Can You Solve 4?" (Long ~7 min)** – Quiz World 510k (274×), Quiz Guy 80k (70×), Puzzle Code 66k; nach E8-Verdict, nur wenn Renderer Rätseltexte sauber zeigt.
5. **GTA Quiz (E8-Long 18./19.11.) + 6-Q "Only Real Fans Get 6/6 🎮 GTA Quiz"** – GTA VI laut Take-Two weiter 19.11.2026; nur Fakten, keine Spielbilder/Logos.
6. **VS "Which Is Older?" (Erfindungen/Bauwerke)** – Which-Came-First R1 1.234 + VS-Format kombiniert.
7. **Emoji-Long 2×/Woche (nächstes 10.11.): "Guess the Movie by Emoji – 30 Rounds 🎬"** – einziges Long mit Reichweite (Emoji-15: 141, stayed 73 %); Quiz Bunny Movie-Emoji 672k (109×); nur Filmtitel als Text, keine Poster.
8. **"Human Body Quiz: 30 Questions" (E8) + VS "Which Organ Is Bigger/Heavier?"** – Autocomplete "can you pass this human body quiz"; enges Thema.
9. **"World Flags Quiz: 30 Questions" (E8)** – Autocomplete "country guess by flag"/"geography quiz flags", 10 Flaggenbilder vorhanden (cap-flag-*).
10. **Thanksgiving 26.11.: "Thanksgiving Trivia: 30 Questions 🦃" (E8)** – saisonal US; Halloween-35 war bestes Fragen-Long (185).

## Für den Produktions-Agenten (gilt heute, überschreibt ältere Defaults)
- **3 Items für 08.11.** anlegen: `2026-11-08-solar-system-quiz-30-1.json` (Long, publishAt "14:00", E8-Format wie Capitals-30), `2026-11-08-six-q-genius-space.json` (publishAt "16:00"), `2026-11-08-vs-planets-bigger-1.json` (publishAt "21:00").
- Weltraum-Tag: Long, 6-Q und VS **ohne gleiche Fakten** (Ganymed nur im VS → im Long dann Finale ersetzen, z. B. "Which planet has the most volcanoes?" → Venus oder "How long is a year on Neptune?" ≈165 Erdjahre). Shorts-Kommentar verlinkt aufs Solar-System-Long (sobald öffentlich).
- Fotos nur aus image-credits.json (`bilder/q2-sun.jpg`, `bilder/q2-venus.jpg`); sonst cardText / B-Roll (KI- und Politikfilter aktiv). VS mit icons statt Fotos.
- Scoreboard: nach videoId deduplizieren (Technik 3).
- **Keine E1-Longs (7-Min-Test / Score-Hürde) mehr** – gestoppt. Kein Halloween, keine Politik.
- Im Analytics-Lauf: stayed/Ø angesehen der Videos ab 04.11. + `qa`-LUFS in done/*.json notieren (E6- und Lautheits-Verdict 08.11.).
