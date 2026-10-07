#!/usr/bin/env python3
"""dmyor reel registry: scaffold, log audio/publish/performance, report.

  reel.py new <slug> --hint "..."          scaffold reels/<slug>
  reel.py audio <slug> --file p [--voice]  record the VO + its settings
  reel.py publish <slug> --platform ...    log where/when it went out
  reel.py perf <slug> --platform ...       append a metrics reading
  reel.py rate                             measured words/sec across reels
  reel.py gaps <slug>                      dead air in the timeline
  reel.py report                           what correlates with reach
  reel.py list                             every reel and its status
"""
import argparse, json, os, re, shutil, statistics as st, subprocess, sys
from datetime import datetime

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..'))
REELS = os.path.join(ROOT, 'reels')

def rdir(slug): return os.path.join(REELS, slug)
def jload(p, d=None): return json.load(open(p)) if os.path.exists(p) else d
def jdump(p, o):
    os.makedirs(os.path.dirname(p), exist_ok=True)
    json.dump(o, open(p, 'w'), indent=1)

def cmd_new(a):
    d = rdir(a.slug)
    if os.path.exists(d) and not a.force:
        sys.exit(f"{d} exists (use --force)")
    os.makedirs(d, exist_ok=True)
    jdump(os.path.join(d, 'script.meta.json'), {
        'slug': a.slug, 'hint': a.hint, 'created': datetime.now().isoformat(timespec='seconds'),
        'hook_pattern': a.hook, 'target_seconds': a.target, 'status': 'drafting'})
    if not os.path.exists(os.path.join(d, 'script.md')):
        open(os.path.join(d, 'script.md'), 'w').write(
            f"<!-- hint: {a.hint} -->\n<!-- keep one idea per sentence; the animation needs a cue per beat -->\n\n")
    print(f"scaffolded {d}\nnext: draft 2-3 openings, then save the final into script.md")

def cmd_audio(a):
    d = rdir(a.slug)
    if not os.path.isdir(d): sys.exit(f"no such reel: {a.slug}")
    ext = os.path.splitext(a.file)[1].lstrip('.') or 'mp3'
    shutil.copy(a.file, os.path.join(d, f'audio.{ext}'))
    dur = subprocess.run(['ffprobe','-v','error','-show_entries','format=duration',
                          '-of','csv=p=0', a.file], capture_output=True, text=True).stdout.strip()
    meta = {k: v for k, v in {
        'source': os.path.basename(a.file), 'duration': round(float(dur), 2),
        'provider': a.provider, 'voice': a.voice, 'model': a.model,
        'stability': a.stability, 'similarity': a.similarity,
        'style': a.style, 'speed': a.speed, 'notes': a.notes,
        'logged': datetime.now().isoformat(timespec='seconds')}.items() if v is not None}
    jdump(os.path.join(d, 'audio.meta.json'), meta)
    print(f"audio {meta['duration']}s logged for {a.slug}")
    print("next: align.py reels/%s" % a.slug)

def cmd_publish(a):
    d = rdir(a.slug)
    p = os.path.join(d, 'publish.json')
    all_ = jload(p, {})
    all_[a.platform] = {k: v for k, v in {
        'posted_at': a.at, 'caption': a.caption, 'hashtags': a.hashtags,
        'url': a.url, 'logged': datetime.now().isoformat(timespec='seconds')}.items() if v}
    jdump(p, all_)
    print(f"{a.slug} logged as posted to {a.platform} at {a.at}")

PERF_FIELDS = ['views','reach','likes','comments','shares','saves','avg_watch','follows',
               'profile_visits','hold3','impressions','ctr','avg_view','pct_viewed',
               'subs','swipe_away']

def cmd_perf(a):
    d = rdir(a.slug)
    p = os.path.join(d, 'performance.json')
    rows = jload(p, [])
    row = {'platform': a.platform, 'at': datetime.now().isoformat(timespec='seconds')}
    for f in PERF_FIELDS:
        v = getattr(a, f)
        if v is not None: row[f] = v
    pub = jload(os.path.join(d, 'publish.json'), {}).get(a.platform, {})
    if pub.get('posted_at'):
        try:
            t0 = datetime.fromisoformat(pub['posted_at'].replace(' ', 'T'))
            row['hours_after_post'] = round((datetime.now() - t0).total_seconds()/3600, 1)
        except Exception: pass
    rows.append(row)
    jdump(p, rows)
    print(f"logged {a.platform} reading for {a.slug}"
          + (f" ({row['hours_after_post']}h after post)" if 'hours_after_post' in row else ""))

