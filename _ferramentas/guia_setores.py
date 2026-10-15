# -*- coding: utf-8 -*-
"""O bloco dos setores da secao Guia da home: SANFONA no estilo da tabela «Nossos servicos» (14/10/2026), com o titulo
e o fluxo da secao presos na metade esquerda enquanto a sanfona sobe a direita (15/10/2026).

    python _ferramentas/guia_setores.py            grava a sanfona dos setores entre <!-- foco --> e <!-- fim foco -->
    python _ferramentas/guia_setores.py cartoes    volta o bloco dos cartoes (3x3 com a foto presa), guardado em
                                                   _ferramentas/guia_bloco_cartoes.html

Historia (14/10/2026): «nao estou satisfeito com esta secao; ja temos a divisao, e ja temos a foto, sugira outros
esquemas»; das 14 maquetes (A a N), as propostas H (lista com as normas em etiquetas) e I (fios setor -> norma) foram
para o site em teste (commits 7a49a20 e 0a72b50) e sairam no mesmo dia: «acho que gostei mais estilo esta tabela que
ja existe, tire as outras, monte aqui», apontando a sanfona da secao Servicos.

A SANFONA usa as MESMAS classes da de Servicos (.sv-line, .sv-title, .sv-list, .sv-acc, .sv-item, .sv-panel, .sv-foto,
.sv-texto, .sv-desc, .sv-more), entao herda tudo dela: o + que gira para x, o painel que abre em .5 s, a foto do setor
a esquerda no motor da trama (que so liga com o item aberto), o zoom da foto no mouse, o «[ Detalhes -> ]» com a letra
embaralhando. «Igual» e o comportamento inteiro (regra do site). O primeiro item nasce aberto, como la. No painel: o
resumo do setor e, embaixo, as normas proprias dele, no mesmo mono; o «Detalhes» leva a pagina do setor.
Duas mudancas no index.html que valem para as duas sanfonas (feitas aqui, de forma idempotente):
  - o script da sanfona fechava TODOS os .sv-item da pagina; agora fecha so os irmaos da mesma sanfona;
  - o motor das fotos da sanfona (perto()) passa a ler o data-tom da foto, para as fotos com tom proprio.

As normas de cada setor vem de js/setores-dados.js (o setores.py), sem as que valem para qualquer setor (ISO 9001, 14001
e 45001) e sem as que sairam do site (SA 8000, ISO 39002)."""

import json, os, re, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(AQUI)
GUARDA = os.path.join(AQUI, 'guia_bloco_cartoes.html')
FORA = {'SA 8000', 'ISO 39002'}
TRANSV = {'ISO 9001', 'ISO 14001', 'ISO 45001'}

# as nove fotos do bloco antigo (src, data-lum, data-tom) e as rubricas, na ordem dos setores
FOTOS = [
    ('img/logistica-bayer-st.webp?v=25092026', 'img/logistica-lum-st.webp?v=25092026', None, 'Manufatura'),
    ('img/transporte-bayer-st.webp?v=12102026', 'img/transporte-lum-st.webp?v=12102026', None, 'Mobilidade'),
    ('img/facilities-02-bayer-gs.webp?v=14102026', 'img/facilities-02-lum-gs.webp?v=14102026',
     '{"brilhoTom":0.36,"gama":0.8,"ctr":1.9,"escuro":1.3,"limiar":-0.05,"veu":0.07,"cores":["#14304C","#336699","#D3E2F2","#FAF9F5"]}', 'Predial'),
    ('img/alimentos-01-bayer-gs.webp?v=13102026', 'img/alimentos-01-lum-gs.webp?v=13102026', None, 'Alimentício'),
    ('img/agro-02-bayer-gs.webp?v=13102026', 'img/agro-02-lum-gs.webp?v=13102026', None, 'Agroflorestal'),
    ('img/saude-03-bayer-gs.webp?v=14102026', 'img/saude-03-lum-gs.webp?v=14102026',
     '{"brilhoTom":0.34,"gama":0.81,"ctr":1.85,"escuro":1.6,"limiar":0,"veu":0.07,"cores":["#14304C","#336699","#D3E2F2","#FAF9F5"]}', 'Hospitalar'),
    ('img/energia-01-bayer-gs.webp?v=13102026', 'img/energia-01-lum-gs.webp?v=13102026',
     '{"brilhoTom":0.09,"gama":1.13,"ctr":1.7,"escuro":0.4,"limiar":0.03,"veu":0.19,"cores":["#14304C","#336699","#D3E2F2","#FAF9F5"]}', 'Energético'),
    ('img/tecnologia-02-bayer-gs.webp?v=13102026', 'img/tecnologia-02-lum-gs.webp?v=13102026',
     '{"brilhoTom":0.21,"gama":0.81,"ctr":1.9,"escuro":1.7,"limiar":0,"veu":0.08,"cores":["#153351","#183858","#6792BD","#FAF9F5"]}', 'Digital'),
    ('img/servicos-03-bayer-gs.webp?v=13102026', 'img/servicos-03-lum-gs.webp?v=13102026',
     '{"brilhoTom":0.27,"gama":0.86,"ctr":1.7,"escuro":1,"limiar":0,"veu":0.1,"cores":["#153351","#183858","#6792BD","#FAF9F5"]}', 'Serviços'),
]

