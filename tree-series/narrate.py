"""Narrated tree reel: script -> Kokoro voice -> whisper word timings -> visuals on spoken cues.

    python3 tree-series/narrate.py reels/<slug>

Reads reels/<slug>/narration.json:
  base      tree reel whose config.json supplies the look (palette, layout, cards)
  override  fields to replace in that config (hook, vision, milestones, actions, ...)
  voice, speed, script
  anchors   event -> phrase (or list of phrases) as spoken; searched in order
  tail      seconds kept after the last word (brand card)

Writes audio.mp3 (voice), cues.json, config.json (events in beats, subs in seconds),
reel.html, music.mp3 (bed) and audio_mixed.mp3 (voice + quiet bed) ready for record.js.
"""
import json, os, re, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, ".claude/skills/dmyor-reel/scripts"))
from align import find  # noqa: E402

NUM = {"0": "zero", "1": "one", "2": "two", "3": "three", "4": "four", "5": "five", "10": "ten", "500": "five hundred"}


def run(*cmd):
    subprocess.run(list(cmd), check=True)


def locate(cues, phrase, after):
    hit = find(cues, phrase, after)
    if not hit:  # whisper may write numbers as digits or words; try the other spelling
        alt = " ".join(NUM.get(t, t) for t in phrase.split())
        inv = {v: k for k, v in NUM.items()}
        alt2 = phrase
        for w, d in sorted(inv.items(), key=lambda x: -len(x[0])):
            alt2 = re.sub(r"\b%s\b" % w, d, alt2, flags=re.I)
        hit = find(cues, alt, after) or find(cues, alt2, after)
    if not hit:
        sys.exit(f"anchor not found after {after:.2f}s: {phrase!r}\nspoken: {cues['text']}")
    return hit


def main(d):
    n = json.load(open(os.path.join(d, "narration.json")))
    cfg = json.load(open(os.path.join(ROOT, "reels", n["base"], "config.json")))
    cfg.update(n.get("override", {}))

    # 1. voice
    spoken = re.sub(r"\bDmyor\b", "Deem-yor", n["script"])  # owner: said "DEEM-yor" (2026-10-22)
    run(os.path.join(ROOT, "tts/.venv/bin/python"), os.path.join(ROOT, "tts/say.py"), spoken,
        os.path.join(d, "audio.mp3"), "--voice", n["voice"], "--speed", str(n.get("speed", 0.9)),
        "--gap-min", str(n.get("gap_min", 0.30)), "--gap-max", str(n.get("gap_max", 0.55)))
    # 2. word timings
    run("python3", os.path.join(ROOT, ".claude/skills/dmyor-reel/scripts/align.py"), d)
    cues = json.load(open(os.path.join(d, "cues.json")))

    # 3. events on spoken cues (seconds), then into beats for the template
    B = 60 / cfg["bpm"]
    t = 0.0
    ev_s = {}
    for k in ["hookOut", "vision", "trunk", "milestones", "actions", "focus", "done", "grow", "brand"]:
        a = n["anchors"][k]
        if isinstance(a, list):
            ev_s[k] = []
            for ph in a:
                s, e = locate(cues, ph, t)
                ev_s[k].append(s); t = s + 0.05
        else:
            s, e = locate(cues, a, t)
            ev_s[k] = s; t = s + 0.05
    ev_s["titleM"], ev_s["titleA"] = ev_s["milestones"][0], ev_s["actions"][0]
    cfg["events"] = {k: ([round(x / B, 3) for x in v] if isinstance(v, list) else round(v / B, 3)) for k, v in ev_s.items()}
    last = cues["words"][-1]["e"]
    cfg["total"] = round(last + n.get("tail", 1.8), 2)

    # 4. subtitles: the SCRIPT's own words and punctuation, timed by matching them to whisper's words
    import difflib
    def nz(w):
        w = re.sub(r"[^a-z0-9]", "", w.lower())
        return NUM.get(w, w)
    W = cues["words"]
    sw = [w for w in n["script"].replace("||", " ").split() if w.strip()]
    a_, b_ = [nz(w) for w in sw], [nz(w["raw"]) for w in W]
    tm = [None] * len(sw)
    for blk in difflib.SequenceMatcher(None, a_, b_, autojunk=False).get_matching_blocks():
        for j in range(blk.size):
            tm[blk.a + j] = (W[blk.b + j]["s"], W[blk.b + j]["e"])
    for i in range(len(sw)):  # unmatched words take the nearest known timing
        if tm[i] is None:
            prev = next((tm[j] for j in range(i - 1, -1, -1) if tm[j]), (0.0, 0.0))
            tm[i] = (prev[1], prev[1] + 0.2)
    phrases, cur = [], []
    for i, w in enumerate(sw):
        cur.append(i)
        if re.search(r"[.,!?;:]$", w) or i == len(sw) - 1:
            phrases.append(cur); cur = []
    chunks = []
    for ph in phrases:
        while len(ph) > 7:
            cut = len(ph) // 2
            chunks.append(ph[:cut]); ph = ph[cut:]
        chunks.append(ph)
    subs = []
    for ci, ch in enumerate(chunks):
        t0 = tm[ch[0]][0]
        t1 = tm[chunks[ci + 1][0]][0] if ci + 1 < len(chunks) else tm[ch[-1]][1] + 0.4
        if ev_s["hookOut"] - 0.05 <= t0 < ev_s["brand"] - 0.05:
            txt = " ".join(sw[j] for j in ch).strip().rstrip(",;")
            subs.append({"t0": round(t0, 2), "t1": round(min(t1, ev_s["brand"]), 2), "text": txt[:1].upper() + txt[1:]})
    cfg["subs"] = subs
    cfg["narration"] = {"voice": n["voice"], "provider": "kokoro-onnx v1.0", "script": n["script"]}
    json.dump(cfg, open(os.path.join(d, "config.json"), "w"), indent=1)

    # 5. visuals, then the voice track (optional music bed)
    run("python3", os.path.join(HERE, "build.py"), d)
    if n.get("music"):  # off by default (owner, 2026-10-22: no background music under narration)
        run("python3", os.path.join(HERE, "music.py"), d, "music.mp3")
        mix = "[0:a]apad,atrim=0:%s[v];[1:a]volume=0.16[m];[v][m]amix=inputs=2:normalize=0,loudnorm=I=-14:TP=-1.5[o]" % cfg["total"]
        ins = ["-i", os.path.join(d, "audio.mp3"), "-i", os.path.join(d, "music.mp3")]
    else:
        mix = "[0:a]apad,atrim=0:%s,loudnorm=I=-14:TP=-1.5[o]" % cfg["total"]
        ins = ["-i", os.path.join(d, "audio.mp3")]
    run("ffmpeg", "-loglevel", "error", "-y", *ins, "-filter_complex", mix,
        "-map", "[o]", "-ar", "44100", "-b:a", "192k", os.path.join(d, "audio_mixed.mp3"))
    print(f"ready: {d}  total {cfg['total']}s, {len(subs)} subtitle phrases, events(s) {json.dumps({k: v for k, v in ev_s.items()})}")


if __name__ == "__main__":
    main(sys.argv[1])
