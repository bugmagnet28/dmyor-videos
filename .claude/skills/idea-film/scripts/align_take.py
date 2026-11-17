"""Fit a recorded narration take (owner's ElevenLabs file, or any mp3) to the script.
    python3 .claude/skills/idea-film/scripts/align_take.py reels/<slug> <take.mp3>
Needs reels/<slug>/lines.json ({"H": [["line", pause], ...], ...}, same words as the take).
Runs local whisper (word timestamps), matches every scripted line to its words and writes:
  timeline.json / timeline.js (var TL = {total, scenes, lines:[[key,i,start,end,text]], subs})  and  audio.wav (the take, 44.1 kHz mono).
If a line's last word does not match, it stops and prints the mismatch: fix lines.json to the words actually spoken."""
import json, os, re, subprocess, sys
D, TAKE = sys.argv[1], sys.argv[2]
os.makedirs(os.path.join(D, "asr"), exist_ok=True)
subprocess.run(["whisper", TAKE, "--model", "small.en", "--language", "en", "--word_timestamps", "True", "--output_format", "json", "--output_dir", os.path.join(D, "asr")], check=True, capture_output=True)
asr = json.load(open(os.path.join(D, "asr", os.path.splitext(os.path.basename(TAKE))[0] + ".json")))
norm = lambda s: re.sub(r"[^a-z0-9']", "", s.lower())
W = [(norm(w["word"]), w["start"], w["end"]) for s in asr["segments"] for w in s["words"] if norm(w["word"])]
lines = json.load(open(os.path.join(D, "lines.json"))); i = 0; out = []
for k, ls in lines.items():
    for j, (text, _) in enumerate(ls):
        toks = [norm(x) for x in text.split() if norm(x)]; a = W[i][1]; i += len(toks); b = W[i - 1][2]
        if W[i - 1][0] != toks[-1]: sys.exit(f"mismatch at {k}{j}: heard '{W[i - 1][0]}', script '{toks[-1]}'")
        out.append([k, j, round(a, 3), round(b, 3), text])
TOT = round(out[-1][3] + 1.4, 3); subs = []
for k, j, a, b, text in out:
    chunks, c = [], ""
    for w in text.split():
        if len(c) + len(w) + 1 > 30 and c: chunks.append(c); c = w
        else: c = (c + " " + w).strip()
    chunks.append(c); n = sum(len(x) for x in chunks); t = a
    for x in chunks: d = (b - a) * len(x) / n; subs.append([round(t, 3), round(t + d + .12, 3), re.sub(r"[^A-Z0-9 .,'?!:#@/-]", "", x.upper())]); t += d
scenes = {}
for k, j, a, b, _ in out: scenes.setdefault(k, [a, b]); scenes[k][1] = b
json.dump({"total": TOT, "scenes": scenes, "lines": out}, open(os.path.join(D, "timeline.json"), "w"), indent=1)
open(os.path.join(D, "timeline.js"), "w").write("var TL = " + json.dumps({"total": TOT, "scenes": scenes, "lines": out, "subs": subs}) + ";\n")
subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", TAKE, "-af", "apad=pad_dur=2", "-t", str(TOT), "-ar", "44100", "-ac", "1", os.path.join(D, "audio.wav")], check=True)
for l in out: print(l[:4])
print("total", TOT)