TITULO = ('O portfólio da Ideal Metrics se organiza em três entradas: o setor da organização, o tema de gestão e a norma '
          'ou padrão a atender.')
FLUXO = ('<div class="mp-fluxo" aria-hidden="true"><span>Setor</span><i></i><span>Tema de gestão</span><i></i>'
         '<span>Norma ou padrão</span><i></i><span>Página do serviço</span></div>')
ROTULO = '<p class="mp-rotulo"><span>Por onde começar</span><span>[ GUIA ]</span></p>'
# o cabecalho da secao antes da sanfona (rotulo, titulo e fluxo, como era ate 14/10/2026), para o modo cartoes
CAB_ORIGINAL = ('  <div class="mp-cab">\n    %s\n    <h2 class="mp-titulo" id="mp-titulo">%s</h2>\n  </div>\n  %s\n  '
                % (ROTULO, TITULO, FLUXO))
CAB_SANFONA = '  <div class="mp-cab">\n    %s\n  </div>\n  ' % ROTULO

PLUS = ('<svg class="sv-plus" viewBox="0 0 15 15" aria-hidden="true"><line x1="7.5" y1="0" x2="7.5" y2="15"/>'
        '<line x1="0" y1="7.5" x2="15" y2="7.5"/></svg>')
SETA = '<svg viewBox="0 0 14 10" aria-hidden="true"><path d="M0 5h13M9 1l4 4-4 4"/></svg>'


def esc(t):
    return t.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;')


def setores():
    d = open(os.path.join(SITE, 'js', 'setores-dados.js'), encoding='utf-8').read()
    D = json.loads(d[d.index('{'):d.rindex('}') + 1]); N = D['normas']
    out = []
    for k, s in enumerate(D['setores']):
        ns = [n for n in s['normas'] if n in N and N[n]['nome'] not in FORA and N[n]['nome'] not in TRANSV]
        out.append(dict(n='%02d' % (k + 1), nome=s['nome'], pag=s['pagina'], resumo=s['resumo'], cat=FOTOS[k][3],
                        normas=[N[n]['nome'] for n in ns]))
    assert len(out) == len(FOTOS), 'setores e fotos fora de ordem'
    return out


