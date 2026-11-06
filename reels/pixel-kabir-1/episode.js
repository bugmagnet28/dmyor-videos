// =================== KABIR VS. KABIR #1: "Starting Monday" (Reason #1: the motivation you planned with is gone by the time you start) ===================
// Room art 270x480: bed x 4-93 (mattress top ~337), nightstand x 96-123, chair x 130-160, desk x 150-263 (top ~340), lamp ~246,310, floor y 400.

// ---------- wall calendar: 7 x 5, Mondays in column 0 ----------
var CAL = { x: 14, y: 104, cw: 14, ch: 12 };
function wallCalendar(u, mode, k) {   // mode "old": crossed Mondays; "new": a fresh month that fills with ticks (k = 0..1)
  calendarGrid(CAL.x, CAL.y, 7, 5, CAL.cw, CAL.ch, function (i, cx, cy, c, r) {
    if (mode === "old") {
      if (c === 0) { rect(cx + 1, cy + 1, CAL.cw - 3, 1, "#E0453A"); rect(cx + 1, cy + CAL.ch - 3, CAL.cw - 3, 1, "#E0453A"); rect(cx + 1, cy + 1, 1, CAL.ch - 3, "#E0453A"); rect(cx + CAL.cw - 3, cy + 1, 1, CAL.ch - 3, "#E0453A");
        if (r < 4 || u >= EP.xAt) redX(cx + 3, cy + 2, 7); }
    } else {
      var n = Math.floor(k * 33); if (i < n) { tick(cx + 1, cy + 4); if (i > 0 && c > 0) rect(cx - 3, cy + 6, 4, 1, "#7FE0A8"); }
    }
  });
  "MTWTFSS".split("").forEach(function (d, j) { ptext(L, d, CAL.x + j * CAL.cw + 4, CAL.y - 10, 1, "#FFFFFF"); });
}
function note(x, y, l1, l2, k) {      // sticky note on the wall
  if (k <= 0) return; var s = eout(k), w = 52, h = 26; L.save(); L.translate(x + w / 2, y + h / 2); L.scale(s, s); L.rotate(-.05); L.translate(-w / 2, -h / 2);
  L.fillStyle = "#2A1F2E"; L.fillRect(1, 2, w, h); L.fillStyle = "#FFE066"; L.fillRect(0, 0, w, h); L.fillStyle = "#F2C94C"; L.fillRect(0, 0, w, 4);
  ptext(L, l1, Math.round((w - pwidth(l1, 1)) / 2), 7, 1, "#2A1F2E"); ptext(L, l2, Math.round((w - pwidth(l2, 1)) / 2), 16, 1, "#E0453A"); L.restore();
}
var KX = 26, KY = 296;                // Kabir sitting on the bed
function room(u, dawn) { img(dawn ? "room_dawn" : "room_night", 0, 0); }
function motivation(u, v, x, y) { bar(x || 22, y || 284, 52, v, "MOTIVATION"); }

