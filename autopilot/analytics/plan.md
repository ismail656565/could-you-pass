# Plan – 2026-11-15 (So)

TECHNIK-PROBLEM: nichts Blockierendes. Läufe 14.11. grün (country-emoji-30-1 14:00, six-q-genius-animals 16:00, map-lie-2 21:00 hochgeladen, alle 3 Kommentare gepostet 13:56/15:57/20:58). Hinweise: (1) **Analytics-Snapshot ist vom 14.11. 11:31** – alle 14.11.-Videos dort noch privat, Europe/People-R3 erst <1 T alt → heutiger 08:15-Lauf muss frischen Snapshot ziehen (für E15/Animals/Map-Lie-2-Verdicts). (2) QA-Warnung „Standbild 9,4 s“ beim Country-Emoji-Long (14.11.) – vermutlich Abspann/Endkarte (wie Karten-Long 11,6 s), bitte kurz prüfen, ob es nicht mitten im Video liegt. (3) CTR per API weiter HttpError 400 (bekannt). (4) Am 16.11. erstes pop-Item → Log auf „Gerendert“ für six-q-genius-country-pop prüfen (lokal wegen Font-Download nicht testbar).

## Zusammenfassung (Deutsch)
- **Shorts-Delle seit 11.11.:** Snapshot 14.11.: flags 303 (≈2,8 T), colder 147 (≈2,6 T), older 178 (≈2 T), movies 362 (≈1,6 T), **Europe 84 (≈0,85 T), People-R3 98 (≈0,6 T)** – sogar das bewährte Bevölkerungs-VS (R1/R2 1.089/1.189) startet schwach. Alle seit 11.11. in atlas → Layout-Verdacht (E16 ab morgen) bleibt der wichtigste Test; Themen-Exploit (Geo/Länder) unverändert.
- **Verdicts ≥3 T:** flags 303 ✗ (Ziel 800), colder 147 ✗ (Kälte-VS bereits gestrichen). Tricky 1.541 / map-lie-1 1.021 (≈4 T) bleiben die einzigen atlas-Gewinner.
- **Longs (E13):** Karten-Long True Size **133** (≈4 T, stayed 75,6 %) = mit Abstand bestes Long seit Okt.; Movie-Emoji **14** (≈1,9 T) ✗-Kurs. → Karten-Long Folge 2 (US-Staaten vs. Länder) Di 17.11. ist der stärkste Long-Slot; Emoji-Longs hängen am Country-Emoji-Wert (14.11.).
- **Konkurrenz:** unverändert dominieren ~7-min-IQ/Rätsel-Longs (Quiz World 520k = 277× Median, GK Studio 45k = 48×, Quiz Guy 38k = 33×) und Erkennungs-Longs „from above/outline“ als Serie (Dopamine Quiz F1 Part 3, 30k = 42×). GTA VI bleibt 19.11. (mehrfach bestätigt).
- **Änderung heute:** keine Regeländerung; Produktion legt 17.11. an (Karten-Long Folge 2 + E16 Tag 2: atlas 16:00 / pop 21:00 USA-Quiz gepaart zum Long).

## Konkurrenz-Gewinner heute (competitors-report.json 14.11., letzte 30 Tage)

