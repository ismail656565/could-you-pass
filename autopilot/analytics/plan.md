# Plan – 2026-11-11

## TECHNIK-PROBLEM
1. **Bug Short→Long-Verlinkung (seit 10.11., 3× im Log):** `Verlinkung Short → langes Video fehlgeschlagen: 'questions'`. Ursache: `link_short_to_long()` in autopilot.py (Zeile ~1020) liest `long_item['story']['questions']` – das Karten-Long (story.type "truesize") hat `story.rounds`. Fix: `n = len(long_item['story'].get('questions') or long_item['story'].get('rounds') or [])` und Text je nach Typ: Quiz → `▶ Full {n}-question quiz:`, truesize → `▶ Full {n}-round map challenge:`. Danach einmal manuell für 10.11. nachholen (map-lie-1 + six-q-genius-tricky → pgaClOjxsBw verlinken), sonst bleibt das Karten-Paar ohne Beschreibungs-Link. Der Kommentar-Link lief (map-lie-1 21:06 gepostet).
2. **Analytics-Stand 10.11. 11:46 (18 Abos):** die drei 10.11.-Videos (erste atlas-/Karten-Videos) waren beim Snapshot noch privat → E12/E13 heute noch nicht bewertbar. Heute nach dem Snapshot die 24-h-Werte von map-lie-1, six-q-genius-tricky und pgaClOjxsBw in experiments.md eintragen.
3. **experiments.md:** Doppelzeile E8 #5 country-emoji ist bereits bereinigt (nur noch 1 Zeile; läuft Sa 14.11.) – erledigt.
4. Layout-Regel bleibt: **Shorts = atlas, Longs = tvshow/TrueSizeLong** (Besitzer-STRATEGIE 09.11., neuer als der Agenten-Prompt „tvshow für alles“).

## Zusammenfassung (Deutsch)
- **Shorts-Delle am 08./09.11.:** Space-6-Q 229 / VS Planets 127 (≈2,7 T, Weltraum ✗ endgültig), stick-Shorts Berlin Wall 96 / Heavier 79 nach ~0,8 T – weit unter dem 24-h-Median (~436). Gegenbeweis 07.11.: Geo-Paar 1.072 / 1.019. → Themen sind der Hebel: **nur Geo / Allgemeinwissen-leicht / Länder-VS** bis atlas bewertet ist.
- **Shorts-Format-Ranking bleibt:** 6+ Fragen Median 994 · VS 716 · 4-Trap 251 · Wahr/Falsch 143. Musik: game-show Median 622 > world-trip 449 > brain-pulse 316.
- **Longs:** Flag-30 10 Views n. 0,9 T, Solar-30 4, Capitals-30 16 → 30-Fragen-Text-Longs bleiben tot; E13 (Karten-/Emoji-Long) hängt an pgaClOjxsBw (10.11.), movie-emoji (12.11.), country-emoji (14.11.).
- **Konkurrenz:** stärkstes neues Signal = **niedrige Punkt-Hürde** („Can You Score More Than 2?“ QuizNova 425k/72k, „Score Above 5“ Golden Memory 242k) + Rätsel-Longs (Quiz World 519k). Termine: **Fr 13.11. = Freitag der 13.** (bewusst nicht gruselig bespielt), **GTA VI 19.11.** (Take-Two bestätigt), Hunger Games 20.11., Thanksgiving 26.11.

## Konkurrenz-Gewinner heute (competitors.md 10.11. + outliers.md, letzte 30 Tage)

