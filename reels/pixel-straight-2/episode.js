// =================== STRAIGHT ANSWER #2: "You can't do a goal" (Reason #7: the goal has no "today" in it) ===================
function cloud(cx, cy, w, label, k) {
  if (k != null && k <= 0) return; var s = k == null ? 1 : eout(k); L.save(); L.translate(cx, cy); L.scale(s, s);
  rect(-w / 2, -8, w, 18, "#FFFFFF"); rect(-w / 2 + 6, -14, w * .4, 8, "#FFFFFF"); rect(-w / 2 + w * .45, -18, w * .35, 12, "#FFFFFF"); rect(-w / 2 - 4, -2, w + 8, 10, "#FFFFFF"); rect(-w / 2, 8, w, 3, "#D8E4F4");
  ptext(L, label, -pwidth(label, 1) / 2, -2, 1, "#3A3560"); L.restore();
}
function daySky(u) { var C = ["#6FA8E8", "#86B9EE", "#9DC9F2", "#B4D8F6"]; for (var i = 0; i < 4; i++) rect(0, i * 95, W, 95, C[i]); rect(0, 380, W, H - 380, "#5A8A4A"); rect(0, 380, W, 3, "#4E7A40"); }
var GOALS = [["GET FIT", 70, 185], ["LEARN TO CODE", 192, 218], ["FIX MY MONEY", 110, 258]];
function sClouds(u, a, b) {
  daySky(u); GOALS.forEach(function (g, i) { cloud(g[1] + 3 * Math.sin(u * .8 + i), g[2], pwidth(g[0], 1) + 14, g[0]); });
  chr(blinkAt(u, .3) ? "blink" : "lookup", 111, 327);
  if (u > LN("S1", 1)) GOALS.forEach(function (g, i) { var k = seg(u, LN("S1", 1) + i * .3, LN("S1", 1) + i * .3 + .2); if (k > 0) redX(g[1] - 4, g[2] + 14, 8); });
  return camAt([[0, 135, 250, 1.1], [b, 135, 255, 1.15, b]], u);
}
function sWhy(u, a, b) { return whyScene(u, a, b); }
// S3: the goal sits on a peak, in a cloud; "what do I do about it?" gets no answer
function sPeak(u, a, b) {
  daySky(u); L.fillStyle = "#7A8AB0"; for (var y = 120; y < 380; y++) { var hw = (y - 120) * .55; L.fillRect(Math.round(180 - hw), y, Math.round(hw * 2), 1); }
  L.fillStyle = "#FFFFFF"; for (var y2 = 120; y2 < 150; y2++) { var h2 = (y2 - 120) * .55; L.fillRect(Math.round(180 - h2), y2, Math.round(h2 * 2), 1); }
  cloud(180, 112, 70, "GET FIT");
  var q = LN("S3", 1), n = LN("S3", 2), sat = u > n + .4;
  chr(sat ? "crouch" : (blinkAt(u, .4) ? "blink" : "lookup"), 40, 327);
  if (u > q && u < n) { bubble(14, 270, 140, 16, 64); ptext(L, "WHAT DO I DO ABOUT IT?", 19, 275, 1, "#1A1530"); }
  if (u > n) { bubble(50, 276, 30, 16, 64); ptext(L, "...", 56, 281, 1, "#1A1530"); }
  return camAt([[a, 135, 240, 1.05], [q, 120, 260, 1.25, q - a], [b, 110, 270, 1.3, b - q]], u);
}
// S4: break it down until the step is physical
var LAD = ["GET FIT", "RUN A 5K", "RUN 3X A WEEK", "RUN MONDAY 7:00", "SHOES BY THE DOOR"];
function ladder(u, t0, t1, hi, f0) {
  LAD.forEach(function (s, i) { var ti = i === 0 && f0 != null ? f0 : t0 + (t1 - t0) * (i - (f0 != null ? 1 : 0)) / (f0 != null ? 4 : 5), k = seg(u, ti, ti + .3); if (k <= 0) return; var y = 110 + i * 46, w = pwidth(s, 1) + 16, last = i === 4;
    if (i > 0) { rect(134, y - 14, 2, 12, "#FFFFFF"); rect(131, y - 5, 8, 2, "#FFFFFF"); rect(132, y - 3, 6, 2, "#FFFFFF"); }
    L.save(); L.translate(135, y + 8); L.scale(eout(k), eout(k)); L.translate(-w / 2, -8);
    var col = last ? (hi ? "#28A86A" : "#3A3560") : (i === 0 ? "#FFFFFF" : "#3A3560"); rect(-1, -1, w + 2, 18, "#1A1530"); rect(0, 0, w, 16, col); ptext(L, s, 8, 5, 1, i === 0 ? "#3A3560" : "#FFFFFF"); L.restore();
    if (i === 0) { rect(135 - w / 2 - 6, y + 2, 3, 3, "#FFFFFF"); rect(135 + w / 2 + 4, y + 4, 3, 3, "#FFFFFF"); } });
}
function sLadder(u, a, b) {
  rect(0, 0, W, H, "#1A1530"); stars(u, 30, "#5A5590"); ladder(u, LN("S4", 1) + .3, LE("S4", 1) - .4, u > LE("S4", 1) - .4, a + .2);
  if (u > LE("S4", 1) - .2) { ptext(L, "PHYSICAL", 135 - pwidth("PHYSICAL", 2) / 2, 330, 2, "#B8F5C8"); }
  return camAt([[a, 135, 230, 1.15], [b, 135, 240, 1.2, b - a]], u);
}
// S5: the hands test
function door(x) { rect(x, 250, 52, 130, "#2A1F2E"); rect(x + 2, 252, 48, 128, "#8A5228"); rect(x + 6, 258, 40, 50, "#7A4620"); rect(x + 6, 316, 40, 58, "#7A4620"); rect(x + 42, 318, 4, 4, "#FFC145"); }
function shoes(x, y) { for (var i = 0; i < 2; i++) { var sx = x + i * 16; rect(sx, y, 14, 7, "#2A1F2E"); rect(sx + 1, y + 1, 12, 5, "#E0453A"); rect(sx + 1, y + 5, 12, 2, "#FFFFFF"); rect(sx + 3, y + 2, 4, 1, "#FFFFFF"); } }
function sHands(u, a, b) {
  floorRoom("#3B3A6A", "#34335E"); door(176); shoes(150, 372);
  signCard(98, 200, ["GET FIT"], "#FFFFFF", "#3A3560", 2); if (u > a + 1.2) redX(86, 200, 24);
  if (u > a + 1.9) { var k = eout(seg(u, a + 1.9, a + 2.2)); L.save(); L.translate(170, 350); L.scale(2.5 * k, 2.5 * k); tick(0, 0, "#28A86A"); L.restore(); }
  chr(blinkAt(u, .2) ? "blink" : "stand", 96, 327);
  return camAt([[a, 135, 280, 1.3], [b, 140, 285, 1.35, b - a]], u);
}
// S6: Dmyor close: the ladder, ticked at the bottom
function sClose(u, a, b) {
  rect(0, 0, W, H, "#1A1530"); stars(u, 30, "#5A5590"); ladder(u, a - 9, a - 8, true);
  if (u > a + .6) { L.save(); L.translate(208, 296); L.scale(2, 2); tick(0, 0, "#B8F5C8"); L.restore(); }
  return camAt([[a, 135, 240, 1.2], [b, 135, 250, 1.3, b - a]], u);
}

var SCENES = [["S1", sClouds], ["S2", sWhy], ["S3", sPeak], ["S4", sLadder], ["S5", sHands], ["S6", sClose]];
var EP = {
  badge: "STRAIGHT ANSWER #2", badgeBg: STRAIGHT.badgeBg, badgeFg: STRAIGHT.badgeFg, hook: "YOU CAN'T *DO* A GOAL.", hookEnd: LN("S1", 1) + .6,
  endAt: function () { return LN("S6", 1); }, endQ: "WHAT'S YOUR NEXT *PHYSICAL* STEP?",
  titles: [["WHY DO WE STOP DOING THINGS WE KNOW ARE *GOOD* FOR US?", LN("S2", 0), SCN.S2[1], 470, 8],
           ["REASON #7", LN("S2", 1), SCN.S2[1], 860, 14],
           ["THE GOAL HAS NO *TODAY* IN IT.", LN("S2", 1) + .5, SCN.S2[1], 1060, 7],
           ["CAN YOU PICTURE YOUR *HANDS* DOING IT?", SCN.S5[0], SCN.S5[1], 300, 8]]
};
