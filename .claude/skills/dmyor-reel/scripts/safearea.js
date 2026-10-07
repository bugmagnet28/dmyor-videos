// Reels UI covers the top strip and the bottom third. Flag content outside the band.
const puppeteer=require("puppeteer"),path=require("path");
const TOP=240,BOT=1250;
(async()=>{
 const b=await puppeteer.launch({headless:"new",args:["--no-sandbox"]});
 const p=await b.newPage(); await p.setViewport({width:1080,height:1920,deviceScaleFactor:1});
 await p.goto("file://"+path.resolve(process.argv[2]),{waitUntil:"load"});
 await p.waitForFunction("typeof window.__seek==='function'");
 const dur=await p.evaluate(()=>window.__duration); const bad=new Map();
 for(let t=0;t<=dur;t+=0.25){
  const r=await p.evaluate((s,TOP,BOT)=>{window.__seek(s);

   // an element scrolled out of an overflow:hidden parent is not on screen.
   // measure what is actually visible, not the raw rect.
   const clipRect = el => {
     let r = null, n = el.parentElement;
     while (n && n !== document.body) {
       const cs = getComputedStyle(n);
       if (cs.overflow !== 'visible' || cs.overflowY !== 'visible' || cs.overflowX !== 'visible') {
         const b = n.getBoundingClientRect();
         r = r ? {l:Math.max(r.l,b.left), t:Math.max(r.t,b.top),
                  rt:Math.min(r.rt,b.right), b:Math.min(r.b,b.bottom)}
               : {l:b.left, t:b.top, rt:b.right, b:b.bottom};
       }
       n = n.parentElement;
     }
     return r;
   };
   const visRect = (el, bb) => {
     const c = clipRect(el);
     if (!c) return bb;
     const l = Math.max(bb.left, c.l), t = Math.max(bb.top, c.t);
     const rt = Math.min(bb.right, c.rt), b = Math.min(bb.bottom, c.b);
     if (rt - l < 2 || b - t < 2) return null;          // clipped away entirely
     return {left:l, top:t, right:rt, bottom:b, width:rt-l, height:b-t};
   };
   const vis=e=>{let n=e,o=1;while(n&&n!==document.body){o*=parseFloat(getComputedStyle(n).opacity);n=n.parentElement;}return o;};
   const o=[];
   document.querySelectorAll('#stage *').forEach(el=>{
     if(vis(el)<0.12)return;
     if(el.closest && el.closest('[data-decor]')) return;
     const cs=getComputedStyle(el);
     const painted=cs.backgroundColor!=='rgba(0, 0, 0, 0)'||parseFloat(cs.borderTopWidth)>0;
     const isText=!el.children.length&&el.textContent.trim();
     if(!isText&&!painted)return;
     let bb; if(isText){const rg=document.createRange();rg.selectNodeContents(el);bb=rg.getBoundingClientRect();}
     else bb=el.getBoundingClientRect();
     bb=visRect(el,bb); if(!bb) return;
     if(bb.width<2||bb.height<2)return;
     if(bb.width>=1080||bb.height>=1920)return;   // full-bleed layers bleed on purpose
     if(bb.top<TOP||bb.bottom>BOT)
       o.push([(el.id||el.className||'?')+'', el.textContent.trim().slice(0,22),Math.round(bb.top),Math.round(bb.bottom)]);
   });return o;},t,TOP,BOT);
  r.forEach(x=>{const k=x[0]+'|'+x[1]; if(!bad.has(k))bad.set(k,[t.toFixed(1),x[2],x[3]]);});
 }
 await b.close();
 if(!bad.size)console.log(`all content inside the Reels safe band (y ${TOP}..${BOT})`);
 else for(const [k,v] of bad) console.log(`OUTSIDE t=${v[0]} y ${v[1]}..${v[2]}  ${k}`);
})();
