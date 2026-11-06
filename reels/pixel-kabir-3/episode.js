// =================== KABIR VS. KABIR #3: "Today was okay" (Reason #3: you never notice you have stopped, because "okay" hides it) ===================

var DN = ["MON", "TUE", "WED", "THU", "FRI", "SAT", "SUN"];
function spread(u, lines, hiK) {      // open journal, two pages; lines(i) -> text for day i; hiK = highlighter sweep 0..7
  rect(0, 0, W, H, "#3A2A22"); for (var i = 0; i < 12; i++) rect(0, i * 40, W, 1, "#33241D");
  rect(4, 138, 262, 262, "#2A1F2E"); rect(6, 140, 128, 258, "#FFF4E0"); rect(136, 140, 128, 258, "#FFF4E0"); rect(133, 140, 4, 258, "#D8C9A8");
  for (var r = 0; r < 16; r++) { rect(10, 158 + r * 15, 120, 1, "#E4D6B8"); rect(140, 158 + r * 15, 120, 1, "#E4D6B8"); }
  for (var d = 0; d < 7; d++) {
    var left = d < 4, x = left ? 12 : 142, y = 150 + (left ? d : d - 4) * 60, t = lines(d);
    ptext(L, DN[d], x, y, 1, "#E0453A");
    if (hiK != null && hiK > d) rect(x - 2, y + 12, Math.min(1, hiK - d) * (pwidth(t[0], 1) + 4), 10, "#FFE066");
    ptext(L, t[0], x, y + 14, 1, t[2] || "#3A3560"); if (t[1]) ptext(L, t[1], x, y + 28, 1, t[2] || "#3A3560");
  }
}
function okay(d) { return ["TODAY WAS OKAY.", ""]; }
function deskNight(u, writing) {
  img("room_night", 0, 0); ddisc(246, 318, 40, "#FFE9A0", .3);
  chr(writing ? (Math.floor(u * 5) % 2 ? "sit_write1" : "sit_write0") : "sit_write0", 120, 302); rect(166, 334, 22, 6, "#C2566A"); rect(168, 334, 18, 2, "#FFF4E0");
}
// S1: the week of "today was okay" (frame 0) -> Kabir writing, very serious -> back to the week, highlighted
function sWeek(u, a, b) {
  var c1 = LN("S1", 1) - .15, c2 = LN("S1", 2) - .15;
  if (u >= c1 && u < c2) { deskNight(u, true); return camAt([[c1, 165, 300, 2.6], [c2, 160, 305, 2.8, c2 - c1]], u); }
  spread(u, okay, u >= c2 ? 7 * seg(u, LN("S1", 3), LE("S1", 3)) : null);
  return u < c1 ? camAt([[0, 135, 240, 1], [c1, 135, 250, 1.04, c1]], u) : camAt([[c2, 135, 240, 1], [b, 135, 250, 1.05, b - c2]], u);
}
function sWhy(u, a, b) { return whyScene(u, a, b); }
// S3: the week strip: every day says OKAY while the gym, the book and the plan fade out
function icon(kind, x, y, ghost) {
  var c = ghost ? "#B8B0C8" : null;
  if (kind === 0) { rect(x + 4, y + 7, 16, 3, c || "#3A3560"); rect(x + 1, y + 3, 4, 11, c || "#E0453A"); rect(x + 19, y + 3, 4, 11, c || "#E0453A"); }
  else if (kind === 1) { rect(x + 3, y + 2, 18, 13, c || "#2A1F2E"); rect(x + 4, y + 3, 8, 11, c || "#4C9AFF"); rect(x + 12, y + 3, 8, 11, c || "#3A7AE0"); }
  else { rect(x + 5, y + 1, 14, 16, c || "#2A1F2E"); rect(x + 6, y + 2, 12, 14, c || "#FFFFFF"); for (var i = 0; i < 3; i++) rect(x + 8, y + 5 + i * 3, 8, 1, c || "#28A86A"); }
  if (ghost) { L.fillStyle = "#FFF4E0"; for (var yy = 0; yy < 18; yy++) for (var xx = 0; xx < 24; xx++) if (bay(xx, yy) < .55) L.fillRect(x + xx, y + yy, 1, 1); }
}
var STOP = [1, 3, 4];                 // gym stops on Tue, the book on Thu, the plan on Fri
function sStrip(u, a, b) {
  rect(0, 0, W, H, "#2A2245"); rect(10, 140, 250, 208, "#1A1530"); rect(12, 142, 246, 204, "#FFF4E0");
  var lab = ["GYM", "BOOK", "PLAN"], f0 = LN("S3", 2);
  for (var i = 0; i < 7; i++) { var x = 16 + i * 34; rect(x, 148, 32, 12, "#3A3560"); ptext(L, DN[i], x + 7, 151, 1, "#FFFFFF");
    for (var k = 0; k < 3; k++) { var gone = i >= STOP[k] && u > f0 + k * .7 + (i - STOP[k]) * .12; icon(k, x + 4, 172 + k * 34, gone); }
    var ok = u > LN("S3", 1) + i * .15; rect(x + 1, 290, 30, 14, ok ? "#28A86A" : "#E4D6B8"); if (ok) ptext(L, "OKAY", x + 4, 294, 1, "#FFFFFF"); }
  for (var k2 = 0; k2 < 3; k2++) ptext(L, lab[k2], 16, 166 + k2 * 34, 1, "#9A92C0");
  return camAt([[a, 135, 240, 1.08], [b, 135, 244, 1.14, b - a]], u);
}
// S4: the mirror: "how was today?" "okay." (shrug)
function sMirror(u, a, b) {
  rect(0, 0, W, H, "#5A6B8C"); for (var y = 0; y < 400; y += 14) for (var x = (y / 14) % 2 ? 7 : 0; x < W; x += 14) rect(x, y, 13, 13, "#647698");
  rect(0, 380, W, H - 380, "#3A4560"); rect(140, 180, 92, 150, "#2A1F2E"); rect(144, 184, 84, 142, "#A8C8E8"); rect(150, 190, 6, 40, "#D8ECFF");
  chr(blinkAt(u, .2) ? "blink" : "stand", 84, 327);
  L.save(); L.beginPath(); L.rect(144, 184, 84, 142); L.clip(); var shrug = u > LN("S4", 1) + 1.1; chr(shrug ? "wave_off" : "stand", 166, 238, true); L.fillStyle = "rgba(168,200,232,.3)"; L.fillRect(144, 184, 84, 142); L.restore();
  var q = LN("S4", 1); if (u > q) { bubble(60, 262, 88, 16, 110); ptext(L, "HOW WAS TODAY?", 64, 267, 1, "#1A1530"); }
  if (u > q + 1.1) { bubble(186, 196, 38, 16, 0); ptext(L, "OKAY.", 191, 201, 1, "#1A1530"); }
  return camAt([[a, 150, 280, 1.45], [b, 150, 276, 1.55, b - a]], u);
}
// S5/S6: one page, the new question, then the honest answers
var ANS = ["CALLED NO ONE ABOUT THE JOB.", "SKIPPED THE HARD CHAPTER.", "DIDN'T OPEN THE BUSINESS PLAN."];
function page(u) { rect(0, 0, W, H, "#3A2A22"); rect(26, 110, 218, 272, "#2A1F2E"); rect(28, 112, 214, 268, "#FFF4E0"); for (var r = 0; r < 16; r++) rect(34, 150 + r * 14, 202, 1, "#E4D6B8"); rect(40, 112, 1, 268, "#F0B8B0"); }
function question(u, t0) { var s = "WHAT DID I AVOID TODAY?", n = Math.floor(seg(u, t0, t0 + .9) * s.length); ptext(L, s.slice(0, n), 46, 128, 1, "#C9902E"); rect(46, 137, pwidth(s, 1) * (n / s.length), 1, "#C9902E"); }
function sAsk(u, a, b) { page(u); ptext(L, "TODAY WAS OKAY.", 46, 128, 1, u < LN("S5", 1) - .2 ? "#3A3560" : "rgba(0,0,0,0)"); if (u > LN("S5", 0) + 1 && u < LN("S5", 1) - .2) { var k = seg(u, LN("S5", 0) + 1, LN("S5", 1) - .2); rect(44, 131, (pwidth("TODAY WAS OKAY.", 1) + 4) * k, 1, "#E0453A"); }
  if (u > LN("S5", 1) - .2) question(u, LN("S5", 1) - .2); return camAt([[a, 135, 250, 1.2], [b, 135, 210, 1.25, b - a]], u); }