def sanfona(S):
    # 15/10/2026: «aqui pode travar a parte escrita do lado esquerdo enquanto a parte direita sobe no scroll do mouse»:
    # o titulo e o fluxo vem para a coluna da esquerda da sanfona (.gs-cab, sticky), e a sanfona sobe a direita
    o = ['  <div class="gs" id="guiaSetores">',
         '    <div class="gs-cab">',
         '      <h2 class="mp-titulo" id="mp-titulo">%s</h2>' % TITULO,
         '      ' + FLUXO,
         '    </div>',
         '    <div class="sv-line" aria-hidden="true"></div>',
         '    <div class="sv-title" aria-hidden="true"><div class="sv-title-b">Setores atendidos</div></div>',
         '    <div class="sv-list">',
         '      <div class="sv-acc" role="presentation">']
    for k, s in enumerate(S):
        src, lum, tom, cat = FOTOS[k]
        img = '<img src="%s" data-lum="%s"%s alt="" loading="lazy">' % (src, lum, " data-tom='%s'" % tom if tom else '')
        o += ['',
              '        <div class="sv-item%s">' % (' sv-open' if k == 0 else ''),
              '          <h3 class="sv-item-h"><button type="button" class="sv-item-title" id="gs-btn-%d" aria-expanded="%s" '
              'aria-controls="gs-panel-%d"><span>%s</span>%s</button></h3>' % (k, 'true' if k == 0 else 'false', k, esc(s['nome']), PLUS),
              '          <div class="sv-panel" id="gs-panel-%d" role="region" aria-labelledby="gs-btn-%d">' % (k, k),
              '            <div class="sv-panel-inner">',
              '              <div class="sv-panel-body">',
              '                <figure class="sv-foto">%s</figure>' % img,
              '                <div class="sv-texto">',
              '                <p class="sv-desc">%s</p>' % esc(s['resumo']),
              '                <p class="sv-desc gs-normas">%s</p>' % esc(' · '.join(s['normas'][:5])),
              '                <a class="sv-more" href="%s">[<span class="sv-more-in"><span class="js-scramble">Detalhes</span>%s</span>]</a>' % (s['pag'], SETA),
              '              </div>',
              '              </div>',
              '            </div>',
              '          </div>',
              '        </div>']
    o += ['', '      </div>', '    </div>', '  </div>']
    return '\n'.join(o)


def bloco_n(S):
    """PROPOSTA N em teste (15/10/2026: a L saiu, «nao gostei deste novo, pode tirar, faca esse aqui para eu ver, no
    lugar»): nove itens compactos em tres colunas, cada um com a miniatura da foto, numero e rubrica, nome e normas; no
    mouse o item fica azul e a miniatura liga o motor da trama (um item por vez). Cada item leva a pagina do setor."""
    o = ['  <div class="gn-palco" id="guiaNpalco"><div class="gn-fixo">',
         '  <div class="gx-rot gn-rot"><span>Proposta N · lista com miniaturas</span><span>[ em teste ]</span></div>',
         '  <div class="gn" id="guiaN">']
    for k, s in enumerate(S):
        src, lum, tom, cat = FOTOS[k]
        o.append('    <a class="gn-item" data-ordem="%d" href="%s"><span class="gn-foto" aria-hidden="true"><img src="%s" data-lum="%s"%s alt="" '
                 'loading="lazy"></span><span class="gn-txt"><span class="gn-top">%s · %s</span><span class="gn-nome">%s</span>'
                 '<span class="gn-normas">%s</span></span></a>'
                 % ((k % 3) * 3 + k // 3, s['pag'], src, lum, " data-tom='%s'" % tom if tom else '', s['n'], esc(cat), esc(s['nome']),
                    esc(' · '.join(s['normas'][:3]))))
    o.append('  </div>')
    o.append('  </div></div>')
    o.append(JS_N)
    return '\n'.join(o)


