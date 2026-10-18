# COULD YOU PASS? – Quiz-Shorts

Remotion-Vorlagen (Layouts `comic` und `neon`) + Autopilot.

## Ablauf (vollautomatisch)
1. **09:45 (Claude):** wertet `autopilot/analytics/report.json` aus, schreibt Erkenntnisse in `autopilot/analytics/learnings.md` und legt ein neues Quiz als JSON in `autopilot/queue/`.
2. **16:00 (GitHub Action `Quiz Autopilot`):** Stimme über ElevenLabs → Rendern mit Remotion → Upload auf YouTube → neue Zahlen holen → alles zurück ins Repository.

Manuell starten: Tab **Actions → Quiz Autopilot → Run workflow**. Das fertige Video liegt danach unter dem Lauf als „videos“ zum Herunterladen.

## Secrets (Settings → Secrets and variables → Actions)
- `ELEVENLABS_API_KEY`
- `GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET`, `GOOGLE_REFRESH_TOKEN` (einmalig mit `autopilot/google-anmelden.bat` erzeugen)
- optional Variable `PRIVACY` = `public` | `private` | `unlisted`
