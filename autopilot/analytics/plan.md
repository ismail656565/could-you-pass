# Plan – 2026-10-31

## TECHNIK-PROBLEM
1. **Konkurrenz-Bereinigung wurde von der Action rückgängig gemacht:** `competitors()` hat gestern die 5 entfernten Off-Topic-Kanäle (Routed, GK Prashnix, Quiz Baazi, Shailesh Rajput, ABCInfoTales) aus dem Ausreißer-Scan wieder aufgenommen (log 30.10.: "25 Kanäle"). **Heute vom Research-Agenten behoben:** neue Liste `blocked` (Kanal-IDs) in competitors.json, `autopilot.py competitors()` überspringt diese IDs beim Laden und beim Nachfüllen (py_compile ok). Produktions-Agent: nur prüfen, dass der nächste Lauf "Konkurrenz: 20 Kanäle" loggt.
2. **Scoreboard/report.json noch vom 30.10. 11:32** – Videos ab 28.10. ohne Views im Report (Analytics-Verzug). Kein Fehler, aber Verdicts für Sloth/Food/Animal-50 erst ab 02.11. möglich.
3. **Queue:** 31.10. (3 Items) und 01.11. (3 Items) vollständig. **Fehlt: 02.11. komplett** → heute anlegen (Tabelle unten).
4. B-Roll: Wikimedia-429 am 30.10. 20:18 bei 3 Clips – Pause/Wiederholung ist eingebaut; falls in den Logs heute wieder >2 Clips pro Video fehlen, Abstand zwischen Downloads erhöhen.

## Zusammenfassung (Deutsch)
- **Keine neuen Messwerte seit gestern** (Report 30.10. 11:32). Shorts-Stand: 6+-Fragen Median **1.333** (stayed 56 %), leichte 1-Frage-Shorts **1.137** (n=3), 4-Fragen-Trap 294 (n=6), tvshow **968** vs. neon 338, game-show **1.084** vs. brain-pulse 338. Honig-1-Frage jetzt 855, "4 History Questions" 998 → reine Themen-Sets + Foto funktionieren.
- **Lange Videos weiter das Problem:** Median 9 Views (tvshow, 50 Q), CTR 2,9 %. Heute startet E1 (12 Fragen, ~7 min, "Score 4/12?"), morgen True-or-False-50. Testwoche bis 05.11. läuft unverändert weiter – keine Strategiewechsel.
- **Neu aus der Konkurrenz:** Clear Think "Part 2" (8 min) holt 187k (297×) → **7-Min-Tests funktionieren als Serie**; Quibby (206 Abos!) 343k mit "Name the Movie By The Car" = "Errate X an einem Detail" (Bilder nötig, bei uns nur mit image-credits machbar → Backlog).
- **Events:** 01.11. US-Zeitumstellung, **03.11. US-Midterms** → 02.11. "US Presidents Quiz" als E1 #2 (nur Fakten, keine Parteipolitik), 05.11. Bonfire Night, 11.11. Veterans Day.

## Konkurrenz-Gewinner heute

| # | Video (Kanal, Abos) | Views | × Median | Länge | Titel-Muster | Was wir übernehmen → Slot |
|---|---|---|---|---|---|---|
| 1 | "Test Your iQ in just 7 minutes" (Clear Think, 5,1k) | 1,30 Mio | 2067× | 6:48 | Zeitversprechen + IQ | Länge ~7 min → **E1 Long 31.10.** (in Queue) + 02.11. |
| 2 | "Are You Well Educated? … Score At Least 4/10!" (GK STUDIO PRO, 1,75k) | 980k | 1194× | 7:15 | Identität + niedrige Hürde "at least 4/10" | Hürde ⅓ → E1 31.10. "Score 4/12?", 02.11. "Score 5/15?" |
| 3 | "Test Your IQ Level in just 8 Min (Part 2)" (Clear Think) | 187k | 297× | 8:09 | Serien-Fortsetzung "Part 2" | Wenn E1 #1 ≥30 Views: E1 als Serie "7-Minute Test #2/#3" (Backlog 2) |
| 4 | "trivia challenge quiz 😌" (Think Nova, 2,5k) | 473k | 725× | 1:02 | generischer Suchbegriff, ~6–8 leichte Fragen | = unser 6-Fragen-Sieger → **Short 16:00 01.11.** (in Queue) |
| 5 | "Name the Movie By The Car … All 30 Movies" (Quibby, 206) | 343k | 1060× | 6:55 | "Name the X by the Y" + Zahl, ~7 min | Detail-Errate-Format; machbar als "Guess the Country by Its Outline/Flag" (Fotos aus image-credits) → Backlog 3 |

