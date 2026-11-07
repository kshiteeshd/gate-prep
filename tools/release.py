"""Build a release:  python tools/release.py 1.1.0
   1) bumps gate/version.py  2) rebuilds the question pack  3) PyInstaller build  4) Inno Setup installer (if ISCC found)
   5) writes dist/latest.json (publish it at your UPDATE_FEED URL together with the installer)."""
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ver = sys.argv[1] if len(sys.argv) > 1 else None
vp = os.path.join(ROOT, "gate", "version.py")
src = open(vp, encoding="utf-8").read()
if ver:
    src = re.sub(r'VERSION = "[^"]*"', 'VERSION = "%s"' % ver, src)
    open(vp, "w", encoding="utf-8").write(src)
ver = re.search(r'VERSION = "([^"]*)"', src).group(1)
run = lambda *a, **k: subprocess.run(a, cwd=ROOT, check=True, **k)

run(sys.executable, "tools/build_pack.py")
excl = sum([["--exclude-module", m] for m in ("PyQt5", "PySide6", "PyQt6", "PySide2", "qtpy", "matplotlib", "numpy", "pandas", "scipy", "IPython", "tkinter")], [])
run(sys.executable, "-m", "PyInstaller", "--noconfirm", "--clean", "--windowed", "--name", "GATEPrep", "--collect-submodules", "learn", *excl,
    "--add-data", "templates;templates", "--add-data", "static;static", "--add-data", "content/pack.json;content", "desktop.py")

iscc = shutil.which("iscc") or next((p for p in (r"C:\Program Files (x86)\Inno Setup 6\ISCC.exe", r"C:\Program Files\Inno Setup 6\ISCC.exe",
                                                  os.path.expandvars(r"%LOCALAPPDATA%\Programs\Inno Setup 6\ISCC.exe")) if os.path.exists(p)), None)
if iscc:
    env = dict(os.environ, GATEPREP_VERSION=ver)
    subprocess.run([iscc, os.path.join("installer", "GATEPrep.iss")], cwd=ROOT, check=True, env=env)
    setup = os.path.join(ROOT, "installer", "Output", "GATEPrep-Setup-%s.exe" % ver)
    sha = hashlib.sha256(open(setup, "rb").read()).hexdigest()
    feed = {"version": ver, "url": "https://REPLACE-WITH-YOUR-HOST/GATEPrep-Setup-%s.exe" % ver, "sha256": sha, "notes": "GATE Prep %s" % ver}
    json.dump(feed, open(os.path.join(ROOT, "installer", "Output", "latest.json"), "w"), indent=2)
    print("\nInstaller:", setup, "\nPublish latest.json (edit the url) at your UPDATE_FEED location.")
else:
    print("\nInno Setup (ISCC.exe) not found — built dist\\GATEPrep. Install Inno Setup 6 to produce the setup .exe, or run installer\\Install-GATEPrep.ps1")
