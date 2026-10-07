# Reading performance, and what to change

## Metrics to enter

Instagram (Insights on the reel, "View insights"):

| flag | where it comes from | why |
|---|---|---|
| `--views` | Plays | volume |
| `--reach` | Accounts reached | the number to grow |
| `--likes` `--comments` | obvious | weak reach signals |
| `--shares` | Shares | **strongest reach driver** |
| `--saves` | Saves | second strongest |
| `--avg-watch` | Average watch time (s) | quality |
| `--follows` | Follows from this reel | audience growth |
| `--profile-visits` | Profile visits | intent |
| `--hold3` | Plays that passed 3s / plays, as % | hook quality |

YouTube Shorts (Analytics > the Short):

| flag | where | why |
|---|---|---|
| `--views` | Views | volume |
| `--impressions` `--ctr` | Impressions, CTR % | thumbnail/first frame |
| `--avg-view` | Average view duration (s) | quality |
| `--pct-viewed` | Average percentage viewed | the Shorts ranking signal |
| `--likes` `--comments` `--shares` | obvious | |
| `--subs` | Subscribers gained | growth |
| `--swipe-away` | Swiped away % if shown | hook failure rate |

Enter whatever you have. Missing values are simply excluded from the correlations.

## Derived ratios the report computes

- `share_rate` = shares / reach - the one to optimise on Instagram
- `save_rate` = saves / reach
- `follow_rate` = follows / reach
- `watch_pct` = avg_watch / duration
- `hold3` - if the hook is weak nothing downstream matters

## How to act on it

**Low hold3 / high swipe-away** - the first 3 seconds are the problem, not the reel.
Change the hook pattern, not the body. Check `report.py` for which hook patterns held.

**Good hold3, low watch_pct** - it stops giving new information partway. Look at the
`gaps` output for that reel; dead air is usually the cause. Add scenes, do not shorten
the script first.

**Good watch_pct, low share_rate** - it is satisfying but not useful to send to
someone. Sharpen the one line a viewer would send with. Usually the permanence or
verification idea, not the product description.

**Good everything, low reach** - posting time or frequency, not content. The report
buckets by weekday and hour once there are enough data points.

## Discipline

- Enter metrics at a consistent age (48h is a reasonable default) or the comparison is
  meaningless. `perf` records `hours_after_post` so mixed ages are at least visible.
- Log more than once per reel if you want a curve; each entry is appended.
- Fewer than ~5 reels means the report shows raw rows and no correlations. Do not read
  signal into 2 data points, and say so to the user rather than implying a trend.