JS_N = r"""  <script>
  /* Guia, proposta N (_ferramentas/guia_setores.py): a miniatura do item sob o mouse liga o motor da trama (um por vez) */
  (function(){
    var raiz = document.getElementById('guiaN'); if(!raiz) return;
    var gl = null, ativo = null, OFICIAL = [[21.2,50.9,80.6],[24.2,56.2,88.1],[103.0,146.1,189.4],[250,249,245]];
    [].slice.call(raiz.querySelectorAll('.gn-item')).forEach(function(it){
      function liga(){
        if(it === ativo || !window.ditherVivo) return; ativo = it;
        if(gl){ try { gl.destruir(); } catch(e){} gl = null; }
        var f = it.querySelector('.gn-foto'), im = f.querySelector('img'), tom = null;
        try { tom = JSON.parse(im.getAttribute('data-tom') || 'null'); } catch(e){}
        gl = window.ditherVivo({brilhoTom:0.35, gama:0.88, ctr:1.55, escuro:0.35, lavaRepouso:0.12, raiz:f,
          planos:[{el:f, lum:im.getAttribute('data-lum'), tom:tom}], classeCanvas:'vv-gl', revelar:'visivel', cores:OFICIAL, pincel:.7, zoomHover:1.06});
      }
      it.addEventListener('mouseenter', liga); it.addEventListener('focus', liga);
    });
  })();
  /* 15/10/2026: «no scroll a primeira fileira fique, depois a segunda, depois a terceira coluna, depois entao a tela
     continua; nao precisa para o contrario, quando estamos subindo» e, corrigido, «uma coluna por vez, nao uma linha
     por vez» e, depois, «faca entrar um card por vez». O bloco fica preso no meio da tela (sticky) e a cada passo de
     rolagem (cerca de um giro da roda) entra UM cartao, na ordem das colunas: a da esquerda de cima para baixo, depois a
     do meio, depois a da direita (data-ordem); um passo depois do nono a pagina segue. Visto uma vez, nao volta: os
     cartoes ficam e, com o bloco ja acima da tela e a rolagem parada, a trava sai (a altura extra sai e a rolagem e compensada
     na mesma conta, sem pulo), para a subida passar direto. No celular (uma coluna) e sem animacao, nada prende. */
  (function(){
    var palco = document.getElementById('guiaNpalco'); if(!palco) return;
    if(matchMedia('(max-width:880px), (prefers-reduced-motion: reduce)').matches) return;
    var fixo = palco.querySelector('.gn-fixo'), itens = [].slice.call(palco.querySelectorAll('.gn-item'));
    var CAB = 92, S = 0, extra = 0, topo = 0, vistos = 0, N = itens.length, solto = false, t = null;
    function cabe(){ return fixo.offsetHeight <= innerHeight - CAB - 40; }
    function mede(){
      var h = fixo.offsetHeight;
      S = Math.round(Math.max(80, Math.min(120, innerHeight * .11))); extra = (N + 1) * S;   /* um passo por cartao e mais um */
      topo = Math.round(CAB + Math.max(20, (innerHeight - CAB - h) / 2));
      palco.style.setProperty('--gn-top', topo + 'px'); palco.style.height = (h + extra) + 'px';
    }
    function mostra(n){ for(; vistos < Math.min(n, N); vistos++) itens.forEach(function(it){ if(+it.getAttribute('data-ordem') === vistos) it.classList.add('gn-vis'); }); }
    function solta(){
      if(solto) return; solto = true; mostra(N); clearTimeout(t);
      var acima = palco.getBoundingClientRect().bottom <= 0, raiz = document.documentElement;
      /* a ancoragem de rolagem do Chrome, Edge e Firefox ja compensaria a altura que sai acima da tela, e a conta abaixo
         dobraria (o Safari nao tem): desligada neste quadro, a compensacao e so a nossa, igual nos navegadores */
      raiz.style.overflowAnchor = 'none';
      palco.classList.remove('gn-anima'); palco.style.height = '';
      if(acima) window.scrollTo({top: window.scrollY - extra, behavior: 'instant'});   /* instantanea: o html tem scroll-behavior:smooth */
      requestAnimationFrame(function(){ requestAnimationFrame(function(){ raiz.style.overflowAnchor = ''; }); });
      removeEventListener('scroll', rola); removeEventListener('resize', ajusta);
    }
    function rola(){
      if(solto) return;
      var r = palco.getBoundingClientRect(), d = topo - r.top;   /* quanto ja rolou desde que o bloco chegou ao meio da tela */
      if(d >= -.4 * S) mostra(Math.floor(Math.max(0, d) / S) + 1);
      clearTimeout(t);
      if(vistos === N && r.bottom <= 0) t = setTimeout(function(){ if(palco.getBoundingClientRect().bottom <= 0) solta(); }, 160);
    }
    function ajusta(){ if(solto) return; if(matchMedia('(max-width:880px)').matches || !cabe()) solta(); else { mede(); rola(); } }
    if(!cabe()) return;
    palco.classList.add('gn-anima'); mede(); rola();
    addEventListener('scroll', rola, {passive: true}); addEventListener('resize', ajusta);
    addEventListener('load', ajusta);
  })();
  </script>"""


