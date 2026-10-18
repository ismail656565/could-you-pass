@echo off
chcp 65001 >nul
cd /d "%~dp0.."
echo Google-Anmeldung fuer den Autopilot ...
python -m pip install -q google-api-python-client google-auth-oauthlib
python autopilot\autopilot.py auth
echo.
echo Die 3 Werte oben bei GitHub als Secrets eintragen.
pause
