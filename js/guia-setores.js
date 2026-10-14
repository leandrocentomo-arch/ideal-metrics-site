/* Guia da home: o bloco dos setores em TESTE, propostas H e I (14/10/2026; marcacao e CSS em _ferramentas/guia_setores.py).
   H: nomes grandes; a foto (a pilha de nove no motor da trama) flutua ao lado do ponteiro e troca com a linha.
   I: fios setor -> norma; no mouse sobre um setor os fios dele acendem e a foto troca; sobre uma norma, acendem os
   setores dela. O motor liga perto da tela e e destruido longe dela, como no bloco antigo (js/guia-foto.js). */
(function(){
  var OFICIAL = [[21.2,50.9,80.6],[24.2,56.2,88.1],[103.0,146.1,189.4],[250,249,245]];
  var calmo = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* a pilha de fotos de um bloco no motor; devolve {vai(i)} */
  function pilha(midia, opcoes){
    var camadas = [].slice.call(midia.querySelectorAll('.sx-layer')), gl = null, ativo = 0;
    function vai(i){
      if(i === ativo) return; ativo = i;
      camadas.forEach(function(c, k){ c.classList.toggle('sx-layer-ativa', k === i); });
      if(gl) gl.fundir(i);
    }
    if(window.ditherVivo && 'IntersectionObserver' in window){
      var planos = camadas.map(function(c){ var im = c.querySelector('img'), tom = null;
        try { tom = JSON.parse(im.getAttribute('data-tom') || 'null'); } catch(e){}
        return {el:midia, lum:im.getAttribute('data-lum'), ax:.5, tom:tom}; });
      new IntersectionObserver(function(es){
        es.forEach(function(e){
          if(e.isIntersecting && !gl){
            gl = window.ditherVivo({brilhoTom:0.35, gama:0.88, ctr:1.55, escuro:0.35, lavaRepouso:0.12, raiz:midia, planos:planos,
              classeCanvas:'sx-gl', revelar:'visivel', empilhado:true, cores:OFICIAL, pincel:opcoes.pincel, zoomHover:1.03});
            if(gl && ativo) gl.fundir(ativo);
          } else if(!e.isIntersecting && gl){ gl.destruir(); gl = null; }
        });
      }, {rootMargin:'60% 0px 60% 0px'}).observe(midia);
    }
    return {vai:vai};
  }

  /* ---------------- H ---------------- */
  function iniciaH(){
    var raiz = document.getElementById('guiaH'); if(!raiz) return;
    var flut = raiz.querySelector('.gh-flut'), lista = raiz.querySelector('.gh-lista');
    var P = pilha(flut.querySelector('.sx-midia'), {pincel:.0001});   /* a foto anda com o mouse: sem rastro */
    var alvo = {x:0, y:0}, pos = {x:0, y:0}, rodando = false, dentro = false;
    function passo(){
      pos.x += (alvo.x - pos.x) * (calmo ? 1 : .16); pos.y += (alvo.y - pos.y) * (calmo ? 1 : .16);
      flut.style.transform = 'translate3d(' + pos.x.toFixed(1) + 'px,' + pos.y.toFixed(1) + 'px,0)';
      if(Math.abs(alvo.x - pos.x) > .3 || Math.abs(alvo.y - pos.y) > .3) requestAnimationFrame(passo); else rodando = false;
    }
    function mira(e, salta){
      var r = raiz.getBoundingClientRect(), w = flut.offsetWidth || 300, h = flut.offsetHeight || 300;
      var x = e.clientX - r.left, y = e.clientY - r.top;
      /* do lado de la da tela, para a foto nao cobrir as normas da linha */
      alvo.x = x > r.width * .55 ? x - w - 48 : x + 48;
      alvo.y = Math.max(0, Math.min(r.height - h, y - h / 2));
      if(salta){ pos.x = alvo.x; pos.y = alvo.y; }
      if(!rodando){ rodando = true; requestAnimationFrame(passo); }
    }
    lista.addEventListener('mouseenter', function(e){ dentro = true; mira(e, true); flut.classList.add('on'); });
    lista.addEventListener('mousemove', function(e){ if(dentro) mira(e, false); });
    lista.addEventListener('mouseleave', function(){ dentro = false; flut.classList.remove('on'); });
    [].slice.call(raiz.querySelectorAll('.gh-li')).forEach(function(a){
      var i = +a.getAttribute('data-i');
      a.addEventListener('mouseenter', function(){ P.vai(i); });
      a.addEventListener('focus', function(){ P.vai(i); });
    });
  }

  /* ---------------- I ---------------- */
  function iniciaI(){
    var raiz = document.getElementById('guiaI'); if(!raiz) return;
    var svg = raiz.querySelector('.gi-svg'), P = pilha(raiz.querySelector('.sx-midia'), {pincel:.7});
    var resumo = raiz.querySelector('.gi-resumo'), normas = raiz.querySelector('.gi-normas');
    var fios = [].slice.call(svg.querySelectorAll('.gi-fio'));
    var sets = [].slice.call(svg.querySelectorAll('.gi-s')), nos = [].slice.call(svg.querySelectorAll('.gi-n'));
    function limpa(){ fios.concat(sets, nos).forEach(function(el){ el.classList.remove('on'); }); }
    function acende(filtro){
      limpa(); svg.classList.add('gi-foco');
      fios.forEach(function(f){ if(filtro(f)){ f.classList.add('on');
        sets[+f.getAttribute('data-s')].classList.add('on'); nos[+f.getAttribute('data-n')].classList.add('on'); } });
    }
    function setor(k){
      acende(function(f){ return +f.getAttribute('data-s') === k; });
      P.vai(k);
      resumo.textContent = raiz.getAttribute('data-r' + k); normas.textContent = raiz.getAttribute('data-m' + k);
    }
    function norma(j){ acende(function(f){ return +f.getAttribute('data-n') === j; }); }
    sets.forEach(function(t, k){ var a = t.parentNode;
      a.addEventListener('mouseenter', function(){ setor(k); }); a.addEventListener('focus', function(){ setor(k); }); });
    nos.forEach(function(t, j){ var a = t.parentNode;
      a.addEventListener('mouseenter', function(){ norma(j); }); a.addEventListener('focus', function(){ norma(j); }); });
    fios.forEach(function(f){ f.addEventListener('mouseenter', function(){ setor(+f.getAttribute('data-s')); }); });
    svg.addEventListener('mouseleave', function(){ svg.classList.remove('gi-foco'); limpa(); });
  }

  function init(){ iniciaH(); iniciaI(); }
  if(document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init); else init();
})();
