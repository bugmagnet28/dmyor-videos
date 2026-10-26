# Scene backgrounds + props for pixel-book. Every world is 270x480 at 1x.
import sys, random, math; sys.path.insert(0, "/Users/sanyampathak/Documents/dmyor-videos/.claude/skills/pixel-art-studio/scripts")
from pixelstudio import Sprite, ramp, mix
from PIL import Image
W, H = 270, 480
OUT = "/Users/sanyampathak/Documents/dmyor-videos/reels/pixel-book/art/scenes/"
OL = "#2A1F2E"
def new(w=W, h=H): return Sprite(w, h, snap=False)
def save(s, n): s.save_png(OUT + n + ".png")

# ================= HOUSE AT SUNSET =================
s = new()
s.gradient_dither(0, 0, W - 1, 330, ["#2E2A6B", "#5B3F8C", "#B4508A", "#F2706A", "#FBB46B", "#FDE3A0"], pattern="bayer4")
s.circle(200, 300, 26, "#FFD27A", fill=True); s.circle(200, 300, 20, "#FFEDB0", fill=True)
for i, (x, y, w) in enumerate([(20, 120, 60), (150, 80, 80), (60, 200, 50)]):
    s.rect(x, y, x + w, y + 4, "#F79A8A"); s.rect(x + 8, y - 3, x + w - 10, y, "#FBB9A0")
s.polygon([(0, 330), (50, 310), (110, 322), (180, 300), (240, 316), (269, 308), (269, 345), (0, 345)], "#6A4C8C")
s.rect(0, 340, W - 1, H - 1, "#4E8A55")
s.noise(0, 340, W - 1, H - 1, "#5FA064", density=.08, seed=2, only="#4E8A55")
# house: two stacked white boxes, glass, warm lights
s.rect(40, 250, 250, 345, "#E9E4DA"); s.rect(40, 250, 250, 253, "#FFFFFF"); s.rect(40, 342, 250, 345, "#BDB4A6")
s.rect(110, 205, 230, 252, "#F4F0E8"); s.rect(104, 200, 236, 205, "#3A3550")
s.rect(36, 246, 254, 251, "#3A3550")
for x0 in (52, 92, 132): s.rect(x0, 266, x0 + 32, 330, "#2C3A5A"); s.rect(x0 + 2, 268, x0 + 30, 328, "#FFC46B"); s.dither(x0 + 2, 268, x0 + 30, 328, "keep", "#FFDE9A", mix=.3, pattern="bayer4", only="#FFC46B"); s.line(x0 + 16, 268, x0 + 16, 328, "#2C3A5A")
s.rect(176, 262, 238, 338, "#2C3A5A"); s.rect(178, 264, 236, 336, "#7FA8D8"); s.line(178, 264, 200, 300, "#B8D4F0"); s.rect(198, 300, 212, 336, "#3A3550")
s.rect(122, 214, 218, 244, "#2C3A5A"); s.rect(124, 216, 216, 242, "#FFC46B"); s.line(170, 216, 170, 242, "#2C3A5A")
s.dither(124, 216, 216, 242, "keep", "#FFDE9A", mix=.3, pattern="bayer4", only="#FFC46B")
# pool
s.rect(60, 352, 200, 368, "#BDB4A6"); s.rect(64, 354, 196, 366, "#3FB6D8"); s.noise(64, 354, 196, 366, "#9EE6F5", density=.12, seed=5, only="#3FB6D8")
# driveway
s.polygon([(0, 384), (W - 1, 376), (W - 1, 402), (0, 410)], "#8E8A96"); s.line(0, 384, W - 1, 376, "#B6B2BC"); s.noise(0, 378, W - 1, 410, "#7A7684", density=.06, seed=8, only="#8E8A96")
# palms
def palm(x, y, h):
    for i in range(h): s.px(x + int(math.sin(i / 9) * 3), y - i, "#7A5236"); s.px(x + 1 + int(math.sin(i / 9) * 3), y - i, "#5E3E28")
    tx, ty = x + int(math.sin(h / 9) * 3), y - h
    for a in range(-160, 0, 28):
        for r in range(1, 20):
            ax = tx + int(math.cos(math.radians(a)) * r); ay = ty + int(math.sin(math.radians(a)) * r * .5 + (r * r) / 30)
            s.px(ax, ay, "#2F7A4A"); s.px(ax, ay + 1, "#1F5A38")