| # | Video (Kanal, Abos) | Views | × Median | Länge | Titel-Muster | Was wir übernehmen → Slot |
|---|---|---|---|---|---|---|
| 1 | "10 Tricky IQ Riddles / Test Your Intelligence!" (Quiz World, 1.080) – 22.10. | 519.172 | 277× | 6:48 | Zahl + „Tricky“ + IQ, kein Emoji | „Tricky“ lief 10.11. im 6-Q; Rätsel-Long mit cardText-Zahlenfolgen bleibt Backlog #2 (nach E13-Verdict 21.11.) |
| 2 | "Can You Score More Than 2? Test For Ages 70-95!" (QuizNova, 1.380) – Okt. | 425.160 | 308× (Outlier) / 35× (60-90er-Version 72k) | 6:42 | **Extrem niedrige Punkt-Hürde** + Alter | Alter ist bei uns verboten → nur die Hürde übernehmen: erlaubtes 7-Min-Experiment „Can You Score 3/12?“ – unsere 2 Versuche (4/12, 5/15) hatten 0 Views, aber als Text-Allgemeinwissen. Neu: Hürde am **visuellen** Format (Emoji/Karten) → Backlog #3 |
| 3 | "You're Not Smart Enough to Solve These 12 Puzzles!" (Quiz Guy, 491) – 15.10. | 84.710 | 73× | 8:15 | Provokation + 12 | Provokations-Titel als späterer 6-Q-Titeltest (eine Variable) → Backlog #6 |
| 4 | "Name a European city that starts with..." (Chauncey Asks, 5.400) – Short 15.10. | 908.783 | 25× | 1:55 | Europa-Geo, offene Frage | Geo = unser Bestes → **13.11. 16:00 6-Q „Europe Quiz“** (unsere Fragen, Multiple Choice) |
| 5 | "English QuizZ iq test time" (Math Quiz, 2.160) – Short 02.11. | 108.561 | 27× | 1:20 | IQ-Etikett auf Wortquiz, Serie | Wortschatz floppte bei uns (147) → nicht übernehmen; Lehre: Serien-Titel mit gleichem Muster funktionieren (wie unser „Only Geniuses Get 6/6“) |

Nicht übernommen: Playbill/Airline-Livery (Marken), F1 Google Earth (Satellitenbilder unlizenziert), Disney-Songs/Gabby (Rechte), Anime-Zeichnungen, Would-You-Rather (kein Quiz, nicht renderbar).

## 3-Tage-Plan

Layout: **Shorts = atlas** (keine Emojis/Maskottchen/KI-Clips im Bild, Bild nur `broll` – darf Antwort nicht verraten – oder `image` aus image-credits.json), **Longs = tvshow bzw. TrueSizeLong**. Fakten vor dem Schreiben prüfen. Gegen `queue/done/*` greppen (keine Wiederholung von Fragen/VS-Paaren).

