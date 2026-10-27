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
    fetch('dados/painel-normas.json').then(function (r) { return r.json(); }),
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

  function mostraAba(id) {
    if (!$('#v-' + id)) return;
    $$('.pn-abas button').forEach(function (b) { b.setAttribute('aria-selected', b.dataset.aba === id); });
    $$('.pn-vista').forEach(function (v) { v.classList.toggle('ativa', v.id === 'v-' + id); });
    $('.pn-main').scrollTop = 0;
    fechaDetalhe();
    if (id === 'mapa') montaMapa();
    if (id === 'tempo') montaTempo();
    if (id === 'mudancas') montaMudancas();
    if (id === 'revisao') montaRevisao();
    history.replaceState(null, '', '#' + id);
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
    lista.innerHTML = ''; maisLinhas();
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
  }

  /* ---------- mapa ---------- */
  var mapaFeito = false, mapaNum = '9001', paths = null, dica = null;
  function escolheSurvey(num) { mapaNum = num; $$('.mp-sel button').forEach(function (b) { b.setAttribute('aria-pressed', b.dataset.num === num); }); pintaMapa(); }
  function montaMapa() {
    if (mapaFeito) return; mapaFeito = true;
    var nums = Object.keys(D.survey).sort(function (a, b) { return D.survey[b].total - D.survey[a].total; });
    $('#mp-sel').innerHTML = nums.map(function (k) { return '<button data-num="' + k + '" aria-pressed="' + (k === mapaNum) + '">' + (SURVEY_NOME[k] || 'ISO ' + k) + '</button>'; }).join('');
    $$('.mp-sel button').forEach(function (b) { b.addEventListener('click', function () { escolheSurvey(b.dataset.num); }); });
    var box = $('#mp-mapa'); dica = $('#mp-dica');
    if (!window.d3 || !window.topojson) { box.innerHTML = '<p class="pn-vazio" style="padding:20px">O mapa precisa das bibliotecas d3 e topojson, que não carregaram. A tabela ao lado continua válida.</p>'; pintaLado(); return; }
    fetch('dados/mundo-110m.json').then(function (r) { return r.json(); }).then(function (topo) {
      MUNDO = topojson.feature(topo, topo.objects.countries);
      var W = 960, H = 480, proj = d3.geoNaturalEarth1().fitExtent([[6, 6], [W - 6, H - 6]], { type: 'Sphere' }), geo = d3.geoPath(proj);
      var svg = d3.select(box).insert('svg', ':first-child').attr('viewBox', '0 0 ' + W + ' ' + H).attr('role', 'img').attr('aria-label', 'Mapa de certificados por país');
      svg.append('path').attr('d', geo({ type: 'Sphere' })).attr('fill', '#FAF9F5').attr('stroke', 'rgba(20,48,76,.3)').attr('stroke-width', .6);
      paths = svg.append('g').selectAll('path').data(MUNDO.features.filter(function (f) { return f.id !== '010'; })).enter().append('path').attr('class', 'pais').attr('d', geo);
      var porNum = {}; Object.keys(D.paises).forEach(function (a2) { if (D.paises[a2].n) porNum[D.paises[a2].n] = a2; });
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
      '<ul class="mp-rank">' + top.map(function (a) { var p = rank.indexOf(a) + 1; return '<li' + (a === 'BR' ? ' class="br"' : '') + '><span class="m">' + p + '</span><span>' + esc(nomePais(a)) + '</span><b>' + fmt(s.paises[a]) + '</b><span class="barra"><i style="width:' + (s.paises[a] / max * 100) + '%"></i></span></li>'; }).join('') + '</ul>' +
      '<p class="mp-nota">Só certificados emitidos por organismos acreditados por membros do IAF. Países sem certificado acreditado não aparecem. Fonte: ISO Survey 2025.</p>';
  }
})();
