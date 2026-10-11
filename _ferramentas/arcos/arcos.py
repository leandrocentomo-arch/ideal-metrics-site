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
VB_W, VB_H = 1000, 600
PAD_X, PIL_H = 8, 20           # respiro lateral e altura da pilula, em unidades do viewBox
# 24/09: TODAS as etiquetas com a mesma largura, 62 unidades, menos as de nome
# muito grande, que crescem so o necessario (GHG Protocol, ABNT PR 2030,
# ISO/IEC 27001 e Observatorio setorial)
PIL_W = 62
TXT_PIL, TXT_TIT, LH_TIT = 8.5, 10.5, 12.5   # 22/09: titulo menor a pedido do Leandro (era 13)
# 21/09: etiqueta menor a pedido do Leandro (era 12,5 de corpo e 26 de altura).
# larguras.json foi medido a 12,5: a largura do texto escala linear com o corpo
ESC_PIL = TXT_PIL / 12.5
ESC_TIT = TXT_TIT / 19          # os titulos de larguras.json foram medidos a 19

# (id, pagina, divisao, cx, cy, r, linhas do titulo, [(norma, angulo em graus)])
# angulo: 0 = direita, 90 = baixo (y do SVG cresce para baixo)
TEMAS = [
 # 10/10/2026 (noite): OS DEZ TEMAS DO SITE (os mesmos da figura «Temas de gestao», da grade e do filtro), a pedido
 # do Leandro. «Sistemas de gestao ISO» continua o EIXO no meio, sem etiqueta propria: oito temas ENCOSTAM nele
 # (tangentes, a 45 graus um do outro) e a norma ISO de cada tema mora no ponto de contato (ISO 9001, 14001, 50001,
 # 22000, 37001, 39001, 45001 e ISO/IEC 27001). Fora do eixo, Sustentabilidade e ESG encosta em Responsabilidade
 # social pela SA 8000, e Estudos fica a parte. «Padroes de mercado» deixou de ser tema: FSC foi para Meio ambiente,
 # EcoVadis e IFC para Sustentabilidade e ESG. Segurança viaria (ISO 39001) entrou.
 ('iso', 'implantacao-iso.html', 'p', 420, 300, 120, ['Sistemas de', 'gestão ISO'], []),
 ('qualidade', 'norma-iso-9001.html', 'p', 420, 128, 52, ['Qualidade'],
    [('ISO 9001', 'cruza:iso:baixo'), ('ISO 41001', -135), ('IATF 16949', -45)]),
 ('ambiente', 'norma-iso-14001.html', 'p', 547, 173, 60, ['Meio', 'ambiente'],
    [('ISO 14001', 'cruza:iso:baixo'), ('FSC', -125), ('Rainforest Alliance', -40)]),
 ('carbono', 'gestao-carbono.html', 'p', 604, 300, 64, ['Clima e', 'carbono'],
    [('ISO 50001', 'cruza:iso:baixo'), ('GHG Protocol', -75), ('ISO 14064', -25), ('ISO 14068', 25), ('SBTi', 75)]),
 ('alimentos', 'seguranca-alimentos.html', 'p', 541.6, 421.6, 52, ['Segurança', 'de alimentos'],
    [('ISO 22000', 'cruza:iso:baixo'), ('FSSC 22000', 45)]),
 ('compliance', 'compliance-seguranca-informacao.html', 'p', 420, 472, 52, ['Compliance', 'e riscos'],
    [('ISO 37001', 'cruza:iso:baixo'), ('ISO 37301', 45), ('ISO 22301', 135)]),
 ('viaria', 'seguranca-viaria.html', 'p', 298.4, 421.6, 52, ['Segurança', 'viária'],
    [('ISO 39001', 'cruza:iso:baixo'), ('ISO 39002', 135)]),
 ('nrs', 'norma-iso-45001.html', 'p', 236, 300, 64, ['Saúde e', 'segurança', 'do trabalho'],
    [('ISO 45001', 'cruza:iso:baixo'), ('NR-01', 135), ('NR-12', 180), ('NR-17', -135)]),
 ('si', 'compliance-seguranca-informacao.html', 'p', 293, 173, 60, ['Segurança da', 'informação'],
    [('ISO/IEC 27001', 'cruza:iso:baixo'), ('ISO/IEC 27701', -150), ('LGPD', -100)]),
 ('esg', 'esg.html', 'p', 800, 225, 74, ['Sustentabilidade', 'e ESG'],
    [('ABNT PR 2030', -140), ('GRI', 140), ('IFRS S1 e S2', -90), ('EcoVadis', 90), ('IFC', 40)]),
 ('smeta', 'sedex-smeta.html', 'p', 898, 142, 54, ['Responsabilidade', 'social'],
    [('SA 8000', 'cruza:esg:baixo'), ('SMETA 7.0', -65)]),
 ('estudos', 'estudos-pesquisa.html', 'i', 850, 455, 62, ['Estudos e', 'pesquisa', 'aplicada'],
    [('Nota técnica', 90), ('Observatório setorial', -145), ('EUDR', -35)]),
]

