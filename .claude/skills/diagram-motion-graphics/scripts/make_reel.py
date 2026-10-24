"""Build a narrated goal-tree diagram reel end to end.

    python3 .claude/skills/diagram-motion-graphics/scripts/make_reel.py reels/<slug> [--record] [--package YYYY-MM-DD]

Input: reels/<slug>/narration.json (see examples/narration.example.json).
Steps:
  1. voice      scripts/say.py (Kokoro, local, free) -> audio.mp3; thoughts split by "||", varied pauses, room tone
  2. timings    dmyor-reel align.py (whisper word timestamps) -> cues.json
  3. events     every visual beat placed on its spoken anchor phrase (seconds -> template beats)
  4. subtitles  the script's own words + punctuation, timed by matching to whisper's words
  5. html       assets/diagram.html + config -> reel.html (fonts referenced from assets/fonts)
  6. audio      voice only (no music), padded to the reel length -> audio_mixed.mp3
  7. --record   node record.js -> reel.mp4 (1080x1920, 30 fps) and checks duration
  8. --package  copies to ready-to-post/<date>-<slug>/video.mp4 and writes post.md from the narration's caption
Run from the project root (the folder with record.js).
"""
import argparse, difflib, json, os, re, shutil, subprocess, sys

SKILL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROOT = os.getcwd()
if not os.path.exists(os.path.join(ROOT, "record.js")):
    sys.exit("run from the project root (folder containing record.js)")
sys.path.insert(0, os.path.join(ROOT, ".claude/skills/dmyor-reel/scripts"))
from align import find  # noqa: E402  (whisper-based phrase finder from the dmyor-reel skill)

BPM = 100
STAGE_TAG = r"\[(?:hook|body|turn|land|outro)\]\s*"  # delivery tags for say.py --stages, never shown or matched
  # the template counts time in beats; 100 bpm -> 0.6 s per beat
NUM = {"0": "zero", "1": "one", "2": "two", "3": "three", "4": "four", "5": "five",
       "10": "ten", "100": "one hundred", "500": "five hundred"}
BRAND_SPOKEN = "Deem-yor"  # owner: "Dmyor" is pronounced DEEM-yor (2026-10-22)
# whisper's spellings of the spoken brand, mapped back to "Dmyor" in subtitles
BRAND_HEARD = r"\bD(?:ee|e|i)?-?\s?m(?:y|i)(?:o|e)?re?\b|\bDeem[- ]?yo(?:u)?re?\b|\bD-?[Mm]ure\b|\bdemure\b"

DEFAULT_CONTENT = {
    "handle": "@becauseidmyor",
    "tagline": "Turn your dream into\na plan you can see.",
    "actionParent": 1,   # which milestone (0-2) the actions hang from; keep 1 (centre) for symmetry
    "todayIdx": 0,       # which action (0-2) gets the TODAY focus and the check
}


def run(*cmd):
    subprocess.run(list(cmd), check=True)


def locate(cues, phrase, after):
    hit = find(cues, phrase, after)
    if not hit:  # whisper may write numbers as digits or words; try both spellings
        alt = " ".join(NUM.get(t, t) for t in phrase.split())
        alt2 = phrase
        for d, w in sorted(NUM.items(), key=lambda x: -len(x[1])):
            alt2 = re.sub(r"\b%s\b" % w, d, alt2, flags=re.I)
        hit = find(cues, alt, after) or find(cues, alt2, after)
    if not hit:
        sys.exit(f"anchor not found after {after:.2f}s: {phrase!r}\nwhisper heard: {cues['text']}\n"
                 "fix: choose an anchor made of words whisper transcribed exactly (avoid homophones like write/right)")
    return hit


