"""Reel library: one place that lists every reel we made, how it was made, its hook, where it is posted and how it did.

    python3 studio/tools/reel_library.py          # from ~/Documents/dmyor-videos
Writes studio/library/reel-library.csv, studio/library/index.html (open in a browser: thumbnails, filters, sort)
and studio/library/thumbs/<slug>.jpg. Reads only: reels/*, ready-to-post/*, analytics/catalog/content.csv,
analytics/reports/latest_by_post.csv, studio/post-queue.md. Safe to re-run any time (the agent runs it after each batch).
"""
import csv, glob, html, json, os, re, subprocess
from collections import defaultdict

ROOT = os.getcwd(); OUT = os.path.join(ROOT, "studio", "library"); os.makedirs(os.path.join(OUT, "thumbs"), exist_ok=True)

# production style -> art style (how it looks) and a short label
STYLE_BY_PREFIX = [("ill-", "animated-illustration-explainer"), ("kt-", "kinetic-typography"), ("tree-", "illustrated-scene"),
                   ("diagram-", "diagram-motion-graphics"), ("dg-", "diagram-motion-graphics"), ("hybrid-", "hybrid-graphics-plus-demo"),
                   ("pixel-", "pixel-story"), ("brand-", "cinematic-motion"), ("anim-", "prompt-animation")]
ART = {"animated-illustration-explainer": "Line-art scenes · Graphite & Sage", "kinetic-typography": "Text on screen · punch cards",
       "illustrated-scene": "Illustrated tree scenes", "diagram-motion-graphics": "Diagram nodes · dark",
       "hybrid-graphics-plus-demo": "Graphics + app demo", "pixel-story": "16-bit pixel art story",
       "cinematic-motion": "Designed cosmic canvas · cinematic", "prompt-animation": "Colourful 2D animated world"}

def read(p):
    try: return open(p, encoding="utf-8").read()
    except Exception: return ""

def clean(t):
    t = re.sub(r"\[[^\]]*\]", "", t or ""); t = re.sub(r"<[^>]+>", " ", t); t = t.replace("Deem-yor", "Dmyor")
    return re.sub(r"\s+", " ", t).strip()

def made_with(slug, d):
    """Which skill built the reel, from evidence in its folder. Returns (how, detail)."""
    src = "".join(read(os.path.join(d, f)) for f in ("reel.html", "film.html", "anim.html"))
    m = re.search(r"skills/([a-z-]+)", src)
    if m:
        sk = {"narrated-goal-tree-diagram-reel": "diagram-motion-graphics"}.get(m.group(1), m.group(1))
        return "skill", sk + ("" if sk == m.group(1) else " (then named narrated-goal-tree-diagram-reel)")
    if slug.startswith("pixel-"):
        return "skill + custom", "pixel-art-studio for sprites and scenes; film engine (pixel.html, audio, timing) written by prompt for this reel"
    if "tree-series" in src or "diagram.html" in read(os.path.join(d, "config.json")):
        return "template (pre-skill)", "tree-series template, written by prompt; later turned into the diagram-motion-graphics skill"
    if os.path.exists(os.path.join(d, "timeline.json")):
        return "skill + custom", "dmyor-reel pipeline (script, voice, sync, record); animation hand-written by prompt for this reel"
    if not glob.glob(os.path.join(d, "*.html")): return "none", "script only, never animated"
    return "prompt-built", "written by prompt, no skill"

catalog = defaultdict(list)
for r in csv.DictReader(open(os.path.join(ROOT, "analytics/catalog/content.csv"))): catalog[r["slug"]].append(r)
latest = {}
p = os.path.join(ROOT, "analytics/reports/latest_by_post.csv")
if os.path.exists(p):
    for r in csv.DictReader(open(p)): latest[(r["platform"], r["slug"])] = r.get("latest_views", "")
queue = read(os.path.join(ROOT, "studio/post-queue.md"))

def ready_dirs(slug):
    return sorted(glob.glob(os.path.join(ROOT, "ready-to-post", f"*-{slug}")) + glob.glob(os.path.join(ROOT, "ready-to-post", "_superseded", f"*-{slug}")))

