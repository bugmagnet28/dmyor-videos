#!/usr/bin/env python3
"""Inline timeline.json into the engine -> reels/<slug>/reel.html (self-contained)."""
import json, os, sys, re

def main():
    d = sys.argv[1] if len(sys.argv) > 1 else sys.exit("usage: build.py reels/<slug>")
    assets = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'assets')
    tl_path = os.path.join(d, 'timeline.json')
    if not os.path.exists(tl_path):
        sys.exit(f"no {tl_path} - write the timeline before building")
    tl = json.load(open(tl_path))

    cues = os.path.join(d, 'cues.json')
    if os.path.exists(cues):
        dur = json.load(open(cues)).get('duration')
        if dur and abs(dur - tl.get('total', 0)) > 0.25:
            print(f"note: timeline total {tl.get('total')} vs audio {dur} - using audio duration")
            tl['total'] = dur

    eng = tl.get('engine', 'mono')          # "mono" = monochrome, "motion" = colour + camera
    # "punch" = bold bright kinetic type for muted autoplay (2026-10-08)
    hf, jf = {'mono': ('engine.html','engine.js'),
              'punch': ('engine-punch.html','engine-punch.js')}.get(eng, ('engine-motion.html','engine-motion.js'))
    html = open(os.path.join(assets, hf)).read()
    js   = open(os.path.join(assets, jf)).read()
    html = re.sub(r'var TL = /\*__TIMELINE__\*/.*?;',
                  # lambda: a plain replacement string would turn "\\n" in the JSON into a raw
                  # newline and break the page (found 2026-10-08)
                  lambda m: 'var TL = ' + json.dumps(tl, ensure_ascii=False) + ';', html, count=1, flags=re.S)
    html = html.replace('<script src="%s"></script>' % jf, '<script>\n' + js + '\n</script>')
    out = os.path.join(d, 'reel.html')
    open(out, 'w').write(html)
    n = len(tl.get('scenes', []))
    print(f"built {out}  ({n} scenes, {tl['total']}s, {eng} engine, self-contained)")

if __name__ == '__main__':
    main()
