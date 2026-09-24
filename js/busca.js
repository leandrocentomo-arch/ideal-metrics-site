/* A super busca (23/09/2026; desde 24/09 na segunda secao da home) e o painel
   «Todos os servicos» do menu grande.

   O site e estatico, entao a busca acontece no navegador: o indice
   busca-indice.json (gerado por _ferramentas/busca.py) so e baixado quando a
   pessoa digita a primeira letra, e fica em memoria dali em diante.

   PONTUACAO por pagina: titulo vale 10, os titulos internos 4, a chamada 3 e o
   corpo 1. Todos os termos digitados precisam aparecer em algum campo, senao a
   pagina sai. Acento e caixa nao contam: tudo e normalizado.

   TECLADO: seta para baixo e para cima andam na lista, Enter abre o primeiro
   (ou o marcado) e Esc limpa. */
(function(){
  var campo = document.getElementById('buscaCampo');
  var lista = document.getElementById('buscaRes');
  if(!campo || !lista) return;

  var indice = null, carregando = false, sel = -1;

  function limpa(s){
    return (s || '').toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g, '');
  }

  function carrega(){
    if(indice || carregando) return;
    carregando = true;
    fetch('busca-indice.json?v=1').then(function(r){ return r.json(); }).then(function(d){
      indice = d.map(function(p){
        return {u:p.u, t:p.t, d:p.d,
                lt:limpa(p.t), ld:limpa(p.d), lh:limpa(p.h), lc:limpa(p.c)};
      });
      carregando = false;
      if(campo.value.trim()) procura();
    }).catch(function(){ carregando = false; });
  }

  function procura(){
    var q = limpa(campo.value).split(/\s+/).filter(Boolean);
    if(!q.length){ lista.hidden = true; lista.innerHTML = ''; sel = -1; return; }
    if(!indice){ carrega(); return; }
    var achados = [];
    indice.forEach(function(p){
      var nota = 0, todos = true;
      q.forEach(function(termo){
        var n = 0;
        if(p.lt.indexOf(termo) >= 0) n += 10;
        if(p.lh.indexOf(termo) >= 0) n += 4;
        if(p.ld.indexOf(termo) >= 0) n += 3;
        if(p.lc.indexOf(termo) >= 0) n += 1;
        if(!n) todos = false;
        nota += n;
      });
      if(todos) achados.push({p:p, nota:nota});
    });
    achados.sort(function(a, b){ return b.nota - a.nota; });
    achados = achados.slice(0, 8);
    sel = -1;
    if(!achados.length){
      lista.innerHTML = '<li class="veu-res-vazio">Nada encontrado. Tente o nome da norma, do padrão ou do tema.</li>';
      lista.hidden = false;
      return;
    }
    lista.innerHTML = achados.map(function(a){
      return '<li role="option"><a href="' + a.p.u + '">' + a.p.t +
             (a.p.d ? '<span class="veu-res-d">' + a.p.d + '</span>' : '') + '</a></li>';
    }).join('');
    lista.hidden = false;
  }

  function marca(n){
    var itens = lista.querySelectorAll('li');
    if(!itens.length) return;
    if(sel >= 0 && itens[sel]) itens[sel].classList.remove('sel');
    sel = (n + itens.length) % itens.length;
    itens[sel].classList.add('sel');
    itens[sel].scrollIntoView({block:'nearest'});
  }

  campo.addEventListener('focus', carrega);
  campo.addEventListener('input', procura);
  campo.addEventListener('keydown', function(e){
    if(e.key === 'ArrowDown'){ e.preventDefault(); marca(sel + 1); }
    else if(e.key === 'ArrowUp'){ e.preventDefault(); marca(sel - 1); }
    else if(e.key === 'Enter'){
      var alvo = lista.querySelector(sel >= 0 ? 'li.sel a' : 'li a');
      if(alvo){ e.preventDefault(); location.href = alvo.getAttribute('href'); }
    } else if(e.key === 'Escape'){ campo.value = ''; procura(); }
  });

})();

/* «Todos os servicos», no menu grande, ABRE o painel com todos os temas em vez de
   navegar (24/09/2026). Sem JS o link continua indo para servicos.html. */
