// =================== SMALL STORIES #1: "Same start" (Reason #8: the cost is now, the reward is later) ===================
// Split screen: left half x 0-134, right half x 136-270. Both people have the same desk, the same goal.
function half(x0, wall, wall2) { rect(x0, 0, 134, 380, wall); for (var i = 0; i < 7; i++) rect(x0 + i * 20, 0, 1, 380, wall2); rect(x0, 380, 134, 100, "#6B4430"); rect(x0, 392, 134, 1, "#5A3826");
  rect(x0 + 44, 214, 56, 60, "#E9E4D0"); rect(x0 + 47, 217, 50, 54, "#2A2E5E"); rect(x0 + 71, 217, 2, 54, "#E9E4D0"); rect(x0 + 47, 243, 50, 2, "#E9E4D0"); for (var j = 0; j < 8; j++) rect(x0 + 49 + hash(j + x0) * 46, 219 + hash(j + 5 + x0) * 22, 1, 1, "#FFFFFF");
  rect(x0 + 50, 256, 8, 15, "#1A1E44"); rect(x0 + 60, 250, 10, 21, "#1A1E44"); rect(x0 + 80, 254, 12, 17, "#1A1E44"); rect(x0 + 40, 274, 64, 3, "#D8D0B8"); }
function desk(x0, lit) {
  rect(x0 + 52, 336, 74, 6, "#8A5228"); rect(x0 + 56, 342, 4, 38, "#6B4430"); rect(x0 + 118, 342, 4, 38, "#6B4430");
  rect(x0 + 74, 318, 30, 18, "#2A1F2E"); rect(x0 + 76, 320, 26, 14, lit ? "#7FD4FF" : "#3A3560"); rect(x0 + 70, 336, 38, 2, "#2A1F2E");
  rect(x0 + 112, 316, 2, 20, "#2A1F2E"); rect(x0 + 106, 310, 14, 7, "#FFC145"); if (lit) ddisc(x0 + 113, 318, 20, "#FFE9A0", .25);
}
function note(x, y, s) { rect(x, y, 54, 14, "#FFE066"); rect(x, y, 54, 2, "#F2C94C"); ptext(L, s, x + 27 - pwidth(s, 1) / 2, y + 5, 1, "#E0453A"); }
function screenLines(x0, n) { for (var i = 0; i < n; i++) rect(x0 + 79, 323 + i * 3, 6 + (i * 7) % 16, 1, "#1A1530"); }
function bar(x0, v, col) { rect(x0 + 20, 150, 96, 10, "#1A1530"); rect(x0 + 21, 151, Math.max(0, 94 * v), 8, col); ptext(L, "PROGRESS", x0 + 20, 140, 1, "#FFFFFF"); }
function people(u, lWork, rNote) {
  half(0, "#3B4A7A", "#35436E"); half(136, "#3B4A7A", "#35436E"); rect(134, 0, 2, H, "#1A1530");
  desk(0, lWork); desk(136, false);
  chr(blinkAt(u, .3) ? "blink" : "stand", 30, 327);
  chr(blinkAt(u, .7) ? "olook" : "ostand", 166, 327);
  if (rNote) note(200, 290, "TOMORROW");
}
// S1: two people, same Monday (frame 0)
function sSame(u, a, b) { people(u, false, false); dayTag("MON", 46, 160); dayTag("MON", 182, 160); return camAt([[0, 135, 290, 1.1], [b, 135, 290, 1.12, b]], u); }
function sWhy(u, a, b) { return whyScene(u, a, b); }
// S3: twenty minutes vs "tomorrow"
function sDaily(u, a, b) {
  people(u, u > LN("S3", 0), u > LN("S3", 1));
  if (u > LN("S3", 0)) { var s = Math.max(0, 1200 - Math.floor((u - LN("S3", 0)) * 140)), t = Math.floor(s / 60) + ":" + ("0" + s % 60).slice(-2); rect(30, 284, 40, 14, "#1A1530"); ptext(L, t, 50 - pwidth(t, 1) / 2, 288, 1, "#B8F5C8"); screenLines(0, Math.floor((u - LN("S3", 0)) * 3) % 4); }
  return camAt([[a, 135, 280, 1.1], [b, 135, 280, 1.12, b - a]], u);
}
// S4: a week, a month: barely different
function sWeekMonth(u, a, b) {
  var m = u > LN("S4", 1); people(u, true, true); screenLines(0, 3);
  dayTag(m ? "1 MONTH" : "1 WEEK", 135 - pwidth(m ? "1 MONTH" : "1 WEEK", 3) / 2 - 5, 186, "#FFFFFF", "#1A1530");
  bar(0, m ? .09 : .025, "#28A86A"); bar(136, 0, "#28A86A");
  return camAt([[a, 135, 260, 1.1], [b, 135, 260, 1.12, b - a]], u);
}
// S5: the scale: cost now (heavy, close), reward later (far, faint)
function sScale(u, a, b) {
  rect(0, 0, W, H, "#1A1530"); stars(u, 30, "#5A5590");
  var tilt = .22 * eio(seg(u, a + .2, a + 1)); rect(133, 250, 4, 110, "#C8C0E8"); rect(110, 356, 50, 6, "#C8C0E8");
  L.save(); L.translate(135, 250); L.rotate(tilt); rect(-100, -2, 200, 4, "#C8C0E8");
  rect(-100, 0, 2, 30, "#9A92C0"); rect(-118, 30, 38, 4, "#C8C0E8"); rect(-114, 6, 30, 24, "#E0453A"); ptext(L, "20", -106, 12, 1, "#FFFFFF"); ptext(L, "MIN", -108, 20, 1, "#FFFFFF");
  rect(98, 0, 2, 30, "#9A92C0"); rect(80, 30, 38, 4, "#C8C0E8"); L.globalAlpha = .35 + .2 * Math.sin(u * 2); rect(90, 18, 18, 12, "#28A86A"); ptext(L, "?", 96, 21, 1, "#FFFFFF"); L.globalAlpha = 1; L.restore();
  if (u > LN("S5", 1)) { ptext(L, "TODAY", 20, 330, 2, "#E0453A"); ptext(L, "1 YEAR", 170, 330, 2, "#28A86A"); }
  return camAt([[a, 135, 280, 1.15], [b, 135, 280, 1.2, b - a]], u);
}
// S6: a year later: a finished thing vs a wall of notes
function finished(u, k) { if (k <= 0) return; var s = eout(k); L.save(); L.translate(64, 250); L.scale(s, s); rect(-30, -30, 60, 44, "#1A1530"); rect(-28, -28, 56, 40, "#FFF4E0"); rect(-28, -28, 56, 8, "#28A86A"); ptext(L, "LIVE", -11, -26, 1, "#FFFFFF");
  for (var i = 0; i < 4; i++) rect(-22, -14 + i * 6, 20 + (i * 9) % 24, 2, "#3A3560"); rect(10, -14, 14, 18, "#B8F5C8"); L.restore(); ddisc(64, 250, 40 * s, "#FFE9A0", .2); }
