/* dmyor reel engine. Everything renders as a pure function of time from TL,
   so the recorder can seek frame by frame and the output is deterministic.
   The cursor path is DERIVED from the scenes: each scene says where the pointer
   must be and when, and the engine inserts arrive-then-hold waypoints. That is
   what keeps the pointer from snapping or drifting. */
(function () {
"use strict";
var TOTAL = TL.total, W = 1080, H = 1920;
var stage = document.getElementById("stage"), sc = 1;
function fit(){ sc = Math.min(innerWidth/W, innerHeight/H); stage.style.transform = "scale("+sc+")"; }
fit(); addEventListener("resize", fit);
var cl=function(x){return x<0?0:(x>1?1:x)}, seg=function(t,a,b){return b<=a?(t>=b?1:0):cl((t-a)/(b-a))};
var eio=function(x){return x<.5?4*x*x*x:1-Math.pow(-2*x+2,3)/2}, eo=function(x){return 1-Math.pow(1-x,3)};
function fade(el,o){ if(el) el.style.opacity=o; }
function rectOf(el){var s=stage.getBoundingClientRect(),r=el.getBoundingClientRect();
 return{left:(r.left-s.left)/sc,top:(r.top-s.top)/sc,width:r.width/sc,height:r.height/sc};}

// ---- scene lookup ----
function S(type){ for(var i=0;i<TL.scenes.length;i++) if(TL.scenes[i].type===type) return TL.scenes[i]; return null; }
function ALL(type){ return TL.scenes.filter(function(x){return x.type===type;}); }
function has(type){ return !!S(type); }

// ================= diary geometry =================
var CS=460/1080, PX=540, PY=960-1920*CS/2, INSET=46*CS, PW=988*CS, PH=1828*CS;
var PTOP=PY+INSET, FLIP_W=INSET+PW, COVER_W=FLIP_W+12, COVER_H=PH+20, COVER_TOP=PTOP-10, PAGE_L=PX+INSET;
var diary=document.getElementById("diaryPage");
diary.style.cssText+=";left:"+PAGE_L+"px;top:"+PTOP+"px;width:"+PW+"px;height:"+PH+"px";
var spine=document.getElementById("spine");
spine.style.cssText+=";left:"+PX+"px;top:"+PTOP+"px;height:"+PH+"px";
var bookBase=document.getElementById("bookBase");
for(var e=0;e<4;e++){var eg=document.createElement("div");eg.className="edge";
 eg.style.cssText="left:"+(PAGE_L+PW+2+e*2.5)+"px;top:"+(PTOP+6+e*2)+"px;height:"+(PH-12-e*4)+"px;opacity:"+(1-e*.18);
 bookBase.appendChild(eg);}
var cover=document.getElementById("cover");
cover.style.cssText+=";left:"+PX+"px;top:"+COVER_TOP+"px;width:"+COVER_W+"px;height:"+COVER_H+"px";
var coverShade=document.getElementById("coverShade"), bookWorld=document.getElementById("bookWorld");
function ghostGrid(c0,x0,y0,w,h,seed){var GH=[58,70,54,65,76,56,68,61,73,52,64,71,57,67],pad=14,gap=11,cols=3;
 var cw=(w-pad*2-gap*(cols-1))/cols,stg=[0,25,11];
 for(var c=0;c<cols;c++){var y=y0+pad+stg[(c+seed)%3];
  for(var k=0;;k++){var hh=GH[(k+seed*3+c)%GH.length]; if(y+hh>y0+h-pad)break;
   var g=document.createElement("div");g.className="ghostCard";
   g.style.cssText="left:"+(x0+pad+c*(cw+gap))+"px;width:"+cw+"px;top:"+y+"px;height:"+hh+"px";
   c0.appendChild(g);y+=hh+gap;}}}
ghostGrid(document.querySelector(".coverInner"),INSET-4,10,PW,PH,2);

var writeSc=S("diary.write")||{lines:[]};
var LINES_TXT=(writeSc.lines||[]).map(function(l){return l.text;});
var L_TOP=104,L_GAP=74,L_X=34,CHAR_W=12.4;
for(var i=0;i<8;i++){var r=document.createElement("div");r.className="rule";
 r.style.cssText="left:"+L_X+"px;width:"+(PW-L_X*2)+"px;top:"+(L_TOP+i*L_GAP+34)+"px";diary.appendChild(r);}
var dstampEl=null;
if(writeSc.stamp){ dstampEl=document.createElement("div"); dstampEl.className="written";
 dstampEl.style.cssText="left:"+L_X+"px;font-size:15px;color:#8C8C86;letter-spacing:2px;opacity:0";
 diary.appendChild(dstampEl); }
var lines=LINES_TXT.map(function(txt,i){var d=document.createElement("div");d.className="written";
 d.style.cssText="left:"+L_X+"px;top:"+(L_TOP+i*L_GAP)+"px";
 d.innerHTML='<span class="t"></span><span class="caret">|</span>';diary.appendChild(d);
 return{el:d,txt:d.querySelector(".t"),caret:d.querySelector(".caret"),
   absY:PTOP+L_TOP+i*L_GAP,absX:PAGE_L+L_X};});
function capStart(i){return lines[i].absX+6;}
function capEnd(i){return lines[i].absX+LINES_TXT[i].length*CHAR_W+6;}
function tapX(){return PAGE_L+L_X+150;}

// ================= archive =================
var DREAMS=TL.dreams&&TL.dreams.length?TL.dreams:["Write something real"];
var YRS=["2027","2028","2029","2030","2031","2032","2033","2035"];
var NC=3,PC=14,COUNT=NC*PC,RH=[136,164,128,152,178,132,158,142,170,126,148,166,134,156],CST=[0,58,26];
function ci(c,r){return c*PC+r;}
function block(){var row=document.createElement("div");
 row.style.cssText="display:flex;justify-content:center;gap:30px;width:988px";var cols=[];
 for(var c=0;c<NC;c++){var w=document.createElement("div");w.className="colWrap";
  var col=document.createElement("div");col.className="col";col.style.transform="translateY("+CST[c]+"px)";
  w.appendChild(col);row.appendChild(w);cols.push(col);}
 for(var c2=0;c2<NC;c2++)for(var r=0;r<PC;r++){var idx=ci(c2,r);
  var card=document.createElement("div");card.className="card";card.dataset.idx=idx;
  card.style.height=RH[r%RH.length]+"px";
  var inner=document.createElement("div");inner.className="cardInner";
  inner.innerHTML='<div class="dream">'+DREAMS[idx%DREAMS.length]+'</div><div class="meta"><span class="date">'
   +YRS[idx%YRS.length]+'</span><span class="standby">standby</span></div>';
  card.appendChild(inner);cols[c2].appendChild(card);} return row;}
var gi=document.getElementById("gridInner"),bA=block(),bB=block();
var ld=document.createElement("div");ld.style.height="34px";
var gp=document.createElement("div");gp.style.height="30px";
gi.appendChild(ld);gi.appendChild(bA);gi.appendChild(gp);gi.appendChild(bB);
var inA={},inB={},slotA={};
bA.querySelectorAll(".card").forEach(function(c){slotA[c.dataset.idx]=c;inA[c.dataset.idx]=c.querySelector(".cardInner");});
bB.querySelectorAll(".card").forEach(function(c){inB[c.dataset.idx]=c.querySelector(".cardInner");});
var loopD=0, canvasWrap=document.getElementById("canvasWrap"), gridLayer=document.getElementById("gridLayer");
var hoverRing=document.getElementById("hoverRing");
var FLIPS=ALL("archive.flip").map(function(f){var idx=ci(f.card[0],f.card[1]);
 return{idx:idx,t:f.at,y:f.year||"2030",a:inA[idx].querySelector(".standby"),b:inB[idx].querySelector(".standby")};});

// ================= calendar + progress log =================
var MON=["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"];
var calSc=S("calendar.year"), calCells=[];
var calEl=document.getElementById("calendar"), calRing=document.getElementById("calRing");
if(calSc){ var yr=calSc.year||"2026";
 MON.forEach(function(m,i){ var c=document.createElement("div"); c.className="mcell";
  c.innerHTML='<div class="mn">'+m+'</div><div class="my">'+yr+'</div><div class="mstrike"></div>';
  calEl.appendChild(c); calCells.push({el:c,strike:c.querySelector(".mstrike")}); }); }
var plogSc=S("progress.log"), plogMarks=[];
var plogEl=document.getElementById("plog"), plogGrid=document.getElementById("plogGrid"),
    plogNum=document.getElementById("plogNum");
if(plogSc){ var n=plogSc.count||36;
 for(var pi=0;pi<n;pi++){ var dm=document.createElement("div"); dm.className="dmark";
  plogGrid.appendChild(dm); plogMarks.push(dm); } }

// ================= a record with fields that were never filled ==============
var recSc=S("record.blank");
var recEl=document.getElementById("record"), recRows=[0,1,2].map(function(i){
  var el=document.getElementById("rr"+i); return {el:el, k:el.querySelector(".rk"), v:el.querySelector(".rv")}; });
if(recSc){ document.getElementById("recTitle").textContent=recSc.dream||"";
  document.getElementById("recDate").textContent=recSc.sub||"";
  (recSc.fields||[]).forEach(function(f,i){ if(recRows[i]) recRows[i].k.textContent=f.label; }); }

// ================= the wrong culprits, crossed off =================
var cuSc=S("strike.words");
var culpEl=document.getElementById("culprits"), cuEls=[0,1].map(function(i){
 var el=document.getElementById("cu"+i); return {el:el, t:el.querySelector("span"), x:el.querySelector(".cx")}; });
if(cuSc) (cuSc.words||[]).forEach(function(w,i){ if(cuEls[i]) cuEls[i].t.textContent=w; });

// ================= a dated ledger accumulating =================
var lgSc=S("ledger.rows"), lgEls=[];
var ledgerEl=document.getElementById("ledger"), ledgerRows=document.getElementById("ledgerRows"),
    ledgerNum=document.getElementById("ledgerNum");
if(lgSc){ (lgSc.entries||[]).forEach(function(e,i){
  var r=document.createElement("div"); r.className="lrow"+(e.missed?" miss":"");
  r.innerHTML='<span class="lt">'+e.text+'</span><span class="ld">'+e.date+'</span>';
  ledgerRows.appendChild(r); lgEls.push(r); }); }

// ================= everyone's records, streaming =================
var fdSc=S("feed.stream"), fdCols=[], fdRows=[];
var feedEl=document.getElementById("feed"), feedRing=document.getElementById("feedRing");
var fnEls=[document.getElementById("fn0"),document.getElementById("fn1")];
if(fdSc){ var NCOL=2, per=9;
 for(var c=0;c<NCOL;c++){ var col=document.createElement("div"); col.className="fcol";
  col.style.left=(c*512)+"px"; feedEl.appendChild(col); fdCols.push(col);
  // two identical sets per column so the stream can loop without ever emptying
  for(var r2=0;r2<per*3;r2++){ var idx=c*per+(r2%per);
   var row=document.createElement("div"); row.className="frow";
   var dr=DREAMS[idx%DREAMS.length], yr=YRS[idx%YRS.length];
   row.innerHTML='<div class="ft">'+dr+'</div><div class="fm"><span>'+yr+'</span><span class="fs">standby</span></div>';
   col.appendChild(row); fdRows.push({el:row, st:row.querySelector(".fs"), col:c}); } } }
var fhSc=S("feed.highlight"), frSc=S("feed.real"), fhPick=null;
// distance travelled, integrated in fixed steps: pausing must not teleport the stream
function fdTravel(t,spd,holdNow){
  if(!fdSc) return 0;
  var dt=1/30, acc=0;
  for(var u=fdSc.in; u<t; u+=dt){
    var h=fhSc?seg(u,fhSc.at-0.5,fhSc.at)*(1-seg(u,fhSc.out,fhSc.out+0.5)):0;
    acc += spd*(1-0.94*h)*dt;
  }
  return acc;
}

// ================= two phases, one live =================
var pbSc=S("phases.bar");
var phbarEl=document.getElementById("phbar"), phNote=document.getElementById("phNote");
var phSegs=[document.getElementById("ph0"),document.getElementById("ph1")];
var phFills=phSegs.map(function(e){return e.querySelector(".phfill");});

// ================= three things =================
var st3Sc=S("steps.three");
var steps3El=document.getElementById("steps3"),
    s3Els=["s3a","s3b","s3c"].map(function(id){return document.getElementById(id);});
if(st3Sc) (st3Sc.items||[]).forEach(function(it,i){ if(s3Els[i]) s3Els[i].querySelector("span").textContent=it; });

// ================= vague -> specific =================
var shSc=S("sharpen.text");
var sharpenEl=document.getElementById("sharpen"), shOld=document.getElementById("shOld"),
    shNew=document.getElementById("shNew");
if(shSc){ shOld.textContent=shSc.vague||""; }

// ================= everything collapsing to one action =================
var clSc=S("collapse.step");
var collapseEl=document.getElementById("collapse"), clBig=document.getElementById("clBig"),
    clSmall=document.getElementById("clSmall");
if(clSc){ clBig.textContent=clSc.big||""; clSmall.textContent=clSc.small||""; }

// ================= orbit: ideas circling a point they never leave =================
var orbSc=S("orbit.trapped"), orbEls=[];
var orbEl=document.getElementById("orbit"), orbCore=document.getElementById("orbitCore");
if(orbSc){ (orbSc.items||[]).forEach(function(it,i){
  var d=document.createElement("div"); d.className="orb";
  d.innerHTML='<span class="ot">'+it+'</span><span class="obr">[  -  -  ]</span>';
  orbEl.appendChild(d); orbEls.push({el:d, txt:d.querySelector(".ot"), br:d.querySelector(".obr"), raw:it}); }); }

// ================= recall: what you meant to do, rising out of a spent month ======
var rcSc=S("calendar.recall"), rcEls=[];
var rcEl=document.getElementById("recall");
if(rcSc){ (rcSc.items||[]).forEach(function(it,i){
  var d=document.createElement("div"); d.className="rgh"; d.textContent=it;
  rcEl.appendChild(d);
  // one at a time, clear above the grid: recalling, not annotating
  rcEls.push({el:d, x:540, y:436 + (i%2)*54}); }); }

// ================= thoughts / tally / streak / stamps / path =================
var thSc=S("thoughts.float"), thEls=[];
var thEl=document.getElementById("thoughts");
if(thSc){ (thSc.items||[]).forEach(function(it,i){
  var d=document.createElement("div"); d.className="thought";
  d.innerHTML=it+(thSc.showNoDate?'<span class="nd">no date</span>':'');
  thEl.appendChild(d);
  // spread them loosely; each drifts on its own phase so nothing sits still
  var col=i%2, row=(i/2)|0;
  thEls.push({el:d, bx:190+col*520, by:640+row*190, ph:i*1.7, dir:(i%2?1:-1)}); }); }

var tlySc=S("tally.compare");
var tPlan=document.getElementById("tPlan"), tDone=document.getElementById("tDone"),
    tallyEl=document.getElementById("tally");

var stkSc=S("streak.bars"), stkBars=[];
var streakEl=document.getElementById("streak"), streakBarsEl=document.getElementById("streakBars"),
    streakNum=document.getElementById("streakNum");
if(stkSc){ var H2=[38,52,44,66,58,74,68,86,79,94,88,100,96,100];
 for(var bi=0;bi<H2.length;bi++){ var bar=document.createElement("div"); bar.className="sbar";
  streakBarsEl.appendChild(bar); stkBars.push({el:bar,h:H2[bi]}); } }

var stmSc=S("stamp.trio");
var stampsEl=document.getElementById("stamps"),
    stmpEls=[0,1,2].map(function(i){return document.getElementById("stmp"+i);});
if(stmSc&&stmSc.words) stmSc.words.forEach(function(w,i){ if(stmpEls[i]) stmpEls[i].textContent=w; });

var pathSc=S("path.arc");
var pathSvg=document.getElementById("pathSvg"), pArc=document.getElementById("pArc"),
    pB=document.getElementById("pB"), pDot=document.getElementById("pDot");
var pArcLen=pArc.getTotalLength(); pArc.style.strokeDasharray=pArcLen;

// ================= ui refs =================
var R=function(id){return document.getElementById(id);};
var tab1=R("tab1"),tab2=R("tab2"),panel=R("panel"),panelNo=R("panelNo"),panelTitle=R("panelTitle"),panelBody=R("panelBody");
var stepEls=[R("st0"),R("st1"),R("st2")];
var addBtn=R("addBtn"),compose=R("compose"),field=R("field"),fieldText=R("fieldText"),fieldCaret=R("fieldCaret");
var postBtn=R("postBtn"),flyCard=R("flyCard"),scanEl=R("scan"),promptEl=R("prompt"),promptCaret=R("promptCaret");
var counter=R("counter"),countNum=R("countNum"),ghost=R("ghostDiary"),ghostSlash=R("ghostSlash");
var tlSvg=R("tl"),tlPath=R("tlPath"),tlA=R("tlA"),tlB=R("tlB"),tlLabA=R("tlLabA"),tlLabB=R("tlLabB");
var cursorEl=R("cursor"),rippleEl=R("ripple"),pulseEl=R("pulse");
var tlLen=tlPath.getTotalLength(); tlPath.style.strokeDasharray=tlLen;
var tlSc=S("timeline.draw"); if(tlSc){ tlLabA.textContent=tlSc.from||"2026"; tlLabB.textContent=tlSc.to||"2031"; }
var tabsSc=S("phase.tabs");
if(tabsSc&&tabsSc.labels){ tab1.textContent=tabsSc.labels[0]; tab2.textContent=tabsSc.labels[1]; }
var stepsSc=S("phase.steps");
if(stepsSc) (stepsSc.steps||[]).forEach(function(s,i){ if(stepEls[i]) stepEls[i].querySelector("span").textContent=s; });
var composeType=S("compose.type")||{text:""};

// ================= captions =================
var textLayer=R("textLayer"), showText=false;
var BEATS=TL.captions||[];
var beatEls=BEATS.map(function(b){var el=document.createElement("div");
 el.className="beat"+(b.final?" final":"");
 var l1=document.createElement("div");l1.className="line1";l1.textContent=b.l1;
 l1.style.fontSize=(b.size||46)+"px";el.appendChild(l1);
 if(b.l2){var l2=document.createElement("div");l2.className="line2";l2.textContent=b.l2;el.appendChild(l2);}
 textLayer.appendChild(el);return el;});
var endSc=S("end.card");
var finalIdx=BEATS.map(function(b,i){return b.final?i:-1;}).filter(function(i){return i>=0;})[0];
var finalL2=(finalIdx!=null&&beatEls[finalIdx])?beatEls[finalIdx].querySelector(".line2"):null;
var URL_TXT=(TL.brand&&TL.brand.url)||"";
function placeBeats(){beatEls.forEach(function(el,i){var h=el.getBoundingClientRect().height/sc;
 el.style.top=((BEATS[i].y||250)-h/2)+"px";});}

// ================= derived cursor path =================
// Scenes declare where the pointer must be; the engine inserts the travel and the hold.
var TARGETS=[], CLICKS=[], PULSES=[], TYPEWIN=[];
function tgt(t,x,y,pin){ if(x!=null&&y!=null&&isFinite(t)) TARGETS.push({t:t,x:x,y:y,pin:!!pin}); }
// a "park here until something happens" target: dropped if the next beat is close
function rest(t,x,y){ if(isFinite(t)) TARGETS.push({t:t,x:x,y:y,rest:true}); }
function clk(t,x,y){ if(x!=null&&y!=null&&isFinite(t)) CLICKS.push({t:t,x:x,y:y}); }
var REST={x:905,y:1585}, REST2={x:900,y:1520};
var LATE=null; // filled after layout for measured targets

function buildSchedule(){
  var s;
  if((s=S("diary.open"))){ tgt(s.click,556,966); clk(s.click,556,966); rest(s.end+0.5,REST.x,REST.y); }
  (writeSc.lines||[]).forEach(function(l,i){
    TYPEWIN.push({s:l.start,e:l.end,line:i});
    tgt(l.start,capStart(i),lines[i].absY+30,true); tgt(l.end,capEnd(i),lines[i].absY+30,true); });
  if((s=S("diary.tap"))) (s.at||[]).forEach(function(t,i){
    var row=(s.rows&&s.rows[i]!=null)?s.rows[i]:i;      // which ruled line, not which written line
    var y=PTOP+L_TOP+row*L_GAP+16;
    tgt(t-0.25,tapX(),y); clk(t,tapX(),y); PULSES.push({t:t,x:tapX(),y:y}); });
  if((s=S("diary.close"))){ tgt(s.click,560,966); clk(s.click,560,966); }
  if((s=S("calendar.year"))){
    if(s.point!=null) tgt(s.point, 290, 700);
    if(s.sweep) { tgt(s.sweep[0], 290, 700); tgt(s.sweep[1], 800, 1180); } }
  if((s=S("record.blank"))&&s.fields) s.fields.forEach(function(f){ tgt(f.at+0.2, 800, 760+ (s.fields.indexOf(f))*96); });
  if((s=S("record.blank"))&&s.fields) s.fields.forEach(function(f,i){
    if(f.fillAt!=null) tgt(f.fillAt-0.15, 700, 760+i*96); });
  if((s=S("ledger.rows"))) tgt((s.rowStart!=null?s.rowStart:s.in)-0.25, 300, 790);
  if((s=S("feed.highlight"))) tgt(s.at-0.3, 700, 900);
  if((s=S("phases.bar"))) tgt((s.fill0!=null?s.fill0:s.in)-0.2, 380, 1230);
  if((s=S("steps.three"))&&s.at) s.at.forEach(function(a4,i){ tgt(a4-0.15, 250, 430+i*62); });
  if((s=S("strike.words"))&&s.at) s.at.forEach(function(a6,i){ tgt(a6-0.2, 420+i*260, 1430); });
  if((s=S("sharpen.text"))){ if(s.vagueAt!=null) tgt(s.vagueAt, 430, 1010); tgt(s.at-0.2, 470, 1070); }
  if((s=S("collapse.step"))) tgt(s.at+0.9, 560, 1120);
  if((s=S("orbit.trapped"))){
    tgt(s.in+0.7, 540, (s.cy||900)-((s.ry||205)+90));
    if(s.brackets!=null) tgt(s.brackets+0.5, 540+(s.rx||330)*0.72, (s.cy||900)+40);
    if(s.scramble!=null) tgt(s.scramble+0.6, 540-(s.rx||330)*0.6, (s.cy||900)-60); }
  if((s=S("calendar.recall"))&&s.at&&s.at.length){
    tgt(s.at[0]-0.2, 274, 700); tgt(s.at[s.at.length-1], 806, 1040); }
  if((s=S("tally.compare"))) tgt(s.in+0.9, 700, 900);
  if((s=S("thoughts.float"))) { tgt(s.in+0.8, 620, 720); tgt(s.dissolve!=null?s.dissolve-0.3:s.out-0.5, 460, 980); }
  if((s=S("streak.bars"))) tgt(s.growStart!=null?s.growStart-0.3:s.in, 300, 1290);
  if((s=S("stamp.trio"))) tgt(s.at&&s.at.length?s.at[0]-0.3:s.in, 420, 1245);
  if((s=S("path.arc"))) { tgt(s.start, 230, 1150); tgt(s.end, 850, 1150); }
  if((s=S("progress.log"))) tgt(s.fillStart!=null?s.fillStart-0.3:s.in, 300, 1000);
  if((s=S("archive.zoom"))){ tgt(s.start-0.05,540,960); clk(s.start,540,960); rest(s.end+0.6,REST.x,REST.y); }
  if((s=S("archive.hover"))) { tgt(s.start,"HOVER","HOVER"); tgt(s.end,"HOVER","HOVER"); }
  if((s=S("archive.drag"))) { tgt(s.start,880,1190); tgt(s.end,880,790); rest(s.end+0.7,REST2.x,REST2.y); }
  if((s=S("timeline.draw"))){ tgt(s.start-0.1,250,1050); tgt(s.end,830,1050); }
  if((s=S("diary.ghost"))){ tgt(s.in+0.6,430,960); tgt(s.strike!=null?s.strike+0.8:s.in+1.7,650,960); }
  ALL("phase.select").forEach(function(p){ var x=p.index===0?335:745; tgt(p.at-0.05,x,592); clk(p.at,x,592); });
  if((s=S("compose.open"))){ tgt(s.clickAt-0.1,"ADD","ADD"); clk(s.clickAt,"ADD","ADD"); }
  if((s=S("compose.type"))){ tgt(s.start-0.4,"FIELD","FIELD"); tgt(s.start,"FIELD","FIELD",true); tgt(s.end,"FIELDEND","FIELDEND",true); }
  if((s=S("compose.post"))){ tgt(s.clickAt-0.15,"POST","POST"); clk(s.clickAt,"POST","POST"); rest(s.flyEnd+0.6,REST2.x,REST2.y); }
  if((s=S("archive.scan"))) rest(s.start-0.3,REST2.x,REST2.y);
  if((s=S("prompt.turn"))){ tgt(s.clickAt!=null?s.clickAt-0.5:s.in+0.6,300,1180);
    if(s.clickAt!=null) clk(s.clickAt,300,1180); tgt(s.out-0.6,300,1180); }
  ALL("archive.drag2").forEach(function(d){ tgt(d.start,880,1190); tgt(d.end,880,790); });
  if(endSc){ tgt(endSc.in+0.4,540,1010); clk(endSc.in+0.5,540,1010); tgt(TOTAL,540,1010); }
}

var PATH=[];
function resolveTargets(){
  var HOVER_RECT=null, FIELD_RECT=null, POST_RECT=null, ADD_RECT=null;
  var hv=S("archive.hover");
  var hidx=hv?ci(hv.card[0],hv.card[1]):ci(0,3);
  inA[hidx].style.opacity=1; HOVER_RECT=rectOf(slotA[hidx]); inA[hidx].style.opacity=0;
  compose.style.opacity=1; FIELD_RECT=rectOf(field); POST_RECT=rectOf(postBtn); compose.style.opacity=0;
  addBtn.style.opacity=1; ADD_RECT=rectOf(addBtn); addBtn.style.opacity=0;
  var fy=FIELD_RECT.top+FIELD_RECT.height/2+16;
  var M={ HOVER:{x:HOVER_RECT.left+HOVER_RECT.width-46,y:HOVER_RECT.top+HOVER_RECT.height/2},
    FIELD:{x:FIELD_RECT.left+22,y:fy},
    FIELDEND:{x:FIELD_RECT.left+22+(composeType.text||"").length*13.2,y:fy},
    POST:{x:POST_RECT.left+POST_RECT.width/2,y:POST_RECT.top+POST_RECT.height/2+14},
    ADD:{x:ADD_RECT.left+ADD_RECT.width/2,y:ADD_RECT.top+ADD_RECT.height/2+14} };
  [TARGETS,CLICKS].forEach(function(L){ L.forEach(function(p){
    if(typeof p.x==="string"&&M[p.x]){ var m=M[p.x]; p.x=m.x; p.y=m.y; } }); });
  LATE={HOVER_RECT:HOVER_RECT,FIELD_RECT:FIELD_RECT};
  TARGETS.sort(function(a,b){return a.t-b.t;});
  // Two scenes can each want the pointer somewhere within a few frames of each other,
  // which forces an impossible sprint. When that happens the later target wins: it is
  // the one with the click on it. This is why hops stay smooth without hand-tuning.
  var keep=[];
  for(var q=0;q<TARGETS.length;q++){
    var a1=TARGETS[q], b1=TARGETS[q+1];
    if(a1.rest && b1 && b1.t-a1.t < 1.5) continue;   // do not park if the next beat is imminent
    if(!a1.pin && b1 && !b1.pin && b1.t-a1.t < 0.28 && Math.hypot(b1.x-a1.x,b1.y-a1.y) > 150) continue;
    if(!a1.pin && b1 && b1.pin && b1.t-a1.t < 0.28 && Math.hypot(b1.x-a1.x,b1.y-a1.y) > 150) continue;
    keep.push(a1);
  }
  TARGETS=keep;
  // arrive-then-hold: travel scaled by distance, so nothing crawls and nothing whips
  var cur={x:1010,y:1770}; PATH=[{t:0,x:cur.x,y:cur.y}];
  TARGETS.forEach(function(g){
    var d=Math.hypot(g.x-cur.x,g.y-cur.y);
    if(d<1){ PATH.push({t:g.t,x:g.x,y:g.y}); cur=g; return; }
    var trav=Math.max(0.42,Math.min(1.05,d/1250));
    var dep=g.t-trav, last=PATH[PATH.length-1];
    if(dep>last.t+0.02) PATH.push({t:dep,x:cur.x,y:cur.y});
    PATH.push({t:g.t,x:g.x,y:g.y}); cur={x:g.x,y:g.y};
  });
  PATH.push({t:TOTAL,x:cur.x,y:cur.y});
  PATH.sort(function(a,b){return a.t-b.t;});
}
function pathAt(t){ if(t<=PATH[0].t)return PATH[0];
 for(var i=0;i<PATH.length-1;i++){var a=PATH[i],b=PATH[i+1];
  if(t>=a.t&&t<=b.t){ if(b.t-a.t<1e-6) return b; var k=eio((t-a.t)/(b.t-a.t));
   return{x:a.x+(b.x-a.x)*k,y:a.y+(b.y-a.y)*k};}}
 return PATH[PATH.length-1];}

// ================= render =================
function render(t){
 t=Math.max(0,Math.min(TOTAL,t));
 var s, capOverGrid=0;
 for(var i=0;i<BEATS.length;i++){var b=BEATS[i],op=0;
  if(b.final){ if(t>=b.s) op=cl((t-b.s)/0.7); }
  else if(t>=b.s&&t<b.e) op=cl(Math.min((t-b.s)/0.7,(b.e-t)/0.5));
  var vis=(b.final||showText)?op:0; fade(beatEls[i],vis);
  if(vis&&!b.final&&vis>capOverGrid) capOverGrid=vis;}
 if(finalL2&&endSc){var us=endSc.urlStart!=null?endSc.urlStart:endSc.in,
   ue=endSc.urlEnd!=null?endSc.urlEnd:endSc.in+2;
  var un=Math.floor(cl((t-us)/Math.max(0.1,ue-us))*URL_TXT.length);
  finalL2.textContent=t<us?"":URL_TXT.slice(0,un);}

 // diary
 var o=S("diary.open"), c=S("diary.close");
 var openE=o?eio(seg(t,o.start,o.end)):0, closeE=c?eio(seg(t,c.start,c.end)):0;
 var ang=-179*openE+179*closeE;
 cover.style.transform="rotateY("+ang+"deg)";
 coverShade.style.opacity=Math.sin(Math.abs(ang)*Math.PI/180)*.5;
 var zoom=S("archive.zoom");
 var bookVis=o?seg(t,Math.max(0,o.click-0.7),o.click)*(zoom?(1-seg(t,zoom.start,zoom.start+1.5)):1):0;
 fade(bookWorld,bookVis);
 bookWorld.style.transform="translateX("+(-(COVER_W/2)*(1-openE+closeE))+"px) rotateX("+(5*openE*(1-closeE))+"deg)";
 var sv=cl((openE-.45)*3)*(1-cl(closeE*2.2)); fade(bookBase,sv); fade(spine,sv);
 fade(diary,cl(openE*2.2)*(1-cl((closeE-.55)*3)));
 var dis=S("diary.dissolve"), gone=dis?seg(t,dis.start,dis.end):0;
 for(var w=0;w<lines.length;w++){var L=lines[w],tw=(writeSc.lines||[])[w];
  if(!tw)continue; var full=LINES_TXT[w];
  var n=Math.floor(cl((t-tw.start)/Math.max(0.1,tw.end-tw.start))*full.length);
  L.txt.textContent=full.slice(0,n);
  L.caret.style.opacity=(t>=tw.start&&t<tw.end)?1:0;
  fade(L.el,(t>=tw.start?1:0)*(1-gone));}
 if(dstampEl&&writeSc.stamp){ var stp=writeSc.stamp, sAt=stp.at!=null?stp.at:0;
  var sn=Math.floor(cl((t-sAt)/0.9)*(stp.text||"").length);
  dstampEl.textContent=(stp.text||"").slice(0,sn);
  dstampEl.style.top=((writeSc.lines[0]?L_TOP+32:L_TOP+32))+"px";
  fade(dstampEl, seg(t,sAt,sAt+0.25)*(1-gone)); }

 // the diary returning, struck out
 if((s=S("diary.ghost"))){ fade(ghost,seg(t,s.in,s.in+0.5)*(1-seg(t,s.out-0.6,s.out)));
  var stk=s.strike!=null?s.strike:s.in+0.9;
  ghostSlash.style.transform="scaleX("+eio(seg(t,stk,stk+0.8))+")"; } else fade(ghost,0);

 // timeline rule
 if(tlSc){ var tv=seg(t,tlSc.in,tlSc.in+0.6)*(1-seg(t,tlSc.out,tlSc.out+0.7));
  fade(tlSvg,tv); tlPath.style.strokeDashoffset=tlLen*(1-eio(seg(t,tlSc.start,tlSc.end)));
  tlA.style.opacity=seg(t,tlSc.start,tlSc.start+.3); tlB.style.opacity=seg(t,tlSc.end-.2,tlSc.end+.2);
  fade(tlLabA,tv*seg(t,tlSc.start+.2,tlSc.start+.8)); fade(tlLabB,tv*seg(t,tlSc.end-.1,tlSc.end+.5)); }

 // archive
 var zp=zoom?eio(seg(t,zoom.start,zoom.end)):0, s0=COVER_W/1080, ss=s0+(1-s0)*zp;
 var pb=S("archive.pullback"), pull=pb?eio(seg(t,pb.start,pb.end))*(1-(pb.back!=null?seg(t,pb.back,pb.back+1.5):0)):0;
 var kk=1-0.085*pull, x0=PX-COVER_W/2, y0=COVER_TOP;
 canvasWrap.style.transform="translate("+(x0*(1-zp)+(1-kk)*540)+"px,"+(y0*(1-zp)+(1-kk)*960)+"px) scale("+(ss*kk)+")";
 fade(canvasWrap, zoom?seg(t,zoom.start,zoom.start+0.9):0);
 var fl=S("archive.fill");
 for(var idx=0;idx<COUNT;idx++){
  var rt=fl?(fl.start+(idx/PC|0)*(fl.colDelay||0.42)+(idx%PC)*(fl.rowDelay||0.30)):1e9;
  var ce=eo(cl((t-rt)/0.45)), tr="scale("+(0.94+0.06*ce)+")";
  inA[idx].style.opacity=ce; inA[idx].style.transform=tr;
  inB[idx].style.opacity=ce; inB[idx].style.transform=tr;}
 FLIPS.forEach(function(F){var on=t>=F.t,txt=on?("real · "+F.y):"standby";
  F.a.textContent=txt;F.b.textContent=txt;
  inA[F.idx].classList.toggle("isReal",on);inB[F.idx].classList.toggle("isReal",on);});
 var dimTo=0.34;
 var gOp=1-0.5*capOverGrid;
 var pan=S("phase.tabs"); if(pan) gOp*=1-(1-dimTo)*seg(t,pan.in-0.8,pan.in+0.2);
 if(tlSc) gOp*=1-(1-0.45)*seg(t,tlSc.in-0.6,tlSc.in+0.4)*(1-seg(t,tlSc.out,tlSc.out+0.6));
 if(endSc) gOp*=(1-seg(t,endSc.in,endSc.in+1.6));
 gridLayer.style.opacity=gOp;
 if((s=S("archive.hover"))&&LATE){var hr=LATE.HOVER_RECT;
  hoverRing.style.cssText+=";left:"+(hr.left-6)+"px;top:"+(hr.top-6)+"px;width:"+(hr.width+12)+"px;height:"+(hr.height+12)+"px";
  fade(hoverRing,seg(t,s.start,s.start+.4)*(1-seg(t,s.end,s.end+.4)));}
 var scr=S("archive.scroll"), off=0;
 if(scr&&t>=scr.start){ off=(t-scr.start)*(scr.speed||15); if(loopD>0) off=off%loopD; }
 gi.style.transform="translateY(-"+off+"px)";
 if((s=S("archive.scan"))){ fade(scanEl,seg(t,s.start,s.start+.3)*(1-seg(t,s.end-.5,s.end)));
  scanEl.style.top=(60+eio(seg(t,s.start,s.end))*1790)+"px"; } else fade(scanEl,0);
 if((s=S("archive.counter"))){ var post=S("compose.post");
  var cN=Math.round((s.from||1200)+eo(seg(t,s.start,s.end))*((s.to||12000)-(s.from||1200))+Math.max(0,t-s.end)*7);
  if(post&&t>=post.flyEnd) cN+=1;
  countNum.textContent=cN.toLocaleString("en-US");
  var cv=seg(t,s.start,s.start+.6)*(1-(tlSc?seg(t,tlSc.in-0.8,tlSc.in-0.2):0));
  if(post) cv=Math.max(cv, seg(t,post.flyEnd-0.4,post.flyEnd+0.2)*(1-seg(t,post.flyEnd+6,post.flyEnd+7)));
  fade(counter,cv); } else fade(counter,0);






 // Big panels breathe. A blinking bracket is too few pixels to read as motion;
 // drifting the whole card is what stops the frame looking like a photograph.
 function floaty(el,ph,amp){ if(el) el.style.transform=
   "translateY("+(Math.sin(t*0.85+ph)*(amp||9))+"px)"; }
 floaty(recEl,0,10); floaty(steps3El,1.4,8); floaty(sharpenEl,2.6,9);
 floaty(collapseEl,0.7,9); floaty(culpEl,3.3,7);


 // the ledger: one dated line per day, piling up into something with weight
 if(lgSc){ fade(ledgerEl, seg(t,lgSc.in,lgSc.in+0.4)*(1-seg(t,lgSc.out,lgSc.out+0.5)));
  var lst=lgSc.rowStart!=null?lgSc.rowStart:lgSc.in, lstep=lgSc.rowStep||0.34;
  lgEls.forEach(function(r,i){ fade(r, seg(t,lst+i*lstep,lst+i*lstep+0.3)); });
  var shownN=0; lgEls.forEach(function(r,i){ if(t>=lst+i*lstep) shownN++; });
  ledgerNum.textContent=Math.round(shownN*(lgSc.perRow||1)); }
 else fade(ledgerEl,0);

 // the archive as a live feed: everyone's records, always moving
 if(fdSc){ fade(feedEl, seg(t,fdSc.in,fdSc.in+0.6)*(1-seg(t,fdSc.out,fdSc.out+0.6)));
  var spd=fdSc.speed||46, sp2=[1,0.74];
  // the stream settles while an entry is being annotated, so the labels stay with it
  var hold=fhSc?seg(t,fhSc.at-0.5,fhSc.at)*(1-seg(t,fhSc.out,fhSc.out+0.5)):0;
  var travelled=fdTravel(t,spd,hold);
  fdCols.forEach(function(col,ci2){
   var setH=col.scrollHeight/3 || 950;
   var off2=(travelled*sp2[ci2])%setH;
   col.style.transform="translateY("+(-off2)+"px)"; });
  var widen=fdSc.widen!=null?eio(seg(t,fdSc.widen,fdSc.widen+1.2)):1;
  feedEl.style.opacity=feedEl.style.opacity; // keep
  fdCols.forEach(function(col,ci3){ col.style.opacity=ci3===0?1:(0.3+0.7*widen); });
  // when a phase bar or the end card takes over, the stream drops right back
  var pbb=S("phases.bar"), edd=S("end.card");
  var recede = pbb?seg(t,pbb.in-0.5,pbb.in+0.5):0;
  feedEl.style.opacity = (parseFloat(feedEl.style.opacity)||0) * (1-0.82*recede);
  // one entry turns real
  var realIdx = (fhPick!=null?fhPick:(frSc?(frSc.row||4):4));
  if(frSc) fdRows.forEach(function(r,i){ if(i===realIdx){
    var on2=t>=frSc.at; r.el.classList.toggle("real",on2);
    r.st.textContent=on2?("real · "+(frSc.year||"2029")):"standby"; } });
  // annotations attaching to a highlighted entry
  if(fhSc){ var hv2=seg(t,fhSc.at,fhSc.at+0.4)*(1-seg(t,fhSc.out,fhSc.out+0.4));
   var focus=seg(t,fhSc.at-0.3,fhSc.at+0.5)*(1-seg(t,fhSc.out,fhSc.out+0.5));
   // lock onto whichever entry is nearest the centre when the annotation starts
   if(fhPick===null && t>=fhSc.at-0.5){
     var best=1e9;
     fdRows.forEach(function(rw,ri){ if(rw.col!==0) return;
       var rc=rectOf(rw.el); if(rc.width<10) return;
       var d3=Math.abs(rc.top+rc.height/2-880);
       if(d3<best){ best=d3; fhPick=ri; } });
   }
   var tr2=fdRows[fhPick!=null?fhPick:(fhSc.row||4)];
   fdRows.forEach(function(rw,ri){ rw.el.style.opacity = (ri===fhPick)?1:(1-0.72*focus); });
   if(tr2){ var rr=rectOf(tr2.el);
    feedRing.style.cssText+=";left:"+(rr.left-6)+"px;top:"+(rr.top-6)+"px;width:"+(rr.width+12)+"px;height:"+(rr.height+12)+"px";
    fade(feedRing,hv2);
    (fhSc.labels||[]).forEach(function(lb,i){ var el=fnEls[i]; if(!el)return;
     el.textContent=lb;
     el.style.left=(rr.left+rr.width+22)+"px";
     el.style.top=(rr.top+rr.height/2-30+i*56)+"px";
     fade(el, hv2*seg(t,fhSc.at+0.3+i*0.45,fhSc.at+0.7+i*0.45)); }); } }
  else { fade(feedRing,0); fnEls.forEach(function(e){fade(e,0);});
    fdRows.forEach(function(rw){ rw.el.style.opacity=1; }); } }
 else { fade(feedEl,0); fade(feedRing,0); fnEls.forEach(function(e){fade(e,0);}); }

 // two phases: one filling, one still outlined
 if(pbSc){ fade(phbarEl, seg(t,pbSc.in,pbSc.in+0.4)*(1-seg(t,pbSc.out,pbSc.out+0.5)));
  phFills[0].style.width=(eio(seg(t,pbSc.fill0||pbSc.in,(pbSc.fill0||pbSc.in)+1.1))*100)+"%";
  phSegs[0].classList.toggle("live", t>=(pbSc.fill0||pbSc.in)+0.55);
  if(pbSc.fill1!=null){ phFills[1].style.width=(eio(seg(t,pbSc.fill1,pbSc.fill1+1.4))*(pbSc.fill1Pct||34))+"%"; }
  phNote.textContent=pbSc.note2||"";
  fade(phNote, pbSc.noteAt!=null?seg(t,pbSc.noteAt,pbSc.noteAt+0.4):0); }
 else fade(phbarEl,0);

 // the record whose fields were never filled
 if(recSc){ fade(recEl, seg(t,recSc.in,recSc.in+0.5)*(1-seg(t,recSc.out-0.4,recSc.out)));
  (recSc.fields||[]).forEach(function(f,i){ var r=recRows[i]; if(!r)return;
   fade(r.el, seg(t,f.at,f.at+0.4));
   // the empty slot keeps blinking: nothing ever goes in it
   // the slot keeps hunting for a value and never finds one
   var glyph="-/-\\|"; var gi2=Math.floor(t*9)%glyph.length;
   if(f.fillAt!=null && t>=f.fillAt){        // the same slot, finally answered
     var fn3=Math.floor(cl((t-f.fillAt)/0.5)*(f.value||"").length);
     r.v.textContent=(f.value||"").slice(0,fn3);
     r.v.style.opacity=1; r.v.style.color="#F5F5F0"; r.v.style.letterSpacing="1px";
   } else {
     r.v.textContent = t>=f.at ? ("[  "+glyph[gi2]+"  ]") : "[    ]";
     r.v.style.opacity = 0.45+0.55*Math.abs(Math.sin((t-f.at)*3.4));
     r.v.style.color="#6B6B6B"; r.v.style.letterSpacing="6px";
   }
  }); } else fade(recEl,0);


 // "not motivation, not talent" - name them, cross them off
 if(cuSc){ fade(culpEl, seg(t,cuSc.in,cuSc.in+0.35)*(1-seg(t,cuSc.out,cuSc.out+0.4)));
  (cuSc.at||[]).forEach(function(a5,i){ var c=cuEls[i]; if(!c)return;
   c.el.style.opacity=seg(t,a5-0.35,a5-0.05);
   c.x.style.transform="scaleX("+eio(seg(t,a5,a5+0.42))+")"; }); }
 else fade(culpEl,0);

 // three things, filling in one per spoken step
 if(st3Sc){ fade(steps3El, seg(t,st3Sc.in,st3Sc.in+0.4)*(1-seg(t,st3Sc.out,st3Sc.out+0.5)));
  (st3Sc.at||[]).forEach(function(a3,i){ if(s3Els[i]) s3Els[i].classList.toggle("on", t>=a3); }); }
 else fade(steps3El,0);

 // "get healthy" resolving into something you can check
 if(shSc){ fade(sharpenEl, seg(t,shSc.in,shSc.in+0.35)*(1-seg(t,shSc.out,shSc.out+0.4)));
  var vt=shSc.vagueAt!=null?shSc.vagueAt:shSc.in;
  var vn=Math.floor(cl((t-vt)/0.9)*(shSc.vague||"").length);
  shOld.textContent=(shSc.vague||"").slice(0,vn);
  var rp2=seg(t,shSc.at,shSc.at+1.1), raw2=shSc.specific||"";
  var keep2=Math.round(raw2.length*eo(rp2));
  shNew.textContent=raw2.slice(0,keep2)+raw2.slice(keep2).replace(/\S/g,"\u00b7");
  shOld.style.opacity=1-rp2; shOld.style.textDecoration=rp2>0.35?"line-through":"none";
  shNew.style.opacity=rp2>0.02?1:0; }
 else fade(sharpenEl,0);

 // the whole ambition contracting to one thing you can do tomorrow
 if(clSc){ fade(collapseEl, seg(t,clSc.in,clSc.in+0.35)*(1-seg(t,clSc.out,clSc.out+0.4)));
  var cp2=eio(seg(t,clSc.at,clSc.at+1.0));
  clBig.style.transform="scale("+(1-0.42*cp2)+")";
  clBig.style.opacity=1-0.55*cp2;
  clSmall.style.opacity=eo(seg(t,clSc.at+0.55,clSc.at+1.25));
  clSmall.style.transform="scale("+(0.85+0.15*eo(seg(t,clSc.at+0.55,clSc.at+1.25)))+")"; }
 else fade(collapseEl,0);

 // orbit: it stayed in your head -> no date will stick -> it decays into a mood
 if(orbSc){ var oin=seg(t,orbSc.in,orbSc.in+0.5), oout=1-seg(t,orbSc.out-0.3,orbSc.out);
  fade(orbEl,oin*oout); fade(orbCore,oin*oout*0.9);
  var brP=orbSc.brackets!=null?seg(t,orbSc.brackets,orbSc.brackets+0.5):0;
  var scP=orbSc.scramble!=null?seg(t,orbSc.scramble,orbSc.scramble+1.6):0;
  var stP=orbSc.scatter!=null?eio(seg(t,orbSc.scatter,orbSc.out)):0;
  var N2=orbEls.length, cx0=540, cy0=orbSc.cy||900;
  orbEls.forEach(function(o,i){
   var ang=(t-orbSc.in)*0.42 + i*(Math.PI*2/N2);          // never stops going round
   var rx=(orbSc.rx||330)*(1+stP*2.4), ry=(orbSc.ry||205)*(1+stP*2.4);
   o.el.style.left=(cx0+Math.cos(ang)*rx)+"px";
   o.el.style.top=(cy0+Math.sin(ang)*ry)+"px";
   // the far side of the orbit sits back, so the ring reads as depth
   var depth=0.55+0.45*((Math.sin(ang)+1)/2);
   o.el.style.opacity=depth*(1-stP);
   // a date bracket that blinks and never fills
   o.br.style.opacity=brP*(1-scP)*(0.35+0.65*Math.abs(Math.sin(t*3.1+i)));
   // the words lose their edges: a plan becomes a mood
   if(scP>0){ var raw=o.raw, keep=Math.max(0,Math.round(raw.length*(1-scP)));
    o.txt.textContent=raw.slice(0,keep)+raw.slice(keep).replace(/\S/g,"\u00b7"); }
   else o.txt.textContent=o.raw;
  }); } else { fade(orbEl,0); fade(orbCore,0); }

 // recall: ghosts of the plans rising out of the months already spent
 if(rcSc){ fade(rcEl, seg(t,rcSc.in,rcSc.in+0.3)*(1-seg(t,rcSc.out-0.3,rcSc.out)));
  rcEls.forEach(function(g,i){
   var gt=(rcSc.at||[])[i]; if(gt==null){ fade(g.el,0); return; }
   var k4=seg(t,gt,gt+1.1);
   g.el.style.left=g.x+"px"; g.el.style.top=(g.y-k4*52)+"px";
   g.el.style.fontSize=(26-4*k4)+"px";
   fade(g.el, Math.sin(cl(k4)*Math.PI)*0.95); }); }
 else fade(rcEl,0);

 // thoughts: unanchored, drifting, then scattering into nothing
 if(thSc){ var dv=thSc.dissolve!=null?eio(seg(t,thSc.dissolve,thSc.out)):0;
  fade(thEl, seg(t,thSc.in,thSc.in+0.6)*(1-seg(t,thSc.out-0.2,thSc.out)));
  thEls.forEach(function(o,i){
   var dx=Math.sin(t*0.55+o.ph)*26, dy=Math.cos(t*0.42+o.ph*1.3)*20;   // never still
   var sx=dv*o.dir*420, sy=dv*(i%3-1)*260;                              // scatter on dissolve
   o.el.style.left=(o.bx+dx+sx)+"px"; o.el.style.top=(o.by+dy+sy)+"px";
   o.el.style.opacity=(0.6-0.6*dv)*(0.75+0.25*Math.sin(t*0.9+o.ph));    // breathing, then gone
  }); } else fade(thEl,0);

 // planned vs done
 if(tlySc){ fade(tallyEl, seg(t,tlySc.in,tlySc.in+0.4)*(1-seg(t,tlySc.out,tlySc.out+0.4)));
  tPlan.textContent=Math.round(eo(seg(t,tlySc.in+0.2,tlySc.in+1.2))*(tlySc.planned||12));
  tDone.textContent=Math.round(eo(seg(t,tlySc.in+1.1,tlySc.in+2.1))*(tlySc.done||2)); }
 else fade(tallyEl,0);

 // the record building: bars growing, streak climbing
 if(stkSc){ fade(streakEl, seg(t,stkSc.in,stkSc.in+0.4)*(1-seg(t,stkSc.out,stkSc.out+0.4)));
  var gp2=seg(t,stkSc.growStart!=null?stkSc.growStart:stkSc.in,stkSc.growEnd!=null?stkSc.growEnd:stkSc.out);
  stkBars.forEach(function(b,i){
   var lead=cl((gp2*stkBars.length-i)/1.0);   // bars rise left to right
   b.el.style.height=(b.h*eo(lead))+"%"; });
  streakNum.textContent=Math.round(gp2*(stkSc.days||14)); }
 else fade(streakEl,0);

 // dated / public / permanent, stamping on one at a time
 if(stmSc){ fade(stampsEl, seg(t,stmSc.in,stmSc.in+0.3)*(1-seg(t,stmSc.out,stmSc.out+0.4)));
  (stmSc.at||[]).forEach(function(a2,i){ if(!stmpEls[i])return;
   var k3=eo(seg(t,a2,a2+0.42));
   stmpEls[i].style.opacity=k3; stmpEls[i].style.transform="scale("+(0.82+0.18*k3)+")"; }); }
 else fade(stampsEl,0);

 // from here to there
 if(pathSc){ fade(pathSvg, seg(t,pathSc.in,pathSc.in+0.3)*(1-seg(t,pathSc.out,pathSc.out+0.4)));
  var dp=eio(seg(t,pathSc.start,pathSc.end));
  pArc.style.strokeDashoffset=pArcLen*(1-dp);
  var pt=pArc.getPointAtLength(pArcLen*dp);
  pDot.setAttribute("cx",pt.x); pDot.setAttribute("cy",pt.y);
  pDot.setAttribute("opacity", dp>0.02&&dp<0.995?1:0);
  pB.setAttribute("opacity", eo(seg(t,pathSc.end-0.25,pathSc.end+0.15))); }
 else fade(pathSvg,0);

 // calendar: the year burning down
 if(calSc){ var cvis=seg(t,calSc.in,calSc.in+0.5)*(1-seg(t,calSc.out,calSc.out+0.6));
  fade(calEl,cvis);
  var strikes=calSc.strike||[];
  calCells.forEach(function(c,i){
   var st2=strikes[i];
   c.strike.style.transform="scaleX("+(st2==null?0:eio(seg(t,st2,st2+0.32)))+")";
   var isLeft = calSc.remain!=null && i>=calSc.remain && t>=(calSc.remainAt||1e9);
   c.el.classList.toggle("left", !!isLeft);
   // the months still on the clock keep breathing, so the frame never freezes
   var breathe = isLeft ? (0.86+0.14*Math.sin(t*2.1+i*0.8)) : 1;
   c.el.style.opacity = ((st2!=null && t>=st2+0.32) ? 0.45 : 1) * breathe;
   c.el.style.transform = isLeft ? "scale("+(0.99+0.012*Math.sin(t*2.1+i*0.8))+")" : "scale(1)"; });
  if(calSc.point!=null&&calCells.length){ var pr=rectOf(calCells[0].el);
   calRing.style.cssText+=";left:"+(pr.left-5)+"px;top:"+(pr.top-5)+"px;width:"+(pr.width+10)+"px;height:"+(pr.height+10)+"px";
   fade(calRing, cvis*seg(t,calSc.point,calSc.point+0.3)*(1-seg(t,calSc.point+1.6,calSc.point+2.0))); }
  else fade(calRing,0);
 } else { fade(calEl,0); fade(calRing,0); }

 // progress log: days becoming visible
 if(plogSc){ var pvis=seg(t,plogSc.in,plogSc.in+0.5)*(1-seg(t,plogSc.out,plogSc.out+0.6));
  fade(plogEl,pvis);
  var fs0=plogSc.fillStart!=null?plogSc.fillStart:plogSc.in, fe0=plogSc.fillEnd!=null?plogSc.fillEnd:plogSc.out;
  var shown=Math.floor(cl((t-fs0)/Math.max(0.1,fe0-fs0))*plogMarks.length);
  plogMarks.forEach(function(m,i){ m.classList.toggle("on", i<shown); });
  plogNum.textContent=shown;
 } else fade(plogEl,0);

 // phases
 if(pan){ var tv2=seg(t,pan.in,pan.in+.6)*(1-seg(t,pan.out,pan.out+.5));
  fade(tab1,tv2); fade(tab2,tv2);
  var sel=null; ALL("phase.select").forEach(function(p){ if(t>=p.at) sel=p; });
  tab1.classList.toggle("on",!!sel&&sel.index===0); tab2.classList.toggle("on",!!sel&&sel.index===1);
  if(sel){ panelNo.textContent=(tabsSc.labels||["Phase 01","Phase 02"])[sel.index];
   panelTitle.textContent=sel.title||""; panelBody.textContent=sel.body||"";
   fade(panel,seg(t,sel.at+.15,sel.at+.75)*(1-seg(t,pan.out,pan.out+.5))); } else fade(panel,0);
 } else { fade(tab1,0);fade(tab2,0);fade(panel,0); }
 if(stepsSc) (stepsSc.at||[]).forEach(function(st,i){ if(stepEls[i])
   fade(stepEls[i],seg(t,st,st+0.5)*(pan?(1-seg(t,pan.out,pan.out+.5)):1)); });
 else stepEls.forEach(function(el){fade(el,0);});

 // compose
 var op2=S("compose.open"), ty=S("compose.type"), po=S("compose.post");
 if(op2){ fade(addBtn,seg(t,op2.addAt,op2.addAt+.4)*(1-seg(t,op2.clickAt+0.4,op2.clickAt+0.7)));
  addBtn.classList.toggle("hot",t>=op2.clickAt-0.1&&t<op2.clickAt+0.25); } else fade(addBtn,0);
 if(ty){ var cEnd=po?po.flyEnd+1.6:ty.end+2;
  fade(compose,seg(t,op2?op2.clickAt+0.2:ty.start-0.6,(op2?op2.clickAt+0.2:ty.start-0.6)+0.5)*(1-seg(t,cEnd,cEnd+0.5)));
  field.classList.toggle("focus",t>=ty.start-0.4&&t<ty.end+0.6);
  var fn=Math.floor(cl((t-ty.start)/Math.max(0.1,ty.end-ty.start))*(ty.text||"").length);
  fieldText.textContent=(ty.text||"").slice(0,fn);
  fieldCaret.style.opacity=(t>=ty.start-0.4&&t<ty.end+0.4)?1:0; } else fade(compose,0);
 if(po){ postBtn.classList.toggle("hot",t>=po.clickAt-0.1&&t<po.clickAt+0.3);
  if(t>=po.flyStart&&t<po.flyEnd+0.3&&LATE){var fr=LATE.FIELD_RECT,k2=eio(seg(t,po.flyStart,po.flyEnd));
   flyCard.style.left=(fr.left+(150-fr.left)*k2)+"px"; flyCard.style.top=(fr.top+(120-fr.top)*k2)+"px";
   flyCard.style.width=(fr.width+(248-fr.width)*k2)+"px"; flyCard.style.fontSize=(24-4*k2)+"px";
   flyCard.textContent=(ty&&ty.text)||""; fade(flyCard,1-cl((k2-0.72)/0.28)); } else fade(flyCard,0); }
 else fade(flyCard,0);
 if((s=S("prompt.turn"))){ fade(promptEl,seg(t,s.in,s.in+.5)*(1-seg(t,s.out,s.out+.5)));
  promptCaret.style.opacity=(t>=s.in+0.6&&Math.floor(t*2)%2===0)?1:0.15; } else fade(promptEl,0);

 // cursor: typing windows steer it to the caret
 var p=pathAt(t), cx=p.x, cy=p.y;
 TYPEWIN.forEach(function(tw2,q){ if(t>=tw2.s&&t<tw2.e){
  var nn=cl((t-tw2.s)/(tw2.e-tw2.s))*LINES_TXT[q].length;
  cx=lines[q].absX+nn*CHAR_W+6; cy=lines[q].absY+30; }});
 if(ty&&LATE&&t>=ty.start&&t<ty.end){ var fr2=LATE.FIELD_RECT;
  var fn2=cl((t-ty.start)/(ty.end-ty.start))*(ty.text||"").length;
  cx=fr2.left+22+fn2*13.2; cy=fr2.top+fr2.height/2+16; }
 if(tlSc&&t>=tlSc.start&&t<tlSc.end){ cx=250+eio(seg(t,tlSc.start,tlSc.end))*580; cy=1050; }
 cursorEl.style.left=cx+"px"; cursorEl.style.top=cy+"px";
 fade(cursorEl, endSc?(1-seg(t,endSc.in+1.8,endSc.in+2.6)):1);
 var rop=0,rx=0,ry=0;
 CLICKS.forEach(function(m){var d=t-m.t; if(d>=0&&d<0.5){rop=1-d/0.5;rx=m.x;ry=m.y;
  rippleEl.style.transform="scale("+(0.35+d*2.2)+")";}});
 rippleEl.style.left=rx+"px";rippleEl.style.top=ry+"px";fade(rippleEl,rop);
 var pop=0,px2=0,py2=0;
 PULSES.forEach(function(n2){var pd=t-n2.t; if(pd>=0&&pd<1.5){pop=(1-pd/1.5)*0.8;px2=n2.x;py2=n2.y;
  pulseEl.style.transform="scale("+(0.25+pd*2.6)+")";}});
 pulseEl.style.left=px2+"px";pulseEl.style.top=py2+"px";fade(pulseEl,pop);
}

// ================= driver =================
var st0=null,raf=null;
function frame(now){ if(st0===null)st0=now; var t=(now-st0)/1000;
 if(t>=TOTAL){render(TOTAL);raf=null;return;} render(t); raf=requestAnimationFrame(frame); }
function play(){ R("playBtn").style.display="none"; st0=null;
 if(raf)cancelAnimationFrame(raf); raf=requestAnimationFrame(frame); }
addEventListener("load",function(){
 loopD=(bB.getBoundingClientRect().top-bA.getBoundingClientRect().top)/sc;
 placeBeats(); buildSchedule(); resolveTargets();
 var q=new URLSearchParams(location.search);
 if(q.get("text")==="1") showText=true;
 render(0);
 window.__seek=function(x){render(x);}; window.__duration=TOTAL;
 var tp=q.get("t");
 if(tp!==null&&!isNaN(parseFloat(tp))){R("playBtn").style.display="none";render(parseFloat(tp));return;}
 if(q.get("autoplay")==="1") play(); else R("playBtn").addEventListener("click",play);
});
})();
