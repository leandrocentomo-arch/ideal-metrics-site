/* O pássaro do monograma bate as asas na entrada da página (27/10/2026).
   Nasceu no Painel de normas («é possível criar um gif de forma que o pássaro do logo bata as asas na entrada?») e em
   27/10 o Leandro pediu em todas as páginas («quero que em todas as páginas do site tenha esse logo animado também, lá
   no menu de topo principal»). Sem GIF: o SVG oficial do monograma entra inline no lugar do <img class="marca-frente">,
   a asa longa (filho 25 do grupo do pássaro, o grande caminho à esquerda) e as lâminas da asa curta (filhos 8, 20, 21,
   22, 24, 43, 44) giram em torno do ombro. Na entrada só o pássaro nasce a 35% e cresce até o tamanho cheio em 2,4 s,
   com três batidas inteiras cada vez mais fracas (1, .7, .45), e ao assentar um brilho prateado em diagonal atravessa
   o pássaro e a parte escrita (máscara alfa com o próprio monograma). Nada é redesenhado nem pintado: é a geometria
   oficial girada; ao fim, tudo volta ao desenho original. Respeita prefers-reduced-motion.
   window.bateAsasMonograma(img, {prata:true}): anima um <img> específico; o brilho prateado só com prata:true (o Painel
   de normas pede na cópia do logo do cabeçalho; na barra do topo «não precisa do pulse», 27/10).
   Na carga, anima sozinho o logo da barra do topo, menos no Painel de normas (lá a barra fica recolhida e o painel
   cuida da cópia). */
