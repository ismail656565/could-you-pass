# Plan – 2026-11-13 (Fr)

TECHNIK-PROBLEM: nichts Blockierendes. Läufe 12.11. grün (movie-emoji-30-1 14:00, vs-older-1 16:00, six-q-genius-movies 21:00 hochgeladen, alle 3 Kommentare gepostet). Hinweise: (1) Letzter Analytics-Snapshot 12.11. 11:52 – die 12.11.-Videos waren dort noch privat → heutiger Lauf muss frischen Snapshot ziehen. (2) Kleinigkeit scoreboard.md: Karten-Long (TrueSizeLong) wird als Format „0 Fragen“/Layout „comic“ gezählt und map-lie-1 als „comic“ → in der Scoreboard-Gruppierung `story.type == "truesize"` als Format „Karten“ / Layout „atlas“ führen (nicht kritisch). (3) CTR per API weiter nicht messbar (HttpError 400, bekannt).

## Zusammenfassung (Deutsch)
- **atlas gemischt statt klar vorn:** six-q-genius-tricky **1.045** (~1,9 T) und map-lie-1 **940** (~1,7 T) stark, aber six-q-genius-flags nur **165** (~0,9 T) und vs-colder-1 **72** (~0,7 T) – beide weit unter 24-h-Median ~436. E12 bleibt offen (2/4 drüber); Verdict nach den 12.11.-/13.11.-Paaren. atlas bleibt (Besitzer-Regel 09.11.), Themen strikt auf die bewiesenen Gewinner (Geo-Mix, Bevölkerung, Karten).
- **E13 Longs 2.0 läuft gut:** Karten-Long True Size **84 öffentliche Views n. ~2 T** (Text-Longs 4–13) → Folge 2 Di 17.11. bleibt.
- **Verdicts ≥~3 T:** VS Heavier **388** ✗ (Ziel 700), Berlin-Wall-6-Q **229** ✗ (E10: Jahrestage raus aus 16:00), Flag-30-Long **13** ✗.
- **Konkurrenz:** Rätsel-Longs explodieren weiter – neu „15 Mystery Riddles That Will Test Your IQ 99% Fail“ (Can You Solve?, **517k, 106k/Tag**) neben Quiz World 519k (277×) → E14 Rätsel-Long Do 19.11. bestätigt, Titel mit Zahl + „Riddles“ + IQ.
- **Neu für So 15.11.:** World-Geography-6-Q 16:00 + Länder-Größe-VS 21:00 (Titel ohne „Round 2“, das floppte mit 158).

## Konkurrenz-Gewinner heute (competitors.md + outliers.md 12.11., letzte 30 Tage)

| # | Video (Kanal, Abos) | Views | × Median | Länge | Titel-Muster | Was wir übernehmen → Slot |
|---|---|---|---|---|---|---|
| 1 | "10 Tricky IQ Riddles / Test Your Intelligence!" (Quiz World, 1.080) – 22.10. | 519.490 | 277× | 6:48 | Zahl + „Tricky“ + IQ, ohne Emoji | Länge ~7 min, 10–12 sichtbare Rätsel → **Do 19.11. Long E14** |
| 2 | "15 Mystery Riddles That Will Test Your IQ 99% Fail🧠🔥" (Can You Solve?, 5.210) – Okt. | 516.612 (106k/Tag) | 99× Abos | 8:44 | Zahl + Riddles + IQ + „99% Fail“ + 2 Emojis | Titelmechanik für E14: „12 Tricky IQ Riddles – Only Geniuses Solve 4 🧠“; Rätsel als cardText |
| 3 | "You're Not Smart Enough to Solve These 12 Puzzles!" (Quiz Guy, 493) – 15.10. | 85.042 | 73× | 8:15 | Provokation („Not Smart Enough“) + 12 | Backlog #6: Titel-Variante für E14-Folge 2, wenn #1 ≥50 Views |
| 4 | "Name a European city that starts with..." (Chauncey Asks, 5.690) – Short 15.10. | 945.812 | 20× | 1:55 | Europa-Geo, offene Frage | Europa-Geo-6-Q **heute 16:00** (Queue) + World-Geo-6-Q **15.11. 16:00** |
| 5 | "Can You Pass This Thanksgiving Trivia Quiz? 🦃 45 Questions for Adults" (Still Sharp Trivia, 337) | 43.699 | 87× Abos | 21:47 | Event + „Can You Pass“ | Thanksgiving 26.11.: Emoji-Long „Guess the Thanksgiving Food by Emoji“ (Do 26.11.) – visuell statt 45 Text-Fragen |

