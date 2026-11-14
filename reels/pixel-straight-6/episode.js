// =================== STRAIGHT ANSWER #6: daily weigh-ins (water noise vs the weekly average) ===================
var DAILY = [.55, .62, .48, .6, .44, .52, .38, .5, .4, .47, .33, .42, .3, .38], AVG = [.56, .54, .52, .5, .48, .46, .44, .42, .4, .38, .37, .35, .34, .33];
function bath(u) { rect(0, 0, W, H, "#5A6B8C"); for (var y = 0; y < 380; y += 14) for (var x = (y / 14) % 2 ? 7 : 0; x < W; x += 14) rect(x, y, 13, 13, "#647698"); rect(0, 380, W, H - 380, "#3A4560"); }
function scale(x, y, txt, col) { rect(x - 2, y - 2, 134, 38, "#1A1530"); rect(x, y, 130, 34, "#E9E4D0"); rect(x + 6, y + 5, 118, 22, "#1A1530"); var b = pwidth(txt, 2) <= 112 ? 2 : 1; ptext(L, txt, x + 65 - pwidth(txt, b) / 2, y + 16 - 4 * b, b, col); }
function checks(x, y) { ["HEALTHY FOOD", "LONG WALK", "WATER"].forEach(function (s, i) { ptext(L, s, x + 12, y + i * 14, 1, "#FFFFFF"); L.save(); L.translate(x, y + i * 14 + 1); tick(0, 0, "#28A86A"); L.restore(); }); }
function weighChart(u, kDaily, kAvg, band) {
  var g = lineChart(20, 150, 230, 130, [{ pts: DAILY, col: "#E0453A", k: kDaily }].concat(kAvg > 0 ? [{ pts: AVG, col: "#28A86A", k: kAvg }] : []), "MORNING WEIGHT, 14 DAYS");
  if (band) { L.fillStyle = "rgba(76,154,255,.18)"; L.fillRect(g.gx, g.gy - .66 * (g.gh - 4), g.gw, .4 * (g.gh - 4)); ptext(L, "WATER, SALT, FOOD", g.gx + 6, g.gy - .7 * (g.gh - 4) - 8, 1, "#4C9AFF"); }
  return g;
}
// S1: perfect day, +1.2 kg (frame 0)
function sHook(u, a, b) { bath(u); scale(104, 342, "UP 1.2 KG", "#E0453A"); checks(44, 206); chr(blinkAt(u, .3) ? "sad_blink" : "sad", 44, 327); return camAt([[0, 135, 280, 1.3], [b, 135, 282, 1.35, b]], u); }
// S2: that's not fat: daily weight swings 1-2 kg
function sNoise(u, a, b) { bath(u); weighChart(u, seg(u, a + .2, LE("S2", 1)), 0, u > LN("S2", 1) + 2); return camAt([[a, 135, 230, 1.15], [b, 135, 232, 1.2, b - a]], u); }
// S3: 1 kg of fat is about 7,500 calories
function sMath(u, a, b) {
  bath(u); L.fillStyle = "rgba(20,15,46,.5)"; L.fillRect(0, 0, W, H); var k = eio(seg(u, a + .3, a + 1.6));
  rect(50, 330 - 180 * k, 60, 180 * k, "#E0453A"); ptext(L, "1 KG FAT", 80 - pwidth("1 KG FAT", 1) / 2, 338, 1, "#FFFFFF"); ptext(L, "7,500 CAL", 80 - pwidth("7,500 CAL", 1) / 2, 320 - 180 * k, 1, "#FFFFFF");
  if (u > LN("S3", 0) + 2.6) { var k2 = eio(seg(u, LN("S3", 0) + 2.6, LN("S3", 0) + 3.4)); rect(160, 330 - 180 * .27 * k2, 60, 180 * .27 * k2, "#28A86A"); ptext(L, "YOUR DAY", 190 - pwidth("YOUR DAY", 1) / 2, 338, 1, "#FFFFFF"); ptext(L, "2,000 CAL", 190 - pwidth("2,000 CAL", 1) / 2, 320 - 180 * .27 * k2, 1, "#FFFFFF"); }
  return camAt([[a, 135, 240, 1.15], [b, 135, 240, 1.2, b - a]], u);
}
// S4: trust the weekly average, the line under the noise
function sAvg(u, a, b) { bath(u); var g = weighChart(u, 1, seg(u, LN("S4", 1), LE("S4", 2)), false); if (u > LN("S4", 2)) ptext(L, "WEEKLY AVERAGE", g.gx + g.gw - 90, g.gy - 24, 1, "#28A86A"); return camAt([[a, 135, 230, 1.15], [b, 135, 232, 1.2, b - a]], u); }
// S5: back to the scale, reading the average (loop)
function sEnd(u, a, b) { bath(u); scale(104, 342, "AVG -0.4 KG/WK", "#28A86A"); checks(44, 206); chr("stand", 44, 327); return camAt([[a, 135, 282, 1.35], [b, 135, 280, 1.3, b - a]], u); }

var SCENES = [["S1", sHook], ["S2", sNoise], ["S3", sMath], ["S4", sAvg], ["S5", sEnd]];
var EP = {
  badge: "STRAIGHT ANSWER #6", badgeBg: STRAIGHT.badgeBg, badgeFg: STRAIGHT.badgeFg, hook: "PERFECT DAY. *UP 1.2 KG.*", hookEnd: LN("S1", 1) + .5,
  endAt: function () { return LN("S5", 1); }, endQ: "DO YOU WEIGH YOURSELF *EVERY DAY?*",
  titles: [["THAT'S NOT *FAT.*", LN("S2", 0), SCN.S2[1], 300, 9],
           ["TRUST THE *WEEKLY AVERAGE.*", LN("S4", 1), SCN.S4[1], 300, 9],
           ["SEND TO THE FRIEND WHO QUIT OVER *ONE MORNING.*", LN("S5", 0), LN("S5", 1), 300, 7]]
};
