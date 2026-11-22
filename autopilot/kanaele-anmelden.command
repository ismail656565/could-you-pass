#!/bin/bash
# Mac: Doppelklick -> alle YouTube-Kanaele mit dem Autopiloten verbinden
cd "$(dirname "$0")/.."
python3 -m pip install -q google-api-python-client google-auth-oauthlib
python3 autopilot/studio.py auth "$@"
read -p "Fertig - Enter zum Schliessen"
