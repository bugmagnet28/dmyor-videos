"""pixel-destiny audio: soft chiptune score + object sound effects, mixed under the Kokoro narration.
    tts/.venv/bin/python reels/pixel-destiny/make_audio.py   (from the project root)"""
import importlib.util, json, os, subprocess, sys
import numpy as np, soundfile as sf
ROOT = os.getcwd(); D = os.path.join(ROOT, "reels/pixel-destiny"); SR = 44100
TL = json.load(open(os.path.join(D, "timeline.json"))); TOTAL = TL["total"]; SC = TL["scenes"]
LN = {(l[0], l[1]): l[2] for l in TL["lines"]}
def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m
sys.argv = ["kit", D]
kit = load("kit", os.path.join(ROOT, ".claude/skills/animated-illustration-explainer/scripts/sfx.py"))
syn = load("syn", os.path.join(ROOT, ".claude/skills/cinematic-motion/scripts/make_film.py"))
def tt(d): return np.arange(int(d * SR)) / SR
def hz(m): return 440 * 2 ** ((m - 69) / 12)
def env(n, a=.005, r=.08):
    e = np.ones(n); na, nr = int(a * SR), int(r * SR)
    if na: e[:na] = np.linspace(0, 1, na)
    if nr and nr < n: e[-nr:] *= np.linspace(1, 0, nr)
    return e