## 3-Tage-Plan

Layout überall **tvshow**. Zeiten Berlin. Fakten vor dem Schreiben prüfen (Britannica/NASA/CIA Factbook/Guinness/whitehouse.gov). broll-Regeln aus learnings.md (30.10.) gelten.

| Datum / Slot | Format | Thema | Arbeitstitel (YouTube) | Fragen + timing | Hook / Frage 1 | Musik | cardColors | Thumbnail A/B/C + Foto | Warum | Erfolgskriterium |
|---|---|---|---|---|---|---|---|---|---|---|
| **31.10. Long 14:00** | E1 7-Min (in Queue) | sehr schweres GK | (in Queue) General Knowledge Quiz: Can You Score 4/12? 🧠 | 12 | in Queue | brain-pulse | in Queue | in Queue | Konkurrenz #1/#2 | ≥30 Views n. 3 T ODER CTR ≥4 % ODER Ø angesehen ≥45 % |
| **31.10. Short 16:00** | 1-Frage leicht (in Queue) | Stunden/Woche | (in Queue) Can You Answer: How Many Hours Are in a Week? | 1 | in Queue | game-show | – | – | Exploit leichte Frage (1.137) | ≥700 Views n. 3 T |
| **31.10. Short 21:00** | VS E2 #1 (in Queue) | Ländergröße | (in Queue) Which Country Is Bigger? 4 Rounds 90% Get Wrong | 4 | in Queue | world-trip | – | – | neues Format | 3 VS ≥ 294 Views |
| **01.11. Long 14:00** | QuizLong 50 (in Queue) | True/False | (in Queue) True or False Quiz: 50 Facts From Easy to Legend ✅❌ | 50 | in Queue | game-show | – | in Queue | Keyword Nr. 1 | ≥50 Views n. 3 T |
| **01.11. Short 16:00** | 6-Fragen (in Queue) | GK | (in Queue) Only Geniuses Get 6/6 🧠 Trivia Challenge Quiz | 6 | in Queue | game-show | – | – | Exploit 1.333 | ≥1.000 Views |
| **01.11. Short 21:00** | True/False-Trap E3 #1 (in Queue) | Mythen | (in Queue) True or False? 4 Facts 90% Get Wrong ✅❌ | 4 | in Queue | brain-pulse | – | – | Experiment | ≥294 Views + stayed ≥50 % |
| **02.11. Long 14:00** | QuizLong **15 Fragen, ~7–8 min – E1 #2** | US-Präsidenten (Tag vor den Midterms; nur belegbare Fakten, keine Wertungen, keine aktuellen Kandidaten) | **US Presidents Quiz: Can You Score 5/15? 🇺🇸 7-Minute Test** (58 Zeichen) | 15, Level 5 HARD / 5 VERY HARD / 5 LEGEND, timing count 8.0 / tail 1.8 / tempo 0.95; nach jeder Antwort 1 Satz Erklärung | Intro 1 Satz: "Fifteen presidential questions, about seven minutes – most people don't get five. First one:" Q1 "Which president served the shortest time in office?" (William Henry Harrison, 31 Tage) – broll "white house exterior" | brain-pulse | navy / rot / weiß | A "SCORE 5/15?" + Foto aus image-credits (US-Flagge/Kapitol, falls vorhanden; sonst Flagge USA) · B "PRESIDENTS QUIZ" · C "MOST GET 3"; thumbBadge "HARD" | E1-Muster (Konkurrenz #1/#2) + Suchspitze rund um Wahltag 03.11.; Suchbegriff vorn ("us presidents quiz") | wie E1: ≥30 Views n. 3 T ODER CTR ≥4 % ODER Ø angesehen ≥45 % |
| **02.11. Short 16:00** | 1-Frage LEICHT – Exploit (n=3 Median 1.137) | Weltraum leicht | **Can You Answer: Which Planet Is Closest to the Sun? ☀️🤯** | 1, count 3.0 / tail 0.4 | Frage sofort gesprochen; Optionen Venus / Mercury / Mars / Earth (Merkur); Hinweis-Satz nach Reveal: "And it's not the hottest – that's Venus!" (Haken-Fakt); Loop "Follow if you got it!"; broll "night sky stars" (verrät nichts) | game-show | gelb/dunkelblau | – | leichte Frage schlägt schwere Ego-Hooks 3,4× | ≥700 Views n. 3 T |
| **02.11. Short 21:00** | VS-Vergleich – E2 #2 | Tiere Tempo | **Which Is Faster? 4 Races 90% Get Wrong 🐆** | 4 Runden, timing count 3.0 / tail 1.2; correctLabel "FASTER!"; valueLabels in km/h | R1 Hauskatze (~48 km/h) vs Usain Bolt (44,7 km/h Spitze) → Katze (Haken); R2 Grizzly (~56) vs Vollblut-Rennpferd (~70) → Pferd; R3 Flusspferd (~30) vs Mensch-Durchschnitt-Sprint (~24, belegen oder ersetzen) → Flusspferd; R4 Gepard (~110) vs Gabelbock (~88) → Gepard. Werte nur mit Quelle (Britannica/NatGeo/Guinness), Quelle in Beschreibung. Fotos aus image-credits.json, sonst icons. | world-trip | grün/orange | – | E2 #2 (eine Variable: Thema), VS-Themenliste aus STRATEGIE 29.10. | E2 gesamt: 3 VS ≥ 294 Views (4-Trap-Median) |

