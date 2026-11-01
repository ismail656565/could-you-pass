# Plan – 2026-11-01

## TECHNIK-PROBLEM
1. **Shorts bekommen ihren Pin-Kommentar erst am nächsten Tag:** Die Kommentar-Crons in `.github/workflows/autopilot.yml` laufen nur 08:10/09:10/12:10/13:10 UTC (= 09:10–14:10 Berlin, Winterzeit). Shorts gehen um 16:00 und 21:00 Berlin (15:00/20:00 UTC) online → log 31.10.: `one-q-hours-week` / `vs-countries-bigger-1` "noch nicht öffentlich" beim letzten Lauf 13:49 UTC, danach kein Lauf mehr. **Fix (Produktions-Agent):** zwei Kommentar-Crons ergänzen: `'20 15 * * *'` und `'20 20 * * *'` (gleicher Job/Modus wie die bestehenden Kommentar-Crons). Der erste Kommentar in der ersten Stunde ist für Shorts am wichtigsten.
2. **E1 #1 war zu kurz:** "Can You Score 4/12?" hat **4:38 min** (278 s, 12 Q, count 9.0/tail 2.0) statt ~7 min. ≈ 23 s pro Frage. E1 #2 (US Presidents, 15 Q, count 8.0/tail 1.8) käme nur auf ~5:30. **Heute im Queue-Item `2026-11-02-us-presidents-5-15.json` timing auf `{"count":10.0,"tail":2.6,"tempo":0.95}` setzen** und jede Erklärzeile auf 1–2 Sätze (mit Zusatzfakt) verlängern → Ziel 6:45–7:30. Titel bleibt ("7-Minute Test" muss stimmen; wenn Render < 6:00 → Titel auf "…Can You Score 5/15? 🏛️ Hard Quiz" ändern).
3. **Konkurrenzliste wieder mit Off-Topic-Kanälen aufgefüllt** (Blocked-Fix greift, aber der Ausreißer-Scan füllt neue Fremd-Nischen nach). Heute vom Research-Agenten entfernt + in `blocked`: The Brownish Bros ("Girls Maths Test"-Memes), Master m ("Best comebacks"), Next Line (Sitcom-Zitate). Liste jetzt 22 Kanäle. Kein Code-Fix nötig.
4. **Analytics-Stand 31.10. 11:29** (8 Abos). Videos ab 30.10. haben noch keine 3 Tage → Verdicts Sloth/Food/Animal-50/E1/VS ab 03.–04.11.

## Zusammenfassung (Deutsch)
- **Shorts-Reichweite fällt:** Ersatz-1-Frage 28.10. 603 → 29.10. 292/176; Sloth 99 und Food-Trap 66 nach ~1 Tag (noch kein Verdict). Spitze bleiben **6+-Fragen-Shorts (Median 1.334, stayed 56 %)** und reine Themen-Sets "4 History Questions" (1.081). → 16:00-Slot am 03.11. wird ein 6-Fragen-Short statt 1-Frage.
- **Long:** Median weiter ~10 Views (Animal-50: 2, GK-50 29.10.: 2). E1 #1 (4/12) erst seit gestern 14:00 öffentlich, aber nur 4:38 lang → Technik-Problem 2. Kein Strategiewechsel (Testwoche bis 05.11.).
- **Konkurrenz:** Dopamine Quiz (372 Abos!) holt mit **F1-Strecken-Quiz 262k + 196k** – Sport-Erkennungs-Quiz zu aktuellen Events tragen; GK STUDIO PRO setzt die Hürden-Serie fort ("Score 3+ of 10" 35k, "10-Question IQ Quiz" 26k).
- **Großes Event:** **GTA VI erscheint 19.11.2026** (Take-Two bestätigt) → größte Gaming-Suchwelle des Jahres; wir planen ab 15.11. ein "GTA Quiz" (nur Fakten über die Serie, keine Screenshots/Logos). Nächste Woche: 03.11. US-Wahltag, 05.11. Bonfire Night, 11.11. Veterans/Remembrance Day.

## Konkurrenz-Gewinner heute

| # | Video (Kanal, Abos) | Views | × Median | Länge | Titel-Muster | Was wir übernehmen → Slot |
|---|---|---|---|---|---|---|
| 1 | "Test Your iQ in just 7 minutes" (Clear Think, 5,4k) | 1,42 Mio | 2209× | 6:48 | Zeit-Versprechen + IQ | 7-Min-Länge → E1 #2 02.11. (timing-Fix, s. Technik 2) |
| 2 | "Are You Well Educated? … Score At Least 4/10!" (GK STUDIO PRO, 1,8k) | 990k | 1185× | 7:15 | Identität + niedrige Hürde | Hürde "5/15" in E1 #2; E1 #3 Backlog 2 |
| 3 | "Guess the F1 Track No Longer in 2027 Calendar!" (Dopamine Quiz, 372) | 262k | 438× | 9:00 | "Guess the X" + Aktualitäts-Haken | Event-Aktualität als Titelhaken → Backlog 3 (Football/F1 nur mit eigenen Fakten, keine Google-Earth-Bilder) |
| 4 | "trivia challenge quiz 😌" (Think Nova, 2,5k) | 474k | 719× | 1:02 | generischer Suchbegriff, viele leichte Fragen, ~1 min | 6-Fragen-Short 01.11. (Queue) + **03.11. 16:00** |
| 5 | "Name the Movie By The Car … All 30 Movies" (Quibby, 210) | 348k | 1070× | 6:55 | "Name the X by the Y" + Zahl | Detail-Errate-Format → Backlog 4 (Flaggen-Fotos vorhanden) |

