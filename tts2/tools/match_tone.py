"""Match a voice's tonal balance to a reference (e.g. Adam) using earshot's band measurements.

    tools/earshot/.venv/bin/python tts2/tools/match_tone.py REF.wav IN.wav OUT.wav
Iterates a 5-band EQ (sub, low-mid body, mid, presence, air) plus cleanup until earshot's
band levels are within ~1 dB of the reference. Prints the final ffmpeg chain to reuse.
"""
import json, subprocess, sys
E = "/Users/sanyampathak/Documents/dmyor-videos/tools/earshot/.venv/bin/earshot"
ref, src, out = sys.argv[1:4]
def bands(f):
    r = json.loads(subprocess.run([E, "measure", f, "--json"], capture_output=True, text=True).stdout)
    m = r.get("measurements", r); b = m.get("bands_db") or m.get("bands")
    return b, m
rb, rm = bands(ref)
print("reference bands", rb)
g = {"sub": 0.0, "lowmid": 0.0, "mid": 0.0, "presence": 0.0, "air": 0.0}
for it in range(6):
    chain = (f"highpass=f=60,afftdn=nr=10:nf=-55,"
             f"equalizer=f=60:t=q:w=1:g={g['sub']:.1f},equalizer=f=400:t=q:w=1.2:g={g['lowmid']:.1f},"
             f"equalizer=f=1500:t=q:w=1.2:g={g['mid']:.1f},equalizer=f=4000:t=q:w=1:g={g['presence']:.1f},"
             f"highshelf=f=8000:g={g['air']:.1f},aexciter=amount=1.5:drive=6:blend=0:freq=6000:ceil=16000,"
             f"acompressor=threshold=-20dB:ratio=2.5:attack=10:release=150:makeup=1.5,loudnorm=I=-18:TP=-2")
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", src, "-af", chain, "-ar", "44100", out], check=True)
    b, m = bands(out)
    # compare shapes relative to the 'low' band so loudness differences don't matter
    d = {k: (rb[k] - rb["low"]) - (b[k] - b["low"]) for k in g}
    print(f"iter {it}: diff", {k: round(v, 1) for k, v in d.items()}, "brightness", m.get("brightness_hz"))
    if all(abs(v) < 1.0 for v in d.values()): break
    for k in g: g[k] = max(-12, min(12, g[k] + 0.8 * d[k]))
print("CHAIN", chain)
