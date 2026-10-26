"""One-page dashboard of all content and its performance (Graphite & Sage).

    analytics/.venv/bin/python analytics/scripts/dashboard.py   ->  analytics/reports/charts/DASHBOARD.png

Reads reports/latest_by_post.csv and every daily/*/account.csv (run build.py first).
Panels: every reel on Instagram (bars by post time, coloured by style, age shown), average views by style
(Instagram vs YouTube), views vs age (the fair comparison: newer reels have had less time), totals per platform,
followers over time.
"""
import csv, glob, os
from collections import defaultdict
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

A = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BG, PANEL, INK, MUTE, LINE = "#151719", "#1D2023", "#E9E7E2", "#8C8F8A", "#33373B"
STYLE_COL = {"kinetic-typography": "#8C8F8A", "illustrated-scene": "#D8CBA8", "diagram-motion-graphics": "#6FA59A",
             "animated-illustration-explainer": "#9DB8A3", "cinematic-motion": "#C98B7B"}
STYLE_NAME = {"kinetic-typography": "Kinetic text (Oct 21)", "illustrated-scene": "Tree scenes (Oct 22)", "diagram-motion-graphics": "Diagram + voice (Oct 23)",
              "animated-illustration-explainer": "Illustrated explainer (Oct 25-26)", "cinematic-motion": "Cinematic film"}