palm(20, 345, 70); palm(256, 345, 85)
save(s, "house")
# hedge foreground (separate layer, in front)
s = new(); s.rect(0, 410, 120, H - 1, "#2F6B3E")
for i in range(16): s.circle(i * 8, 412 + (i % 3), 8, "#2F6B3E", fill=True)
s.noise(0, 400, 120, H - 1, "#3E8A52", density=.18, seed=9, only="#2F6B3E"); s.noise(0, 400, 120, H - 1, "#1F4A2C", density=.1, seed=10, only="#2F6B3E")
s.rect(121, 430, W - 1, H - 1, "#4E8A55"); s.noise(121, 430, W - 1, H - 1, "#5FA064", density=.1, seed=12, only="#4E8A55")
save(s, "hedge")

# ================= LUXURY CAR (side view, facing right) + wheel =================
c = new(84, 30)
c.polygon([(2, 22), (4, 15), (20, 12), (32, 4), (56, 3), (70, 11), (80, 13), (82, 22)], "#151821")
c.polygon([(30, 6), (36, 2), (52, 2), (60, 9), (34, 10)], "#151821")
c.polygon([(34, 9), (38, 4), (50, 4), (56, 9)], "#6E8FB8"); c.line(45, 4, 45, 9, "#151821"); c.line(38, 5, 42, 5, "#B8D0EA")
c.line(6, 14, 78, 14, "#3A4256"); c.line(20, 12, 32, 5, "#3A4256"); c.line(4, 18, 80, 18, "#C9A24A")
c.rect(78, 14, 81, 16, "#FFE9A0"); c.rect(2, 15, 4, 17, "#E0453A"); c.px(46, 15, "#9AA3B5"); c.px(47, 15, "#9AA3B5")
c.outline(OL, where="outside"); save(c, "car")
for i in range(2):
    wv = new(14, 14); wv.circle(7, 7, 6, "#1A1A22", fill=True); wv.circle(7, 7, 3, "#9AA3B5", fill=True); wv.circle(7, 7, 1, "#3A4256", fill=True)
    if i: wv.px(7, 4, "#3A4256"); wv.px(7, 10, "#3A4256")
    else: wv.px(4, 7, "#3A4256"); wv.px(10, 7, "#3A4256")
    save(wv, f"wheel{i}")

