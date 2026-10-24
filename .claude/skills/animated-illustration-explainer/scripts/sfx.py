"""Subtle, synthesized sound design for illustrated reels (no samples, no licensing).

    python3 sfx.py <reel_dir> --level subtle|present [--kit-out DIR]

Reads <reel_dir>/config.json (scene types + t0/t1, brandT, total) and ../assets/events.json (sound moments per
scene type), renders an effects track and mixes it under <reel_dir>/audio_voice.mp3 (voice ducks the effects)
into <reel_dir>/audio_mixed.mp3. Scene changes get a soft swish, except the first scene (already on screen at frame 0)
and scenes that open with their own sound; the brand card gets a soft chord.
"""
import argparse, json, os, re, subprocess, tempfile
import numpy as np

SR = 44100
rng = np.random.default_rng(3)
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def env(n, a, d):
    t = np.arange(n) / SR
    return np.minimum(1, t / max(a, 1e-4)) * np.exp(-t / d)


def lowpass(x, fc):
    a = np.exp(-2 * np.pi * np.asarray(fc) / SR); y = np.zeros_like(x); s = 0.0
    a = np.broadcast_to(a, x.shape)
    for i in range(len(x)):
        s = (1 - a[i]) * x[i] + a[i] * s; y[i] = s
    return y


def tick():
    n = int(.09 * SR); t = np.arange(n) / SR
    s = (np.sin(2 * np.pi * 2100 * t) * .6 + np.sin(2 * np.pi * 3150 * t) * .25) * env(n, .001, .018)
    return s + lowpass(rng.standard_normal(n), 3000) * env(n, .0005, .004) * .5


def tap():
    n = int(.14 * SR); t = np.arange(n) / SR
    body = np.sin(2 * np.pi * (170 + 60 * np.exp(-t / .02)) * t) * env(n, .002, .045)
    paper = lowpass(rng.standard_normal(n), 1800) * env(n, .001, .012) * .9
    return body * .8 + paper


def swish(d=.42):
    n = int(d * SR); t = np.arange(n) / SR; ph = t / d
    sh = np.sin(np.pi * ph) ** 2
    x = lowpass(rng.standard_normal(n), 400 + 2200 * sh)
    x = x - lowpass(x, 250)
    return x * sh * 1.6


def ratchet(d=1.2):
    n = int((d + .1) * SR); out = np.zeros(n); k = 14
    for i in range(k):
        u = (i / (k - 1)) ** 1.6; at = int(u * d * SR)   # eases out like the counters
        c = tick()[: int(.03 * SR)] * (.55 - .25 * i / k)
        out[at:at + len(c)] += c[: n - at]
    return out


def tone(d=2.2):
    n = int(d * SR); t = np.arange(n) / SR
    s = sum(w * np.sin(2 * np.pi * f * t) for f, w in [(196, .5), (196.6, .3), (293.7, .35), (392, .18)])
    return lowpass(s, 1200) * env(n, .35, .9) * .55


def chord(d=3.0):
    n = int(d * SR); t = np.arange(n) / SR; s = np.zeros(n)
    for f in (261.6, 329.6, 392.0, 493.9):
        s += (np.sin(2 * np.pi * f * t) + .25 * np.sin(2 * np.pi * 2 * f * t) + .08 * np.sin(2 * np.pi * 3.01 * f * t)) * env(n, .02, 1.1)
    return lowpass(s, 2600) * .22


def reson(x, f, q=12):
    """2-pole resonator (band-pass) at f Hz"""
    w = 2 * np.pi * f / SR; r = 1 - w / (2 * q); c1, c2 = 2 * r * np.cos(w), -r * r; y = np.zeros_like(x); y1 = y2 = 0.0
    for i in range(len(x)):
        y0 = x[i] + c1 * y1 + c2 * y2; y[i] = y0; y2, y1 = y1, y0
    return y


def noise(n):
    return rng.standard_normal(n)


def hp(x, fc):
    return x - lowpass(x, fc)


# ---- object sounds (diegetic: each thing sounds like itself) ----
def clock_click(hi=True):
    n = int(.05 * SR); x = noise(n) * env(n, .0003, .003)
    return reson(x, 3400 if hi else 2700, 18) + reson(x, 1250 if hi else 1050, 10) * .5


def clock(d=4.0):
    """mechanical tick-tock, two per second, for as long as the clock is on screen"""
    n = int(d * SR); out = np.zeros(n + SR)
    for i in range(int(d / .5) + 1):
        c = clock_click(i % 2 == 0); at = int(i * .5 * SR); out[at:at + len(c)] += c
    return out[:n]


def timer(d=2.0):
    """faster, lighter ticking of a running timer"""
    n = int(d * SR); out = np.zeros(n + SR)
    for i in range(int(d / .16) + 1):
        c = clock_click(True)[: int(.03 * SR)] * .7; at = int(i * .16 * SR); out[at:at + len(c)] += c
    return out[:n]


