/* banner das paginas internas: creme a esquerda, trama azulada a direita, com o
   rastro do mouse. Motor: js/trama.js. Gerado a mao; a imagem vem de
   _ferramentas/banner/banner.py. Abaixo de 769px o banner fica creme liso. */
(function(){
  var b = document.querySelector('.page-banner');
  if(!b || !window.ditherVivo || !window.matchMedia('(min-width:769px)').matches) return;
  /* 23/09: cada pagina pode ter a SUA foto no banner, por data-lum no .page-banner.
     Sem isso, fica a rampa neutra de creme a trama. A foto ja vem esvanecida no
     proprio arquivo de luminancia (ver _ferramentas/banner/foto_banner.py). */
  /* 28/09: com data-cor, a foto vem EM COR (RGBA, alfa = esvanecimento) e passa pelo
     FILTRO EM COR do site (ditherVivo.RECEITA_COR). Sem data-cor, a luminancia de sempre. */
  var cor = b.getAttribute('data-cor'), lum = b.getAttribute('data-lum') || 'img/banner-trama-lum.webp';
  var cfg = {raiz:b, planos:[{el:b, lum:cor || lum, ax:1}], classeCanvas:'pb-gl', revelar:'visivel',
    cores:[[21.2,50.9,80.6],[24.2,56.2,88.1],[103.0,146.1,189.4],[250,249,245]], pincel:.7};
  window.ditherVivo(cor ? window.ditherVivo.emCor(cfg) : cfg);
})();
