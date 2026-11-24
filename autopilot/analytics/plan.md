# Plan – 2026-11-24 (Di)

Kanal **43 Abos** (report.json 23.11. 22:31) – **+11 in ≈28 h** (32 → 43) bei ≈4.500 neuen Views ≈ **2,4 Abos/1.000 im aktuellen Fenster** (Ziel 2,0 erstmals erreicht). Analytics gesamt (2–3 T Verzug): 35.881 Views → 26 Abos = 0,72/1.000.
Flag Duel trägt: #1 3.119 Views (+18 Abos), #2 1.155 Views n. ≈6,5 h (≈35 % unter #1 im gleichen Fenster). Karten-VS jetzt messbar ≈1,0 Abos/1.000 (#4/#5 je +1) → bleibt.
Kommentare: 4 offen → alle 4 beantwortet (gesamt 20). Kein Faktenfehler.
Änderungen: Flag Duel #4 (Do 26.11.) testet wieder den #1-Titel mit Folgennummer („Left or Right?“), Flag Duel #5 Sa 28.11.; Sa-Long = Rätsel #3.

## TECHNIK-PROBLEM
- Keine. Log 23.11.: 2 Shorts hochgeladen, Kommentare/Antworten gepostet, Analytics 19:18 + 22:31 ok. Thumbnail-CTR per API weiter HttpError 400 (bekannt, kein Fix nötig).
- Hinweis: `2026-11-26-flag-duel-4.json` (Nachtrag 23.11.) wurde noch NICHT angelegt → heute Pflicht für den Produktions-Agenten.

