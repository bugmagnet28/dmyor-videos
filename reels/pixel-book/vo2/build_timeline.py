# v6 timeline: narration plays back to back (short breaths), and each line's slot is mapped onto the story-time span of the
# picture it describes. Writes audio.mp3 (voice), timemap.json (film u -> story t segments) and captions.json.
import json, os, numpy as np, soundfile as sf, subprocess
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SR = 44100; GAP = .36; LEAD = .35; END_HOLD = 2.4
# line: (story spans, extra time after the line for picture-only beats)
PLAN = {
 "N1": ([[0.5, 4.6]], 0), "N2": ([[4.6, 5.0], [6.3, 8.6]], 0), "N3": ([[8.6, 12.4]], .9), "N4": ([[12.4, 14.2]], 0),
 "N5": ([[14.2, 17.8]], .5), "N6": ([[17.8, 20.6]], .5), "N7": ([[20.6, 21.2], [25.5, 30.4]], .2), "N8": ([[32.0, 36.3]], 0),
 "N9": ([[36.3, 39.2]], 0), "N10": ([[40.9, 43.3]], .4), "N11": ([[46.15, 50.35]], 0), "N12": ([[50.35, 54.9]], .2),
 "N13": ([[55.15, 58.8]], 0), "N14": ([[60.2, 63.9]], 1.0), "N15": ([[66.15, 69.55]], 0), "N16": ([[69.55, 73.3]], .2),
 "N17": ([[73.55, 77.0]], 0), "N18": ([[77.8, 80.6]], 1.1), "N19": ([[80.6, 88.6]], .5), "N20": ([[90.55, 95.3]], .5),
 "N21": ([[96.9, 99.6]], 0), "N22": ([[99.6, 103.4]], .3), "N23": ([[105.55, 110.0]], .3), "N24": ([[110.9, 114.2]], .3),
 "N25": ([[116.6, 123.3]], .2), "N26": ([[124.6, 130.0]], .9), "N27": ([[130.0, 133.6]], 0), "N28": ([[139.5, 143.6]], .4),
 "N29": ([[143.6, 154.4]], 0), "END": ([[154.4, 157.0]], 0)}
CAP = {"N1": ["THIS BOOK OPENED A *DOOR.*", "N2"], "N4": ["*10 YEARS* LATER", "N5"], "N6": ["I DID ALL I *WANTED TO.*", "N6"], "N7": ["BUT *HOW?*", "N7"],
       "N9": ["STEP ONE: *WRITE IT DOWN.*", "N10"], "N14": ["WHICH *ONE?*", "N14"], "N18": ["WHICH *ONE?*", "N18"], "N19": ["AGAIN. AND *AGAIN.*", "N19"],
       "N20": ["NOT EVERY CHOICE WAS *RIGHT.*", "N20", 1560], "N21": ["IT WAS A *LESSON.*", "N22", 1560], "N24": ["EVERY SCENE. *A CHOICE.*", "N24", 900],
       "N25": ["ALL *CONNECTED.*", "N26", 1560], "N28": ["WRITE IT *DOWN.*", "N28"]}
u = 0.0; segs = []; voice = np.zeros(int(100 * SR)); slots = {}
for k, (spans, extra) in PLAN.items():
    if k == "END": d = END_HOLD; x = None
    else: x, _ = sf.read(f"vo2/_{k}.wav"); d = len(x) / SR
    lead = LEAD if k == "N1" else 0
    slot = lead + d + (GAP if k != "END" else 0) + extra
    if x is not None: i = int((u + lead) * SR); voice[i:i + len(x)] += x
    slots[k] = [round(u + lead, 3), round(u + lead + d, 3)]
    tot = sum(b - a for a, b in spans); uu = u
    for a, b in spans:
        du = slot * (b - a) / tot; segs.append([round(uu, 4), round(uu + du, 4), a, b]); uu += du
    u += slot
TOTAL = round(u, 3)
sf.write("audio.wav", voice[: int(TOTAL * SR)].astype(np.float32), SR)
subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", "audio.wav", "-b:a", "192k", "audio.mp3"], check=True)
caps = []
for k, v in CAP.items(): caps.append([slots[k][0] - .05, slots[v[1]][1] + .35, v[0], v[2] if len(v) > 2 else None])
json.dump({"segs": segs, "end_u": TOTAL, "slots": slots}, open("timemap.json", "w"), indent=0)
json.dump(caps, open("captions.json", "w"), indent=0)
print("film length", TOTAL); [print(k, s, "speed", round((s[3] - s[2]) / (s[1] - s[0]), 2)) for k, s in zip([k for k in PLAN for _ in PLAN[k][0]], segs) if (s[3] - s[2]) / (s[1] - s[0]) > 2.2]
