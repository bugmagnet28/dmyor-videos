"""Shared sound layer for pixel-series episodes: object sounds + quiet CC0 room tone under the Kokoro voice. No music
(music: optional bed from studio/music-library, owner 2026-11-15). An episode's make_audio.py does:
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
    def music_track(self, mood):
        """Pick a library track for this reel: same reel always gets the same track."""
        lib = os.path.join(ROOT, "studio/music-library/tracks"); opts = sorted(f for f in os.listdir(lib) if f.startswith(mood + "-"))
        slug = os.path.basename(self.D.rstrip("/")); return os.path.join(lib, opts[sum(map(ord, slug)) % len(opts)])
    def write(self, bed_db=-27, music=None, music_lufs=-26, music_start=4.0):
        """music: a mood in studio/music-library/tracks (playful, lofi, ambient) or a file path. Writes audio_mixed.mp3 (with music
        when given) and always audio_nomusic.mp3 (for posts that get trending audio added in the Instagram app)."""
        T = self.TOTAL; fx = self.fx[: int(T * SR)]; ref = np.percentile(np.abs(fx[np.abs(fx) > 1e-4]), 99.5) + 1e-9
        sf.write(os.path.join(self.D, "sfx.wav"), (np.tanh(fx / ref * 1.1) * .62).astype(np.float32), SR)
        bed = os.path.join(ROOT, "studio/sfx-library/real/ambience-room.wav")
        base = (f"[0:a]apad,atrim=0:{T},loudnorm=I=-16:TP=-2,asplit=2[v][key];[1:a]volume=0.75[f];[2:a]atrim=0:{T},volume={10 ** (bed_db / 20) * 3:.3f},afade=t=in:d=0.4,afade=t=out:st={T - 1.5}:d=1.5[b];")
        tail = f"atrim=0:{T},alimiter=limit=0.89,loudnorm=I=-14:TP=-1.5"
        ins = ["-i", os.path.join(self.D, "audio.mp3"), "-i", os.path.join(self.D, "sfx.wav"), "-stream_loop", "-1", "-i", bed]
        fc0 = base + f"[key]anullsink;[v][f][b]amix=inputs=3:normalize=0:duration=first," + tail
        subprocess.run(["ffmpeg", "-loglevel", "error", "-y", *ins, "-filter_complex", fc0, "-ar", "44100", "-b:a", "192k", os.path.join(self.D, "audio_nomusic.mp3")], check=True)
        if music:
            track = music if os.path.exists(music) else self.music_track(music)
            fc = base + (f"[3:a]atrim=0:{T},loudnorm=I={music_lufs}:TP=-6,afade=t=in:d=0.3,afade=t=out:st={T - 1.6}:d=1.6[m0];"
                         f"[m0][key]sidechaincompress=threshold=0.02:ratio=5:attack=20:release=450[m];"
                         f"[v][f][b][m]amix=inputs=4:normalize=0:duration=first," + tail)
            subprocess.run(["ffmpeg", "-loglevel", "error", "-y", *ins, "-ss", str(music_start), "-stream_loop", "-1", "-i", track,
                            "-filter_complex", fc, "-ar", "44100", "-b:a", "192k", os.path.join(self.D, "audio_mixed.mp3")], check=True)
            open(os.path.join(self.D, "music.txt"), "w").write(os.path.relpath(track, ROOT) + "\n")
            print("audio ok (music: %s)" % os.path.basename(track), T)
        else:
            import shutil; shutil.copy(os.path.join(self.D, "audio_nomusic.mp3"), os.path.join(self.D, "audio_mixed.mp3")); print("audio ok", T)
