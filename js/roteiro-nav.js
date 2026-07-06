/* Efeito de navegacao das paginas de carbono (roteiro) — Ideal Metrics.
   Scroll-reveal das secoes + scrollspy da barra .secnav + sombra ao rolar.
   Interacao espelhada de — CQT/cqt-smeta.html. */
(function () {
  'use strict';

  // Fallback: sem IntersectionObserver, revela tudo (nao deixa conteudo oculto)
  if (!('IntersectionObserver' in window)) {
    document.querySelectorAll('.rot-sec').forEach(function (s) { s.classList.add('in-view'); });
    return;
  }

  // 1) Scroll-reveal das secoes
  var secs = document.querySelectorAll('.rot-sec');
  if (secs.length) {
    var reveal = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) {
          e.target.classList.add('in-view');
          reveal.unobserve(e.target);
        }
      });
    }, { threshold: 0.06, rootMargin: '0px 0px -40px 0px' });
    secs.forEach(function (s) { reveal.observe(s); });
  }

  // 2) Scrollspy da nav de secao — barra do topo (.secnav) OU rail lateral (.rail)
  var nav = document.querySelector('.secnav') || document.querySelector('.rail');
  if (nav) {
    var isBar = nav.classList.contains('secnav'); // barra horizontal do topo
    var links = nav.querySelectorAll('a');
    var targets = document.querySelectorAll('.rot-sec[id]');
    var activeId = null;
    if (targets.length) {
      var spy = new IntersectionObserver(function (entries) {
        entries.forEach(function (e) {
          if (!e.isIntersecting) return;
          var id = e.target.id;
          if (id === activeId) return;
          activeId = id;
          links.forEach(function (l) { l.classList.remove('active'); });
          var a = nav.querySelector('a[href="#' + id + '"]');
          if (!a) return;
          a.classList.add('active');
          if (isBar) {
            // centraliza o link ativo na barra horizontal (rolavel no mobile)
            var nr = nav.getBoundingClientRect();
            var ar = a.getBoundingClientRect();
            nav.scrollLeft += (ar.left - nr.left) - (nr.width / 2) + (ar.width / 2);
          }
        });
      }, { rootMargin: '-30% 0px -65% 0px' });
      targets.forEach(function (t) { spy.observe(t); });
    }

    // 3) Sombra da barra do topo ao rolar (so a .secnav tem sombra)
    if (isBar) {
      var ticking = false;
      window.addEventListener('scroll', function () {
        if (ticking) return;
        ticking = true;
        requestAnimationFrame(function () {
          nav.classList.toggle('scrolled', window.scrollY > 80);
          ticking = false;
        });
      }, { passive: true });
    }
  }
})();
