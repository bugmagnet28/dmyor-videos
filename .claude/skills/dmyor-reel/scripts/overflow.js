const puppeteer=require("puppeteer"),path=require("path");
(async()=>{
 const b=await puppeteer.launch({headless:"new",args:["--no-sandbox"]});
 const p=await b.newPage(); await p.setViewport({width:1080,height:1920,deviceScaleFactor:1});
 await p.goto("file://"+path.resolve(process.argv[2]),{waitUntil:"load"});
 await p.waitForFunction("typeof window.__seek==='function'");
 const dur=await p.evaluate(()=>window.__duration);
 const bad=new Map();
 for(let t=0;t<=dur;t+=0.25){
  const r=await p.evaluate(s=>{window.__seek(s);

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
   const vis=el=>{let n=el;while(n&&n!==document.body){if(parseFloat(getComputedStyle(n).opacity)<0.12)return false;n=n.parentElement;}return true;};
   const o=[];
   document.querySelectorAll('#stage *').forEach(el=>{
     if(!vis(el))return;
     if(el.closest && el.closest('[data-decor]')) return;
     const cs=getComputedStyle(el);
     const painted = cs.backgroundColor!=='rgba(0, 0, 0, 0)' ||
                     parseFloat(cs.borderTopWidth)>0 || parseFloat(cs.borderLeftWidth)>0;
     const isText = !el.children.length && el.textContent.trim();
     if(!isText && !painted) return;
     // text is measured by its glyph ink; painted boxes by their own rect
     let b;
     if(isText){ const rg=document.createRange(); rg.selectNodeContents(el);
                 b=rg.getBoundingClientRect(); rg.detach&&rg.detach(); }
     else b=el.getBoundingClientRect();
     b=visRect(el,b); if(!b) return;
     if(b.width<2||b.width>=1080||b.height>=1920)return;  // full-bleed layers are intentional
     if(b.left<14||b.right>1066) o.push(['x',el.textContent.trim().slice(0,26),Math.round(b.left),Math.round(b.right)]);
     else if(b.top<14||b.bottom>1906) o.push(['y',el.textContent.trim().slice(0,26),Math.round(b.top),Math.round(b.bottom)]);
   });return o;},t);
  r.forEach(x=>{const k=x[0]+'|'+x[1]; if(!bad.has(k))bad.set(k,[t.toFixed(1),x[0],x[2],x[3]]);});
 }
 await b.close();
 if(!bad.size)console.log("no overflow (x and y)");
 else for(const [k,v] of bad) console.log(`OVERFLOW ${v[1]==="x"?"horiz":"vert"} t=${v[0]} ${v[2]}..${v[3]}  "${k.split("|")[1]}"`);
})();
