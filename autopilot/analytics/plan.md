# Plan – 2026-11-08

## TECHNIK-PROBLEM
1. **Gunpowder-Short bestätigt unterdrückt:** "4 Gunpowder Plot Questions – Can You Get 4/4? 💥" hat **1 öffentlichen View nach ~53 h** (Status public, keine ytRating/regionRestriction/rejectionReason). → Besitzer wird informiert (Studio prüfen: „eingeschränkt“/Werbe-Eignung). **Nicht neu hochladen.** Regel bleibt: keine Sprengstoff-/Waffen-/Anschlags-Themen, kein 💥.
2. **Reichweiten-Einbruch seit 05.11. (4/4 Shorts unter Median):** erster Snapshot nach Upload (~19–29 h): Vocabulary 115, Gunpowder 0, Science 6-Q **67**, VS Taller 271 – vorher Geo-6-Q 769, VS People 1.007, Trivia-6-Q 1.032. Teilweise Thema (Vocab, Gunpowder, Science war schon früher schwach: 154), aber auffällig: **Render-Änderung 05.11. 10:10 (Commit 3a4c87a: Lautheit −14 LUFS + wortsynchroner Schlüsselwort-Marker in QuizTV)** gilt ab den 06.11.-Shorts. Prüfregel für den Produktions-Agenten: Wenn im Analytics-Lauf heute (≈08:10) **"Only Geniuses Get 6/6 🧠 Capital Cities Quiz" < 300 UND "Which Country Has More People?" < 300** öffentliche Views haben → Schlüsselwort-Marker per Flag abschalten (Lautheits-Normalisierung behalten) und in learnings.md als Regressions-Test vermerken. Sonst nichts ändern.
3. **Standbild-Warnungen:** QA meldet Standbild 6,8 s im VS Taller (06.11., Short!) und 7,8–8,8 s in Longs. In Shorts darf kein Bild > 3 s stillstehen (Wisch-Gefahr) → während der Denkzeit muss sich Countdown/Balken/Puls sichtbar bewegen; bei VS count ≤ 3.0 s lassen, und wenn QA > 4 s meldet, neu rendern statt hochladen.
4. Kein Lauf-Fehler im Log (07.11.: Uploads 06:17–06:38, Kommentare 13:54/15:55/20:58 mit Long-Link, Konkurrenz 25 Kanäle / 132 Gewinner). Analytics-Stand noch **07.11. 11:30**. Queue 08.11. + 09.11. vollständig → **nur 10.11. neu anlegen.**
5. Risiko GitHub-Actions-Minuten (Limit 2.000/Monat) bleibt – bei "spending limit"-Fehlern Besitzer informieren.

## Zusammenfassung (Deutsch)
- **VS bleibt Leader:** "Which Has More People?" 1.142 final (stayed 62 %), Geo-6-Q 975 final. VS-Median jetzt 875 (≈1,9× Shorts-Median 454). VS Taller aber nur 271 n. ~15 h (Standbild 6,8 s!) → 21:00 VS bleibt, Standbild-Fix Pflicht.
- **6-Q: nur leichte Allgemein-/Geo-Fragen tragen.** Gewinner (1.433 / 1.218 / 975) = sehr leichte Fragen + "Only Geniuses"-Titel; Themen-6-Q floppen: Vocabulary 144 (E5 ✗), Science 67 n. 20 h, Which-First R2 158. → 10.11. zurück zum stärksten Muster "Only Geniuses Get 6/6 🧠 … Trivia" mit Konkurrenz-Wort „Tricky“ (Quiz World 518k).
- **Longs weiter 0–3 Views** (History-50 um 19:00 [E7]: 0 n. ~17 h; Geography-50 final 3). E8 (30 Q, enges Suchthema) läuft bis Verdict 12.11.; 10.11. E8 #4 = **Guess the Movie by Emoji** (einziges Long-Muster mit Reichweite bei uns: Emoji-15 = 141; Konkurrenz Quiz Bunny 680k, 129×).
- Abos 15 (+1). Warnsignal: seit 05.11. alle 4 Shorts unter Median → Regressions-Test (Technik 2).

## Konkurrenz-Gewinner heute (letzte 30–45 Tage, competitors.md 07.11. + outliers.md 06.11.)

