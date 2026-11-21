# Plan – 2026-11-21 (Sa)

## TECHNIK-PROBLEM (zuerst erledigen)
1. **22.11.-Items fehlen in `autopilot/queue/`** (nur die drei 21.11.-Items liegen dort). Heute ZUERST 22.11. anlegen (16:00 + 21:00), danach 23.11. und – neu – schon das Rätsel-Long für Di 24.11.
2. **map-lie-6 ohne neue Formen:** zimbabwe/kenya/indonesia fehlen weiter in `src/data/truesize.json`. Damit es heute nicht blockiert, nutzt map-lie-6 nur **vorhandene** Formen (siehe Tabelle). Neue Formen sind kein Muss mehr.
3. **Layout-Umstellung kam am 20.11. zu spät:** `six-q-genius-iq-pop` wurde 06:27 noch mit pop gerendert, die Umstellung auf tvshow erfolgte erst 07:30. → Layout-Änderungen an Queue-Items immer VOR dem Dispatch committen.
4. Thumbnail-CTR per API weiter HttpError 400 (bekannt). Kosmetik: scoreboard.md führt Karten-Longs als „0 Fragen“.
5. Still Sharp Trivia (Thanksgiving-/Christmas-Gewinner, 498 Abos) ist NICHT in competitors.json – Kanal-ID ließ sich per Websuche nicht finden. Falls der Produktions-Agent sie per YouTube-API (search → channelId) bekommt: `{"id": "UC…", "name": "Still Sharp Trivia", "source": "research"}` eintragen.

