/* 04/11/2026: comportamento da 2a rodada dos modelos. Fotos no motor da trama, com o contrato de sempre: a peca liga
   perto da tela e e destruida ao sair, porque o navegador segura poucos contextos WebGL. */
(function(){
  var q = function(s, r){ return [].slice.call((r || document).querySelectorAll(s)); };

  /* seletor de acento da prova */
  var guarda = null;
  try { guarda = localStorage.getItem('sm-acento'); } catch(e){}
  var bar = document.createElement('div');
  bar.className = 'sm-acento';
  bar.innerHTML = '<span>Acento</span><div class="sm-abas" role="tablist" aria-label="Cor de acento" style="--n:3"><i class="sm-desl"></i>' +
    '<button type="button" data-a="azul">Azul</button><button type="button" data-a="celeste">Celeste</button><button type="button" data-a="laranja">Laranja</button></div>';
  document.body.appendChild(bar);
  var abasAc = bar.querySelector('.sm-abas'), btsAc = q('button', abasAc);
  function acento(nome){
    var i = 0;
    btsAc.forEach(function(b, n){ var on = b.getAttribute('data-a') === nome; b.setAttribute('aria-selected', on); if(on) i = n; });
    abasAc.style.setProperty('--i', i);
    document.body.setAttribute('data-acento', nome);
    try { localStorage.setItem('sm-acento', nome); } catch(e){}
  }
  btsAc.forEach(function(b){ b.addEventListener('click', function(){ acento(b.getAttribute('data-a')); }); });
  acento(['azul','celeste','laranja'].indexOf(guarda) >= 0 ? guarda : 'azul');

  /* fotos */
  var ditherVivo = window.ditherVivo;
  if(ditherVivo && 'IntersectionObserver' in window){
    var OFICIAL = [[21.2,50.9,80.6],[24.2,56.2,88.1],[103.0,146.1,189.4],[250,249,245]];
    q('.sm-quadro').forEach(function(raiz){
      var im = raiz.querySelector('img[data-lum]'); if(!im) return;
      var gl = null, dentro = false;
      function atualiza(){
        if(dentro && !gl) gl = ditherVivo({brilhoTom:0.35, gama:0.88, ctr:1.55, escuro:0.35, lavaRepouso:0.12, raiz:raiz,
          planos:[{el:raiz, lum:im.getAttribute('data-lum'), tom:null}], classeCanvas:'vv-gl', revelar:'visivel', cores:OFICIAL,
          pincel:.7, zoomHover:1.035});
        else if(!dentro && gl){ gl.destruir(); gl = null; }
      }
      new IntersectionObserver(function(es){ es.forEach(function(e){ dentro = e.isIntersecting; }); atualiza(); },
        {rootMargin:'30% 0px 30% 0px'}).observe(raiz);
    });
  }

  /* 01 ficha: abas com deslize; a pilha guarda a altura da maior ficha */
  var fc = document.getElementById('smFc'), fp = document.getElementById('smFcP');
  if(fc && fp){
    var bts = q('button', fc);
    bts.forEach(function(b, i){
      b.addEventListener('click', function(){
        bts.forEach(function(o){ o.setAttribute('aria-selected', o === b); });
        fc.style.setProperty('--i', i);
        q('.fc-p', fp).forEach(function(p){ p.classList.toggle('on', p.getAttribute('data-t') === b.getAttribute('data-t')); });
      });
    });
  }

  /* 06 cartoes: o acento desliza para o cartao sob o mouse */
  var c3 = document.getElementById('smC3');
  if(c3){
    var cs = q('.c3f-c', c3);
    var marca = function(i){ c3.style.setProperty('--i', i); cs.forEach(function(c, n){ c.classList.toggle('on', n === i); }); };
    cs.forEach(function(c, i){ c.addEventListener('mouseenter', function(){ marca(i); }); });
    marca(0);
  }

  /* 10 indice: losango unico segue o mouse */
  var ix = document.getElementById('smIx');
  if(ix){
    var cur = ix.querySelector('.ix-cur');
    q('a', ix).forEach(function(a){
      a.addEventListener('mouseenter', function(){ cur.style.setProperty('--y', (a.offsetTop + a.offsetHeight/2 - 5) + 'px'); cur.style.opacity = 1; });
    });
    ix.addEventListener('mouseleave', function(){ cur.style.opacity = 0; });
  }

  /* 13 planta: marcador e lista acendem juntos */
  var pl = document.getElementById('smPl'), pll = document.getElementById('smPlL');
  if(pl && pll){
    var todos = q('[data-p]', pl).concat(q('li', pll));
    var acende = function(n){ todos.forEach(function(o){ o.classList.toggle('on', o.getAttribute('data-p') === n); }); };
    todos.forEach(function(o){
      o.addEventListener('mouseenter', function(){ acende(o.getAttribute('data-p')); });
      o.addEventListener('focus', function(){ acende(o.getAttribute('data-p')); });
    });
    acende('1');
  }

  /* 28 perguntas: abre uma por vez */
  q('#smPq .pq-i').forEach(function(it){
    var b = it.querySelector('button');
    b.addEventListener('click', function(){
      var abre = !it.classList.contains('aberto');
      q('#smPq .pq-i').forEach(function(o){ o.classList.remove('aberto'); o.querySelector('button').setAttribute('aria-expanded', 'false'); });
      if(abre){ it.classList.add('aberto'); b.setAttribute('aria-expanded', 'true'); }
    });
  });
})();
