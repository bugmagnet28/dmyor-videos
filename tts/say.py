"""Local narration with Kokoro (open model, Apache-2.0, runs offline), tuned to sound more human.

    tts/.venv/bin/python tts/say.py "text" out.mp3 [options]
    tts/.venv/bin/python tts/say.py @script.txt out.mp3

Delivery
  "||" separates THOUGHTS. Each thought is generated in one pass (natural intonation across its commas
  and sentences); pauses only between thoughts, varied (--gap-min..--gap-max), a bit longer after "?".
  --clause-pause / --sentence-pause   pauses at commas / full stops inside a thought (Kokoro default 0.10 / 0.25)
Humanising (all optional, see --preset)
  --blend "am_eric:0.7,am_michael:0.3"   mix voices: fuller, less "stock" timbre (overrides --voice)
  --vary 0.04                            each thought at a slightly different pace (+/- 4%), not a metronome
  --land 0.94                            the last thought (and questions) a touch slower, to land the point
  --fx                                   "recorded in a room": warmth EQ, light compression, subtle early reflections
  --breaths                              faint synthetic inhale before some thoughts
  --stages                               tone changes by stage: [hook] [body] [turn] [land] [outro] tags per
                                         thought (auto if untagged) + a conclusive, faded ending
  --preset human                         = --blend am_eric:0.7,am_michael:0.3 --vary 0.04 --land 0.94 --fx
                                           --clause-pause 0.16 --sentence-pause 0.32
Writes a 44.1 kHz mp3 normalised to -16 LUFS. Run from the project root (models in ./tts/models or $KOKORO_MODELS).
"""
import argparse, os, random, subprocess, tempfile
import numpy as np
import soundfile as sf
from kokoro_onnx import Kokoro

ap = argparse.ArgumentParser()
ap.add_argument("text"); ap.add_argument("out")
ap.add_argument("--voice", default="am_eric"); ap.add_argument("--speed", type=float, default=1.0)
ap.add_argument("--gap-min", type=float, default=0.30); ap.add_argument("--gap-max", type=float, default=0.55)
ap.add_argument("--clause-pause", type=float, default=0.10); ap.add_argument("--sentence-pause", type=float, default=0.25)
ap.add_argument("--blend"); ap.add_argument("--vary", type=float, default=0.0); ap.add_argument("--land", type=float, default=1.0)
ap.add_argument("--fx", action="store_true"); ap.add_argument("--breaths", action="store_true")
ap.add_argument("--preset", choices=["plain", "human"], default="plain")
ap.add_argument("--stages", action="store_true", help="tone changes by stage (hook/body/turn/land/outro), conclusive ending")
ap.add_argument("--seed", type=int, default=7)
a = ap.parse_args()
if a.preset == "human":
    a.blend = a.blend or "am_eric:0.7,am_michael:0.3"; a.vary = a.vary or 0.04; a.land = 0.94 if a.land == 1.0 else a.land
    a.fx = True; a.clause_pause = max(a.clause_pause, 0.16); a.sentence_pause = max(a.sentence_pause, 0.32)


def _models():
    if os.environ.get("KOKORO_MODELS"):
        return os.environ["KOKORO_MODELS"]
    d = os.getcwd()
    while d != "/":
        if os.path.exists(os.path.join(d, "tts/models/kokoro-v1.0.onnx")):
            return os.path.join(d, "tts/models")
        d = os.path.dirname(d)
    here = os.path.dirname(os.path.abspath(__file__))
    if os.path.exists(os.path.join(here, "models/kokoro-v1.0.onnx")):
        return os.path.join(here, "models")
    raise SystemExit("Kokoro models not found: run setup_tts.sh from the project root")


M = _models()
k = Kokoro(os.path.join(M, "kokoro-v1.0.onnx"), os.path.join(M, "voices-v1.0.bin"))
voice = a.voice
if a.blend:
    parts = [p.split(":") for p in a.blend.split(",")]
    tot = sum(float(w) for _, w in parts)
    voice = sum(k.get_voice_style(v) * (float(w) / tot) for v, w in parts).astype(np.float32)
text = open(a.text[1:]).read() if a.text.startswith("@") else a.text
rng = random.Random(a.seed); nrng = np.random.default_rng(a.seed)
sr = 24000


def room(n):
    w = nrng.standard_normal(n).astype(np.float32)
    return np.convolve(w, np.ones(24) / 24, mode="same") * 0.0018


def breath(sr):
    """soft inhale: band-limited noise, slow attack, quick release (~0.32 s)"""
    n = int(0.32 * sr); t = np.linspace(0, 1, n)
    w = nrng.standard_normal(n).astype(np.float32)
    w = np.convolve(w, np.ones(6) / 6, mode="same") - np.convolve(w, np.ones(60) / 60, mode="same")  # crude band-pass
    env = np.sin(np.pi * np.clip(t * 1.25, 0, 1)) ** 2
    return (w * env * 0.035).astype(np.float32)


