#!/usr/bin/env python3
"""Synthesise a sound-effect bed from a reel's timeline and mix it under the VO.

  sfx.py reels/<slug> [--gain 0.22] [--dry]

No sample library: every hit is generated with ffmpeg, so there is nothing to license
and nothing to download. Cues come from the timeline itself, which means the sound
lands on the animation by construction rather than by ear.

Writes <dir>/audio_mixed.mp3. Record with --audio audio_mixed.mp3.
"""
import argparse, json, os, subprocess, sys, tempfile

SR = 48000

# name -> (duration, lavfi source, filter chain, default gain)
VOICES = {
 "whoosh": (0.55, "anoisesrc=d=0.55:c=pink:a=0.7:r=%d" % SR,
            "highpass=f=300,lowpass=f=5200,afade=t=in:st=0:d=0.10,afade=t=out:st=0.16:d=0.39", 0.9),
 "swish":  (0.34, "anoisesrc=d=0.34:c=pink:a=0.6:r=%d" % SR,
            "highpass=f=900,lowpass=f=9000,afade=t=in:st=0:d=0.05,afade=t=out:st=0.08:d=0.26", 0.7),
 "tick":   (0.07, "anoisesrc=d=0.07:c=white:a=0.8:r=%d" % SR,
            "highpass=f=2200,afade=t=out:st=0:d=0.07", 0.5),
 "pop":    (0.16, "aevalsrc='0.6*sin(2*PI*520*t)+0.25*sin(2*PI*1040*t)':d=0.16:s=%d" % SR,
            "afade=t=out:st=0.01:d=0.15", 0.55),
 "thud":   (0.40, "aevalsrc='0.8*sin(2*PI*68*t)':d=0.40:s=%d" % SR,
            "afade=t=out:st=0.02:d=0.38", 0.85),
 "chime":  (1.10, "aevalsrc='0.5*sin(2*PI*880*t)+0.3*sin(2*PI*1320*t)+0.18*sin(2*PI*1760*t)':d=1.1:s=%d" % SR,
            "afade=t=out:st=0.03:d=1.05", 0.6),
 "riser":  (1.30, "aevalsrc='0.5*sin(2*PI*(180+900*t/1.3)*t)':d=1.3:s=%d" % SR,
            "afade=t=in:st=0:d=0.5,afade=t=out:st=1.05:d=0.25", 0.5),
 "drop":   (0.90, "aevalsrc='0.5*sin(2*PI*(520-430*t/0.9)*t)+0.35*sin(2*PI*60*t)':d=0.9:s=%d" % SR,
            "afade=t=out:st=0.15:d=0.75", 0.7),
 "sub":    (1.20, "aevalsrc='0.9*sin(2*PI*48*t)':d=1.2:s=%d" % SR,
            "afade=t=in:st=0:d=0.12,afade=t=out:st=0.4:d=0.8", 0.9),

 # ---- the classy set: mechanical, papery, restrained ----
 # a soft mallet: one clean partial, quick decay. Reads as "a mark was made"
 # without pretending to be a mechanism.
 "mark":   (0.30, "aevalsrc='0.5*sin(2*PI*1046*t)+0.2*sin(2*PI*1568*t)':d=0.30:s=%d" % SR,
            "afade=t=out:st=0.01:d=0.29", 0.34),
 "bell":   (1.40, "aevalsrc='0.5*sin(2*PI*1568*t)+0.25*sin(2*PI*2350*t)':d=1.4:s=%d" % SR,
            "afade=t=out:st=0.02:d=1.38", 0.4),
 # paper: soft filtered noise, no transient
 "paper":  (0.42, "anoisesrc=d=0.42:c=brown:a=0.7:r=%d" % SR,
            "highpass=f=700,lowpass=f=4200,afade=t=in:st=0:d=0.12,afade=t=out:st=0.14:d=0.28", 0.5),
 # a relay clack: wooden, dry, no ring
 "clack":  (0.11, "aevalsrc='0.6*sin(2*PI*320*t)+0.4*sin(2*PI*760*t)':d=0.11:s=%d" % SR,
            "afade=t=out:st=0.002:d=0.108", 0.4),
 # reverse swell: builds INTO the beat rather than punctuating it
 "swell":  (1.10, "anoisesrc=d=1.1:c=pink:a=0.7:r=%d" % SR,
            "highpass=f=500,lowpass=f=7000,afade=t=in:st=0:d=1.02,afade=t=out:st=1.04:d=0.06", 0.42),
 # soft high sparkle for a reveal
 "shimmer":(0.95, "aevalsrc='0.30*sin(2*PI*2093*t)+0.20*sin(2*PI*2637*t)+0.14*sin(2*PI*3136*t)':d=0.95:s=%d" % SR,
            "afade=t=in:st=0:d=0.05,afade=t=out:st=0.10:d=0.85", 0.34),
}


