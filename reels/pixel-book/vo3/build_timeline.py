# v7 timeline: Sam's story, one clip per sentence with a set pause after each (longer after questions and beats).
# Each line's slot maps onto the story-time span of the picture it describes. Writes audio.mp3, timemap.json, captions.json.
import json, os, subprocess, numpy as np, soundfile as sf
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SR = 44100; TEMPO = 1.09; LEAD = .35; END_HOLD = 2.4
LINES = json.load(open("vo3/lines.json"))
PLAN = {
 "N1": ([[0.5, 4.6]], 0), "N2": ([[4.6, 5.0], [6.3, 8.6]], 0), "N3": ([[8.6, 12.4]], .4), "N4": ([[12.4, 14.2]], 0),
 "N5": ([[14.2, 17.8]], 0), "N6": ([[17.8, 20.6]], 0), "N7": ([[20.6, 21.2], [25.5, 30.4]], 0), "N8": ([[32.0, 36.3]], 0),
 "N9": ([[36.3, 39.2]], 0), "N10": ([[40.9, 43.3]], 0), "N11": ([[46.15, 50.35]], 0), "N12": ([[50.35, 54.9]], 0),
 "N13": ([[55.15, 58.8]], 0), "N14": ([[60.2, 63.9]], .5), "N15": ([[66.15, 69.55]], 0), "N16": ([[69.55, 73.3]], 0),
 "N17": ([[73.55, 77.0]], 0), "N18": ([[77.8, 80.6]], .5), "N19": ([[80.6, 88.6]], 0), "N20": ([[90.55, 95.3]], 0),
 "N21": ([[96.9, 99.6]], 0), "N22": ([[99.6, 103.4]], 0), "N23": ([[105.55, 110.0]], 0), "N24": ([[110.9, 115.0]], .2),
 "N25": ([[115.0, 124.5]], .3), "N26": ([[124.5, 130.0]], .3), "N27": ([[130.0, 133.6]], 0), "N28": ([[139.5, 143.6]], 0),
 "N29": ([[143.6, 154.4]], 0), "END": ([[154.4, 157.0]], 0)}
CAP = {"N1": ["THIS BOOK OPENED A *DOOR.*", "N2"], "N4": ["*10 YEARS* LATER", "N5"], "N7": ["BUT *HOW?*", "N7"],
       "N9": ["STEP ONE: *WRITE IT DOWN.*", "N10"], "N14": ["WHICH *ONE?*", "N14"], "N18": ["WHICH *ONE?*", "N18"], "N19": ["AGAIN. AND *AGAIN.*", "N19"],
       "N20": ["NOT EVERY CHOICE WAS *RIGHT.*", "N20", 1560], "N21": ["IT WAS A *LESSON.*", "N22", 1560], "N24": ["EVERY SCENE. *A CHOICE.*", "N24", 1560],
       "N25": ["ALL *CONNECTED.*", "N26", 1560], "N28": ["WRITE IT *DOWN.*", "N28"]}
def clip(k, i):
    out = f"vo3/__{k}_{i}.wav"
    if not os.path.exists(out): subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", f"vo3/_{k}_{i}.wav", "-af", f"atempo={TEMPO}", "-ar", str(SR), "-ac", "1", out], check=True)
    return sf.read(out)[0]
u = 0.0; segs = []; voice = np.zeros(int(110 * SR)); slots = {}
for k, (spans, extra) in PLAN.items():
    lead = LEAD if k == "N1" else 0; s0 = u + lead; cur = s0
    if k == "END": cur += END_HOLD
    else:
        for i, (_, pause) in enumerate(LINES[k]):
            x = clip(k, i); j = int(cur * SR); voice[j:j + len(x)] += x; cur += len(x) / SR + pause
    slots[k] = [round(s0, 3), round(cur, 3)]
    slot = cur - u + extra; tot = sum(b - a for a, b in spans); uu = u
    for a, b in spans: du = slot * (b - a) / tot; segs.append([round(uu, 4), round(uu + du, 4), a, b]); uu += du
    u += slot
TOTAL = round(u, 3)
sf.write("audio.wav", voice[: int(TOTAL * SR)].astype(np.float32), SR)
subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", "audio.wav", "-b:a", "192k", "audio.mp3"], check=True)
caps = [[slots[k][0] - .05, slots[v[1]][1], v[0], v[2] if len(v) > 2 else None] for k, v in CAP.items()]
json.dump({"segs": segs, "end_u": TOTAL, "slots": slots}, open("timemap.json", "w"), indent=0); json.dump(caps, open("captions.json", "w"), indent=0)
print("film length", TOTAL)