## 3-Tage-Plan

Layout überall **tvshow**. Zeiten Berlin. Fakten vor dem Schreiben prüfen (Britannica/NASA/CIA Factbook/Guinness). broll-Regeln (learnings 30.10.) gelten. 01.11. und 02.11. liegen schon in der Queue → nur 03.11. neu anlegen.

| Datum / Slot | Format | Thema | Arbeitstitel (YouTube) | Fragen + timing | Hook / Frage 1 | Musik | cardColors | Thumbnail A/B/C + Foto | Warum | Erfolgskriterium |
|---|---|---|---|---|---|---|---|---|---|---|
| **01.11. Long 14:00** | QuizLong 50 (Queue) | True/False | True or False Quiz: 50 Facts From Easy to Legend ✅❌ | 50, 5.0/1.2 | in Queue | game-show | in Queue | in Queue | Keyword Nr. 1 | ≥50 Views n. 3 T |
| **01.11. Short 16:00** | 6-Fragen (Queue) | GK | Only Geniuses Get 6/6 🧠 Trivia Challenge Quiz | 6 | in Queue | game-show | – | – | Exploit 1.334 | ≥1.000 Views |
| **01.11. Short 21:00** | E3 True/False #1 (Queue) | Mythen | True or False? 4 Facts 90% Get Wrong ✅❌ | 4 | in Queue | brain-pulse | – | – | Experiment | ≥294 Views + stayed ≥50 % |
| **02.11. Long 14:00** | E1 #2 (Queue) | US-Präsidenten (unpolitisch) | US Presidents Quiz: Can You Score 5/15? 🏛️ 7-Minute Test | 15, **timing neu 10.0/2.6/0.95** | in Queue | brain-pulse | navy | in Queue | Konkurrenz #1/#2 + Wahltag 03.11. | ≥30 Views n. 3 T ODER CTR ≥4 % ODER Ø angesehen ≥45 % |
| **02.11. Short 16:00** | 1-Frage leicht #2 (Queue) | Planeten | Can You Answer: Which Planet Is Closest to the Sun? ☀️🤯 | 1 | in Queue | game-show | – | – | Exploit leichte Frage | ≥700 Views |
| **02.11. Short 21:00** | E2 VS #2 (Queue) | Tier-Tempo | Which Is Faster? 4 Races 90% Get Wrong 🐆 | 4 | in Queue | world-trip | – | – | E2 | 3 VS ≥294 Views |
| **03.11. Long 14:00** | QuizLong **50** (Standard) | Geografie | **Geography Quiz: 50 Questions From Easy to Legend 🌍** (55 Z.) | 50, 5 Runden à 10 (EASY→MEDIUM→HARD→VERY HARD→LEGEND), timing 5.0/1.2/1.0 | 1 Satz: "Fifty geography questions, easy to legend – keep score! First one:" Q1 leicht "Which is the largest ocean on Earth?" **nur wenn nicht schon benutzt** (sonst "On which continent is Egypt?"); Haken-Fragen einbauen (z. B. Kanada hat die längste Küste; Russland grenzt an 14 Länder – prüfen); broll nur Q1–2 je Runde, nie antwortverratend | world-trip | petrol / gelb | A "GEOGRAPHY QUIZ" + Flaggen-/Globus-Foto aus image-credits (keine Lösung) · B "40/50?" · C "LEGEND LEVEL"; thumbBadge "50 Q" | Exploit: eigene Geo-Shorts 714–1.325 Views; Autocomplete "geography quiz hard" (2,4); Suchbegriff vorn | ≥50 Views n. 3 T (Long-Median ≈10) |
| **03.11. Short 16:00** | **6-Fragen-Short** (Exploit, Median 1.334) | "Which Came First?" #2 | **Which Came First? 6 Questions 90% Get Wrong 🤔** – Titel existiert schon → **"Which Came First? Round 2 – 6 Questions 🤯"** | 6, count 2.5 / tail 0.8; Jahr nach jedem Reveal einblenden | Q1 leicht & überraschend: "Which came first: Oxford University or the Aztec Empire?" (Oxford ~1096 vs. Tenochtitlan 1325 – prüfen); weitere Paare: Nintendo vs. Titanic-Untergang (1889 vs. 1912), Fax vs. Telefon (1843 vs. 1876), Haie vs. Bäume (~450 vs. ~385 Mio J.), Cleopatra näher an Mondlandung als an Pyramidenbau (als Paar umformen), Kleopatra vs. Pyramiden; nur Paare mit klaren Jahreszahlen; Loop "Think you got all six? Go again!" | brain-pulse | dunkelblau / orange-gelb (kein Schwarz-Orange) | – | eigener 1.234-Views-Sieger (stayed 55 %) + Konkurrenz #4 | ≥1.000 Views n. 3 T |
| **03.11. Short 21:00** | 4-Fragen-Trap Geschichte – **E4 Titel-Test** (einzige Variable: Titel) | Geschichte (reines Themen-Set) | **4 History Questions – The Last One Will Humble You 😏** (52 Z.) | 4, Standard 2.5/1.0; schwerste Frage an Platz 4 | Q1 sofort: "How long did the shortest war in history last?" – NUR falls Sansibar nicht schon benutzt (wurde 25.10. benutzt!) → stattdessen "Which is older: the Great Wall's oldest parts or the Colosseum?"; Q4 = fieser, aber eindeutig belegter Haken | brain-pulse | weinrot / beige | – | Vergleich mit "4 History Questions Almost Everyone Gets Wrong" (1.081); Muster last30days "The last one will HUMBLE you" 279k/7,5k Kommentare | ≥800 Views n. 3 T UND mehr Kommentare als History-Trap 26.10. |

