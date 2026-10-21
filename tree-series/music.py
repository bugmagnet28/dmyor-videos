"""Original soundtrack for a tree-series reel, synthesized from scratch (no samples,
nothing to license). Reads the reel's config.json so musical accents land on the
same beats as the visuals: a bell on every card that appears, a lift when the
tree blooms, a resolved chord under the brand card.

    python3 tree-series/music.py reels/<slug>      -> reels/<slug>/audio.mp3
"""
import json, os, subprocess, sys, wave
import numpy as np

SR = 44100


def midi(n):
    return 440.0 * 2 ** ((n - 69) / 12)


def env(n, a, d, s=0.0):
    """attack seconds, exponential decay time constant, sustain floor"""
    t = np.arange(n) / SR
    e = np.minimum(1, t / max(a, 1e-4)) * (s + (1 - s) * np.exp(-t / d))
    return e


def lowpass(x, cutoff):
    a = np.exp(-2 * np.pi * cutoff / SR)
    y = np.empty_like(x)
    acc = 0.0
    # vectorised one-pole via cumulative trick is unstable; chunked loop is fast enough
    for i in range(len(x)):
        acc = (1 - a) * x[i] + a * acc
        y[i] = acc
    return y


def saw(f, n, phase=0.0):
    t = np.arange(n) / SR
    return 2 * ((f * t + phase) % 1.0) - 1


def pad_chord(notes, dur):
    n = int(dur * SR)
    out = np.zeros(n)
    for m in notes:
        for det in (-0.08, 0.0, 0.07):
            out += saw(midi(m + det), n, np.random.rand())
    out /= len(notes) * 3
    t = np.arange(n) / SR
    shape = np.minimum(1, t / 0.35) * np.minimum(1, (dur - t) / 0.4).clip(0, 1)
    return out * shape


def pluck(m, dur=0.9, bright=1.0):
    n = int(dur * SR)
    t = np.arange(n) / SR
    f = midi(m)
    y = np.zeros(n)
    for h, amp in ((1, 1.0), (2, 0.45 * bright), (3, 0.22 * bright), (4, 0.1 * bright)):
        y += amp * np.sin(2 * np.pi * f * h * t) * np.exp(-t * (3.2 + h * 1.6))
    return y * np.minimum(1, t / 0.004)


def bell(m, dur=2.2):
    n = int(dur * SR)
    t = np.arange(n) / SR
    f = midi(m)
    y = (np.sin(2 * np.pi * f * t) * np.exp(-t * 1.8)
         + 0.5 * np.sin(2 * np.pi * f * 2.76 * t) * np.exp(-t * 3.5)
         + 0.25 * np.sin(2 * np.pi * f * 5.4 * t) * np.exp(-t * 6))
    return y * np.minimum(1, t / 0.002)


def kick(dur=0.45):
    n = int(dur * SR)
    t = np.arange(n) / SR
    f = 45 + 75 * np.exp(-t * 22)
    ph = 2 * np.pi * np.cumsum(f) / SR
    return np.sin(ph) * np.exp(-t * 7.5)


def hat(dur=0.08):
    n = int(dur * SR)
    x = np.random.randn(n)
    x = np.diff(np.concatenate([[0], x]))  # crude highpass
    return x * np.exp(-np.arange(n) / SR * 55) * 0.35


def shaker(dur=0.12):
    n = int(dur * SR)
    x = np.random.randn(n)
    t = np.arange(n) / SR
    return x * np.sin(np.pi * t / dur) * 0.12


def add(buf, sig, t, g):
    i = int(t * SR)
    if i >= len(buf):
        return
    j = min(len(buf), i + len(sig))
    buf[i:j] += sig[: j - i] * g


