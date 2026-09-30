# -*- coding: utf-8 -*-
"""A tira panoramica no TINGIMENTO OFICIAL AZUL (30/09/2026).

    python _ferramentas/panorama_azul.py

«Volte o tingimento azulado que era antes no site, quero ver como fica com esta nova
configuracao.» A panoramica (img/tira-panorama-cor.webp, feita pelo panorama.py) sai
tambem no modo azul da tira antiga, o de antes do filtro em cor de 28/09:

  img/tira-panorama-lum.webp        a LUMINANCIA (Rec.709) da mestra, em cinza, sem perda:
                                    e o que o motor (js/trama.js, sem emCor) trama ao vivo,
                                    com a curva do tingimento oficial dentro do shader
                                    (gama .86, contraste 1,55, brilho .35) e a rampa
                                    14304C 336699 D3E2F2 FAF9F5 (escuro 1,4)
  img/tira-<servico>-bayer.webp     um quarto por card, 633 x 788, ja tramado (Bayer 4x4,
                                    4 niveis, ponto de 1 px): a reserva sem WebGL e o
                                    telefone. SEM o creme 1,06 embutido: na tira quem faz o
                                    min(creme, 1,06x) e o filtro CSS #foto-creme da .sh-foto.

A receita e a OFICIAL do _tingir-fotos/refazer-fotos-da-home.py (vaga qc)."""

import os
import numpy as np
from PIL import Image

SITE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG = os.path.join(SITE, 'img')
ORDEM = ['carbono', 'iso', 'smeta', 'esg']
CARD_W, CARD_H = 633, 788
RAMPA = ['14304C', '336699', 'D3E2F2', 'FAF9F5']
R = dict(gama=0.86, ctr=1.55, brilho=0.35, escuro=1.4, niveis=4, n=4)


def lumin(im):
    a = np.asarray(im.convert('RGB'), np.float32) / 255.0
    return 0.2126 * a[..., 0] + 0.7152 * a[..., 1] + 0.0722 * a[..., 2]


def tom(g):
    v = np.clip(np.power(g, R['gama']), 1e-6, 1 - 1e-6)
    p, q = np.power(v, R['ctr']), np.power(1 - v, R['ctr'])
    return np.clip(p / (p + q) + R['brilho'], 0, 1)


def lut_rampa():
    A = [np.array([int(h[i:i + 2], 16) for i in (0, 2, 4)], np.float32) for h in RAMPA]
    L = np.zeros((256, 3), np.float32)
    for i in range(256):
        u = i / 255
        if u < 0.78: u = 0.78 * (u / 0.78) ** (1 + R['escuro'] * 2)
        x = u * 3; k = min(2, int(x // 1)); t = x - k
        L[i] = A[k] * (1 - t) + A[k + 1] * t
    return L


def bayer(n):
    m = [[0]]
    while len(m) < n:
        k = len(m); o = [[0] * (2 * k) for _ in range(2 * k)]
        for y in range(k):
            for x in range(k):
                v = m[y][x] * 4
                o[y][x] = v; o[y][x + k] = v + 2; o[y + k][x] = v + 3; o[y + k][x + k] = v + 1
        m = o
    return (np.array(m, np.float32) + 0.5) / (n * n)


def tramar(g):
    v = tom(g); H, W = v.shape; M = bayer(R['n']); nv = R['niveis']
    T = M[np.arange(H) % R['n']][:, np.arange(W) % R['n']]
    v = np.clip(np.floor(v * (nv - 1) + T) / (nv - 1), 0, 1)
    L = lut_rampa()
    return Image.fromarray(np.clip(np.rint(L[np.rint(v * 255).astype(np.int32)]), 0, 255).astype(np.uint8), 'RGB')


mestra = Image.open(os.path.join(IMG, 'tira-panorama-cor.webp')).convert('RGB')
W, HM = mestra.size
g = lumin(mestra)
dest = os.path.join(IMG, 'tira-panorama-lum.webp')
Image.fromarray(np.clip(np.rint(g * 255), 0, 255).astype(np.uint8), 'L').save(dest, lossless=True)
print('%s  %dx%d  %d KB' % (os.path.basename(dest), W, HM, os.path.getsize(dest) // 1024))
for i, nome in enumerate(ORDEM):
    q = mestra.crop((round(i * W / 4.0), 0, round((i + 1) * W / 4.0), HM))
    q = q.resize((CARD_W, round(q.height * CARD_W / q.width)), Image.LANCZOS)
    q = q.crop((0, q.height - CARD_H, CARD_W, q.height)) if q.height >= CARD_H else q.resize((CARD_W, CARD_H), Image.LANCZOS)
    arq = os.path.join(IMG, 'tira-%s-bayer.webp' % nome)
    tramar(lumin(q)).save(arq, 'WEBP', lossless=True, quality=100, method=6)
    print('  %-28s %dx%d  %d KB' % (os.path.basename(arq), CARD_W, CARD_H, os.path.getsize(arq) // 1024))
