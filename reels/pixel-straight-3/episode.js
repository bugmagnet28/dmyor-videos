// =================== STRAIGHT ANSWER #3: "Plan the bad day" (Reason #10: no plan for the obstacle) ===================
function world(u, dusk) {
  var C = dusk ? ["#4A2A66", "#7A3A6E", "#C2566A", "#F08A5C"] : ["#6FA8E8", "#86B9EE", "#9DC9F2", "#B4D8F6"]; for (var i = 0; i < 4; i++) rect(0, i * 75, W, 75, C[i]);
  rect(0, 300, W, 180, "#5A8A4A"); rect(0, 340, W, 34, "#4A4A5A"); rect(0, 340, W, 2, "#2A2A3A"); rect(0, 372, W, 2, "#2A2A3A"); for (var x = 0; x < W; x += 24) rect(x + 6, 356, 12, 2, "#E9E4D0");
  rect(212, 286, 2, 56, "#2A1F2E"); rect(214, 286, 4 + 0, 11, "#E0453A"); rect(214, 286, 12, 11, "#E0453A"); ptext(L, "GOAL", 200, 274, 1, "#FFFFFF");
}
function rock(x, label, k) { if (k <= 0) return; var y = 334 - (1 - eout(k)) * 120; rect(x - 16, y - 18, 32, 22, "#1A1530"); rect(x - 15, y - 17, 30, 20, "#8A8070"); rect(x - 12, y - 15, 10, 4, "#A89F8C"); ptext(L, label, x - pwidth(label, 1) / 2, y - 30, 1, "#FFFFFF"); }
function rain(u, x, k) { if (k <= 0) return; rect(x - 18, 264, 36, 12, "#5A6A8A"); rect(x - 12, 258, 22, 8, "#5A6A8A"); for (var i = 0; i < 10; i++) { var t = (u * 2 + hash(i)) % 1; rect(x - 16 + hash(i + 4) * 32, 278 + t * 56, 1, 5, "#9FB4E8"); } ptext(L, "RAIN", x - 11, 260 - 10, 1, "#FFFFFF"); }
function ringing(u, x, k) { if (k <= 0) return; var j = Math.floor(u * 16) % 2; rect(x - 5 + j, 314, 10, 16, "#1A1530"); rect(x - 4 + j, 315, 8, 14, "#7FD4FF"); rect(x - 10, 316, 2, 2, "#FFFFFF"); rect(x + 8, 316, 2, 2, "#FFFFFF"); ptext(L, "CALL", x - 11, 300, 1, "#FFFFFF"); }
var OB = [122, 158, 190];
function walkerX(u, t0, t1, x0, x1) { return lerp(x0, x1, seg(u, t0, t1)); }
// S1: the plan, on a normal day (frame 0)
function sPlan(u, a, b) { world(u); var x = walkerX(u, 0, b, 30, 50); chr("walk" + (Math.floor(u * 7) % 4), x, 340 - GY); signCard(130, 204, ["PLAN:", "GYM, 7 PM"], "#FFFFFF", "#3A3560", 2); return camAt([[0, 130, 270, 1.5], [b, 130, 270, 1.5, b]], u); }
function sWhy(u, a, b) { return whyScene(u, a, b); }
// S3: late, rain, a call: the plan stops
function sBreak(u, a, b) {
  world(u); var t1 = LN("S3", 1), e1 = LE("S3", 1), stop = LN("S3", 2);
  var x = u < stop ? walkerX(u, a, stop, 46, 52) : 52; chr(u < stop ? "walk" + (Math.floor(u * 7) % 4) : (blinkAt(u, .2) ? "sad_blink" : "sad"), x, 340 - GY);
  rock(OB[0], "LATE AT WORK", seg(u, t1, t1 + .4)); rain(u, OB[1], seg(u, t1 + (e1 - t1) * .45, t1 + (e1 - t1) * .45 + .3)); ringing(u, OB[2], seg(u, t1 + (e1 - t1) * .75, t1 + (e1 - t1) * .75 + .2));
  var g = u > stop + .3; signCard(130, 204, ["PLAN:", "GYM, 7 PM"], g ? "#8A8498" : "#FFFFFF", "#3A3560", 2); if (g) rect(84, 219, 92 * eout(seg(u, stop + .3, stop + .7)), 2, "#E0453A");
  return camAt([[a, 130, 270, 1.5], [b, 130, 275, 1.55, b - a]], u);
}
// S4: inventing a new plan, while tired
function sTired(u, a, b) {
  world(u, true); chr(blinkAt(u, .1) ? "sad_blink" : "sad", 52, 340 - GY); rock(OB[0], "LATE AT WORK", 1);
  rect(30, 210, 50, 20, "#1A1530"); rect(32, 212, 46, 16, "#3A3560"); rect(34, 214, 6, 12, "#E0453A"); ptext(L, "ENERGY", 42, 216, 1, "#FFFFFF"); rect(80, 216, 3, 8, "#1A1530");
  if (u < LN("S4", 1)) { bubble(96, 248, 74, 16, 104); ptext(L, "NEW PLAN?", 106, 253, 1, "#1A1530"); } else { bubble(100, 254, 32, 16, 104); ptext(L, "NAH.", 106, 259, 1, "#1A1530"); }
  return camAt([[a, 105, 280, 1.6], [b, 100, 285, 1.7, b - a]], u);
}
// S5: decide it in advance: if-then cards
function ifThen(y, i1, t1, k) { if (k <= 0) return; var s = eout(k); L.save(); L.translate(135, y + 22); L.scale(s, s); L.translate(-110, -22);
  rect(-1, -1, 222, 46, "#1A1530"); rect(0, 0, 220, 44, "#FFF4E0"); rect(0, 0, 40, 44, "#E0453A"); ptext(L, "IF", 13, 18, 2, "#FFFFFF"); ptext(L, i1, 48, 8, 1, "#3A3560");
  rect(48, 22, 160, 1, "#C8C0B0"); ptext(L, "THEN: " + t1, 48, 29, 1, "#28A86A"); L.restore(); }
