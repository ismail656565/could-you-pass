# Studio: alle Kanäle automatisiert

Das Ziel: Jeder Kanal bekommt einen Autopiloten wie COULD YOU PASS?.
Claude plant die Inhalte, eine GitHub Action vertont und rendert sie, lädt hoch, setzt den ersten Kommentar und holt die Zahlen.

| Datei | Wozu |
|---|---|
| `channels/channels.json` | Liste aller Kanäle mit Name, Handle, Google-Konto und Schutzwort gegen den falschen Kanal |
| `autopilot/studio.py` | gemeinsamer Google-Zugang (`studio.yt('perceptlab')`), Kanal-Schutz, Status-Check |
| `autopilot/kanaele-anmelden.bat` / `.command` | **einmalig lokal:** alle Kanäle mit Google verbinden |
| Workflow „Studio – Kanal-Check“ | jeden Morgen um 06:45: Ist jedes Token gültig und gehört es zum richtigen Kanal? Dazu Abos, Videos und letzte Uploads → `channels/status.md` |

## Schritt 1: Kanäle verbinden (einmalig, ca. 5 Minuten am PC)
1. Neuen Stand holen: `git pull` im Ordner `could-you-pass`.
2. `autopilot\kanaele-anmelden.bat` doppelklicken. Pro Kanal: **Google-Konto wählen → Kanal wählen → erlauben**.
   Das Skript sagt jedes Mal an, welches Konto und welchen Kanal du anklicken musst. Wählst du den falschen Kanal, merkt es das und fragt noch einmal.
3. Zum Schluss wird das Secret `YT_TOKENS_JSON` automatisch gesetzt, wenn die GitHub-CLI angemeldet ist.
   Sonst öffnet sich GitHub: Name `YT_TOKENS_JSON`, Wert mit Strg+V einfügen, dann „Add secret“.
4. Danach zeigt `channels/status.md` nach dem nächsten Check für jeden Kanal ✅.

Die Tokens liegen lokal in `autopilot/tokens.local.json`. Die Datei steht in `.gitignore` und wird nie hochgeladen.
Einen einzelnen Kanal neu verbinden: `kanaele-anmelden.bat perceptlab`.

## Schritt 2: Eine Pipeline pro Kanal (Reihenfolge)
| Kanal | Stand | Nächster Schritt |
|---|---|---|
| WILDLY TRUE | Pipeline fertig (`wildlytrue.py`) | läuft sofort, sobald das Token da ist |
| PERCEPT LAB | Format steht (optische Täuschungen) | Illusionen direkt per Code zeichnen, ganz ohne KI-Bilder |
| Myth Dug Up | Themenliste steht | Kunst- bzw. Notizbuch-Look mit huashu-art-motion |
| HUMAN LIMIT, HiddenFrontlines, PlotMelt | Nische laut Kanal-Check | Format pro Kanal festlegen |
| RageLoop Clips, The Podcast Cut | Clipping-Kampagnen | halbautomatisch, weil Quellvideo und Kampagnenregeln pro Clip nötig sind |

## Grenzen, die wir im Blick behalten
* **YouTube-API:** Uploads haben ein eigenes Kontingent von 100 pro Tag und Google-Projekt. Ein Projekt reicht für alle Kanäle.
* **GitHub Actions:** Dieses Repo ist privat, dafür gibt es 2.000 Minuten pro Monat frei. Allein COULD YOU PASS? verbraucht hochgerechnet etwa 1.500.
  Tägliche Renders für viele Kanäle passen da nicht mehr hinein. Die Render-Jobs der neuen Kanäle kommen deshalb in ein **öffentliches** Repo, dort sind sie unbegrenzt kostenlos. Die Secrets bleiben dabei privat.
* **Qualität:** YouTube demonetarisiert massenhaft gleichförmige Inhalte. Deshalb bekommt jeder Kanal ein eigenes Format, nichts wird kopiert.
