"""Build studio/sfx-library/compare.html: our synthesised effect next to 2 CC0 recordings per object, to listen and pick.
Run from ~/Documents/dmyor-videos:  python3 studio/sfx-library/build_compare.py
Candidates go to studio/sfx-library/candidates/<object>-<n>.wav (logged in LICENSES.md by fetch_sfx)."""
import importlib.util, os, sys, wave, html
import numpy as np
ROOT = os.getcwd(); LIB = os.path.join(ROOT, "studio", "sfx-library"); CAND = os.path.join(LIB, "candidates")
sys.path.insert(0, os.path.join(ROOT, "studio", "tools"))
import fetch_sfx
fetch_sfx.LIB = CAND
spec = importlib.util.spec_from_file_location("sfx", os.path.join(ROOT, ".claude/skills/animated-illustration-explainer/scripts/sfx.py"))
sfx = importlib.util.module_from_spec(spec); spec.loader.exec_module(sfx)

# object -> (synth function name, search words)
OBJECTS = {
    "page-flip":  ("page",   "page turn paper"),
    "typing":     ("typing", "keyboard typing"),
    "door-close": ("door",   "door close"),
    "plate-clink":("plate",  "weight plate clink"),
    "stamp":      ("stamp",  "rubber stamp"),
    "clock-tick": ("tick",   "clock tick"),
    "footstep":   ("step",   "footstep"),
    "phone-buzz": ("buzz",   "phone vibrate"),
    "switch":     ("toggle", "switch click"),
}
os.makedirs(CAND, exist_ok=True)
rows = []
for obj, (fn, q) in OBJECTS.items():
    x = getattr(sfx, fn)(); x = x / (np.abs(x).max() + 1e-9) * .5
    syn = os.path.join(CAND, f"{obj}-synth.wav")
    with wave.open(syn, "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(sfx.SR); w.writeframes((x * 32767).astype("<i2").tobytes())
    found = []
    try:
        rs = fetch_sfx.search(q, False, 4)
    except SystemExit as e:
        rs = []; print(obj, "search failed:", e)
    for n, r in enumerate(rs[:2], 1):
        name = f"{obj}-{n}"
        if not os.path.exists(os.path.join(CAND, name + ".wav")):
            try: fetch_sfx.fetch(r, name)
            except SystemExit as e: print(obj, n, "failed:", e); continue
        found.append((name, r))
    rows.append((obj, q, found))
cards = ""
for obj, q, found in rows:
    cards += f'<section><h2>{html.escape(obj)} <small>search: {html.escape(q)}</small></h2><div class="r"><div><b>our synth</b><audio controls src="candidates/{obj}-synth.wav"></audio></div>'
    for name, r in found:
        cards += f'<div><b>{html.escape(name)}</b> <small>{(r.get("duration") or 0)/1000:.1f}s by {html.escape(r.get("creator") or "?")}</small><audio controls src="candidates/{name}.wav"></audio></div>'
    cards += "</div></section>"
open(os.path.join(LIB, "compare.html"), "w").write(f"""<!doctype html><meta charset=utf-8><title>Sound compare</title>
<style>body{{background:#151719;color:#e9e7e2;font:15px -apple-system,sans-serif;padding:24px;max-width:900px;margin:auto}}section{{border-bottom:1px solid #33373b;padding:12px 0}}
h2{{margin:0 0 8px}}small{{color:#8c8f8a;font-weight:400}}.r{{display:flex;gap:18px;flex-wrap:wrap}}.r div{{min-width:230px}}audio{{display:block;margin-top:4px;width:230px}}</style>
<h1>Our synth vs CC0 recordings</h1><p>All recordings are CC0. Play each row, note which you prefer (or tell me "keep synth").</p>{cards}""")
print("built studio/sfx-library/compare.html")
