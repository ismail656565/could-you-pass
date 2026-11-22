@echo off
chcp 65001 >nul
cd /d "%~dp0.."
echo.
echo  ==========================================================
echo   Alle YouTube-Kanaele mit dem Autopiloten verbinden
echo   (pro Kanal: Konto waehlen, Kanal waehlen, erlauben)
echo  ==========================================================
python -m pip install -q google-api-python-client google-auth-oauthlib
python autopilot\studio.py auth %*
echo.
pause
