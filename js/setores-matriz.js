/* Grafico setor x norma da home (09/10/2026): ao passar o mouse, acende a linha do setor e a coluna da norma.
   O desenho e estatico (SVG gerado por _ferramentas/setores.py); aqui so entra o destaque. */
(function(){
  var fig = document.querySelector('.qc-mat'); if(!fig) return;
  var linhas = fig.querySelectorAll('.li'), cols = fig.querySelectorAll('.co'), qs = fig.querySelectorAll('.q');
  var linhaInfo = document.getElementById('qcMatInfo');
  function mostra(norma){
    if(!linhaInfo) return;
    linhaInfo.textContent = '';
    if(!norma) return;
    var c = fig.querySelector('.co[data-n="' + norma + '"]'); if(!c) return;
    var b = document.createElement('b'); b.textContent = c.getAttribute('data-rev');
    var sp = document.createElement('span'); sp.textContent = '  ·  ' + c.getAttribute('data-tit');
    linhaInfo.appendChild(b); linhaInfo.appendChild(sp);
  }
  function limpa(){ mostra(null); fig.classList.remove('hov'); [].forEach.call(fig.querySelectorAll('.on'), function(e){ e.classList.remove('on'); }); }
  function acende(setor, norma){
    limpa();
    [].forEach.call(linhas, function(l){ if(setor && l.getAttribute('data-s') === setor) l.classList.add('on'); });
    [].forEach.call(cols, function(c){ if(norma && c.getAttribute('data-n') === norma) c.classList.add('on'); });
    [].forEach.call(qs, function(q){
      var ok = (setor && q.parentNode.getAttribute('data-s') === setor) || (norma && q.getAttribute('data-n') === norma);
      if(ok) q.classList.add('on');
    });
    fig.classList.add('hov');
    mostra(norma);
  }
  [].forEach.call(linhas, function(l){ l.addEventListener('mouseenter', function(){ acende(l.getAttribute('data-s'), null); }); });
  [].forEach.call(cols, function(c){ c.addEventListener('mouseenter', function(){ acende(null, c.getAttribute('data-n')); }); });
  [].forEach.call(qs, function(q){ q.addEventListener('mouseenter', function(){ acende(q.parentNode.getAttribute('data-s'), q.getAttribute('data-n')); }); });
  fig.querySelector('svg').addEventListener('mouseleave', limpa);
})();

