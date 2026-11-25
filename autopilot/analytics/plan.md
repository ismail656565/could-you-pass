# Plan – 2026-11-25 (Mi)

Kanal **53 Abos** (report.json 24.11. 21:03) – **+10 in ≈22 h** (43 → 53), **50er-Marke geknackt**. Analytics gesamt (2–3 T Verzug): 38.162 Views → 45 Abos = **1,18 Abos/1.000** (Vortag 0,72).
Flag Duel trägt allein: #1 3.717 Views (+19 Abos ≈ 6,9/1.000), #2 2.417, #3 988 n. ≈6 h (#2 lag n. 6,5 h bei 1.155 → gleicher Kurs). Karten-VS endgültig schwach (0,37/1.000 über 8 Folgen, #8 394 n. 1 T) → Streichung von gestern bestätigt.
Kommentare: 3 offen → alle 3 beantwortet (23 Antworten gesamt). Kein Faktenfehler.
Änderungen: heute Start „Real or Fake Flag? #1“ (21:00) + E23 Sofort-Start; Flag Duel täglich ab Sa 28.11.; Sa-Long = Rätsel #3 nach Konkurrenz-Muster „10 Tricky Riddles“ (152×).

## TECHNIK-PROBLEM
- Keine Ausfälle. Log 24.11.: 3/3 hochgeladen (Rätsel-Long 14:00, flag-duel-3 16:00, map-lie-8 21:00), Kommentare gepostet, Analytics 18:55 + 21:03 ok.
- Beobachten (kein Bug): Rätsel-Long #2 (exam) **0 publicViews n. ≈8 h**, Status public/processed. Thanksgiving-Long zeigte dasselbe (0 n. 5 h → 37 n. 1 T) → Long-Zähler hängt am Anfang. Wenn n. 48 h < 20 → Titel/Thumbnail prüfen.
- Offen aus gestern: `2026-11-27-real-fake-flag-3.json` fehlt noch, `2026-11-29-one-q-further-west.json` liegt noch in der Queue → beides heute Produktions-Agent (s. unten).

## Zuschauer
- 35 Kommentare (21 T), 3 offen → beantwortet: @neptuneee_official 4/4 Slovakia (auf Real-or-Fake heute eingeladen), @FakeDianaNeedsToBeStoped „Yesssss“ (Frage nach Score), @WildlyTrue65 4/4 Qatar.
- FEHLER-HINWEIS (1) = alter Score-Kommentar „I only got 1 wrong“ (kein Fehler, beantwortet).
- 12 von 13 gemeldeten Scores aus Flag Duel; fast alle 4/4 → Schwierigkeit hoch genug für Ego, aber LEGEND-Runde darf härter werden.
- Wünsche: Science (@Jo-wl5fj) Fr 27.11. 16:00 in Queue (Kommentar „You asked for it – science! 🔬“); Art + classical music im Backlog.

## Diagnose (Videos ≥ 3 T unter Format-Median)
| Video | Views | Ursache | Fix |
|---|---|---|---|
| Keine neuen Flops ≥ 3 T | – | which-first-3 1.040, Quick IQ 1.016, map-lie-5/6 1.007/1.186 = im/über Median | – |
| map-lie-7 (2 T) / map-lie-8 (1 T) | 631 / 394 | Format-Ermüdung (8 Folgen, stayed ≈50 %, 0,37 Abos/1k) | schon eingestellt → Real or Fake Flag 21:00 |
| Thanksgiving-Long (4 T) | 95 | zu spät für Saisonsuche, Ø angesehen 28 % | Feiertags-Longs ≥ 3 Wochen vorher (Christmas Do 26.11. ok) |
| Rätsel-Long #1 | 234 | stayed 79 %, aber Ø angesehen 11,7 % → Absprung nach Rätsel 1–2 | exam-Look (#2) + Sa #3: Rätsel 1 leicht, Antwort sofort, Timer ≤ 10 s |
- **KPI Abos/1.000 je Format (Analytics):** Flag Duel ≈ 6,9 · Longs ≈ 3,1 · übrige Shorts ≈ 0,7 · Karten-VS 0,37 (eingestellt). Ziel 2,0 bis 15.12. gesamt: 1,18 und steigend.

