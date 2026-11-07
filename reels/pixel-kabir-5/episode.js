// =================== KABIR VS. KABIR #5: "The guitar in the closet" (Reason #6: the good thing is far, the easy thing is near) ===================
function guitar(x, y, rot, s) {        // acoustic guitar, body centre at x,y
  L.save(); L.translate(x, y); L.rotate(rot || 0); L.scale(s || 1, s || 1);
  rect(-3, -46, 6, 34, "#2A1F2E"); rect(-2, -46, 4, 34, "#8A5228"); rect(-4, -52, 8, 7, "#2A1F2E"); rect(-3, -51, 6, 5, "#6B4430");
  rect(-12, -14, 24, 30, "#2A1F2E"); rect(-14, -6, 28, 22, "#2A1F2E"); rect(-11, -13, 22, 28, "#E08A3A"); rect(-13, -5, 26, 20, "#E08A3A"); rect(-11, 10, 22, 4, "#C26A22");
  rect(-4, -3, 8, 8, "#2A1F2E"); rect(-6, 9, 12, 2, "#2A1F2E"); for (var i = -1; i <= 1; i++) rect(i * 2, -46, 1, 56, "#FFF4E0"); L.restore();
}
function caseShape(cx, cy) {   // guitar-shaped case lying on its side
  rect(cx - 46, cy - 5, 50, 10, "#1A1530"); rect(cx + 2, cy - 14, 28, 28, "#1A1530"); rect(cx + 28, cy - 10, 16, 20, "#1A1530");
  rect(cx - 45, cy - 4, 48, 8, "#4A3428"); rect(cx + 3, cy - 13, 26, 26, "#4A3428"); rect(cx + 29, cy - 9, 14, 18, "#4A3428"); rect(cx - 30, cy - 1, 60, 1, "#C9A86A"); rect(cx + 12, cy + 9, 8, 3, "#C9A86A");
}
function box(x, y, w, h) { rect(x - 1, y - 1, w + 2, h + 2, "#2A1F2E"); rect(x, y, w, h, "#C99A5E"); rect(x, y, w, 3, "#B0824A"); rect(x + w / 2 - 3, y, 6, h, "#E0C08A"); }
function closet(u, open) {
  rect(146, 140, 108, 240, "#2A1F2E"); rect(148, 142, 104, 236, open ? "#231C3A" : "#8A5228");
  if (open) { rect(150, 172, 100, 2, "#6B4430"); for (var i = 0; i < 6; i++) rect(156 + i * 15, 176, 12, 60 + (i % 2) * 14, ["#4C9AFF", "#E0453A", "#6CC7A3", "#FFC145", "#B07CFF", "#FF9FC2"][i]);
    caseShape(200, 362);      // guitar case
    box(158, 322, 34, 22); box(196, 316, 40, 28); box(176, 292, 36, 24); }
  else { rect(199, 142, 2, 236, "#6B4430"); rect(190, 250, 3, 12, "#FFC145"); rect(207, 250, 3, 12, "#FFC145"); }
}
function phone(x, y, lit) { rect(x - 1, y - 1, 10, 16, "#1A1530"); rect(x, y, 8, 14, lit ? "#7FD4FF" : "#3A3560"); if (lit) ddisc(x + 4, y + 7, 14, "#7FD4FF", .25); }
// S1: the closet, the case, three boxes (frame 0)
function sCloset(u, a, b) {
  floorRoom("#3B3A6A", "#34335E"); closet(u, true); chr(blinkAt(u, .4) ? "blink" : "stand", 70, 327);
  if (u > LN("S1", 1) + .4) ptext(L, "1", 178, 298, 1, "#1A1530"), ptext(L, "2", 204, 322, 1, "#1A1530"), ptext(L, "3", 172, 328, 1, "#1A1530");
  return camAt([[0, 190, 300, 1.9], [LN("S1", 1) - .2, 190, 300, 1.9], [LN("S1", 1) + 1.2, 150, 280, 1.35, 1.2], [b, 150, 280, 1.4]], u);
}
function sWhy(u, a, b) { return whyScene(u, a, b); }
// S3: six steps vs one step
var GSTEPS = ["OPEN CLOSET", "MOVE BOX 1", "MOVE BOX 2", "MOVE BOX 3", "OPEN CASE", "TUNE IT"];
function sSteps(u, a, b) {
  rect(0, 0, W, H, "#1A1530"); stars(u, 20, "#5A5590");
  ptext(L, "GUITAR", 20, 120, 2, "#E08A3A"); ptext(L, "PHONE", 160, 120, 2, "#7FD4FF");
  var t0 = a + .2, step = (LE("S3", 0) - t0) / 6;
  GSTEPS.forEach(function (s, i) { var k = seg(u, t0 + i * step, t0 + i * step + .2); if (k <= 0) return; var y = 146 + i * 26; rect(18, y, 120, 20, "#2A1F2E"); rect(19, y + 1, 118, 18, "#3A3560"); ptext(L, (i + 1) + ". " + s, 24, y + 7, 1, "#FFFFFF"); });
  if (u > LN("S3", 1)) { rect(158, 146, 76, 20, "#2A1F2E"); rect(159, 147, 74, 18, "#3A3560"); ptext(L, "1. UNLOCK", 164, 153, 1, "#FFFFFF"); phone(192, 180, true); }
  if (u > LE("S3", 0)) { ptext(L, "6", 70, 312, 4, "#E08A3A"); } if (u > LN("S3", 1) + .4) { ptext(L, "1", 188, 312, 4, "#7FD4FF"); }
  return camAt([[a, 135, 230, 1.08], [b, 135, 236, 1.1, b - a]], u);
}
// S4: every evening the phone wins; the clock runs
function sScroll(u, a, b) {
  img("room_night", 0, 0); closet(u, false);
  chr(blinkAt(u, .2) ? "bed_phone_blink" : "bed_phone", 26, 296); ddisc(56, 316, 22, "#7FD4FF", .3);
  var k = seg(u, a, b), hrs = ["9:00 PM", "10:00 PM", "11:00 PM", "12:00 AM", "1:00 AM"], h = hrs[Math.min(4, Math.floor(k * 5))];
  rect(20, 150, 70, 22, "#2A1F2E"); rect(21, 151, 68, 20, "#1A1530"); ptext(L, h, 55 - pwidth(h, 1) / 2, 158, 1, "#FF7A59");
  var d = ["MON", "TUE", "WED", "THU", "FRI"][Math.min(4, Math.floor(k * 5))]; dayTag(d, 20, 186, "#FFC145");
  return camAt([[a, 100, 260, 1.5], [b, 95, 270, 1.6, b - a]], u);
}
// S5: distance decides: one step to the phone, six to the guitar
function sDistance(u, a, b) {
  rect(0, 0, W, H, "#2A2245"); rect(0, 300, W, 180, "#3A3560");
  chr("stand", 111, 247); var k = seg(u, a + .2, a + 1.2);
  for (var i = 0; i < 6; i++) if (k * 6 > i) { rect(156 + i * 16, 296, 10, 4, "#E08A3A"); }
  rect(108, 296, 10, 4, "#7FD4FF");
  phone(86, 262, true); guitar(258, 260, 0, .9);
  ptext(L, "1 STEP", 62, 310, 1, "#7FD4FF"); ptext(L, "6 STEPS", 190, 310, 1, "#E08A3A");
  if (u > LN("S5", 1)) { var w = eout(seg(u, LN("S5", 1), LN("S5", 1) + .3)); signCard(94, 200, ["WINS"], "#7FD4FF", "#1A1530", 2, w); }
  return camAt([[a, 150, 260, 1.4], [b, 150, 260, 1.45, b - a]], u);
}
// S6: the guitar moves next to the bed; the phone sleeps in the kitchen
function sMove(u, a, b) {
  if (u < LN("S6", 1) - .1) {
    img("room_night", 0, 0); closet(u, false); var k = eio(seg(u, a + .3, a + 1.6)); guitar(lerp(200, 112, k), lerp(330, 344, k), lerp(-.3, -.15, k));
    if (k >= 1) { rect(104, 372, 16, 3, "#2A1F2E"); rect(110, 360, 3, 14, "#2A1F2E"); }
    return camAt([[a, 130, 300, 1.7], [b, 120, 300, 1.8, b - a]], u);
  }
  rect(0, 0, W, H, "#E9E4D0"); for (var i = 0; i < 14; i++) for (var j = 0; j < 9; j++) rect(i * 20 + (j % 2) * 10, 160 + j * 12, 19, 11, "#F4F0E2");
  rect(0, 270, W, 110, "#8A5228"); rect(0, 266, W, 6, "#C9A86A"); rect(0, 380, W, H - 380, "#B8B0A0");
  rect(150, 238, 40, 30, "#FFFFFF"); rect(150, 238, 40, 3, "#C8C0B0"); phone(166, 246, false); rect(169, 260, 2, 8, "#2A1F2E");
  ptext(L, "Z", 186, 226 - 4 * Math.sin(u * 3), 1, "#3A3560"); ptext(L, "Z", 194, 214 - 4 * Math.sin(u * 3 + 1), 2, "#3A3560");
  signCard(135, 120, ["KITCHEN"], "#FFFFFF", "#1A1530", 2);
  return camAt([[LN("S6", 1), 150, 240, 1.6], [b, 160, 240, 1.75, b - LN("S6", 1)]], u);
}
// S7: one step to play, six to scroll (loops to the room)
function sPlay(u, a, b) {
  img("room_night", 0, 0); closet(u, false); chr("sit_bed", 26, 296); guitar(56, 330, -1.1, .8);
  for (var i = 0; i < 3; i++) { var t = (u * .7 + i / 3) % 1; var nx = 70 + i * 12 + t * 20, ny = 300 - t * 40, nc = ["#FFC145", "#6CC7A3", "#FF9FC2"][i]; rect(nx, ny + 6, 4, 3, nc); rect(nx + 3, ny, 1, 8, nc); rect(nx + 3, ny, 3, 1, nc); }
  signCard(112, 186, ["PLAY: 1 STEP", "SCROLL: 6 STEPS"], "#28A86A", "#FFFFFF", 1);
  return camAt([[a, 100, 280, 1.6], [b, 100, 280, 1.7, b - a]], u);
}

var SCENES = [["S1", sCloset], ["S2", sWhy], ["S3", sSteps], ["S4", sScroll], ["S5", sDistance], ["S6", sMove], ["S7", sPlay]];
var EP = {
  badge: "KABIR VS. KABIR #5", hook: "THE GUITAR IS *IN THERE.*", hookEnd: LN("S1", 1) + .5,
  endAt: function () { return LN("S7", 1); }, endQ: "WHAT'S HIDING IN YOUR *CLOSET?*",
  titles: [["WHY DO WE STOP DOING THINGS WE KNOW ARE *GOOD* FOR US?", LN("S2", 0), SCN.S2[1], 470, 8],
           ["REASON #6", LN("S2", 1), SCN.S2[1], 860, 14],
           ["THE GOOD THING IS *FAR.*", LN("S2", 1) + .5, SCN.S2[1], 1060, 7],
           ["WHATEVER IS *CLOSEST* WINS.", LN("S5", 1), SCN.S5[1], 300, 8]]
};
