"""Self-update: check a JSON feed, download the new installer, verify its SHA-256, run it silently and exit.

latest.json format:
  {"version": "1.1.0", "url": "https://.../GATEPrep-Setup-1.1.0.exe", "sha256": "<hex>", "notes": "What's new"}
Your data lives in %LOCALAPPDATA%\\GATEPrep (separate from the program), so updating never touches progress."""
import hashlib
import json
import os
import subprocess
import sys
import tempfile
import threading
import urllib.request

from . import db, version

_state = {"checked": False, "available": None, "error": None}


def _ver(v):
    return tuple(int(x) for x in str(v).strip().lstrip("v").split(".") if x.isdigit())


def feed_url():
    return db.get_setting("update_feed") or os.environ.get("GATEPREP_UPDATE_FEED") or version.UPDATE_FEED


def check(force=False):
    """Return {'version','url','sha256','notes'} when a newer version exists, else None."""
    url = feed_url()
    if not url:
        _state.update(checked=True, available=None, error="No update feed configured")
        return None
    if not url.lower().startswith("https://"):
        _state.update(checked=True, available=None, error="Update feed must use HTTPS")
        return None
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "GATEPrep/" + version.VERSION})
        with urllib.request.urlopen(req, timeout=8) as r:
            info = json.loads(r.read().decode("utf-8"))
        newer = _ver(info["version"]) > _ver(version.VERSION)
        ok = str(info.get("url", "")).lower().startswith("https://") and len(str(info.get("sha256", ""))) == 64
        _state.update(checked=True, available=info if newer and ok else None, error=None if ok or not newer else "Feed entry is missing an HTTPS url or sha256")
    except Exception as e:  # offline, bad JSON, ...
        _state.update(checked=True, available=None, error=str(e)[:120])
    return _state["available"]


def state():
    return dict(_state)


def check_in_background():
    if db.get_setting("auto_update", True) and feed_url() and not _state["checked"]:
        threading.Thread(target=check, daemon=True).start()


def install():
    """Download the installer, verify the hash, launch it silently, then exit the app."""
    info = _state["available"] or check(True)
    if not info:
        raise RuntimeError("No update available")
    dst = os.path.join(tempfile.gettempdir(), "GATEPrep-Setup-%s.exe" % info["version"])
    h = hashlib.sha256()
    req = urllib.request.Request(info["url"], headers={"User-Agent": "GATEPrep/" + version.VERSION})
    with urllib.request.urlopen(req, timeout=60) as r, open(dst, "wb") as f:
        while True:
            chunk = r.read(1 << 20)
            if not chunk:
                break
            h.update(chunk)
            f.write(chunk)
    if h.hexdigest().lower() != info["sha256"].lower():
        os.remove(dst)
        raise RuntimeError("Downloaded file failed the SHA-256 check — update aborted")
    flags = 0x00000008 | 0x00000200   # DETACHED_PROCESS | CREATE_NEW_PROCESS_GROUP
    subprocess.Popen([dst, "/SILENT", "/CLOSEAPPLICATIONS", "/RESTARTAPPLICATIONS", "/SP-"], creationflags=flags, close_fds=True)
    threading.Timer(0.8, lambda: os._exit(0)).start()
    return info["version"]
