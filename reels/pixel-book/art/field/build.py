# Style test: opening field shot. 270x480 at 1x, shown at 4x (1080x1920).
import sys; sys.path.insert(0, "/Users/sanyampathak/Documents/dmyor-videos/.claude/skills/pixel-art-studio/scripts")
from pixelstudio import Sprite, ramp, mix
from PIL import Image
W, H = 270, 480
OUT = "/Users/sanyampathak/Documents/dmyor-videos/reels/pixel-book/art/field/"

# ---------- palette ----------
SKY = ["#3E7FD8", "#5AA2EC", "#86C3F4", "#B6DDF8", "#F6E7C4"]
CLOUD = ["#9FB4DA", "#D6E2F4", "#FFFFFF"]
FAR = ["#6F8FC4", "#87A6D2"]            # distant blue hills
MID = ramp("#6DB86A", 4, hue_shift=18)   # mid hills
GRASS = ramp("#4FA65A", 5, hue_shift=20)
LEAF = ramp("#3E9A55", 5, hue_shift=22)
BARK = ramp("#8A5A34", 4, hue_shift=14)
FLOW = ["#FF7A59", "#FFC145", "#FFFFFF", "#B07CFF", "#FF9FC2"]

def layer_png(s, name):
    s.save_png(OUT + name + ".png")

# ---------- sky ----------
sky = Sprite(W, H, snap=False)
sky.gradient_dither(0, 0, W - 1, 300, SKY, axis="v", pattern="bayer4")
sky.rect(0, 301, W - 1, H - 1, SKY[-1])
layer_png(sky, "sky")

# ---------- clouds (separate sprite, drifts) ----------
def cloud(s, x, y, k=1.0):
    blobs = [(0, 6, 9), (10, 0, 11), (22, 4, 10), (31, 8, 7), (14, 9, 9)]
    for dx, dy, r in blobs: s.circle(int(x + dx * k), int(y + dy * k), int(r * k), CLOUD[0], fill=True)
    for dx, dy, r in blobs: s.circle(int(x + dx * k) - 1, int(y + dy * k) - 2, int(r * k) - 1, CLOUD[1], fill=True, only="opaque")
    for dx, dy, r in blobs[:3]: s.circle(int(x + dx * k) - 2, int(y + dy * k) - 4, int(r * k) - 4, CLOUD[2], fill=True, only="opaque")
cl = Sprite(W, H, snap=False)
cloud(cl, 30, 70, 1.0); cloud(cl, 170, 40, 1.3); cloud(cl, 120, 150, .8)
layer_png(cl, "clouds")

# ---------- far hills ----------
far = Sprite(W, H, snap=False)
far.polygon([(0, 300), (40, 270), (90, 285), (140, 255), (200, 280), (250, 262), (269, 270), (269, 330), (0, 330)], FAR[0])
far.polygon([(0, 310), (60, 292), (120, 305), (180, 288), (269, 300), (269, 330), (0, 330)], FAR[1])
layer_png(far, "far")

# ---------- mid hills ----------
mid = Sprite(W, H, snap=False)
mid.ellipse(-120, 296, 200, 440, MID[1]); mid.ellipse(90, 304, 400, 440, MID[0])
mid.ellipse(-116, 299, 196, 440, MID[2], only=MID[1]); mid.ellipse(96, 307, 396, 440, MID[1], only=MID[0])
layer_png(mid, "mid")

# ---------- ground ----------
gr = Sprite(W, H, snap=False)
gr.ellipse(-60, 340, 330, 560, GRASS[2])
gr.rect(0, 380, W - 1, H - 1, GRASS[2])
gr.gradient_dither(0, 400, W - 1, H - 1, [GRASS[2], GRASS[1]], axis="v", pattern="bayer4", only=GRASS[2])
gr.noise(0, 345, W - 1, H - 1, GRASS[3], density=.05, seed=3, only="opaque")
gr.noise(0, 360, W - 1, H - 1, GRASS[0], density=.03, seed=4, only="opaque")
# grass tufts
import random; R = random.Random(7)
for i in range(70):
    x, y = R.randint(2, W - 3), R.randint(352, H - 4)
    c = GRASS[3] if y < 410 else GRASS[4]
    gr.px(x, y, c); gr.px(x - 1, y + 1, c); gr.px(x + 1, y + 1, c)
