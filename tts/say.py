"""Local narration with Kokoro (open model, Apache-2.0, runs offline).

    tts/.venv/bin/python tts/say.py "text" out.mp3 [--voice am_eric] [--speed 0.9]
    tts/.venv/bin/python tts/say.py @script.txt out.mp3        # read text from a file

Speaks like a person, not a stream: every sentence is generated on its own and joined
with silence, so the voice breathes.
  - between sentences:        --gap seconds (default 0.42)
  - "||" in the script:       a longer, deliberate pause (--beat, default 0.8)
  - a short lead-in/out of silence at the ends
Writes a 44.1 kHz mp3 normalised to -16 LUFS, ready for the reel pipeline.
"""
import argparse, os, re, subprocess, tempfile
import numpy as np
import soundfile as sf
from kokoro_onnx import Kokoro

HERE = os.path.dirname(os.path.abspath(__file__))
ap = argparse.ArgumentParser()
ap.add_argument("text"); ap.add_argument("out")
ap.add_argument("--voice", default="am_eric"); ap.add_argument("--speed", type=float, default=0.9)
ap.add_argument("--gap", type=float, default=0.42); ap.add_argument("--beat", type=float, default=0.8)
a = ap.parse_args()
text = open(a.text[1:]).read() if a.text.startswith("@") else a.text
k = Kokoro(os.path.join(HERE, "models/kokoro-v1.0.onnx"), os.path.join(HERE, "models/voices-v1.0.bin"))

parts, sr, n = [], 24000, 0
blocks = [b.strip() for b in text.split("||") if b.strip()]
for bi, block in enumerate(blocks):
    sentences = [s.strip() for s in re.split(r"(?<=[.!?])\s+", block) if s.strip()]
    for si, s in enumerate(sentences):
        samples, sr = k.create(s, voice=a.voice, speed=a.speed, lang="en-us")
        # trim the model's own leading/trailing near-silence so the gaps are exactly what we set
        idx = np.where(np.abs(samples) > 0.01)[0]
        if len(idx):
            samples = samples[max(0, idx[0] - int(0.02 * sr)): idx[-1] + int(0.06 * sr)]
        parts.append(samples.astype(np.float32)); n += 1
        last = si == len(sentences) - 1
        if not (last and bi == len(blocks) - 1):
            parts.append(np.zeros(int((a.beat if last else a.gap) * sr), dtype=np.float32))
audio = np.concatenate([np.zeros(int(0.12 * sr), dtype=np.float32)] + parts + [np.zeros(int(0.3 * sr), dtype=np.float32)])
tmp = tempfile.mktemp(suffix=".wav"); sf.write(tmp, audio, sr)
subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", tmp, "-af", "loudnorm=I=-16:TP=-1.5", "-ar", "44100", "-b:a", "192k", a.out], check=True)
os.remove(tmp)
print(f"{a.out}  {len(audio)/sr:.2f}s  voice={a.voice} speed={a.speed} sentences={n}")