rows = []
for d in sorted(glob.glob(os.path.join(ROOT, "reels", "*"))):
    if not os.path.isdir(d): continue
    slug = os.path.basename(d); cat = catalog.get(slug, [])
    rd = ready_dirs(slug); post_md = read(os.path.join(rd[-1], "post.md")) if rd else ""
    narr = {}
    for f in ("narration.json", "scene.json"):
        try: narr = json.load(open(os.path.join(d, f))); break
        except Exception: pass
    meta = {}
    try: meta = json.load(open(os.path.join(d, "script.meta.json")))
    except Exception: pass
    # hook line: first spoken thought, else first scene headline, else first caption line
    hook = ""
    if narr.get("spoken"): hook = clean(narr["spoken"].split("||")[0])
    if not hook and isinstance(narr.get("scenes"), list) and narr["scenes"] and isinstance(narr["scenes"][0], dict): hook = clean(narr["scenes"][0].get("head", ""))
    if not hook:
        lj = os.path.join(d, "vo3", "lines.json")
        if os.path.exists(lj): hook = clean(json.load(open(lj))["N1"][0][0])
    if not hook and post_md:
        m = re.search(r"## (?:Caption|Instagram caption)\s*\n+(.+)", post_md); hook = clean(m.group(1)) if m else ""
    if not hook and isinstance(narr.get("text"), list) and narr["text"]: hook = clean(narr["text"][0].get("text", "").replace("*", ""))
    if not hook:
        for ln in read(os.path.join(d, "script.md")).splitlines():
            ln = clean(ln.lstrip("#>-* ").strip())
            if ln and not ln.lower().startswith(("script", "slug", "hook", "#")) and len(ln) > 12: hook = ln; break
    if not hook and "--" in slug:
        base = slug.split("--")[0]; hook = next((r["hook"] for r in rows if r["slug"] == base), "")
    if not hook: hook = clean(meta.get("hint", ""))[:120]
    style = (cat[0]["style"] if cat else "") or next((s for pfx, s in STYLE_BY_PREFIX if slug.startswith(pfx)), "kinetic-typography" if "--bcd" in slug else "")
    if not style:
        cfg = read(os.path.join(d, "config.json")) + read(os.path.join(d, "timeline.json"))
        style = "kinetic-typography" if (meta.get("engine") or os.path.exists(os.path.join(d, "timeline.json")) or "punch" in cfg) else ("cinematic-motion" if os.path.exists(os.path.join(d, "film.html")) else "kinetic-typography (legacy)")
    posted = sorted({r["posted_at_ist"] for r in cat if r["posted_at_ist"]})
    date = posted[0][:10] if posted else (os.path.basename(rd[-1])[:10] if rd else "")
    links = {r["platform"]: r["url"] for r in cat if r["url"]}
    if any(r["url"] for r in cat): status = "posted"
    elif re.search(rf"\[x\][^\n]*\*\*{re.escape(slug)}\*\*", queue) or re.search(rf"\[x\][^\n]*{re.escape(slug)}", queue): status = "scheduled"
    elif rd and "_superseded" in rd[-1]: status = "superseded"
    elif rd: status = "ready"
    elif "--bcd" in slug or slug.endswith(("-adam", "-zara")): status = "variant"
    else: status = "draft"
    views = {pf: latest.get((pf, slug), "") for pf in ("instagram", "youtube", "x")}
    video = next((os.path.join(d, v) for v in ("reel.mp4", "film_final.mp4", "film.mp4", "anim.mp4", f"{slug}.mp4", "pixel-book-v11.mp4") if os.path.exists(os.path.join(d, v))), "")
    if not video:
        vids = sorted(glob.glob(os.path.join(d, "*.mp4")), key=os.path.getmtime); video = vids[-1] if vids else ""
    thumb = os.path.join(OUT, "thumbs", slug + ".jpg")
    if video and not os.path.exists(thumb):
        subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-ss", "0.5", "-i", video, "-frames:v", "1", "-vf", "scale=180:-2", thumb])
    length = (cat[0]["length_s"] if cat else "") or (str(meta.get("target_seconds", "")) if meta else "")
    if not length and video:
        try: length = "%.0f" % float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", video], capture_output=True, text=True).stdout)
        except Exception: pass
    voice = (cat[0]["voice"] if cat else "") or ("ElevenLabs Adam" if slug.endswith("-adam") or slug == "pixel-book" else ("ElevenLabs Zara" if slug.endswith("-zara") else ("am_eric" if narr.get("spoken") else "")))
    hook_type = cat[0]["hook_type"] if cat else ""
    if not hook_type and hook:
        h = hook.lower()
        if style == "pixel-story" or re.match(r"^[A-Z][a-z]+ (was|found|had)", hook): hook_type = "~story"
        elif h.endswith("?") or h.startswith(("want ", "what ", "why ", "how ")): hook_type = "~question"
        elif re.search(r"\b(don't|doesn't|isn't|won't|not|no|wrong|never|probably)\b", h): hook_type = "~hard-truth"
        elif re.search(r"\d", h): hook_type = "~number-fact"
        else: hook_type = "~statement"
    how, how_detail = made_with(slug, d)
    rows.append({"date": date, "slug": slug, "status": status, "style": style, "art_style": ART.get(style, ""), "made_with": how, "made_with_detail": how_detail,
                 "hook_type": hook_type, "hook": hook,
                 "topic": cat[0]["topic"] if cat else "", "voice": voice or "none", "length_s": length,
                 "experiment": cat[0]["experiment"] if cat else "", "ig_views": views["instagram"], "yt_views": views["youtube"],
                 "x_views": views["x"], "links": " ".join(f"{k}:{v}" for k, v in links.items()), "folder": os.path.relpath(d, ROOT),
                 "thumb": "thumbs/" + slug + ".jpg" if os.path.exists(thumb) else ""})

