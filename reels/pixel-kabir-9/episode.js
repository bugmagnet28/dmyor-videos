// =================== KABIR VS. KABIR #9: no rest days (muscle rebuilds while you rest) ===================
var DN7 = ["M", "T", "W", "T", "F", "S", "S"];
function gym(u) { rect(0, 0, W, H, "#2A2245"); for (var i = 0; i < 14; i++) rect(i * 20, 0, 1, 380, "#262040"); rect(0, 380, W, H - 380, "#3A3560"); rect(0, 380, W, 2, "#4A4470"); rect(200, 250, 50, 130, "#1A1530"); for (var r = 0; r < 4; r++) { rect(204, 262 + r * 28, 42, 4, "#8A8498"); } }
function barbell(x, y, up) { var yy = up ? y : y + 18; rect(x - 6, yy, 60, 3, "#C8C0E8"); rect(x - 12, yy - 8, 6, 19, "#1A1530"); rect(x + 54, yy - 8, 6, 19, "#1A1530"); }
function lifter(u, x, k) { var up = Math.floor(u * (k || 2)) % 2; chr(up ? "lookup" : "stand", x, 327); barbell(x - 4, 322, up); }
function week(u, x, y, cells, n) { for (var i = 0; i < n; i++) { var c = cells[i], cx = x + i * 30; rect(cx, y, 28, 30, "#1A1530"); rect(cx + 1, y + 1, 26, 28, c === "R" ? "#2E5A3E" : "#3A3560"); ptext(L, DN7[i % 7], cx + 11, y + 4, 1, "#FFFFFF"); if (c === "R") ptext(L, "REST", cx + 3, y + 17, 1, "#B8F5C8"); else { L.save(); L.translate(cx + 9, y + 16); tick(0, 0, "#FFC145"); L.restore(); } } }
function liftBars(u, vals, n, col) { rect(20, 162, 230, 96, "#1A1530"); rect(22, 164, 226, 92, "#FFF4E0"); ptext(L, "WEIGHT LIFTED", 30, 169, 1, "#3A3560");
  for (var i = 0; i < n; i++) { var h = (vals[i] - 40) * 2.6, x = 32 + i * 27; rect(x, 250 - h, 20, h, typeof col === "function" ? col(i) : col); ptext(L, vals[i] + "", x + 2, 240 - h, 1, "#3A3560"); } }
var DOWN = [60, 58, 54], UP = [54, 57, 60, 63, 66, 68, 70, 72];
// S1: seven gym days, zero rest (frame 0)
function sHook(u, a, b) { gym(u); week(u, 30, 170, "TTTTTTT", 7); lifter(u, 100, 3); return camAt([[0, 135, 255, 1.12], [b, 135, 258, 1.15, b]], u); }
// S2: week three, lifting less; he adds an eighth day
function sWorse(u, a, b) {
  gym(u); liftBars(u, DOWN, Math.min(3, 1 + Math.floor(seg(u, a + .2, LE("S2", 0)) * 2.99)), "#E0453A");
  if (u > LN("S2", 1) + 1.4) { week(u, 16, 262, "TTTTTTTT", 8); rect(16 + 7 * 30, 262, 28, 30, "#1A1530"); rect(17 + 7 * 30, 263, 26, 28, "#E0453A"); ptext(L, "8?!", 17 + 7 * 30 + 4, 272, 1, "#FFFFFF"); }
  chr(blinkAt(u, .1) ? "sad_blink" : "sad", 100, 327);
  return camAt([[a, 135, 255, 1.12], [b, 135, 258, 1.15, b - a]], u);
}
// S3: the twist: training breaks the muscle; rest rebuilds it stronger
function block(x, y, k, broken) { rect(x, y, 24, 18, "#B5523A"); if (broken) { rect(x + 6, y, 1, 18, "#1A1530"); rect(x + 15, y + 4, 1, 14, "#1A1530"); rect(x, y + 9, 24, 1, "#1A1530"); } else if (k > 0) { rect(x - 2, y - 2, 28, 22 * 0 + 2, "#FF9F80"); } }
function sTwist(u, a, b) {
  gym(u); L.fillStyle = "rgba(20,15,46,.55)"; L.fillRect(0, 0, W, H);
  var t1 = LN("S3", 1), mid = t1 + (LE("S3", 1) - t1) * .5;
  rect(24, 160, 104, 120, "#1A1530"); rect(26, 162, 100, 116, "#3A3560"); ptext(L, "WORKOUT", 76 - pwidth("WORKOUT", 1) / 2, 168, 1, "#FFFFFF");
  for (var r = 0; r < 3; r++) for (var c = 0; c < 3; c++) block(36 + c * 28, 184 + r * 26, 0, u > t1 + .3);
  if (u > mid) { rect(142, 160, 104, 120, "#1A1530"); rect(144, 162, 100, 116, "#2E5A3E"); ptext(L, "REST", 194 - pwidth("REST", 1) / 2, 168, 1, "#B8F5C8");
    var g = eout(seg(u, mid, mid + 1)); for (var r2 = 0; r2 < 3; r2++) for (var c2 = 0; c2 < 3; c2++) { var s = 24 + 4 * g; rect(156 + c2 * 28 - (s - 24) / 2, 184 + r2 * 26 - (s - 24) / 4, s, 18 + 2 * g, "#C8603F"); } ptext(L, "STRONGER", 194 - pwidth("STRONGER", 1) / 2, 266, 1, "#B8F5C8"); }
  if (u > LN("S3", 2)) { rect(26, 290, 220, 18, "#1A1530"); ptext(L, "NO REST: ONLY BREAKING", 135 - pwidth("NO REST: ONLY BREAKING", 1) / 2, 296, 1, "#FF9F94"); }
  return camAt([[a, 135, 240, 1.15], [b, 135, 240, 1.2, b - a]], u);
}
// S4: two rest days, on purpose
function sFix(u, a, b) { gym(u); week(u, 30, 170, "TTRTTRT".split(""), Math.min(7, Math.floor(seg(u, a + .2, a + 2) * 7.99))); sofaAt(30); chr(blinkAt(u, .3) ? "sit_bed_blink" : "sit_bed", 54, 300); if (u > LN("S4", 1)) ptext(L, "2 REST DAYS", 135 - pwidth("2 REST DAYS", 2) / 2, 216, 2, "#B8F5C8"); return camAt([[a, 135, 255, 1.12], [b, 135, 258, 1.15, b - a]], u); }
// S5: lifts more (loops to the gym frame)
function sEnd(u, a, b) { gym(u); liftBars(u, UP, Math.min(8, 1 + Math.floor(seg(u, a, a + 1.6) * 7.99)), "#28A86A"); lifter(u, 100, 2); return camAt([[a, 135, 255, 1.12], [b, 135, 255, 1.15, b - a]], u); }

var SCENES = [["S1", sHook], ["S2", sWorse], ["S3", sTwist], ["S4", sFix], ["S5", sEnd]];
var EP = {
  badge: "KABIR VS. KABIR #9", hook: "7 GYM DAYS A WEEK. *REST DAYS: 0.*", hookEnd: LN("S1", 1) + .5,
  endAt: function () { return LN("S5", 2); }, endQ: "HOW MANY *REST DAYS* DO YOU TAKE?",
  titles: [["IT GROWS WHILE YOU *REST.*", LN("S3", 1), SCN.S3[1], 300, 9],
           ["SEND TO THE FRIEND WHO *NEVER RESTS.*", LN("S5", 1), LN("S5", 2), 300, 8]]
};
