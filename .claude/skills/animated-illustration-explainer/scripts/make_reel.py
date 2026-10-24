"""Animated illustration explainer: every spoken thought gets an animated vector scene + a short headline.

    python3 .claude/skills/animated-illustration-explainer/scripts/make_reel.py reels/<slug> [--record] [--package YYYY-MM-DD]

narration.json:
  spoken    the narration, thoughts split by "||", optional [hook]/[turn]/[land]/[outro] tags (write for the ear)
  scenes    one entry per thought, in order: {"type": <scene name>, "params": {...}, "head": "short <b>headline</b>"}
            params.cue = [word, ...]: the spoken word that triggers each animation beat (null = default timing);
            resolved to params.at (seconds after the scene starts), which both the scene and its sounds use
            or null to keep the previous scene on screen through that thought
  brand_from  index of the first thought that belongs to the brand card (usually the outro)
  sfx       "present" (default), "subtle" or "off": synthesized sound design under the voice (scripts/sfx.py, assets/events.json)
  tagline, handle, caption
Scene names: see SKILL.md (scene catalogue) / SCENES in assets/illustrated.html.
Run from the project root.
"""
import argparse, difflib, json, os, re, shutil, subprocess, sys

SKILL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROOT = os.getcwd()
if not os.path.exists(os.path.join(ROOT, "record.js")):
    sys.exit("run from the project root (folder containing record.js)")
TAG = r"\[(?:hook|body|turn|land|outro)\]\s*"
NUM = {"1": "one", "2": "two", "3": "three", "5": "five", "10": "ten", "100": "one hundred", "500": "five hundred"}
nz = lambda s: (lambda x: NUM.get(x, x))(re.sub(r"[^a-z0-9]", "", s.lower()))


