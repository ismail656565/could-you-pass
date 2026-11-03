# Plan – 2026-11-03

## TECHNIK-PROBLEM
1. **Status-Check E1 #1 erledigt – kein Bug:** report.json (02.11. 11:49) zeigt für "Can You Score 4/12?" (ixo369QcvVk) `public`, `madeForKids false`, `selfDeclaredMadeForKids false`, `ytRating null` – trotzdem **0 öffentliche Views nach ~46 h**, ebenso True/False-50 (01.11.) **0 nach ~23 h**. Longs bekommen praktisch keine Impressionen. **Produktions-Agent bitte prüfen:** (a) ob `publicViews` (statistics.viewCount) für diese Longs wirklich 0 ist oder die Analytics-Zahl (`views`) abweicht – beide in learnings.md notieren; (b) ob beim Long-Upload `notifySubscribers` aktiv ist und `defaultAudioLanguage`/`defaultLanguage` = "en" gesetzt sind (fehlt beides → setzen, schadet nicht). Kein weiterer Umbau.
2. **E1 #2 Presidents nur 6:21 (381 s) statt ~7 min.** Für E1 #3 (`2026-11-04-gk-well-educated-5-15.json`) vor dem Render die geschätzte Länge prüfen; liegt sie < 6:40 → `timing.count` auf 11.0 und Erklärsätze um je einen Satz verlängern (Ziel 6:45–7:30), sonst ist E1 nicht vergleichbar mit den Konkurrenz-Gewinnern (6:42–7:15).
3. keywords.md ist jetzt vom 02.11. (Montagslauf ok) → Technik 3 von gestern erledigt. competitors.json hat wieder 25 Kanäle – kurz prüfen, ob die Auto-Nachfüllung erneut Nicht-Englisch aufgenommen hat (blocked respektieren).

