/* Menu lateral (drawer) + reveal suave do conteudo. Ideal Metrics.
   Carregado em todas as paginas que usam css/style.css. */
(function () {
  'use strict';

  // ---- Menu lateral ----
  var toggle = document.getElementById('menuToggle');
  var drawer = document.getElementById('siteDrawer');
  var overlay = document.getElementById('drawerOverlay');
  var closeBtn = document.getElementById('drawerClose');
  var overlayTimer = null;

  // contem o foco e o leitor de tela no drawer: o resto da pagina fica inert
  function setPageInert(on) {
    if (!('inert' in HTMLElement.prototype)) return;
    Array.prototype.forEach.call(document.body.children, function (el) {
      if (el === drawer || el === overlay || el.tagName === 'SCRIPT') return;
      el.inert = on;
    });
  }

  function openDrawer() {
    clearTimeout(overlayTimer);
    drawer.classList.add('open');
    overlay.hidden = false;
    // forca reflow pra transicao do overlay rodar
    void overlay.offsetHeight;
    overlay.classList.add('open');
    document.body.classList.add('drawer-open');
    toggle.setAttribute('aria-expanded', 'true');
    drawer.setAttribute('aria-hidden', 'false');
    setPageInert(true);
    if (closeBtn) closeBtn.focus();
  }
  function closeDrawer() {
    setPageInert(false);
    toggle.focus(); // devolve o foco ANTES de esconder (evita aviso de aria-hidden com foco)
    drawer.classList.remove('open');
    overlay.classList.remove('open');
    document.body.classList.remove('drawer-open');
    toggle.setAttribute('aria-expanded', 'false');
    drawer.setAttribute('aria-hidden', 'true');
    overlayTimer = setTimeout(function () { overlay.hidden = true; }, 320);
  }
  if (toggle && drawer && overlay) {
    toggle.addEventListener('click', openDrawer);
    overlay.addEventListener('click', closeDrawer);
    if (closeBtn) closeBtn.addEventListener('click', closeDrawer);
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && drawer.classList.contains('open')) closeDrawer();
    });
  }

  // ---- Reveal suave dos blocos de conteudo ----
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
