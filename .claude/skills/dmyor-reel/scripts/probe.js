const puppeteer=require("puppeteer"),path=require("path");
(async()=>{
 const b=await puppeteer.launch({headless:"new",args:["--no-sandbox"]});
 const p=await b.newPage(); await p.setViewport({width:1080,height:1920,deviceScaleFactor:1});
 await p.goto("file://"+path.resolve(process.argv[2]),{waitUntil:"load"});
 await p.waitForFunction("typeof window.__seek==='function'");
 for(const t of process.argv.slice(3)){
  const r=await p.evaluate(s=>{window.__seek(+s);
    const out=[];
    document.querySelectorAll('#stage *').forEach(el=>{
      const cs=getComputedStyle(el); if(parseFloat(cs.opacity)<0.05) return;
      if(!el.textContent.trim()) return;
      if(el.children.length) return;
      const b=el.getBoundingClientRect(); if(b.width<2||b.height<2) return;
      out.push({tx:el.textContent.trim().slice(0,26),cx:Math.round(b.x+b.width/2),
        cy:Math.round(b.y+b.height/2),fs:cs.fontSize,fw:cs.fontWeight,col:cs.color});
    });
    const cam=document.getElementById('cam');
    return {t:s,cam:cam?getComputedStyle(cam).transform:null,out};
  },t);
  console.log("t="+r.t,"cam="+r.cam);
  r.out.forEach(o=>console.log(`   cx=${o.cx} cy=${o.cy} ${o.fs}/${o.fw} ${o.col}  "${o.tx}"`));
 }
 await b.close();
})();
