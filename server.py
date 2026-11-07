"""GATE Prep — local server for the desktop app: serves the web app (web/) and keeps its saved state in the app's own SQLite database."""
import json
import os
import threading
import time

from flask import Flask, jsonify, request, send_from_directory

from gate import db, migrate, version

WEB = os.path.join(db.APP_DIR, "web")
app = Flask(__name__, static_folder=None)
_lock = threading.Lock()
_last_backup = [0.0]


def prepare():
    """Repair a damaged database if needed and make sure the tables exist. Never touches saved progress."""
    db.heal()
    db.init()
    if db.get_setting("app_version") != version.VERSION:
        db.backup("pre-update")
        db.set_setting("app_version", version.VERSION)


@app.route("/api/state", methods=["GET", "PUT", "POST"])
def state():
    if request.method == "GET":
        s = db.get_setting("spa_state")
        if not s:
            s = migrate.from_legacy()             # first launch of the new version: carry the old progress over
            db.set_setting("spa_state", s)
            db.backup("migrated")
        return jsonify(s)
    try:
        s = json.loads(request.get_data(as_text=True))
        if not isinstance(s, dict) or not s.get("v"):
            raise ValueError
    except ValueError:
        return jsonify(error="bad state"), 400
    with _lock:
        db.set_setting("spa_state", s)
        if time.time() - _last_backup[0] > 3600:   # at most one safety copy an hour
            db.backup("auto")
            _last_backup[0] = time.time()
    return jsonify(ok=True)


@app.route("/api/learn/sql", methods=["POST"])
def learn_sql():
    from learn import sampledb
    return jsonify(sampledb.run_query((request.get_json(force=True) or {}).get("sql", "")))


@app.route("/")
def index():
    return send_from_directory(WEB, "index.html")


@app.route("/<path:p>")
def files(p):
    return send_from_directory(WEB, p)


@app.after_request
def nocache(r):
    r.headers["Cache-Control"] = "no-cache"
    return r
