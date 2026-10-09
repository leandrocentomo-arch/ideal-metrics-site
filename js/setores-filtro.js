/* Filtro por setor ou por norma (09/10/2026). Le window.IM_SETORES (js/setores-dados.js, gerado por
   _ferramentas/setores.py). Por setor: mostra as normas aplicaveis, cada uma com o link da pagina do servico.
   Por norma: mostra os setores em que ela se aplica, com o link da pagina do setor. Sem dependencias. */
(function(){
  var D = window.IM_SETORES, raiz = document.getElementById('stf');
  if(!D || !raiz) return;
  var chips = raiz.querySelector('.stf-chips'), res = raiz.querySelector('.stf-res'), abas = raiz.querySelectorAll('.stf-modo');
  var modo = 'setor', sel = null;

  function no(tag, cls, txt){ var e = document.createElement(tag); if(cls) e.className = cls; if(txt != null) e.textContent = txt; return e; }

  function cartao(titulo, desc, href, rotulo){
    var c = no(href ? 'a' : 'div', 'stf-card');
    if(href) c.href = href;
    c.appendChild(no('b', null, titulo));
    c.appendChild(no('span', null, desc));
    if(href) c.appendChild(no('i', null, rotulo));
    return c;
  }

  function desenhaChips(){
    chips.textContent = '';
    var lista = modo === 'setor'
      ? D.setores.map(function(s){ return {id:s.id, nome:s.nome}; })
      : D.ordemNormas.map(function(id){ return {id:id, nome:D.normas[id].nome}; });
    lista.forEach(function(it){
      var b = no('button', 'stf-chip', it.nome); b.type = 'button';
      b.setAttribute('aria-pressed', it.id === sel ? 'true' : 'false');
      b.addEventListener('click', function(){ sel = (sel === it.id) ? null : it.id; desenhaChips(); desenhaRes(); });
      chips.appendChild(b);
    });
  }

  function desenhaRes(){
    res.textContent = '';
    if(!sel){ res.appendChild(no('p', 'stf-dica', modo === 'setor' ? 'Escolha um setor para ver as normas e os padrões aplicáveis.' : 'Escolha uma norma ou um padrão para ver os setores em que ele se aplica.')); return; }
    var cab = no('div', 'stf-cab'), grade = no('div', 'stf-grade');
    if(modo === 'setor'){
      var s = D.setores.filter(function(x){ return x.id === sel; })[0];
      cab.appendChild(no('h3', null, s.nome));
      var ir = no('a', 'stf-ir', 'Página do setor →'); ir.href = s.pagina; cab.appendChild(ir);
      res.appendChild(cab); res.appendChild(no('p', 'stf-sub', s.resumo));
      s.normas.forEach(function(id){ var n = D.normas[id]; grade.appendChild(cartao(n.nome, n.desc, n.pagina, 'Ver serviço →')); });
      res.appendChild(grade);
    } else {
      var n = D.normas[sel];
      cab.appendChild(no('h3', null, n.nome));
      if(n.pagina){ var ir2 = no('a', 'stf-ir', 'Página do serviço →'); ir2.href = n.pagina; cab.appendChild(ir2); }
      res.appendChild(cab); res.appendChild(no('p', 'stf-sub', n.desc));
      res.appendChild(no('p', 'stf-rot', 'Setores em que se aplica'));
      D.setores.filter(function(x){ return x.normas.indexOf(sel) >= 0; }).forEach(function(x){ grade.appendChild(cartao(x.nome, x.resumo, x.pagina, 'Ver setor →')); });
      res.appendChild(grade);
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
