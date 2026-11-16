# Plan – 2026-11-16 (Mo)

TECHNIK-PROBLEM: nichts Blockierendes. Läufe 15.11. grün (six-q-genius-world-geo 16:00, vs-countries-bigger-2 21:00 hochgeladen, Kommentare 15:57/20:58 gepostet; kein Long-Tag). Hinweise: (1) **Analytics-Snapshot ist vom 15.11. 11:33** – beide 15.11.-Videos dort noch privat → heutiger 08:15-Lauf muss frischen Snapshot ziehen. (2) **Heute erstes pop-Item (six-q-genius-country-pop, 16:00)** – im Log auf „Gerendert“ + QA-Zeile prüfen; scheitert pop (Font/Komposition), Item mit `layout: "atlas"` neu rendern statt Slot ausfallen lassen und in learnings.md notieren (dann ist E16-Paar 1 ungültig). (3) **keywords.md ist vom 09.11.** – Montags-Refresh (keywords.py) heute prüfen, ob er läuft. (4) vidIQ: Konto hat erst **4 Credits** (Tools kosten 5) → heute kein vidIQ-Aufruf möglich; nicht erneut versuchen, bis die Credits aufgefüllt sind. (5) CTR per API weiter HttpError 400 (bekannt).

## Zusammenfassung (Deutsch)
- **Karten-Format bleibt unser bester Hebel:** map-lie-2 **341 Views nach ≈0,6 T** (map-lie-1 lag nach ~11 h bei 931, Ziel 800) – Karten-VS startet wieder über allen anderen Shorts der Woche; Karten-Long #1 131 (≈4,9 T) bleibt das einzige Long >30. Morgen Karten-Long Folge 2 (US-Staaten).
- **Shorts-Delle hält an:** Median der letzten 14 Shorts mit ≥3 T = **280** (Gesamt-Median 366). Verdicts: **older-VS 191 (2,9 T) ✗**, **Movie-6-Q 409 (2,6 T) ✗** (Ziel 600 → Filme nur noch als Long/Event), Europe 152 (1,9 T), People-R3 163 (1,6 T), Animals 108 (0,9 T) alle schwach → E16 (pop vs. atlas, ab heute) ist richtig gesetzt.
- **Longs:** Movie-Emoji-Long **18 (2,9 T) ✗** (Ziel 30), Country-Emoji 13 nach 0,9 T (besser als Movie bei 0,9 T: 4) → E13-Verdict 21.11. hängt an Karten-Long Folge 2 + Country-Emoji.
- **Konkurrenz:** unverändert IQ-/Rätsel-Longs ~7 min (Quiz World 520k = 277×, GK Studio 45k = 48×, Quiz Guy 38k = 33×), Serien-Erkennung (Dopamine F1 Part 3 = 42×), niedrige Punkt-Hürde (QuizNova „Scoring 5 Out Of 25“ = 16×). GTA VI 19.11. erneut bestätigt (Take-Two). → E14 Rätsel-Long + GTA-Short am Do 19.11. bleiben.
- **Änderung heute:** keine Regeländerung. 18.11. = E16 Tag 3 (gerader Tag → pop 16:00): pop „Capitals Quiz“ vs. atlas „Tricky Trivia Quiz“ (beide Themen = unsere zwei besten 6-Q-Muster: Capitals 1.068, Tricky 1.550). Am 19.11. Arme tauschen (Tricky-Klasse in pop), damit kein Arm das stärkere Thema bekommt.

## Konkurrenz-Gewinner heute (competitors-report.json 15.11., letzte 30 Tage)

| # | Video (Kanal, Abos) | Views | × Median | Länge | Titel-Muster | Was wir übernehmen → Slot |
|---|---|---|---|---|---|---|
| 1 | "10 Tricky IQ Riddles / Test Your Intelligence!" (Quiz World, 1.080) – 22.10. | 519.944 | 277× | 6:48 | Zahl + „Tricky“ + IQ, kein Emoji, kein Score | **E14 Do 19.11. Long** (~7 min, 12 eigene sichtbare Rätsel) |
| 2 | "Can You Name F1 Track From Above? — Part 3" (Dopamine Quiz, 441) – 31.10. | 30.103 | 42× | 8:50 | Erkennen aus Vogelperspektive + Serien-Nummer | **Di 17.11. Karten-Long Folge 2** (Serie, Suchphrase vorn) |
| 3 | "ARE YOU A GENIUS? Prove It By Scoring 5 Out Of 25 On This Extreme IQ Test!" (QuizNova, 1.410) – 28.10. | 22.628 | 16× | 8:21 | **niedrige Punkt-Hürde** + Genius-Identität | Titel-Mechanik für E14 („Only Geniuses Solve 4“) – erlaubtes Besitzer-Experiment; Senioren-Teil NICHT |
| 4 | "Name the artist by the album cover" / "Name the airline from its livery" (Chauncey Asks, 6.330) – 04.11./20.10. | 508.296 / 783.740 | 10× / 16× | 1:37 / 1:17 | „Name the X from its Y“ – Erkennen aus Detail | Backlog #3: 6-Q „Name the Country From Its Outline“ (eigene Umrisse aus truesize.json); keine Logos/Cover |
| 5 | "Are You Smarter Than A 12 Year Old? 🤔" (Studio Seven, 1.480) – 10.11. | 64.606 | 9× | 1:56 | Vergleichs-Identität „smarter than a kid“ | Backlog #7: Titeltest nach E16 (nicht jetzt – sonst 2 Variablen) |