def main(reel):
    cfg = json.load(open(os.path.join(reel, "config.json")))
    np.random.seed(cfg.get("seed", 7))
    bpm = cfg["bpm"]
    B = 60 / bpm
    T = cfg["total"]
    E = cfg["events"]
    M = cfg["music"]
    root = M["root"]                 # midi note of the key centre
    prog = M["progression"]          # list of chords, semitone offsets from root
    n = int((T + 1.5) * SR)
    pad = np.zeros(n); keys = np.zeros(n); drums = np.zeros(n); bells = np.zeros(n); bass = np.zeros(n)

    bar = 4 * B
    nbars = int(np.ceil(T / bar)) + 1
    chord_at = lambda t: prog[int(t / bar) % len(prog)]

    # pad: one chord per bar, whole track
    for b in range(nbars):
        ch = prog[b % len(prog)]
        notes = [root + 12 + c for c in ch]
        add(pad, pad_chord(notes, bar + 0.3), b * bar, 1.0)
        add(bass, pluck(root - 12 + ch[0], bar, 0.2), b * bar, 0.9)

    # arpeggio: 8ths, enters with the vision, thins out in the focus, full in the bloom
    step = B / 2
    k = 0
    t = E["vision"] * B
    while t < E["brand"] * B:
        ch = chord_at(t)
        seq = [ch[0], ch[1], ch[2], ch[1] + 12, ch[2], ch[1]]
        note = root + 24 + seq[k % len(seq)]
        focus = E["focus"] * B <= t < E["grow"] * B
        g = 0.22 if not focus else (0.14 if k % 2 == 0 else 0.0)
        if g:
            add(keys, pluck(note, 0.8, 0.9), t, g)
        k += 1
        t += step

    # drums: soft kick on 1 and 3 after the trunk grows, shaker on 8ths, hats on offbeats in the bloom
    t = E["trunk"] * B
    i = 0
    while t < E["brand"] * B:
        focus = E["focus"] * B <= t < E["grow"] * B
        if i % 4 == 0 and not focus:
            add(drums, kick(), t, 0.55)
        if i % 4 == 2 and not focus:
            add(drums, kick(), t, 0.35)
        add(drums, shaker(), t + B / 2, 0.5 if not focus else 0.25)
        if t >= E["grow"] * B:
            add(drums, hat(), t + B / 2, 0.6)
        i += 1
        t += B

    # bells on every card, pitched up the chord so the tree "climbs"
    ladder = [0, 4, 7, 12, 16, 19, 24]
    cues = [E["vision"]] + E["milestones"] + E["actions"]
    for idx, bt in enumerate(cues):
        ch = chord_at(bt * B)
        m = root + 24 + ch[0] + ladder[min(idx, len(ladder) - 1)] % 12 + 12 * (ladder[min(idx, len(ladder) - 1)] // 12)
        add(bells, bell(m), bt * B, 0.32)
    # "done": a bright two-note chime
    d = E["done"] * B
    add(bells, bell(root + 36 + 7), d, 0.36)
    add(bells, bell(root + 36 + 12), d + B / 2, 0.36)
    # bloom: rising glissando of bells
    g0 = E["grow"] * B
    for j, off in enumerate([0, 4, 7, 12, 16, 19]):
        add(bells, bell(root + 24 + off, 1.6), g0 + j * B / 4, 0.18)
    # brand: final chord rings out
    bt = E["brand"] * B
    for off in (0, 7, 12, 16):
        add(bells, bell(root + 24 + off, 3.0), bt, 0.16)

    pad = lowpass(pad, 1400) * 0.55
    mix = pad + keys + drums + bells * 0.9 + bass * 0.45
    # fade in from frame 0 (soft, but not silent) and out at the end
    tt = np.arange(n) / SR
    mix *= np.minimum(1, 0.35 + tt / 0.8)
    mix *= np.clip((T + 0.2 - tt) / 1.2, 0, 1)
    mix = mix[: int(T * SR)]
    mix = np.tanh(mix * 1.4) / np.tanh(1.4)
    mix /= np.max(np.abs(mix)) + 1e-9
    mix *= 0.89
    stereo = np.stack([mix, np.roll(mix, 220) * 0.98], axis=1)
    pcm = (stereo * 32767).astype(np.int16)
    wav_path = os.path.join(reel, "audio.wav")
    with wave.open(wav_path, "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())
    mp3 = os.path.join(reel, "audio.mp3")
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", wav_path, "-af", "loudnorm=I=-14:TP=-1.5:LRA=9",
                    "-ar", "44100", "-b:a", "192k", mp3], check=True)
    os.remove(wav_path)
    print("wrote", mp3, f"{T:.1f}s")


if __name__ == "__main__":
    main(sys.argv[1])
