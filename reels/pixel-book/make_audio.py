"""Pixel Book audio: chiptune score + 8-bit/object sound effects timed to the picture, mixed under the narration.

    tts/.venv/bin/python reels/pixel-book/make_audio.py      (run from the project root)
Writes score.wav, sfx.wav, audio_mixed.mp3 in reels/pixel-book/.
"""
import importlib.util, os, subprocess, sys
import numpy as np, soundfile as sf

ROOT = os.getcwd(); D = os.path.join(ROOT, "reels/pixel-book"); SR = 44100; TOTAL = 55.4


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
def sq(m, d, duty=.5, vib=0.0):
    t = tt(d); f = hz(m) * (1 + vib * np.sin(2 * np.pi * 5.5 * t)); ph = np.cumsum(f) / SR
    return np.where((ph % 1) < duty, 1.0, -1.0) * env(len(t), .004, min(.12, d * .5))
def tri(m, d):
    t = tt(d); ph = hz(m) * t; return (2 * np.abs(2 * (ph % 1) - 1) - 1) * env(len(t), .005, min(.1, d * .4))
def nz(d, decay=30.0, hp=6000):
    x = np.random.default_rng(int(d * 1e4)).uniform(-1, 1, int(d * SR)) * np.exp(-tt(d) * decay); return syn.hp(x, hp)
def sweep(m0, m1, d, duty=.25):
    t = tt(d); f = hz(m0) * (hz(m1) / hz(m0)) ** (t / d); ph = np.cumsum(f) / SR
    return np.where((ph % 1) < duty, 1.0, -1.0) * env(len(t), .003, .05)
def K(name, *a):
    f = getattr(kit, name)(*a); return f / (np.abs(f).max() + 1e-9)

