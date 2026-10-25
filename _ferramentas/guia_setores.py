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
    ('img/industria-01-bayer-st.webp?v=19102026', 'img/industria-01-lum-st.webp?v=19102026',   # 19/10/2026: consultores no galpao (a foto que esteve em Experiencia desde 1998), receita industria-01-st.json
     '{"brilhoTom":0.32,"gama":1.02,"ctr":1.6,"escuro":0.2,"limiar":-0.04,"veu":0,"cores":["#153351","#183858","#6792BD","#FAF9F5"]}', 'Manufatura'),
    ('img/transporte-bayer-st.webp?v=12102026', 'img/transporte-lum-st.webp?v=12102026', None, 'Mobilidade'),
    ('img/facilities-02-bayer-gs.webp?v=14102026', 'img/facilities-02-lum-gs.webp?v=14102026',
     '{"brilhoTom":0.36,"gama":0.8,"ctr":1.9,"escuro":1.3,"limiar":-0.05,"veu":0.07,"cores":["#14304C","#336699","#D3E2F2","#FAF9F5"]}', 'Predial'),
    ('img/alimentos-03-bayer-st.webp?v=19102026', 'img/alimentos-03-lum-st.webp?v=19102026',   # 19/10/2026 (2a): inspecao numa linha de embalagem (Google Flow), receita _ferramentas/receitas/alimentos-03-st.json
     '{"brilhoTom":0.32,"gama":1.02,"ctr":1.6,"escuro":0.15,"limiar":-0.04,"veu":0,"cores":["#153351","#183858","#6792BD","#FAF9F5"]}', 'Alimentício'),
    ('img/agro-02-bayer-gs.webp?v=13102026', 'img/agro-02-lum-gs.webp?v=13102026', None, 'Agroflorestal'),
    ('img/saude-03-bayer-gs.webp?v=14102026', 'img/saude-03-lum-gs.webp?v=14102026',
     '{"brilhoTom":0.34,"gama":0.81,"ctr":1.85,"escuro":1.6,"limiar":0,"veu":0.07,"cores":["#14304C","#336699","#D3E2F2","#FAF9F5"]}', 'Hospitalar'),
    ('img/energia-01-bayer-gs.webp?v=13102026', 'img/energia-01-lum-gs.webp?v=13102026',
     '{"brilhoTom":0.09,"gama":1.13,"ctr":1.7,"escuro":0.4,"limiar":0.03,"veu":0.19,"cores":["#14304C","#336699","#D3E2F2","#FAF9F5"]}', 'Energético'),
    ('img/tecnologia-03-bayer-gs.webp?v=25102026b', 'img/tecnologia-03-lum-gs.webp?v=25102026b',   # 25/10/2026: corredor de data center com dois profissionais de TI (Google Flow), receita _ferramentas/receitas/tecnologia-03-gs.json; a 02 (painel de fibra) saiu («nao gosto dela»)
     '{"brilhoTom":0.38,"gama":0.81,"ctr":1.9,"escuro":0.5,"limiar":0,"veu":0.08,"cores":["#153351","#183858","#6792BD","#FAF9F5"]}', 'Digital'),
    ('img/servicos-03-bayer-gs.webp?v=13102026', 'img/servicos-03-lum-gs.webp?v=13102026',
     '{"brilhoTom":0.27,"gama":0.86,"ctr":1.7,"escuro":1,"limiar":0,"veu":0.1,"cores":["#153351","#183858","#6792BD","#FAF9F5"]}', 'Serviços'),
]

# 17/10/2026: «Consultoria, auditoria, treinamento, inspeções para organizações», e logo abaixo, menor, a chamada para a
# pesquisa aplicada, com link (era «O portfolio da Ideal Metrics se organiza em tres entradas...», recusado: slogan)
TITULO = 'Consultoria, auditoria, treinamento, inspeções para organizações.'
PESQUISA = ('<p class="gs-pesquisa"><a href="estudos-pesquisa.html">Consulte a frente de pesquisa aplicada a setores '
            '&rarr;</a></p>')
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
         # 19/10/2026: «tire esta legenda»: o fluxo Setor > Tema > Norma > Pagina do servico saiu da coluna da esquerda
         '      ' + PESQUISA,
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
              'aria-controls="gs-panel-%d"><span><span class="gs-num">%s</span>%s</span>%s</button></h3>' % (k, 'true' if k == 0 else 'false', k, s['n'], esc(s['nome']), PLUS),
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


