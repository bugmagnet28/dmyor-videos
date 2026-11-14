// =================== HABIT ROAST #1: crunches (you can't choose where fat comes off) ===================
var FLAT = [.62, .63, .61, .62, .63, .62], DOWN = [.62, .58, .52, .47, .43, .38];
function gymFloor(u) { rect(0, 0, W, H, "#2A2245"); for (var i = 0; i < 14; i++) rect(i * 20, 0, 1, 380, "#262040"); rect(0, 380, W, H - 380, "#3A3560"); rect(0, 380, W, 2, "#4A4470"); }
function cruncher(u, x, fast) { mat(x - 4, 376, 60); chr(Math.floor(u * (fast ? 4 : 2)) % 2 ? "crouch" : "sit_bed", x, 327); }
function fatChart(u, pts, k, title, col) { var g = lineChart(26, 150, 218, 120, [{ pts: pts, col: col, k: k }], title); ptext(L, "WEEK 1", g.gx, g.gy + 3, 1, "#9A92C0"); ptext(L, "WEEK 6", g.gx + g.gw - 34, g.gy + 3, 1, "#9A92C0"); return g; }
// S1: 1,000 crunches a day, belly line flat (frame 0)
function sHook(u, a, b) {
  gymFloor(u); fatChart(u, FLAT, 1, "BELLY FAT", "#E0453A"); cruncher(u, 60, true);
  counter(150, 292, "CRUNCHES TODAY", "1,000", "#FFC145", 3);
  if (u > LN("S1", 1)) { ptext(L, "UNCHANGED", 236 - pwidth("UNCHANGED", 1), 182, 1, "#E0453A"); }
  return camAt([[0, 135, 250, 1.12], [b, 135, 255, 1.16, b]], u);
}
// S2: the twist: muscle under, fat over; crunches train the muscle, not the fat
function torso(u, glow, drain) {
  var cx = 135, top = 176; rect(cx - 18, top - 34, 36, 34, "#E0A57A"); rect(cx - 12, top - 30, 24, 8, "#5A3826"); rect(cx - 56, top, 112, 170, "#E0A57A"); rect(cx - 56, top, 112, 4, "#C98A5E");
  var fat = Math.round(20 * (1 - drain)); rect(cx - 56 - fat, top + 30, fat, 120, "#F2C9A0"); rect(cx + 56, top + 30, fat, 120, "#F2C9A0");
  for (var r = 0; r < 4; r++) for (var c = 0; c < 2; c++) { var x = cx - 34 + c * 36, y = top + 30 + r * 30; rect(x, y, 32, 26, "#B5523A"); if (glow) { rect(x, y, 32, 3, "#FF9F80"); } }
  L.fillStyle = "rgba(242,201,160," + (.8 * (1 - drain)) + ")"; for (var yy = top + 26; yy < top + 152; yy++) for (var xx = cx - 40; xx < cx + 40; xx++) if (bay(xx, yy) < .45) L.fillRect(xx, yy, 1, 1);
}
function sTwist(u, a, b) {
  gymFloor(u); var m = LN("S2", 1); torso(u, u > m + .3, 0);
  if (u > m + .3) { rect(30, 160, 84, 14, "#1A1530"); ptext(L, "ABS: STRONGER", 34, 164, 1, "#6CC7A3"); }
  if (u > m + 1.6) { rect(180, 160, 70, 14, "#1A1530"); ptext(L, "FAT: SAME", 186, 164, 1, "#E0453A"); ptext(L, "YOUR BODY PICKS", 135 - pwidth("YOUR BODY PICKS", 1) / 2, 336, 1, "#FFE066"); ptext(L, "WHERE FAT LEAVES", 135 - pwidth("WHERE FAT LEAVES", 1) / 2, 346, 1, "#FFE066"); }
  return camAt([[a, 135, 250, 1.2], [b, 135, 250, 1.28, b - a]], u);
}
// S3: the fix: 100 crunches + a walk + a better plate; the line finally drops
function sFix(u, a, b) {
  gymFloor(u); var k = seg(u, a + .3, LE("S3", 0)); fatChart(u, DOWN, k, "BELLY FAT", "#28A86A");
  counter(30, 292, "CRUNCHES", "" + Math.round(lerp(1000, 100, eio(seg(u, a, a + 1)))), "#FFFFFF", 3);
  chr("walk" + (Math.floor(u * 7) % 4), 150, 327); plateIcon(230, 310);
  return camAt([[a, 135, 255, 1.12], [b, 135, 255, 1.16, b - a]], u);
}
// S4: loop: frame-0 chart, now going down
function sEnd(u, a, b) { gymFloor(u); fatChart(u, DOWN, 1, "BELLY FAT", "#28A86A"); cruncher(u, 60, false); counter(150, 292, "CRUNCHES TODAY", "100", "#FFFFFF", 3); return camAt([[a, 135, 255, 1.16], [b, 135, 250, 1.12, b - a]], u); }

var SCENES = [["S1", sHook], ["S2", sTwist], ["S3", sFix], ["S4", sEnd]];
var EP = {
  badge: "HABIT ROAST #1", badgeBg: ROAST.badgeBg, badgeFg: ROAST.badgeFg, hook: "1,000 CRUNCHES. *BELLY: SAME.*", hookEnd: LN("S1", 1) + .5,
  endAt: function () { return LN("S4", 0); }, endQ: "HOW MANY ARE *YOU* ON?",
  titles: [["CRUNCHES DON'T PICK WHICH *FAT* LEAVES.", LN("S2", 1), SCN.S2[1], 300, 8],
           ["SEND TO YOUR *CRUNCH #600* FRIEND.", LN("S3", 1), SCN.S3[1], 300, 8]]
};
