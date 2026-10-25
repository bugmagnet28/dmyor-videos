import json,sys,shutil,os,subprocess
date="2026-10-26"
times={"ill-night-before":"Mon Oct 26, 09:30 IST","kt-later-trigger":"Mon Oct 26, 13:00 IST","ill-track-inputs":"Mon Oct 26, 16:30 IST","kt-five-goals":"Mon Oct 26, 19:30 IST"}
for s in sys.argv[1:]:
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
V-EXP-28 (same-day style split, hard-truth behaviour hooks). {m['note']}

## Quality score
hook {q['hook']} · usefulness {q['usefulness']} · specificity {q['specificity']} · clarity {q['clarity']} · retention {q['retention']} · craft {q['craft']} · voice {q['voice']} · brand {q['brand']} = **{q['total']}/40**

## Spoken script
{n['spoken'].replace('||',chr(10)+chr(10)).replace('[hook] ','').replace('[turn] ','').replace('[land] ','').replace('[outro] ','')}

## Status
Waiting for Sanyam's approval (batch message 2026-10-25). Not scheduled.
""")
    print(d,round(dur,2))