CSS = r"""/* ===== GUIA SETORES (sanfona; _ferramentas/guia_setores.py, 14/10/2026) ===== */
/* a sanfona dos setores do Guia, com as classes da de Servicos (.sv-*): so a moldura e daqui */
.gs{display:grid;grid-template-columns:repeat(12,minmax(0,1fr));column-gap:15px;margin-top:34px}
/* 15/10/2026: o titulo e o fluxo presos na metade esquerda (abaixo do cabecalho de 92 px + 28), a sanfona subindo a
   direita; a coluna so se solta quando o fim da sanfona chega ao fim dela */
.gs-cab{grid-column:1/7;grid-row:1/3;align-self:start;position:sticky;top:120px;padding-right:40px}
.gs-cab .mp-titulo{margin-top:0}
/* 17/10/2026: «o consulte a frente poderia ficar em baixo»: a coluna presa ocupa a altura da tela e a chamada vai
   para o pe dela, na altura da ultima linha da sanfona */
.gs-cab{display:flex;flex-direction:column;min-height:calc(100svh - 170px);padding-bottom:38px}   /* 17/10/2026: «alinhado com Servicos e setor publico, ultima frase com a ultima frase»: 38 px poe a linha de base da chamada na do ultimo item */
.gs-pesquisa{margin:auto 0 0;padding-top:40px;font-family:var(--sans);font-size:18px;color:var(--azul-escuro)}
.gs-pesquisa a{color:inherit;text-decoration:none;border-bottom:1px solid rgba(20,48,76,.3)}
.gs-pesquisa a:hover{color:var(--azul);border-bottom-color:var(--azul)}
.gs .sv-line{grid-row:1/3}
.gs .sv-title{grid-column:7/-1;grid-row:1;display:block;background:none;margin-top:6px}
.gs .sv-list{grid-row:2}
.gs .sv-desc.gs-normas{margin-top:14px}
/* 16/10/2026: «a aparencia desta lista conforme a outra» (a proposta H): nome um pouco mais grosso, o numero em mono
   antes, e o + recuado da linha da direita da pagina */
.gs .sv-item-title{font-weight:600;padding:9px 12px 9px 0}   /* 19/10/2026: «deixe a tabela com as linhas mais estreitas» (era 16 px em cima e embaixo) */
.gs-num{display:inline-block;min-width:44px;font-family:var(--mono);font-size:11px;font-weight:400;letter-spacing:.1em;color:var(--azul)}
.gs ~ .mp-grade{margin-top:230px}
@media (max-width:880px){ .gs-cab{position:static;grid-column:1/-1;grid-row:auto;padding-right:0;min-height:0;padding-bottom:0}
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
        novo = '\n' + sanfona(S) + '\n  '
        ancora = '/* ===== secao: processo ===== */'
        if ancora not in t:   # 17/10/2026: o Processo saiu da home; o CSS do Guia entra antes do dos Diferenciais
            ancora = '/* ===== secao: diferenciais ===== */'
        assert t.count(ancora) == 1
        t = t.replace(ancora, CSS + ancora, 1)
    i, j = t.index('<!-- foco -->'), t.index('<!-- fim foco -->')   # de novo: o CSS tirado ou posto mudou as posicoes
    t = t[:i + len('<!-- foco -->')] + novo + t[j:]
    open(p, 'wb').write((t.replace('\n', '\r\n') if crlf else t).encode('utf-8'))
    print('index.html: bloco dos setores do Guia =', 'cartoes' if len(sys.argv) > 1 else 'sanfona')


if __name__ == '__main__':
    main()