function sFull(u, a, b) {
  page(u); question(u, -9); var g = LN("S6", 1);
  ANS.forEach(function (s, i) { var t0 = a + .2 + i * .55, n = Math.floor(seg(u, t0, t0 + .5) * s.length); if (u > g + .3 + i * .5) rect(44, 160 + i * 28 - 2, pwidth(s, 1) + 4, 10, "#FFE066"); ptext(L, s.slice(0, n), 46, 160 + i * 28, 1, "#3A3560"); });
  for (var j = 0; j < 4; j++) rect(46, 250 + j * 14, 60 + hash(j) * 100, 1, "#B8B0C8");
  return camAt([[a, 135, 210, 1.25], [b, 135, 222, 1.25, b - a]], u);
}
// S7: next morning: the avoided email goes first
function sSend(u, a, b) {
  img("room_dawn", 0, 0); var s0 = LN("S7", 1) - .2, sent = u > s0;
  chr(sent ? "sit_type0" : (Math.floor(u * 6) % 2 ? "sit_type1" : "sit_type0"), 120, 302); img("laptop", 166, 314);
  if (!sent) { bubble(150, 268, 70, 22, 0); ptext(L, "RE: THE JOB", 154, 272, 1, "#1A1530"); ptext(L, "SEND >", 154, 281, 1, "#28A86A"); }
  else { var k = seg(u, s0, s0 + 1.2), ex = lerp(186, 300, eio(k)), ey = lerp(300, 120, eio(k)); rect(ex, ey, 14, 10, "#FFFFFF"); rect(ex, ey, 14, 1, "#3A3560"); rect(ex + 3, ey + 2, 8, 3, "#C8C0E8");
    if (u > s0 + .4) { L.save(); L.translate(198, 262); L.scale(2, 2); tick(0, 0, "#28A86A"); L.restore(); } }
  return camAt([[a, 165, 300, 2.3], [b, 170, 296, 2.5, b - a]], u);
}
// S8: the journal now: one honest line a day (loops to frame 0)
var HON = [["AVOIDED: THE CALL.", "DID IT TUE."], ["AVOIDED: CHAPTER 7.", "READ 4 PAGES."], ["AVOIDED: THE PLAN.", "OPENED IT."], ["AVOIDED: NOTHING.", "GYM, 7:00."], ["AVOIDED: THE EMAIL.", "SENT IT."], ["AVOIDED: RUNNING.", "WALKED."], ["AVOIDED: ...", ""]];
function sHonest(u, a, b) { spread(u, function (d) { return [HON[d][0], HON[d][1], d < 6 ? "#3A3560" : "#9A92C0"]; }, null); return camAt([[a, 135, 240, 1], [b, 135, 240, 1]], u); }

