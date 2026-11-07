// =================== KABIR VS. KABIR #4: "The ruined Tuesday" (Reason #4: one miss feels like the whole thing is ruined) ===================
function cells(fn) { var c = []; for (var i = 0; i < 35; i++) c.push(fn(i)); return c; }
var STREAK = cells(function (i) { return i < 12 ? "tick" : (i === 12 ? "now" : null); });
var RUIN = cells(function (i) { return i < 12 ? "tick" : (i === 12 ? "x" : (i < 30 ? "grey" : null)); });
var HABIT = cells(function (i) { return i >= 30 ? null : ([12, 19, 26].indexOf(i) >= 0 ? "x" : "tick"); });
var KX = 26, KY = 296;
function streakBox(x, y, lab, num, col) { rect(x - 1, y - 1, 46, 42, "#1A1530"); rect(x, y, 44, 40, col); ptext(L, lab, x + 22 - pwidth(lab, 1) / 2, y + 4, 1, "#FFFFFF"); ptext(L, num, x + 22 - pwidth(num, 3) / 2, y + 15, 3, "#FFFFFF"); }

// S1: twelve ticks in a row, a streak badge, Kabir proud
function sStreak(u, a, b) {
  img("room_night", 0, 0); monthGrid(14, 104, STREAK);
  streakBox(117, 104, "STREAK", "12", "#FF7A59");
  chr(blinkAt(u, .4) ? "blink" : "stand", 120, 327);
  return camAt([[0, 88, 150, 1.9], [LN("S1", 1), 88, 150, 1.9], [b, 110, 240, 1.4, b - LN("S1", 1)]], u);
}
function sWhy(u, a, b) { return whyScene(u, a, b); }
// S3: the cousin's birthday; the streak resets to zero
function sParty(u, a, b) {
  floorRoom("#4A2A66", "#432560"); for (var i = 0; i < 18; i++) { var bx = i * 16; rect(bx, 150 + (i % 2) * 2, 16, 1, "#FFC145"); for (var j = 0; j < 6; j++) rect(bx + 4 + j / 2, 152 + j, 8 - j, 1, BCK[i % BCK.length]); }
  rect(130, 340, 100, 6, "#8A5228"); rect(136, 346, 4, 34, "#6B4430"); rect(220, 346, 4, 34, "#6B4430");
  rect(150, 314, 60, 26, "#FFF4E0"); rect(150, 314, 60, 4, "#FF9FC2"); rect(158, 298, 44, 16, "#FFF4E0"); rect(158, 298, 44, 3, "#FF9FC2");
  for (var c = 0; c < 4; c++) { rect(166 + c * 9, 290, 2, 8, "#4C9AFF"); if (Math.floor(u * 8 + c) % 2) rect(166 + c * 9, 286, 2, 3, "#FFC145"); else rect(166 + c * 9, 287, 2, 2, "#FF7A59"); }
  chr(Math.floor(u * 3) % 2 ? "jump" : "stand", 70, 327);
  var z = u > LN("S3", 1) + .4, sh = z ? Math.round(Math.sin(u * 60) * 2 * (1 - seg(u, LN("S3", 1) + .4, LN("S3", 1) + .9))) : 0;
  signCard(135 + sh, 196, ["STREAK", z ? "0" : "12"], z ? "#E0453A" : "#FF7A59", "#FFFFFF", 2);
  return camAt([[a, 135, 280, 1.35], [b, 135, 285, 1.45, b - a]], u);
}
var BCK = ["#FF7A59", "#FFC145", "#6CC7A3", "#4C9AFF", "#B07CFF"];
// S4: "It's ruined now." Seventeen grey days and a pizza box
function sRuined(u, a, b) {
  floorRoom("#3B3A6A", "#34335E"); sofaAt(20); chr(blinkAt(u, .3) ? "sit_bed_blink" : "sit_bed", 44, 300);
  rect(120, 372, 26, 8, "#2A1F2E"); rect(121, 372, 24, 6, "#F2C94C"); rect(121, 372, 24, 1, "#C99A2E");
  var g = seg(u, LN("S4", 1), LE("S4", 1)); monthGrid(134, 196, RUIN.map(function (s, i) { return s === "grey" && (i - 13) / 17 > g ? null : s; }));
  if (u > a + .2 && u < LN("S4", 1) + .3) { bubble(56, 252, 96, 16, 70); ptext(L, "IT'S RUINED NOW.", 60, 257, 1, "#1A1530"); }
  return camAt([[a, 135, 290, 1.3], [b, 140, 285, 1.35, b - a]], u);
}
// S5: the mechanism: a miss is a dip; deciding it's broken is the cliff
function sChart(u, a, b) {
  rect(0, 0, W, H, "#1A1530"); stars(u, 30);
  var A = [.2, .32, .44, .56, .38, .6, .72, .86], B = [.2, .32, .44, .56, .38, .06, .02, .02];
  var g = lineChart(25, 150, 220, 160, [{ pts: A, col: "#28A86A", k: seg(u, a + .2, LE("S5", 0)) }, { pts: B, col: "#E0453A", k: seg(u, LN("S5", 1), LE("S5", 1) + .3) }], "ONE MISSED DAY");
  if (u > a + 1) ptext(L, "MISS", g.gx + g.gw * 4 / 7 - 8, g.gy - 4 - .38 * (g.gh - 4) + 8, 1, "#3A3560");
  if (u > LN("S5", 1) + .6) { ptext(L, "\"IT'S RUINED\"", g.gx + g.gw * 5 / 7 - 20, g.gy - 22, 1, "#E0453A"); }
  if (u > LE("S5", 0) - .2) ptext(L, "KEPT GOING", g.gx + g.gw - 64, g.gy - .86 * (g.gh - 4) - 12, 1, "#28A86A");
  return camAt([[a, 135, 230, 1.15], [b, 135, 230, 1.2, b - a]], u);
}
// S6: the rule card and day fourteen
function sRule(u, a, b) {
  rect(0, 0, W, H, "#2A2245"); stars(u, 20, "#5A5590");
  signCard(135, 110, ["NEVER", "MISS TWICE"], "#FFC145", "#1A1530", 3, seg(u, LN("S6", 1), LN("S6", 1) + .35));
  var day14 = u > LN("S6", 2); monthGrid(86, 236, cells(function (i) { return i < 12 ? "tick" : (i === 12 ? "x" : (i === 13 ? (day14 ? "now" : null) : null)); }));
  if (day14) { var p = .5 + .5 * Math.sin(u * 8); ddisc(177, 254, 14, "#FFE066", .3 + .2 * p); ptext(L, "DAY 14", 135 - pwidth("DAY 14", 2) / 2, 306, 2, "#FFE066"); }
  return camAt([[a, 135, 220, 1.2], [b, 135, 230, 1.3, b - a]], u);
}
// S7: gaps, and a habit (loops to frame 0)
function sEnd(u, a, b) {
  img("room_night", 0, 0); monthGrid(14, 104, HABIT, 5, eio(seg(u, a, a + 1.6)));
  streakBox(117, 104, "DAYS", "" + Math.round(27 * eio(seg(u, a, a + 1.6))), "#28A86A");
  chr(Math.floor(u * 2) % 2 ? "stretch" : "stand", 120, 327);
  return camAt([[a, 110, 240, 1.4], [LN("S7", 1), 88, 150, 1.9, 1.2]], u);
}

var SCENES = [["S1", sStreak], ["S2", sWhy], ["S3", sParty], ["S4", sRuined], ["S5", sChart], ["S6", sRule], ["S7", sEnd]];
var EP = {
  badge: "KABIR VS. KABIR #4", hook: "12 DAY *STREAK.*", hookEnd: LN("S1", 1) + .2,
  endAt: function () { return LN("S7", 2); }, endQ: "WHAT DID YOU QUIT AFTER *ONE BAD DAY?*",
  titles: [["WHY DO WE STOP DOING THINGS WE KNOW ARE *GOOD* FOR US?", LN("S2", 0), SCN.S2[1], 470, 8],
           ["REASON #4", LN("S2", 1), SCN.S2[1], 860, 14],
           ["ONE MISS FEELS LIKE *RUIN.*", LN("S2", 1) + .5, SCN.S2[1], 1060, 7],
           ["A MISS DOESN'T BREAK A HABIT. *DECIDING* IT'S BROKEN DOES.", LN("S5", 1), SCN.S5[1], 300, 7]]
};
