# -*- coding: utf-8 -*-
"""A foto do terco direito da secao «Conhecimento» (22/09/2026).

Paginas de revista abertas em leque, em close. Escolhida pelo Leandro depois de
tres tentativas com barquinhos de papel (a trama apagava os barcos brancos, e o
duotom sem trama nao ficou bom).

    python _ferramentas/arcos/foto.py

ORIGEM. O cru fica em Ideal Metrics/_tingir-fotos/FOTOS/paginas-revista-leque.jpg
(2000 x 1333), como manda a regra da casa.

ESPELHADA. No original o lado direito e o mais claro; o Leandro pediu espelhar,
para o leque denso ficar a DIREITA e o lado claro encostar no esquema.

TRAMA DA CASA, sem ajuste: a foto tem tom de sobra (5% abaixo de 0,20, mediana
0,84), entao a curva do shader ja deixa o papel em creme e o leque em azul.
A pagina faz object-fit cover (vaga ~426 x 384 css numa tela de 1440; a foto e
1,5:1, entao so os lados sao cortados).

SAIDA em img/, para o motor ditherVivo:
  conhecimento-paginas-lum.webp     luminancia, sem perda, 1200 x 800
  conhecimento-paginas-bayer.webp   a mesma ja tramada, para quem nao tem WebGL"""

import os, sys
import numpy as np
from PIL import Image, ImageOps

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import manchas   # a curva de tom e a rampa

SITE = os.path.dirname(os.path.dirname(AQUI))
CRU = os.path.join(os.path.dirname(SITE), '_tingir-fotos', 'FOTOS', 'paginas-revista-leque.jpg')
LARG = 1200


def main():
    im = ImageOps.mirror(Image.open(CRU).convert('L'))
    im = im.resize((LARG, round(im.height * LARG / im.width)), Image.LANCZOS)
    lum = np.asarray(im, dtype=np.float64) / 255
    img = os.path.join(SITE, 'img')
    im.save(os.path.join(img, 'conhecimento-paginas-lum.webp'), lossless=True)
    m4 = np.array([[0, 8, 2, 10], [12, 4, 14, 6], [3, 11, 1, 9], [15, 7, 13, 5]])
    yy, xx = np.mgrid[0:im.height, 0:im.width]
    T = (m4[yy % 4, xx % 4] + .5) / 16
    k = np.clip(np.floor(manchas.tom(lum) * 3 + T), 0, 3).astype(int)
    Image.fromarray(manchas.CORES[k].round().astype(np.uint8), 'RGB').save(
        os.path.join(img, 'conhecimento-paginas-bayer.webp'), lossless=True)
    print('conhecimento-paginas: %d x %d, espelhada' % im.size)


if __name__ == '__main__':
    main()