def subtitles(script, words, start, stop):
    nz = lambda w: NUM.get(re.sub(r"[^a-z0-9]", "", w.lower()), re.sub(r"[^a-z0-9]", "", w.lower()))
    sw = [w for w in script.replace("||", " ").split() if w.strip()]
    a, b = [nz(w) for w in sw], [nz(w["raw"]) for w in words]
    tm = [None] * len(sw)
    for blk in difflib.SequenceMatcher(None, a, b, autojunk=False).get_matching_blocks():
        for j in range(blk.size):
            tm[blk.a + j] = (words[blk.b + j]["s"], words[blk.b + j]["e"])
    for i in range(len(sw)):
        if tm[i] is None:
            prev = next((tm[j] for j in range(i - 1, -1, -1) if tm[j]), (0.0, 0.0))
            tm[i] = (prev[1], prev[1] + 0.2)
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
    for ci, ch in enumerate(chunks):
        t0 = tm[ch[0]][0]
        t1 = tm[chunks[ci + 1][0]][0] if ci + 1 < len(chunks) else tm[ch[-1]][1] + 0.4
        if start - 0.05 <= t0 < stop - 0.05:
            txt = re.sub(BRAND_HEARD, "Dmyor", " ".join(sw[j] for j in ch), flags=re.I).strip().rstrip(",;")
            subs.append({"t0": round(t0, 2), "t1": round(min(t1, stop), 2), "text": txt[:1].upper() + txt[1:]})
    return subs


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("reel"); ap.add_argument("--record", action="store_true"); ap.add_argument("--package")
    o = ap.parse_args()
    d = o.reel.rstrip("/"); slug = os.path.basename(d)
    n = json.load(open(os.path.join(d, "narration.json")))
    cfg = dict(DEFAULT_CONTENT); cfg.update(n["content"]); cfg["bpm"] = BPM

    # 1. voice
    spoken = re.sub(r"\bDmyor\b", BRAND_SPOKEN, n["script"])
    run(os.path.join(ROOT, "tts/.venv/bin/python"), os.path.join(SKILL, "scripts/say.py"), spoken,
        os.path.join(d, "audio.mp3"), "--voice", n.get("voice", "am_eric"), "--speed", str(n.get("speed", 1.0)),
        "--gap-min", str(n.get("gap_min", 0.30)), "--gap-max", str(n.get("gap_max", 0.55)),
        *(["--stages"] if n.get("stages", True) else []))
    # 2. timings
    run("python3", os.path.join(ROOT, ".claude/skills/dmyor-reel/scripts/align.py"), d)
    cues = json.load(open(os.path.join(d, "cues.json")))
    # 3. events on spoken anchors, searched in order
    B = 60 / BPM; t = 0.0; ev = {}
    for k in ["hookOut", "vision", "trunk", "milestones", "actions", "focus", "done", "grow", "brand"]:
        a = n["anchors"][k]
        if isinstance(a, list):
            ev[k] = []
            for ph in a:
                s, _ = locate(cues, ph, t); ev[k].append(s); t = s + 0.05
        else:
            s, _ = locate(cues, a, t); ev[k] = s; t = s + 0.05
    cfg["events"] = {k: ([round(x / B, 3) for x in v] if isinstance(v, list) else round(v / B, 3)) for k, v in ev.items()}
    cfg["total"] = round(cues["words"][-1]["e"] + n.get("tail", 1.2), 2)
    # 4. subtitles
    cfg["subs"] = subtitles(re.sub(STAGE_TAG, "", n["script"]), cues["words"], ev["hookOut"], ev["brand"])
    cfg["narration"] = {"voice": n.get("voice", "am_eric"), "provider": "kokoro-onnx v1.0", "script": n["script"]}
    json.dump(cfg, open(os.path.join(d, "config.json"), "w"), indent=1)
    # 5. html
    html = open(os.path.join(SKILL, "assets/diagram.html")).read().replace("/*__CONFIG__*/{}", json.dumps(cfg))
    html = html.replace("url(fonts/", "url(" + os.path.relpath(os.path.join(SKILL, "assets/fonts"), d) + "/")
    open(os.path.join(d, "reel.html"), "w").write(html)
    # 6. audio: voice only
    run("ffmpeg", "-loglevel", "error", "-y", "-i", os.path.join(d, "audio.mp3"),
        "-af", "apad,atrim=0:%s,loudnorm=I=-14:TP=-1.5" % cfg["total"], "-ar", "44100", "-b:a", "192k",
        os.path.join(d, "audio_mixed.mp3"))
    print(f"built {d}: {cfg['total']}s, {cues['wps']} words/sec, {len(cfg['subs'])} subtitles")
    print("events (s):", json.dumps({k: (round(v, 2) if not isinstance(v, list) else [round(x, 2) for x in v]) for k, v in ev.items()}))
    print("whisper heard:", cues["text"])
    # 7. record
    if o.record or o.package:
        out = os.path.join(d, "reel.mp4")
        with open(os.path.join(d, "record.log"), "w") as log:
            subprocess.run(["node", "record.js", "--page", os.path.join(d, "reel.html"), "--out", out,
                            "--audio", os.path.join(d, "audio_mixed.mp3")], check=True, stdout=log, stderr=log)
        dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", out],
                                   capture_output=True, text=True).stdout)
        if abs(dur - cfg["total"]) > 0.2:
            sys.exit(f"recorded {dur:.2f}s but reel is {cfg['total']}s: check record.log")
        print(f"recorded {out} ({dur:.2f}s)")
    # 8. package
    if o.package:
        pd = os.path.join(ROOT, "ready-to-post", f"{o.package}-{slug}"); os.makedirs(pd, exist_ok=True)
        shutil.copy(os.path.join(d, "reel.mp4"), os.path.join(pd, "video.mp4"))
        cap = n.get("caption", {})
        open(os.path.join(pd, "post.md"), "w").write(
            f"# {slug} (narrated goal-tree diagram reel, voice {n.get('voice', 'am_eric')}, {cfg['total']}s)\n\n"
            f"## Caption\n{cap.get('instagram', '')}\n\n## Hashtags\n{cap.get('hashtags', '')}\n\n"
            f"## X\n{cap.get('x', '')}\n\n## YouTube\nTitle: {cap.get('youtube_title', '')}\n\n"
            f"## Experiment\n{n.get('experiment', '')}\n\n## Status\nNot approved yet: Sanyam watches first.\n")
        print("packaged", pd)


if __name__ == "__main__":
    main()
