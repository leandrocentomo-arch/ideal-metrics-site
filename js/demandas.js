/* js/demandas.js (19/10/2026): os scripts do painel Demandas, que saiu da home para Todos os servicos: a entrada no
   scroll e a folha no motor da trama (com a medida dos dois baloes da direita). O titulo digitado continua no js/busca.js. */
// ===== painel Demandas: entrada no scroll =====
// Sem biblioteca. O original usa GSAP + ScrollTrigger com start "top 85%",
// sem scrub, uma vez so. O equivalente e um IntersectionObserver com a base
// da raiz recolhida em 15% e unobserve no primeiro disparo. O movimento em si
// e todo CSS: o script so poe classes.
(function(){
  var sec = document.getElementById('demandas');
  if(!sec) return;
  // os dois portoes. Saindo aqui, .dm-js nunca entra e NADA e escondido.
  if(!('IntersectionObserver' in window)) return;
  if(window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;

  // indice de cada pilula, para o atraso de .1s em cascata
  [].forEach.call(sec.querySelectorAll('.dm-lista > .dm-sobe'), function(li, i){
    li.style.setProperty('--dm-i', i);
  });

  sec.classList.add('dm-js');

  /* O foco de teclado tambem revela. As nove pilulas sao links desde a carga, mas
     com .dm-js ficavam em opacity:0 (o <li> inteiro, entao o contorno de
     :focus-visible sumia junto) ate o observador falar. Com a lista logo abaixo
     da linha de 85% da janela o navegador nao rola ao focar, e o Tab caia em
     links invisiveis. */
  sec.addEventListener('focusin', function(){
    [].forEach.call(sec.querySelectorAll('[data-dm-entra]'), function(a){ a.classList.add('dm-on'); io.unobserve(a); });
  }, {once:true});

  var vivo = false; // o observer ja falou pelo menos uma vez?
  var io = new IntersectionObserver(function(es){
    vivo = true;
    es.forEach(function(e){
      // bottom < 0: a pagina abriu ja rolada para baixo (ancora, voltar do
      // navegador) e a peca ficou ACIMA da tela. O ScrollTrigger trataria
      // como "ja passou"; aqui tambem, senao ela ficaria oculta ate alguem
      // voltar rolando.
      if(e.isIntersecting || e.boundingClientRect.bottom < 0){
        e.target.classList.add('dm-on');
        io.unobserve(e.target);
      }
    });
  }, {rootMargin:'0px 0px -15% 0px', threshold:0});

  // cada peca tem o proprio gatilho (etiqueta, titulo, lista, ilustracao e
  // sonda das barras). No telefone o painel e uma coluna alta: com gatilho
  // unico a lista animaria fora da tela.
  [].forEach.call(sec.querySelectorAll('[data-dm-entra]'), function(a){ io.observe(a); });

  // rede de seguranca. Todo observer da um primeiro aviso logo depois do
  // observe(), com a peca dentro ou fora da tela. Se em 1,5s de aba VISIVEL
  // ele nao falou, o navegador nao esta entregando o observer e a secao
  // ficaria apagada para sempre: devolve tudo ao estado visivel. Aba aberta em
  // segundo plano nao conta tempo (ali o observer dorme de proposito).
  function vigia(){
    if(vivo) return;
    if(document.visibilityState === 'hidden'){
      document.addEventListener('visibilitychange', function volta(){
        document.removeEventListener('visibilitychange', volta);
        vigia();
      });
      return;
    }
    setTimeout(function(){
      if(vivo) return;
      if(document.visibilityState === 'hidden'){ vigia(); return; }
      io.disconnect();
      sec.classList.remove('dm-js');
    }, 1500);
  }
  vigia();

  // fim da subida: solta o transform e o will-change. O filtro por .dm-sobe
  // deixa de fora o transitionend do texto da pilula no hover.
  sec.addEventListener('transitionend', function(e){
    if(e.propertyName === 'transform' && e.target.classList && e.target.classList.contains('dm-sobe')){
      e.target.classList.add('dm-fim');
    }
  });
})();

(function(){ if(!window.ditherVivo) return;
  /* ---------------- a folha do painel Demandas ----------------
     15/10/2026: os dois baloes da direita so aparecem se cabem inteiros antes da coluna das pilulas; e a folha
     (o desenho de antes de 15/10, img/demandas-folha-*) no motor da trama, como as fotos. */
  (function(){
    var arte = document.querySelector('.dm-arte'), col = document.querySelector('.dm-coluna');
    if(arte && col){
      var dir = [].slice.call(arte.querySelectorAll('.dm-svg--larga .dm-tag--dir'));
      var mede = function(){
        arte.classList.remove('dm-dir-nao-cabe');
        var lim = col.getBoundingClientRect().left - 12, nao = false;
        dir.forEach(function(g){ var r = g.getBoundingClientRect(); if(r.width && r.right > lim) nao = true; });
        arte.classList.toggle('dm-dir-nao-cabe', nao);
      };
      mede(); addEventListener('resize', mede); addEventListener('load', mede);
    }
    var folha = document.querySelector('.dm-trama') || document.querySelector('.dm-folha-foto'); if(!folha) return;   /* 19/10/2026: a trama na arte inteira */
    var im = folha.querySelector('img'); if(!im) return;
    window.ditherVivo({brilhoTom:0.35, gama:0.88, ctr:1.55, escuro:0.35, lavaRepouso:0.12, raiz:folha, planos:[{el:folha, lum:im.getAttribute('data-lum')}], classeCanvas:'dm-gl', revelar:'visivel',
      cores:[[21.2,50.9,80.6],[24.2,56.2,88.1],[103.0,146.1,189.4],[250,249,245]], pincel:.5, respiro:.008, pixMul:2.2});
  })();
})();
