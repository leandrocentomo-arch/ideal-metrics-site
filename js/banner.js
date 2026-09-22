/* banner das paginas internas: creme a esquerda, trama azulada a direita, com o
   rastro do mouse. Motor: js/trama.js. Gerado a mao; a imagem vem de
   _ferramentas/banner/banner.py. Abaixo de 769px o banner fica creme liso. */
(function(){
  var b = document.querySelector('.page-banner');
  if(!b || !window.ditherVivo || !window.matchMedia('(min-width:769px)').matches) return;
  window.ditherVivo({raiz:b, planos:[{el:b, lum:'img/banner-trama-lum.webp', ax:1}], classeCanvas:'pb-gl', revelar:'visivel',
    cores:[[21.2,50.9,80.6],[24.2,56.2,88.1],[103.0,146.1,189.4],[250,249,245]], pincel:.7});
})();
