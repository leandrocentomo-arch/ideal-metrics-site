# -*- coding: utf-8 -*-
"""A foto do terco direito da secao «Conhecimento» (22/09/2026).

Os barquinhos de papel: um vermelho saindo na frente, a trilha tracejada e os
brancos atras. O Leandro pediu o corte pegando o barquinho vermelho.

    python _ferramentas/arcos/foto.py

ORIGEM. O cru fica em Ideal Metrics/_tingir-fotos/FOTOS/barquinhos-papel-vermelho.jpg
(1920 x 1020), como manda a regra da casa: sem ele nao se recalibra depois.

CORTE. Quadrado de 1020 x 1020 a partir de x = 420: o barco vermelho (centro em
x 665, y 327 no original) cai a 24% da largura, a trilha atravessa o quadro e os
brancos ocupam a direita e o pe. A vaga e quase quadrada (~420 x 394 css numa
tela de 1440); o motor faz object-fit cover com ancora X 0,15, entao numa vaga
mais estreita o corte come a DIREITA e o barco vermelho fica.

SAIDA em img/, como as outras pecas do motor ditherVivo:
  conhecimento-barco-lum.webp     luminancia, sem perda, 900 px
  conhecimento-barco-bayer.webp   a mesma ja tramada, para quem nao tem WebGL

COR. Passa pela trama da casa como toda foto do site: o vermelho vira o azul
mais escuro da rampa, e o barco continua sendo a peca mais escura do quadro.
O fundo cinza-claro do papel cai no creme.

NIVEIS. Direto na curva da casa (brilho +0,35) tudo acima de ~0,6 de
luminancia vira creme: a trilha (0,66 a 0,82) e os barcos brancos (0,79 a 0,87,
quase o fundo, 0,886) sumiam e sobrava so o vermelho. Por isso:
  1. esticar 0,62 -> 0 e 0,875 -> 1 (o fundo fica creme, a trilha aparece);
  2. os barcos brancos sao AZULADOS (B - R = 12,5) e o papel nao (1,0): a mascara
     de B - R, suavizada, da a eles um tom fixo, PROF_BRANCOS = 0,48, trama leve;
  3. piso de 0,30, para o vermelho nao virar um borrao chapado."""

import os, sys, shutil
import numpy as np
from PIL import Image, ImageFilter

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import manchas   # a curva de tom e a rampa

SITE = os.path.dirname(os.path.dirname(AQUI))
FOTOS = os.path.join(os.path.dirname(SITE), '_tingir-fotos', 'FOTOS')
CRU = os.path.join(FOTOS, 'barquinhos-papel-vermelho.jpg')
CORTE = (420, 0, 1440, 1020)
LADO = 900
PRETO, BRANCO, PROF_BRANCOS, PISO = .62, .875, .48, .30


def main(origem=None):
    if origem and not os.path.exists(CRU):
        shutil.copy2(origem, CRU)
    im = Image.open(CRU).convert('RGB').crop(CORTE).resize((LADO, LADO), Image.LANCZOS)
    a = np.asarray(im).astype(np.float64)
    bruta = np.asarray(im.convert('L'), dtype=np.float64) / 255
    def borra(x, r):
        return np.asarray(Image.fromarray(np.clip(x * 255, 0, 255).astype(np.uint8))
                          .filter(ImageFilter.GaussianBlur(r)), dtype=np.float64) / 255
    azul = np.clip((a[..., 2] - a[..., 0]) / 30, 0, 1)
    m = borra((borra(azul, 4) > 6 / 30).astype(np.float64), 1.5)
    esticada = np.clip((bruta - PRETO) / (BRANCO - PRETO), 0, 1)
    lum = np.maximum(np.minimum(esticada, 1 - PROF_BRANCOS * m), PISO)
    img = os.path.join(SITE, 'img')
    Image.fromarray((lum * 255).round().astype(np.uint8), 'L').save(
        os.path.join(img, 'conhecimento-barco-lum.webp'), lossless=True)
    m4 = np.array([[0, 8, 2, 10], [12, 4, 14, 6], [3, 11, 1, 9], [15, 7, 13, 5]])
    yy, xx = np.mgrid[0:LADO, 0:LADO]
    T = (m4[yy % 4, xx % 4] + .5) / 16
    k = np.clip(np.floor(manchas.tom(lum) * 3 + T), 0, 3).astype(int)
    Image.fromarray(manchas.CORES[k].round().astype(np.uint8), 'RGB').save(
        os.path.join(img, 'conhecimento-barco-bayer.webp'), lossless=True)
    print('conhecimento-barco: %d x %d, corte %s' % (LADO, LADO, CORTE))


if __name__ == '__main__':
    main(sys.argv[1] if len(sys.argv) > 1 else None)
