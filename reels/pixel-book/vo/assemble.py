# Place each narration clip (sped up by TEMPO) at its mapped film time. Writes audio.mp3.
import json, os, sys, subprocess, numpy as np, soundfile as sf
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))); sys.path.insert(0, ".")
from timemap import t2u, TEMPO, TOTAL
START = json.load(open("vo_times.json")); SR = 44100; out = np.zeros(int((TOTAL + 1) * SR)); prev = 0
for k in sorted(START, key=lambda k: START[k][0]):
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", f"vo/{k}.wav", "-af", f"atempo={TEMPO}", "-ar", str(SR), "-ac", "1", f"vo/_{k}.wav"], check=True)
    x, _ = sf.read(f"vo/_{k}.wav"); u = t2u(START[k][0]); i = int(u * SR)
    assert u >= prev - .02, (k, u, prev); out[i:i + len(x)] += x; prev = u + len(x) / SR
sf.write("audio.wav", out[: int(TOTAL * SR)].astype(np.float32), SR)
subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", "audio.wav", "-b:a", "192k", "audio.mp3"], check=True); print("vo ok", TOTAL)
