# -*- coding: utf-8 -*-
"""Uma foto de pagina interna no TINGIMENTO AZUL (o oficial do site desde 02/10/2026).

    python _ferramentas/foto_azul.py <cru.jpg> <nome> [--larg 562 --alt 422] [--px 50 --py 50] [--gama 1.0]

Sai o par que o motor js/trama.js usa:
  img/<nome>-lum.webp     a luminancia (Rec.709), 1,6x a reserva: e o que o motor trama ao vivo
  img/<nome>-bayer.webp   a reserva ja tramada (Bayer 4x4, 4 niveis, ponto de 1 px), para quando nao ha WebGL
O tom e o de _ferramentas/tom_azul.json e a rampa e a da casa (14304C 336699 D3E2F2 FAF9F5, escuro 1,4),
os mesmos do _ferramentas/panorama_azul.py. --gama corrige a exposicao de UMA foto (fica gravada na luminancia)."""
import os, sys, json
import numpy as np
from PIL import Image

AQUI = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(AQUI)
TOM = json.load(open(os.path.join(AQUI, 'tom_azul.json'), encoding='utf-8'))
RAMPA = ['14304C', '336699', 'D3E2F2', 'FAF9F5']
ESCURO = 1.4


def arg(n, pad):
    a = sys.argv
    return type(pad)(a[a.index(n) + 1]) if n in a else pad


def tom(g):
    v = np.clip(np.power(g, TOM['gama']), 1e-6, 1 - 1e-6)
    p, q = np.power(v, TOM['ctr']), np.power(1 - v, TOM['ctr'])
    return np.clip(p / (p + q) + TOM['brilhoTom'], 0, 1)


def lut():
    A = [np.array([int(h[i:i + 2], 16) for i in (0, 2, 4)], np.float32) for h in RAMPA]
    L = np.zeros((256, 3), np.float32)
    for i in range(256):
        u = i / 255
        if u < 0.78: u = 0.78 * (u / 0.78) ** (1 + ESCURO * 2)
        x = u * 3; k = min(2, int(x // 1)); t = x - k
        L[i] = A[k] * (1 - t) + A[k + 1] * t
    return L


def recorte(im, W, H, px, py):
    e = max(W / im.width, H / im.height)
    r = im.resize((max(W, round(im.width * e)), max(H, round(im.height * e))), Image.LANCZOS)
    x0 = round((r.width - W) * px / 100.0); y0 = round((r.height - H) * py / 100.0)
    return r.crop((x0, y0, x0 + W, y0 + H))


def da_receita(receita, cru, nome):
    """02/10/2026: a foto do corpo da pagina pela receita da aba [ 08 ] do Spirit (tipo «foto da página»).

        python _ferramentas/foto_azul.py --receita receita.json <cru.jpg> <nome>

    A luminancia sai a 1,6x da vaga, com recorte, espelho, inclinacao, zoom e os ajustes da foto; a reserva
    e a mesma luminancia reduzida a vaga e tramada no tom padrao."""
    sys.path.insert(0, os.path.join(AQUI, 'banner'))
    import foto_banner
    R = json.load(open(receita, encoding='utf-8'))
    W, H = R.get('vaga', [562, 422])
    wl, hl = round(W * 1.6), round(H * 1.6)
    g, masc = foto_banner.luz_da_receita(cru, R, wl, hl, com_mascara=True)
    if masc is not None:      # 05/10: zoom negativo, a borda da foto esmaece para o creme, no tom das fotos do site
        tg = R.get('tingimento')
        T = foto_banner.tom_da_receita(R) if isinstance(tg, dict) else {'brilhoTom': TOM['brilhoTom'], 'gama': TOM['gama'], 'ctr': TOM['ctr'], 'escuro': TOM.get('escuro', 0)}
        g = foto_banner.passagem_no_tom(g, masc, T)
    L = Image.fromarray(np.uint8(np.clip(np.rint(g * 255), 0, 255)), 'L')
    L.convert('RGB').save(os.path.join(SITE, 'img', nome + '-lum.webp'), 'WEBP', quality=90, method=6)
    v = tom(np.asarray(L.resize((W, H), Image.LANCZOS), np.float32) / 255.0)
    M = np.array([[0, 8, 2, 10], [12, 4, 14, 6], [3, 11, 1, 9], [15, 7, 13, 5]], np.float32)
    T = (M[np.arange(H) % 4][:, np.arange(W) % 4] + .5) / 16
    v = np.clip(np.floor(v * 3 + T) / 3, 0, 1)
    Image.fromarray(np.uint8(np.clip(np.rint(lut()[np.rint(v * 255).astype(np.int32)]), 0, 255)), 'RGB').save(
        os.path.join(SITE, 'img', nome + '-bayer.webp'), 'WEBP', lossless=True, quality=100, method=6)
    for t in ('lum', 'bayer'):
        f = os.path.join(SITE, 'img', '%s-%s.webp' % (nome, t))
        print('%-28s %dx%d  %d KB' % (os.path.basename(f), *Image.open(f).size, os.path.getsize(f) // 1024))


def main():
    if '--receita' in sys.argv:
        i = sys.argv.index('--receita'); rec = sys.argv[i + 1]; del sys.argv[i:i + 2]
        return da_receita(rec, sys.argv[1], sys.argv[2])
    cru, nome = sys.argv[1], sys.argv[2]
    W, H = arg('--larg', 562), arg('--alt', 422)
    px, py, gama = arg('--px', 50.0), arg('--py', 50.0), arg('--gama', 1.0)
    im = Image.open(cru).convert('RGB')
    def luz(w, h):
        a = np.asarray(recorte(im, w, h, px, py), np.float32) / 255.0
        return np.power(0.2126 * a[..., 0] + 0.7152 * a[..., 1] + 0.0722 * a[..., 2], gama)
    wl, hl = round(W * 1.6), round(H * 1.6)
    Image.fromarray(np.uint8(np.clip(np.rint(luz(wl, hl) * 255), 0, 255)), 'L').convert('RGB').save(
        os.path.join(SITE, 'img', nome + '-lum.webp'), 'WEBP', quality=90, method=6)
    v = tom(luz(W, H))
    M = np.array([[0, 8, 2, 10], [12, 4, 14, 6], [3, 11, 1, 9], [15, 7, 13, 5]], np.float32)
    T = (M[np.arange(H) % 4][:, np.arange(W) % 4] + .5) / 16
    v = np.clip(np.floor(v * 3 + T) / 3, 0, 1)
    Image.fromarray(np.uint8(np.clip(np.rint(lut()[np.rint(v * 255).astype(np.int32)]), 0, 255)), 'RGB').save(
        os.path.join(SITE, 'img', nome + '-bayer.webp'), 'WEBP', lossless=True, quality=100, method=6)
    for t in ('lum', 'bayer'):
        f = os.path.join(SITE, 'img', '%s-%s.webp' % (nome, t))
        print('%-28s %dx%d  %d KB' % (os.path.basename(f), *Image.open(f).size, os.path.getsize(f) // 1024))


if __name__ == '__main__':
    main()