# ================= BEDROOM (night + dawn) =================
def room(kind):
    s = new()
    wall, wall2 = ("#2E3A5C", "#283352") if kind == "night" else ("#E9B88F", "#DDA77D")
    s.rect(0, 0, W - 1, 400, wall)
    for x in range(0, W, 14): s.line(x, 0, x, 400, wall2)
    s.rect(0, 400, W - 1, H - 1, "#6B4430" if kind == "night" else "#B27A50")
    for y in range(404, H, 10): s.line(0, y, W - 1, y, "#5A3826" if kind == "night" else "#9A6640")
    s.rect(0, 396, W - 1, 400, "#3B2A24" if kind == "night" else "#7A5034")
    # window
    sky = ["#0B1D3A", "#1D3766", "#2B4C7E"] if kind == "night" else ["#6A5ACD", "#E98A8A", "#FFD3A5"]
    s.rect(150, 190, 240, 300, "#F4E3C8"); s.gradient_dither(155, 195, 235, 295, sky, pattern="bayer4")
    if kind == "night":
        R = random.Random(4)
        for i in range(16): s.px(R.randint(156, 234), R.randint(196, 260), "#FFFFFF")
        s.circle(220, 212, 7, "#FFF4D6", fill=True); s.circle(223, 210, 6, "#1D3766", fill=True)
        for i, hh in enumerate([40, 26, 50, 32, 44]): s.rect(155 + i * 16, 295 - hh, 168 + i * 16, 295, "#14284A")
        for i in range(10): s.px(158 + (i * 7) % 76, 262 + (i * 11) % 30, "#FFD66B")
    else:
        s.circle(200, 280, 10, "#FFE9A0", fill=True)
        for i, hh in enumerate([30, 20, 38, 24, 34]): s.rect(155 + i * 16, 295 - hh, 168 + i * 16, 295, "#B47AA0")
    s.rect(194, 190, 196, 300, "#F4E3C8"); s.rect(150, 244, 240, 246, "#F4E3C8"); s.rect(144, 298, 246, 303, "#D8C4A2")
    # poster
    s.rect(70, 200, 112, 252, "#FFF4E0"); s.gradient_dither(74, 204, 108, 236, ["#FF9A8B", "#FFD3A5"], pattern="bayer4"); s.polygon([(74, 236), (86, 218), (96, 230), (108, 214), (108, 236)], "#5A6BB0")
    # bed (left)
    s.rect(4, 330, 92, 400, "#5A3A2E"); s.rect(4, 318, 14, 400, "#4A2E24"); s.rect(8, 340, 92, 372, "#ECE6F2"); s.rect(28, 344, 92, 380, "#4C9AFF"); s.rect(28, 344, 92, 348, "#7FB8FF")
    s.rect(10, 336, 32, 348, "#FFFFFF")
    # nightstand + alarm clock
    s.rect(96, 362, 122, 400, "#7A5034"); s.rect(96, 362, 122, 365, "#9A6640"); s.rect(100, 375, 118, 377, "#5A3826")
    # desk (right)
    s.rect(150, 340, 262, 346, "#A8693B"); s.rect(150, 346, 262, 349, "#8A5228"); s.rect(156, 349, 160, 400, "#8A5228"); s.rect(252, 349, 256, 400, "#8A5228")
    s.rect(228, 349, 252, 380, "#9A5E30"); s.rect(236, 362, 244, 364, "#E8C08A")
    # chair
    s.rect(132, 352, 160, 357, "#5B6EAE"); s.rect(134, 357, 137, 400, "#3E4C82"); s.rect(155, 357, 158, 400, "#3E4C82"); s.rect(130, 318, 135, 356, "#6A7FC2")
    # lamp
    s.rect(240, 334, 252, 339, "#F2C14E"); s.line(246, 334, 246, 318, "#E0A93A"); s.polygon([(238, 318), (254, 318), (250, 308), (242, 308)], "#F2C14E")
    # shelf with books
    s.rect(20, 240, 60, 243, "#7A5034")
    for i, cc in enumerate(["#FF7A59", "#FFC145", "#6CC7A3", "#4C9AFF", "#B07CFF"]): s.rect(22 + i * 7, 222 + (i % 2) * 3, 27 + i * 7, 239, cc)
    if kind == "night":
        s.dither(0, 0, W - 1, H - 1, "keep", None, mix=0, pattern="bayer4")
    save(s, "room_" + kind)
