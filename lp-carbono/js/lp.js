/* Ideal Metrics — LP Gestão de Carbono (modelo amirco): slider, reveal, menu */
(function () {
  'use strict';

  /* ---- Hero slider (crossfade, dots + setas, autoplay) ---- */
  var slides = [].slice.call(document.querySelectorAll('.hero__slide'));
  var dots = [].slice.call(document.querySelectorAll('.hero__dots button'));
  var cur = 0, timer = null;

  function go(i) {
    if (!slides.length) return;
    cur = (i + slides.length) % slides.length;
    slides.forEach(function (s, k) { s.classList.toggle('on', k === cur); });
    dots.forEach(function (d, k) { d.classList.toggle('on', k === cur); });
  }
  function next() { go(cur + 1); }
  function prev() { go(cur - 1); }
  function restart() { if (timer) clearInterval(timer); timer = setInterval(next, 5500); }

  if (slides.length) {
    go(0); restart();
    var bn = document.querySelector('.hero__nav .nx');
    var bp = document.querySelector('.hero__nav .pv');
    if (bn) bn.addEventListener('click', function () { next(); restart(); });
    if (bp) bp.addEventListener('click', function () { prev(); restart(); });
    dots.forEach(function (d, k) { d.addEventListener('click', function () { go(k); restart(); }); });
  }

  /* ---- Menu mobile ---- */
  var burger = document.getElementById('burger');
  var nav = document.getElementById('nav');
  if (burger && nav) {
    burger.addEventListener('click', function () { nav.classList.toggle('open'); });
    nav.addEventListener('click', function (e) { if (e.target.tagName === 'A') nav.classList.remove('open'); });
  }

  /* ---- Reveal on scroll (handler robusto, sem depender de IO) ---- */
  var reveals = [].slice.call(document.querySelectorAll('.reveal'));
  function checkReveals() {
    for (var i = reveals.length - 1; i >= 0; i--) {
      var el = reveals[i];
      var r = el.getBoundingClientRect();
      if (r.top < window.innerHeight * 0.88 && r.bottom > 0) {
        el.classList.add('in');
        reveals.splice(i, 1);
      }
    }
  }
  checkReveals();
  window.addEventListener('scroll', checkReveals, { passive: true });
  window.addEventListener('resize', checkReveals);
  window.addEventListener('load', checkReveals);
  /* re-check apos reflow de webfonts/imagens (nao revela abaixo da dobra) */
  setTimeout(checkReveals, 400);
  if (document.fonts && document.fonts.ready) { document.fonts.ready.then(checkReveals); }

  /* ---- Newsletter (visual: sem backend, abre mailto) ---- */
  var nf = document.getElementById('newsForm');
  if (nf) {
    nf.addEventListener('submit', function (e) {
      e.preventDefault();
      var v = (nf.querySelector('input') || {}).value || '';
      window.location.href = 'mailto:info@cqt-br.com?subject=Assinatura%20de%20conteudo%20-%20Gestao%20de%20Carbono&body=' + encodeURIComponent('E-mail: ' + v);
    });
  }
})();
