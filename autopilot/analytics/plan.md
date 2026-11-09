# Plan – 2026-11-09

## TECHNIK-PROBLEM
1. **Kein Lauf-Fehler** im Log (08.11.: Uploads 06:20–06:37, Kommentare 13:54/15:54/20:57 mit Long-Link, Konkurrenz 25 Kanäle / 132 Gewinner). Analytics-Stand **08.11. 11:31** (17 Abos).
2. **Marker-Regressionstest bestanden → kein Render-Problem:** 6-Q Capitals **819** n. ~20 h, VS More People 2 **741** n. ~15 h (beide ≫ 300). Schlüsselwort-Marker + −14 LUFS bleiben. Der Einbruch 05.–06.11. war Thema (Vocabulary/Gunpowder/Science), nicht Technik.
3. **Standbild:** QA 08.11. Long 9,6 s, 6-Q Space 5,2 s, VS Planets 4,4 s. Ab heute laufen alle Shorts im neuen **stick**-Layout (Besitzer 08.11.) → QA longestFreezeSec der ersten stick-Shorts prüfen; Gedankenblasen-Countdown muss sich bewegen. Wenn > 4 s in einem Short → neu rendern statt hochladen. Longs: 9,6 s ist zu lang → während Denkzeit Countdown-Ring/Puls sichtbar animieren.
4. **Experiment-Kollision:** Das stick-Experiment heißt in learnings.md „E9“, E9 ist aber schon Space-6-Q. → stick-Test ab jetzt **E11** (in experiments.md angelegt).
5. keywords.md noch vom 02.11. (Montags-Refresh steht heute an) – im Produktionslauf prüfen, dass der Refresh läuft; wenn nicht, im Log vermerken.
6. Risiko GitHub-Actions-Minuten (2.000/Monat) bleibt – bei "spending limit" Besitzer informieren.

## Zusammenfassung (Deutsch)
- **Reichweite ist zurück:** "Only Geniuses Get 6/6 🧠 Capital Cities" 819 Views nach <1 Tag (Shorts-Median 436), VS "Which Country Has More People?" 741 nach ~15 h. Leichte Fragen + bewährter Titel funktionieren wieder → Exploit unverändert: **VS 21:00, 6-Q „Only Geniuses“ 16:00**.
- **Themen-Flops bestätigt:** Science-6-Q 157 (1,8 T), VS Taller 380 (1,6 T, Ziel 500 ✗ vorläufig), Vocabulary 146 final. Wissenschaft/Wortschatz bleiben raus; Bauwerks-Höhen schwächer als Länder/Einwohner.
- **Longs:** E8 #1 Capitals-30 = **7 Views n. ~22 h** – bestes Long seit 31.10., aber Long-Median nur 6. History-50 @19:00 (E7) 0 Views in 3 Snapshots → **E7 gestoppt, 14:00 bleibt**. E8-Verdict 12.11.
- **Neu ab heute:** alle Shorts im Besitzer-Layout **stick** (Strichmännchen, Notizbuch). Das ist eine zweite Variable neben Thema → als E11 messen (Ziel: erste 4 stick-Shorts im Median ≥ 436 Views n. 24 h).
- Konkurrenz: weiterhin dominiert „IQ/Rätsel in ~7 min“ (Quiz World 518k, Clear Think 242k Part 2) – nach E8-Verdict testen wir ein 10–12-Rätsel-Long.

## Konkurrenz-Gewinner heute (competitors.md 08.11., letzte 30 Tage)

