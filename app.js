(function(){
  var P = window.PHOTOS || [], W = [800, 1200, 1600, 2000];
  var esc = function(s){var d=document.createElement('div');d.textContent=s==null?'':String(s);return d.innerHTML.replace(/"/g,'&quot;');};
  var _s = function(t){return String(t||'').toLowerCase().replace(/[^a-z0-9]+/g,'-').replace(/^-|-$/g,'');};
  // Link id per photo (#autumn-trees); untitled/duplicate titles fall back to the file name. Mirrors tools/build.py.
  var seen = {}; P.forEach(function(p){ var s=_s(p.title); if(!s||s==='untitled'||seen[s]) s=_s(p.name); seen[s]=1; p._slug=s; });
  var slug = function(p){return p._slug;};
  var set = function(p,ext){return W.map(function(w){return 'photos/'+p.name+'-'+w+'.'+ext+' '+w+'w';}).join(', ');};
  function picture(p, sizes, attrs){
    return '<picture><source type="image/avif" srcset="'+set(p,'avif')+'" sizes="'+sizes+'">' +
      '<source type="image/webp" srcset="'+set(p,'webp')+'" sizes="'+sizes+'">' +
      '<img src="photos/'+p.name+'-1200.jpg" srcset="'+set(p,'jpg')+'" sizes="'+sizes+'" width="'+p.width+'" height="'+p.height+'" alt="'+esc(p.alt)+'" '+attrs+'></picture>';
  }
  var hero = document.getElementById('hero'), grid = document.getElementById('grid');
  if (P[0]) {
    var h = P[0], hs = 'min(100vw, calc(85vh * '+(h.width/h.height).toFixed(4)+'))';
    if (h.height > h.width) hero.classList.add('portrait');
    hero.innerHTML = '<a href="#'+slug(h)+'" data-i="0" aria-label="Open '+esc(h.title)+' full screen">'+picture(h, hs, 'fetchpriority="high" loading="eager"')+'</a>' +
      '<p class="cap"><strong>'+esc(h.title)+'</strong>'+esc(h.caption||'')+' <span class="by">Photo by Mike Kerr</span></p>';
  }
  grid.innerHTML = P.map(function(p,i){
    var ar = p.width/p.height;
    return '<li style="--ar:'+ar.toFixed(4)+'"><a href="#'+slug(p)+'" data-i="'+i+'" aria-label="Open '+esc(p.title)+'">' +
      picture(p, '(max-width: 600px) 100vw, '+Math.round(300*ar)+'px', 'loading="lazy"') +
      '</a><div class="meta">'+esc(p.title)+'<span class="by">Photo by Mike Kerr</span></div></li>';
  }).join('');

  var lb = document.getElementById('lightbox'), pic = document.getElementById('lb-pic'),
      t = document.getElementById('lb-title'), c = document.getElementById('lb-cap'), cur = 0, last = null;
  var LBS = '92vw';
  function preload(i){ var p=P[(i+P.length)%P.length]; if(!p) return; var im=new Image(); im.sizes=LBS; im.srcset=set(p, 'webp'); }
  function show(i, push){
    cur = (i+P.length)%P.length; var p = P[cur];
    pic.outerHTML = '<picture id="lb-pic">'+picture(p, LBS, '').slice(9);
    pic = document.getElementById('lb-pic');
    t.textContent = p.title; c.textContent = p.caption;
    var hash = '#'+slug(p);
    if (location.hash !== hash) history[push?'pushState':'replaceState'](null, '', hash);
    if (P.length > 1) preload(cur+1);
  }
  function open(i){ if(!P[i]) return; if(!lb.open){ last=document.activeElement; lb.showModal(); } show(i, true); lb.querySelector('.lb-close').focus(); }
  function close(){ if(lb.open) lb.close(); }
  lb.addEventListener('close', function(){
    if (location.hash) history.replaceState(null, '', location.pathname + location.search);
    if (last && last.focus) last.focus();
  });
  document.addEventListener('click', function(e){
    var a = e.target.closest('a[data-i]'); if (a) { e.preventDefault(); open(+a.dataset.i); return; }
  });
  lb.addEventListener('click', function(e){
    if (e.target.closest('.lb-prev')) show(cur-1);
    else if (e.target.closest('.lb-next')) show(cur+1);
    else if (e.target.closest('.lb-close') || e.target === lb) close();
  });
  lb.addEventListener('keydown', function(e){
    if (e.key === 'ArrowLeft') show(cur-1); else if (e.key === 'ArrowRight') show(cur+1);
  });
  var x0 = null, y0 = null;
  lb.addEventListener('touchstart', function(e){ x0=e.touches[0].clientX; y0=e.touches[0].clientY; }, {passive:true});
  lb.addEventListener('touchend', function(e){
    if (x0 === null) return; var dx=e.changedTouches[0].clientX-x0, dy=e.changedTouches[0].clientY-y0; x0=null;
    if (Math.abs(dx) > 50 && Math.abs(dx) > Math.abs(dy)) show(cur + (dx < 0 ? 1 : -1));
  });
  function fromHash(){
    var s = decodeURIComponent(location.hash.slice(1)); if (!s) { close(); return; }
    for (var i=0;i<P.length;i++) if (slug(P[i])===s) { if(!lb.open||i!==cur) open(i); return; }
  }
  window.addEventListener('hashchange', fromHash); window.addEventListener('popstate', fromHash);
  fromHash();
})();