room("night"); room("dawn")
# props: notebook open on desk, laptop, alarm clock frames, phone
n = new(30, 10); n.polygon([(1, 8), (14, 6), (14, 9), (1, 9)], "#FFF4E0"); n.polygon([(15, 6), (28, 8), (28, 9), (15, 9)], "#FFF4E0"); n.line(14, 6, 14, 9, "#C9B48A"); n.rect(0, 9, 29, 9, "#6A4FD1"); save(n, "notebook")
l = new(34, 26); l.rect(4, 1, 30, 19, "#AEB4BE"); l.rect(6, 3, 28, 17, "#1D2B4A"); l.rect(0, 20, 33, 23, "#C9CED6"); l.outline(OL); save(l, "laptop")
for i in range(2):
    a = new(16, 16); a.circle(8, 9, 6, "#E0453A", fill=True); a.circle(8, 9, 4, "#FFF4E0", fill=True); a.line(8, 9, 8, 6, OL); a.line(8, 9, 10, 9, OL)
    a.circle(3 + (i * 1), 3, 2, "#FFC145", fill=True); a.circle(13 - (i * 1), 3, 2, "#FFC145", fill=True); a.rect(4, 14, 5, 15, OL); a.rect(11, 14, 12, 15, OL); a.outline(OL); save(a, f"alarm{i}")
p = new(8, 12); p.rect(0, 0, 7, 11, "#1E2233"); p.rect(1, 1, 6, 9, "#7FD4FF"); save(p, "phone")
# friends' car (seen through window, small) + 2 friend heads
f = new(60, 24); f.polygon([(2, 20), (4, 12), (14, 10), (20, 3), (40, 3), (48, 10), (58, 12), (58, 20)], "#FFC145"); f.polygon([(22, 5), (38, 5), (44, 10), (18, 10)], "#9ED2F0")
f.circle(26, 8, 3, "#C98F65", fill=True); f.circle(36, 8, 3, "#F2C6A0", fill=True); f.rect(23, 4, 29, 6, "#151018"); f.rect(33, 4, 39, 6, "#C9853F")
f.circle(14, 20, 4, "#1A1A22", fill=True); f.circle(46, 20, 4, "#1A1A22", fill=True); f.outline(OL); save(f, "friendcar")