| # | Video (Kanal, Abos) | Views | × Median | Länge | Titel-Muster | Was wir übernehmen → Slot |
|---|---|---|---|---|---|---|
| 1 | "10 Tricky IQ Riddles / Test Your Intelligence!" (Quiz World, 1.080) – 22.10. | 518.524 | 277× | 6:48 | Zahl + „Tricky“ + IQ-Versprechen, kein Emoji | „Tricky“ ist schon im 10.11.-6-Q-Titel. Long-Version „10 Tricky Riddles“ = Backlog #2 (nach E8-Verdict 12.11.) |
| 2 | "Test Your IQ Level in just 8 Min (Part 2)" (Clear Think, 6.720) – 13.10. | 242.074 | 265× | 8:09 | IQ + Zeitversprechen | Länge 7–8 min (E8) bestätigt; Zeit-Titel = Backlog #3 |
| 3 | "🧠 Your Brain Is Ageless! Take This 10-Question IQ Quiz" (GK STUDIO PRO, 1.880) – 27.10. | 44.388 | 48× | 7:14 | Kompliment-Hook + kleine Fragenzahl | Kleine Fragenzahl + 7 min = E1-Struktur (bei uns gestoppt, 0/0/1). Nicht vor E8-Verdict; Alters-Anspielung meiden |
| 4 | "Name a European city that starts with..." (Chauncey Asks, 5.030) – Short 15.10. | 881.126 | 28× | 1:55 | Wortspiel/Anfangsbuchstabe, Geografie | Geografie bleibt unser stärkstes Thema → 11.11. 16:00 Flaggen-6-Q (Geo-Exploit). Straßen-Interview-Format können wir nicht rendern |
| 5 | "Can You Score More Than 2? Test For Ages 70-95!" (QuizNova, 1.390) – 10.10. | 430.970 | 197× | 6:42 | sehr niedrige Hürde + Altersgruppe | Alters-Titel bei uns gestoppt (Memory-Long 59/4). Wir übernehmen nur die **sehr niedrige Hürde** – später, als Titel-Variable im E8-Nachfolger |

Nicht übernommen: Playbill/Airline-Livery (Markenrechte), comicnutz (Comic-Figuren), Disney-Songs (Musikrechte), Math-Quiz „English Quizz IQ test“ 85k (Wortschatz = bei uns Flop 146), F1-/Stadion-Google-Earth (Satellitenbilder nicht in image-credits).

## 3-Tage-Plan

Layout: **Shorts = stick** (Besitzer 08.11.), **Longs = tvshow**. Fakten vor dem Schreiben prüfen (Britannica, NASA, NOAA, WMO). Gegen `queue/done/*` greppen. **09.11. + 10.11. liegen fertig in der Queue → nur 11.11. neu anlegen.**