layer_png(gr, "ground")

# ---------- flowers (sway layer) ----------
fl = Sprite(W, H, snap=False)
for i in range(40):
    x, y = R.randint(4, W - 5), R.randint(360, H - 6)
    c = FLOW[i % len(FLOW)]
    fl.px(x, y + 1, GRASS[0]); fl.px(x, y + 2, GRASS[0])
    fl.px(x, y - 1, c); fl.px(x - 1, y, c); fl.px(x + 1, y, c); fl.px(x, y + 0, "#FFE9A0" if c != "#FFC145" else "#FF9F45")
layer_png(fl, "flowers")

# ---------- tree ----------
tr = Sprite(W, H, snap=False)
tx, ty = 78, 392                          # trunk base
tr.polygon([(tx - 9, ty), (tx - 5, ty - 70), (tx + 5, ty - 70), (tx + 10, ty)], BARK[1])
tr.polygon([(tx - 3, ty), (tx, ty - 70), (tx + 5, ty - 70), (tx + 10, ty)], BARK[0])
tr.line(tx - 4, ty - 66, tx - 3, ty - 4, BARK[2]); tr.line(tx - 6, ty - 3, tx - 14, ty + 1, BARK[1]); tr.line(tx + 9, ty - 2, tx + 17, ty + 2, BARK[0])
import math
R2 = random.Random(21); clusters = []
for i in range(26):
    ang = R2.uniform(0, 2 * math.pi); rad = R2.uniform(0, 1) ** .6
    cx = tx + int(math.cos(ang) * rad * 62); cy = ty - 126 + int(math.sin(ang) * rad * 44); clusters.append((cx, cy, R2.randint(11, 19)))
clusters.sort(key=lambda c: c[1])
for cx, cy, r in clusters: tr.circle(cx, cy, r, LEAF[0], fill=True)
for cx, cy, r in clusters: tr.circle(cx + 1, cy - 2, r - 2, LEAF[1], fill=True, only="opaque")
for cx, cy, r in clusters:
    if cy < ty - 95: tr.circle(cx + 3, cy - 5, r - 6, LEAF[2], fill=True, only=LEAF[1])
for cx, cy, r in clusters:
    if cy < ty - 135: tr.circle(cx + 5, cy - 8, max(2, r - 12), LEAF[3], fill=True, only=LEAF[2])
tr.noise(tx - 90, ty - 200, tx + 90, ty - 60, LEAF[0], density=.06, seed=11, only=LEAF[1])
tr.noise(tx - 90, ty - 200, tx + 90, ty - 60, LEAF[1], density=.05, seed=13, only=LEAF[2])
tr.noise(tx - 90, ty - 200, tx + 90, ty - 60, LEAF[4], density=.06, seed=12, only=LEAF[3])
tr.outline("#1F4A3A", where="inside")
layer_png(tr, "tree")
# tree shadow on grass
sh = Sprite(W, H, snap=False); sh.ellipse(tx - 70, ty - 6, tx + 90, ty + 14, GRASS[1]); layer_png(sh, "shadow")

