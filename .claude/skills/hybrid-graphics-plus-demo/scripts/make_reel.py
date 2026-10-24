"""Hybrid reel: kinetic hook -> REAL dmyor screens in a phone (recorded footage) -> motion-graphics panel
(e.g. Phase 2 features) -> kinetic CTA -> brand. All beats land on spoken words.

    python3 .claude/skills/hybrid-graphics-plus-demo/scripts/make_reel.py reels/<slug> [--record] [--package YYYY-MM-DD]

Footage must exist first (app-capture/raw/<clip>_frames/, made by scripts/capture.js).
narration.json (see examples/narration.example.json):
  script            narration; "||" = thought/breath. Mark *emphasis* (shown on kinetic cards).
  hook_until        anchor where the hook card ends and the phone comes in
  clips             [{name, beats:[[anchor, footage_seconds], ...]}] footage time pinned to spoken anchors;
                    each clip runs from its first beat to the next clip's first beat (or phone_out)
  phone_out         anchor where the phone leaves
  taps              [{anchor, x, y}]  tap ring on the screen (x,y = 0-1 of the screen)
  callouts          [{anchor, until, text, side: left|right, y: 0-1}]
  zooms             [{anchor, s, x, y}] zoom into the screen (s=1 none)
  phase2            {from, unlock, until, items:[{k, t}]}  feature panel shown with motion graphics
  cta               {from, text}  kinetic CTA card (text with *emphasis*) until the brand
  brand_anchor      anchor where the brand card starts ("That's")
Run from the project root.
"""
import argparse, difflib, json, os, re, shutil, subprocess, sys

SKILL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROOT = os.getcwd()
if not os.path.exists(os.path.join(ROOT, "record.js")):
    sys.exit("run from the project root (folder containing record.js)")
sys.path.insert(0, os.path.join(ROOT, ".claude/skills/dmyor-reel/scripts"))
from align import find  # noqa: E402
NUM = {"1": "one", "2": "two", "3": "three", "5": "five", "10": "ten", "100": "one hundred", "2000": "two thousand"}
STAGE_TAG = r"\[(?:hook|body|turn|land|outro)\]\s*"  # delivery tags for say.py --stages, never shown or matched
BRAND_HEARD = r"\bD(?:ee|e|i)?-?\s?m(?:y|i)(?:o|e)?re?\b|\bDeem[- ]?yo(?:u)?re?\b|\bD-?[Mm]ure\b|\bdemure\b"


def run(*cmd):
    subprocess.run(list(cmd), check=True)