# Stage-aware delivery: a thought can start with [hook] [body] [turn] [land] [outro]; untagged thoughts are
# assigned automatically (first = hook, last two = outro, the one before = land, the rest = body).
# speed multiplier, pitch shift (fraction), extra pause before, extra pause after
STAGE = {"hook": (1.03, 0.015, 0.0, 0.10), "body": (1.0, 0.0, 0.0, 0.0), "turn": (0.97, -0.01, 0.15, 0.0),
         "land": (0.93, -0.02, 0.25, 0.25), "outro": (0.94, -0.03, 0.20, 0.0)}


def pitch(samples, sr, shift):
    """shift pitch by a fraction (e.g. -0.02) without changing duration (asetrate + atempo)"""
    if abs(shift) < 1e-4:
        return samples
    i, o = tempfile.mktemp(suffix=".wav"), tempfile.mktemp(suffix=".wav")
    sf.write(i, samples, sr); f = 1 + shift
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", i, "-af", f"asetrate={sr * f:.0f},aresample={sr},atempo={1 / f:.5f}", o], check=True)
    y, _ = sf.read(o, dtype="float32"); os.remove(i); os.remove(o)
    return y


raw = [t.strip() for t in text.split("||") if t.strip()]
thoughts, stages = [], []
for i, t in enumerate(raw):
    tag = None
    if t.startswith("[") and "]" in t[:8]:
        tag, t = t[1:t.index("]")].strip(), t[t.index("]") + 1:].strip()
    if not tag and a.stages:
        tag = "hook" if i == 0 else "outro" if i >= len(raw) - 2 else "land" if i == len(raw) - 3 else "body"
    thoughts.append(t); stages.append(tag or "body")
out = []
for i, th in enumerate(thoughts):
    st_sp, st_pitch, pre, post = STAGE.get(stages[i], STAGE["body"]) if a.stages else (1.0, 0.0, 0.0, 0.0)
    sp = a.speed * st_sp * (1 + rng.uniform(-a.vary, a.vary))
    if not a.stages and (i == len(thoughts) - 1 or th.rstrip().endswith("?")):
        sp *= a.land
    if pre and out:
        out.append(room(int(pre * sr)))
    samples, sr = k.create(th, voice=voice, speed=sp, lang="en-us",
                           clause_pause=a.clause_pause, sentence_pause=a.sentence_pause)
    last = i == len(thoughts) - 1
    idx = np.where(np.abs(samples) > 0.006)[0]
    if len(idx):  # keep the natural decay of the final word (longer on the very last thought)
        samples = samples[max(0, idx[0] - int(0.03 * sr)): idx[-1] + int((0.35 if last else 0.10) * sr)]
    samples = pitch(samples.astype(np.float32), sr, st_pitch)
    f = int(0.015 * sr); samples[:f] *= np.linspace(0, 1, f)
    fo = int((0.30 if last else 0.015) * sr); samples[-fo:] *= np.linspace(1, 0, fo) ** (2 if last else 1)
    if post:
        samples = np.concatenate([samples, np.zeros(int(post * sr), dtype=np.float32)])
    if a.breaths and i > 0 and (i % 2 == 1 or len(th.split()) > 9):
        out[-1] = out[-1][: max(0, len(out[-1]) - int(0.34 * sr))]  # breath sits inside the pause
        out.append(room(int(0.02 * sr)) + 0); out.append(breath(sr) + room(int(0.32 * sr)))
    out.append(samples + room(len(samples)))
    if i < len(thoughts) - 1:
        g = rng.uniform(a.gap_min, a.gap_max) + (0.12 if th.endswith("?") else 0.0)
        out.append(room(int(g * sr)))
audio = np.concatenate([room(int(0.15 * sr))] + out + [room(int((0.8 if a.stages else 0.35) * sr))])
tmp = tempfile.mktemp(suffix=".wav"); sf.write(tmp, audio, sr)
chain = "loudnorm=I=-16:TP=-1.5"
if a.fx:
    chain = ("highpass=f=70,equalizer=f=180:t=q:w=1.1:g=2.2,equalizer=f=3200:t=q:w=1.4:g=-1.6,"
             "equalizer=f=9000:t=q:w=1.0:g=1.2,acompressor=threshold=-20dB:ratio=2.4:attack=12:release=180:makeup=2,"
             "aecho=0.85:0.45:17|29|43:0.10|0.07|0.045," + chain)
subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", tmp, "-af", chain, "-ar", "44100", "-b:a", "192k", a.out], check=True)
os.remove(tmp)
print(f"{a.out}  {len(audio)/sr:.2f}s  voice={a.blend or a.voice} preset={a.preset} fx={a.fx} breaths={a.breaths} stages={' '.join(stages) if a.stages else 'off'}")
