/* Guia da home, «Setores» no desenho de Conteudo de destaque (10/10/2026): grade 3x3 com os nove setores e UMA foto
   menor a esquerda, no motor da trama (as nove fotos empilhadas, modo empilhado). A legenda traz o resumo do setor e
   os tres temas de gestao com mais normas em destaque (de window.IM_SETORES). O motor so liga perto da tela e e
   destruido longe dela.

   11/10/2026: «o efeito aqui nao esta igual ao da secao de baixo; era para ter sido igual». O movimento da grade
   agora e o MESMO da secao Conteudo de destaque (index.html, bloco «noticias (modo fluido)»), copiado numero a numero:
   - UM fundo azul so (.sx-bg), filho do cartao ativo, que voa de cartao em cartao por FLIP: 500 ms em power4.out;
   - UM quadrado da seta (90 px), filho do fundo, que viaja junto: abre ao entrar na grade (500 ms; a seta 400 ms
     com 100 ms de atraso), pulsa ao trocar de cartao (seta 1 -> 0 -> 1) e recolhe ao sair; os cartoes em repouso
     nao mostram seta;
   - a letra troca de cor com a mesma duracao e a mesma curva do fundo (CSS);
   - a foto funde em 800 ms, power4.inOut (gl.fundir no motor; a troca de classe faz a mesma fusao sem WebGL);
   - nao ha volta: ao sair, o estado fica no ultimo cartao visitado.
   Modo fluido = (hover:hover) E janela acima de 880 px; fora dele, o cartao pinta o proprio fundo (.on). */