| Datum / Slot | Format | Thema | Arbeitstitel (YouTube) | Fragen + timing | Hook / Frage 1 | Musik | cardColors | Thumbnail A/B/C + Foto | Warum | Erfolgskriterium |
|---|---|---|---|---|---|---|---|---|---|---|
| 09.11. Long 14:00 | E8 #3 (Queue) | Flaggen | Flag Quiz: 30 Questions From Easy to Legend 🚩 | 30 (Queue) | Queue | world-trip | #7F1D1D/#FFF7ED | Queue | E8 | E8-Verdict 12.11. |
| 09.11. Short 16:00 | 6-Q E10 (Queue), stick | Mauerfall-Jahrestag | Only Geniuses Get 6/6 🧠 Berlin Wall Quiz | 6 (Queue) | Queue | game-show | – | – | Jahrestag + E11 | ≥800; <400 → keine Jahrestage um 16:00 |
| 09.11. Short 21:00 | VS #7 (Queue), stick | Gewicht | Which Is Heavier? 4 Rounds 90% Get #2 Wrong 🐘 | 4 (Queue) | Queue | world-trip | – | – | Exploit VS + E11 | ≥700 |
| 10.11. Long 14:00 | E8 #4 (Queue) | Filme per Emoji | Guess the Movie by Emoji: 30 Rounds From Easy to Legend 🎬 | 30 (Queue) | Queue | game-show | Queue | Queue | E8 + Quiz Bunny 689k | E8-Verdict 12.11. |
| 10.11. Short 16:00 | 6-Q (Queue), stick | Allgemeinwissen leicht | Only Geniuses Get 6/6 🧠 Tricky Trivia Quiz | 6 (Queue) | Queue | game-show | – | – | Exploit + Quiz World „Tricky“ | ≥1.000 |
| 10.11. Short 21:00 | VS #8 (Queue), stick | Alter | Which Is Older? 4 Rounds 90% Get #2 Wrong 🏛️ | 4 (Queue) | Queue | world-trip | – | – | Exploit VS | ≥700 |
| **11.11. Long 14:00** | **E8 #5** (letztes E8-Long): QuizLong 30 Runden, 5 Level à 6 EASY→MEDIUM→HARD→VERY HARD→LEGEND, Ziel 7–8 min, Emoji-Format wie movie-emoji-30-1 | Länder per Emoji | **Guess the Country by Emoji: 30 Rounds From Easy to Legend 🌍** (57 Z.) | 30, count 6.0 / tail 1.2, midCtaIndex 14, `fact` bei allen 30 (1 Satz) | Hook "CAN YOU GET 25/30? 🌍"; Q1 sehr leicht: 🍕🍝🛵 → Italy; z. B. 🦘🏄‍♂️ Australia, 🗼🥖 France, 🍁🏒 Canada, 🌮🌵 Mexico, 🍣🗻 Japan … LEGEND z. B. 🧂🏞️🇧🇴-frei: 🦙🧂🏔️ → Bolivia (Salar de Uyuni), 🐉🏔️⚡ → Bhutan („Land of the Thunder Dragon“); **keine Flaggen-Emojis** (verraten Antwort), keine Länder aus dem Emoji-Länder-Short 16.10. und dem Flag-Long 09.11. als identische Hinweise | world-trip | #0F766E / #FEF3C7 | A "GUESS THE COUNTRY" + Foto aus image-credits (Landschaft, die NICHT als Rätsel vorkommt) / B "25/30?" / C "LEGEND LEVEL" | Experiment E8 #5 + Keyword „country guess the country“ (Autocomplete 4,2) + unser Emoji-Länder-Short 937 + Emoji = einziges Long-Muster mit Reichweite (141) | E8: Median ≥10 öffentl. Views n. 3 T über #1–#5 UND Ø angesehen ≥40 % |
| **11.11. Short 16:00** | 6-Q Exploit, stick, ≤50 s | Flaggen (Text-Fragen) | **Only Geniuses Get 6/6 🧠 Flag Quiz** (+ #shorts, 37 Z.) | 6, count 2.5 / tail 0.8, 4 Optionen, Antworten ≤ 4 Wörter | Q1 sehr leicht: "Which country's flag has a red maple leaf?" → Canada. Dann z. B.: "How many stars are on the US flag?" → 50; "Which flag is NOT a rectangle?" → Nepal (nur wenn nicht schon im Flag-Long – sonst Schweiz quadratisch); **#4 Trick: "Which country's flag has a dragon?" → Bhutan** (Fallen Wales/China/Vietnam – Wales ist kein Land mit UN-Sitz, Antwort eindeutig Bhutan, Wales nicht als Option!); "What colour is the circle on Japan's flag?" → Red; Finale: "Which two countries have almost identical flags?" → Chad & Romania NUR wenn nicht im Flag-Long-Finale (laut Queue ist es dort Finale → ersetzen durch "Indonesia & Monaco") | game-show | – (stick) | – (Short), cardText-Emoji je Frage nicht verratend (🍁 NICHT bei Q1 → 🗺️) | Exploit 6-Q leicht (819/975/1.203) + Geo = bestes Thema + Question Time „Only 5% can name these flags“ 188k | ≥800 Views n. 3 T |
| **11.11. Short 21:00** | VS #9, stick, CompareScene (values) | Kälte | **Which Is Colder? 4 Rounds 90% Get #2 Wrong 🥶** (+ #shorts, 46 Z.) | 4, count 3.0 / tail 1.2, correctLabel "COLDER!", valueLabels "°C" (Balken = Kälte als positiver Wert, Label zeigt echtes Minus) | R1 leicht: South Pole Station Winter-Ø ≈ −60 °C vs North Pole Winter-Ø ≈ −40 °C → Süd; **R2 Haken: Mars Ø ≈ −63 °C (NASA) vs Erdrekord Vostok −89,2 °C (WMO, 1983)** → Erde kälter; R3: Yakutsk Jan-Ø ≈ −39 °C vs Ulaanbaatar Jan-Ø ≈ −22 °C; R4 Finale: Uranus min ≈ −224 °C vs Neptun ≈ −214 °C (NASA, kälteste Planetenatmosphäre = Uranus) | world-trip | – (stick) | – | Exploit VS (Median der VS ≈ 750, bestes Format nach stayed 55,7 %) + Backlog #2 von gestern | ≥700 Views n. 3 T |

Bandit 09.–11.11.: Exploit 6 (VS ×3, 6-Q leicht ×2, + Berlin-6-Q-Format) / Experiment 3 (E8 ×3) + Querschnitts-Experiment E11 stick (Besitzer-Vorgabe) ≈ 67/33.

## Ideen-Backlog (nach erwartetem Potenzial)
1. **GTA VI (Release 19.11.2026, Take-Two bestätigt): 6-Q "Only Real Fans Get 6/6 🎮 GTA Quiz" 18./19.11. + Long "GTA Quiz: 30 Questions…" 17.11.** – größte Gaming-Suchspitze des Jahres; nur Textfakten (Vice City = Miami, Release-Jahre der Teile), keine Spielbilder/Logos, keine Waffen-/Gewaltfragen.
2. **Long "10 Tricky Riddles – Can You Solve 4?" (~7 min)** – Quiz World 518k (277×), Quiz Guy 84k/41k/38k; nach E8-Verdict 12.11.; Riddle als Frage + 4 Optionen.
3. **Long-Titeltest "Test Your General Knowledge in Just 7 Minutes"** – Clear Think 1,7 Mio + 242k; Zeitversprechen statt Score-Hürde, eine Variable.
4. **VS "Which Is Longer?" (Flüsse/Brücken/Grenzen)** – VS-Format, nur unstrittige Paare (nicht Nil vs Amazonas).
5. **6-Q "Only Geniuses Get 6/6 🧠 Europe Quiz"** – Chauncey Asks „European city that starts with…“ 881k; Geo bleibt bestes Thema.
6. **VS "Which Is Deeper?" (Seen/Ozeangräben/Minen)** – VS-Variante, Haken Baikal vs Tanganjika.
7. **Hunger Games: Sunrise on the Reaping (Kinostart 20.11.)** – 6-Q "Only Real Fans Get 6/6 🏹 Hunger Games Quiz" 19./20.11.; nur Buch-/Filmfakten als Text.
8. **Thanksgiving 26.11.: 6-Q "Only Geniuses Get 6/6 🦃 Thanksgiving Quiz" + Long** – US-saisonal; Halloween-35 war bestes Fragen-Long (186).
9. **Long "Guess the Animal by Emoji: 30 Rounds"** – Emoji = einziges Long-Muster mit Reichweite; nur wenn E8 positiv.
10. **Remembrance/Veterans Day nächstes Jahr bzw. Armistice-Fakten** – heuer bewusst übersprungen: Krieg ≈ Gewalt-Thema, nach Gunpowder-Unterdrückung (1 View) zu riskant.

## Für den Produktions-Agenten (gilt heute, überschreibt ältere Defaults)
- **3 Items für 11.11.** anlegen: `2026-11-11-country-emoji-30-1.json` (Long, publishAt "14:00", layout tvshow, Emoji-Format wie movie-emoji-30-1), `2026-11-11-six-q-genius-flags.json` (publishAt "16:00", layout stick), `2026-11-11-vs-colder-1.json` (publishAt "21:00", layout stick, Kälte-Werte als positive Balkenlänge, Label mit Minus).
- **Layout-Regel ab heute:** Shorts **stick** (Besitzer 08.11., überschreibt „tvshow für alles“), Longs **tvshow**. LTX für Shorts aus (kostenlos); jede stick-Frage braucht ein nicht verratendes cardText-Emoji (nie ❓).
- **E11-Abbruchregel (stick):** Wenn die ersten 4 stick-Shorts (09.+10.11.) nach 24 h **alle** unter 436 Views liegen UND Ø stayed < 45 %, VS-Shorts zurück auf tvshow (VS war Leader im TV-Look), 6-Q bleibt stick, und Besitzer per Nachricht informieren.
- Flaggen-6-Q: gegen `queue/2026-11-09-flag-quiz-30-1.json` greppen – keine Frage doppelt zum Flag-Long.
- 6-Q-Fragen leicht halten, nur #4 ist die Fangfrage. Keine Wissenschafts-/Wortschatz-/Bauwerkshöhen-Themen in Shorts.
- Kein Sprengstoff/Waffen/Krieg/Anschlag, kein 💥, keine Politik, kein Halloween, keine Alters-Titel, keine E1-Longs, kein 19:00-Long (E7 gestoppt).
- Standbild Shorts ≤ 3 s (QA > 4 s → neu rendern). Shorts-Kommentar 11.11. verlinkt aufs Country-Emoji-Long.
