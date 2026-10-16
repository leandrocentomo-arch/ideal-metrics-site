# -*- coding: utf-8 -*-
"""O PASSARO DA IDEAL METRICS NO BANNER, tramado, com zoom e as asas cortadas (15/10/2026).

    python _ferramentas/banner/passaro_banner.py [saida-lum.webp] [--prova prova.png]

«encaixe o passaro da ideal metrics com as tramas aplicadas no banner de todos os servicos, faca zoom, com as asas
cortadas». O passaro solo (img/passaro-ideal-m.svg, o grupo do passaro do 18Asset 253) e renderizado grande e
posto na area da foto do banner (os 2/3 da direita, como nas receitas do Spirit), com o olho dentro da faixa e as
pontas das asas passando das bordas (cima, direita e baixo). Para a trama aparecer, o passaro nao e tinta chapada:
o tom vai do mais escuro no olho ao mais claro nas pontas das penas. A passagem para o creme e a do banner (no TOM),
pela mesma conta do foto_banner.py.

Saida padrao: img/banner-todos-servicos-passaro-lum.webp (2400 x 800, 3:1)."""
import os, sys
import numpy as np
from PIL import Image

AQUI = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(os.path.dirname(AQUI))
sys.path.insert(0, AQUI)
import foto_banner as FB

SVG = os.path.join(SITE, 'img', 'passaro-ideal-m.svg')
SAIDA = os.path.join(SITE, 'img', 'banner-todos-servicos-passaro-lum.webp')
LARG, ALT = FB.LARG, FB.ALT
AREA = .67                          # a foto (aqui, o passaro) ocupa os 2/3 da direita
LARGURA_PASSARO = 2200              # o passaro inteiro, em px do banner de 2400: maior que a area, as asas saem
OLHO_ALVO = (.62, 360)              # onde fica o olho: fracao da area da foto (x) e px do banner (y)
OLHO_NO_SVG = (400.79, 45.33)       # o olho, no viewBox do svg (287.02 0 213.17 104.07)
VB = (287.02, 0.0, 213.17, 104.07)
TOM_OLHO, TOM_PONTA = .04, .42      # luminancia do passaro: escuro no olho, claro nas pontas
PASSAGEM = {'inicio': 0, 'fim': .35, 'suave': 1.0}
TOM = {'brilho_do_tom': .3, 'gama': .91, 'contraste': 1.05, 'escuro': .1, 'veu_creme': .03}


def renderiza(larg):
    alt = int(round(larg * VB[3] / VB[2]))
    svg = open(SVG, encoding='utf-8').read().split('?>', 1)[-1]
    svg = svg.replace('<svg ', '<svg width="%d" height="%d" ' % (larg, alt), 1)
    from playwright.sync_api import sync_playwright
    with sync_playwright() as pw:
        b = pw.chromium.launch()
        pg = b.new_page(viewport={'width': larg, 'height': alt})
        pg.set_content('<html><body style="margin:0;background:#fff">%s</body></html>' % svg)
        tmp = os.path.join(AQUI, '_passaro_tmp.png')
        pg.screenshot(path=tmp, clip={'x': 0, 'y': 0, 'width': larg, 'height': alt})
        b.close()
    a = np.asarray(Image.open(tmp).convert('L'), np.float64) / 255
    os.remove(tmp)
    return 1 - a                      # 1 = passaro, 0 = fundo


def main(saida=SAIDA, prova=None):
    m = renderiza(LARGURA_PASSARO); bh, bw = m.shape
    esc = bw / VB[2]
    ox, oy = (OLHO_NO_SVG[0] - VB[0]) * esc, (OLHO_NO_SVG[1] - VB[1]) * esc
    PW = int(round(LARG * AREA)); X0 = LARG - PW
    ex, ey = X0 + OLHO_ALVO[0] * PW, OLHO_ALVO[1]
    x0, y0 = int(round(ex - ox)), int(round(ey - oy))          # canto do passaro no banner
    masc = np.zeros((ALT, LARG))
    sx0, sy0 = max(0, -x0), max(0, -y0)
    dx0, dy0 = max(0, x0), max(0, y0)
    w = min(bw - sx0, LARG - dx0); h = min(bh - sy0, ALT - dy0)
    masc[dy0:dy0 + h, dx0:dx0 + w] = m[sy0:sy0 + h, sx0:sx0 + w]
    # o tom do passaro: escuro no olho, clareando para as pontas das penas
    yy, xx = np.mgrid[0:ALT, 0:LARG]
    d = np.hypot(xx - ex, yy - ey) / (LARGURA_PASSARO * .55)
    base = TOM_OLHO + (TOM_PONTA - TOM_OLHO) * np.clip(d, 0, 1) ** .8
    foto = 1 - masc * (1 - base)
    # a passagem para o creme, medida na largura da area, no TOM do banner (a conta do foto_banner)
    x = (np.arange(LARG) + .5 - X0) / PW
    t = np.clip((x - PASSAGEM['inicio']) / (PASSAGEM['fim'] - PASSAGEM['inicio']), 0, 1)
    t = (t * t * (3 - 2 * t)) ** PASSAGEM['suave']
    tt = np.broadcast_to(t[None, :], foto.shape)
    R = {'tingimento': dict(TOM)}
    lum = FB.passagem_no_tom(foto, tt, FB.tom_da_receita(R))
    Image.fromarray((np.clip(lum, 0, 1) * 255).round().astype(np.uint8), 'L').save(saida, lossless=True)
    print('%s: %d x %d' % (os.path.basename(saida), LARG, ALT))
    if prova:
        m4 = np.array([[0, 8, 2, 10], [12, 4, 14, 6], [3, 11, 1, 9], [15, 7, 13, 5]])
        kk = np.clip(np.floor(FB.manchas.tom(lum) * 3 + (m4[yy % 4, xx % 4] + .5) / 16), 0, 3).astype(int)
        Image.fromarray(FB.manchas.CORES[kk].round().astype(np.uint8), 'RGB').save(prova)
        print('prova:', prova)


if __name__ == '__main__':
    pv = None
    if '--prova' in sys.argv:
        i = sys.argv.index('--prova'); pv = sys.argv[i + 1]; del sys.argv[i:i + 2]
    main(sys.argv[1] if len(sys.argv) > 1 else SAIDA, pv)
