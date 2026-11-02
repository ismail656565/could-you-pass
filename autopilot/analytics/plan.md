# Plan – 2026-11-02

## TECHNIK-PROBLEM
1. **E1 #1 "Can You Score 4/12?" (ixo369QcvVk) hat 0 öffentliche Views** im Analytics-Stand 01.11. 11:28 – ~21 h nach Veröffentlichung (Kommentar wurde 31.10. 13:49 gepostet, also öffentlich). Selbst 50-Fragen-Longs hatten nach 1 Tag 2–10. **Produktions-Agent bitte prüfen** (videos.list part=status,contentDetails,statistics für ixo369QcvVk, Uqu-veLODm8, brCR2MyeQr0): privacyStatus = public? `madeForKids`/`selfDeclaredMadeForKids` = false? Altersbeschränkung (contentRating.ytRating)? `embeddable`/`publicStatsViewable` true? Falls ein Long fälschlich "made for kids" oder unlisted ist → korrigieren und im Upload-Code fest `selfDeclaredMadeForKids: false` setzen. Ergebnis in learnings.md notieren. Wenn alles korrekt ist: kein Fix, nur Notiz (dann ist es reine Reichweite).
2. **Konkurrenzliste wieder mit Nicht-Englisch aufgefüllt:** Ajmal Quiz (Urdu/Islam) und Gk Quiz Study (Odia) heute entfernt und in `blocked` (jetzt 23 Kanäle, 10 blockiert). Dauerhaft-Fix (optional, klein): in `competitors()` beim Auto-Nachfüllen Titel mit "Urdu|Hindi|Odia|Islami|Bangla|Tamil" bzw. nicht-lateinischer Schrift überspringen.
3. **keywords.md ist vom 29.10.** – heute ist Montag, der mode=all-Lauf sollte sie erneuern. Falls nach dem Lauf weiterhin 29.10. → `keywords()`-Montags-Bedingung prüfen (Zeitzone/Weekday).
4. Neue Konkurrenz-Kandidaten ohne Kanal-ID im Ausreißer-Scan (Golden Memory Quiz, 2.240 Abos: "ARE YOU WELL-EDUCATED? TRY TO SCORE ABOVE 5!" 186k/8:06; Puzzle Code, 208 Abos: "18 Hard Riddles…" 66k/8:03). Falls die Action die Kanal-ID aus der Video-ID (3O-2CFoLOuw, WyShr0ebbrI) holen kann → in competitors.json mit `"source": "research"` aufnehmen.

## Zusammenfassung (Deutsch)
- **VS-Vergleich zündet:** E2 #1 "Which Country Is Bigger?" 525 Views nach ~15 h – schon jetzt doppelt so viel wie der 4-Trap-Median (251) und weit über leichter 1-Frage "Hours in a Week" (206 nach 20 h). → E2 #3 kommt am 04.11. 21:00 (Einwohner-Vergleich mit Flaggen), damit E2 bis 07.11. entschieden ist.
- **Shorts-Bild klar:** 6+-Fragen bleibt Spitze (Median 1.334, stayed 56 %); Sloth (154) und Food-Trap (125) final unter Median → Flops. Konkurrenz bestätigt Mehr-Fragen-Shorts: FlameTimer "Quick Fire General Knowledge Quiz" **6,9 Mio** (0:59), Y King "Bible Facts Quiz! Can You Get 6/6?" 316k. → 04.11. 16:00 "Quick Fire"-6-Fragen-Short.
- **Long weiter tot (Median ~3–10 Views)**, E1 #1 sogar 0 → Technik 1 prüfen. Konkurrenz-Beweis für 7-Min-Format wird noch stärker (Clear Think 1,53 Mio, GK STUDIO PRO 1,0 Mio, Quiz World "10 Tricky IQ Riddles" 364k neu seit 22.10., Golden Memory "Try to Score Above 5!" 186k) → E1 #3 am 04.11. schließt die Testreihe vor der Auswertung 05.11.
- Keine Strategieänderung (Testwoche bis 05.11.); 02./03.11. bleiben wie in der Queue.

## Konkurrenz-Gewinner heute