(function(){
  var alvo = document.getElementById('veuTodos'), mapa = document.getElementById('veuMapa');
  if(!alvo || !mapa) return;
  alvo.addEventListener('click', function(e){
    e.preventDefault();
    var aberto = !mapa.hidden;
    mapa.hidden = aberto;
    alvo.setAttribute('aria-expanded', aberto ? 'false' : 'true');
    if(!aberto) mapa.scrollIntoView({block:'nearest', behavior:'smooth'});
  });
  var fecha = document.getElementById('fechaMenu');
  if(fecha) fecha.addEventListener('click', function(){ mapa.hidden = true; alvo.setAttribute('aria-expanded','false'); });
})();

/* 24/09: o MEGA-MENU flutuante. Abre por «Todos os servicos» na barra (hover e
   clique) e fecha ao sair com o mouse, em Esc ou no clique fora. Dentro do veu,
   o mesmo item continua abrindo o painel proprio do veu. */
(function(){
  var abre = document.getElementById('megaAbre'), mega = document.getElementById('megaMenu');
  if(!abre || !mega) return;
  var timer = null;
  function mostra(){ clearTimeout(timer); mega.classList.add('aberto'); abre.setAttribute('aria-expanded','true'); }
  function esconde(){ timer = setTimeout(function(){ mega.classList.remove('aberto'); abre.setAttribute('aria-expanded','false'); }, 180); }
  abre.addEventListener('mouseenter', mostra);
  abre.addEventListener('mouseleave', esconde);
  mega.addEventListener('mouseenter', mostra);
  mega.addEventListener('mouseleave', esconde);
  abre.addEventListener('click', function(e){
    /* no primeiro clique abre; no segundo, com o painel aberto, navega */
    if(!mega.classList.contains('aberto')){ e.preventDefault(); mostra(); }
  });
  document.addEventListener('keydown', function(e){ if(e.key === 'Escape') esconde(); });
  document.addEventListener('click', function(e){ if(!mega.contains(e.target) && e.target !== abre) esconde(); });
})();

/* 24/09: cursor grosso do campo de busca (o do navegador e um fio de 1px) e a
   frase de abertura da segunda secao em maquina de escrever, quando aparece. */
(function(){
  var campo = document.getElementById('buscaCampo');
  var caixa = campo && campo.closest('.qc-busca-caixa'), caret = caixa && caixa.querySelector('.qc-caret');
  if(campo && caret){
    var medidor = document.createElement('span');
    medidor.style.cssText = 'position:absolute;visibility:hidden;white-space:pre;font:inherit';
    caixa.appendChild(medidor);
    function move(){
      var cs = getComputedStyle(campo);
      medidor.style.font = cs.font; medidor.style.letterSpacing = cs.letterSpacing;
      medidor.textContent = campo.value.slice(0, campo.selectionStart || campo.value.length);
      var recuo = parseFloat(cs.paddingLeft) || 0;
      caret.style.left = Math.min(recuo * (campo.value ? 1 : 0) + medidor.offsetWidth, campo.clientWidth - 8) + 'px';
    }
    move();
    campo.addEventListener('focus', function(){ caixa.classList.add('foco'); move(); });
    campo.addEventListener('blur', function(){ caixa.classList.remove('foco'); });
    ['input','keyup','click','select'].forEach(function(ev){ campo.addEventListener(ev, move); });
  }

  var lead = document.getElementById('qcLead');
  if(!lead || !('IntersectionObserver' in window)) return;
  var texto = lead.getAttribute('data-texto') || lead.textContent;
  var reduz = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  if(reduz) return;
  var feito = false;
  var obs = new IntersectionObserver(function(es){
    es.forEach(function(e){
      if(!e.isIntersecting || feito) return;
      feito = true; obs.disconnect();
      lead.textContent = '';
      var cur = document.createElement('span'); cur.className = 'qc-cursor'; lead.appendChild(cur);
      var i = 0;
      (function passo(){
        if(i < texto.length){
          lead.insertBefore(document.createTextNode(texto.charAt(i)), cur);
          i++;
          var ch = texto.charAt(i - 1);
          /* 24/09: «mais lento»: 55 ms por letra, 70 no espaco, 380 na virgula (era 22/34/160) */
          setTimeout(passo, ch === ',' ? 380 : (ch === ' ' ? 70 : 55));
        } else {
          setTimeout(function(){ lead.classList.add('pronta'); }, 900);
        }
      })();
    });
  }, {threshold: .35});
  obs.observe(lead);
})();
