# -*- coding: utf-8 -*-
"""A foto do terco direito da secao «Conhecimento» (22/09/2026).

Os barquinhos de papel: um vermelho saindo na frente, a trilha tracejada e seis
brancos atras. Recorte feito pelo proprio Leandro.

    python _ferramentas/arcos/foto.py

ORIGEM. O cru fica em Ideal Metrics/_tingir-fotos/FOTOS/
barquinhos-papel-vermelho-recorte.jpg (1332 x 784), como manda a regra da casa.

DUOTOM, NAO TRAMA. Na trama Bayer os barcos brancos perdiam a definicao: a face
iluminada deles tem o mesmo cinza do papel (0,87), e a curva da casa leva os dois
ao creme. Aqui o tom e continuo, do azul-tinta #14304C ao creme #FAF9F5:
  lum 0,20 ou menos -> azul-tinta   (o barco vermelho, que fica azul-escuro)
  lum do fundo      -> creme        (o papel some no fundo da secao)
As dobras e as sombras dos brancos ficam, porque nada vira ponto.
O papel e nivelado (dividido pela propria luz, desfoque de 60 px) e as bordas se
esfumam em 36 px: sem isso a foto aparecia como um retangulo cinza.
Sem o motor da trama, entao sem rastro do mouse nesta peca.

ENCAIXE. A pagina mostra a foto INTEIRA, na proporcao dela, sem preencher a vaga
(object-fit: contain em monta.py): «sem mexer na proporcao, sem preencher o
espaco todo».

SAIDA: img/conhecimento-barco.webp, WebP q88, 900 px de largura (a vaga tem ~426
css numa tela de 1440; 900 cobre tela de densidade 2)."""

import os
import numpy as np
from PIL import Image, ImageFilter

AQUI = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(os.path.dirname(AQUI))
CRU = os.path.join(os.path.dirname(SITE), '_tingir-fotos', 'FOTOS', 'barquinhos-papel-vermelho-recorte.jpg')
ESCURO, CREME = np.array([20, 48, 76.]), np.array([250, 249, 245.])
PRETO, LARG = .20, 900


def main():
    im = Image.open(CRU).convert('RGB')
    im = im.resize((LARG, round(im.height * LARG / im.width)), Image.LANCZOS)
    l = np.asarray(im.convert('L'), dtype=np.float64) / 255
    # o papel nao e uniforme (clareia a esquerda, acinzenta a direita) e desenhava
    # um retangulo cinza sobre o creme da secao. A luz do papel e estimada com um
    # desfoque largo dos pixels claros (os barcos entram pouco) e dividida fora.
    claro = np.where(l > .6, l, np.percentile(l, 50))
    papel = np.asarray(Image.fromarray((claro * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(60)),
                       dtype=np.float64) / 255
    plano = l / np.maximum(papel, .05)
    branco = np.percentile(plano, 50) - .015   # abaixo da mediana: o papel satura no creme
    t = np.clip((plano - PRETO) / (branco - PRETO), 0, 1)
    # bordas esfumadas no creme, 36 px, para a foto nao ter contorno nenhum
    h, w = t.shape
    yy, xx = np.mgrid[0:h, 0:w]
    borda = np.minimum(np.minimum(xx, w - 1 - xx), np.minimum(yy, h - 1 - yy))
    t = 1 - (1 - t) * np.clip(borda / 36, 0, 1)
    rgb = ESCURO + (CREME - ESCURO) * t[..., None]
    dst = os.path.join(SITE, 'img', 'conhecimento-barco.webp')
    Image.fromarray(rgb.round().astype(np.uint8), 'RGB').save(dst, quality=88)
    print('img/conhecimento-barco.webp: %d x %d, duotom, papel em %.3f' % (im.width, im.height, branco))


if __name__ == '__main__':
    main()
