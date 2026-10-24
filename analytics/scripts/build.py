"""Rebuild every human-readable report and chart from the raw data. Safe to run any time.

    analytics/.venv/bin/python analytics/scripts/build.py

Reads   catalog/content.csv, daily/<date>/{instagram,youtube,x,account}.csv
Writes  daily/<date>/SUMMARY.md               (one per collection day)
        reports/OVERALL.md                     (progress + leaderboard + charts, start here)
        reports/WHAT_WORKED.md                 (trait comparisons)
        reports/latest_by_post.csv             (every post: latest + 48h checkpoint + traction)
        reports/charts/*.png
Definitions: METRICS.md
"""
import csv, os, statistics as st
from collections import defaultdict
from datetime import datetime, timedelta

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

A = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
R = os.path.join(A, "reports"); C = os.path.join(R, "charts")
PLAT = ["instagram", "youtube", "x"]
PCOL = {"instagram": "#E1306C", "youtube": "#FF0000", "x": "#1D9BF0"}
STYLE_COL = {}
PALETTE = ["#FF7A1A", "#3DDC97", "#7B61FF", "#1D9BF0", "#E1306C", "#F5C542", "#8B909A", "#00B8A9"]
NOW = datetime.now()


def read(p):
    if not os.path.exists(p):
        return []
    with open(p, newline="") as f:
        return list(csv.DictReader(f))


def num(x):
    try:
        return float(x) if x not in (None, "") else None
    except ValueError:
        return None


def ts(s):
    return datetime.strptime(s, "%Y-%m-%d %H:%M")


def fmt(x, d=0):
    if x is None:
        return "–"
    return f"{x:,.{d}f}"


def scol(style):
    if style not in STYLE_COL:
        STYLE_COL[style] = PALETTE[len(STYLE_COL) % len(PALETTE)]
    return STYLE_COL[style]


# ---------------------------------------------------------------- load
catalog = {r["content_id"]: r for r in read(os.path.join(A, "catalog", "content.csv"))}
days = sorted(d for d in os.listdir(os.path.join(A, "daily")) if len(d) == 10 and d[4] == "-") if os.path.isdir(os.path.join(A, "daily")) else []
snaps = defaultdict(list)       # content_id -> [row,...]
accounts = defaultdict(list)    # platform -> [row,...]
per_day = defaultdict(dict)     # day -> platform -> rows
for d in days:
    for p in PLAT:
        rows = read(os.path.join(A, "daily", d, f"{p}.csv"))
        per_day[d][p] = rows
        for r in rows:
            r["_platform"] = p; r["_day"] = d
            for k in ["age_h", "views", "reach", "nonfollower_pct", "likes", "comments", "shares", "saves", "self_saves",
                      "follows", "profile_visits", "link_clicks", "avg_watch_s", "watched_pct", "skip_rate_pct"]:
                r[k] = num(r.get(k))
            snaps[r["content_id"]].append(r)
    for r in read(os.path.join(A, "daily", d, "account.csv")):
        r["followers"] = num(r.get("followers")); r["_day"] = d
        accounts[r["platform"]].append(r)
for v in snaps.values():
    v.sort(key=lambda r: r["captured_at_ist"])


def derive(r, cat):
    base = r["reach"] if r.get("reach") else r.get("views")
    out = {"reach_or_views": base}
    L = num(cat.get("length_s")) if cat else None
    ret = r.get("watched_pct")
    if ret is None and r.get("avg_watch_s") is not None and L:
        ret = min(100.0, r["avg_watch_s"] / L * 100)
    out["retention"] = ret
    if base:
        z = lambda k: r.get(k) or 0
        saves = max(0.0, z("saves") - z("self_saves"))
        out["eng_per_1k"] = (z("likes") + z("comments") + z("shares") + saves) / base * 1000
        out["shares_per_1k"] = z("shares") / base * 1000
        out["saves_per_1k"] = saves / base * 1000
        out["follows_per_1k"] = z("follows") / base * 1000
    return out


def checkpoint(rows, lo, hi, target):
    c = [r for r in rows if r.get("age_h") is not None and lo <= r["age_h"] <= hi]
    return min(c, key=lambda r: abs(r["age_h"] - target)) if c else None


