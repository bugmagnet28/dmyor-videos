"""Cinematic motion film: narration + composed score + sound design + one continuous-camera page.

    tts/.venv/bin/python .claude/skills/cinematic-motion/scripts/make_film.py reels/<slug> [--record] [--skip-voice]

Reads <slug>/narration.json (spoken, voice; optional dream/milestones/steps texts), makes the voice (say.py, stages),
aligns words (whisper), maps beats to spoken words (BEATS below), writes config + page, composes the score
(score() below: pads, plucks, risers, impacts; all synthesised, no samples), places sound effects on the same beats,
mixes (voice ducks music), and optionally records 1080x1920 @ 30 fps. Run from the project root.
"""
import argparse, importlib.util, json, os, re, shutil, subprocess, sys
import numpy as np, soundfile as sf
from scipy.signal import butter, sosfilt, fftconvolve

ROOT = os.getcwd(); SKILL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SR = 44100; LEAD = 1.0; TAIL = 3.2
nz = lambda s: re.sub(r"[^a-z0-9]", "", s.lower())

# beat name -> (spoken word, which occurrence after the previous beat's word); times get LEAD added
BEATS = [("hook", "dreams"), ("notes", "notes"), ("head", "head"), ("fade", "fade"), ("turn", "so"), ("one", "one"),
         ("write", "write"), ("keeps", "keeps"), ("years", "years"), ("started", "started"), ("breakdown", "break"),
         ("milestones", "milestones"), ("steps", "steps"), ("week", "week"), ("step1", "small"), ("grow", "grow"),
         ("close", "thats"), ("archive", "archive"), ("tomorrow", "tomorrow"), ("breakit", "break"), ("link", "if")]


def beats(words):
    T, i = {}, 0
    for name, w in BEATS:
        j = next(k for k in range(i, len(words)) if nz(words[k]["raw"]) == w)
        T[name] = round(words[j]["s"] + LEAD, 3); i = j + 1
    T["ring"] = round(T["one"] + .75, 3); T["light"] = round(T["ring"] + .9, 3)
    return T


# ---------------- synthesis ----------------
def tt(d): return np.arange(int(d * SR)) / SR
def hz(m): return 440 * 2 ** ((m - 69) / 12)
def lp(x, f): return sosfilt(butter(2, f, "low", fs=SR, output="sos"), x)
def hp(x, f): return sosfilt(butter(2, f, "high", fs=SR, output="sos"), x)
def bp(x, lo, hi): return sosfilt(butter(2, [lo, hi], "band", fs=SR, output="sos"), x)
rng = np.random.default_rng(5)


def add(buf, x, at, g=1.0):
    i = int(at * SR)
    if i >= len(buf) or i + len(x) <= 0: return
    j = max(0, -i); x = x[j:]; i = max(0, i); n = min(len(x), len(buf) - i); buf[i:i + n] += x[:n] * g


def env(n, a, r):
    e = np.ones(n); ai = int(a * SR); ri = int(r * SR)
    if ai: e[:ai] = np.linspace(0, 1, ai) ** 2
    if ri: e[-ri:] *= np.linspace(1, 0, ri) ** 2
    return e


def pad(notes, d, bright=6.0, a=1.6, r=2.0):
    t = tt(d); out = np.zeros(len(t))
    for m in notes:
        for det in (-.06, 0, .07):
            f = hz(m + det)
            for h in range(1, 10):
                if f * h > 9000: break
                out += np.sin(2 * np.pi * f * h * t + rng.random() * 6.28) * (1 / h) * np.exp(-h / bright)
    out = lp(out, 2400) * env(len(t), a, r)
    return out / (np.abs(out).max() + 1e-9)


def pluck(m, d=2.2, soft=1.0):
    t = tt(d); f = hz(m)
    x = (np.sin(2 * np.pi * f * t) * np.exp(-t / (.9 * soft)) + .35 * np.sin(2 * np.pi * 2.0 * f * t) * np.exp(-t / .35)
         + .12 * np.sin(2 * np.pi * 3.01 * f * t) * np.exp(-t / .18) + .05 * np.sin(2 * np.pi * 4.2 * f * t) * np.exp(-t / .08))
    a = int(.004 * SR); x[:a] *= np.linspace(0, 1, a)
    return lp(x, 3800)


def bell(m, d=3.5):
    t = tt(d); f = hz(m)
    return sum(w * np.sin(2 * np.pi * f * k * t) * np.exp(-t / dd) for k, w, dd in [(1, 1, 1.6), (2.76, .35, .7), (5.4, .15, .35), (8.9, .06, .2)])


