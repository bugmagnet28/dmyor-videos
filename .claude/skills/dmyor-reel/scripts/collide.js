const puppeteer=require("puppeteer"),path=require("path");
(async()=>{
 const b=await puppeteer.launch({headless:"new",args:["--no-sandbox"]});
 const p=await b.newPage(); await p.setViewport({width:1080,height:1920,deviceScaleFactor:1});
 await p.goto("file://"+path.resolve(process.argv[2]),{waitUntil:"load"});
 await p.waitForFunction("typeof window.__seek==='function'");
 const dur=await p.evaluate(()=>window.__duration);
 const seen=new Map();
 for(let t=0;t<=dur;t+=0.25){
  const r=await p.evaluate(s=>{window.__seek(s);
   // top-level scene layers that are actually visible

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
   const vis=el=>{let n=el,o=1;while(n&&n!==document.body){o*=parseFloat(getComputedStyle(n).opacity);n=n.parentElement;}return o;};
   const groups=[...document.querySelectorAll('#cam > div, #cam > svg')]
     .filter(g=>vis(g)>0.15 && !(g.matches&&g.matches('[data-decor]')))
     .map(g=>{
       const rects=[...g.querySelectorAll('*')]
         .filter(e=>vis(e)>0.15 && (!e.children.length || e.textContent.trim()))
         .map(e=>{const r=document.createRange();r.selectNodeContents(e);
                  const tb=e.textContent.trim()?r.getBoundingClientRect():e.getBoundingClientRect();
                  return visRect(e,tb);})
         .filter(r=>r&&r.width>4&&r.height>4);
       if(!rects.length)return null;
       return {id:g.id||g.className,
         x1:Math.min(...rects.map(r=>r.left)),x2:Math.max(...rects.map(r=>r.right)),
         y1:Math.min(...rects.map(r=>r.top)),y2:Math.max(...rects.map(r=>r.bottom))};
     }).filter(Boolean);
   const hits=[];
   for(let i=0;i<groups.length;i++)for(let j=i+1;j<groups.length;j++){
     const a=groups[i],c=groups[j];
     const ox=Math.min(a.x2,c.x2)-Math.max(a.x1,c.x1), oy=Math.min(a.y2,c.y2)-Math.max(a.y1,c.y1);
     if(ox>30&&oy>30) hits.push([a.id,c.id,Math.round(ox),Math.round(oy)]);
   }
   return hits;},t);
  r.forEach(h=>{const k=h[0]+" x "+h[1]; if(!seen.has(k))seen.set(k,[t.toFixed(1),h[2],h[3]]);});
 }
 await b.close();
 if(!seen.size)console.log("no scene-layer collisions");
 else for(const [k,v] of seen) console.log(`COLLIDE first t=${v[0]}  overlap ${v[1]}x${v[2]}px  ${k}`);
})();