var SCENES = [["S1", sWeek], ["S2", sWhy], ["S3", sStrip], ["S4", sMirror], ["S5", sAsk], ["S6", sFull], ["S7", sSend], ["S8", sHonest]];
var EP = {
  badge: "KABIR VS. KABIR #3", hook: "7 DAYS OF *REFLECTION.*", hookEnd: LN("S1", 1) - .2,
  endAt: function () { return LN("S8", 2); }, endQ: "WHAT DID YOU *AVOID* TODAY?",
  titles: [["WHY DO WE STOP DOING THINGS WE KNOW ARE *GOOD* FOR US?", LN("S2", 0), SCN.S2[1], 470, 8],
           ["REASON #3", LN("S2", 1), SCN.S2[1], 860, 14],
           ["\"OKAY\" *HIDES* IT.", LN("S2", 1) + .5, SCN.S2[1], 1060, 7],
           ["YOU DON'T NOTICE YOU *STOPPED.*", LN("S3", 0), SCN.S3[1], 300, 8],
           ["THE EASIEST QUESTION TO *LIE* TO.", LN("S4", 1), SCN.S4[1], 300, 8],
           ["YOUR AVOID LIST IS YOUR *REAL* TO-DO LIST.", LN("S7", 1), SCN.S7[1], 300, 8]]
};