CSS = r"""/* ===== GUIA SETORES (sanfona; _ferramentas/guia_setores.py, 14/10/2026) ===== */
/* a sanfona dos setores do Guia, com as classes da de Servicos (.sv-*): so a moldura e daqui */
.gs{display:grid;grid-template-columns:repeat(12,minmax(0,1fr));column-gap:15px;margin-top:34px}
/* 15/10/2026: o titulo e o fluxo presos na metade esquerda (abaixo do cabecalho de 92 px + 28), a sanfona subindo a
   direita; a coluna so se solta quando o fim da sanfona chega ao fim dela */
.gs-cab{grid-column:1/7;grid-row:1/3;align-self:start;position:sticky;top:120px;padding-right:40px}
.gs-cab .mp-titulo{margin-top:0}
.gs .sv-line{grid-row:1/3}
.gs .sv-title{grid-column:7/-1;grid-row:1;display:block;background:none;margin-top:6px}
.gs .sv-list{grid-row:2}
.gs .sv-desc.gs-normas{margin-top:14px}
.gs ~ .mp-grade{margin-top:230px}
/* propostas em teste (15/10/2026): N, lista com miniaturas (a L saiu no mesmo dia) */
.gx-rot{display:flex;justify-content:space-between;font-family:var(--mono);font-size:11px;letter-spacing:.14em;text-transform:uppercase;color:var(--azul)}
.gn-palco{margin-top:150px}
/* os cartoes entrando na rolagem, um por vez, na ordem das colunas (so com o JS ligado, .gn-anima; 15/10/2026) */
.gn-palco.gn-anima .gn-fixo{position:sticky;top:var(--gn-top,120px)}
.gn-palco.gn-anima .gn-item{opacity:0;transform:translateY(28px);pointer-events:none;
  transition:opacity .7s ease,transform .7s cubic-bezier(.2,.7,.2,1),background .3s ease,color .3s ease,border-color .3s ease}
.gn-palco.gn-anima .gn-item.gn-vis{opacity:1;transform:none;pointer-events:auto}
.gn{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:8px;margin-top:16px}
.gn-item{display:grid;grid-template-columns:110px minmax(0,1fr);gap:16px;align-items:center;padding:12px;background:#fff;
  border:1px solid rgba(20,48,76,.14);border-radius:3px;color:var(--azul);text-decoration:none;transition:background .3s ease,color .3s ease,border-color .3s ease}
.gn-foto{position:relative;display:block;width:110px;height:110px;overflow:hidden;border-radius:2px;background:var(--mercurio)}
.gn-foto img,.gn-foto .vv-gl{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;display:block}
.gn-foto.gl-on img{visibility:hidden}
.gn-top{display:block;font-family:var(--mono);font-size:11px;letter-spacing:.14em;text-transform:uppercase}
.gn-nome{display:block;margin:6px 0;font-family:var(--sans);font-size:19px;font-weight:600;line-height:1.15}
.gn-normas{display:block;font-family:var(--sans);font-size:12.5px;font-weight:500}
.gn-item:is(:hover,:focus-visible){background:#336699;border-color:#336699;color:var(--mercurio)}
.gn-item:focus{outline:none}
@media (max-width:880px){ .gn{grid-template-columns:1fr} .gn-palco{margin-top:90px} }
@media (max-width:880px){ .gs-cab{position:static;grid-column:1/-1;grid-row:auto;padding-right:0}
  .gs .sv-title{grid-column:1/-1;grid-row:auto;margin-top:40px} .gs .sv-list{grid-row:auto;margin-top:20px}
  .gs ~ .mp-grade{margin-top:156px} }
/* ===== fim GUIA SETORES ===== */
"""

