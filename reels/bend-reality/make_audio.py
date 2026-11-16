# sound design for bend-reality: voice (audio.wav) + effects -> audio_mixed.wav/mp3 (music added later by add_music.py)
import json, os, sys, subprocess, numpy as np, soundfile as sf
ROOT = os.getcwd(); D = os.path.join(ROOT, "reels/bend-reality"); sys.path.insert(0, os.path.join(ROOT, ".claude/skills/animated-illustration-explainer/scripts"))
import sfx as S
SR = 44100; tl = json.load(open(os.path.join(D, "timeline_v1.json"))); tn = json.load(open(os.path.join(D, "timeline.json"))); TOT = tn["total"]
ANCH = [[0, 0], [2.12, 2.475], [2.84, 2.875], [3.54, 4.0], [4.22, 4.55], [5.06, 5.46], [5.64, 5.665], [11.36, 9.717], [11.94, 10.217], [14.9, 12.181], [18.66, 15.82], [19.42, 16.27], [21.38, 18.507], [22.42, 18.6], [22.92, 18.857], [23.24, 19.48], [23.96, 20.03], [27.04, 23.106], [30.76, 26.156], [31.26, 26.456], [34.32, 29.253], [35.1, 29.803], [38.38, 33.2], [39.22, 33.429], [41.74, 34.62], [43.64, 37.427], [44.0, 37.627], [45.0, 39.098], [45.38, 39.298], [47.9, 41.71], [48.48, 42.21], [51.38, 44.675], [53.94, 47.376], [54.58, 47.976], [57.04, 49.219], [57.68, 49.469], [61.62, 52.802], [63.02, 55.702]]
def new(to):
    for i in range(1, len(ANCH)):
        if to <= ANCH[i][1]: a, b = ANCH[i - 1], ANCH[i]; return a[0] + (b[0] - a[0]) * (to - a[1]) / max(1e-6, b[1] - a[1])
    return TOT
def L(k, i): return [l for l in tl["lines"] if l[0] == k and l[1] == i][0][2]
fx = np.zeros(int((TOT + 1) * SR))
def put(x, t, g=1.0):
    x = np.asarray(x, dtype=np.float64)
    if x.ndim > 1: x = x.mean(axis=1)
    j = int(new(t) * SR); n = min(len(x), len(fx) - j)
    if n > 0: fx[j:j + n] += x[:n] * g
def env(n, a, r): e = np.ones(n); a, r = int(a * SR), int(r * SR); e[:a] = np.linspace(0, 1, a); e[n - r:] *= np.linspace(1, 0, r); return e
# the bend: a low drone whose pitch wobbles while the picture warps
n = int(3.2 * SR); tt = np.arange(n) / SR; f = 55 + 9 * np.sin(2 * np.pi * .9 * tt) * np.sin(np.pi * np.clip(tt / 3.0, 0, 1))
ph = 2 * np.pi * np.cumsum(f) / SR; drone = (np.sin(ph) + .5 * np.sin(2 * ph + .3) + .25 * np.sin(3.01 * ph)) * env(n, .25, 1.0)
put(drone, 0.0, .5)
def wind(d):
    n = int(d * SR); w = np.random.default_rng(5).standard_normal(n); w = S.lowpass(w, 700); m = .6 + .4 * np.sin(2 * np.pi * .35 * np.arange(n) / SR); return w * m * env(n, .6, .8)
for t in [4.3, 10.0, 19.8, 26.2, 29.6, 34.3, 37.4, 39.1, 42.0]: put(S.swish(.5), t - .12, .7)
put(S.reveal(), 8.0, .5)                          # the branch splits
put(S.swish(.7), L("B", 1) - .05, .8)             # screen splits
put(S.reveal(), L("C", 1) - .02, .9)              # "Yes."
put(S.clock(2.6), 20.3, .45)                      # late-night scroll
put(S.swish(.8), 23.3, .9); put(S.reveal(), 23.45, .6)  # reality split
put(wind(3.6), 26.3, .35)                         # wing
put(S.tone(3.8), 30.0, .25)                       # tree grows
for t0, txt in [(L("G", 0) + .9, "Thriving."), (L("G", 1) + .5, "Happy."), (L("G", 2) + .7, "The one I always dreamed of.")]: put(S.typing(len(txt) * .045), t0, .5)
nodes = 7
for i in range(1, nodes + 1): put(S.pop(i % 4), 42.5 + 4.4 * (i + .5) / (nodes + 1), .45)
put(S.chord(3.0), 46.7, .4)                       # the future lights up
put(S.typing(.6), L("J", 0) + .35, .6); put(S.toggle(), L("J", 0) + 1.05, .7)
v, sr = sf.read(os.path.join(D, "audio.wav")); assert sr == SR
out = np.zeros(max(len(v), len(fx))); out[:len(v)] += v; out[:len(fx)] += fx * .5
out = out[: int(TOT * SR)]; out /= max(1, np.abs(out).max() / .95)
sf.write(os.path.join(D, "audio_mixed.wav"), out.astype(np.float32), SR)
subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", os.path.join(D, "audio_mixed.wav"), "-af", "loudnorm=I=-15:TP=-1.5", "-b:a", "192k", os.path.join(D, "audio_mixed.mp3")], check=True)
print("ok", TOT)