def f(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return None


def main():
    rows = list(csv.DictReader(open(os.path.join(A, "reports", "latest_by_post.csv"))))
    plt.rcParams.update({"font.family": "DejaVu Sans", "text.color": INK, "axes.labelcolor": MUTE, "xtick.color": MUTE, "ytick.color": MUTE,
                         "axes.edgecolor": LINE, "axes.facecolor": PANEL, "figure.facecolor": BG, "axes.titleweight": "bold", "axes.titlesize": 13})
    fig = plt.figure(figsize=(16, 21))
    gs = fig.add_gridspec(4, 2, height_ratios=[2.3, 1, 1, .8], hspace=.42, wspace=.28, left=.2, right=.96, top=.93, bottom=.04)
    fig.suptitle("Dmyor content performance: every reel so far", fontsize=22, fontweight="bold", x=.06, ha="left", y=.975)
    ig = sorted([r for r in rows if r["platform"] == "instagram" and f(r["latest_views"]) is not None], key=lambda r: r["posted_at_ist"])
    last = max(r["latest_captured"] for r in rows if r["latest_captured"])
    fig.text(.06, .952, f"Instagram reels, YouTube Shorts and X posts of @becauseidmyor. Latest reading {last} IST. Views only (watch time needs app screenshots).",
             color=MUTE, fontsize=11.5)

    # A: every reel on Instagram
    ax = fig.add_subplot(gs[0, :])
    ys = range(len(ig))
    ax.barh(list(ys), [f(r["latest_views"]) for r in ig], color=[STYLE_COL.get(r["style"], MUTE) for r in ig], height=.72)
    ax.set_yticks(list(ys)); ax.set_yticklabels([f'{r["slug"]}  ({r["posted_at_ist"][5:10]})' for r in ig], fontsize=10)
    ax.invert_yaxis(); ax.grid(axis="x", color=LINE, lw=.6); ax.set_axisbelow(True)
    for y, r in zip(ys, ig):
        ax.text(f(r["latest_views"]) + 3, y, f'{int(f(r["latest_views"]))}  ·  {int(f(r["latest_age_h"]) or 0)} h old', va="center", fontsize=9.5, color=INK)
    ax.set_title("Instagram views per reel, oldest at top (colour = production style)", loc="left")
    ax.set_xlabel("views")
    hs = [plt.Rectangle((0, 0), 1, 1, color=c) for c in STYLE_COL.values()]
    ax.legend(hs, STYLE_NAME.values(), loc="lower right", facecolor=BG, edgecolor=LINE, fontsize=10)

    # B: average by style, Instagram vs YouTube
    ax = fig.add_subplot(gs[1, 0])
    by = defaultdict(lambda: defaultdict(list))
    for r in rows:
        v = f(r["latest_views"])
        if v is not None and r["platform"] in ("instagram", "youtube"):
            by[r["style"]][r["platform"]].append(v)
    styles = [s for s in STYLE_COL if s in by]
    import numpy as np
    xs = np.arange(len(styles))
    for i, (pf, col) in enumerate([("instagram", "#9DB8A3"), ("youtube", "#C98B7B")]):
        vals = [np.mean(by[s][pf]) if by[s][pf] else 0 for s in styles]
        b = ax.bar(xs + (i - .5) * .38, vals, .36, color=col, label=pf.capitalize())
        for x, v, s in zip(xs, vals, styles):
            if by[s][pf]:
                ax.text(x + (i - .5) * .38, v + 2, f"{v:.0f}\n(n={len(by[s][pf])})", ha="center", fontsize=9, color=INK)
    ax.set_xticks(xs); ax.set_xticklabels([STYLE_NAME[s].split(" (")[0] for s in styles], fontsize=9.5)
    ax.set_title("Average views by style", loc="left"); ax.legend(facecolor=BG, edgecolor=LINE); ax.grid(axis="y", color=LINE, lw=.6); ax.set_axisbelow(True)

    # C: views vs age (fair comparison)
    ax = fig.add_subplot(gs[1, 1])
    for r in ig:
        ax.scatter(f(r["latest_age_h"]), f(r["latest_views"]), s=90, color=STYLE_COL.get(r["style"], MUTE), edgecolor=BG, zorder=3)
    for r in sorted(ig, key=lambda r: -f(r["latest_views"]))[:5]:
        ax.annotate(r["slug"].replace("ill-", ""), (f(r["latest_age_h"]), f(r["latest_views"])), xytext=(6, 4), textcoords="offset points", fontsize=9, color=INK)
    ax.set_xlabel("hours since posting"); ax.set_ylabel("Instagram views"); ax.grid(color=LINE, lw=.6)
    ax.set_title("Views vs age: newer reels earn more in less time", loc="left")

    # D: totals per platform
    ax = fig.add_subplot(gs[2, 0])
    tot = defaultdict(float); cnt = defaultdict(int)
    for r in rows:
        v = f(r["latest_views"])
        if v is not None:
            tot[r["platform"]] += v; cnt[r["platform"]] += 1
    pfs = [p for p in ("instagram", "youtube", "x") if p in tot]
    ax.bar(pfs, [tot[p] for p in pfs], color=["#9DB8A3", "#C98B7B", "#8C8F8A"][:len(pfs)])
    for i, p in enumerate(pfs):
        ax.text(i, tot[p] + 15, f"{tot[p]:.0f} views\n{cnt[p]} posts measured\n{tot[p] / cnt[p]:.1f} per post", ha="center", fontsize=9.5, color=INK)
    ax.set_title("Total views by platform", loc="left"); ax.grid(axis="y", color=LINE, lw=.6); ax.set_axisbelow(True)
    ax.set_ylim(0, max(tot.values()) * 1.3)

    # E: by hook type (Instagram)
    ax = fig.add_subplot(gs[2, 1])
    hk = defaultdict(list)
    for r in ig:
        hk[r["hook_type"]].append(f(r["latest_views"]))
    items = sorted(hk.items(), key=lambda kv: -np.mean(kv[1]))
    ax.barh([k for k, _ in items], [np.mean(v) for _, v in items], color="#6FA59A")
    for i, (k, v) in enumerate(items):
        ax.text(np.mean(v) + 2, i, f"{np.mean(v):.0f} (n={len(v)})", va="center", fontsize=9.5, color=INK)
    ax.invert_yaxis(); ax.set_title("Instagram average views by hook type", loc="left"); ax.grid(axis="x", color=LINE, lw=.6); ax.set_axisbelow(True)

    # F: followers
    ax = fig.add_subplot(gs[3, :])
    fol = defaultdict(list)
    for p in sorted(glob.glob(os.path.join(A, "daily", "*", "account.csv"))):
        for r in csv.DictReader(open(p)):
            if f(r.get("followers")) is not None:
                fol[r["platform"]].append((r["captured_at_ist"][:10], f(r["followers"])))
    for p, col in [("instagram", "#9DB8A3"), ("youtube", "#C98B7B"), ("x", "#8C8F8A")]:
        if fol[p]:
            d = sorted(fol[p]); ax.plot([a for a, _ in d], [b for _, b in d], marker="o", color=col, lw=2.5, label=p)
            ax.text(len(d) - 1, d[-1][1] + .6, f"{int(d[-1][1])}", color=col, fontsize=10)
    ax.set_title("Followers", loc="left"); ax.legend(facecolor=BG, edgecolor=LINE); ax.grid(color=LINE, lw=.6)
    out = os.path.join(A, "reports", "charts", "DASHBOARD.png")
    fig.savefig(out, dpi=110); print(out)


if __name__ == "__main__":
    main()