def riser(d, f0=200, f1=4000):
    n = int(d * SR); x = rng.standard_normal(n); out = np.zeros(n); seg = int(.05 * SR)
    for s in range(0, n, seg):
        k = s / n; f = f0 * (f1 / f0) ** k
        out[s:s + seg] = bp(x[s:s + seg + 1][:seg] if s + seg <= n else x[s:], max(40, f * .7), min(18000, f * 1.3))[:len(out[s:s + seg])]
    return out * np.linspace(0, 1, n) ** 2.2


def impact(big=1.0):
    t = tt(2.6)
    sub = np.sin(2 * np.pi * (48 + 40 * np.exp(-t / .08)) * t) * np.exp(-t / .55)
    nb = lp(rng.standard_normal(len(t)), 900) * np.exp(-t / .12) * .6
    return (sub + nb) * big


def whoosh(d=.9, lo=300, hi=3000):
    n = int(d * SR); x = rng.standard_normal(n); k = np.linspace(0, 1, n); sh = np.sin(np.pi * k) ** 2
    return bp(x, lo, hi) * sh


def reverb(x, decay=2.6, wet=.28):
    n = int(decay * SR); ir = rng.standard_normal(n) * np.exp(-np.arange(n) / SR / (decay / 5.5)); ir = lp(ir, 5000); ir /= np.abs(ir).sum() ** .5 * 6
    return x * (1 - wet) + fftconvolve(x, ir)[:len(x)] * wet * 3


def score(T, total):
    buf = np.zeros(int((total + 4) * SR))
    D = 50  # D3 = MIDI 50
    # A: dark, uncertain: low drone + D minor add9 pad, sparse "thought" plucks
    add(buf, pad([38, 45], T["ring"] + .5, bright=3, a=.5, r=1.2), 0, .6)
    add(buf, bell(74, 4), .05, .12); add(buf, whoosh(1.6, 120, 1500), 0, .25)
    add(buf, pad([D, D + 3, D + 7, D + 14], T["turn"] + 1.0, bright=3.5, a=.7, r=1.5), 0, .38)
    for i, at in enumerate(np.arange(.6, T["turn"], 1.05)):
        add(buf, pluck([74, 77, 79, 81, 72, 76][i % 6], 1.8, .7), at + rng.random() * .15, .16)
    # turn: lift, then the point of light
    add(buf, riser(T["one"] - T["turn"] + .1, 150, 2500), T["turn"], .22)
    add(buf, pad([D, D + 4, D + 7, D + 11], T["light"] - T["turn"] + .8, bright=5, a=1.0, r=.8), T["turn"], .3)
    add(buf, bell(86, 3), T["one"], .14); add(buf, impact(.5), T["one"], .35)
    # tunnel into light: whoosh + impact, then the bright D major world
    add(buf, riser(T["light"] - T["ring"] + .1, 300, 9000), T["ring"] - .1, .3)
    add(buf, impact(1.0), T["light"] - .05, .55)
    add(buf, pad([D - 12, D, D + 4, D + 7, D + 11, D + 14], T["breakdown"] - T["light"] + 1.5, bright=7, a=.4, r=1.5), T["light"] - .05, .4)
    for at, m in [(T["keeps"], 81), (T["years"], 78), (T["years"] + .45, 76), (T["started"], 86)]:
        add(buf, pluck(m, 2.5, 1.2), at, .3)
    # C: the tree grows: chord walk G - A - Bm - G - A with a rising pluck arpeggio
    chords = [(T["breakdown"], [43, 55, 59, 62, 69]), (T["milestones"], [45, 57, 61, 64, 69]), (T["steps"], [47, 59, 62, 66, 69]),
              (T["step1"], [43, 55, 59, 62, 71]), (T["grow"] - .4, [45, 57, 61, 64, 71])]
    for i, (at, ns) in enumerate(chords):
        end = chords[i + 1][0] if i + 1 < len(chords) else T["close"]
        add(buf, pad(ns, end - at + 1.2, bright=6, a=.5, r=1.0), at, .32)
        arp = ns[1:] + [n + 12 for n in ns[1:3]]
        k = 0
        for bt in np.arange(at + .1, end, .33):
            dens = .12 + .18 * (bt - T["breakdown"]) / (T["close"] - T["breakdown"])
            add(buf, pluck(arp[k % len(arp)] + 12, 1.6), bt, dens); k += 1
    # D: arrival, warm D major; E: the wordmark resolves
    add(buf, pad([D - 12, D, D + 4, D + 7, D + 14, D + 16], T["link"] - T["close"] + 1.5, bright=6, a=1.0, r=1.5), T["close"] - .2, .4)
    for i, at in enumerate(np.arange(T["close"] + .3, T["link"] - .3, .66)):
        add(buf, pluck([74, 78, 81, 83, 81, 78][i % 6], 2.2, 1.3), at, .18)
    add(buf, riser(.9, 400, 6000), T["link"] - .55, .2)
    add(buf, pad([D - 24, D - 12, D, D + 4, D + 7, D + 11, D + 14], total - T["link"] + 2, bright=7, a=.25, r=2.5), T["link"] + .3, .8)
    add(buf, bell(86, 4), T["link"] + .35, .3); add(buf, bell(81, 4), T["link"] + .6, .2); add(buf, bell(78, 4), T["link"] + 1.6, .15)
    # pulse: soft kick on every beat + hats off-beat from the turn to the wordmark (keeps the reel moving)
    bp_ = .5
    for i, at in enumerate(np.arange(T["turn"], T["link"] + 1.5, bp_)):
        tk = tt(.35); kick = np.sin(2 * np.pi * (52 + 70 * np.exp(-tk / .03)) * tk) * np.exp(-tk / .16)
        g = .28 if at > T["light"] else .18
        add(buf, kick, at, g)
        hat = hp(rng.standard_normal(int(.05 * SR)), 7000) * np.exp(-np.arange(int(.05 * SR)) / SR / .012)
        add(buf, hat, at + bp_ / 2, .06 if at > T["light"] else .04)
    buf = reverb(buf[:int(total * SR)], 3.0, .3)
    fo = int(1.8 * SR); buf[-fo:] *= np.linspace(1, 0, fo) ** 2
    return buf / (np.abs(buf).max() + 1e-9)


