"""Prompt-to-animation: scene.json (written from a plain-language prompt) -> animated 1080x1920 video with sound.

    tts/.venv/bin/python .claude/skills/prompt-animation/scripts/make_anim.py reels/<slug> [--record]

reels/<slug>/scene.json (see SKILL.md for the full vocabulary):
  duration, scenes[{start, dur, bg, transition, camera, props[], actors[], fx[]}], text[], music ("calm"|"none"),
  narration (optional: {"spoken": "...", "at": 0.5, "voice": "am_eric"})
Sound effects are derived from the script automatically (walk -> footsteps, type -> keys, ledges -> rising chime,
props appearing -> pop, scene change -> whoosh, plant/celebrate -> stamp + chime). Run from the project root.
"""
import argparse, importlib.util, json, os, re, subprocess, sys
import numpy as np, soundfile as sf

ROOT = os.getcwd(); SKILL = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); SR = 44100


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("reel"); ap.add_argument("--record", action="store_true"); o = ap.parse_args()
    d = o.reel.rstrip("/"); S = json.load(open(os.path.join(d, "scene.json"))); total = float(S["duration"])
    html = open(os.path.join(SKILL, "assets", "engine.html")).read().replace("/*__SCENE__*/{}", json.dumps(S))
    html = html.replace("url(fonts/", "url(" + os.path.relpath(os.path.join(SKILL, "assets/fonts"), d) + "/")
    open(os.path.join(d, "anim.html"), "w").write(html)

    sys.argv = ["kit", d]
    kit = load("kit", os.path.join(ROOT, ".claude/skills/animated-illustration-explainer/scripts/sfx.py"))
    syn = load("syn", os.path.join(ROOT, ".claude/skills/cinematic-motion/scripts/make_film.py"))
    def K(name, *a):
        f = getattr(kit, name)(*a); return f / (np.abs(f).max() + 1e-9)
    fx = np.zeros(int((total + 3) * SR)); add = lambda s, at, g: syn.add(fx, s, at, g)
    for i, sc in enumerate(S.get("scenes", [])):
        t0 = sc["start"]
        if i > 0: add(syn.whoosh(.6, 300, 4000), t0 - .15, .35)
        for p in sc.get("props", []):
            if p.get("in") is not None: add(K("pop", i % 6), t0 + p["in"], .35)
            if p.get("typeFrom") is not None:
                for at in np.arange(t0 + p["typeFrom"], t0 + p["typeFrom"] + p.get("typeDur", 1.6), .07):
                    add(K("tick")[: int(.02 * SR)], at, .2)
            for j, L in enumerate(p.get("ledges", [])):
                if L.get("at") is not None: add(K("right", j), t0 + L["at"], .4)
            if p["type"] == "flag" and p.get("at") is not None: add(K("stamp"), t0 + p["at"], .5); add(K("right", 5), t0 + p["at"] + .2, .4)
        for a in sc.get("actors", []):
            for ac in a.get("actions", []):
                at, dur, kind = t0 + ac["at"], ac.get("dur", 0), ac["do"]
                if kind in ("walk", "run", "climb") and dur:
                    step = {"walk": .58 / ac.get("speed", 1), "run": .36, "climb": .55}[kind]
                    for k2, st in enumerate(np.arange(at + .1, at + dur, step)): add(kit.step() / .6, st, .3 if kind != "climb" else .22)
                if kind == "type" and dur:
                    for st in np.arange(at, at + dur, .09):
                        if (int(st * 100) % 7) != 0: add(K("tick")[: int(.02 * SR)], st, .18)
                if kind == "write" and dur: add(K("pencil", dur), at, .3)
                if kind == "jump": add(syn.whoosh(.4, 600, 5000), at, .25); add(kit.step() / .6, at + .62, .45)
                if kind == "plant": add(K("stamp"), at + .55, .5)
                if kind == "celebrate": add(K("right", 3), at, .4); add(K("chord"), at + .15, .3)
        for f in sc.get("fx", []):
            if f["type"] == "sparkle": add(K("right", 4), t0 + f["at"], .35)
    for tx in S.get("text", []): add(K("tap"), tx["at"], .12)
    fx = fx[: int(total * SR)]

    mus = np.zeros(int(total * SR))
    if S.get("music", "calm") != "none":
        D = 50; seg = total / 3
        for k2, ns in enumerate([[D - 12, D, D + 4, D + 7, D + 14], [D - 10, D + 2, D + 5, D + 9, D + 14], [D - 12, D, D + 4, D + 7, D + 11, D + 16]]):
            syn.add(mus, syn.pad(ns, seg + 1.5, bright=6, a=1.0, r=1.2), k2 * seg, .5)
        for k2, at in enumerate(np.arange(.5, total - 1, .62)):
            syn.add(mus, syn.pluck([74, 78, 81, 83, 81, 78, 76, 78][k2 % 8], 2.0, 1.2), at, .16)
        mus = syn.reverb(mus, 2.6, .3); fo = int(1.5 * SR); mus[-fo:] *= np.linspace(1, 0, fo) ** 2
        mus = mus / (np.abs(mus).max() + 1e-9)
    sf.write(os.path.join(d, "music.wav"), (mus * .5).astype(np.float32), SR)
    sf.write(os.path.join(d, "sfx.wav"), (fx / (np.abs(fx).max() + 1e-9) * .5).astype(np.float32), SR)

    inputs, fc_v = [], None
    N = S.get("narration")
    if N:
        say = re.sub(r"\bDmyor\b", "Deem-yor", N["spoken"])
        subprocess.run([os.path.join(ROOT, "tts/.venv/bin/python"), os.path.join(ROOT, ".claude/skills/cinematic-motion/scripts/say.py"), say, os.path.join(d, "voice.mp3"),
                        "--voice", N.get("voice", "am_eric"), "--stages"], check=True)
    mix = os.path.join(d, "audio_mixed.mp3"); ms = int(1000 * (N or {}).get("at", .5))
    if N:
        fc = (f"[0:a]adelay={ms}|{ms},apad,atrim=0:{total},loudnorm=I=-16:TP=-2,asplit[v][sc];[1:a]volume=0.4[m0];[m0][sc]sidechaincompress=threshold=0.04:ratio=5:attack=20:release=400[m];"
              f"[2:a]volume=0.6[f];[v][m][f]amix=inputs=3:normalize=0:duration=longest,atrim=0:{total},alimiter=limit=0.89,loudnorm=I=-14:TP=-1.5")
        cmd = ["-i", os.path.join(d, "voice.mp3"), "-i", os.path.join(d, "music.wav"), "-i", os.path.join(d, "sfx.wav")]
    else:
        fc = f"[0:a]volume=0.55[m];[1:a]volume=0.8[f];[m][f]amix=inputs=2:normalize=0:duration=longest,atrim=0:{total},alimiter=limit=0.89,loudnorm=I=-15:TP=-1.5"
        cmd = ["-i", os.path.join(d, "music.wav"), "-i", os.path.join(d, "sfx.wav")]
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y"] + cmd + ["-filter_complex", fc, "-ar", "44100", "-b:a", "192k", mix], check=True)
    print(f"built {d}/anim.html, {mix} ({total}s)")
    if o.record:
        mp4 = os.path.join(d, "anim.mp4")
        with open(os.path.join(d, "record.log"), "w") as log:
            subprocess.run(["node", "record.js", "--page", os.path.join(d, "anim.html"), "--out", mp4, "--audio", mix], check=True, stdout=log, stderr=log)
        print("recorded", mp4)


if __name__ == "__main__":
    main()
