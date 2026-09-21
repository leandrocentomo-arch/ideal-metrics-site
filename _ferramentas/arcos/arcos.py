# -*- coding: utf-8 -*-
"""Esquema por arcos da home da Ideal Metrics (secao «Conhecimento»).

REFERENCIA. catalystbehavioral.com/litigation-surveys monta o esquema com quatro
camadas SVG empilhadas: discos palidos cheios, contornos finos de 1px, os
rotulos e uns cartoes. Cada camada desliza numa velocidade propria quando a
pagina rola, e e isso que da profundidade. Os discos NAO sao concentricos aos
contornos: sao manchas independentes por tras.

AQUI. Tres camadas no mesmo vocabulario do site:
  discos    #F0EFEA, o «creme da casa escurecido 4%» que a secao Demandas ja usa
  aros      1px em tinta a 16%; tracejado = divisao de inteligencia
  rotulos   titulo do tema no centro do aro e as normas em pilulas SOBRE o aro,
            no mesmo desenho das etiquetas da secao Demandas (rx 3, branco,
            contorno a 10%, IBM Plex Sans Condensed 500)

CONTEUDO. Temas e normas tirados do mapa estrategico v1.1
(mapa-estrategico-ideal-metrics.html, MAPA.padronizacao e MAPA.inteligencia).
Nada de cliente, onde ja aconteceu, estado ou CNAE.

As larguras das pilulas vem de larguras.json, MEDIDAS no navegador com a fonte
do site (getComputedTextLength), e nao estimadas."""

import json, math, os

AQUI = os.path.dirname(os.path.abspath(__file__))
VB_W, VB_H = 1200, 760
PAD_X, PIL_H = 8, 20           # respiro lateral e altura da pilula, em unidades do viewBox
TXT_PIL, TXT_TIT, LH_TIT = 10.5, 17, 21
# larguras.json foi medido com pilula a 12,5 e titulo a 19: a largura de texto
# escala linear com o corpo, entao basta a razao
ESC_PIL, ESC_TIT = TXT_PIL / 12.5, TXT_TIT / 19.0
FOLGA_MIOLO = 12               # o miolo de cada aro para 12 antes da linha

# (id, pagina, divisao, cx, cy, r, linhas do titulo, [(norma, angulo em graus)])
# angulo: 0 = direita, 90 = baixo (y do SVG cresce para baixo)
TEMAS = [
 ('iso', 'implantacao-iso.html', 'p', 320, 318, 178, ['Sistemas de', 'gestão ISO'],
    [('ISO 9001', -135), ('ISO 14001', -75), ('ISO 45001', 180), ('ISO 50001', 145), ('ISO 41001', -15)]),
 ('nrs', 'nrs.html', 'p', 215, 578, 104, ['Normas', 'Regulamentadoras'],
    [('NR-01', -120), ('NR-12', 130), ('NR-17', 60)]),
 ('compliance', 'compliance-seguranca-informacao.html', 'p', 525, 598, 106, ['Compliance e', 'segurança da', 'informação'],
    [('ISO 37001', -110), ('ISO/IEC 27001', 60), ('LGPD', 125)]),
 ('carbono', 'gestao-carbono.html', 'p', 680, 218, 140, ['Gestão', 'de carbono'],
    [('GHG Protocol', -150), ('ISO 14064', -90), ('ISO 14068-1', -30), ('SBTi', 100)]),
 ('esg', 'esg.html', 'p', 895, 350, 124, ['ESG'],
    [('ABNT PR 2030', -40), ('GRI', 160), ('IFRS S1 e S2', 80)]),
 ('smeta', 'sedex-smeta.html', 'p', 1090, 150, 86, ['SEDEX', 'SMETA'],
    [('SMETA 7.0', -150), ('SA 8000', 140)]),
 ('padroes', 'padroes-mercado.html', 'p', 1080, 420, 78, ['Padrões', 'de mercado'],
    [('EcoVadis', -60), ('FSC', 40)]),
 ('alimentos', 'seguranca-alimentos.html', 'p', 760, 620, 92, ['Segurança', 'de alimentos'],
    [('ISO 22000', -130), ('FSSC 22000', 60)]),
 ('estudos', 'estudos-pesquisa.html', 'i', 1045, 640, 100, ['Estudos e', 'pesquisa', 'aplicada'],
    [('Nota técnica', -130), ('Observatório setorial', 100), ('EUDR', -40)]),
]

