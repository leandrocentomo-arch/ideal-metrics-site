"""Fundo do Painel de normas com foto tingida (27/10/2026, «teste uma foto tingida atrás do painel mas que seja clara»).

Parte do -lum.webp de um banner do site (luminância crua) e aplica o TINGIMENTO OFICIAL, conta por conta igual ao
js/trama.js: gama 0,86, sigmoide de contraste 1,55, brilho +0,35, escuro 1,4 (só abaixo de 78% do tom), Bayer 4x4
com limiar (m+0,5)/16, quatro níveis e a rampa 14304C 336699 D3E2F2 FAF9F5. O clareamento («que seja clara») é o
VÉU creme por cima, no CSS, e não mexe na receita.

Uso: python _ferramentas/fundo_foto.py img/banner-estudos-pesquisa-lum.webp img/fundo-painel-foto.webp
     [--larg 1920 --alt 1080 --ancora 1]   (ancora: 0 = recorte à esquerda, 1 = à direita, .5 = centro)
"""
import sys, argparse
import numpy as np
from PIL import Image

RAMPA = ['14304C', '336699', 'D3E2F2', 'FAF9F5']
BAYER4 = np.array([[0, 8, 2, 10], [12, 4, 14, 6], [3, 11, 1, 9], [15, 7, 13, 5]], dtype=np.float64)


def tom(g, gama=.86, ctr=1.55, brilho=.35, escuro=1.4):
    v = np.clip(np.power(np.maximum(g, 0), gama), 1e-6, 1 - 1e-6)
    a, b = np.power(v, ctr), np.power(1 - v, ctr)
    w = np.clip(a / (a + b) + brilho, 0, 1)
    return np.where(w < .78, .78 * np.power(w / .78, 1 + 2 * escuro), w)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('entrada'); ap.add_argument('saida')
    ap.add_argument('--larg', type=int, default=1920); ap.add_argument('--alt', type=int, default=1080)
    ap.add_argument('--ancora', type=float, default=1.0)
    o = ap.parse_args()
    im = Image.open(o.entrada).convert('L')
    W, H = im.size
    alvo = o.larg / o.alt
    if W / H > alvo:   # recorta a largura na proporção da tela
        w = round(H * alvo); x = round((W - w) * o.ancora); im = im.crop((x, 0, x + w, H))
    else:
        h = round(W / alvo); y = round((H - h) / 2); im = im.crop((0, y, W, y + h))
    im = im.resize((o.larg, o.alt), Image.LANCZOS)
    g = np.asarray(im, dtype=np.float64) / 255
    t = tom(g)
    lim = (np.tile(BAYER4, (o.alt // 4 + 1, o.larg // 4 + 1))[:o.alt, :o.larg] + .5) / 16
    k = np.clip(np.floor(t * 3 + lim), 0, 3).astype(int)   # quatro níveis
    cores = np.array([[int(c[i:i + 2], 16) for i in (0, 2, 4)] for c in RAMPA], dtype=np.uint8)
    Image.fromarray(cores[k]).save(o.saida, 'WEBP', lossless=True, method=6)
    print(o.saida, o.larg, 'x', o.alt)


if __name__ == '__main__':
    main()
