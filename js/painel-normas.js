/* Painel de normas ISO. Dados: dados/painel-normas.json (gerado por _ferramentas/painel_normas.py),
   dados/painel-mudancas.json (diferenças entre gerações) e dados/mundo-110m.json (world-atlas).
   Fontes públicas: ISO Open Data (ODC-By 1.0) e ISO Survey 2025. */
(function () {
  'use strict';
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
  var esc = function (s) { return String(s == null ? '' : s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); };
  /* 27/10/2026, versão em inglês («faça uma versão em inglês de todo esse conteúdo… tem que ter as duas bandeirinhas no canto
     direito, tem que ser default português»): o idioma vem de ?lang=en|pt na URL ou da última escolha guardada (localStorage);
     sem nada, português. T(pt, en) escolhe o texto. Os dados (JSON) são os mesmos nas duas línguas, então a atualização
     semanal da rotina «Ballots ISO/ABNT» vale para as duas sem passo extra. */
  var LANG = (function () { var q = /[?&]lang=(en|pt)\b/.exec(location.search); if (q) return q[1]; try { return localStorage.getItem('pn-lang') === 'en' ? 'en' : 'pt'; } catch (e) { return 'pt'; } })();
  var EN = LANG === 'en', T = function (pt, en) { return EN ? en : pt; };
  var MESES = EN ? ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec'] : ['jan', 'fev', 'mar', 'abr', 'mai', 'jun', 'jul', 'ago', 'set', 'out', 'nov', 'dez'];
  var dataBR = function (iso) { var p = String(iso).split('-'); return p.length < 3 ? iso : p[2] + '-' + MESES[+p[1] - 1] + '-' + p[0]; };   // dd-mmm-aaaa (26/10/2026)
  var fmt = function (n) { return (n == null ? '' : Number(n).toLocaleString(EN ? 'en-US' : 'pt-BR')); };

  var FASES = [
    ['proposta', 'Proposta', '00 e 10', 'Estudo preliminar ou proposta de trabalho novo (NP). Os países votam se a norma deve existir. Nada do texto está decidido.'],
    ['preparacao', 'Rascunho de trabalho', '20', 'Um grupo de especialistas escreve o primeiro texto (WD). Circula só dentro do grupo de trabalho.'],
    ['comite', 'Rascunho de comitê', '30', 'O texto (CD) é discutido e comentado pelos países membros do comitê. Ainda muda bastante.'],
    ['consulta', 'Consulta pública', '40', 'O Draft International Standard (DIS) vai a voto de todos os membros da ISO, por 12 semanas. No Brasil, a ABNT abre consulta nacional. É o primeiro texto estável.'],
    ['aprovacao', 'Aprovação final', '50', 'O Final Draft (FDIS) recebe só voto, sem comentário técnico. Aprovado, a ISO publica em poucas semanas. É a versão que vai valer.'],
    ['publicada', 'Publicada', '60', 'Norma em vigor. Pode ser comprada na ISO e, no Brasil, na ABNT (versão NBR).'],
    ['revisao', 'Revisão sistemática', '90', 'A cada cinco anos a ISO consulta os países: manter, revisar ou cancelar. Um voto por revisar abre um projeto novo e a edição atual segue válida até a nova sair.']
  ];
  if (EN) FASES = [
    ['proposta', 'Proposal', '00 and 10', 'Preliminary study or new work item proposal (NP). Member countries vote on whether the standard should exist. Nothing in the text is settled.'],
    ['preparacao', 'Working draft', '20', 'A group of experts writes the first text (WD). It circulates only within the working group.'],
    ['comite', 'Committee draft', '30', 'The text (CD) is discussed and commented on by the committee member countries. It still changes considerably.'],
    ['consulta', 'Enquiry', '40', 'The Draft International Standard (DIS) goes to a vote of all ISO members for 12 weeks. In Brazil, ABNT opens a national consultation. It is the first stable text.'],
    ['aprovacao', 'Final approval', '50', 'The Final Draft (FDIS) receives a vote only, without technical comments. Once approved, ISO publishes it within a few weeks. It is the version that will apply.'],
    ['publicada', 'Published', '60', 'Standard in force. It can be purchased from ISO and, in Brazil, from ABNT (NBR version).'],
    ['revisao', 'Systematic review', '90', 'Every five years ISO consults member countries: confirm, revise or withdraw. A vote to revise opens a new project, and the current edition remains valid until the new one is published.']
  ];
  var FASE_IDX = {}; FASES.forEach(function (f, i) { FASE_IDX[f[0]] = i; });
  var TIPOS = { IS: 'Norma internacional', TS: 'Especificação técnica', TR: 'Relatório técnico', PAS: 'Especificação publicamente disponível', IWA: 'Acordo de workshop internacional', GUIDE: 'Guia ISO' };
  if (EN) TIPOS = { IS: 'International Standard', TS: 'Technical Specification', TR: 'Technical Report', PAS: 'Publicly Available Specification', IWA: 'International Workshop Agreement', GUIDE: 'ISO Guide' };
  /* nomes dos temas em inglês, pelo id do JSON; tema novo sem tradução aparece com o nome em português até entrar aqui */
  var TEMAS_EN = { clima: 'Climate and carbon', ambiente: 'Environment', qualidade: 'Quality', sst: 'Occupational health and safety', viaria: 'Road traffic safety', esg: 'Sustainability and ESG', social: 'Social responsibility and value chain', alimentos: 'Food safety', informacao: 'Information security and privacy', compliance: 'Compliance, risk and continuity', conformidade: 'Conformity assessment', facilities: 'Facilities', energia: 'Energy', consultoria: 'Management consulting' };
  var CHAVE = ['9001', '14001', '45001', '39001', '22000', '27001', '37001', '37301', '14064-1', '14067', '14068-1', '14060', '41001', '22301', '31000', '50001', '42001', '53001', '59004', '17065', '17021-1'];
  var SURVEY_NOME = { '9001': 'ISO 9001', '14001': 'ISO 14001', '45001': 'ISO 45001', '27001': 'ISO/IEC 27001', '22000': 'ISO 22000', '13485': 'ISO 13485', '50001': 'ISO 50001', '20000-1': 'ISO/IEC 20000-1', '37001': 'ISO 37001', '22301': 'ISO 22301', '39001': 'ISO 39001', '28000': 'ISO 28000', '37301': 'ISO 37301', '41001': 'ISO 41001', '42001': 'ISO/IEC 42001', '44001': 'ISO 44001', '21001': 'ISO 21001', '55001': 'ISO 55001', '20121': 'ISO 20121', '22716': 'ISO 22716' };
  var LATAM = ['AR', 'BO', 'BR', 'CL', 'CO', 'CR', 'CU', 'DO', 'EC', 'SV', 'GT', 'HN', 'MX', 'NI', 'PA', 'PY', 'PE', 'PR', 'UY', 'VE'];

  var D = null, MUD = null, MUNDO = null, WORLD_OK = false;
  var F = { q: '', temas: {}, fases: {}, tipos: {}, pagina: false, ord: 'num' };
  var paisNome = (window.Intl && Intl.DisplayNames) ? new Intl.DisplayNames([EN ? 'en' : 'pt-BR'], { type: 'region' }) : null;

  function nomePais(a2) {
    try { var n = paisNome && paisNome.of(a2); if (n && n !== a2) return n; } catch (e) { }
    return (D.paises[a2] && D.paises[a2].nome) || a2;
  }

  /* ---------- idioma (27/10/2026) ---------- */
  (function idioma() {
    var q = /[?&]lang=(en|pt)\b/.exec(location.search); if (q) { try { localStorage.setItem('pn-lang', q[1]); } catch (e) { } }
    if (EN) {
      document.documentElement.lang = 'en';
      document.title = 'ISO Standards Dashboard | Ideal Metrics';
      var ds = 'Progress of ISO standards for management systems, sustainability and safety: stage, committee, systematic review and certificates by country. Sources: ISO Open Data and ISO Survey.';
      $$('meta[name="description"],meta[property="og:description"]').forEach(function (m) { m.setAttribute('content', ds); });
      $$('meta[property="og:title"]').forEach(function (m) { m.setAttribute('content', document.title); });
      /* o texto em inglês do HTML fica no próprio elemento: data-en (conteúdo), data-en-ph (placeholder), data-en-al (aria-label) */
      $$('[data-en]').forEach(function (el) { el.innerHTML = el.getAttribute('data-en'); });
      $$('[data-en-ph]').forEach(function (el) { el.setAttribute('placeholder', el.getAttribute('data-en-ph')); });
      $$('[data-en-al]').forEach(function (el) { el.setAttribute('aria-label', el.getAttribute('data-en-al')); });
    }
    /* bandeirinhas: a escolha fica guardada e a página recarrega na mesma aba; o inglês leva ?lang=en na URL (link compartilhável) */
    $$('.pn-lang button').forEach(function (b) {
      b.setAttribute('aria-pressed', b.dataset.lang === LANG);
      b.addEventListener('click', function () {
        if (b.dataset.lang === LANG) return;
        try { localStorage.setItem('pn-lang', b.dataset.lang); } catch (e) { }
        var s = location.search.replace(/([?&])lang=(en|pt)(&|$)/, '$1').replace(/[?&]$/, '');
        if (b.dataset.lang === 'en') s += (s ? '&' : '?') + 'lang=en';
        location.replace(location.pathname + s + location.hash);
      });
    });
  })();

  /* 31/10/2026, «faça a versão escura dessa página; dê a opção, mesmo que a versão clara deva ficar como default»: interruptor
     sol/lua ao lado das bandeirinhas; a escolha fica guardada (localStorage pn-tema) e o <head> já a aplica antes de pintar.
     Sem escolha guardada, claro. Ao trocar, avisa o mapa (evento pn-tema) para refazer as cores da trama. */
  /* 31/10, 2º, «deixar o fundo escuro um pouco mais claro… não refaça o atual, faça uma terceira opção»: escuro suave =
     data-tema=noite + data-noite=clara (todas as regras do escuro valem, e o bloco do suave clareia o fundo e as placas) */
  var NOITE = document.documentElement.getAttribute('data-tema') === 'noite', TEMA = NOITE ? ({ azul: 'marinho', marinho: 'marinho' }[document.documentElement.getAttribute('data-noite')] || 'noite') : 'dia';   // 31/10, 7º: «tonalidade de azul pode tirar»: ficam claro, escuro e marinho; quem tinha azul cai no marinho   // 31/10, 6º: quarta opção «marinho», entre o escuro e o #336699   // 31/10, 4º: terceira opção «azul», mais clara, puxada para o #336699   // 31/10, 3º: «gostei dessa segunda, pode eliminar a outra noite»: só claro e escuro (o escuro é o suave)
  (function () {
    var lang = $('.pn-lang'); if (!lang) return;
    var t = document.createElement('div'); t.className = 'pn-tema'; t.setAttribute('role', 'group'); t.setAttribute('aria-label', T('Tema claro ou escuro', 'Light or dark theme'));
    t.innerHTML = '<button type="button" data-tema="dia" title="' + T('Claro', 'Light') + '" aria-label="' + T('Claro', 'Light') + '"><svg viewBox="0 0 16 16" aria-hidden="true"><circle cx="8" cy="8" r="3"/><path d="M8 1v2M8 13v2M1 8h2M13 8h2M3 3l1.4 1.4M11.6 11.6L13 13M13 3l-1.4 1.4M4.4 11.6L3 13"/></svg></button>' +
      '<button type="button" data-tema="noite" title="' + T('Escuro', 'Dark') + '" aria-label="' + T('Escuro', 'Dark') + '"><svg viewBox="0 0 16 16" aria-hidden="true"><circle cx="8" cy="8" r="4.6"/><path d="M8 1v14"/></svg></button>' +
      '<button type="button" data-tema="marinho" title="' + T('Marinho', 'Navy') + '" aria-label="' + T('Marinho', 'Navy') + '"><svg viewBox="0 0 16 16" aria-hidden="true"><circle cx="8" cy="8" r="4.6"/><circle class="cheio" cx="8" cy="8" r="2"/></svg></button>';
   // 31/10: «um ciclo sem preenchimento, com uma linha no meio, na vertical, um pouco acima e abaixo do ciclo, na altura do sol"
    /* 31/10, «aqui tem que estar tudo na mesma linha… faça as bandeiras melhores e coloque PT e EN»: tema e idioma numa barra só
       (.pn-ctrl), com a mesma altura; cada bandeira ganha a sigla */
    var ctrl = document.createElement('div'); ctrl.className = 'pn-ctrl'; lang.parentNode.insertBefore(ctrl, lang);
    ctrl.appendChild(t); ctrl.appendChild(lang);
    $$('button', lang).forEach(function (b) { if (!$('.sigla', b)) { var sg = document.createElement('span'); sg.className = 'sigla'; sg.textContent = b.dataset.lang.toUpperCase(); b.appendChild(sg); } });
    function marca() { $$('button', t).forEach(function (b) { b.setAttribute('aria-pressed', b.dataset.tema === TEMA); }); }
    marca();
    $$('button', t).forEach(function (b) {
      b.addEventListener('click', function () {
        if (b.dataset.tema === TEMA) return; TEMA = b.dataset.tema; NOITE = TEMA !== 'dia';
        var h = document.documentElement;
        if (NOITE) h.setAttribute('data-tema', 'noite'); else h.removeAttribute('data-tema');
        if (NOITE) h.setAttribute('data-noite', TEMA === 'azul' || TEMA === 'marinho' ? TEMA : 'clara'); else h.removeAttribute('data-noite');
        try { localStorage.setItem('pn-tema', TEMA); } catch (e) { }
        marca(); document.dispatchEvent(new CustomEvent('pn-tema'));
      });
    });
  })();

  /* ---------- carga ---------- */
  Promise.all([
    fetch('dados/painel-normas.json?v=' + (document.querySelector('script[src*="painel-normas.js"]').src.split('v=')[1] || 1)).then(function (r) { return r.json(); }),
    fetch('dados/painel-mudancas.json').then(function (r) { return r.ok ? r.json() : { itens: [] }; }).catch(function () { return { itens: [] }; })
  ]).then(function (res) {
    D = res[0]; MUD = res[1];
    if (EN) D.temas.forEach(function (t) { if (TEMAS_EN[t.id]) t.nome = TEMAS_EN[t.id]; });
    D.temasMap = {}; D.temas.forEach(function (t) { D.temasMap[t.id] = t.nome; });
    D.porNum = {}; D.normas.forEach(function (n) { (D.porNum[n.num] = D.porNum[n.num] || []).push(n); });
    montaFiltros(); liga(); render();
    $('#pn-gerado').textContent = dataBR(D.gerado);
    var h = location.hash.replace('#', '');
    if (/^n\d+$/.test(h)) abreDetalhe(+h.slice(1));
    else mostraAba(h && $('#v-' + h) ? h : 'mapa');   /* 27/10: Certificados no mundo é a primeira aba e abre por padrão */
  });

  /* ---------- filtros ---------- */
  function montaFiltros() {
    var cont = {}; D.normas.forEach(function (n) { cont[n.tema] = (cont[n.tema] || 0) + 1; });
    $('#f-temas').innerHTML = D.temas.filter(function (t) { return cont[t.id]; }).map(function (t) {
      return '<label class="pn-op"><input type="checkbox" data-k="temas" value="' + t.id + '" checked> <span>' + esc(t.nome) + '</span><span class="n">' + cont[t.id] + '</span></label>';
    }).join('');
    var cf = {}; D.normas.forEach(function (n) { cf[n.fase] = (cf[n.fase] || 0) + 1; });
    $('#f-fases').innerHTML = FASES.map(function (f) {
      return '<label class="pn-op' + (cf[f[0]] ? '' : ' off') + '"><input type="checkbox" data-k="fases" value="' + f[0] + '" checked> <span>' + f[1] + ' <span class="m" style="font-size:10px">' + f[2] + '</span></span><span class="n">' + (cf[f[0]] || 0) + '</span></label>';
    }).join('');
    var ct = {}; D.normas.forEach(function (n) { ct[n.tipo] = (ct[n.tipo] || 0) + 1; });
    $('#f-tipos').innerHTML = Object.keys(TIPOS).filter(function (t) { return ct[t]; }).map(function (t) {
      return '<label class="pn-op"><input type="checkbox" data-k="tipos" value="' + t + '" checked> <span>' + TIPOS[t] + ' <span class="m" style="font-size:10px">' + t + '</span></span><span class="n">' + ct[t] + '</span></label>';
    }).join('');
    ['temas', 'fases', 'tipos'].forEach(function (k) { F[k] = {}; $$('input[data-k=' + k + ']').forEach(function (i) { F[k][i.value] = true; }); });
  }

  function liga() {
    $('#pn-q').addEventListener('input', function (e) { F.q = e.target.value.trim().toLowerCase(); renderLogo(); });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Enter' && e.target.classList && e.target.classList.contains('pn-item')) abreDetalhe(+e.target.dataset.id);
    });
    var cab = $('.pn-cab'), poeCab = function () { $('.pn').style.setProperty('--cab-h', cab.offsetHeight + 'px'); };
    poeCab(); window.addEventListener('resize', poeCab);
    document.addEventListener('change', function (e) {
      var i = e.target; if (i.dataset && i.dataset.k) { F[i.dataset.k][i.value] = i.checked; render(); }
      if (i.id === 'f-pagina') { F.pagina = i.checked; render(); }
    });
    $$('.pn-bloco .m button').forEach(function (b) {
      b.addEventListener('click', function () {
        var k = b.dataset.k, on = b.dataset.on === '1';
        $$('input[data-k=' + k + ']').forEach(function (i) { i.checked = on; F[k][i.value] = on; });
        render();
      });
    });
    $$('.pn-abas button').forEach(function (b) { b.addEventListener('click', function () { mostraAba(b.dataset.aba); }); });
    $$('.pn-ord button').forEach(function (b) { b.addEventListener('click', function () { F.ord = b.dataset.ord; $$('.pn-ord button').forEach(function (x) { x.setAttribute('aria-pressed', x === b); }); render(); }); });
    $('#pn-det .fechar').addEventListener('click', fechaDetalhe);
    $('#pn-veu').addEventListener('click', fechaDetalhe);
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape') fechaDetalhe(); });
    document.addEventListener('click', function (e) {
      var a = e.target.closest('[data-id]'); if (a) { abreDetalhe(+a.dataset.id); }
    });
  }

  /* 27/10: a coluna de busca e filtros fica recolhida numa etiqueta e se puxa para abrir (Leandro: «o menu da esquerda pode ser
     puxado por tag, para ficar mais espaço») */
  /* 27/10: «talvez um tag colapsado como o do lado esquerdo, mas no topo, com os elementos do menu»: no computador a tarja e a
     barra do menu ficam recolhidas acima da tela e uma etiqueta «Menu» no topo (mesma família da etiqueta da gaveta) as puxa
     para baixo; Esc, clique fora ou a própria etiqueta recolhem. Ganha os 72 px do topo para o painel. */
  (function () {
    var b = document.createElement('button'); b.type = 'button'; b.className = 'pn-menu-puxa'; b.setAttribute('aria-expanded', 'false'); b.setAttribute('aria-label', T('Abrir o menu do site', 'Open the site menu'));
    b.innerHTML = '<svg viewBox="0 0 22 14" aria-hidden="true"><path d="M3 0l3 3-3 3-3-3zM11 0l3 3-3 3-3-3zM19 0l3 3-3 3-3-3zM3 8l3 3-3 3-3-3zM11 8l3 3-3 3-3-3zM19 8l3 3-3 3-3-3z"/></svg><span>Menu</span>';
    document.body.appendChild(b);
    /* 27/10: «o logo tem que aparecer sempre»: cópia da caixa do logo, fixa no lugar de sempre, visível enquanto o menu está
       recolhido (a original desce junto com a barra quando o menu abre) */
    var marca = $('header.barra .barra-marca'); if (marca) { var cp = marca.cloneNode(true); cp.classList.add('pn-logo-fixo'); cp.removeAttribute('id'); ($('.pn-cab') || document.body).appendChild(cp); if (window.bateAsasMonograma) bateAsasMonograma(cp.querySelector('img')); }   // 27/10: sem o brilho prateado («tire o pulse do logo também»)   // dentro do cabeçalho do painel: rola junto com ele («o logo tem que ficar fixo [no lugar], está descendo junto no scroll»)
    /* 27/10: a batida de asas (antes aqui) vive em js/monograma-asas.js, compartilhado por todas as páginas */
    function poe(ab) { document.body.classList.toggle('menu-aberto', ab); b.setAttribute('aria-expanded', ab); b.setAttribute('aria-label', ab ? T('Recolher o menu do site', 'Collapse the site menu') : T('Abrir o menu do site', 'Open the site menu')); }
    b.addEventListener('click', function () { poe(!document.body.classList.contains('menu-aberto')); });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && document.body.classList.contains('menu-aberto')) poe(false); });
    document.addEventListener('pointerdown', function (e) { if (document.body.classList.contains('menu-aberto') && !e.target.closest('.tarja, header.barra, .mega-menu, .pn-menu-puxa')) poe(false); });
  })();

  /* 31/10/2026, «copie o efeito de vidro feito no HASDA para o painel de normas»: atrás do vidro, manchas de cor nas cores da
     marca flutuando devagar e o rastro de luz do mouse (molde do dashboard do HASDA 2027: raio 36, 680 ms, força .46); o
     desfoque do vidro espalha os dois. Sem movimento com prefers-reduced-motion. */
  (function () {
    var f = document.createElement('div'); f.className = 'pn-fundo'; f.setAttribute('aria-hidden', 'true');
    f.innerHTML = '<i class="o1"></i><i class="o2"></i><i class="o3"></i><i class="o4"></i><i class="o5"></i>';
    document.body.insertBefore(f, document.body.firstChild);
    if (window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches) return;
    var cv = document.createElement('canvas'); cv.className = 'pn-luz'; cv.setAttribute('aria-hidden', 'true'); document.body.insertBefore(cv, f.nextSibling);
    var cx = cv.getContext('2d'); if (!cx) return;
    /* 31/10, «o rastro na tela escura está muito forte… deixa menos intenso; queria o rastro na tela clara também»: no escuro,
       luz azul a .2 (era .46); no claro, a luz branca não aparecia sobre o fundo claro, então o rastro é um véu azul da marca
       a .12, pintado por cima (sem somar luz). Mesma velocidade (680 ms) */
    var RAIO = 36, VIDA = 680, FORCA = .46, pts = [], laco = 0, dpr = Math.min(2, window.devicePixelRatio || 1);
    function medida() { var w = Math.round(innerWidth * dpr), h = Math.round(innerHeight * dpr); if (cv.width !== w || cv.height !== h) { cv.width = w; cv.height = h; } }
    function pinta() {
      var ag = performance.now(); pts = pts.filter(function (p) { return ag - p.t < VIDA; });
      cx.clearRect(0, 0, cv.width, cv.height); cx.globalCompositeOperation = NOITE ? 'lighter' : 'source-over'; FORCA = NOITE ? .2 : .12;
      pts.forEach(function (p) { var k = 1 - (ag - p.t) / VIDA, rr = RAIO * dpr * (.35 + .65 * k), gr = cx.createRadialGradient(p.x, p.y, 0, p.x, p.y, rr); var lz = NOITE ? '150,180,255' : '51,102,153'; gr.addColorStop(0, 'rgba(' + lz + ',' + (FORCA * k * k) + ')'); gr.addColorStop(1, 'rgba(' + lz + ',0)'); cx.fillStyle = gr; cx.beginPath(); cx.arc(p.x, p.y, rr, 0, 6.2832); cx.fill(); });
      laco = pts.length ? requestAnimationFrame(pinta) : 0;
    }
    document.addEventListener('pointermove', function (e) { if (e.pointerType === 'touch') return; medida(); pts.push({ x: e.clientX * dpr, y: e.clientY * dpr, t: performance.now() }); if (!laco) laco = requestAnimationFrame(pinta); }, { passive: true });
  })();

  $('.pn-puxa').addEventListener('click', function () {
    var ab = $('.pn').classList.toggle('lado-aberto');
    this.setAttribute('aria-expanded', ab); this.setAttribute('aria-label', ab ? T('Recolher busca e filtros', 'Collapse search and filters') : T('Abrir busca e filtros', 'Open search and filters'));
    if (ab) setTimeout(function () { $('#pn-q').focus({ preventScroll: true }); }, 360);
  });

  /* 27/10: navegação entre botões sempre com deslize (Leandro: «a navegação entre botões deve ser sempre com aquele efeito de
     deslize»): uma placa escura desliza do botão anterior para o escolhido, nas abas e nas normas do mapa */
  function desliza(caixa, sel) {
    if (!caixa) return;
    var pl = caixa.querySelector('.desliza'), b = caixa.querySelector(sel);
    if (!pl) { pl = document.createElement('span'); pl.className = 'desliza sem-anima'; caixa.insertBefore(pl, caixa.firstChild); }
    if (!b || !b.offsetWidth) return;
    pl.style.width = b.offsetWidth + 'px'; pl.style.height = b.offsetHeight + 'px';
    pl.style.transform = 'translate(' + b.offsetLeft + 'px,' + b.offsetTop + 'px)';
    if (pl.classList.contains('sem-anima')) { pl.offsetWidth; pl.classList.remove('sem-anima'); }
    var esq = b.offsetLeft - caixa.scrollLeft, dir = esq + b.offsetWidth;   // na fileira que rola, traz o escolhido para a vista
    if (caixa.scrollWidth > caixa.clientWidth && (esq < 0 || dir > caixa.clientWidth)) caixa.scrollTo({ left: b.offsetLeft - 24, behavior: 'smooth' });
  }
  function deslizaTudo() { desliza($('.pn-abas'), '[aria-selected=true]'); desliza($('#mp-sel'), '[aria-pressed=true]'); desliza($('#st-sel'), '[aria-pressed=true]'); if ($('#br-sel button')) desliza($('#br-sel'), '[aria-pressed=true]'); }
  window.addEventListener('resize', deslizaTudo);

  /* 27/10: efeito de entrada: cada filho direto do bloco (linhas, cartões) nasce 10 px abaixo e sobe, um atrás do outro */
  /* 27/10, 2ª versão («a entrada, nem desta nem das tabelas, seja "onda", mas entrada da esquerda para direita, deslize»): o
     bloco inteiro desliza da esquerda de uma vez; nada de atraso item a item */
  function entra(bloco) {
    if (!bloco || (window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches)) return;
    bloco.classList.remove('entra'); void bloco.offsetWidth; bloco.classList.add('entra');
  }
  /* 27/10: «para as tabelas, no efeito de entrada, faça as linhas surgirem de cima para baixo»: cada linha nasce 8 px acima
     e desce no lugar, uma atrás da outra (35 ms; a partir da 25ª todas juntas, já fora da tela) */
  function cascata(caixa, sel) {
    if (!caixa || (window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches)) return;
    var xs = $$(sel, caixa);
    xs.forEach(function (x, i) { x.classList.remove('cai'); x.style.animationDelay = (Math.min(i, 24) * .035).toFixed(3) + 's'; });
    void caixa.offsetWidth;
    xs.forEach(function (x) { x.classList.add('cai'); });
  }
  /* mapa de calor: linhas em cascata e barras crescendo do zero, a cada vez que a aba abre */
  function animaCalor() {
    var cal = $('#st-calor'); if (!cal || !cal.dataset.pronto) return;
    var linhas = $$('.ca-linha[data-i]', cal);
    cascata(cal, '.ca-linha');
    if (window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches) return;
    linhas.forEach(function (li, i) { var b = $('.ca-barra i', li); if (!b) return; var w = b.style.width; b.style.transition = 'none'; b.style.width = '0'; void b.offsetWidth; b.style.transition = ''; b.style.transitionDelay = (Math.min(i, 24) * .035 + .15).toFixed(3) + 's'; b.style.width = w; });
    clearTimeout(animaCalor.t); animaCalor.t = setTimeout(function () { linhas.forEach(function (li) { var b = $('.ca-barra i', li); if (b) b.style.transitionDelay = ''; }); }, 1800);
  }
  var primeiraAba = true;
  function mostraAba(id) {
    if (!$('#v-' + id)) return;
    $$('.pn-abas button').forEach(function (b) { b.setAttribute('aria-selected', b.dataset.aba === id); });
    $$('.pn-vista').forEach(function (v) { v.classList.toggle('ativa', v.id === 'v-' + id); });
    $('.pn').classList.toggle('sem-lado', id === 'mapa' || id === 'setores' || id === 'brasil');   // 27/10: os filtros não valem para o mapa nem para os setores, então a coluna some
    $('.pn-main').scrollTop = 0;
    fechaDetalhe();
    if (id === 'mapa') montaMapa();
    if (id === 'brasil') montaBrasil();
    if (id === 'setores') montaSetores();
    if (id === 'tempo') montaTempo();
    if (id === 'mudancas') montaMudancas();
    if (id === 'revisao') montaRevisao();
    history.replaceState(null, '', '#' + id);
    deslizaTudo();
    /* 27/10: a batida na troca de seção entrou e saiu no mesmo dia («não precisa bater asa quando muda de seção»); só na entrada */
    var vista = $('#v-' + id); if (vista) { vista.classList.remove('entra'); void vista.offsetWidth; vista.classList.add('entra'); }
    if (id === 'setores') animaCalor();
    if (id === 'normas') cascata($('#pn-lista'), '.pn-item');
    if (id === 'mapa' && $('#mp-lado').dataset.pronto) cascata($('#mp-lado .mp-rank'), 'li');
  }

  /* ---------- lista ---------- */
  /* 27/10/2026 (Leandro: «parece que o filtro não está funcionando»): busca e filtros valem para todas as abas de normas, não só
     para Normas por tema. passa() é a regra única; semFase ignora o filtro de estágio (linha do tempo e o que mudou mostram
     a norma em qualquer estágio). */
  function passa(n, semFase) {
    if (!F.temas[n.tema] || (!semFase && !F.fases[n.fase]) || !F.tipos[n.tipo]) return false;
    if (F.pagina && !n.pagina) return false;
    var q = F.q; if (!q) return true;
    var qn = q.replace(/^iso[\/\s-]*(iec)?[\s-]*/, '').replace(/[^0-9a-z:\-]/g, '');
    var hay = (n.ref + ' ' + n.titulo + ' ' + n.comite + ' ' + (n.tcnome || '')).toLowerCase();
    return hay.indexOf(q) >= 0 || (qn && (n.num.indexOf(qn) === 0 || n.ref.toLowerCase().replace(/[^0-9a-z:\-]/g, '').indexOf(qn) >= 0));
  }
  function semFiltro() {
    if (F.q || F.pagina) return false;
    for (var k in F.temas) if (!F.temas[k]) return false;
    for (var t in F.tipos) if (!F.tipos[t]) return false;
    return true;
  }
  function filtra() { return D.normas.filter(function (n) { return passa(n); }); }
  function vistaAtiva() { var v = $('.pn-vista.ativa'); return v ? v.id.replace(/^v-/, '') : ''; }
  function ordena(xs) {
    var k = F.ord;
    return xs.sort(function (a, b) {
      if (k === 'fase') return (FASE_IDX[a.fase] - FASE_IDX[b.fase]) || a.num.localeCompare(b.num, undefined, { numeric: true });
      if (k === 'data') return String(b.pub || '9999').localeCompare(String(a.pub || '9999')) || a.ref.localeCompare(b.ref);
      return a.num.localeCompare(b.num, undefined, { numeric: true }) || a.ref.localeCompare(b.ref);
    });
  }
  function barraEst(n) {
    var i = FASE_IDX[n.fase];
    return '<span class="est" aria-hidden="true">' + FASES.map(function (f, j) {
      var c = j < i ? ' on' : ''; if (j === i) c = n.fase === 'publicada' ? ' pub' : n.fase === 'revisao' ? ' rev' : ' on';
      return '<i class="' + c.trim() + '"></i>';
    }).join('') + '</span>';
  }
  /* 17/10: lista em lotes de 60, o próximo entra quando o fim chega perto (sem montar 800 linhas de uma vez) */
  var LOTE = 60, atual = [], mostrados = 0, obs = null;
  function linha(n) {
    var f = FASES[FASE_IDX[n.fase]];
    return '<li class="pn-item" data-id="' + n.id + '" tabindex="0"><span class="ref">' + esc(n.ref) + '</span>' +
      '<span class="tit">' + esc(n.titulo) + '<small>' + esc(n.comite) + (n.tcnome ? ' · ' + esc(n.tcnome) : '') + ' · ' + esc(D.temasMap[n.tema]) + '</small></span>' +
      '<span class="fase">' + barraEst(n) + '<span>' + f[1] + ' · ' + n.est + '</span></span>' +
      '<span class="seta"><svg viewBox="0 0 24 24"><path d="M5 12h14M13 6l6 6-6 6"/></svg></span></li>';
  }
  function maisLinhas() {
    var lista = $('#pn-lista'), velho = $('#pn-mais', lista);
    if (velho) velho.remove();
    if (mostrados >= atual.length) return;
    lista.insertAdjacentHTML('beforeend', atual.slice(mostrados, mostrados + LOTE).map(linha).join(''));
    mostrados += LOTE;
    if (mostrados < atual.length) {
      lista.insertAdjacentHTML('beforeend', '<li class="pn-mais" id="pn-mais" aria-hidden="true"></li>');
      if (!obs) obs = new IntersectionObserver(function (es) { if (es[0].isIntersecting) maisLinhas(); }, { root: $('.pn-main'), rootMargin: '600px 0px' });
      obs.disconnect(); obs.observe($('#pn-mais'));
    }
  }
  function render() {
    var v = vistaAtiva();
    if (v === 'tempo') montaTempo(); else if (v === 'mudancas') montaMudancas(); else if (v === 'revisao') montaRevisao();
    atual = ordena(filtra()); mostrados = 0;
    $('#pn-total').innerHTML = '<b>' + fmt(atual.length) + '</b> ' + T('de', 'of') + ' ' + fmt(D.normas.length) + T(' normas', ' standards');
    var lista = $('#pn-lista');
    if ($('#v-normas').classList.contains('ativa')) $('.pn-main').scrollTop = 0;
    if (!atual.length) { lista.innerHTML = '<li class="pn-vazio">' + T('Nenhuma norma com esses filtros. A busca aceita número (9001, 14064-1), palavra do título em inglês ou comitê (TC 207).', 'No standard matches these filters. Search accepts a number (9001, 14064-1), a word from the title or a committee (TC 207).') + '</li>'; return; }
    lista.innerHTML = ''; maisLinhas(); cascata(lista, '.pn-item');
  }
  var adia = null;
  function renderLogo() { clearTimeout(adia); adia = setTimeout(function () { requestAnimationFrame(render); }, 140); }

  /* ---------- detalhe ---------- */
  function abreDetalhe(id) {
    var n = null; for (var i = 0; i < D.normas.length; i++) if (D.normas[i].id === id) { n = D.normas[i]; break; }
    if (!n) return;
    var f = FASES[FASE_IDX[n.fase]], det = $('#pn-det');
    var irmas = (D.porNum[n.num] || []).filter(function (x) { return x.id !== n.id; });
    var trilha = '<div class="pn-trilha">' + FASES.map(function (g, j) {
      var c = j < FASE_IDX[n.fase] ? 'feito' : j === FASE_IDX[n.fase] ? 'on' : '';
      return '<div class="' + c + '">' + g[2] + '<br>' + g[1] + '</div>';
    }).join('') + '</div>';
    var mud = (MUD.itens || []).filter(function (m) { return m.id === n.id; });
    var sv = D.survey[n.num];
    det.innerHTML = '<button class="fechar" aria-label="' + T('Fechar', 'Close') + '"><svg viewBox="0 0 24 24" fill="none"><path d="M5 5l14 14M19 5L5 19"/></svg></button>' +
      '<span class="m">' + esc(TIPOS[n.tipo] || n.tipo) + (n.ed ? T(' · edição ', ' · edition ') + n.ed : '') + '</span>' +
      '<div class="ref">' + esc(n.ref) + '</div><h2>' + esc(n.titulo) + '</h2>' +
      '<p class="tema">' + esc(D.temasMap[n.tema]) + ' · ' + esc(n.comite) + (n.tcnome ? ', ' + esc(n.tcnome) : '') + '</p>' +
      '<div class="pn-sec"><span class="m">' + T('Estágio atual · código ', 'Current stage · code ') + n.est + '</span><p><b>' + f[1] + '.</b> ' + f[3] + '</p>' + trilha + '</div>' +
      (n.escopo ? '<div class="pn-sec"><span class="m">' + T('Do que trata (escopo, texto da ISO)', 'Scope (text from ISO)') + '</span><p>' + esc(n.escopo).replace(/\s*\n+\s*/g, '</p><p>') + (n.escopo.length >= 900 ? ' […]' : '') + '</p></div>' : '') +
      '<div class="pn-sec"><span class="m">' + T('Ficha', 'Record') + '</span><dl class="pn-kv">' +
      (n.pub ? '<dt>' + T('Publicação', 'Publication') + '</dt><dd>' + dataBR(n.pub) + '</dd>' : '') +
      (n.pag ? '<dt>' + T('Páginas', 'Pages') + '</dt><dd>' + n.pag + '</dd>' : '') +
      '<dt>' + T('Comitê ISO', 'ISO committee') + '</dt><dd>' + esc(n.comite) + (n.tcnome ? ' · ' + esc(n.tcnome) : '') + '</dd>' +
      (n.abnt ? '<dt>' + T('Espelho ABNT', 'ABNT adoption') + '</dt><dd>' + esc(n.abnt) + '</dd>' : '') +
      (n.ics ? '<dt>ICS</dt><dd>' + n.ics.join(' · ') + '</dd>' : '') +
      (irmas.length ? '<dt>' + T('Outras edições e projetos', 'Other editions and projects') + '</dt><dd>' + irmas.map(function (x) { return '<a href="#n' + x.id + '" data-id="' + x.id + '">' + esc(x.ref) + '</a> <span class="m" style="font-size:10px">' + FASES[FASE_IDX[x.fase]][1] + '</span>'; }).join('<br>') + '</dd>' : '') +
      (sv ? '<dt>' + T('Certificados', 'Certificates') + '</dt><dd>' + fmt(sv.total) + T(' no mundo', ' worldwide') + (sv.paises.BR ? ', ' + fmt(sv.paises.BR) + T(' no Brasil', ' in Brazil') : '') + ' <span class="m" style="font-size:10px">ISO Survey 2025</span> · <a href="#mapa" data-mapa="' + n.num + '">' + T('ver no mapa', 'see on map') + '</a></dd>' : '') +
      '</dl></div>' +
      (mud.length ? '<div class="pn-sec"><span class="m">' + T('Movimentos registrados neste painel', 'Movements recorded in this dashboard') + '</span><p>' + mud.map(function (m) { return dataBR(m.data) + ': ' + (m.tipo === 'nova' ? T('entrou na base', 'entered the database') : m.tipo === 'saiu' ? T('saiu da base', 'left the database') : T('estágio ', 'stage ') + m.de + T(' para ', ' to ') + m.para); }).join('<br>') + '</p></div>' : '') +
      '<div class="pn-sec"><span class="m">Links</span><div class="pn-links">' +
      '<a href="https://www.iso.org/standard/' + n.id + '.html" target="_blank" rel="noopener">' + T('Página da norma na ISO', 'Standard page at ISO') + ' <span class="m">iso.org</span></a>' +
      (n.tcid ? '<a href="https://www.iso.org/committee/' + n.tcid + '.html" target="_blank" rel="noopener">' + T('Comitê ', 'Committee ') + esc(n.comite) + ' <span class="m">iso.org</span></a>' : '') +
      (n.pagina ? '<a href="' + n.pagina + '">' + T('Serviço da Ideal Metrics nesta norma', 'Ideal Metrics service for this standard') + ' <span class="m">' + T('neste site', 'on this site') + '</span></a>' : '') +
      '<a href="contato.html">' + T('Contato com a equipe técnica', 'Contact the technical team') + ' <span class="m">Ideal Metrics</span></a>' +
      '</div></div>';
    det.querySelector('.fechar').addEventListener('click', fechaDetalhe);
    var am = det.querySelector('[data-mapa]'); if (am) am.addEventListener('click', function (e) { e.preventDefault(); fechaDetalhe(); mostraAba('mapa'); escolheSurvey(am.dataset.mapa); });
    det.classList.add('aberta'); $('#pn-veu').classList.add('on'); det.scrollTop = 0;
    $$('.pn-item').forEach(function (li) { li.classList.toggle('sel', +li.dataset.id === id); });
    history.replaceState(null, '', '#n' + id);
  }
  function fechaDetalhe() {
    $('#pn-det').classList.remove('aberta'); $('#pn-veu').classList.remove('on');
    $$('.pn-item.sel').forEach(function (li) { li.classList.remove('sel'); });
    if (/^#n\d+/.test(location.hash)) history.replaceState(null, '', location.pathname + location.search);   // mantém o ?lang=en
  }

  /* ---------- linha do tempo ---------- */
  function montaTempo() {
    var A0 = 1985, A1 = 2028, span = A1 - A0;
    var px = function (d) { var y = +String(d).slice(0, 4), m = +(String(d).slice(5, 7) || 6); return ((y + (m - 1) / 12 - A0) / span * 100); };
    var anos = ''; for (var a = 1990; a <= 2025; a += 5) anos += '<span style="left:' + px(a) + '%">' + a + '</span>';
    $('#lt-anos').innerHTML = anos;
    var hist = {}; (D.historico || []).forEach(function (h) { (hist[h.num] = hist[h.num] || []).push(h); });
    var chaves = CHAVE.filter(function (k) { return D.porNum[k] && D.porNum[k].some(function (x) { return passa(x, true); }); });
    if (!chaves.length) { $('#lt-corpo').innerHTML = '<p class="pn-vazio">' + T('Nenhuma norma-chave com esses filtros.', 'No key standard matches these filters.') + '</p>'; return; }
    $('#lt-corpo').innerHTML = chaves.map(function (k) {
      var xs = D.porNum[k].slice().sort(function (a, b) { return String(a.pub || '9999').localeCompare(String(b.pub || '9999')); });
      var atual = xs.filter(function (x) { return x.fase === 'publicada' || x.fase === 'revisao'; }).pop();
      var nome = (atual || xs[0]).titulo.split(/ [—–-] /)[0];
      var antigas = (hist[k] || []).map(function (h) {
        return '<span class="lt-ed ant" style="left:' + px(h.pub) + '%" title="' + esc(h.ref) + T(' · edição retirada', ' · withdrawn edition') + '"><span class="r">' + h.pub.slice(0, 4) + '</span></span>';
      }).join('');
      var marcas = antigas + xs.map(function (x) {
        if (x.pub) return '<span class="lt-ed' + (x === atual ? '' : ' ant') + '" style="left:' + px(x.pub) + '%" data-id="' + x.id + '" title="' + esc(x.ref) + '"><span class="r">' + x.pub.slice(0, 4) + '</span></span>';
        return '<span class="lt-ed dev" style="left:' + px(D.gerado) + '%" data-id="' + x.id + '" title="' + esc(x.ref) + T(' · em desenvolvimento', ' · under development') + '"><span class="r">' + esc(x.ref.replace(/^ISO(\/IEC)?\s*/, '')) + '</span></span>';
      }).join('');
      /* 27/10 («uma linha do tempo mais bonita»): trilho fino ligando a primeira edição ao hoje, segmento cheio entre a primeira e a
         edição em vigor, marcas redondas (anteriores vazadas, em vigor cheia, projeto tracejado) e os anos só no hover */
      var pubs = (hist[k] || []).map(function (h) { return h.pub; }).concat(xs.filter(function (x) { return x.pub; }).map(function (x) { return x.pub; })).sort();
      var ini = pubs.length ? px(pubs[0]) : px(D.gerado), fim = atual && atual.pub ? px(atual.pub) : ini;
      var trilho = '<i class="lt-trilho" style="left:' + ini + '%;right:' + (100 - px(D.gerado)) + '%"></i><i class="lt-vivo" style="left:' + ini + '%;width:' + Math.max(0, fim - ini) + '%"></i>';
      return '<div class="lt-linha"><div class="lt-nome"><b>ISO ' + k + '</b>' + esc(nome) + '</div><div class="lt-faixa" style="--lt-passo:' + (500 / span) + '%">' + trilho + marcas + '</div></div>';
    }).join('');
    /* 27/10: «aqui também tem que ter animação»: na entrada cada trilho se desenha da esquerda para a direita (uma linha atrás
       da outra, 50 ms) e cada marca acende quando o traço chega nela */
    var corpo = $('#lt-corpo');
    $$('.lt-linha', corpo).forEach(function (li, i) {
      var tr = $('.lt-trilho', li), L = tr ? parseFloat(tr.style.left) || 0 : 0, R = tr ? 100 - (parseFloat(tr.style.right) || 0) : 100, d0 = Math.min(i, 24) * .035 + .1;
      $$('.lt-trilho,.lt-vivo', li).forEach(function (t) { t.style.animationDelay = d0.toFixed(2) + 's'; });
      $$('.lt-ed', li).forEach(function (e) { var x = parseFloat(e.style.left) || 0, k = R > L ? Math.max(0, Math.min(1, (x - L) / (R - L))) : 0; e.style.animationDelay = (d0 + k * .9).toFixed(2) + 's'; });
    });
    corpo.classList.remove('lt-anima'); void corpo.offsetWidth; corpo.classList.add('lt-anima');
    cascata(corpo, '.lt-linha');
  }

  /* ---------- mudanças ---------- */
  function montaMudancas() {
    var el = $('#md-corpo'), it = (MUD.itens || []).slice().sort(function (a, b) { return b.data.localeCompare(a.data) || a.ref.localeCompare(b.ref); });
    var desde = dataBR((MUD.desde || D.gerado)), todos = semFiltro();
    var achaN = function (id) { for (var i = 0; i < D.normas.length; i++) if (D.normas[i].id === id) return D.normas[i]; return null; };
    var total = it.length;
    // norma que saiu da base não tem mais ficha: só aparece quando nenhum filtro está ligado
    it = it.filter(function (m) { var n = achaN(m.id); return n ? passa(n, true) : todos; });
    if (total && !it.length) { el.innerHTML = '<p class="pn-vazio">' + T('Nenhum movimento com esses filtros.', 'No movement matches these filters.') + '</p>'; return; }
    if (!it.length) {
      el.innerHTML = '<p class="pn-vazio">' + T('Nenhuma mudança de estágio registrada desde ' + desde + '. A base da ISO é comparada toda semana; o que entrar, avançar de estágio ou for publicado aparece aqui.', 'No stage change recorded since ' + desde + '. The ISO database is compared every week; whatever enters, moves to another stage or is published appears here.') + '</p>';
      return;
    }
    var grupos = {}; it.forEach(function (m) { (grupos[m.data] = grupos[m.data] || []).push(m); });
    el.innerHTML = Object.keys(grupos).sort().reverse().map(function (d) {
      return '<div class="md-grupo"><span class="m">' + dataBR(d) + ' · ' + grupos[d].length + T(' movimento(s)', ' movement(s)') + '</span>' + grupos[d].map(function (m) {
        var o = m.tipo === 'nova' ? T('entrou na base · ', 'entered the database · ') + m.para : m.tipo === 'saiu' ? T('saiu da base', 'left the database') : m.de + ' → ' + m.para;
        var n = D.normas.filter(function (x) { return x.id === m.id; })[0];
        return '<div class="md-item" data-id="' + m.id + '"><span class="ref">' + esc(m.ref) + '</span><span>' + esc(n ? n.titulo : '') + '</span><span class="de">' + esc(o) + ' · ' + (FASES[FASE_IDX[m.fase]] || [])[1] + '</span></div>';
      }).join('') + '</div>';
    }).join('');
    cascata(el, '.md-grupo > *');
  }

  /* ---------- revisão sistemática ---------- */
  function montaRevisao() {
    var todas = D.normas.filter(function (n) { return n.fase === 'revisao'; });
    var xs = todas.filter(function (n) { return passa(n); }).sort(function (a, b) { return a.num.localeCompare(b.num, undefined, { numeric: true }); });
    $('#rv-total').innerHTML = '<b>' + xs.length + '</b>' + (xs.length < todas.length ? T(' de ', ' of ') + todas.length : '') + T(' normas em revisão sistemática', ' standards under systematic review');
    if (!xs.length) { $('#rv-corpo').innerHTML = '<li class="pn-vazio">' + T('Nenhuma norma em revisão sistemática com esses filtros.', 'No standard under systematic review matches these filters.') + '</li>'; return; }
    $('#rv-corpo').innerHTML = xs.map(function (n) {
      var proj = (D.porNum[n.num] || []).filter(function (x) { return x.id !== n.id && !x.pub; });
      return '<li class="pn-item" data-id="' + n.id + '"><span class="ref">' + esc(n.ref) + '</span><span class="tit">' + esc(n.titulo) + '<small>' + esc(D.temasMap[n.tema]) + ' · ' + esc(n.comite) + (proj.length ? T(' · projeto de nova edição em curso: ', ' · new edition project under way: ') + esc(proj[0].ref) : '') + '</small></span>' +
        '<span class="fase">' + barraEst(n) + '<span>' + T('código ', 'code ') + n.est + '</span></span><span class="seta"><svg viewBox="0 0 24 24"><path d="M5 12h14M13 6l6 6-6 6"/></svg></span></li>';
    }).join('');
    cascata($('#rv-corpo'), '.pn-item');
  }

  /* ---------- certificados por setor (27/10/2026) ---------- */
  /* 39 setores EA (índice 0 a 38) agrupados nos setores que a Ideal Metrics atende; a ilustração é a da brochura (coleção C) */
  var GRUPOS = [
    { id: 'industria', nome: 'Indústria', ea: [1, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23] },
    { id: 'facilities', nome: 'Construção e facilities', ea: [27] },
    { id: 'comercio', nome: 'Comércio e serviços', ea: [28, 29, 31, 34] },
    { id: 'tecnologia', nome: 'Tecnologia e engenharia', ea: [32, 33] },
    { id: 'transporte', nome: 'Transporte e logística', ea: [30] },
    { id: 'saude', nome: 'Saúde', ea: [37] },
    { id: 'energia', nome: 'Energia e saneamento', ea: [24, 25, 26] },
    { id: 'alimentos', nome: 'Alimentos e bebidas', ea: [2] },
    { id: 'publico', nome: 'Setor público e educação', ea: [35, 36, 38] },
    { id: 'agro', nome: 'Agro', ea: [0] }
  ];
  var EA_PT = ['Agricultura, pesca e florestas', 'Mineração', 'Alimentos, bebidas e tabaco', 'Têxteis', 'Couro', 'Madeira', 'Celulose e papel', 'Editoras', 'Gráficas', 'Coque e refino de petróleo', 'Combustível nuclear', 'Químicos e fibras', 'Farmacêuticos', 'Borracha e plástico', 'Minerais não metálicos', 'Concreto, cimento, cal e gesso', 'Metalurgia e produtos de metal', 'Máquinas e equipamentos', 'Equipamentos elétricos e ópticos', 'Construção naval', 'Aeroespacial', 'Outros equipamentos de transporte', 'Outras indústrias', 'Reciclagem', 'Energia elétrica', 'Gás', 'Água', 'Construção', 'Comércio e reparação de veículos', 'Hotéis e restaurantes', 'Transporte, armazenagem e comunicação', 'Finanças, imóveis e aluguel', 'Tecnologia da informação', 'Serviços de engenharia', 'Outros serviços', 'Administração pública', 'Educação', 'Saúde e assistência social', 'Outros serviços sociais'];
  if (EN) { var GRUPOS_EN = { industria: 'Industry', facilities: 'Construction and facilities', comercio: 'Trade and services', tecnologia: 'Technology and engineering', transporte: 'Transport and logistics', saude: 'Health', energia: 'Energy and utilities', alimentos: 'Food and beverages', publico: 'Public sector and education', agro: 'Agribusiness' }; GRUPOS.forEach(function (g) { g.nome = GRUPOS_EN[g.id] || g.nome; }); }
  var eaNome = function (i) { var S = D.setores.setores; return EN ? S[i] : (EA_PT[i] || S[i]); };   // em inglês, o nome original do ISO Survey
  var stFeito = false, stNum = '9001', stOnde = 'mundo';
  function montaSetores() {
    if (stFeito) return; stFeito = true;
    var S = D.setores; if (!S || !S.normas) { $('#st-grade').innerHTML = '<p class="pn-vazio">' + T('Sem dados de setor nesta base.', 'No sector data in this database.') + '</p>'; return; }
    var nums = Object.keys(S.normas).sort(function (a, b) { return D.survey[b].total - D.survey[a].total; });
    $('#st-sel').innerHTML = nums.map(function (k) { var nm = SURVEY_NOME[k] || 'ISO ' + k; return '<button data-num="' + k + '" aria-pressed="' + (k === stNum) + '"' + (nm.length > 13 ? ' class="longo"' : '') + '>' + nm + '</button>'; }).join('');
    $$('#st-sel button').forEach(function (b) { b.addEventListener('click', function () { stNum = b.dataset.num; $$('#st-sel button').forEach(function (x) { x.setAttribute('aria-pressed', x === b); }); desliza($('#st-sel'), '[aria-pressed=true]'); pintaSetores(); }); });
    $$('.st-onde button').forEach(function (b) { b.addEventListener('click', function () { stOnde = b.dataset.onde; $$('.st-onde button').forEach(function (x) { x.setAttribute('aria-pressed', x === b); }); pintaSetores(); }); });
    desliza($('#st-sel'), '[aria-pressed=true]');
    pintaSetores();
  }
  function pintaSetores() {
    var S = D.setores, n = S.normas[stNum]; if (!n) return;
    var v = n[stOnde], total = v.reduce(function (a, b) { return a + b; }, 0);
    var grupos = GRUPOS.map(function (g) { return { g: g, soma: g.ea.reduce(function (a, i) { return a + v[i]; }, 0) }; }).sort(function (a, b) { return b.soma - a.soma; });
    var max = grupos[0].soma || 1;
    $('#st-total').textContent = fmt(total) + T(' certificados com setor informado · ', ' certificates with sector reported · ') + (SURVEY_NOME[stNum] || 'ISO ' + stNum) + ' · ' + (stOnde === 'br' ? T('Brasil', 'Brazil') : T('mundo', 'world'));
    /* 27/10: «pode tirar os cards, não está legal, deixe só o diagrama»: os cartões ficam no código, desligados (st-grade sumiu do HTML) */
    if ($('#st-grade')) $('#st-grade').innerHTML = grupos.map(function (x) {
      var g = x.g, pct = total ? (x.soma / total * 100) : 0;
      var ea = g.ea.map(function (i) { return { i: i, v: v[i] }; }).sort(function (a, b) { return b.v - a.v; });
      return '<article class="st-card entra">' + (g.sem ? '<div class="st-sem"></div>' : '<img class="st-ilus" src="img/setores/setor-' + g.id + '.webp?v=2" alt="" loading="lazy">') +
        '<h3>' + g.nome + '</h3><div class="st-n"><b>' + fmt(x.soma) + '</b><span class="m">' + (EN ? pct.toFixed(1) : pct.toFixed(1).replace('.', ',')) + '% · ' + ea.length + (ea.length > 1 ? T(' setores EA', ' EA sectors') : T(' setor EA', ' EA sector')) + '</span></div>' +
        '<div class="st-barra"><i style="width:' + (x.soma / max * 100) + '%"></i></div>' +
        '<ul class="st-ea">' + ea.slice(0, 6).map(function (e) { return '<li' + (e.v ? '' : ' class="zero"') + '><span title="' + esc(S.setores[e.i]) + '">' + esc(eaNome(e.i)) + '</span><b>' + fmt(e.v) + '</b></li>'; }).join('') +
        (ea.length > 6 ? '<li><span class="m">+ ' + (ea.length - 6) + T(' setores EA', ' EA sectors') + '</span><b>' + fmt(ea.slice(6).reduce(function (a, e) { return a + e.v; }, 0)) + '</b></li>' : '') + '</ul></article>';
    }).join('');
    if ($('#st-grade')) entra($('#st-grade'));
    pintaCalor();
  }
  /* 27/10: «a base traz mais divisões por setores… fazer um gráfico, um dashboard melhor», com o calendário de quadrados que
     o Leandro mandou como linguagem: mapa de calor dos 39 setores EA × 17 normas (quadrado por célula, 5 níveis em escala
     log) e, na mesma linha, a barra do setor na norma escolhida. Linhas na ordem da norma escolhida. */
  function pintaCalor() {
    /* 27/10: «não quero que o painel pisque quando mudar de norma»: o DOM do mapa é montado UMA vez (ao abrir a aba); a troca
       de norma ou de Mundo/Brasil só atualiza no lugar: nível e valor de cada quadrado, coluna marcada, barras (que deslizam
       da largura atual para a nova) e números. Nada é recriado, então nada pisca. */
    var S = D.setores, nums = Object.keys(S.normas).sort(function (a, b) { return D.survey[b].total - D.survey[a].total; });
    var atual = S.normas[stNum][stOnde], max = Math.max.apply(null, atual) || 1;
    var soma = S.setores.map(function (_, i) { return nums.reduce(function (t, k) { return t + S.normas[k].mundo[i]; }, 0); });
    var ordem = atual.map(function (v, i) { return i; }).sort(function (a, b) { return soma[b] - soma[a]; });   // ordem fixa
    var nivel = function (v) { return !v ? 0 : v < 10 ? 1 : v < 100 ? 2 : v < 1000 ? 3 : 4; };
    var onde = stOnde === 'br' ? T('Brasil', 'Brazil') : T('mundo', 'world'), nome = SURVEY_NOME[stNum] || 'ISO ' + stNum;
    var cal = $('#st-calor'), calmo = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;
    if (!cal.dataset.pronto) {
      cal.dataset.pronto = '1';
      var cab = '<div class="ca-linha ca-cabeca"><span></span><div class="ca-cels">' + nums.map(function (k) { return '<button type="button" data-num="' + k + '"><i>' + (SURVEY_NOME[k] || 'ISO ' + k).replace('ISO/IEC ', '') + '</i></button>'; }).join('') + '</div><span class="m" id="ca-norma"></span></div>';
      var corpo = ordem.map(function (i) {
        return '<div class="ca-linha" data-i="' + i + '"><span class="ca-nome" title="' + esc(S.setores[i]) + '">' + esc(eaNome(i)) + '</span><div class="ca-cels">' +
          nums.map(function (k) { return '<span class="ca-q" tabindex="0" data-k="' + k + '" data-s="' + esc(eaNome(i)) + '"></span>'; }).join('') +
          '</div><span class="ca-barra"><i style="width:0"></i></span><b></b></div>';
      }).join('');
      cal.innerHTML = '<div class="ca-cab"><b>' + T('Setores EA por norma', 'EA sectors by standard') + '</b><span id="ca-sub"></span></div>' + cab + corpo +
        '<div class="ca-pe"><span>' + T('Quadrado = certificados do setor na norma; barra = norma escolhida.', 'Square = certificates of the sector in the standard; bar = selected standard.') + '</span><span class="ca-leg"><em>0</em><span class="ca-q" data-n="0"></span><span class="ca-q" data-n="1"></span><span class="ca-q" data-n="2"></span><span class="ca-q" data-n="3"></span><span class="ca-q" data-n="4"></span><em>' + T('10 mil+', '10k+') + '</em></span></div><div class="ca-dica"></div>';
      var dica = $('.ca-dica', cal);
      function mostra(q) {
        var rc = q.getBoundingClientRect(), rb = cal.getBoundingClientRect();
        dica.innerHTML = '<b>' + fmt(+q.dataset.v) + '</b> · ' + q.dataset.s + ' · ' + (SURVEY_NOME[q.dataset.k] || 'ISO ' + q.dataset.k);
        var meia = dica.offsetWidth / 2, x = rc.left - rb.left + rc.width / 2; x = Math.max(meia, Math.min(rb.width - meia, x));
        dica.style.left = x + 'px'; dica.style.top = (rc.top - rb.top) + 'px'; dica.classList.add('on');
      }
      $$('.ca-linha .ca-q', cal).forEach(function (q) {
        q.addEventListener('mouseenter', function () { mostra(q); }); q.addEventListener('focus', function () { mostra(q); });
        q.addEventListener('mouseleave', function () { dica.classList.remove('on'); }); q.addEventListener('blur', function () { dica.classList.remove('on'); });
      });
      $$('.ca-cabeca button', cal).forEach(function (b) { b.addEventListener('click', function () { var t = $('#st-sel button[data-num="' + b.dataset.num + '"]'); if (t) t.click(); }); });
      cal.classList.remove('ca-on'); void cal.offsetWidth;
      if (calmo) cal.classList.add('ca-on'); else requestAnimationFrame(function () { cal.classList.add('ca-on'); });
    }
    $('#ca-sub', cal).textContent = S.setores.length + T(' setores EA · ', ' EA sectors · ') + nums.length + T(' normas · ', ' standards · ') + onde;
    $('#ca-norma', cal).textContent = ((D.survey[stNum] && D.survey[stNum].titulo) || nome) + ' · ' + onde;   // 27/10: «que aparecesse o nome da norma aqui também»: título completo da norma, como no ISO Survey
    $$('.ca-cabeca button', cal).forEach(function (b) { b.setAttribute('aria-pressed', b.dataset.num === stNum); });
    $$('.ca-linha[data-i]', cal).forEach(function (li) {
      var i = +li.dataset.i;
      $$('.ca-q', li).forEach(function (q) { var v = S.normas[q.dataset.k][stOnde][i]; q.dataset.n = nivel(v); q.dataset.v = v; q.classList.toggle('sel', q.dataset.k === stNum); });
      $('.ca-barra i', li).style.width = (atual[i] / max * 100) + '%';
      roleta($('b', li), atual[i]);   // 27/10: números do mapa de calor também em roleta
    });
  }

  /* ---------- certificados no Brasil (Inmetro, Certifiq) ----------
     31/10/2026, Leandro: «coloque a opção de abrir o mapa do Brasil de certificados por estado e por setor; coloque como uma
     opção no cabeçalho, ao lado de Certificados no mundo, e tente fazer do jeito que está». Dados do Certifiq, do Inmetro
     (dados/inmetro-certifiq.json, gerado por _ferramentas/inmetro_certifiq.py): só ISO 9001 e ISO 14001. Por estado, o
     Certifiq não publica os válidos; a aba mostra as empresas certificadas ou recertificadas nos três últimos anos (o ciclo
     de um certificado) e diz isso. Por setor, os certificados válidos por setor IAF. Mapa dos estados (IBGE, malha mínima)
     na mesma trama de pontos do mapa do mundo, com haste e etiqueta nos maiores estados. */
  var brFeito = false, brNum = '9001', brModo = 'uf', BRD = null, brDesenha = null;
  var UF_IBGE = { 11: 'RO', 12: 'AC', 13: 'AM', 14: 'RR', 15: 'PA', 16: 'AP', 17: 'TO', 21: 'MA', 22: 'PI', 23: 'CE', 24: 'RN', 25: 'PB', 26: 'PE', 27: 'AL', 28: 'SE', 29: 'BA', 31: 'MG', 32: 'ES', 33: 'RJ', 35: 'SP', 41: 'PR', 42: 'SC', 43: 'RS', 50: 'MS', 51: 'MT', 52: 'GO', 53: 'DF' };
  var UF_NOME = { AC: 'Acre', AL: 'Alagoas', AM: 'Amazonas', AP: 'Amapá', BA: 'Bahia', CE: 'Ceará', DF: 'Distrito Federal', ES: 'Espírito Santo', GO: 'Goiás', MA: 'Maranhão', MG: 'Minas Gerais', MS: 'Mato Grosso do Sul', MT: 'Mato Grosso', PA: 'Pará', PB: 'Paraíba', PE: 'Pernambuco', PI: 'Piauí', PR: 'Paraná', RJ: 'Rio de Janeiro', RN: 'Rio Grande do Norte', RO: 'Rondônia', RR: 'Roraima', RS: 'Rio Grande do Sul', SC: 'Santa Catarina', SE: 'Sergipe', SP: 'São Paulo', TO: 'Tocantins' };
  /* 31/10, 2º («faça a sua sugestão, com percentual»): a aba mostra só a DISTRIBUIÇÃO (participação de cada estado e setor
     no total do Certifiq), nunca o total absoluto, que competiria com o número oficial do ISO Survey da aba do mundo */
  var CERTIFIQ = 'https://certifiq.inmetro.gov.br/', BR_CORTES = [.001, .01, .02, .05, .10];
  function brNivel(f) { if (!f) return 0; for (var i = BR_CORTES.length - 1; i >= 0; i--) if (f >= BR_CORTES[i]) return i + 1; return 1; }
  function pct(f) { var v = f * 100; return (v >= 10 ? Math.round(v) : v >= 1 ? v.toFixed(1) : v.toFixed(2)).toString().replace('.', EN ? '.' : ',') + '%'; }
  function brPartes(o) { var t = 0, k; for (k in o) t += o[k]; var r = {}; for (k in o) r[k] = t ? o[k] / t : 0; return r; }
  function montaBrasil() {
    if (brFeito) { if (brDesenha) brDesenha(true); return; } brFeito = true;
    var box = $('#br-mapa'), dicaB = $('#br-dica');
    $('#br-sel').innerHTML = ['9001', '14001'].map(function (k, i) { return '<button style="--i:' + i + '" data-num="' + k + '" aria-pressed="' + (k === brNum) + '">ISO ' + k + '</button>'; }).join('');
    $$('#br-sel button').forEach(function (b) { b.addEventListener('click', function () { brNum = b.dataset.num; $$('#br-sel button').forEach(function (x) { x.setAttribute('aria-pressed', x === b); }); desliza($('#br-sel'), '[aria-pressed=true]'); if (brDesenha) brDesenha(true); }); });
    $$('.br-modo button').forEach(function (b) { b.setAttribute('role', 'radio'); b.setAttribute('aria-checked', b.getAttribute('aria-pressed')); b.addEventListener('click', function () { brModo = b.dataset.modo; $$('.br-modo button').forEach(function (x) { x.setAttribute('aria-pressed', x === b); x.setAttribute('aria-checked', x === b); }); if (brDesenha) brDesenha(true); }); });
    desliza($('#br-sel'), '[aria-pressed=true]');
    if (!window.d3 || !window.topojson) { box.innerHTML = '<p class="pn-vazio" style="padding:20px">' + T('O mapa precisa das bibliotecas d3 e topojson, que não carregaram.', 'The map needs the d3 and topojson libraries, which did not load.') + '</p>'; return; }
    Promise.all([fetch('dados/inmetro-certifiq.json?v=' + (document.querySelector('script[src*="painel-normas.js"]').src.split('v=')[1] || 1)).then(function (r) { return r.json(); }), fetch('dados/brasil-uf.json').then(function (r) { return r.json(); })]).then(function (res) {
      BRD = res[0]; var topo = res[1], FE = topojson.feature(topo, topo.objects.BRUF).features, FC = { type: 'FeatureCollection', features: FE };
      FE.forEach(function (f) { f.uf = UF_IBGE[+f.properties.codarea]; });
      var W = 960, H = 480, proj = d3.geoMercator(), cv = document.createElement('canvas'); cv.className = 'mp-pontos'; cv.setAttribute('aria-hidden', 'true'); box.insertBefore(cv, box.firstChild);
      var ctx = cv.getContext('2d'), svg = d3.select(box).insert('svg', '.mp-dica').attr('role', 'img').attr('aria-label', T('Mapa do Brasil por estado', 'Map of Brazil by state'));
      var paths = svg.append('g').selectAll('path').data(FE).enter().append('path').attr('class', 'pais');
      var gEtq = svg.append('g').attr('class', 'pulsos'), t0 = 0, crescendo = false, calmo = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;
      paths.on('mousemove', function (ev, f) {
        var v = brPartes(BRD.normas[brNum].uf || {})[f.uf] || 0, r = box.getBoundingClientRect();
        dicaB.style.display = 'block'; dicaB.style.left = (ev.clientX - r.left) + 'px'; dicaB.style.top = (ev.clientY - r.top) + 'px';
        dicaB.innerHTML = esc(UF_NOME[f.uf] || f.uf) + ' · <b>' + pct(v) + '</b>' + T(' das empresas certificadas', ' of certified companies');
      }).on('mouseleave', function () { dicaB.style.display = 'none'; });
      function quadro() {
        var r = box.getBoundingClientRect();
        W = (getComputedStyle(box).position === 'absolute' && r.height > 40) ? Math.max(480, Math.round(H * r.width / r.height)) : 960;
        svg.attr('viewBox', '0 0 ' + W + ' ' + H);
        proj.fitExtent([[24, 30], [W - 24, H - 14]], FC);
      }
      function pontos() {
        var r = svg.node().getBoundingClientRect(); if (!r.width) return;
        var dpr = Math.min(2, window.devicePixelRatio || 1), cw = Math.round(r.width * dpr), ch = Math.round(r.height * dpr), br = box.getBoundingClientRect();
        cv.width = cw; cv.height = ch; cv.style.width = r.width + 'px'; cv.style.height = r.height + 'px'; cv.style.left = (r.left - br.left) + 'px'; cv.style.top = (r.top - br.top) + 'px';
        var s = Math.min(r.width / W, r.height / H), ox = (r.width - W * s) / 2, oy = (r.height - H * s) / 2;
        /* raster dos estados: cada um pintado com a cor-número dele, num canvas fora da tela do mesmo tamanho */
        var oc = document.createElement('canvas'); oc.width = cw; oc.height = ch; var o = oc.getContext('2d');
        o.setTransform(dpr * s, 0, 0, dpr * s, dpr * ox, dpr * oy); var gp = d3.geoPath(proj, o);
        FE.forEach(function (f, i) { var k = i + 1; o.fillStyle = 'rgb(' + k + ',' + ((k * 37) % 256) + ',97)'; o.beginPath(); gp(f); o.fill(); });
        var px = o.getImageData(0, 0, cw, ch).data, P = Math.max(3, Math.round(2.5 * dpr)), D = Math.max(2, Math.round(P * .62)), m = Math.floor(D / 2);
        var C = coresTema(), dados = brPartes(BRD.normas[brNum].uf || {});
        ctx.clearRect(0, 0, cw, ch);
        var grupos = FE.map(function () { return []; });
        for (var y = Math.floor(P / 2); y < ch; y += P) for (var x = Math.floor(P / 2); x < cw; x += P) {
          var q = (y * cw + x) * 4, k = px[q];
          if (px[q + 3] === 255 && px[q + 2] === 97 && k >= 1 && k <= FE.length && px[q + 1] === (k * 37) % 256) grupos[k - 1].push(x, y);
        }
        grupos.forEach(function (g, i) { ctx.fillStyle = C[brNivel(dados[FE[i].uf] || 0)]; for (var j = 0; j < g.length; j += 2) ctx.fillRect(g[j] - m, g[j + 1] - m, D, D); });
      }
      function etiquetas(reinicia) {
        var dados = brPartes(BRD.normas[brNum].uf || {}), top = Object.keys(dados).sort(function (a, b) { return dados[b] - dados[a]; }).slice(0, 8);
        var cen = {}; FE.forEach(function (f) { cen[f.uf] = proj(d3.geoCentroid(f)); });
        var g = gEtq.selectAll('g.pulso').data(top.map(function (u) { return { uf: u, v: dados[u], p: cen[u] }; }), function (d) { return d.uf; });
        g.exit().remove();
        var e = g.enter().append('g').attr('class', 'pulso no-mapa');
        e.append('path').attr('class', 'vareta'); e.append('circle').attr('class', 'ponto').attr('r', 1.6);
        var et = e.append('g').attr('class', 'etq'); et.append('path').attr('class', 'fio'); et.append('rect').attr('class', 'pilula').attr('height', 18).attr('rx', 3); et.append('text').attr('class', 'en');
        if (reinicia) t0 = performance.now();
        poe();
      }
      function poe() {
        var agora = performance.now(), gr = calmo ? 1 : Math.max(0, Math.min(1, (agora - t0) / 1200)), cr = 1 - Math.pow(1 - gr, 3), postos = [];
        crescendo = gr < 1;
        var lista = []; gEtq.selectAll('g.pulso').each(function (d) { lista.push([this, d]); }); lista.sort(function (a, b) { return b[1].v - a[1].v; });
        lista.forEach(function (it) {
          var d = it[1], g = d3.select(it[0]), p = d.p; if (!p) return;
          var PILHA = 24, base = p[1] - 3, topo = base - PILHA, txt = d.uf + ' ' + pct(d.v), pw = 14 + txt.length * 6.3, ph = 18, lx = p[0], ly = topo - ph / 2 - 2, alvo = [0, 0];
          var livre = function (x, y) { return y - ph / 2 > 4 && postos.every(function (q) { return x + pw / 2 + 3 < q[0] || x - pw / 2 - 3 > q[1] || y + ph / 2 + 3 < q[2] || y - ph / 2 - 3 > q[3]; }); };
          if (!livre(lx, ly)) for (var k = 1, ok = false; k <= 10 && !ok; k++) [[pw + 6, -(k - 1) * (ph + 4)], [-(pw + 6), -(k - 1) * (ph + 4)], [0, -k * (ph + 4)]].some(function (c) { if (livre(lx + c[0], ly + c[1])) { alvo = c; ok = true; return true; } return false; });
          postos.push([lx + alvo[0] - pw / 2, lx + alvo[0] + pw / 2, ly + alvo[1] - ph / 2, ly + alvo[1] + ph / 2]);
          var sobe = calmo ? 0 : Math.pow(1 - Math.min(1, gr / .6), 3) * 18, x = lx + alvo[0], y = ly + alvo[1] + sobe;
          g.select('circle').attr('cx', p[0]).attr('cy', p[1]);
          g.select('path.vareta').attr('d', 'M' + p[0].toFixed(1) + ',' + base.toFixed(1) + 'V' + (base - PILHA * cr).toFixed(1));
          var et = g.select('g.etq').style('opacity', Math.min(1, gr / .25));
          et.select('rect').attr('x', (x - pw / 2).toFixed(1)).attr('y', (y - ph / 2).toFixed(1)).attr('width', pw.toFixed(1));
          et.select('text').attr('x', (x - pw / 2 + 7).toFixed(1)).attr('y', (y + 3.6).toFixed(1));
          et.select('text').text(d.uf + ' ' + pct(d.v * (calmo ? 1 : 1 - Math.pow(1 - gr, 3))));   // o percentual corre de zero junto com a haste
          et.select('path.fio').attr('d', Math.abs(alvo[0]) + Math.abs(alvo[1]) > 3 ? 'M' + p[0].toFixed(1) + ',' + topo.toFixed(1) + 'L' + x.toFixed(1) + ',' + (y + (alvo[1] < -3 ? ph / 2 : 0)).toFixed(1) : null);
        });
        if (crescendo) requestAnimationFrame(poe);
      }
      function setores() {
        var lista = (BRD.normas[brNum].setores || []).slice().sort(function (a, b) { return b.n - a.n; }), max = lista.length ? lista[0].n : 1, tot = lista.reduce(function (a, x) { return a + x.n; }, 0) || 1;
        $('#br-setores').innerHTML = '<ul class="br-set">' + lista.map(function (x) { return '<li><span title="' + esc(x.setor) + '">' + esc(x.setor) + '</span><span class="barra"><i style="width:' + (x.n / max * 100).toFixed(1) + '%"></i></span><b>' + pct(x.n / tot) + '</b></li>'; }).join('') + '</ul>';
        cascata($('#br-setores .br-set'), 'li');
      }
      function lado() {
        var N = BRD.normas[brNum], dados = brPartes(N.uf || {}), rank = Object.keys(dados).sort(function (a, b) { return dados[b] - dados[a]; }), max = dados[rank[0]] || 1, anos = BRD.anos_uf || [];
        var se = (N.setores || []).slice().sort(function (a, b) { return b.n - a.n; }), stot = se.reduce(function (a, x) { return a + x.n; }, 0) || 1;
        $('#br-lado').innerHTML = '<h3>ISO ' + brNum + '</h3><div class="m">' + esc(N.nome) + '</div>' +
          '<div class="tot"><span>' + pct(dados[rank[0]] || 0) + '</span><small>' + T('das empresas certificadas estão em ', 'of certified companies are in ') + esc(UF_NOME[rank[0]] || rank[0]) + '</small></div>' +
          (se[0] ? '<div class="mp-br"><span class="m">' + T('Setor com mais certificados', 'Sector with most certificates') + '</span><div class="v">' + pct(se[0].n / stot) + '<small>' + esc(se[0].setor) + '</small></div></div>' : '') +
          '<a class="mp-fonte-card" href="' + CERTIFIQ + '" target="_blank" rel="noopener">' + T('Dados do Inmetro (Certifiq)', 'Data from Inmetro (Certifiq)') + ' ↗</a>' +
          '<div class="mp-rola"><ul class="mp-rank">' + rank.map(function (u, i) { return '<li><span class="m">' + (i + 1) + '</span><span><span class="nome">' + esc(UF_NOME[u] || u) + '</span></span><b>' + pct(dados[u]) + '</b><span class="barra"><i style="width:' + (dados[u] / max * 100).toFixed(1) + '%"></i></span></li>'; }).join('') + '</ul>' +
          '<p class="mp-nota">' + T('Distribuição, em percentual, dos certificados registrados no Certifiq, a base pública do Inmetro com os certificados emitidos no Brasil por organismos acreditados pelo Inmetro (ISO 9001 e ISO 14001). Por estado: empresas certificadas ou recertificadas de ' + anos[0] + ' a ' + anos[anos.length - 1] + ' (o ciclo de um certificado), cada uma no estado do seu cadastro, mesmo com unidades em outros estados. Por setor: certificados válidos, pela seção da classificação NACE. Base atualizada em ' + dataBR(BRD.gerado) + '.', 'Percentage distribution of the certificates registered in Certifiq, the public Inmetro database of certificates issued in Brazil by Inmetro-accredited bodies (ISO 9001 and ISO 14001). By state: companies certified or recertified from ' + anos[0] + ' to ' + anos[anos.length - 1] + ' (a certificate cycle), each in the state of its registration, even with units in other states. By sector: valid certificates, by NACE section. Database updated on ' + dataBR(BRD.gerado) + '.') + '</p></div>';
        cascata($('#br-lado .mp-rank'), 'li');
      }
      function legenda() {
        var C = coresTema();
        $('#br-esc').innerHTML = '<span style="margin-left:0">' + T('participação', 'share') + '</span>' + ['0', pct(.001), pct(.01), pct(.02), pct(.05), pct(.10) + '+'].map(function (t, i) { return '<i style="background:' + C[i] + '"></i><span>' + t + '</span>'; }).join('') +
          '<a class="mp-fonte" href="' + CERTIFIQ + '" target="_blank" rel="noopener">' + T('Fonte: Inmetro, Certifiq · certificados emitidos no Brasil por organismos acreditados pelo Inmetro', 'Source: Inmetro, Certifiq · certificates issued in Brazil by Inmetro-accredited bodies') + ' <b aria-hidden="true">↗</b></a>';
      }
      brDesenha = function (reinicia) {
        var setor = brModo === 'setor';
        box.hidden = setor; $('#br-setores').hidden = !setor; $('#br-esc').style.display = setor ? 'none' : '';
        lado(); legenda();
        if (setor) setores();
        else { quadro(); paths.attr('d', d3.geoPath(proj)); pontos(); etiquetas(reinicia); }
      };
      if (window.ResizeObserver) new ResizeObserver(function () { if (brModo === 'uf' && !box.hidden) { quadro(); paths.attr('d', d3.geoPath(proj)); pontos(); etiquetas(false); } }).observe(box);
      document.addEventListener('pn-tema', function () { if (brDesenha) brDesenha(false); });
      brDesenha(true);
    }).catch(function () { box.innerHTML = '<p class="pn-vazio" style="padding:20px">' + T('Os dados do Inmetro não carregaram.', 'The Inmetro data did not load.') + '</p>'; });
  }

  /* ---------- mapa ---------- */
  var mapaFeito = false, mapaNum = '9001', paths = null, dica = null, refazPulsos = null, pintaPaises = null;
  function escolheSurvey(num) { mapaNum = num; $$('.mp-sel button').forEach(function (b) { b.setAttribute('aria-pressed', b.dataset.num === num); }); desliza($('#mp-sel'), '[aria-pressed=true]'); pintaMapa(); }
  function montaMapa() {
    if (mapaFeito) return; mapaFeito = true;
    var nums = Object.keys(D.survey).sort(function (a, b) { return D.survey[b].total - D.survey[a].total; });
    $('#mp-sel').innerHTML = nums.map(function (k, i) { var nm = SURVEY_NOME[k] || 'ISO ' + k; return '<button style="--i:' + i + '" data-num="' + k + '" aria-pressed="' + (k === mapaNum) + '"' + (nm.length > 13 ? ' class="longo"' : '') + '>' + nm + '</button>'; }).join('');
    $$('.mp-sel button').forEach(function (b) { b.addEventListener('click', function () { escolheSurvey(b.dataset.num); }); });
    var box = $('#mp-mapa'); dica = $('#mp-dica');
    if (!window.d3 || !window.topojson) { box.innerHTML = '<p class="pn-vazio" style="padding:20px">' + T('O mapa precisa das bibliotecas d3 e topojson, que não carregaram. A tabela ao lado continua válida.', 'The map needs the d3 and topojson libraries, which did not load. The table alongside remains valid.') + '</p>'; pintaLado(); return; }
    fetch('dados/mundo-110m.json').then(function (r) { return r.json(); }).then(function (topo) {
      MUNDO = topojson.feature(topo, topo.objects.countries);
      var porNumFeat = {}; Object.keys(D.paises).forEach(function (a2) { if (D.paises[a2].n) porNumFeat[D.paises[a2].n] = a2; });
      /* 27/10: globo que gira e se desenrola em mapa (projeção ortográfica interpolada com a Natural Earth) */
      /* 31/10/2026, «quero que o globo fique aberto, e passando conforme no HASDA»: o mapa aberto é o padrão e corre da
         esquerda para a direita em loop (molde do dashboard do HASDA 2027). Mapa plano equirretangular de 78N a 56S
         ocupando a altura; a largura (2π × escala) passa da tela e a emenda do loop fica escondida pela borda esmaecida.
         No computador o quadro acompanha o tamanho da área (W muda, H fica 480) e a coluna dos dados passa por cima, no vidro. */
      /* 31/10/2026, «usar o novo mapa global, que mostra a proporção exata dos países»: o mapa aberto passa à projeção Equal
         Earth (Šavrič, Patterson e Jenny, 2018), de área igual: cada país no tamanho real em relação aos outros (Rússia,
         Canadá e Groenlândia deixam de parecer gigantes; África e América do Sul aparecem no tamanho de verdade). A faixa
         de 78N a 56S ocupa a altura; a borda do mapa é curva, e o mapa corre dentro dela. */
      /* 31/10, 2º, «ligeiramente mais esticado, parece que ficou muito narrow»: a Equal Earth esticada 15% na horizontal. A
         escala uniforme mantém a proporção de área entre os países (todos crescem 15%), que é o que a projeção mostra */
      var ESTICA = 1.15, MAPA_RAW = function (l, p) { var r = d3.geoEqualEarthRaw(l, p); return [r[0] * ESTICA, r[1]]; }, RAD0 = Math.PI / 180;
      MAPA_RAW.invert = function (x, y) { return d3.geoEqualEarthRaw.invert(x / ESTICA, y); };
      var W = 960, H = 480, LAT_N = 86, LAT_S = -58, Y_N = MAPA_RAW(0, LAT_N * RAD0)[1], Y_S = MAPA_RAW(0, LAT_S * RAD0)[1], ESC_MAPA = H / (Y_N - Y_S), Y_MAPA = (Y_N + Y_S) / 2 * ESC_MAPA, X_EQ = MAPA_RAW(Math.PI, 0)[0], ESC_GLOBO = H / 2 - 8, KM = ESC_MAPA * X_EQ / 180;
      var GIRO_BR = [52, 12], giro = [-10, 0], prog = 1, anima = false, arrasta = null, sobre = false, cxG = W / 2, cxM = W / 2, fimVis = W * .92, crescendo = false, mouseDentro = false;
      var muta = d3.geoProjectionMutator(function (t) { return function (x, y) { var a = d3.geoOrthographicRaw(x, y), b = MAPA_RAW(x, y); return [a[0] + t * (b[0] - a[0]), a[1] + t * (b[1] - a[1])]; }; });
      var proj = muta(0).translate([W / 2, H / 2]).precision(.5), geo = d3.geoPath(proj);
      var FEATS = MUNDO.features.filter(function (f) { return f.id !== '010'; });
      /* 31/10/2026, «quero que os pontos dos países fiquem parecidos com o da Sodexo»: o mapa é uma trama de pontos, como no
         dashboard do HASDA 2027, desenhada num canvas atrás do SVG. O SVG fica com os contornos invisíveis (só para a dica
         do mouse) e com as etiquetas dos países. Malha de 0,6°, tirada do próprio mundo-110m: cada país é pintado num canvas
         fora da tela com uma cor que é o seu número, e a malha lê a cor em cada nó; onde a cor vem misturada (borda entre
         dois países, costa), vale o vizinho mais próximo com cor limpa. */
      var cv = document.createElement('canvas'); cv.className = 'mp-pontos'; cv.setAttribute('aria-hidden', 'true'); box.insertBefore(cv, box.firstChild);
      var ctx = cv.getContext('2d');
      var svg = d3.select(box).insert('svg', '.mp-dica').attr('viewBox', '0 0 ' + W + ' ' + H).attr('role', 'img').attr('aria-label', T('Mapa de certificados por país', 'Map of certificates by country')).classed('plano', true);
      var PASSO = .6, PTS = FEATS.map(function () { return []; }), RID = null, RW = 0, RH = 0, celas = null, celasChave = '', img = null, buf = null;
      (function () {
        var cw = Math.round(720 / PASSO), ch = Math.round(360 / PASSO), oc = document.createElement('canvas'); oc.width = cw; oc.height = ch;
        var o = oc.getContext('2d'), gp = d3.geoPath(d3.geoEquirectangular().scale(cw / (2 * Math.PI)).translate([cw / 2, ch / 2]).precision(.2), o);
        FEATS.forEach(function (f, i) { var k = i + 1; o.fillStyle = 'rgb(' + k + ',' + ((k * 37) % 256) + ',97)'; o.beginPath(); gp(f); o.fill(); });
        var px = o.getImageData(0, 0, cw, ch).data, n = cw * ch; RW = cw; RH = ch; RID = new Int16Array(n);
        for (var t = 0, q = 0; t < n; t++, q += 4) {   // número do país em cada pixel; -2 = cor misturada de borda com mais de meio pixel de terra
          var al = px[q + 3], k = px[q];
          RID[t] = !al ? -1 : (al === 255 && px[q + 2] === 97 && k >= 1 && k <= FEATS.length && px[q + 1] === (k * 37) % 256) ? k - 1 : (al >= 128 ? -2 : -1);
        }
        var viz = [-1, 1, -cw, cw, -cw - 1, -cw + 1, cw - 1, cw + 1, -2, 2, -2 * cw, 2 * cw];
        for (var t2 = 0; t2 < n; t2++) if (RID[t2] === -2) { var achou = -1; for (var v = 0; v < viz.length; v++) { var u = RID[t2 + viz[v]]; if (u >= 0) { achou = u; break; } } RID[t2] = achou; }
        for (var la = 84 - PASSO / 2; la > -60; la -= PASSO) for (var lo = -180 + PASSO / 2; lo < 180; lo += PASSO) {
          var idx = RID[Math.floor((90 - la) / 180 * ch) * cw + Math.floor((lo + 180) / 360 * cw)];
          if (idx >= 0) PTS[idx].push(lo, la);
        }
        PTS = PTS.map(function (a) { return new Float32Array(a); });
      })();
      /* cor de cada país pelo número de certificados (5 faixas); terra sem certificado em tinta a 20%. Na troca de norma a cor
         de cada país passa da antiga para a nova em .6 s; na entrada, sai do tom apagado */
      var NIV_DIA = [[20, 48, 76, .2], [169, 195, 222, 1], [127, 163, 201, 1], [92, 136, 184, 1], [51, 102, 153, 1], [20, 48, 76, 1]];
      /* no escuro a escala se inverte: mais certificados, mais claro (o ponto cheio acende sobre o fundo azul-noite) */
      var NIV_NOITE = [[220, 230, 242, .16], [44, 74, 110, 1], [62, 101, 147, 1], [92, 136, 184, 1], [141, 179, 221, 1], [214, 228, 245, 1]];
      /* 31/10, «com essa cor tem estados que não aparecem; a mesma cor dos gráficos»: no marinho e no azul a escala é de branco
         translúcido (16% a 100%), que aparece sobre qualquer fundo azul; os tons azuis do escuro se confundiam com o fundo */
      var NIV_BRANCA = [[255, 255, 255, .16], [255, 255, 255, .38], [255, 255, 255, .55], [255, 255, 255, .72], [255, 255, 255, .88], [255, 255, 255, 1]];
      function nivTema() { var p = paletaTema(); return p === 'dia' ? NIV_DIA : p === 'branca' ? NIV_BRANCA : NIV_NOITE; }
      var NIV = nivTema();
      var nivelF = FEATS.map(function () { return 0; }), corAt = FEATS.map(function () { return NIV[0].slice(); }), corPara = corAt, corDe = null, corT0 = 0, faixa = null, corChave = '';
      /* quadro do tamanho da área: H fixo, W pela proporção da caixa; o globo fica no centro da parte livre, à esquerda da placa dos dados */
      function quadro() {
        var r = box.getBoundingClientRect(), lado = $('#mp-lado'), cobre = 0;
        if (getComputedStyle(box).position === 'absolute' && r.height > 40) {
          W = Math.max(480, Math.round(H * r.width / r.height));
          if (lado && getComputedStyle(lado).position === 'absolute') cobre = Math.max(0, r.right - lado.getBoundingClientRect().left) * H / r.height;
        } else W = 960;
        svg.attr('viewBox', '0 0 ' + W + ' ' + H);
        cxM = W / 2; cxG = Math.max(ESC_GLOBO + 20, (W - cobre) / 2); fimVis = W - cobre;   // rótulos somem antes da placa dos dados
      }
      quadro();
      function pintaPontos() {
        var r = svg.node().getBoundingClientRect(); if (!r.width || !ctx) return;
        var br = box.getBoundingClientRect(), dpr = Math.min(2, window.devicePixelRatio || 1), cwp = Math.round(r.width * dpr), chp = Math.round(r.height * dpr);
        if (cv.width !== cwp || cv.height !== chp) { cv.width = cwp; cv.height = chp; cv.style.width = r.width + 'px'; cv.style.height = r.height + 'px'; }
        cv.style.left = (r.left - br.left) + 'px'; cv.style.top = (r.top - br.top) + 'px';
        var s = Math.min(r.width / W, r.height / H), ox = (r.width - W * s) / 2, oy = (r.height - H * s) / 2;
        ctx.setTransform(dpr * s, 0, 0, dpr * s, dpr * ox, dpr * oy); ctx.clearRect(-ox / s, -oy / s, r.width / s, r.height / s);
        if (corDe) {
          var kc = Math.min(1, (performance.now() - corT0) / 600), e = 1 - Math.pow(1 - kc, 3);
          corAt = corDe.map(function (c, i) { var p = corPara[i]; return [c[0] + (p[0] - c[0]) * e, c[1] + (p[1] - c[1]) * e, c[2] + (p[2] - c[2]) * e, c[3] + (p[3] - c[3]) * e]; });
          if (kc >= 1) corDe = null;
        }
        var a = Math.sqrt(Math.max(0, Math.min(1, prog))), lam = giro[0], ph = giro[1] * Math.PI / 180, cP = Math.cos(ph), sP = Math.sin(ph), R = ESC_GLOBO, tyM = H / 2 + Y_MAPA, RAD = Math.PI / 180;
        if (a < 1) {   // bola de vidro do globo (some ao abrir em mapa); no escuro, vidro azulado com borda clara
          var gr = ctx.createRadialGradient(cxG - R * .36, H / 2 - R * .48, R * .05, cxG, H / 2, R);
          if (NOITE) { gr.addColorStop(0, 'rgba(120,150,220,.22)'); gr.addColorStop(.5, 'rgba(60,80,140,.10)'); gr.addColorStop(1, 'rgba(110,140,220,.28)'); }
          else { gr.addColorStop(0, 'rgba(255,255,255,.62)'); gr.addColorStop(.45, 'rgba(255,255,255,.24)'); gr.addColorStop(.82, 'rgba(232,240,248,.26)'); gr.addColorStop(1, 'rgba(185,205,226,.5)'); }
          /* 31/10: «o globo só apareça depois que os continentes se juntarem em forma esférica»: o vidro da bola só acende nos últimos
             15% da passagem (a de .15 a 0), quando os pontos já fecharam a esfera; ao abrir em mapa, apaga logo no começo */
          var esf = Math.max(0, Math.min(1, 1 - a / .15)); esf = esf * esf * (3 - 2 * esf);
          ctx.globalAlpha = esf; ctx.beginPath(); ctx.arc(cxG, H / 2, R, 0, 6.2832); ctx.fillStyle = gr; ctx.fill(); ctx.lineWidth = 1.2; ctx.strokeStyle = NOITE ? 'rgba(170,195,255,.35)' : 'rgba(255,255,255,.9)'; ctx.stroke();
        }
        var qM = PASSO * KM, qG = PASSO * RAD * R;
        /* 31/10, «a trama não ficou legal»: no mapa aberto a trama é de TELA, não geográfica: um ponto quadrado de 2 px a cada
           3 px de tela (2,5 px css × escala, ponto em 62% do passo), cravado no pixel, e cada nó lê o país no raster.
           Equal Earth (31/10, 2º): a longitude escala diferente em cada latitude, então o giro não é mais um deslize da faixa;
           cada quadro refaz a malha (inversa da projeção por linha, guardada) e escreve os pontos direto num ImageData */
        if (a >= 1) {
          var sd = s * dpr, PX = Math.max(3, Math.round(2.5 * dpr)), DOT = Math.max(2, Math.round(PX * .62)), Wd = cv.width, Hd = cv.height, ck = [Wd, Hd, PX, W, sd.toFixed(4)].join();
          if (celasChave !== ck) {   // por linha da malha: y na tela, linha do raster e unidades por radiano de longitude nessa latitude
            celasChave = ck; celas = [];
            for (var cy = Math.floor(PX / 2); cy < Hd; cy += PX) {
              var yr = (tyM - (cy - oy * dpr) / sd) / ESC_MAPA; if (yr > Y_N + .03 || yr < Y_S - .03) continue;
              var phi = MAPA_RAW.invert(0, yr)[1], lat = phi / RAD0; if (!(lat <= 84 && lat >= -60)) continue;
              celas.push(cy, Math.floor((90 - lat) / 180 * RH) * RW, MAPA_RAW(1, phi)[0] * ESC_MAPA);
            }
            img = ctx.createImageData(Wd, Hd); buf = new Uint32Array(img.data.buffer);
          }
          buf.fill(0);
          var cores = corAt.map(function (c) { return ((Math.round(c[3] * 255) << 24) | (Math.round(c[2]) << 16) | (Math.round(c[1]) << 8) | Math.round(c[0])) >>> 0; });
          var mD = Math.floor(DOT / 2), x0u = ox * dpr, PI = Math.PI;
          for (var r = 0; r < celas.length; r += 3) {
            var cy2 = celas[r], ry = celas[r + 1], kx = celas[r + 2], lin = (cy2 - mD) * Wd;
            for (var cx2 = Math.floor(PX / 2); cx2 < Wd; cx2 += PX) {
              var lonR = ((cx2 - x0u) / sd - cxM) / kx; if (lonR < -PI || lonR > PI) continue;
              var lon = lonR / RAD0 - lam; lon = ((lon % 360) + 540) % 360 - 180;
              var id = RID[ry + Math.min(RW - 1, Math.floor((lon + 180) / 360 * RW))]; if (id < 0) continue;
              var cor = cores[id]; if (!cor) continue;
              for (var dy = 0; dy < DOT; dy++) { var o = lin + dy * Wd + cx2 - mD; if (o < 0 || o >= buf.length - DOT) continue; for (var dx = 0; dx < DOT; dx++) buf[o + dx] = cor; }
            }
          }
          ctx.putImageData(img, 0, 0);
          return;
        }
        for (var i = 0; i < PTS.length; i++) {
          var P = PTS[i]; if (!P.length) continue;
          var c = corAt[i], L = nivelF[i], qm = qM * (L ? .62 : .5);
          ctx.fillStyle = 'rgb(' + Math.round(c[0]) + ',' + Math.round(c[1]) + ',' + Math.round(c[2]) + ')';
          if (a >= 1) {   // mapa aberto: só a conta da longitude, sem trigonometria
            ctx.globalAlpha = c[3];
            for (var j = 0; j < P.length; j += 2) { var lw = ((P[j] + lam) % 360 + 540) % 360 - 180; ctx.fillRect(cxM + lw * KM - qm / 2, tyM - P[j + 1] * KM - qm / 2, qm, qm); }
            continue;
          }
          for (var j2 = 0; j2 < P.length; j2 += 2) {   // globo e passagem: cada ponto viaja da posição no globo para a do mapa
            var lo = (P[j2] + lam) * RAD, la = P[j2 + 1] * RAD, cl = Math.cos(la), x = cl * Math.cos(lo), y = cl * Math.sin(lo), z = Math.sin(la);
            var Y = z * cP + x * sP, Dp = x * cP - z * sP;
            if (Dp <= 0 && a < .02) { ctx.globalAlpha = c[3] * .07; ctx.fillRect(cxG + R * y - .35, H / 2 - R * Y - .35, .7, .7); continue; }
            var lw2 = ((P[j2] + lam) % 360 + 540) % 360 - 180, gx = cxG + R * y, gy = H / 2 - R * Y, pm = MAPA_RAW(lw2 * RAD, P[j2 + 1] * RAD), mx = cxM + pm[0] * ESC_MAPA, my = tyM - pm[1] * ESC_MAPA;
            var aG = Dp > 0 ? .45 + .55 * Dp : .05, qg = Dp > 0 ? qG * (L ? .55 : .45) * (.65 + .35 * Dp) : qG * .3, q = qg + (qm - qg) * a;
            ctx.globalAlpha = c[3] * (aG + (1 - aG) * a);
            ctx.fillRect(gx + (mx - gx) * a - q / 2, gy + (my - gy) * a - q / 2, q, q);
          }
        }
        ctx.globalAlpha = 1;
      }
      pintaPaises = function () {
        var s = D.survey[mapaNum], cortes = [1, 10, 100, 1000, 10000];
        nivelF = FEATS.map(function (f) { var a2 = porNumFeat[f.id], v = a2 ? s.paises[a2] : 0; if (!v) return 0; for (var i = cortes.length - 1; i >= 0; i--) if (v >= cortes[i]) return i + 1; return 1; });
        corPara = nivelF.map(function (n) { return NIV[n]; }); corChave = mapaNum + paletaTema();
        if (calmo) { corAt = corPara.map(function (c) { return c.slice(); }); corDe = null; } else { corDe = corAt.map(function (c) { return c.slice(); }); corT0 = performance.now(); }
        pintaPontos();
      };
      paths = svg.append('g').selectAll('path').data(FEATS).enter().append('path').attr('class', 'pais');
      /* 27/10: «nos principais países, com pulso animado, fosse mostrando os números conforme o globo gira». 31/10, no mapa
         aberto, a marcação do HASDA: ponto no país, haste fina que cresce para cima e, na ponta, a etiqueta de vidro com a
         bandeira e o número, que sobe de baixo e conta de zero quando o país entra; nenhuma etiqueta sobre outra (a do maior
         país escolhe primeiro; a seguinte sobe ou vai para o lado e ganha um fio até a haste). No globo continua a coluna
         com as varetas em curva. */
      var gPulsos = svg.append('g').attr('class', 'pulsos'), centro = {};
      MUNDO.features.forEach(function (f) { var a2 = porNumFeat[f.id]; if (a2) centro[a2] = d3.geoCentroid(f); });
      refazPulsos = function () {
        var s = D.survey[mapaNum]; if (!s) return;
        var top = Object.keys(s.paises).filter(function (a) { return centro[a]; }).sort(function (a, b) { return s.paises[b] - s.paises[a]; }).slice(0, 10);
        if (s.paises.BR && centro.BR && top.indexOf('BR') < 0) top.push('BR');
        var g = gPulsos.selectAll('g.pulso').data(top.map(function (a) { return { a2: a, c: centro[a], v: s.paises[a] }; }), function (d) { return d.a2; });
        g.exit().remove();
        var e = g.enter().append('g').attr('class', 'pulso');
        e.append('path').attr('class', 'vareta');
        e.append('circle').attr('class', 'anel').attr('r', 7).style('animation-delay', function (d, i) { return (i * .27) + 's'; });
        e.append('circle').attr('class', 'ponto').attr('r', 1.8);
        var t = e.append('text').attr('class', 'rot'); t.append('tspan').attr('class', 'nome'); t.append('tspan').attr('class', 'n').attr('dx', 6);
        var et = e.append('g').attr('class', 'etq');
        et.append('path').attr('class', 'fio'); et.append('rect').attr('class', 'pilula').attr('height', 18).attr('rx', 3);
        et.append('image').attr('class', 'bandeira').attr('width', 16).attr('height', 12).attr('preserveAspectRatio', 'none');
        et.append('text').attr('class', 'en');
        gPulsos.selectAll('g.pulso').each(function (d, i) { d.vaga = i; d.naFrente = false; d.t0 = 0; d.lo = null; });
        /* 27/10: «quando mudo de norma tem que sair os dados da anterior»: select (não selectAll) repassa o dado novo aos filhos */
        gPulsos.selectAll('g.pulso').select('.nome').text(function (d) { return nomePais(d.a2); });
        gPulsos.selectAll('g.pulso').select('.n').each(function () { this.dataset.v = 0; this.textContent = ''; });
        gPulsos.selectAll('g.pulso').select('.en').each(function () { this.dataset.v = 0; this.textContent = ''; });
        gPulsos.selectAll('g.pulso').select('image').attr('href', function (d) { return 'https://cdn.jsdelivr.net/npm/flag-icons@7.2.3/flags/4x3/' + d.a2.toLowerCase() + '.svg'; });
        poePulsos();
      };
      function poePulsos() {
        var a = Math.sqrt(Math.max(0, Math.min(1, prog))), olho = [-giro[0], -giro[1]], agora = performance.now(), mapa = a > .5;
        var n = gPulsos.selectAll('g.pulso').size(), x0 = cxG + ESC_GLOBO + 26, y0 = H / 2 - (n - 1) * 11, postos = [], lista = [];
        gPulsos.selectAll('g.pulso').each(function (d) { lista.push([this, d]); });
        lista.sort(function (u, v) { return v[1].v - u[1].v; });   // o maior país escolhe o lugar da etiqueta primeiro
        crescendo = false;
        lista.forEach(function (it) {
          var el = it[0], d = it[1], g = d3.select(el), p = proj(d.c), sy = y0 + d.vaga * 22;
          /* no mapa que corre, a marcação surge só depois que o país entrou 8% da largura e some antes da placa dos dados */
          var vis = !!p && (a > .98 ? p[0] > W * .08 && p[0] < fimVis - 30 : d3.geoDistance(d.c, olho) < 1.42);
          if (d.modo !== mapa) { d.modo = mapa; d.naFrente = false; }
          g.classed('no-mapa', mapa).style('opacity', vis ? 1 : 0);
          /* 27/10: ao entrar na frente, o número corre de zero até o valor em 1,2 s; ao sair, volta a zero */
          var nEl = el.querySelector(mapa ? '.en' : '.n'), outro = el.querySelector(mapa ? '.n' : '.en');
          if (vis && !d.naFrente) { d.naFrente = true; d.t0 = agora; d.lo = null; outro.dataset.v = 0; outro.textContent = ''; roleta(nEl, d.v, 1200); }
          else if (!vis && d.naFrente) { d.naFrente = false; nEl.dataset.v = 0; nEl.textContent = ''; }
          if (!p) return;
          g.selectAll('circle').attr('cx', p[0]).attr('cy', p[1]);
          if (mapa) {
            var gr = calmo ? 1 : Math.max(0, Math.min(1, (agora - d.t0) / 1200)); if (vis && gr < 1) crescendo = true;
            var cr = 1 - Math.pow(1 - gr, 3), PILHA = 26, base = p[1] - 3, topo = base - PILHA;
            g.select('path.vareta').attr('d', 'M' + p[0].toFixed(1) + ',' + base.toFixed(1) + 'V' + (base - PILHA * cr).toFixed(1));
            var pw = 35 + fmt(d.v).length * 6.3, ph = 18, lx0 = p[0], ly0 = topo - ph / 2 - 2, alvo = [0, 0];
            var livre = function (x, y) { return y - ph / 2 > 4 && postos.every(function (q) { return x + pw / 2 + 3 < q[0] || x - pw / 2 - 3 > q[1] || y + ph / 2 + 3 < q[2] || y - ph / 2 - 3 > q[3]; }); };
            if (vis && !livre(lx0, ly0)) {
              for (var k = 1, ok = false; k <= 14 && !ok; k++) [[0, -k * (ph + 4)], [pw + 6, -(k - 1) * (ph + 4)], [-(pw + 6), -(k - 1) * (ph + 4)]].some(function (c) { if (livre(lx0 + c[0], ly0 + c[1])) { alvo = c; ok = true; return true; } return false; });
            }
            if (vis) postos.push([lx0 + alvo[0] - pw / 2, lx0 + alvo[0] + pw / 2, ly0 + alvo[1] - ph / 2, ly0 + alvo[1] + ph / 2]);
            if (!d.lo) d.lo = alvo.slice(); else { d.lo[0] += (alvo[0] - d.lo[0]) * .2; d.lo[1] += (alvo[1] - d.lo[1]) * .2; }
            var sobe = calmo ? 0 : Math.pow(1 - Math.min(1, gr / .6), 3) * 22, px = lx0 + d.lo[0], py = ly0 + d.lo[1] + sobe;
            var et = g.select('g.etq').style('opacity', Math.min(1, gr / .25));
            et.select('rect').attr('x', (px - pw / 2).toFixed(1)).attr('y', (py - ph / 2).toFixed(1)).attr('width', pw.toFixed(1));
            et.select('image').attr('x', (px - pw / 2 + 7).toFixed(1)).attr('y', (py - 6).toFixed(1));
            et.select('text').attr('x', (px - pw / 2 + 28).toFixed(1)).attr('y', (py + 3.6).toFixed(1));
            et.select('path.fio').attr('d', Math.abs(d.lo[0]) + Math.abs(d.lo[1]) > 3 ? 'M' + p[0].toFixed(1) + ',' + topo.toFixed(1) + 'L' + px.toFixed(1) + ',' + (py + (d.lo[1] < -3 ? ph / 2 : 0)).toFixed(1) : null);
          } else {
            /* curva em S: sai do país na horizontal e chega na vaga na horizontal (bezier com os dois controles no meio do caminho) */
            var xm = (p[0] + x0 - 6) / 2;
            g.select('path.vareta').attr('d', 'M' + p[0].toFixed(1) + ',' + p[1].toFixed(1) + 'C' + xm.toFixed(1) + ',' + p[1].toFixed(1) + ' ' + xm.toFixed(1) + ',' + sy + ' ' + (x0 - 6) + ',' + sy);
            g.select('text.rot').attr('x', x0).attr('y', sy + 4);
          }
        });
      }
      function desenha() {
        var a = Math.sqrt(Math.max(0, Math.min(1, prog)));
        proj = muta(a).scale(ESC_GLOBO + a * (ESC_MAPA - ESC_GLOBO)).translate([cxG + a * (cxM - cxG), H / 2 + a * Y_MAPA]).rotate(giro).precision(.5);
        var raio = (90 + a * 89) * Math.PI / 180;   // corte em círculo que cresce até quase o antípoda, encadeado com o corte no antimeridiano
        proj.preclip(a < .999 ? function (s) { return d3.geoClipCircle(raio)(d3.geoClipAntimeridian(s)); } : d3.geoClipAntimeridian);
        geo = d3.geoPath(proj);
        if (mouseDentro || a < 1) paths.attr('d', geo);   // contornos invisíveis, só para a dica do mouse: no mapa aberto, só com o mouse sobre o mapa
        pintaPontos(); poePulsos();
      }
      var calmo = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches, ult = 0;
      function gira(t) {
        /* 31/10: o mapa aberto também corre (da esquerda para a direita, .007 grau/ms, cerca de 50 s por volta); o globo segue a .009.
           Parado (mouse sobre um país), as etiquetas que estão nascendo e a troca de cor continuam */
        var ativa = !document.hidden && $('#v-mapa').classList.contains('ativa');
        if ((prog === 0 || prog === 1) && !anima && !arrasta && !sobre && ativa) { giro[0] += Math.min(t - ult, 50) * (prog ? .0095 : .0099); desenha(); }   // 31/10: «10% mais rápida»; 2º, «girasse um pouquinho mais rápido»: mapa .0095
        else if (ativa && !anima) { if (corDe) pintaPontos(); if (crescendo) poePulsos(); }
        ult = t; if (!calmo) requestAnimationFrame(gira);
      }
      var bt = d3.select(box).append('div').attr('class', 'mp-ctl'), btVira = bt.append('button').attr('type', 'button').text(T('Abrir em globo', 'Open as globe')), btCentro = bt.append('button').attr('type', 'button').text(T('Centralizar', 'Recenter'));
      function lonPerto(de, para) { return para + Math.round((de - para) / 360) * 360; }
      btVira.on('click', function () {
        if (anima) return; anima = true; btVira.property('disabled', true);
        var p0 = prog, p1 = prog < .5 ? 1 : 0, g0 = giro.slice(), g1 = p1 ? [giro[0], 0] : [lonPerto(giro[0], GIRO_BR[0]), GIRO_BR[1]], t0 = performance.now(), dur = calmo ? 1 : 1600;
        (function passo(t) {
          var k = Math.min((t - t0) / dur, 1), e = d3.easeCubicInOut(k);
          prog = p0 + (p1 - p0) * e; giro = [g0[0] + (g1[0] - g0[0]) * e, g0[1] + (g1[1] - g0[1]) * e]; desenha();
          if (k < 1) return requestAnimationFrame(passo);
          prog = p1; anima = false; btVira.property('disabled', false).text(p1 ? T('Abrir em globo', 'Open as globe') : T('Abrir em mapa', 'Open as map'));
          svg.classed('plano', !!p1).attr('aria-label', p1 ? T('Mapa de certificados por país', 'Map of certificates by country') : T('Globo de certificados por país', 'Globe of certificates by country'));
          desenha();
        })(t0);
      });
      btCentro.on('click', function () { if (!anima && prog === 0) { giro = GIRO_BR.slice(); desenha(); } });
      /* 31/10: no mapa aberto o arraste puxa o mapa para os lados (só a longitude) */
      svg.on('pointerdown', function (ev) { if (anima) return; arrasta = [ev.clientX, ev.clientY]; svg.classed('arrastando', true); });
      window.addEventListener('pointermove', function (ev) {
        if (!arrasta) return; var w = svg.node().getBoundingClientRect().width;
        if (prog === 1) giro[0] += (ev.clientX - arrasta[0]) * 360 * W / (2 * X_EQ * ESC_MAPA * w);
        else { var k = 300 / w; giro[0] += (ev.clientX - arrasta[0]) * k; giro[1] = Math.max(-80, Math.min(80, giro[1] - (ev.clientY - arrasta[1]) * k)); }
        arrasta = [ev.clientX, ev.clientY]; desenha();
      });
      window.addEventListener('pointerup', function () { arrasta = null; svg.classed('arrastando', false); });
      svg.on('pointermove', function (ev) {   // 27/10: para de girar só com o mouse sobre o globo; 31/10: no mapa aberto, com o mouse sobre um país
        if (prog === 1) { sobre = !!(ev.target && ev.target.classList && ev.target.classList.contains('pais')); return; }
        var r = this.getBoundingClientRect(), x = (ev.clientX - r.left) * W / r.width - cxG, y = (ev.clientY - r.top) * H / r.height - H / 2;
        sobre = x * x + y * y <= ESC_GLOBO * ESC_GLOBO;
      }).on('pointerleave', function () { sobre = false; mouseDentro = false; }).on('pointerenter', function () { mouseDentro = true; paths.attr('d', geo); });
      if (window.ResizeObserver) new ResizeObserver(function () { quadro(); desenha(); }).observe(box);
      document.addEventListener('pn-tema', function () { NIV = nivTema(); pintaPaises(); pintaMapaLegenda(); desenha(); });
      desenha(); requestAnimationFrame(function (t) { ult = t; gira(t); });
      var porNum = porNumFeat;
      paths.on('mousemove', function (ev, f) {
        var a2 = porNum[f.id], v = a2 && D.survey[mapaNum].paises[a2];
        dica.style.display = 'block'; var r = box.getBoundingClientRect();
        dica.style.left = (ev.clientX - r.left) + 'px'; dica.style.top = (ev.clientY - r.top) + 'px';
        dica.innerHTML = esc(a2 ? nomePais(a2) : f.properties.name) + (v ? ' · <b>' + fmt(v) + '</b>' : T(' · sem certificado registrado', ' · no certificate recorded'));
      }).on('mouseleave', function () { dica.style.display = 'none'; });
      WORLD_OK = true; pintaMapa();
    });
  }
  var CORES_DIA = ['rgba(20,48,76,.2)', '#A9C3DE', '#7FA3C9', '#5C88B8', '#336699', '#14304C'], CORES_NOITE = ['rgba(220,230,242,.16)', '#2C4A6E', '#3E6593', '#5C88B8', '#8DB3DD', '#D6E4F5'];   // 31/10: as faixas da trama de pontos, nos dois temas
  /* 31/10, «deixe bem claro que esses dados são da ISO Survey… o link para o ISO Survey logo na página inicial, próximo à
     legenda; a legenda pode ficar um pouquinho menos larga»: a legenda ganha uma segunda linha com a fonte e o link oficial */
  var ISO_SURVEY = 'https://www.iso.org/the-iso-survey.html';
  var CORES_BRANCA = ['rgba(255,255,255,.16)', 'rgba(255,255,255,.38)', 'rgba(255,255,255,.55)', 'rgba(255,255,255,.72)', 'rgba(255,255,255,.88)', '#FFFFFF'];
  function paletaTema() { var v = document.documentElement.getAttribute('data-noite'); return !NOITE ? 'dia' : v === 'azul' ? 'branca' : 'noite'; }   // 31/10, 2º: «preferiria que tivesse mexido na cor do fundo»: no marinho volta a escala azul e o fundo escurece (CSS)
  function coresTema() { var p = paletaTema(); return p === 'dia' ? CORES_DIA : p === 'branca' ? CORES_BRANCA : CORES_NOITE; }
  function pintaMapaLegenda() { var C = coresTema(); $('#mp-esc').innerHTML = '<span style="margin-left:0">' + T('certificados', 'certificates') + '</span>' + ['0', '1', '10', '100', T('1 mil', '1k'), T('10 mil+', '10k+')].map(function (t, i) { return '<i style="background:' + C[i] + '"></i><span>' + t + '</span>'; }).join('') +
    '<a class="mp-fonte" href="' + ISO_SURVEY + '" target="_blank" rel="noopener">' + T('Fonte: ISO Survey 2025 (ISO) · certificados acreditados em vigor em 31-dez-2025', 'Source: ISO Survey 2025 (ISO) · accredited certificates in force on 31-dec-2025') + ' <b aria-hidden="true">↗</b></a>'; }
  function pintaMapa() {
    var s = D.survey[mapaNum]; if (!s) return;
    var porNum = {}; Object.keys(D.paises).forEach(function (a2) { if (D.paises[a2].n) porNum[D.paises[a2].n] = a2; });
    var cortes = [1, 10, 100, 1000, 10000];
    var cor = function (v) { if (!v) return CORES[0]; for (var i = cortes.length - 1; i >= 0; i--) if (v >= cortes[i]) return CORES[i + 1]; return CORES[1]; };
    if (pintaPaises) pintaPaises();   // 31/10: os países são a trama de pontos do canvas
    if (refazPulsos) refazPulsos();
    pintaMapaLegenda();
    pintaLado();
  }
  /* 27/10: «faça os números com efeito tipo roleta»: o número corre do valor atual até o novo em .7 s (ease-out), formatado */
  function roleta(el, para, dur) {
    para = +para || 0; var de = +el.dataset.v || 0; el.dataset.v = para;
    if (el._roleta) cancelAnimationFrame(el._roleta);
    if (de === para || (window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches)) { el.textContent = fmt(para); return; }
    var t0 = performance.now(); dur = dur || 700;
    (function passo(t) {
      var k = Math.min((t - t0) / dur, 1), e = 1 - Math.pow(1 - k, 3);
      el.textContent = fmt(Math.round(de + (para - de) * e));
      if (k < 1) el._roleta = requestAnimationFrame(passo); else el._roleta = null;
    })(t0);
  }
  function pintaLado() {
    /* 27/10: «a mesma coisa para aqui, não quero que pisque»: a lateral é montada UMA vez, com 11 vagas no ranking (10 + Brasil
       fora do top 10); a troca de norma só troca textos, bandeiras e larguras no lugar, com as barras deslizando. */
    var s = D.survey[mapaNum], nome = SURVEY_NOME[mapaNum] || 'ISO ' + mapaNum;
    var rank = Object.keys(s.paises).sort(function (a, b) { return s.paises[b] - s.paises[a]; });
    var posBR = rank.indexOf('BR') + 1, latam = rank.filter(function (a) { return LATAM.indexOf(a) >= 0; }), posLA = latam.indexOf('BR') + 1;
    var max = s.paises[rank[0]];
    var top = rank.slice(0, 10); if (posBR > 10) top.push('BR');
    var lado = $('#mp-lado');
    if (!lado.dataset.pronto) {
      lado.dataset.pronto = '1';
      lado.innerHTML = '<h3></h3><div class="m" id="mp-tit"></div><div class="tot"><span id="mp-tot"></span><small id="mp-paises"></small></div>' +
        '<a class="mp-fonte-card" href="' + ISO_SURVEY + '" target="_blank" rel="noopener">' + T('Dados do ISO Survey 2025 (ISO)', 'Data from the ISO Survey 2025 (ISO)') + ' ↗</a>' +
        '<div class="mp-br"><span class="m">' + T('Brasil', 'Brazil') + '</span><div class="v"><span id="mp-brv"></span><small id="mp-brpos"></small></div><div class="mp-brsit" id="mp-brsit"></div></div>' +
        '<div class="mp-rola"><ul class="mp-rank">' + Array.apply(null, Array(11)).map(function () { return '<li><span class="m"></span><span><img class="bandeira" alt="" loading="lazy"><span class="nome"></span></span><b></b><span class="barra"><i style="width:0"></i></span></li>'; }).join('') + '</ul>' +
        '<p class="mp-nota">' + T('Como ler: o número é o total de certificados em vigor em 31-dez-2025, emitidos em qualquer ano e ainda válidos nessa data; não é o número de certificações feitas em 2025. Site é cada local permanente coberto por um certificado. Entram só certificados de organismos acreditados por membros da Global ACI (antigo IAF), carregados no IAF CertSearch: certificação sem acreditação e certificadoras que ainda não enviaram dados ficam de fora, então o total real do país pode ser maior. Fonte: ISO Survey 2025, publicado em outubro de 2026.', 'How to read: the figure is the total of certificates in force on 31-dec-2025, issued in any year and still valid on that date; it is not the number of certifications granted in 2025. A site is each permanent location covered by a certificate. Only certificates from bodies accredited by Global ACI members (formerly IAF), uploaded to IAF CertSearch, are counted: non-accredited certification and certification bodies that have not yet uploaded data are left out, so the real total for a country may be higher. Source: ISO Survey 2025, published October 2026.') + '</p></div>';   // 27/10: ranking e nota numa caixa que rola; total e Brasil ficam fixos em cima
      cascata($('.mp-rank', lado), 'li');
    }
    $('h3', lado).textContent = nome; $('#mp-tit').textContent = s.titulo || '';
    roleta($('#mp-tot'), s.total); $('#mp-paises').textContent = T('certificados em vigor em ', 'certificates in force on ') + dataBR('2025-12-31') + (s.total_sites ? ' · ' + fmt(s.total_sites) + ' sites' : '') + ' · ' + rank.length + T(' países', ' countries');   // 27/10: «ficar bem claro que esse número é de 2025… todos os números válidos»
    roleta($('#mp-brv'), s.paises.BR || 0); $('#mp-brsit').textContent = (s.sites && s.sites.BR ? fmt(s.sites.BR) + ' sites · ' : '') + T('certificados em vigor em ', 'certificates in force on ') + dataBR('2025-12-31');
    $('#mp-brpos').textContent = (posBR ? T(posBR + 'º no mundo · ' + posLA + 'º na América Latina', '#' + posBR + ' worldwide · #' + posLA + ' in Latin America') : '');
    $$('.mp-rank li', lado).forEach(function (li, i) {
      var a = top[i]; li.style.display = a ? '' : 'none'; if (!a) return;
      li.classList.toggle('br', a === 'BR');
      $('.m', li).textContent = rank.indexOf(a) + 1;
      /* 27/10: «faça o nome e bandeira dos países também com efeito roleta»: quando o país da vaga muda, nome e bandeira
         rolam para cima e o novo entra por baixo (classe .rola; a troca do conteúdo acontece no meio do giro) */
      var img = $('.bandeira', li), src = 'https://cdn.jsdelivr.net/npm/flag-icons@7.2.3/flags/4x3/' + a.toLowerCase() + '.svg', cel = img.parentNode;
      var troca = function () { img.style.visibility = 'visible'; img.onerror = function () { img.style.visibility = 'hidden'; }; img.setAttribute('src', src); $('.nome', li).textContent = nomePais(a); };
      if (li.dataset.a !== a) {
        li.dataset.a = a; cel.classList.remove('rola'); void cel.offsetWidth; cel.classList.add('rola');
        clearTimeout(li._troca); li._troca = setTimeout(troca, 260);
      }
      roleta($('b', li), s.paises[a]);
      $('.barra i', li).style.width = (s.paises[a] / max * 100) + '%';
    });
  }
})();
