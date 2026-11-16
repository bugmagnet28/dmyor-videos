# sound design for bend-reality: voice (audio.wav) + effects -> audio_mixed.wav/mp3 (music added later by add_music.py)
import json, os, sys, subprocess, numpy as np, soundfile as sf
ROOT = os.getcwd(); D = os.path.join(ROOT, "reels/bend-reality"); sys.path.insert(0, os.path.join(ROOT, ".claude/skills/animated-illustration-explainer/scripts"))
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
# real recorded effects (Pixabay, sfx/), each RMS-normalised then set relative to the voice
def snd(name, start=0.0, dur=None, fin=.05, fout=.3):
    raw = subprocess.run(["ffmpeg", "-loglevel", "error", "-ss", str(start)] + (["-t", str(dur)] if dur else []) + ["-i", os.path.join(D, "sfx", name + ".mp3"), "-f", "f32le", "-ac", "1", "-ar", str(SR), "-"], capture_output=True, check=True).stdout
    x = np.frombuffer(raw, dtype=np.float32).astype(np.float64); n = len(x)
    if n == 0: return x
    e = np.ones(n); fi, fo = int(fin * SR), int(min(fout, n / SR / 2) * SR); e[:fi] = np.linspace(0, 1, fi); e[n - fo:] *= np.linspace(1, 0, fo)
    x = x * e; r = np.sqrt(np.mean(x[np.abs(x) > 1e-4] ** 2)) if np.any(np.abs(x) > 1e-4) else 1; return x / r
put(snd("warp", 0, 3.4, .02, 1.0), 0.15, .30)                         # the bend
put(snd("whoosh", 0, 2.2, .02, .6), L("B", 1) - .35, .22)             # screen splits into two realities
put(snd("chime", 0, 3.5, .02, 1.2), L("C", 1) - .05, .30)             # "Yes."
put(snd("clock", 0, 3.0, .2, .6), 20.3, .18)                         # late-night scroll
put(snd("whoosh", 0, 2.2, .02, .6), 23.15, .22)                        # reality diverged
put(snd("wind", 3, 4.0, .6, 1.0), 26.3, .16)                          # wing
put(snd("shimmer", 0, 4.6, .8, 1.2), 30.0, .12)                       # tree grows
for t0, txt in [(L("G", 0) + .9, "Thriving."), (L("G", 1) + .5, "Happy."), (L("G", 2) + .7, "The one I always dreamed of.")]: put(snd("typing", 1.0, len(txt) * .045 + .1, .02, .08), t0, .14)
put(snd("spell", 0, 3.0, .05, 1.0), 46.6, .22)                        # the future lights up
put(snd("typing", 1.0, .65, .02, .08), L("J", 0) + .35, .16); put(snd("send", 0, 1.1, .01, .3), L("J", 0) + 1.05, .25)
put(snd("warp2", 0, 2.2, .1, .8), 7.3, .12)                         # the road forks
put(snd("tap", 0, .5, .005, .1), 10.6, .14); put(snd("tap", 0, .5, .005, .1), 11.5, .12)   # scrolling taps
put(snd("riser", 0.2, 3.6, .8, .2), 18.857 - 3.6, .14)              # build into "yes"
put(snd("switch", 0, .6, .005, .1), 22.25, .26)                      # lights out
put(snd("cafe", 2, 3.4, .5, .6), 34.4, .10); put(snd("kids", 0, 2.2, .3, .6), 37.5, .12); put(snd("mountain", 1, 3.3, .5, .8), 39.2, .12)
for n in range(1, 8): put(snd("uiclick", 0, .4, .005, .1), 42.5 + 4.4 * (n + 1) / 8, .13)   # path lights node by node
# every movement gets a sound (owner 2026-11-17)
for t0 in [4.3, 10.0, 19.8, 26.2, 29.6, 34.6, 42.0]: put(snd("whoosh2", 0, 1.2, .005, .3), t0 - .2, .18)   # stage changes
for t0 in [2.875, 4.5, 7.6, 8.4, 10.6, 14.08, 20.3, 24.6, 27.9, 34.75, 47.9, 49.47]: put(snd("pop", 0, .5, .003, .15), t0, .15)   # labels / text appear
put(snd("risershort", 0, 2.0, .05, .4), 5.0, .14); put(snd("risershort", 0, 1.4, .05, .4), 27.3, .14)   # line climbs, lift arrow
put(snd("swipe", 0, .9, .005, .2), 26.7, .12)                        # airflow lines
for t0 in [37.4, 39.1]: put(snd("swipe", 0, .9, .005, .2), t0 - .1, .14); put(snd("paperdrop", 0, .52, .003, .15), t0 + .3, .22)   # polaroids land
put(snd("chime", 0, 2.5, .02, 1.0), 52.6, .14)                       # wordmark
# diagrams
put(snd("swipe", 0, .9, .005, .2), 16.2, .14); put(snd("risershort", 0, 1.4, .05, .4), 16.4, .12); put(snd("pop", 0, .5, .003, .15), 17.9, .15)
put(snd("warp2", 0, 1.6, .05, .6), 23.9, .10); put(snd("pop", 0, .5, .003, .15), 24.6, .15)
v, sr = sf.read(os.path.join(D, "audio.wav")); assert sr == SR
vr = np.sqrt(np.mean(v[np.abs(v) > 1e-3] ** 2)); out = np.zeros(max(len(v), len(fx))); out[:len(v)] += v; out[:len(fx)] += fx * vr
out = out[: int(TOT * SR)]; out /= max(1, np.abs(out).max() / .95)
sf.write(os.path.join(D, "audio_mixed.wav"), out.astype(np.float32), SR)
subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", os.path.join(D, "audio_mixed.wav"), "-af", "loudnorm=I=-15:TP=-1.5", "-b:a", "192k", os.path.join(D, "audio_mixed.mp3")], check=True)
print("ok", TOT)
