"""Subtle, synthesized sound design for illustrated reels (no samples, no licensing).

    python3 sfx.py <reel_dir> --level subtle|present [--kit-out DIR]

Reads <reel_dir>/config.json (scene types + t0/t1, brandT, total) and ../assets/events.json (sound moments per
scene type), renders an effects track and mixes it under <reel_dir>/audio_voice.mp3 (voice ducks the effects)
into <reel_dir>/audio_mixed.mp3. Scene changes get a soft swish, except the first scene (already on screen at frame 0)
and scenes that open with their own sound; the brand card gets a soft chord.
"""
import argparse, json, os, subprocess, tempfile
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


KIT = {"tick": tick, "tap": tap, "swish": swish, "ratchet": ratchet, "tone": tone, "chord": chord}
PEAK = {"tick": -19, "tap": -19, "swish": -25, "ratchet": -23, "tone": -24, "chord": -19}   # dBFS peak per sound at "present" (voice peaks ~-1.5)
LEVEL = {"present": 0, "subtle": -6}


def events(cfg, table, min_gap=.28):
    ev = []
    for i, sc in enumerate(cfg["scenes"]):
        own = table.get(sc["type"], [])
        if i > 0 and not (own and own[0][0] < .1):
            ev.append((sc["t0"], "swish", None))
        if i == 0:
            continue   # the hook scene is already finished on frame 0
        for e in own:
            at = sc["t0"] + e[0]
            if at < sc["t1"]:
                ev.append((at, e[1], e[2] if len(e) > 2 else None))
    ev.append((cfg["brandT"], "chord", None))
    ev.sort(); kept = []
    for e in ev:
        if not kept or e[0] - kept[-1][0] >= min_gap or e[1] in ("tone", "chord"):
            kept.append(e)
    return kept


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("reel"); ap.add_argument("--level", default="subtle", choices=["subtle", "present", "off"])
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
        s = KIT[kind](dur) if dur else KIT[kind](); s = s / np.abs(s).max() * 10 ** ((PEAK[kind] + LEVEL[o.level]) / 20); i = int(at * SR)
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
