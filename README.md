# COULD YOU PASS? – Quiz-Shorts

Remotion-Vorlagen (Layouts `comic`, `neon`, `tvshow`, `stick` = 2D-Strichmännchen und `atlas` = Druck-/Atlas-Look, Standard für Shorts; dazu das Karten-Short `TrueSize`) + Autopilot.

## Ablauf (vollautomatisch)
1. **09:45 (Claude):** wertet `autopilot/analytics/report.json` aus, schreibt Erkenntnisse in `autopilot/analytics/learnings.md` und legt ein neues Quiz als JSON in `autopilot/queue/`.
2. **16:00 (GitHub Action `Quiz Autopilot`):** Stimme über ElevenLabs → Rendern mit Remotion → Upload auf YouTube → neue Zahlen holen → alles zurück ins Repository.

Manuell starten: Tab **Actions → Quiz Autopilot → Run workflow**. Das fertige Video liegt danach unter dem Lauf als „videos“ zum Herunterladen.

## Secrets (Settings → Secrets and variables → Actions)
- `ELEVENLABS_API_KEY`
- `LTX_API_KEY` (KI-Doodle-Clips für das Strichmännchen-Layout `stick`, https://console.ltx.io; optional Variable `LTX_MAX_CLIPS`, Standard 6)
- `GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET`, `GOOGLE_REFRESH_TOKEN` (einmalig mit `autopilot/google-anmelden.bat` erzeugen)
- optional Variable `PRIVACY` = `public` | `private` | `unlisted`

## Studio (alle weiteren Kanäle)
Siehe `channels/README.md`. Kurz:
- **einmalig lokal:** `autopilot/kanaele-anmelden.bat` → alle Kanäle mit Google verbinden → Secret `YT_TOKENS_JSON`
- Workflow **Studio – Kanal-Check** (täglich 06:45) → `channels/status.md`