| Datum / Slot | Format | Thema | Arbeitstitel (YouTube) | Fragen + timing | Hook / Frage 1 | Musik | cardColors | Thumbnail A/B/C + Foto | Warum | Erfolgskriterium |
|---|---|---|---|---|---|---|---|---|---|---|
| 11.11. Long | **kein Long** (Mi) | – | – | – | – | – | – | – | Longs 2.0 nur Di/Do/Sa | – |
| 11.11. Short 16:00 | 6-Q atlas (Queue) | Flaggen | Only Geniuses Get 6/6 🧠 Flag Quiz | 6 (Queue) | Queue | game-show | – | – | Exploit Geo + 6-Q (Median 994) | ≥800 n. 3 T |
| 11.11. Short 21:00 | VS atlas (Queue) | Kälte | Which Is Colder? 4 Rounds 90% Get #2 Wrong 🥶 | 4 (Queue) | Queue | world-trip | – | – | Exploit VS (Median 716) | ≥700 n. 3 T |
| 12.11. Long 14:00 | Emoji-Long QuizLong tvshow (Queue) | Filme per Emoji | Guess the Movie by Emoji: 30 Rounds From Easy to Legend 🎬 | 30 (Queue) | Queue | game-show | violett/gold | A "GUESS THE MOVIE" + DeLorean / B "25/30" / C "LEGEND LEVEL" | E13 + Quiz Bunny 694k (119×), Quibby 391k (1.228×) | E13: ≥30 n. 3 T |
| 12.11. Short 16:00 | VS atlas (Queue) | Alter | Which Is Older? 4 Rounds 90% Get #2 Wrong 🏛️ | 4 (Queue) | Queue | world-trip | – | – | Exploit VS | ≥700 n. 3 T |
| 12.11. Short 21:00 | 6-Q atlas (Queue), gepaart mit Movie-Long | Filme | Only Geniuses Get 6/6 🧠 Movie Quiz | 6 (Queue) | Queue | game-show | – | – | **Experiment Thema Filme** | ≥600 n. 3 T; <400 → Filme nur als Long |
| **13.11. Long** | **kein Long** (Fr) | – | – | – | – | – | – | – | Regel Longs 2.0 | – |
| **13.11. Short 16:00 (NEU)** | 6-Q atlas | Europa-Geografie (leicht → Falle) | **Only Geniuses Get 6/6 🧠 Europe Quiz** (+ #shorts) | 6, count 2.5 / tail 0.8, 4 Optionen, Antworten ≤ 3 Wörter | Q1 "Which country is shaped like a boot?" → Italy. Q2 "Which river flows through Vienna, Budapest and Belgrade?" → Danube. Q3 "Which of these countries does NOT border Germany?" (Austria/Poland/Hungary/Denmark) → Hungary. **#4 Falle: "What is the smallest country in Europe?" → Vatican City** (Falle Monaco). Q5 "Which is the northernmost capital of a sovereign country?" (Helsinki/Oslo/Reykjavik/Stockholm) → Reykjavik. Finale: "Which country has the most people in the EU?" (France/Italy/Germany/Spain) → Germany. Doppelte gegen six-q-genius-capitals / six-q-quick-geo prüfen und ggf. ersetzen | game-show | – (atlas) | – (Short); broll: Q1 "Mediterranean coastline", Q2 "river bridge city", Q3 "European border sign", Q4 "St Peter's Square" ✗ (verrät) → "small European old town", Q5 "snowy harbour", Q6 "European parliament flags" | **Exploit** Geo-6-Q (Capitals 1.019, Quick Fire Geo 994) + **Konkurrenz #4** Chauncey 909k | ≥800 n. 3 T |
| **13.11. Short 21:00 (NEU)** | VS atlas (AtlasCompareScene, Balken mit echten Werten) | Bevölkerung Runde 3 | **Which Country Has More People? Round 3 – 90% Fail 👥** (+ #shorts) | 4 Runden, count 3.0 / tail 1.2 | R1 Egypt (~116 Mio.) vs Germany (~84 Mio.) → Egypt. **R2 Falle: Bangladesh (~173 Mio.) vs Russia (~144 Mio.) → Bangladesh.** R3 Canada (~41 Mio.) vs Poland (~37 Mio.) → Canada. Finale: Nigeria (~230 Mio.) vs Brazil (~212 Mio.) → Nigeria. Werte = UN WPP 2024 Schätzung 2025, in Beschreibung als Quelle; Gewinnerseite abwechseln; Paare gegen vs-population-1 / vs-more-people-2 greppen | world-trip | – | – | **Exploit stärkstes VS** (More People 1.188 + 1.072, stayed 61 %/53 %) – Serie mit „Round 3“ wie Konkurrenz-Serien | ≥800 n. 3 T |

Vorschau Sa 14.11. (Long-Tag, damit morgen nichts fehlt): Long 14:00 country-emoji-30-1 (Queue). Short 16:00 **Experiment Thema Tiere**: „Only Geniuses Get 6/6 🧠 Animal Quiz“ (Blauwal größtes Tier, Spinne 8 Beine, Kolibri fliegt rückwärts, **#4 Falle Eisbär-Haut = schwarz**, Oktopus 3 Herzen, Fledermaus einziges echt fliegendes Säugetier; game-show) – Konkurrenz Quiz Dolphy Animal 177k (110×), Nature-Quiz 866; Kriterium ≥600 n. 3 T. Short 21:00 gepaart mit Country-Emoji-Long: **Karten-VS „This Map Is Lying To You #2“**, falls map-lie-1 im heutigen Snapshot ≥436 Views n. 24 h hat, sonst 6-Q „Only Geniuses Get 6/6 🧠 Capital Cities Quiz #2“.

Bandit 11.–13.11.: Exploit 6 (Flags, Colder, Older, Emoji-Long, Europe-6-Q, VS People R3) / Experiment 1 (Movie-6-Q) + Querschnitt atlas (E12) und Longs 2.0 (E13) → bewusst exploitlastig nach der 08./09.11.-Delle; Sa 14.11. wieder 2 Experimente (Tiere, Karten-VS #2).

## Ideen-Backlog (nach erwartetem Potenzial)
1. **GTA VI (19.11., Take-Two bestätigt): 6-Q „Only Real Fans Get 6/6 🎮 GTA Quiz“ Do 19.11. 21:00** – größte Gaming-Suchspitze des Jahres; nur Textfakten (Vice City = Miami-Vorbild, GTA III 2001 / GTA V 2013), keine Spielbilder/Logos/Gewaltfragen.
2. **Long „Can You Solve These 10 Tricky Riddles?“ (~7 min, Zahlenfolgen/Muster als cardText)** – Quiz World 519k (277×), Quiz Guy 85k, Puzzle Code 66k; nach E13-Verdict 21.11.
3. **Low-Hurdle am visuellen Long: „Guess the Country by Emoji – Can You Get 5/20?“** – QuizNova 425k / Golden Memory 242k („Score Above 5“); eine Variable (Titel) gegen das Emoji-Long vom 14.11.
4. **Hunger Games: Sunrise on the Reaping (20.11.): 6-Q „Only Real Fans Get 6/6 🏹 Hunger Games Quiz“** – Buchfakten, keine Filmstills.
5. **Thanksgiving Do 26.11.: Long „Guess the Thanksgiving Food by Emoji“ + 6-Q 21:00** – Trends „thanksgiving trivia“ +350 %; bestes Fragen-Long war ein Event (186).
6. **6-Q-Titeltest „You're Not Smart Enough to Get 6/6 🧠 …“** – Quiz Guy 85k/41k/38k; eine Variable gegen „Only Geniuses“.
7. **Karten-Long Folge 2 Sa 21.11.: „The True Size of US States vs Countries“** (California nachtragen) – „country guess the country“ Autocomplete 4,2.
8. **VS „Which Country Is Bigger? Round 2“ (atlas)** – VS Bigger 876, Trends-Breakout „which is bigger“.
9. **Long „Guess the Animal by Emoji: 30 Rounds“** – „animal quiz on youtube“ 2,6, Trends +130 %; nach Animal-6-Q-Ergebnis.
10. **True/False-6-Q „True or False? 6 Geography Facts 90% Get Wrong“** – Keyword #1 „true or false quiz“ (17,7), aber eigener T/F-Short 143 → nur als Geo-Version, niedrige Priorität.

Gestrichen: Weltraum (6-Q 229, VS 127, Long 4 – endgültig), Wissenschaft, Wortschatz, Bauwerkshöhen, Krieg/Sprengstoff, Halloween, Freitag-der-13.-Grusel.

## Für den Produktions-Agenten (gilt heute, überschreibt ältere Defaults)
- **Zuerst TECHNIK 1 fixen** (`link_short_to_long` für story.rounds) und 10.11. nachverlinken.
- **Heute produzieren:** six-q-genius-flags 16:00, vs-colder-1 21:00, **kein Long** (Mi).
- **Für 13.11. anlegen:** `2026-11-13-six-q-genius-europe.json` (publishAt "16:00", atlas, game-show) und `2026-11-13-vs-more-people-3.json` (publishAt "21:00", atlas, world-trip) wie in der Tabelle; Werte/Fakten prüfen, Duplikate gegen queue/done greppen. **Kein Long** am Fr.
- Für 14.11. vorbereiten, falls Zeit: `2026-11-14-six-q-genius-animals.json` (16:00) + 21:00-Short nach der Bedingung oben (map-lie-1 ≥436 n. 24 h → Karten-VS #2, sonst Capitals #2).
- Kein Weltraum, kein Halloween/Grusel (auch nicht „Friday the 13th“), Politik, Krieg/Waffen/Sprengstoff, 💥, Alters-Titel, 50-Fragen-Text-Longs, Longs an Mo/Mi/Fr/So.
- E12 (atlas) nach heutigem Snapshot gegen Shorts-24-h-Median ~436 und stayed ~51 % eintragen; wenn beide 10.11.-atlas-Shorts <200 n. 24 h → in learnings.md als Warnsignal notieren (Verdict erst nach 4 Videos).
