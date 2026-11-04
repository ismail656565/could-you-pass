# Plan – 2026-11-04

## TECHNIK-PROBLEM
1. **Longs bekommen seit 31.10. exakt 0 öffentliche Views** (report.json 03.11. 11:47): E1 #1 "Score 4/12" 0 nach ~3 T, True/False-50 0 nach ~2,9 T, Presidents 0 nach ~23 h. Davor hatten selbst schwache Longs 2–14. Status ist public/nicht MFK (02./03.11. geprüft) → reines Distributionsproblem ODER versteckte Einschränkung. **Produktions-Agent:** in analytics() zusätzlich `contentDetails.regionRestriction`, `contentDetails.contentRating` und `status.rejectionReason/failureReason` abfragen und in report.json schreiben; bei regionRestriction.blocked/allowed → Log "Status-Warnung". Ergebnis in learnings.md. Kein weiterer Umbau. (Besitzer prüft parallel im Studio die Spalte "Einschränkungen".)
2. **AI-Clip in B-Roll:** Geography-50 (03.11.) Frage 42 nutzte "Wooly Mammoth by OpenAI Sora.webm" (log 03.11. 06:41) – KI-Video widerspricht der Besitzer-Regel "kein AI-Look" und kann eine Synthetic-Content-Kennzeichnung erfordern. **Fix in `fetch_broll` (autopilot.py ~Z. 691):** Kandidaten verwerfen, deren Titel/Beschreibung (case-insensitive) `sora|openai|midjourney|dall-?e|stable diffusion|runway|veo|ai[- ]generated|kling|pika` enthält; bereits hochgeladenes Video nicht ändern.
3. Läufe 03.11. alle grün, 03.11. Soll erfüllt (geography-quiz-50-1, six-q-which-first-2, trap-4-history-humble, Kommentare 13:04/16:13/21:08). competitors.md vom 03.11. ok (25 Kanäle, 140 Gewinner).

