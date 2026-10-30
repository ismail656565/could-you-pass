# Plan – 2026-10-30

## TECHNIK-PROBLEM
1. **Queue 31.10. unvollständig:** nur `2026-10-31-vs-countries-bigger-1.json` (Short 21:00). Produktions-Agent muss heute zusätzlich **Long 14:00 + Short 16:00 für 31.10.** anlegen (siehe Tabelle), sonst springt wieder der Ersatz-Generator ein (27.–29.10. lief nur noch generate_queue.py).
2. **Thumbnail-A/B/C-Test misst keine CTR:** log 29.10. 18:02 → `HttpError 400` bei youtubeanalytics reports (Thumbnail-Test fällt auf "views/day" zurück). Abfrage prüfen (vermutlich Metrik `impressions`/`impressionClickThroughRate` wird von der Analytics-API v2 nicht unterstützt bzw. falsche dimensions/startDate). Fix: Fehler abfangen, CTR weglassen, Rotation weiter nach views/day – aber 400 nicht täglich loggen.
3. competitors.json bereinigt (25 → 20): entfernt Routed (Food-Vlog/Bollywood), GK Prashnix (Hindi), Quiz Baazi (Urdu), Shailesh Rajput (Bollywood), ABCInfoTales (Kinder-Lernvideos) – off-topic für englische Quiz-Zielgruppe.

## Zusammenfassung (Deutsch)
- **Einfach schlägt schwer:** Die 3 Ersatz-Generator-Shorts mit leichten Einzelfragen ("Can You Answer: What is the smallest prime number?") holten Median **1.112 Views** – kuratierte "schwere" 1-Frage-Ego-Hooks nur **330** (n=5). 6+-Fragen-Shorts bleiben Spitze (Median **1.333**, stayed 56 %). tvshow-Layout Median 958 vs. neon 338, Musik game-show 1.072 vs. brain-pulse 338.
- **Lange Videos sind das Problem:** 11 Videos, Median <20 Views, CTR 2,9 %, 7 Abos gesamt. 50-Fragen-Videos Median 3 Views. Konkurrenz zeigt: kleine Kanäle (1–5k Abos) machen 0,4–1,3 Mio mit **~7-Minuten-Tests, 10–12 Fragen, niedrige Score-Hürde im Titel**.
- **Änderungen:** (a) ab 31.10. Long-Slot im Wechsel 7-Min-Experiment ↔ 50-Fragen-Suchthema; (b) 16:00-Short: leichte, sofort verständliche Frage + Titel "Can You Answer …?" statt Nischen-Fakt; (c) 6-Fragen-Short kommt zurück (01.11.); (d) "True or False" (Autocomplete Nr. 1, Score 17,8) als Long und Short.
- Events: **01.11. US-Zeitumstellung**, **03.11. US-Midterms** (Civics/Presidents-Quiz passt), **05.11. Guy Fawkes/Bonfire Night** (UK-Geschichte). Halloween bleibt tabu (auch 31.10. kein Halloween-Bezug!).

## Konkurrenz-Gewinner heute

| # | Video (Kanal, Abos) | Views | × Median | Länge | Titel-Muster | Was wir übernehmen → Slot |
|---|---|---|---|---|---|---|
| 1 | "Test Your iQ in just 7 minutes" (Clear Think, 4,9k) | 1,26 Mio | 2006× | 6:48 | Zeitversprechen "in just 7 minutes" + IQ | Länge ~7 min, Zeit im Titel → **Long 31.10.** |
| 2 | "Are You Well Educated? … Score At Least 4/10!" (GK STUDIO PRO, 1,7k) | 971k | 1187× | 7:15 | Identitäts-Frage + **niedrige Hürde "at least 4/10"** | 10–12 sehr schwere GK-Fragen, Hürde ~⅓ → **Long 31.10.** |
| 3 | "Can You Score More Than 2? Test For Ages 70-95!" (QuizNova, 1,2k) | 380k | 180× | 6:42 | "More than X" + Altersgruppe | Hürde-Mechanik bestätigt (3 Videos des Kanals >50k); Altersansprache bei uns gefloppt → ohne Alter testen; 2. Variante im Backlog |
| 4 | "trivia challenge quiz 😌" (Think Nova, 2,5k) | 471k | 725× | 1:02 | generischer Suchbegriff, ~6–8 leichte GK-Fragen | deckt sich mit unserem 6+-Fragen-Sieger → **Short 16:00 01.11.** |
| 5 | "Only 1% Can Get 50/50 on This Animal Quiz!" (Quiz Dolphy, 953) | 162k | 142× | 23:30 | Suchthema + "50/50" + "Only 1%" | läuft heute als Animal Quiz 50 (14:00); Titel-Variante "Only 1%" im Backlog falls Animal floppt |