## Konkurrenz-Gewinner heute (vidIQ outliers, 2 Abfragen)
| # | Video (Kanal, Abos) | Views / × | Länge | Muster | → Slot |
|---|---|---|---|---|---|
| 1 | „Can You Find The Real Grenada Flag? 🇬🇩“ (Globonk, 1,9k) | 48,8k / 65 Views/h | 0:25 | echte Flagge EINES Landes im Titel | Real or Fake #4/#5: Ländername in Titel |
| 2 | „One Flag Is a Total Fake! 🧐 Can You Get 3/3?“ (WonderQ, 4,7k) | 31k / 5,5× | 0:46 | Fake-Flagge, Score-Hürde | bestätigt E24 |
| 3 | „Guess the Flag by Its Missing Symbol 👀 Part 3“ (Ballandia, 27k) | 95,3k / 194 Views/h | 0:47 | Symbol fehlt, Teil-Nummer | Backlog #3 (Fake = Symbol entfernt, gleicher Renderer) |
| 4 | „Which One Is INDONESIA? Left or Right?! 4 Levels… 99% Fail the Last!“ (ThinkBop!, 2,5k) | 14,6k / 14× | 0:26 | exakt Flag-Duel, Land im Titel | Flag Duel #5 Titel mit Zielland |
| 5 | „CAN YOU SOLVE THESE 10 TRICKY RIDDLES? \| ONLY A GENIUS CAN PASS“ (Test And Quiz Institution, 6,9k) | 27,8k / 152× | 5:45 | 10 Rätsel, ~6 min, Genie-Hürde | Rätsel-Long #3 Sa 28.11. |
- Weitere: „NIGERIA Waits in Round 5: Every Grid Hides One Wrong Flag“ (Flag Pals 18k), „54 flags, one odd one out“ (27,5k) → Gitter-Format braucht neuen Renderer (Backlog #6).
- Events: Thanksgiving Do 26.11., Black Friday 27.11., 1. Advent So 29.11., St Andrew's Day 30.11., Rumänien-Nationaltag 1.12., **UAE National Day 2.12.** (Flag Duel Kuwait/UAE).

## 3-Tage-Plan
| Datum / Slot | Format | Thema | Titel (YouTube) | Fragen + timing | Hook / Fragen | Musik | cardColors | Thumbnail | Warum | Erfolg |
|---|---|---|---|---|---|---|---|---|---|---|
| 25.11. 16:00 (Queue) | Wahr/Falsch tvshow | Thanksgiving | Thanksgiving True or False 🦃 90% Get #4 Wrong #shorts | 6 | Queue (Hook 4 Wörter) | game-show | Queue | – | E18 Event, Vorabend | ≥ 500 n. 3 T |
| 25.11. 21:00 (Queue) | Real or Fake Flag #1 (flagduel) | FR/DE/LT/SE | Real or Fake Flag? #1 Only 1 in 10 Spot All 4 🧐 #shorts | 4, E23 (2.6/0.7/0.2, outro 0.6) | ohne Vorrede | game-show | – | – | E24 (WonderQ 525k/79×) | Median #1–#3 ≥ 1.500, stayed ≥ 60 % |
| 26.11. Long 14:00 (Queue) | QuizLong exam, 50 Q | Christmas | Christmas Quiz 2026 🎄 50 Questions – Can You Get 40? | 50 | Queue | brain-pulse | #B91C1C/#14532D | B zuerst „CAN YOU GET **40/50**?“ | Saison | ≥ 100 n. 3 T |
| 26.11. 16:00 (Queue) | Flag Duel #4 | IT/MX, BG/HU, NI/HN, GN/ML | Flag Quiz #4: Left or Right? Only 1 in 10 Get 4/4 🌍 #shorts | 4, E23 | ohne Vorrede | game-show | – | – | E22 + E23 | stayed ≥ 65 %, Ø angesehen ≥ 90 % |
| 26.11. 21:00 (Queue) | Real or Fake Flag #2 | CA/IT/CH/JP | Real or Fake Flag? #2 Only 1 in 10 Spot All 4 🧐 #shorts | 4, E23 | ohne Vorrede | game-show | – | – | E24 | s. o. |
| 27.11. 16:00 (Queue) | 6-Q tvshow | Science (Wunsch) | Science Trivia: 90% Get #4 Wrong 🔬 #shorts | 6 | Queue; Kommentar „You asked for it – science! 🔬“ | game-show | Queue | – | Zuschauer-Wunsch | ≥ 600 n. 3 T |
| **27.11. 21:00 – NEU** | Real or Fake Flag #3 | **DK / AT / FI** (Fakes vorhanden) + 1 neues Fake (Vorschlag **Norway**: Kreuz mittig statt nach links versetzt) | Real or Fake Flag? #3 Only 1 in 10 Spot All 4 🧐 #shorts | 4, E23, outro 0.6 | Q1 „Which is the real Denmark? Left, or right?“ · Original-Seite mischen (a/b/b/a) · Schluss „Follow for number four!“ | game-show | – | – | E24 | s. o. |
| **28.11. Long 14:00 – NEU** | QuizLong exam, 10 Rätsel (~6 min) | IQ-Rätsel #3 | **Tricky Riddles IQ Test: Can You Solve 7 of 10? 🧠** | 10, count ≤ 10 | Rätsel 1 leicht (Einstieg halten), Schwierigkeit steigend, Rätsel 10 = „Genius“-Stempel | brain-pulse | Queue-Standard | B zuerst „F“ + „CAN YOU SOLVE **7**?“, A „10 TRICKY **RIDDLES**“, C „ONLY A **GENIUS**“ | Konkurrenz #5 (152×) + E14 ✓ | ≥ 150 n. 3 T, ≥ 1 Abo |
| **28.11. 16:00 – NEU** | Flag Duel #5 (täglich ab jetzt) | EASY **USA/Liberia** · MEDIUM **Belgium/Germany** · HARD **Bolivia/Lithuania** · LEGEND **Kuwait/UAE** | Flag Quiz #5: Which One Is Liberia? 99% Miss the Last 🌍 #shorts | 4, E23 | „Who is Liberia? Left or right?“ · Gewinner b/a/b/a · Schluss „Follow for number six!“ | game-show | – | – | Exploit + ThinkBop-Muster (Land im Titel) | ≥ 1.500 n. 3 T, ≥ 3 Abos/1k |
| **28.11. 21:00 – NEU** | Real or Fake Flag #4 | **USA** (Kanton rechts), **UK** (Union Jack ohne Versatz), **Brazil** (Band verkehrt geneigt), **Turkey** (Halbmond gespiegelt) | Real or Fake Flag? #4 Can You Spot the Real USA? 🧐 #shorts | 4, E23 | Fakes selbst erzeugen, nie = Flagge eines anderen Landes · Schluss „Follow for number five!“ | game-show | – | – | E24 + Globonk-Muster (Land im Titel) | s. o. |

Vorschau So 29.11. (1. Advent): 16:00 Flag Duel #6 (Denmark/Switzerland, Ghana/Cameroon, Egypt/Yemen, Niger/India), 21:00 Real or Fake #5 (South Korea Trigramme vertauscht, Greece Kanton unten, Spain gleich breite Streifen, Chile Stern rechts; Argentinien ohne Sonne NICHT – ist eine echte Flaggenvariante). Mo 30.11.: Flag Duel #7 (Japan/Bangladesh, Peru/Canada, Greece/Uruguay, Chile/Puerto Rico). Mi 2.12. (UAE National Day): Kuwait/UAE dann schon in #5 verbraucht → im Kommentar/Beschreibung auf #5 verweisen statt Paar wiederholen.
Bandit 25.–28.11. (10 Slots): 7 Exploit (Flag Duel, Feiertage, Wunsch, Rätsel), 3 Experimente (E18 T/F, E23 Timing, E24 Real or Fake).

## Ideen-Backlog
1. Real or Fake Flag täglich 21:00 – stärkstes Nischenmuster (WonderQ 525k, Globonk 48,8k in 3 T); Ländername im Titel ab #4.
2. Flag Duel mit Zielland im Titel („Which One Is X?“) – ThinkBop 22,7k/14,6k bei 2,5k Abos, eigener #2 „Who Is Slovakia?“ 2.417.
3. „Missing Symbol“-Variante (Flagge ohne Wappen/Stern gegen Original) – Ballandia 95k, 194 Views/h; gleicher flagduel-Renderer, nur andere Fakes.
4. Flag-Long „50 Look-Alike Flags – Can You Get 40?“ (exam) – Long-Version des einzigen Gewinners, Sa 5.12.
5. Rätsel-Long wöchentlich nach „10 Tricky Riddles“-Muster (152×), Rätsel 1 leicht gegen frühen Absprung.
6. Flaggen-Gitter „One Flag Is Wrong – Find It“ (Flag Pals 18k, 54-Flaggen 27,5k) – neuer Renderer nötig, Aufwand mittel.
7. Nationaltags-Flag-Duels (UAE 2.12., Finnland 6.12.) – Aktualität ohne Politik.
8. „Can You Pass the U.S. Citizenship Test?“ exam-Long – Trivia Square 2,8 Mio, passt zum Kanalnamen.
9. Art-Trivia-Short – Zuschauer-Wunsch @Jo-wl5fj.
10. Klassik-Fakten-Short (ohne Musikausschnitte) – Zuschauer-Wunsch @Jo-wl5fj.

## Für den Produktions-Agenten (heute)
- **Anlegen:** `2026-11-27-real-fake-flag-3.json` (21:00), `2026-11-28-iq-riddles-10-3.json` (Long 14:00, layout exam), `2026-11-28-flag-duel-5.json` (16:00), `2026-11-28-real-fake-flag-4.json` (21:00) – Titel exakt wie in der Tabelle.
- **Aus der Queue nehmen:** `2026-11-29-one-q-further-west.json` (16:00 ist ab 28.11. täglich Flag Duel) → nach queue/backlog o. ä. verschieben, nicht hochladen.
- Flag-Serien: hookLine "", timing {think 2.6, move 0.7, tail 0.2, outro 0.6}, Antworten ≤ 3 Wörter, ≤ 27 s (Log „Dauer“ prüfen), Schluss nur „Follow for number N+1!“. Paare/Fakes nie wiederholen (Liste: pl/id, ie/ci, au/nz, td/ro, is/no, ml/sn, nl/lu, si/sk, lv/at, ec/co, ht/li, qa/bh, it/mx, bg/hu, ni/hn, gn/ml; Fakes fr/de/lt/se/ca/it/ch/jp + dk/at/fi für #3). Indonesia/Monaco und politisch umstrittene Flaggen (Kosovo, Palästina, Taiwan, Westsahara usw.) verboten.
- Fakes: nur Farben tauschen, Elemente verschieben/spiegeln, Proportionen ändern; Ergebnis gegen alle 270 Flaggen in public/flags prüfen (darf keiner echten gleichen). Probe-Still rendern.
- Rätsel-Long #3: Duplikat-grep gegen iq-riddles-12-1/-2, jede Lösung zweimal nachrechnen, count ≤ 10 (QA-Standbild), Texte ohne Emoji in hook/finalLabel/ctaText/outroText.
- Keine Halloween-, Alters- oder Politik-Themen; keine Longs Mo/Mi/Fr/So; max. 2 Shorts/Tag.

## NACHTRAG 25.11. 11:05 – Besitzer: tvshow-Short-Layout „gefällt gar nicht“
- **Entscheidung:** Es gibt keine tvshow-Shorts mehr. Alle Shorts laufen im FlagDuel-Renderer (16:00 Flag Duel, 21:00 Real or Fake Flag). Das ist auch das einzige Short-Format über dem Abo-Ziel (≈6,9/1k gegenüber ≈0,7 bei tvshow).
- Der Science-Short 27.11. liegt jetzt in queue/backlog/. Der Wunsch wird als exam-Long am Di 1.12. erfüllt („Science Quiz: 30 Questions – Can You Pass?“, B „CAN YOU GET **25/30**?“).
- **Für den Produktions-Agenten (26.11.):** `2026-11-27-flag-duel-5.json` (16:00) anlegen und das bisherige 28.11.-Item zu #6 machen. Konkret: Flag Duel #5 = Paare aus dem jetzigen `2026-11-28-flag-duel-5.json` → Datei auf 27.11. umbenennen. Für 28.11. ein neues flag-duel-6 anlegen (Paare aus der Vorschau 29.11.: Denmark/Switzerland, Ghana/Cameroon, Egypt/Yemen, Niger/India), Schluss jeweils „Follow for number N+1!“. Danach täglich eine Folge.
- Long Di 1.12.: science-quiz-30-1 (exam) anlegen, Fakten per WebSearch prüfen, Kommentar „You asked for it – science! 🔬“.
