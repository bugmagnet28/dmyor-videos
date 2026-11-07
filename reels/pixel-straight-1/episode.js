// =================== STRAIGHT ANSWER #1: "Nothing shows yet" (Reason #5: progress is invisible at first) ===================
var GY0 = 236;                         // ground line
function sky(u) { var C = ["#8FD3FF", "#A8DDFF", "#C2E8FF", "#DDF2FF"]; for (var i = 0; i < 4; i++) rect(0, i * 59, W, 59, C[i]); ddisc(220, 50, 16, "#FFF1A8", .9); }
function soil(u) { rect(0, GY0, W, H - GY0, "#6B4430"); rect(0, GY0, W, 4, "#4E9A4A"); rect(0, GY0 + 4, W, 2, "#3C7A3A");
  for (var i = 0; i < 160; i++) rect(hash(i) * W, GY0 + 8 + hash(i + 40) * 240, 2, 1, i % 3 ? "#5A3826" : "#7E5638"); for (var j = 0; j < 9; j++) rect(hash(j + 90) * W, GY0 + 30 + hash(j + 7) * 200, 5, 3, "#8A7A70"); }
function line(x0, y0, x1, y1, c, w) { var n = Math.max(Math.abs(x1 - x0), Math.abs(y1 - y0)); for (var i = 0; i <= n; i++) rect(lerp(x0, x1, i / n), lerp(y0, y1, i / n), w || 1, w || 1, c); }
function roots(x, y, ang, len, depth, grow, seed) {   // grow 0..1 across the whole tree
  if (depth < 0 || grow <= 0) return; var g = cl(grow * 4 - (3 - depth) * .9, 0, 1); if (g <= 0) return;
  var x1 = x + Math.cos(ang) * len * g, y1 = y + Math.sin(ang) * len * g; line(x, y, x1, y1, "#F2E6CC", depth > 1 ? 2 : 1);
  if (g >= 1) { roots(x1, y1, ang - .5 - hash(seed) * .3, len * .7, depth - 1, grow, seed * 2 + 1); roots(x1, y1, ang + .45 + hash(seed + 3) * .3, len * .68, depth - 1, grow, seed * 2 + 2); }
}
function seed(x, y) { rect(x - 3, y - 2, 7, 5, "#2A1F2E"); rect(x - 2, y - 1, 5, 3, "#C99A2E"); }
function sprout(x, k) { if (k <= 0) return; var h = Math.round(4 + 40 * k); rect(x, GY0 - h, 2, h, "#3C9A4A"); if (k > .3) { rect(x - 8, GY0 - h + 6, 8, 4, "#4EBA5A"); rect(x + 2, GY0 - h + 2, 8, 4, "#4EBA5A"); } if (k > .7) { rect(x - 12, GY0 - h + 18, 10, 5, "#4EBA5A"); rect(x + 2, GY0 - h + 14, 12, 5, "#4EBA5A"); ddisc(x + 1, GY0 - h, 6, "#FFE066", .8); } }
function field(u, rootK, sproutK, who) {
  sky(u); soil(u); seed(150, GY0 + 20); roots(150, GY0 + 20, Math.PI / 2, 66, 3, rootK, 1); sprout(150, sproutK);
  if (who) chr(who, 70, GY0 - GY);
}
// S1: an empty patch of soil, roots already huge underneath (frame 0)
function sHook(u, a, b) { field(u, .95, 0, blinkAt(u, .3) ? "blink" : "stand"); ptext(L, "?", 96, GY0 - 66 - 2 * Math.sin(u * 3), 2, "#3A3560"); return camAt([[0, 135, 270, 1.15], [b, 135, 270, 1.2, b]], u); }
function sWhy(u, a, b) { return whyScene(u, a, b); }
// S3: effort vs results
var EFF = [0, .14, .28, .42, .56, .7, .84, .98], RES = [0, .01, .02, .04, .08, .18, .45, 1];
function chartScene(u, a, effK, resK, gapK) {
  rect(0, 0, W, H, "#1A1530"); stars(u, 25, "#5A5590");
  var g = lineChart(20, 140, 230, 190, [{ pts: EFF, col: "#4C9AFF", k: effK }, { pts: RES, col: "#28A86A", k: resK }], "EFFORT VS. RESULTS");
  if (effK > .9) ptext(L, "EFFORT", g.gx + g.gw - 40, g.gy - .98 * (g.gh - 4) + 6, 1, "#4C9AFF");
  if (resK > .9) ptext(L, "RESULTS", g.gx + g.gw - 82, g.gy - .62 * (g.gh - 4), 1, "#28A86A");
  if (gapK > 0) { L.fillStyle = "rgba(224,69,58," + (.25 * gapK) + ")"; for (var t = .08; t < .7; t += .004) { var f = t * 7, i = Math.floor(f), r = f - i, e = lerp(EFF[i], EFF[i + 1], r), q = lerp(RES[i], RES[i + 1], r); var y0 = g.gy - 2 - e * (g.gh - 4), y1 = g.gy - 2 - q * (g.gh - 4); L.fillRect(Math.round(g.gx + t * g.gw), Math.round(y0 + 2), 1, Math.max(0, Math.round(y1 - y0 - 2))); }
    if (gapK > .6) { ptext(L, "THE GAP", g.gx + g.gw * .3, g.gy - 40, 2, "#E0453A"); ptext(L, "MOST PEOPLE QUIT HERE", 135 - pwidth("MOST PEOPLE QUIT HERE", 1) / 2, 342, 1, "#FF9F94"); } }
}
function sChart(u, a, b) { chartScene(u, a, seg(u, a + .2, LE("S3", 0)), seg(u, LN("S3", 1), LE("S3", 1) + .6), 0); return camAt([[a, 135, 236, 1.1], [b, 135, 236, 1.15, b - a]], u); }
// S4: weeks one to three: nothing above, roots below
function sWeeks(u, a, b) {
  var w = u < LN("S4", 1) ? 1 : (u < LN("S4", 2) ? 2 : 3), rk = u < LN("S4", 3) ? .08 + w * .1 : lerp(.38, .85, seg(u, LN("S4", 3), LE("S4", 3)));
  field(u, rk, 0, blinkAt(u, .2) ? "blink" : (w === 3 ? "sad" : "stand")); dayTag("WEEK " + w, 100, 120, "#FFFFFF", "#1A1530");
  return camAt([[a, 135, 200, 1.5], [LN("S4", 3), 135, 200, 1.5], [LN("S4", 3) + 1.4, 140, 300, 1.35, 1.4], [b, 140, 300, 1.35]], u);
}
function sGap(u, a, b) { chartScene(u, a, 1, 1, seg(u, a + .2, a + 1)); return camAt([[a, 135, 236, 1.1], [b, 120, 250, 1.3, b - a]], u); }
// S6: the scoreboard counts reps, not results
function sReps(u, a, b) {
  rect(0, 0, W, H, "#2A2245"); rect(30, 130, 210, 190, "#1A1530"); rect(33, 133, 204, 184, "#2E5A3E"); rect(33, 133, 204, 4, "#3C7A50");
  ptext(L, "SCOREBOARD", 135 - pwidth("SCOREBOARD", 2) / 2, 146, 2, "#FFFFFF"); ptext(L, "DID I SHOW UP?", 135 - pwidth("DID I SHOW UP?", 1) / 2, 172, 1, "#FFE066");
  var n = Math.floor(28 * seg(u, LN("S6", 1), LE("S6", 1) + .4));
  for (var i = 0; i < n; i++) { var grp = Math.floor(i / 5), k = i % 5, gx = 48 + (grp % 3) * 62, gy = 196 + Math.floor(grp / 3) * 44;
    if (k < 4) rect(gx + k * 8, gy, 3, 28, "#FFFFFF"); else line(gx - 3, gy + 24, gx + 33, gy + 4, "#FFFFFF", 2); }
  ptext(L, "REPS: " + n, 135 - pwidth("REPS: " + n, 2) / 2, 290, 2, "#B8F5C8");
  return camAt([[a, 135, 230, 1.15], [b, 135, 230, 1.2, b - a]], u);
}
// S7: the sprout breaks through (loops to frame 0's patch)
function sGrow(u, a, b) { var k = eout(seg(u, a + .3, LE("S7", 1))); field(u, .9, k, k > .8 ? (Math.floor(u * 3) % 2 ? "jump" : "stand") : "lookup"); return camAt([[a, 135, 230, 1.3], [b, 135, 240, 1, b - a]], u); }

var SCENES = [["S1", sHook], ["S2", sWhy], ["S3", sChart], ["S4", sWeeks], ["S5", sGap], ["S6", sReps], ["S7", sGrow]];
var EP = {
  badge: "STRAIGHT ANSWER #1", badgeBg: STRAIGHT.badgeBg, badgeFg: STRAIGHT.badgeFg, hook: "NOTHING SHOWS. *YET.*", hookEnd: LN("S1", 1) + .4,
  endAt: function () { return LN("S7", 3); }, endQ: "WHAT ARE YOU WAITING TO SEE *RESULTS* ON?",
  titles: [["WHY DO WE STOP DOING THINGS WE KNOW ARE *GOOD* FOR US?", LN("S2", 0), SCN.S2[1], 470, 8],
           ["REASON #5", LN("S2", 1), SCN.S2[1], 860, 14],
           ["PROGRESS IS *INVISIBLE* AT FIRST.", LN("S2", 1) + .5, SCN.S2[1], 1060, 7],
           ["COUNT *REPS*, NOT RESULTS.", LN("S6", 1), SCN.S6[1], 300, 8]]
};
