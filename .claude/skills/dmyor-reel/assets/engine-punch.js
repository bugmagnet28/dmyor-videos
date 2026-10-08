/* dmyor punch engine: bold kinetic type on flat bright panes, for muted autoplay.
   Same contract as the other engines: render(t) is a pure function of time,
   window.__seek / window.__duration for record.js and the audits.

   Rule baked in: anything whose time is <= 0 is drawn FINISHED at t=0, so frame 0
   (the scroll-stopper and the grid cover) is never empty or mid-entrance.

   timeline.json
   { "engine":"punch", "total":22.5,
     "bg":[{t,c,dir}],                       flat panes that wipe in; t<=0 is already on
     "camera":[{t,s,x,y}],                   keyframed push/pull, plus a permanent drift
     "scenes":[
       {type:"stack", in,out,y,align, lines:[{text,size,color,at,pill,weight,
            strikeAt,strikeColor, swapAt,swapText,swapColor, pulseAt:[t]}]},
       {type:"plan",  in,out,y,title,titleColor,labelColor,textColor,chkColor,
            items:[{label,text,at,checkAt}]},
       {type:"brand", in,out,y,mark,line,handle,color,lineColor,handleBg,handleColor}
     ],
     "sfx":[{t,v,g}]                         optional extra hand-placed cues (sfx.py)
   } */
