"""Shared sound layer for pixel-series episodes: object sounds + quiet CC0 room tone under the Kokoro voice. No music
(owner 2026-11-06: music is added in the Instagram app). An episode's make_audio.py does:
    from sfxmix import Mix; m = Mix("reels/<ep>"); m.A(m.K("stamp"), m.LN["S1", 0], .3); ...; m.write()"""
import importlib.util, json, os, subprocess, sys
import numpy as np, soundfile as sf
ROOT = os.getcwd(); SR = 44100
def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m
class Mix:
    def __init__(self, ep):
        self.D = os.path.join(ROOT, ep); TL = json.load(open(os.path.join(self.D, "timeline.json")))
        self.TOTAL, self.SC = TL["total"], TL["scenes"]; self.LN = {(l[0], l[1]): l[2] for l in TL["lines"]}; self.LE = {(l[0], l[1]): l[3] for l in TL["lines"]}
        argv = sys.argv; sys.argv = ["kit", self.D]
        self.kit = _load("kit", os.path.join(ROOT, ".claude/skills/animated-illustration-explainer/scripts/sfx.py"))
        self.syn = _load("syn", os.path.join(ROOT, ".claude/skills/cinematic-motion/scripts/make_film.py")); sys.argv = argv
        self.fx = np.zeros(int((self.TOTAL + 3) * SR))
    def A(self, x, at, g): self.syn.add(self.fx, x, at, g)
    def K(self, name, *a): f = getattr(self.kit, name)(*a); return f / (np.abs(f).max() + 1e-9)
    def tt(self, d): return np.arange(int(d * SR)) / SR
    def sq(self, m, d, duty=.5):   # tiny chiptune blip for UI-ish pixel moments
        t = self.tt(d); ph = 440 * 2 ** ((m - 69) / 12) * t; e = np.ones(len(t)); r = int(min(.05, d * .5) * SR); e[-r:] = np.linspace(1, 0, r); return np.where((ph % 1) < duty, 1.0, -1.0) * e
    def write(self, bed_db=-27):
        T = self.TOTAL; fx = self.fx[: int(T * SR)]; ref = np.percentile(np.abs(fx[np.abs(fx) > 1e-4]), 99.5) + 1e-9
        sf.write(os.path.join(self.D, "sfx.wav"), (np.tanh(fx / ref * 1.1) * .62).astype(np.float32), SR)
        bed = os.path.join(ROOT, "studio/sfx-library/real/ambience-room.wav")
        fc = (f"[0:a]apad,atrim=0:{T},loudnorm=I=-16:TP=-2[v];[1:a]volume=0.75[f];[2:a]atrim=0:{T},volume={10 ** (bed_db / 20) * 3:.3f},afade=t=in:d=0.4,afade=t=out:st={T - 1.5}:d=1.5[b];"
              f"[v][f][b]amix=inputs=3:normalize=0:duration=first,atrim=0:{T},alimiter=limit=0.89,loudnorm=I=-14:TP=-1.5")
        subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", os.path.join(self.D, "audio.mp3"), "-i", os.path.join(self.D, "sfx.wav"), "-stream_loop", "-1", "-i", bed,
                        "-filter_complex", fc, "-ar", "44100", "-b:a", "192k", os.path.join(self.D, "audio_mixed.mp3")], check=True)
        print("audio ok", T)
