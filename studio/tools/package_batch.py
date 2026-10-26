"""Package a day's batch: package_batch.py <date YYYY-MM-DD> <slug>=<time label> ... (e.g. ill-save-first="Tue Oct 27, 09:30 IST").
Reads reels/<slug>/{narration,script.meta}.json + reel.mp4 -> ready-to-post/<date>-<slug>/{video.mp4,post.md}."""
import json,sys,shutil,os,subprocess
date=sys.argv[1];times=dict(a.split("=",1) for a in sys.argv[2:])
for s in times:
    n=json.load(open(f"reels/{s}/narration.json"));m=json.load(open(f"reels/{s}/script.meta.json"));c=n["caption"]
    src=f"reels/{s}/reel.mp4";dur=float(subprocess.run(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",src],capture_output=True,text=True).stdout)
    d=f"ready-to-post/{date}-{s}";os.makedirs(d,exist_ok=True);shutil.copy(src,f"{d}/video.mp4")
    q=m["quality"]
    open(f"{d}/post.md","w").write(f"""# {s} ({m['style']}, {dur:.1f}s, voice am_eric, @becauseidmyor)

## Caption
{c['instagram']}

## Hashtags
{c['hashtags']}

## X
{c['x']}

## YouTube
Title: {c['youtube_title']}

## Suggested time
{times.get(s,'')} (≥ 3h from the other reels of the batch). Same time on X and YouTube Shorts.

## Cover
Frame 0 (the hook is fully drawn at 0.0s).

## Experiment
{m.get('experiment','')}. {m['note']}

## Quality score
hook {q['hook']} · usefulness {q['usefulness']} · specificity {q['specificity']} · clarity {q['clarity']} · retention {q['retention']} · craft {q['craft']} · voice {q['voice']} · brand {q['brand']} = **{q['total']}/40**

## Spoken script
{n['spoken'].replace('||',chr(10)+chr(10)).replace('[hook] ','').replace('[turn] ','').replace('[land] ','').replace('[outro] ','')}

## Status
Waiting for Sanyam's approval (batch message {date}). Not scheduled.
""")
    print(d,round(dur,2))
