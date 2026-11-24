---
name: shorts-retention
description: Regeln für YouTube Shorts aller Studio-Kanäle (COULD YOU PASS?, WILDLY TRUE, PERCEPT LAB, PlotMelt, Myth Dug Up, HiddenFrontlines, HUMAN LIMIT, RageLoop Clips, The Podcast Cut). Laden vor jedem Skript, Schnitt oder Render eines Shorts und bei der Diagnose, warum ein Short bei ~1.000 Views hängen bleibt.
---

# Shorts-Retention – Studio-Regeln (aus eigenen Daten, Stand 24.11.2026)

Warum: Unsere Shorts bleiben fast immer im ersten Test-Pool (≈1.000 Views). 95 % des Traffics kommt aus dem Shorts-Feed. Dort entscheiden **Sekunde 1** und **Länge**, nicht der Titel. Nur Flag Duel #1 (56 % stayed, 84 % Ø angesehen, 34 s) kam auf etwa 3.000 Views und +18 Abos.

## Zielwerte (YouTube Analytics)
- **stayed (engagedViews/views) ≥ 70 %**. Unter 60 % kommt das Short praktisch nie über ~1.500 Views.
- **Ø angesehen ≥ 90 %**, am besten > 100 % (Loop).
- Abos pro 1.000 Views ≥ 2 (Kanal-Ziel).

## Sekunde 0–1
- Erster Frame = Kerninhalt (Frage, Fakt, Bild des Ereignisses). Kein Logo, kein Intro, kein „Hey guys“.
- Erste gesprochene Worte = die Frage oder die Behauptung selbst. Keine Vorrede wie „Only one in ten get this“. Der Ego-Hook gehört als Text ins Bild, nicht in den Ton.
- Bewegung oder Pop-in im ersten Frame. Erster Frame nicht schwarz (QA misst Frame0-Luma).

## Länge
- Quiz-Shorts ≤ 27 s, Fakten-Shorts ≤ 35 s, Clips (Podcast/Rage) 20–40 s. Die Gewinner der Konkurrenz liegen bei 21–27 s.
- ≤ 80 gesprochene Wörter. Antwort- und Auflösungszeilen ≤ 4 Wörter.
- Jede Pause > 0,8 s ohne neue Information streichen (QA: Standbild max. ≤ 2,5 s).

## Ende = Loop
- Das letzte Bild muss in das erste übergehen (gleicher Hintergrund, keine lange Endkarte). Endkarte max. 1,5 s.
- Gesprochener CTA max. 1 kurzer Satz: „Follow for number N+1!“ Serien mit Folgennummer bringen messbar mehr Abos.
- Score-Prompt („Comment your score /4“) als Text, nicht als eigener Abschnitt.

## Ton
- Loudness −14 LUFS, True Peak ≤ −1 dBTP (autopilot normalisiert).
- Musik leise unter der Stimme (≈ 0,08). Sound bei jedem Reveal (ding/tick).

## Text im Bild
- Max. 3–4 Wörter pro Zeile, große Schrift, Outline. Wichtiges im mittleren Drittel, nicht in den unteren 20 % (YouTube-UI).
- Für Clip-Kanäle: Wort-für-Wort-Captions (siehe remotion-best-practices → Captions), 1–3 Wörter gleichzeitig.

## Format-Muster, die in Nov. 2026 funktionieren (vidIQ-Outliers)
- Zwei Optionen links/rechts mit Countdown, 4 steigende Level, „99 % fail the last“ (Flag Duel, Real-or-Fake-Flag).
- Serien mit Nummer im Titel („#4“, „Day 30“, „Part 9“).
- Nicht mehr: Karten-Größenvergleich (This Map Is Lying), lange 6-Fragen-Shorts > 45 s, Alters-Titel.

## Diagnose-Reihenfolge, wenn ein Short floppt
1. stayed < 60 % → Sekunde 1 (Vorrede? langsamer Einstieg? schwacher erster Frame?)
2. Ø angesehen < 80 % → zu lang oder Mittelteil zäh → kürzen
3. Beides gut, aber Views < 1.000 → Thema/Nische (Konkurrenz-Outlier prüfen)
4. Views gut, aber Abos ≈ 0 → kein Serienversprechen am Ende
