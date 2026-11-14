// =================== HABIT ROAST #3: cramming the night before (spacing + self-testing) ===================
var CRAM = [1, .52, .32, .22, .16, .12], SPACED = [.45, .38, .62, .55, .76, .7, .86, .82, .92];
function room(u) { img("room_night", 0, 0); }
function curve(u, pts, k, col, t) { var g = lineChart(24, 168, 222, 118, [{ pts: pts, col: col, k: k }], "WHAT YOU REMEMBER"); ptext(L, t[0], g.gx, g.gy + 3, 1, "#9A92C0"); ptext(L, t[1], g.gx + g.gw - pwidth(t[1], 1), g.gy + 3, 1, "#9A92C0"); return g; }
function clockChip(x, y, s) { rect(x - 1, y - 1, 52, 18, "#1A1530"); rect(x, y, 50, 16, "#2A2245"); ptext(L, s, x + 25 - pwidth(s, 1) / 2, y + 5, 1, "#FF7A59"); }
// S1: six hours the night before, curve crashes by Friday (frame 0)
function sHook(u, a, b) {
  room(u); curve(u, CRAM, 1, "#E0453A", ["THU NIGHT", "FRI"]); chr(Math.floor(u * 5) % 2 ? "sit_write1" : "sit_write0", 120, 302); clockChip(200, 296, "2:00 AM");
  rect(170, 328, 8, 10, "#FFF4E0"); rect(171, 330, 6, 7, "#6B4430");
  return camAt([[0, 135, 255, 1.12], [b, 135, 258, 1.15, b]], u);
}
// S2: seen once fades; fetched again stays
function card(x, y, title, sub, col, alpha) { L.globalAlpha = alpha; rect(x - 1, y - 1, 102, 72, "#1A1530"); rect(x, y, 100, 70, "#FFF4E0"); rect(x, y, 100, 14, col); ptext(L, title, x + 50 - pwidth(title, 1) / 2, y + 4, 1, "#FFFFFF"); ptext(L, sub, x + 50 - pwidth(sub, 1) / 2, y + 40, 1, "#3A3560"); L.globalAlpha = 1; }
function sTwist(u, a, b) {
  room(u); L.fillStyle = "rgba(20,15,46,.55)"; L.fillRect(0, 0, W, H);
  var f = seg(u, LN("S2", 0) + .8, LE("S2", 0)); card(26, 170, "SEEN ONCE", "FADES", "#8A8498", 1 - .75 * f);
  if (u > LN("S2", 1)) { var k = eout(seg(u, LN("S2", 1), LN("S2", 1) + .4)); card(144, 170, "FETCHED AGAIN", "STAYS", "#28A86A", k); for (var i = 0; i < 3; i++) { var t = (u * .8 + i / 3) % 1; rect(194 - 20 + i * 20, 250 - t * 20, 2, 6, "#B8F5C8"); } }
  return camAt([[a, 135, 230, 1.2], [b, 135, 230, 1.25, b - a]], u);
}
// S3: same six hours, one a day, quiz each time; the curve climbs and stays
function sFix(u, a, b) {
  room(u); L.fillStyle = "rgba(20,15,46,.4)"; L.fillRect(0, 0, W, H);
  var days = ["MON", "TUE", "WED", "THU", "FRI", "SAT"], n = Math.floor(seg(u, a + .2, LE("S3", 0)) * 6.99);
  days.forEach(function (d, i) { if (i >= n) return; var x = 22 + i * 38; rect(x, 292, 34, 30, "#1A1530"); rect(x + 1, 293, 32, 28, "#3A3560"); ptext(L, d, x + 17 - pwidth(d, 1) / 2, 296, 1, "#FFFFFF"); ptext(L, "1H", x + 12, 306, 1, "#FFE066"); L.save(); L.translate(x + 12, 314); tick(0, 0, "#28A86A"); L.restore(); });
  if (u > LN("S3", 1) - .3) curve(u, SPACED, seg(u, LN("S3", 1) - .3, LE("S3", 1)), "#28A86A", ["MON", "EXAM"]);
  return camAt([[a, 135, 255, 1.12], [b, 135, 258, 1.15, b - a]], u);
}
function sEnd(u, a, b) { room(u); curve(u, SPACED, 1, "#28A86A", ["MON", "EXAM"]); chr(blinkAt(u, .3) ? "sit_read_blink" : "sit_read_happy", 26, 296); clockChip(200, 296, "9:00 PM"); return camAt([[a, 135, 258, 1.15], [b, 135, 255, 1.12, b - a]], u); }

var SCENES = [["S1", sHook], ["S2", sTwist], ["S3", sFix], ["S4", sEnd]];
var EP = {
  badge: "HABIT ROAST #3", badgeBg: ROAST.badgeBg, badgeFg: ROAST.badgeFg, hook: "CRAMMED 6 HOURS. *GONE BY FRIDAY.*", hookEnd: LN("S1", 1) + .5,
  endAt: function () { return LN("S4", 0); }, endQ: "WHEN'S YOUR NEXT *EXAM?*",
  titles: [["YOUR BRAIN KEEPS WHAT IT HAS TO *FETCH.*", LN("S2", 1), SCN.S2[1], 300, 8],
           ["SEND TO TONIGHT'S *CRAMMER.*", LN("S3", 2), SCN.S3[1], 300, 9]]
};
