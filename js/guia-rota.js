/* Guia da home, «Ou monte a sua rota» (10/10/2026). Le window.IM_SETORES (js/setores-dados.js, gerado por
   _ferramentas/setores.py). Escolhido o setor, fios finos ligam o setor aos temas de gestao das normas dele e cada
   tema as suas normas; a norma leva a pagina do servico. Passar o mouse num tema filtra as normas daquele tema.
   Sem setor escolhido, o tema mostra todas as normas dele. Sem dependencias. */
(function(){
  function init(){
    var D = window.IM_SETORES, raiz = document.getElementById('mpRota');
    if(!D || !raiz) return;
    var grade = raiz.querySelector('.mr-grade'), svg = raiz.querySelector('.mr-fios');
    var ulS = raiz.querySelector('.mr-col--s ul'), ulT = raiz.querySelector('.mr-col--t ul'), ulN = raiz.querySelector('.mr-col--n ul');
    var info = raiz.querySelector('.mr-info');
    var NS = 'http://www.w3.org/2000/svg';
    var selS = D.setores[0].id, hovT = null;
    var ordem = {}; D.ordemNormas.forEach(function(id, i){ ordem[id] = i; });

    function no(tag, cls, txt){ var e = document.createElement(tag); if(cls) e.className = cls; if(txt != null) e.textContent = txt; return e; }
    function setor(id){ return D.setores.filter(function(s){ return s.id === id; })[0]; }

    D.setores.forEach(function(s){
      var li = no('li'), b = no('button', 'mr-no', s.nome); b.type = 'button'; b.setAttribute('data-s', s.id);
      b.addEventListener('click', function(){ selS = (selS === s.id) ? null : s.id; hovT = null; desenha(); });
      b.addEventListener('mouseenter', function(){ if(window.matchMedia('(hover:hover)').matches){ selS = s.id; hovT = null; desenha(); } });
      li.appendChild(b); ulS.appendChild(li);
    });
    D.grupos.forEach(function(g){
      var li = no('li'), b = no('button', 'mr-no', g.nome); b.type = 'button'; b.setAttribute('data-t', g.id);
      b.addEventListener('mouseenter', function(){ hovT = g.id; desenha(); });
      b.addEventListener('focus', function(){ hovT = g.id; desenha(); });
      b.addEventListener('click', function(){ hovT = (hovT === g.id) ? null : g.id; desenha(); });
      li.appendChild(b); ulT.appendChild(li);
    });
    raiz.querySelector('.mr-col--t').addEventListener('mouseleave', function(){ if(hovT){ hovT = null; desenha(); } });

    function normasVisiveis(){
      var s = selS && setor(selS), ids;
      if(s) ids = s.normas.slice();
      else if(hovT) ids = D.ordemNormas.filter(function(id){ return D.normas[id].grupo === hovT; });
      else ids = [];
      if(s && hovT) ids = ids.filter(function(id){ return D.normas[id].grupo === hovT; });
      return ids.sort(function(a, b){ return ordem[a] - ordem[b]; });
    }

    function fio(x1, y1, x2, y2, cls){
      var dx = (x2 - x1) * 0.5, p = document.createElementNS(NS, 'path');
      p.setAttribute('d', 'M' + x1 + ' ' + y1 + ' C' + (x1 + dx) + ' ' + y1 + ' ' + (x2 - dx) + ' ' + y2 + ' ' + x2 + ' ' + y2);
      if(cls) p.setAttribute('class', cls);
      svg.appendChild(p);
      var L = p.getTotalLength(); p.style.strokeDasharray = L; p.style.strokeDashoffset = L;
      requestAnimationFrame(function(){ p.style.strokeDashoffset = 0; });
    }

    function desenha(){
      var s = selS && setor(selS), ids = normasVisiveis();
      var temasDoSetor = {};
      if(s) s.normas.forEach(function(id){ temasDoSetor[D.normas[id].grupo] = true; });
      [].forEach.call(ulS.querySelectorAll('.mr-no'), function(b){ b.classList.toggle('on', b.getAttribute('data-s') === selS); });
      [].forEach.call(ulT.querySelectorAll('.mr-no'), function(b){
        var t = b.getAttribute('data-t');
        b.classList.toggle('on', s ? !!temasDoSetor[t] : t === hovT);
        b.classList.toggle('apagado', !!s && !temasDoSetor[t]);
        b.classList.toggle('foco', t === hovT);
      });
      ulN.textContent = '';
      if(!ids.length){
        ulN.appendChild(no('li', 'mr-vazio', 'Nenhum setor ou tema selecionado.'));
      }
      ids.forEach(function(id){
        var n = D.normas[id], li = no('li'), el;
        if(n.pagina){
          el = no('a', 'mr-no mr-norma'); el.href = n.pagina;
          el.appendChild(no('span', null, n.nome));
          el.insertAdjacentHTML('beforeend', '<svg viewBox="0 0 9 9" aria-hidden="true" focusable="false"><path d="M0 4.35H8M4 8.35L8 4.35L4 .35"/></svg>');
        } else {
          el = no('span', 'mr-no mr-norma mr-sem', n.nome);
        }
        el.title = n.desc; el.setAttribute('data-t', n.grupo);
        li.appendChild(el); ulN.appendChild(li);
      });
      var nT = Object.keys(temasDoSetor).length;
      info.textContent = s ? (s.nome + ': ' + s.normas.length + ' normas e padrões em destaque, em ' + nT + (nT === 1 ? ' tema' : ' temas') + '. ' +
        (s.normas.length ? 'A norma leva à página do serviço.' : '')) + ' As que valem para qualquer setor estão na página do setor.'
        : (hovT ? 'Todas as normas e padrões deste tema.' : '');
      /* fios: medidos depois do layout */
      requestAnimationFrame(function(){
        while(svg.firstChild) svg.removeChild(svg.firstChild);
        if(window.matchMedia('(max-width:880px)').matches) return;
        var G = grade.getBoundingClientRect();
        svg.setAttribute('viewBox', '0 0 ' + G.width + ' ' + G.height);
        function dir(el){ var r = el.getBoundingClientRect(); return [r.right - G.left, r.top + r.height / 2 - G.top]; }
        function esq(el){ var r = el.getBoundingClientRect(); return [r.left - G.left, r.top + r.height / 2 - G.top]; }
        var noT = {}; [].forEach.call(ulT.querySelectorAll('.mr-no'), function(b){ noT[b.getAttribute('data-t')] = b; });
        if(s){
          var bS = ulS.querySelector('.mr-no[data-s="' + selS + '"]'), a = dir(bS);
          Object.keys(temasDoSetor).forEach(function(t){
            if(hovT && t !== hovT) return;
            var b = esq(noT[t]); fio(a[0], a[1], b[0], b[1]);
          });
        }
        [].forEach.call(ulN.querySelectorAll('.mr-norma'), function(el){
          var t = el.getAttribute('data-t'); if(!noT[t]) return;
          var a = dir(noT[t]), b = esq(el); fio(a[0], a[1], b[0], b[1], 'mr-fio2');
        });
      });
    }
    var tm = null; window.addEventListener('resize', function(){ clearTimeout(tm); tm = setTimeout(desenha, 150); });
    desenha();
  }
  if(document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init); else init();
})();
