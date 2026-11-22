# Plan – 2026-11-22 (So)

Kanal 30 Abos (report.json 21.11. 17:55). Analytics-Views 31.308 → 21 neue Abos = **0,67 Abos/1.000 Views** (Ziel ≥ 2,0 bis 15.12.). Shorts ≈ 0,5, Longs ≈ 4,0 (aber nur ~1k Views).
Shorts ≤ 45 s halten das Niveau: Quick IQ Test **1.010**, map-lie-4 **1.043**, Capitals 1.054, Geo-Trivia 1.019, Tricky 965 – Karten-VS hat sich nach #3 (256) erholt → Serie bleibt täglich 21:00.
Rätsel-Long 194 (≈2 T, bestes Long). Thanksgiving-Long 0 öffentliche Views nach ≈5 h (Warnsignal, s. Diagnose).
**Neu heute:** jede Serien-Folge endet ab sofort gesprochen mit „Follow, number N+1 drops tomorrow!“ (in map-lie-6/7, flag-duel-1/2 bereits eingebaut). Zuschauer-Wunsch **Science** bekommt Di 24.11. 16:00 (Reno-1-Frage rückt auf Do 26.11.).

## TECHNIK-PROBLEM
1. Keine Fehler im Log (alle Läufe 21.11. grün, 11 Antworten gepostet 23:23). Kein Code-Fix nötig.
2. **Fehlende Queue-Items:** 24.11. 21:00 (map-lie-8) und 25.11. 21:00 (map-lie-9) – heute anlegen (siehe Tabelle).
3. **Thanksgiving-Long R-Oqrw1B_9o:** public, nicht „for kids“, aber `publicViews 0` nach ≈5 h (Rätsel-Long hatte 32 n. 2 h). Produktions-Agent: im nächsten report.json prüfen; wenn weiter < 5 → Titel/Thumbnail-Problem, nicht Technik (Status ist ok). Kein Eingriff am Video.
4. Thumbnail-CTR per API weiter HttpError 400 (bekannt).
5. Ich habe heute selbst geändert: Schlusszeilen (lines.a der letzten Runde) in map-lie-6, map-lie-7, flag-duel-1, flag-duel-2; `git mv` one-q-further-west → `2026-11-26-…`.

## Zuschauer
- 16 Kommentare (21 T), **1 offen → beantwortet** (@eddiecromwell2954 „It all“ = 6/6 → gelobt + auf Karten-Test eingeladen). Gesamt jetzt 12/12 beantwortet.
- FEHLER-HINWEIS (1): „I only got 1 wrong“ (@AdnanSadaqat) = Fehlklassifizierung (Score-Meldung, kein Faktenfehler), bereits beantwortet. **Kein bestätigter Fehler.**
- Wünsche: @Jo-wl5fj (Stammzuschauer, 3 Kommentare) – **Art, classical music, science** → Science-Short Di 24.11. 16:00 („You asked for it“ im gepinnten Kommentar), Kunst als Backlog #3, Klassik nur ohne Musik-Ausschnitte (Rechte) → Fakten-Fragen.

