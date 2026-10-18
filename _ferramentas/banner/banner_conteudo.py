# -*- coding: utf-8 -*-
"""Banner das paginas de Conteudo (blog.html e os posts), 18/10/2026: «faca um banner diferente para a pagina de
conteudo», escolhido «trama sem foto, mais baixa». E a luminancia que o js/banner.js trama: creme ate 38% da largura
e dali uma passagem suave (sem o degrau do banner-trama-lum.webp padrao) ate a trama mais densa na borda direita,
com uma leve ondulacao vertical para a trama nao sair em faixas retas. Proporcao 4:1, a do banner baixo.

    python _ferramentas/banner/banner_conteudo.py      ->  img/banner-conteudo-lum.webp
"""
import os
import numpy as np
from PIL import Image

SITE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
W, H = 1600, 400
x = np.linspace(0, 1, W)[None, :]
y = np.linspace(0, 1, H)[:, None]
# 18/10/2026: «a cor da trama igual a das paginas padrao»: os MESMOS niveis do banner-trama-lum.webp (0,55 logo depois da
# passagem, caindo a 0,44 na borda direita); so a passagem do creme para a trama continua suave (de 38% a 56%), sem degrau
t = np.clip((x - 0.38) / 0.18, 0, 1)
t = t * t * (3 - 2 * t)                                   # smoothstep: entra e sai sem quina
base = 0.55 - 0.11 * np.clip((x - 0.47) / 0.53, 0, 1)    # 0,55 a 0,44, como o padrao
lum = np.clip(1.0 * (1 - t) + base * t, 0, 1)
Image.fromarray(np.uint8(np.rint(lum * 255)), 'L').convert('RGB').save(
    os.path.join(SITE, 'img', 'banner-conteudo-lum.webp'), 'WEBP', quality=92, method=6)
print('img/banner-conteudo-lum.webp', W, 'x', H)