# ================= SHOP IN THE RAIN =================
s = new()
s.gradient_dither(0, 0, W - 1, 200, ["#1B2233", "#2C3550", "#3D4766"], pattern="bayer4")
s.rect(0, 120, W - 1, 400, "#5A3A3A")
for y in range(124, 400, 8):
    off = 0 if (y // 8) % 2 else 8
    for x in range(-8 + off, W, 16): s.rect(x, y, x + 14, y + 6, "#6E4646")
s.rect(20, 160, 250, 176, "#2E3A5C"); s.rect(20, 176, 250, 182, "#E0453A")
for x in range(20, 250, 20): s.rect(x, 176, x + 9, 182, "#F4E3C8")
s.rect(30, 196, 150, 330, "#2C3A5A"); s.rect(33, 199, 147, 327, "#3D4E6E"); s.line(33, 199, 70, 260, "#5A6E90"); s.line(40, 199, 80, 270, "#4C5E80")
s.rect(160, 196, 230, 340, "#3B2A24"); s.rect(164, 200, 226, 340, "#4E3A30"); s.rect(170, 210, 220, 260, "#2C3A5A"); s.px(218, 290, "#C9A24A"); s.px(219, 290, "#C9A24A")
# boxes inside window
for i, (x, y) in enumerate([(50, 300), (78, 306), (60, 284)]): s.rect(x, y, x + 24, y + 20, "#B0804E"); s.line(x, y + 4, x + 24, y + 4, "#8A5E36"); s.rect(x + 10, y, x + 13, y + 4, "#D8C4A2")
# steps
s.rect(140, 340, 250, 352, "#7A7684"); s.rect(130, 352, 260, 364, "#8E8A96"); s.rect(120, 364, 270, 376, "#7A7684")
s.rect(0, 376, W - 1, H - 1, "#3A3E4E"); s.rect(0, 376, W - 1, 379, "#5A5E70")
for i in range(18): x = (i * 37) % W; s.rect(x, 400 + (i * 13) % 70, x + 18 + (i % 3) * 6, 401 + (i * 13) % 70, "#5E6E90")
save(s, "shop")
for i in range(2):
    g = new(44, 28); g.line(14, 0, 22, 8, "#C9CED6"); g.line(30, 0, 22, 8, "#C9CED6"); g.rect(2, 8, 41, 27, "#FFF4E0" if i == 0 else "#E0453A"); g.rect(4, 10, 39, 25, "#E0453A" if i == 0 else "#FFF4E0"); g.outline(OL); save(g, f"sign{i}")

# ================= OFFICE =================
s = new()
s.rect(0, 0, W - 1, 400, "#DCE8F0")
for x in range(0, W, 30): s.line(x, 0, x, 400, "#CFDDE8")
s.rect(0, 400, W - 1, H - 1, "#8C9AAE"); s.noise(0, 400, W - 1, H - 1, "#7E8CA0", density=.08, seed=3, only="#8C9AAE")
s.rect(150, 160, 260, 300, "#2C3A5A"); s.gradient_dither(153, 163, 257, 297, ["#7FC3F0", "#BFE3FA"], pattern="bayer4")
for i, hh in enumerate([60, 90, 50, 110, 70, 80]): s.rect(155 + i * 17, 297 - hh, 168 + i * 17, 297, "#7C93BC"); s.rect(158 + i * 17, 297 - hh + 6, 160 + i * 17, 297 - hh + 8, "#FFFFFF")
s.rect(20, 190, 130, 270, "#FFFFFF"); s.rect(18, 188, 132, 190, "#8C9AAE"); s.rect(18, 270, 132, 273, "#8C9AAE")
pts = [(30, 258), (50, 250), (66, 254), (84, 236), (100, 228), (120, 204)]
for a, b in zip(pts, pts[1:]): s.line(a[0], a[1], b[0], b[1], "#28A86A"); s.line(a[0], a[1] - 1, b[0], b[1] - 1, "#28A86A")
s.polygon([(120, 200), (124, 208), (114, 206)], "#28A86A")
for i in range(5): s.rect(30 + i * 20, 262 - i * 6, 38 + i * 20, 266, "#4C9AFF")
s.rect(110, 340, 230, 346, "#F4F1EA"); s.rect(116, 346, 120, 400, "#B8BEC8"); s.rect(220, 346, 224, 400, "#B8BEC8")
s.rect(10, 360, 40, 400, "#E07A5F"); s.circle(25, 350, 14, "#3E8E5A", fill=True); s.circle(20, 344, 8, "#4CAF6E", fill=True)
save(s, "office")

# ================= LIBRARY (grid tile) =================
s = new(); s.rect(0, 0, W - 1, H - 1, "#5A3A2E")
R = random.Random(6); cols = ["#FF7A59", "#FFC145", "#6CC7A3", "#4C9AFF", "#B07CFF", "#E0453A", "#F4E3C8"]
for sy in range(120, 400, 46):
    s.rect(10, sy, 260, sy + 4, "#3B2A24"); x = 14
    while x < 255:
        w = R.randint(5, 9); h = R.randint(28, 40); s.rect(x, sy - h, x + w - 1, sy - 1, R.choice(cols)); x += w + 1
s.rect(0, 400, W - 1, H - 1, "#8A5A3C")
save(s, "library")

# ================= BIG BOOK (field close-up: open book, blank right page) =================
b = new(150, 96)
b.polygon([(2, 90), (74, 94), (74, 8), (4, 4)], "#FFF4E0"); b.polygon([(76, 94), (148, 90), (146, 4), (76, 8)], "#FFF4E0")
b.dither(2, 4, 74, 94, "keep", "#EADBB8", mix=.12, pattern="bayer4", only="#FFF4E0")
b.line(75, 8, 75, 94, "#C9B48A"); b.polygon([(0, 92), (75, 96), (150, 92), (150, 95), (75, 95), (0, 95)], "#6A4FD1")
for y in range(18, 88, 8): b.line(10, y, 68, y + 1, "#E3D3AE"); b.line(82, y + 1, 140, y, "#E3D3AE")
b.outline(OL); save(b, "bigbook")
print("scenes ok")
