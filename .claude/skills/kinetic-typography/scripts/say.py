"""Local narration with Kokoro (open model, Apache-2.0, runs offline).

    tts/.venv/bin/python <skill>/scripts/say.py "text" out.mp3 [--voice am_eric] [--speed 1.0]
    tts/.venv/bin/python <skill>/scripts/say.py @script.txt out.mp3     # read text from a file
(run from the project root; models are found in ./tts/models or $KOKORO_MODELS)

Aims for human delivery, not a word stream and not a list of fragments:
  - "||" separates THOUGHTS. Each thought (one or more sentences) is generated in one pass,
    so intonation flows across its commas and sentences like a person's would.
  - Pauses happen only between thoughts, and they vary (--gap-min..--gap-max seconds,
    a little longer after a question), seeded so a rebuild sounds the same.
  - Pauses are filled with very faint room tone instead of digital silence.
Writes a 44.1 kHz mp3 normalised to -16 LUFS, ready for the reel pipeline.
"""
import argparse, os, random, subprocess, tempfile
import numpy as np
import soundfile as sf
from kokoro_onnx import Kokoro

HERE = os.path.dirname(os.path.abspath(__file__))
ap = argparse.ArgumentParser()
ap.add_argument("text"); ap.add_argument("out")
ap.add_argument("--voice", default="am_eric"); ap.add_argument("--speed", type=float, default=1.0)
ap.add_argument("--gap-min", type=float, default=0.30); ap.add_argument("--gap-max", type=float, default=0.55)
ap.add_argument("--seed", type=int, default=7)
a = ap.parse_args()
text = open(a.text[1:]).read() if a.text.startswith("@") else a.text
def _models():
    if os.environ.get("KOKORO_MODELS"):
        return os.environ["KOKORO_MODELS"]
    d = os.getcwd()
    while d != "/":
        if os.path.exists(os.path.join(d, "tts/models/kokoro-v1.0.onnx")):
            return os.path.join(d, "tts/models")
        d = os.path.dirname(d)
    raise SystemExit("Kokoro models not found: run scripts/setup_tts.sh from the project root")
M = _models()
k = Kokoro(os.path.join(M, "kokoro-v1.0.onnx"), os.path.join(M, "voices-v1.0.bin"))
rng = random.Random(a.seed)
nrng = np.random.default_rng(a.seed)


def room(sec, sr, n=None):
    """faint pinkish room tone (~ -60 dB) so pauses are not dead digital silence"""
    n = int(sec * sr) if n is None else n
    w = nrng.standard_normal(n).astype(np.float32)
    w = np.convolve(w, np.ones(24) / 24, mode="same")  # soften the hiss
    return w * 0.0018


sr = 24000
thoughts = [t.strip() for t in text.split("||") if t.strip()]
parts = []
for i, th in enumerate(thoughts):
    samples, sr = k.create(th, voice=a.voice, speed=a.speed, lang="en-us")
    idx = np.where(np.abs(samples) > 0.01)[0]
    if len(idx):
        samples = samples[max(0, idx[0] - int(0.03 * sr)): idx[-1] + int(0.08 * sr)]
    # gentle 15 ms fades so cuts never click
    f = int(0.015 * sr)
    samples = samples.astype(np.float32)
    samples[:f] *= np.linspace(0, 1, f); samples[-f:] *= np.linspace(1, 0, f)
    parts.append(samples + room(0, sr, n=len(samples)))
    if i < len(thoughts) - 1:
        g = rng.uniform(a.gap_min, a.gap_max) + (0.12 if th.endswith("?") else 0.0)
        parts.append(room(g, sr))
audio = np.concatenate([room(0.15, sr)] + parts + [room(0.35, sr)])
tmp = tempfile.mktemp(suffix=".wav"); sf.write(tmp, audio, sr)
subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", tmp, "-af", "loudnorm=I=-16:TP=-1.5", "-ar", "44100", "-b:a", "192k", a.out], check=True)
os.remove(tmp)
print(f"{a.out}  {len(audio)/sr:.2f}s  voice={a.voice} speed={a.speed} thoughts={len(thoughts)}")