## Diagnose (Videos ≥ 3 T unter Format-Median)
| Video | Views | Ursache | Fix |
|---|---|---|---|
| Geography Quiz (17.11., 58 s) | 118 | > 45 s + abgenutzter „Only Geniuses“-Titel | erledigt: ≤ 80 Wörter, Titelrotation |
| Landmarks Quiz (16.11., 55 s, atlas) | 67 | Länge + atlas + Thema (Landmarks-Bilder schwach) | Thema gestrichen |
| Country / World Geo Quiz (15./16.11.) | 149 / 152 | Länge 55–56 s, gleicher Titel 2×/Tag | erledigt |
| Bigger-VS-2 (15.11.) | 157 | alte VS-Optik vs. Karten-VS | VS nur noch als Karten-VS |
| map-lie-3 (19.11.) | 256 | erste Runde Grönland-Wiederholung (#1/#2 hatten auch Grönland) → kein Überraschungs-Hook | Grönland gesperrt für #8/#9; R1 immer ein neues, überraschendes Paar |
| US-Karten-Long (17.11.) | 38 | Karten-Longs ziehen nicht (E13 ✗) | gestrichen |
- **KPI Abos/1.000 Views je Format** (Scoreboard-Abos ÷ Views): Longs ≈ 4,0 · VS ≈ 0,9 · 6+ Fragen ≈ 0,7 · 1-Frage ≈ 0,6 · 4-Fragen-Trap ≈ 0,3 (9 Videos → bleibt gestrichen) · Karten-VS 0 (3 Videos, Analytics-Verzug; Bewertung nach #5). Abo-Hebel = Long-Views + Serien-Schluss.

## Konkurrenz-Gewinner heute (competitors.md 21.11., letzte 30 Tage)
| # | Video (Kanal) | Views / × | Länge | Muster | → Slot |
|---|---|---|---|---|---|
| 1 | „🧠 Your Brain Is Ageless! Take This 10-Question IQ Quiz“ (GK STUDIO PRO) 27.10. | 46k / 50× | 7:14 | Fragenzahl + IQ (Alter weglassen) | Sa 28.11. Rätsel-Long #3 „10-Question IQ Quiz“ |
| 2 | „ARE YOU A GENIUS? … Scoring 5 Out Of 25“ (QuizNova) 28.10. | 23k / 19× | 8:21 | niedrige Hürde | Di 24.11. Thumb B „CAN YOU SOLVE 5?“ |
| 3 | „English QuizZ iq test time“ (Math Quiz) 02.11. | 123k / 27× | 1:20 | Wortschatz als IQ-Test | Backlog #4 Vokabel-IQ-Short |
| 4 | „Can You Name F1 Track From Above? — Part 3“ (Dopamine Quiz) 31.10. | 30k / 43× | 8:50 | nummerierte Serie | Serien-Schluss „number N+1 drops tomorrow“ |
| 5 | „#392 90% FAILED HERE – Find the Difference“ (IQ Mazz) 12.11. | 27k / 16× | 0:12 | Folgennummer vorn + 90 % FAILED | bestätigt „#N“ + „90% Get #4 Wrong“ im Titel |

## 3-Tage-Plan
| Datum / Slot | Format | Thema | Titel (YouTube) | Fragen + timing | Hook / Fragen | Musik | cardColors | Thumbnail | Warum | Erfolg |
|---|---|---|---|---|---|---|---|---|---|---|
| 22.11. 16:00 (Queue) | Flag Duel #1 (flagduel) | Doppelgänger-Flaggen | Queue | 4 Runden | Queue; Schluss „Follow for flag duel number two!“ | game-show | – | – | E19 | ≥ 800 n. 3 T |
| 22.11. 21:00 (Queue) | Karten-VS #6 | India/Greenland … | This Map Is Lying To You #6 🌍 Which Is REALLY Bigger? | 4 Runden | Schluss „Follow, number seven drops tomorrow!“ | world-trip | – | – | Exploit | ≥ 800 |
| 23.11. 16:00 (Queue) | Wahr/Falsch (tvshow) | Thanksgiving | Thanksgiving True or False 🦃 90% Get #4 Wrong | 6 Aussagen | Queue | game-show | Queue | – | E18 | ≥ 500 |
| 23.11. 21:00 (Queue) | Karten-VS #7 | Cuba/Iceland … | This Map Is Lying To You #7 🌍 Which Is REALLY Bigger? | 4 | Schluss „number eight drops tomorrow!“ | world-trip | – | – | Exploit | ≥ 800 |
| **24.11. (Di) Long 14:00** (Queue) | QuizLong **exam**, 12 Rätsel | IQ-Rätsel | Test Your IQ: 12 Hard Riddles – Can You Solve 5? 🧠 | 12, count 10 | Queue | brain-pulse | Queue | B zuerst: „F“ + „CAN YOU SOLVE **5**?“ | E14 ✓ + Konkurrenz #2 | ≥ 100 n. 3 T, ≥ 1 Abo |
| **24.11. 16:00 – NEU ANLEGEN** | 6-Q tvshow (≤ 70 Wörter, ≤ 45 s) | **Science (Zuschauer-Wunsch)** | **Science Trivia: 90% Get #4 Wrong 🔬** #shorts | 6, count 2.5 / tail 0.6 | Q1 leicht/visuell (z. B. „Which planet is the hottest?“ → Venus), #4 Falle; Duplikat-grep gegen one-q-sunlight, six-q-quick-science, six-q-genius-space, solar-system-quiz-30-1; Antwortzeile ≤ 4 Wörter | game-show | ["#0F766E","#134E4A"] | – | Viewer-Wunsch + Titelmuster „X Trivia: 90% Get #4 Wrong“ (1.019) | ≥ 600 n. 3 T |
| **24.11. 21:00 – NEU ANLEGEN** | Karten-VS #8 (truesize) | nur vorhandene Formen, **kein Grönland** | This Map Is Lying To You #8 🌍 Which Is REALLY Bigger? | 4 Runden, ≤ 55 Wörter | Vorschlag: R1 **Turkey** 783,562 vs Texas 695,662 (Twist US-Stolz) · R2 **France** (Festland) vs Montana · R3 **Philippines** 300,000 vs Colorado 269,601 · R4 **China** vs Brazil. Kontrollspalte muss jede Seite stützen, sonst Paar aus iran/romania/minnesota/utah/nevada ersetzen. Gewinnerseite mischen. Schluss „Follow, number nine drops tomorrow!“ | world-trip | – | – | Exploit (1.043 / 935 / 1.021) + 75 % US-Publikum | ≥ 800 |
| 25.11. 16:00 (Queue) | Flag Duel #2 | Iceland/Norway … | Queue | 4 | Schluss „Follow for number three!“ | game-show | – | – | E19 | ≥ 800 |
| **25.11. 21:00 – NEU ANLEGEN** | Karten-VS #9 | US-Staaten vs Länder | This Map Is Lying To You #9 🌍 Which Is REALLY Bigger? | 4 | Vorschlag: R1 **Iran** vs Alaska (nur wenn Kontrolle eindeutig, sonst Iran vs Mongolia) · R2 **Minnesota** vs Romania (nur bei ≥ 5 %, sonst Utah/UK) · R3 **Nevada** vs UK · R4 **Sri Lanka** vs … (falls kein Partner: Japan vs Germany). Paare nie aus #1–#8 wiederholen. Schluss „Follow, number ten drops tomorrow!“ | world-trip | – | – | Exploit | ≥ 800 |

Vorschau: Do 26.11. Long „Christmas Quiz 🎄 50 Questions – Can You Get 40?“ (exam, Thumb B „CAN YOU GET **40/50**?“) + 16:00 Reno-1-Frage (Queue) · Fr 27.11. 16:00 Flag Duel #3 · Sa 28.11. Rätsel-Long #3.
Bandit 23.–25.11. (7 Slots): 5 Exploit (Karten-VS ×3, Rätsel-Long, Science = Wunsch im Gewinner-Titelmuster), 2 Experimente (E18, E19).

## Ideen-Backlog
1. Rätsel-Long jeden Di/Sa – 194 Views, bestes Long; Konkurrenz 46k–1,9 Mio.
2. Christmas-Long 26.11. – Saisonsuche startet, Still Sharp 62,9k.
3. Kunst-Short „Art Trivia: 90% Get #4 Wrong 🎨“ – Zuschauer-Wunsch @Jo-wl5fj.
4. Vokabel-IQ-Short – Math Quiz 123k (27×).
5. Flag Duel als Serie 2–3×/Woche – wenn E19 ≥ 800.
6. Klassik-Fakten-Short („Which composer was deaf?“) – Wunsch, ohne Musik-Ausschnitte.
7. „Can You Pass the U.S. Citizenship Test?“ Long #2 – Trivia Square 2,79 Mio; 54 % Publikum 65+, 44 % USA.
8. Black-Friday „Which Costs More?“ 27.11. – nur Listenpreise.
9. Advent-Serie ab 29.11. „Christmas Trivia #1–24“ – Serienlogik + Saison.
10. Find-the-Difference-Short – IQ Mazz #392 (Serie) – braucht neuen Render-Baustein → erst prüfen.

## Für den Produktions-Agenten (heute)
- Anlegen: `2026-11-24-six-q-science-trivia.json` (16:00), `2026-11-24-map-lie-8.json` (21:00), `2026-11-25-map-lie-9.json` (21:00). Reno liegt jetzt als `2026-11-26-one-q-further-west.json` (publishAt 16:00) – nicht anfassen.
- **Serien-Schluss Pflicht:** letzte Antwortzeile jeder Karten-VS/Flag-Duel-Folge = Antwort + „Follow, number <N+1> drops tomorrow!“ (Flag Duel: „Follow for flag duel number <N+1>!“, da nicht täglich). Bei Mehrfragen-Shorts letzte Zeile „Follow for a new quiz every day!“. Zählt in die ≤ 80 Wörter.
- Science-Short: gepinnter Kommentar beginnt mit „You asked for it – science! 🔬“.
- Longs nur `layout "exam"`, thumbTexts[1] als Hürde („CAN YOU SOLVE **5**?“ / „CAN YOU GET **40/50**?“).
- Karten-VS: Grönland gesperrt, R1 muss überraschen, Kontrollspalte für jedes Paar ≥ 5 %.
- Weiter verboten: Halloween, Alters-Titel, Politik (Syria/Iran nur als neutrale Fläche, Iran im Zweifel weglassen), Longs Mo/Mi/Fr/So, 3. Short.

## NACHTRAG 22.11. 18:15 – E19 Flag Duel startet stärker als alles bisher (Besitzer-Screenshot)
- flag-duel-1: **1.000 Views in 2 h 15 min**, 58,1 % stayed, 7 Likes, 2 Kommentare (Karten-VS braucht ~1 Tag für 1.000). Kanal 32 Abos.
- Konsequenz: **flag-duel-2 vorgezogen auf Mo 23.11. 16:00** (Datei `2026-11-23-flag-duel-2.json`) – passt zum gesprochenen Schluss „Follow for flag duel number two!“. Thanksgiving-Wahr/Falsch (E18) rückt auf **Mi 25.11. 16:00** (`2026-11-25-true-false-thanksgiving.json`, Tag vor Thanksgiving).
- Produktions-Agent: flag-duel-2 Schlusszeile bleibt „Follow for number three!“; **flag-duel-3 für Mi 25.11. NICHT anlegen** (16:00 = E18), aber Flag Duel #3 für Fr 27.11. 16:00 vorbereiten (neue Doppelgänger-Paare, z. B. Romania/Andorra-Stil nur wenn klar unterscheidbar; Indonesia/Monaco verboten).
- Verdict E19 nach 3 Tagen; bleibt flag-duel-1 ≥ 2.000 → Flag Duel wird feste Serie 16:00 jeden 2. Tag.
