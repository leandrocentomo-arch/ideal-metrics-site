/* 04/11/2026: paginas inteiras (modelos 33 a 41). Cartao, circulo e linha com o mesmo data-i acendem juntos; o acento desliza para o escolhido. */
(function(){
  var q = function(s, r){ return [].slice.call((r || document).querySelectorAll(s)); };
  q('[data-pg]').forEach(function(raiz){
    var itens = q('[data-i]', raiz), cur = raiz.querySelector('.pc-cur');
    function poeCur(){
      if(!cur || getComputedStyle(cur).display === 'none') return;
      var c = raiz.querySelector('.pc.on'); if(!c) return;
      cur.style.width = c.offsetWidth + 'px';
      cur.style.height = c.offsetHeight + 'px';
      cur.style.transform = 'translate(' + c.offsetLeft + 'px,' + c.offsetTop + 'px)';
    }
    function marca(n){
      itens.forEach(function(o){ o.classList.toggle('on', o.getAttribute('data-i') === n); });
      poeCur();
    }
    itens.forEach(function(o){
      var n = o.getAttribute('data-i');
      ['mouseenter', 'focusin', 'click'].forEach(function(ev){ o.addEventListener(ev, function(){ marca(n); }); });
    });
    marca(raiz.getAttribute('data-pg'));
    window.addEventListener('resize', poeCur);
    if(document.fonts && document.fonts.ready) document.fonts.ready.then(poeCur);
  });
  /* entrada a cada vez que a pagina entra na tela; o atraso segue a ordem dos cartoes */
  q('.sm-pg .pg-c').forEach(function(c){
    q(':scope > .pc, :scope > .pg-ac, :scope > .pg-li > *', c).forEach(function(o, k){ o.style.setProperty('--o', k); });
    if('IntersectionObserver' in window) new IntersectionObserver(function(es){
      es.forEach(function(e){ c.classList.toggle('vis', e.isIntersecting); });
    }, {threshold:0}).observe(c);
  });
})();
