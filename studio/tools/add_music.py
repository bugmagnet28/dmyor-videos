"""Add an emotion-arc music bed to a finished reel (any style), ducked under its existing audio.

    python3 studio/tools/add_music.py <video.mp4> [arc]        arc default: "mystery:0,resolve:0.62"
      arc = comma list of mood:start where start is seconds or a fraction (<1) of the length.
Writes <video> with music in place and keeps the original as <dir>/video-nomusic.mp4 (if not already there).
Uses the same moods/tracks and levels as reels/pixel-series/sfxmix.py (studio/music-library/tracks)."""
import os, shutil, subprocess, sys
ROOT = os.getcwd(); LIB = os.path.join(ROOT, "studio/music-library/tracks")
def dur(f): return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f], capture_output=True, text=True).stdout)
def pick(mood, salt, key):
    opts = sorted(f for f in os.listdir(LIB) if f.startswith(mood + "-")); return os.path.join(LIB, opts[(sum(map(ord, key)) + salt) % len(opts)])
def main():
    v = sys.argv[1]; arc_s = sys.argv[2] if len(sys.argv) > 2 else "mystery:0,resolve:0.62"
    d = os.path.dirname(v); orig = os.path.join(d, "video-nomusic.mp4")
    if not os.path.exists(orig): shutil.copy(v, orig)
    T = dur(orig); key = os.path.basename(d.rstrip("/"))
    arc = []
    for i, part in enumerate(arc_s.split(",")):
        m, t = part.split(":"); t = float(t); arc.append((m, t * T if t < 1 and i else t))
    xf = 1.0; ins = ["-i", orig]; fc = "[0:a]asplit=2[v][key];"; used = []
    for k, (m, t0) in enumerate(arc):
        t1 = arc[k + 1][1] if k + 1 < len(arc) else T; tr = pick(m, k, key); used.append(os.path.basename(tr))
        a0 = max(0, t0 - (xf / 2 if k else 0)); a1 = min(T, t1 + (xf / 2 if k + 1 < len(arc) else 0)); dd = a1 - a0
        fin = .3 if k == 0 else xf; fout = 1.6 if k + 1 == len(arc) else xf
        ins += ["-ss", "3", "-stream_loop", "-1", "-i", tr]
        fc += (f"[{k + 1}:a]atrim=0:{dd:.3f},loudnorm=I=-21:TP=-4,afade=t=in:d={fin},afade=t=out:st={max(0, dd - fout):.3f}:d={fout},"
               f"adelay={int(a0 * 1000)}|{int(a0 * 1000)},apad,atrim=0:{T}[s{k}];")
    fc += "".join(f"[s{k}]" for k in range(len(arc))) + f"amix=inputs={len(arc)}:normalize=0[m0];"
    fc += f"[m0][key]sidechaincompress=threshold=0.06:ratio=2.2:attack=40:release=500:knee=4[m];[v][m]amix=inputs=2:normalize=0:duration=first,alimiter=limit=0.89,loudnorm=I=-14:TP=-1.5[a]"
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", *ins, "-filter_complex", fc, "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "160k", "-movflags", "+faststart", v], check=True)
    open(os.path.join(d, "music.txt"), "w").write(arc_s + "\n" + "\n".join(used) + "\n"); print("music:", v, used)
if __name__ == "__main__": main()
