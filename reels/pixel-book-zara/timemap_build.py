# Builds timemap.json: keep only narration (sped up 7%) + the visual moments that matter; cut every other dead span.
import json, subprocess
TEMPO = 1.12
START = json.load(open("vo_times.json"))
dur = {k: (v[1] - v[0]) / TEMPO for k, v in START.items()}
need = [[v[0] - .12, v[0] + dur[k] + .2] for k, v in START.items()]
need += [[0.5, 1.0], [2.9, 3.8], [4.5, 5.0], [6.4, 8.0], [9.6, 13.3], [13.6, 15.2], [15.6, 17.2], [17.9, 18.6], [25.6, 30.3],
         [30.4, 31.4], [44.4, 45.3], [64.4, 65.3], [88.8, 89.7], [103.8, 104.7],
         [36.0, 38.6], [41.0, 41.7], [42.4, 43.0], [46.4, 47.0], [50.6, 53.4], [57.3, 57.8], [60.2, 63.8], [72.5, 73.3], [75.9, 76.4], [77.8, 80.6],
         [93.5, 94.0], [94.7, 95.3], [97.7, 99.5], [100.8, 103.4], [106.0, 107.6], [108.8, 109.7], [111.0, 112.6], [116.9, 118.6],
         [120.5, 121.4], [121.9, 123.3], [124.8, 125.4], [125.8, 129.4], [130.1, 131.4], [140.4, 144.4], [154.4, 157.0]]
for b in [12.0, 26.9, 30.6, 32.2, 44.6, 46.4, 50.6, 55.4, 60.2, 64.6, 66.4, 69.8, 73.8, 77.8, 80.6, 89.0, 90.8, 104.0, 105.8, 111.0, 117.6, 131.4]:
    need.append([b - .3, b + .25])                      # scene transitions stay whole
need.sort(); merged = []
for a, b in need:
    if merged and a <= merged[-1][1] + .05: merged[-1][1] = max(merged[-1][1], b)
    else: merged.append([a, b])
END = 157.0; cuts = []; prev = 0.0
for a, b in merged:
    if a - prev > .25: cuts.append([round(prev, 3), round(a, 3)])
    prev = max(prev, b)
FAST = [[9.6, 12.0, .65], [12.0, 12.85, .7], [25.0, 27.45, .6], [30.4, 31.4, .7], [60.2, 61.65, .6], [77.8, 80.6, .6], [111.0, 112.45, .7],
        [116.9, 118.25, .7], [128.1, 129.4, .6], [130.1, 131.4, .7], [142.8, 144.4, .6]]
segs = [[a, b, 0.0] for a, b in cuts]
for a, b, f in FAST:                                      # only where no narration plays
    if all(b <= v[0] - .12 or a >= v[0] + dur[k] + .1 for k, v in START.items()): segs.append([a, b, f])
    else: print("skip fast", a, b)
segs.sort()
json.dump({"tempo": TEMPO, "end": END, "segs": segs}, open("timemap.json", "w"), indent=0)
t2u = lambda t: t - sum((max(0, min(b, t) - a)) * (1 - f) for a, b, f in segs)
print(len(cuts), "cuts, new length", round(t2u(END), 1))