function sIfThen(u, a, b) {
  rect(0, 0, W, H, "#1A1530"); stars(u, 25, "#5A5590");
  var t = LN("S5", 2), e = LE("S5", 2), mid = t + (e - t) * .5;
  if (u > LN("S5", 1) && u < t) ifThen(170, "THIS HAPPENS", "I'LL DO THAT", seg(u, LN("S5", 1), LN("S5", 1) + .3));
  ifThen(170, "I'M LATE AT WORK", "10 MIN AT HOME", seg(u, t, t + .3)); ifThen(240, "IT RAINS", "TAKE THE STAIRS", seg(u, mid, mid + .3));
  if (u > e) ifThen(310, "SOMEONE CALLS", "CALL BACK AT 8", seg(u, e, e + .3));
  return camAt([[a, 135, 250, 1.04], [b, 135, 255, 1.06, b - a]], u);
}
// S6: every obstacle has a detour; the walker reaches the goal
function sDetour(u, a, b) {
  world(u); OB.forEach(function (x, i) { if (i === 0) rock(x, "LATE", 1); else if (i === 1) rain(u, x, 1); else ringing(u, x, 1);
    for (var d = 0; d < 7; d++) rect(x - 24 + d * 8, 324 - 34 * Math.sin(d / 6 * Math.PI), 4, 2, "#FFE066"); });
  var k = seg(u, a + .2, LN("S6", 2) - .3), x = lerp(40, 180, k), off = 0; OB.forEach(function (ox) { var dd = Math.abs(x + 24 - ox); if (dd < 26) off = Math.max(off, Math.sin((1 - dd / 26) * Math.PI / 2) * 36); });
  chr(k < 1 ? (off > 4 ? "jump" : "walk" + (Math.floor(u * 7) % 4)) : "jump", x, 340 - GY - off); if (k >= 1) ddisc(216, 290, 24, "#FFE9A0", .4);
  return camAt([[a, 130, 270, 1.45], [b, 130, 270, 1.5, b - a]], u);
}

var SCENES = [["S1", sPlan], ["S2", sWhy], ["S3", sBreak], ["S4", sTired], ["S5", sIfThen], ["S6", sDetour]];
var EP = {
  badge: "STRAIGHT ANSWER #3", badgeBg: STRAIGHT.badgeBg, badgeFg: STRAIGHT.badgeFg, hook: "PLANS BREAK ON *BAD DAYS.*", hookEnd: LN("S1", 1) + .4,
  endAt: function () { return LN("S6", 2); }, endQ: "WHAT USUALLY *BREAKS* YOUR PLAN?",
  titles: [["WHY DO WE STOP DOING THINGS WE KNOW ARE *GOOD* FOR US?", LN("S2", 0), SCN.S2[1], 470, 8],
           ["REASON #10", LN("S2", 1), SCN.S2[1], 860, 14],
           ["NO PLAN FOR THE *OBSTACLE.*", LN("S2", 1) + .5, SCN.S2[1], 1060, 7],
           ["DECIDE IT *IN ADVANCE.*", LN("S5", 0), SCN.S5[1], 300, 9]]
};
