// =================== HABIT ROAST #2: every run all out (most runs should be easy) ===================
var SAME = ["32:10", "32:05", "32:20", "32:00", "32:15", "32:10"], FAST = ["32:10", "31:30", "30:50", "30:05", "29:20", "28:40"];
function track(u) { rect(0, 0, W, H, "#2E4A3A"); rect(0, 0, W, 150, "#8FD3FF"); rect(0, 150, W, 6, "#3C7A50"); rect(0, 330, W, 50, "#C2566A"); for (var i = 0; i < 4; i++) rect(0, 334 + i * 12, W, 1, "#FFFFFF"); rect(0, 380, W, H - 380, "#2E4A3A"); }
function times(u, vals, n, col, title) {
  rect(20, 148, 230, 124, "#1A1530"); rect(22, 150, 226, 120, "#FFF4E0"); ptext(L, title, 30, 156, 1, "#3A3560");
  for (var i = 0; i < n; i++) { var v = parseInt(vals[i]) * 60 + parseInt(vals[i].split(":")[1]), h = (v - 1600) / 340 * 80 + 10; var x = 34 + i * 35; h *= .85; rect(x, 258 - h, 24, h, col); ptext(L, vals[i], x - 2, 248 - h, 1, "#3A3560"); ptext(L, "W" + (i + 1), x + 6, 261, 1, "#9A92C0"); }
}
function runner(u, x, mode) { var f = mode === "sprint" ? 10 : 6; chr("walk" + (Math.floor(u * f) % 4), x, 330 - GY + 4); if (mode === "sprint") { rect(x + 30, 290, 2, 2, "#7FD4FF"); rect(x + 34, 296, 2, 2, "#7FD4FF"); } }
function effort(v, x, y) { rect(x - 1, y - 1, 92, 16, "#1A1530"); rect(x, y, 90, 14, "#2A2245"); rect(x, y, 90 * v, 14, v > .8 ? "#E0453A" : "#28A86A"); ptext(L, "EFFORT " + Math.round(v * 100) + "%", x + 4, y + 4, 1, "#FFFFFF"); }
// S1: every run 100%, the 5K time doesn't move (frame 0)
function sHook(u, a, b) { track(u); times(u, SAME, 6, "#E0453A", "5K TIME, WEEK BY WEEK"); runner(u, (u * 40 + 70) % 300 - 40, "sprint"); effort(1, 160, 290); return camAt([[0, 135, 250, 1.12], [b, 135, 252, 1.15, b]], u); }
// S2: the twist: good runners do most runs easy, easy enough to talk
function sTwist(u, a, b) {
  track(u); var k = seg(u, LN("S2", 1), LN("S2", 1) + 1.2);
  rect(20, 160, 230, 40, "#1A1530"); rect(22, 162, 226 * .8 * k, 36, "#28A86A"); if (k > .99) { rect(22 + 226 * .8, 162, 226 * .2, 36, "#E0453A"); ptext(L, "4 OF 5 EASY", 40, 176, 2, "#FFFFFF"); ptext(L, "HARD", 210, 176, 1, "#FFFFFF"); }
  runner(u, 90, "easy"); if (u > LN("S2", 1) + .8) { bubble(126, 250, 92, 16, 116); ptext(L, "...SO ANYWAY,", 132, 255, 1, "#1A1530"); }
  effort(.6, 160, 290);
  return camAt([[a, 135, 250, 1.15], [b, 135, 255, 1.2, b - a]], u);
}
// S3: the fix: four easy, one hard, and the time starts dropping
function sFix(u, a, b) {
  track(u); var w = ["EASY", "EASY", "EASY", "EASY", "HARD"];
  w.forEach(function (s, i) { var k = seg(u, a + .2 + i * .25, a + .4 + i * .25); if (k <= 0) return; var x = 22 + i * 46; rect(x, 280, 42, 18, "#1A1530"); rect(x + 1, 281, 40, 16, s === "EASY" ? "#28A86A" : "#E0453A"); ptext(L, s, x + 21 - pwidth(s, 1) / 2, 286, 1, "#FFFFFF"); });
  times(u, FAST, Math.min(6, 1 + Math.floor(seg(u, LN("S3", 1), LE("S3", 1)) * 5.99)), "#28A86A", "5K TIME, WEEK BY WEEK");
  runner(u, 80, "easy");
  return camAt([[a, 135, 250, 1.12], [b, 135, 252, 1.15, b - a]], u);
}
function sEnd(u, a, b) { track(u); times(u, FAST, 6, "#28A86A", "5K TIME, WEEK BY WEEK"); runner(u, (u * 25) % 300 - 40, "easy"); effort(.6, 160, 290); return camAt([[a, 135, 252, 1.15], [b, 135, 250, 1.12, b - a]], u); }

var SCENES = [["S1", sHook], ["S2", sTwist], ["S3", sFix], ["S4", sEnd]];
var EP = {
  badge: "HABIT ROAST #2", badgeBg: ROAST.badgeBg, badgeFg: ROAST.badgeFg, hook: "EVERY RUN ALL OUT. *SAME TIME.*", hookEnd: LN("S1", 1) + .5,
  endAt: function () { return LN("S4", 0); }, endQ: "CAN YOU *TALK* ON YOUR RUNS?",
  titles: [["SLOW IS HOW YOU GET *FAST.*", LN("S2", 0), SCN.S2[1], 300, 9],
           ["SEND TO YOUR *WARM-UP SPRINTER.*", LN("S3", 2), SCN.S3[1], 300, 8]]
};
