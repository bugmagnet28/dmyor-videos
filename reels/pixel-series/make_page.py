"""Assemble an episode page: python3 reels/pixel-series/make_page.py reels/<episode> "<title>"
Load order: timeline.js (TL) -> kit_head.js (engine + helpers) -> episode.js (SCENES, EP) -> kit_run.js (render, overlays, __seek)."""
import os, sys
d, title = sys.argv[1], sys.argv[2]
open(os.path.join(d, "pixel.html"), "w").write(f"""<!doctype html>
<html><head><meta charset="utf-8"><title>{title}</title>
<style>html,body{{margin:0;background:#000;overflow:hidden}}canvas{{display:block;width:1080px;height:1920px;image-rendering:pixelated}}</style></head>
<body><canvas id="c" width="1080" height="1920"></canvas>
<script src="timeline.js"></script><script src="../pixel-series/kit_head.js"></script><script src="episode.js"></script><script src="../pixel-series/kit_run.js"></script>
</body></html>
""")
print("wrote", os.path.join(d, "pixel.html"))
