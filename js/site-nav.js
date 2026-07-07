/* Reveal suave do conteudo. Ideal Metrics.
   Carregado em todas as paginas que usam css/style.css. */
(function () {
  'use strict';
  if ('IntersectionObserver' in window) {
    var els = document.querySelectorAll('.content > *');
    if (els.length) {
      // pequeno stagger em lotes de 5
      els.forEach(function (el, i) {
        el.style.setProperty('--rvl-d', (i % 5) * 45 + 'ms');
      });
      var io = new IntersectionObserver(function (entries) {
        entries.forEach(function (e) {
          if (e.isIntersecting) { e.target.classList.add('in-view'); io.unobserve(e.target); }
        });
      }, { threshold: 0.04, rootMargin: '0px 0px -30px 0px' });
      els.forEach(function (el) { io.observe(el); });
    }
  } else {
    document.querySelectorAll('.content > *').forEach(function (el) { el.classList.add('in-view'); });
  }
})();