// S1: the calendar of crossed Mondays; pull back to Kabir writing tomorrow's plan
function sMonday(u, a, b) {
  room(u); wallCalendar(u, "old");
  var tl = LN("S1", 1); ptext(L, "X41", CAL.x + 100 - pwidth("X41", 2), CAL.y + 64, 2, "#E0453A");
  note(124, 112, "START", "MONDAY!", seg(u, LN("S1", 0) + .4, LN("S1", 0) + .8));
  chr(blinkAt(u, .4) ? "sit_bed_blink" : "sit_bed", KX, KY);
  return camAt([[0, 64, 150, 2], [tl + .2, 64, 150, 2], [tl + 1.6, 95, 250, 1.4, 1.4], [b, 95, 250, 1.4]], u);
}
// S2: the series question
function sWhy(u, a, b) {
  rect(0, 0, W, H, "#140F2E"); stars(u, 70);
  var k = eout(seg(u, a + .1, a + .6)); img(blinkAt(u, .2) ? "c_blink" : "c_lookup", 87, 298 + (1 - k) * 8, false, 2);
  if (u > a + .3) ptext(L, "?", 178, 282 - 3 * Math.sin(u * 3), 4, "#FFC145");
  return { x: 135, y: 240, z: 1 + .04 * seg(u, a, b) };
}
// S3: Kabir at the desk making the plan; the bar fills to 100%
function sPlan(u, a, b) {
  room(u); wallCalendar(u, "old"); note(124, 112, "START", "MONDAY!", 1);
  var w = Math.floor(u * 5) % 2 ? "sit_write1" : "sit_write0"; chr(w, 120, 302);
  rect(166, 328, 30, 12, "#FFF4E0"); for (var i = 0; i < 3; i++) rect(169, 331 + i * 3, 6 + 8 * seg(u, a + .3 + i * .5, a + .8 + i * .5), 1, "#3A3560");
  var v = eout(seg(u, LN("S3", 1), LN("S3", 1) + 1.6)); motivation(u, .12 + .88 * v, 120, 284);
  if (v >= 1) ddisc(146, 288, 26, "#FFE9A0", .35 * (1 - seg(u, LN("S3", 1) + 1.6, b)));
  return camAt([[a, 160, 318, 2.1], [b, 155, 310, 2.4, b - a]], u);
}
// S4: Friday, Saturday, Sunday: the bar drains on the bed
var DAYS = ["FRI", "SAT", "SUN"];
function sDrain(u, a, b) {
  var l0 = LN("S4", 0), e0 = LE("S4", 0), d = Math.min(2, Math.floor(seg(u, l0, e0 + .01) * 3)), dawn = d % 2 === 0 && u < LN("S4", 1);
  room(u, dawn); wallCalendar(u, "old"); note(124, 112, "START", "MONDAY!", 1);
  chr(blinkAt(u, .7) ? "bed_phone_blink" : "bed_phone", KX, KY);
  var steps = [.7, .4, .15], v = u < l0 ? 1 : (u < LN("S4", 1) ? lerp(d ? steps[d - 1] : 1, steps[d], eio(seg(u, l0 + d * (e0 - l0) / 3, l0 + d * (e0 - l0) / 3 + .4))) : lerp(.15, .05, seg(u, LN("S4", 1), LE("S4", 1))));
  motivation(u, v);
  if (u < LN("S4", 1) + .2) { var lab = DAYS[d], bw = pwidth(lab, 3) + 10; rect(100, 186, bw, 32, "#2A1F2E"); rect(101, 187, bw - 2, 30, "#FFC145"); ptext(L, lab, 105, 192, 3, "#1A1530"); }
  else { rect(100, 186, pwidth("MON", 3) + 10, 32, "#2A1F2E"); rect(101, 187, pwidth("MON", 3) + 8, 30, "#E0453A"); ptext(L, "MON", 105, 192, 3, "#FFFFFF"); }
  return camAt([[a, 95, 262, 1.6], [b, 90, 270, 1.7, b - a]], u);
}
// S5: Monday morning: alarm, 5%, "absolutely not", and another red X
function sNope(u, a, b) {
  room(u, true); wallCalendar(u, "old"); note(124, 112, "START", "MONDAY!", 1);
  var ring = u < a + 1.6, al = ring && Math.floor(u * 14) % 2; img(al ? "alarm1" : "alarm0", 102 + (ring ? (al ? 1 : -1) : 0), 346);
  if (ring) { rect(98, 342, 2, 2, "#FFFFFF"); rect(120, 342, 2, 2, "#FFFFFF"); }
  var no = u >= LN("S5", 1); chr(no ? "wave_off" : (blinkAt(u, .3) ? "sit_bed_blink" : "bed_yawn"), KX, KY);
  motivation(u, .05);
  if (no) { var k = eout(seg(u, LN("S5", 1), LN("S5", 1) + .3)); rect(66, 300, 34 * k, 14, "#2A1F2E"); if (k > .9) ptext(L, "NOPE.", 70, 304, 1, "#FFFFFF"); }
  return camAt([[a, 90, 300, 1.8], [LN("S5", 1) + .5, 92, 290, 1.7, .5], [LN("S5", 1) + 1.2, 62, 150, 2.4, .7], [b, 62, 150, 2.4]], u);
}
// S6: rewind to Sunday night: two minutes, right now, while the bar is full
function sTonight(u, a, b) {
  room(u); wallCalendar(u, "old"); note(124, 112, "TONIGHT", "2 MIN", 1);
  var r0 = LN("S6", 2), r1 = LE("S6", 2), done = u > r1 - .3;
  chr(done ? "sit_read_happy" : (blinkAt(u, .1) ? "sit_read_blink" : "sit_read"), KX, KY);
  motivation(u, 1);
  var left = Math.max(0, 120 - Math.floor(120 * seg(u, r0, r1 - .3))), ts = Math.floor(left / 60) + ":" + ("0" + left % 60).slice(-2);
  rect(76, 300, 30, 14, "#2A1F2E"); rect(77, 301, 28, 12, done ? "#28A86A" : "#3A3560"); ptext(L, ts, 80, 304, 1, "#FFFFFF");
  if (done) { var k = eout(seg(u, r1 - .3, r1 + .1)); ddisc(60, 300, 30 * k, "#B8F5C8", .4); L.save(); L.translate(52, 288); L.scale(2 * k, 2 * k); L.translate(-5, -3); tick(0, 0, "#28A86A"); L.restore(); }
  if (u < a + .6) { var s = seg(u, a, a + .6); for (var i = 0; i < 9; i++) rect(0, (hash(i + Math.floor(u * 20)) * H), W, 2 + hash(i) * 4, "rgba(255,255,255," + (.5 * (1 - s)) + ")"); ptext(L, "<<", 220, 30, 3, "#FFFFFF"); }
  return camAt([[a, 70, 285, 2.2], [b, 70, 290, 2.4, b - a]], u);
}
// S7: a fresh month; ticks fill in, a green chain
function sChain(u, a, b) {
  room(u); wallCalendar(u, "new", eio(seg(u, a + .3, b - .3)));
  note(124, 112, "TONIGHT", "2 MIN", 1);
  return camAt([[a, 64, 136, 2.5], [b, 64, 136, 2.7, b - a]], u);
}
// S8: Sunday night, pyjamas, the full calendar; push back into it (loops to frame 0)
function sEnd(u, a, b) {
  room(u); wallCalendar(u, "new", 1); note(124, 112, "TONIGHT", "2 MIN", 1);
  chr(blinkAt(u, .5) ? "sit_read_blink" : "sit_read_happy", KX, KY); motivation(u, .8 + .1 * Math.sin(u * 2));
  return camAt([[a, 95, 262, 1.4], [LN("S8", 1) + 1, 95, 262, 1.4], [LN("S8", 2), 64, 150, 2, 1.4]], u);
}

