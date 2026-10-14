# -*- coding: utf-8 -*-
"""O bloco dos setores da secao Guia da home, em TESTE: as propostas H e I (14/10/2026).

    python _ferramentas/guia_setores.py            grava H e I, uma embaixo da outra, entre <!-- foco --> e <!-- fim foco -->
    python _ferramentas/guia_setores.py cartoes    volta o bloco dos cartoes (3x3 com a foto presa), guardado em
                                                   _ferramentas/guia_bloco_cartoes.html na primeira rodada

Pedido do Leandro: «nao estou satisfeito com esta secao; ja temos a divisao, e ja temos a foto, sugira outros esquemas»;
das 14 maquetes (A a N), «substitua pelo H e pelo I, quero ver como fica».

H, NOMES GRANDES COM FOTO QUE ACOMPANHA: os nove setores em letra grande, um por linha, como um sumario de revista; no
mouse, os outros nomes recuam, o da linha mostra as normas proprias do setor e a foto aparece flutuando ao lado do
ponteiro (do lado de la da tela, para nao cobrir as normas). A foto e a mesma pilha de nove do bloco antigo, no motor
da trama (empilhado, com o tom de cada uma em data-tom). No celular nao ha foto: a lista fica com as normas embaixo.

I, FIOS SETOR -> NORMA: a foto a esquerda e, a direita, os setores numa coluna, as normas proprias na outra e fios
ligando cada setor as suas (tres por setor), na linha fina do mapa da secao Conhecimento, com a mesma entrada (.ln-svg).
No mouse sobre um setor, os fios dele ficam azuis, a foto troca e a legenda traz o resumo; sobre uma norma, acendem os
setores dela (mostra que uma norma serve a mais de um setor). Some abaixo de 880 px.

As normas de cada setor vem de js/setores-dados.js (o setores.py), sem as que valem para qualquer setor (ISO 9001, 14001
e 45001) e sem as que sairam do site (SA 8000, ISO 39002)."""

import json, os, re, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(AQUI)
GUARDA = os.path.join(AQUI, 'guia_bloco_cartoes.html')
FORA = {'SA 8000', 'ISO 39002'}
TRANSV = {'ISO 9001', 'ISO 14001', 'ISO 45001'}
JS_V = '1'

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


def esc(t):
    return t.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;')


def setores():
    d = open(os.path.join(SITE, 'js', 'setores-dados.js'), encoding='utf-8').read()
    D = json.loads(d[d.index('{'):d.rindex('}') + 1]); N = D['normas']
    out = []
    for k, s in enumerate(D['setores']):
        ns = [n for n in s['normas'] if n in N and N[n]['nome'] not in FORA and N[n]['nome'] not in TRANSV]
        out.append(dict(n='%02d' % (k + 1), nome=s['nome'], pag=s['pagina'], resumo=s['resumo'], cat=FOTOS[k][3],
                        normas=[(N[n]['nome'], N[n].get('pagina')) for n in ns]))
    assert len(out) == len(FOTOS), 'setores e fotos fora de ordem'
    return out


def midia():
    o = ['<div class="sx-midia" aria-hidden="true">']
    for k, (src, lum, tom, cat) in enumerate(FOTOS):
        o.append('<div class="sx-layer%s"><img src="%s" data-lum="%s"%s alt="" loading="lazy" decoding="async"></div>'
                 % (' sx-layer-ativa' if k == 0 else '', src, lum, " data-tom='%s'" % tom if tom else ''))
    o.append('</div>')
    return ''.join(o)


def bloco_h(S):
    o = ['  <div class="gx-rot"><span>Proposta H · nomes grandes</span><span>[ em teste ]</span></div>',
         '  <div class="gh" id="guiaH">',
         '    <ol class="gh-lista">']
    for k, s in enumerate(S):
        o.append('      <li><a class="gh-li" href="%s" data-i="%d"><span class="gh-n">%s</span><span class="gh-nome">%s</span>'
                 '<span class="gh-normas">%s</span></a></li>'
                 % (s['pag'], k, s['n'], esc(s['nome']), esc(' · '.join(n for n, p in s['normas'][:4]))))
    o += ['    </ol>',
          '    <div class="gh-flut" aria-hidden="true"><div class="gh-flut-in">' + midia() + '</div></div>',
          '  </div>']
    return '\n'.join(o)