# ================= SCORE =================
mus = np.zeros(int((TOTAL + 2) * SR)); add = lambda buf, x, at, g: syn.add(buf, x, at, g)
CH = {"C": [60, 64, 67, 71], "F": [53, 57, 60, 64], "G": [55, 59, 62, 65], "Am": [57, 60, 64, 67], "Em": [52, 55, 59, 62], "Dm": [50, 53, 57, 60]}
def section(a, b, prog, step, pattern, lead_g=.16, bass_g=.3, hat=False, oct=12, kick=False):
    t, i = a, 0
    while t < b - .01:
        ch = CH[prog[int((t - a) / (step * len(pattern))) % len(prog)]]
        n = pattern[i % len(pattern)]
        if n is not None: add(mus, sq(ch[n % 4] + oct + 12 * (n // 4), step * .9, duty=.25), t, lead_g)
        if i % len(pattern) == 0: add(mus, tri(ch[0] - 12, step * len(pattern) * .95), t, bass_g)
        if hat and i % 2 == 1: add(mus, nz(.05), t, .06)
        if kick and i % 4 == 0: add(mus, sweep(52, 28, .14, .5), t, .22)
        t += step; i += 1
# 1 wonder: twinkling arps
section(0, 2.85, ["C", "F"], .15, [0, 1, 2, 3, 4, 3, 2, 1], .11, .18)
# 2 the future: warm, broad
section(2.85, 8.75, ["F", "G", "Em", "Am"], .184, [0, 2, 1, 2, 3, 2, 1, 2], .12, .28)
# 3 choices: steady pulse with hats
section(8.75, 22.85, ["Am", "F", "C", "G"], .3, [0, 2, 1, 2, 3, 2, 1, 2], .12, .3, hat=True)
# 4 failure: sparse, low
section(22.85, 25.95, ["Am", "Dm"], .6, [0, None, 2, None], .1, .26, oct=0)
# 5 again + grid: brighter, kick
section(25.95, 31.3, ["C", "G", "Am", "F"], .25, [0, 2, 4, 2, 1, 3, 5, 3], .12, .3, hat=True, kick=True)
# 6 beams: full arps 16ths
section(31.3, 37.9, ["F", "G", "Am", "C"], .125, [0, 1, 2, 3, 4, 5, 6, 7], .1, .32, hat=True, kick=True)
# 7 converge -> white
section(37.9, 40.0, ["F", "G"], .1, [0, 2, 4, 6, 7, 6, 4, 2], .09, .3)
add(mus, syn.riser(2.1, 300, 5000), 37.9, .25)
for m in CH["C"] + [72, 76, 79]: add(mus, sq(m, 3.0, .5, vib=.004) * np.exp(-tt(3.0) * .9), 40.0, .07)
add(mus, tri(36, 3.0), 40.0, .35)
# 8 field again: gentle
section(41.8, TOTAL - 1.2, ["C", "Am", "F", "G"], .3, [0, 2, 1, 3, None, 2, 1, None], .09, .22)
for m in [60, 64, 67, 72]: add(mus, sq(m, 2.8, .5) * np.exp(-tt(2.8) * 1.4), TOTAL - 2.9, .06)
mus = syn.reverb(mus, 1.6, .18)[: int(TOTAL * SR)]
fo = int(1.6 * SR); mus[-fo:] *= np.linspace(1, 0, fo) ** 2; mus /= np.abs(mus).max() + 1e-9
sf.write(os.path.join(D, "score.wav"), (mus * .5).astype(np.float32), SR)

# ================= SOUND EFFECTS =================
fx = np.zeros(int((TOTAL + 3) * SR)); A = lambda x, at, g: syn.add(fx, x, at, g)
# 1 field + pulled into the book
for i in range(10): A(nz(.4, 6, 3000) * .3, i * .28, .05)                      # breeze
A(K("riffle", 1.0), .4, .35); A(syn.riser(1.2, 600, 6000), .25, .2)
for i, m in enumerate([72, 76, 79, 84, 88]): A(sq(m, .09, .25), .3 + i * .1, .12)  # shimmer
A(syn.whoosh(1.0, 200, 5000), 1.45, .55); A(sweep(84, 40, .7), 1.5, .22)           # suction zap
A(K("page", .3), 2.25, .5); A(syn.bell(84, 2.0), 2.55, .25)
# 2 house
t = tt(1.25); A(np.sin(2 * np.pi * (48 + 10 * t) * t) * np.exp(-((t - .6) ** 2) * 3) * .9 + nz(1.25, 1.5, 1500) * .5, 2.85, .4)   # engine + gravel
A(K("door"), 4.35, .5)
for st in np.arange(4.5, 5.7, .26): A(kit.step() / .6, st, .35)
A(sweep(60, 79, .18, .5), 7.38, .25); A(K("pop", 2), 7.42, .3)                   # surprised blip
# 3 flips between chapters
for at in (8.55, 14.35, 17.3, 22.65, 25.75): A(K("page", .32), at, .55)
A(K("pencil", 1.4), 9.0, .35); A(syn.bell(79, 1.5), 10.3, .18)
A(K("pencil", 1.9), 11.75, .45); A(K("right", 3), 13.75, .45)
# alarm
for b in np.arange(14.6, 16.55, .14): A(sq(93, .06, .5), b, .14 if int((b - 14.6) / .14) % 4 < 3 else 0)
A(K("pop", 0), 15.35, .4); A(K("pop", 1), 15.5, .4); A(K("right", 0), 16.6, .5); A(K("tick"), 16.6, .4)
# friends, choices, typing
for at in (17.62, 17.82): A(sq(67, .16, .5) + sq(71, .16, .5), at, .14)        # horn
A(K("pop", 2), 17.6, .4); A(K("pop", 3), 17.75, .4); A(K("right", 1), 18.2, .5)
for st in np.arange(18.45, 18.95, .26): A(kit.step() / .6, st, .3)
A(K("pop", 4), 18.5, .4); A(K("pop", 5), 18.62, .4); A(K("buzz", .5), 18.55, .25); A(K("right", 2), 19.13, .5)
A(K("typing", 3.8), 19.0, .3)
# shop in the rain
r = nz(3.4, 0, 2500) * .8; r *= env(len(r), .3, .4); A(r, 22.75, .28)
A(K("page", .3), 24.98, .45); A(K("miss", 0), 25.1, .5)
# office
for i, at in enumerate(np.arange(26.0, 26.95, .06)): A(K("tick"), at, .18)
A(K("pop", 3), 26.85, .45); A(K("right", 4), 26.9, .5); A(K("chord", 1.5), 27.05, .25)
# grid
A(syn.whoosh(.8, 300, 4000), 28.25, .35)
for i in range(8): A(K("pop", i % 6), 28.55 + i * .1, .3)
# melt + beams
for i, m in enumerate([84, 79, 76, 72, 67, 64, 60]): A(sq(m, .07, .25), 31.3 + i * .07, .12)
A(syn.whoosh(1.0, 200, 6000), 31.5, .4)
for i in range(4): A(sweep(70 + i * 3, 90 + i * 3, .22), 33.3 + i * .08, .1)
for i, at in enumerate((34.6, 34.9, 35.2, 35.5)): A(syn.bell(76 + [0, 3, 7, 12][i], 2.0), at, .22)
for i, m in enumerate([84, 88, 91, 96]): A(sq(m, .08, .25), 36.05 + i * .06, .1)
A(syn.impact(.7), 40.0, .3); A(nz(2.5, .9, 800) * .6, 40.0, .25)
# field again, writing
for i in range(6): A(sweep(88 + (i % 2) * 3, 96, .07, .5), 41.9 + i * .37 + (i % 2) * .12, .05)   # birds
A(K("page", .32), 42.5, .5); A(K("pencil", 1.7), 43.35, .45); A(K("right", 5), 45.0, .45)
A(syn.bell(84, 2.5), 50.6, .2)
fx = fx[: int(TOTAL * SR)]
sf.write(os.path.join(D, "sfx.wav"), (fx / (np.abs(fx).max() + 1e-9) * .6).astype(np.float32), SR)

# ================= MIX =================
fc = (f"[0:a]apad,atrim=0:{TOTAL},loudnorm=I=-16:TP=-2,asplit[v][sc];[1:a]volume=0.42[m0];[m0][sc]sidechaincompress=threshold=0.05:ratio=4:attack=20:release=350[m];"
      f"[2:a]volume=0.75[f];[v][m][f]amix=inputs=3:normalize=0:duration=longest,atrim=0:{TOTAL},alimiter=limit=0.89,loudnorm=I=-14:TP=-1.5")
subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", os.path.join(D, "audio.mp3"), "-i", os.path.join(D, "score.wav"), "-i", os.path.join(D, "sfx.wav"),
                "-filter_complex", fc, "-ar", "44100", "-b:a", "192k", os.path.join(D, "audio_mixed.mp3")], check=True)
print("audio ok")
