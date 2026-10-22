"""Build a tree-series reel: reels/<slug>/config.json -> reels/<slug>/reel.html (+ audio via music.py)."""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
reel = sys.argv[1]
cfg = json.load(open(os.path.join(reel, "config.json")))
html = open(os.path.join(HERE, cfg.get("template", "tree.html"))).read()
html = html.replace("/*__CONFIG__*/{}", json.dumps(cfg))
rel = os.path.relpath(os.path.join(HERE, "fonts"), reel)
html = html.replace("url(fonts/", "url(" + rel + "/")
open(os.path.join(reel, "reel.html"), "w").write(html)
print("built", os.path.join(reel, "reel.html"), cfg["total"], "s")