def bloco_i(S):
    # a coluna das normas na ordem em que aparecem, de cima para baixo, para os fios cruzarem pouco
    todas = []
    for s in S:
        for n, p in s['normas'][:3]:
            if n not in [t[0] for t in todas]: todas.append((n, p))
    W, XS, XN = 860, 290, 690
    H = max(len(S) * 58, len(todas) * 24) + 24
    ys = [28 + k * (H - 52) / (len(S) - 1) for k in range(len(S))]
    yn = {n: 16 + j * (H - 32) / (len(todas) - 1) for j, (n, p) in enumerate(todas)}
    ixn = {n: j for j, (n, p) in enumerate(todas)}
    o = ['<svg class="ln-svg gi-svg" viewBox="0 0 %d %d" role="group" aria-label="Setores e normas próprias de cada um">' % (W, H)]
    for k, s in enumerate(S):
        for n, p in s['normas'][:3]:
            y1, y2 = ys[k], yn[n]
            o.append('<path class="ln-linha gi-fio" data-s="%d" data-n="%d" d="M%d %.1f C %d %.1f, %d %.1f, %d %.1f" '
                     'style="--ox:%dpx;--oy:%.1fpx;--d:%d"/>' % (k, ixn[n], XS + 10, y1, 480, y1, 500, y2, XN - 10, y2, XS + 10, y1, 300 + 110 * k))
    for k, s in enumerate(S):
        o.append('<g class="ln-b" style="--dx:0px;--dy:0px;--d:%d"><a href="%s"><text class="gi-s" data-s="%d" x="%d" y="%.1f" '
                 'text-anchor="end"><tspan class="gi-sn">%s</tspan> %s</text></a></g>'
                 % (120 + 110 * k, s['pag'], k, XS, ys[k] + 6, s['n'], esc(s['nome'])))
    for j, (n, p) in enumerate(todas):
        t = '<text class="gi-n" data-n="%d" x="%d" y="%.1f">%s</text>' % (j, XN, yn[n] + 4.5, esc(n))
        o.append('<g class="ln-b" style="--dx:-16px;--dy:0px;--d:%d">%s</g>' % (900 + 50 * j, '<a href="%s">%s</a>' % (p, t) if p else t))
    o.append('</svg>')
    s0 = S[0]
    dados = ' '.join('data-r%d="%s" data-m%d="%s"' % (k, esc(s['resumo']), k, esc(' · '.join(n for n, p in s['normas'][:4])))
                     for k, s in enumerate(S))
    return '\n'.join([
        '  <div class="gx-rot gx-rot--i"><span>Proposta I · fios setor → norma</span><span>[ em teste ]</span></div>',
        '  <div class="gi" id="guiaI" %s>' % dados,
        '    <figure class="gi-fig">' + midia() + '<figcaption><p class="gi-resumo">%s</p><p class="gi-normas">%s</p></figcaption></figure>'
        % (esc(s0['resumo']), esc(' · '.join(n for n, p in s0['normas'][:4]))),
        '    <div class="gi-mapa">' + ''.join(o) + '</div>',
        '  </div>'])


