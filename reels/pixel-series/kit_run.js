// =================== pixel-series runtime: needs EP + SCENES from the episode file ===================
var SC = SCENES.map(function (s, i) { var sp = SCN[s[0]]; return { a: i === 0 ? 0 : sp[0], b: sp[1], f: s[1], k: s[0] }; });
function renderTo(e, u, ctx) { L.setTransform(1, 0, 0, 1, 0, 0); L.clearRect(0, 0, W, H); var cam = e.f(u, e.a, e.b); ctx.save(); blit(cam, 0, 0, OW, OH, ctx); ctx.restore(); }
function popTrans(u, prev, next, k) {
  X.fillStyle = "#0B0920"; X.fillRect(0, 0, OW, OH);
  if (k < .4) { var q = eio(k / .4), sc = 1 - .14 * q; renderTo(prev, Math.min(u, prev.b - .001), OA[1]);
    X.save(); X.globalAlpha = 1 - .5 * q; X.drawImage(OA[0], Math.round(OW * (1 - sc) / 2), Math.round(OH * (1 - sc) / 2), Math.round(OW * sc), Math.round(OH * sc)); X.restore(); }
  else { var r = (k - .4) / .6, sc2 = r < .6 ? lerp(.82, 1.04, eout(r / .6)) : lerp(1.04, 1, eio((r - .6) / .4)); renderTo(next, Math.max(u, next.a), OB[1]);
    X.drawImage(OB[0], Math.round(OW * (1 - sc2) / 2), Math.round(OH * (1 - sc2) / 2), Math.round(OW * sc2), Math.round(OH * sc2)); }
}
function render(u) {
  X.setTransform(1, 0, 0, 1, 0, 0); X.imageSmoothingEnabled = false; X.globalAlpha = 1; X.filter = "none";
  var i = 0; while (i < SC.length - 1 && u >= SC[i + 1].a) i++;
  var cur = SC[i], nxt = SC[i + 1], noPop = EP.noPop || [];
  if (nxt && u > nxt.a - .25 && noPop.indexOf(nxt.k) < 0) popTrans(u, cur, nxt, seg(u, nxt.a - .25, nxt.a + .2));
  else if (i > 0 && u < cur.a + .2 && noPop.indexOf(cur.k) < 0) popTrans(u, SC[i - 1], cur, seg(u, cur.a - .25, cur.a + .2));
  else renderTo(cur, u, X);
  overlays(u);
}
function badge(u) { var s = EP.badge, B = 4, w = pwidth(s, B); X.fillStyle = "#1A1530"; X.fillRect(48, 96, w + 40, 52); X.fillStyle = EP.badgeBg || "#FFC145"; X.fillRect(52, 100, w + 32, 44); ptext(X, s, 68, 112, B, EP.badgeFg || "#1A1530"); }
function overlays(u) {
  var endAt = EP.endAt();
  if (u < endAt) badge(u);
  caption(u + 3, EP.hook, 0, EP.hookEnd + 3, { y: 300, b: 9 });
  (EP.titles || []).forEach(function (c) { caption(u, c[0], c[1], c[2], { y: c[3] || 300, b: c[4] || 9 }); });
  if (EP.extra) EP.extra(u);
  if (u > endAt) { var k = seg(u, endAt, endAt + .5); X.globalAlpha = .6 * k; X.fillStyle = "#140F2E"; X.fillRect(0, 0, OW, OH); X.globalAlpha = 1;
    caption(u, EP.endQ, endAt, 999, { y: 560 });
    if (u > endAt + .3) { var lab = "DMYOR", B = 20, w2 = pwidth(lab, B); ptext(X, lab, (OW - w2) / 2 + B, 1080 + B, B, "#1A1530"); ptext(X, lab, (OW - w2) / 2, 1080, B, "#FFFFFF");
      var h = "@BECAUSEIDMYOR", w3 = pwidth(h, 7); ptext(X, h, (OW - w3) / 2, 1280, 7, "#FFC145"); } }
  else TL.subs.forEach(function (c) { if (u >= c[0] && u < c[1]) caption(u, c[2], c[0], c[1], { y: 1650, b: 7, accent: "#FFFFFF" }); });
}
window.__duration = DUR;
window.__seek = function (u) { return READY.then(function () { render(u); }); };
READY.then(function () { render(0); });
