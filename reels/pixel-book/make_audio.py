"""Pixel Book audio: chiptune score + 8-bit/object sound effects timed to the picture, mixed under the narration.

    tts/.venv/bin/python reels/pixel-book/make_audio.py      (run from the project root)
Writes score.wav, sfx.wav, audio_mixed.mp3 in reels/pixel-book/.
"""
import importlib.util, os, subprocess, sys
import numpy as np, soundfile as sf

ROOT = os.getcwd(); D = os.path.join(ROOT, "reels/pixel-book"); SR = 44100
sys.path.insert(0, D); from timemap import t2u, in_cut, U, TOTAL


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

# ================= SCORE (v4 timeline) =================
mus = np.zeros(int((TOTAL + 2) * SR)); add = lambda buf, x, at, g: None if in_cut(at) else syn.add(buf, x, t2u(at), g)
CH = {"C": [60, 64, 67, 71], "F": [53, 57, 60, 64], "G": [55, 59, 62, 65], "Am": [57, 60, 64, 67], "Em": [52, 55, 59, 62], "Dm": [50, 53, 57, 60]}
def section(a, b, prog, step, pattern, lead_g=.16, bass_g=.3, hat=False, oct=12, kick=False, duty=.25):
    t, i = a, 0
    while t < b - .01:
        ch = CH[prog[int((t - a) / (step * len(pattern))) % len(prog)]]
        n = pattern[i % len(pattern)]
        if in_cut(t): t += step; i += 1; continue
        if n is not None: add(mus, sq(ch[n % 4] + oct + 12 * (n // 4), step * .9, duty=duty), t, lead_g)
        if i % len(pattern) == 0 and bass_g: add(mus, tri(ch[0] - 12, step * len(pattern) * .95), t, bass_g)
        if hat and i % 2 == 1: add(mus, nz(.05), t, .05)
        if kick and i % 4 == 0: add(mus, sweep(52, 28, .14, .5), t, .2)
        t += step; i += 1
ARP = [0, 1, 2, 3, 4, 3, 2, 1]; BRK = [0, 2, 1, 2, 3, 2, 1, 2]; SPARSE = [0, None, 2, None, 1, None, 3, None]
section(0, 6.6, ["C", "F"], .2, ARP, .09, .16)                                   # wonder
section(6.6, 11.3, ["Am", "F"], .14, ARP, .1, .2); add(mus, syn.riser(U(6.6, 11.2), 200, 4000), 6.6, .2)
section(12.0, 26.6, ["F", "G", "Em", "Am"], .25, BRK, .11, .26)                  # the future
section(26.9, 30.6, ["C", "G"], .1, ARP, .08, .2)                                # pages flip
section(30.6, 44.6, ["Am", "F", "C", "G"], .4, SPARSE, .1, .22)                  # ch1, quiet night
section(44.6, 50.6, ["C", "G"], .3, BRK, .1, .22)                                # morning fork
section(50.6, 55.4, ["Dm"], .8, [0, None, None, None], .07, .2, oct=0, duty=.5)  # sleep in: dull
section(55.4, 60.2, ["C", "G", "Am", "F"], .2, ARP, .11, .26, hat=True)         # get up: bright
section(60.2, 62.6, ["Am"], .2, [0, None, 0, None], .08, .2)                     # which one?
section(62.6, 64.6, ["C", "F"], .2, ARP, .11, .26)
section(64.6, 69.8, ["Am", "F"], .4, SPARSE, .09, .22)                           # evening
section(69.8, 73.8, ["Dm"], .8, [0, None, None, None], .07, .2, oct=0, duty=.5)  # scroll: dull
section(73.8, 77.8, ["F", "G", "C", "Am"], .2, ARP, .11, .26, hat=True)         # build: bright
section(77.8, 79.6, ["Am"], .2, [0, None, 0, None], .08, .2)
section(79.6, 89.0, ["C", "G", "Am", "F"], .2, BRK, .11, .28, hat=True, kick=True)   # again and again
section(89.0, 99.0, ["Am", "Dm"], .6, [0, None, 2, None], .08, .24, oct=0)      # the wrong turn
section(99.0, 104.0, ["F", "C"], .4, SPARSE, .1, .24)                            # a lesson
section(104.0, 111.0, ["C", "G", "Am", "F"], .25, BRK, .12, .28, hat=True, kick=True)  # chose again
section(111.0, 117.6, ["F", "G", "Am", "C"], .2, ARP, .1, .3, hat=True, kick=True)    # grid
section(117.6, 126.0, ["F", "G", "Am", "C"], .125, [0, 1, 2, 3, 4, 5, 6, 7], .09, .32, hat=True, kick=True)   # beams
section(126.0, 128.6, ["F", "G"], .1, [0, 2, 4, 6, 7, 6, 4, 2], .08, .3); add(mus, syn.riser(U(126.0, 128.7), 300, 5000), 126.0, .25)
for m in CH["C"] + [72, 76, 79]: add(mus, sq(m, 3.0, .5, vib=.004) * np.exp(-tt(3.0) * .9), 128.6, .07)
add(mus, tri(36, 3.0), 128.6, .35)
section(130.0, 156.0, ["C", "Am", "F", "G"], .32, [0, 2, 1, 3, None, 2, 1, None], .08, .2)   # back in the field
for m in [60, 64, 67, 72]: add(mus, sq(m, 2.8, .5) * np.exp(-tt(2.8) * 1.4), 154.0, .06)
mus = syn.reverb(mus, 1.6, .18)[: int(TOTAL * SR)]
fo = int(1.8 * SR); mus[-fo:] *= np.linspace(1, 0, fo) ** 2; mus /= np.abs(mus).max() + 1e-9
sf.write(os.path.join(D, "score.wav"), (mus * .5).astype(np.float32), SR)

# ================= SOUND EFFECTS (v4 timeline) =================
fx = np.zeros(int((TOTAL + 3) * SR)); A = lambda x, at, g: None if in_cut(at) else syn.add(fx, x, t2u(at), g)
for i in range(22): A(nz(.4, 6, 3000) * .3, i * .3, .04)                       # breeze
A(K("riffle", 1.2), 3.2, .35); for_i = [A(sq(m, .09, .25), 2.9 + i * .1, .1) for i, m in enumerate([72, 76, 79, 84])]
A(kit.step() / .6, 4.62, .35); A(K("page", .25), 4.7, .3)                       # stands, sets the book down
A(syn.riser(1.4, 200, 3000), 6.5, .3); A(sweep(48, 72, 1.3, .5), 6.6, .12)     # portal rises
for st in (7.05, 7.25): A(kit.step() / .6, st, .3)
A(K("pop", 2), 7.4, .25)                                                        # surprise
A(kit.step() / .6, 10.4, .3); A(sweep(60, 84, .35, .5), 10.65, .25)           # crouch, jump
A(syn.whoosh(1.1, 200, 6000), 11.0, .55); A(sweep(90, 40, .9), 11.25, .2)     # into the portal
A(sweep(84, 50, .5), 12.0, .2); A(kit.step() / .6, 12.5, .5)                    # tumbles out, lands
for st in np.arange(13.35, 14.7, .25): A(kit.step() / .6, st, .25)
hd = U(14.0, 21.2); th = tt(hd); chop = (0.5 + 0.5 * np.sign(np.sin(2 * np.pi * 13 * th))) * np.minimum(1, th / 1.2) * np.minimum(1, (hd - th) / 1.0)
A((nz(hd, 0, 300) * .8 + np.sin(2 * np.pi * 55 * th) * .5) * chop, 14.0, .35)                                  # helicopter rotor
A(K("door"), 16.0, .5)
for st in np.arange(16.35, 17.4, .27): A(kit.step() / .6, st, .35)
A(sweep(60, 79, .18, .5), 17.0, .25); A(K("pop", 3), 17.05, .3)
A(sq(72, .1, .5), 22.1, .08); A(sq(76, .1, .5), 22.25, .08)                   # "?"
A(syn.riser(.8, 300, 3000), 25.7, .25); A(syn.whoosh(.9, 200, 6000), 26.4, .5)
A(K("riffle", U(26.9, 30.1)), 26.9, .5); A(K("page", .32), 30.2, .45)
for at in (30.35, 32.0, 44.35, 46.2, 50.35, 55.15, 64.35, 66.2, 69.55, 73.55, 88.75, 90.6, 103.75, 105.6): A(K("page", .32), at, .5)
A(K("pencil", 1.0), 34.9, .3); A(K("pencil", 1.7), 36.35, .45); A(K("pop", 1), 38.2, .4); A(K("pencil", .5), 41.1, .4); A(syn.bell(79, 2.0), 42.5, .2)
for b in np.arange(46.5, 50.5, .14): A(sq(93, .06, .5), b, .12 if int((b - 46.5) / .14) % 4 < 3 else 0)
A(K("clock", U(51.0, 54.8)), 51.0, .3)                                                    # time slipping by
A(K("pencil", 1.2), 56.2, .3); A(K("right", 2), 57.4, .45)
A(sq(67, .12, .5), 60.6, .08); A(sq(72, .12, .5), 60.8, .08)
for st in np.arange(60.75, 62.0, .25): A(kit.step() / .6, st, .25)
A(sweep(72, 96, .3, .5), 62.25, .15); A(K("right", 4), 62.6, .5); A(syn.whoosh(.8, 400, 5000), 62.9, .35)
A(K("buzz", .5), 66.8, .2)
for i in range(18): A(K("tap"), 70.2 + i * .19, .15)                           # scrolling flicks
A(syn.whoosh(.5, 300, 1200), 72.6, .15)                                         # yawn
A(K("typing", U(74.0, 77.6)), 74.0, .3); A(K("pop", 4), 76.0, .4)
for st in np.arange(78.05, 79.2, .25): A(kit.step() / .6, st, .25)
A(sweep(72, 96, .3, .5), 79.25, .15); A(K("right", 5), 79.6, .5); A(syn.whoosh(.8, 400, 5000), 79.8, .35)
A(K("typing", U(80.8, 88.8)), 80.8, .2)
for i in range(30): A(K("tick"), 80.85 + i * .25, .12)                         # days ticking by
r = nz(U(90.7, 103.7), 0, 2500) * .8; r *= env(len(r), .4, 2.5); A(r, 90.7, .26)        # rain
A(K("page", .3), 93.55, .45); A(K("miss", 0), 93.75, .5)
A(kit.step() / .6, 97.85, .3); A(K("page", .3), 98.7, .4); A(syn.bell(84, 2.0), 99.05, .22)
for st in np.arange(100.85, 103.4, .27): A(kit.step() / .6, st, .3)
for i, at in enumerate(np.arange(106.0, 107.6, .07)): A(K("tick"), at, .15)
A(K("pop", 3), 108.85, .45); A(K("right", 4), 108.95, .5); A(K("chord", 1.5), 109.1, .25)
A(syn.whoosh(.8, 300, 4000), 110.95, .35)                                       # into the galaxy
for i in range(7): A(K("pop", i % 6), 111.2 + i * .12, .26)
A(syn.whoosh(1.0, 200, 5000), 113.5, .35)                                       # dive to the first scene
for i, at in enumerate([114.8, 116.0, 117.2, 118.4, 121.0, 122.4]): A(K("right", i), at, .4)   # the light reaches each scene
A(sweep(70, 94, .3), 118.4, .12); A(sweep(74, 98, .3), 118.5, .1)                # the path splits
A(K("miss", 1), 119.4, .25)                                                      # the wrong turn
A(syn.bell(79, 2.2), 120.6, .25); A(syn.bell(86, 2.2), 120.75, .18)             # back together
A(syn.whoosh(1.2, 200, 3000), 122.4, .3)
for i, m in enumerate([84, 88, 91, 96]): A(sq(m, .08, .25), 124.6 + i * .08, .08)
A(syn.impact(.7), 128.6, .3); A(nz(2.5, .9, 800) * .6, 128.6, .25)
for i in range(8): A(sweep(88 + (i % 2) * 3, 96, .07, .5), 131.6 + i * .5 + (i % 2) * .12, .05)   # birds
A(K("page", .32), 140.45, .5); A(K("pencil", 1.8), 141.0, .45); A(K("right", 5), 142.8, .45)
A(syn.bell(84, 2.5), 154.8, .2)
fx = fx[: int(TOTAL * SR)]
sf.write(os.path.join(D, "sfx.wav"), (fx / (np.abs(fx).max() + 1e-9) * .6).astype(np.float32), SR)

# ================= MIX =================
fc = (f"[0:a]apad,atrim=0:{TOTAL},loudnorm=I=-16:TP=-2,asplit[v][sc];[1:a]volume=0.42[m0];[m0][sc]sidechaincompress=threshold=0.05:ratio=4:attack=20:release=350[m];"
      f"[2:a]volume=0.75[f];[v][m][f]amix=inputs=3:normalize=0:duration=longest,atrim=0:{TOTAL},alimiter=limit=0.89,loudnorm=I=-14:TP=-1.5")
subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", os.path.join(D, "audio.mp3"), "-i", os.path.join(D, "score.wav"), "-i", os.path.join(D, "sfx.wav"),
                "-filter_complex", fc, "-ar", "44100", "-b:a", "192k", os.path.join(D, "audio_mixed.mp3")], check=True)
print("audio ok")
