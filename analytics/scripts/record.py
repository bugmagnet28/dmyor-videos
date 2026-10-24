"""Write content-performance data into analytics/ (the only way agents should write it).

  # 1. register a posted piece of content (once per platform)
  python3 analytics/scripts/record.py content --platform instagram --slug someday-is-not-a-day \
      --url https://www.instagram.com/reel/Devf-yOz9AS/ --posted "2026-10-21 09:30" \
      --style kinetic-typography --hook-type hard-truth --topic procrastination --length 12.8

  # 2. log a metrics snapshot for it (goes to daily/<date>/<platform>.csv, one row per post per day)
  python3 analytics/scripts/record.py metrics --platform instagram --slug someday-is-not-a-day \
      --captured "2026-10-22 19:40" --views 74 --reach 65 --nonfollower-pct 100 --likes 0 --saves 1 --self-saves 1 \
      --source web-insights

  # 3. log follower counts
  python3 analytics/scripts/record.py account --platform instagram --followers 21 --posts 33 --captured "2026-10-22 19:40"

  # batch: a JSON list of {"kind": "content"|"metrics"|"account", ...same field names with underscores...}
  python3 analytics/scripts/record.py batch file.json

Re-recording the same post on the same day replaces that row (so a later reading wins).
Then run:  analytics/.venv/bin/python analytics/scripts/build.py
"""
import argparse, csv, json, os, sys
from datetime import datetime

A = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CATALOG = os.path.join(A, "catalog", "content.csv")
CONTENT_COLS = ["content_id", "platform", "slug", "url", "posted_at_ist", "kind", "style", "hook_type", "topic",
                "narrated", "voice", "length_s", "cta", "experiment", "notes"]
METRIC_COLS = ["content_id", "slug", "captured_at_ist", "age_h", "views", "reach", "nonfollower_pct", "likes",
               "comments", "shares", "saves", "self_saves", "follows", "profile_visits", "link_clicks",
               "avg_watch_s", "watched_pct", "skip_rate_pct", "source", "note"]
ACCOUNT_COLS = ["platform", "account", "captured_at_ist", "followers", "posts", "source"]
PLATFORMS = ["instagram", "youtube", "x"]
ACCOUNTS = {"instagram": "@becauseidmyor", "youtube": "Dmyor (UC-EN3-xvVXtzgob7WybfS6g)", "x": "@becauseidmyor"}


def read(path, cols):
    if not os.path.exists(path):
        return []
    with open(path, newline="") as f:
        return list(csv.DictReader(f))


def write(path, cols, rows):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore")
        w.writeheader()
        for r in rows:
            w.writerow({c: r.get(c, "") for c in cols})


def ts(s):
    return datetime.strptime(s, "%Y-%m-%d %H:%M")


def cid(platform, slug):
    return f"{platform}:{slug}"


def content(o):
    rows = read(CATALOG, CONTENT_COLS)
    r = {k: v for k, v in o.items() if v not in (None, "")}
    r["content_id"] = cid(o["platform"], o["slug"])
    r.setdefault("kind", "video")
    rows = [x for x in rows if x["content_id"] != r["content_id"]] + [r]
    rows.sort(key=lambda x: (x.get("posted_at_ist", ""), x["platform"]))
    write(CATALOG, CONTENT_COLS, rows)
    print("content", r["content_id"])


def metrics(o):
    if o["platform"] not in PLATFORMS:
        sys.exit(f"platform must be one of {PLATFORMS}")
    day = o["captured"][:10]
    path = os.path.join(A, "daily", day, f"{o['platform']}.csv")
    r = {k: v for k, v in o.items() if v not in (None, "")}
    r["content_id"] = cid(o["platform"], o["slug"])
    r["captured_at_ist"] = o["captured"]
    if not r.get("age_h"):
        cat = {x["content_id"]: x for x in read(CATALOG, CONTENT_COLS)}
        p = cat.get(r["content_id"], {}).get("posted_at_ist")
        if p:
            r["age_h"] = round((ts(o["captured"]) - ts(p)).total_seconds() / 3600, 1)
        else:
            print(f"warning: {r['content_id']} not in catalog; register it with `record.py content` (age unknown)")
    rows = [x for x in read(path, METRIC_COLS) if x["content_id"] != r["content_id"]] + [r]
    write(path, METRIC_COLS, rows)
    print("metrics", day, r["content_id"], "views", r.get("views", "?"), "age_h", r.get("age_h", "?"))


def account(o):
    day = o["captured"][:10]
    path = os.path.join(A, "daily", day, "account.csv")
    r = {k: v for k, v in o.items() if v not in (None, "")}
    r["captured_at_ist"] = o["captured"]
    r.setdefault("account", ACCOUNTS.get(o["platform"], ""))
    rows = [x for x in read(path, ACCOUNT_COLS) if x["platform"] != o["platform"]] + [r]
    write(path, ACCOUNT_COLS, rows)
    print("account", day, o["platform"], r.get("followers"))


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("content")
    for f in ["platform", "slug"]:
        c.add_argument("--" + f, required=True)
    for f in ["url", "posted", "kind", "style", "hook-type", "topic", "narrated", "voice", "length", "cta", "experiment", "notes"]:
        c.add_argument("--" + f)
    m = sub.add_parser("metrics")
    for f in ["platform", "slug", "captured"]:
        m.add_argument("--" + f, required=True)
    for f in ["age-h", "views", "reach", "nonfollower-pct", "likes", "comments", "shares", "saves", "self-saves",
              "follows", "profile-visits", "link-clicks", "avg-watch-s", "watched-pct", "skip-rate-pct", "source", "note"]:
        m.add_argument("--" + f)
    ac = sub.add_parser("account")
    for f in ["platform", "captured", "followers"]:
        ac.add_argument("--" + f, required=True)
    for f in ["posts", "account", "source"]:
        ac.add_argument("--" + f)
    b = sub.add_parser("batch"); b.add_argument("file")
    a = ap.parse_args()
    norm = lambda d: {k.replace("-", "_"): v for k, v in d.items()}
    if a.cmd == "batch":
        for item in json.load(open(a.file)):
            item = norm(item); kind = item.pop("kind_of_record", None) or item.pop("record")
            {"content": lambda x: content(fix_content(x)), "metrics": metrics, "account": account}[kind](item)
        return
    d = norm(vars(a)); d.pop("cmd")
    if a.cmd == "content":
        content(fix_content(d))
    elif a.cmd == "metrics":
        metrics(d)
    else:
        account(d)


def fix_content(d):
    d = dict(d)
    if "posted" in d:
        d["posted_at_ist"] = d.pop("posted")
    if "length" in d:
        d["length_s"] = d.pop("length")
    return d


if __name__ == "__main__":
    main()
