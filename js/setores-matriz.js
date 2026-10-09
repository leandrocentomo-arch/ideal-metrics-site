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