posts = []
for cid_, rows in snaps.items():
    cat = catalog.get(cid_, {})
    latest = rows[-1]
    c48 = checkpoint(rows, 24, 96, 48)
    c7d = checkpoint(rows, 150, 200, 168)
    p = {"content_id": cid_, "platform": latest["_platform"], "slug": latest["slug"], "cat": cat, "latest": latest,
         "c48": c48, "c7d": c7d, "d_latest": derive(latest, cat), "d48": derive(c48, cat) if c48 else None}
    posts.append(p)


def pct_rank(vals, v):
    vals = [x for x in vals if x is not None]
    if v is None or not vals:
        return None
    below = sum(1 for x in vals if x < v); eq = sum(1 for x in vals if x == v)
    return (below + 0.5 * eq) / len(vals) * 100


for plat in PLAT:
    ps = [p for p in posts if p["platform"] == plat and p["d48"]]
    cols = {
        "reach": [p["d48"]["reach_or_views"] for p in ps],
        "ret": [p["d48"]["retention"] for p in ps],
        "ss": [(p["d48"].get("shares_per_1k") or 0) + (p["d48"].get("saves_per_1k") or 0) for p in ps],
        "fol": [p["d48"].get("follows_per_1k") for p in ps],
    }
    for i, p in enumerate(ps):
        parts = [(0.40, pct_rank(cols["reach"], cols["reach"][i])),
                 (0.25, pct_rank(cols["ret"], cols["ret"][i])),
                 (0.20, pct_rank(cols["ss"], cols["ss"][i])),
                 (0.15, pct_rank(cols["fol"], cols["fol"][i]))]
        parts = [(w, v) for w, v in parts if v is not None]
        p["traction"] = sum(w * v for w, v in parts) / sum(w for w, _ in parts) if parts else None


def label(p):
    return p["slug"][:28]


# ---------------------------------------------------------------- daily summaries
prev_followers = {}
for d in days:
    out = [f"# {d} · content performance snapshot", "",
           f"_Generated by `scripts/build.py`. Raw data: the CSV files in this folder. Definitions: [METRICS.md](../../METRICS.md)._", ""]
    acc = read(os.path.join(A, "daily", d, "account.csv"))
    if acc:
        out += ["## Accounts", "", "| Platform | Account | Followers | Change since last reading | Posts |", "|---|---|---|---|---|"]
        for a in acc:
            f = num(a.get("followers")); pf = prev_followers.get(a["platform"])
            ch = "–" if pf is None or f is None else f"{f - pf:+.0f}"
            out.append(f"| {a['platform']} | {a.get('account','')} | {fmt(f)} | {ch} | {a.get('posts','')} |")
            if f is not None:
                prev_followers[a["platform"]] = f
        out.append("")
    for plat in PLAT:
        rows = per_day[d].get(plat) or []
        if not rows:
            continue
        rows = sorted(rows, key=lambda r: -(r["views"] or 0))
        tv = sum(r["views"] or 0 for r in rows)
        out += [f"## {plat.capitalize()} ({len(rows)} posts, {fmt(tv)} views total)", "",
                "| Post | Age (h) | Views | Reach | Non-followers | Likes | Comments | Shares | Saves | Follows | Watched % | Source |",
                "|---|---|---|---|---|---|---|---|---|---|---|---|"]
        for r in rows:
            cat = catalog.get(r["content_id"], {})
            dr = derive(r, cat)
            link = f"[{r['slug']}]({cat['url']})" if cat.get("url") else r["slug"]
            out.append(f"| {link} | {fmt(r['age_h'])} | {fmt(r['views'])} | {fmt(r['reach'])} | "
                       f"{fmt(r['nonfollower_pct'])}{'%' if r['nonfollower_pct'] is not None else ''} | {fmt(r['likes'])} | "
                       f"{fmt(r['comments'])} | {fmt(r['shares'])} | {fmt(r['saves'])}{' (self ' + fmt(r['self_saves']) + ')' if r['self_saves'] else ''} | "
                       f"{fmt(r['follows'])} | {fmt(dr['retention'])} | {r.get('source','')} |")
        notes = [f"- **{r['slug']}**: {r['note']}" for r in rows if r.get("note")]
        out += [""] + (["Notes:"] + notes + [""] if notes else [])
    open(os.path.join(A, "daily", d, "SUMMARY.md"), "w").write("\n".join(out) + "\n")

