# -*- coding: utf-8 -*-
"""Gera o PAR de arquivos de uma coluna da tira da home (a primeira secao):

    python _ferramentas/foto_coluna.py <cru.jpg> <assunto> [--ax 0.5] [--ay 0.5] [--gama 1.0]

  img/<assunto>-lum-qc.webp     luminancia 900 x 1120, sem perda: e o que o motor
                                js/trama.js desenha (a trama ao vivo com o rastro)
  img/<assunto>-bayer-qc.webp   633 x 788, ja tramada, para quem nao tem WebGL

POR QUE EXISTE (24/09/2026). Os arquivos -lum-qc de 18/09 nao saiam de nenhum
gerador: refazer-fotos-da-home.py so escreve a reserva -bayer. Mexer no
enquadramento la nao mudava nada na tela, porque o motor le a luminancia.
Este script escreve os dois de uma vez, com o mesmo enquadramento.

ENQUADRAMENTO: cover na proporcao da vaga (633:788), ancora --ax/--ay (0 = borda
esquerda/topo, 1 = direita/base). A coluna ISO espelha a imagem na tela (index.html,
`espelha`), entao o que esta a esquerda no arquivo aparece a direita.

TOM: a luminancia passa por --gama antes de gravar (1 = como veio). A curva da
casa e aplicada depois, pelo shader e pela reserva (gama 0,86, contraste 1,55,
brilho +0,35), a mesma das outras colunas."""

import os, sys
import numpy as np
from PIL import Image

SITE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(SITE, '_ferramentas', 'arcos'))
import manchas

LUM_W, LUM_H = 900, 1120
BAY_W, BAY_H = 633, 788
CORES = np.array([[21.2, 50.9, 80.6], [24.2, 56.2, 88.1], [103.0, 146.1, 189.4], [250, 249, 245]])


def enquadrar(im, W, H, ax, ay):
    w, h = im.size
    e = max(W / w, H / h)
    cw, ch = int(round(W / e)), int(round(H / e))
    x0 = int(round((w - cw) * ax)); y0 = int(round((h - ch) * ay))
    return im.crop((x0, y0, x0 + cw, y0 + ch)).resize((W, H), Image.LANCZOS)


def main(cru, assunto, ax=.5, ay=.5, gama=1.0):
    src = Image.open(cru).convert('L')
    img = os.path.join(SITE, 'img')
    lum_im = enquadrar(src, LUM_W, LUM_H, ax, ay)
    lum = np.clip(np.asarray(lum_im, dtype=np.float64) / 255, 0, 1) ** gama
    Image.fromarray((lum * 255).round().astype(np.uint8), 'L').save(
        os.path.join(img, '%s-lum-qc.webp' % assunto), lossless=True)
    bay_im = enquadrar(src, BAY_W, BAY_H, ax, ay)
    g = np.clip(np.asarray(bay_im, dtype=np.float64) / 255, 0, 1) ** gama
    m4 = np.array([[0, 8, 2, 10], [12, 4, 14, 6], [3, 11, 1, 9], [15, 7, 13, 5]])
    yy, xx = np.mgrid[0:BAY_H, 0:BAY_W]
    T = (m4[yy % 4, xx % 4] + .5) / 16
    k = np.clip(np.floor(manchas.tom(g) * 3 + T), 0, 3).astype(int)
    Image.fromarray(CORES[k].round().astype(np.uint8), 'RGB').save(
        os.path.join(img, '%s-bayer-qc.webp' % assunto), lossless=True)
    print('%s: lum %dx%d e bayer %dx%d, ax %.2f ay %.2f gama %.2f' % (assunto, LUM_W, LUM_H, BAY_W, BAY_H, ax, ay, gama))


if __name__ == '__main__':
    args = sys.argv[1:]
    opts = {'--ax': .5, '--ay': .5, '--gama': 1.0}
    for k in list(opts):
        if k in args:
            i = args.index(k); opts[k] = float(args[i + 1]); del args[i:i + 2]
    main(args[0], args[1], opts['--ax'], opts['--ay'], opts['--gama'])
