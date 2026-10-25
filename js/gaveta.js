/* js/gaveta.js (17/10/2026): as duas ETIQUETAS FLUTUANTES do site, em todas as paginas.
   - A GAVETA DO GUIA, na borda esquerda: «este menu pode ficar flutuante em todas as paginas». A etiqueta mora na
     borda da gaveta e as duas deslizam juntas; clique ou arrasto para a direita abre, e Esc, [ Fechar ], clique fora
     ou arrasto para a esquerda fecham. O miolo (Por setor, Por tema de gestao, Por norma ou padrao) e o que estava
     no fim da secao Guia da home.
   - O WHATSAPP, na borda direita: «quero que o whatsapp tambem seja um menu flutuante assim, mas do lado direito, um
     pouco mais discreto, na cor do whatsapp». Substitui o botao redondo (.whatsapp-float, escondido aqui). Clicar
     na etiqueta abre um cartao para a esquerda com o numero e o botao «Abrir conversa».  */
/* 25/10/2026: «quero que estas linhas (de contorno da etiqueta que puxa as tabelas e menus) sejam desta cor, como padrao»: contorno das etiquetas em #336699 (o #0000FF da caneta durou uma rodada: «nao ficou legal o azul neon, pode ser o azul 336699») */
(function(){
  if(document.getElementById('gaveta')) return;
  var MIOLO = "<div class=\"mp-grade\">\n<nav class=\"mp-col\" aria-label=\"Por setor\">\n<div class=\"mp-col-cab\"><span class=\"mp-n\">01</span><h3 class=\"mp-col-tit\">Por setor</h3><p class=\"mp-q\">Onde a organização atua</p></div>\n<ul class=\"mp-lista\"><li><a href=\"setor-industria.html\"><span>Indústria</span><svg class=\"mp-seta\" viewBox=\"0 0 9 9\" aria-hidden=\"true\" focusable=\"false\"><path d=\"M0 4.35H8M4 8.35L8 4.35L4 .35\"/></svg></a></li><li><a href=\"setor-transporte-rodovias.html\"><span>Transporte e rodovias</span><svg class=\"mp-seta\" viewBox=\"0 0 9 9\" aria-hidden=\"true\" focusable=\"false\"><path d=\"M0 4.35H8M4 8.35L8 4.35L4 .35\"/></svg></a></li><li><a href=\"setor-facilities.html\"><span>Facilities</span><svg class=\"mp-seta\" viewBox=\"0 0 9 9\" aria-hidden=\"true\" focusable=\"false\"><path d=\"M0 4.35H8M4 8.35L8 4.35L4 .35\"/></svg></a></li><li><a href=\"setor-alimentos.html\"><span>Alimentos e serviços de alimentação</span><svg class=\"mp-seta\" viewBox=\"0 0 9 9\" aria-hidden=\"true\" focusable=\"false\"><path d=\"M0 4.35H8M4 8.35L8 4.35L4 .35\"/></svg></a></li><li><a href=\"setor-agro-florestal.html\"><span>Agro e florestal</span><svg class=\"mp-seta\" viewBox=\"0 0 9 9\" aria-hidden=\"true\" focusable=\"false\"><path d=\"M0 4.35H8M4 8.35L8 4.35L4 .35\"/></svg></a></li><li><a href=\"setor-saude.html\"><span>Saúde</span><svg class=\"mp-seta\" viewBox=\"0 0 9 9\" aria-hidden=\"true\" focusable=\"false\"><path d=\"M0 4.35H8M4 8.35L8 4.35L4 .35\"/></svg></a></li><li><a href=\"setor-energia.html\"><span>Energia e utilities</span><svg class=\"mp-seta\" viewBox=\"0 0 9 9\" aria-hidden=\"true\" focusable=\"false\"><path d=\"M0 4.35H8M4 8.35L8 4.35L4 .35\"/></svg></a></li><li><a href=\"setor-tecnologia.html\"><span>Tecnologia e serviços financeiros</span><svg class=\"mp-seta\" viewBox=\"0 0 9 9\" aria-hidden=\"true\" focusable=\"false\"><path d=\"M0 4.35H8M4 8.35L8 4.35L4 .35\"/></svg></a></li><li><a href=\"setor-servicos-setor-publico.html\"><span>Serviços e setor público</span><svg class=\"mp-seta\" viewBox=\"0 0 9 9\" aria-hidden=\"true\" focusable=\"false\"><path d=\"M0 4.35H8M4 8.35L8 4.35L4 .35\"/></svg></a></li></ul>\n</nav>\n<nav class=\"mp-col\" aria-label=\"Por tema de gestão\">\n<div class=\"mp-col-cab\"><span class=\"mp-n\">02</span><h3 class=\"mp-col-tit\">Por tema de gestão</h3><p class=\"mp-q\">O que a organização precisa gerir</p></div>\n<ul class=\"mp-lista\"><li><a href=\"norma-iso-9001.html\"><span>Qualidade</span><svg class=\"mp-seta\" viewBox=\"0 0 9 9\" aria-hidden=\"true\" focusable=\"false\"><path d=\"M0 4.35H8M4 8.35L8 4.35L4 .35\"/></svg></a></li><li><a href=\"norma-iso-14001.html\"><span>Meio ambiente</span><svg class=\"mp-seta\" viewBox=\"0 0 9 9\" aria-hidden=\"true\" focusable=\"false\"><path d=\"M0 4.35H8M4 8.35L8 4.35L4 .35\"/></svg></a></li><li><a href=\"norma-iso-45001.html\"><span>Saúde e segurança do trabalho</span><svg class=\"mp-seta\" viewBox=\"0 0 9 9\" aria-hidden=\"true\" focusable=\"false\"><path d=\"M0 4.35H8M4 8.35L8 4.35L4 .35\"/></svg></a></li><li><a href=\"seguranca-viaria.html\"><span>Segurança viária</span><svg class=\"mp-seta\" viewBox=\"0 0 9 9\" aria-hidden=\"true\" focusable=\"false\"><path d=\"M0 4.35H8M4 8.35L8 4.35L4 .35\"/></svg></a></li><li><a href=\"gestao-carbono.html\"><span>Clima e carbono</span><svg class=\"mp-seta\" viewBox=\"0 0 9 9\" aria-hidden=\"true\" focusable=\"false\"><path d=\"M0 4.35H8M4 8.35L8 4.35L4 .35\"/></svg></a></li><li><a href=\"esg.html\"><span>Sustentabilidade e ESG</span><svg class=\"mp-seta\" viewBox=\"0 0 9 9\" aria-hidden=\"true\" focusable=\"false\"><path d=\"M0 4.35H8M4 8.35L8 4.35L4 .35\"/></svg></a></li><li><a href=\"sedex-smeta.html\"><span>Responsabilidade social</span><svg class=\"mp-seta\" viewBox=\"0 0 9 9\" aria-hidden=\"true\" focusable=\"false\"><path d=\"M0 4.35H8M4 8.35L8 4.35L4 .35\"/></svg></a></li><li><a href=\"seguranca-alimentos.html\"><span>Segurança de alimentos</span><svg class=\"mp-seta\" viewBox=\"0 0 9 9\" aria-hidden=\"true\" focusable=\"false\"><path d=\"M0 4.35H8M4 8.35L8 4.35L4 .35\"/></svg></a></li><li><a href=\"compliance-seguranca-informacao.html\"><span>Segurança da informação</span><svg class=\"mp-seta\" viewBox=\"0 0 9 9\" aria-hidden=\"true\" focusable=\"false\"><path d=\"M0 4.35H8M4 8.35L8 4.35L4 .35\"/></svg></a></li><li><a href=\"compliance-seguranca-informacao.html\"><span>Compliance, riscos e continuidade</span><svg class=\"mp-seta\" viewBox=\"0 0 9 9\" aria-hidden=\"true\" focusable=\"false\"><path d=\"M0 4.35H8M4 8.35L8 4.35L4 .35\"/></svg></a></li></ul>\n</nav>\n<nav class=\"mp-col\" aria-label=\"Por norma ou padrão\">\n<div class=\"mp-col-cab\"><span class=\"mp-n\">03</span><h3 class=\"mp-col-tit\">Por norma ou padrão</h3><p class=\"mp-q\">O que a organização precisa comprovar</p></div>\n<ul class=\"mp-lista\"><li><a href=\"norma-iso-9001.html\"><span>ISO 9001</span><svg class=\"mp-seta\" viewBox=\"0 0 9 9\" aria-hidden=\"true\" focusable=\"false\"><path d=\"M0 4.35H8M4 8.35L8 4.35L4 .35\"/></svg></a></li><li><a href=\"norma-iso-14001.html\"><span>ISO 14001</span><svg class=\"mp-seta\" viewBox=\"0 0 9 9\" aria-hidden=\"true\" focusable=\"false\"><path d=\"M0 4.35H8M4 8.35L8 4.35L4 .35\"/></svg></a></li><li><a href=\"norma-iso-45001.html\"><span>ISO 45001</span><svg class=\"mp-seta\" viewBox=\"0 0 9 9\" aria-hidden=\"true\" focusable=\"false\"><path d=\"M0 4.35H8M4 8.35L8 4.35L4 .35\"/></svg></a></li><li><a href=\"seguranca-viaria.html\"><span>ISO 39001</span><svg class=\"mp-seta\" viewBox=\"0 0 9 9\" aria-hidden=\"true\" focusable=\"false\"><path d=\"M0 4.35H8M4 8.35L8 4.35L4 .35\"/></svg></a></li><li><a href=\"setor-facilities.html\"><span>ISO 41001</span><svg class=\"mp-seta\" viewBox=\"0 0 9 9\" aria-hidden=\"true\" focusable=\"false\"><path d=\"M0 4.35H8M4 8.35L8 4.35L4 .35\"/></svg></a></li><li><a href=\"compliance-seguranca-informacao.html\"><span>ISO/IEC 27001</span><svg class=\"mp-seta\" viewBox=\"0 0 9 9\" aria-hidden=\"true\" focusable=\"false\"><path d=\"M0 4.35H8M4 8.35L8 4.35L4 .35\"/></svg></a></li><li><a href=\"compliance-seguranca-informacao.html\"><span>ISO 37001 e ISO 37301</span><svg class=\"mp-seta\" viewBox=\"0 0 9 9\" aria-hidden=\"true\" focusable=\"false\"><path d=\"M0 4.35H8M4 8.35L8 4.35L4 .35\"/></svg></a></li><li><a href=\"seguranca-alimentos.html\"><span>ISO 22000 e FSSC 22000</span><svg class=\"mp-seta\" viewBox=\"0 0 9 9\" aria-hidden=\"true\" focusable=\"false\"><path d=\"M0 4.35H8M4 8.35L8 4.35L4 .35\"/></svg></a></li><li><a href=\"sedex-smeta.html\"><span>SEDEX / SMETA</span><svg class=\"mp-seta\" viewBox=\"0 0 9 9\" aria-hidden=\"true\" focusable=\"false\"><path d=\"M0 4.35H8M4 8.35L8 4.35L4 .35\"/></svg></a></li><li><a href=\"ifc-performance-standards.html\"><span>IFC Performance Standards</span><svg class=\"mp-seta\" viewBox=\"0 0 9 9\" aria-hidden=\"true\" focusable=\"false\"><path d=\"M0 4.35H8M4 8.35L8 4.35L4 .35\"/></svg></a></li><li><a href=\"carbono-inventario-gee.html\"><span>GHG Protocol e ISO 14064</span><svg class=\"mp-seta\" viewBox=\"0 0 9 9\" aria-hidden=\"true\" focusable=\"false\"><path d=\"M0 4.35H8M4 8.35L8 4.35L4 .35\"/></svg></a></li><li><a href=\"nrs.html\"><span>Normas regulamentadoras</span><svg class=\"mp-seta\" viewBox=\"0 0 9 9\" aria-hidden=\"true\" focusable=\"false\"><path d=\"M0 4.35H8M4 8.35L8 4.35L4 .35\"/></svg></a></li><li class=\"mp-fim\"><a href=\"servicos.html#stf\"><span>Todos os padrões, na grade e no filtro</span><svg class=\"mp-seta\" viewBox=\"0 0 9 9\" aria-hidden=\"true\" focusable=\"false\"><path d=\"M0 4.35H8M4 8.35L8 4.35L4 .35\"/></svg></a></li></ul>\n</nav>\n</div>\n<p class=\"mp-pe\">O portfólio completo está em <a href=\"servicos.html\">Todos os serviços</a> e na <a href=\"index.html#buscaCampo\">busca do site</a>. A <a href=\"contato.html\">equipe técnica da Ideal Metrics</a> atende pelo contato.</p>";
  var WA = 'https://wa.me/5511954684086';
  var css = document.createElement('style');
  css.textContent = [
    '.whatsapp-float{display:none!important}',
    '.gaveta{position:fixed;left:0;top:0;bottom:0;z-index:899;width:min(1180px,94vw);transform:translateX(-100%);transition:transform .7s cubic-bezier(.65,.05,.36,1);color:#14304C}',
    '.gaveta.aberta{transform:none}',
    '/* 19/10/2026: «deixe as etiquetas na cor do fundo da pagina, nao em branco» */ .gaveta-aba{position:absolute;left:100%;top:50%;transform:translateY(-50%);display:flex;flex-direction:column;align-items:center;gap:14px;padding:16px 9px;background:#FAF9F5;border:1px solid #336699;border-left:0;border-radius:0 3px 3px 0;cursor:pointer;color:#14304C;box-shadow:6px 0 18px -10px rgba(20,48,76,.35);transition:background .25s,color .25s;touch-action:none}',
    '.gaveta-aba svg{width:18px;height:11px;fill:currentColor;flex:none}',   /* 17/10/2026: o simbolo das outras etiquetas (os seis losangos) */
    '.gaveta-aba span,.wa-aba span{writing-mode:vertical-rl;transform:rotate(180deg);font-family:"IBM Plex Mono",monospace;font-size:11px;letter-spacing:.18em;text-transform:uppercase}',
    '.gaveta-aba:hover,.gaveta-aba:focus-visible,.gaveta.aberta .gaveta-aba{background:#14304C;color:#FAF9F5;outline:none}',
    '.gaveta-painel{position:absolute;inset:0;overflow:auto;padding:118px 48px 48px 56px;background:#FAF9F5;border-right:1px solid rgba(20,48,76,.16);box-shadow:24px 0 60px -30px rgba(20,48,76,.45);visibility:hidden;transition:visibility 0s .7s;text-align:left}',
    '.gaveta.aberta .gaveta-painel{visibility:visible;transition:visibility 0s}',
    '.gaveta-cab{display:flex;justify-content:space-between;align-items:center;font-family:"IBM Plex Mono",monospace;font-size:12px;letter-spacing:.14em;text-transform:uppercase;border-bottom:1px solid rgba(20,48,76,.16);padding-bottom:14px}',
    '.gaveta-fecha{background:none;border:0;font:inherit;letter-spacing:inherit;color:inherit;cursor:pointer;padding:4px 0}.gaveta-fecha:hover{color:#336699}',
    '.gaveta .mp-grade{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:0 44px;margin-top:28px}',
    '.gaveta .mp-col-cab{border-bottom:1px solid #14304C;padding-bottom:12px}',
    '.gaveta .mp-n{display:block;font-family:"IBM Plex Mono",monospace;font-size:11px;letter-spacing:.14em;color:#315275}',
    '.gaveta .mp-col-tit{margin:10px 0 4px;font-family:"IBM Plex Sans Condensed",sans-serif;font-weight:600;font-size:20px;line-height:1.2;color:#14304C;text-transform:none;letter-spacing:0}',
    '.gaveta .mp-q{margin:0;font-family:"IBM Plex Mono",monospace;font-size:11px;letter-spacing:.04em;color:#315275}',
    '.gaveta .mp-lista{list-style:none;margin:0;padding:0}.gaveta .mp-lista li{margin:0;padding:0}.gaveta .mp-lista li::before{content:none}',
    '.gaveta .mp-lista a{display:flex;justify-content:space-between;align-items:center;gap:14px;height:42px;box-sizing:border-box;padding:0 2px;border-bottom:1px solid rgba(20,48,76,.2);color:#14304C;text-decoration:none;font-family:"IBM Plex Sans Condensed",sans-serif;font-weight:500;font-size:16px;line-height:1.3}',
    '.gaveta .mp-lista a span{min-width:0;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}',
    '.gaveta .mp-seta{flex:none;width:9px;height:9px;overflow:visible;transition:transform .3s cubic-bezier(.4,0,.2,1)}.gaveta .mp-seta path{fill:none;stroke:currentColor;stroke-width:1}',
    '.gaveta .mp-lista a:hover .mp-seta,.gaveta .mp-lista a:focus-visible .mp-seta{transform:translateX(4px)}',
    '.gaveta .mp-fim a{font-family:"IBM Plex Mono",monospace;font-size:12px;letter-spacing:.04em;color:#315275}',
    '.gaveta .mp-pe{margin:36px 0 0;font-family:"IBM Plex Sans Condensed",sans-serif;font-size:16px;color:#315275}.gaveta .mp-pe a{color:#14304C;text-underline-offset:3px}',
    '.wa{position:fixed;right:0;bottom:96px;z-index:898;display:flex;align-items:stretch;transition:opacity .35s ease,transform .35s ease}',
    '.wa.oculto{opacity:0;transform:translateX(14px);pointer-events:none}',
    '.wa-aba{display:flex;flex-direction:column;align-items:center;gap:10px;padding:12px 7px;background:#25D366;color:#fff;border:0;border-radius:3px 0 0 3px;cursor:pointer;box-shadow:-5px 0 16px -10px rgba(20,48,76,.4);opacity:.92;transition:opacity .25s}',
    '.wa-aba:hover,.wa-aba:focus-visible,.wa.aberta .wa-aba{opacity:1;outline:none}',
    '.wa-aba img{width:15px;height:15px;filter:brightness(0) invert(1)}',
    '.wa-aba span{font-size:10px;letter-spacing:.16em}',
    '.wa-cartao{width:0;overflow:hidden;background:#FAF9F5;border:1px solid rgba(20,48,76,.16);border-right:0;border-radius:3px 0 0 3px;box-shadow:-10px 0 30px -18px rgba(20,48,76,.45);transition:width .5s cubic-bezier(.65,.05,.36,1);visibility:hidden}',
    '.wa.aberta .wa-cartao{width:250px;visibility:visible}',
    '.wa-dentro{width:250px;box-sizing:border-box;padding:16px 18px;display:flex;flex-direction:column;justify-content:center;height:100%;text-align:left}',
    '.wa-rot{margin:0;font-family:"IBM Plex Mono",monospace;font-size:10px;letter-spacing:.16em;text-transform:uppercase;color:#315275}',
    '.wa-num{margin:8px 0 12px;font-family:"IBM Plex Sans Condensed",sans-serif;font-size:19px;font-weight:600;color:#14304C}',
    '.wa-ir{align-self:flex-start;display:inline-flex;align-items:center;gap:8px;padding:7px 12px;border-radius:3px;background:#25D366;color:#fff;text-decoration:none;font-family:"IBM Plex Mono",monospace;font-size:11px;letter-spacing:.12em;text-transform:uppercase}',
    '.wa-ir:hover,.wa-ir:focus-visible{background:#1DA851;outline:none}',
    '.gaveta.oculta:not(.aberta) .gaveta-aba{opacity:0;pointer-events:none}',
    '.gaveta-aba{transition:background .25s,color .25s,opacity .45s ease,transform .55s cubic-bezier(.65,.05,.36,1)}',
    /* 19/10/2026: «as etiquetas devem existir somente dentro da pagina, nao sobre banner ou rodape, crie efeitos»: fora da area
       do conteudo a etiqueta recolhe para fora da tela (desliza e some) e volta deslizando ao entrar */
    '.gaveta.fora:not(.aberta) .gaveta-aba{transform:translate(-110%,-50%);opacity:0;pointer-events:none}',
    '.wa{transition:opacity .45s ease,transform .55s cubic-bezier(.65,.05,.36,1)}',
    '.wa.fora:not(.aberta){opacity:0;transform:translateX(110%);pointer-events:none}',
    '@media (prefers-reduced-motion:reduce){.gaveta{transition:none}}',
    '@media (max-width:880px){.gaveta-painel{padding:96px 22px 40px}.gaveta .mp-grade{grid-template-columns:1fr;gap:36px}.wa-aba{bottom:24px}}'
  ].join('\n');
  document.head.appendChild(css);

  var g = document.createElement('aside');
  g.className = 'gaveta'; g.id = 'gaveta'; g.setAttribute('aria-label', 'Guia do portfólio');
  g.innerHTML = '<button type="button" class="gaveta-aba" id="gavetaAba" aria-expanded="false" aria-controls="gavetaPainel"><svg viewBox="0 0 22 14" aria-hidden="true"><path d="M3 0l3 3-3 3-3-3zM11 0l3 3-3 3-3-3zM19 0l3 3-3 3-3-3zM3 8l3 3-3 3-3-3zM11 8l3 3-3 3-3-3zM19 8l3 3-3 3-3-3z"/></svg><span>Guia · setor · tema · norma</span></button>' +
    '<div class="gaveta-painel" id="gavetaPainel" role="dialog" aria-label="Guia do portfólio"><div class="gaveta-cab"><span>Guia do portfólio</span><button type="button" class="gaveta-fecha" id="gavetaFecha">[ Fechar ]</button></div>' + MIOLO + '</div>';
  document.body.appendChild(g);

  /* WHATSAPP (17/10/2026): «a etiqueta se expande para a esquerda para clicar no contato, nao leva direto ao contato» */
  var wa = document.createElement('div');
  wa.className = 'wa oculto'; wa.id = 'wa';
  wa.innerHTML = '<div class="wa-cartao" id="waCartao"><div class="wa-dentro"><p class="wa-rot">Atendimento pelo WhatsApp</p>' +
    '<p class="wa-num">Fale conosco</p><a class="wa-ir" href="' + WA + '" target="_blank" rel="noopener">Abrir conversa &rarr;</a></div></div>' +
    '<button type="button" class="wa-aba" id="waAba" aria-expanded="false" aria-controls="waCartao" aria-label="WhatsApp da Ideal Metrics"><img src="img/WhatsApp_Logo_White.svg" alt=""><span>WhatsApp</span></button>';
  document.body.appendChild(wa);
  var waAba = document.getElementById('waAba');
  function waAbre(sim){ wa.classList.toggle('aberta', sim); waAba.setAttribute('aria-expanded', sim ? 'true' : 'false'); }
  waAba.addEventListener('click', function(){ waAbre(!wa.classList.contains('aberta')); });
  document.addEventListener('pointerdown', function(e){ if(wa.classList.contains('aberta') && !wa.contains(e.target)) waAbre(false); });
  document.addEventListener('keydown', function(e){ if(e.key === 'Escape') waAbre(false); });

  /* REGRA DAS ETIQUETAS (17/10/2026): «uma etiqueta nao deve ficar em cima da outra». O WhatsApp so aparece depois de a
     pagina rolar um pouco (360 px) e some enquanto encostar em outra etiqueta (as da tira e da grade da home, ou a da
     gaveta); a da gaveta, fechada, tambem some se encostar em outra. Conferido na rolagem, no redimensionar e depois
     de cliques (a tira desliza). */
  var OUTRAS = '.sh-aba,.qc-mat-aba';
  function caixa(el){ var r = el.getBoundingClientRect(); return r.width && r.height && r.bottom > 0 && r.top < innerHeight ? r : null; }
  function bate(a, b){ return a && b && a.left < b.right + 6 && a.right > b.left - 6 && a.top < b.bottom + 6 && a.bottom > b.top - 6; }
  function colide(el, sel){ var r = caixa(el); if(!r) return false;
    return [].some.call(document.querySelectorAll(sel), function(o){ return o !== el && !el.contains(o) && bate(r, caixa(o)); }); }
  var pend = 0;
  /* 19/10/2026: a area em que as etiquetas existem: da base do banner, da migalha ou (na home) da tira e do letreiro, ate o
     topo do rodape. A etiqueta so aparece se couber inteira nessa faixa. */
  function zona(){
    var topo = 0;
    ['.page-banner', '.breadcrumb', '#shRolo', '.qc-letreiro'].forEach(function(sel){
      var e = document.querySelector(sel); if(e){ var b = e.getBoundingClientRect().bottom; if(b > topo) topo = b; } });
    var f = document.querySelector('footer'), fim = f ? f.getBoundingClientRect().top : innerHeight;
    return [topo + 8, fim - 8];
  }
  function cabe(r, z){ return r && r.height && r.top >= z[0] && r.bottom <= z[1]; }
  function confere(){
    pend = 0;
    var z = zona();
    var ga = document.getElementById('gavetaAba'), gt = innerHeight / 2 - ga.offsetHeight / 2;
    var gDentro = cabe({top: gt, bottom: gt + ga.offsetHeight, height: ga.offsetHeight}, z);
    g.classList.toggle('fora', !gDentro);
    var sn = document.querySelector('.sidenav'); if(sn) sn.classList.toggle('fora', !gDentro);
    wa.classList.toggle('fora', !cabe(waAba.getBoundingClientRect(), z));
    var desce = true;   /* 19/10/2026: o limite de 360 px de rolagem deu lugar a area do conteudo (acima) */
    var waBate = colide(waAba, OUTRAS + ',.gaveta-aba');
    wa.classList.toggle('oculto', !(desce && !waBate) && !wa.classList.contains('aberta'));
    g.classList.toggle('oculta', colide(document.getElementById('gavetaAba'), OUTRAS + (wa.classList.contains('oculto') ? '' : ',.wa-aba')));
  }
  function agenda(){ if(!pend) pend = requestAnimationFrame(confere); }
  addEventListener('scroll', agenda, {passive: true}); addEventListener('resize', agenda);
  document.addEventListener('click', function(){ setTimeout(agenda, 50); setTimeout(agenda, 900); setTimeout(agenda, 1700); });
  setTimeout(agenda, 300); setTimeout(agenda, 2500); confere();

  var aba = document.getElementById('gavetaAba'), painel = document.getElementById('gavetaPainel');
  function abre(sim){ g.classList.toggle('aberta', sim); aba.setAttribute('aria-expanded', sim ? 'true' : 'false'); if(sim) painel.scrollTop = 0; }
  var x0 = null, moveu = false;
  aba.addEventListener('pointerdown', function(e){ x0 = e.clientX; moveu = false; try { aba.setPointerCapture(e.pointerId); } catch(_){} });
  aba.addEventListener('pointermove', function(e){ if(x0 === null) return; var dx = e.clientX - x0; if(Math.abs(dx) > 30){ moveu = true; abre(dx > 0); x0 = null; } });
  aba.addEventListener('pointerup', function(){ if(x0 !== null && !moveu) abre(!g.classList.contains('aberta')); x0 = null; });
  aba.addEventListener('keydown', function(e){ if(e.key === 'Enter' || e.key === ' '){ e.preventDefault(); abre(!g.classList.contains('aberta')); } });
  document.getElementById('gavetaFecha').addEventListener('click', function(){ abre(false); aba.focus(); });
  document.addEventListener('keydown', function(e){ if(e.key === 'Escape' && g.classList.contains('aberta')){ abre(false); aba.focus(); } });
  document.addEventListener('pointerdown', function(e){ if(g.classList.contains('aberta') && !g.contains(e.target)) abre(false); });

  /* MENU LATERAL RECOLHIDO (17/10/2026): o conteudo do .sidenav vai para um painel e a etiqueta «Navegacao» fica na
     borda direita dele; o CSS (css/style.css, v88) recolhe a coluna. */
  var sn = document.querySelector('.sidenav');
  if(sn && !sn.querySelector('.sn-caixa')){
    var cx = document.createElement('div'); cx.className = 'sn-caixa';
    var pn = document.createElement('div'); pn.className = 'sn-painel'; pn.id = 'snPainel';
    var pi = document.createElement('div'); pi.className = 'sn-painel-in';
    while(sn.firstChild) pi.appendChild(sn.firstChild);
    pn.appendChild(pi); cx.appendChild(pn);
    var sa = document.createElement('button'); sa.type = 'button'; sa.className = 'sn-aba';
    sa.setAttribute('aria-expanded', 'false'); sa.setAttribute('aria-controls', 'snPainel');
    sa.innerHTML = '<svg viewBox="0 0 22 14" aria-hidden="true"><path d="M3 0l3 3-3 3-3-3zM11 0l3 3-3 3-3-3zM19 0l3 3-3 3-3-3zM3 8l3 3-3 3-3-3zM11 8l3 3-3 3-3-3zM19 8l3 3-3 3-3-3z"/></svg><span>Navegação</span>';
    cx.appendChild(sa); sn.appendChild(cx);
    /* 17/10/2026: «isso aqui nao deve ocorrer» (o painel aberto passava por cima do rodape no fim da pagina): a altura
       do painel vai ate o fim do texto da pagina (o .page-layout sem o branco de baixo) e, se sobrar menos de 160 px,
       o painel fecha. */
    var lay = sn.closest('.page-layout');
    var snMede = function(){
      if(!sn.classList.contains('aberta') || !lay) return;
      var fim = lay.getBoundingClientRect().bottom - parseFloat(getComputedStyle(lay).paddingBottom || 0);
      var cabe = Math.min(innerHeight - 30, fim) - sn.getBoundingClientRect().top;
      if(cabe < 160){ snAbre(false); return; }
      pi.style.maxHeight = Math.floor(cabe) + 'px';
    };
    var snAbre = function(sim){ sn.classList.toggle('aberta', sim); sa.setAttribute('aria-expanded', sim ? 'true' : 'false'); snMede(); };
    /* 19/10/2026: «ficaria legal as duas etiquetas encostadas»: a Navegacao fica fixa na borda da tela, colada a direita da
       etiqueta do Guia e com o topo alinhado a ela (mede a etiqueta do Guia; com a gaveta fechada). Antes (17/10) ficava
       na coluna da pagina, encostada na migalha e presa ao cabecalho. */
    var snCola = function(){
      if(innerWidth <= 900){ sn.style.left = ''; sn.style.top = ''; sn.style.transform = ''; return; }
      if(g.classList.contains('aberta')) return;
      var r = aba.getBoundingClientRect(); if(!r.width) return;
      sn.style.left = Math.round(r.right) + 'px'; sn.style.top = Math.round(r.top) + 'px'; sn.style.transform = 'none';
    };
    snCola();
    addEventListener('scroll', function(){ snCola(); snMede(); }, {passive: true}); addEventListener('resize', function(){ snCola(); snMede(); });
    sa.addEventListener('click', function(){ snAbre(!sn.classList.contains('aberta')); });
    document.addEventListener('keydown', function(e){ if(e.key === 'Escape') snAbre(false); });
    document.addEventListener('pointerdown', function(e){ if(sn.classList.contains('aberta') && !sn.contains(e.target)) snAbre(false); });
  }
})();
