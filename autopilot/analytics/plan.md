# Plan – 2026-11-14 (Sa)

TECHNIK-PROBLEM: nichts Blockierendes. Läufe 13.11. grün (six-q-genius-europe 16:00, vs-more-people-3 21:00 hochgeladen, beide Kommentare gepostet 16:08/21:11). Hinweise: (1) **Analytics-Snapshot ist vom 13.11. 11:49** – Europe/People-R3 dort noch privat; der heutige Lauf muss frischen Snapshot ziehen (sonst Verdicts unmöglich). (2) **Movie-Emoji-Long (12.11.) nur 4 öffentliche Views n. ~22 h** trotz v2-Thumb-Neustart – bitte im heutigen Lauf prüfen, ob das Video wirklich öffentlich + nicht „made for kids“ ist und ob das neue Thumbnail A gesetzt wurde (Log-Zeile „Thumbnail gesetzt“). (3) CTR per API weiter HttpError 400 (bekannt). (4) Scoreboard zählt TrueSize-Videos noch als „0 Fragen“/„comic“ (nicht kritisch).

## Zusammenfassung (Deutsch)
- **atlas kippt:** Von den 6 atlas-Shorts 10.–12.11. liegen nur 2 über dem 24-h-Median ~436 (tricky **1.297**, map-lie-1 **1.015**); flags **286** (1,8 T), colder **118**, movies **299** (~15 h), older **94** (~20 h). Atlas-Median damit ~290 vs. tvshow-Shorts-Median 439 → E12-Regel ausgelöst; der Besitzer testet ab 16.11. ohnehin pop vs. atlas (E16) – genau richtig.
- **Longs:** Karten-Long True Size **101** öffentl. (~2,9 T) = E13 #1 ✓. Movie-Emoji-Long **4** n. ~22 h = Warnsignal für E13 (#2). Heute 14:00 Country-Emoji-Long (E13 #3) entscheidet, ob Emoji-Longs bleiben.
- **Gewinner bestätigt (≥2,6 T):** tricky 1.297 ✓, map-lie-1 1.015 ✓ → „Only Geniuses 6/6“ + leichtes Allgemeinwissen/Geo und Karten-VS bleiben Exploit #1/#2. Themen-Flops bleiben gestrichen (Weltraum, Jahrestage, Gewicht, Kälte 118, Alter 94).
- **Konkurrenz:** Rätsel-/IQ-Longs dominieren weiter (Quiz World 520k, Can You Solve? 517k, Clear Think 1,79 Mio). GTA VI erscheint laut Take-Two weiter am **19.11.** → größte Suchspitze der Woche.
- **Änderung:** ab 16.11. E16 strikt (2× 6-Q, pop/atlas), keine VS-Shorts; Do 19.11. E14 Rätsel-Long + GTA-6-Q als **3. Short 10:00** außerhalb des Tests.

## Konkurrenz-Gewinner heute (competitors.md 13.11. + outliers.md 12.11., letzte 30 Tage)

