"""Local narration with Kokoro (open model, Apache-2.0, runs offline).

    tts/.venv/bin/python tts/say.py "text" out.mp3 [--voice af_heart] [--speed 1.0]
    tts/.venv/bin/python tts/say.py @script.txt out.mp3        # read text from a file

Writes a 44.1 kHz mp3 normalised to -16 LUFS, ready for the reel pipeline (reel.py audio / align.py).
"""
import argparse, os, subprocess, tempfile
import soundfile as sf
from kokoro_onnx import Kokoro

HERE = os.path.dirname(os.path.abspath(__file__))
ap = argparse.ArgumentParser()
ap.add_argument("text"); ap.add_argument("out")
ap.add_argument("--voice", default="af_heart"); ap.add_argument("--speed", type=float, default=1.0)
a = ap.parse_args()
text = open(a.text[1:]).read() if a.text.startswith("@") else a.text
k = Kokoro(os.path.join(HERE, "models/kokoro-v1.0.onnx"), os.path.join(HERE, "models/voices-v1.0.bin"))
samples, sr = k.create(text, voice=a.voice, speed=a.speed, lang="en-us")
tmp = tempfile.mktemp(suffix=".wav"); sf.write(tmp, samples, sr)
subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", tmp, "-af", "loudnorm=I=-16:TP=-1.5", "-ar", "44100", "-b:a", "192k", a.out], check=True)
os.remove(tmp)
print(f"{a.out}  {len(samples)/sr:.2f}s  voice={a.voice} speed={a.speed}")