# o script da sanfona e o motor das fotos dela: ajustes para valer nas duas sanfonas
TROCAS = [
    # 15/10/2026: «nesta tabela, deixe a fonte maior» (18 -> 22) e, no mesmo dia, «faca as fontes ainda maiores» (22 -> 28):
    # o titulo do item das duas sanfonas (Guia e Servicos)
    (".sv-item-title{width:100%;display:flex;align-items:center;justify-content:space-between;gap:15px;padding:16px 0;margin:0;background:none;border:0;cursor:pointer;text-align:left;font-family:var(--sans);font-weight:500;font-size:22px;line-height:1.1;letter-spacing:0;color:var(--azul)}   /* 15/10/2026: «deixe a fonte maior» (era 18) */",
     ".sv-item-title{width:100%;display:flex;align-items:center;justify-content:space-between;gap:15px;padding:16px 0;margin:0;background:none;border:0;cursor:pointer;text-align:left;font-family:var(--sans);font-weight:500;font-size:28px;line-height:1.1;letter-spacing:0;color:var(--azul)}   /* 15/10/2026: «deixe a fonte maior», depois «ainda maiores» (era 18, depois 22) */"),
    ("      itens.forEach(function(o){ if (o !== item) abre(o, false); });",
     "      /* 14/10/2026: so os irmaos da mesma sanfona (a dos setores do Guia usa as mesmas classes) */\n"
     "      itens.forEach(function(o){ if (o !== item && o.parentNode === item.parentNode) abre(o, false); });"),
    ("        if(quer && !gl) gl = ditherVivo({brilhoTom:0.35, gama:0.88, ctr:1.55, escuro:0.35, lavaRepouso:0.12, raiz:raiz, planos:[{el:raiz, lum:im.getAttribute('data-lum')}], classeCanvas:'vv-gl',",
     "        /* 14/10/2026: a foto com tom proprio (data-tom, receita do Spirit) leva o tom para o motor */\n"
     "        var tom = null; try { tom = JSON.parse(im.getAttribute('data-tom') || 'null'); } catch(e){}\n"
     "        if(quer && !gl) gl = ditherVivo({brilhoTom:0.35, gama:0.88, ctr:1.55, escuro:0.35, lavaRepouso:0.12, raiz:raiz, planos:[{el:raiz, lum:im.getAttribute('data-lum'), tom:tom}], classeCanvas:'vv-gl',"),
]


def main():
    p = os.path.join(SITE, 'index.html')
    raw = open(p, 'rb').read(); crlf = b'\r\n' in raw
    t = raw.decode('utf-8').replace('\r\n', '\n')
    i, j = t.index('<!-- foco -->'), t.index('<!-- fim foco -->')
    atual = t[i + len('<!-- foco -->'):j]
    if 'id="sfSetores"' in atual and not os.path.exists(GUARDA):
        open(GUARDA, 'w', encoding='utf-8').write(atual)
        print('guardado o bloco dos cartoes em', GUARDA)
    t = re.sub(r'/\* ===== GUIA SETORES.*?/\* ===== fim GUIA SETORES ===== \*/\n', '', t, flags=re.S)
    for a, b in TROCAS:
        if a in t: t = t.replace(a, b, 1)
        assert b in t, 'ajuste nao aplicado: ' + a[:60]
    # o cabecalho da secao (do <div class="mp-cab"> do Guia ate o <!-- foco -->)
    gi = t.index('<section class="mp-sec" id="guia"'); ci = t.index('  <div class="mp-cab">', gi); cf = t.index('<!-- foco -->')
    cab = CAB_ORIGINAL if len(sys.argv) > 1 and sys.argv[1] == 'cartoes' else CAB_SANFONA
    t = t[:ci] + cab + t[cf:]
    if len(sys.argv) > 1 and sys.argv[1] == 'cartoes':
        novo = open(GUARDA, encoding='utf-8').read()
    else:
        S = setores()
        novo = '\n' + sanfona(S) + '\n' + bloco_n(S) + '\n  '
        ancora = '/* ===== secao: processo ===== */'
        assert t.count(ancora) == 1
        t = t.replace(ancora, CSS + ancora, 1)
    i, j = t.index('<!-- foco -->'), t.index('<!-- fim foco -->')   # de novo: o CSS tirado ou posto mudou as posicoes
    t = t[:i + len('<!-- foco -->')] + novo + t[j:]
    open(p, 'wb').write((t.replace('\n', '\r\n') if crlf else t).encode('utf-8'))
    print('index.html: bloco dos setores do Guia =', 'cartoes' if len(sys.argv) > 1 else 'sanfona')


if __name__ == '__main__':
    main()
