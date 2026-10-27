# Fit the film to an external narration take (e.g. ElevenLabs one-take): find each script line N1..N30 in the take
# (whisper word times), cut the take at the pauses between lines, add a little room only where a picture-only beat
# needs it, and map each line's slot onto its story-time span. Writes audio.mp3, timemap.json, captions.json.
#   tts/.venv/bin/python reels/pixel-book/vo_external.py reels/<copy> <take.mp3>
import difflib, json, os, re, subprocess, sys, numpy as np, soundfile as sf
D, TAKE = sys.argv[1], sys.argv[2]; SR = 44100; END_HOLD = 1.8; LEAD = .3
PLAN = {
 "N1": [[0.5, 4.6]], "N2": [[4.6, 5.0], [6.3, 8.6]], "N3": [[8.6, 12.4]], "N4": [[12.4, 14.2]], "N5": [[14.2, 17.8]], "N6": [[17.8, 20.6]],
 "N7": [[20.6, 21.2], [25.5, 30.4]], "N8": [[32.0, 36.3]], "N9": [[36.3, 39.2]], "N10": [[40.9, 43.3]], "N11": [[46.15, 50.35]], "N12": [[50.35, 54.9]],
 "N13": [[55.15, 58.8]], "N14": [[60.2, 63.9]], "N15": [[66.15, 69.55]], "N16": [[69.55, 73.3]], "N17": [[73.55, 77.0]], "N18": [[77.8, 80.6]],
 "N19": [[80.6, 88.6]], "N20": [[90.55, 95.3]], "N21": [[96.9, 99.6]], "N22": [[99.6, 103.4]], "N23": [[105.55, 110.0]], "N24": [[110.9, 115.0]],
 "N25": [[115.0, 124.5]], "N26": [[124.5, 130.0]], "N27": [[130.0, 133.6]], "N28": [[139.5, 143.6]], "N29": [[143.6, 154.4]], "N30": [[154.4, 155.8]]}
MIN_AFTER = {"N3": .7, "N14": .7, "N18": .8, "N24": .5, "N25": .5, "N26": .7}     # picture-only beats need at least this much after the line
CAP = {"N1": ["THIS BOOK OPENED A *DOOR.*", "N2"], "N4": ["*10 YEARS* LATER", "N5"], "N7": ["BUT *HOW?*", "N7"],
       "N9": ["STEP ONE: *WRITE IT DOWN.*", "N10"], "N14": ["WHICH *ONE?*", "N14"], "N18": ["WHICH *ONE?*", "N18"], "N19": ["AGAIN. AND *AGAIN.*", "N19"],
       "N20": ["NOT EVERY CHOICE WAS *RIGHT.*", "N20", 1560], "N21": ["IT WAS A *LESSON.*", "N22", 1560], "N24": ["EVERY SCENE. *A CHOICE.*", "N24", 1560],
       "N25": ["ALL *CONNECTED.*", "N26", 1560], "N28": ["WRITE IT *DOWN.*", "N28"]}
norm = lambda w: re.sub(r"[^a-z0-9]", "", w.lower().replace("favourite", "favorite"))
LINES = json.load(open(os.path.join(D, "vo3/lines.json"))); keys = sorted(LINES, key=lambda k: int(k[1:]))
sw, owner = [], []
for k in keys:
    for txt, _ in LINES[k]:
        for w in txt.split():
            if norm(w): sw.append(norm(w)); owner.append(k)
W = json.load(open(os.path.join(D, "cues.json")))["words"]; hw = [norm(w["w"]) for w in W]
match = {}
for a, b, n in difflib.SequenceMatcher(None, sw, hw, autojunk=False).get_matching_blocks():
    for i in range(n): match[a + i] = b + i
span = {}
for i, k in enumerate(owner):
    if i in match: j = match[i]; s = span.setdefault(k, [W[j]["s"], W[j]["e"]]); s[0] = min(s[0], W[j]["s"]); s[1] = max(s[1], W[j]["e"])
miss = [k for k in keys if k not in span]; assert not miss, ("lines not found in take", miss)
x, sr = sf.read(TAKE) if TAKE.endswith(".wav") else (None, None)
if x is None:
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", TAKE, "-ar", str(SR), "-ac", "1", os.path.join(D, "_take.wav")], check=True); x, sr = sf.read(os.path.join(D, "_take.wav"))
def quiet(a, b):                                       # cut at the quietest 20 ms between two lines, never inside a word
    a, b = max(0, a), min(len(x) / SR, max(a + .02, b)); fr = int(.02 * SR); best, bt = 1e9, (a + b) / 2
    for t in np.arange(a, b - .02, .01):
        e = float((x[int(t * SR):int(t * SR) + fr] ** 2).mean())
        if e < best: best, bt = e, t + .01
    return bt
# whisper word ends run early, so search a little past them; the last line keeps the take to its very end
cuts = [max(0, span[keys[0]][0] - LEAD)] + [quiet(span[keys[i]][1] - .05, span[keys[i + 1]][0]) for i in range(len(keys) - 1)] + [len(x) / SR]
out, u, segs, slots = [], 0.0, [], {}
for i, k in enumerate(keys):
    a, b = cuts[i], cuts[i + 1]; piece = x[int(a * SR):int(b * SR)]
    after = b - span[k][1]; pad = max(0, MIN_AFTER.get(k, 0) - after) + (END_HOLD if k == keys[-1] else 0)
    piece = np.concatenate([piece, np.zeros(int(pad * SR))]); dur = len(piece) / SR
    slots[k] = [round(u + (span[k][0] - a), 3), round(u + (span[k][1] - a), 3)]
    tot = sum(q - p for p, q in PLAN[k]); uu = u
    for p, q in PLAN[k]:
        du = (dur - (END_HOLD if k == keys[-1] else 0)) * (q - p) / tot; segs.append([round(uu, 4), round(uu + du, 4), p, q]); uu += du
    if k == keys[-1]: segs.append([round(uu, 4), round(uu + END_HOLD, 4), 155.8, 157.0])
    out.append(piece); u += dur
voice = np.concatenate(out); TOTAL = round(len(voice) / SR, 3)
sf.write(os.path.join(D, "audio.wav"), voice.astype(np.float32), SR)
subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", os.path.join(D, "audio.wav"), "-b:a", "192k", os.path.join(D, "audio.mp3")], check=True)
caps = [[slots[k][0] - .05, slots[v[1]][1] + .2, v[0], v[2] if len(v) > 2 else None] for k, v in CAP.items()]
json.dump({"segs": segs, "end_u": TOTAL, "slots": slots}, open(os.path.join(D, "timemap.json"), "w"), indent=0)
json.dump(caps, open(os.path.join(D, "captions.json"), "w"), indent=0)
print(D, "film length", TOTAL, "| speed of picture per line:", {k: round(sum(s[3] - s[2] for s in segs if s[2] >= PLAN[k][0][0] and s[3] <= PLAN[k][-1][1]) / (slots[k][1] - slots[k][0] + 1e-9), 1) for k in ("N3", "N19", "N25")})