function sYear(u, a, b) {
  var y = u > LN("S6", 1) - .2; people(u, true, true); screenLines(0, 3);
  if (u < LN("S6", 1) - .2) { var k = seg(u, a, LN("S6", 1)); L.fillStyle = "rgba(20,15,46," + (.5 * Math.sin(k * Math.PI)) + ")"; L.fillRect(0, 0, W, H); dayTag("1 YEAR", 135 - pwidth("1 YEAR", 3) / 2 - 5, 186, "#FFFFFF", "#1A1530"); }
  if (y) { finished(u, seg(u, LN("S6", 1) - .2, LN("S6", 1) + .4)); bar(0, .9, "#28A86A"); }
  if (u > LN("S6", 2)) { for (var i = 0; i < 6; i++) note(144 + (i % 2) * 62, 170 + Math.floor(i / 2) * 18 + (i % 2) * 4, "TOMORROW"); bar(136, 0, "#28A86A"); }
  return camAt([[a, 135, 280, 1.1], [b, 135, 280, 1.12, b - a]], u);
}
// S7: close on the twenty minutes (loops to the same split frame)
function sClose(u, a, b) { people(u, true, true); finished(u, 1); bar(0, .9, "#28A86A"); bar(136, 0, "#28A86A"); return camAt([[a, 135, 280, 1.12], [LN("S7", 2), 135, 280, 1.1, 1.2]], u); }

var SCENES = [["S1", sSame], ["S2", sWhy], ["S3", sDaily], ["S4", sWeekMonth], ["S5", sScale], ["S6", sYear], ["S7", sClose]];
var EP = {
  badge: "SMALL STORIES #1", badgeBg: STORY.badgeBg, badgeFg: STORY.badgeFg, hook: "SAME DESK. SAME GOAL. *SAME START.*", hookEnd: LN("S1", 1) + .4,
  endAt: function () { return LN("S7", 2); }, endQ: "WHAT'S YOUR *20 MINUTES?*",
  titles: [["WHY DO WE STOP DOING THINGS WE KNOW ARE *GOOD* FOR US?", LN("S2", 0), SCN.S2[1], 470, 8],
           ["REASON #8", LN("S2", 1), SCN.S2[1], 860, 14],
           ["THE COST IS *NOW.* THE REWARD IS *LATER.*", LN("S2", 1) + .5, SCN.S2[1], 1060, 7],
           ["THE COST IS TODAY. THE REWARD *DOESN'T FEEL REAL.*", LN("S5", 1), SCN.S5[1], 300, 7]]
};
