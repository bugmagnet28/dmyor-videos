// =================== KABIR VS. KABIR #6: "New Year Kabir" (Reason #9: too many changes at once) ===================
function circ(cx, cy, r, c) { for (var y = -r; y <= r; y++) { var w = Math.round(Math.sqrt(r * r - y * y)); rect(cx - w, cy + y, w * 2 + 1, 1, c); } }
var HB = [["5AM", "#FFC145"], ["GYM", "#E0453A"], ["ICE", "#7FD4FF"], ["READ", "#4C9AFF"], ["ZEN", "#B07CFF"], ["SUGAR", "#FF9FC2"], ["ES", "#6CC7A3"]];
function ball(x, y, i, r) { r = r || 9; circ(x, y, r + 1, "#1A1530"); circ(x, y, r, HB[i][1]); rect(x - r / 2, y - r / 2, 3, 2, "rgba(255,255,255,.6)"); var s = HB[i][0]; if (r >= 9) ptext(L, s.length > 3 ? s.slice(0, 3) : s, x - pwidth(s.length > 3 ? s.slice(0, 3) : s, 1) / 2, y - 3, 1, "#1A1530"); }
var NEWME = ["5 AM WAKE UP", "GYM DAILY", "COLD SHOWER", "50 PAGES", "MEDITATE", "NO SUGAR", "SPANISH"];
function listBoard(x, y, k) { rect(x - 2, y - 2, 104, 128, "#1A1530"); rect(x, y, 100, 124, "#FFF4E0"); rect(x, y, 100, 14, "#E0453A"); ptext(L, "NEW ME", x + 50 - pwidth("NEW ME", 1) / 2, y + 4, 1, "#FFFFFF");
  NEWME.forEach(function (s, i) { if (k * 7 > i) { rect(x + 6, y + 21 + i * 14, 5, 5, "#3A3560"); ptext(L, s, x + 15, y + 20 + i * 14, 1, "#3A3560"); } }); }