| # | Video (Kanal, Abos) | Views | × Median | Länge | Titel-Muster | Was wir übernehmen → Slot |
|---|---|---|---|---|---|---|
| 1 | "Test Your iQ in just 7 minutes" (Clear Think, 5,8k; +880 Abos in 3 Tagen) | 1,53 Mio | 2295× | 6:48 | Zeitversprechen + IQ | 7-Min-Länge, wenige schwere Fragen → E1 #2 (heute) + **E1 #3 04.11.** |
| 2 | "Are You Well Educated? … Score At Least 4/10!" (GK STUDIO PRO, 1,8k) | 1,0 Mio | 1164× | 7:15 | Identitäts-Frage + niedrige Hürde | "Well Educated?"-Identitätshaken + Hürde 5/15 → **E1 #3 04.11.** (eigene Formulierung) |
| 3 | "10 Tricky IQ Riddles / Test Your Intelligence!" (Quiz World, 834; +180 Abos in 1 Tag) | 364k | 214× | 6:48 | Zahl + "Tricky" + IQ | Fangfragen-/Denkfragen-Anteil (≈5 von 15) in E1 #3, eigene Rätsel |
| 4 | "Quick Fire General Knowledge Quiz #shorts" (FlameTimer, 44k; Ausreißer-Scan) | 6,9 Mio | 156× (Views/Abos) | 0:59 | "Quick Fire" + Thema, viele schnelle Fragen | Titelbegriff "Quick Fire" + 6 schnelle Fragen → **04.11. 16:00** |
| 5 | "Bible Facts Quiz! 📖 Can You Get 6/6?" (Y King, 2,6k) | 316k | 123× (Views/Abos) | 1:10 | Thema + "Can You Get 6/6?" | Score-Frage "6/6" im Titel (unser Genius-6/6 = 1.433) → **04.11. 16:00** (Thema Geografie statt Religion) |

Nicht übernommen: Chauncey Asks ("Name the musical from its Playbill" 1,7 Mio) = Straßen-Personenformat; Dopamine/BLINK Football = Spielerfotos/Google-Earth-Bilder (Rechte); Disney-Songs (Musikrechte).

## 3-Tage-Plan

Layout überall **tvshow**. Zeiten Berlin. Fakten vor dem Schreiben prüfen (Britannica/NASA/CIA Factbook/UN/Guinness). broll-Regeln (learnings 30.10.) gelten. **02.11. und 03.11. liegen schon in der Queue → nur 04.11. neu anlegen.**