# os pares que se tocam de proposito: a etiqueta da norma mora no ponto de contato
_SAT = ['qualidade', 'ambiente', 'carbono', 'alimentos', 'compliance', 'viaria', 'nrs', 'si']
CRUZAM = {frozenset((t, 'iso')) for t in _SAT} | {frozenset(('smeta', 'esg'))}

# 27/09/2026: «quero que encoste mas nao passe, apenas encoste os aros». O primeiro de cada par anda na linha dos
# centros ate a distancia ser exatamente a soma dos raios; o segundo fica. 10/10: os oito temas do eixo e o par
# Responsabilidade social / Sustentabilidade e ESG.
ENCOSTAR = [(t, 'iso') for t in _SAT] + [('smeta', 'esg')]
def _encosta():
    por = {t[0]: list(t) for t in TEMAS}
    for mov, fixo in ENCOSTAR:
        m, f = por[mov], por[fixo]
        dx, dy = m[3] - f[3], m[4] - f[4]
        d = math.hypot(dx, dy)
        m[3] = f[3] + dx / d * (m[5] + f[5]); m[4] = f[4] + dy / d * (m[5] + f[5])
    return [tuple(por[t[0]]) for t in TEMAS]
TEMAS = _encosta()

# manchas cheias por tras, independentes dos aros (como na referencia), todas
# DENTRO da prancha: a primeira versao deixava uma sair por baixo
# 22/09: manchas 20% menores e tudo mais junto (o esquema deixou de ocupar a largura da pagina)
DISCOS = [(360, 250, 88), (530, 390, 72), (230, 375, 64), (825, 170, 70), (880, 462, 58)]   # 10/10: refeitas para o desenho dos dez temas
# 21/09/2026: tres dos cinco discos em AZUL palido (o ISO, o do ESG com Padroes
# de mercado e o de Estudos), a pedido do Leandro: «quero que tenha partes em
# azul». Os outros dois ficam no bege da casa. Indices de DISCOS.
# 21/09 (noite): «esqueca o bege no diagrama»: TODAS as manchas na trama da do
# ISO (tom 0,95, ~15% de pontos azuis). Antes eram 0, 2 e 4 azuis e o resto bege.
DISCOS_AZUIS = set(range(len(DISCOS)))
# 21/09/2026: os aros soltos (sem rotulo, so ritmo, copiados da referencia)
# SAIRAM. O Leandro perguntou para que serviam, e a resposta era: para nada.
# Todo aro desta secao e um tema.
AROS_SOLTOS = []

def larguras():
    p = os.path.join(AQUI, 'larguras.json')
    return json.load(open(p, encoding='utf-8')) if os.path.exists(p) else {}


def aro(tid):
    for t in TEMAS:
        if t[0] == tid: return t[3], t[4], t[5]
    raise KeyError(tid)


