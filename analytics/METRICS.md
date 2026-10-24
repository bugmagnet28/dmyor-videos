# How we judge content

Every number in `analytics/` follows these definitions. If a platform calls it something else, the mapping is below.

## Raw metrics (collected per post, per snapshot)

| Column | Meaning | Instagram | YouTube Shorts | X |
|---|---|---|---|---|
| `views` | times the post was played/seen | Views | Views | Impressions (Views) |
| `reach` | unique accounts that saw it | Accounts reached / "Viewers" | Unique viewers (if shown) else blank | blank (X does not give unique) |
| `nonfollower_pct` | % of views from non-followers (= discovery) | Views → Non-followers % | "From non-subscribers" % if shown | blank |
| `likes` `comments` `shares` `saves` | interactions | Likes, Comments, Shares (sends), Saves | Likes, Comments, Shares, blank | Likes, Replies, Reposts+Quotes, Bookmarks |
| `follows` | follows/subscribers caused by this post | Follows | Subscribers gained | blank unless shown |
| `profile_visits` | profile activity from this post | Profile activity / visits | blank | Profile visits |
| `link_clicks` | clicks to dmyor.com | blank (bio) | blank | Link clicks |
| `avg_watch_s` | average watch time per view, seconds | Average watch time (app) | Average view duration | blank |
| `watched_pct` | average % of the video watched | avg_watch_s / length | Average percentage viewed | blank |
| `skip_rate_pct` | % who swiped away in the first ~3 s | Skip rate (app) | 100 - "Stayed to watch" % | blank |
| `age_h` | hours between posting and this snapshot | | | |
| `source` | where the number came from: `web-insights`, `app-screenshot`, `studio`, `x-analytics`, `typed` | | | |

Rules: never invent a number. Unknown = empty cell. Own-account saves (e.g. a save on every post by the account itself) are recorded but flagged in `note` and excluded from analysis via `self_saves`.

## Derived metrics (computed by `scripts/build.py`)

| Metric | Formula | Why it matters |
|---|---|---|
| `reach_or_views` | reach if known else views | comparable "how many people" number |
| `eng_per_1k` | (likes + comments + shares + saves - self_saves) / reach_or_views × 1000 | overall response |
| `shares_per_1k`, `saves_per_1k`, `follows_per_1k` | / reach_or_views × 1000 | **the signals that make platforms push a post** (shares > saves > follows > comments > likes) |
| `retention` | watched_pct (or avg_watch_s / length) | did people stay |

## Fair comparison: the 48-hour checkpoint

Posts are compared at the same age. For each post we use the snapshot **closest to 48 h** (accepted window 24-96 h; readings under ~36 h undercount, so aim to collect around 48 h). Posts younger than 24 h are shown as "too early" and kept out of verdicts. A later 7-day snapshot (150-200 h) is shown separately when we have it.

## Traction score (0-100, per platform)

For each post at its 48 h checkpoint, within the same platform:

```
traction = 40% × percentile(reach_or_views)
         + 25% × percentile(retention)                (dropped and re-weighted if unknown)
         + 20% × percentile(shares_per_1k + saves_per_1k)
         + 15% × percentile(follows_per_1k)
```

Percentiles (rank among all posts on that platform) keep it robust with few posts and wildly different sizes. Likes are deliberately left out of the score.

## "What worked"

Posts are grouped by their traits from `catalog/content.csv` (style, hook_type, topic, narrated, length bucket, posting hour IST, weekday). For each group: number of posts, median reach at 48 h, median traction. A trait is only called a **signal** when the group has n ≥ 3 and differs from the rest by ≥ 1.5×; otherwise it is labelled **hint (small n)**.

## Progress ("are we getting better?")

- **Followers per platform** over time (account.csv).
- **Median reach at 48 h of posts, by posting week**, and a rolling median by post order: if new posts reach more people than old ones, we are improving.
- **Total views per day** (sum over all posts of views gained since the previous snapshot).
