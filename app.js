(function(){
  var P = window.PHOTOS || [];
  var esc = function(s){var d=document.createElement('div');d.textContent=s||'';return d.innerHTML;};
  var hero = document.getElementById('hero'), grid = document.getElementById('grid');
  if (P[0]) {
    hero.innerHTML = '<button data-i="0" aria-label="Open '+esc(P[0].title)+'"><img src="'+esc(P[0].file)+'" alt="'+esc(P[0].alt)+'"></button>' +
      '<p class="cap"><strong>'+esc(P[0].title)+'</strong> — '+esc(P[0].caption)+' <span class="by">Photo by Mike Kerr</span></p>';
  }
  grid.innerHTML = P.map(function(p,i){
    return '<li><button data-i="'+i+'" aria-label="Open '+esc(p.title)+'"><img loading="lazy" src="'+esc(p.thumb||p.file)+'" alt="'+esc(p.alt)+'"></button>' +
      '<div class="meta">'+esc(p.title)+'<span class="by">Photo by Mike Kerr</span></div></li>';
  }).join('');
  var lb=document.getElementById('lightbox'), img=document.getElementById('lb-img'),
      t=document.getElementById('lb-title'), c=document.getElementById('lb-cap'), cur=0, last=null;
  function show(i){ cur=(i+P.length)%P.length; var p=P[cur]; img.src=p.file; img.alt=p.alt; t.textContent=p.title; c.textContent=p.caption; }
  function open(i){ last=document.activeElement; show(i); lb.hidden=false; lb.querySelector('.lb-close').focus(); }
  function close(){ lb.hidden=true; img.src=''; if(last) last.focus(); }
  document.addEventListener('click',function(e){
    var b=e.target.closest('button[data-i]'); if(b){open(+b.dataset.i);return;}
    if(lb.hidden) return;
    if(e.target.closest('.lb-prev')) show(cur-1);
    else if(e.target.closest('.lb-next')) show(cur+1);
    else close();
  });
  document.addEventListener('keydown',function(e){
    if(lb.hidden) return;
    if(e.key==='Escape') close();
    else if(e.key==='ArrowLeft') show(cur-1);
    else if(e.key==='ArrowRight') show(cur+1);
    else if(e.key==='Tab'){ var f=lb.querySelectorAll('button'),a=f[0],z=f[f.length-1];
      if(e.shiftKey&&document.activeElement===a){e.preventDefault();z.focus();}
      else if(!e.shiftKey&&document.activeElement===z){e.preventDefault();a.focus();} }
  });
})();
