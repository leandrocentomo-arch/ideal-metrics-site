# -*- coding: utf-8 -*-
"""Foto no banner de uma pagina, no jeito do site da CQT: creme puro a esquerda,
onde se le o titulo, e a foto aparecendo sob a trama para a direita.

    python _ferramentas/banner/foto_banner.py <cru.jpg> <saida-lum.webp> [--gama 1.4]

COMO FUNCIONA. O motor js/trama.js recebe uma imagem de LUMINANCIA e faz a trama
Bayer da casa por pixel de tela. Entao o esvanecimento nao e opacidade: e a
propria luminancia que vai de 1 (creme, sem ponto nenhum) a esquerda para a foto
a direita. Assim o titulo fica sobre creme limpo e a foto nasce sem borda.

  x < INICIO          -> creme puro
  INICIO .. FIM       -> rampa suave (smoothstep) entre creme e foto
  x > FIM             -> a foto, com a gama aplicada

RECORTE. A faixa e larga (a vaga tem ~1900 x 300 css). A imagem sai em 3:1, e o
cover do motor corta o resto. O recorte pega a parte de baixo do quadro, onde
esta a operacao, e nao o ceu vazio."""

import os, sys
import numpy as np
from PIL import Image

AQUI = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(os.path.dirname(AQUI))
sys.path.insert(0, os.path.join(SITE, '_ferramentas', 'arcos'))
import manchas

LARG, ALT = 2400, 800          # 3:1, com folga para o cover
INICIO, FIM = .30, .78         # onde a foto comeca a aparecer e onde fica inteira
TOPO = .30                     # de onde cortar na vertical (0 = topo do original)


def main(cru, saida, gama=1.4, inicio=INICIO, fim=FIM, suave=1.0):
    im = Image.open(cru).convert('L')
    # recorte 3:1, ancorado abaixo do topo
    alvo = LARG / ALT
    w, h = im.size
    if w / h > alvo:
        nw = round(h * alvo); x0 = (w - nw) // 2
        im = im.crop((x0, 0, x0 + nw, h))
    else:
        nh = round(w / alvo); y0 = min(max(0, round(h * TOPO)), h - nh)
        im = im.crop((0, y0, w, y0 + nh))
    im = im.resize((LARG, ALT), Image.LANCZOS)

    foto = np.clip(np.asarray(im, dtype=np.float64) / 255, 0, 1) ** gama
    x = (np.arange(LARG) + .5) / LARG
    t = np.clip((x - inicio) / (fim - inicio), 0, 1)
    t = t * t * (3 - 2 * t)                      # smoothstep
    # 02/10/2026: «o corte entre a foto e a parte escrita esta muito acentuado, mais smooth». --suave > 1
    # atrasa a entrada da foto (t elevado a potencia): foto escura deixa de nascer de uma vez
    t = t ** suave
    lum = 1 - t[None, :] * (1 - foto)            # 1 = creme; a foto entra pela direita

    Image.fromarray((lum * 255).round().astype(np.uint8), 'L').save(saida, lossless=True)
    # prova tramada, para conferir sem abrir o site
    m4 = np.array([[0, 8, 2, 10], [12, 4, 14, 6], [3, 11, 1, 9], [15, 7, 13, 5]])
    yy, xx = np.mgrid[0:ALT, 0:LARG]
    T = (m4[yy % 4, xx % 4] + .5) / 16
    k = np.clip(np.floor(manchas.tom(lum) * 3 + T), 0, 3).astype(int)
    prova = saida.replace('.webp', '-prova.png')
    Image.fromarray(manchas.CORES[k].round().astype(np.uint8), 'RGB').save(prova)
    print('%s: %d x %d, gama %.1f, creme ate %d%%' % (os.path.basename(saida), LARG, ALT, gama, INICIO * 100))
    print('prova:', prova)


def _caixa(a, r):
    """Media em caixa de raio r, com a borda repetida (a mesma conta da aba [ 08 ] do Spirit)."""
    if r < 1: return a
    n = 2 * r + 1
    for eixo in (1, 0):
        p = np.pad(a, [(r + 1, r) if e == eixo else (0, 0) for e in (0, 1)], mode='edge')
        c = np.cumsum(p, axis=eixo)
        a = (np.take(c, range(n, c.shape[eixo]), axis=eixo) - np.take(c, range(0, c.shape[eixo] - n), axis=eixo)) / n
    return a


