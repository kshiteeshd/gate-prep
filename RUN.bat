@echo off
title GATE Prep
cd /d "%~dp0"
python --version >nul 2>&1
if errorlevel 1 (
  echo [ERROR] Python not found. Install Python 3.10+ from https://www.python.org/downloads/
  pause & exit /b 1
)
pip install -q -r requirements.txt
if not exist web\data\meta.json python tools\export_site.py
start "" pythonw desktop.py