# ---------------------------------------------------------------- latest_by_post.csv
os.makedirs(C, exist_ok=True)
cols = ["content_id", "platform", "slug", "posted_at_ist", "style", "hook_type", "topic", "narrated", "length_s",
        "latest_captured", "latest_age_h", "latest_views", "latest_reach", "views_48h", "reach_48h", "age_48h",
        "retention_48h", "shares_per_1k_48h", "saves_per_1k_48h", "follows_per_1k_48h", "traction", "views_7d"]
with open(os.path.join(R, "latest_by_post.csv"), "w", newline="") as f:
    w = csv.writer(f); w.writerow(cols)
    for p in sorted(posts, key=lambda p: (p["platform"], p["cat"].get("posted_at_ist", ""))):
        c, L, c48, d48 = p["cat"], p["latest"], p["c48"], p["d48"]
        w.writerow([p["content_id"], p["platform"], p["slug"], c.get("posted_at_ist", ""), c.get("style", ""),
                    c.get("hook_type", ""), c.get("topic", ""), c.get("narrated", ""), c.get("length_s", ""),
                    L["captured_at_ist"], L["age_h"], L["views"], L["reach"],
                    c48["views"] if c48 else "", c48["reach"] if c48 else "", c48["age_h"] if c48 else "",
                    round(d48["retention"], 1) if d48 and d48["retention"] is not None else "",
                    round(d48.get("shares_per_1k", 0), 1) if d48 else "", round(d48.get("saves_per_1k", 0), 1) if d48 else "",
                    round(d48.get("follows_per_1k", 0), 1) if d48 else "",
                    round(p["traction"]) if p.get("traction") is not None else "",
                    p["c7d"]["views"] if p["c7d"] else ""])

# ---------------------------------------------------------------- charts
plt.rcParams.update({"figure.dpi": 130, "axes.spines.top": False, "axes.spines.right": False, "font.size": 9,
                     "axes.titleweight": "bold", "axes.titlesize": 11})
charts = []


def save(name, title):
    plt.tight_layout(); plt.savefig(os.path.join(C, name)); plt.close(); charts.append((name, title))


# 1 followers over time
if any(accounts.values()):
    plt.figure(figsize=(7, 3.2))
    for plat, rows in accounts.items():
        rows = sorted([r for r in rows if r["followers"] is not None], key=lambda r: r["captured_at_ist"])
        if rows:
            plt.plot([ts(r["captured_at_ist"]) for r in rows], [r["followers"] for r in rows], marker="o",
                     color=PCOL.get(plat, "#555"), label=plat)
    plt.title("Followers over time"); plt.legend(frameon=False); plt.gcf().autofmt_xdate()
    save("followers.png", "Followers over time (are we growing?)")

# 2 reach at 48h per post, in posting order (progress)
for plat in PLAT:
    ps = [p for p in posts if p["platform"] == plat and p["d48"] and p["cat"].get("posted_at_ist")]
    if not ps:
        continue
    ps.sort(key=lambda p: p["cat"]["posted_at_ist"])
    vals = [p["d48"]["reach_or_views"] or 0 for p in ps]
    plt.figure(figsize=(max(7, 0.45 * len(ps) + 2), 3.8))
    plt.bar(range(len(ps)), vals, color=[scol(p["cat"].get("style", "?")) for p in ps])
    roll = [st.median(vals[max(0, i - 2): i + 1]) for i in range(len(vals))]
    plt.plot(range(len(ps)), roll, color="#111", lw=1.5, label="rolling median (last 3 posts)")
    plt.xticks(range(len(ps)), [label(p) for p in ps], rotation=60, ha="right", fontsize=7)
    plt.ylabel("reach (or views) at ~48h")
    plt.title(f"{plat.capitalize()}: reach at 48h by post, oldest → newest")
    handles = [plt.Rectangle((0, 0), 1, 1, color=c) for c in STYLE_COL.values()]
    plt.legend(handles + [plt.Line2D([0], [0], color="#111")], list(STYLE_COL.keys()) + ["rolling median"],
               frameon=False, fontsize=7, loc="upper left")
    save(f"{plat}_reach48_by_post.png", f"{plat.capitalize()}: reach at 48h per post, in posting order (bars coloured by style)")

