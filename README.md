# GATE Prep

A study app for **GATE CS & IT**: 80+ interactive lessons, ~15,000 practice questions, spaced review of the questions you miss, topic drills, DPPs and CBT-style mock tests with a time-per-question analysis.

One web app, two ways to use it:

| | |
|---|---|
| **In the browser / on your phone** | https://kshiteeshd.github.io/gate-prep/ — installable (Add to Home screen) and readable offline once opened |
| **As a Windows program** | the same app in its own window, with progress kept in a local database (`BUILD_EXE.bat`) |

Your progress is saved on the device you study on. On the web it lives in the browser; use **Menu → Export progress** / **Import progress** to move it between your phone and PC.

## What is in it

- **Learn** – chapters of long-form lessons (read like a textbook), typeset maths, worked examples, proofs, GATE traps, a quick check, and interactive tools.
- **Practice** – spaced review (a missed question returns after 1, 3, 7 and 21 days), 10-question topic drills, and 30-question DPPs with instant feedback.
- **Tests** – subject tests and 30 full GATE-style mocks (GA + CS, 65 questions, 3 hours) in a CBT layout with a question palette, mark-for-review and a pre-submit review. An optional *exam-day dry run* hides hints.
- **Results** – score with GATE negative marking, where the time went, slow-and-wrong vs fast-and-wrong, weakest topics.
- **Progress** – activity calendar and a topic heat-map. **Search** with `Ctrl K`. Six themes, text sizes, full screen (`F11`).
- Layout adapts from desktop down to phones (bottom tab bar, palette as a sheet).

## Repository layout

```
web/            the app (static HTML/CSS/JS) – what GitHub Pages publishes and the desktop window shows
  data/         generated: questions per subject, tests, lessons (git-ignored; built by tools/export_site.py)
tools/          export_site.py (builds web/data), build_pack.py (builds the question pack), checks and helpers
content/        question sources (c_*.py hand-written, g_*.py generators) and the built pack.json
learn/          lesson sources (l_*, d_*, e_*.py) and the interactive-tool data
gate/           test builder, database, one-time migration from the earlier Flask version
server.py       local server for the desktop app (serves web/, stores progress in SQLite)
desktop.py      native window (pywebview)
app.py, templates/, static/   the earlier Flask interface, kept for tools/check_learn.py
.github/workflows/pages.yml   builds web/data and publishes web/ to GitHub Pages on every push to main
```

## Run it

**Web version locally**

```bash
python tools/export_site.py --public      # writes web/data (use without --public to include local past-paper files)
python -m http.server 8000 --directory web
# open http://localhost:8000
```

**Desktop version** (Windows, Python 3.10+)

```bash
pip install -r requirements.txt
python tools/export_site.py
python desktop.py
```

**Build the .exe** – run `BUILD_EXE.bat`; the result is `dist/GATEPrep/GATEPrep.exe`. Progress is stored in `%LOCALAPPDATA%\GATEPrep\gateprep.db`, outside the program folder, so rebuilding or reinstalling never touches it. The first launch of a new version copies progress from an older version's database automatically.

## Content notes

- The public site is built **without** past-paper (PYQ) questions and without any private study files; those stay on the owner's machine (`content/pyq_*.json` is git-ignored). A local build includes them if the files are present.
- Lesson text, hand-written questions and generators are original. Hand-written explanations are not machine-verified; if you find a mistake, please open an issue.
- The SQL playground lesson tool needs the desktop app (it runs a real SQLite database); everything else works in the browser.

## Updating content

Edit the sources in `content/` or `learn/`, run `python tools/build_pack.py` if question sources changed, commit and push — the workflow rebuilds and republishes the site.
