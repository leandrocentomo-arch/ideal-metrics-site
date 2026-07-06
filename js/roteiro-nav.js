/* Efeito de navegacao das paginas de carbono (roteiro) — Ideal Metrics.
   Scroll-reveal das secoes + scrollspy da barra .secnav + sombra ao rolar.
   Interacao espelhada de — CQT/cqt-smeta.html. */
(function () {
  'use strict';

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

  // 2) Scrollspy da barra de secao
  var nav = document.querySelector('.secnav');
  if (nav) {
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
          // centraliza o link ativo sem animacao (barra rolavel no mobile)
          var nr = nav.getBoundingClientRect();
          var ar = a.getBoundingClientRect();
          nav.scrollLeft += (ar.left - nr.left) - (nr.width / 2) + (ar.width / 2);
        });
      }, { rootMargin: '-30% 0px -65% 0px' });
      targets.forEach(function (t) { spy.observe(t); });
    }

    // 3) Sombra da barra ao rolar
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
})();