def pencil(d=.3):
    """graphite on paper: grainy high noise, a little pressure swell"""
    n = int(d * SR); t = np.arange(n) / SR
    grain = np.repeat(rng.uniform(.3, 1, int(n / 90) + 1), 90)[:n]
    x = hp(lowpass(noise(n), 7000), 1800) * grain
    shape = np.sin(np.pi * np.clip(t / d, 0, 1)) ** .6
    return x * shape


def pen_check():
    """a check mark written by hand: short down-stroke, longer up-stroke"""
    a, b = pencil(.06), pencil(.15)
    return np.concatenate([a, np.zeros(int(.02 * SR)), b * 1.1])


def page(d=.32):
    """single paper page flip"""
    n = int(d * SR); t = np.arange(n) / SR; ph = t / d
    flutter = 1 + .6 * np.sin(2 * np.pi * (18 + 30 * ph) * t)
    x = hp(lowpass(noise(n), 5200), 700) * flutter * np.sin(np.pi * ph) ** 1.5
    snap = hp(noise(n), 2000) * env(n, .0005, .008) * .8
    return x + np.roll(snap, int(.7 * n))


def riffle(d=1.5):
    """a stack of pages riffling (pages counting up)"""
    n = int(d * SR); out = np.zeros(n + SR); k = int(d / .06)
    for i in range(k):
        u = (i / k) ** 1.4; p_ = page(.09) * (.5 + .5 * rng.random()); at = int(u * d * SR); out[at:at + len(p_)] += p_
    return out[:n]


def step():
    n = int(.16 * SR); t = np.arange(n) / SR
    thud = np.sin(2 * np.pi * (85 + 40 * np.exp(-t / .015)) * t) * env(n, .003, .035)
    scuff = hp(lowpass(noise(n), 2500), 400) * env(n, .01, .03) * .35
    return thud + scuff


def footsteps(d=3.5):
    n = int(d * SR); out = np.zeros(n + SR)
    for i in range(int(d / .52) + 1):
        s_ = step() * (.85 if i % 2 else 1); at = int(i * .52 * SR); out[at:at + len(s_)] += s_
    return out[:n]


def plate():
    """weight plate clink: inharmonic metal partials over a low thump"""
    n = int(1.2 * SR); t = np.arange(n) / SR
    m = sum(w * np.sin(2 * np.pi * f * t) * np.exp(-t / dd) for f, w, dd in [(523, .5, .5), (1318, .35, .3), (2467, .2, .18), (3950, .12, .1)])
    thump = np.sin(2 * np.pi * 70 * t) * env(n, .002, .06) * .6
    return (m * env(n, .001, 10) + thump)


def stamp():
    """rubber stamp on paper"""
    n = int(.25 * SR); t = np.arange(n) / SR
    return np.sin(2 * np.pi * (95 + 50 * np.exp(-t / .01)) * t) * env(n, .002, .05) + hp(lowpass(noise(n), 3000), 300) * env(n, .001, .015) * .7


def beep2():
    """soft double beep: the timer is over"""
    n = int(.11 * SR); t = np.arange(n) / SR; b = np.sin(2 * np.pi * 880 * t) * np.sin(np.pi * t / .11) ** 2
    return np.concatenate([b, np.zeros(int(.07 * SR)), b])


def right(i=0):
    """"correct" chime: two quick soft mallet notes rising a fifth; i = position in a run of checks (each one a step higher)"""
    f = 659.3 * 2 ** ([0, 4, 7, 12, 14, 16, 19, 24][min(i, 7)] / 12)
    def note(fr, d=.45):
        n = int(d * SR); t = np.arange(n) / SR
        return (np.sin(2 * np.pi * fr * t) + .18 * np.sin(2 * np.pi * 3.98 * fr * t) * np.exp(-t / .04)) * env(n, .002, .16)
    a, b = note(f), note(f * 1.5); gap = int(.075 * SR); out = np.zeros(gap + len(b))
    out[:len(a)] += a * .75; out[gap:] += b
    return out


def pop(i=0):
    """bubble pop for something appearing: quick upward pitch sweep, tight decay; pitch varies a little per item"""
    n = int(.1 * SR); t = np.arange(n) / SR; base = 380 * 2 ** (([0, 3, 5, 7, 10, 12][i % 6] + rng.uniform(-.4, .4)) / 12)
    fr = base * (1 + 1.6 * (1 - np.exp(-t / .012)))
    ph = 2 * np.pi * np.cumsum(fr) / SR
    body = np.sin(ph) * env(n, .0015, .022)
    click = hp(noise(n), 3000) * env(n, .0003, .002) * .25
    return body + click


def miss(i=0):
    """soft "wrong": two muted notes falling"""
    def note(f, d=.24):
        n = int(d * SR); t = np.arange(n) / SR
        return lowpass(np.sin(2 * np.pi * f * t) + .3 * np.sin(2 * np.pi * 2 * f * t), 1400) * env(n, .004, .08)
    a, b = note(330), note(247); gap = int(.1 * SR); out = np.zeros(gap + len(b)); out[:len(a)] += a; out[gap:] += b
    return out