# 3 views per collection day (total across posts) per platform
daily_tot = defaultdict(dict)
for d in days:
    for plat in PLAT:
        rows = per_day[d].get(plat) or []
        if rows:
            daily_tot[plat][d] = sum(r["views"] or 0 for r in rows)
if daily_tot:
    plt.figure(figsize=(7, 3.2))
    for plat, m in daily_tot.items():
        ds = sorted(m)
        plt.plot([datetime.strptime(x, "%Y-%m-%d") for x in ds], [m[x] for x in ds], marker="o", color=PCOL[plat], label=plat)
    plt.title("Total views of tracked posts, per snapshot day"); plt.legend(frameon=False); plt.gcf().autofmt_xdate()
    save("views_per_snapshot_day.png", "Total views across tracked posts, per snapshot day")


# 4 trait comparisons (instagram has the most data; one chart per trait, all platforms combined by platform)
def group_chart(trait, title):
    for plat in PLAT:
        ps = [p for p in posts if p["platform"] == plat and p["d48"]]
        g = defaultdict(list)
        for p in ps:
            g[p["cat"].get(trait) or "unknown"].append(p["d48"]["reach_or_views"] or 0)
        if len(g) < 2:
            continue
        items = sorted(g.items(), key=lambda kv: -st.median(kv[1]))
        plt.figure(figsize=(7, 0.42 * len(items) + 1.2))
        plt.barh([f"{k} (n={len(v)})" for k, v in items][::-1], [st.median(v) for _, v in items][::-1], color=PCOL[plat])
        plt.xlabel("median reach at 48h"); plt.title(f"{plat.capitalize()}: {title}")
        save(f"{plat}_by_{trait}.png", f"{plat.capitalize()}: median reach at 48h by {title.lower()}")


group_chart("style", "Style")
group_chart("hook_type", "Hook type")
group_chart("topic", "Topic")
for p in posts:
    pa = p["cat"].get("posted_at_ist")
    p["cat"]["post_hour"] = f"{pa[11:13]}:00 IST" if pa else "unknown"
    L = num(p["cat"].get("length_s"))
    p["cat"]["length_bucket"] = "unknown" if L is None else ("<15s" if L < 15 else "15-20s" if L < 20 else "20-30s" if L <= 30 else ">30s")
group_chart("post_hour", "Posting hour")

# 5 engagement rates per post (instagram)
for plat in PLAT:
    ps = [p for p in posts if p["platform"] == plat and p["d48"] and p["d48"].get("eng_per_1k") is not None]
    if len(ps) < 2:
        continue
    ps.sort(key=lambda p: p["cat"].get("posted_at_ist", ""))
    x = range(len(ps)); wdt = 0.27
    plt.figure(figsize=(max(7, 0.45 * len(ps) + 2), 3.6))
    for j, (k, c) in enumerate([("shares_per_1k", "#7B61FF"), ("saves_per_1k", "#F5C542"), ("follows_per_1k", "#3DDC97")]):
        plt.bar([i + (j - 1) * wdt for i in x], [p["d48"].get(k) or 0 for p in ps], width=wdt, color=c, label=k.replace("_", " "))
    plt.xticks(list(x), [label(p) for p in ps], rotation=60, ha="right", fontsize=7)
    plt.title(f"{plat.capitalize()}: shares / saves / follows per 1,000 reached (48h, own saves removed)")
    plt.legend(frameon=False, fontsize=7)
    save(f"{plat}_engagement_rates.png", f"{plat.capitalize()}: shares, saves and follows per 1,000 reached")