# 21/09/2026 (2a volta): as manchas soltas por tras SAIRAM. Desalinhadas dos
# aros e em duas cores, liam como erro de registro. Agora cada aro tem o seu
# MIOLO, concentrico, parando FOLGA_MIOLO antes da linha; onde dois miolos se
# cruzam o tom escurece sozinho (multiply). Tres miolos sao frios, no
# cinza-azulado da liga fria (#A3B5C8 a 25% sobre o creme = #E4E8EA), no mesmo
# valor do bege: «mais proximo do bege», como o Leandro pediu.
DISCOS = []
TEMAS_FRIOS = {'iso', 'esg', 'estudos'}
# 21/09/2026: os aros soltos (sem rotulo, so ritmo, copiados da referencia)
# SAIRAM. O Leandro perguntou para que serviam, e a resposta era: para nada.
# Todo aro desta secao e um tema.
AROS_SOLTOS = []

def larguras():
    p = os.path.join(AQUI, 'larguras.json')
    return json.load(open(p, encoding='utf-8')) if os.path.exists(p) else {}


def pilulas(L):
    """posicao e caixa de cada pilula, centrada NO aro"""
    out = []
    for tid, pag, div, cx, cy, r, tit, normas in TEMAS:
        for txt, ang in normas:
            w = L.get(txt, len(txt) * 6.6) * ESC_PIL + 2 * PAD_X
            t = math.radians(ang)
            x, y = cx + r * math.cos(t), cy + r * math.sin(t)
            out.append(dict(tema=tid, txt=txt, x=x, y=y, w=w, h=PIL_H,
                            x0=x - w / 2, y0=y - PIL_H / 2, x1=x + w / 2, y1=y + PIL_H / 2))
    return out


def titulos(L):
    out = []
    for tid, pag, div, cx, cy, r, tit, normas in TEMAS:
        n = len(tit)
        w = max(L.get('T:' + l, len(l) * 9.4) for l in tit) * ESC_TIT
        h = LH_TIT * n
        out.append(dict(tema=tid, x0=cx - w / 2, y0=cy - h / 2, x1=cx + w / 2, y1=cy + h / 2))
    return out


def colisoes(L, folga=6):
    P, T = pilulas(L), titulos(L)
    ruim = []
    def bate(a, b):
        return not (a['x1'] + folga <= b['x0'] or b['x1'] + folga <= a['x0'] or
                    a['y1'] + folga <= b['y0'] or b['y1'] + folga <= a['y0'])
    for i in range(len(P)):
        for j in range(i + 1, len(P)):
            if bate(P[i], P[j]): ruim.append('pilula x pilula: %s / %s' % (P[i]['txt'], P[j]['txt']))
        for t in T:
            if bate(P[i], t): ruim.append('pilula x titulo: %s / %s' % (P[i]['txt'], t['tema']))
        p = P[i]
        if p['x0'] < 4 or p['y0'] < 4 or p['x1'] > VB_W - 4 or p['y1'] > VB_H - 4:
            ruim.append('fora da prancha: %s (%.0f,%.0f)-(%.0f,%.0f)' % (p['txt'], p['x0'], p['y0'], p['x1'], p['y1']))
    for i in range(len(T)):
        for j in range(i + 1, len(T)):
            if bate(T[i], T[j]): ruim.append('titulo x titulo: %s / %s' % (T[i]['tema'], T[j]['tema']))
    # a pilula tem de ler como do SEU aro: longe da linha de qualquer outro
    for p in P:
        for tid, pag, div, cx, cy, r, tit, normas in TEMAS:
            if tid == p['tema']: continue
            d = math.hypot(p['x'] - cx, p['y'] - cy)
            if abs(d - r) < 34:
                ruim.append('pilula no aro alheio: %s perto do aro de %s (%.0f)' % (p['txt'], tid, abs(d - r)))
        for cx, cy, r in AROS_SOLTOS:
            d = math.hypot(p['x'] - cx, p['y'] - cy)
            if d < r + p['w'] / 2 + 8:
                ruim.append('pilula x aro solto: %s' % p['txt'])
    # titulo nao pode ser cortado pela linha de outro aro
    for t, tema in zip(T, TEMAS):
        tx, ty = (t['x0'] + t['x1']) / 2, (t['y0'] + t['y1']) / 2
        meia = math.hypot(t['x1'] - t['x0'], t['y1'] - t['y0']) / 2
        for tid, pag, div, cx, cy, r, tit, normas in TEMAS:
            if tid == tema[0]: continue
            if abs(math.hypot(tx - cx, ty - cy) - r) < meia + 8:
                ruim.append('titulo cortado por aro: %s por %s' % (tema[0], tid))
    for cx, cy, r in DISCOS:
        if cx - r < 0 or cy - r < 0 or cx + r > VB_W or cy + r > VB_H:
            ruim.append('disco fora da prancha: (%d,%d,%d)' % (cx, cy, r))
    return ruim