## 3-Tage-Plan

Layout überall **tvshow**. Zeiten Berlin. Fakten vor dem Schreiben prüfen (Britannica/NASA/CIA Factbook/Guinness).

| Datum / Slot | Format | Thema | Arbeitstitel (YouTube) | Fragen + timing | Hook / Frage 1 | Musik | cardColors | Thumbnail A/B/C + Foto | Warum | Erfolgskriterium |
|---|---|---|---|---|---|---|---|---|---|---|
| **30.10. Long 14:00** | QuizLong 50 | Tiere | (in Queue) Animal Quiz: 50 Questions From Easy to Legend 🐾 | 50, count 5.0/tail 1.2 | in Queue | game-show | petrol | in Queue | Suchthema-Test (Konkurrenz #5) | ≥50 Views nach 3 T (Kanal-Median Long ≈10) |
| **30.10. Short 16:00** | 1-Frage-Ego-Hook | Faultier | (in Queue) | 1 | in Queue | world-trip | – | – | bereits produziert | – |
| **30.10. Short 21:00** | 4-Fragen-Trap | Essen | (in Queue) 4 Food Questions Almost Everyone Gets Wrong | 4 | in Queue | game-show | – | – | bereits produziert | – |
| **31.10. Long 14:00** | QuizLong **12 Fragen, ~7 min** – EXPERIMENT E1 | sehr schweres Allgemeinwissen (Geschichte, Wissenschaft, Geografie, Sprache) | **General Knowledge Quiz: Can You Score 4/12? 🧠 7-Minute Test** | 12, level nur HARD/VERY HARD/LEGEND (4/4/4), timing count 9.0 / tail 2.0 / tempo 0.95; nach jeder Antwort 1 Satz Erklärung | Intro 1 Satz: "Twelve hard questions, seven minutes – most people score under four. First one:" Q1: "Which country has the most time zones, including overseas territories?" (France – 12, bzw. 13 mit Antarktis-Anspruch; Antwortoptionen so wählen, dass es eindeutig ist) | brain-pulse | dunkelblau/gold | A "SCORE 4/12?" + bilder/q2-pyramid.jpg · B "7-MINUTE TEST" · C "MOST SCORE UNDER 4"; thumbBadge "HARD" | Konkurrenz #1+#2 (1,26 Mio / 971k, 7 min, Hürde ⅓) | Verdict nach 3 Videos: Median ≥3× unser 50-Q-Median (≥30 Views) ODER CTR ≥4 % ODER Ø angesehen ≥45 %; sonst stoppen |
| **31.10. Short 16:00** | 1-Frage – EXPLOIT "leichte Frage" (Ersatz-Sieger 1.112 Median) | Geografie leicht | **Can You Answer: What Is the Largest Ocean? 🌊🤯** | 1, count 3.0 / tail 0.4 | Frage sofort gesprochen; 4 Antworten Atlantic/Indian/Pacific/Arctic; Loop "Follow if you got it!" | game-show | blau | – (Short) | 3/3 Ersatz-Shorts mit leichter Frage >1.100 Views | ≥700 Views nach 3 T (Median 1-Frage-Ego 330) |
| **31.10. Short 21:00** | VS-Vergleich (Exp. E2, in Queue) | Ländergröße | (in Queue) Which Country Is Bigger? 4 Rounds 90% Get Wrong | 4 | in Queue | world-trip | – | – | neues Format | 3 VS-Shorts: Views ≥ 4-Fragen-Trap-Median (294) |
| **01.11. Long 14:00** | QuizLong 50 – Keyword-Exploit | True/False Allgemeinwissen (answers ["True","False"] falls QuizLong 2 Optionen rendert, sonst Aussage + 4 echte Antwortoptionen) | **True or False Quiz: 50 Facts From Easy to Legend ✅❌** | 50, 5 Runden à 10, count 5.0 / tail 1.2 / tempo 1.0 | Intro 1 Satz; Q1 "True or false: Lightning never strikes the same place twice." (False) | game-show | grün/rot | A "TRUE OR FALSE?" + bilder/q2-octopus.jpg · B "40/50?" · C "MOST GET 30" ; thumbEmoji ✅❌ | keywords.md Nr. 1 "true or false quiz" (17,8, 23 Treffer) + "for seniors" | ≥50 Views nach 3 T |
| **01.11. Short 16:00** | 6-Fragen-Quiz – EXPLOIT (Median 1.333, stayed 56 %) | leichtes→mittleres Allgemeinwissen | **Only Geniuses Get 6/6 🧠 Trivia Challenge Quiz** | 6, count 2.5 / tail 0.8; Q1 Foto | Q1 "What is the hardest natural substance?" (Diamond), cardText; Endzeile "Think you can get all six? Go again!" | game-show | lila | – | eigener Top-Short + Konkurrenz #4 | ≥1.000 Views nach 3 T |
| **01.11. Short 21:00** | True/False-Trap 4 Fragen – EXPERIMENT E3 (Format g) | gemischte Mythen | **True or False? 4 Facts 90% Get Wrong ✅❌** | 4, count 2.5 / tail 1.0 | Q1 "True or false: Goldfish have a 3-second memory." (False), cardText | brain-pulse | grün | – | Keyword Nr. 1, eine Variable (Fragetyp) vs. 4-Fragen-Trap | Views ≥ 4-Trap-Median (294) und stayed ≥50 % |

Bandit: 9 Slots, davon 3 Experimente (E1 7-Min-Long, E2 VS, E3 True/False-Short) ≈ 33 %.

## Ideen-Backlog (nach erwartetem Potenzial)
1. **US Presidents Quiz: Can You Score 5/15?** (02./03.11. vor Midterms) – Citizenship-Konkurrent 2,56 Mio; Wahltag = Suchspitze; unpolitisch (nur Fakten).
2. **"Are You Well Educated? Score at Least 4/12"** – 2. E1-Video (Titelvariante Identitätsfrage, Konkurrenz #2).
3. **Guess the Country by Flag – 50 Flags** – Trends "guess the country" 30, Flaggen-Fotos vorhanden (10 Flaggen, mehr Fotos für 50 nötig → image-credits erweitern oder Emoji-Flaggen).
4. **Guess the Movie by Emoji (Long)** – Konkurrenz 503k; unser Emoji-Long beste Bindung (72 % nach 0:30).
5. **6-Fragen-Short "Which Came First?"** – eigener 1.234-Views-Short, Wiederholung mit neuen Paaren.
6. **Guy Fawkes / Bonfire Night 4 Questions** (Short 05.11.) – UK-Datum, Geschichte statt Halloween.
7. **Daylight Saving Time 1-Frage** ("Which US state doesn't change its clocks?") – 01.11. Zeitumstellung USA.
8. **Can You Score More Than 3? Hard Science Quiz (7 min)** – 3. E1-Variante, Konkurrenz #3.
9. **Which Is Faster? VS Tiere** – VS-Format #2, Gepard/Gabelbock usw. (Guinness-Daten).
10. **Geography Quiz Hard: 50 Questions** – Autocomplete "geography quiz hard/difficult/americans".

## Für den Produktions-Agenten (gilt heute, überschreibt ältere Defaults)
- Heute die **fehlenden 31.10.-Items** (Long 14:00 E1, Short 16:00) UND die **01.11.-Items** (alle 3) anlegen. Dateinamen so wählen, dass die Sortierung zum Slot passt (one-q < trap/vs; long eigener Slot).
- **E1 7-Min-Long ist erlaubt und überschreibt "immer 50 Fragen"** für 31.10.: genau 12 Fragen, count 9.0, kurze Erklärung (max. 1 Satz) nach jeder Antwort, Ziel 6:30–7:30 min. Score-Hürde im Titel und Outro: "Comment your score – did you beat 4?"
- 16:00-1-Frage-Shorts ab 31.10.: **leichte, allgemein bekannte Frage**, Titel "Can You Answer: <Frage>? 🤯" (keine #-Nummerierung).
- Fotos nur aus image-credits.json und nur wenn sie zur Frage passen und die Antwort nicht verraten; sonst cardText.
- Kein Halloween-Bezug am 31.10. (Titel, Fragen, Farben Orange/Schwarz vermeiden).
- Plan-Titel dürfen nur geändert werden, wenn ein Fakt nicht belegbar ist oder der Titel schon existiert.
