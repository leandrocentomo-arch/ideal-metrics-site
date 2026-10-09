/* Grafico setor x norma da home (09/10/2026): ao passar o mouse, acende a linha do setor e a coluna da norma.
   O desenho e estatico (SVG gerado por _ferramentas/setores.py); aqui so entra o destaque. */
(function(){
  var fig = document.querySelector('.qc-mat'); if(!fig) return;
  var linhas = fig.querySelectorAll('.li'), cols = fig.querySelectorAll('.co'), qs = fig.querySelectorAll('.q');
  function limpa(){ fig.classList.remove('hov'); [].forEach.call(fig.querySelectorAll('.on'), function(e){ e.classList.remove('on'); }); }
  function acende(setor, norma){
    limpa();
    [].forEach.call(linhas, function(l){ if(setor && l.getAttribute('data-s') === setor) l.classList.add('on'); });
    [].forEach.call(cols, function(c){ if(norma && c.getAttribute('data-n') === norma) c.classList.add('on'); });
    [].forEach.call(qs, function(q){
      var ok = (setor && q.parentNode.getAttribute('data-s') === setor) || (norma && q.getAttribute('data-n') === norma);
      if(ok) q.classList.add('on');
    });
    fig.classList.add('hov');
  }
  [].forEach.call(linhas, function(l){ l.addEventListener('mouseenter', function(){ acende(l.getAttribute('data-s'), null); }); });
  [].forEach.call(cols, function(c){ c.addEventListener('mouseenter', function(){ acende(null, c.getAttribute('data-n')); }); });
  [].forEach.call(qs, function(q){ q.addEventListener('mouseenter', function(){ acende(q.parentNode.getAttribute('data-s'), q.getAttribute('data-n')); }); });
  fig.querySelector('svg').addEventListener('mouseleave', limpa);
})();

/* 09/10/2026: a etiqueta da parede direita abre a grade na largura da pagina e fecha de novo */
(function(){
  var fig = document.getElementById('qcMat'), aba = document.getElementById('qcMatAba'); if(!fig || !aba) return;
  var linha = fig.parentNode, cauda = linha.querySelector('.qc-abre-cauda');
  var rola = fig.querySelector('.qc-mat-rola');
  /* o desenho fica sempre do tamanho que tera aberto, e a janela recolhida guarda a altura com a barra de rolagem,
     para nada mudar de tamanho nem de lugar durante a abertura */
  function medir(){
    if(window.innerWidth <= 880){ fig.style.removeProperty('--mat-w'); if(rola) rola.style.height = ''; return; }
    fig.style.setProperty('--mat-w', (linha.clientWidth - 41 - 47 - 2) + 'px');
    if(rola && !fig.classList.contains('aberto')){ rola.style.height = ''; rola.style.height = rola.offsetHeight + 'px'; }
  }
  medir();
  var tm = null; window.addEventListener('resize', function(){ clearTimeout(tm); tm = setTimeout(medir, 150); });
  aba.addEventListener('click', function(){
    var abre = !fig.classList.contains('aberto');
    if(abre && cauda){ linha.style.setProperty('--cauda-w', cauda.offsetWidth + 'px'); linha.classList.add('mat-ok'); }
    fig.classList.toggle('aberto', abre); linha.classList.toggle('mat-aberto', abre);
    aba.setAttribute('aria-expanded', abre ? 'true' : 'false');
    var r = fig.querySelector('.qc-mat-rola'); if(r) r.scrollLeft = 0;
  });
  /* recolhida de novo: solta a largura guardada quando a coluna termina de voltar */
  if(cauda) cauda.addEventListener('transitionend', function(e){
    if(e.propertyName === 'flex-basis' && !linha.classList.contains('mat-aberto')){ linha.classList.remove('mat-ok'); linha.style.removeProperty('--cauda-w'); }
  });
})();