# ---------- hero: sitting, reading (facing right) ----------
SK = ramp("#F2C6A0", 3, hue_shift=10); SH = ramp("#FF7A59", 3, hue_shift=16); PA = ramp("#34477A", 3, hue_shift=12)
HA = "#3B2416"; HA2 = "#5E3A24"; OL = "#2A1F2E"
hero = Sprite(40, 40, snap=False)
def build_hero(s, page=0):
    s.polygon([(14, 29), (25, 19), (28, 21), (17, 31)], PA[0])                       # far leg
    s.polygon([(29, 21), (31, 33), (28, 34)], PA[0])
    s.polygon([(6, 29), (17, 29), (18, 37), (5, 37)], PA[1])                          # seat
    s.polygon([(12, 30), (17, 28), (26, 20), (30, 23), (20, 35), (12, 36)], PA[1])    # near thigh
    s.polygon([(26, 21), (30, 22), (32, 34), (28, 35)], PA[1])                        # shin
    s.line(28, 23, 30, 32, mix(PA[1], PA[2], .35))
    s.rect(27, 34, 34, 36, "#1E2233"); s.px(35, 36, "#1E2233"); s.line(28, 34, 32, 34, "#3A4060")
    s.polygon([(7, 15), (16, 15), (18, 29), (6, 30)], SH[1])                         # torso
    s.polygon([(7, 15), (9, 15), (8, 30), (6, 30)], mix(SH[0], SH[1], .45))                           # back in shadow
    s.line(14, 16, 17, 27, SH[2])
    s.polygon([(10, 13), (13, 13), (13, 16), (10, 16)], SK[0])                        # neck
    s.circle(12, 8, 6, SK[1], fill=True)                                              # head
    s.px(19, 8, SK[1]); s.px(18, 9, SK[1])                                            # nose
    s.polygon([(6, 3), (9, 1), (14, 1), (17, 3), (17, 5), (13, 4), (11, 7), (10, 10), (7, 11), (6, 8)], HA)  # hair
    s.line(9, 2, 13, 2, HA2)
    s.rect(8, 7, 9, 9, SK[0]); s.px(9, 8, SK[1])                                               # ear
    # book (open, on knees) + page flip
    s.polygon([(18, 20), (32, 19), (32, 21), (18, 22)], "#6A4FD1")
    s.polygon([(19, 20), (25, 15), (25, 20)], "#FFF4E0"); s.polygon([(19, 20), (19, 16), (25, 14), (25, 20)], "#FFF4E0")
    s.polygon([(25, 14), (31, 15), (31, 20), (25, 20)], "#FFF4E0")
    s.line(25, 14, 25, 20, "#C9B48A")
    for yy in (16, 18): s.line(20, yy + 1, 24, yy, "#C9B48A"); s.line(26, yy, 30, yy + 1, "#C9B48A")
    # arm: shoulder -> elbow -> hand on book edge
    s.polygon([(11, 16), (15, 16), (17, 23), (13, 24)], SH[1]); s.line(11, 17, 13, 24, mix(SH[0], SH[1], .5))
    s.polygon([(14, 21), (19, 18), (21, 20), (16, 24)], SK[1])
    s.rect(19, 18, 21, 20, SK[2])
    s.outline(OL, where="outside")
    s.px(16, 7, "#1C1A24"); s.px(16, 8, "#1C1A24"); s.line(15, 5, 17, 5, HA)          # eye, brow
    s.px(17, 11, "#B8584E"); s.px(16, 11, "#B8584E")                                  # smile
    s.px(17, 9, "#F4A7A0")                                                             # cheek
build_hero(hero)
hero.save_png(OUT + "hero_read.png")
hb = Sprite.from_png(OUT + "hero_read.png", scale=1); hb.px(16, 7, SK[1]); hb.px(15, 8, "#1C1A24"); hb.px(16, 8, "#1C1A24"); hb.save_png(OUT + "hero_read_blink.png"); hero.preview(OUT + "hero_preview.png", scale=10, labels=False)

# ---------- composite at 4x ----------
comp = Image.new("RGBA", (W, H))
for n in ["sky", "clouds", "far", "mid", "ground", "shadow", "flowers", "tree"]:
    comp.alpha_composite(Image.open(OUT + n + ".png").convert("RGBA"))
h = Image.open(OUT + "hero_read.png").convert("RGBA")
comp.alpha_composite(h, (tx + 4, ty - h.height + 5))
comp.resize((W * 4, H * 4), Image.NEAREST).save(OUT + "composite_4x.png")
print("ok")