Nicht übernommen: WWII-50-Fragen (Passmark 171k – Krieg verboten), Senioren-/Alters-Titel (QuizNova, QuizVerse), F1-Google-Earth (Satellitenbilder), Disney/Anime/YouTuber-Stimmen (Rechte), Math-Quiz-Wort-Shorts (Wortschatz bei uns 144 ✗).

## 3-Tage-Plan

Layout: **Shorts = atlas** (Besitzer-STRATEGIE 09.11. ist neuer als „tvshow für alles“ im Agenten-Prompt), **Longs = tvshow mit Thumbnails v2 bzw. TrueSizeLong**. Longs nur Di/Do/Sa. Fakten vor dem Schreiben prüfen, gegen `queue/done/*` greppen.

| Datum / Slot | Format | Thema | Arbeitstitel (YouTube) | Fragen + timing | Hook / Frage 1 | Musik | cardColors | Thumbnail A/B/C + Foto | Warum | Erfolgskriterium |
|---|---|---|---|---|---|---|---|---|---|---|
| 13.11. Long | **kein Long** (Fr) | – | – | – | – | – | – | – | Longs nur Di/Do/Sa | – |
| 13.11. Short 16:00 | 6-Q atlas (Queue six-q-genius-europe) | Europa | Only Geniuses Get 6/6 🧠 Europe Quiz | 6 (Queue) | Queue (Donau …) | game-show | – | – | Exploit Geo-6-Q (Capitals 1.061) + Konkurrenz #4 | ≥800 n. 3 T |
| 13.11. Short 21:00 | VS atlas (Queue vs-more-people-3) | Bevölkerung R3 | Which Country Has More People? Round 3 – 90% Fail 👥 | 4 (Queue) | Queue | world-trip | – | – | Exploit bestes VS (1.188 / 1.080) | ≥800 n. 3 T |
| 14.11. Long 14:00 | Emoji-Long QuizLong tvshow v2 (Queue country-emoji-30-1) | Länder per Emoji | Guess the Country by Emoji: 30 Rounds From Easy to Legend 🌍 | 30 (Queue) | Queue | world-trip | petrol | v2: A "GUESS THE COUNTRY" + thumbPuzzle 🌋+♨️+🐋 / B "CAN YOU GET 25/30?" / C "ONLY 1% GET 30/30" | E13 #3; Autocomplete „country guess the country“ 4,2 | E13: ≥30 n. 3 T |
| 14.11. Short 16:00 | 6-Q atlas (Queue six-q-genius-animals) | Tiere | Only Geniuses Get 6/6 🧠 Animal Quiz | 6 (Queue) | Queue | game-show | – | – | **Experiment Thema Tiere** (Quiz Dolphy 177k) | ≥600 n. 3 T; <400 → Tiere raus aus 6-Q |
| 14.11. Short 21:00 | Karten-VS atlas truesize (Queue map-lie-2), Paar zum Country-Long | Wahre Größe #2 | This Map Is Lying To You #2 🌍 Which Is REALLY Bigger? | 4 (Queue) | Queue (UK/Italien …) | world-trip | – | fest | Exploit Karten-VS (940) | ≥800 n. 3 T |
| 15.11. Long | **kein Long** (So) | – | – | – | – | – | – | – | – | – |
| **15.11. Short 16:00 (NEU)** | 6-Q atlas | Welt-Geografie | **Only Geniuses Get 6/6 🧠 World Geography Quiz** (+ #shorts) | 6, count 2.5 / tail 0.8, 4 Optionen, Antworten ≤3 Wörter, ≤50 s | Q1 "Which river flows through London?" (Thames/Seine/Rhine/Danube) → Thames · Q2 "Which country is a long thin strip on South America's west coast?" (Chile/Peru/Argentina/Ecuador) → Chile · Q3 "Which imaginary line runs through Greenwich, London?" (Prime Meridian/Equator/Tropic of Cancer/Date Line) → Prime Meridian · **#4 Falle "Which country has the most time zones?" (Russia/USA/France/China) → France (12, dank Überseegebieten; Russland 11)** · Q5 "What is the tallest waterfall in the world?" (Angel Falls/Niagara Falls/Victoria Falls/Iguazu Falls) → Angel Falls · Finale "Which country has the most islands?" (Sweden/Japan/Indonesia/Philippines) → Sweden (~267.000) | game-show | – (atlas) | – ; broll: Q1 "river city bridge", Q2 "Andes mountains", Q3 "old observatory telescope", Q4 "world clocks", Q5 "jungle waterfall", Q6 "archipelago sea aerial" (keine Antwort verraten) | **Exploit** Geo-6-Q (Capitals 1.061, Quick Geo 994, Tricky 1.045) | ≥800 n. 3 T |
| **15.11. Short 21:00 (NEU)** | VS atlas CompareScene (Muster queue/done/2026-10-31-vs-countries-bigger-1.json) | Ländergröße | **Which Country Is Bigger? 90% Get #4 Wrong 🌍** (+ #shorts) – kein „Round 2“ | 4 Runden, timing count 3.0 / tail 1.2 | R1 **Libya 1.759.540** vs Iran 1.648.195 → Libya · R2 Egypt 1.001.450 vs **Bolivia 1.098.581** → Bolivia · R3 **South Africa 1.219.090** vs Colombia 1.138.910 → South Africa · **Finale-Falle: Argentina 2.780.400 vs India 3.287.263 → India** (Argentinien wirkt auf Karten riesig). CIA World Factbook km², Quelle in Beschreibung; Flaggenfotos aus image-credits.json, sonst Icons; Gewinnerseite a/b/b/b → R3 auf b drehen (Colombia vs South Africa) | world-trip | – | – (Short) | **Exploit** VS (Bigger 862, Karten-VS 940, People 1.080); neue Paare (Iran/Mongolei schon benutzt) | ≥700 n. 3 T |

Vorschau (nicht anlegen): Mo 16.11. 6-Q Capitals #2 „Only Geniuses Get 6/6 🧠 Capital Cities Quiz #2“? → **nein, Sequel-Titel tot**; stattdessen „Only Geniuses Get 6/6 🧠 Country Quiz“ + VS „Which Is Older?“ je nach Verdict · **Di 17.11.** Karten-Long Folge 2 „The True Size of US States vs Countries“ + Karten-VS #3 21:00 · **Do 19.11.** Long = **E14 Rätsel-Long** + GTA-6-Q 16:00 (GTA VI 19.11. laut Take-Two weiter fix).

Bandit 13.–15.11.: Exploit 7 (Europe-6-Q, People-VS R3, Country-Long, Karten-VS #2, World-Geo-6-Q, Bigger-VS, + E13) / Experiment 1 (Animal-6-Q) + E12 atlas läuft im Hintergrund ≈ 75/25.

## Ideen-Backlog (nach erwartetem Potenzial)
1. **E14 Do 19.11. 14:00 – Rätsel-Long (erlaubtes 7-Min-Experiment): „12 Tricky IQ Riddles – Only Geniuses Solve 4 🧠 7-Minute Test“** – 12 eigene Rätsel als cardText (Zahlenfolgen, Uhr-/Kalender-Logik, Wort-Logik), count 20 s, EASY→LEGEND, game-show, Thumb v2 A "12 TRICKY RIDDLES" + thumbPuzzle "2 · 6 · 12 · 20 · ?" / B "CAN YOU SOLVE 4?" / C "ONLY 1% SOLVE #12". Evidenz: Quiz World 519k (277×), Can You Solve? 517k (106k/Tag), Quiz Guy 85k. Erfolg: ≥50 Views n. 3 T. **Anlegen am 17.11.**
2. **GTA VI 19.11.: 6-Q „Only Real Fans Get 6/6 🎮 GTA Quiz“ 16:00** – größte Gaming-Suchspitze des Jahres; nur Textfakten (Vice City = Miami, GTA V 2013), keine Spielbilder/Logos/Gewaltfragen.
3. **Karten-Long Folge 2 Di 17.11.: „The True Size of US States vs Countries“** – Folge 1 84 Views n. 2 T (bestes Long seit Okt.).
4. **Thanksgiving Do 26.11.: Long „Guess the Thanksgiving Food by Emoji 🦃“ + 6-Q 21:00** – Trends „thanksgiving trivia“ +350 %, Still Sharp 44k bei 337 Abos.
5. **Hunger Games: Sunrise on the Reaping (Kinostart 20.11.): 6-Q „Only Real Fans Get 6/6 🏹 Hunger Games Quiz“** – nur Buchfakten, keine Stills.
6. **Math-Rätsel-Long „Can You Pass This Math Quiz? Easy to Impossible“** – CandyQuiz 377k (105×); erst nach E14-Verdict, gleiche Rätsel-Mechanik.
7. **Long „Guess the Word by Emoji – USA Edition“** – Again Quiz 437k, Kids Quizzy 752k; Emoji-Wort-Long hatte 141 (bestes frühes Long) – nach E13-Verdict 21.11.
8. **VS „Which US State Has More People?“** – Bevölkerungs-VS ist bestes VS-Muster, US = 60 % Publikum.
9. **6-Q-Titeltest „You're Not Smart Enough to Get 6/6 🧠 …“** – Quiz Guy 85k/41k/38k; eine Variable gegen „Only Geniuses“.
10. **Long „Guess the Animal by Emoji: 30 Rounds“** – Trends „guess the animal challenge“ +130 %; nur wenn Animal-6-Q (14.11.) ≥600.

Gestrichen: Weltraum, Wissenschaft, Wortschatz, Bauwerkshöhen, Gewicht-VS (388 ✗), Jahrestage im 16:00-Slot (Berlin Wall 229 ✗), Krieg/Sprengstoff, Halloween/Grusel, Alters-Titel, 50-Fragen-Text-Longs, „Round 2“-Sequeltitel bei 6-Q.

## Für den Produktions-Agenten (gilt heute, überschreibt ältere Defaults)
- **Heute produzieren (Fr, kein Long-Tag):** six-q-genius-europe 16:00 + vs-more-people-3 21:00 (beide in Queue). country-emoji-30-1 wartet auf Sa.
- **Für 15.11. anlegen:** `2026-11-15-six-q-genius-world-geo.json` (publishAt "16:00", atlas, game-show, count 2.5/tail 0.8) und `2026-11-15-vs-countries-bigger-2.json` (publishAt "21:00", atlas CompareScene, world-trip, Muster vs-countries-bigger-1) exakt wie in der Tabelle. Duplikat-Check: Kilimanjaro, Baikal, Kairo, trockenster Kontinent, Japans Inseln, Iran/Mongolei sind schon benutzt (deshalb nicht im Plan). Falls Thames/Chile in done als **Frage** (nicht nur Option) vorkommen → ersetzen durch „Which is the largest country in Africa?“ (Algeria/DR Congo/Sudan/Libya) → Algeria (2.381.741 km²).
- Titel-Regel: keine „Round 2/#2“-Titel bei 6-Q (Which-First R2 158 ✗); bei VS ok nur mit Nummer am Ende (map-lie-2).
- Nach dem heutigen Snapshot: 24-h-Werte von six-q-genius-movies und vs-older-1 und die ≥3-T-Werte von tricky/map-lie-1 in experiments.md eintragen. **E12-Regel:** wenn von den 6 atlas-Shorts 10.–12.11. höchstens 2 über dem 24-h-Median (~436) liegen → als TECHNIK/STRATEGIE-Hinweis in learnings.md notieren (Besitzer entscheidet über Look, nicht wir).
- Scoreboard-Gruppierung: TrueSize-Videos als Format „Karten“ / Layout „atlas“ führen (siehe TECHNIK-PROBLEM 2), wenn ohne Risiko machbar.
- Weiter: kein Weltraum, Halloween/Grusel, Politik, Krieg/Waffen, 💥, Alters-Titel; keine Longs an Mo/Mi/Fr/So.
- **NEU 13.11. 20:15 – E15 Retention (Besitzer-Auftrag):** Bei allen NEUEN 6-Fragen-Shorts ab 16.11. ist `lines[0].a` nur die Antwort mit Ausrufezeichen (1–3 Wörter, kein Fakt-Satz); Fragen 2–6 unverändert. six-q-genius-world-geo (15.11.) ist schon umgestellt. VS-/Karten-Shorts NICHT ändern (Kontrollgruppe). Nach jedem Snapshot in experiments.md eintragen: Kurvenwert 1,5 s nach Start Q2 ÷ Kurvenwert bei Auflösung Q1 (Ziel ≥ 0,75, Basis 0,62) und Ø angesehen.