CSS = r"""/* ===== GUIA SETORES H e I (_ferramentas/guia_setores.py; em teste desde 14/10/2026) ===== */
.gx-rot{display:flex;justify-content:space-between;margin-top:44px;font-family:var(--mono);font-size:11px;letter-spacing:.14em;text-transform:uppercase;color:var(--azul)}
.gx-rot--i{margin-top:150px}
/* H: nomes grandes; a foto flutua ao lado do ponteiro */
.gh{position:relative;margin-top:16px}
.gh-lista{list-style:none;margin:0;padding:0;border-top:1px solid var(--fio)}
.gh-li{display:grid;grid-template-columns:64px minmax(0,1fr) auto;align-items:baseline;gap:20px;padding:12px 0 10px;
  border-bottom:1px solid var(--fio);color:var(--azul);text-decoration:none}
.gh-n{font-family:var(--mono);font-size:11px;letter-spacing:.14em}
.gh-nome{font-family:var(--sans);font-weight:600;font-size:clamp(28px,3vw,44px);line-height:1.06;letter-spacing:-.015em;transition:color .35s ease}
.gh-normas{font-family:var(--sans);font-size:14px;font-weight:500;opacity:0;transform:translateX(-8px);transition:opacity .35s ease,transform .35s ease}
.gh-lista:hover .gh-nome{color:rgba(20,48,76,.26)}
.gh-li:is(:hover,:focus-visible) .gh-nome{color:var(--azul)}
.gh-li:is(:hover,:focus-visible) .gh-normas{opacity:1;transform:none}
.gh-li:focus{outline:none}
.gh-flut{position:absolute;left:0;top:0;width:300px;pointer-events:none;z-index:3;will-change:transform}
.gh-flut-in{opacity:0;transform:scale(.88) rotate(-2deg);transition:opacity .3s ease,transform .45s cubic-bezier(.2,.8,.2,1);
  box-shadow:0 18px 40px rgba(20,48,76,.22)}
.gh-flut.on .gh-flut-in{opacity:1;transform:scale(1) rotate(-2deg)}
/* I: fios setor -> norma, na linha fina do mapa da secao Conhecimento */
.gi{display:grid;grid-template-columns:repeat(12,minmax(0,1fr));column-gap:15px;margin-top:16px}
.gi-fig{grid-column:1 / span 4;margin:0;align-self:start}
.gi-fig figcaption{margin:14px 0 0}
.gi-resumo{margin:0;font-family:var(--sans);font-weight:500;font-size:16px;line-height:1.35;color:var(--azul)}
.gi-normas{margin:8px 0 0;font-family:var(--mono);font-size:10.5px;line-height:1.5;letter-spacing:.06em;text-transform:uppercase;color:var(--azul)}
.gi-mapa{grid-column:5 / -1}
.gi-svg{display:block;width:100%;height:auto}
.gi-svg path{vector-effect:non-scaling-stroke}
.gi-svg .gi-fio{fill:none;stroke:rgba(20,48,76,.22);stroke-width:.8;transition:stroke .25s ease,stroke-width .25s ease,opacity .25s ease}
.gi-svg.gi-foco .gi-fio{opacity:.3}
.gi-svg .gi-fio.on{stroke:#336699;stroke-width:1.3;opacity:1}
.gi-s{font-family:var(--sans);font-size:17px;font-weight:600;fill:#14304C;transition:opacity .25s ease}
.gi-sn{font-family:var(--mono);font-size:11px;font-weight:400;letter-spacing:.14em}
.gi-n{font-family:var(--sans);font-size:13px;font-weight:500;fill:#14304C;transition:opacity .25s ease}
.gi-svg.gi-foco :is(.gi-s,.gi-n){opacity:.3}
.gi-svg.gi-foco :is(.gi-s,.gi-n).on{opacity:1}
.gi-svg a{cursor:pointer}
.gi-svg a:focus{outline:none}
.gi ~ .mp-grade{margin-top:230px}   /* ~ e nao +: a tag do script fica entre os dois */
@media (max-width:880px){
  .gh-flut{display:none}
  .gh-li{grid-template-columns:44px minmax(0,1fr);gap:4px 12px}
  .gh-normas{grid-column:2;opacity:1;transform:none;font-size:13px}
  .gh-lista:hover .gh-nome{color:var(--azul)}
  .gx-rot--i,.gi{display:none}
  .gi ~ .mp-grade{margin-top:156px}
}
/* ===== fim GUIA SETORES ===== */
"""


def main():
    p = os.path.join(SITE, 'index.html')
    raw = open(p, 'rb').read(); crlf = b'\r\n' in raw
    t = raw.decode('utf-8').replace('\r\n', '\n')
    i, j = t.index('<!-- foco -->'), t.index('<!-- fim foco -->')
    atual = t[i + len('<!-- foco -->'):j]
    if 'id="sfSetores"' in atual and not os.path.exists(GUARDA):
        open(GUARDA, 'w', encoding='utf-8').write(atual)
        print('guardado o bloco dos cartoes em', GUARDA)
    t = re.sub(r'/\* ===== GUIA SETORES H e I .*?/\* ===== fim GUIA SETORES ===== \*/\n', '', t, flags=re.S)
    if len(sys.argv) > 1 and sys.argv[1] == 'cartoes':
        novo = open(GUARDA, encoding='utf-8').read()
    else:
        S = setores()
        novo = '\n' + bloco_h(S) + '\n' + bloco_i(S) + '\n  <script src="js/guia-setores.js?v=%s" defer></script>\n  ' % JS_V
        ancora = '/* ===== secao: processo ===== */'
        assert t.count(ancora) == 1
        t = t.replace(ancora, CSS + ancora, 1)
    i, j = t.index('<!-- foco -->'), t.index('<!-- fim foco -->')   # de novo: o CSS tirado ou posto mudou as posicoes
    t = t[:i + len('<!-- foco -->')] + novo + t[j:]
    open(p, 'wb').write((t.replace('\n', '\r\n') if crlf else t).encode('utf-8'))
    print('index.html: bloco dos setores do Guia =', 'cartoes' if len(sys.argv) > 1 else 'H e I')


if __name__ == '__main__':
    main()