(function(){
  var OFICIAL = [[21.2,50.9,80.6],[24.2,56.2,88.1],[103.0,146.1,189.4],[250,249,245]];
  var T_FUNDO = 500, T_BTN = 500, T_SETA = 400, ATRASO_SETA = 100;
  var P4OUT_EXATA   = 'linear(0, 0.4095 10%, 0.6723 20%, 0.8319 30%, 0.9222 40%, 0.9688 50%, 0.9898 60%, 0.9976 70%, 0.9997 80%, 1)';
  var P4OUT_RESERVA = 'cubic-bezier(0.22,1,0.36,1)';
  var P1INOUT = 'cubic-bezier(0.45,0,0.55,1)';

  function init(){
    var raiz = document.getElementById('sfSetores'); if(!raiz) return;
    var D = window.IM_SETORES;
    var grade = raiz.querySelector('.sx-grade');
    var cartoes = [].slice.call(raiz.querySelectorAll('.sx-card'));
    var camadas = [].slice.call(raiz.querySelectorAll('.sx-layer'));
    var midia = raiz.querySelector('.sx-midia');
    var resumo = raiz.querySelector('.sx-resumo'), temasEl = raiz.querySelector('.sx-temas');
    if(!grade || !cartoes.length || !midia) return;
    var gl = null, ativo = 0, dentro = false, mouseDentro = false;

    var temWAAPI = typeof Element !== 'undefined' && typeof Element.prototype.animate === 'function';
    var p4out = P4OUT_EXATA;
    try { if(!(window.CSS && CSS.supports && CSS.supports('transition-timing-function', P4OUT_EXATA))) p4out = P4OUT_RESERVA; }
    catch(e){ p4out = P4OUT_RESERVA; }
    function consulta(q){ return window.matchMedia ? window.matchMedia(q) : {matches:false}; }
    var mqHover = consulta('(hover: hover)'), mqEstreito = consulta('(max-width: 880px)'), mqCalmo = consulta('(prefers-reduced-motion: reduce)');
    function fluido(){ return mqHover.matches && !mqEstreito.matches; }
    function semMovimento(){ return mqCalmo.matches || !temWAAPI; }
    function anima(el, quadros, op){
      if(!temWAAPI) return null;
      try { return el.animate(quadros, op); }
      catch(e){
        if(op.easing !== P4OUT_EXATA) return null;
        p4out = P4OUT_RESERVA; op.easing = P4OUT_RESERVA;
        try { return el.animate(quadros, op); } catch(e2){ return null; }
      }
    }
    function solta(el){ if(el && el._sxA){ try { el._sxA.cancel(); } catch(e){} el._sxA = null; } }

    /* ---- legenda: resumo e os tres temas com mais normas em destaque ---- */
    function temas(id){
      if(!D) return '';
      var s = D.setores.filter(function(x){ return x.id === id; })[0]; if(!s) return '';
      var cont = {}, nomes = {};
      D.grupos.forEach(function(g){ nomes[g.id] = g.nome; });
      s.normas.forEach(function(n){ var g = D.normas[n].grupo; cont[g] = (cont[g] || 0) + 1; });
      return Object.keys(cont).sort(function(a, b){ return cont[b] - cont[a]; }).slice(0, 3).map(function(g){ return nomes[g]; }).join('  ·  ');
    }

    /* ---- o fundo unico e o quadrado unico (nascem aqui: sem JS a grade fica como no markup) ---- */
    var bg = document.createElement('div'); bg.className = 'sx-bg'; bg.setAttribute('aria-hidden', 'true');
    var molde = grade.querySelector('.sx-card > .sx-btn');
    var btn = molde ? molde.cloneNode(true) : document.createElement('div');
    if(!molde){ btn.className = 'sx-btn'; btn.innerHTML = '<svg width="22" height="16" viewBox="0 0 22 16"><path d="M0 8h19M13 2l6 6-6 6" fill="none" stroke="currentColor" stroke-width="1"/></svg>'; }
    btn.setAttribute('aria-hidden', 'true');
    bg.appendChild(btn);
    var seta = btn.querySelector('svg');

    /* 1. o fundo: FLIP (medir, cancelar, mudar de pai, medir de novo, animar ate «none») */
    function poeFundo(cartao, voa){
      var antes = null;
      if(voa && bg.parentNode && !semMovimento()) antes = bg.getBoundingClientRect();
      solta(bg);
      if(bg.parentNode !== cartao) cartao.appendChild(bg);
      if(!antes || !antes.width || !antes.height) return;
      var depois = bg.getBoundingClientRect();
      if(!depois.width || !depois.height) return;
      var dx = antes.left - depois.left, dy = antes.top - depois.top;
      var sx = antes.width / depois.width, sy = antes.height / depois.height;
      if(Math.abs(dx) < .5 && Math.abs(dy) < .5 && Math.abs(sx - 1) < .002 && Math.abs(sy - 1) < .002) return;
      bg._sxA = anima(bg, [{transform:'translate(' + dx + 'px,' + dy + 'px) scale(' + sx + ',' + sy + ')'}, {transform:'none'}],
        {duration:T_FUNDO, easing:p4out});
    }
    /* 2. a letra: so classe; a transicao de cor esta no CSS */
    function marca(i){ cartoes.forEach(function(c, k){ c.classList.toggle('on', k === i); }); }
    /* 3. a foto e a legenda */
    function trocaFoto(i){
      camadas.forEach(function(c, k){ c.classList.toggle('sx-layer-ativa', k === i); });
      if(gl) gl.fundir(i);
      if(resumo) resumo.textContent = cartoes[i].getAttribute('data-resumo');
      if(temasEl) temasEl.textContent = temas(cartoes[i].getAttribute('data-s'));
    }
    /* 4. o quadrado da seta: escala de repouso inline, animacao por cima */
    function escalaDe(el){
      var m = window.getComputedStyle(el).transform;
      if(!m || m === 'none') return 1;
      var p = /matrix\(\s*([^,]+)/.exec(m), v = p ? parseFloat(p[1]) : 1;
      return isNaN(v) ? 1 : v;
    }
    function escalaVai(el, alvo, ms, atraso){
      var de = escalaDe(el);
      solta(el);
      el.style.transform = 'scale(' + alvo + ')';
      if(semMovimento() || Math.abs(de - alvo) < .001) return;
      el._sxA = anima(el, [{transform:'scale(' + de + ')'}, {transform:'scale(' + alvo + ')'}],
        {duration:ms, delay:atraso || 0, easing:p4out, fill:'backwards'});
    }
    function abre(){ dentro = true; escalaVai(btn, 1, T_BTN, 0); if(seta) escalaVai(seta, 1, T_SETA, ATRASO_SETA); }
    function pulsa(){
      if(!seta || semMovimento()) return;
      if(seta._sxA && seta._sxA.playState === 'running') return;
      solta(seta);
      seta.style.transform = 'scale(1)';
      seta._sxA = anima(seta, [{transform:'scale(1)', easing:P1INOUT}, {transform:'scale(0)', easing:P1INOUT}, {transform:'scale(1)'}],
        {duration:T_BTN, easing:p4out});
    }
    function recolhe(){ if(!dentro) return; dentro = false; escalaVai(btn, 0, T_BTN, 0); if(seta) escalaVai(seta, 0, T_SETA, 0); }

    /* entrada e saida */
    function entra(i){
      if(!mqHover.matches) return;
      var mudou = i !== ativo;
      if(mudou){
        ativo = i;
        if(fluido()) poeFundo(cartoes[i], true);
        marca(i);
        trocaFoto(i);
      }
      if(!fluido()) return;
      if(!dentro) abre(); else if(mudou) pulsa();
    }
    function focoVisivelDentro(){
      var a = document.activeElement;
      if(!a || a === document.body || !grade.contains(a)) return false;
      try { return a.matches(':focus-visible'); } catch(e){ return true; }
    }
    cartoes.forEach(function(c, i){
      c.addEventListener('mouseenter', function(){ entra(i); });
      c.addEventListener('focusin', function(){ entra(i); });
    });
    grade.addEventListener('mouseenter', function(){ mouseDentro = true; });
    grade.addEventListener('mouseleave', function(){ mouseDentro = false; if(focoVisivelDentro()) return; recolhe(); });
    grade.addEventListener('focusout', function(e){
      var prox = e.relatedTarget;
      if(prox && grade.contains(prox)) return;
      if(mouseDentro) return;
      recolhe();
    });

    /* modo (carga e resize) */
    function aplicaModo(){
      var f = fluido();
      grade.classList.add('sx-parado');
      grade.classList.toggle('sx-fluido', f);
      solta(bg); solta(btn); solta(seta);
      dentro = false;
      btn.style.transform = 'scale(0)';
      if(seta) seta.style.transform = 'scale(0)';
      if(f) poeFundo(cartoes[ativo], false);
      marca(ativo);
      void grade.offsetWidth;
      grade.classList.remove('sx-parado');
    }
    function escuta(m){ if(!m) return; if(m.addEventListener) m.addEventListener('change', aplicaModo); else if(m.addListener) m.addListener(aplicaModo); }
    aplicaModo();
    escuta(mqHover); escuta(mqEstreito); escuta(mqCalmo);
    if(temasEl) temasEl.textContent = temas(cartoes[0].getAttribute('data-s'));

    /* o motor da trama: liga perto da tela, e destruido longe dela */
    if(!window.ditherVivo || !('IntersectionObserver' in window)) return;
    var planos = camadas.map(function(c){ return {el:midia, lum:c.querySelector('img').getAttribute('data-lum')}; });
    new IntersectionObserver(function(es){
      es.forEach(function(e){
        if(e.isIntersecting && !gl){
          gl = window.ditherVivo({brilhoTom:0.35, gama:0.88, ctr:1.55, escuro:0.35, lavaRepouso:0.12, raiz:midia, planos:planos,
            classeCanvas:'sx-gl', revelar:'visivel', empilhado:true, cores:OFICIAL, pincel:.7, zoomHover:1.03});
          if(gl && ativo) gl.fundir(ativo);
        } else if(!e.isIntersecting && gl){ gl.destruir(); gl = null; }
      });
    }, {rootMargin:'60% 0px 60% 0px'}).observe(midia);
  }
  if(document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init); else init();
})();