# ---------------------------------------------------------------- WHAT_WORKED.md
def trait_section(trait, name):
    lines = []
    for plat in PLAT:
        ps = [p for p in posts if p["platform"] == plat and p["d48"]]
        if len(ps) < 3:
            continue
        g = defaultdict(list)
        for p in ps:
            g[p["cat"].get(trait) or "unknown"].append(p)
        if len(g) < 2:
            continue
        allmed = st.median([p["d48"]["reach_or_views"] or 0 for p in ps])
        lines += [f"**{plat.capitalize()}** (all posts: median reach {fmt(allmed)})", "",
                  f"| {name} | Posts | Median reach 48h | Median traction | Verdict |", "|---|---|---|---|---|"]
        for k, v in sorted(g.items(), key=lambda kv: -st.median([p['d48']['reach_or_views'] or 0 for p in kv[1]])):
            med = st.median([p["d48"]["reach_or_views"] or 0 for p in v])
            rest = [p["d48"]["reach_or_views"] or 0 for p in ps if p not in v]
            rmed = st.median(rest) if rest else None
            tr = [p["traction"] for p in v if p.get("traction") is not None]
            ratio = (med / rmed) if rmed else None
            if len(v) >= 3 and ratio and (ratio >= 1.5 or ratio <= 1 / 1.5):
                verdict = f"**signal**: {ratio:.1f}× the rest"
            elif ratio:
                verdict = f"hint (n={len(v)}): {ratio:.1f}× the rest"
            else:
                verdict = "–"
            lines.append(f"| {k} | {len(v)} | {fmt(med)} | {fmt(st.median(tr)) if tr else '–'} | {verdict} |")
        lines.append("")
    return lines


ww = ["# What worked", "",
      f"_Generated {NOW:%Y-%m-%d %H:%M} by `scripts/build.py`. Compares posts at their 48-hour checkpoint. "
      "A **signal** needs n ≥ 3 and a ≥ 1.5× difference; everything else is a hint. Definitions: [METRICS.md](../METRICS.md)._", ""]
for trait, name in [("style", "Style"), ("hook_type", "Hook type"), ("topic", "Topic"), ("narrated", "Narrated"),
                    ("length_bucket", "Length"), ("post_hour", "Posting hour")]:
    sec = trait_section(trait, name)
    if sec:
        ww += [f"## By {name.lower()}", ""] + sec
for plat in PLAT:
    ps = sorted([p for p in posts if p["platform"] == plat and p.get("traction") is not None], key=lambda p: -p["traction"])
    if len(ps) >= 3:
        top, bot = ps[:3], ps[-3:]
        ww += [f"## {plat.capitalize()}: top vs bottom 3 (by traction)", "", "| | Post | Style | Hook | Topic | Reach 48h | Traction |", "|---|---|---|---|---|---|---|"]
        for tag, grp in [("top", top), ("bottom", bot)]:
            for p in grp:
                c = p["cat"]
                ww.append(f"| {tag} | {p['slug']} | {c.get('style','')} | {c.get('hook_type','')} | {c.get('topic','')} | "
                          f"{fmt(p['d48']['reach_or_views'])} | {fmt(p['traction'])} |")
        shared = {t: {p['cat'].get(t) for p in top} for t in ["style", "hook_type", "topic", "post_hour"]}
        common = [f"{t.replace('_', ' ')} = {list(v)[0]}" for t, v in shared.items() if len(v) == 1]
        ww += ["", f"Shared by all top 3: {', '.join(common) if common else 'nothing in common yet'}.", ""]
open(os.path.join(R, "WHAT_WORKED.md"), "w").write("\n".join(ww) + "\n")

# ---------------------------------------------------------------- OVERALL.md
ov = ["# Content performance: overall", "",
      f"_Last rebuilt {NOW:%Y-%m-%d %H:%M} IST from {len(days)} snapshot day(s) and {len(posts)} tracked post(s). "
      "Start here. Raw data lives in `daily/<date>/`, post traits in `catalog/content.csv`, definitions in [METRICS.md](../METRICS.md)._", ""]
ov += ["## Headline", "", "| Platform | Followers now | Change (first → latest reading) | Posts tracked | Posts with 48h data | Median reach at 48h | Best post (traction) |",
       "|---|---|---|---|---|---|---|"]
for plat in PLAT:
    acc = sorted([r for r in accounts.get(plat, []) if r["followers"] is not None], key=lambda r: r["captured_at_ist"])
    fnow = acc[-1]["followers"] if acc else None
    ch = f"{acc[0]['followers']:.0f} → {fnow:.0f} ({fnow - acc[0]['followers']:+.0f})" if acc else "–"
    ps = [p for p in posts if p["platform"] == plat]
    p48 = [p for p in ps if p["d48"]]
    med = st.median([p["d48"]["reach_or_views"] or 0 for p in p48]) if p48 else None
    best = max([p for p in p48 if p.get("traction") is not None], key=lambda p: p["traction"], default=None)
    ov.append(f"| {plat} | {fmt(fnow)} | {ch} | {len(ps)} | {len(p48)} | {fmt(med)} | {best['slug'] + ' (' + fmt(best['traction']) + ')' if best else '–'} |")
