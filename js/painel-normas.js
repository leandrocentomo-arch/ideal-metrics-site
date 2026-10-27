/* Painel de normas ISO. Dados: dados/painel-normas.json (gerado por _ferramentas/painel_normas.py),
   dados/painel-mudancas.json (diferenças entre gerações) e dados/mundo-110m.json (world-atlas).
   Fontes públicas: ISO Open Data (ODC-By 1.0) e ISO Survey 2025. */
(function () {
  'use strict';
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
  var esc = function (s) { return String(s == null ? '' : s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); };
  var MESES = ['jan', 'fev', 'mar', 'abr', 'mai', 'jun', 'jul', 'ago', 'set', 'out', 'nov', 'dez'];
  var dataBR = function (iso) { var p = String(iso).split('-'); return p.length < 3 ? iso : p[2] + '-' + MESES[+p[1] - 1] + '-' + p[0]; };   // dd-mmm-aaaa (26/10/2026)
  var fmt = function (n) { return (n == null ? '' : Number(n).toLocaleString('pt-BR')); };

  var FASES = [
    ['proposta', 'Proposta', '00 e 10', 'Estudo preliminar ou proposta de trabalho novo (NP). Os países votam se a norma deve existir. Nada do texto está decidido.'],
    ['preparacao', 'Rascunho de trabalho', '20', 'Um grupo de especialistas escreve o primeiro texto (WD). Circula só dentro do grupo de trabalho.'],
    ['comite', 'Rascunho de comitê', '30', 'O texto (CD) é discutido e comentado pelos países membros do comitê. Ainda muda bastante.'],
    ['consulta', 'Consulta pública', '40', 'O Draft International Standard (DIS) vai a voto de todos os membros da ISO, por 12 semanas. No Brasil, a ABNT abre consulta nacional. É o primeiro texto estável.'],
    ['aprovacao', 'Aprovação final', '50', 'O Final Draft (FDIS) recebe só voto, sem comentário técnico. Aprovado, a ISO publica em poucas semanas. É a versão que vai valer.'],
    ['publicada', 'Publicada', '60', 'Norma em vigor. Pode ser comprada na ISO e, no Brasil, na ABNT (versão NBR).'],
    ['revisao', 'Revisão sistemática', '90', 'A cada cinco anos a ISO consulta os países: manter, revisar ou cancelar. Um voto por revisar abre um projeto novo e a edição atual segue válida até a nova sair.']
  ];
  var FASE_IDX = {}; FASES.forEach(function (f, i) { FASE_IDX[f[0]] = i; });
  var TIPOS = { IS: 'Norma internacional', TS: 'Especificação técnica', TR: 'Relatório técnico', PAS: 'Especificação publicamente disponível', IWA: 'Acordo de workshop internacional', GUIDE: 'Guia ISO' };
  var CHAVE = ['9001', '14001', '45001', '39001', '22000', '27001', '37001', '37301', '14064-1', '14067', '14068-1', '14060', '41001', '22301', '31000', '50001', '42001', '53001', '59004', '17065', '17021-1'];
  var SURVEY_NOME = { '9001': 'ISO 9001', '14001': 'ISO 14001', '45001': 'ISO 45001', '27001': 'ISO/IEC 27001', '22000': 'ISO 22000', '13485': 'ISO 13485', '50001': 'ISO 50001', '20000-1': 'ISO/IEC 20000-1', '37001': 'ISO 37001', '22301': 'ISO 22301', '39001': 'ISO 39001', '28000': 'ISO 28000', '37301': 'ISO 37301', '41001': 'ISO 41001', '42001': 'ISO/IEC 42001', '44001': 'ISO 44001', '21001': 'ISO 21001', '55001': 'ISO 55001', '20121': 'ISO 20121', '22716': 'ISO 22716' };
  var LATAM = ['AR', 'BO', 'BR', 'CL', 'CO', 'CR', 'CU', 'DO', 'EC', 'SV', 'GT', 'HN', 'MX', 'NI', 'PA', 'PY', 'PE', 'PR', 'UY', 'VE'];

  var D = null, MUD = null, MUNDO = null, WORLD_OK = false;
  var F = { q: '', temas: {}, fases: {}, tipos: {}, pagina: false, ord: 'num' };
  var paisNome = (window.Intl && Intl.DisplayNames) ? new Intl.DisplayNames(['pt-BR'], { type: 'region' }) : null;

  function nomePais(a2) {
    try { var n = paisNome && paisNome.of(a2); if (n && n !== a2) return n; } catch (e) { }
    return (D.paises[a2] && D.paises[a2].nome) || a2;
  }

  /* ---------- carga ---------- */
  Promise.all([
    fetch('dados/painel-normas.json?v=' + (document.querySelector('script[src*="painel-normas.js"]').src.split('v=')[1] || 1)).then(function (r) { return r.json(); }),
    fetch('dados/painel-mudancas.json').then(function (r) { return r.ok ? r.json() : { itens: [] }; }).catch(function () { return { itens: [] }; })
  ]).then(function (res) {
    D = res[0]; MUD = res[1];
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
  $('.pn-puxa').addEventListener('click', function () {
    var ab = $('.pn').classList.toggle('lado-aberto');
    this.setAttribute('aria-expanded', ab); this.setAttribute('aria-label', ab ? 'Recolher busca e filtros' : 'Abrir busca e filtros');
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
  function deslizaTudo() { desliza($('.pn-abas'), '[aria-selected=true]'); desliza($('#mp-sel'), '[aria-pressed=true]'); desliza($('#st-sel'), '[aria-pressed=true]'); }
  window.addEventListener('resize', deslizaTudo);

  /* 27/10: efeito de entrada: cada filho direto do bloco (linhas, cartões) nasce 10 px abaixo e sobe, um atrás do outro */
  function entra(bloco) {
    if (!bloco || (window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches)) return;
    var i = 0; Array.prototype.forEach.call(bloco.children, function (el) {
      if (i > 40) return; el.classList.remove('entra'); void el.offsetWidth; el.style.animationDelay = (i++ * 35) + 'ms'; el.classList.add('entra');
    });
  }
  function mostraAba(id) {
    if (!$('#v-' + id)) return;
    $$('.pn-abas button').forEach(function (b) { b.setAttribute('aria-selected', b.dataset.aba === id); });
    $$('.pn-vista').forEach(function (v) { v.classList.toggle('ativa', v.id === 'v-' + id); });
    $('.pn').classList.toggle('sem-lado', id === 'mapa' || id === 'setores');   // 27/10: os filtros não valem para o mapa nem para os setores, então a coluna some
    $('.pn-main').scrollTop = 0;
    fechaDetalhe();
    if (id === 'mapa') montaMapa();
    if (id === 'setores') montaSetores();
    if (id === 'tempo') montaTempo();
    if (id === 'mudancas') montaMudancas();
    if (id === 'revisao') montaRevisao();
    history.replaceState(null, '', '#' + id);
    deslizaTudo();
    var vista = $('#v-' + id); if (vista) { vista.classList.remove('entra'); void vista.offsetWidth; vista.classList.add('entra'); }
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
    $('#pn-total').innerHTML = '<b>' + fmt(atual.length) + '</b> de ' + fmt(D.normas.length) + ' normas';
    var lista = $('#pn-lista');
    if ($('#v-normas').classList.contains('ativa')) $('.pn-main').scrollTop = 0;
    if (!atual.length) { lista.innerHTML = '<li class="pn-vazio">Nenhuma norma com esses filtros. A busca aceita número (9001, 14064-1), palavra do título em inglês ou comitê (TC 207).</li>'; return; }
    lista.innerHTML = ''; maisLinhas(); entra(lista);
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
    det.innerHTML = '<button class="fechar" aria-label="Fechar"><svg viewBox="0 0 24 24" fill="none"><path d="M5 5l14 14M19 5L5 19"/></svg></button>' +
      '<span class="m">' + esc(TIPOS[n.tipo] || n.tipo) + (n.ed ? ' · edição ' + n.ed : '') + '</span>' +
      '<div class="ref">' + esc(n.ref) + '</div><h2>' + esc(n.titulo) + '</h2>' +
      '<p class="tema">' + esc(D.temasMap[n.tema]) + ' · ' + esc(n.comite) + (n.tcnome ? ', ' + esc(n.tcnome) : '') + '</p>' +
      '<div class="pn-sec"><span class="m">Estágio atual · código ' + n.est + '</span><p><b>' + f[1] + '.</b> ' + f[3] + '</p>' + trilha + '</div>' +
      (n.escopo ? '<div class="pn-sec"><span class="m">Do que trata (escopo, texto da ISO)</span><p>' + esc(n.escopo).replace(/\s*\n+\s*/g, '</p><p>') + (n.escopo.length >= 900 ? ' […]' : '') + '</p></div>' : '') +
      '<div class="pn-sec"><span class="m">Ficha</span><dl class="pn-kv">' +
      (n.pub ? '<dt>Publicação</dt><dd>' + dataBR(n.pub) + '</dd>' : '') +
      (n.pag ? '<dt>Páginas</dt><dd>' + n.pag + '</dd>' : '') +
      '<dt>Comitê ISO</dt><dd>' + esc(n.comite) + (n.tcnome ? ' · ' + esc(n.tcnome) : '') + '</dd>' +
      (n.abnt ? '<dt>Espelho ABNT</dt><dd>' + esc(n.abnt) + '</dd>' : '') +
      (n.ics ? '<dt>ICS</dt><dd>' + n.ics.join(' · ') + '</dd>' : '') +
      (irmas.length ? '<dt>Outras edições e projetos</dt><dd>' + irmas.map(function (x) { return '<a href="#n' + x.id + '" data-id="' + x.id + '">' + esc(x.ref) + '</a> <span class="m" style="font-size:10px">' + FASES[FASE_IDX[x.fase]][1] + '</span>'; }).join('<br>') + '</dd>' : '') +
      (sv ? '<dt>Certificados</dt><dd>' + fmt(sv.total) + ' no mundo' + (sv.paises.BR ? ', ' + fmt(sv.paises.BR) + ' no Brasil' : '') + ' <span class="m" style="font-size:10px">ISO Survey 2025</span> · <a href="#mapa" data-mapa="' + n.num + '">ver no mapa</a></dd>' : '') +
      '</dl></div>' +
      (mud.length ? '<div class="pn-sec"><span class="m">Movimentos registrados neste painel</span><p>' + mud.map(function (m) { return dataBR(m.data) + ': ' + (m.tipo === 'nova' ? 'entrou na base' : m.tipo === 'saiu' ? 'saiu da base' : 'estágio ' + m.de + ' para ' + m.para); }).join('<br>') + '</p></div>' : '') +
      '<div class="pn-sec"><span class="m">Links</span><div class="pn-links">' +
      '<a href="https://www.iso.org/standard/' + n.id + '.html" target="_blank" rel="noopener">Página da norma na ISO <span class="m">iso.org</span></a>' +
      (n.tcid ? '<a href="https://www.iso.org/committee/' + n.tcid + '.html" target="_blank" rel="noopener">Comitê ' + esc(n.comite) + ' <span class="m">iso.org</span></a>' : '') +
      (n.pagina ? '<a href="' + n.pagina + '">Serviço da Ideal Metrics nesta norma <span class="m">neste site</span></a>' : '') +
      '<a href="contato.html">Contato com a equipe técnica <span class="m">Ideal Metrics</span></a>' +
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
    if (/^#n\d+/.test(location.hash)) history.replaceState(null, '', location.pathname);
  }

  /* ---------- linha do tempo ---------- */
  function montaTempo() {
    var A0 = 1985, A1 = 2028, span = A1 - A0;
    var px = function (d) { var y = +String(d).slice(0, 4), m = +(String(d).slice(5, 7) || 6); return ((y + (m - 1) / 12 - A0) / span * 100); };
    var anos = ''; for (var a = 1990; a <= 2025; a += 5) anos += '<span style="left:' + px(a) + '%">' + a + '</span>';
    $('#lt-anos').innerHTML = anos;
    var hist = {}; (D.historico || []).forEach(function (h) { (hist[h.num] = hist[h.num] || []).push(h); });
    var chaves = CHAVE.filter(function (k) { return D.porNum[k] && D.porNum[k].some(function (x) { return passa(x, true); }); });
    if (!chaves.length) { $('#lt-corpo').innerHTML = '<p class="pn-vazio">Nenhuma norma-chave com esses filtros.</p>'; return; }
    $('#lt-corpo').innerHTML = chaves.map(function (k) {
      var xs = D.porNum[k].slice().sort(function (a, b) { return String(a.pub || '9999').localeCompare(String(b.pub || '9999')); });
      var atual = xs.filter(function (x) { return x.fase === 'publicada' || x.fase === 'revisao'; }).pop();
      var nome = (atual || xs[0]).titulo.split(/ [—–-] /)[0];
      var antigas = (hist[k] || []).map(function (h) {
        return '<span class="lt-ed ant" style="left:' + px(h.pub) + '%" title="' + esc(h.ref) + ' · edição retirada"><span class="r">' + h.pub.slice(0, 4) + '</span></span>';
      }).join('');
      var marcas = antigas + xs.map(function (x) {
        if (x.pub) return '<span class="lt-ed' + (x === atual ? '' : ' ant') + '" style="left:' + px(x.pub) + '%" data-id="' + x.id + '" title="' + esc(x.ref) + '"><span class="r">' + x.pub.slice(0, 4) + '</span></span>';
        return '<span class="lt-ed dev" style="left:' + px(D.gerado) + '%" data-id="' + x.id + '" title="' + esc(x.ref) + ' · em desenvolvimento"><span class="r">' + esc(x.ref.replace(/^ISO(\/IEC)?\s*/, '')) + '</span></span>';
      }).join('');
      return '<div class="lt-linha"><div class="lt-nome"><b>ISO ' + k + '</b>' + esc(nome) + '</div><div class="lt-faixa" style="--lt-passo:' + (500 / span) + '%">' + marcas + '</div></div>';
    }).join('');
    entra($('#lt-corpo'));
  }

  /* ---------- mudanças ---------- */
  function montaMudancas() {
    var el = $('#md-corpo'), it = (MUD.itens || []).slice().sort(function (a, b) { return b.data.localeCompare(a.data) || a.ref.localeCompare(b.ref); });
    var desde = dataBR((MUD.desde || D.gerado)), todos = semFiltro();
    var achaN = function (id) { for (var i = 0; i < D.normas.length; i++) if (D.normas[i].id === id) return D.normas[i]; return null; };
    var total = it.length;
    // norma que saiu da base não tem mais ficha: só aparece quando nenhum filtro está ligado
    it = it.filter(function (m) { var n = achaN(m.id); return n ? passa(n, true) : todos; });
    if (total && !it.length) { el.innerHTML = '<p class="pn-vazio">Nenhum movimento com esses filtros.</p>'; return; }
    if (!it.length) {
      el.innerHTML = '<p class="pn-vazio">Nenhuma mudança de estágio registrada desde ' + desde + '. A base da ISO é comparada toda semana; o que entrar, avançar de estágio ou for publicado aparece aqui.</p>';
      return;
    }
    var grupos = {}; it.forEach(function (m) { (grupos[m.data] = grupos[m.data] || []).push(m); });
    el.innerHTML = Object.keys(grupos).sort().reverse().map(function (d) {
      return '<div class="md-grupo"><span class="m">' + dataBR(d) + ' · ' + grupos[d].length + ' movimento(s)</span>' + grupos[d].map(function (m) {
        var o = m.tipo === 'nova' ? 'entrou na base · ' + m.para : m.tipo === 'saiu' ? 'saiu da base' : m.de + ' → ' + m.para;
        var n = D.normas.filter(function (x) { return x.id === m.id; })[0];
        return '<div class="md-item" data-id="' + m.id + '"><span class="ref">' + esc(m.ref) + '</span><span>' + esc(n ? n.titulo : '') + '</span><span class="de">' + esc(o) + ' · ' + (FASES[FASE_IDX[m.fase]] || [])[1] + '</span></div>';
      }).join('') + '</div>';
    }).join('');
    entra(el);
  }

  /* ---------- revisão sistemática ---------- */
  function montaRevisao() {
    var todas = D.normas.filter(function (n) { return n.fase === 'revisao'; });
    var xs = todas.filter(function (n) { return passa(n); }).sort(function (a, b) { return a.num.localeCompare(b.num, undefined, { numeric: true }); });
    $('#rv-total').innerHTML = '<b>' + xs.length + '</b>' + (xs.length < todas.length ? ' de ' + todas.length : '') + ' normas em revisão sistemática';
    if (!xs.length) { $('#rv-corpo').innerHTML = '<li class="pn-vazio">Nenhuma norma em revisão sistemática com esses filtros.</li>'; return; }
    $('#rv-corpo').innerHTML = xs.map(function (n) {
      var proj = (D.porNum[n.num] || []).filter(function (x) { return x.id !== n.id && !x.pub; });
      return '<li class="pn-item" data-id="' + n.id + '"><span class="ref">' + esc(n.ref) + '</span><span class="tit">' + esc(n.titulo) + '<small>' + esc(D.temasMap[n.tema]) + ' · ' + esc(n.comite) + (proj.length ? ' · projeto de nova edição em curso: ' + esc(proj[0].ref) : '') + '</small></span>' +
        '<span class="fase">' + barraEst(n) + '<span>código ' + n.est + '</span></span><span class="seta"><svg viewBox="0 0 24 24"><path d="M5 12h14M13 6l6 6-6 6"/></svg></span></li>';
    }).join('');
    entra($('#rv-corpo'));
  }

  /* ---------- certificados por setor (27/10/2026) ---------- */
  /* 39 setores EA (índice 0 a 38) agrupados nos setores que a Ideal Metrics atende; a ilustração é a da brochura (coleção C) */
  var GRUPOS = [
    { id: 'industria', nome: 'Indústria', ea: [1, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23] },
    { id: 'facilities', nome: 'Construção e facilities', ea: [27] },
    { id: 'comercio', nome: 'Comércio e serviços', ea: [28, 29, 31, 34], sem: true },
    { id: 'tecnologia', nome: 'Tecnologia e engenharia', ea: [32, 33] },
    { id: 'transporte', nome: 'Transporte e logística', ea: [30] },
    { id: 'saude', nome: 'Saúde', ea: [37] },
    { id: 'energia', nome: 'Energia e saneamento', ea: [24, 25, 26] },
    { id: 'alimentos', nome: 'Alimentos e bebidas', ea: [2] },
    { id: 'publico', nome: 'Setor público e educação', ea: [35, 36, 38] },
    { id: 'agro', nome: 'Agro', ea: [0] }
  ];
  var EA_PT = ['Agricultura, pesca e florestas', 'Mineração', 'Alimentos, bebidas e tabaco', 'Têxteis', 'Couro', 'Madeira', 'Celulose e papel', 'Editoras', 'Gráficas', 'Coque e refino de petróleo', 'Combustível nuclear', 'Químicos e fibras', 'Farmacêuticos', 'Borracha e plástico', 'Minerais não metálicos', 'Concreto, cimento, cal e gesso', 'Metalurgia e produtos de metal', 'Máquinas e equipamentos', 'Equipamentos elétricos e ópticos', 'Construção naval', 'Aeroespacial', 'Outros equipamentos de transporte', 'Outras indústrias', 'Reciclagem', 'Energia elétrica', 'Gás', 'Água', 'Construção', 'Comércio e reparação de veículos', 'Hotéis e restaurantes', 'Transporte, armazenagem e comunicação', 'Finanças, imóveis e aluguel', 'Tecnologia da informação', 'Serviços de engenharia', 'Outros serviços', 'Administração pública', 'Educação', 'Saúde e assistência social', 'Outros serviços sociais'];
  var stFeito = false, stNum = '9001', stOnde = 'mundo';
  function montaSetores() {
    if (stFeito) return; stFeito = true;
    var S = D.setores; if (!S || !S.normas) { $('#st-grade').innerHTML = '<p class="pn-vazio">Sem dados de setor nesta base.</p>'; return; }
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
    $('#st-total').textContent = fmt(total) + ' certificados com setor informado · ' + (SURVEY_NOME[stNum] || 'ISO ' + stNum) + ' · ' + (stOnde === 'br' ? 'Brasil' : 'mundo');
    $('#st-grade').innerHTML = grupos.map(function (x) {
      var g = x.g, pct = total ? (x.soma / total * 100) : 0;
      var ea = g.ea.map(function (i) { return { i: i, v: v[i] }; }).sort(function (a, b) { return b.v - a.v; });
      return '<article class="st-card entra">' + (g.sem ? '<div class="st-sem"></div>' : '<img class="st-ilus" src="img/setores/setor-' + g.id + '.webp" alt="" loading="lazy">') +
        '<h3>' + g.nome + '</h3><div class="st-n"><b>' + fmt(x.soma) + '</b><span class="m">' + pct.toFixed(1).replace('.', ',') + '% · ' + ea.length + (ea.length > 1 ? ' setores EA' : ' setor EA') + '</span></div>' +
        '<div class="st-barra"><i style="width:' + (x.soma / max * 100) + '%"></i></div>' +
        '<ul class="st-ea">' + ea.slice(0, 6).map(function (e) { return '<li' + (e.v ? '' : ' class="zero"') + '><span title="' + esc(S.setores[e.i]) + '">' + esc(EA_PT[e.i] || S.setores[e.i]) + '</span><b>' + fmt(e.v) + '</b></li>'; }).join('') +
        (ea.length > 6 ? '<li><span class="m">+ ' + (ea.length - 6) + ' setores EA</span><b>' + fmt(ea.slice(6).reduce(function (a, e) { return a + e.v; }, 0)) + '</b></li>' : '') + '</ul></article>';
    }).join('');
    entra($('#st-grade'));
  }

  /* ---------- mapa ---------- */
  var mapaFeito = false, mapaNum = '9001', paths = null, dica = null, refazPulsos = null;
  function escolheSurvey(num) { mapaNum = num; $$('.mp-sel button').forEach(function (b) { b.setAttribute('aria-pressed', b.dataset.num === num); }); desliza($('#mp-sel'), '[aria-pressed=true]'); pintaMapa(); }
  function montaMapa() {
    if (mapaFeito) return; mapaFeito = true;
    var nums = Object.keys(D.survey).sort(function (a, b) { return D.survey[b].total - D.survey[a].total; });
    $('#mp-sel').innerHTML = nums.map(function (k) { var nm = SURVEY_NOME[k] || 'ISO ' + k; return '<button data-num="' + k + '" aria-pressed="' + (k === mapaNum) + '"' + (nm.length > 13 ? ' class="longo"' : '') + '>' + nm + '</button>'; }).join('');
    $$('.mp-sel button').forEach(function (b) { b.addEventListener('click', function () { escolheSurvey(b.dataset.num); }); });
    var box = $('#mp-mapa'); dica = $('#mp-dica');
    if (!window.d3 || !window.topojson) { box.innerHTML = '<p class="pn-vazio" style="padding:20px">O mapa precisa das bibliotecas d3 e topojson, que não carregaram. A tabela ao lado continua válida.</p>'; pintaLado(); return; }
    fetch('dados/mundo-110m.json').then(function (r) { return r.json(); }).then(function (topo) {
      MUNDO = topojson.feature(topo, topo.objects.countries);
      var porNumFeat = {}; Object.keys(D.paises).forEach(function (a2) { if (D.paises[a2].n) porNumFeat[D.paises[a2].n] = a2; });
      /* 27/10: globo que gira e se desenrola em mapa (projeção ortográfica interpolada com a Natural Earth) */
      var W = 960, H = 480, ESC_MAPA = d3.geoNaturalEarth1().fitExtent([[6, 6], [W - 6, H - 6]], { type: 'Sphere' }).scale(), ESC_GLOBO = H / 2 - 8;
      var GIRO_BR = [52, 12], giro = GIRO_BR.slice(), prog = 0, anima = false, arrasta = null, sobre = false;
      var muta = d3.geoProjectionMutator(function (t) { return function (x, y) { var a = d3.geoOrthographicRaw(x, y), b = d3.geoNaturalEarth1Raw(x, y); return [a[0] + t * (b[0] - a[0]), a[1] + t * (b[1] - a[1])]; }; });
      var proj = muta(0).translate([W / 2, H / 2]).precision(.5), geo = d3.geoPath(proj);
      var svg = d3.select(box).insert('svg', ':first-child').attr('viewBox', '0 0 ' + W + ' ' + H).attr('role', 'img').attr('aria-label', 'Globo de certificados por país');
      /* 27/10: oceano de vidro, no mesmo tom da placa onde o globo está (só um brilho claro no alto à esquerda); mais transparente desde o 2º ajuste */
      var brilho = svg.append('defs').append('radialGradient').attr('id', 'mp-vidro').attr('cx', '32%').attr('cy', '26%').attr('r', '78%');
      /* 27/10, 3º: oceano branco a ~78% (mais claro que o #F2F1F5 da legenda, e o globo fica 20% menos transparente) */
      brilho.append('stop').attr('offset', '0').attr('stop-color', '#fff').attr('stop-opacity', .86);
      brilho.append('stop').attr('offset', '.55').attr('stop-color', '#fff').attr('stop-opacity', .78);
      brilho.append('stop').attr('offset', '1').attr('stop-color', '#fff').attr('stop-opacity', .74);
      /* 27/10: «se a bola do globo ficasse ligeiramente transparente»: os países do lado de trás aparecem apagados através do
         globo. Lado de trás = ortográfica centrada no antípoda e espelhada (mesma posição de tela de quem olha através da bola) */
      var esfera = svg.append('path').attr('class', 'esfera').attr('fill', 'url(#mp-vidro)').attr('stroke', 'rgba(255,255,255,.9)').attr('stroke-width', 1.2);
      var tras = svg.append('g').attr('class', 'tras').selectAll('path').data(MUNDO.features.filter(function (f) { return f.id !== '010'; })).enter().append('path');   // sobre o oceano, para aparecer através dele
      var grade = svg.append('path').datum(d3.geoGraticule10()).attr('class', 'grade');
      paths = svg.append('g').selectAll('path').data(MUNDO.features.filter(function (f) { return f.id !== '010'; })).enter().append('path').attr('class', 'pais');
      /* 27/10: «nos principais países, com pulso animado, fosse mostrando os números conforme o globo gira»: os oito maiores da
         norma (e o Brasil) ganham um anel que pulsa e o número, no centro do país, só enquanto estão no hemisfério da frente */
      var gPulsos = svg.append('g').attr('class', 'pulsos'), centro = {};
      MUNDO.features.forEach(function (f) { var a2 = porNumFeat[f.id]; if (a2) centro[a2] = d3.geoCentroid(f); });
      refazPulsos = function () {
        var s = D.survey[mapaNum]; if (!s) return;
        var top = Object.keys(s.paises).filter(function (a) { return centro[a]; }).sort(function (a, b) { return s.paises[b] - s.paises[a]; }).slice(0, 8);
        if (s.paises.BR && centro.BR && top.indexOf('BR') < 0) top.push('BR');
        var g = gPulsos.selectAll('g.pulso').data(top.map(function (a) { return { a2: a, c: centro[a], v: s.paises[a] }; }), function (d) { return d.a2; });
        g.exit().remove();
        var e = g.enter().append('g').attr('class', 'pulso');
        e.append('circle').attr('class', 'anel').attr('r', 7).style('animation-delay', function (d, i) { return (i * .27) + 's'; });
        e.append('circle').attr('class', 'ponto').attr('r', 2.2);
        e.append('text').attr('x', 10).attr('y', 4);
        gPulsos.selectAll('g.pulso text').text(function (d) { return fmt(d.v); });
        poePulsos();
      };
      function poePulsos() {
        var a = Math.sqrt(Math.max(0, Math.min(1, prog))), olho = [-giro[0], -giro[1]];
        gPulsos.selectAll('g.pulso').each(function (d) {
          var vis = a > .98 || d3.geoDistance(d.c, olho) < 1.42, p = proj(d.c);
          d3.select(this).style('display', vis && p ? null : 'none').attr('transform', p ? 'translate(' + p[0].toFixed(1) + ',' + p[1].toFixed(1) + ')' : null);
        });
      }
      function desenha() {
        var a = Math.sqrt(Math.max(0, Math.min(1, prog)));
        proj = muta(a).scale(ESC_GLOBO + a * (ESC_MAPA - ESC_GLOBO)).translate([W / 2, H / 2]).rotate(giro).precision(.5);
        var raio = (90 + a * 89) * Math.PI / 180;   // corte em círculo que cresce até quase o antípoda, encadeado com o corte no antimeridiano (sem ele os países cortados viram faixas no meio da transição)
        proj.preclip(a < .999 ? function (s) { return d3.geoClipCircle(raio)(d3.geoClipAntimeridian(s)); } : d3.geoClipAntimeridian);
        geo = d3.geoPath(proj);
        esfera.attr('d', geo({ type: 'Sphere' })); grade.attr('d', geo); paths.attr('d', geo);
        if (a < .02) {
          var pt = d3.geoOrthographic().scale(ESC_GLOBO).translate([W / 2, H / 2]).rotate([giro[0] + 180, -giro[1]]).reflectX(true).precision(.5);
          tras.attr('d', d3.geoPath(pt)).style('display', null);
        } else tras.style('display', 'none');
        poePulsos();
      }
      var calmo = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches, ult = 0;
      function gira(t) {
        if (prog === 0 && !anima && !arrasta && !sobre && !document.hidden && $('#v-mapa').classList.contains('ativa')) { giro[0] += Math.min(t - ult, 50) * .009; desenha(); }
        ult = t; if (!calmo) requestAnimationFrame(gira);
      }
      var bt = d3.select(box).append('div').attr('class', 'mp-ctl'), btVira = bt.append('button').attr('type', 'button').text('Abrir em mapa'), btCentro = bt.append('button').attr('type', 'button').text('Centralizar');
      function lonPerto(de, para) { return para + Math.round((de - para) / 360) * 360; }
      btVira.on('click', function () {
        if (anima) return; anima = true; btVira.property('disabled', true);
        var p0 = prog, p1 = prog < .5 ? 1 : 0, g0 = giro.slice(), g1 = p1 ? [lonPerto(giro[0], 0), 0] : [lonPerto(giro[0], GIRO_BR[0]), GIRO_BR[1]], t0 = performance.now(), dur = calmo ? 1 : 1600;
        (function passo(t) {
          var k = Math.min((t - t0) / dur, 1), e = d3.easeCubicInOut(k);
          prog = p0 + (p1 - p0) * e; giro = [g0[0] + (g1[0] - g0[0]) * e, g0[1] + (g1[1] - g0[1]) * e]; desenha();
          if (k < 1) return requestAnimationFrame(passo);
          prog = p1; anima = false; btVira.property('disabled', false).text(p1 ? 'Voltar ao globo' : 'Abrir em mapa');
          svg.classed('plano', !!p1).attr('aria-label', p1 ? 'Mapa de certificados por país' : 'Globo de certificados por país');
        })(t0);
      });
      btCentro.on('click', function () { if (!anima && prog === 0) { giro = GIRO_BR.slice(); desenha(); } });
      svg.on('pointerdown', function (ev) { if (prog > 0 || anima) return; arrasta = [ev.clientX, ev.clientY]; svg.classed('arrastando', true); });
      window.addEventListener('pointermove', function (ev) {
        if (!arrasta) return; var k = 300 / box.getBoundingClientRect().width;
        giro[0] += (ev.clientX - arrasta[0]) * k; giro[1] = Math.max(-80, Math.min(80, giro[1] - (ev.clientY - arrasta[1]) * k));
        arrasta = [ev.clientX, ev.clientY]; desenha();
      });
      window.addEventListener('pointerup', function () { arrasta = null; svg.classed('arrastando', false); });
      svg.on('pointermove', function (ev) {   // 27/10: para de girar só com o mouse sobre o globo, não em qualquer lugar da área
        var r = this.getBoundingClientRect(), x = (ev.clientX - r.left) * W / r.width - W / 2, y = (ev.clientY - r.top) * H / r.height - H / 2;
        sobre = x * x + y * y <= ESC_GLOBO * ESC_GLOBO;
      }).on('pointerleave', function () { sobre = false; });
      desenha(); requestAnimationFrame(function (t) { ult = t; gira(t); });
      var porNum = porNumFeat;
      paths.on('mousemove', function (ev, f) {
        var a2 = porNum[f.id], v = a2 && D.survey[mapaNum].paises[a2];
        dica.style.display = 'block'; var r = box.getBoundingClientRect();
        dica.style.left = (ev.clientX - r.left) + 'px'; dica.style.top = (ev.clientY - r.top) + 'px';
        dica.innerHTML = esc(a2 ? nomePais(a2) : f.properties.name) + (v ? ' · <b>' + fmt(v) + '</b>' : ' · sem certificado registrado');
      }).on('mouseleave', function () { dica.style.display = 'none'; });
      WORLD_OK = true; pintaMapa();
    });
  }
  var CORES = ['#F2F1F5', '#D3E2F2', '#9FC5F0', '#6A9CC9', '#336699', '#14304C'];
  function pintaMapa() {
    var s = D.survey[mapaNum]; if (!s) return;
    var porNum = {}; Object.keys(D.paises).forEach(function (a2) { if (D.paises[a2].n) porNum[D.paises[a2].n] = a2; });
    var cortes = [1, 10, 100, 1000, 10000];
    var cor = function (v) { if (!v) return CORES[0]; for (var i = cortes.length - 1; i >= 0; i--) if (v >= cortes[i]) return CORES[i + 1]; return CORES[1]; };
    if (paths) paths.transition().duration(400).attr('fill', function (f) { var a2 = porNum[f.id]; return cor(a2 ? s.paises[a2] : 0); });
    if (refazPulsos) refazPulsos();
    $('#mp-esc').innerHTML = '<span style="margin-left:0">certificados</span>' + ['0', '1', '10', '100', '1 mil', '10 mil+'].map(function (t, i) { return '<i style="background:' + CORES[i] + '"></i><span>' + t + '</span>'; }).join('');
    pintaLado();
  }
  function pintaLado() {
    var s = D.survey[mapaNum], nome = SURVEY_NOME[mapaNum] || 'ISO ' + mapaNum;
    var rank = Object.keys(s.paises).sort(function (a, b) { return s.paises[b] - s.paises[a]; });
    var posBR = rank.indexOf('BR') + 1, latam = rank.filter(function (a) { return LATAM.indexOf(a) >= 0; }), posLA = latam.indexOf('BR') + 1;
    var max = s.paises[rank[0]];
    var top = rank.slice(0, 10); if (posBR > 10) top.push('BR');
    $('#mp-lado').innerHTML = '<h3>' + esc(nome) + '</h3><div class="m">' + esc(s.titulo || '') + '</div>' +
      '<div class="tot">' + fmt(s.total) + '<small>certificados válidos em 31-dez-2025 · ' + rank.length + ' países</small></div>' +
      (posBR ? '<div class="mp-br"><span class="m">Brasil</span><div class="v">' + fmt(s.paises.BR) + '<small>' + posBR + 'º no mundo · ' + posLA + 'º na América Latina</small></div></div>' : '<div class="mp-br"><span class="m">Brasil</span><div class="v">0</div></div>') +
      '<ul class="mp-rank">' + top.map(function (a) { var p = rank.indexOf(a) + 1; return '<li' + (a === 'BR' ? ' class="br"' : '') + '><span class="m">' + p + '</span><span><img class="bandeira" src="https://cdn.jsdelivr.net/npm/flag-icons@7.2.3/flags/4x3/' + a.toLowerCase() + '.svg" alt="" loading="lazy" onerror="this.remove()">' + esc(nomePais(a)) + '</span><b>' + fmt(s.paises[a]) + '</b><span class="barra"><i style="width:' + (s.paises[a] / max * 100) + '%"></i></span></li>'; }).join('') + '</ul>' +
      '<p class="mp-nota">Só certificados emitidos por organismos acreditados por membros do IAF. Países sem certificado acreditado não aparecem. Fonte: ISO Survey 2025.</p>';
    entra($('#mp-lado .mp-rank'));
  }
})();
