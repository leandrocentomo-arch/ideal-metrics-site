# -*- coding: utf-8 -*-
"""Banner das paginas internas SEM FOTO, por ora (22/09/2026).

O Leandro pediu: do creme a trama azulada, da esquerda para a direita, com o
efeito (rastro do mouse). A esquerda tem de ser creme puro, porque e ali que o
titulo e o subtitulo sao lidos.

    python _ferramentas/banner/banner.py

O QUE FAZ
  1. img/banner-trama-lum.webp: luminancia para o motor js/trama.js. Creme puro
     (sem ponto nenhum) ate 42% da largura; dali uma rampa suave (smoothstep)
     ate o tom 0,84 na borda direita, cerca de 48% de pontos azuis, a trama das
     fotos da primeira secao clareada. A curva do shader e invertida por
     bissecao, como em arcos/manchas.py.
     Proporcao 2:1: o motor faz object-fit cover, e toda faixa de banner e mais
     larga que 2:1, entao o corte e sempre vertical e a rampa inteira aparece.
  2. Em cada pagina com .page-banner: garante js/trama.js e js/banner.js antes
     de </body>. A foto de cada pagina (--banner-photo) continua no HTML, mas o
     CSS deixou de usa-la: quando as fotos vierem, voltam por aqui.

Sem WebGL, ou abaixo de 769px, o banner fica creme liso."""

import os, sys, glob, re
import numpy as np
from PIL import Image

AQUI = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(os.path.dirname(AQUI))
sys.path.insert(0, os.path.join(AQUI, '..', 'arcos'))
import manchas   # a curva de tom e a inversao

W, H = 1200, 600
INICIO, TOM_DIREITA = .42, .84


def imagem():
    x = (np.arange(W) + .5) / W
    t = np.clip((x - INICIO) / (1 - INICIO), 0, 1)
    t = t * t * (3 - 2 * t)                         # smoothstep
    alvo = 1 - t * (1 - TOM_DIREITA)                # 1 = creme, sem trama
    # tabela: 256 niveis de alvo -> luminancia
    niveis = np.linspace(TOM_DIREITA, 1, 64)
    lum_niveis = np.array([manchas.lum_para(a) if a < .999 else 1.0 for a in niveis])
    lum = np.interp(alvo, niveis, lum_niveis)
    lum[alvo >= .999] = 1.0
    img = np.tile(lum, (H, 1))
    Image.fromarray((img * 255).round().astype(np.uint8), 'L').save(
        os.path.join(SITE, 'img', 'banner-trama-lum.webp'), lossless=True)
    print('img/banner-trama-lum.webp: %dx%d, creme ate %d%%, tom %.2f na direita' % (W, H, INICIO * 100, TOM_DIREITA))


def paginas():
    n = 0
    for p in sorted(glob.glob(os.path.join(SITE, '*.html'))):
        raw = open(p, 'rb').read()
        s = raw.decode('utf-8')
        if 'class="page-banner"' not in s: continue
        eol = '\r\n' if b'\r\n' in raw else '\n'
        mud = False
        for js in ('js/trama.js', 'js/banner.js'):
            if js not in s:
                assert s.count('</body>') == 1, p
                s = s.replace('</body>', '<script src="%s"></script>%s</body>' % (js, eol), 1); mud = True
        if mud:
            open(p, 'wb').write(s.encode('utf-8')); n += 1
    print('%d paginas com o banner em trama' % n)


if __name__ == '__main__':
    imagem()
    paginas()