def cues_from(tl):
    """Scene timings -> (time, voice, gain). One rule per scene type."""
    C = []
    def add(t, v, g=1.0):
        if isinstance(t, (int, float)): C.append((float(t), v, g))
    for s in tl.get("scenes", []):
        ty = s.get("type", "")
        if ty == "kinetic.title":
            add(s.get("in"), "swish", 0.55)
            # opt-in: a soft hit per word, so a text-only close is not silent
            if s.get("sfxWords"):
                st = s.get("stagger") or 0.07
                for i, _w in enumerate((s.get("text") or "").split()):
                    add(s.get("in", 0) + 0.18 + i * st, "tick", 0.26)
            if s.get("sfxChime"):
                add(s.get("in", 0) + 0.18, "chime", 0.45)
                add(s.get("in", 0) + 0.18, "sub", 0.38)
        elif ty == "split.paths":
            add(s.get("start"), "whoosh", 0.7)
            add(s.get("winEnd") or s.get("end"), "chime", 0.55)
            add(s.get("loseEnd"), "thud", 0.45)
        elif ty == "cards.dismiss":
            for it in s.get("items", []):
                add(it.get("at"), "clack", 0.5)
                add(it.get("dismiss"), "swish", 0.42)
        elif ty == "field.expand":
            add(s.get("start") or s.get("in"), "riser", 0.5)
            add(s.get("collapse"), "drop", 0.75)
        elif ty == "plan.empty":
            add(s.get("in"), "paper", 0.5)
            add(s.get("stampAt"), "thud", 0.65)
            add(s.get("stampAt"), "clack", 0.45)
        elif ty == "chips.reorder":
            add(s.get("in"), "paper", 0.45)
            add(s.get("orderAt") - 0.9 if s.get("orderAt") else None, "swell", 0.45)
            add(s.get("orderAt"), "sub", 0.55)
            add(s.get("liveAt"), "shimmer", 0.5)
        elif ty == "slot.waiting":
            add(s.get("in"), "paper", 0.55)
            ta = s.get("typeAt")
            if ta is not None:
                add(ta, "mark", 0.45)                 # the line starts
                add(ta + 1.2, "shimmer", 0.4)         # and resolves
        elif ty == "stage.two":
            for it in s.get("items", []):
                add(it.get("at"), "pop", 0.55)
                add(it.get("fillAt"), "riser", 0.32)
        elif ty == "date.roll":
            add(s.get("roll") or s.get("in"), "riser", 0.45)
            r = s.get("roll") or s.get("in")
            for k in range(4): add(r + 0.18 * k, "clack", 0.30)   # digits landing
            add((s.get("roll") or s.get("in")) + 0.95, "mark", 0.45)
        elif ty == "tokens.land":
            for it in s.get("items", []): add(it.get("at"), "clack", 0.55)
        elif ty == "count.up":
            add(s.get("start") or s.get("in"), "riser", 0.5)
            add(s.get("end"), "mark", 0.5)
        elif ty == "daygrid.fill":
            fs, fe = s.get("fillStart"), s.get("fillEnd")
            if fs is not None and fe is not None:
                n = 7                                              # a tick every so often
                for k in range(n): add(fs + (fe - fs) * k / n, "tick", 0.34)
                add(fe, "shimmer", 0.42)
            for m in (s.get("dead") or [])[:1]:                     # the streak breaking
                if fs is not None and fe is not None:
                    add(fs + (fe - fs) * (m / float(s.get("count", 120))), "thud", 0.6)
        elif ty == "thresholds":
            for it in s.get("items", []): add(it.get("at"), "pop", 0.5)
        elif ty == "captions.track":
            # a soft tick only where a caption is emphasised, so the mix stays clean
            for it in (s.get("items") or []):
                if it.get("accent"): add(it.get("t"), "tick", 0.20)
        elif ty == "fields.empty":
            for it in (s.get("items") or []):
                add(it.get("at"),      "clack", 0.40)     # a field arriving
                add(it.get("emptyAt"), "drop",  0.44)     # its value draining away
                add(it.get("fillAt"),  "pop",   0.48)     # and coming back
            add(s.get("stampAt"), "thud", 0.58)
            add(s.get("stampAt"), "sub",  0.38)
        elif ty == "span.bookend":
            add(s.get("drawAt") or s.get("in"), "swish", 0.40)
            for k in ("recordLeft", "recordRight"):
                r = s.get(k) or {}
                add(r.get("at"), "chime" if k.endswith("Right") else "pop", 0.52)
        elif ty == "ambient.field":
            for b2 in (s.get("bursts") or []):
                add(b2.get("t"), "swell", 0.34 * (b2.get("power") or 1))
            for f2 in (s.get("flashes") or []):
                add(f2.get("t"), "shimmer", 0.36)
        elif ty == "card.pressure":
            add(s.get("in"), "shimmer", 0.42)                  # the memory arriving
            for w in (s.get("weights") or []):
                add(w.get("at"), "thud", 0.58)                 # each one landing on it
                add(w.get("at"), "sub", 0.34)
            add(s.get("dimAt"), "swell", 0.40)
            add(s.get("driftAt"), "drop", 0.46)                # losing track of it
            sn = s.get("snapAt")
            if sn is not None:                                  # "not a chance"
                add(sn, "bell", 0.70)
                add(sn, "sub", 0.52)
                add(sn, "shimmer", 0.44)
        elif ty == "archive.scroll":
            sp = s.get("scroll") or {}
            a2, e2 = sp.get("at") or s.get("in"), sp.get("end") or s.get("out")
            add(s.get("in"), "paper", 0.44)
            if a2 is not None and e2 is not None and e2 > a2:
                n = 7                                           # a pulse as it runs on
                for k in range(n): add(a2 + (e2 - a2) * k / n, "tick", 0.22)
            add(e2, "swell", 0.40)
        elif ty == "phase.marks":
            for it in (s.get("items") or []):
                add(it.get("at"), "pop" if it.get("live") else "clack",
                    0.52 if it.get("live") else 0.34)
            add(s.get("capAt"), "mark", 0.42)
        elif ty == "stair.build":
            dk = s.get("draw") or []
            if dk:
                add(dk[0].get("t"), "swish", 0.38)             # the line starting
                # a tick as each drawing run finishes, so growth is audible
                for k1, k2 in zip(dk, dk[1:]):
                    if (k2.get("n") or 0) > (k1.get("n") or 0):
                        add(k2.get("t"), "tick", 0.32)
            for c2 in (s.get("cam") or []):                    # each camera move
                add(c2.get("t"), "whoosh", 0.30)
            tw = s.get("tower") or {}
            add(tw.get("at"), "thud", 0.42)
            for m in (s.get("markers") or []):
                add(m.get("at"), "mark", 0.46)                 # an altitude crossed
            add(s.get("strikeAt"), "drop", 0.62)
            add(s.get("strikeAt"), "sub", 0.44)
            for c2 in (s.get("captions") or []): add(c2.get("t"), "swish", 0.26)
        elif ty == "receipt.print":
            add(s.get("in"), "paper", 0.55)                  # the roll feeding up
            add(s.get("titleAt"), "thud", 0.55)
            add(s.get("subAt"), "clack", 0.40)
            for it in s.get("items", []):
                at = it.get("at")
                if at is None: continue
                add(at,        "clack", 0.46)                # the head chattering across
                add(at + 0.12, "tick",  0.30)
                add(at + 0.24, "clack", 0.34)
                add(at + 0.46, it.get("figSfx", "tick"), 0.46)   # the figure landing
            add(s.get("ruleAt"), "swish", 0.45)
            for i, it in enumerate(s.get("totals", [])):
                at = it.get("at")
                add(at, "bell" if i else "chime", 0.55)
                if it.get("big"):
                    add(at, "sub", 0.45)
                    add(at + (it.get("rollFor") or 1.1), "shimmer", 0.40)
            st = s.get("stampAt")
            if st is not None:
                add(st, "thud", 0.70)                         # the stamp coming down
                add(st, "paper", 0.40)
            add(s.get("out"), "paper", 0.45)                  # and feeding back out
        elif ty == "axis.travel":
            add(s.get("drawAt") or s.get("in"), "whoosh", 0.42)
            ta, step = s.get("tickAt"), s.get("tickStep") or 0.14
            if ta is not None:
                for i in range(len(s.get("years") or [])):
                    add(ta + i * max(step, 0.10), "tick", 0.30)   # keep clear of the 0.09 guard
            add(s.get("cardAt"), "pop", 0.52)
            tv = s.get("travelAt")
            if tv is not None:
                add(tv, "riser", 0.44)                            # the years going past
                add(s.get("travelEnd") or (tv + 1.6), "chime", 0.50)
                add(s.get("travelEnd") or (tv + 1.6), "sub", 0.38)
        elif ty == "dream.stack":
            for it in s.get("items", []):
                add(it.get("at"), "pop", 0.46)
                add(it.get("outAt"), "drop", 0.50)                # the one that goes out
                add(it.get("outAt"), "sub", 0.34)
            add(s.get("dimAt"), "swell", 0.40)
            add(s.get("capAt"), "mark", 0.38)
        elif ty == "rows.verdict":
            VSFX = {"done": ("chime", 0.50), "close": ("pop", 0.48), "open": ("thud", 0.44)}
            for it in s.get("items", []):
                add(it.get("at"), "clack", 0.42)
                v, g = VSFX.get(it.get("verdict"), ("pop", 0.45))
                add(it.get("verdictAt"), v, g)                    # the verdict lands
            add(s.get("capAt"), "shimmer", 0.42)
        elif ty == "year.grid":
            # replicate the engine's eased front so every hit lands on a real cell
            def _eio(x): return 4*x*x*x if x < .5 else 1 - ((-2*x+2)**3)/2
            def _front(keys, t2):
                if not keys: return 0.0
                if t2 <= keys[0]["t"]: return float(keys[0]["n"])
                for k1, k2 in zip(keys, keys[1:]):
                    if k1["t"] <= t2 <= k2["t"]:
                        u = (t2-k1["t"])/max(1e-6, k2["t"]-k1["t"])
                        return k1["n"] + (k2["n"]-k1["n"])*_eio(u)
                return float(keys[-1]["n"])
            def _crossings(keys):
                """time at which the front first passes each integer index"""
                out, prev = {}, None
                if not keys: return out
                t2, tend = keys[0]["t"], keys[-1]["t"]
                while t2 <= tend:
                    n = _front(keys, t2)
                    if prev is not None:
                        for i in range(int(prev)+1, int(n)+1): out.setdefault(i, t2)
                    prev = n; t2 += 0.01
                return out
            rev = _crossings(s.get("reveal") or [])
            fil = _crossings(s.get("fill") or [])
            elapsed = s.get("elapsed", 10**9)
            for i, t2 in rev.items():
                if i < 8: add(t2, "pop", 0.42)             # the first boxes arriving
            for i, t2 in fil.items():
                if i >= elapsed: continue
                if i < 36: add(t2, "tick", 0.34)           # every day, while you can count them
                elif i % 5 == 0: add(t2, "tick", 0.20)     # then just the pulse of it
            prevz = None
            for z in (s.get("zoom") or []):                # only sound an actual move
                key = (z.get("focus"), z.get("fit"))
                if key != prevz: add(z.get("t"), "whoosh", 0.34)
                prevz = key
            # a soft mark as each month completes
            mstart, md = 0, [31,28,31,30,31,30,31,31,30,31,30,31]
            for m in md:
                mstart += m
                if mstart - 1 in fil and mstart - 1 < elapsed:
                    add(fil[mstart-1], "mark", 0.34)
            add(s.get("labelsAt"), "shimmer", 0.40)
            for c2 in (s.get("captions") or []): add(c2.get("t"), "swish", 0.30)
            for i, c2 in enumerate(s.get("stats") or []):
                add(c2.get("t"), "thud" if i == 0 else "chime", 0.60)
                add(c2.get("t"), "sub", 0.42)
        elif ty == "arc.curve":
            add(s.get("drawAt") or s.get("in"), "swell", 0.42)     # the curve starts climbing
            for it in s.get("items", []): add(it.get("at"), "pop", 0.5)
            add(s.get("capAt"), "shimmer", 0.42)
        elif ty == "method.flow":
            for it in s.get("items", []): add(it.get("at"), "clack", 0.5)
            add(s.get("capAt"), "mark", 0.4)
        elif ty == "miss.rule":
            for key in ("rowA", "rowB"):
                r = s.get(key) or {}
                at, step = r.get("at"), r.get("step") or 0.085
                pat = r.get("pattern") or ""
                if at is None: continue
                for i, ch in enumerate(pat):                       # a tick per marked day
                    if ch == "#": add(at + 0.25 + i * step, "tick", 0.30)
                br = r.get("breakAt")
                if br is not None:
                    add(br, "drop", 0.55)                          # the chain going dead
                    add(br, "sub", 0.42)
            add(s.get("verdictAt"), "thud", 0.55)
        elif ty == "floor.bar":
            add(s.get("fillAt") or s.get("in"), "riser", 0.4)
            add(s.get("floorAt"), "mark", 0.45)
            add(s.get("dropAt"), "drop", 0.5)
        elif ty == "collapse.step":
            add(s.get("at"), "swish", 0.5)
            add((s.get("at") or 0) + 0.5, "pop", 0.5)
        elif ty == "sharpen.text":
            add(s.get("vagueAt"), "mark", 0.35)
            add(s.get("at"), "shimmer", 0.45)
        elif ty == "steps.three":
            for a2 in (s.get("at") or []): add(a2, "clack", 0.45)
        elif ty == "end.card":
            add(s.get("in") - 1.0, "swell", 0.5)      # builds into the reveal
            add(s.get("in"), "chime", 0.6)
            add(s.get("in"), "sub", 0.45)
            us, ue = s.get("urlStart"), s.get("urlEnd")
            if us is not None:
                add(us, "mark", 0.4)                   # the URL begins to appear
        # ---- punch-engine scenes (bold kinetic type, no VO) ----
        elif ty == "stack":
            for L in s.get("lines", []) or []:
                at = L.get("at", s.get("in"))
                if at is not None and at > 0.05: add(at, L.get("sfx", "pop"), L.get("sfxGain", 0.5))
                if L.get("strikeAt") is not None: add(L["strikeAt"], "swish", 0.5)
                if L.get("swapAt") is not None: add(L["swapAt"], "thud", 0.6)
        elif ty == "plan":
            ta = s.get("titleAt", s.get("in"))
            if ta is not None and ta > 0.05: add(ta, "whoosh", 0.5)
            for it in s.get("items", []) or []:
                add(it.get("at"), "clack", 0.55)
                if it.get("checkAt") is not None: add(it["checkAt"], "tick", 0.5)
        elif ty == "brand":
            add(s.get("in") - 1.0, "swell", 0.5)
            add(s.get("in"), "chime", 0.55)
            add(s.get("in"), "sub", 0.45)
        # ---- mono-engine scenes ----
        elif ty in ("diary.open", "diary.close"):
            add(s.get("click"), "whoosh", 0.6)
        elif ty == "diary.tap":
            for a in s.get("at", []): add(a, "clack", 0.5)
        elif ty == "archive.zoom":
            add(s.get("start"), "riser", 0.45)
        elif ty == "archive.flip":
            add(s.get("at"), "chime", 0.4)
        elif ty == "calendar.year":
            for a in (s.get("strike") or []):
                if a is not None: add(a, "tick", 0.5)
        elif ty == "diary.write":
            for l in s.get("lines", []) or []:
                add(l.get("start"), "mark", 0.4)
        elif ty == "compose.type":
            add(s.get("start"), "mark", 0.42)
            add(s.get("end"), "bell", 0.34)
        elif ty == "compose.post":
            add(s.get("clickAt"), "pop", 0.6)
            add(s.get("flyEnd"), "chime", 0.45)
    for b in tl.get("bg", []) or []:
        if b.get("t", 0) > 0.2: add(b["t"], "swish", 0.34)
    for x in tl.get("sfx", []) or []:            # hand-placed extras
        add(x.get("t"), x.get("v", "pop"), x.get("g", 0.5))
    for c in tl.get("camera", []) or []:
        if (c.get("s") or 1) >= 1.10: add(c.get("t"), "swish", 0.28)
    C = [c for c in C if c[0] is not None and c[0] >= 0]
    C.sort(key=lambda x: x[0])
    # thin out pile-ups: two hits inside 90ms just sound like one messy hit
    out, last = [], {}
    for t, v, g in C:
        if v in last and t - last[v] < 0.09: continue
        last[v] = t; out.append((t, v, g))
    return out

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("dir"); ap.add_argument("--gain", type=float, default=0.32)  # ~9dB under a -26dB VO
    ap.add_argument("--dry", action="store_true", help="list cues, write nothing")
    ap.add_argument("--no-vo", action="store_true",
                    help="no narration: the effects bed IS the soundtrack, at full level")
    a = ap.parse_args()

    tl_p = os.path.join(a.dir, "timeline.json")
    if not os.path.exists(tl_p): sys.exit("no timeline.json")
    tl = json.load(open(tl_p))
    vo = None
    for e in ("mp3", "wav", "m4a"):
        p = os.path.join(a.dir, "audio." + e)
        if os.path.exists(p): vo = p; break
    if not vo and not a.no_vo: sys.exit("no audio.* to mix under (use --no-vo for a silent reel)")

    cues = cues_from(tl)
    print(f"{len(cues)} cues from {len(tl.get('scenes',[]))} scenes")
    if a.dry:
        for t, v, g in cues: print(f"  {t:6.2f}  {v:<7s} x{g}")
        return

    tmp = tempfile.mkdtemp(prefix="sfx_")
    made = {}
    for name in set(v for _, v, _ in cues):
        d, src, filt, base = VOICES[name]
        w = os.path.join(tmp, name + ".wav")
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "lavfi", "-i", src,
                        "-af", f"{filt},volume={base}", w], check=True)
        made[name] = w

    # one input per hit, delayed into place, summed without normalisation
    ins, parts = [], []
    for i, (t, v, g) in enumerate(cues):
        ins += ["-i", made[v]]
        ms = int(t * 1000)
        parts.append(f"[{i}:a]adelay={ms}|{ms},volume={g}[s{i}]")
    mix = "".join(f"[s{i}]" for i in range(len(cues)))
    parts.append(f"{mix}amix=inputs={len(cues)}:normalize=0:dropout_transition=0[bed]")
    bed = os.path.join(tmp, "bed.wav")
    subprocess.run(["ffmpeg", "-v", "error", "-y"] + ins +
                   ["-filter_complex", ";".join(parts), "-map", "[bed]", bed], check=True)

    out = os.path.join(a.dir, "audio_mixed.mp3")
    if a.no_vo:
        # nothing to duck under: run the bed at full level, padded to the timeline
        total = float(tl.get("total") or 0)
        pad = ["-af", f"apad=whole_dur={total},alimiter=limit=0.95"] if total else \
              ["-af", "alimiter=limit=0.95"]
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", bed] + pad +
                       ["-c:a", "libmp3lame", "-b:a", "192k", out], check=True)
        dur = subprocess.run(["ffprobe","-v","error","-show_entries","format=duration",
                              "-of","csv=p=0",out], capture_output=True, text=True).stdout.strip()
        print(f"-> {out}  ({float(dur):.2f}s, sound design only, no VO)")
        print(f"record with: --audio {out}")
        return
    # the bed sits under the voice; the voice is never touched
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", vo, "-i", bed,
                    "-filter_complex",
                    f"[1:a]volume={a.gain}[b];[0:a][b]amix=inputs=2:normalize=0:dropout_transition=0,"
                    f"alimiter=limit=0.95[m]",
                    "-map", "[m]", "-c:a", "libmp3lame", "-b:a", "192k", out], check=True)
    dur = subprocess.run(["ffprobe","-v","error","-show_entries","format=duration",
                          "-of","csv=p=0",out], capture_output=True, text=True).stdout.strip()
    print(f"-> {out}  ({float(dur):.2f}s, bed at {a.gain:.2f})")
    print(f"record with: --audio {out}")

if __name__ == "__main__":
    main()