ov.append("")

ov += ["## Are we improving?", ""]
for plat in PLAT:
    ps = sorted([p for p in posts if p["platform"] == plat and p["d48"] and p["cat"].get("posted_at_ist")],
                key=lambda p: p["cat"]["posted_at_ist"])
    if len(ps) < 4:
        if ps:
            ov.append(f"- **{plat}**: only {len(ps)} post(s) with 48h data; need 4+ for a trend.")
        continue
    half = len(ps) // 2
    old = st.median([p["d48"]["reach_or_views"] or 0 for p in ps[:half]])
    new = st.median([p["d48"]["reach_or_views"] or 0 for p in ps[half:]])
    trend = "improving" if new > old * 1.15 else "declining" if new < old / 1.15 else "flat"
    ov.append(f"- **{plat}**: newer half of posts median reach {fmt(new)} vs older half {fmt(old)} → **{trend}**.")
ov.append("")

ov += ["## Charts", ""]
for name, title in charts:
    ov += [f"### {title}", "", f"![{title}](charts/{name})", ""]

ov += ["## Leaderboard (48h checkpoint)", ""]
for plat in PLAT:
    ps = sorted([p for p in posts if p["platform"] == plat and p["d48"]], key=lambda p: -(p.get("traction") or 0))
    if not ps:
        continue
    ov += [f"### {plat.capitalize()}", "", "| # | Post | Posted (IST) | Style | Hook | Reach 48h | Retention % | Shares+saves /1k | Follows /1k | Traction |",
           "|---|---|---|---|---|---|---|---|---|---|"]
    for i, p in enumerate(ps, 1):
        c, d48 = p["cat"], p["d48"]
        link = f"[{p['slug']}]({c['url']})" if c.get("url") else p["slug"]
        ov.append(f"| {i} | {link} | {c.get('posted_at_ist','')} | {c.get('style','')} | {c.get('hook_type','')} | "
                  f"{fmt(d48['reach_or_views'])} | {fmt(d48['retention'])} | {fmt((d48.get('shares_per_1k') or 0) + (d48.get('saves_per_1k') or 0), 1)} | "
                  f"{fmt(d48.get('follows_per_1k'), 1)} | {fmt(p.get('traction'))} |")
    ov.append("")
young = [p for p in posts if not p["d48"]]
if young:
    ov += ["## Too early to judge (no 48h reading yet)", "", "| Post | Platform | Posted (IST) | Latest age (h) | Latest views |", "|---|---|---|---|---|"]
    for p in sorted(young, key=lambda p: p["cat"].get("posted_at_ist", "")):
        ov.append(f"| {p['slug']} | {p['platform']} | {p['cat'].get('posted_at_ist','')} | {fmt(p['latest']['age_h'])} | {fmt(p['latest']['views'])} |")
    ov.append("")
gaps = []
nret = sum(1 for p in posts if p["d48"] and p["d48"]["retention"] is None)
if nret:
    gaps.append(f"- {nret} post(s) have no retention (watch time) data: Instagram web insights do not show it; get app screenshots.")
unc = [cid_ for cid_ in snaps if cid_ not in catalog]
if unc:
    gaps.append(f"- Not in catalog (traits unknown): {', '.join(unc)}. Register with `record.py content`.")
nocap = [c for c in catalog if c not in snaps]
if nocap:
    gaps.append(f"- In catalog but never measured: {', '.join(nocap)}.")
if gaps:
    ov += ["## Data gaps", ""] + gaps + [""]
ov += ["See [WHAT_WORKED.md](WHAT_WORKED.md) for trait-by-trait comparisons and [latest_by_post.csv](latest_by_post.csv) for every number in one table.", ""]
open(os.path.join(R, "OVERALL.md"), "w").write("\n".join(ov) + "\n")
print(f"built: {len(days)} day(s), {len(posts)} post(s), {len(charts)} chart(s) -> reports/OVERALL.md")