| # | Video (Kanal, Abos) | Views | × Median | Länge | Titel-Muster | Was wir übernehmen → Slot |
|---|---|---|---|---|---|---|
| 1 | "10 Tricky IQ Riddles / Test Your Intelligence!" (Quiz World, 1.080) – 22.10. | 519.627 | 277× | 6:48 | Zahl + „Tricky“ + IQ, ohne Emoji | ~7 min, 10–12 sichtbare Rätsel → **Do 19.11. Long E14** |
| 2 | "15 Mystery Riddles That Will Test Your IQ 99% Fail🧠🔥" (Can You Solve?, 5.210) | 516.612 (106k/Tag) | 99× Abos | 8:44 | Zahl + Riddles + IQ + „99% Fail“ | Titelmechanik E14: „12 Tricky IQ Riddles – Only Geniuses Solve 4 🧠“ |
| 3 | "ARE YOU WELL-EDUCATED? TRY TO SCORE ABOVE 5!" (Golden Memory Quiz, 2.790) | 267.000 | 96× Abos | 8:06 | Identitäts-Hook + niedrige Hürde | Bestätigt die Hürde „Solve 4“ im E14-Titel; NICHT als Text-Allgemeinwissen (E1 floppte 0/0/1) – nur mit sichtbaren Rätseln |
| 4 | "Name the airline from its livery" (Chauncey Asks, 5.940) – Short 20.10. | 749.214 | 15× | 1:17 | Erkennen aus einem Bild-Detail | Pop-Arm E16: großes Foto/B-Roll pro Frage ist der Klickgrund → pop-Items immer mit `broll`; später Short „Name the Country From Its Outline“ (Backlog #5) |
| 5 | "Bird Quiz 🐦 / Can You Answer All 6 Questions Correctly?" (GK QuizCast, 807) – Short | 60.147 | 74× Abos | 1:07 | Tier-Thema + „all 6“ | Stützt das Tier-6-Q-Experiment von heute 16:00; bei ≥600 → Tier-Emoji-Long im Backlog |

Nicht übernommen: Alters-/Senioren-Titel (QuizNova, QuizVerse – Besitzer-Verbot), Disney/Gabby/YouTuber-Stimmen (Rechte), F1-Google-Earth (Satellitenbilder), WWII-Quiz (Krieg), Religions-Quiz (Y King Bible 374k – heikel), Wortschatz-Shorts (bei uns 144 ✗).

## 3-Tage-Plan

Layout: **Shorts 14./15.11. atlas (Queue), ab 16.11. E16 pop/atlas**; Longs tvshow v2 bzw. TrueSizeLong (Besitzer-STRATEGIE 09./13.11. ist neuer als „tvshow für alles“). Longs nur Di/Do/Sa 14:00. Fakten prüfen, gegen `queue/done/*` greppen (für 16.11. schon gegrept, s. u.).

| Datum / Slot | Format | Thema | Arbeitstitel (YouTube) | Fragen + timing | Hook / Fragen | Musik | cardColors | Thumbnail A/B/C + Foto | Warum | Erfolgskriterium |
|---|---|---|---|---|---|---|---|---|---|---|
| **14.11. Long 14:00** | Emoji-Long QuizLong tvshow v2 (Queue country-emoji-30-1) | Länder per Emoji | Guess the Country by Emoji: 30 Rounds From Easy to Legend 🌍 | 30 (Queue) | Queue | world-trip | petrol | v2: A "GUESS THE COUNTRY" + 🌋+♨️+🐋 / B "CAN YOU GET 25/30?" / C "ONLY 1% GET 30/30" | E13 #3 | ≥30 n. 3 T |
| 14.11. Short 16:00 | 6-Q atlas (Queue six-q-genius-animals) | Tiere | Only Geniuses Get 6/6 🧠 Animal Quiz | 6 (Queue) | Queue | game-show | – | – | **Experiment Thema Tiere** (Konkurrenz #5) | ≥600 n. 3 T; <400 → Tiere raus |
| 14.11. Short 21:00 | Karten-VS truesize (Queue map-lie-2), Paar zum Long | Wahre Größe #2 | This Map Is Lying To You #2 🌍 Which Is REALLY Bigger? | 4 (Queue) | Queue | world-trip | – | fest | Exploit Karten-VS (1.015) | ≥800 n. 3 T |
| 15.11. Long | kein Long (So) | – | – | – | – | – | – | – | – | – |
| 15.11. Short 16:00 | 6-Q atlas (Queue six-q-genius-world-geo, E15) | Welt-Geo | Only Geniuses Get 6/6 🧠 World Geography Quiz | 6 (Queue) | Queue | game-show | – | – | Exploit Geo-6-Q + E15 #1 | ≥800 n. 3 T; E15-Kurvenquote ≥0,75 |
| 15.11. Short 21:00 | VS atlas (Queue vs-countries-bigger-2) | Ländergröße | Which Country Is Bigger? 90% Get #4 Wrong 🌍 | 4 (Queue) | Queue | world-trip | – | – | Exploit VS (letztes VS vor E16-Woche) | ≥700 n. 3 T |
| 16.11. Long | kein Long (Mo) | – | – | – | – | – | – | – | – | – |
| **16.11. Short 16:00 (NEU, E16 pop)** | 6-Q **layout "pop"** | Länder | **Only Geniuses Get 6/6 🧠 Country Quiz** (+ #shorts) | 6, count 2.5 / tail 0.8, 4 Optionen, Antworten ≤3 Wörter, E15 (`lines[0].a` = „Morocco!“) | Q1 "Which country is home to the city of Marrakech?" (Morocco/Egypt/Tunisia/Turkey) → Morocco · Q2 "Which country has the most people in South America?" (Brazil/Argentina/Colombia/Peru) → Brazil · Q3 "Which country is famous for its fjords?" (Norway/Sweden/Finland/Denmark) → Norway · **#4 Falle "Which country drinks the most coffee per person?" (Italy/Brazil/USA/Finland) → Finland** (~12 kg/Kopf/Jahr) · Q5 "The unicorn is the national animal of which country?" (Ireland/Wales/Scotland/Norway) → Scotland · Finale "Which country has the most lakes?" (USA/Russia/Finland/Canada) → Canada (≈60 % aller Seen) | game-show | **nicht setzen** (pop) | – ; broll Q1 "desert market spices", Q2 "rainforest river aerial", Q3 "steep cliffs boat", Q4 "coffee cups cafe", Q5 "highland castle mist", Q6 "forest lakes aerial"; cardText Q1 "🕌", Q2 "👥", Q3 "⛰️🌊", Q4 "☕", Q5 "🦄", Q6 "💧" | **E16 pop-Arm** (Besitzer); Exploit Geo/Länder | E16 (s. experiments.md) + ≥600 n. 3 T |
| **16.11. Short 21:00 (NEU, E16 atlas)** | 6-Q **layout "atlas"** | Wahrzeichen | **Only Geniuses Get 6/6 🧠 Landmarks Quiz** (+ #shorts) | 6, count 2.5 / tail 0.8, E15 (`lines[0].a` = „Barcelona!“) | Q1 "In which city is the Sagrada Família?" (Madrid/Barcelona/Lisbon/Rome) → Barcelona · Q2 "In which country is Stonehenge?" (Ireland/Scotland/England/France) → England · Q3 "How many presidents' faces are carved into Mount Rushmore?" (3/4/5/6) → 4 · **#4 Falle "The Leaning Tower of Pisa was built as a…?" (Lighthouse/Bell tower/Watchtower/Church) → Bell tower** · Q5 "In which city is the Acropolis?" (Rome/Istanbul/Athens/Cairo) → Athens · Finale "Neuschwanstein Castle is in which country?" (Austria/Switzerland/France/Germany) → Germany (Bayern) | game-show | – (atlas) | – ; broll neutral: Q1 "church construction crane", Q2 "ancient stones field", Q3 "mountain granite cliff", Q4 "italian piazza old town" (Frage nennt den Turm, broll zeigt ihn nicht), Q5 "ancient columns hill", Q6 "castle mountains forest" | **E16 atlas-Arm** (Kontrolle) | E16 + ≥600 n. 3 T |

Duplikat-Check 16.11. erledigt (grep queue/done): Tulpen/Windmühlen, Ahornblatt, Freiheitsstatue, Kolosseum, Taj Mahal, Big Ben, Petra, Pyramiden, Drachenflagge, längste Küste sind schon benutzt → nicht im Plan. Marrakech, Fjorde, Kaffee, Einhorn, Seen, Sagrada, Stonehenge, Rushmore, Pisa-als-Frage, Acropolis, Neuschwanstein: frei.

Vorschau (nicht anlegen, morgen fein planen): **Di 17.11.** Long 14:00 Karten-Long Folge 2 „The True Size of US States vs Countries“ (Kalifornien-Form ergänzen) · 16:00 atlas „Only Geniuses Get 6/6 🧠 Geography Quiz“ · 21:00 **pop** „Only Geniuses Get 6/6 🧠 USA Quiz“ (ungerader Tag = pop 21:00, gepaart zum Long). **Do 19.11.** Long = **E14 Rätsel-Long** (anlegen am 17.11.) + GTA-6-Q als 3. Short 10:00 (außerhalb E16).

Bandit 14.–16.11.: Exploit 5 (Country-Long-Format E13, Karten-VS, World-Geo, Bigger-VS, Länder-Themen in E16) / Experiment 3 (Tiere, E15, E16-Layout vom Besitzer) ≈ 65/35 – vertretbar, weil E16 vom Besitzer gesetzt ist.

## Ideen-Backlog (nach erwartetem Potenzial)
1. **E14 Do 19.11. Long: „12 Tricky IQ Riddles – Only Geniuses Solve 4 🧠 7-Minute Test“** – 12 eigene Rätsel als cardText, count 20 s, Thumb v2 A "12 TRICKY RIDDLES" + "2 · 6 · 12 · 20 · ?" / B "CAN YOU SOLVE 4?" / C "ONLY 1% SOLVE #12". Evidenz: Quiz World 520k, Can You Solve? 517k, Golden Memory 267k. Erfolg ≥50 n. 3 T.
2. **GTA VI 19.11. (Take-Two bestätigt): „Only Real Fans Get 6/6 🎮 GTA Quiz“ 10:00** – reine Textfakten (Vice City = Miami-Vorbild, GTA V 2013, Leonida), keine Spielbilder/Logos/Gewalt.
3. **Karten-Long Folge 2 Di 17.11.: „The True Size of US States vs Countries“** – Folge 1 101 Views (bestes Long seit Okt.), US = 60 % Publikum.
4. **Thanksgiving Do 26.11.: Emoji-Long „Guess the Thanksgiving Food by Emoji 🦃“** – Trends „thanksgiving trivia“ +350 %, Still Sharp 44k bei 337 Abos. Nur wenn Country-Emoji-Long ≥30.
5. **Short „Name the Country From Its Outline“ (6-Q, Umriss als Bild aus truesize.json-Formen)** – Chauncey-Muster (livery 749k, European city 964k); braucht ggf. kleinen Code-Hook → erst nach E16.
6. **Hunger Games: Sunrise on the Reaping (20.11.): 6-Q „Only Real Fans Get 6/6 🏹 Hunger Games Quiz“** als 3. Short – nur Buchfakten.
7. **Math-Rätsel-Long „Can You Pass This Math Quiz? Easy to Impossible“** – CandyQuiz 377k; nach E14-Verdict.
8. **Long „Guess the Word by Emoji – USA Edition“** – Again Quiz 437k, Kids Quizzy 752k; nach E13-Verdict 21.11.
9. **VS „Which US State Has More People?“** – bestes VS-Muster, ab 24.11. (nach E16).
10. **6-Q-Titeltest „You're Not Smart Enough to Get 6/6 🧠 …“** – Quiz Guy 85k; nach E16 (sonst 2 Variablen).

Gestrichen: Weltraum, Wissenschaft, Wortschatz, Bauwerkshöhen, Gewicht-/Kälte-/Alter-VS (388/118/94), Jahrestage im 16:00-Slot, Krieg/Sprengstoff, Halloween, Alters-Titel, 50-Fragen-Text-Longs, „Round 2“-Titel bei 6-Q.

## Für den Produktions-Agenten (gilt heute, überschreibt ältere Defaults)
- **Heute produzieren (Sa = Long-Tag):** country-emoji-30-1 14:00, six-q-genius-animals 16:00, map-lie-2 21:00 (alle in Queue).
- **Für 16.11. anlegen (E16 Tag 1, gerader Tag → pop = 16:00):** `2026-11-16-six-q-genius-country-pop.json` (publishAt "16:00", `layout: "pop"`, game-show, count 2.5/tail 0.8, jede Frage `broll` + `cardText`, kein `cardColors`) und `2026-11-16-six-q-genius-landmarks.json` (publishAt "21:00", `layout: "atlas"`, game-show, count 2.5/tail 0.8, `broll`) exakt wie in der Tabelle; bei beiden E15: `lines[0].a` nur Antwort + „!“. Antwortpositionen mischen (Country-Optionen so umsortieren, dass die Indizes z. B. 0/1/2/3/1/2 ergeben; Landmarks ergibt 1/2/1/1/2/3 → Q4 auf Index 0 drehen). Kaffee-Fakt: Finnland ≈12 kg/Kopf/Jahr (ICO/Statista) in der Beschreibung nennen.
- **Vorher:** frischen Analytics-Snapshot ziehen und prüfen, warum movie-emoji-30-1 nur 4 Views hat (Status/Thumbnail, s. TECHNIK-PROBLEM 2).
- Nach dem Snapshot in experiments.md: 24-h-Werte six-q-genius-europe + vs-more-people-3, ≥3-T-Werte flags/colder/movies/older.
- **Keine VS-Shorts 16.–22.11.**, kein VS mit pop, keine Longs Mo/Mi/Fr/So. Weiter verboten: Weltraum, Halloween, Politik, Krieg/Waffen, 💥, Alters-Titel.