def cmd_rate(a):
    rates = []
    for s in sorted(os.listdir(REELS)) if os.path.isdir(REELS) else []:
        c = jload(os.path.join(rdir(s), 'cues.json'))
        if c and c.get('wps'): rates.append((s, c['wps']))
    if not rates:
        print("no aligned reels yet; assume ~2.5 words/sec"); return
    vals = [r for _, r in rates]
    for s, r in rates: print(f"  {r:5.2f} w/s  {s}")
    print(f"\nmean {st.mean(vals):.2f} w/s -> ~{st.mean(vals)*60:.0f} wpm")
    print(f"a 60s reel is about {st.mean(vals)*60:.0f} words")

def cmd_gaps(a):
    """Dead air = stretches with no NEW event and no continuous motion.

    A scene with a start/end span (a rule drawing, a scan sweeping, a URL typing)
    covers its whole interval - counting only its endpoints reported false gaps."""
    d = rdir(a.slug)
    tl = jload(os.path.join(d, 'timeline.json'))
    if not tl: sys.exit("no timeline.json yet")
    SPAN = [('start','end'), ('in','out'), ('flyStart','flyEnd'), ('urlStart','urlEnd')]
    POINT = ('at','click','clickAt','addAt','strike')
    covered, points = [], []
    for sc in tl.get('scenes', []):
        for s0, e0 in SPAN:
            if isinstance(sc.get(s0),(int,float)) and isinstance(sc.get(e0),(int,float)):
                covered.append((float(sc[s0]), float(sc[e0])))
        for k in POINT:
            v = sc.get(k)
            if isinstance(v,(int,float)): points.append(float(v))
            elif isinstance(v, list):
                points += [float(x) for x in v if isinstance(x,(int,float))]
        for l in (sc.get('lines') or []):
            if isinstance(l, dict) and 'start' in l and 'end' in l:
                covered.append((float(l['start']), float(l['end'])))
    total = float(tl.get('total') or 0)
    # a point event holds attention briefly
    for p_ in points: covered.append((p_, p_ + a.hold))
    covered.sort()
    merged = []
    for s0, e0 in covered:
        if merged and s0 <= merged[-1][1] + 1e-6: merged[-1][1] = max(merged[-1][1], e0)
        else: merged.append([s0, e0])
    print(f"{len(tl.get('scenes',[]))} scenes, {len(merged)} active stretches across {total}s")
    gaps, cur = [], 0.0
    for s0, e0 in merged:
        if s0 - cur > a.max_gap: gaps.append((cur, s0))
        cur = max(cur, e0)
    if total - cur > a.max_gap: gaps.append((cur, total))
    active = sum(min(e0,total)-max(s0,0) for s0,e0 in merged)
    print(f"active {active/total*100:.0f}% of runtime" if total else "")
    if not gaps:
        print(f"no dead air over {a.max_gap}s - good"); return
    print(f"\ndead air over {a.max_gap}s:")
    for s0, e0 in gaps: print(f"  {s0:6.2f} -> {e0:6.2f}   ({e0-s0:.1f}s nothing happening)")
    print("\nfill with: a flip wave, counter tick, scan sweep, pullback, or a pointer visit")

def _num(x):
    try: return float(x)
    except Exception: return None

