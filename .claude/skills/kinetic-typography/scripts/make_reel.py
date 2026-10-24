"""Build a kinetic-typography reel: words are the animation, synced to narration (or silent).

    python3 .claude/skills/kinetic-typography/scripts/make_reel.py reels/<slug> [--record] [--package YYYY-MM-DD]

Input reels/<slug>/narration.json (see examples/). Script markup:
    ||        new card (and a breath in the voice)
    *word*    emphasis: accent colour + punch            ~word~  struck through just after it is said
    {word}    muted grey (asides)
Write "Dmyor"; it is spoken "Deem-yor". The card containing `brand_anchor` (default "That's Dmyor") and
everything after it is replaced by the brand card. Set "voice": null for a silent reel (reading-pace timing).
Run from the project root (folder with record.js).
"""
import argparse, difflib, json, os, re, shutil, subprocess, sys

SKILL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROOT = os.getcwd()
if not os.path.exists(os.path.join(ROOT, "record.js")):
    sys.exit("run from the project root (folder containing record.js)")
NUM = {"0": "zero", "1": "one", "2": "two", "3": "three", "4": "four", "5": "five", "10": "ten", "20": "twenty",
       "100": "one hundred", "500": "five hundred"}


def run(*cmd):
    subprocess.run(list(cmd), check=True)


def parse(script):
    """-> cards: [[{text, e, s, m}], ...] in script order (markup removed)."""
    cards = []
    for th in [x.strip() for x in script.split("||") if x.strip()]:
        words = []
        for tok in th.split():
            w = {"text": tok, "e": False, "s": False, "m": False}
            for mark, key in (("*", "e"), ("~", "s")):
                if tok.startswith(mark) and tok.rstrip(".,!?;:'\"").endswith(mark) and len(tok) > 2:
                    core = tok.rstrip(".,!?;:'\""); tail = tok[len(core):]
                    w["text"] = core[1:-1] + tail; w[key] = True
            if tok.startswith("{") and "}" in tok:
                core = tok.replace("{", "").replace("}", ""); w["text"] = core; w["m"] = True
            words.append(w)
        cards.append(words)
    return cards


