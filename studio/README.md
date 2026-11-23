# STUDIO – Kanäle mit eigener Handschrift

Jeder Kanal hat einen festen Stil, aber **jede Episode bekommt eigene, mit Code gemalte Bilder** (kein Bild-Generator,
keine Stock-Fotos). Daraus entsteht eine durchgehende Welt, durch die eine Kamera fährt.

| Baustein | Woher |
|---|---|
| Malerei (83 Stile: Vasenmalerei, Mosaik, Linolschnitt, Feldbuch …) | `vendor/drawing` = claude-drawing-skill (MIT) |
| Kamera durch *eine* Welt statt Folien, max. 2 Textebenen | Regeln aus bang-motion |
| Papierschnipsel, Klebeband, Stempel, Stück-für-Stück-Aufbau | Idee aus vox-director |
| Körnung, Vignette, Textur | huashu-art-motion |
| Stimme | Kokoro-82M (lokal, kostenlos) + faster-whisper für Wort-Timing |
| Musik + Sounds | eigener Generator `engine/audio.py` (keine Lizenzen) |

## Ablauf (GitHub Actions `studio-produce.yml`, täglich 05:30)
1. `produce.py <kanal>` nimmt die nächsten 2 Episoden aus `channels/<kanal>/episodes/`,
   malt, vertont, rendert und lädt sie **geplant** hoch (Zeiten in `channel.json`, z. B. 13:00 + 19:30).
   Kanal-Schutz: lädt nie auf einen falschen Kanal hoch (`autopilot/studio.py`).
2. `longform.py <kanal>`: lange 16:9-Videos (6–8 Min.) im 2D-Cartoon-Stil (ReachMora-Kit, verschlüsselt in `kits/`,
   Schlüssel = Secret `STUDIO_KIT_KEY`). Projekte liegen in `channels/<kanal>/longs/NNN-slug/` (script.txt, story.json, meta.json)
   und gehen am selben Tag um `long_time` online. (`long.py` = alter Zusammenschnitt aus Shorts, nur noch Reserve.)
3. Was hochgeladen ist, steht in `channels/<kanal>/state.json`.

## Neue Episode
`channels/<kanal>/episodes/NNN-slug/episode.py` mit `paint(work)` (Bilder malen) und `EPISODE = dict(...)`
(Text, Kamera, Schnipsel, Stempel, Musik) – Vorlage: `channels/mythdugup/episodes/001-troy`.
Testen: `python studio/engine/film.py <episode.py> --work /tmp/x --stills 1,5,10` (Hochformat) oder `--landscape`.

**Aussprache:** Namen und Fachwörter immer richtig geschrieben in `lines` lassen. Was die Stimme sagen soll, steht in
`engine/pronunciations.json` (für alle Episoden, z. B. `"Pyke": "Pike"`) oder pro Episode in `EPISODE['say'] = {...}`
(hat Vorrang). Nur die Stimme hört die Aussprache-Form; Untertitel, Cues (`'L1:pykrete'`) und `display` nutzen weiter
das geschriebene Wort. Kein Trick mehr mit falsch geschriebenen Zeilen + `display`-Korrektur.

## Kanäle
| Kanal | Status | Stil |
|---|---|---|
| Myth Dug Up | läuft | Kunst der jeweiligen Kultur + Feldbuch des Ausgräbers |
| HiddenFrontlines | als Nächstes | Geheimakte / Blaupause |
| HUMAN LIMIT | geplant | Röntgen / Wärmebild |
| PlotMelt | geplant | 1930er-Cartoon |
| Percept Lab | geplant | Op-Art, echte bewegte Täuschungen |
