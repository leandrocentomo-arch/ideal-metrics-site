# -*- coding: utf-8 -*-
"""Mosaico em L da home (11/10/2026): «colocar o mosaico que criamos em forma de L» na vaga ao lado de Temas de gestao,
com o efeito do mouse e a trama.

Fonte: Ideal Metrics/mosaicos/parede-mosaico-simbolos-L-01.svg (2160 x 2160, recortado em L, quatro tintas da marca).
Saidas em img/:
  mosaico-l-lum.webp    a luminancia que o motor da trama (js/trama.js) re-trama ao vivo. Cada tinta vira um cinza
                        escolhido para o motor com o tom NEUTRO (gama 1, contraste 1, brilho 0): o azul-marinho sai
                        chapado, os dois azuis medios saem tramados entre o marinho e o azul da rampa, o azul claro
                        sai tramado entre o azul e o creme, e o creme fica creme.
  mosaico-l-bayer.webp  a mesma trama, ja feita (Bayer 4x4, rampa oficial), para quem nao roda o motor.
Rodar: python _ferramentas/mosaico_l.py
"""
import pathlib, re, sys
from PIL import Image

SITE = pathlib.Path(__file__).resolve().parent.parent
SVG = SITE.parent / 'mosaicos' / 'parede-mosaico-simbolos-L-01.svg'
LADO = 2160          # a luminancia no tamanho do desenho: a vaga tem no maximo ~640 px css (1280 px de tela a 2x)
LADO_BAYER = 1280    # a reserva tramada

# tinta do mosaico -> tom que o motor recebe (0 a 1); com o tom neutro, k = floor(v*3 + limiar)
TOM = {'#14304c': .12, '#315275': .42, '#336699': .56, '#d3e2f2': .88, '#faf9f5': 1.0}
# rampa OFICIAL do site (a mesma das pecas da home): indices 0, 1, 2 e 3
RAMPA = [(21, 51, 81), (24, 56, 88), (103, 146, 189), (250, 249, 245)]


def cinza(v):
    n = round(v * 255)
    return '#%02x%02x%02x' % (n, n, n)


def svg_lum():
    s = SVG.read_text(encoding='utf-8')
    for cor, v in TOM.items():
        s = re.sub(r'(fill|stroke)="%s"' % cor, lambda m: '%s="%s"' % (m.group(1), cinza(v)), s, flags=re.I)
    sobra = set(re.findall(r'(?:fill|stroke)="(#[0-9a-fA-F]{6})"', s)) - {cinza(v) for v in TOM.values()}
    assert not sobra, 'tinta sem tom: %s' % sobra
    return s


def renderiza(svg, lado, saida_png):
    from playwright.sync_api import sync_playwright
    html = '<html><body style="margin:0;background:#fff">%s</body></html>' % svg.replace(
        'width="2160" height="2160"', 'width="%d" height="%d"' % (lado, lado), 1)
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={'width': lado, 'height': lado}, device_scale_factor=1)
        pg.set_content(html)
        pg.screenshot(path=str(saida_png), clip={'x': 0, 'y': 0, 'width': lado, 'height': lado})
        b.close()


def bayer4():
    m = [[0]]
    while len(m) < 4:
        k = len(m); o = [[0] * (2 * k) for _ in range(2 * k)]
        for y in range(k):
            for x in range(k):
                v = m[y][x] * 4
                o[y][x] = v; o[y][x + k] = v + 2; o[y + k][x] = v + 3; o[y + k][x + k] = v + 1
        m = o
    return [[(m[y][x] + .5) / 16 for x in range(4)] for y in range(4)]


def main():
    tmp = SITE / '_ferramentas' / '_mosaico_l_tmp.png'
    renderiza(svg_lum(), LADO, tmp)
    lum = Image.open(tmp).convert('L')
    lum.save(SITE / 'img' / 'mosaico-l-lum.webp', lossless=True, quality=100, method=6)
    # a reserva: a mesma conta do shader com o tom neutro e o limiar de Bayer 4x4 por pixel
    pequena = lum.resize((LADO_BAYER, LADO_BAYER), Image.LANCZOS)
    T = bayer4(); px = pequena.load()
    saida = Image.new('RGB', pequena.size); po = saida.load()
    for y in range(pequena.size[1]):
        for x in range(pequena.size[0]):
            k = int(min(3, max(0, (px[x, y] / 255) * 3 + T[y % 4][x % 4])))
            po[x, y] = RAMPA[k]
    saida.save(SITE / 'img' / 'mosaico-l-bayer.webp', lossless=True, quality=100, method=6)
    tmp.unlink()
    for n in ('mosaico-l-lum.webp', 'mosaico-l-bayer.webp'):
        print(n, (SITE / 'img' / n).stat().st_size // 1024, 'KB')


if __name__ == '__main__':
    main()
