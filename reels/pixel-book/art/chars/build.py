# Pixel character rig: one parametric person, drawn per pose with Pixel Art Studio. Facing right (+x).
import sys, math, json; sys.path.insert(0, "/Users/sanyampathak/Documents/dmyor-videos/.claude/skills/pixel-art-studio/scripts")
from pixelstudio import Sprite, ramp, mix
from PIL import Image
OUT = "/Users/sanyampathak/Documents/dmyor-videos/reels/pixel-book/art/chars/"
CW, CH, GY = 48, 56, 53                     # canvas, ground line
OL = "#2A1F2E"
def kit(shirt, pants, skin, hair, shoes="#1E2233"):
    return dict(SH=ramp(shirt, 3, hue_shift=16), PA=ramp(pants, 3, hue_shift=12), SK=ramp(skin, 3, hue_shift=10), HA=hair, SO=shoes)
OUTFITS = {
    "young": dict(kit("#FF7A59", "#34477A", "#F2C6A0", "#3B2416"), style="young"),
    "older": dict(kit("#2B3150", "#3A3A4C", "#E8B992", "#2A1A12"), style="older"),
    "client": dict(kit("#4C9AFF", "#2C3346", "#9C6644", "#141018"), style="client"),
}
L = dict(torso=13, ua=7, fa=7, th=9, sn=9)
def vec(a, l): return (math.sin(a) * l, math.cos(a) * l)
def limb(s, a, b, w, c):
    dx, dy = b[0] - a[0], b[1] - a[1]; n = math.hypot(dx, dy) or 1; nx, ny = -dy / n * w / 2, dx / n * w / 2
    s.polygon([(a[0] + nx, a[1] + ny), (b[0] + nx, b[1] + ny), (b[0] - nx, b[1] - ny), (a[0] - nx, a[1] - ny)], c)
    s.circle(round(b[0]), round(b[1]), max(1, int(w // 2)), c, fill=True)
def R(p): return (round(p[0]), round(p[1]))
def person(s, P, O, ox=0, oy=0):
    """P: hip(x,y), lean, head(tilt px), shL elL shR elR hipL knL hipR knR (radians, 0 = straight down, + = forward)."""
    hx, hy = P["hip"][0] + ox, P["hip"][1] + oy
    lean = P.get("lean", 0); sh = (hx + math.sin(lean) * L["torso"], hy - math.cos(lean) * L["torso"])
    def leg(hipa, kna, c, cs):
        k = (hx + vec(hipa, L["th"])[0], hy + vec(hipa, L["th"])[1]); f = (k[0] + vec(hipa + kna, L["sn"])[0], k[1] + vec(hipa + kna, L["sn"])[1])
        limb(s, (hx, hy), k, 5, c); limb(s, k, f, 4, c)
        s.rect(round(f[0]) - 2, round(f[1]) - 1, round(f[0]) + 3, round(f[1]) + 1, cs)
    def arm(sa, ea, c, cs, hand):
        e = (sh[0] + vec(sa, L["ua"])[0], sh[1] + 1 + vec(sa, L["ua"])[1]); h = (e[0] + vec(sa + ea, L["fa"])[0], e[1] + vec(sa + ea, L["fa"])[1])
        limb(s, (sh[0], sh[1] + 1), e, 4, c); limb(s, e, h, 3, cs if P.get("sleeve") == "short" else c)
        s.rect(round(h[0]) - 1, round(h[1]) - 1, round(h[0]) + 1, round(h[1]) + 1, hand)
    if not P.get("noLegs"):
        leg(P.get("hipL", 0), P.get("knL", 0), O["PA"][0], mix(O["SO"], "#000000", .2))
    arm(P.get("shL", 0), P.get("elL", 0), O["SH"][0], O["SK"][0], O["SK"][0])
    # torso
    tw = 5
    nx, ny = math.cos(lean) * tw, math.sin(lean) * tw
    s.polygon([(hx - nx, hy - ny), (hx + nx, hy + ny), (sh[0] + nx * .9, sh[1] + ny * .9), (sh[0] - nx * .9, sh[1] - ny * .9)], O["SH"][1])
    s.polygon([(hx - nx, hy - ny), (hx - nx * .3, hy - ny * .3), (sh[0] - nx * .3, sh[1] - ny * .3), (sh[0] - nx * .9, sh[1] - ny * .9)], mix(O["SH"][0], O["SH"][1], .5))
    if O["style"] == "older":   # open jacket shows white shirt + tie
        s.line(round(sh[0] + nx * .2), round(sh[1]) + 1, round(hx + nx * .3), round(hy) - 2, "#F4F1EA"); s.line(round(sh[0] + nx * .5), round(sh[1]) + 1, round(hx + nx * .6), round(hy) - 3, "#F4F1EA")
        s.line(round(sh[0] + nx * .35), round(sh[1]) + 2, round(hx + nx * .45), round(hy) - 4, "#C0392B")
    s.rect(round(hx - nx) , round(hy) - 1, round(hx + nx), round(hy) + 1, O["PA"][1])
    if not P.get("noLegs"):
        leg(P.get("hipR", 0), P.get("knR", 0), O["PA"][1], O["SO"])
    # head
    tilt = P.get("head", 0); hdx = math.sin(lean) * 8 + tilt * .5 + 1; hdy = -8 + abs(tilt) * .4
    cx, cy = round(sh[0] + hdx), round(sh[1] + hdy)
    s.rect(round(sh[0]) - 1, round(sh[1]) - 3, round(sh[0]) + 1, round(sh[1]), O["SK"][0])
    s.circle(cx, cy, 6, O["SK"][1], fill=True); s.px(cx + 7, cy, O["SK"][1]); s.px(cx + 6, cy + 1, O["SK"][1])
    s.rect(cx - 4, cy - 1, cx - 3, cy + 1, O["SK"][0])
    HA = O["HA"]
    if O["style"] == "young":
        s.polygon([(cx - 6, cy - 4), (cx - 3, cy - 7), (cx + 2, cy - 7), (cx + 6, cy - 4), (cx + 5, cy - 3), (cx + 1, cy - 4), (cx - 1, cy - 1), (cx - 2, cy + 2), (cx - 5, cy + 3), (cx - 6, cy)], HA)
        s.line(cx - 3, cy - 6, cx + 1, cy - 6, mix(HA, "#FFFFFF", .2))
    elif O["style"] == "older":
        s.polygon([(cx - 6, cy - 3), (cx - 4, cy - 7), (cx + 3, cy - 8), (cx + 6, cy - 5), (cx + 2, cy - 4), (cx - 1, cy - 2), (cx - 3, cy + 2), (cx - 6, cy + 1)], HA)
        s.polygon([(cx - 1, cy + 2), (cx + 6, cy + 2), (cx + 5, cy + 5), (cx + 1, cy + 6), (cx - 2, cy + 4)], mix(HA, O["SK"][1], .25))   # beard
    else:
        s.polygon([(cx - 6, cy - 3), (cx - 3, cy - 7), (cx + 3, cy - 7), (cx + 6, cy - 3), (cx + 3, cy - 4), (cx - 2, cy - 3), (cx - 3, cy + 2), (cx - 6, cy + 1)], HA)
    # near arm (over torso)
    arm(P.get("shR", 0), P.get("elR", 0), mix(O["SH"][1], O["SH"][2], .3) if O["style"] != "older" else O["SH"][1], O["SK"][1], O["SK"][2])
    for extra in P.get("extra", []): extra(s, cx, cy, sh, (hx, hy))
    return cx, cy

def face(s, cx, cy, P, O):
    m = P.get("face", "calm")
    if P.get("blink"): s.line(cx + 3, cy, cx + 4, cy, "#1C1A24")
    elif m == "shock": s.rect(cx + 3, cy - 1, cx + 4, cy + 1, "#FFFFFF"); s.px(cx + 4, cy, "#1C1A24")
    else: s.px(cx + 4, cy - 1, "#1C1A24"); s.px(cx + 4, cy, "#1C1A24")
    if m == "sad": s.line(cx + 2, cy - 3, cx + 4, cy - 2, O["HA"])
    else: s.line(cx + 3, cy - 3, cx + 5, cy - 3, O["HA"])
    if O["style"] == "older": return
    if m == "shock": s.rect(cx + 4, cy + 3, cx + 5, cy + 4, "#7A2E2E")
    elif m == "happy": s.line(cx + 3, cy + 3, cx + 5, cy + 3, "#B8584E"); s.px(cx + 2, cy + 2, "#B8584E")
    elif m == "sad": s.line(cx + 3, cy + 4, cx + 5, cy + 4, "#8A4A44")
    else: s.line(cx + 4, cy + 3, cx + 5, cy + 3, "#B8584E")
    s.px(cx + 5, cy + 1, "#F4A7A0")

def render(name, P, O, w=CW, h=CH):
    s = Sprite(w, h, snap=False)
    cx, cy = person(s, P, OUTFITS[O])
    s.outline(OL, where="outside")
    face(s, cx, cy, P, OUTFITS[O])
    for post in P.get("post", []): post(s)
    s.save_png(OUT + name + ".png")
    return s

H0 = (24, 35)            # standing hip
SIT = (18, 40)           # sitting on chair-height hip
D = math.radians
POSES = {}
POSES["stand"] = ("young", dict(hip=H0, shL=D(8), elL=D(10), shR=D(-6), elR=D(12), hipL=D(4), hipR=D(-4)))
POSES["blink"] = ("young", dict(POSES["stand"][1], blink=True))
POSES["shock"] = ("young", dict(hip=H0, lean=D(-8), shL=D(-28), elL=D(-10), shR=D(30), elR=D(10), hipL=D(10), hipR=D(-10), face="shock"))
for i in range(4):
    p = math.sin(i / 4 * 2 * math.pi)
    POSES[f"walk{i}"] = ("young", dict(hip=(H0[0], H0[1] - abs(math.cos(i / 4 * 2 * math.pi)) * 1), lean=D(4), shL=D(-30 * p), elL=D(20), shR=D(30 * p), elR=D(20),
                                       hipL=D(28 * p), knL=D(-28 * max(0, -p) - 6), hipR=D(-28 * p), knR=D(-28 * max(0, p) - 6), face="calm"))
    POSES[f"owalk{i}"] = ("older", POSES[f"walk{i}"][1])
POSES["ostand"] = ("older", dict(hip=H0, shL=D(6), elL=D(8), shR=D(-4), elR=D(10), hipL=D(4), hipR=D(-4)))
POSES["olook"] = ("older", dict(hip=H0, lean=D(-4), head=-3, shL=D(6), elL=D(8), shR=D(30), elR=D(90), hipL=D(4), hipR=D(-4)))
POSES["sit_write0"] = ("young", dict(hip=SIT, lean=D(14), head=2, shL=D(50), elL=D(40), shR=D(60), elR=D(30), hipL=D(85), knL=D(-85), hipR=D(90), knR=D(-90)))
POSES["sit_write1"] = ("young", dict(POSES["sit_write0"][1], shR=D(66), elR=D(26)))
POSES["sit_type0"] = ("young", dict(hip=SIT, lean=D(10), shL=D(55), elL=D(40), shR=D(62), elR=D(36), hipL=D(85), knL=D(-85), hipR=D(90), knR=D(-90)))
POSES["sit_type1"] = ("young", dict(POSES["sit_type0"][1], shL=D(60), shR=D(57)))
POSES["sit_bed"] = ("young", dict(hip=SIT, lean=D(-4), shL=D(10), elL=D(20), shR=D(18), elR=D(30), noLegs=True, face="calm"))
POSES["sit_bed_blink"] = ("young", dict(POSES["sit_bed"][1], blink=True))
POSES["stretch"] = ("young", dict(hip=SIT, lean=D(-6), shL=D(165), elL=D(-10), shR=D(160), elR=D(-10), noLegs=True, face="happy"))
POSES["wave_off"] = ("young", dict(hip=H0, shL=D(8), elL=D(10), shR=D(100), elR=D(70), hipL=D(4), hipR=D(-4), face="happy"))
POSES["sad"] = ("young", dict(hip=(20, 44), lean=D(30), head=4, shL=D(40), elL=D(20), shR=D(45), elR=D(15), hipL=D(70), knL=D(-120), hipR=D(75), knR=D(-125), face="sad"))
POSES["sad_blink"] = ("young", dict(POSES["sad"][1], blink=True))
POSES["shake0"] = ("young", dict(hip=H0, shL=D(8), elL=D(10), shR=D(70), elR=D(15), hipL=D(4), hipR=D(-4), face="happy"))
POSES["shake1"] = ("young", dict(POSES["shake0"][1], shR=D(62), elR=D(25)))
POSES["cshake0"] = ("client", dict(POSES["shake0"][1]))
POSES["cshake1"] = ("client", dict(POSES["shake1"][1]))
POSES["sit_read"] = ("young", dict(hip=(16, 46), lean=D(-12), head=1, shL=D(45), elL=D(35), shR=D(50), elR=D(40), hipL=D(130), knL=D(-150), hipR=D(125), knR=D(-145), face="calm"))
POSES["sit_read_blink"] = ("young", dict(POSES["sit_read"][1], blink=True))
POSES["sit_read_happy"] = ("young", dict(POSES["sit_read"][1], face="happy"))
for n, (o, p) in POSES.items(): render(n, p, o)
names = list(POSES)
sheet = Image.new("RGBA", (CW * 8 * 4, CH * ((len(names) + 7) // 8) * 4), "#3A3F55")
for i, n in enumerate(names):
    im = Image.open(OUT + n + ".png").resize((CW * 4, CH * 4), Image.NEAREST); sheet.alpha_composite(im, ((i % 8) * CW * 4, (i // 8) * CH * 4))
sheet.save(OUT + "_sheet.png"); json.dump({"w": CW, "h": CH, "ground": GY, "names": names}, open(OUT + "chars.json", "w")); print(len(names), "poses")