## Zusammenfassung (Deutsch)
- **Shorts tragen, Longs sind tot:** 6+-Fragen jetzt 3/3 über 1.000 ("Only Geniuses 6/6" #2 **1.181**), VS #1 **854 final (3,4× 4-Trap-Median 251)**, VS #2 "Which Is Faster?" **488 nach ~16 h** → VS ist das zweitbeste Short-Format. Flops final: True/False-Short 120, leichte 1-Frage "Hours" 463 (Ziel 700 ✗), "Closest to the Sun" 193.
- **Longs: 4 Uploads in Folge 0 Views** (inkl. Keyword-#1 "True or False Quiz"). Das Problem ist nicht Thema/Format, sondern Ausspielung → Technik 1 + neues Timing-Experiment **E7: Long 06.11. um 19:00 statt 14:00** (= 13:00 ET; US = 60 % unseres Publikums; die einzigen Longs mit Reichweite – Emoji 141, Halloween 185 – liefen nicht im 14:00-Slot).
- **E1 (7-Min-Test):** #1 final 0, #2 0 → wenn #3 (heute) nach 3 T ebenfalls < Long-Median ist, wird E1 am 07.11. gestoppt.
- 06.11.: 16:00 Quick-Fire-6-Q (Science), 21:00 VS #4 "Which Is Taller?", Long History-50 um 19:00.

## Konkurrenz-Gewinner heute (letzte 30 Tage)

| # | Video (Kanal, Abos) | Views | × Median | Länge | Titel-Muster | Was wir übernehmen → Slot |
|---|---|---|---|---|---|---|
| 1 | "10 Tricky IQ Riddles / Test Your Intelligence!" (Quiz World, 988) – 22.10. | 468.755 (+9 % seit 03.11.) | 257× | 6:48 | Zahl + "Tricky" + IQ | Fangfragen-Anteil (E1 #3 heute); Riddles-Long erst nach Long-Fix |
| 2 | "trivia challenge quiz 😌" (Think Nova, 2,5k) – 05.10. | 481.835 | 712× | 1:02 | Minimal-Titel + Emoji, viele Fragen in ~1 min | 6-Q-Shorts 16:00 (04.–06.11.) |
| 3 | "Can You Score More Than 2? Test For Ages 70-95!" (QuizNova, 1,4k) – 10.10. (+ "No Person Born Before 1960 Gets Even 4 Right" 65k) | 411.966 | 136× | 6:42 | extrem niedrige Score-Hürde | Hürde "5/15" in E1 #3; Alters-Hook bleibt aus (bei uns 1–59 Views) |
| 4 | "Your Brain Is Ageless! Take This 10-Question IQ Quiz" (GK STUDIO PRO, 1,8k) – 27.10. | 40.236 | 47× | 7:14 | Kompliment-Hook + Fragenanzahl | nur Backlog (Kompliment-Titel als Titeltest für Long, wenn Longs wieder Impressionen bekommen) |
| 5 | "Can You Guess 20 F1 Tracks From Above? – Part 3" (Dopamine Quiz, 410) – 31.10. | 26.057 (in 4 T) | 38× | 8:50 | Serie "Part 3" + Zahl | Serien-Nummern: "Quick Fire … Quiz" als Serie (Geo 04.11. → Science 06.11.), VS-Reihe #4 |

Nicht übernommen: Chauncey Asks (Straßen-Personen + Markenlogos), FootyMind/BLINK (Spielerfotos), Quiz Phoenix (Disney-Songs = Musikrechte), Dopamine Google-Earth-Bilder (Kartenrechte).

## 3-Tage-Plan

Layout überall **tvshow** (Editorial-Look seit 04.11.). Fakten vor dem Schreiben prüfen (Britannica/NASA/Guinness/CTBUH/offizielle Bauwerks-Seiten). broll-Regeln gelten + Technik 2. **04.11. und 05.11. liegen in der Queue → nur 06.11. neu anlegen.**

| Datum / Slot | Format | Thema | Arbeitstitel (YouTube) | Fragen + timing | Hook / Frage 1 | Musik | cardColors | Thumbnail A/B/C + Foto | Warum | Erfolgskriterium |
|---|---|---|---|---|---|---|---|---|---|---|
| 04.11. Long 14:00 | E1 #3 (Queue) | GK schwer + 5 Fangfragen | Are You Well Educated? Hard Quiz – Score 5/15 to Pass 🎓 | 15, 11.5/2.6/0.95 | Queue | brain-pulse | dunkelgrün/gold | Queue (A "SCORE 5/15?" + Pyramide) | E1 #3; Konkurrenz #1/#3 | ≥30 Views n. 3 T ODER Ø angesehen ≥45 %; sonst E1-Stopp 07.11. |
| 04.11. Short 16:00 | 6-Q (Queue) | Geografie | Quick Fire Geography Quiz – Can You Get 6/6? 🌍 | 6, Queue | Queue | game-show | – | – | Exploit 6+ (3/3 > 1.000) | ≥1.000 Views |
| 04.11. Short 21:00 | E2 VS #3 (Queue) | Einwohner | Which Has More People? 4 Rounds 90% Get Wrong 👥 | 4, Queue | Queue | world-trip | – | – | E2 | E2 gesamt: 3 VS ≥294 Views n. 3 T |
| 05.11. Long 14:00 | Emoji-50 (Queue) | Wörter aus Emojis | Emoji Quiz: Guess the Word – 50 Rounds, Easy to Legend 🧩 | 50, 5.5/1.4 | Queue | game-show | gelb/violett | Queue (thumbPuzzle) | Exploit bestes eigenes Long | ≥50 Views ODER stayed ≥60 % |
| 05.11. Short 16:00 | E5 6-Q Wortschatz (Queue) | Vokabeln | Vocabulary Quiz – Can You Get 6/6? 📚 | 6, Queue | Queue | brain-pulse | – | – | E5, Konkurrenz Math Quiz | ≥1.000; <500 → Thema verwerfen |
| 05.11. Short 21:00 | 4-Trap + Event (Queue) | Gunpowder Plot | 4 Gunpowder Plot Questions – Can You Get 4/4? 💥 | 4, Queue | Queue | world-trip | – | – | Exploit History-Set + Bonfire Night | ≥800 Views |
| **06.11. Long 19:00** | QuizLong 50 + **E7 Timing** (einzige Variable: `publishAt` "19:00") | Geschichte (Antike → 20. Jh., KEINE Politik/Wahlen) | **History Quiz: 50 Questions From Easy to Legend 🏛️** (52 Z.) | 50, timing **5.0/1.2/1.0**, 5 Runden à 10 EASY→LEGEND, `fact` bei allen Fragen | 1 Satz Regeln, dann Q1 (leicht): "Which ancient wonder still stands today?" → Great Pyramid of Giza; Haken-Fragen verteilen: Kleopatra näher an Mondlandung als an Pyramidenbau (nur wenn nicht schon benutzt – greppen), Napoleon war durchschnittlich groß, Wikinger ohne Hörnerhelme (gegen True/False-50 greppen!), Berliner Mauer fiel 1989 (Teaser 09.11.) | world-trip | weinrot/creme | A "HISTORY QUIZ" + Foto `bilder/q2-pyramid.jpg` · B "50 QUESTIONS" Stempel + Pyramide · C "LEGEND LEVEL"; thumbBadge "50" | Keyword "history quizzes"/"history quiz bee" (Autocomplete #6/#11), eigene History-Shorts 1.081; **E7**: 14:00-Longs seit 31.10. alle 0 Views | **≥10 öffentliche Views n. 3 T** (sonst Timing nicht die Ursache) |
| **06.11. Short 16:00** | 6-Q Quick Fire (Exploit, Serie #2) | Wissenschaft | **Quick Fire Science Quiz – Can You Get 6/6? 🔬** (41 Z. + #shorts) | 6, count 2.5 / tail 0.8, leicht → schwer, schwerste an Platz 4 | Q1 (sehr leicht, broll "lightning storm night"): "What gas do plants breathe in?" → CO₂; weitere: Wasser kocht auf Mount Everest unter 100 °C (≈70 °C), Mensch hat 206 Knochen, Licht vs Schall (schneller: Licht), Diamant = Kohlenstoff, Bananen sind leicht radioaktiv (Kalium-40) – alles gegen done/ greppen ("hardest natural substance" schon benutzt!); Loop-Satz "Think you got all six? Go again!" | game-show | – | – | Exploit 6+ (1.433/1.234/1.181) + Konkurrenz #2 Think Nova; game-show = beste Short-Musik (Median 824) | ≥1.000 Views n. 3 T |
| **06.11. Short 21:00** | E2 VS #4 (Fortsetzung, Format bewährt 854/488) | Höhe von Bauwerken | **Which Is Taller? 4 Rounds 90% Get Wrong 🏙️** (43 Z.) | 4, count 3.0 / tail 1.2, correctLabel "TALLER!" | R1 (leicht): Eiffelturm 330 m vs Große Pyramide ~139 m; R2 (Haken): Freiheitsstatue inkl. Sockel 93 m vs Elizabeth Tower (Big Ben) 96 m; R3: Tokyo Skytree 634 m vs CN Tower 553 m; R4 (Haken): Christusstatue Rio 38 m inkl. Sockel vs Freiheitsstatue nur Figur 46 m – jeweils exakte Bezugsgröße in valueLabels ("93 m incl. pedestal") und Quellen in Beschreibung | world-trip | – | – (VS; images Pyramide `bilder/q2-pyramid.jpg`, sonst icons 🗼🗽🕰️⛪) | E2-Fortsetzung, Daten-Vergleich = stärkste automatisierbare Nische (Big Data Factor 2,9 Mio) | ≥500 Views n. 3 T |

Bandit 04.–06.11.: 6 Exploit / 3 Experiment (E1 #3, E5 #1, E7 #1; VS gilt nach 2/2 Treffern als Exploit) ≈ 70/30.

## Ideen-Backlog (nach erwartetem Potenzial)
1. **"Which Came First? Round 3" (6-Q-Short)** – Runde 1: 1.234, 6-Q-Format 3/3 > 1.000; Serie mit Nummer (Konkurrenz #5 "Part 3").
2. **VS "Which Is Heavier?" / "Which Is Older?" (Short)** – VS 854/488, nach E2-Verdict 07.11. als feste 21:00-Reihe.
3. **Fall of the Berlin Wall 09.11.: "Cold War Quiz – Can You Get 6/6? 🧱" (Short 16:00)** – Jahrestag, DE = Nr. 2 unseres Publikums (2.492 Views), History-Sets tragen.
4. **Veterans/Remembrance Day 11.11.: "WW1 Quiz – Can You Get 6/6?" (Short)** – US+UK = 69 % Publikum, nur Fakten.
5. **GTA Quiz (Long, 15.–18.11.)** – GTA VI laut Take-Two weiter am 19.11.2026; "GTA Quiz: How Well Do You Know Grand Theft Auto? 🎮", nur Fakten, keine Spielbilder/Logos.
6. **"Which Is Bigger? 50 Rounds" (Long)** – nur wenn QuizLong VS-Balken rendern kann (prüfen, nicht erfinden) und Long-Distribution wieder läuft.
7. **Emoji-Short "Guess the Word by Emoji – 6/6" (Short)** – Emoji-8-Länder-Short 937–1.303, Kids Quizzy "Guess the Word by Emoji" 528k.
8. **12 Tricky Riddles: Can You Solve 4? (Long ~7 min)** – Quiz World 469k (257×); erst nach Long-Fix + E1-Verdict.
9. **Thanksgiving 26.11.: "Thanksgiving Trivia: 50 Questions From Easy to Legend 🦃"** – saisonal; Halloween-35 war bestes Fragen-Long (185).
10. **"Can You Pass 5th Grade Science?" (Long)** – Autocomplete "can you pass high school quiz"/"science quiz for grade 5"; Can-You-Pass-Serie passt zum Kanalnamen.

## Für den Produktions-Agenten (gilt heute, überschreibt ältere Defaults)
- Zuerst **Technik 1–2** (Status-Felder erweitern, AI-Clip-Filter in fetch_broll) – Ergebnis in learnings.md.
- Dann **3 Items für 06.11.** anlegen: `2026-11-06-history-quiz-50-1.json` (Long, **`"publishAt": "19:00"`** = E7), `2026-11-06-six-q-quick-science.json` (publishAt "16:00"), `2026-11-06-vs-taller-4.json` (publishAt "21:00"). Sortierung "six-q" < "vs" passt.
- History-50: gegen `queue/done/*` und alle Queue-Items greppen (True/False-50 01.11. enthielt Napoleon/Wikinger/Kleopatra-Mythen → dort benutzte Fakten nicht wiederholen, andere wählen). Keine Politik-/Wahl-/Kriegsverbrechen-Details; `fact` bei allen 50 Fragen.
- VS-Taller: jede Höhe mit Bezug (Spitze/Antenne/Sockel) aus offizieller Quelle; ist ein Paar nicht eindeutig, ersetzen (z. B. Burj Khalifa 828 m vs Shanghai Tower 632 m).
- Long-Beschreibung unverändert, aber die beiden Shorts vom 06.11. auf das **neue** History-Long verlinken (erst nach dessen Upload möglich – sonst aufs Emoji-50 vom 05.11.).
- Kein Halloween, keine Wahl-/Politikfragen.
