@echo off
chcp 65001 >nul
cd /d "%~dp0.."
echo Google-Anmeldung fuer WILDLY TRUE ...
echo WICHTIG: Im Browser beim Kanal-Auswahlschritt "WILDLY TRUE" waehlen, nicht COULD YOU PASS?
python -m pip install -q google-api-python-client google-auth-oauthlib
python autopilot\wildlytrue.py auth
echo.
echo Den Wert WT_GOOGLE_REFRESH_TOKEN oben bei GitHub als Secret eintragen.
pause
