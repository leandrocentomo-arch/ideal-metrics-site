/* Filtro por setor ou por norma (09/10/2026). Le window.IM_SETORES (js/setores-dados.js, gerado por
   _ferramentas/setores.py). Por setor: as normas aplicaveis ao setor, por grupo, e a lista das que valem para qualquer
   setor, com link para a pagina do servico. Por norma: os setores em que ela se aplica, com link. Sem dependencias. */
(function(){
  var D = window.IM_SETORES, raiz = document.getElementById('stf');
  if(!D || !raiz) return;
  var chips = raiz.querySelector('.stf-chips'), res = raiz.querySelector('.stf-res'), abas = raiz.querySelectorAll('.stf-modo');
  var modo = 'setor', sel = null;
  var NOME_G = {}; D.grupos.forEach(function(g){ NOME_G[g.id] = g.nome; });

  function no(tag, cls, txt){ var e = document.createElement(tag); if(cls) e.className = cls; if(txt != null) e.textContent = txt; return e; }

  function cartao(titulo, desc, href, rotulo){
    var c = no(href ? 'a' : 'div', 'stf-card');
    if(href) c.href = href;
    c.appendChild(no('b', null, titulo));
    c.appendChild(no('span', null, desc));
    if(href) c.appendChild(no('i', null, rotulo));
    return c;
  }

  function lista(ids){
    var ul = no('ul', 'stf-cl');
    ids.forEach(function(id){
      var n = D.normas[id], li = no('li'); li.title = n.desc;
      if(n.pagina){ var a = no('a', null, n.nome); a.href = n.pagina; li.appendChild(a); } else li.textContent = n.nome;
      ul.appendChild(li);
    });
    return ul;
  }

  function chip(id, nome){
    var b = no('button', 'stf-chip', nome); b.type = 'button';
    b.setAttribute('aria-pressed', id === sel ? 'true' : 'false');
    b.addEventListener('click', function(){ sel = (sel === id) ? null : id; desenhaChips(); desenhaRes(); });
    return b;
  }

  function desenhaChips(){
    chips.textContent = '';
    if(modo === 'setor'){
      D.setores.forEach(function(s){ chips.appendChild(chip(s.id, s.nome)); });
      return;
    }
    var ult = null;
    D.ordemNormas.forEach(function(id){
      var n = D.normas[id];
      if(n.grupo !== ult){ chips.appendChild(no('span', 'stf-gl', NOME_G[n.grupo])); ult = n.grupo; }
      chips.appendChild(chip(id, n.nome));
    });
  }

  function desenhaRes(){
    res.textContent = '';
    if(!sel){ res.appendChild(no('p', 'stf-dica', modo === 'setor' ? 'Escolha um setor para ver as normas e os padrões aplicáveis.' : 'Escolha uma norma ou um padrão para ver os setores em que ele se aplica.')); return; }
    var cab = no('div', 'stf-cab');
    if(modo === 'setor'){
      var s = D.setores.filter(function(x){ return x.id === sel; })[0];
      cab.appendChild(no('h3', null, s.nome));
      var ir = no('a', 'stf-ir', 'Página do setor →'); ir.href = s.pagina; cab.appendChild(ir);
      res.appendChild(cab); res.appendChild(no('p', 'stf-sub', s.resumo));
      D.grupos.forEach(function(g){
        var ids = s.normas.filter(function(id){ return D.normas[id].grupo === g.id; });
        if(!ids.length) return;
        res.appendChild(no('p', 'stf-rot', g.nome));
        var grade = no('div', 'stf-grade');
        ids.forEach(function(id){ var n = D.normas[id]; grade.appendChild(cartao(n.nome, n.desc, n.pagina, 'Ver serviço →')); });
        res.appendChild(grade);
      });
      var outras = D.ordemNormas.filter(function(id){ return D.normas[id].todos && s.normas.indexOf(id) < 0; });
      res.appendChild(no('p', 'stf-rot', 'Outros padrões que valem para qualquer setor'));
      res.appendChild(lista(outras));
    } else {
      var n = D.normas[sel];
      cab.appendChild(no('h3', null, n.nome));
      if(n.pagina){ var ir2 = no('a', 'stf-ir', 'Página do serviço →'); ir2.href = n.pagina; cab.appendChild(ir2); }
      res.appendChild(cab); res.appendChild(no('p', 'stf-sub', n.desc));
      res.appendChild(no('p', 'stf-rot', 'Setores em que se aplica'));
      var grade2 = no('div', 'stf-grade');
      if(n.todos){
        res.appendChild(no('p', 'stf-sub', 'Vale para qualquer setor. Veja as páginas de setor:'));
        D.setores.forEach(function(x){ grade2.appendChild(cartao(x.nome, x.resumo, x.pagina, 'Ver setor →')); });
      } else if(n.fora){
        res.appendChild(no('p', 'stf-sub', 'Aplica-se a ' + n.fora.toLowerCase() + ', fora dos seis setores listados.'));
      } else if(n.setores.length){
        D.setores.filter(function(x){ return n.setores.indexOf(x.id) >= 0; }).forEach(function(x){ grade2.appendChild(cartao(x.nome, x.resumo, x.pagina, 'Ver setor →')); });
      } else {
        res.appendChild(no('p', 'stf-sub', 'Atendida fora dos seis setores listados.'));
      }
      res.appendChild(grade2);
    }
  }

  [].forEach.call(abas, function(a){
    a.addEventListener('click', function(){
      modo = a.getAttribute('data-modo'); sel = null;
      [].forEach.call(abas, function(o){ o.setAttribute('aria-selected', o === a ? 'true' : 'false'); });
      desenhaChips(); desenhaRes();
    });
  });
  desenhaChips(); desenhaRes();
})();