// S1: Jan 1: the list of everything (frame 0)
function sList(u, a, b) {
  floorRoom("#3B3A6A", "#34335E"); listBoard(140, 160, 1); dayTag("JAN 1", 150, 292, "#FFFFFF", "#E0453A");
  for (var i = 0; i < 12; i++) { var t = (u * .5 + hash(i)) % 1; rect(hash(i + 3) * W, t * 380, 2, 2, ["#FFC145", "#FF9FC2", "#7FD4FF"][i % 3]); }
  chr(Math.floor(u * 2.5) % 2 ? "jump" : "stand", 60, 327);
  return camAt([[0, 180, 228, 1.7], [LN("S1", 1), 180, 228, 1.7], [b, 140, 270, 1.25, b - LN("S1", 1)]], u);
}
function sWhy(u, a, b) { return whyScene(u, a, b); }
// S3: juggling seven balls; day three one drops, day four all of them
function sJuggle(u, a, b) {
  floorRoom("#3B3A6A", "#34335E"); var n = Math.min(7, Math.floor(seg(u, a + .1, LE("S3", 0)) * 7.999)), d3 = LN("S3", 1) + .3, d4 = LN("S3", 2) + .3;
  var all = u > d4; chr(all ? (u > d4 + 1 ? "sad" : "shock") : (blinkAt(u, .2) ? "blink" : "stand"), 111, 327);
  for (var i = 0; i < n; i++) { var drop = (i === 2 && u > d3) || all, t0 = i === 2 && u > d3 ? d3 : d4;
    if (!drop) { var ph = u * 2.2 + i / 7, ang = ph * Math.PI * 2; ball(135 + Math.cos(ang) * 44, 286 + Math.sin(ang) * 22 - 16 * Math.abs(Math.sin(ang)), i); }
    else { var tt = u - t0, x0 = 135 + Math.cos((t0 * 2.2 + i / 7) * Math.PI * 2) * 40, fy = Math.min(372, 286 + 160 * tt * tt * 3), bx = x0 + (i - 3) * 14 * Math.min(1, tt * 2); ball(bx, fy, i); } }
  var dl = u < LN("S3", 1) ? "DAY 1" : (u < LN("S3", 2) ? "DAY 3" : "DAY 4"); dayTag(dl, 44, 150, u < LN("S3", 1) ? "#FFC145" : "#E0453A", u < LN("S3", 1) ? "#1A1530" : "#FFFFFF");
  return camAt([[a, 135, 260, 1.3], [b, 135, 265, 1.35, b - a]], u);
}
// S4: the effort tank: seven starts drain it by lunch
function sTank(u, a, b) {
  rect(0, 0, W, H, "#1A1530"); stars(u, 25, "#5A5590");
  rect(60, 130, 60, 200, "#C8C0E8"); rect(63, 133, 54, 194, "#2A2245"); ptext(L, "EFFORT", 90 - pwidth("EFFORT", 1) / 2, 118, 1, "#FFFFFF");
  var k = seg(u, a + .2, LE("S4", 1)), lvl = Math.max(0, 1 - k * 1.05), h = 190 * lvl; rect(65, 325 - h, 50, h, lvl > .35 ? "#6CC7A3" : (lvl > .1 ? "#FFC145" : "#E0453A"));
  for (var i = 0; i < 7; i++) { var on = k * 7 > i; ball(170 + (i % 2) * 34, 146 + i * 26, i, 8); if (on) { rect(126, 150 + i * 26, 30, 1, "#E0453A"); rect(126, 149 + i * 26, 3, 3, "#E0453A"); } }
  var clk = ["7:00", "8:00", "9:00", "10:00", "11:00", "12:00", "LUNCH"], c = clk[Math.min(6, Math.floor(k * 6.99))]; rect(48, 344, 84, 22, "#2A1F2E"); ptext(L, c, 90 - pwidth(c, 2) / 2, 349, 2, c === "LUNCH" ? "#E0453A" : "#FFFFFF");
  return camAt([[a, 135, 240, 1.15], [b, 135, 245, 1.2, b - a]], u);
}
// S5: one ball, until it runs on autopilot
function sOne(u, a, b) {
  floorRoom("#3B3A6A", "#34335E"); chr(blinkAt(u, .3) ? "blink" : "stand", 111, 327);
  var ph = u * 1.6, auto = u > LN("S5", 1) + 1.2; ball(135, 270 - 34 * Math.abs(Math.sin(ph * Math.PI)), 1, 11);
  if (auto) { signCard(135, 190, ["AUTOPILOT"], "#28A86A", "#FFFFFF", 2, seg(u, LN("S5", 1) + 1.2, LN("S5", 1) + 1.5)); }
  for (var i = 0; i < 6; i++) if (i !== 1) ball(26 + i * 10 + (i > 1 ? 120 : 0), 372, i === 0 ? 0 : i, 5);
  return camAt([[a, 135, 280, 1.5], [b, 135, 270, 1.6, b - a]], u);
}
// S6: one at a time across the year (loops to the board)
var MON = ["JAN", "MAR", "MAY", "JUL", "SEP", "DEC"];
function sYear(u, a, b) {
  rect(0, 0, W, H, "#2A2245"); stars(u, 20, "#5A5590");
  var k = seg(u, a + .2, LE("S6", 0) + .4);
  MON.forEach(function (m, i) { var y = 120 + i * 36, on = k * 6 > i; rect(40, y, 190, 28, "#1A1530"); rect(41, y + 1, 188, 26, on ? "#3A3560" : "#262040"); ptext(L, m, 50, y + 10, 1, "#FFFFFF");
    for (var j = 0; j <= Math.min(i, 4); j++) if (on) ball(100 + j * 26, y + 14, [1, 3, 0, 4, 6][j], 9); });
  if (u > LN("S6", 1)) ptext(L, "5 NEW HABITS. FOR REAL.", 135 - pwidth("5 NEW HABITS. FOR REAL.", 1) / 2, 350, 1, "#B8F5C8");
  return camAt([[a, 135, 240, 1.15], [b, 135, 240, 1.2, b - a]], u);
}

var SCENES = [["S1", sList], ["S2", sWhy], ["S3", sJuggle], ["S4", sTank], ["S5", sOne], ["S6", sYear]];
var EP = {
  badge: "KABIR VS. KABIR #6", hook: "JANUARY 1. *NEW ME.*", hookEnd: LN("S1", 1) + .4,
  endAt: function () { return LN("S6", 2); }, endQ: "IF YOU COULD KEEP ONLY *ONE?*",
  titles: [["WHY DO WE STOP DOING THINGS WE KNOW ARE *GOOD* FOR US?", LN("S2", 0), SCN.S2[1], 470, 8],
           ["REASON #9", LN("S2", 1), SCN.S2[1], 860, 14],
           ["TOO MANY CHANGES *AT ONCE.*", LN("S2", 1) + .5, SCN.S2[1], 1060, 7],
           ["EVERY NEW HABIT COSTS *EFFORT* TO START.", LN("S4", 0), SCN.S4[1], 300, 7],
           ["*ONE* AT A TIME.", LN("S5", 0), SCN.S5[1], 300, 9]]
};
