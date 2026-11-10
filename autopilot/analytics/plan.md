# Plan – 2026-11-10

## TECHNIK-PROBLEM
1. **Kein Lauf-Fehler** im Log (09.11.: Uploads 06:28–06:48, Kommentare 13:17 / 16:22 / 21:12 mit Long-Link, Konkurrenz 25 Kanäle / 135 Gewinner). Analytics-Stand **09.11. 11:55** (17 Abos) – die 09.11.-Videos waren beim Snapshot noch privat → heute neuer Snapshot nötig.
2. **Heute erste echte Uploads der neuen Formate** (Karten-Long TrueSizeLong 14:00, Karten-Short map-lie-1 21:00, atlas-6-Q 16:00). Nach dem Rendern QA prüfen: Standbild Shorts ≤ 3 s (> 4 s → neu rendern), Long-Standbild nur im Abspann erlaubt (Probelauf 11,6 s = Endkarten-Standzeit, ok). Vorschaubild TrueSizeThumb + Kapitel prüfen.
3. **Queue-Zuordnung Longs (geprüft, ok):** autopilot.py nimmt `sorted(QUEUE.glob('*.json'))` → heute `2026-11-10-map-true-size-20-1` vor `2026-11-10-movie-emoji-30-1` (alphabetisch map < movie), Do 12.11. movie-emoji, Sa 14.11. country-emoji. Nichts umbenennen – nur im Log bestätigen, dass heute das Karten-Long lief.
4. **experiments.md** enthält die Zeile E8 #5 country-emoji doppelt (11.11.) → beim nächsten Eintrag eine löschen; sie läuft jetzt am 14.11.
5. Hinweis Prompt-Konflikt: Der Agenten-Prompt sagt noch „tvshow für alles“, die neueste Besitzer-STRATEGIE (09.11., learnings.md) sagt **Shorts = atlas, Longs = tvshow/TrueSizeLong**. Es gilt die neueste Besitzer-Regel.

## Zusammenfassung (Deutsch)
- **Geografie/Länder bleiben König:** VS „Which Country Has More People?“ 1.037 Views (2,2 T), 6-Q Capital Cities 891 (2,2 T) – Shorts-Median 466 (tvshow). 
- **Weltraum floppt formatübergreifend:** 6-Q Space 162 n. ~21 h, VS Planets & Moons 79 n. ~16 h, Solar-System-Long 3. → Weltraum raus aus allen Slots (E9 vorläufig ✗).
- **Longs:** Capitals-30 12 Views (bestes 30er-Long), Rest 0–3. Ab heute Longs 2.0 (E13): nur Di/Do/Sa, Karten-/Emoji-Format. E8 geht in E13 auf.
- **Look-Wechsel:** stick (E11) nach nur 2 Videos vom Besitzer durch **atlas** (E12) ersetzt – E11 ohne Daten abgelöst. Heute die ersten 3 atlas-/Karten-Videos.
- **Konkurrenz:** Rätsel/IQ in ~7 min dominiert weiter (Quiz World 519k, Clear Think 246k, Quiz Guy 84k). Kommende Suchspitzen: **GTA VI 19.11.** (Take-Two bestätigt), **Hunger Games: Sunrise on the Reaping 20.11.**, Thanksgiving 26.11.

## Konkurrenz-Gewinner heute (competitors.md 09.11., letzte 30 Tage)