def plain(cards):
    return " || ".join(" ".join(w["text"] for w in c) for c in cards)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("reel"); ap.add_argument("--record", action="store_true"); ap.add_argument("--package")
    o = ap.parse_args()
    d = o.reel.rstrip("/"); slug = os.path.basename(d)
    n = json.load(open(os.path.join(d, "narration.json")))
    cards = parse(n["script"])                       # what is SHOWN (short, punchy, with markup)
    flat = [w for c in cards for w in c]
    brand_anchor = n.get("brand_anchor", "That's Dmyor")
    voice = n.get("voice", "am_eric")
    TAG = r"\[(?:hook|body|turn|land|outro)\]\s*"
    # what is SAID: "spoken" (fuller, conversational, one thought per card, optional [stage] tags); default = shown text
    spoken_src = n.get("spoken") or plain(cards)
    thoughts = [t.strip() for t in spoken_src.split("||") if t.strip()]
    if len(thoughts) != len(cards):
        sys.exit(f"'spoken' has {len(thoughts)} thoughts but 'script' has {len(cards)} cards: they must pair up 1:1")
    nz = lambda s: NUM.get(re.sub(r"[^a-z0-9]", "", s.lower()), re.sub(r"[^a-z0-9]", "", s.lower()))

    if voice:
        say_text = re.sub(r"[*~{}]", "", re.sub(r"\bDmyor\b", "Deem-yor", " || ".join(thoughts)))
        run(os.path.join(ROOT, "tts/.venv/bin/python"), os.path.join(SKILL, "scripts/say.py"), say_text,
            os.path.join(d, "audio.mp3"), "--voice", voice, "--speed", str(n.get("speed", 1.0)),
            "--gap-min", str(n.get("gap_min", 0.30)), "--gap-max", str(n.get("gap_max", 0.55)),
            *(["--stages"] if n.get("stages", True) else []))
        run("python3", os.path.join(ROOT, ".claude/skills/dmyor-reel/scripts/align.py"), d)
        cues = json.load(open(os.path.join(d, "cues.json")))
        W = cues["words"]
        sp_words, sp_thought = [], []
        for ti, th in enumerate(thoughts):
            for tok in re.sub(r"[*~{}]", "", re.sub(TAG, "", th)).split():
                sp_words.append(tok); sp_thought.append(ti)
        st = [None] * len(sp_words)
        for blk in difflib.SequenceMatcher(None, [nz(x) for x in sp_words], [nz(w["raw"]) for w in W], autojunk=False).get_matching_blocks():
            for j in range(blk.size):
                st[blk.a + j] = W[blk.b + j]["s"]
        for i in range(len(st)):
            if st[i] is None:
                st[i] = next((st[j] for j in range(i - 1, -1, -1) if st[j] is not None), 0.0) + 0.15
        th_t0 = [min(st[i] for i in range(len(st)) if sp_thought[i] == ti) for ti in range(len(thoughts))]
        th_t1 = th_t0[1:] + [W[-1]["e"]]
        # each shown word takes the time of the same word inside its own spoken thought
        for ci, c in enumerate(cards):
            idx = [i for i in range(len(sp_words)) if sp_thought[i] == ci]
            m = difflib.SequenceMatcher(None, [nz(w["text"]) for w in c], [nz(sp_words[i]) for i in idx], autojunk=False)
            got = [None] * len(c)
            for blk in m.get_matching_blocks():
                for j in range(blk.size):
                    got[blk.a + j] = st[idx[blk.b + j]]
            for wi in range(len(c)):
                if got[wi] is None:  # not spoken verbatim: spread through the thought
                    prev = next((got[j] for j in range(wi - 1, -1, -1) if got[j] is not None), th_t0[ci])
                    got[wi] = min(prev + 0.25, th_t1[ci] - 0.2)
                c[wi]["t"] = round(got[wi], 3)
        end = W[-1]["e"]
        heard = cues["text"]; wps = cues["wps"]
    else:  # silent: reading pace 0.32 s/word, 0.7 s between cards, hook held 1.6 s
        t = 0.0; th_t0 = []
        for ci, c in enumerate(cards):
            th_t0.append(t if ci else 0.0)
            for w in c:
                w["t"] = round(t if ci else 0.0, 3); t += 0.32 if ci else 0.0
            t += 1.6 if ci == 0 else 0.7
        end = t; heard = "(silent)"; wps = None
    # brand: first card containing the anchor text
    bi = next((i for i, c in enumerate(cards) if brand_anchor.lower().replace("'", "") in " ".join(w["text"] for w in c).lower().replace("'", "")), len(cards))
    brandT = th_t0[bi] if bi < len(cards) else end + 0.2
    shown = cards[:bi]
    out = []
    for i, c in enumerate(shown):
        t0 = 0.0 if i == 0 else th_t0[i] - 0.05
        t1 = th_t0[i + 1] - 0.05 if i + 1 < len(shown) else brandT
        out.append({"t0": round(t0, 3), "t1": round(t1, 3), "words": c, "max": n.get("max_font", 150)})
    total = round(end + n.get("tail", 1.2), 2)
    cfg = {"total": total, "cards": out, "brandT": round(brandT, 3), "tagline": n.get("tagline", "Turn your dream into\na plan you can see."),
           "handle": n.get("handle", "@becauseidmyor"), "voice": voice, "script": n["script"], "spoken": spoken_src}
    json.dump(cfg, open(os.path.join(d, "config.json"), "w"), indent=1)
    html = open(os.path.join(SKILL, "assets/kinetic.html")).read().replace("/*__CONFIG__*/{}", json.dumps(cfg))
    html = html.replace("url(fonts/", "url(" + os.path.relpath(os.path.join(SKILL, "assets/fonts"), d) + "/")
    open(os.path.join(d, "reel.html"), "w").write(html)
    if voice:
        run("ffmpeg", "-loglevel", "error", "-y", "-i", os.path.join(d, "audio.mp3"), "-af",
            "apad,atrim=0:%s,loudnorm=I=-14:TP=-1.5" % total, "-ar", "44100", "-b:a", "192k", os.path.join(d, "audio_mixed.mp3"))
    print(f"built {d}: {total}s, {len(out)} cards, brand at {brandT:.2f}s" + (f", {wps} words/sec" if wps else " (silent)"))
    print("whisper heard:", heard)

    if o.record or o.package:
        out_mp4 = os.path.join(d, "reel.mp4")
        cmd = ["node", "record.js", "--page", os.path.join(d, "reel.html"), "--out", out_mp4]
        if voice:
            cmd += ["--audio", os.path.join(d, "audio_mixed.mp3")]
        with open(os.path.join(d, "record.log"), "w") as log:
            subprocess.run(cmd, check=True, stdout=log, stderr=log)
        dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", out_mp4],
                                   capture_output=True, text=True).stdout)
        if abs(dur - total) > 0.2:
            sys.exit(f"recorded {dur:.2f}s but reel is {total}s: check record.log")
        print(f"recorded {out_mp4} ({dur:.2f}s)")
    if o.package:
        pd = os.path.join(ROOT, "ready-to-post", f"{o.package}-{slug}"); os.makedirs(pd, exist_ok=True)
        shutil.copy(os.path.join(d, "reel.mp4"), os.path.join(pd, "video.mp4"))
        cap = n.get("caption", {})
        open(os.path.join(pd, "post.md"), "w").write(
            f"# {slug} (kinetic typography, voice {voice or 'none'}, {total}s)\n\n## Caption\n{cap.get('instagram','')}\n\n"
            f"## Hashtags\n{cap.get('hashtags','')}\n\n## X\n{cap.get('x','')}\n\n## YouTube\nTitle: {cap.get('youtube_title','')}\n\n"
            f"## Experiment\n{n.get('experiment','')}\n\n## Status\nNot approved yet: Sanyam watches first.\n")
        print("packaged", pd)


if __name__ == "__main__":
    main()
