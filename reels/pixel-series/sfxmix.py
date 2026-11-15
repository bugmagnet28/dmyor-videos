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
    def music_track(self, mood, salt=0):
        """Pick a library track for this reel and mood: same reel always gets the same track."""
        lib = os.path.join(ROOT, "studio/music-library/tracks"); opts = sorted(f for f in os.listdir(lib) if f.startswith(mood + "-"))
        slug = os.path.basename(self.D.rstrip("/")); return os.path.join(lib, opts[(sum(map(ord, slug)) + salt) % len(opts)])
    def write(self, bed_db=-27, music=None, music_lufs=-21, duck_ratio=2.2, xfade=1.0, music_start=3.0):
        """music: None, a mood/file, or an emotion arc [(mood_or_file, start_s), ...] that crossfades at each start time
        (e.g. [("investigate", 0), ("resolve", SC["S4"][0])]). Music sits ~9 dB under the voice while it speaks (owner
        2026-11-15: keep it audible) and a little higher in pauses. Always also writes audio_nomusic.mp3."""
        T = self.TOTAL; fx = self.fx[: int(T * SR)]; ref = np.percentile(np.abs(fx[np.abs(fx) > 1e-4]), 99.5) + 1e-9
        sf.write(os.path.join(self.D, "sfx.wav"), (np.tanh(fx / ref * 1.1) * .62).astype(np.float32), SR)
        bed = os.path.join(ROOT, "studio/sfx-library/real/ambience-room.wav")
        base = (f"[0:a]apad,atrim=0:{T},loudnorm=I=-16:TP=-2,asplit=2[v][key];[1:a]volume=0.75[f];[2:a]atrim=0:{T},volume={10 ** (bed_db / 20) * 3:.3f},afade=t=in:d=0.4,afade=t=out:st={T - 1.5}:d=1.5[b];")
        tail = f"atrim=0:{T},alimiter=limit=0.89,loudnorm=I=-14:TP=-1.5"
        ins = ["-i", os.path.join(self.D, "audio.mp3"), "-i", os.path.join(self.D, "sfx.wav"), "-stream_loop", "-1", "-i", bed]
        fc0 = base + "[key]anullsink;[v][f][b]amix=inputs=3:normalize=0:duration=first," + tail
        subprocess.run(["ffmpeg", "-loglevel", "error", "-y", *ins, "-filter_complex", fc0, "-ar", "44100", "-b:a", "192k", os.path.join(self.D, "audio_nomusic.mp3")], check=True)
        if not music:
            import shutil; shutil.copy(os.path.join(self.D, "audio_nomusic.mp3"), os.path.join(self.D, "audio_mixed.mp3")); print("audio ok", T); return
        arc = [(music, 0)] if isinstance(music, str) else list(music)
        segs, used = [], []
        for k, (m, t0) in enumerate(arc):
            t1 = arc[k + 1][1] if k + 1 < len(arc) else T
            track = m if os.path.exists(m) else self.music_track(m, k); used.append(os.path.relpath(track, ROOT))
            a0 = max(0, t0 - (xfade / 2 if k else 0)); a1 = min(T, t1 + (xfade / 2 if k + 1 < len(arc) else 0)); dur = a1 - a0
            fin = .3 if k == 0 else xfade; fout = 1.6 if k + 1 == len(arc) else xfade
            segs.append((track, a0, dur, fin, fout))
        fc = base; ins2 = list(ins)
        for k, (track, a0, dur, fin, fout) in enumerate(segs):
            ins2 += ["-ss", str(music_start), "-stream_loop", "-1", "-i", track]
            fc += (f"[{3 + k}:a]atrim=0:{dur:.3f},loudnorm=I={music_lufs}:TP=-4,afade=t=in:d={fin},afade=t=out:st={max(0, dur - fout):.3f}:d={fout},"
                   f"adelay={int(a0 * 1000)}|{int(a0 * 1000)},apad,atrim=0:{T}[s{k}];")
        fc += "".join(f"[s{k}]" for k in range(len(segs))) + f"amix=inputs={len(segs)}:normalize=0[m0];"
        fc += f"[m0][key]sidechaincompress=threshold=0.06:ratio={duck_ratio}:attack=40:release=500:knee=4[m];[v][f][b][m]amix=inputs=4:normalize=0:duration=first," + tail
        subprocess.run(["ffmpeg", "-loglevel", "error", "-y", *ins2, "-filter_complex", fc, "-ar", "44100", "-b:a", "192k", os.path.join(self.D, "audio_mixed.mp3")], check=True)
        open(os.path.join(self.D, "music.txt"), "w").write("\n".join(f"{t0:.2f}s {u}" for (m, t0), u in zip(arc, used)) + "\n")
        print("audio ok (music: %s)" % ", ".join(os.path.basename(u) for u in used), T)