(function(){
"use strict";
var TOTAL=TL.total, W=1080, H=1920;
var stage=document.getElementById("stage");
function fit(){ var s=Math.min(innerWidth/W, innerHeight/H); stage.style.transform="scale("+s+")"; }
fit(); addEventListener("resize",fit);
var cl=function(x){return x<0?0:(x>1?1:x)};
var seg=function(t,a,b){return b<=a?(t>=b?1:0):cl((t-a)/(b-a))};
var eio=function(x){return x<.5?4*x*x*x:1-Math.pow(-2*x+2,3)/2};
var eob=function(x){var c=1.6;return 1+(c+1)*Math.pow(x-1,3)+c*Math.pow(x-1,2);};
var CO={ink:"#0B0B0F",black:"#0B0B0F",paper:"#FFFFFF",white:"#FFFFFF",amber:"#FFC530",blue:"#2F5BFF",
        coral:"#FF4D5E",green:"#18C77A",cream:"#FFF6E5",dim:"#5A5A66"};
function col(n,d){ return CO[n]||n||d||CO.ink; }
// entrance progress: finished at t=0 if the cue is at or before 0
function prog(t,at,dur){ if(at==null||at<=0) return 1; return t<at?0:eob(cl((t-at)/(dur||0.3))); }
function bump(t,list,dur){ var b=0; (list||[]).forEach(function(a){ var u=(t-a)/(dur||0.36);
  if(u>=0&&u<=1) b=Math.max(b,Math.sin(Math.PI*u)); }); return b; }

// ---------- background panes ----------
var bgEl=document.getElementById("bg");
var BG=(TL.bg||[]).map(function(b){ var d=document.createElement("div"); d.className="bgpane";
  d.style.background=col(b.c); bgEl.appendChild(d); return {sc:b, el:d}; });

// ---------- scenes ----------
var cam=document.getElementById("cam");
var SC=(TL.scenes||[]).map(function(s,si){
  var el=document.createElement("div"); el.className="scene"; el.id="sc"+si+"_"+s.type.replace(/\W/g,"");
  el.style.top=(s.y||400)+"px"; el.style.textAlign=s.align||"center";
  cam.appendChild(el);
  var o={sc:s, el:el, parts:[]};
  if(s.type==="stack"){
    (s.lines||[]).forEach(function(L){
      var ln=document.createElement("div"); ln.className="ln";
      ln.style.fontSize=(L.size||110)+"px"; if(L.weight) ln.style.fontWeight=L.weight;
      if(L.gap!=null) ln.style.marginTop=L.gap+"px";
      var tx=document.createElement("span"); tx.className="tx"+(L.pill?" pill":"");
      tx.textContent=L.text; tx.style.color=col(L.color);
      if(L.pill) tx.style.background=col(L.pill);
      ln.appendChild(tx);
      var st=null; if(L.strikeAt!=null){ st=document.createElement("span"); st.className="strike";
        st.style.background=col(L.strikeColor||"coral"); tx.appendChild(st); }
      el.appendChild(ln); o.parts.push({L:L, ln:ln, tx:tx, st:st, swapped:false}); });
  } else if(s.type==="plan"){
    var ti=document.createElement("div"); ti.className="ptitle"; ti.textContent=s.title||"";
    ti.style.color=col(s.titleColor); el.appendChild(ti); o.title=ti;
    (s.items||[]).forEach(function(it){
      var r=document.createElement("div"); r.className="prow";
      r.innerHTML='<div class="pchk"><i></i></div><div class="pbody"><div class="plab"></div><div class="ptxt"></div></div>';
      var chk=r.querySelector(".pchk"); chk.style.borderColor=col(s.chkColor||"green");
      chk.querySelector("i").style.background=col(s.chkColor||"green");
      var lab=r.querySelector(".plab"); lab.textContent=it.label; lab.style.color=col(it.labelColor||s.labelColor||"blue");
      var txt=r.querySelector(".ptxt"); txt.textContent=it.text; txt.style.color=col(s.textColor);
      el.appendChild(r); o.parts.push({it:it, row:r, dot:chk.querySelector("i")}); });
  } else if(s.type==="brand"){
    el.innerHTML='<div class="bmark"></div><div class="bline"></div><div class="bhandle"></div>';
    var m=el.querySelector(".bmark"), l=el.querySelector(".bline"), h=el.querySelector(".bhandle");
    m.textContent=s.mark||"dmyor"; m.style.color=col(s.color||"paper");
    l.textContent=s.line||""; l.style.color=col(s.lineColor||s.color||"paper");
    h.textContent=s.handle||"@dmyor_global"; h.style.background=col(s.handleBg||"amber"); h.style.color=col(s.handleColor||"ink");
    o.parts=[m,l,h];
  }
  return o; });

// ---------- camera ----------
var CAM=(TL.camera||[]).slice().sort(function(a,b){return a.t-b.t;});
function camAt(t){
  if(!CAM.length) return {s:1,x:0,y:0};
  if(t<=CAM[0].t) return CAM[0];
  for(var i=0;i<CAM.length-1;i++){ var a=CAM[i],b=CAM[i+1];
    if(t>=a.t&&t<=b.t){ var k=eio((t-a.t)/Math.max(1e-6,b.t-a.t));
      return {s:(a.s||1)+((b.s||1)-(a.s||1))*k, x:(a.x||0)+((b.x||0)-(a.x||0))*k, y:(a.y||0)+((b.y||0)-(a.y||0))*k}; } }
  return CAM[CAM.length-1]; }

function render(t){
  t=Math.max(0,Math.min(TOTAL,t));
  BG.forEach(function(B){ var b=B.sc;
    var k=b.t<=0?1:eio(seg(t,b.t,b.t+(b.dur||0.32))), off=(1-k)*100, dir=b.dir||"up";
    B.el.style.transform= dir==="down"?"translateY("+(-off)+"%)": dir==="left"?"translateX("+off+"%)":
                          dir==="right"?"translateX("+(-off)+"%)":"translateY("+off+"%)"; });
  // permanent drift: large flat panes give the frame-diff nothing to see, so the type itself moves
  var c=camAt(t);
  var ds=1+Math.sin(t*0.9)*0.014, dx=Math.sin(t*0.73)*12, dy=Math.cos(t*0.81)*14;
  cam.style.transform="translate("+(-(c.x||0)+dx)+"px,"+(-(c.y||0)+dy)+"px) scale("+((c.s||1)*ds)+")";

  SC.forEach(function(O){ var s=O.sc;
    var vin= s.in<=0?1:seg(t,s.in,s.in+0.12);
    var vout= s.out==null?0:seg(t,s.out-0.15,s.out);
    O.el.style.opacity=vin*(1-vout);
    if(s.type==="stack"){
      O.parts.forEach(function(P,i){ var L=P.L;
        var at=L.at!=null?L.at:s.in;
        var p=prog(t,at,0.3);
        var pu=bump(t,L.pulseAt,0.36)*0.07;
        if(L.swapAt!=null){ var sw=t>=L.swapAt;
          if(sw!==P.swapped){ P.tx.firstChild.nodeValue=sw?L.swapText:L.text;
            P.tx.style.color=col(sw&&L.swapColor?L.swapColor:L.color); P.swapped=sw; }
          pu=Math.max(pu,bump(t,[L.swapAt],0.3)*0.09); }
        P.ln.style.transform="translateY("+((1-p)*70)+"px) scale("+(0.9+0.1*p+pu)+")";
        P.ln.style.opacity=cl(p*1.6);
        if(P.st) P.st.style.width=(eio(seg(t,L.strikeAt,L.strikeAt+0.28))*104)+"%"; });
    } else if(s.type==="plan"){
      var tp=prog(t,s.titleAt!=null?s.titleAt:s.in,0.3);
      O.title.style.opacity=cl(tp*1.6); O.title.style.transform="translateY("+((1-tp)*50)+"px)";
      O.parts.forEach(function(P){ var p=prog(t,P.it.at,0.32);
        P.row.style.opacity=cl(p*1.6); P.row.style.transform="translateX("+((1-p)*90)+"px)";
        var ck=P.it.checkAt==null?0:(t<P.it.checkAt?0:eob(cl((t-P.it.checkAt)/0.25)));
        P.dot.style.transform="scale("+ck+")"; });
    } else if(s.type==="brand"){
      var p0=prog(t,s.in,0.4), p1=prog(t,s.in+0.35,0.3), p2=prog(t,s.in+0.7,0.3);
      O.parts[0].style.transform="scale("+(1.12-0.12*p0)+")"; O.parts[0].style.opacity=cl(p0*1.4);
      O.parts[1].style.transform="translateY("+((1-p1)*40)+"px)"; O.parts[1].style.opacity=cl(p1*1.6);
      O.parts[2].style.transform="translateY("+((1-p2)*40)+"px) scale("+(1+bump(t,[s.in+1.4],0.4)*0.06)+")";
      O.parts[2].style.opacity=cl(p2*1.6);
    } });
}

var st0=null,raf=null;
function frame(now){ if(st0===null)st0=now; var t=(now-st0)/1000;
  if(t>=TOTAL){render(TOTAL);raf=null;return;} render(t); raf=requestAnimationFrame(frame); }
function play(){ document.getElementById("playBtn").style.display="none"; st0=null;
  if(raf)cancelAnimationFrame(raf); raf=requestAnimationFrame(frame); }
addEventListener("load",function(){
  render(0);
  window.__seek=function(x){render(x);}; window.__duration=TOTAL;
  var q=new URLSearchParams(location.search), tp=q.get("t");
  if(tp!==null&&!isNaN(parseFloat(tp))){ document.getElementById("playBtn").style.display="none"; render(parseFloat(tp)); return; }
  if(q.get("autoplay")==="1") play(); else document.getElementById("playBtn").addEventListener("click",play);
});
})();