def luz_da_receita(cru, R, LARG, ALT):
    """A foto enquadrada e ajustada pela receita do Spirit, em luminancia 0..1, no tamanho LARG x ALT.
    Serve ao banner (2400 x 800, depois vem a passagem para o creme) e a foto do corpo da pagina (foto_azul.py)."""
    q, a = R['tamanho_e_posicao'], R['ajustes_da_foto']
    im = Image.open(cru).convert('RGB')
    cl, cr, ct, cb = [q.get(k, 0) / 100 for k in ('corte_esq', 'corte_dir', 'corte_topo', 'corte_base')]
    if cl or cr or ct or cb:                                            # o recorte vem antes de tudo
        im = im.crop((round(cl * im.width), round(ct * im.height), max(round(cl * im.width) + 1, round((1 - cr) * im.width)),
                      max(round(ct * im.height) + 1, round((1 - cb) * im.height))))
    if q.get('espelhar'): im = im.transpose(Image.FLIP_LEFT_RIGHT)      # o enquadramento vale sobre a foto ja espelhada
    ang = q.get('inclinar', 0)
    if not ang:
        e = max(LARG / im.width, ALT / im.height) * q.get('zoom', 1)
        ox, oy = (LARG - im.width * e) * q.get('px', 50) / 100, (ALT - im.height * e) * q.get('py', 50) / 100
        im = im.resize((LARG, ALT), Image.LANCZOS, box=(-ox / e, -oy / e, (LARG - ox) / e, (ALT - oy) / e))
    else:
        # inclinada: gira em torno do centro da faixa e cresce o bastante para nao sobrar canto vazio (a `poe` da aba)
        import math
        co, si = math.cos(math.radians(ang)), math.sin(math.radians(ang))
        rw, rh = LARG * abs(co) + ALT * abs(si), LARG * abs(si) + ALT * abs(co)
        e = max(rw / im.width, rh / im.height) * q.get('zoom', 1)
        dw, dh = im.width * e, im.height * e
        if e < 1:                                   # reduz antes, para a rotacao nao serrilhar
            im = im.resize((max(1, round(dw)), max(1, round(dh))), Image.LANCZOS)
        kx, ky = im.width / dw, im.height / dh
        ox, oy = (.5 - q.get('px', 50) / 100) * (dw - rw), (.5 - q.get('py', 50) / 100) * (dh - rh)
        im = im.transform((LARG, ALT), Image.AFFINE, (
            co * kx, si * kx, (-co * LARG / 2 - si * ALT / 2 - ox + dw / 2) * kx,
            -si * ky, co * ky, (si * LARG / 2 - co * ALT / 2 - oy + dh / 2) * ky), resample=Image.BICUBIC)
    c = np.asarray(im, dtype=np.float64) / 255
    Y = .2126 * c[..., 0] + .7152 * c[..., 1] + .0722 * c[..., 2]
    if a.get('suavizar', 0) > 0:
        r = max(1, round(a['suavizar'] * 3)); Y = _caixa(_caixa(Y, r), r)
    if a.get('nitidez', 0) > 0:
        Y = Y + a['nitidez'] * (Y - _caixa(Y, 4))
    v = np.clip(np.minimum(1, np.clip(Y, 0, 1) * 2 ** a.get('exposicao', 0)) ** a.get('gama', 1), 1e-6, 1 - 1e-6)
    k = a.get('ctr', 1)
    if k != 1: v = v ** k / (v ** k + (1 - v) ** k)
    piso, teto = a.get('piso', 0), a.get('teto', 1)
    foto = np.clip(piso + (teto - piso) * v + a.get('brilho', 0), 0, 1)
    return foto


TOM_BANNER = {'brilhoTom': .35, 'gama': .86, 'ctr': 1.55, 'escuro': 0.0}      # o padrao do js/banner.js


def tom_da_receita(R):
    """O tom com que o site trama o banner: o da receita, se foi ajustado no Spirit; senao o padrao do banner."""
    g = R.get('tingimento')
    if isinstance(g, dict):
        return {'brilhoTom': g.get('brilho_do_tom', .35), 'gama': g.get('gama', .86), 'ctr': g.get('contraste', 1.55), 'escuro': g.get('escuro', 0) or 0}
    return dict(TOM_BANNER)


def curva_tom(L, T):
    """A funcao tom() do js/trama.js (e a curvaTom do Spirit): luz 0..1 -> tom 0..1 antes da trama."""
    v = np.clip(np.power(np.maximum(L, 0), T['gama']), 1e-6, 1 - 1e-6)
    a, b = v ** T['ctr'], (1 - v) ** T['ctr']
    w = np.clip(a / (a + b) + T['brilhoTom'], 0, 1)
    if T['escuro'] > 0:
        w = np.where(w < .78, .78 * (w / .78) ** (1 + 2 * T['escuro']), w)
    return w