def cmd_report(a):
    reels = []
    for s in sorted(os.listdir(REELS)) if os.path.isdir(REELS) else []:
        d = rdir(s)
        if not os.path.isdir(d): continue
        meta = jload(os.path.join(d,'script.meta.json'), {})
        cues = jload(os.path.join(d,'cues.json'), {})
        aud  = jload(os.path.join(d,'audio.meta.json'), {})
        pub  = jload(os.path.join(d,'publish.json'), {})
        perf = jload(os.path.join(d,'performance.json'), [])
        if not perf: continue
        latest = {}
        for r in perf: latest[r['platform']] = r
        for plat, r in latest.items():
            reach = _num(r.get('reach')) or _num(r.get('views'))
            dur = cues.get('duration') or aud.get('duration')
            row = {'slug': s, 'platform': plat, 'hook': meta.get('hook_pattern'),
                   'words': len(cues.get('words', [])) or None, 'dur': dur,
                   'voice': aud.get('voice'), 'reach': reach,
                   'share_rate': (_num(r.get('shares'))/reach*100) if reach and r.get('shares') is not None else None,
                   'save_rate': (_num(r.get('saves'))/reach*100) if reach and r.get('saves') is not None else None,
                   'follow_rate': (_num(r.get('follows'))/reach*100) if reach and r.get('follows') is not None else None,
                   'watch_pct': (_num(r.get('avg_watch'))/dur*100) if dur and r.get('avg_watch') is not None
                                else _num(r.get('pct_viewed')),
                   'hold3': _num(r.get('hold3')),
                   'posted': (pub.get(plat) or {}).get('posted_at')}
            reels.append(row)
    if not reels:
        print("no performance logged yet.\nlog one with: reel.py perf <slug> --platform instagram --views ... --reach ...")
        return
    hdr = f"{'reel':22s} {'plat':9s} {'reach':>8s} {'shr%':>6s} {'sav%':>6s} {'fol%':>6s} {'watch%':>7s} {'hold3':>6s}  hook"
    print(hdr); print('-'*len(hdr))
    for r in sorted(reels, key=lambda x: -(x['reach'] or 0)):
        f = lambda v, p='.2f': (format(v, p) if v is not None else '-')
        print(f"{r['slug'][:22]:22s} {r['platform'][:9]:9s} {str(int(r['reach'])) if r['reach'] else '-':>8s} "
              f"{f(r['share_rate']):>6s} {f(r['save_rate']):>6s} {f(r['follow_rate']):>6s} "
              f"{f(r['watch_pct'],'.1f'):>7s} {f(r['hold3'],'.0f'):>6s}  {r['hook'] or '-'}")
    if len(reels) < 5:
        print(f"\nonly {len(reels)} logged reading(s). Too few to infer anything - "
              "report raw numbers to the user, do not claim a trend.")
        return
    print("\nby hook pattern (mean reach):")
    byh = {}
    for r in reels:
        if r['hook'] and r['reach']: byh.setdefault(r['hook'], []).append(r['reach'])
    for k, v in sorted(byh.items(), key=lambda kv: -st.mean(kv[1])):
        print(f"  {k:24s} {st.mean(v):9.0f}  (n={len(v)})")
    print("\nby posting hour (mean reach):")
    byt = {}
    for r in reels:
        if r['posted'] and r['reach']:
            try: byt.setdefault(int(r['posted'].replace(' ','T').split('T')[1][:2]), []).append(r['reach'])
            except Exception: pass
    for k, v in sorted(byt.items(), key=lambda kv: -st.mean(kv[1])):
        print(f"  {k:02d}:00 {st.mean(v):9.0f}  (n={len(v)})")
    print("\nread performance-playbook.md before deciding what to change.")

def cmd_list(a):
    if not os.path.isdir(REELS): print("no reels yet"); return
    for s in sorted(os.listdir(REELS)):
        d = rdir(s)
        if not os.path.isdir(d): continue
        have = [n for n, f in [('script','script.md'), ('audio','audio.meta.json'),
                ('cues','cues.json'), ('timeline','timeline.json'),
                ('html','reel.html'), ('mp4','reel.mp4'), ('posted','publish.json'),
                ('perf','performance.json')] if os.path.exists(os.path.join(d, f))]
        print(f"  {s:26s} {' > '.join(have) if have else '(empty)'}")

def main():
    ap = argparse.ArgumentParser(); sub = ap.add_subparsers(dest='cmd', required=True)
    n = sub.add_parser('new'); n.add_argument('slug'); n.add_argument('--hint', required=True)
    n.add_argument('--hook'); n.add_argument('--target', type=float); n.add_argument('--force', action='store_true')
    n.set_defaults(fn=cmd_new)
    au = sub.add_parser('audio'); au.add_argument('slug'); au.add_argument('--file', required=True)
    for f in ['provider','voice','model','notes']: au.add_argument('--'+f)
    for f in ['stability','similarity','style','speed']: au.add_argument('--'+f, type=float)
    au.set_defaults(fn=cmd_audio)
    pb = sub.add_parser('publish'); pb.add_argument('slug'); pb.add_argument('--platform', required=True)
    for f in ['at','caption','hashtags','url']: pb.add_argument('--'+f)
    pb.set_defaults(fn=cmd_publish)
    pf = sub.add_parser('perf'); pf.add_argument('slug'); pf.add_argument('--platform', required=True)
    for f in PERF_FIELDS: pf.add_argument('--'+f.replace('_','-'), dest=f, type=float)
    pf.set_defaults(fn=cmd_perf)
    g = sub.add_parser('gaps'); g.add_argument('slug'); g.add_argument('--max-gap', type=float, default=4.0)
    g.add_argument('--hold', type=float, default=1.2)
    g.set_defaults(fn=cmd_gaps)
    sub.add_parser('rate').set_defaults(fn=cmd_rate)
    sub.add_parser('report').set_defaults(fn=cmd_report)
    sub.add_parser('list').set_defaults(fn=cmd_list)
    a = ap.parse_args(); a.fn(a)

if __name__ == '__main__':
    main()
