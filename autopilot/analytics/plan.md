# Plan – 2026-11-20 (Fr)

## TECHNIK-PROBLEM (zuerst erledigen)
1. **Produktions-Auftrag vom 19.11. wurde NICHT ausgeführt:** Kein Produktions-Commit am 19.11., `autopilot/queue/` enthält nur die zwei 20.11.-Items. Es fehlen **alle drei Items für Sa 21.11. (Long-Tag!)** – ohne sie läuft morgen kein Long und ggf. nur der Ersatz-Generator. → Heute ZUERST 21.11. anlegen (Thanksgiving-Long, Which-Came-First #3, map-lie-5), danach 22.11.
2. **Karten-Formen fehlen weiter:** `egypt`, `saudiarabia`, `argentina` (map-lie-5) und `zimbabwe`, `kenya`, `indonesia` (map-lie-6) sind NICHT in `src/data/truesize.json` (`mongolia`, `peru` sind da). In `scripts/build-truesize-data.mjs` ergänzen, Skript laufen lassen, Kontrollspalte prüfen, committen.
3. **QA-Warnung Long iq-riddles-12-1 (19.11.): „Standbild 26,6 s“** (Grenze sonst Abspann ~11,6 s). Prüfen, wo das Bild steht (vermutlich langer Rätsel-Denk-Count `count 20` ohne Bewegung oder Abspann). Wenn es die Denkzeit ist: ab nächstem Rätsel-Long Timer/Balken-Animation sicherstellen bzw. count ≤ 15. Kein Re-Upload.
4. Snapshot report.json = 19.11. 19:25 (≈11 h alt) – ok. Kosmetik offen: scoreboard.md führt Karten-Longs als „0 Fragen“.

**Layout-Regel (geändert, siehe unten):** Alle Nicht-Karten-Videos ab heute `layout "tvshow"` (Owner-Vorgabe „kein AI-Look, tvshow für alles“). Karten-VS bleibt `story.type "truesize"` (eigene Komposition, unverändert).

## Zusammenfassung (Deutsch)
- **E16-Paar 3 dreht das pop-Ergebnis:** atlas „Tricky Quiz“ (41 s) **635 Views n. ≈1 T** vs. pop „Capitals Quiz“ 160 → Summe der 3 Paare pop 405 vs. atlas 721. Layout ist NICHT der Hebel; Hebel = Titel/Thema („Tricky“ = 1.554 + 635) und Länge ≤ 45 s. Darum zurück zu **tvshow** (Owner-Pflicht, historisch Shorts-Median 442) statt pop.
- **Rätsel-Long E14 startet stark:** „Test Your IQ: 12 Tricky Riddles“ **32 Views n. ≈2 h** – mehr als US-Karten-Long (19) nach 2,3 Tagen. Die zwei früheren 7-min-Videos hatten 0 → E14 NICHT gestoppt (3. Video liegt klar über Long-Median ~8).
- **E13 (Longs 2.0) Vorab-Verdict ✗:** erste 4 Longs ab 10.11. = 131 / 18 / 25 / 19 → Median 22 (Ziel 30), nur 1 ≥ 100. Karten-/Emoji-Long-Serie eingestellt; Long-Plätze gehen an Suchanlässe (Thanksgiving, Christmas) und IQ-Rätsel.
- Geo-Trivia (atlas, 43 s) 244 n. ≈2,5 h – guter Start. Karten-VS #3 lief erst 21:00 (noch keine Zahlen).

## Konkurrenz-Gewinner heute (competitors.md 19.11., Upload ≤ ~30–55 Tage)

| # | Video (Kanal, Abos) | Views | × Median | Länge | Titel-Muster | Was wir übernehmen → Slot |
|---|---|---|---|---|---|---|
| 1 | "Can You Pass This Thanksgiving Trivia Quiz? 🦃 45 Questions for Adults" (Still Sharp Trivia, 498) | 65.308 | 130,6× Abos | 21:47 | Feiertag + Fragenzahl + „for Adults“ | **Sa 21.11. Long „Thanksgiving Trivia Quiz 🦃 Can You Get 40/50?“** (eigene 50 Fragen) |
| 2 | "Christmas Quiz for Adults 🎄 Can You Get 40 Out of 45?" (Still Sharp Trivia, 498) | 62.927 | 125,9× Abos | 18:37 | Feiertag + Zielgruppe + Hürde | **Di 24.11. Long Christmas Quiz for Adults** |
| 3 | "10 Tricky IQ Riddles / Test Your Intelligence!" (Quiz World, 1.080) – 22.10. | 520.397 | 277,5× | 6:48 | Zahl + „Tricky“ + IQ | unser E14 läuft gut an → **Do 26.11. Rätsel-Long #2** (falls E14 ≥ 50 n. 3 T) |
| 4 | "You're Not Smart Enough to Solve These 12 Puzzles!" (Quiz Guy, 495) – 15.10. | 85.661 | 73,7× | 8:15 | Ego-Provokation + Zahl | Titelalternative für Rätsel-Long #2: „12 Riddles You're Not Smart Enough to Solve 🧠“ |
| 5 | "Can You Name F1 Track From Above? — Part 3" (Dopamine Quiz, 443) – 31.10. | 30.267 | 42,2× | 8:50 | Erkennen von oben + Serien-Nr. | bestätigt Serien-Nummerierung → Karten-VS „#N“ täglich 21:00 |

Nicht übernommen: Senioren-/Alters-Titel, Fußballer/F1/Disney (Bild-/Musikrechte), Promi-Stimmen, Filme zu „Hexed“ / „Focker-In-Law“ (Kinostart 25.11., aber Movie-Quiz bei uns ✗ und keine Bilder erlaubt).

## 3-Tage-Plan

| Datum / Slot | Format | Thema | Arbeitstitel (YouTube) | Fragen + timing | Hook / Fragen | Musik | cardColors | Thumbnail / Bild | Warum | Erfolgskriterium |
|---|---|---|---|---|---|---|---|---|---|---|
| **20.11. (Fr) Long 14:00** | – | – | kein Long (LONG_DAYS Di/Do/Sa) | – | – | – | – | – | Owner-Strategie 09.11. | – |
| 20.11. Short 16:00 | 6-Q (Queue six-q-iq-quiz) – **layout auf "tvshow" umstellen** | Logik | Quick IQ Test: Can You Get 6/6? 🧠 | Queue | Queue | game-show | ["#5B21B6","#1E1B4B"] | cardText | Exploit IQ/Tricky-Titel; Verweis auf E14-Long | ≥ 400 n. 3 T |
| 20.11. Short 21:00 | Karten-VS (Queue map-lie-4) | 4 Paare | This Map Is Lying To You #4 🌍 Which Is REALLY Bigger? | 4 Runden | Queue | world-trip | – | – | Exploit #1 (936/1.021) | ≥ 800 n. 3 T |
| **21.11. (Sa) Long 14:00 – HEUTE ANLEGEN** | QuizLong tvshow v2, Levels-Banner EASY 1–15 / MEDIUM 16–30 / HARD 31–42 / LEGEND 43–50 | Thanksgiving (Geschichte, Essen, Parade, Football, Tiere) | **Thanksgiving Trivia Quiz 🦃 Can You Get 40/50? \| For Adults** | 50, count 6 / tail 1.2 / tempo 1.0 | Hook „Only true Thanksgiving experts get 40 out of 50. Ready?“ · Q1 „In which month is US Thanksgiving?“ (November) · Kandidaten (prüfen + Duplikat-grep; „Thanksgiving“ steht schon in citizenship-test-50-1 – diese Frage nicht wiederholen): Mayflower-Ankunft 1620 · Plymouth = heutiges Massachusetts · Wampanoag-Anführer Massasoit · Lincoln 1863 Nationalfeiertag · FDR 1939 „Franksgiving“ · 1941 = 4. Donnerstag per Gesetz · Macy's Parade seit 1924 · Kanada = 2. Montag im Oktober · Präsidenten-„Turkey Pardon“ · Detroit Lions spielen traditionell · Cranberry in Nordamerika heimisch · männlicher Truthahn = „tom“ · Wildtruthähne können fliegen · Sarah Josepha Hale · Black Friday = Tag danach | game-show | ["#B45309","#7C2D12"] | A „THANKSGIVING / TRIVIA“, B „CAN YOU GET / 40/50?“, C „ONLY 1% GET / 50/50“; `thumbPuzzle` „🦃 + 🚢 + 1620 = ?“; Badge „50 Q“ | Konkurrenz #1 (130,6×) + Halloween-Text-Long = unser bestes Long (186) + US-Publikum 75 % | ≥ 60 n. 3 T, ≥ 150 bis 27.11. |
| 21.11. Short 16:00 – HEUTE ANLEGEN | 5-Q Mehrfachauswahl, **tvshow** | Zeitachsen-Fallen | **Which Came First? Most People Fail #3 🦣** (+ #shorts) | 5, count 2.5 / tail 0.6, ≤ 70 Wörter | Q1 Amazon 1994 (vs Google 1998/Netflix 1997/Wikipedia 2001) · Q2 Wright brothers 1903 (vs Titanic 1912/WWI 1914/Hollywood sign 1923) · Q3 Falle Great Pyramid c. 2560 BC vor letzten Mammuts c. 2000 BC (vs Rom 753 BC / Olympia 776 BC) · Q4 „Which was invented first?“ Lighter 1823 (vs Matches 1826 / Typewriter 1868 / Sewing machine 1846) · Q5 Ottoman Empire 1299 (vs Ming 1368 / Tenochtitlan 1325 / Inca 1438) → Antwortreihenfolge mischen | game-show | ["#0E7490","#164E63"] | cardText „🔍“, „✈️?“, „🦣 vs 🔺“, „🔥“, „👑“ | Exploit Titeltyp (Median 698, stayed 62,5 %) | ≥ 600 n. 3 T |
| 21.11. Short 21:00 – HEUTE ANLEGEN | Karten-VS `story.type "truesize"`, Muster map-lie-4 | Sweden/Egypt, Norway/Philippines, Alaska/Saudi Arabia, Argentina/Greenland | **This Map Is Lying To You #5 🌍 Which Is REALLY Bigger?** (+ #shorts) | 4 Runden, kicker „MAP TEST #5“ | R1 Sweden vs **Egypt** (2× bigger) · R2 **Norway** vs Philippines (8 %, Twist) · R3 Alaska vs **Saudi Arabia** (25 %) · R4 **Argentina** vs Greenland (28 %). CIA km²: Sweden 450,295 · Egypt 1,001,450 · Norway 323,802 · Philippines 300,000 · Alaska 1,717,856 · Saudi Arabia 2,149,690 · Argentina 2,780,400 · Greenland 2,166,086 | world-trip | – | – | Exploit #1 + Konkurrenz #5 (Serie) | ≥ 800 n. 3 T |
| **22.11. (So) Long 14:00** | – | – | kein Long (LONG_DAYS) | – | – | – | – | – | – | – |
| 22.11. Short 16:00 – HEUTE ANLEGEN | 1-Frage-Ego-Hook, **tvshow** | Geo-Falle USA | **Which City Is Further West? 9 in 10 Get It Wrong 🤯** (+ #shorts) | 1 Frage, count 4 / tail 1.0, ≤ 35 Wörter | „Which city is further WEST?“ Los Angeles / **Reno** / Las Vegas / Phoenix → Reno (≈119,8° W vs LA ≈118,2° W); Antwortzeile „Reno! Yes, really.“ (Reno nicht in stories – gegrept, nur „Renoir“) | game-show | ["#1D4ED8","#1E3A8A"] | cardText „🧭⬅️“ | Exploit kürzestes Format (1-Frage-Ersatz Median 622, Bestes 1.208) + US-Publikum | ≥ 600 n. 3 T |
| 22.11. Short 21:00 – HEUTE ANLEGEN | Karten-VS #6 | Germany/Zimbabwe, Spain/Kenya, Greenland/Indonesia, Mongolia/Peru | **This Map Is Lying To You #6 🌍 Which Is REALLY Bigger?** | 4 Runden | Zimbabwe 390,757 > Germany 357,022 (+9 %) · Kenya 580,367 > Spain 505,370 (+15 %) · Greenland 2,166,086 > Indonesia 1,904,569 (+14 %, Twist) · Mongolia 1,564,116 > Peru 1,285,216 (+22 %) | world-trip | – | – | Exploit #1 | ≥ 800 n. 3 T |

**Vorschau (nicht anlegen):** Di 24.11. Long „Christmas Quiz for Adults 🎄 Can You Get 40/50?“ (50 Q, tvshow v2, thumbPuzzle „🎄 + 🇩🇪 = ?“) · Mi 25.11. 16:00 „Thanksgiving Trivia Quiz! Can You Get 5/5? 🦃“ (verlinkt Long) · Do 26.11. (Thanksgiving) Long = Rätsel-Long #2 „12 Riddles You're Not Smart Enough to Solve 🧠“ falls E14 ≥ 50 n. 3 T, sonst Thanksgiving-Short-Paket.

Bandit 20.–22.11.: 6 Slots Exploit (Karten-VS ×3, Which-Came-First, 1-Frage-Hook, IQ-Short), 1 Konkurrenz-Muster mit starker Evidenz (Thanksgiving-Long), Experiment-Variable diese Tage = **Layout tvshow** (Rückkehr, alle Mehrfragen-Shorts).

## Ideen-Backlog (nach erwartetem Potenzial)
1. **Karten-VS täglich 21:00 (#7 ff.)** – 936 / 1.021 Views, Ø angesehen 74–81 %; pro Woche 6–8 neue Formen bauen.
2. **„Tricky Quiz“-Titel öfter (alle 4–5 Tage, wechselnde Themen)** – 1.554 + 635 n. 1 T; 41-s-Länge.
3. **Christmas Quiz for Adults (Long 24.11.)** – Still Sharp 62,9k (125,9×); Suchphrase „christmas quiz for adults“.
4. **Rätsel-Long #2** – E14 32 Views in 2 h; Clear Think 1,87 Mio (1.777×), Quiz World 520k.
5. **Thanksgiving-Short 25.11.** – Feiertagssuche + Long-Verlinkung.
6. **True-or-False-Short (tvshow, 5 Aussagen)** – „true or false quiz“ = Autocomplete-Platz 1 (17,1); einziger alter T/F-Versuch 145 (atlas, lang).
7. **„Name the Country From Its Outline“** – Chauncey „airline from its livery“ 825k, Playbill 1,96 Mio; Umrisse aus truesize.json, braucht Code-Hook.
8. **„Can You Pass the U.S. Citizenship Test?“ Long #2** – Trivia Square 2,78 Mio (74×); Suchphrase in Autocomplete (2,2); unser Versuch 26.10. alt → neue Fragen.
9. **„Which Came First?“ alle 2 Wochen** – falls #3 ≥ 600.
10. **Black-Friday-VS „Which Costs More?“ 27.11.** – nur mit offiziellen Listenpreisen.

Gestrichen: Karten-Long #3 / Emoji-Longs (E13 ✗), pop als Standard, People-/Bigger-VS, Europa-/Flaggen-/Film-/Tier-/World-Geo-6-Q, Weltraum, Alters-Titel, Halloween, F1/GTA/Disney (Rechte).

## Für den Produktions-Agenten (gilt heute, überschreibt ältere Defaults)
- **Reihenfolge:** (1) Formen egypt, saudiarabia, argentina, zimbabwe, kenya, indonesia bauen + prüfen; (2) **21.11. anlegen:** `2026-11-21-thanksgiving-quiz-50-1.json` (Long 14:00), `2026-11-21-six-q-which-first-3.json` (16:00), `2026-11-21-map-lie-5.json` (21:00); (3) **22.11. anlegen:** `2026-11-22-one-q-further-west.json` (16:00), `2026-11-22-map-lie-6.json` (21:00); (4) in `2026-11-20-six-q-iq-quiz.json` `layout` von "pop" auf **"tvshow"** ändern (vor dem 16:00-Lauf).
- **Layout:** Alle Shorts außer Karten-VS und alle Longs `layout "tvshow"` (kein pop, kein atlas mehr). Grund: Owner-Vorgabe + E16-Paar 3 (atlas 635 vs. pop 160) widerlegt den pop-Vorteil.
- Shorts ≤ 80 gesprochene Wörter (Ziel ≤ 45 s), Antwortzeile nur Antwort (+ max. 4 Wörter).
- Alle Fragen frisch schreiben, faktenprüfen, Duplikat-grep über stories/ + queue/done (Inhalt, nicht nur Wortlaut).
- Weiter verboten: VS mit pop, Longs Mo/Mi/Fr/So, 3. Short am Tag, Weltraum, Halloween, Politik, Krieg/Waffen, 💥, Alters-Titel.
- vidIQ: heute kein Aufruf nötig (Konkurrenzdaten frisch vom 19.11.).