var SCENES = [["S1", sMonday], ["S2", sWhy], ["S3", sPlan], ["S4", sDrain], ["S5", sNope], ["S6", sTonight], ["S7", sChain], ["S8", sEnd]];
var EP = {
  badge: "KABIR VS. KABIR #1", hook: "HE STARTS ON *MONDAY.*", hookEnd: LN("S1", 1) + .3,
  xAt: LN("S5", 1) + 1.5, endAt: function () { return LN("S8", 2); }, endQ: "WHAT ARE YOU STARTING ON *MONDAY?*",
  titles: [["WHY DO WE STOP DOING THINGS WE KNOW ARE *GOOD* FOR US?", LN("S2", 0), SCN.S2[1], 470, 8],
           ["REASON #1", LN("S2", 1), SCN.S2[1], 860, 14],
           ["MOTIVATION *EXPIRES.*", LN("S2", 1) + .5, SCN.S2[1], 1060, 7],
           ["MOTIVATION PEAKS AT THE *PLAN.*", LN("S3", 1), SCN.S3[1], 300, 8],
           ["A *SMALLER* TONIGHT.", LN("S6", 1), SCN.S6[1], 300, 9],
           ["TOO SMALL TO *SKIP.*", LN("S7", 0), SCN.S7[1], 300, 9]]
};