def sq(m, d, duty=.5): t = tt(d); ph = hz(m) * t; return np.where((ph % 1) < duty, 1.0, -1.0) * env(len(t), .004, min(.12, d * .5))
def tri(m, d): t = tt(d); ph = hz(m) * t; return (2 * np.abs(2 * (ph % 1) - 1) - 1) * env(len(t), .005, min(.1, d * .4))
def nz(d, decay=30.0, hp=6000): x = np.random.default_rng(int(d * 1e4)).uniform(-1, 1, int(d * SR)) * np.exp(-tt(d) * decay); return syn.hp(x, hp)
def sweep(m0, m1, d, duty=.25): t = tt(d); f = hz(m0) * (hz(m1) / hz(m0)) ** (t / d); ph = np.cumsum(f) / SR; return np.where((ph % 1) < duty, 1.0, -1.0) * env(len(t), .003, .05)
def K(name, *a): f = getattr(kit, name)(*a); return f / (np.abs(f).max() + 1e-9)
mus = np.zeros(int((TOTAL + 3) * SR)); add = lambda x, at, g: syn.add(mus, x, at, g)
CH = {"C": [60, 64, 67, 71], "F": [53, 57, 60, 64], "G": [55, 59, 62, 65], "Am": [57, 60, 64, 67], "Em": [52, 55, 59, 62], "Dm": [50, 53, 57, 60]}
def section(a, b, prog, step, pattern, lead_g=.1, bass_g=.22, hat=False, oct=12, duty=.25):
    t, i = a, 0
    while t < b - .01:
        ch = CH[prog[int((t - a) / (step * len(pattern))) % len(prog)]]; n = pattern[i % len(pattern)]
        if n is not None: add(sq(ch[n % 4] + oct + 12 * (n // 4), step * .9, duty), t, lead_g)
        if i % len(pattern) == 0 and bass_g: add(tri(ch[0] - 12, step * len(pattern) * .95), t, bass_g)
        if hat and i % 2 == 1: add(nz(.05), t, .04)
        t += step; i += 1
SP = [0, None, 2, None, 1, None, 3, None]; ARP = [0, 1, 2, 3, 4, 3, 2, 1]; BRK = [0, 2, 1, 2, 3, 2, 1, 2]
section(0, SC["S2"][1], ["Am", "F", "C", "G"], .45, SP, .07, .16)                       # night, thinking
section(SC["S3"][0], SC["S4"][0], ["Am", "F"], .3, SP, .08, .2)                          # possibility
section(SC["S4"][0], SC["S5"][0], ["F", "G", "Em", "Am"], .25, BRK, .09, .22)            # the path
section(SC["S5"][0], SC["S6"][1], ["C", "G", "Am", "F"], .2, ARP, .09, .24, hat=True)    # execution, again
section(SC["S7"][0], SC["S7"][1], ["F", "G", "Am", "C"], .16, ARP, .08, .26, hat=True)   # many realities
section(SC["S8"][0], TOTAL, ["C", "Am", "F", "G"], .4, SP, .07, .18)
mus = syn.reverb(mus, 1.6, .2)[: int(TOTAL * SR)]; fo = int(2.0 * SR); mus[-fo:] *= np.linspace(1, 0, fo) ** 2; mus /= np.abs(mus).max() + 1e-9
fx = np.zeros(int((TOTAL + 3) * SR)); A = lambda x, at, g: syn.add(fx, x, at, g)
# fan whir: soft, slow amplitude wobble, fades out after the opening and comes back at the end
def whir(d): t = tt(d); return syn.lp(np.random.default_rng(3).uniform(-1, 1, len(t)), 500) * (0.75 + 0.25 * np.sin(2 * np.pi * 2.3 * t))
w1 = whir(SC["S2"][1]); w1 *= np.clip(1 - (tt(len(w1) / SR) - (SC["S1"][1] - 1)) / 3, 0, 1); A(w1, 0, .22)
w2 = whir(2.0) * np.linspace(1, 0, int(2.0 * SR)); A(w2, SC["S8"][0], .2)
s2 = LN[("S2", 0)]; [A(K("tap"), s2 + .3 + i * .16, .3) for i in range(5)]               # dice rattle
A(syn.whoosh(.4, 600, 5000), LN[("S2", 1)] - .1, .3); A(K("page", .32), LN[("S2", 1)] + .1, .25); A(K("pop", 1), LN[("S2", 2)], .3)
for i in range(14): A(K("tick"), LN[("S3", 2)] + i * .1, .12)                            # gauge needle falling
A(K("miss", 0), LN[("S3", 3)], .3); A(K("right", 2), LN[("S3", 4)] + .3, .4)
for i in range(3): A(K("pop", i), LN[("S4", 1)] + i * .25, .3)                           # signposts
pick = LN[("S4", 2)] + 2.2; A(K("right", 3), pick, .45)
for st in np.arange(pick + .55, SC["S4"][1], .3): A(kit.step() / .6, st, .25)
A(K("stamp"), LN[("S5", 1)] + .2, .35); A(syn.impact(.25), LN[("S5", 2)], .2)             # the goal block cracks
for i in range(3): A(K("pop", i + 2), LN[("S5", 3)] + .1 + i * .2, .3)
for i in range(9): A(sq(72 + i, .06, .5), LN[("S5", 4)] + i * .22, .07)                  # stairs assemble
A(kit.step() / .6, LN[("S5", 5)] + .6, .35); A(syn.bell(84, 2.0), LN[("S5", 5)] + .65, .22)
cyc = (SC["S6"][1] - SC["S6"][0]) / 2.2
for r in range(3):
    t0 = SC["S6"][0] + r * cyc
    if t0 + cyc * .45 < SC["S6"][1]: A(K("miss", 1), t0 + cyc * .45, .25); A(nz(.5, 6, 2000), t0 + cyc * .47, .12)
    if t0 + cyc * .7 < SC["S6"][1]: A(K("right", 4), t0 + cyc * .7, .3)
for i in range(10): A(sq(84 + (i % 5) * 2, .07, .25), SC["S7"][0] + .5 + i * .9, .05)     # lights branching
A(K("page", .32), SC["S8"][0] + 1.4, .2); A(K("toggle"), SC["S8"][0] + 1.6, .35)          # lamp on
for i in range(4): A(kit.softwrite(.5) if hasattr(kit, "softwrite") else K("pencil", .5), SC["S8"][0] + 2.2 + i * .6, .18)
A(syn.bell(79, 2.5), LN[("S8", 2)] - .2, .2)
fx = fx[: int(TOTAL * SR)]; ref = np.percentile(np.abs(fx[np.abs(fx) > 1e-4]), 99.5) + 1e-9
sf.write(os.path.join(D, "score.wav"), (mus * .5).astype(np.float32), SR); sf.write(os.path.join(D, "sfx.wav"), (np.tanh(fx / ref * 1.1) * .62).astype(np.float32), SR)
fc = (f"[0:a]apad,atrim=0:{TOTAL},loudnorm=I=-16:TP=-2,asplit[v][sc];[1:a]volume=0.38[m0];[m0][sc]sidechaincompress=threshold=0.05:ratio=4:attack=20:release=350[m];"
      f"[2:a]volume=0.75[f];[v][m][f]amix=inputs=3:normalize=0:duration=longest,atrim=0:{TOTAL},alimiter=limit=0.89,loudnorm=I=-14:TP=-1.5")
subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", os.path.join(D, "audio.mp3"), "-i", os.path.join(D, "score.wav"), "-i", os.path.join(D, "sfx.wav"),
                "-filter_complex", fc, "-ar", "44100", "-b:a", "192k", os.path.join(D, "audio_mixed.mp3")], check=True)
print("audio ok", TOTAL)