Bandit: 9 Slots, 4 Experiment-Slots (E1 ×2, E2 ×2, E3 ×1 – 31.10. + 02.11. je 2 Experimente) ≈ 40 % in dieser Testwoche, danach wieder 30 %.

## Ideen-Backlog (nach erwartetem Potenzial)
1. **03.11. Long: Geography Quiz Hard: 50 Questions From Easy to Legend 🌍** – 50-Q-Slot im Wechsel; Autocomplete "geography quiz hard/difficult/americans" (Score 2,4/2,0/2,7), eigener 8-Geography-Short 1.325.
2. **E1-Serie "General Knowledge Quiz #2: Can You Score 4/12?"** – nur wenn E1 #1 Kriterium erfüllt; Konkurrenz #3 (Part 2 = 187k).
3. **Guess the Country by Flag – 30 Flags (~7 min)** – Trends "guess the country" 30, Konkurrenz #5-Mechanik; Flaggen-Fotos in image-credits ggf. erweitern.
4. **6-Fragen "Which Came First?" #2** (Short) – eigener 1.234-Views-Short, neue Paare mit Jahren.
5. **Bonfire Night 05.11.: "4 British History Questions Almost Everyone Gets Wrong 💥"** – UK-Datum, Themen-Set Geschichte (998 Views-Muster).
6. **Guess the Movie by Emoji (Long, ~7 min, 20 Filme)** – Konkurrenz 512k; unser Emoji-Long beste Bindung (72 %).
7. **Tricky Quiz – Level 1/2/3 (Short-Serie)** – last30days 1,66 Mio (Instagram); Serien-Experiment ab 06.11.
8. **Which Is Taller? VS Gebäude/Berge** – E2 #3, CTBUH-Daten, Fotos.
9. **Veterans Day 11.11.: "US History Quiz: Can You Score 4/12?"** – Events + E1-Mechanik.
10. **"The Last One Will Humble You" Titeltest auf 4-Fragen-Trap** – last30days 279k/7,5k Kommentare; nur Titel ändern.

## Für den Produktions-Agenten (gilt heute, überschreibt ältere Defaults)
- Heute die **3 Items für 02.11.** anlegen (Dateinamen: `2026-11-02-us-presidents-5-15.json`, `2026-11-02-one-q-closest-sun.json`, `2026-11-02-vs-animals-faster-1.json`). Wenn Zeit bleibt, 03.11. Long aus Backlog 1 vorziehen.
- **E1 #2 (02.11.) ist erlaubt und überschreibt "immer 50 Fragen":** genau 15 Fragen, Ziel 7:00–8:00 min, Outro "Comment your score – did you beat five?". Strikt unpolitisch: nur historische Fakten (Amtszeiten, Reihenfolge, Gesichter auf Geld, Rekorde), keine Fragen zu aktuellen Wahlen oder Kandidaten.
- VS-Werte: wenn ein Tempo-Wert nicht eindeutig belegbar ist (z. B. Mensch-Durchschnitt), Runde ersetzen (z. B. Strauß ~70 vs Windhund ~72 nur bei klarer Quelle) – keine strittigen Zahlen.
- Vor jedem Item gegen queue/done + stories greppen (Fragen + Titel); Fotos nur aus image-credits.json, nie antwortverratend.
- Kein Halloween-Bezug (heute 31.10.!): keine Orange/Schwarz-Kombination, keine Spooky-Wörter.
