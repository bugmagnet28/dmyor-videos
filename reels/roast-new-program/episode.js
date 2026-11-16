// =================== HABIT ROAST #7: new program every Monday (muscles don't get confused) ===================
var FLAT = [.3, .31, .3, .32, .3, .31, .3, .31], STAIR = [.3, .36, .42, .48, .55, .62, .7, .78];
function gym(u) { rect(0, 0, W, H, "#2A2245"); for (var i = 0; i < 14; i++) rect(i * 20, 0, 1, 380, "#262040"); rect(0, 380, W, H - 380, "#3A3560"); rect(0, 380, W, 2, "#4A4470"); }
function barbell(cx, y, plates) { rect(cx - 70, y, 140, 3, "#C8C0E8"); for (var i = 0; i < plates; i++) { rect(cx - 56 + i * 5, y - 10, 4, 23, "#E0453A"); rect(cx + 52 - i * 5, y - 10, 4, 23, "#E0453A"); } }
function liftChart(u, pts, k, col) { var g = lineChart(26, 140, 218, 120, [{ pts: pts, col: col, k: k }], "BENCH PRESS (KG)"); ptext(L, "WEEK 1", g.gx, g.gy + 3, 1, "#9A92C0"); ptext(L, "WEEK 8", g.gx + g.gw - 34, g.gy + 3, 1, "#9A92C0"); return g; }
function cards(n, x, y) { for (var i = 0; i < n; i++) { var cx = x + i * 4, cy = y - i * 3; rect(cx - 1, cy - 1, 52, 30, "#1A1530"); rect(cx, cy, 50, 28, i % 2 ? "#FFF4E0" : "#F2E6CC"); ptext(L, "PLAN " + (i + 1), cx + 6, cy + 4, 1, "#3A3560"); rect(cx + 6, cy + 14, 36, 2, "#8A86A8"); rect(cx + 6, cy + 20, 26, 2, "#8A86A8"); } }
// S1 (frame 0): 8 program cards stacked, bench line flat
function sHook(u, a, b) {
  gym(u); liftChart(u, FLAT, 1, "#E0453A"); cards(Math.min(8, 1 + Math.floor(u * 3)), 150, 312);
  counter(24, 290, "PROGRAMS", "" + Math.min(8, 1 + Math.floor(u * 3)), "#FFC145", 3); chr("stand", 92, 327);
  return camAt([[0, 135, 250, 1.12], [b, 135, 255, 1.16, b]], u);
}
// S2: "confuse your muscles" crossed out; the staircase of the same lift getting heavier
function sTwist(u, a, b) {
  gym(u); var m = LN("S2", 1), k = seg(u, m + 1.4, m + 4.4);
  signCard(135, 136, ["CONFUSE THE MUSCLES"], "#FFC145", "#1A1530", 1, seg(u, a, a + .3)); if (u > m) rect(70, 144, 130, 2, "#E0453A");
  if (u > m + 1) { liftChart(u, STAIR, k, "#28A86A"); }
  barbell(135, 330, 1 + Math.floor(k * 5)); chr(u > m ? "lookup" : "stand", 20, 327);
  return camAt([[a, 135, 240, 1.18], [b, 135, 250, 1.24, b - a]], u);
}
// S3: one program, 8 weeks: calendar fills with ticks, plates added
function sFix(u, a, b) {
  gym(u); var k = seg(u, LN("S3", 0) + .4, LE("S3", 1)); var cells = []; for (var i = 0; i < 24; i++) cells.push("tick");
  rect(40, 124, 190, 14, "#1A1530"); ptext(L, "1 PROGRAM X 8 WEEKS", 70, 128, 1, "#6CC7A3");
  monthGrid(86, 160, cells, 4, k * .99); barbell(135, 330, 1 + Math.floor(k * 6));
  if (u > LN("S3", 1)) { rect(50, 230, 170, 16, "#1A1530"); ptext(L, "+1 REP OR +2.5 KG A WEEK", 60, 235, 1, "#FFE066"); }
  chr("crouch", 111, 327);
  return camAt([[a, 135, 250, 1.12], [b, 135, 252, 1.16, b - a]], u);
}
function sEnd(u, a, b) { gym(u); liftChart(u, STAIR, 1, "#28A86A"); cards(1, 150, 312); counter(24, 290, "PROGRAMS", "1", "#FFFFFF", 3); chr("jump", 92, 327); return camAt([[a, 135, 255, 1.16], [b, 135, 250, 1.12, b - a]], u); }

var SCENES = [["S1", sHook], ["S2", sTwist], ["S3", sFix], ["S4", sEnd]];
var EP = {
  badge: "HABIT ROAST #7", badgeBg: ROAST.badgeBg, badgeFg: ROAST.badgeFg, hook: "8 PROGRAMS. *SAME WEIGHT.*", hookEnd: LN("S1", 1) + .5,
  endAt: function () { return LN("S4", 0); }, endQ: "HOW MANY PROGRAMS HAVE *YOU* SAVED?",
  titles: [["MUSCLES DON'T GET *CONFUSED.*", LN("S2", 1), SCN.S2[1], 300, 9],
           ["SEND TO YOUR *40 SAVED WORKOUTS* FRIEND.", LN("S3", 2), SCN.S3[1], 300, 8]]
};
