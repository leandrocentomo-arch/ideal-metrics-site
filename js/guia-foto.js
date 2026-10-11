/* Guia da home, «Setores» no desenho de Conteudo de destaque (10/10/2026): grade 3x3 com os nove setores e UMA foto
   menor a esquerda; a casa sob o mouse fica azul e a foto troca (as nove fotos empilhadas no motor da trama, modo
   empilhado, como a moldura de noticias). A legenda traz o resumo do setor e os tres temas de gestao com mais normas
   em destaque (de window.IM_SETORES). O motor so liga perto da tela e e destruido longe dela. */
(function(){
  var OFICIAL = [[21.2,50.9,80.6],[24.2,56.2,88.1],[103.0,146.1,189.4],[250,249,245]];
  function init(){
    var raiz = document.getElementById('sfSetores'); if(!raiz) return;
    var D = window.IM_SETORES;
    var casas = [].slice.call(raiz.querySelectorAll('.sx-card'));
    var camadas = [].slice.call(raiz.querySelectorAll('.sx-layer'));
    var midia = raiz.querySelector('.sx-midia');
    var resumo = raiz.querySelector('.sx-resumo'), temasEl = raiz.querySelector('.sx-temas');
    var gl = null, atual = 0;
    function temas(id){
      if(!D) return '';
      var s = D.setores.filter(function(x){ return x.id === id; })[0]; if(!s) return '';
      var cont = {}, nomes = {};
      D.grupos.forEach(function(g){ nomes[g.id] = g.nome; });
      s.normas.forEach(function(n){ var g = D.normas[n].grupo; cont[g] = (cont[g] || 0) + 1; });
      return Object.keys(cont).sort(function(a, b){ return cont[b] - cont[a]; }).slice(0, 3).map(function(g){ return nomes[g]; }).join('  ·  ');
    }
    function mostra(i){
      if(i === atual) return;
      atual = i;
      casas.forEach(function(c, k){ c.classList.toggle('on', k === i); });
      camadas.forEach(function(c, k){ c.classList.toggle('sx-layer-ativa', k === i); });
      if(gl) gl.fundir(i);
      resumo.textContent = casas[i].getAttribute('data-resumo');
      temasEl.textContent = temas(casas[i].getAttribute('data-s'));
    }
    casas.forEach(function(c, i){
      c.addEventListener('mouseenter', function(){ mostra(i); });
      c.addEventListener('focusin', function(){ mostra(i); });
    });
    temasEl.textContent = temas(casas[0].getAttribute('data-s'));
    if(!window.ditherVivo || !('IntersectionObserver' in window)) return;
    var planos = camadas.map(function(c){ return {el:midia, lum:c.querySelector('img').getAttribute('data-lum')}; });
    new IntersectionObserver(function(es){
      es.forEach(function(e){
        if(e.isIntersecting && !gl){
          gl = window.ditherVivo({brilhoTom:0.35, gama:0.88, ctr:1.55, escuro:0.35, lavaRepouso:0.12, raiz:midia, planos:planos,
            classeCanvas:'sx-gl', revelar:'visivel', empilhado:true, cores:OFICIAL, pincel:.7, zoomHover:1.03});
          if(gl && atual) gl.fundir(atual);
        } else if(!e.isIntersecting && gl){ gl.destruir(); gl = null; }
      });
    }, {rootMargin:'60% 0px 60% 0px'}).observe(midia);
  }
  if(document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init); else init();
})();
