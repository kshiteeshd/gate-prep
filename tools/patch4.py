R = "E:/Test Platform/"


def rd(p): return open(R + p, encoding="utf-8").read()
def wr(p, s): open(R + p, "w", encoding="utf-8").write(s)


s = rd("installer/GATEPrep.iss")
s = s.replace("{{6B1D2E5C-3F0A-4C9E-9B7A-GATEPREP0001}", "{{6B1D2E5C-3F0A-4C9E-9B7A-0A7E9CE00001}")
wr("installer/GATEPrep.iss", s)

s = rd("app.py")
s = s.replace("from gate import db, game, seed, service, syllabus", "from gate import db, game, seed, service, syllabus, updater, version")
s = s.replace("seed.ensure_ready()\n", "seed.ensure_ready()\nupdater.check_in_background()\n", 1)
s = s.replace('"strict": db.get_setting("strict", False), "now_year": datetime.now().year}',
              '"strict": db.get_setting("strict", False), "now_year": datetime.now().year,\n            "update": updater.state()["available"], "APP_VERSION": version.VERSION}')
s = s.replace('''        db.set_setting("strict", request.form.get("strict") == "on")''', '''        db.set_setting("strict", request.form.get("strict") == "on")
        db.set_setting("auto_update", request.form.get("auto_update") == "on")
        db.set_setting("update_feed", (request.form.get("update_feed") or "").strip())''')
s = s.replace('    return render_template("settings.html", db_path=db.DB_PATH)',
              '    return render_template("settings.html", db_path=db.DB_PATH, auto_update=db.get_setting("auto_update", True),\n                           feed=updater.feed_url(), ustate=updater.state())')
s = s.replace('@app.route("/settings/backup")', '''@app.route("/update/check", methods=["POST"])
def update_check():
    info = updater.check(True)
    st = updater.state()
    flash(("Version %s is available — use the banner or the button below to install." % info["version"]) if info else
          ("Could not check: %s" % st["error"] if st["error"] else "You are on the latest version (%s)." % version.VERSION), "ok" if not st["error"] else "err")
    return redirect(url_for("settings"))


@app.route("/update/install", methods=["POST"])
def update_install():
    try:
        v = updater.install()
        return "Installing version %s … the app will close and reopen automatically." % v
    except Exception as e:
        flash("Update failed: %s" % e, "err")
        return redirect(url_for("settings"))


@app.route("/settings/backup")''')
wr("app.py", s)

s = rd("templates/base.html")
s = s.replace('<div class="page">', '''<div class="page">
   {% if update %}<div class="flash ok row sp"><span>⬆ <b>GATE Prep {{ update.version }}</b> is available{% if update.notes %} — {{ update.notes }}{% endif %}</span>
     <form method="post" action="/update/install"><button class="btn pri sm">Update &amp; restart</button></form></div>{% endif %}''', 1)
wr("templates/base.html", s)

s = rd("templates/settings.html")
s = s.replace('''  <button class="btn pri" style="margin-top:20px">Save</button></form>''', '''  <label class="f row" style="gap:10px;margin-top:20px"><input type="checkbox" name="auto_update" {{ 'checked' if auto_update }} style="width:auto"> Check for updates automatically</label>
  <label class="f">Update feed URL (HTTPS, latest.json)</label><input type="text" name="update_feed" value="{{ feed }}" placeholder="https://…/latest.json">
  <p class="small muted" style="margin:6px 0 0">Version <b>{{ APP_VERSION }}</b>{% if ustate.error %} · last check: {{ ustate.error }}{% endif %}</p>
  <button class="btn pri" style="margin-top:20px">Save</button>
  <button class="btn" formaction="/update/check" style="margin-top:20px">Check for updates now</button></form>''')
wr("templates/settings.html", s)
print("ok")
