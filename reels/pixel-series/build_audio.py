"""pixel-series narration (usage: tts/.venv/bin/python reels/pixel-series/build_audio.py reels/<episode>): one Kokoro clip per line (am_eric, human preset), set pauses after each.
Film time = narration time. Writes audio.mp3, timeline.js (scene spans, line spans, subtitles).
    tts/.venv/bin/python reels/pixel-destiny/build_audio.py   (from the project root)"""
import json, os, re, subprocess, numpy as np, soundfile as sf
import sys
ROOT = os.getcwd(); D = os.path.join(ROOT, sys.argv[1]); SR = 44100; TEMPO = 1.06; LEAD = .5; TAIL = 2.2
os.makedirs(os.path.join(D, "vo"), exist_ok=True)
LINES = json.load(open(os.path.join(D, "lines.json")))
def clip(k, i, text):
    raw, out = os.path.join(D, f"vo/{k}_{i}.mp3"), os.path.join(D, f"vo/{k}_{i}.wav")
    if not os.path.exists(raw):
        subprocess.run([os.path.join(ROOT, "tts/.venv/bin/python"), os.path.join(ROOT, "tts/say.py"), text, raw, "--preset", "human"], check=True, cwd=ROOT)
    if not os.path.exists(out):
        subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", raw, "-af", f"silenceremove=start_periods=1:start_threshold=-45dB,areverse,silenceremove=start_periods=1:start_threshold=-45dB,areverse,atempo={TEMPO}", "-ar", str(SR), "-ac", "1", out], check=True)
    return sf.read(out)[0]
voice = np.zeros(int(200 * SR)); cur = LEAD; scenes = {}; lines = []
for k, ls in LINES.items():
    a = cur
    for i, (text, pause) in enumerate(ls):
        x = clip(k, i, text); j = int(cur * SR); voice[j:j + len(x)] += x
        lines.append([k, i, round(cur, 3), round(cur + len(x) / SR, 3), text.replace("Deem-yor", "Dmyor")]); cur += len(x) / SR + pause
    scenes[k] = [round(a, 3), round(cur, 3)]
TOTAL = round(cur + TAIL, 3); scenes[list(scenes)[-1]][1] = TOTAL
sf.write(os.path.join(D, "audio.wav"), voice[: int(TOTAL * SR)].astype(np.float32), SR)
subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", os.path.join(D, "audio.wav"), "-b:a", "192k", os.path.join(D, "audio.mp3")], check=True)
# subtitles: split each line into chunks of <= 30 chars, timed by character share
subs = []
for k, i, a, b, text in lines:
    words, chunks, c = text.split(), [], ""
    for w in words:
        if len(c) + len(w) + 1 > 30 and c: chunks.append(c); c = w
        else: c = (c + " " + w).strip()
    chunks.append(c); n = sum(len(x) for x in chunks); t = a
    for x in chunks: d = (b - a) * len(x) / n; subs.append([round(t, 3), round(t + d + .12, 3), re.sub(r"[^A-Z0-9 .,'?!:#@/-]", "", x.upper())]); t += d
json.dump({"total": TOTAL, "scenes": scenes, "lines": lines}, open(os.path.join(D, "timeline.json"), "w"), indent=1)
open(os.path.join(D, "timeline.js"), "w").write("var TL = " + json.dumps({"total": TOTAL, "scenes": scenes, "lines": lines, "subs": subs}) + ";\n")
print("length", TOTAL); [print(k, v) for k, v in scenes.items()]