Nicht übernommen: Senioren-/Alters-Titel (QuizNova „Brain Exam for Seniors“ 57k – Besitzer-Verbot), Gabby's Dollhouse/Disney-Stimmen (Rechte), „English Quizz“-Wortschatz (bei uns 148 ✗), Google-Earth-Satellitenbilder (Lizenz), WWII (Krieg).

## 3-Tage-Plan

Layout-Regel (neueste Besitzer-STRATEGIE 13.11. überschreibt „tvshow für alles“): Shorts 16.–22.11. E16 pop/atlas (gerade Tage pop 16:00, ungerade pop 21:00); Longs tvshow v2 bzw. TrueSizeLong; Longs nur Di/Do/Sa 14:00 (STRATEGIE 09.11. überschreibt „1 Long pro Tag“).

| Datum / Slot | Format | Thema | Arbeitstitel (YouTube) | Fragen + timing | Hook / Fragen | Musik | cardColors | Thumbnail / Bild | Warum | Erfolgskriterium |
|---|---|---|---|---|---|---|---|---|---|---|
| 16.11. Long | kein Long (Mo) | – | – | – | – | – | – | – | Long-Tage Di/Do/Sa | – |
| 16.11. Short 16:00 | 6-Q **pop** (Queue six-q-genius-country-pop) | Länder | Only Geniuses Get 6/6 🧠 Country Quiz | 6 (Queue), E15 | Queue | game-show | – (pop) | – | E16 Paar 1 pop | ≥600 n. 3 T |
| 16.11. Short 21:00 | 6-Q **atlas** (Queue six-q-genius-landmarks) | Wahrzeichen | Only Geniuses Get 6/6 🧠 Landmarks Quiz | 6 (Queue), E15 | Queue | game-show | – | – | E16 Paar 1 atlas | ≥600 n. 3 T |
| 17.11. Long 14:00 | Karten-Long TrueSizeLong (Queue map-true-size-us-20-2) | US-Staaten vs. Länder | The True Size of US States: 20 Maps That Lie to You 🇺🇸 | 20 Runden (Queue) | Queue | world-trip | – | TrueSizeThumb „ALASKA IS A LIE“ | Exploit #1 Long + Konkurrenz #2 | ≥100 n. 3 T |
| 17.11. Short 16:00 | 6-Q **atlas** (Queue six-q-genius-geography) | Welt-Geo | Only Geniuses Get 6/6 🧠 Geography Quiz | 6 (Queue) | Queue | game-show | – | – | E16 Paar 2 atlas | ≥600 n. 3 T |
| 17.11. Short 21:00 | 6-Q **pop** (Queue six-q-genius-usa-pop) | USA, gepaart zum Long | Only Geniuses Get 6/6 🧠 USA Quiz | 6 (Queue) | Queue | game-show | – (pop) | – | E16 Paar 2 pop + Short→Long | ≥600 n. 3 T |
| 18.11. Long | kein Long (Mi) | – | – | – | – | – | – | – | – | – |
| **18.11. Short 16:00 (NEU, E16 pop)** | 6-Q **layout "pop"** | Hauptstädte | **Only Geniuses Get 6/6 🧠 Capitals Quiz** (+ #shorts) | 6, count 2.5 / tail 0.8, E15 (`lines[0].a` = „Tokyo!“) | Q1 EASY "What is the capital of **Japan**?" (Osaka/Kyoto/**Tokyo**/Hiroshima) · Q2 EASY "What is the capital of **Wales**?" (**Cardiff**/Swansea/Newport/Bangor) · Q3 MEDIUM "What is the capital of **Switzerland**?" (Zurich/**Bern**/Geneva/Basel) · **#4 Falle** "What is the capital of **Brazil**?" (Rio de Janeiro/São Paulo/Salvador/**Brasília**) · Q5 HARD "What is the capital of **Kazakhstan**?" (Almaty/**Astana**/Tashkent/Bishkek) · Finale LEGEND "What is the capital of **Nigeria**?" (Lagos/Kano/**Abuja**/Ibadan) → Indizes 2/0/1/3/1/2 | game-show | **nicht setzen** (pop) | broll Q1 "cherry blossom temple", Q2 "castle green hills", Q3 "alpine lake mountains", Q4 "tropical beach city", Q5 "steppe horses", Q6 "busy african market"; cardText Q1 "🍣", Q2 "🐉", Q3 "🧀⌚", Q4 "⚽🌴", Q5 "🐎🏔️", Q6 "🌍" | **E16 Tag 3 pop** + Themen-Exploit (Capitals-6-Q 1.068 ✓) | E16 + ≥600 n. 3 T |
| **18.11. Short 21:00 (NEU, E16 atlas)** | 6-Q **layout "atlas"** | leichtes Allgemeinwissen | **Only Geniuses Get 6/6 🧠 Tricky Trivia Quiz** (+ #shorts) | 6, count 2.5 / tail 0.8, E15 (`lines[0].a` = „1,440!“) | Q1 EASY "How many **minutes** are in one day?" (1,240/1,400/**1,440**/2,400) · Q2 EASY "How many **squares** are on a chessboard?" (**64**/36/48/100) · Q3 MEDIUM "Add up all the **dots** on one die. Total?" (18/**21**/24/36) · **#4 Falle** "How many **bones** does a shark have?" (About 300/About 200/About 100/**Zero**) – Skelett aus Knorpel · Q5 HARD "What is the most common **bird** on Earth?" (Pigeon/**Chicken**/Sparrow/Crow) – ~25–30 Mrd. Hühner · Finale LEGEND "**Thursday** is named after which god?" (Odin/Zeus/Mars/**Thor**) → Indizes 2/0/1/3/1/3 | game-show | – (atlas) | broll Q1 "clock time lapse", Q2 "chess game hands", Q3 "rolling dice table", Q4 "shark swimming underwater", Q5 "birds flock sky", Q6 "thunderstorm lightning" (keine Clips mit Huhn/Hammer) | **E16 Tag 3 atlas** + Themen-Exploit (Tricky Trivia 1.550 = bestes Short) | E16 + ≥600 n. 3 T |

Duplikat-Check 18.11. erledigt (grep über queue/done + queue, alle question-Texte): frei = Hauptstadt Japan/Wales/Schweiz/Brasilien (nur „In welchem Jahr wurde Brasília Hauptstadt“ benutzt → andere Frage, ok)/Kasachstan/Nigeria, Minuten pro Tag, Schachbrett-Felder, Würfelaugen, Hai-Knochen, häufigster Vogel, Thursday/Thor. Schon benutzt (nicht nehmen): Kanada, Australien, Türkei, Neuseeland, Marokko, Vietnam, Pakistan, Myanmar, Südkorea, Philippinen, Kenia (Hauptstädte); Buchstabe Q, Giraffenzunge, Blutgruppe, Freiheitsstatue, größte Wüste, Fingerabdruck Koala, Regenbogen, Papier, Black Box, flüssiges Metall, Mauna Kea, Muttersprache, Huhn-Männchen.

Bandit 16.–18.11.: Themen in allen Slots = Exploit (Geo/Länder/Capitals/Tricky, Karten-Long); variiert wird nur das Layout (E16) + E15 → saubere Ein-Variablen-Tests.

## Ideen-Backlog (nach erwartetem Potenzial)
1. **E14 Do 19.11. Long (am 17.11. anlegen): „12 Tricky IQ Riddles – Only Geniuses Solve 4 🧠“** – 12 eigene Rätsel als cardText (Zahlenreihen, Uhr-/Wochentag-Logik, Wortlogik), count 20 s, ~7 min, Thumb v2 A "12 TRICKY RIDDLES" + Rätsel „2 · 6 · 12 · 20 · ?“ / B "CAN YOU SOLVE 4?" / C "ONLY 1% SOLVE #12". Evidenz: Quiz World 520k (277×), Quiz Guy 38k/85k, QuizNova-Hürde 16×. Erfolg ≥50 n. 3 T.
2. **GTA VI (Release 19.11., Take-Two bestätigt): „Only Real Fans Get 6/6 🎮 GTA Quiz“ als 3. Short 19.11. 10:00** außerhalb E16 – Textfakten (Vice City ↔ Miami, GTA V 2013, Staat Leonida, Lucia & Jason), keine Spielbilder/Logos/Gewalt; broll neutral ("miami beach palm trees"). Suchspitze der Woche.
3. **Short „Name the Country From Its Outline“** (6-Q, Umriss aus truesize.json) – Chauncey-Muster (airline 784k, album 508k); braucht Code-Hook q["shape"] → nach E16-Verdict 25.11.
4. **Karten-VS #3 Di 24.11. 21:00 „This Map Is Lying To You #3 🇺🇸“** – map-lie-1 1.023 (Ø angesehen 81 %), map-lie-2 341 nach 0,6 T; Reserve-Paare aus Folge 2.
5. **Hunger Games: Sunrise on the Reaping (Kinostart 20.11.)**: „Only Real Fans Get 6/6 🏹 Hunger Games Quiz“ als 3. Short 20.11. 10:00 – nur Buchfakten, keine Filmbilder (Movie-6-Q 409 ✗ → nur wegen Suchspitze, nicht als Dauer-Thema).
6. **Thanksgiving Do 26.11. Long „Thanksgiving Trivia Quiz 🦃 Can You Get 10/15?“** (7-min-Format) – Trends „thanksgiving trivia“ +350 %, Still Sharp 44k bei 337 Abos; 25.11. 21:00 gepaartes 6-Q.
7. **6-Q-Titeltest „Are You Smarter Than a 5th Grader? 🧠“** – Studio Seven 64,6k (9×, 10.11.); nach E16.
8. **VS „Which US State Has More People?“** – bestes VS-Muster (1.090/1.189) mit US-Publikum (US = 75 % unserer Views), ab 24.11. (kein VS in E16-Woche).
9. **Math-Rätsel-Long „Can You Pass This Math Quiz? Easy to Impossible“** – CandyQuiz 377k; nach E14-Verdict.
10. **Long „Guess the Word by Emoji – USA Edition“** – Again Quiz 437k, Kids Quizzy 752k; nur wenn Country-Emoji-Long ≥30 n. 3 T (E13-Verdict 21.11.; Movie-Emoji 18 ✗ spricht dagegen).

Gestrichen: Weltraum, Wissenschaft, Wortschatz, Bauwerkshöhen, Gewicht-/Kälte-/Alter-VS (older 191 ✗), Flaggen-6-Q, **Film-6-Q als Dauer-Thema (409 ✗)**, Jahrestage im 16:00-Slot, Krieg/Sprengstoff, Halloween, Alters-Titel, 50-Fragen-Text-Longs, „Round 2“-Titel bei 6-Q.

## Für den Produktions-Agenten (gilt heute, überschreibt ältere Defaults)
- **Heute produzieren (Mo, kein Long-Tag):** six-q-genius-country-pop 16:00 (erstes pop – Render prüfen, s. TECHNIK), six-q-genius-landmarks 21:00.
- **Für 18.11. anlegen (Mi, kein Long, E16 Tag 3, gerader Tag → pop = 16:00):**
  - `2026-11-18-six-q-genius-capitals-pop.json` (publishAt "16:00", `layout: "pop"`, game-show, count 2.5/tail 0.8, `broll` + `cardText` je Frage, kein `cardColors`, E15 „Tokyo!“). Muster: queue/2026-11-17-six-q-genius-usa-pop.json.
  - `2026-11-18-six-q-genius-tricky-2.json` (publishAt "21:00", `layout: "atlas"`, game-show, count 2.5/tail 0.8, `broll` je Frage, E15 „1,440!“). Titel OHNE „2“/„Round 2“: "Only Geniuses Get 6/6 🧠 Tricky Trivia Quiz #shorts" – falls YouTube-Titel-Duplikat stört: "Only Geniuses Get 6/6 🧠 Tricky Quiz #shorts".
  - Fragen + Antwortindizes exakt wie in der Tabelle (Positionen schon gemischt). Fakten-Zeilen kurz halten (z. B. Hai: „Zero! Sharks are made of cartilage.“; Huhn: „Chicken! Over 25 billion of them.“; Thor: „Thor! Thor's day.“; Brasília: „Brasília! Not Rio.“; Abuja: „Abuja! Not Lagos.“).
- **Vorschau 19.11. (Do, Long-Tag, ungerader Tag → pop = 21:00) – morgen anlegen, Research bestätigt morgen:** E14 Rätsel-Long 14:00 (Backlog #1, tvshow v2), atlas-6-Q 16:00 + pop-6-Q 21:00 (Arme tauschen: Allgemeinwissen-Klasse in pop, Geo in atlas), GTA-6-Q als 3. Short 10:00 außerhalb E16 (Backlog #2).
- **Vor dem Anlegen:** frischen Analytics-Snapshot ziehen; in experiments.md 24-h-Werte world-geo/bigger-2 und ≥3-T-Werte europe/people-R3/animals/map-lie-2 nachtragen (Verdicts older/movies/movie-emoji hat Research heute eingetragen).
- Weiter verboten: VS-Shorts 16.–22.11. (außer Karten-Long), VS mit pop, Longs Mo/Mi/Fr/So, Weltraum, Halloween, Politik, Krieg/Waffen, 💥, Alters-Titel.