def run(*cmd):
    subprocess.run(list(cmd), check=True)


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("reel"); ap.add_argument("--record", action="store_true"); ap.add_argument("--package")
    o = ap.parse_args(); d = o.reel.rstrip("/"); slug = os.path.basename(d)
    n = json.load(open(os.path.join(d, "narration.json")))
    thoughts = [t.strip() for t in n["spoken"].split("||") if t.strip()]
    scenes = n["scenes"]
    if len(scenes) != len(thoughts):
        sys.exit(f"{len(thoughts)} spoken thoughts but {len(scenes)} scenes: give one scene (or null) per thought")
    say_text = re.sub(r"\bDmyor\b", "Deem-yor", " || ".join(thoughts))
    run(os.path.join(ROOT, "tts/.venv/bin/python"), os.path.join(SKILL, "scripts/say.py"), say_text, os.path.join(d, "audio.mp3"),
        "--voice", n.get("voice", "am_eric"), "--speed", str(n.get("speed", 1.0)),
        "--gap-min", str(n.get("gap_min", 0.18)), "--gap-max", str(n.get("gap_max", 0.32)), *(["--stages"] if n.get("stages", True) else []))
    run("python3", os.path.join(ROOT, ".claude/skills/dmyor-reel/scripts/align.py"), d)
    cues = json.load(open(os.path.join(d, "cues.json"))); W = cues["words"]
    words, owner = [], []
    for ti, th in enumerate(thoughts):
        for tok in re.sub(TAG, "", th).split():
            words.append(tok); owner.append(ti)
    st = [None] * len(words)
    for blk in difflib.SequenceMatcher(None, [nz(x) for x in words], [nz(w["raw"]) for w in W], autojunk=False).get_matching_blocks():
        for j in range(blk.size):
            st[blk.a + j] = W[blk.b + j]["s"]
    for i in range(len(st)):
        if st[i] is None:
            st[i] = next((st[j] for j in range(i - 1, -1, -1) if st[j] is not None), 0.0) + 0.15
    t0 = [min(st[i] for i in range(len(st)) if owner[i] == k) for k in range(len(thoughts))]
    bf = n.get("brand_from", len(thoughts))
    brandT = t0[bf] if bf < len(thoughts) else W[-1]["e"] + 0.2
    out = []
    for k in range(min(bf, len(thoughts))):
        if scenes[k] is None:
            if out:
                out[-1]["t1"] = t0[k + 1] if k + 1 < bf else brandT
                out[-1]["_ks"].append(k)
            continue
        out.append({**scenes[k], "t0": 0.0 if k == 0 else round(t0[k] - 0.05, 3), "t1": round(t0[k + 1] - 0.05 if k + 1 < bf else brandT, 3), "_ks": [k]})
    for sc in out:   # params.cue: one spoken word per animation beat -> params.at (seconds after the scene starts)
        P = dict(sc.get("params") or {}); ks = sc.pop("_ks")
        if "cue" not in P:
            continue
        toks = [i for i in range(len(words)) if owner[i] in ks]; at, ptr = [], 0
        for c in P["cue"]:
            hit = None
            if c:
                for j in list(range(ptr, len(toks))) + list(range(0, ptr)):
                    if nz(words[toks[j]]) == nz(c):
                        hit = j; break
                if hit is None:
                    print(f"  cue not found in {sc['type']}: {c!r}")
            if hit is not None:
                v = st[toks[hit]] - sc["t0"]; ptr = hit + 1
            else:
                v = at[-1] + 0.6 if at else 0.2
            at.append(round(max(0.0, v), 3))
        P["at"] = at; sc["params"] = P
    total = round(W[-1]["e"] + n.get("tail", 1.2), 2)
    cfg = {"total": total, "brandT": round(brandT, 3), "scenes": out, "tagline": n.get("tagline", "Turn your dream into\na plan you can see."),
           "handle": n.get("handle", "@becauseidmyor")}
    json.dump(cfg, open(os.path.join(d, "config.json"), "w"), indent=1)
    html = open(os.path.join(SKILL, "assets/illustrated.html")).read().replace("/*__CONFIG__*/{}", json.dumps(cfg))
    html = html.replace("url(fonts/", "url(" + os.path.relpath(os.path.join(SKILL, "assets/fonts"), d) + "/")
    open(os.path.join(d, "reel.html"), "w").write(html)
    run("ffmpeg", "-loglevel", "error", "-y", "-i", os.path.join(d, "audio.mp3"), "-af", "apad,atrim=0:%s,loudnorm=I=-14:TP=-1.5" % total,
        "-ar", "44100", "-b:a", "192k", os.path.join(d, "audio_voice.mp3"))
    run(os.path.join(ROOT, "tts/.venv/bin/python"), os.path.join(SKILL, "scripts/sfx.py"), d, "--level", n.get("sfx", "present"))
    print(f"built {d}: {total}s, {len(out)} scenes, brand {brandT:.2f}s, {cues['wps']} words/sec")
    print("scenes:", [(s["type"], s["t0"], s["t1"], (s.get("params") or {}).get("at")) for s in out])
    if o.record or o.package:
        mp4 = os.path.join(d, "reel.mp4")
        with open(os.path.join(d, "record.log"), "w") as log:
            subprocess.run(["node", "record.js", "--page", os.path.join(d, "reel.html"), "--out", mp4, "--audio", os.path.join(d, "audio_mixed.mp3")], check=True, stdout=log, stderr=log)
        dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", mp4], capture_output=True, text=True).stdout)
        if abs(dur - total) > 0.2:
            sys.exit(f"recorded {dur:.2f}s but reel is {total}s")
        print(f"recorded {mp4} ({dur:.2f}s)")
    if o.package:
        pd = os.path.join(ROOT, "ready-to-post", f"{o.package}-{slug}"); os.makedirs(pd, exist_ok=True)
        shutil.copy(os.path.join(d, "reel.mp4"), os.path.join(pd, "video.mp4")); cap = n.get("caption", {})
        open(os.path.join(pd, "post.md"), "w").write(f"# {slug} (animated illustration explainer, {total}s)\n\n## Caption\n{cap.get('instagram','')}\n\n## Hashtags\n{cap.get('hashtags','')}\n\n"
            f"## X\n{cap.get('x','')}\n\n## YouTube\nTitle: {cap.get('youtube_title','')}\n\n## Status\nNot approved yet.\n")
        print("packaged", pd)


if __name__ == "__main__":
    main()