/* 09/10/2026: a etiqueta da parede direita abre a grade na largura da pagina e fecha de novo */
(function(){
  var fig = document.getElementById('qcMat'), aba = document.getElementById('qcMatAba'); if(!fig || !aba) return;
  var linha = fig.parentNode, cauda = linha.querySelector('.qc-abre-texto');   /* 10/10: a coluna que fecha e a da frase */
  var rola = fig.querySelector('.qc-mat-rola');
  /* o desenho fica sempre do tamanho que tera aberto, e a janela recolhida guarda a altura com a barra de rolagem,
     para nada mudar de tamanho nem de lugar durante a abertura */
  function medir(){
    if(window.innerWidth <= 880){ fig.style.removeProperty('--mat-w'); if(rola) rola.style.height = ''; return; }
    fig.style.setProperty('--mat-w', (linha.clientWidth - 41 - 47 - 2) + 'px');
    /* 19/10/2026: a altura soma a da barra horizontal (no Windows ela ocupa ~17 px dentro da caixa) e 10 px de folga, para
       nunca aparecer a barra vertical */
    if(rola && !fig.classList.contains('aberto')){ rola.style.height = ''; rola.style.height = (rola.offsetHeight + (rola.offsetHeight - rola.clientHeight) + 10) + 'px'; }
  }
  medir();
  window.addEventListener('load', medir);   /* 19/10/2026: mede de novo com as fontes carregadas */
  var tm = null; window.addEventListener('resize', function(){ clearTimeout(tm); tm = setTimeout(medir, 150); });
  /* 13/10/2026: a altura da grade vai para --mat-h; o bloco da frase Construimos (.qc-chega) tem essa altura, para a grade
     (sticky) so se soltar quando a frase chegar ao alto da coluna */
  function alturaGrade(){ linha.style.setProperty('--mat-h', fig.offsetHeight + 'px'); }
  alturaGrade();
  if('ResizeObserver' in window) new ResizeObserver(alturaGrade).observe(fig); else window.addEventListener('resize', alturaGrade);
  function guarda(){   /* a coluna da frase guarda a largura de recolhida, para o texto nao reflutuar enquanto fecha */
    if(cauda && !linha.classList.contains('mat-ok')){ linha.style.setProperty('--cauda-w', cauda.offsetWidth + 'px'); linha.classList.add('mat-ok'); }
  }
  function solta(){ linha.classList.remove('mat-ok'); linha.style.removeProperty('--cauda-w'); }
  function poe(abre){
    if(abre) guarda();
    fig.classList.toggle('aberto', abre); linha.classList.toggle('mat-aberto', abre);
    aba.setAttribute('aria-expanded', abre ? 'true' : 'false');
    if(abre && rola) rola.scrollLeft = 0;
  }
  var arrastouEm = 0;
  aba.addEventListener('click', function(){
    if(Date.now() - arrastouEm < 400) return;   /* o clique que fecha um arrasto nao conta */
    poe(!fig.classList.contains('aberto'));
  });
  /* recolhida de novo: solta a largura guardada quando a coluna termina de voltar */
  if(cauda) cauda.addEventListener('transitionend', function(e){
    if(e.propertyName === 'flex-basis' && !linha.classList.contains('mat-aberto')) solta();
  });

  /* 12/10/2026: «seria possivel fazer com que a tabela abrisse tambem arrastando a aba com o cursor do mouse?»
     A aba vai junto com o ponteiro: a grade cresce (ou encolhe) e a coluna da frase fecha (ou abre) na mesma medida,
     sem transicao. Ao soltar, a grade termina o caminho com a transicao de sempre (0,8 s): abre se passou de 25% do
     curso partindo de recolhida, fecha se voltou mais de 25% partindo de aberta. Sem mover (menos de 5 px) e clique. */
  var arr = null;
  /* 13/10/2026: «quando estou empurrando a tabela de volta, a frase aparece embaixo». A linha tem vao de 40 px e a soma
     grade + vao + margem + coluna fechava na largura exata da linha, sem folga; o clientWidth arredonda (linha de
     1385,53 px dava 1386) e, com meio pixel a mais, «O que fazemos» descia para baixo da grade durante o arrasto.
     Agora a largura e a exata (getBoundingClientRect) e a coluna fica com o que sobra da linha, menos 1 px de folga. */
  function medidas(){
    var L = linha.getBoundingClientRect().width;
    return {L: L, fechada: L * .42 - 40, aberta: L - 41, frase: L * .58 - 20};
  }
  function arrasta(p){
    var m = arr.m, f = m.fechada + p * (m.aberta - m.fechada), mg = 20 * (1 - p);
    fig.style.flexBasis = f + 'px';
    if(cauda){
      cauda.style.flexBasis = Math.max(0, Math.min(m.frase * (1 - p), m.L - 40 - f - mg - 1)) + 'px';
      cauda.style.marginRight = mg + 'px'; cauda.style.opacity = String(1 - p);   /* 25/10/2026: a frase fica a esquerda da grade */
    }
    arr.p = p;
  }
  function limpa(){
    fig.style.flexBasis = '';
    if(cauda){ cauda.style.flexBasis = ''; cauda.style.marginRight = ''; cauda.style.opacity = ''; }
  }
  aba.addEventListener('pointerdown', function(e){
    if(e.button !== 0 || window.innerWidth <= 880) return;
    arr = {x0: e.clientX, id: e.pointerId, aberto: fig.classList.contains('aberto'), ativo: false, p: 0};
    try { aba.setPointerCapture(e.pointerId); } catch(er){}   /* ja no toque: a aba tem 39 px e o primeiro passo do mouse sai dela */
  });
  aba.addEventListener('pointermove', function(e){
    if(!arr) return;
    var dx = arr.x0 - e.clientX;   /* 25/10/2026: a grade esta a direita e abre para a esquerda: puxar a etiqueta para a esquerda abre */
    if(!arr.ativo){
      if(Math.abs(dx) < 5) return;
      arr.ativo = true; arr.m = medidas();
      guarda();
      if(!arr.aberto && rola) rola.scrollLeft = 0;
      linha.classList.add('mat-arrasta');
    }
    var p = (arr.aberto ? 1 : 0) + dx / (arr.m.aberta - arr.m.fechada);
    arrasta(Math.max(0, Math.min(1, p)));
    e.preventDefault();
  });
  function fim(){
    if(!arr) return;
    var a = arr; arr = null;
    if(!a.ativo) return;
    arrastouEm = Date.now();
    var abre = a.aberto ? a.p > .75 : a.p > .25;
    linha.classList.remove('mat-arrasta');
    void linha.offsetWidth;            /* as transicoes voltam antes de soltar os valores do arrasto */
    limpa(); poe(abre);
    /* se a grade ja estava no fim do caminho nao ha transicao, e o transitionend nao vem: solta a largura aqui */
    if(!abre) setTimeout(function(){ if(!linha.classList.contains('mat-aberto')) solta(); }, 900);
  }
  aba.addEventListener('pointerup', fim);
  aba.addEventListener('pointercancel', fim);
  aba.addEventListener('lostpointercapture', fim);
})();
