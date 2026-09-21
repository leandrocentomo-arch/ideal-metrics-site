# -*- coding: utf-8 -*-
"""As manchas da secao «Conhecimento» viram imagem, para o motor ditherVivo.

POR QUE. O Leandro pediu as manchas mais escuras e com o mesmo rastro do mouse
das fotos da primeira secao. Esse rastro e do motor ditherVivo do index.html:
ele recebe uma imagem de LUMINANCIA, passa pela curva de tom da casa, trama em
Bayer 4x4 por pixel de tela nas quatro cores da rampa, e engrossa a trama onde o
mouse passa. A folha da secao Demandas ja usa o motor assim, com imagem gerada.

O QUE SAI em img/:
  conhecimento-manchas-lum.webp    luminancia, sem perda, que o motor le
  conhecimento-manchas-bayer.webp  a mesma coisa ja tramada, para quem nao tem
                                   WebGL (e para o primeiro quadro)

TOM. O fundo sai em luminancia 1, que a curva leva ao creme puro: fora das
manchas, nada de trama. Dentro, o tom-alvo e escolhido NA SAIDA e a curva e
invertida para achar a luminancia, como o gerador da folha fez:
  mancha azul   tom 0,84  -> 48% dos pontos na azul clara da rampa
  mancha bege   tom 0,90  -> 30%
  cruzamento    o mais escuro dos dois, menos 0,03
A curva e a do shader: tom = sigmoide(g^0,86, contraste 1,55) + 0,35.

A imagem tem a MESMA caixa do viewBox do SVG, entao cada mancha cai exatamente
onde estava o circulo."""

import math, os, sys
import numpy as np
from PIL import Image

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import arcos

SITE = os.path.dirname(os.path.dirname(AQUI))
GAMA, CTR, BRILHO = .86, 1.55, .35
TOM_AZUL, TOM_BEGE, CRUZA = .84, .90, .03
# a rampa da folha Demandas (e da tira da 1a secao), ja passada pelo filtro creme
CORES = np.array([[21.2, 50.9, 80.6], [24.2, 56.2, 88.1], [103.0, 146.1, 189.4], [250, 249, 245]])
LARG = 1350          # 1080 px css da vaga vezes 1,25, como as outras imagens tramadas


def tom(g):
    v = np.clip(np.power(np.maximum(g, 0), GAMA), 1e-6, 1 - 1e-6)
    a, b = np.power(v, CTR), np.power(1 - v, CTR)
    return np.clip(a / (a + b) + BRILHO, 0, 1)


def lum_para(alvo):
    """inverte a curva: acha g com tom(g) = alvo, por bissecao"""
    lo, hi = 0.0, 1.0
    for _ in range(60):
        m = (lo + hi) / 2
        if tom(np.array(m)) < alvo: lo = m
        else: hi = m
    return (lo + hi) / 2


def main():
    L = arcos.larguras()
    x0, y0, w, h = arcos.limites(L)
    H = int(round(LARG * h / w))
    s = LARG / w
    yy, xx = np.mgrid[0:H, 0:LARG].astype(np.float64)
    ux, uy = xx / s + x0, yy / s + y0          # centro do pixel em unidades do viewBox
    ux += .5 / s; uy += .5 / s
    alvo = np.ones((H, LARG))                  # 1 = creme, sem trama
    for k, (cx, cy, r) in enumerate(arcos.DISCOS):
        dentro = (ux - cx) ** 2 + (uy - cy) ** 2 <= r * r
        t = TOM_AZUL if k in arcos.DISCOS_AZUIS else TOM_BEGE
        ja = dentro & (alvo < 1)
        alvo = np.where(ja, np.minimum(alvo, t) - CRUZA, np.where(dentro, np.minimum(alvo, t), alvo))
    # alvo -> luminancia, por tabela (a curva e monotona)
    tabela = {t: lum_para(t) for t in np.unique(alvo) if t < 1}
    lum = np.ones_like(alvo)
    for t, g in tabela.items():
        lum[alvo == t] = g
    img = os.path.join(SITE, 'img')
    Image.fromarray((lum * 255).round().astype(np.uint8), 'L').save(
        os.path.join(img, 'conhecimento-manchas-lum.webp'), lossless=True)

    # a reserva tramada: mesma conta do shader, Bayer 4x4 por pixel
    m4 = np.array([[0, 8, 2, 10], [12, 4, 14, 6], [3, 11, 1, 9], [15, 7, 13, 5]])
    T = (m4[yy.astype(int) % 4, xx.astype(int) % 4] + .5) / 16
    v = tom((lum * 255).round() / 255)
    k = np.clip(np.floor(v * 3 + T), 0, 3).astype(int)
    Image.fromarray(CORES[k].round().astype(np.uint8), 'RGB').save(
        os.path.join(img, 'conhecimento-manchas-bayer.webp'), lossless=True)

    print('manchas: %d x %d | tons %s' % (LARG, H, {round(t, 2): round(g, 3) for t, g in tabela.items()}))
    for t in sorted(tabela):
        print('  tom %.2f -> %2.0f%% de pontos azuis' % (t, 100 * (1 - (t * 3 - 2))))
    return LARG, H


if __name__ == '__main__':
    main()
