#!/usr/bin/env python3
"""Contact sheet: sheet.py <out.png> <img1> <img2> ... (labels = file stem). Needs Pillow (analytics/.venv)."""
import sys, os
from PIL import Image, ImageDraw
out, imgs = sys.argv[1], sys.argv[2:]
W, H, cols = 360, 640, 5
rows = (len(imgs) + cols - 1) // cols
S = Image.new("RGB", (cols * W, rows * (H + 30)), "white")
d = ImageDraw.Draw(S)
for i, p in enumerate(imgs):
    im = Image.open(p).convert("RGB").resize((W, H))
    x, y = (i % cols) * W, (i // cols) * (H + 30)
    S.paste(im, (x, y + 30)); d.text((x + 6, y + 8), os.path.splitext(os.path.basename(p))[0], fill="black")
S.save(out); print(out)
