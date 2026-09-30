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
R = dict(gama=0.86, ctr=1.55, brilho=0.20, escuro=1.4, niveis=4, n=4)   # 30/09 (noite): brilho .20 (o oficial e .35), igual a tira da pagina azul


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


def reforcar(m, g):
    """30/09: «escureca os moinhos e o vapor para aparecerem no azul». No azul, tudo acima de
    ~55%% de luminancia vira creme: o ceu (82%%), o vapor (mais claro que o ceu) e os moinhos
    (cinza de 53%%) sumiam. So a LUMINANCIA muda; a mestra em cor fica como esta.
      moinhos  pixel = ceu + a x (cinza do moinho - ceu), com a lido na reta ceu-cinza;
               entram so os pedacos acima e a esquerda dos tanques (tanques e predio ficam fora).
               Luminancia vai a MOINHO (22%%): azul medio.
      vapor    o que e mais claro que o ceu e se liga ao alto da foto, na metade de producao
               (x < 1300). Luminancia vai a VAPOR (42%%) na parte mais densa: pontinhos
               azul-claros sobre o ceu creme; nas bordas, na proporcao da densidade."""
    import cv2
    H, W = g.shape
    S = np.median(m[50:200, 1500:2000].reshape(-1, 3), axis=0)
    Ls = float(lumin(Image.fromarray(np.uint8(S[None, None, :]))).ravel()[0])
    out = g.copy()
    # moinhos
    y0, y1, x0, x1 = 600, 1060, 2380, 2900
    bx = m[y0:y1, x0:x1]
    # 30/09 (noite): os moinhos passaram a ser fotograficos (Flow), claros e com sombreado; em vez
    # da reta ceu-cinza, conta o que se afasta do ceu (o ceu e plano, --ceu-plano)
    dist = np.abs(bx - S).max(axis=2)
    a = np.clip((dist - 6) / 20.0, 0, 1)
    cand = (dist > 8)
    # so a faixa de ceu dos moinhos: entre o predio do SMETA (a esquerda) e os tanques (a direita),
    # acima dos paineis; sem isso os moinhos se ligam a paineis, tanques e predio num bloco so
    yy, xx = np.mgrid[0:cand.shape[0], 0:cand.shape[1]]
    cand &= (xx >= 60) & (xx < 440) & (yy < 410) & ~((xx < 95) & (yy > 320))
    cand = cand.astype(np.uint8)
    n, lab, st, _ = cv2.connectedComponentsWithStats(cand, connectivity=8)
    # os pedacos dos moinhos: sobem acima dos tanques (topo < linha 300 da caixa) e ficam a
    # esquerda deles (x < 420 da caixa); tanques, paineis e predio ficam fora
    altos = [i for i in range(1, n) if st[i, cv2.CC_STAT_AREA] > 20]
    moinho = np.isin(lab, altos)
    # (sem engrossar: os moinhos fotograficos ja tem a espessura certa)
    aa = np.clip(a, 0, 1) * moinho
    MOINHO, VAPOR = 0.40, 0.42         # moinho a 40%: azul medio-claro (22% com o desenho antigo, fino)
    reg = out[y0:y1, x0:x1]
    out[y0:y1, x0:x1] = reg * (1 - aa) + MOINHO * aa
    # vapor
    lum = g
    claro = (lum > Ls + 0.007)
    perto = np.abs(m - S).max(axis=2) < 16
    regiao = ((claro | perto) & (np.arange(H)[:, None] < int(0.75 * H)) & (np.arange(W)[None, :] < 1300)).astype(np.uint8)
    n, lab = cv2.connectedComponents(regiao, connectivity=4)
    ceu = np.isin(lab, np.unique(lab[0][lab[0] > 0]))
    av = np.clip((lum - Ls - 0.007) / 0.07, 0, 1) * ceu
    av = cv2.GaussianBlur(av.astype(np.float32), (0, 0), 1.0)
    out = out * (1 - av) + VAPOR * av
    print('reforco: moinhos %d px, vapor %d px (ceu a %.2f de luminancia)' % (int(moinho.sum()), int((av > 0.1).sum()), Ls))
    return out


mestra = Image.open(os.path.join(IMG, 'tira-panorama-cor.webp')).convert('RGB')
W, HM = mestra.size
g = reforcar(np.asarray(mestra, np.float64), lumin(mestra))
dest = os.path.join(IMG, 'tira-panorama-lum.webp')
Image.fromarray(np.clip(np.rint(g * 255), 0, 255).astype(np.uint8), 'L').save(dest, lossless=True)
print('%s  %dx%d  %d KB' % (os.path.basename(dest), W, HM, os.path.getsize(dest) // 1024))
for i, nome in enumerate(ORDEM):
    q = Image.fromarray(np.clip(g * 255, 0, 255).astype(np.uint8), 'L').crop((round(i * W / 4.0), 0, round((i + 1) * W / 4.0), HM))
    q = q.resize((CARD_W, round(q.height * CARD_W / q.width)), Image.LANCZOS)
    q = q.crop((0, q.height - CARD_H, CARD_W, q.height)) if q.height >= CARD_H else q.resize((CARD_W, CARD_H), Image.LANCZOS)
    arq = os.path.join(IMG, 'tira-%s-bayer.webp' % nome)
    tramar(np.asarray(q, np.float32) / 255.0).save(arq, 'WEBP', lossless=True, quality=100, method=6)
    print('  %-28s %dx%d  %d KB' % (os.path.basename(arq), CARD_W, CARD_H, os.path.getsize(arq) // 1024))