def cruzamento(a, b, lado='baixo'):
    """um dos dois pontos onde os aros dos temas a e b se cruzam"""
    (x1, y1, r1), (x2, y2, r2) = aro(a), aro(b)
    d = math.hypot(x2 - x1, y2 - y1)
    if abs(d - (r1 + r2)) < 1e-6:          # tangentes (27/09): o ponto em que se tocam
        return (x1 + (x2 - x1) / d * r1, y1 + (y2 - y1) / d * r1)
    assert abs(r1 - r2) < d < r1 + r2, 'os aros de %s e %s nao se cruzam' % (a, b)
    k = (d * d + r1 * r1 - r2 * r2) / (2 * d)
    h = math.sqrt(r1 * r1 - k * k)
    mx, my = x1 + k * (x2 - x1) / d, y1 + k * (y2 - y1) / d
    p = [(mx + h * (y2 - y1) / d, my - h * (x2 - x1) / d), (mx - h * (y2 - y1) / d, my + h * (x2 - x1) / d)]
    return max(p, key=lambda q: q[1]) if lado == 'baixo' else min(p, key=lambda q: q[1])


def normas_de(tid):
    """as normas do tema, mais as que ele divide com outro aro no cruzamento"""
    out = []
    for t in TEMAS:
        for n, a in t[7]:
            if t[0] == tid or (isinstance(a, str) and a.split(':')[1] == tid):
                out.append(n)
    return out


def pilulas(L):
    """posicao e caixa de cada pilula, centrada NO aro"""
    out = []
    for tid, pag, div, cx, cy, r, tit, normas in TEMAS:
        for txt, ang in normas:
            w = max(PIL_W, L.get(txt, len(txt) * 6.6) * ESC_PIL + 2 * PAD_X)
            cruza = None
            if isinstance(ang, str):
                _, cruza, lado = ang.split(':')
                x, y = cruzamento(tid, cruza, lado)
            else:
                # a etiqueta fica centrada NA linha do aro. Por dentro so caberia
                # com texto minusculo: «Observatorio setorial» sozinha mede 95
                # unidades, quase o diametro do aro dela. O alinhamento vem dos
                # angulos, iguais em todos os temas (-160, -125, -90, -55, 55, 90,
                # 125, 160), e nao de encostar por dentro.
                t = math.radians(ang)
                x, y = cx + r * math.cos(t), cy + r * math.sin(t)
            out.append(dict(tema=tid, txt=txt, x=x, y=y, w=w, h=PIL_H, cruza=cruza,
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
            if tid == p['tema'] or tid == p.get('cruza'): continue
            d = math.hypot(p['x'] - cx, p['y'] - cy)
            if abs(d - r) < 34:
                ruim.append('pilula no aro alheio: %s perto do aro de %s (%.0f)' % (p['txt'], tid, abs(d - r)))
        for cx, cy, r in AROS_SOLTOS:
            d = math.hypot(p['x'] - cx, p['y'] - cy)
            if d < r + p['w'] / 2 + 8:
                ruim.append('pilula x aro solto: %s' % p['txt'])
    # titulo nao pode ser cortado pela linha de outro aro
    for t, tema in zip(T, TEMAS):
        for tid, pag, div, cx, cy, r, tit, normas in TEMAS:
            if tid == tema[0]: continue
            # distancia minima e maxima do centro do aro a caixa do titulo (exata)
            dx = max(t['x0'] - cx, 0, cx - t['x1']); dy = max(t['y0'] - cy, 0, cy - t['y1'])
            dmin = math.hypot(dx, dy)
            dmax = max(math.hypot(x - cx, y - cy) for x in (t['x0'], t['x1']) for y in (t['y0'], t['y1']))
            if dmin < r + 8 and dmax > r - 8:
                ruim.append('titulo cortado por aro: %s por %s (%.0f..%.0f, r %d)' % (tema[0], tid, dmin, dmax, r))
    # aros nao se sobrepoem (folga de 10), salvo compliance/si, que se cruzam para a LGPD
    for a in range(len(TEMAS)):
        for b in range(a + 1, len(TEMAS)):
            ta, tb = TEMAS[a], TEMAS[b]
            if frozenset((ta[0], tb[0])) in CRUZAM: continue
            d = math.hypot(ta[3] - tb[3], ta[4] - tb[4])
            if d < ta[5] + tb[5] + 10:
                ruim.append('aros encostam: %s / %s (%.0f de folga)' % (ta[0], tb[0], d - ta[5] - tb[5]))
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
                    ''.join('<span>%s</span>' % esc(n) for n in normas_de(tid))))
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