def passagem_no_tom(foto, t, T):
    """04/10/2026: «quero o esmaecimento mais longo, deixar menos evidente a fronteira da foto».
    A passagem na LUZ (1 - t*(1 - luz)) perde a primeira metade: o tom do banner clareia +0,35, entao toda luz acima
    de ~55% ja e creme puro, e a foto so aparece quando t passa de ~0,6, de uma vez, numa faixa curta. Aqui a passagem
    e feita no TOM, como opacidade da foto ja tingida sobre o creme: tom final = 1 - t*(1 - tom(foto)). A luz gravada
    e a inversa da curva desse tom, entao o motor do site, que aplica a curva, chega exatamente nele."""
    Ls = np.linspace(0, 1, 4097)
    Ts = curva_tom(Ls, T)                                   # crescente; achata em 1 a partir do joelho
    alvo = 1 - t * (1 - curva_tom(foto, T))
    i = np.clip(np.searchsorted(Ts, alvo, side='left'), 0, 4096)
    lum = Ls[i]
    return np.where(alvo >= 1 - 1e-9, 1 - t * (1 - foto), lum)   # tom 1 (creme): a luz de sempre


def da_receita(cru, saida, receita, prova=None):
    """02/10/2026: o banner pela RECEITA da aba [ 08 ] Banner de pagina do Spirit («copiar receita para o Claude»).

        python _ferramentas/banner/foto_banner.py --receita receita.json <cru.jpg> <saida-lum.webp> [--prova prova.png]

    Mesma conta da aba: enquadramento (recorte, espelhar, inclinar, zoom, px, py) no 3:1, luminancia Rec.709, suavizar, nitidez, exposicao,
    gama, contraste, piso, teto, brilho, e a passagem para o creme (inicio, fim, suave)."""
    import json
    R = json.load(open(receita, encoding='utf-8')) if isinstance(receita, str) else receita
    f = R['passagem_para_o_creme']
    # 03/10/2026: a foto ocupa so a parte da direita do banner (area, 2/3 nas receitas novas do Spirit; sem a chave,
    # a largura toda, como nas receitas antigas). A passagem para o creme e medida na largura da foto.
    area = f.get('area', 1.0)
    PW = int(round(LARG * area)); X0 = LARG - PW
    foto = np.ones((ALT, LARG))
    foto[:, X0:] = luz_da_receita(cru, R, PW, ALT)
    ini = f.get('inicio', INICIO); fim = max(ini + .02, f.get('fim', FIM))
    x = (np.arange(LARG) + .5 - X0) / PW
    t = np.clip((x - ini) / (fim - ini), 0, 1)
    t = (t * t * (3 - 2 * t)) ** f.get('suave', 1)
    # 04/10/2026: receita nova do Spirit traz medida_no_tom; sem a chave, a passagem na luz, como nas receitas antigas
    if f.get('medida_no_tom'):
        lum = passagem_no_tom(foto, np.broadcast_to(t[None, :], foto.shape), tom_da_receita(R))
    else:
        lum = 1 - t[None, :] * (1 - foto)
    Image.fromarray((lum * 255).round().astype(np.uint8), 'L').save(saida, lossless=True)
    print('%s: %d x %d, pela receita do Spirit' % (os.path.basename(saida), LARG, ALT))
    if prova:
        m4 = np.array([[0, 8, 2, 10], [12, 4, 14, 6], [3, 11, 1, 9], [15, 7, 13, 5]])
        yy, xx = np.mgrid[0:ALT, 0:LARG]
        kk = np.clip(np.floor(manchas.tom(lum) * 3 + (m4[yy % 4, xx % 4] + .5) / 16), 0, 3).astype(int)
        Image.fromarray(manchas.CORES[kk].round().astype(np.uint8), 'RGB').save(prova)
        print('prova:', prova)


if __name__ == '__main__':
    if '--receita' in sys.argv:
        i = sys.argv.index('--receita'); rec = sys.argv[i + 1]; del sys.argv[i:i + 2]
        pv = None
        if '--prova' in sys.argv:
            i = sys.argv.index('--prova'); pv = sys.argv[i + 1]; del sys.argv[i:i + 2]
        da_receita(sys.argv[1], sys.argv[2], rec, pv); sys.exit()
    g = 1.4
    if '--gama' in sys.argv:
        i = sys.argv.index('--gama'); g = float(sys.argv[i + 1]); del sys.argv[i:i + 2]
    def _op(n, pad):
        if n in sys.argv:
            i = sys.argv.index(n); v = float(sys.argv[i + 1]); del sys.argv[i:i + 2]; return v
        return pad
    ini, fim, suave = _op('--inicio', INICIO), _op('--fim', FIM), _op('--suave', 1.0)
    main(sys.argv[1], sys.argv[2], g, ini, fim, suave)
