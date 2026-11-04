/* 03/11/2026: comportamento dos 30 modelos de secao. Fotos no motor da trama com o contrato de sempre: a peca liga
   perto da tela e e destruida ao sair, porque o navegador segura poucos contextos WebGL. */
(function(){
  var ditherVivo = window.ditherVivo;
  if(ditherVivo && 'IntersectionObserver' in window){
    var OFICIAL = [[21.2,50.9,80.6],[24.2,56.2,88.1],[103.0,146.1,189.4],[250,249,245]];
    [].forEach.call(document.querySelectorAll('.sm-quadro'), function(raiz){
      var im = raiz.querySelector('img[data-lum]'); if(!im) return;
      var gl = null, dentro = false;
      function atualiza(){
        if(dentro && !gl) gl = ditherVivo({brilhoTom:0.35, gama:0.88, ctr:1.55, escuro:0.35, lavaRepouso:0.12, raiz:raiz,
          planos:[{el:raiz, lum:im.getAttribute('data-lum'), tom:null}], classeCanvas:'vv-gl', revelar:'visivel', cores:OFICIAL,
          pincel:.7, zoomHover:1.035});
        else if(!dentro && gl){ gl.destruir(); gl = null; }
      }
      new IntersectionObserver(function(es){ es.forEach(function(e){ dentro = e.isIntersecting; }); atualiza(); },
        {rootMargin:'30% 0px 30% 0px'}).observe(raiz);
    });
  }

  /* barras crescem ao entrar na tela */
  var barras = document.querySelector('.sm-barras');
  if(barras && 'IntersectionObserver' in window && !matchMedia('(prefers-reduced-motion:reduce)').matches){
    barras.classList.add('sm-anim');
    new IntersectionObserver(function(es, o){ es.forEach(function(e){ if(e.isIntersecting){ barras.classList.remove('sm-anim'); o.disconnect(); } }); },
      {threshold:.3}).observe(barras);
  }

  /* sanfona */
  [].forEach.call(document.querySelectorAll('#smSanfona .sm-sf'), function(sf, i, todos){
    sf.querySelector('button').addEventListener('click', function(){
      var abre = !sf.classList.contains('aberto');
      [].forEach.call(document.querySelectorAll('#smSanfona .sm-sf'), function(o){
        o.classList.remove('aberto'); o.querySelector('button').setAttribute('aria-expanded', 'false');
      });
      if(abre){ sf.classList.add('aberto'); this.setAttribute('aria-expanded', 'true'); }
    });
  });

  /* filtro: indicador desliza; a caixa do resultado tem altura fixa */
  var filtro = document.getElementById('smFiltro'), res = document.getElementById('smFiltroRes');
  if(filtro && res){
    var bts = filtro.querySelectorAll('button');
    [].forEach.call(bts, function(b, i){
      b.addEventListener('click', function(){
        [].forEach.call(bts, function(o){ o.setAttribute('aria-selected', o === b ? 'true' : 'false'); });
        filtro.style.setProperty('--i', i);
        filtro.style.setProperty('--x', i % 2);
        filtro.style.setProperty('--y', Math.floor(i / 2));
        [].forEach.call(res.children, function(p){ p.classList.toggle('on', p.getAttribute('data-t') === b.getAttribute('data-t')); });
      });
    });
  }

  /* matriz: acende linha e coluna; a linha de cima mostra a norma com a revisao */
  var mat = document.getElementById('smMat'), info = document.getElementById('smMatInfo');
  if(mat){
    var limpa = function(){ [].forEach.call(mat.querySelectorAll('.acende'), function(c){ c.classList.remove('acende'); }); };
    mat.addEventListener('mouseover', function(e){
      var c = e.target.closest('[data-l]'); if(!c) return;
      limpa();
      [].forEach.call(mat.querySelectorAll('[data-l="' + c.getAttribute('data-l') + '"],[data-c="' + c.getAttribute('data-c') + '"]'), function(o){ o.classList.add('acende'); });
      if(info) info.textContent = c.getAttribute('data-txt') || ' ';
    });
    mat.addEventListener('mouseleave', function(){ limpa(); if(info) info.textContent = ' '; });
  }

  /* carrossel: um losango por posicao que a fila alcanca (4 cards na tela: 3 posicoes; 1 card na tela: 6) */
  var carro = document.getElementById('smCarro'), pontos = document.getElementById('smPontos');
  if(carro && pontos){
    var cards = carro.children;
    var passo = function(){ return cards[1].offsetLeft - cards[0].offsetLeft; };
    var marca = function(){
      var n = Math.round(carro.scrollLeft / passo());
      [].forEach.call(pontos.children, function(b, i){ b.setAttribute('aria-current', i === Math.min(n, pontos.children.length - 1) ? 'true' : 'false'); });
    };
    var monta = function(){
      var total = Math.min(cards.length, Math.ceil((carro.scrollWidth - carro.clientWidth) / passo() - .02) + 1);
      if(pontos.children.length === total) return marca();
      pontos.textContent = '';
      for(var i = 0; i < total; i++) (function(i){
        var b = document.createElement('button'); b.type = 'button'; b.setAttribute('aria-label', 'Posição ' + (i + 1));
        b.addEventListener('click', function(){ carro.scrollTo({left: i * passo(), behavior: 'smooth'}); });
        pontos.appendChild(b);
      })(i);
      marca();
    };
    carro.addEventListener('scroll', marca, {passive:true});
    window.addEventListener('resize', monta);
    monta();
  }
})();