| # | Video (Kanal, Abos) | Views | × Median | Länge | Titel-Muster | Was wir übernehmen → Slot |
|---|---|---|---|---|---|---|
| 1 | "Test Your iQ in just 7 minutes" (Clear Think, 6.650) – 29.09. + Part 2 "in just 8 Min" 13.10. | 1.695.777 / 237.745 | 2.007× / 281× | 6:48 / 8:09 | IQ + Zeitversprechen, kein Emoji | Bestätigt Länge 7–8 min (E8). Unser E1 (Score-X-Hürde) war 0/0/1 → Zeitversprechen erst nach E8-Verdict als Titel-Test (Backlog #4) |
| 2 | "Are You Well Educated? … Score At Least 4/10!" (GK STUDIO PRO, 1.870) | 1.057.910 | 1.134× | 7:15 | Identitäts-Frage + niedrige Hürde | = unser E1 „Well Educated 5/15“ (1 View) → Muster greift bei uns nicht, solange Longs keine Impressionen bekommen; nicht wiederholen vor 12.11. |
| 3 | "trivia challenge quiz 😌" (Think Nova, 2.540) – Short | 485.006 | 547× | 1:02 | generischer Suchbegriff klein, 1 Emoji | Deckt sich mit unserem 1.218er "Trivia Challenge Quiz" → **10.11. 16:00 6-Q „Tricky Trivia“** (leichte Fragen, ~50 s) |
| 4 | "Name the Movie By The Car / Can You Name All 30 Movies By The Car?" (Quibby, 229) | 380.462 | 1.180× | 6:55 | „Name the Movie by X“ + 30 + Ganzzahl-Challenge | Film-Erkennung + 30 Runden + ~7 min → **10.11. Long E8 #4 "Guess the Movie by Emoji: 30 Rounds"** (Filmtitel nur als Text/Emoji, keine Filmbilder außer lizenzierten mv-*.jpg) |
| 5 | "Guess the Movie by Emoji 🎬🍿 Movie Quiz" (Quiz Bunny, 5.230) | 679.501 | 129× | 12:13 | Suchphrase vorn + 2 Emojis | Gleiche Suchphrase vorn im 10.11.-Long, aber 30 statt ~60 Runden, eigene Emoji-Rätsel |

Nicht übernommen: Chauncey Asks (Straßen-Interviews; Playbill/Airline-Livery = Markenrechte), comicnutz (Comic-Figuren), Clue Senpai (Anime-Zeichnungen), FootyMind A–Z (Sport-Longs bei uns 6–8 Views), QuizNova "Ages 70–95" (= gestopptes Alters-Muster, 4 Views), Disney-Songs (Musikrechte).

## 3-Tage-Plan

Layout überall **tvshow**. Fakten vor dem Schreiben prüfen (Britannica, NASA, Smithsonian, offizielle Firmenseiten). Gegen `queue/done/*` greppen. **08.11. + 09.11. liegen fertig in der Queue → nur 10.11. neu anlegen.**

| Datum / Slot | Format | Thema | Arbeitstitel (YouTube) | Fragen + timing | Hook / Frage 1 | Musik | cardColors | Thumbnail A/B/C + Foto | Warum | Erfolgskriterium |
|---|---|---|---|---|---|---|---|---|---|---|
| 08.11. Long 14:00 | E8 #2 (Queue) | Sonnensystem | Solar System Quiz: 30 Questions From Easy to Legend 🪐 | 30 (Queue) | Queue | brain-pulse | Queue | Queue | E8 | E8-Verdict 12.11. |
| 08.11. Short 16:00 | 6-Q E9 (Queue) | Weltraum | Only Geniuses Get 6/6 🧠 Space Quiz | 6 (Queue) | Queue | game-show | – | – | Themen-Test | ≥800; <400 → Space raus |
| 08.11. Short 21:00 | VS #6 (Queue) | Planeten & Monde | Which Is Bigger? Planets & Moons – 90% Get #2 Wrong 🪐 | 4 (Queue) | Queue | world-trip | – | – | Exploit VS | ≥700 |
| 09.11. Long 14:00 | E8 #3 (Queue) | Flaggen | Flag Quiz: 30 Questions From Easy to Legend 🚩 | 30 (Queue) | Queue | world-trip | #7F1D1D/#FFF7ED | Queue | E8 + Konkurrenz Flaggen | E8-Verdict 12.11. |
| 09.11. Short 16:00 | 6-Q E10 (Queue) | Mauerfall-Jahrestag | Only Geniuses Get 6/6 🧠 Berlin Wall Quiz | 6 (Queue) | Queue | game-show | – | – | Jahrestag | ≥800; <400 → keine Jahrestage um 16:00 |
| 09.11. Short 21:00 | VS #7 (Queue) | Gewicht | Which Is Heavier? 4 Rounds 90% Get #2 Wrong 🐘 | 4 (Queue) | Queue | world-trip | – | – | Exploit VS | ≥700 |
| **10.11. Long 14:00** | **E8 #4**: QuizLong 30 Runden, 5 Level à 6 EASY→MEDIUM→HARD→VERY HARD→LEGEND, Ziel 7–8 min | Filme per Emoji (Emoji-Format wie emoji-word-50-1) | **Guess the Movie by Emoji: 30 Rounds From Easy to Legend 🎬** (55 Z.) | 30, count 6.0 / tail 1.2 (Emoji-Rätsel brauchen mehr Denkzeit als Wissensfragen), midCtaIndex 14, `fact` bei allen 30 (Jahr + 1 Satz) | Hook "CAN YOU GET 25/30? 🎬"; Q1 sehr leicht: 🦁👑 → The Lion King; weiter z. B. 🧊🚢💔 Titanic, 🦖🏝️ Jurassic Park, 🕷️🧑 Spider-Man, 👻🚫 Ghostbusters, 🧙‍♂️💍🌋 Lord of the Rings, 🏠🎈👴 Up, 🐀👨‍🍳 Ratatouille; LEGEND z. B. 🥊👊🧼 (Fight Club), 🕰️🚗⚡ Back to the Future. 4 Optionen, Fangoption je Runde (ähnlicher Film). Nur Titel als Text, keine Logos/Poster | game-show | ['#1E1B4B', '#FDE68A'] (Kino-Violett/Gold) | A "GUESS THE **MOVIE**" + `bilder/mv-delorean.jpg` · B "CAN YOU GET **25/30**?" · C "**LEGEND** LEVEL"; thumbEmoji 🎬, thumbBadge "30 ROUNDS · EASY → LEGEND" | E8 #4 + Konkurrenz #4/#5 (Quibby 380k, Quiz Bunny 680k); bei uns einziges Long mit Reichweite = Emoji (141) | E8 gesamt: Median ≥10 öffentl. Views n. 3 T UND Ø angesehen ≥40 % |
| **10.11. Short 16:00** | 6-Q (Exploit, ≤50 s) | Allgemeinwissen leicht → mittel | **Only Geniuses Get 6/6 🧠 Tricky Trivia Quiz** (+ #shorts, 41 Z.) | 6, count 2.5 / tail 0.8, Antworten ≤ 5 Wörter, 4 Optionen, schwerste an Platz 4 | Q1 sehr leicht: "How many sides does a hexagon have?" → 6. Dann z. B.: "Which ocean is the largest?" → Pacific; "What do bees make?" → Honey (nicht in done prüfen: honey-Short war Blüten-Frage → ok); **#4 Trick: "Which fruit has its seeds on the outside?" → Strawberry** (Fangoptionen Kiwi/Banana/Raspberry); "What is the capital of Australia?" → Canberra (nur wenn nicht in Capitals-30/6-Q → sonst "How many continents are there?" → 7); Finale "Which planet is known as the Red Planet?" → Mars. Loop-Satz "Got all six? Go again!" | game-show | – | – (Shorts: Frame; Q1 cardText ⬡) | Bester Short-Typ: 6-Q leicht + "Only Geniuses" (1.433 / 1.218 / 975); Konkurrenz #3 "trivia challenge quiz" 485k; „Tricky“ aus Quiz World (518k) | ≥1.000 Views n. 3 T |
| **10.11. Short 21:00** | VS #8 (Exploit) | Alter: Bauwerke & Firmen | **Which Is Older? 4 Rounds 90% Get #2 Wrong 🏛️** (44 Z.) | 4, count 3.0 / tail 1.2, correctLabel "OLDER!", valueLabels "≈ … years old" (Basis 2026) | R1 leicht: Big Ben/Elizabeth Tower (1859 → 167 J.) vs Eiffel Tower (1889 → 137 J.); **R2 Haken: Nintendo (gegr. 1889 → 137 J.) vs Ford Motor Company (1903 → 123 J.)** → Nintendo älter; R3: Gutenberg-Druckerpresse (≈1440 → ≈586 J.) vs Machu Picchu (≈1450 → ≈576 J.); R4 Finale: Great Pyramid of Giza (≈2560 v. Chr. → ≈4.580 J.) vs letzte Wollhaarmammuts (Wrangel-Insel, ausgestorben ≈ 2000 v. Chr. → ≈4.000 J.) → Pyramide älter als das Aussterben der Mammuts (Foto `bilder/q2-mammoth.jpg` + `bilder/q2-pyramid.jpg`, wenn CompareScene Fotos nimmt). Vorher gegen done greppen (Which-First R1 hatte „Which is the oldest?“ – wenn Mammut/Pyramide dort schon war, R4 ersetzen durch Harvard 1636 vs Newtons Principia 1687) | world-trip | – | – | VS 4/5 Treffer (875–1.142); „Which Came First“ R1 1.234 = Alters-Thema funktioniert, nur Sequel-Titel war tot → neuer VS-Titel ohne „Round 2“ | ≥700 Views n. 3 T |

Bandit 08.–10.11.: Exploit 5 (VS ×3, 6-Q Tricky Trivia, 6-Q-Format) / Experiment 4 (E8 ×3, E9/E10 Themenvariable) ≈ 60/40 – akzeptiert (Longs ohne Reichweite; alle Shorts im Gewinnerformat).

## Ideen-Backlog (nach erwartetem Potenzial)
1. **11.11. Veterans/Remembrance Day: 6-Q "Only Geniuses Get 6/6 🧠 World War 1 Quiz" (16:00)** – US+UK ≈ 2/3 Publikum, Suchspitze am 11.11.; nur Fakten (11. Stunde, 1918, Mohnblume), keine Waffen-/Gewalt-Bilder, kein 💥 (Lehre aus Gunpowder) → falls Risiko zu hoch: "Poppy & Armistice"-Faktenquiz.
2. **11.11. VS "Which Is Colder?" (Orte/Planeten)** – VS-Variante, Fangrunde Antarktis-Rekord (−89,2 °C) vs Mars-Durchschnitt (≈ −60 °C).
3. **6-Q "Only Geniuses Get 6/6 🧠 Flag Quiz"** – Konkurrenz "Only 5% can name these flags" 189k; erst nach Flag-Long-Daten (09.11.) und mit anderen Flaggen als im Long.
4. **Long-Titeltest nach E8-Verdict: "Test Your General Knowledge in Just 7 Minutes"** – Clear Think 1,7 Mio (2.007×) + 238k; Zeitversprechen statt Score-Hürde.
5. **GTA-VI-Woche (Release 19.11.2026, Take-Two bestätigt): 6-Q "Only Real Fans Get 6/6 🎮 GTA Quiz" 18.11. + E8-Long 17.11.** – riesige Suchspitze; nur Textfakten, keine Spielbilder/Logos.
6. **VS "Which Is Longer?" (Flüsse/Brücken/Mauern)** – VS-Format, Fangrunde Nil vs Amazonas (Streitfall → nur unstrittige Paare).
7. **E8-Long "Guess the Country by Emoji: 30 Rounds"** – unser Emoji-Länder-Short 1.304; Autocomplete "country guess the country" (Score 4,2).
8. **"12 Tricky Riddles – Can You Solve 4?" (~7 min)** – Quiz World 518k, Quiz Guy 82k; nach E8-Verdict, nur wenn Renderer Rätseltexte sauber zeigt.
9. **Hunger Games: Sunrise on the Reaping (Kinostart 20.11.)** – 6-Q "Only Real Fans Get 6/6 🏹 Hunger Games Quiz" 19./20.11.; reine Textfragen.
10. **Thanksgiving 26.11.: 6-Q "Only Geniuses Get 6/6 🦃 Thanksgiving Quiz" + E8-Long** – saisonal US; Halloween-35 war bestes Fragen-Long (185).

## Für den Produktions-Agenten (gilt heute, überschreibt ältere Defaults)
- **3 Items für 10.11.** anlegen: `2026-11-10-movie-emoji-30-1.json` (Long, publishAt "14:00", Emoji-Format wie emoji-word-50-1, 30 Runden, Struktur wie Capitals-30), `2026-11-10-six-q-genius-tricky.json` (publishAt "16:00"), `2026-11-10-vs-older-1.json` (publishAt "21:00").
- **6-Q-Fragen leicht halten** (Gewinner hatten Insekt 6 Beine / Taj Mahal / Saturn-Ringe) – nur Frage 4 ist die Fangfrage. Keine Wissenschafts-/Wortschatz-Themen mehr in 6-Q.
- **Standbild in Shorts ≤ 3 s** (QA-Warnung > 4 s → neu rendern). Technik 2 (Marker-Regressionstest) nach dem heutigen Analytics-Lauf prüfen.
- Keine Sprengstoff-/Waffen-/Anschlags-Themen, kein 💥, keine Politik, kein Halloween, keine E1-Longs, keine Alters-Titel.
- Filmrätsel: nur Filmtitel als Text + Emojis; Bilder nur `bilder/mv-*.jpg` aus image-credits.json.
- Shorts-Kommentar 10.11. verlinkt aufs Movie-Emoji-Long (sobald öffentlich).