(function () {
  var n = 0;
  function bateAsas(img, opts) {
    opts = opts || {};
    if (!img || (window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches)) return;
    var id = ++n;
    fetch(img.getAttribute('src')).then(function (r) { return r.text(); }).then(function (txt) {
      if (!img.parentNode) return;
      var doc = new DOMParser().parseFromString(txt, 'image/svg+xml'), svg = doc.documentElement;
      if (!svg || svg.nodeName !== 'svg') return;
      var mono = svg.querySelector('#monograma-270'), passaro = mono && mono.querySelector(':scope > g');
      /* 01/11/2026, «nesta tela [a abertura do celular] faça o pássaro batendo [asas] como feito para o painel de normas»:
         o lockup prata da abertura não tem o #monograma-270; o pássaro é o primeiro grupo com os mesmos 45 desenhos, na
         mesma ordem, em outra escala. A escala e o deslocamento saem de dois pontos conhecidos (o 1º vértice das lâminas 8 e
         44), e com eles o ombro e o centro do giro passam para as coordenadas desse arquivo */
      var M = function (x, y) { return [x, y]; };
      if (!passaro) {
        passaro = Array.prototype.filter.call(svg.querySelectorAll('g'), function (g) { return g.children.length === 45; })[0];
        if (!passaro) return;
        var v = function (i) { return (passaro.children[i].getAttribute('points') || '').trim().split(/[\s,]+/).slice(0, 2).map(Number); }, a8 = v(8), a44 = v(44);
        var sx = (a44[0] - a8[0]) / (72.02 - 66.91), sy = (a44[1] - a8[1]) / (21.13 - 17.48), ox = a8[0] - 66.91 * sx, oy = a8[1] - 17.48 * sy;
        if (!isFinite(sx) || !isFinite(sy)) return;
        M = function (x, y) { return [ox + x * sx, oy + y * sy]; };
        mono = passaro;
      }
      mono.setAttribute('id', 'monograma-270-' + id);   // ids únicos: pode haver mais de um monograma inline na página
      var filhos = Array.prototype.slice.call(passaro.children), ns = 'http://www.w3.org/2000/svg';
      var longa = doc.createElementNS(ns, 'g'), curta = doc.createElementNS(ns, 'g');
      [25].forEach(function (i) { if (filhos[i]) longa.appendChild(filhos[i]); });
      [8, 20, 21, 22, 24, 43, 44].forEach(function (i) { if (filhos[i]) curta.appendChild(filhos[i]); });
      passaro.appendChild(longa); passaro.appendChild(curta);
      svg.setAttribute('class', img.className); svg.setAttribute('aria-hidden', 'true'); if (!opts.largura) svg.style.width = 'auto'; svg.style.display = 'block';   // largura:true = a largura vem do CSS (abertura)
      img.parentNode.replaceChild(svg, img);
      /* brilho prateado: retângulo com degradê diagonal, mascarado pelo próprio monograma, atravessa em .9 s */
      var vb = (svg.getAttribute('viewBox') || '0 0 100 100').split(/\s+/).map(Number), defs = doc.createElementNS(ns, 'defs');
      defs.innerHTML = '<linearGradient id="prata-' + id + '" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".42" stop-color="#fff" stop-opacity="0"/><stop offset=".5" stop-color="#E6EBF1" stop-opacity=".95"/><stop offset=".58" stop-color="#fff" stop-opacity="0"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>' +
        '<mask id="prata-m-' + id + '" maskUnits="userSpaceOnUse" x="' + vb[0] + '" y="' + vb[1] + '" width="' + vb[2] + '" height="' + vb[3] + '" style="mask-type:alpha"><use href="#monograma-270-' + id + '"/></mask>';
      svg.insertBefore(defs, svg.firstChild);
      var brilho = doc.createElementNS(ns, 'rect');
      brilho.setAttribute('x', vb[0]); brilho.setAttribute('y', vb[1]); brilho.setAttribute('width', vb[2]); brilho.setAttribute('height', vb[3]);
      brilho.setAttribute('fill', 'url(#prata-' + id + ')'); brilho.setAttribute('mask', 'url(#prata-m-' + id + ')'); brilho.setAttribute('pointer-events', 'none'); brilho.style.display = 'none';
      svg.appendChild(brilho);
      function pulsoPrata() {
        var t0 = performance.now(), dur = 900; brilho.style.display = '';
        (function passo(t) {
          var k = Math.max(0, Math.min((t - t0) / dur, 1));
          brilho.setAttribute('transform', 'translate(' + ((k * 2 - 1) * vb[2] * 1.1).toFixed(1) + ' 0)');
          if (k < 1) requestAnimationFrame(passo); else brilho.style.display = 'none';
        })(t0);
      }
      /* entrada: cresce a partir do ombro e bate três vezes; a amplitude só troca no cruzamento do zero, então a terceira
         batida termina inteira junto com o crescimento */
      /* 01/11/2026, abertura do celular: «pode deixar só o logo com efeito, a parte escrita e depois o pássaro vindo, batendo
         asas» (opts.vem): o pássaro fica escondido enquanto a escrita aparece e, depois de opts.atraso ms, entra voando do alto
         à direita, crescendo e batendo as três batidas, até pousar no lugar dele no logo */
      var PL = M(39.5, 20.5), PC = M(45.5, 15), OR = M(39, 20), AMP = [1, .7, .45], t0 = performance.now() + (opts.vem ? opts.atraso || 0 : 0), dur = opts.dur || 2400;
      var DX = opts.vem ? vb[2] * .55 : 0, DY = opts.vem ? -vb[3] * .7 : 0;
      passaro.style.transformOrigin = OR[0].toFixed(2) + 'px ' + OR[1].toFixed(2) + 'px'; passaro.style.transformBox = 'view-box';
      if (opts.vem) passaro.style.opacity = '0';
      (function passo(t) {
        if (t < t0) { requestAnimationFrame(passo); return; }
        var k = Math.max(0, Math.min((t - t0) / dur, 1)), a = -Math.sin(k * Math.PI * 6) * AMP[Math.min(2, Math.floor(k * 3))];
        var g = a < 0 ? a * 18 : a * 7;   // descida ampla, subida curta
        longa.setAttribute('transform', 'rotate(' + g.toFixed(2) + ' ' + PL[0] + ' ' + PL[1] + ')');
        curta.setAttribute('transform', 'rotate(' + (-g * .4).toFixed(2) + ' ' + PC[0] + ' ' + PC[1] + ')');
        var e = 1 - Math.pow(1 - k, 3), voo = opts.vem ? 'translate(' + ((1 - e) * DX).toFixed(1) + 'px,' + ((1 - e) * DY).toFixed(1) + 'px) ' : '';
        passaro.style.transform = voo + 'scale(' + (.35 + .65 * e).toFixed(3) + ')'; passaro.style.opacity = Math.min(1, (opts.vem ? 0 : .3) + k * (opts.vem ? 4 : 1.4)).toFixed(2);
        if (k < 1) requestAnimationFrame(passo);
        else { longa.removeAttribute('transform'); curta.removeAttribute('transform'); passaro.style.transform = ''; passaro.style.opacity = ''; if (opts.prata) pulsoPrata(); }   // 27/10: o brilho prateado só onde for pedido (no logo da barra «não precisa do pulse»)
      })(t0);
    }).catch(function () {});
  }
  window.bateAsasMonograma = bateAsas;
  function auto() { if (document.body.classList.contains('pn-pagina')) return; bateAsas(document.querySelector('header.barra .barra-marca img.marca-frente')); }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', auto); else auto();
})();