rows.sort(key=lambda r: (r["date"] or "0000", r["slug"]), reverse=True)
cols = ["date", "slug", "status", "style", "art_style", "made_with", "made_with_detail", "hook_type", "hook", "topic", "voice", "length_s", "experiment", "ig_views", "yt_views", "x_views", "links", "folder"]
with open(os.path.join(OUT, "reel-library.csv"), "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore"); w.writeheader(); w.writerows(rows)

def opts(k): return "".join(f'<option>{html.escape(v)}</option>' for v in sorted({r[k] for r in rows if r[k]}))
trs = []
for r in rows:
    links = " ".join(f'<a href="{html.escape(u)}" target="_blank">{p[:2].upper()}</a>' for p, u in (x.split(":", 1) for x in r["links"].split()) if u)
    img = f'<img src="{r["thumb"]}" loading="lazy">' if r["thumb"] else ""
    trs.append(f'<tr data-status="{r["status"]}" data-style="{html.escape(r["style"])}" data-hook="{html.escape(r["hook_type"])}" data-topic="{html.escape(r["topic"])}" data-made="{html.escape(r["made_with"])}">'
               f'<td>{img}</td><td>{r["date"]}</td><td><b>{html.escape(r["slug"])}</b><div class="f">{html.escape(r["folder"])}</div></td>'
               f'<td><span class="s {r["status"]}">{r["status"]}</span></td><td>{html.escape(r["style"])}<div class="f">{html.escape(r["art_style"])}</div></td>'
               f'<td><b>{html.escape(r["made_with"])}</b><div class="f">{html.escape(r["made_with_detail"])}</div></td>'
               f'<td>{html.escape(r["hook_type"])}</td><td class="h">{html.escape(r["hook"])}</td><td>{html.escape(r["topic"])}</td>'
               f'<td>{html.escape(r["voice"])}</td><td>{r["length_s"]}</td><td class="n">{r["ig_views"]}</td><td class="n">{r["yt_views"]}</td><td class="n">{r["x_views"]}</td><td>{links}</td></tr>')