def esc(s):
    return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;')


def svg(L):
    o = ['<svg class="ar-svg" viewBox="0 0 %d %d" role="group" aria-label="Temas e normas da Ideal Metrics">' % (VB_W, VB_H)]
    o.append('<g class="ar-discos" data-ar-vel="26">')
    for cx, cy, r in DISCOS:
        o.append('<circle cx="%d" cy="%d" r="%d"/>' % (cx, cy, r))
    o.append('</g>')
    o.append('<g class="ar-aros" data-ar-vel="11">')
    for cx, cy, r in AROS_SOLTOS:
        o.append('<circle class="ar-solto" cx="%d" cy="%d" r="%d"/>' % (cx, cy, r))
    for tid, pag, div, cx, cy, r, tit, normas in TEMAS:
        o.append('<circle class="ar-aro%s" data-t="%s" cx="%d" cy="%d" r="%d"/>'
                 % (' ar-aro--i' if div == 'i' else '', tid, cx, cy, r))
    o.append('</g>')
    o.append('<g class="ar-rotulos">')
    P = pilulas(L)
    for tid, pag, div, cx, cy, r, tit, normas in TEMAS:
        rot = '%s: %s' % (' '.join(tit), ', '.join(n for n, a in normas))
        o.append('<a class="ar-tema" data-t="%s" href="%s" aria-label="%s">' % (tid, pag, esc(rot)))
        o.append('<circle class="ar-alvo" cx="%d" cy="%d" r="%d"/>' % (cx, cy, r))
        y0 = cy - LH_TIT * (len(tit) - 1) / 2.0
        o.append('<text class="ar-tit" x="%d" y="%.1f">' % (cx, y0))
        for k, l in enumerate(tit):
            o.append('<tspan x="%d" dy="%s">%s</tspan>' % (cx, '0' if k == 0 else LH_TIT, esc(l)))
        o.append('</text>')
        for p in (p for p in P if p['tema'] == tid):
            o.append('<g class="ar-pil"><rect x="%.1f" y="%.1f" width="%.1f" height="%d" rx="3"/>'
                     '<text x="%.1f" y="%.1f">%s</text></g>'
                     % (p['x0'], p['y0'], p['w'], PIL_H, p['x'], p['y'] + 4.4, esc(p['txt'])))
        o.append('</a>')
    o.append('</g></svg>')
    return '\n'.join(o)


def lista():
    """a mesma informacao em lista, para tela estreita"""
    o = ['<ul class="ar-lista">']
    for tid, pag, div, cx, cy, r, tit, normas in TEMAS:
        o.append('<li class="ar-item%s"><a href="%s">%s</a><span class="ar-normas">%s</span></li>'
                 % (' ar-item--i' if div == 'i' else '', pag, esc(' '.join(tit)),
                    ''.join('<span>%s</span>' % esc(n) for n, a in normas)))
    o.append('</ul>')
    return '\n'.join(o)


def css_hover():
    """o aro fica na camada de tras e o rotulo na da frente, entao o realce do
    aro sob o mouse precisa do :has() no svg. Um par de regras por tema."""
    r = []
    for t in TEMAS:
        tid = t[0]
        r.append('.ar-svg:has(.ar-tema[data-t="%s"]:is(:hover,:focus-visible)) .ar-aro[data-t="%s"]' % (tid, tid))
    return ',\n'.join(r) + '{stroke:rgba(20,48,76,.5)}'


if __name__ == '__main__':
    L = larguras()
    print('larguras medidas: %d' % len(L))
    ruins = colisoes(L)
    print('colisoes: %d' % len(ruins))
    for x in ruins: print('  ' + x)


def limites(L, margem=10):
    """caixa de tudo o que tem tinta: aros, discos, aros soltos e pilulas.
    A prancha 1200 x 760 sobrava 102 unidades vazias a esquerda e 60 em cima;
    o viewBox passa a ser esta caixa, e a arte cresce e centra sozinha."""
    xs, ys = [], []
    for tid, pag, div, cx, cy, r, tit, normas in TEMAS:
        xs += [cx - r, cx + r]; ys += [cy - r, cy + r]
    for cx, cy, r in DISCOS + AROS_SOLTOS:
        xs += [cx - r, cx + r]; ys += [cy - r, cy + r]
    for p in pilulas(L):
        xs += [p['x0'], p['x1']]; ys += [p['y0'], p['y1']]
    x0, y0 = min(xs) - margem, min(ys) - margem
    return x0, y0, max(xs) + margem - x0, max(ys) + margem - y0