| # | Video (Kanal, Abos) | Views | × Median | Länge | Titel-Muster | Was wir übernehmen → Slot |
|---|---|---|---|---|---|---|
| 1 | "10 Tricky IQ Riddles / Test Your Intelligence!" (Quiz World, 1.080) – 22.10. | 519.769 | 277× | 6:48 | Zahl + „Tricky“ + IQ, kein Emoji, kein Score | **E14 Do 19.11. Long** (~7 min, 12 sichtbare Rätsel) |
| 2 | "🧠 Your Brain Is Ageless! Take This 10-Question IQ Quiz…" (GK STUDIO PRO, 1.910) – 27.10. | 45.130 | 48× | 7:14 | Fragenzahl + IQ + Selbstbild | Bestätigt Länge 7 min + 10–12 Fragen für E14; Alters-Teil NICHT (Besitzer-Verbot) |
| 3 | "Can You Name F1 Track From Above? — Part 3" (Dopamine Quiz, 441) – 31.10. | 30.059 | 42× | 8:50 | Erkennen aus Vogelperspektive + **Serien-Nummer** | **Di 17.11. Karten-Long Folge 2** als klare Serie („Maps That Lie #2“-Logik, Suchphrase vorn) |
| 4 | "12 Puzzles That Expose How Easily You Get Tricked!" (Quiz Guy, 494) – 18.10. | 37.829 | 33× | 8:22 | Zahl + „Puzzles“ + Ego-Drohung, kein Emoji | E14-Titel-Alternative / Thumb B; Rätsel als echte Puzzles (Zahlenreihen, Logik), keine Textfakten |
| 5 | "Name the airline from its livery" (Chauncey Asks, 6.150) – Short 20.10. (+ „Name the artist by the album cover“ 454k, 04.11.) | 767.146 | 16× | 1:17 | „Name the X from its Y“ – Erkennen aus Detail | Nach E16: 6-Q-Short „Name the Country From Its Outline“ mit truesize-Umrissen (Backlog #4); keine Logos/Albumcover (Rechte) |

Nicht übernommen: Alters-/Senioren-Titel (QuizNova 72k/57k – Besitzer-Verbot), Gabby's Dollhouse/Disney-Stimmen (Rechte), Fußballstadien/F1 per Google Earth (Satellitenbilder lizenzpflichtig), „English Quizz“-Wortschatz-Shorts (bei uns 148 ✗), WWII (Krieg).

## 3-Tage-Plan

Layout: Shorts 15.11. atlas (Queue), **16.–22.11. E16 pop/atlas** (gerade Tage pop 16:00, ungerade pop 21:00); Longs tvshow v2 bzw. TrueSizeLong (Besitzer-STRATEGIE 09./13.11. ist neuer als „tvshow für alles“). Longs nur Di/Do/Sa 14:00. Alle Fragen vor dem Anlegen gegen `queue/done/*` greppen (für 17.11. schon gegrept, s. u.).

| Datum / Slot | Format | Thema | Arbeitstitel (YouTube) | Fragen + timing | Hook / Fragen | Musik | cardColors | Thumbnail A/B/C + Foto | Warum | Erfolgskriterium |
|---|---|---|---|---|---|---|---|---|---|---|
| 15.11. Long | kein Long (So) | – | – | – | – | – | – | – | Long-Tage Di/Do/Sa | – |
| 15.11. Short 16:00 | 6-Q atlas (Queue six-q-genius-world-geo) | Welt-Geo | Only Geniuses Get 6/6 🧠 World Geography Quiz | 6 (Queue), E15 #1 | Queue | game-show | – | – | Exploit Geo-6-Q + E15 | ≥800 n. 3 T; E15-Kurvenquote ≥0,75 |
| 15.11. Short 21:00 | VS atlas (Queue vs-countries-bigger-2) | Ländergröße | Which Country Is Bigger? 90% Get #4 Wrong 🌍 | 4 (Queue) | Queue | world-trip | – | – | Exploit VS (letztes VS vor E16) | ≥700 n. 3 T |
| 16.11. Long | kein Long (Mo) | – | – | – | – | – | – | – | – | – |
| 16.11. Short 16:00 | 6-Q **pop** (Queue six-q-genius-country-pop) | Länder | Only Geniuses Get 6/6 🧠 Country Quiz | 6 (Queue), E15 | Queue | game-show | – (pop) | – | E16 Paar 1 pop | E16 + ≥600 n. 3 T |
| 16.11. Short 21:00 | 6-Q **atlas** (Queue six-q-genius-landmarks) | Wahrzeichen | Only Geniuses Get 6/6 🧠 Landmarks Quiz | 6 (Queue), E15 | Queue | game-show | – | – | E16 Paar 1 atlas | E16 + ≥600 n. 3 T |
| **17.11. Long 14:00 (NEU)** | **Karten-Long TrueSizeLong** (story.type "truesize", format "long"), Folge 2 | Wahre Größe: US-Staaten vs. Länder | **The True Size of US States: 20 Maps That Lie to You 🇺🇸** | 20 Runden, EASY→MEDIUM→HARD→LEGEND je 5, `timing {think 3.4, move 1.7, tail 1.0}`, `midCtaIndex` 10 | Runden s. Liste „Karten-Long Folge 2“ unten (Hook R1: „California vs Japan – which is REALLY bigger?“) | world-trip | – | festes TrueSizeThumb; `story.thumbText` = "ALASKA IS A LIE" | **Exploit #1 Long** (Folge 1: 133 Views, stayed 75,6 % – alle anderen Longs ≤21 seit 23.10.) + Konkurrenz #3 (Serie) + US-Publikum | ≥100 n. 3 T (Folge 1: 101) |
| **17.11. Short 16:00 (NEU, E16 atlas)** | 6-Q **layout "atlas"** | Welt-Geo (Wasserfälle/Seen/Hauptstadt) | **Only Geniuses Get 6/6 🧠 Geography Quiz** (+ #shorts) | 6, count 2.5 / tail 0.8, E15 (`lines[0].a` = „Zimbabwe!“) | Q1 "Victoria Falls lies on the border of Zambia and…?" (Kenya/Zimbabwe/Tanzania/Angola) → Zimbabwe · Q2 "The island of Tasmania belongs to which country?" (New Zealand/Australia/UK/Indonesia) → Australia · Q3 "Lake Titicaca lies between Peru and…?" (Chile/Ecuador/Bolivia/Brazil) → Bolivia · **#4 Falle "What is the capital of Turkey?" (Istanbul/Ankara/Izmir/Antalya) → Ankara** · Q5 "The Iguazu Falls are shared by Argentina and…?" (Chile/Brazil/Uruguay/Paraguay) → Brazil · Finale "The Bering Strait separates Russia from which US state?" (Washington/Hawaii/Maine/Alaska) → Alaska | game-show | – (atlas) | – ; broll: Q1 "waterfall mist rainbow", Q2 "eucalyptus forest coast", Q3 "reed boats lake", Q4 "mosque minaret city", Q5 "jungle waterfall aerial", Q6 "icy sea ship" | **E16 Tag 2 atlas** (ungerader Tag → atlas 16:00) | E16 + ≥600 n. 3 T |
| **17.11. Short 21:00 (NEU, E16 pop, gepaart zum Long)** | 6-Q **layout "pop"** | USA | **Only Geniuses Get 6/6 🧠 USA Quiz** (+ #shorts) | 6, count 2.5 / tail 0.8, E15 (`lines[0].a` = „Arizona!“) | Q1 "Which US state is home to the Grand Canyon?" (Nevada/Utah/Arizona/Colorado) → Arizona · Q2 "Las Vegas is in which US state?" (California/Nevada/Arizona/Utah) → Nevada · Q3 "What is the capital of Texas?" (Houston/Dallas/Austin/San Antonio) → Austin · **#4 Falle "What is the capital of New York State?" (New York City/Buffalo/Albany/Rochester) → Albany** · Q5 "Most of Yellowstone National Park lies in which state?" (Montana/Wyoming/Idaho/Colorado) → Wyoming (~96 %) · Finale "Which US state has the longest coastline?" (California/Florida/Hawaii/Alaska) → Alaska (NOAA: 6.640 mi, mehr als alle anderen Staaten zusammen) | game-show | **nicht setzen** (pop) | – ; broll Q1 "red rock canyon river", Q2 "desert city night lights", Q3 "cowboy boots", Q4 "skyscrapers taxi street", Q5 "geyser steam", Q6 "glacier coast boat"; cardText Q1 "🏜️", Q2 "🎰", Q3 "🤠", Q4 "🗽", Q5 "♨️🦬", Q6 "🌊" | **E16 Tag 2 pop** + Paarung Short→Long (Kommentar verlinkt Karten-Long) | E16 + ≥600 n. 3 T |

Duplikat-Check 17.11. erledigt (grep queue/done): frei = Victoria Falls, Tasmania, Titicaca, Ankara, Iguazu, Bering, Grand Canyon, Las Vegas, Austin, Albany, Yellowstone; „longest coastline“ nur als Länder-Frage (Kanada, 23.10.) benutzt → Staaten-Variante ok. Schon benutzt (nicht nehmen): Sunshine State, Big Apple, Golden Gate, Hawaii-Inseln, Rhode Island, Peach State, Mississippi/Missouri, Death Valley, Alaska-Kauf, Everest, Ottawa, Canberra, Sahara, Seine, Fuji. Rushmore läuft am 16.11.

### Karten-Long Folge 2 – 20 Runden (offizielle Gesamtfläche: US Census Bureau für Staaten, CIA World Factbook für Länder; Quelle in die Beschreibung)

| # | Stufe | a vs. b | km² | Gewinner | Diff |
|---|---|---|---|---|---|
| 1 | EASY | California vs Japan | 423.970 / 377.915 | California | 12 % |
| 2 | EASY | Texas vs France (Festland, Shape `france`) | 695.662 / 551.500 | Texas | 26 % |
| 3 | EASY | Spain vs California | 505.370 / 423.970 | Spain | 19 % |
| 4 | EASY | DR Congo vs Alaska | 2.344.858 / 1.723.337 | Congo | 36 % |
| 5 | EASY | Turkey vs Texas | 783.562 / 695.662 | Turkey | 13 % |
| 6 | MEDIUM | Florida vs Syria | 170.312 / 185.180 | Syria | 9 % |
| 7 | MEDIUM | UK vs Minnesota | 243.610 / 225.163 | UK | 8 % |
| 8 | MEDIUM | Italy vs Colorado | 301.340 / 269.601 | Italy | 12 % |
| 9 | MEDIUM | Romania vs Utah | 238.391 / 219.882 | Romania | 8 % |
| 10 | MEDIUM | Chile vs Texas | 756.102 / 695.662 | Chile | 9 % |
| 11 | HARD | Poland vs Nevada | 312.685 / 286.380 | Poland | 9 % |
| 12 | HARD | Cambodia vs Florida | 181.035 / 170.312 | Cambodia | 6 % |
| 13 | HARD | Montana vs Germany | 380.832 / 357.022 | Montana | 7 % |
| 14 | HARD | Greenland vs Alaska | 2.166.086 / 1.723.337 | Greenland | 26 % |
| 15 | HARD | Sweden vs California | 450.295 / 423.970 | Sweden | 6 % |
| 16 | LEGEND | Iceland vs Pennsylvania | 103.000 / 119.280 | Pennsylvania | 16 % |
| 17 | LEGEND | Norway (Festland, ohne Svalbard) vs Montana | 323.802 / 380.832 | Montana | 18 % |
| 18 | LEGEND | India vs Alaska | 3.287.263 / 1.723.337 | India | 91 % (Mercator-Falle: Alaska wirkt größer) |
| 19 | LEGEND | Cuba vs Pennsylvania | 109.884 / 119.280 | Pennsylvania | 9 % (Kuba wirkt länger/größer) |
| 20 | LEGEND (Finale) | Kazakhstan vs Alaska | 2.724.900 / 1.723.337 | Kazakhstan | 58 % (Alaska sieht auf der Karte riesig aus) |

- **Neue Formen** in scripts/build-truesize-data.mjs: Staaten über `stateByName` (California, Florida, Minnesota, Colorado, Utah, Nevada, Montana, Pennsylvania), Länder über `byName` (Turkey, Syria, Romania, Chile [clip Festland ohne Osterinsel], Cambodia, Poland, Norway [clip ca. [4, 57, 32, 72] ohne Svalbard/Jan Mayen]). Skript laufen lassen, truesize.json committen.
- **Kontrollspalte prüfen** (Lehre Alaska-Landfläche 1,49 Mio.): Wenn die berechnete Formfläche eines Paars den Gewinner umdreht oder <5 % Abstand zeigt (Kandidaten: Florida 17,9 % Wasser, Minnesota, Alaska), Paar durch eine Reserve ersetzen: **Madagascar vs Texas** 587.041/695.662 (Texas 18 %) oder **Utah vs UK** 219.882/243.610 (UK 11 %). NICHT nehmen (zu knapp/Land≠Gesamt): Colorado/New Zealand, Montana/Japan, Alaska/Mongolia, New York/North Korea, Hawaii/Israel.
- mover = polnahe Seite; Gewinnerseite a/b mischen (nicht immer a). Wiederholungen aus Folge 1: Greenland/Alaska-Paar ist neu, nur Einzelformen wiederholt → Regel „max. 5 Wiederholungen“ eingehalten.
- Beschreibung: Suchphrasen „true size of US states“, „US states compared to countries“, „mercator projection“, Kapitel automatisch.

Bandit 15.–17.11.: Exploit 6 (World-Geo, Bigger-VS, Karten-Long, Geo/Länder-Themen in allen E16-Slots, USA-Paarung) / Experiment 3 (E15, E16-Layout ×2 Tage) ≈ 67/33.

## Ideen-Backlog (nach erwartetem Potenzial)
1. **E14 Do 19.11. Long (am 17.11. anlegen): „12 Tricky IQ Riddles – Only Geniuses Solve 4 🧠“** – 12 eigene Rätsel als cardText (Zahlenreihen, Uhr-/Wochentag-Logik, Wortlogik), count 20 s, ~7 min, Thumb v2 A "12 TRICKY RIDDLES" + Rätsel „2 · 6 · 12 · 20 · ?“ / B "CAN YOU SOLVE 4?" / C "ONLY 1% SOLVE #12". Evidenz: Quiz World 520k (277×), Quiz Guy 38k/85k, GK Studio 45k. Erfolg ≥50 n. 3 T.
2. **GTA VI 19.11. (Rockstar/Take-Two bestätigt): „Only Real Fans Get 6/6 🎮 GTA Quiz“ als 3. Short 10:00** außerhalb E16 – reine Textfakten (Vice City ↔ Miami, GTA V 2013, Staat Leonida, Protagonisten Lucia & Jason), keine Spielbilder/Logos/Gewalt; broll neutral ("miami beach palm trees"). Suchspitze der Woche.
3. **Hunger Games: Sunrise on the Reaping (Kinostart 20.11.)**: „Only Real Fans Get 6/6 🏹 Hunger Games Quiz“ als 3. Short 20.11. 10:00 – nur Buchfakten, keine Filmbilder.
4. **Short „Name the Country From Its Outline“** (6-Q, Umriss aus truesize.json als Bild) – Chauncey-Muster (airline 767k, album 454k); braucht Code-Hook (q["shape"]) → nach E16-Verdict 25.11.
5. **Karten-VS #3 Di 24.11. 21:00 „This Map Is Lying To You #3 🇺🇸“** mit den Reserve-Paaren aus Folge 2 – map-lie-1 1.021 (Ø angesehen 81 %).
6. **Thanksgiving Do 26.11. Long „Thanksgiving Trivia Quiz 🦃 Can You Get 10/15?“** (7-min-Format mit sichtbaren Bildern) – Trends „thanksgiving trivia“ +350 %, Still Sharp 44k bei 337 Abos.
7. **Math-Rätsel-Long „Can You Pass This Math Quiz? Easy to Impossible“** – CandyQuiz 377k; nach E14-Verdict.
8. **6-Q-Titeltest „Are You Smarter Than a 5th Grader? 🧠 6 Questions“** – Studio Seven „Smarter Than a 12 Year Old?“ 62,5k (10.11.); nach E16 (sonst 2 Variablen).
9. **VS „Which US State Has More People?“** – bestes VS-Muster (1.089/1.189) mit US-Bezug, ab 24.11.
10. **Long „Guess the Word by Emoji – USA Edition“** – Again Quiz 437k, Kids Quizzy 752k; nur wenn Country-Emoji-Long ≥30 n. 3 T (E13-Verdict 21.11.).

Gestrichen: Weltraum, Wissenschaft, Wortschatz, Bauwerkshöhen, Gewicht-/Kälte-/Alter-VS, Flaggen-6-Q (303 ✗), Jahrestage im 16:00-Slot, Krieg/Sprengstoff, Halloween, Alters-Titel, 50-Fragen-Text-Longs, „Round 2“-Titel bei 6-Q.

## Für den Produktions-Agenten (gilt heute, überschreibt ältere Defaults)
- **Heute produzieren (So, kein Long-Tag):** six-q-genius-world-geo 16:00, vs-countries-bigger-2 21:00 (beide in Queue).
- **Für 17.11. anlegen (Di = Long-Tag, E16 Tag 2, ungerader Tag → pop = 21:00):**
  - `2026-11-17-map-true-size-us-20-2.json` (format "long", publishAt "14:00", story.type "truesize", Muster queue/done/2026-11-10-map-true-size-20-1.json; 20 Runden aus der Liste oben, `story.thumbText` "ALASKA IS A LIE", Musik world-trip). Vorher neue Formen bauen + Kontrollspalte prüfen (s. o.).
  - `2026-11-17-six-q-genius-geography.json` (publishAt "16:00", `layout: "atlas"`, game-show, count 2.5/tail 0.8, `broll` je Frage, E15).
  - `2026-11-17-six-q-genius-usa-pop.json` (publishAt "21:00", `layout: "pop"`, game-show, count 2.5/tail 0.8, `broll` + `cardText` je Frage, kein `cardColors`, E15). Antwortpositionen mischen (Optionen im Plan haben die richtige Antwort oft an Index 1/2 und im Finale an 3 → so umsortieren, dass alle 4 Positionen vorkommen).
- **Vor dem Anlegen:** frischen Analytics-Snapshot ziehen; 24-h-Werte six-q-genius-animals, map-lie-2, country-emoji-30-1 und ≥3-T-Werte europe/people-R3/movies/older in experiments.md eintragen.
- **Keine VS-Shorts 16.–22.11.** (außer Karten-Long), kein VS mit pop, keine Longs Mo/Mi/Fr/So. Weiter verboten: Weltraum, Halloween, Politik, Krieg/Waffen, 💥, Alters-Titel.
