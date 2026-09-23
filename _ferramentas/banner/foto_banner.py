# -*- coding: utf-8 -*-
"""Foto no banner de uma pagina, no jeito do site da CQT: creme puro a esquerda,
onde se le o titulo, e a foto aparecendo sob a trama para a direita.

    python _ferramentas/banner/foto_banner.py <cru.jpg> <saida-lum.webp> [--gama 1.4]

COMO FUNCIONA. O motor js/trama.js recebe uma imagem de LUMINANCIA e faz a trama
Bayer da casa por pixel de tela. Entao o esvanecimento nao e opacidade: e a
propria luminancia que vai de 1 (creme, sem ponto nenhum) a esquerda para a foto
a direita. Assim o titulo fica sobre creme limpo e a foto nasce sem borda.

  x < INICIO          -> creme puro
  INICIO .. FIM       -> rampa suave (smoothstep) entre creme e foto
  x > FIM             -> a foto, com a gama aplicada

RECORTE. A faixa e larga (a vaga tem ~1900 x 300 css). A imagem sai em 3:1, e o
cover do motor corta o resto. O recorte pega a parte de baixo do quadro, onde
esta a operacao, e nao o ceu vazio."""

import os, sys
import numpy as np
from PIL import Image

AQUI = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(os.path.dirname(AQUI))
sys.path.insert(0, os.path.join(SITE, '_ferramentas', 'arcos'))
import manchas

LARG, ALT = 2400, 800          # 3:1, com folga para o cover
INICIO, FIM = .30, .78         # onde a foto comeca a aparecer e onde fica inteira
TOPO = .30                     # de onde cortar na vertical (0 = topo do original)


def main(cru, saida, gama=1.4):
    im = Image.open(cru).convert('L')
    # recorte 3:1, ancorado abaixo do topo
    alvo = LARG / ALT
    w, h = im.size
    if w / h > alvo:
        nw = round(h * alvo); x0 = (w - nw) // 2
        im = im.crop((x0, 0, x0 + nw, h))
    else:
        nh = round(w / alvo); y0 = min(max(0, round(h * TOPO)), h - nh)
        im = im.crop((0, y0, w, y0 + nh))
    im = im.resize((LARG, ALT), Image.LANCZOS)

    foto = np.clip(np.asarray(im, dtype=np.float64) / 255, 0, 1) ** gama
    x = (np.arange(LARG) + .5) / LARG
    t = np.clip((x - INICIO) / (FIM - INICIO), 0, 1)
    t = t * t * (3 - 2 * t)                      # smoothstep
    lum = 1 - t[None, :] * (1 - foto)            # 1 = creme; a foto entra pela direita

    Image.fromarray((lum * 255).round().astype(np.uint8), 'L').save(saida, lossless=True)
    # prova tramada, para conferir sem abrir o site
    m4 = np.array([[0, 8, 2, 10], [12, 4, 14, 6], [3, 11, 1, 9], [15, 7, 13, 5]])
    yy, xx = np.mgrid[0:ALT, 0:LARG]
    T = (m4[yy % 4, xx % 4] + .5) / 16
    k = np.clip(np.floor(manchas.tom(lum) * 3 + T), 0, 3).astype(int)
    prova = saida.replace('.webp', '-prova.png')
    Image.fromarray(manchas.CORES[k].round().astype(np.uint8), 'RGB').save(prova)
    print('%s: %d x %d, gama %.1f, creme ate %d%%' % (os.path.basename(saida), LARG, ALT, gama, INICIO * 100))
    print('prova:', prova)


if __name__ == '__main__':
    g = 1.4
    if '--gama' in sys.argv:
        i = sys.argv.index('--gama'); g = float(sys.argv[i + 1]); del sys.argv[i:i + 2]
    main(sys.argv[1], sys.argv[2], g)
