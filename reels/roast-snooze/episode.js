// =================== HABIT ROAST #5: snooze x6 (nine-minute naps are not rest) ===================
// sleep line: high = awake. Six alarms = six spikes; the fix = one alarm, up.
var SNZ = [.15, .9, .35, .2, .9, .35, .2, .9, .35, .2, .9, .35, .2, .9, .35, .2, .9, .35, .9], ONE = [.15, .15, .15, .15, .15, .9, .92, .93, .93];
function bedroom(u, dawn) { rect(0, 0, W, H, dawn ? "#3A3A6A" : "#1E1A3A"); for (var i = 0; i < 14; i++) rect(i * 20, 0, 1, 380, dawn ? "#36366A" : "#1B1734"); rect(0, 380, W, H - 380, dawn ? "#5A4A6A" : "#2E2848"); rect(0, 380, W, 2, "#4A4470"); }
function bed(x) { rect(x - 2, 352, 124, 30, "#1A1530"); rect(x, 354, 120, 18, "#6C5CB0"); rect(x, 370, 120, 8, "#4A3C86"); rect(x + 4, 344, 30, 12, "#F2EEE6"); rect(x - 2, 330, 6, 50, "#3A2A20"); }
function alarmAt(u, x, y, ring) { img(ring && Math.floor(u * 8) % 2 ? "alarm1" : "alarm0", x, y, false, 2); if (ring) { var s = Math.floor(u * 8) % 2; rect(x - 6 - s, y + 6, 2, 8, "#FFC145"); rect(x + 36 + s, y + 6, 2, 8, "#FFC145"); } }
function sleepChart(u, pts, k, col, title) { var g = lineChart(26, 158, 218, 112, [{ pts: pts, col: col, k: k }], title); ptext(L, "6:00", g.gx, g.gy + 3, 1, "#9A92C0"); ptext(L, "6:45", g.gx + g.gw - 22, g.gy + 3, 1, "#9A92C0"); ptext(L, "AWAKE", g.gx + 3, g.gy - g.gh + 2, 1, "#9A92C0"); return g; }
// S1 (frame 0): six alarm spikes, snooze counter 6
function sHook(u, a, b) {
  bedroom(u, false); sleepChart(u, SNZ, 1, "#E0453A", "YOUR LAST 45 MINUTES"); bed(14);
  chr(blinkAt(u, .3) ? "sit_bed_blink" : "sit_bed", 22, 318); alarmAt(u, 140, 330, Math.floor(u * 1.4) % 2 === 0);
  counter(180, 290, "SNOOZES", "6", "#FFC145", 3);
  if (u > LN("S1", 1) + 1.2) { rect(150, 268, 98, 14, "#1A1530"); ptext(L, "MORE TIRED", 160, 272, 1, "#E0453A"); }
  return camAt([[0, 135, 250, 1.12], [b, 135, 255, 1.16, b]], u);
}
// S2: the 45 minutes as six 9-minute naps, each cut off by an alarm
function sCut(u, a, b) {
  bedroom(u, false); var m = LN("S2", 1), n = Math.min(6, Math.floor(seg(u, m, m + 4.2) * 6.99));
  rect(18, 150, 234, 120, "#1A1530"); rect(20, 152, 230, 116, "#FFF4E0"); ptext(L, "6 NAPS. 9 MINUTES EACH.", 30, 160, 1, "#3A3560");
  for (var i = 0; i < 6; i++) { var x = 30 + i * 36, y = 186; rect(x, y, 30, 40, i < n ? "#CFC6B4" : "#6C5CB0"); ptext(L, "9", x + 12, y + 14, 1, "#FFFFFF");
    if (i < n) { redX(x + 8, y + 10, 14); ptext(L, "CUT", x + 6, y + 46, 1, "#E0453A"); } }
  if (u > m + 4.4) { rect(64, 238, 142, 22, "#E0453A"); ptext(L, "6 WAKE-UPS, 0 REST", 76, 245, 1, "#FFFFFF"); }
  bed(14); chr(Math.floor(u * 4) % 2 ? "shake0" : "shake1", 22, 318); alarmAt(u, 140, 330, n > 0 && (u - m) % .7 < .35);
  return camAt([[a, 135, 240, 1.04], [b, 135, 242, 1.08, b - a]], u);
}
// S3: one alarm across the room, walk to it, open the curtain: daylight
function sFix(u, a, b) {
  var c = seg(u, LN("S3", 1), LN("S3", 1) + 1.2); bedroom(u, c > .5);
  rect(150, 140, 100, 120, "#1A1530"); rect(152, 142, 96, 116, c > 0 ? "#FFE9A0" : "#2A2A55"); if (c > 0) ddisc(200, 200, 70 * c, "#FFF4C0", .5);
  var cw = 48 * (1 - eio(c)); rect(152, 142, cw, 116, "#B5523A"); rect(248 - cw, 142, cw, 116, "#B5523A");
  bed(14); rect(222, 352, 40, 28, "#6B4430"); alarmAt(u, 226, 320, u < LN("S3", 0) + 2.4);
  var wk = seg(u, LN("S3", 0) + .6, LN("S3", 0) + 2.4); chr(wk > 0 && wk < 1 ? "walk" + (Math.floor(u * 7) % 4) : (c > .5 ? "stretch" : "stand"), lerp(30, 170, eio(wk)), 327);
  rect(14, 270, 156, 20, "#1A1530"); ptext(L, "1 ALARM.", 20, 274, 1, "#6CC7A3"); ptext(L, "ACROSS THE ROOM.", 20, 282, 1, "#6CC7A3");
  return camAt([[a, 135, 250, 1.12], [b, 140, 250, 1.18, b - a]], u);
}
// S4: loop: frame-0 chart, now one clean wake-up
function sEnd(u, a, b) { bedroom(u, true); sleepChart(u, ONE, 1, "#28A86A", "YOUR LAST 45 MINUTES"); bed(14); chr("stretch", 22, 318); alarmAt(u, 140, 330, false); counter(180, 290, "SNOOZES", "0", "#FFFFFF", 3); return camAt([[a, 135, 255, 1.16], [b, 135, 250, 1.12, b - a]], u); }

var SCENES = [["S1", sHook], ["S2", sCut], ["S3", sFix], ["S4", sEnd]];
var EP = {
  badge: "HABIT ROAST #5", badgeBg: ROAST.badgeBg, badgeFg: ROAST.badgeFg, hook: "6 SNOOZES. *STILL TIRED.*", hookEnd: LN("S1", 1) + .5,
  endAt: function () { return LN("S4", 0); }, endQ: "HOW MANY SNOOZES ARE *YOU* ON?",
  titles: [["A SNOOZE IS A NAP THAT GETS *CUT OFF.*", LN("S2", 1), SCN.S2[1], 300, 8],
           ["SEND TO YOUR *6:09* FRIEND.", LN("S3", 2), SCN.S3[1], 300, 9]]
};