KIT = {"tick": tick, "tap": tap, "swish": swish, "ratchet": ratchet, "tone": tone, "chord": chord,
       "clock": clock, "timer": timer, "pencil": pencil, "pen_check": pen_check, "page": page, "riffle": riffle,
       "footsteps": footsteps, "plate": plate, "stamp": stamp, "beep2": beep2, "right": right, "pop": pop, "miss": miss}
PEAK = {"tick": -16, "tap": -16, "swish": -21, "ratchet": -19, "tone": -21, "chord": -16,   # dBFS peak at "present" (voice peaks ~-1.5)
        "clock": -18, "timer": -20, "pencil": -15, "pen_check": -15, "page": -15, "riffle": -18,
        "footsteps": -15, "plate": -15, "stamp": -14, "beep2": -21, "right": -15, "pop": -14, "miss": -16}
LEVEL = {"present": 0, "subtle": -6}
BEDS = {"clock", "timer", "footsteps", "riffle"}   # continuous sounds: may overlap one-shots


def beat(x, at):
    """a time: seconds, or "@i" / "@i+0.3" = animation beat i of the scene (params.at, resolved from spoken cues)"""
    if isinstance(x, (int, float)):
        return float(x)
    m = re.match(r"@(\d+)([+-][\d.]+)?$", str(x))
    return at[int(m.group(1))] + (float(m.group(2)) if m.group(2) else 0.0)


def events(cfg, table, min_gap=.28):
    ev = []
    for i, sc in enumerate(cfg["scenes"]):
        P = sc.get("params") or {}
        own = table.get(sc["type"] + ":" + str(P.get("stage", "")), table.get(sc["type"], []))
        at_ = P.get("at", [])
        if i > 0 and not (own and isinstance(own[0][0], (int, float)) and own[0][0] < .1):
            ev.append((sc["t0"], "swish", None))
        if i == 0:
            continue   # the hook scene is already finished on frame 0
        run = {}
        for e in own:
            try:
                at = sc["t0"] + beat(e[0], at_)
            except (IndexError, AttributeError):
                print(f"  skip {e}: scene {sc['type']} has no beat for it"); continue
            if e[1] in ("right", "pop"):
                run[e[1]] = run.get(e[1], -1) + 1
            if at < sc["t1"]:
                dur = e[2] if len(e) > 2 else None
                if dur == "end":
                    dur = max(.3, sc["t1"] + .3 - at)   # beds run until the scene has faded out
                elif isinstance(dur, str):
                    dur = max(.3, sc["t0"] + beat(dur, at_) - at)   # "@3" = until beat 3
                ev.append((at, e[1], run[e[1]] if e[1] in ("right", "pop") else dur))
    ev.append((cfg["brandT"], "chord", None))
    ev.sort(key=lambda e: e[0]); kept = []
    for e in ev:
        last = [k for k in kept if k[1] not in BEDS]
        if e[1] in BEDS or e[1] in ("tone", "chord", "stamp") or not last or e[0] - last[-1][0] >= min_gap:
            kept.append(e)
    return kept


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("reel"); ap.add_argument("--level", default="present", choices=["subtle", "present", "off"])
    ap.add_argument("--kit-out"); o = ap.parse_args(); d = o.reel.rstrip("/")
    if o.kit_out:
        import soundfile as sf
        os.makedirs(o.kit_out, exist_ok=True)
        for k, f in KIT.items():
            x = f(); sf.write(os.path.join(o.kit_out, k + ".wav"), (x / np.abs(x).max() * 10 ** (PEAK[k] / 20)).astype(np.float32), SR)
    cfg = json.load(open(os.path.join(d, "config.json"))); voice = os.path.join(d, "audio_voice.mp3"); out = os.path.join(d, "audio_mixed.mp3")
    if o.level == "off":
        subprocess.run(["cp", voice, out], check=True); print("sfx off"); return
    table = json.load(open(os.path.join(HERE, "assets/events.json")))
    ev = events(cfg, table); n = int((cfg["total"] + 3) * SR); trk = np.zeros(n)
    for at, kind, dur in ev:
        s = KIT[kind](dur) if dur is not None else KIT[kind](); s = s / np.abs(s).max() * 10 ** ((PEAK[kind] + LEVEL[o.level]) / 20); i = int(at * SR)
        trk[i:i + len(s)] += s[: n - i]
    trk = trk[: int(cfg["total"] * SR)]
    tmp = tempfile.mktemp(suffix=".wav")
    import soundfile as sf
    sf.write(tmp, trk.astype(np.float32), SR)
    duck = "sidechaincompress=threshold=0.12:ratio=2:attack=10:release=200"
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", voice, "-i", tmp, "-filter_complex",
                    f"[0:a]aresample={SR},asplit[v][sc];[1:a][sc]{duck},asplit[fx][fxo];[v][fx]amix=inputs=2:normalize=0:duration=first,alimiter=limit=0.89[mix]",
                    "-map", "[mix]", "-ar", str(SR), "-b:a", "192k", out, "-map", "[fxo]", os.path.join(d, "audio_fx.wav")], check=True)
    os.remove(tmp)
    print(f"sfx {o.level}: {len(ev)} sounds ->", out, " ".join(f"{k}@{t:.1f}" for t, k, _ in ev))


if __name__ == "__main__":
    main()
