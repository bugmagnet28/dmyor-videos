// =================== STRAIGHT ANSWER #5: practise slow to get fast ===================
function desk(u) { rect(0, 0, W, H, "#1E1A33"); rect(0, 330, W, 150, "#3A2A22"); rect(0, 330, W, 4, "#5A3826"); }
function keyboard(x, y, bad, t) { rect(x - 2, y - 2, 164, 52, "#1A1530"); rect(x, y, 160, 48, "#3A3560");
  for (var r = 0; r < 3; r++) for (var c = 0; c < 10; c++) { var i = r * 10 + c, kx = x + 4 + c * 15 + r * 4, ky = y + 4 + r * 14, hot = bad && hash(i + Math.floor(t * 6)) > .82; rect(kx, ky, 12, 11, hot ? "#E0453A" : "#C8C0E8"); rect(kx, ky + 9, 12, 2, hot ? "#8E3644" : "#8A8498"); } }
function metro(x, y, bpm, t) { rect(x - 12, y, 24, 40, "#1A1530"); rect(x - 10, y + 2, 20, 36, "#8A5228"); var a = Math.sin(t * Math.PI * bpm / 60) * .5; L.save(); L.translate(x, y + 34); L.rotate(a); rect(-1, -30, 2, 30, "#FFF4E0"); rect(-3, -22, 6, 4, "#FFC145"); L.restore(); ptext(L, bpm + " BPM", x - pwidth(bpm + " BPM", 1) / 2, y + 44, 1, "#FFE066"); }
// S1: fast and sloppy (frame 0)
function sHook(u, a, b) { desk(u); keyboard(55, 250, true, u); metro(215, 180, 160, u); counter(30, 180, "MISTAKES PER RUN", "6", "#E0453A", 3); return camAt([[0, 135, 250, 1.15], [b, 135, 252, 1.18, b]], u); }
// S2: every rep teaches your hands; sloppy reps teach sloppy
function sReps(u, a, b) {
  desk(u); var n = Math.min(12, Math.floor(seg(u, a + .2, LE("S2", 0)) * 12.99));
  for (var i = 0; i < n; i++) { var x = 24 + (i % 6) * 38, y = 150 + Math.floor(i / 6) * 40, bad = u > LN("S2", 1); rect(x, y, 34, 34, "#1A1530"); rect(x + 1, y + 1, 32, 32, bad ? "#5A2A2E" : "#3A3560"); ptext(L, "REP", x + 8, y + 4, 1, "#FFFFFF"); if (bad) redX(x + 12, y + 16, 9); else { L.save(); L.translate(x + 12, y + 20); tick(0, 0, "#9A92C0"); L.restore(); } }
  if (u > LN("S2", 1) + 1) signCard(135, 250, ["HANDS LEARN:", "SLOPPY"], "#E0453A", "#FFFFFF", 2, seg(u, LN("S2", 1) + 1, LN("S2", 1) + 1.3));
  return camAt([[a, 135, 240, 1.15], [b, 135, 242, 1.2, b - a]], u);
}
// S3: slow until clean; then speed up a notch while it stays clean
var LADDER = [60, 70, 80, 95, 110, 130, 160];
function sLadder(u, a, b) {
  desk(u); var t = LN("S3", 1), n = u < t ? 1 : Math.min(7, 1 + Math.floor(seg(u, LN("S3", 2), LE("S3", 2)) * 6.99)), cur = LADDER[n - 1];
  LADDER.forEach(function (v, i) { var x = 20 + i * 33, h = 20 + i * 14, y = 300 - h; rect(x, y, 30, h, "#1A1530"); rect(x + 1, y + 1, 28, h - 1, i < n ? "#28A86A" : "#3A3560"); ptext(L, "" + v, x + 15 - pwidth("" + v, 1) / 2, y + 4, 1, "#FFFFFF"); });
  if (u > t) { var c = Math.min(10, Math.floor(seg(u, t, LE("S3", 1)) * 10.99)); counter(30, 158, "CLEAN REPS", c + "/10", "#B8F5C8", 2); }
  metro(215, 150, cur, u);
  return camAt([[a, 135, 240, 1.12], [b, 135, 242, 1.15, b - a]], u);
}
// S4: clean slow becomes clean fast; same rule everywhere (loops to the keyboard)
function sEnd(u, a, b) { desk(u); keyboard(55, 250, false, u); metro(215, 180, 160, u); counter(30, 180, "MISTAKES PER RUN", "0", "#28A86A", 3);
  if (u > LN("S4", 1)) { ["TYPING", "GUITAR", "SERVE"].forEach(function (s, i) { var x = 30 + i * 74; rect(x, 296, 66, 16, "#1A1530"); rect(x + 1, 297, 64, 14, "#2E5A3E"); ptext(L, s, x + 33 - pwidth(s, 1) / 2, 301, 1, "#FFFFFF"); }); }
  return camAt([[a, 135, 252, 1.18], [b, 135, 250, 1.15, b - a]], u); }

var SCENES = [["S1", sHook], ["S2", sReps], ["S3", sLadder], ["S4", sEnd]];
var EP = {
  badge: "STRAIGHT ANSWER #5", badgeBg: STRAIGHT.badgeBg, badgeFg: STRAIGHT.badgeFg, hook: "PRACTISING FAST? *YOU'RE PRACTISING MISTAKES.*", hookEnd: LN("S1", 1) + .5,
  endAt: function () { return LN("S4", 2); }, endQ: "WHAT ARE YOU *RUSHING* RIGHT NOW?",
  titles: [["SLOW UNTIL IT'S *CLEAN.*", LN("S3", 1), SCN.S3[1], 300, 9]]
};