## Zuschauer
- 28 Kommentare (21 T), 4 offen → beantwortet: @BashyWashy29 4/4, @Wolfy2026-7wc 4/4, @cloudynbarlan6435 3/4 (alle auf Flag Duel #3 heute eingeladen), @nickolawright3724y „4000000/20000000“ (Witz aufgenommen + Frage zurück).
- FEHLER-HINWEIS (1) = „I only got 1 wrong“ (Score, kein Fehler, längst beantwortet).
- 8 von 9 gemeldeten Scores kommen aus Flag Duel → Score-Kommentar-Mechanik wirkt.
- Wünsche: Science (@Jo-wl5fj) Fr 27.11. 16:00 in Queue; Art + classical music Backlog #5/#7.

## Diagnose (Videos ≥ 3 T unter Format-Median)
| Video | Views | Ursache | Fix |
|---|---|---|---|
| Keine neuen Flops ≥ 3 T | – | which-first-3 1.024, map-lie-5 1.002 = im Median | – |
| map-lie-7 (23.11., < 3 T) | 266 n. 1,5 h | zu früh; Beobachten (map-lie-3 fiel wegen Wiederholung) | Verdict 26.11. |
| flag-duel-2 (< 3 T) | 1.155 n. 6,5 h (#1: 1.760 n. 7 h) | Titel „Who Is Slovakia?“ weniger Klick-Neugier als „Left or Right? Only 1 in 10 Get 4/4“ (Hypothese) | #4 mit #1-Titelmuster + Nummer → Vergleich |
| Thanksgiving-Long | 95 n. 3 T | spät gestartet | erledigt (Christmas-Long Do) |
- **KPI Abos/1.000 je Format (Analytics):** Flag Duel ≈ 5,8 (#1, Besitzer-Zahlen) · Longs ≈ 3,8 · Karten-VS ≈ 1,0 · 6+ Fragen ≈ 0,7 · VS ≈ 0,9 · 1-Frage ≈ 0,6 · 4-Fragen-Trap ≈ 0,3 (gestrichen). Karten-VS-Bewährung bestanden (> 0,5).

## Konkurrenz-Gewinner heute (vidIQ outliers „flag quiz“, Shorts, Nov.)
| # | Video (Kanal) | Views / × | Länge | Muster | → Slot |
|---|---|---|---|---|---|
| 1 | „Real Flag or Sneaky Fake? Can You Get 5/5?“ (WonderQ, 4,4k Abos) | 334k / 50× (3.400 Views/h) | 1:16 | echte vs. manipulierte Flagge, Score-Hürde | Backlog #2 „Real or Fake Flag“ (Renderer-Check) |
| 2 | „(1) Flag Quiz Can You Name These 10 Flags?“ (Quizzes Mania, 1k) | 108k / 82× | 1:39 | Serie mit Nummer, 10 Flaggen | bestätigt Folgennummer → „Flag Quiz #4“ |
| 3 | „Guess the correct flag!“ (MB GeoPlay, 15,6k) | 160k / 39× | 0:43 | richtige Flagge aus Varianten | = Flag-Duel-Prinzip, Bestätigung |
| 4 | „Which One Is MALAYSIA? Left or Right?! 4 Levels…“ (ThinkBop!, 2,4k) | 22,6k / 13× | 0:26 | exakt Flag-Duel-Struktur, Levels im Titel | Titel #4: „Left or Right?“ zurück (eigene Formulierung) |
| 5 | „Test Your iQ in just 7 minutes“ (Clear Think) | 1,88 Mio / 1.518× | 6:48 | Zeit + IQ, ~7 min Rätsel | Rätsel-Long Sa 28.11. |
- Events: Black Friday Fr 27.11. (Backlog), **1. Advent So 29.11.** → Advent-Serie ab 1.12.

## 3-Tage-Plan
| Datum / Slot | Format | Thema | Titel (YouTube) | Fragen + timing | Hook / Fragen | Musik | cardColors | Thumbnail | Warum | Erfolg |
|---|---|---|---|---|---|---|---|---|---|---|
| 24.11. Long 14:00 (Queue) | QuizLong exam, 12 Rätsel | IQ-Rätsel #2 | Test Your IQ: 12 Hard Riddles – Can You Solve 5? 🧠 | 12 | Queue | brain-pulse | Queue | B zuerst „F“ + „CAN YOU SOLVE **5**?“ | Exploit + erster exam-Look | ≥ 100 n. 3 T, ≥ 1 Abo |
| 24.11. 16:00 (Queue) | Flag Duel #3 | Austria/Latvia, Colombia/Ecuador, Haiti/Liechtenstein, Qatar/Bahrain | Flag Quiz: Who Is Qatar? 90% Pick Wrong 🌍 | 4 | Queue | game-show | – | – | Exploit E21 | ≥ 1.000 n. 3 T |
| 24.11. 21:00 (Queue) | Karten-VS #8 | Queue | This Map Is Lying To You #8 🌍 … | 4 | Queue | world-trip | – | – | Exploit | ≥ 800 |
| 25.11. 16:00 (Queue) | Wahr/Falsch | Thanksgiving | Thanksgiving True or False 🦃 90% Get #4 Wrong | 6 | Queue | game-show | Queue | – | E18 Event | ≥ 500 |
| 25.11. 21:00 (Queue) | Karten-VS #9 | Queue | This Map Is Lying To You #9 🌍 … | 4 | Queue | world-trip | – | – | Exploit | ≥ 800 |
| 26.11. Long 14:00 (Queue) | QuizLong exam, 50 Q | Christmas | Christmas Quiz 2026 🎄 50 Questions – Can You Get 40? | 50 | Queue | brain-pulse | #B91C1C/#14532D | B zuerst „CAN YOU GET **40/50**?“ | Saison | ≥ 100 n. 3 T |
| **26.11. 16:00 – NEU ANLEGEN** | **Flag Duel #4** (flagduel) | 4 neue Doppelgänger-Paare | **Flag Quiz #4: Left or Right? Only 1 in 10 Get 4/4 🌍** #shorts | 4 Runden, timing wie #3 | Vorschlag: EASY **Mexico vs Italy** (Ziel Mexico) · MEDIUM **Bulgaria vs Hungary** (Ziel Bulgaria) · HARD **Honduras vs Nicaragua** (Ziel Honduras) · LEGEND **Guinea vs Mali** (Ziel Guinea). Schluss „Follow for flag duel number five!“ | game-show | – | – | **E22 Titel-Test**: #1-Muster + Nummer vs. „Who Is X?“ (#2/#3) | Views n. 24 h > Ø(#2,#3) |
| 26.11. 21:00 (Queue) | Karten-VS #10 | Queue | This Map Is Lying To You #10 🌍 … | 4 | Queue | world-trip | – | – | Exploit | ≥ 800 |
| 27.11. 16:00 (Queue) | 6-Q tvshow | Science (Wunsch) | Science Trivia: 90% Get #4 Wrong 🔬 | 6 | Queue; Kommentar „You asked for it – science! 🔬“ | game-show | Queue | – | Zuschauer-Wunsch | ≥ 600 |
| **27.11. 21:00 – NEU ANLEGEN** | Karten-VS #11 (truesize) | nur vorhandene Formen, kein Grönland, keine Paare aus #1–#10 | This Map Is Lying To You #11 🌍 Which Is REALLY Bigger? | 4 Runden, ≤ 55 Wörter | R1 muss überraschen, Kontrollspalte ≥ 5 % je Paar, Gewinner mischen. Schluss „Follow, number twelve drops tomorrow!“ | world-trip | – | – | Exploit (≈1,0 Abos/1k, Median ≈1.000) | ≥ 800 |

Vorschau: **Sa 28.11.** Long 14:00 Rätsel #3 „IQ Test: 10 Riddles 90% Fail – Can You Solve 4? 🧠“ (exam, B „CAN YOU SOLVE **4**?“) + 16:00 **Flag Duel #5** (Vorschlag USA/Liberia, Belgium/Germany, Bolivia/Lithuania, Kuwait/UAE; Titel nach E22-Ergebnis) + 21:00 map-lie-12 · So 29.11. 16:00 Reno-1-Frage, 21:00 map-lie-13 (1. Advent).
Bandit 24.–27.11. (11 Slots): 8 Exploit, 3 Experimente (E18 T/F, E21 Takt, E22 Flag-Titel).

## Ideen-Backlog
1. Flag Duel täglich ab 29.11., wenn #3/#4 ≥ 1.000 n. 24 h – einziges Format > 2 Abos/1k.
2. „Real or Fake Flag?“ – WonderQ 334k/50×; eine echte + eine manipulierte Flagge (Farbe/Stern/Streifen geändert). Erst prüfen, ob flagduel eigene SVGs (public/flags/fake/…) laden kann.
3. Flag-Long „Flag Quiz: 50 Look-Alike Flags – Can You Get 40?“ (exam) – Long-Version des Gewinners, Sa 5.12.
4. „Can You Pass the U.S. Citizenship Test?“ exam-Long – Trivia Square 2,8 Mio, passt zum Kanalnamen.
5. Art-Trivia-Short – Wunsch @Jo-wl5fj.
6. Advent-Serie „Christmas Trivia #1–24“ ab 1.12. 16:00 an Nicht-Flag-Tagen.
7. Klassik-Fakten-Short (ohne Musikausschnitte) – Wunsch @Jo-wl5fj.
8. Black Friday „Which Costs More?“-Short – nur Listenpreise (Fr 27.11. belegt → nächstes Jahr / Cyber Monday 30.11.).
9. Vokabel-IQ-Short – Math Quiz 153k.
10. „Name These 10 Flags“ 10-Flaggen-Short (Quizzes Mania 108k/82×) – Variante der 6-Q, wenn Flag Duel ermüdet.

## Für den Produktions-Agenten (heute)
- Anlegen: `2026-11-26-flag-duel-4.json` (16:00, Titel exakt „Flag Quiz #4: Left or Right? Only 1 in 10 Get 4/4 🌍 #shorts“) und `2026-11-27-map-lie-11.json` (21:00).
- Flag Duel #4: nur Flaggen aus public/flags; keine Paare aus #1–#3; nichts Politisches; Indonesia/Monaco verboten; jedes Paar muss sichtbar unterscheidbar sein (sonst Ersatzpaar). Pinned comment „Which pair fooled you? Comment your score /4 👇“. ≤ 80 Wörter.
- Serien-Schluss Pflicht. Keine Halloween-, Alters- oder Politik-Themen; keine Longs Mo/Mi/Fr/So; max. 2 Shorts/Tag.

## NACHTRAG 24.11. 22:30 – Besitzer: „über 60 % Engagement, aber immer noch 1–2k Views“
**Diagnose (report.json, Shorts):** Fast alle Shorts enden bei ≈1.000 Views, also im ersten Test-Pool. Nur Flag Duel #1 kam weiter (2.752 Analytics-Views). Engaged/stayed liegt bei 45–62 %. Damit wischen 4 von 10 Zuschauern in den ersten 1–2 Sekunden weg. Für den nächsten, größeren Pool braucht ein Short erfahrungsgemäß ≈ 70 %+ stayed **und** Ø angesehen ≥ 90–100 % (Loop). Wir haben: Flag Duel 56 % / 84 %, Karten-VS 50–52 % / 74–79 %, 6-Q 45–56 % / 51–71 %. 95 % der Views kommen aus dem Shorts-Feed. Titel und Thumbnail zählen dort kaum, **Sekunde 1 und Länge entscheiden**.
**Ursachen:** (1) Vorrede: Jedes Short beginnt mit einem Hook-Satz („Only one in ten get all four.“, ≈1,8 s), bevor die erste Frage kommt. (2) Zu lang: 34–36 s gegenüber 21–26 s bei den Flag-Gewinnern der Konkurrenz (ThinkBop 0:26, Map Buzzer 0:21, Flag Atlas 0:21). (3) Lange Antwortsätze nach jedem Reveal.
**Fix ab Flag Duel #4 (Produktion 25.11.):**
- `hookLine: ""` (leer) → atlas_voice.py überspringt die Vorrede bei flagduel (Code-Fix heute). Die erste gesprochene Zeile ist die Frage: „Who is Mexico? Left or right?“. Der Kicker „CAN YOU GET 4/4?“ bleibt als Text.
- Antwortzeilen max. 3 Wörter („Right – Mexico!“), timing `{"think": 2.6, "move": 0.7, "tail": 0.2}`, Ziel **≤ 27 s** (log „Dauer“ prüfen; > 28 s → Zeilen kürzen).
- Letzte gesprochene Zeile nur „Follow for number five!“ (≤ 1,5 s).
- Karten-VS #11: hookLine max. 4 Wörter, Antworten max. 4 Wörter, Ziel ≤ 30 s.
- Erfolg (E23): stayed ≥ 65 % und Ø angesehen ≥ 90 % bei #4. Wenn ja → Standard für alle Shorts.

## NACHTRAG 24.11. 23:15 – STRATEGIE Besitzer: „This Map Is Lying raus, Flag Duel bleibt, mit vidIQ neue Ideen“
**vidIQ (3 Outlier-Abfragen, Shorts Nov. 2026)** – mit Abstand stärkstes Muster in unserer Nische ist **echte gegen gefälschte Flagge**:
| Video (Kanal, Abos) | Views / × Kanal | Länge |
|---|---|---|
| „Can You Spot the Real Lithuania Flag? 5/5“ (WonderQ, 4,6k) | 525k / 79× | 1:15 |
| „Real Flag or Sneaky Fake? 5/5“ (WonderQ) | 345k / 59× | 1:16 |
| „GUESS THE REAL FLAG!“ (MB GeoPlay, 15,6k) | 151k / 35× | 0:43 |
| „Can You Find The Real Flag? 99% Fail The Last One!“ (Globonk, 1,9k) | 63k / 32× | 0:27 |
| „(1) Flag Quiz Can You Name These 10 Flags?“ (Quizzes Mania, 1k) | 110k / 91× | 1:39 |
Weitere Muster: „Guess 10 Flags From EASY to IMPOSSIBLE“ (Quizora 112k/17×), „Blind Ranking Countries by Size: Day 30“ (Goober 44k/8×), „Missing Letters Quiz“ (Trivia Quiz 89k, 4.700 Views/h).
**Entscheidung:**
- **Karten-VS („This Map Is Lying“) eingestellt.** map-lie-9/10/11 aus der Queue gelöscht. Die Serie hängt bei ≈1.000 Views und 50 % stayed fest.
- **21:00 = neue Serie „Real or Fake Flag? #N“.** Sie läuft im Flag-Duel-Renderer (story.type "flagduel", neues Feld `ask: "WHICH IS THE REAL"`). Fälschungen liegen in public/flags/fake/<iso2>.svg (fr, de, lt, se, ca, it, ch, jp, dk, at, fi). Probe-Stills sind gerendert und in Ordnung.
- Angelegt (Manager, eilig, weil die Action vor 07:07 läuft): `2026-11-25-real-fake-flag-1.json` (France/Germany/Lithuania/Sweden) und `2026-11-26-real-fake-flag-2.json` (Canada/Italy/Switzerland/Japan). Beide nach E23: ohne Hook-Vorrede, Ziel ≤ 27 s. flag-duel-4 ebenfalls auf E23 umgestellt.
- 16:00 Flag Duel bleibt (#4 Do, #5 Sa).
**Für den Produktions-Agenten (25.11.):** `2026-11-27-real-fake-flag-3.json` (21:00) anlegen. Fälschungen dk (Kreuz mittig), at (weißer Streifen zu breit), fi (Kreuz mittig) sind schon da. Für die 4. Runde selbst ein Fake-SVG in public/flags/fake/ erzeugen (nur Farben tauschen oder verschieben). Eine Fälschung darf **nie** die echte Flagge eines anderen Landes ergeben (z. B. Irland gespiegelt = Elfenbeinküste, Polen umgedreht = Indonesien/Monaco → verboten). Seite des Originals mischen, Titel „Real or Fake Flag? #3 Only 1 in 10 Spot All 4 🧐 #shorts“, Schluss „Follow for number four!“. Danach täglich 21:00 bis auf Widerruf.
**Erfolg E24:** Real-or-Fake #1–#3 Median ≥ 1.500 Views n. 3 T und stayed ≥ 60 %. Abbruch: 3 Folgen unter dem Shorts-Median.
**Ideen-Backlog neu (vidIQ):** (1) „Guess 10 Flags From EASY to IMPOSSIBLE“ als 10-Runden-Flag-Short (Quizora 112k), (2) „Missing Letters: Guess the Country“ (Trivia Quiz 89k, 4.700/h) – tvshow-Short mit Lücken-Wörtern, (3) „Blind Ranking Countries by Size: Day N“ – Serie mit Tagesnummer (Goober 44k), (4) Flag-Long „50 Real or Fake Flags – Can You Get 40?“ (exam).

## NACHTRAG 24.11. 23:15 – Besitzer-Screenshot Flag Duel #2 („Who Is Slovakia?“)
- Nach ≈31 h: **2.463 Views, +12 Abos (≈4,9 pro 1.000), 65,1 % stayed, 47 Likes**, 94 % Shorts-Feed, 131 aus der Suche. Die Kurve ist ab ≈20 h ein zweites Mal gestiegen (zweiter Test-Pool).
- Damit ist das Format bestätigt: #1 3.000+/+18, #2 2.463/+12. Die Titel-Hypothese von heute früh („Who Is X?“ schwächer) ist widerlegt. E22 läuft trotzdem, hat aber geringe Priorität.
- **Entscheidung: Flag Duel täglich um 16:00 ab Sa 28.11.** (Kriterium „#2 ≥ 1.000 n. 24 h“ erfüllt).
- **Für den Produktions-Agenten:**
  - `2026-11-28-flag-duel-5.json` und ab dann jeden Tag eine Folge anlegen. Paare nie wiederholen, E23-Timing beibehalten.
  - `2026-11-29-one-q-further-west.json` ins Backlog verschieben (aus der Queue nehmen), weil 16:00 ab dann Flag Duel ist.
  - Wissenschafts-Short bleibt Fr 27.11. 16:00 (Zuschauerwunsch).
