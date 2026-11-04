/* 04/11/2026: grade setor x norma reta, com o desenho e as medidas da home (monta.py gera o SVG com a mesma geometria do
   setores.py). Por cima dela: ficha, clique que fixa, filtro por tema e so destaque. O tema redistribui as colunas na largura. */
(function(){
  var raiz = document.getElementById('smMg'); if(!raiz) return;
  var D = JSON.parse(document.getElementById('smMdD').textContent);
  var q = function(s, r){ return [].slice.call((r || raiz).querySelectorAll(s)); };
  var svg = raiz.querySelector('svg'), cols = q('.mg-co'), linhas = q('.mg-li'), nN = cols.length, nS = linhas.length;
  var ROT = 238, FIM = 1770, TOPO = 190, LIN = 27, Y0 = 73;
  var base = cols.map(function(c){ return +c.getAttribute('data-x'); });
  var quad = cols.map(function(c){ return q('[data-s]', c); });
  var txt = cols.map(function(c){ return c.querySelector('text'); });
  var X = base.slice(), P = 20, vista = -1, foco = null, fixo = false, topoA = TOPO, linA = LIN;
  var gt = raiz.querySelector('.mg-gt'), gtT = gt.querySelector('text'), gtL = gt.querySelector('path');

  /* ----- distribuicao das colunas */
  function monta(){
    var vis = [], j;
    for(j = 0; j < nN; j++) if(vista < 0 || D.N[j].g === vista) vis.push(j);
    P = vista < 0 ? 20 : Math.min(175, (FIM - ROT - 8) / vis.length);
    var cabe = vista >= 0 && vis.every(function(n){ return D.N[n].l.length * 8 + 12 <= P; });
    /* rotulo na horizontal libera a faixa de cima: as linhas crescem e ocupam esse espaco, sem mudar a altura do bloco */
    var sobe = cabe ? 140 : 0, dl = sobe / nS, h = cabe ? 18 : 13;
    topoA = TOPO - sobe; linA = LIN + dl;
    svg.style.setProperty('--dt', -sobe + 'px');
    svg.style.setProperty('--dl', dl + 'px');
    svg.style.setProperty('--ex', ((linA - h) / 2 - 7) + 'px');
    svg.style.setProperty('--h', h + 'px');
    for(j = 0; j < nN; j++){
      var v = vis.indexOf(j), c = cols[j];
      c.classList.toggle('fora', v < 0);
      if(v < 0){ X[j] = base[j]; continue; }
      X[j] = vista < 0 ? base[j] : ROT + v * P;
      c.style.transform = 'translateX(' + X[j] + 'px)';
      c.style.setProperty('--w', (vista < 0 ? 13 : P - 7) + 'px');
      c.style.setProperty('--vx', (vista < 0 ? 9 : P / 2 - 1) + 'px');
      txt[j].style.transform = cabe ? 'translate(3.5px,' + (182 - sobe) + 'px)' : 'translate(' + (vista < 0 ? 13.5 : P / 2 + 3.5) + 'px,182px) rotate(-90deg)';
    }
    raiz.classList.toggle('tema', vista >= 0);
    gtT.textContent = vista >= 0 ? D.G[vista].n : '';
        gtL.setAttribute('d', 'M' + ROT + ' 17H' + (ROT + vis.length * P - 7));
  }

  /* ----- acender */
  function acende(f){
    foco = f;
    svg.classList.toggle('hov', !!f);
    linhas.forEach(function(l, i){ l.classList.toggle('on', !!f && f.s === i); });
    cols.forEach(function(c, j){
      var fn = !!f && f.n === j, fg = !!f && f.g !== undefined && D.N[j].g === f.g;
      c.classList.toggle('on', fn || fg);
      quad[j].forEach(function(r){
        var i = +r.getAttribute('data-s'), fs = !!f && f.s === i;
        r.classList.toggle('on', fs || fn || fg);
        r.classList.toggle('cruz', fs && fn);
      });
    });
    ficha();
  }

  /* ----- ficha */
  var el = function(id){ return raiz.querySelector('[data-f="' + id + '"]'); };
  var fS = el('setor'), fN = el('norma'), fR = el('rev'), fT = el('tit'), fL = el('rel'), lS = el('ls'), lN = el('ln'), bS = el('solta'), dica = el('dica');
  function poe(n, v){ if(n.textContent !== v){ n.textContent = v; n.title = v; } }
  function ficha(){
    var f = foco || {}, s = f.s !== undefined ? D.S[f.s] : null, n = f.n !== undefined ? D.N[f.n] : null, g = f.g !== undefined ? D.G[f.g] : null, rel = '';
    poe(fS, s ? s.n : '');
    poe(fN, n ? n.l : g ? g.n : '');
    poe(fR, n ? n.rev : '');
    poe(fT, n ? n.tit : s ? s.r : g ? D.N.filter(function(x){ return x.g === f.g; }).map(function(x){ return x.l; }).join(' · ') : '');
    if(s && n){ var k = +D.M[f.s].charAt(f.n); rel = k === 2 ? 'Destaque do setor' : k === 1 ? 'Vale para qualquer setor' : 'Sem relação na grade'; }
    else if(n) rel = D.S.every(function(_, i){ return +D.M[i].charAt(f.n) > 0; }) ? 'Vale para qualquer setor' : 'Destaque em setores específicos';
    poe(fL, rel);
    lS.style.visibility = s ? 'visible' : 'hidden'; if(s) lS.href = s.p;
    lN.style.visibility = n && n.p ? 'visible' : 'hidden'; if(n && n.p) lN.href = n.p;
    bS.hidden = !fixo; dica.hidden = fixo;
  }

  /* ----- onde esta o ponteiro: a conta sai das posicoes atuais, sem um alvo no DOM para cada uma das 630 casas */
  function acerta(e){
    var m = svg.getScreenCTM(); if(!m) return null;
    var p = new DOMPoint(e.clientX, e.clientY).matrixTransform(m.inverse()), x = p.x, y = p.y - Y0, j, col = -1;
    if(x >= ROT) for(j = 0; j < nN; j++){
      if((vista < 0 || D.N[j].g === vista) && x >= X[j] && x < X[j] + P){ col = j; break; }
    }
    var lin = y >= topoA && y < topoA + nS * linA ? Math.floor((y - topoA) / linA) : -1;
    if(lin >= 0 && col >= 0) return {s:lin, n:col};
    if(lin >= 0 && x < ROT) return {s:lin};
    if(col >= 0 && y >= 22 && y < topoA) return {n:col};
    if(col >= 0 && y < 22 && vista < 0) return {g:D.N[col].g};
    return null;
  }
  var igual = function(a, b){ return (!a && !b) || (a && b && a.s === b.s && a.n === b.n && a.g === b.g); };
  svg.addEventListener('pointermove', function(e){
    var a = acerta(e);
    svg.style.cursor = a ? 'pointer' : 'default';
    if(fixo || e.pointerType === 'touch') return;
    if(!igual(a, foco)) acende(a);
  });
  svg.addEventListener('pointerleave', function(){ if(!fixo && foco) acende(null); });
  svg.addEventListener('click', function(e){
    var a = acerta(e);
    if(a && a.g !== undefined){ fixo = false; poeVista(a.g); acende(null); return; }
    if(!a){ fixo = false; acende(null); return; }
    if(fixo && igual(a, foco)){ fixo = false; acende(a); return; }
    fixo = true; acende(a);
  });
  bS.addEventListener('click', function(){ fixo = false; acende(null); });
  svg.addEventListener('keydown', function(e){
    var f = foco && foco.s !== undefined && foco.n !== undefined ? foco : null, vis = [], j;
    for(j = 0; j < nN; j++) if(vista < 0 || D.N[j].g === vista) vis.push(j);
    var s = f ? f.s : 0, p = f ? vis.indexOf(f.n) : 0;
    if(e.key === 'ArrowDown') s = Math.min(nS - 1, s + (f ? 1 : 0));
    else if(e.key === 'ArrowUp') s = Math.max(0, s - (f ? 1 : 0));
    else if(e.key === 'ArrowRight') p = Math.min(vis.length - 1, p + (f ? 1 : 0));
    else if(e.key === 'ArrowLeft') p = Math.max(0, p - (f ? 1 : 0));
    else if(e.key === 'Enter' && foco){ fixo = !fixo; ficha(); e.preventDefault(); return; }
    else return;
    e.preventDefault();
    acende({s:s, n:vis[p]});
  });
  document.addEventListener('keydown', function(e){ if(e.key === 'Escape' && (fixo || foco)){ fixo = false; acende(null); } });

  /* ----- temas e modo */
  var temas = raiz.querySelector('.mg-temas'), bts = q('button[data-g]', temas), desl = temas.querySelector('.md-desl');
  function moveDesl(){
    var b = temas.querySelector('button[data-g][aria-selected=true]'); if(!b) return;
    desl.style.width = b.offsetWidth + 'px'; desl.style.height = b.offsetHeight + 'px';
    desl.style.transform = 'translate(' + b.offsetLeft + 'px,' + b.offsetTop + 'px)';
  }
  function poeVista(v){
    vista = v;
    bts.forEach(function(b){ b.setAttribute('aria-selected', +b.getAttribute('data-g') === v); });
    moveDesl(); monta();
  }
  bts.forEach(function(b){
    b.addEventListener('click', function(){ fixo = false; poeVista(+b.getAttribute('data-g')); acende(null); });
    b.addEventListener('mouseenter', function(){ var v = +b.getAttribute('data-g'); if(!fixo && v >= 0 && vista < 0) acende({g:v}); });
    b.addEventListener('mouseleave', function(){ if(!fixo && foco && foco.g !== undefined) acende(null); });
  });
  var modo = raiz.querySelector('.md-modo'), bm = q('button', modo);
  bm.forEach(function(b, n){
    b.addEventListener('click', function(){
      bm.forEach(function(o){ o.setAttribute('aria-selected', o === b); });
      modo.style.setProperty('--i', n);
      raiz.classList.toggle('so-destaque', n === 1);
    });
  });

  /* ----- entrada: as colunas surgem da esquerda para a direita toda vez que a grade entra na tela */
  if('IntersectionObserver' in window){
    new IntersectionObserver(function(es){
      es.forEach(function(e){
        if(e.isIntersecting) raiz.classList.add('vis');
        else raiz.classList.remove('vis');
      });
    }, {threshold:0}).observe(svg);
  } else raiz.classList.add('vis');

  monta(); moveDesl(); ficha();
  window.addEventListener('resize', moveDesl);
  if(document.fonts && document.fonts.ready) document.fonts.ready.then(moveDesl);
})();
