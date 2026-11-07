@echo off
rem Builds dist\GATEPrep\GATEPrep.exe from the web app in web\ (no Python needed on the target PC).
rem Progress lives in %%LOCALAPPDATA%%\GATEPrep and is never touched by a rebuild or a reinstall.
cd /d "%~dp0"
pip install -q pyinstaller flask pywebview markupsafe
python tools\build_pack.py
python tools\export_site.py
pyinstaller --noconfirm --clean --windowed --name GATEPrep --hidden-import learn.sampledb --exclude-module PyQt5 --exclude-module PySide6 --exclude-module PyQt6 --exclude-module PySide2 --exclude-module qtpy --exclude-module matplotlib --exclude-module numpy --exclude-module pandas --exclude-module scipy --exclude-module IPython --add-data "web;web" desktop.py
echo.
echo Done: dist\GATEPrep\GATEPrep.exe
pause
