# -*- coding: utf-8 -*-
"""A foto do terco direito da secao «Conhecimento» (22/09/2026).

Piramide de bonecos de papel, de maos dadas. Sexta foto da vaga: barquinhos de
papel (tres versoes), paginas de revista em leque e refinaria foram recusados
pelo Leandro.

    python _ferramentas/arcos/foto.py

ORIGEM. O cru fica em Ideal Metrics/_tingir-fotos/FOTOS/piramide-bonecos-papel.jpg
(480 x 720, vertical), como manda a regra da casa.

ESPELHADA, a pedido do Leandro.

INTEIRA NA VAGA. A foto e vertical (2:3) e a vaga quase quadrada (~436 x 394 css
numa tela de 1440): no cover ela perderia a cabeca do boneco de cima e a base.
Por isso a luminancia sai com fundo branco na PROPORCAO DA VAGA (VAGA), com a
piramide inteira no meio; o cover da pagina entao nao corta nada. O fundo da foto
ja e branco (mediana 1,0), e branco vira creme na trama: sem borda nenhuma.

TRAMA DA CASA, com lum = (lum / 0,96) ^ GAMA e GAMA 2,2: com 1,0 os bonecos de
baixo, azul-claro, sumiam; com 1,5 ainda falhavam; com 2,2 aparecem todos.
MAIS CLARA (22/09): os bonecos ficaram escuros demais, entao a luminancia ganha
um PISO de 0,30 (lum = 0,30 + 0,70 x lum): some o azul-tinta e fica a trama
clara. Com piso 0,45 os bonecos de baixo sumiam.

SAIDA em img/, para o motor ditherVivo:
  conhecimento-foto-lum.webp     luminancia, sem perda
  conhecimento-foto-bayer.webp   a mesma ja tramada, para quem nao tem WebGL"""

import os, sys
import numpy as np
from PIL import Image, ImageOps

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import manchas   # a curva de tom e a rampa

SITE = os.path.dirname(os.path.dirname(AQUI))
CRU = os.path.join(os.path.dirname(SITE), '_tingir-fotos', 'FOTOS', 'piramide-bonecos-papel.jpg')
GAMA = 2.2
PISO = .30   # 22/09: «os bonecos estao muito escuros»: nada abaixo de 0,30
VAGA = 262 / 473          # largura / altura da vaga numa tela de 1440 (22/09: esquema em 4/5, foto em 1/5)


def main():
    im = ImageOps.mirror(Image.open(CRU).convert('L'))
    l = PISO + (1 - PISO) * np.clip(np.asarray(im, dtype=np.float64) / 255 / .96, 0, 1) ** GAMA
    # fundo branco na proporcao da vaga: mais largo que a foto -> sobra dos
    # lados; mais estreito -> sobra em CIMA. A foto nunca e cortada.
    if im.width / im.height < VAGA:
        h = im.height; w = round(h * VAGA)
    else:
        w = im.width; h = round(w / VAGA)
    lum = np.ones((h, w))
    # 22/09: «alinhe a figura da direita no bottom com o painel mosaico»: a sobra
    # vertical vai TODA para cima, entao a base da piramide fica na linha de baixo
    # do esquema. A sobra horizontal continua dividida, com a piramide centrada.
    x0, y0 = (w - im.width) // 2, h - im.height
    lum[y0:y0 + im.height, x0:x0 + im.width] = l
    img = os.path.join(SITE, 'img')
    Image.fromarray((lum * 255).round().astype(np.uint8), 'L').save(
        os.path.join(img, 'conhecimento-foto-lum.webp'), lossless=True)
    m4 = np.array([[0, 8, 2, 10], [12, 4, 14, 6], [3, 11, 1, 9], [15, 7, 13, 5]])
    yy, xx = np.mgrid[0:h, 0:w]
    T = (m4[yy % 4, xx % 4] + .5) / 16
    k = np.clip(np.floor(manchas.tom(lum) * 3 + T), 0, 3).astype(int)
    Image.fromarray(manchas.CORES[k].round().astype(np.uint8), 'RGB').save(
        os.path.join(img, 'conhecimento-foto-bayer.webp'), lossless=True)
    print('conhecimento-foto: %d x %d, espelhada, gama %.1f, piso %.2f' % (w, h, GAMA, PISO))


if __name__ == '__main__':
    main()