| # | Video (Kanal, Abos) | Views | × Median | Länge | Titel-Muster | Was wir übernehmen → Slot |
|---|---|---|---|---|---|---|
| 1 | "10 Tricky IQ Riddles / Test Your Intelligence!" (Quiz World, 1.090) – 22.10. | 518.943 | 277× | 6:48 | Zahl + „Tricky“ + IQ-Versprechen, kein Emoji | „Tricky“ im 6-Q heute 16:00. Long-Version nur als **visuelles** Rätsel-Long (Zahlenfolgen/Muster als cardText) → Backlog #3, frühestens nach E13-Verdict 21.11. |
| 2 | "Test Your IQ Level in just 8 Min (Part 2)" (Clear Think, 6.790) – 13.10. | 246.008 | 257× | 8:09 | IQ + Zeitversprechen | Zeitversprechen als Long-Titelvariable („in 7 Minutes“) → Backlog #4 |
| 3 | "You're Not Smart Enough to Solve These 12 Puzzles!" (Quiz Guy, 492) – 15.10. | 84.459 | 73× | 8:15 | Provokation („Not Smart Enough“) + kleine Zahl | Bestätigt Rätsel-Long mit ~12 Runden; Provokations-Titel für 6-Q als späterer Titeltest |
| 4 | "Name a European city that starts with..." (Chauncey Asks, 5.240) – Short 15.10. | 896.039 | 25× | 1:55 | Geo-Wortspiel, offene Frage | Geo = unser Bestes → 11.11. Flaggen-6-Q, Backlog #5 „Europe Quiz“. Interview-Format nicht renderbar |
| 5 | "🧠 Your Brain Is Ageless! Take This 10-Question IQ Quiz" (GK STUDIO PRO, 1.880) – 27.10. | 44.643 | 48× | 7:14 | Kompliment-Hook + 10 Fragen | Struktur = E1 (bei uns 0/0/1, gestoppt) → nicht übernehmen, nur Kompliment-Hook als Idee für Short-Hooktext |

Zusätzlich beobachtet: Quibby „Name the Movie By The Car“ 389k (1.222×) + Quiz Bunny „Guess the Movie by Emoji“ 693k → stützt **12.11. Movie-Paar** (Emoji-Long + Movie-6-Q 21:00). Nicht übernommen: Playbill/Airline-Livery (Marken), F1 Google Earth (Satellitenbilder nicht lizenziert), Disney-Songs (Musikrechte), comicnutz (Comic-Figuren).

## 3-Tage-Plan

Layout: **Shorts = atlas** (Besitzer 09.11., keine Emojis/Maskottchen/KI-Clips im Bild, Bild nur `broll`/`image`), **Longs = tvshow bzw. TrueSizeLong**. Fakten vor dem Schreiben prüfen. Gegen `queue/done/*` greppen.