## Zusammenfassung (Deutsch)
- **Neuer Long-Gewinner: Rätsel-Long (E14)** „Test Your IQ: 12 Tricky Riddles – Can You Solve 4?“ hat **172 Views nach ≈1,1 Tagen** – Long-Median sonst ~8, bisher bestes Long 186 (Halloween). Ziel ≥ 50 n. 3 T schon erreicht → **E14 ✓ (vorzeitig)**. Konsequenz: Rätsel-Long bekommt jeden Di, Christmas-Long Do, Sa frei für Feiertag/Rätsel.
- **Shorts erholen sich durch ≤ 45 s + neue Titel (E17):** Capitals 1.032 (38 s), Tricky-2 962 (41 s), Geo-Trivia 948 (43 s, neues Titelmuster), Quick IQ Test 447 nach nur ≈4 h. Vor der Kürzung (11.–16.11.) Median ≈160.
- **Warnsignal Karten-VS:** map-lie-3 nur **238 nach ≈23 h** (#1 1.021, #2 936). Noch kein Abbruch – aber wenn #4 und #5 nach 3 Tagen auch < 500 liegen, wird 21:00 ab 26.11. abwechselnd Karten-VS / Mehrfragen-Short.
- Layout ist geklärt: tvshow für alles (Owner-Pflicht); der Hebel sind Länge + Titel, nicht das Layout.

## Konkurrenz-Gewinner heute (competitors.md 20.11., Upload in den letzten 30 Tagen)

| # | Video (Kanal, Abos) | Views | × Median | Länge | Titel-Muster | Was wir übernehmen → Slot |
|---|---|---|---|---|---|---|
| 1 | „10 Tricky IQ Riddles / Test Your Intelligence!“ (Quiz World, 1.080) – 22.10. | 520.502 | 277,6× | 6:48 | Zahl + „Tricky“ + IQ, ohne Hürde | Bestätigt unser E14 → **Di 24.11. Rätsel-Long #2** (12 neue Rätsel, ~7 min) |
| 2 | „🧠 Your Brain Is Ageless! Take This 10-Question IQ Quiz…“ (GK STUDIO PRO, 1.950) – 27.10. | 46.252 | 49,6× | 7:14 | Fragenzahl + IQ + „Test Your Mind“ (Alters-Anspielung lassen wir weg) | Titel-Baustein „10-Question IQ Quiz“ als Titel-Variante für Rätsel-Long #3 (Sa 28.11.) |
| 3 | „ARE YOU A GENIUS? Prove It By Scoring 5 Out Of 25 On This Extreme IQ Test!“ (QuizNova, 1.420) – 28.10. | 22.675 | 19,1× | 8:21 | **niedrige Hürde 5/25** + Genie-Ego | Hürden-Mechanik bleibt: „Can You Solve 5?“ im Rätsel-Long #2 |
| 4 | „English QuizZ iq test time“ (Math Quiz, 2.770) – 02.11. | 122.944 | 25,0× | 1:20 | Short, Wortschatz als „IQ-Test“ | Backlog: Vokabel-Short mit IQ-Titel (unser Vocab-Short 148 lief mit neutralem Titel) |
| 5 | „Can You Name F1 Track From Above? — Part 3“ (Dopamine Quiz, 443) – 31.10. | 30.289 | 42,2× | 8:50 | Serie mit Teil-Nr. | Serien-Nummer bei Karten-VS („#6“, „#7“) und Rätsel-Long („Part 2“ nicht nötig – eigener Titel) |

Nicht übernommen: „Brain Exam for Seniors“ (QuizNova 57,6k – Alters-Titel verboten), Would-You-Rather (Quiz Dolphy – kein Render-Baustein), Fußball/F1/Disney/Stimmen (Bild-/Musikrechte).

## 3-Tage-Plan

| Datum / Slot | Format | Thema | Arbeitstitel (YouTube) | Fragen + timing | Hook / Fragen | Musik | cardColors | Thumbnail / Bild | Warum | Erfolgskriterium |
|---|---|---|---|---|---|---|---|---|---|---|
| **21.11. (Sa) Long 14:00** | QuizLong tvshow v2 (liegt in Queue) | Thanksgiving | Thanksgiving Trivia Quiz 🦃 50 Questions – Can You Get 40? | 50, count 5 / tail 1.2 | Queue (unverändert) | Queue | Queue | Queue (🦃, v2) | Konkurrenz Still Sharp 65,3k (130,6×) | ≥ 60 n. 3 T, ≥ 150 bis 27.11. |
| 21.11. Short 16:00 | 6-Q (Queue) | Zeitachsen | Which Came First? Only 1 in 10 Get All 6 ⏳ | Queue (59 Wörter) | Queue | game-show | Queue | – | Exploit Titeltyp (Median 698) | ≥ 700 n. 3 T |
| 21.11. Short 21:00 | Karten-VS (Queue) | map-lie-5 | This Map Is Lying To You #5 🌍 Which Is REALLY Bigger? | 4 Runden | Queue | world-trip | – | – | Exploit (E17) | ≥ 800 n. 3 T |
| **22.11. (So) Long** | – | – | kein Long (LONG_DAYS Di/Do/Sa) | – | – | – | – | – | – | – |
| 22.11. Short 16:00 – HEUTE ANLEGEN | 1-Frage-Ego-Hook, tvshow | US-Geo-Falle | **Which City Is Further West? 9 in 10 Get It Wrong 🤯** (+ #shorts) | 1 Frage, count 4 / tail 1.0, ≤ 35 Wörter | „Which city is further WEST?“ Los Angeles / **Reno** / Las Vegas / Phoenix → Reno (≈119,8° W vs. LA ≈118,2° W). Antwort: „Reno! Yes, really.“ (Reno noch nie benutzt – gegrept) | game-show | ["#1D4ED8","#1E3A8A"] | cardText „🧭⬅️“ | Exploit kürzestes Format (1-Frage-Median 622, Bestes 1.208) + 75 % US-Publikum | ≥ 600 n. 3 T |
| 22.11. Short 21:00 – HEUTE ANLEGEN | Karten-VS `story.type "truesize"` | map-lie-6, nur vorhandene Formen | **This Map Is Lying To You #6 🌍 Which Is REALLY Bigger?** (+ #shorts) | 4 Runden, kicker „MAP TEST #6“, ≤ 55 Wörter | R1 **Algeria** 2,381,741 vs Greenland 2,166,086 (+10 %, Twist) · R2 **Madagascar** 587,041 vs Spain 505,370 (+16 %) · R3 **New Zealand** 268,838 vs UK 243,610 (+10 %) · R4 **Mongolia** 1,564,116 vs Peru 1,285,216 (+22 %). Kontrollspalte muss jede Seite stützen, sonst Paar tauschen gegen Cuba/Iceland | world-trip | – | – | Exploit E17, Serie (Konkurrenz #5) | ≥ 800 n. 3 T; < 500 → Warnsignal zählt |
| **23.11. (Mo) Long** | – | – | kein Long | – | – | – | – | – | – | – |
| 23.11. Short 16:00 – HEUTE ANLEGEN | **EXPERIMENT E18: Wahr/Falsch** (Mehrfach-Antwort „True“/„False“ + 2 Füller, oder 2 Optionen), tvshow | Thanksgiving-Fakten (verlinkt das Long) | **Thanksgiving True or False 🦃 90% Get #4 Wrong** (+ #shorts) | 6 Aussagen, count 2.5 / tail 0.6, ≤ 70 Wörter | 1 „Wild turkeys can fly.“ True · 2 „The first Thanksgiving lasted one day.“ False (3 Tage) · 3 „Canada's Thanksgiving is in October.“ True · 4 Falle „Turkeys come from the country Turkey.“ False (Nordamerika) · 5 „Lincoln made Thanksgiving a national holiday.“ True · 6 „Only male turkeys gobble.“ True. ACHTUNG: alle Fakten stehen auch im Long – im Short andere Wortwahl, Antwortzeile nur „True!“/„False!“ + max. 4 Wörter | game-show | ["#B45309","#7C2D12"] | cardText „✅❌“, „🦃“ | Experiment Format T/F: „true or false quiz“ = Autocomplete-Platz 1 (Score 17,1); einziger alter T/F-Short 145 (atlas, lang) | ≥ 500 n. 3 T (eine Variable: Format; Thema = Feiertagswoche) |
| 23.11. Short 21:00 – HEUTE ANLEGEN | Karten-VS | map-lie-7, vorhandene Formen | **This Map Is Lying To You #7 🌍 Which Is REALLY Bigger?** | 4 Runden | R1 **Chile** 756,102 vs Texas 695,662 (+9 %, Twist: schmale Form) · R2 **California** 423,970 vs Japan 377,915 (+12 %) · R3 **Cuba** 110,860 vs Iceland 103,000 (+8 %) · R4 **Cambodia** 181,035 vs Florida 170,312 (+6 %) – Kontrollspalte prüfen; Paar < 5 % in der Kontrollspalte → durch Madagascar/France ersetzen NICHT (zu knapp), dann Kazakhstan/Argentina auch nicht (2 %) – lieber 3 Runden | world-trip | – | – | Exploit E17 | ≥ 800 n. 3 T |
| **24.11. (Di) Long 14:00 – HEUTE SCHON ANLEGEN** | QuizLong tvshow v2, Rätsel-Muster wie `iq-riddles-12-1` | 12 neue Logik-/Wort-Rätsel | **Test Your IQ: 12 Hard Riddles – Can You Solve 5? 🧠** | 12, Denkzeit count ≤ 12 (nicht 20 – Standbild-QA), tail 1.5 → ~6–7 min | Hook „Most people solve three. Can you solve five?“ · Rätsel frisch schreiben, Duplikat-grep gegen iq-riddles-12-1 und alle 6-Q-IQ-Shorts (17 Schafe, 1/8, O-T-T-F, Ziegel, Handschläge schon benutzt). Stufen EASY 1–3 / MEDIUM 4–7 / HARD 8–10 / LEGEND 11–12 | brain-pulse | ["#5B21B6","#1E1B4B"] | A „TEST YOUR / IQ“, B „CAN YOU / SOLVE 5?“, C „ONLY 1% / SOLVE 12“; `thumbPuzzle` aus Rätsel 6 (2–3 Emojis); Badge „12 RIDDLES“ | Exploit E14 (172 n. 1,1 T) + Konkurrenz #1/#3 | ≥ 100 n. 3 T |

**Vorschau (nicht heute anlegen):** Do 26.11. Long „Christmas Quiz for Adults 🎄 Can You Get 40/50?“ (Still Sharp 62,9k; Thanksgiving-Tag selbst schwach für US-Publikum, aber Christmas-Suche startet) · Sa 28.11. Rätsel-Long #3 „10-Question IQ Quiz: Only 1% Get 10/10 🧠“ · Black-Friday 27.11. 16:00 „Which Costs More?“ nur mit Listenpreisen.

Bandit 21.–23.11. (9 Slots): 7 Exploit/Konkurrenz-Muster (Thanksgiving-Long, Which-First, 1-Frage-Hook, Karten-VS ×3, Rätsel-Long vorproduziert), 1 Experiment (E18 Wahr/Falsch) ≈ 15 % – bewusst niedrig, weil die Shorts sich gerade erst erholen.

## Ideen-Backlog (nach erwartetem Potenzial)
1. **Rätsel-Long jede Woche (Di)** – E14 172 n. 1,1 T; Quiz World 520k, Clear Think 1,87 Mio („Test Your IQ in 7 minutes“).
2. **Christmas Quiz for Adults (Do 26.11.)** – Suchphrase „christmas quiz“; Still Sharp 62,9k (125,9×).
3. **„Tricky Trivia“-Short alle 4–5 Tage** – 1.555 + 962 Views, beide ≤ 48 s.
4. **„X Trivia: 90% Get #4 Wrong“-Titelmuster** – Geo-Trivia 948 n. 1 T; auf Science/History übertragen.
5. **Christmas-Short-Serie ab 29.11. (1. Advent)** – Feiertagssuche, verlinkt Christmas-Long.
6. **IQ-Rätsel-Short (1 Rätsel, ≤ 30 s)** – Quick IQ Test 447 n. 4 h; Konkurrenz-Rätsel-Shorts.
7. **Vokabel-Short mit IQ-Titel („English IQ Test: What Does … Mean?“)** – Math Quiz 122,9k (25×).
8. **„Can You Pass the U.S. Citizenship Test?“ Long #2** – Trivia Square 2,79 Mio (74×), Autocomplete-Score 2,2.
9. **Black-Friday-VS „Which Costs More?“ 27.11.** – Event-Suche, nur offizielle Preise.
10. **„Can You Identify These Old Items?“ (Foto-Long)** – Quiz Magnet 739k (93,9×), aber nur mit Fotos aus image-credits.json → erst Bildbestand prüfen.

Gestrichen: Karten-/Emoji-Longs (E13 ✗), pop/atlas, People-/Bigger-/Older-/Colder-VS, Tier-/Europa-/Landmarks-/Film-6-Q, Alters-Titel, Halloween, Weltraum.


## NACHTRAG 21.11. 10:40 – neues Format „Flag Duel“ (Besitzer-Wunsch: Referenz „Wer ist CHINA? Links oder rechts? Countryballs“)
- **Neue Komposition `FlagDuel`** (`src/FlagDuel.tsx`, story.type **"flagduel"**, 9:16): zwei fast gleiche Flaggen auf Papierkarten (tvshow-Farben), darunter zwei 2D-Länder-Bälle, Countdown 3-2-1 mit Anrempeln, Auflösung mit Haken/X + Ländernamen, Gewinner springt, Verlierer wird weggeschubst. Stimme + Zeiten wie Karten-VS über `atlas_voice.py` (timing think 3.0 / move 0.8 / tail 0.35). Flaggen: `public/flags/<iso2>.svg` (alle 270, flag-icons MIT). Muster: `stories/flag-duel-1.json`.
- **E19 Flag Duel:** flag-duel-1 **So 22.11. 16:00** (Poland/Indonesia, Ireland/Ivory Coast, New Zealand/Australia, Chad/Romania), flag-duel-2 **Mi 25.11. 16:00** (Iceland/Norway, Senegal/Mali, Netherlands/Luxembourg, Slovakia/Slovenia). Erfolg: ≥ 800 n. 3 T (Niveau Karten-VS #1/#2). Bei ✓ → Serie „Flag Quiz #N“ 2–3×/Woche auf 16:00.
- Queue verschoben: `one-q-further-west` (Reno) von 22.11. auf **24.11. 16:00** (Dateiname 2026-11-24-…). Für 24.11. fehlt noch das 21:00-Short (map-lie-8) – beim nächsten Lauf anlegen, sonst rutscht flag-duel-2 auf den 24.11.
- Regeln für neue Flag-Duels: nur echte Doppelgänger-Paare (z. B. Monaco/Indonesia NICHT – im 4:3-Bild identisch), Gewinnerseite mischen, ≤ 60 gesprochene Wörter, Antwortzeile = Seite + Unterschied in ≤ 4 Wörtern, Zielname ≤ 11 Zeichen (sonst Schrift zu klein), keine politisch heiklen Paare (Taiwan/China, Kosovo usw.).

## Für den Produktions-Agenten (gilt heute, überschreibt ältere Defaults)
- **Reihenfolge:** (1) 22.11. anlegen: `2026-11-22-one-q-further-west.json` (16:00), `2026-11-22-map-lie-6.json` (21:00); (2) 23.11.: `2026-11-23-true-false-thanksgiving.json` (16:00, E18), `2026-11-23-map-lie-7.json` (21:00); (3) `2026-11-24-iq-riddles-12-2.json` (Long 14:00) – darf heute schon in die Queue, LONG_DAYS sperrt So/Mo, ältestes Long ist dann dieses.
- **Layout tvshow** für alles außer Karten-VS (truesize). Änderungen vor dem Dispatch committen.
- Shorts ≤ 80 gesprochene Wörter (Ziel ≤ 45 s); Antwortzeile nur Antwort + max. 4 Wörter.
- Rätsel-Long: Denkzeit count ≤ 12 s (QA-Standbild), jedes Rätsel muss eindeutig eine Lösung haben – zweimal durchrechnen.
- Fragen frisch schreiben, Fakten prüfen, Duplikat-grep über stories/ + queue/done.
- Weiter verboten: Longs Mo/Mi/Fr/So, 3. Short am Tag, Halloween, Alters-Titel, Politik/Krieg, Weltraum.
- vidIQ heute nicht nötig (Konkurrenzdaten frisch vom 20.11.).