## Zusammenfassung (Deutsch)
- **Shorts stabil, 6+-Fragen bleibt König:** "Only Geniuses Get 6/6" (01.11.) **1.032 Views nach ~21 h** – 6+-Format jetzt 3/3 Treffer über 1.000. **VS #1 "Which Country Is Bigger?" 757 Views** (~1,7 T, 2,6× 4-Trap-Median 251) → E2 auf Kurs. Flop-Signal: **True/False-Short nur 63 Views nach 16 h** (E3 #1), leichte 1-Frage "Hours in a Week" 358 (Ziel 700 verfehlt, n. <2 T).
- **Longs weiterhin ohne Reichweite** (50-Q-Median 3 Views, E1 #1 0, True/False-50 0) – Status ist sauber, es ist reine Distribution. Einziges tragendes Long bleibt das **Emoji-Long (141 Views, stayed 73 %)**; Konkurrenz bestätigt Emoji (Quiz Bunny 646k).
- **Konkurrenz:** 7-Min-Muster wächst weiter (Quiz World Riddles 203k → **430k** in 12 Tagen, Clear Think 1,59 Mio). Neu entdeckt: **Wortschatz-Shorts** (Math Quiz "English Quizz IQ test" 152k/141k/101k, 1:05) → neues Short-Experiment E5.
- Änderung: 05.11. Long = **Emoji-50** (beste eigene Long-Bindung + 50-Q-Regel erfüllt) statt eines weiteren GK-50; 16:00 = E5 Vocabulary 6/6; 21:00 = Bonfire-Night-History-Trap (Event, UK = Top-5-Land).

## Konkurrenz-Gewinner heute (letzte 30 Tage)

| # | Video (Kanal, Abos) | Views | × Median | Länge | Titel-Muster | Was wir übernehmen → Slot |
|---|---|---|---|---|---|---|
| 1 | "10 Tricky IQ Riddles / Test Your Intelligence!" (Quiz World, 918) – 22.10. | 429.567 | 240× | 6:48 | Zahl + "Tricky" + IQ-Versprechen | Fangfragen-Anteil in E1 #3 (04.11., Queue); bei E1-Erfolg Long "12 Tricky Riddles" (Backlog 2) |
| 2 | "trivia challenge quiz 😌" (Think Nova, 2,5k) – 05.10. | 478.442 | 711× | 1:02 | Minimal-Titel, Emoji, ~1 min viele Fragen | Bestätigt 6–8 Fragen in ~1 min → alle 6-Q-Shorts (03./04./05.11. 16:00) |
| 3 | "Can You Score More Than 2? Test For Ages 70-95!" (QuizNova, 1,3k) – 10.10. | 405.929 | 141× | 6:42 | Extrem niedrige Score-Hürde + Länge ~7 min | Niedrige Hürde ("Score 5/15") in E1; Alters-Hook NICHT (bei uns gestoppt, 4–58 Views) |
| 4 | "Test Your IQ Level in just 8 Min (Part 2)" (Clear Think, 6k) – 13.10. | 215.478 | 316× | 8:09 | Zeitversprechen + IQ + **Serie (Part 2)** | Serien-Nummer im Titel ("Round 2") – genutzt bei Which-Came-First #2 (03.11.) und Emoji-50 (05.11., "Round 2" nach Emoji-15) |
| 5 | "English Quizz IQ test time" (Math Quiz, 1,1k) – 17.10. (+ "Food Quizz IQ test" 141k) | 152.412 | 57× | 1:11 | Wortschatz-/Sprachfrage als IQ-Test | **E5 05.11. 16:00 "Vocabulary Quiz – Can You Get 6/6?"** (eigene Wörter, eigene Definitionen) |

Nicht übernommen: Chauncey Asks ("Name the airline from its livery" 566k, "European city that starts with…" 792k) = Straßen-/Personenformat + Markenlogos; FootyMind/BLINK = Spielerfotos (Rechte); Quiz Phoenix Disney-Songs (Musikrechte); Dopamine F1-Google-Earth (Kartenbilder).

## 3-Tage-Plan

Layout überall **tvshow**. Zeiten Berlin. Fakten vor dem Schreiben prüfen (Britannica/NASA/UN/Merriam-Webster/Oxford). broll-Regeln (learnings 30.10.) gelten. **03.11. und 04.11. liegen in der Queue → nur 05.11. neu anlegen.**

| Datum / Slot | Format | Thema | Arbeitstitel (YouTube) | Fragen + timing | Hook / Frage 1 | Musik | cardColors | Thumbnail A/B/C + Foto | Warum | Erfolgskriterium |
|---|---|---|---|---|---|---|---|---|---|---|
| **03.11. Long 14:00** | QuizLong 50 (Queue) | Geografie | Geography Quiz: 50 Questions From Easy to Legend 🌍 | 50, Queue | Queue | world-trip | petrol | Queue (Flagge Brasilien) | Exploit Suchbegriff "geography quiz hard" | ≥50 Views n. 3 T |
| **03.11. Short 16:00** | 6-Fragen (Queue) | Which Came First #2 | Which Came First? Round 2 – 6 Questions 🤯 | 6, 2.5/0.8 | Queue | brain-pulse | – | – | Exploit (Runde 1: 1.234) | ≥1.000 Views |
| **03.11. Short 21:00** | E4 Titel-Test (Queue) | Geschichte | 4 History Questions – The Last One Will Humble You 😏 | 4, 2.5/1.0 | Queue | brain-pulse | – | – | E4 (nur Titel) | ≥800 Views UND mehr Kommentare als 26.10. |
| **04.11. Long 14:00** | E1 #3 7-Min-Test (Queue) | GK sehr schwer + 5 Fangfragen | Are You Well Educated? Hard Quiz – Score 5/15 to Pass 🎓 | 15, 10.0/2.6/0.95 (**Länge ≥6:40 prüfen, Technik 2**) | Queue | brain-pulse | dunkelgrün/gold | Queue: A "SCORE 5/15?" + Pyramide · B "WELL EDUCATED?" · C "5 TRICK QUESTIONS" | E1 #3; Konkurrenz #1/#3 | ≥30 Views n. 3 T ODER Ø angesehen ≥45 %; E1 Stopp wenn #1–#3 alle < Long-Median |
| **04.11. Short 16:00** | 6-Fragen (Queue) | Geografie Quick Fire | Quick Fire Geography Quiz – Can You Get 6/6? 🌍 | 6, 2.5/0.8 | Queue (Machu Picchu) | game-show | – | – | Exploit 6+ (3/3 > 1.000) | ≥1.000 Views |
| **04.11. Short 21:00** | E2 VS #3 (Queue) | Einwohner | Which Has More People? 4 Rounds 90% Get Wrong 👥 | 4, 3.0/1.2 | Queue (Nigeria vs Brasilien) | world-trip | – | – | E2 (VS #1 757) | E2 gesamt: 3 VS ≥294 Views n. 3 T |
| **05.11. Long 14:00** | **QuizLong 50 – Emoji-Raten** (Exploit: bestes eigenes Long, stayed 73 %) | Wörter/Begriffe aus Emojis (Alltag, Tiere, Essen, Orte, Berufe – KEINE Film-/Marken-/Songtitel) | **Emoji Quiz: Guess the Word – 50 Rounds, Easy to Legend 🧩** (56 Z.) | 50, timing **5.0 / 1.2 / 1.0**, 5 Runden à 10 (EASY → MEDIUM → HARD → VERY HARD → LEGEND); Rätsel steht als `cardText` (z. B. "🐝 + 🍯"), Frage-Zeile "Which word is this?", 4 Antwortoptionen | Intro 1 Satz: "Fifty emoji puzzles, easy to legend – how far can you get?" Q1 (sehr leicht): "☀️ + 🌻" → Sunflower; weitere Ideen (nur eindeutige Paare!): "⭐ + 🐟" Starfish, "🧈 + 🪰" Butterfly, "🌙 + 💡" Moonlight, "🍿 + 🌽" Popcorn, "🐌 + ✉️" Snail mail (VERY HARD), "☁️ + 🏙️ + ⬆️" Skyscraper (LEGEND); jede Antwort eindeutig, Distraktoren plausibel; gegen done/emoji-word-15 greppen (keine Wiederholung) | game-show | gelb/violett (neu, nicht petrol/navy) | A "EMOJI QUIZ" + großes thumbEmoji 🧩 (kein Foto nötig) · B "50/50?" · C "ONLY 1% GET #50"; thumbBadge "50" | Exploit eigener bester Long (Emoji-15: 141 Views, stayed 73 %) + Konkurrenz Quiz Bunny "Guess the Movie by Emoji" 646k (105×) + Keyword "emoji picture quiz" (Autocomplete #21); Serien-Effekt (Clear Think Part 2) | ≥50 Views n. 3 T ODER stayed ≥60 % |
| **05.11. Short 16:00** | **E5 – 6-Fragen Wortschatz** (Variable: Thema; Format bleibt 6-Q) | Bedeutung seltener, aber echter englischer Wörter (Merriam-Webster prüfen) | **Vocabulary Quiz – Can You Get 6/6? 📚** (39 Z. + #shorts) | 6, count 2.5 / tail 0.8, leicht → schwer, schwerste an Platz 4 | Frage = "What does '___' mean?" mit 3 Optionen. Ideen: "Petrichor" (Geruch nach Regen), "Ephemeral" (kurzlebig), "Defenestration" (aus dem Fenster werfen – Haken Q4), "Sonder", NUR wenn im Wörterbuch (sonst "Serendipity"), "Ubiquitous", letztes "Tittle" NICHT (schon benutzt 24.10.) → "Lethologica" (Wort auf der Zunge vergessen); Loop-Satz "Think you got all six? Go again!" | brain-pulse | – | – (Short; cardText = das Wort groß, broll neutral z. B. "old library books") | Experiment E5; Konkurrenz #5 Math Quiz 152k/141k/101k (3 Gewinner in 6 Wochen) + eigenes 6-Q-Format (3/3 > 1.000) | ≥1.000 Views n. 3 T (= 6-Q-Niveau); < 500 → Thema verworfen |
| **05.11. Short 21:00** | 4-Fragen-Trap (Exploit: "4 History Questions" 1.081) + Event | **Bonfire Night / Gunpowder Plot** (05.11., UK) | **4 Gunpowder Plot Questions – Can You Get 4/4? 💥** (49 Z.) | 4, count 2.5 / tail 1.0 | Q1 (leicht, broll "fireworks night sky"): "What year was the Gunpowder Plot?" → 1605; Q2: "Which building did the plotters try to blow up?" → House of Lords (Haken: nicht Big Ben – der Turm existierte noch nicht); Q3 (schwerste, Platz 3/4): "Was Guy Fawkes the leader of the plot?" → Nein, Robert Catesby; Q4: "What was Guy Fawkes caught guarding?" → ~36 Fässer Schießpulver (Zahl vorher prüfen, UK Parliament-Website). Halloween-Duplikat 21.10. ("Gunpowder") greppen – Frage nicht wiederholen. Kein Feuer-/Horror-Look | brain-pulse | – | – | Exploit History-Set + Event-Suche "bonfire night quiz" (jährl. Spitze 05.11.), UK im Top-5 unseres Publikums | ≥800 Views n. 3 T |

Bandit 03.–05.11.: 6 Exploit / 3 Experiment (E1 #3, E2 #3, E5 #1; E4 #1 zählt als Titel-Variante) ≈ 70/30.

## Ideen-Backlog (nach erwartetem Potenzial)
1. **"Which Is Bigger? 50 Rounds" (Long, VS-Balken)** – sobald E2 #3 ≥294 (VS #1 757); Daten-Vergleiche = beste automatisierbare Nische, Long-Version könnte das Long-Reichweitenloch knacken.
2. **12 Tricky Riddles: Can You Solve 4? (Long ~7 min)** – Quiz World 430k (240×), Quiz Guy "12 Puzzles" 78k (68×), Puzzle Code 66k bei 208 Abos; nur wenn E1 Kriterium erfüllt (Verdict 07.11.).
3. **GTA Quiz (Long, 15.–18.11., Release 19.11.)** – "GTA Quiz: How Well Do You Know Grand Theft Auto? 🎮"; nur Fakten, keine Spielbilder/Logos.
4. **Quick Fire General Knowledge – 8 Questions (Short-Serie)** – FlameTimer 6,9 Mio, Think Nova 478k; 6+-Format 3/3 > 1.000.
5. **Vocabulary Round 2 / "Words Nobody Knows" (Short)** – nur wenn E5 #1 ≥1.000; Math Quiz hat 3 Gewinner mit Sprache.
6. **Veterans Day / Remembrance Day 11.11.: "WW1 History Quiz – Can You Score 5/15?"** (Long, E1-Mechanik falls E1 positiv, sonst 6-Q-Short "11/11 History") – Event, nur Fakten.
7. **Fall of the Berlin Wall 09.11.: "Cold War Quiz – Can You Get 6/6?" (Short)** – Jahrestag, Geschichtssets tragen (1.081).
8. **Thanksgiving 26.11.: "Thanksgiving Trivia: 50 Questions From Easy to Legend 🦃"** – saisonal (Halloween-35 war bestes Q-Long mit 184).
9. **"Can You Get 6/6?" nach Themen (Space, Animals, Food)** – Y King 316k; reine Themen-Sets mit 6 Q.
10. **Tricky Quiz – Level 1/2/3 (Short-Serie)** – Instagram 1,66 Mio; Serien bringen Wiederkehrer; nach E4/E5.

## Für den Produktions-Agenten (gilt heute, überschreibt ältere Defaults)
- Zuerst **Technik 1–2** (Views-Abgleich Longs, Länge E1 #3 ≥6:40) – Ergebnis in learnings.md.
- Dann **3 Items für 05.11.** anlegen: `2026-11-05-emoji-word-50-1.json` (Long), `2026-11-05-six-q-vocabulary-1.json` (publishAt "16:00"), `2026-11-05-trap-4-gunpowder.json` (publishAt "21:00"). Sortierung "six-q" < "trap" passt.
- Emoji-50: Rätsel in `cardText` (EMOJI_FONT rendert in QuizLong), jede Lösung **eindeutig**; keine Film-, Marken-, Song- oder Personennamen (Rechte + Streit). broll nur für die ersten 2 Fragen jeder Runde ODER ganz weglassen (Emoji ist das Bild). Beschreibung: "All emoji puzzles are original."
- Vocabulary-Short: jede Definition gegen Merriam-Webster/Oxford prüfen; nur Wörter, die dort stehen (kein "Sonder", falls nicht gelistet).
- Gunpowder-Short: Fakten gegen parliament.uk prüfen; keine Frage aus `done/2026-10-21-halloween-trap-4-0.json` wiederholen.
- Kein Halloween-/Spooky-Bezug, kein Schwarz-Orange, keine Politik-/Wahlfragen (Wahltag heute 03.11.).
