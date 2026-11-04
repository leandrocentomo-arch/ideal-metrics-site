
/* HOME SWISS (03/11/2026): as fotos das secoes novas no motor da trama (js/trama.js), com o mesmo
   contrato das fotos dos Diferenciais: a peca liga quando chega a 60% da tela e e destruida ao sair,
   porque o navegador segura poucos contextos WebGL. Tom proprio por data-tom (receita do Spirit). */
(function(){
  var ditherVivo = window.ditherVivo; if(!ditherVivo || !('IntersectionObserver' in window)) return;
  var OFICIAL = [[21.2,50.9,80.6],[24.2,56.2,88.1],[103.0,146.1,189.4],[250,249,245]];
  [].forEach.call(document.querySelectorAll('.sw-quadro'), function(raiz){
    var im = raiz.querySelector('img[data-lum]'); if(!im) return;
    var gl = null, dentro = false;
    function atualiza(){
      var tom = null; try { tom = JSON.parse(im.getAttribute('data-tom') || 'null'); } catch(e){}
      if(dentro && !gl) gl = ditherVivo({brilhoTom:0.35, gama:0.88, ctr:1.55, escuro:0.35, lavaRepouso:0.12, raiz:raiz,
        planos:[{el:raiz, lum:im.getAttribute('data-lum'), tom:tom}], classeCanvas:'vv-gl', revelar:'visivel', cores:OFICIAL,
        pincel:.7, zoomHover:1.035});
      else if(!dentro && gl){ gl.destruir(); gl = null; }
    }
    new IntersectionObserver(function(es){ es.forEach(function(e){ dentro = e.isIntersecting; }); atualiza(); },
      {rootMargin:'60% 0px 60% 0px'}).observe(raiz);
  });
})();
