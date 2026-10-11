/* Guia da home, «Setores em foco» (10/10/2026): a lista dos nove setores e UMA foto grande que troca quando o mouse
   passa no setor (as nove fotos empilhadas no motor da trama, modo empilhado, como a moldura de noticias). A legenda
   traz o resumo do setor, os tres temas de gestao com mais normas em destaque (de window.IM_SETORES) e o link.
   O motor so liga perto da tela e e destruido longe dela (o navegador segura poucos contextos WebGL). */
(function(){
  var OFICIAL = [[21.2,50.9,80.6],[24.2,56.2,88.1],[103.0,146.1,189.4],[250,249,245]];
  function init(){
    var raiz = document.getElementById('sfSetores'); if(!raiz) return;
    var D = window.IM_SETORES;
    var itens = [].slice.call(raiz.querySelectorAll('.sf-item'));
    var camadas = [].slice.call(raiz.querySelectorAll('.sf-layer'));
    var midia = raiz.querySelector('.sf-midia');
    var resumo = raiz.querySelector('.sf-resumo'), temasEl = raiz.querySelector('.sf-temas'), ir = raiz.querySelector('.sf-ir');
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
      itens.forEach(function(it, k){ it.classList.toggle('on', k === i); });
      camadas.forEach(function(c, k){ c.classList.toggle('sf-layer-ativa', k === i); });
      if(gl) gl.fundir(i);
      var it = itens[i];
      resumo.textContent = it.getAttribute('data-resumo');
      temasEl.textContent = temas(it.getAttribute('data-s'));
      ir.href = it.getAttribute('href');
    }
    itens.forEach(function(it, i){
      it.addEventListener('mouseenter', function(){ mostra(i); });
      it.addEventListener('focus', function(){ mostra(i); });
    });
    temasEl.textContent = temas(itens[0].getAttribute('data-s'));
    if(!window.ditherVivo || !('IntersectionObserver' in window)) return;
    var planos = camadas.map(function(c){ return {el:midia, lum:c.querySelector('img').getAttribute('data-lum')}; });
    new IntersectionObserver(function(es){
      es.forEach(function(e){
        if(e.isIntersecting && !gl){
          gl = window.ditherVivo({brilhoTom:0.35, gama:0.88, ctr:1.55, escuro:0.35, lavaRepouso:0.12, raiz:midia, planos:planos,
            classeCanvas:'sf-gl', revelar:'visivel', empilhado:true, cores:OFICIAL, pincel:.7, zoomHover:1.035});
          if(gl && atual) gl.fundir(atual);
        } else if(!e.isIntersecting && gl){ gl.destruir(); gl = null; }
      });
    }, {rootMargin:'60% 0px 60% 0px'}).observe(midia);
  }
  if(document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init); else init();
})();
