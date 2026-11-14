// =================== KABIR VS. KABIR #10: rehearsing silently (practise out loud) ===================
function stage(u) { rect(0, 0, W, H, "#1E1A33"); ddisc(135, 250, 90, "#FFE9A0", .12); rect(0, 360, W, 20, "#6B4430"); rect(0, 380, W, H - 380, "#2A1F2E");
  for (var i = 0; i < 9; i++) { var x = 8 + i * 30; rect(x + 6, 404, 14, 14, "#1A1530"); rect(x + 2, 418, 22, 20, "#1A1530"); } rect(170, 300, 2, 60, "#8A8498"); rect(164, 296, 14, 8, "#2A1F2E"); }
function slides(x, y, n) { rect(x - 1, y - 1, 62, 42, "#1A1530"); rect(x, y, 60, 40, "#FFFFFF"); rect(x, y, 60, 8, "#4C9AFF"); for (var i = 0; i < 3; i++) rect(x + 6, y + 14 + i * 7, 30 + (i * 13) % 20, 2, "#8A8498"); ptext(L, "SLIDE " + n, x + 4, y + 1, 1, "#FFFFFF"); }
function skillBar(x, y, label, v, col) { ptext(L, label, x, y, 1, "#FFFFFF"); rect(x, y + 10, 200, 14, "#1A1530"); rect(x + 1, y + 11, 198 * v, 12, col); }
// S1: twenty silent read-throughs (frame 0)
function sRead(u, a, b) {
  img("room_night", 0, 0); chr(blinkAt(u, .3) ? "sit_type0" : "sit_type1", 120, 302); slides(170, 290, 4);
  counter(48, 196, "READ-THROUGHS", "20", "#FFC145", 3);
  if (u > LN("S1", 1) + 1.5) { bubble(150, 268, 64, 16, 150); ptext(L, "FLAWLESS.", 156, 273, 1, "#1A1530"); }
  return camAt([[0, 140, 260, 1.3], [b, 140, 262, 1.35, b]], u);
}
// S2: next morning, on stage: nothing comes out
function sStage(u, a, b) {
  stage(u); chr(u > LN("S2", 0) + 1.6 ? "shock" : "stand", 120, 307);
  if (u > LN("S2", 0) + 1.6) { bubble(150, 250, 30, 16, 150); ptext(L, "UH.", 156, 255, 1, "#1A1530"); }
  return camAt([[a, 140, 310, 1.9], [b, 140, 310, 2.0, b - a]], u);
}
// S3: two different skills: reading in your head 20 reps, out loud 0
function sSkills(u, a, b) {
  rect(0, 0, W, H, "#1A1530"); stars(u, 20, "#5A5590");
  skillBar(35, 170, "READING IN YOUR HEAD", eout(seg(u, a + .2, a + 1)), "#4C9AFF"); ptext(L, "20 REPS", 190, 170, 1, "#7FD4FF");
  skillBar(35, 220, "SAYING IT OUT LOUD", 0, "#28A86A"); if (u > a + 1.4) ptext(L, "0 REPS", 196, 220, 1, "#E0453A");
  return camAt([[a, 135, 220, 1.3], [b, 135, 220, 1.35, b - a]], u);
}
// S4: rehearse out loud, standing, once to a friend; the first run is terrible
function sRehearse(u, a, b) {
  img("room_dawn", 0, 0); var n = Math.min(3, 1 + Math.floor(seg(u, a + .3, LE("S4", 0)) * 2.99)); chr("stand", 90, 327);
  if (u > LN("S4", 0) + 2) chr(blinkAt(u, .6) ? "olook" : "ostand", 170, 327, true);
  counter(48, 196, "OUT LOUD", "" + n, "#B8F5C8", 3);
  if (u > LN("S4", 1)) { bubble(116, 266, 76, 16, 120); ptext(L, "UMM... WAIT.", 120, 271, 1, "#1A1530"); }
  return camAt([[a, 140, 270, 1.35], [b, 140, 272, 1.4, b - a]], u);
}
// S5: back on stage, it comes out (loops to the stage)
function sEnd(u, a, b) { stage(u); chr("stand", 120, 307); bubble(150, 246, 74, 16, 150); ptext(L, "SO, HERE'S", 156, 251, 1, "#1A1530"); return camAt([[a, 140, 310, 1.9], [b, 140, 310, 1.9]], u); }

var SCENES = [["S1", sRead], ["S2", sStage], ["S3", sSkills], ["S4", sRehearse], ["S5", sEnd]];
var EP = {
  badge: "KABIR VS. KABIR #10", hook: "READ HIS SPEECH 20 TIMES. *IN HIS HEAD.*", hookEnd: LN("S1", 1) + .5,
  endAt: function () { return LN("S5", 1); }, endQ: "WHEN'S YOUR *NEXT ONE?*",
  titles: [["HIS MOUTH HAD *NEVER MET* THE WORDS.", LN("S2", 1), SCN.S2[1], 300, 8],
           ["SEND TO THE FRIEND READING SLIDES *ON THE TRAIN.*", LN("S5", 0), LN("S5", 1), 300, 7]]
};
