# -*- coding: utf-8 -*-
"""A foto do terco direito da secao «Conhecimento» (22/09/2026).

Refinaria entre campo e ceu com nuvens. Quinta foto da vaga: barquinhos de papel
(tres versoes) e paginas de revista em leque foram recusados pelo Leandro.

    python _ferramentas/arcos/foto.py

ORIGEM. O cru fica em Ideal Metrics/_tingir-fotos/FOTOS/refinaria-campo-ceu.jpg
(1024 x 683), como manda a regra da casa.

TRAMA DA CASA, com GAMA 1,4 antes da curva do shader: com 1,0 o ceu e o campo
ficam ralos; com 1,9 as nuvens escuras pesam. Com 1,4 aparecem as nuvens, as
torres e o campo em trama media.

SEM CEU (22/09): «corte as nuvens do ceu». O enquadramento fica (recortar o alto
obrigaria o cover a AMPLIAR a foto); o que muda e o ceu, que vira creme. Ceu =
acima de y HORIZONTE e azulado (B - R > 25) ou claro e um pouco azulado (lum > 0,72 e
B - R > 8: a chaminé branca, neutra, fica), com a mascara
suavizada; as torres, cinzentas e mais escuras, ficam.

ENCAIXE. A pagina faz object-fit cover (vaga ~436 x 394 css numa tela de 1440;
a foto e 1,5:1, entao so os lados sao cortados). Ancora X 0,60 (monta.py): o
conjunto principal de torres fica no meio da vaga.

SAIDA em img/, para o motor ditherVivo, na largura do original (sem ampliar):
  conhecimento-foto-lum.webp     luminancia, sem perda
  conhecimento-foto-bayer.webp   a mesma ja tramada, para quem nao tem WebGL"""

import os, sys
import numpy as np
from PIL import Image, ImageFilter

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import manchas   # a curva de tom e a rampa

SITE = os.path.dirname(os.path.dirname(AQUI))
CRU = os.path.join(os.path.dirname(SITE), '_tingir-fotos', 'FOTOS', 'refinaria-campo-ceu.jpg')
GAMA = 1.4
HORIZONTE = 478


def main():
    cor = Image.open(CRU).convert('RGB')
    im = cor.convert('L')
    a = np.asarray(cor).astype(np.float64)
    lum = np.asarray(im, dtype=np.float64) / 255
    yy0 = np.arange(im.height)[:, None]
    ceu = ((a[..., 2] - a[..., 0] > 25) | ((lum > .72) & (a[..., 2] - a[..., 0] > 8))) & (yy0 < HORIZONTE)
    ceu = np.asarray(Image.fromarray((ceu * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(1.2)),
                     dtype=np.float64) / 255
    lum = lum ** GAMA
    lum = lum * (1 - ceu) + ceu
    img = os.path.join(SITE, 'img')
    Image.fromarray((lum * 255).round().astype(np.uint8), 'L').save(
        os.path.join(img, 'conhecimento-foto-lum.webp'), lossless=True)
    m4 = np.array([[0, 8, 2, 10], [12, 4, 14, 6], [3, 11, 1, 9], [15, 7, 13, 5]])
    yy, xx = np.mgrid[0:im.height, 0:im.width]
    T = (m4[yy % 4, xx % 4] + .5) / 16
    k = np.clip(np.floor(manchas.tom(lum) * 3 + T), 0, 3).astype(int)
    Image.fromarray(manchas.CORES[k].round().astype(np.uint8), 'RGB').save(
        os.path.join(img, 'conhecimento-foto-bayer.webp'), lossless=True)
    print('conhecimento-foto: %d x %d, gama %.1f' % (im.width, im.height, GAMA))


if __name__ == '__main__':
    main()