def marks(text):
    words = []
    for tok in text.split():
        e = tok.startswith("*") and tok.rstrip(".,!?;:").endswith("*") and len(tok) > 2
        core = tok.rstrip(".,!?;:"); tail = tok[len(core):]
        words.append({"text": (core[1:-1] if e else core) + tail, "e": e})
    return words


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("reel"); ap.add_argument("--record", action="store_true"); ap.add_argument("--package")
    o = ap.parse_args(); d = o.reel.rstrip("/"); slug = os.path.basename(d)
    n = json.load(open(os.path.join(d, "narration.json")))
    clean = re.sub(r"\*([^*]+)\*", r"\1", n["script"])
    spoken = re.sub(r"\bDmyor\b", "Deem-yor", clean)
    clean = re.sub(STAGE_TAG, "", clean)
    run(os.path.join(ROOT, "tts/.venv/bin/python"), os.path.join(SKILL, "scripts/say.py"), spoken, os.path.join(d, "audio.mp3"),
        "--voice", n.get("voice", "am_eric"), "--speed", str(n.get("speed", 1.0)),
        "--gap-min", str(n.get("gap_min", 0.18)), "--gap-max", str(n.get("gap_max", 0.32)),
        *(["--stages"] if n.get("stages", True) else []))
    run("python3", os.path.join(ROOT, ".claude/skills/dmyor-reel/scripts/align.py"), d)
    cues = json.load(open(os.path.join(d, "cues.json"))); W = cues["words"]

    def at(phrase, after=0.0):
        h = find(cues, phrase, after)
        if not h:
            alt = " ".join(NUM.get(x, x) for x in phrase.split())
            h = find(cues, alt, after)
        if not h:
            sys.exit(f"anchor not found: {phrase!r}\nwhisper heard: {cues['text']}")
        return h[0]

    # word times for the script words (for kinetic cards + subtitles)
    sw = clean.replace("||", " ").split()
    nz = lambda s: (lambda x: NUM.get(x, x))(re.sub(r"[^a-z0-9]", "", s.lower()))
    tm = [None] * len(sw)
    for blk in difflib.SequenceMatcher(None, [nz(w) for w in sw], [nz(w["raw"]) for w in W], autojunk=False).get_matching_blocks():
        for j in range(blk.size):
            tm[blk.a + j] = W[blk.b + j]["s"]
    for i in range(len(tm)):
        if tm[i] is None:
            tm[i] = next((tm[j] for j in range(i - 1, -1, -1) if tm[j] is not None), 0.0) + 0.15

    hook_end = at(n["hook_until"]); brandT = at(n["brand_anchor"], hook_end); phone_out = at(n["phone_out"], hook_end)
    end = W[-1]["e"]; total = round(end + n.get("tail", 1.2), 2)
    # cards: hook (script words before hook_end) and CTA
    hook_words = marks(n["hook_text"]) if n.get("hook_text") else None
    k = 0; first = []
    for i, w in enumerate(sw):
        if tm[i] < hook_end - 0.05:
            first.append(i)
    raw_marked = re.sub(STAGE_TAG, "", n["script"]).replace("||", " ").split()
    if not hook_words:
        hook_words = marks(" ".join(raw_marked[i] for i in first))
    for i, w in enumerate(hook_words):
        w["t"] = tm[first[i]] if i < len(first) else 0
    cards = [{"t0": 0.0, "t1": hook_end - 0.05, "words": hook_words, "max": 140}]
    if n.get("cta"):
        ct = at(n["cta"]["from"], hook_end)
        cw = marks(n["cta"]["text"])
        idx = [i for i in range(len(sw)) if ct - 0.05 <= tm[i] < brandT - 0.05]
        for i, w in enumerate(cw):
            w["t"] = tm[idx[i]] if i < len(idx) else ct
        cards.append({"t0": ct - 0.05, "t1": brandT, "words": cw, "max": 140})
    # phone clips
    rel = lambda p: os.path.relpath(p, d)
    clips, starts = [], []
    for c in n["clips"]:
        fj = json.load(open(os.path.join(ROOT, "app-capture/raw", c["name"] + "_frames", "frames.json")))
        frames = [[round(f["t"], 3), os.path.basename(f["file"])] for f in fj]
        t = hook_end; mp = []
        for anchor, ft in c["beats"]:
            t = at(anchor, t - 0.01) if anchor != "@start" else hook_end
            mp.append([round(t, 3), ft])
        clips.append({"dir": rel(os.path.join(ROOT, "app-capture/raw", c["name"] + "_frames")), "frames": frames, "map": mp,
                      "speed_after": c.get("speed_after", 1.0), "dur": frames[-1][0]})
        starts.append(mp[0][0])
    for i, c in enumerate(clips):
        c["t0"] = c["map"][0][0]; c["t1"] = starts[i + 1] if i + 1 < len(clips) else phone_out + 0.4
        last_t, last_f = c["map"][-1]
        c["map"].append([round(c["t1"], 3), min(c["dur"], last_f + (c["t1"] - last_t) * c["speed_after"])])
    phone = {"in": hook_end - 0.1, "out": phone_out, "y": n.get("phone_y", 1060), "clips": clips,
             "taps": [{"t": at(x["anchor"], hook_end), "x": x["x"], "y": x["y"]} for x in n.get("taps", [])],
             "callouts": [{"t0": at(x["anchor"], hook_end), "t1": at(x["until"], hook_end) if x.get("until") else phone_out,
                           "text": x["text"], "side": x.get("side", "right"), "y": x.get("y", .3)} for x in n.get("callouts", [])],
             "zooms": [{"t": at(x["anchor"], hook_end) if x["anchor"] != "@start" else hook_end, "s": x["s"], "x": x["x"], "y": x["y"]} for x in n.get("zooms", [])]}
    phase2 = None
    if n.get("phase2"):
        p = n["phase2"]
        phase2 = {"t0": at(p["from"], hook_end), "unlockT": at(p["unlock"], hook_end), "t1": at(p["until"], hook_end), "items": p["items"], "title": p.get("title", "")}
    phrases, cur = [], []
    for i, w in enumerate(sw):
        cur.append(i)
        if re.search(r"[.,!?;:]$", w) or i == len(sw) - 1:
            phrases.append(cur); cur = []
    chunks = []
    for ph in phrases:  # max ~7 words on screen; long phrases split near the middle
        while len(ph) > 7:
            cut = len(ph) // 2
            chunks.append(ph[:cut]); ph = ph[cut:]
        chunks.append(ph)
    subs = []
    cta_t0 = cards[1]["t0"] if len(cards) > 1 else brandT
    for ci, ch in enumerate(chunks):
        t0 = tm[ch[0]]; t1 = tm[chunks[ci + 1][0]] if ci + 1 < len(chunks) else tm[ch[-1]] + 0.6
        in_p2 = phase2 and phase2["t0"] - 0.05 <= t0 < phase2["t1"]
        if hook_end - 0.05 <= t0 < cta_t0 - 0.05 and not in_p2:
            txt = re.sub(BRAND_HEARD, "Dmyor", " ".join(sw[j] for j in ch)).rstrip(",;")
            subs.append({"t0": round(t0, 2), "t1": round(min(t1, cta_t0), 2), "text": txt[:1].upper() + txt[1:]})
    cfg = {"total": total, "brandT": round(brandT, 3), "cards": cards, "subs": subs, "phone": phone, "phase2": phase2,
           "tagline": n.get("tagline", "Turn your dream into\na plan you can see."), "handle": n.get("handle", "@becauseidmyor")}
    json.dump(cfg, open(os.path.join(d, "config.json"), "w"))
    html = open(os.path.join(SKILL, "assets/hybrid.html")).read().replace("/*__CONFIG__*/{}", json.dumps(cfg))
    html = html.replace("url(fonts/", "url(" + rel(os.path.join(SKILL, "assets/fonts")) + "/")
    open(os.path.join(d, "reel.html"), "w").write(html)
    run("ffmpeg", "-loglevel", "error", "-y", "-i", os.path.join(d, "audio.mp3"), "-af", "apad,atrim=0:%s,loudnorm=I=-14:TP=-1.5" % total,
        "-ar", "44100", "-b:a", "192k", os.path.join(d, "audio_mixed.mp3"))
    print(f"built {d}: {total}s, {cues['wps']} words/sec, phone {phone['in']:.2f}-{phone['out']:.2f}s, brand {brandT:.2f}s")
    print("whisper heard:", cues["text"])
    if o.record or o.package:
        out = os.path.join(d, "reel.mp4")
        with open(os.path.join(d, "record.log"), "w") as log:
            subprocess.run(["node", "record.js", "--page", os.path.join(d, "reel.html"), "--out", out, "--audio", os.path.join(d, "audio_mixed.mp3")],
                           check=True, stdout=log, stderr=log)
        dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", out], capture_output=True, text=True).stdout)
        if abs(dur - total) > 0.2:
            sys.exit(f"recorded {dur:.2f}s but reel is {total}s")
        print(f"recorded {out} ({dur:.2f}s)")
    if o.package:
        pd = os.path.join(ROOT, "ready-to-post", f"{o.package}-{slug}"); os.makedirs(pd, exist_ok=True)
        shutil.copy(os.path.join(d, "reel.mp4"), os.path.join(pd, "video.mp4")); cap = n.get("caption", {})
        open(os.path.join(pd, "post.md"), "w").write(f"# {slug} (hybrid graphics + real app demo, {total}s)\n\n## Caption\n{cap.get('instagram','')}\n\n"
            f"## Hashtags\n{cap.get('hashtags','')}\n\n## X\n{cap.get('x','')}\n\n## YouTube\nTitle: {cap.get('youtube_title','')}\n\n## Status\nNot approved yet.\n")
        print("packaged", pd)


if __name__ == "__main__":
    main()