counts = defaultdict(int)
for r in rows: counts[r["status"]] += 1
page = f"""<!doctype html><html><head><meta charset="utf-8"><title>Reel Library</title><meta name="viewport" content="width=device-width,initial-scale=1">
<style>:root{{--bg:#151719;--panel:#1d2023;--ink:#e9e7e2;--mute:#8c8f8a;--line:#33373b;--acc:#9db8a3}}
body{{margin:0;background:var(--bg);color:var(--ink);font:14px/1.4 -apple-system,Segoe UI,sans-serif;padding:20px}}
h1{{margin:0 0 4px}} .sub{{color:var(--mute);margin-bottom:14px}} select,input{{background:var(--panel);color:var(--ink);border:1px solid var(--line);border-radius:6px;padding:6px;margin-right:6px}}
table{{border-collapse:collapse;width:100%;margin-top:12px}} th,td{{border-bottom:1px solid var(--line);padding:6px 8px;vertical-align:top;text-align:left}}
th{{cursor:pointer;color:var(--mute);position:sticky;top:0;background:var(--bg)}} img{{width:72px;border-radius:6px}} .f{{color:var(--mute);font-size:12px}}
.h{{max-width:300px}} td:nth-child(6){{max-width:240px}} .n{{text-align:right}} a{{color:var(--acc);margin-right:4px}}
.s{{padding:2px 8px;border-radius:10px;font-size:12px;background:#2a2e33}} .posted{{background:#264d3a}} .scheduled{{background:#2d4466}} .ready{{background:#5a4a1f}} .superseded,.variant{{background:#3a3a3a;color:#aaa}}
</style></head><body><h1>Reel Library</h1><div class="sub">Hook types starting with ~ are guessed from the hook line (not yet in analytics). {len(rows)} reels · {" · ".join(f"{v} {k}" for k, v in sorted(counts.items()))} · built by studio/tools/reel_library.py</div>
<input id="q" placeholder="Search hook or slug"><select id="fs"><option value="">All statuses</option>{opts("status")}</select>
<select id="fm"><option value="">Any build</option>{opts("made_with")}</select><select id="fy"><option value="">All styles</option>{opts("style")}</select><select id="fh"><option value="">All hook types</option>{opts("hook_type")}</select><select id="ft"><option value="">All topics</option>{opts("topic")}</select>
<table id="t"><thead><tr><th></th><th>Date</th><th>Reel</th><th>Status</th><th>Style / art</th><th>Made with</th><th>Hook type</th><th>Hook</th><th>Topic</th><th>Voice</th><th>Sec</th><th>IG views</th><th>YT</th><th>X</th><th>Links</th></tr></thead>
<tbody>{"".join(trs)}</tbody></table>
<script>
const f=()=>{{const q=document.getElementById('q').value.toLowerCase(),s=fs.value,y=fy.value,h=fh.value,t=ft.value,m=fm.value;
for(const tr of document.querySelectorAll('#t tbody tr')){{const ok=(!s||tr.dataset.status==s)&&(!y||tr.dataset.style==y)&&(!h||tr.dataset.hook==h)&&(!t||tr.dataset.topic==t)&&(!m||tr.dataset.made==m)&&(!q||tr.innerText.toLowerCase().includes(q));tr.style.display=ok?'':'none'}}}};
['q','fs','fm','fy','fh','ft'].forEach(i=>document.getElementById(i).addEventListener('input',f));
document.querySelectorAll('th').forEach((th,i)=>th.addEventListener('click',()=>{{const b=document.querySelector('#t tbody'),rs=[...b.rows],num=i>=10&&i<=13;
const d=th.dataset.d=th.dataset.d==='1'?'-1':'1';rs.sort((a,c)=>{{let x=a.cells[i].innerText,z=c.cells[i].innerText;if(num){{x=+x||0;z=+z||0;return (x-z)*d}}return x.localeCompare(z)*d}});rs.forEach(r=>b.appendChild(r))}}));
</script></body></html>"""
open(os.path.join(OUT, "index.html"), "w").write(page)
print(f"{len(rows)} reels -> studio/library/index.html and reel-library.csv", dict(counts))
