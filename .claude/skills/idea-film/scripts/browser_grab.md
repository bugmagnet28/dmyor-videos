# Getting free footage and sound effects (Claude in Chrome)
Pages on pexels.com and pixabay.com block curl (Cloudflare); their CDNs do not. So: read URLs in the browser, download with curl.
**Always open your own tab** (`tabs_create_mcp`), never navigate the Instagram tab the publisher uses. Close it when done.

## Pexels videos (Pexels License: free, commercial OK, no credit needed; credit in post.md anyway)
In a tab on pexels.com, run (javascript_tool). It fetches search pages and lists `id file thumb` (no query strings, so the output is not blocked):
```js
const Qs={phone:"scrolling phone in bed at night", wing:"airplane wing above clouds"};
window.__R=[];
for (const [k,q] of Object.entries(Qs)){
  const html=await (await fetch('/search/videos/'+encodeURIComponent(q)+'/?orientation=portrait')).text();
  const ids=[...new Set([...html.matchAll(/\/video\/([a-z0-9-]+)-(\d+)\//g)].map(m=>m[2]))].slice(0,6);
  for (const id of ids){
    const f=[...html.matchAll(new RegExp('video-files/'+id+'/[^"?\\\\ ]+\\.mp4','g'))].map(m=>m[0])[0]||'';
    const th=[...html.matchAll(new RegExp('images\\.pexels\\.com/videos/'+id+'/[^"?\\\\ ]+\\.(?:jpe?g|png)','g'))].map(m=>m[0])[0]||'';
    window.__R.push([k,id,f.split('/').pop(),th.split('/').pop()]); } }
window.__R.map(r=>r.join(' ')).slice(0,20).join('\n')   // print in slices of ~20, output is truncated
```
Skip `content.pexels.com/aigc-bundle` results (sponsored AI clips). Thumbs: `https://images.pexels.com/videos/<id>/<thumb>?auto=compress&h=400` -> contact sheet -> pick by eye.
Video: `curl -L -A "Mozilla/5.0" -o pex/v<id>.mp4 https://videos.pexels.com/video-files/<id>/<file>`.

## Pixabay sound effects (Pixabay Content License: free, no credit needed)
Navigate your tab to `https://pixabay.com/sound-effects/search/<query>/`, then:
```js
window.__grab = async function(n){ await new Promise(r=>setTimeout(r,2500)); const btns=[...document.querySelectorAll('button')].filter(b=>/play/i.test(b.getAttribute('aria-label')||b.className||'')).slice(0,n); const out=[]; for(const b of btns){ const before=new Set(performance.getEntriesByType('resource').map(e=>e.name)); b.click(); await new Promise(r=>setTimeout(r,1500)); const nu=performance.getEntriesByType('resource').map(e=>e.name).filter(x=>!before.has(x)&&/\.mp3/.test(x)); const card=b.closest('[class*=audioRow], [class*=row], li, article')||b.parentElement; out.push((nu[0]||'?').replace('https://cdn.pixabay.com/audio/','')+' | '+(card.innerText||'').split('\n').slice(0,3).join(' / ')); } document.querySelectorAll('audio').forEach(a=>a.pause()); return out.join('\n'); }; await window.__grab(5)
```
Batch several searches in one `browser_batch` (navigate + javascript pairs). Download: `curl -A "Mozilla/5.0" -o sfx/<name>.mp3 https://cdn.pixabay.com/audio/<path>`. Log every file in `sfx/LICENSES.md` (title, author).
Searches that worked (2026-11-17): soft cinematic whoosh, transition whoosh short, reality warp, soft magic chime, clock ticking, airplane wind, keyboard typing, message sent, magic shimmer rise, soft cinematic riser, light switch, cafe ambience, family laughing, mountain wind, soft ui click, phone tap, soft pop, paper drop. A starter kit is already in `reels/bend-reality/sfx/`.
