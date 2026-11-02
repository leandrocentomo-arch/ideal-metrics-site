/* banner das paginas internas: creme a esquerda, trama azulada a direita, com o
   rastro do mouse. Motor: js/trama.js. Gerado a mao; a imagem vem de
   _ferramentas/banner/banner.py. Abaixo de 769px o banner fica creme liso. */
(function(){
  var b = document.querySelector('.page-banner');
  if(!b) return;
  /* 01/11/2026, «seria possível ver a foto do menu bem pequena no celular?»: abaixo de 769 px a foto do banner aparece numa
     faixa baixa embaixo do título e do subtítulo (.pb-tira), com a mesma trama e a mesma passagem para o creme. Só onde a
     página tem foto própria (data-lum); banner só de trama (Todos os serviços, Conteúdo) continua creme liso no celular. */
  var celular = !window.matchMedia('(min-width:769px)').matches;
  if(celular){
    var lumC = b.getAttribute('data-cor') || b.getAttribute('data-lum') || '';
    if(!lumC || /trama|conteudo/.test(lumC)) return;
    /* o motor (js/trama.js) não roda em tela de toque: a faixa é desenhada uma vez, parada, com a receita do banner
       (tom gama .86, contraste 1,55, brilho +.35, 4 níveis em Bayer 4×4, rampa da marca), ponto de 1 px de tela */
    var tira = document.createElement('canvas'); tira.className = 'pb-tira'; tira.setAttribute('aria-hidden', 'true');
    /* 02/11/2026, «colocar o título sobre a foto… tipo grifado em creme»: a foto e o título moram numa capa (css .pb-capa), o
       título ganha um span .pb-grifo, que leva o creme linha a linha, e o subtítulo fica embaixo da capa, no creme */
    b.classList.add('pb-foto');
    var capa = document.createElement('div'); capa.className = 'pb-capa'; capa.appendChild(tira);
    var tituloC = b.querySelector(':scope > h1');
    if(tituloC){
      var grifo = document.createElement('span'); grifo.className = 'pb-grifo';
      while(tituloC.firstChild) grifo.appendChild(tituloC.firstChild);
      tituloC.appendChild(grifo);
      b.insertBefore(capa, tituloC); capa.appendChild(tituloC);
    } else b.insertBefore(capa, b.firstChild);
    var tomC = null; try { tomC = JSON.parse(b.getAttribute('data-tom') || 'null'); } catch(e){}
    var G = (tomC && +tomC.gama) || .86, K = (tomC && +tomC.ctr) || 1.55, BR = (tomC && tomC.brilhoTom != null) ? +tomC.brilhoTom : .35;
    var RAMPA = [[21,51,81],[24,56,88],[103,146,189],[250,249,245]];
    if(tomC && tomC.cores && tomC.cores.length === 4) RAMPA = tomC.cores.map(function(h){ var v = parseInt(String(h).replace('#',''), 16); return [v>>16&255, v>>8&255, v&255]; });
    var BAYER = [0,8,2,10,12,4,14,6,3,11,1,9,15,7,13,5];
    var im = new Image();
    im.onload = function(){
      var dpr = Math.min(3, window.devicePixelRatio || 1), W = Math.round(tira.clientWidth * dpr), H = Math.round(tira.clientHeight * dpr);
      if(!W || !H) return;
      tira.width = W; tira.height = H;
      /* 02/11/2026, «as fotos não ficaram boas no celular»: o arquivo do banner tem a foto na metade direita e o creme da
         passagem na esquerda; a faixa usa só a metade direita, cobrindo a largura inteira, recortada no meio da altura */
      var cx = tira.getContext('2d'), iw = im.naturalWidth, ih = im.naturalHeight, sw = iw * .5, sh = sw * H / W;
      if(sh > ih){ sh = ih; sw = sh * W / H; }
      cx.drawImage(im, iw - sw, (ih - sh) / 2, sw, sh, 0, 0, W, H);
      var d = cx.getImageData(0, 0, W, H), p = d.data, c = Math.max(1, Math.round(dpr));   // célula de 1 px de tela
      for(var y = 0; y < H; y++) for(var x = 0; x < W; x++){
        var i = (y * W + x) * 4, g = (.2126 * p[i] + .7152 * p[i+1] + .0722 * p[i+2]) / 255;
        var v = Math.min(1 - 1e-6, Math.max(1e-6, Math.pow(g, G))), a = Math.pow(v, K), bb = Math.pow(1 - v, K), t = Math.min(1, Math.max(0, a / (a + bb) + BR));
        /* 02/11/2026, «um avanço maior do creme do lado esquerdo para o direito»: a foto se desfaz em trama até o creme, da
           direita para a esquerda; creme cheio na borda esquerda, foto cheia a partir de 68% da largura */
        var fx = Math.max(0, 1 - x / (W * .68)); t += (1 - t) * fx * fx * (3 - 2 * fx);
        var lim = (BAYER[((Math.floor(y / c) & 3) << 2) | (Math.floor(x / c) & 3)] + .5) / 16, n = Math.min(3, Math.floor(t * 3 + lim)), cor = RAMPA[n];
        p[i] = cor[0]; p[i+1] = cor[1]; p[i+2] = cor[2]; p[i+3] = 255;
      }
      cx.putImageData(d, 0, 0);
    };
    im.src = lumC;
    return;
  }
  if(!window.ditherVivo) return;
  /* 23/09: cada pagina pode ter a SUA foto no banner, por data-lum no .page-banner.
     Sem isso, fica a rampa neutra de creme a trama. A foto ja vem esvanecida no
     proprio arquivo de luminancia (ver _ferramentas/banner/foto_banner.py). */
  /* 28/09: com data-cor, a foto vem EM COR (RGBA, alfa = esvanecimento) e passa pelo
     FILTRO EM COR do site (ditherVivo.RECEITA_COR). Sem data-cor, a luminancia de sempre. */
  var cor = b.getAttribute('data-cor'), lum = b.getAttribute('data-lum') || 'img/banner-trama-lum.webp';
  var cfg = {raiz:b, planos:[{el:b, lum:cor || lum, ax:1}], classeCanvas:'pb-gl', revelar:'visivel',
    cores:[[21.2,50.9,80.6],[24.2,56.2,88.1],[103.0,146.1,189.4],[250,249,245]], pincel:.7};
  /* 02/10: data-tom no .page-banner muda o tom SO deste banner (receita do Spirit, aba [ 08 ]):
     {"brilhoTom":.35,"gama":.86,"ctr":1.55,"cores":["#153351","#183858","#6792BD","#FAF9F5"]} */
  var tom = null; try { tom = JSON.parse(b.getAttribute('data-tom') || 'null'); } catch(e){}
  if(tom && !cor){
    if(tom.brilhoTom != null) cfg.brilhoTom = +tom.brilhoTom;
    if(tom.gama) cfg.gama = +tom.gama;
    if(tom.ctr) cfg.ctr = +tom.ctr;
    if(tom.escuro) cfg.escuro = +tom.escuro;
    if(tom.lavaRepouso) cfg.lavaRepouso = +tom.lavaRepouso;
    if(tom.cores && tom.cores.length === 4) cfg.cores = tom.cores.map(function(h){ var v = parseInt(String(h).replace('#',''), 16); return [v>>16&255, v>>8&255, v&255]; });
  }
  /* 17/10/2026: data-pincel no .page-banner deixa o rastro do mouse mais forte SO neste banner (padrao .7) */
  var pc = parseFloat(b.getAttribute('data-pincel')); if(pc > 0) cfg.pincel = pc;
  window.ditherVivo(cor ? window.ditherVivo.emCor(cfg) : cfg);
})();
