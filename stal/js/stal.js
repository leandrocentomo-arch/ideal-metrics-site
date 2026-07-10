/* Ideal Metrics — esquema STÅL: header sticky, reveal, menu mobile */
(function () {
  'use strict';

  // Header solido ao rolar
  var hdr = document.getElementById('hdr');
  function onScroll() { if (hdr) hdr.classList.toggle('scrolled', window.scrollY > 60); }
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  // Menu mobile
  var burger = document.getElementById('burger');
  var nav = document.getElementById('nav');
  if (burger && nav) {
    burger.addEventListener('click', function () {
      var open = nav.style.display === 'flex';
      nav.style.display = open ? '' : 'flex';
      nav.style.position = 'absolute';
      nav.style.top = '100%';
      nav.style.left = '0';
      nav.style.right = '0';
      nav.style.flexDirection = 'column';
      nav.style.gap = '0';
      nav.style.background = '#fff';
      nav.style.padding = open ? '' : '10px 22px 18px';
      nav.style.boxShadow = open ? '' : '0 12px 30px rgba(0,0,0,0.1)';
      [].forEach.call(nav.querySelectorAll('a'), function (a) { a.style.color = '#101010'; a.style.padding = '10px 0'; });
    });
  }

  // Reveal ao rolar
  if ('IntersectionObserver' in window) {
    var els = document.querySelectorAll('.reveal');
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); }
      });
    }, { threshold: 0.08, rootMargin: '0px 0px -40px 0px' });
    els.forEach(function (el) { io.observe(el); });
  } else {
    document.querySelectorAll('.reveal').forEach(function (el) { el.classList.add('in'); });
  }
})();