Bandit: 03.11. = 2 Exploit + 1 Experiment (E4). Laufende Experimente: E1 (7-Min-Long), E2 (VS), E3 (True/False-Short), E4 (Titel "Humble").

## Ideen-Backlog (nach erwartetem Potenzial)
1. **GTA Quiz (Long, ab 15.11., Release 19.11.)** – "GTA Quiz: How Well Do You Know Grand Theft Auto? 🎮" – größte Gaming-Suchwelle 2026; nur eigene Fakten über Serie/Release-Jahre/Städte, keine Spielbilder/Logos (Rechte) → cardText + neutrale Stadt-broll (Miami-Skyline).
2. **E1 #3 "General Knowledge Quiz: Can You Score 5/15? 7-Minute Test"** – wenn E1 #1 oder #2 Kriterium erfüllt; Konkurrenz #1/#2 (1,4 Mio / 990k).
3. **"Guess the Football Club by Its Nickname" (Long ~7 min, 30 Clubs)** – Dopamine Quiz F1/Stadien 15k–262k bei 372 Abos; reiner Text, keine Logos.
4. **Guess the Country by Flag – 30 Flags (~7 min)** – Trends "guess the country" 30, Quibby-Mechanik; Flaggen in image-credits.
5. **Bonfire Night 05.11. Short: "4 British History Questions Almost Everyone Gets Wrong 💥"** – UK-Datum, History-Set-Muster (1.081).
6. **Guess the Movie by Emoji (Long, 20 Filme, ~7 min)** – Quiz Bunny 541k; unser Emoji-Long beste Bindung (73 %).
7. **8-Fragen Geography Short #2 "8 Geography Questions 90% Get Wrong 🌍"** – eigener 1.325-Sieger, seit 17.10. nicht wiederholt.
8. **Veterans Day 11.11.: "US History Quiz: Can You Score 4/12?"** – Event + E1-Mechanik.
9. **Tricky Quiz – Level 1/2/3 (Short-Serie)** – last30days 1,66 Mio; Serien-Experiment, sobald E3/E4 entschieden.
10. **Thanksgiving 26.11.: "Thanksgiving Trivia: 50 Questions …"** – saisonaler Suchbegriff; Halloween-35 war unser bestes Long (182) → saisonal trägt.

## Für den Produktions-Agenten (gilt heute, überschreibt ältere Defaults)
- Zuerst Technik 1 (2 Kommentar-Crons) und Technik 2 (timing im Presidents-Item) erledigen.
- Dann **3 Items für 03.11.** anlegen: `2026-11-03-geography-quiz-50-1.json`, `2026-11-03-which-first-6-2.json`, `2026-11-03-trap-4-history-humble.json`.
- **Ab sofort für E1 (7-Min-Format):** Zielrechnung ≈ 27 s pro Frage → 15 Fragen mit count 10.0 / tail 2.6 + Erklärsatz; nie unter 6:00 rendern, wenn der Titel "7-Minute" sagt.
- Vor jedem Item gegen queue/done + stories greppen (Fragen + Titel); "Which Came First? 6 Questions 90% Get Wrong" existiert schon → Titel aus der Tabelle nehmen. Sansibar-Krieg (25.10.) und "largest ocean" nicht wiederverwenden.
- 03.11. ist US-Wahltag: im Geography-Long keine Politik-/Wahlfragen.
- Kein Halloween-/Spooky-Bezug, kein Schwarz-Orange.
