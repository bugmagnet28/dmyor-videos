"""Add packaged reels to studio/schedule.json in the next free posting slots (the publisher posts from that file).

    python3 studio/tools/schedule_add.py ready-to-post/<date>-<slug> [more folders...]
Slots per day come from schedule.json "slots" (IST). A reel is never placed earlier than tomorrow's first slot when it
is added after 12:00, so the publisher always has lead time. Captions are read from each folder's post.md."""
import json, os, re, sys, datetime as dt
ROOT = os.getcwd(); P = os.path.join(ROOT, "studio/schedule.json")
S = json.load(open(P)); S.setdefault("slots", ["09:30", "13:00", "16:30", "19:30", "22:00"])
def sec(s, name):
    m = re.search(r"^## " + name + r"\s*\n(.*?)(?=^## |\Z)", s, re.S | re.M); return m.group(1).strip() if m else ""
def x_trim(t):
    while len(t) > 270 and "\n\n" in t: t = t.rsplit("\n\n", 1)[0]
    return t[:270]
taken = {o["when_ist"] for o in S["items"]}
now = dt.datetime.now(); day = now.date() + dt.timedelta(days=1 if now.hour >= 12 else 0)
def next_slot():
    global day
    while True:
        for sl in S["slots"]:
            w = f"{day} {sl}"
            if sum(1 for t in taken if t.startswith(str(day))) >= len(S["slots"]): break
            if w not in taken and dt.datetime.strptime(w, "%Y-%m-%d %H:%M") > now + dt.timedelta(hours=3): taken.add(w); return w
        day += dt.timedelta(days=1)
for folder in sys.argv[1:]:
    folder = folder.rstrip("/"); s = open(os.path.join(folder, "post.md")).read()
    if any(o["folder"] == folder for o in S["items"]): print("already scheduled:", folder); continue
    ig = sec(s, "Instagram caption") or (sec(s, "Caption") + ("\n\n" + sec(s, "Hashtags") if sec(s, "Hashtags") else ""))
    yt = sec(s, "YouTube"); title = (re.search(r"Title:\s*(.+)", yt) or [None, ""])[1].strip(); desc = (re.search(r"Description:\s*(.+)", yt) or [None, ""])[1].strip()
    if not desc: desc = (ig.split("\n\n")[1] if "\n\n" in ig else ig[:300]) + " dmyor.com"
    v = os.path.join(folder, "video.mp4"); w = next_slot()
    S["items"].append(dict(when_ist=w, folder=folder, video=v, size_mb=round(os.path.getsize(v) / 1e6, 1), ig_caption=ig, x_text=x_trim(sec(s, "X")), yt_title=title, yt_desc=desc, ig="todo", x="todo", yt="todo"))
    print(w, folder)
S["items"].sort(key=lambda o: o["when_ist"]); json.dump(S, open(P, "w"), indent=1, ensure_ascii=False)