| Datum / Slot | Format | Thema | Arbeitstitel (YouTube) | Fragen + timing | Hook / Frage 1 | Musik | cardColors | Thumbnail A/B/C + Foto | Warum | Erfolgskriterium |
|---|---|---|---|---|---|---|---|---|---|---|
| **02.11. Long 14:00** | E1 #2 (Queue) | US-Präsidenten | US Presidents Quiz: Can You Score 5/15? 🏛️ 7-Minute Test | 15, 10.0/2.6/0.95 | in Queue | brain-pulse | navy | in Queue | Konkurrenz #1/#2 + Wahltag 03.11. | ≥30 Views n. 3 T ODER Ø angesehen ≥45 % |
| **02.11. Short 16:00** | 1-Frage leicht #2 (Queue) | Planeten | Can You Answer: Which Planet Is Closest to the Sun? ☀️🤯 | 1 | in Queue | game-show | – | – | Exploit leichte Frage (Median 886) | ≥700 Views |
| **02.11. Short 21:00** | E2 VS #2 (Queue) | Tier-Tempo | Which Is Faster? 4 Races 90% Get Wrong 🐆 | 4 | in Queue | world-trip | – | – | E2 (VS #1 525 in 15 h) | ≥294 Views |
| **03.11. Long 14:00** | QuizLong 50 (Queue) | Geografie | Geography Quiz: 50 Questions From Easy to Legend 🌍 | 50, 5.0/1.2/1.0 | in Queue | world-trip | petrol | in Queue (Flagge Brasilien) | Exploit Suchbegriff | ≥50 Views n. 3 T |
| **03.11. Short 16:00** | 6-Fragen (Queue) | Which Came First #2 | Which Came First? Round 2 – 6 Questions 🤯 | 6, 2.5/0.8 | in Queue | brain-pulse | – | – | Exploit 1.234 | ≥1.000 Views |
| **03.11. Short 21:00** | E4 Titel-Test (Queue) | Geschichte | 4 History Questions – The Last One Will Humble You 😏 | 4, 2.5/1.0 | in Queue | brain-pulse | – | – | E4 | ≥800 Views UND mehr Kommentare als 26.10. |
| **04.11. Long 14:00** | **E1 #3 – 7-Min-Test** (15 sehr schwere Fragen, 3 Runden à 5: HARD → VERY HARD → LEGEND) | Allgemeinwissen, davon ~5 "Fangfragen"/Denkfragen (eindeutig lösbar, keine Mathe-Tricks mit Streitpotenzial) | **Are You Well Educated? Hard Quiz – Score 5/15 to Pass 🎓** (55 Z.) | 15, timing **10.0/2.6/0.95**, jede Erklärung 1–2 Sätze mit Zusatzfakt → Ziel 6:45–7:30; Fortschritt "x / 15" | 1 Satz: "Fifteen hard questions – score five and you pass. Ready? First one:" Q1 (HARD, sofort verständlich): "Which planet has the most known moons?" (Saturn, Stand 2025 274 – vorher prüfen) – NUR falls nicht schon benutzt (sonst "Which country has the most time zones?" → Frankreich, 12 inkl. Überseegebiete); Fangfragen-Ideen: "How many months have 28 days?" (alle 12), "What is the only letter not in any U.S. state name?" (Q), "A plane crashes on the US–Canada border – where are survivors buried?" (gar nicht) – jeweils gegen queue/done greppen | brain-pulse | dunkelgrün / gold | A "SCORE 5/15?" (riesig) + Foto `bilder/q2-pyramid.jpg` (verrät nichts, falls keine Pyramiden-Frage drin – sonst q2-mammoth) · B "WELL EDUCATED?" · C "ONLY 1 IN 10 PASS"; thumbBadge "15 Q" | Experiment E1 #3 (Variable: Format/Länge); Konkurrenz #1–#3 (1,53 Mio / 1,0 Mio / 364k), Golden Memory 186k | ≥30 Views n. 3 T ODER Ø angesehen ≥45 % (E1 gesamt: Stopp, wenn #1–#3 alle < Long-Median) |
| **04.11. Short 16:00** | **6-Fragen-Short** (Exploit, Median 1.334) | Geografie (keine Überschneidung mit den 50 Fragen vom 03.11.!) | **Quick Fire Geography Quiz – Can You Get 6/6? 🌍** (48 Z. + #shorts) | 6, count 2.5 / tail 0.8, leicht → mittel, Haken an Platz 4 | Sek. 0 Frage 1 (leicht, mit Foto/broll): "What is the capital of Canada?" (Ottawa – Haken: viele sagen Toronto) – nur wenn ungenutzt; weitere Ideen: "Which country is home to Machu Picchu?", "Which river flows through Cairo?", Haken Q4 "Which continent has the most countries?" (Afrika, 54), "Which is the smallest country in the world?", "Mount Kilimanjaro is in which country?"; Loop-Satz "Think you got all six? Go again!" | game-show (Shorts-Median 822, bester Musik-Wert) | marineblau / türkis | – (Short) | Exploit eigener 6+-Sieger + 8-Geo-Short 1.325 + Konkurrenz #4/#5 | ≥1.000 Views n. 3 T |
| **04.11. Short 21:00** | **E2 VS #3** (Balken-Vergleich, 4 Runden) | Einwohner: "Which Has More People?" | **Which Has More People? 4 Rounds 90% Get Wrong 👥** (51 Z.) | 4 Runden, timing 3.0/1.2, correctLabel "MORE PEOPLE!", Flaggen über `images` | R1 (Haken sofort): Nigeria vs Brasilien (Nigeria ~232 Mio > Brasilien ~212 Mio, UN WPP 2024); R2 Japan vs Türkei (~124 Mio vs ~86 Mio); R3 Kanada vs Australien (~40 Mio vs ~27 Mio); R4 Kasachstan vs Schweiz (~20 Mio vs ~9 Mio) – Werte vor Render mit UN World Population Prospects 2024 / World Bank prüfen, Quelle in Beschreibung ("Population data: UN World Population Prospects 2024."); letzte Zeile "Think you can beat all four? Go again!" | world-trip | – (CompareScene) | – | Experiment E2 #3 (Variable: Format VS); E2 #1 525 Views/15 h | E2 gesamt: 3 VS ≥294 Views n. 3 T → dann VS als festes 21:00-Format + Long-Test "Which Is Bigger? 50 Rounds" |

Bandit 02.–04.11.: 5 Exploit / 4 Experiment (Testwoche – E1, E2 brauchen bis 05.–07.11. ihre dritte Folge; ab 05.11. wieder 70/30).

## Ideen-Backlog (nach erwartetem Potenzial)
1. **GTA Quiz (Long, ab 15.11., Release 19.11.)** – "GTA Quiz: How Well Do You Know Grand Theft Auto? 🎮"; größte Gaming-Suchwelle 2026; nur eigene Fakten, keine Spielbilder/Logos.
2. **Quick Fire General Knowledge Quiz – 8 Questions (Short)** – FlameTimer 6,9 Mio (0:59) + unsere 6+-/8-Fragen-Sieger; nach 04.11. als Serie "Quick Fire ___" (Science, History, Animals).
3. **"Which Is Bigger? 50 Rounds" (Long, VS-Balken)** – nur wenn E2 gewinnt; Daten-Vergleiche = viralste automatisierbare Nische (Recherche 29.10.).
4. **10 Tricky Riddles: Can You Solve 4? (Long ~7 min)** – Quiz World 364k / Puzzle Code 66k bei 208 Abos; eigener Riddle-Satz, falls E1 Kriterium erfüllt.
5. **Guess the Word by Emoji – 50 Rounds (Long)** – Kids Quizzy 528k, Quiz Bunny 596k; unser Emoji-Long beste Bindung (73 %).
6. **Veterans Day 11.11.: "US History Quiz: Can You Score 5/15?"** – Event + E1-Mechanik (nur Fakten).
7. **Bonfire Night 05.11. Short: "4 British History Questions – Can You Get 4/4? 💥"** – UK-Datum (GB = Top-5-Land unseres Publikums), History-Set (1.081).
8. **Thanksgiving 26.11.: "Thanksgiving Trivia: 50 Questions From Easy to Legend 🦃"** – saisonal; Halloween-35 war bestes 50-ähnliches Long (183).
9. **"Can You Get 6/6?" Serie nach Themen (Space, Food, Animals)** – Y King 316k mit exakt diesem Muster; Themen-Titel tragen nur als reine Sets.
10. **Tricky Quiz – Level 1/2/3 (Short-Serie)** – last30days 1,66 Mio; Serien-Experiment, sobald E3/E4 entschieden sind.

## Für den Produktions-Agenten (gilt heute, überschreibt ältere Defaults)
- Zuerst **Technik 1** prüfen (Status/madeForKids der Longs) und Ergebnis in learnings.md notieren; Technik 2–4 optional.
- Dann **3 Items für 04.11.** anlegen: `2026-11-04-gk-well-educated-5-15.json` (Long), `2026-11-04-six-q-quick-geo.json` (16:00, publishAt "16:00"), `2026-11-04-vs-population-1.json` (21:00, publishAt "21:00"). Dateinamen-Sortierung: "six-q" < "vs" passt.
- E1 #3: 15 Fragen mit count 10.0 / tail 2.6 / tempo 0.95 + Erklärsatz; nie unter 6:00 rendern (Titel enthält kein "7-Minute", trotzdem Ziel ~7 min). Keine Alters-Ansprache.
- 6-Fragen-Geo-Short: keine Frage aus `2026-11-03-geography-quiz-50-1.json` oder älteren Geo-Items wiederverwenden (grep "Ottawa", "Machu", "Cairo", "Kilimanjaro", "54").
- VS #3: Flaggen-Paare vom 31.10. (Brasilien/Australien, Italien/Japan, Nigeria/Kasachstan, Frankreich/Türkei) nicht wiederholen – die neuen Paare oben sind verschieden. Keine broll bei VS.
- Kein Halloween-/Spooky-Bezug, kein Schwarz-Orange, keine Politik-/Wahlfragen (Wahltag 03.11.).