def sfx(T, total, kit):
    buf = np.zeros(int((total + 3) * SR))
    def k(name, *a): f = getattr(kit, name)(*a); return f / (np.abs(f).max() + 1e-9)
    add(buf, whoosh(1.4, 200, 1800), T["fade"], .25)
    add(buf, whoosh(.8, 800, 6000), T["one"] + .15, .3)                  # fibres spiral out
    add(buf, whoosh(1.2, 150, 4000), T["ring"], .5)                      # tunnel
    for hi in range(int((T["fade"] + 1.0) / 1.6) + 1):                     # opening hero cards: typing, then a whoosh as each flies past
        st = hi * 1.6 - 1.0
        for at in np.arange(max(0, st), st + .85, .06):
            if at < T["fade"] and rng.random() < .75: add(buf, k("tick")[: int(.02 * SR)], at, .16)
        if st + 1.05 < T["fade"]: add(buf, whoosh(.6, 500, 4000), max(0, st + 1.0), .18)
    for i, at in enumerate(np.arange(max(T["write"], T["light"] + .15), max(T["write"], T["light"] + .15) + 1.3, .055)):
        if rng.random() < .8: add(buf, k("tick")[: int(.02 * SR)], at + rng.random() * .02, .25)   # typing
    add(buf, k("stamp"), T["keeps"], .5); add(buf, k("right", 1), T["keeps"] + .12, .35)
    add(buf, k("clock", .9), T["years"], .35)
    add(buf, whoosh(.7, 400, 3000), T["breakdown"] - .05, .4); add(buf, k("tap"), T["breakdown"] + .65, .5)
    r = lp(rng.standard_normal(int((T["grow"] - T["breakdown"]) * SR)), 1200) * .5
    r *= (0.6 + 0.4 * np.sin(np.arange(len(r)) / SR * 7)) * np.linspace(.4, 1, len(r))
    add(buf, r / (np.abs(r).max() + 1e-9), T["breakdown"] + .4, .08)          # branches growing (soft rustle)
    for i in range(3): add(buf, k("pop", i), T["milestones"] + i * .25, .4)
    for i in range(5): add(buf, k("pop", i + 2), T["steps"] + i * .18, .3)
    add(buf, k("right", 2), T["week"], .4)
    for i, at in enumerate(np.linspace(T["step1"] + .2, T["grow"] + .9, 9)): add(buf, k("pop", i % 6), at, .22)   # blossoms
    add(buf, whoosh(1.4, 250, 2500), T["close"] - .2, .4)                   # camera tilts up
    for c in [T["keeps"] - .1, T["years"] - .1, T["milestones"] - .15, T["milestones"] + .5, T["milestones"] + 1.0]:   # camera swipes only (mirrors kf() in cosmos.html)
        add(buf, whoosh(.45, 500, 5000), c, .14)
    for i in range(5): add(buf, k("tick")[: int(.03 * SR)], T["link"] + .35 + i * .09, .3)   # letters land
    return buf[:int(total * SR)]


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("reel"); ap.add_argument("--record", action="store_true"); ap.add_argument("--skip-voice", action="store_true")
    o = ap.parse_args(); d = o.reel.rstrip("/"); n = json.load(open(os.path.join(d, "narration.json")))
    py = os.path.join(ROOT, "tts/.venv/bin/python")
    if not o.skip_voice:
        say = re.sub(r"\bDmyor\b", "Deem-yor", n["spoken"])
        subprocess.run([py, os.path.join(SKILL, "scripts/say.py"), say, os.path.join(d, "audio.mp3"), "--voice", n.get("voice", "am_eric"),
                        "--gap-min", str(n.get("gap_min", .22)), "--gap-max", str(n.get("gap_max", .36)), "--stages"], check=True)
        subprocess.run(["python3", os.path.join(ROOT, ".claude/skills/dmyor-reel/scripts/align.py"), d], check=True)
    cues = json.load(open(os.path.join(d, "cues.json"))); W = cues["words"]
    T = beats(W); total = round(cues["duration"] + LEAD + TAIL, 2)
    cfg = {"t": T, "total": total, "handle": n.get("handle", "@becauseidmyor")}
    for kk in ("dream", "dreamShort", "milestones", "steps", "archived", "reopen"):
        if kk in n: cfg[kk] = n[kk]
    json.dump(cfg, open(os.path.join(d, "config.json"), "w"), indent=1)
    html = open(os.path.join(SKILL, "assets", n.get("page", "one-place.html"))).read().replace("/*__CONFIG__*/{}", json.dumps(cfg))
    html = html.replace("url(fonts/", "url(" + os.path.relpath(os.path.join(SKILL, "assets/fonts"), d) + "/")
    html = html.replace('"photos/', '"' + os.path.relpath(os.path.join(SKILL, "assets/photos"), d) + "/")
    open(os.path.join(d, "film.html"), "w").write(html)
    # audio: score + sfx + voice (voice ducks the score)
    spec = importlib.util.spec_from_file_location("kit", os.path.join(ROOT, ".claude/skills/animated-illustration-explainer/scripts/sfx.py"))
    sys.argv = ["kit", d]; kit = importlib.util.module_from_spec(spec); spec.loader.exec_module(kit)
    mus = score(T, total); fx = sfx(T, total, kit)
    sf.write(os.path.join(d, "score.wav"), (mus * .5).astype(np.float32), SR); sf.write(os.path.join(d, "sfx.wav"), (fx / (np.abs(fx).max() + 1e-9) * .5).astype(np.float32), SR)
    mix = os.path.join(d, "audio_mixed.mp3")
    fc = (f"[0:a]adelay={int(LEAD*1000)}|{int(LEAD*1000)},apad,atrim=0:{total},loudnorm=I=-16:TP=-2,asplit[v][sc];"
          f"[1:a]volume=0.42[m0];[m0][sc]sidechaincompress=threshold=0.04:ratio=5:attack=20:release=400[m];"
          f"[2:a]volume=0.55[f];[v][m][f]amix=inputs=3:normalize=0:duration=longest,atrim=0:{total},alimiter=limit=0.89,loudnorm=I=-14:TP=-1.5")
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", os.path.join(d, "audio.mp3"), "-i", os.path.join(d, "score.wav"), "-i", os.path.join(d, "sfx.wav"),
                    "-filter_complex", fc, "-ar", "44100", "-b:a", "192k", mix], check=True)
    print("beats:", T); print(f"total {total}s -> {d}/film.html, {mix}")
    if o.record:
        mp4 = os.path.join(d, "film.mp4")
        with open(os.path.join(d, "record.log"), "w") as log:
            subprocess.run(["node", "record.js", "--page", os.path.join(d, "film.html"), "--out", mp4, "--audio", mix], check=True, stdout=log, stderr=log)
        print("recorded", mp4)


if __name__ == "__main__":
    main()
