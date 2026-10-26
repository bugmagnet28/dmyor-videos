# Place each narration clip at its start time (pauses are deliberate). Writes audio.mp3 + vo_times.json.
import json, os, numpy as np, soundfile as sf, subprocess
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
START = {"L1":1.0,"L2":7.4,"L3":13.0,"L4":16.6,"L5":22.0,"L6":27.6,"L7":32.6,"L8":36.2,"L9":40.4,"L10":47.0,"L11":51.4,"L12":55.9,"L13":61.8,
         "L14":67.0,"L15":70.3,"L16":74.3,"L17":80.8,"L18":84.9,"L19":91.4,"L20":97.2,"L21":100.8,"L22":106.2,"L23":112.6,"L24":118.4,"L25":124.3,
         "L26":132.0,"L27":135.9,"L28":139.7,"L29":146.8}
TOTAL = 158.5; SR = 44100; out = np.zeros(int(TOTAL * SR)); times = {}; prev_end = 0
for k in sorted(START, key=lambda k: START[k]):
    x, sr = sf.read(f"vo/{k}.wav"); x = x if x.ndim == 1 else x.mean(1)
    assert sr == SR, sr
    i = int(START[k] * SR); out[i:i + len(x)] += x; e = START[k] + len(x) / SR
    assert START[k] >= prev_end - 0.01, (k, START[k], prev_end); prev_end = e
    times[k] = [START[k], round(e, 3)]
sf.write("audio.wav", out.astype(np.float32), SR)
subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", "audio.wav", "-ar", "44100", "-b:a", "192k", "audio.mp3"], check=True)
json.dump(times, open("vo_times.json", "w"), indent=0); print(times["L29"], "ok")