| Datum / Slot | Format | Thema | Arbeitstitel (YouTube) | Fragen + timing | Hook / Frage 1 | Musik | cardColors | Thumbnail A/B/C + Foto | Warum | Erfolgskriterium |
|---|---|---|---|---|---|---|---|---|---|---|
| 10.11. Long 14:00 | Karten-Long TrueSizeLong (Queue) | Wahre Größe der Länder | The True Size of Countries (Queue-Titel) | 20 Runden, think 3.4/move 1.7/tail 1.0 | Queue | Queue | – | TrueSizeThumb (Grönland auf Afrika) | E13 Longs 2.0, Outlier „Provinces“ 169k / Karten-Erkennung | E13: ≥30 Views n. 3 T |
| 10.11. Short 16:00 | 6-Q atlas (Queue) | Allgemeinwissen leicht | Only Geniuses Get 6/6 🧠 Tricky Trivia Quiz | 6 (Queue) | Queue | game-show | – | – | Exploit 6-Q (Median 942) + Quiz World „Tricky“; E12 #1 | ≥800 n. 3 T; E12: ≥436 n. 24 h |
| 10.11. Short 21:00 | Karten-VS truesize (Queue), gepaart mit Long | Kartenlüge | This Map Is Lying To You (Queue) | Queue | Queue | Queue | – | – | E12 Karten-VS (Besitzer-Abnahme) | ≥ VS-Median 876 n. 3 T |
| 11.11. Short 16:00 | 6-Q atlas (Queue) | Flaggen | Only Geniuses Get 6/6 🧠 Flag Quiz | 6 (Queue) | Queue | game-show | – | – | Exploit Geo + 6-Q | ≥800 n. 3 T |
| 11.11. Short 21:00 | VS atlas (Queue) | Kälte | Which Is Colder? 4 Rounds 90% Get #2 Wrong 🥶 | 4 (Queue) | Queue | world-trip | – | – | Exploit VS (Median 876, stayed 54,5 %) | ≥700 n. 3 T |
| 11.11. Long | **kein Long** (Mi ist kein Long-Tag) | – | – | – | – | – | – | – | Regel Longs 2.0 | – |
| 12.11. Long 14:00 | Emoji-Long QuizLong tvshow (Queue `2026-11-10-movie-emoji-30-1`) | Filme per Emoji | Guess the Movie by Emoji: 30 Rounds From Easy to Legend 🎬 | 30 (Queue) | Queue | game-show | violett/gold (Queue) | A "GUESS THE MOVIE" + DeLorean / B "25/30" / C "LEGEND LEVEL" | E13 + Emoji = einziges eigenes Long-Muster mit Reichweite (141) + Quiz Bunny 693k | E13: ≥30 n. 3 T |
| **12.11. Short 16:00** | VS atlas (Queue `2026-11-12-vs-older-1`) – **publishAt von 21:00 auf 16:00 ändern** | Alter | Which Is Older? 4 Rounds 90% Get #2 Wrong 🏛️ | 4 (Queue), count 3.0 / tail 1.2 | Queue | world-trip | – | – | Exploit VS; 21:00 wird für das Long-Paar gebraucht | ≥700 n. 3 T |
| **12.11. Short 21:00 (NEU)** | 6-Q atlas, ≤50 s, gepaart mit Movie-Emoji-Long | Filme (Text-Fragen) | **Only Geniuses Get 6/6 🧠 Movie Quiz** (+ #shorts, 35 Z.) | 6, count 2.5 / tail 0.8, 4 Optionen, Antworten ≤ 4 Wörter | Q1 leicht: "Which animated film stars a race car named Lightning McQueen?" → Cars. Q2: "Which superhero is called 'The Dark Knight'?" → Batman. Q3: "In 'Jurassic Park', where do scientists find dinosaur DNA?" → Mosquito in amber. **#4 Trick: "What colour are Dorothy's slippers in the 1939 'Wizard of Oz' film?" → Red/Ruby** (Falle Silver – im Buch von 1900 silbern, Film machte sie rot für Technicolor). Q5: "Which film won the very first Oscar for Best Animated Feature?" → Shrek (2002). Finale: "How many Oscars did 'Titanic' (1997) win?" → 11 (Optionen 7/9/11/14). **Keine Filme aus dem Emoji-Long als Antwort** (Liste im Queue-File) | game-show | – (atlas) | – (Short); `broll` je Frage, darf Antwort nicht verraten: Q1 "race track", Q2 "city skyline at night", Q3 "fossil museum", Q4 "old film projector" (NICHT rote Schuhe), Q5 "cinema seats", Q6 "golden statue" (NICHT Ozeandampfer) | **Experiment Thema Filme** (eine Variable: Thema; Titel/Format = bewährtes 6-Q) + Paarung mit Long + Quibby 389k / Quiz Bunny 693k | ≥600 n. 3 T; <400 → Filme nicht mehr in 6-Q, nur als Long |

Bandit 10.–12.11.: Exploit 5 (6-Q Tricky, 6-Q Flags, VS Colder, VS Older, Emoji-Long) / Experiment 3 (Karten-Long E13, Karten-VS E12, Movie-6-Q) ≈ 63/37 – plus Querschnitts-Experiment atlas-Look (Besitzer-Vorgabe).

## Ideen-Backlog (nach erwartetem Potenzial)
1. **GTA VI (Release 19.11., Take-Two bestätigt): 6-Q "Only Real Fans Get 6/6 🎮 GTA Quiz" am Do 19.11. 21:00** (gepaart mit Long des Tages) – größte Gaming-Suchspitze des Jahres; nur Textfakten (Vice City = Miami-Vorbild, Erscheinungsjahre GTA III 2001 / V 2013), keine Spielbilder/Logos, keine Gewalt-/Waffenfragen.
2. **Hunger Games: Sunrise on the Reaping (Kinostart 20.11.): 6-Q "Only Real Fans Get 6/6 🏹 Hunger Games Quiz" Fr 20.11.** – Buchfakten (Haymitch, 50. Spiele = 2. Quarter Quell), keine Filmstills.
3. **Long "Can You Solve These 10 Tricky Riddles?" (~7 min, Rätsel als cardText-Muster/Zahlenfolgen = visuell)** – Quiz World 519k (277×), Quiz Guy 84k/41k/38k, Puzzle Code 66k; erst nach E13-Verdict 21.11.
4. **Long-Titeltest „… in Just 7 Minutes“** – Clear Think 1,73 Mio + 246k; eine Variable am Emoji-/Karten-Long.
5. **6-Q "Only Geniuses Get 6/6 🧠 Europe Quiz"** – Chauncey Asks 896k, Geo-Shorts 891–1.188.
6. **Karten-Long Folge 2 Sa 21.11.: "The True Size of US States vs Countries"** (Texas/Alaska vorhanden, California nachtragen) – Karten = Owner-Format, „guess the country“ Autocomplete 4,2.
7. **VS "Which Country Is Bigger? Round 2" (atlas)** – „which is bigger“ Trends-Breakout, VS Bigger 876.
8. **Thanksgiving Do 26.11.: Long "Guess the Thanksgiving Food by Emoji" + 6-Q 21:00** – Trends „thanksgiving trivia“ +350 %; Halloween-35 war bestes Fragen-Long (186).
9. **Long "Guess the Animal by Emoji: 30 Rounds"** – Trends „guess the animal challenge“ +130 %, Emoji-Format.
10. **VS "Which Is Longer?" (Flüsse/Grenzen, atlas)** – VS-Format, nur unstrittige Paare (nicht Nil vs Amazonas).

Gestrichen: Weltraum (6-Q 162, VS 79, Long 3), Wissenschaft, Wortschatz, Bauwerkshöhen, Kriegs-/Sprengstoffthemen (Veterans Day 11.11. bewusst ausgelassen), Halloween.

## Für den Produktions-Agenten (gilt heute, überschreibt ältere Defaults)
- **Heute produzieren:** map-true-size-20-1 (Long, Di = Long-Tag), six-q-genius-tricky 16:00, map-lie-1 21:00. movie-emoji-30-1 erst Do 12.11. (Sortierung passt, siehe TECHNIK 3).
- **Für 12.11. anlegen:** `2026-11-12-six-q-genius-movies.json` (publishAt "21:00", layout atlas, Musik game-show, Fragen wie in der Tabelle, Fakten prüfen, gegen movie-emoji-30-1 und queue/done greppen). In `2026-11-12-vs-older-1.json` **publishAt "16:00"** setzen. Kommentar des 21:00-Shorts verlinkt das Movie-Emoji-Long.
- Für 11.11. nichts neu (kein Long-Tag, beide Shorts liegen bereit).
- **Kein Weltraum-Thema** mehr in Shorts oder Longs (auch nicht als Runde in neuen VS). vs-colder-1 bleibt wie angelegt.
- atlas-Regeln: keine Emojis im Bild, `q["ltx"]` nie setzen, Bild nur `broll` (verrät Antwort nicht) oder `image` aus image-credits.json.
- E12-Bewertung ab Snapshot 11.11.: atlas-Shorts gegen Shorts-Median 466 (24 h) und stayed 51 %.
- Weiter verboten: Halloween, Politik, Krieg/Waffen/Sprengstoff, 💥, Alters-Titel, E1-Longs, 50-Fragen-Text-Longs, Longs an Mo/Mi/Fr/So.
