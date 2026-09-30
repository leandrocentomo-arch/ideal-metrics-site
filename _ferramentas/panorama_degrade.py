# -*- coding: utf-8 -*-
"""Reservas da tira no DEGRADE azul -> cor (30/09/2026).

    python _ferramentas/panorama_degrade.py [de] [ate]

«Nao teria como colorir gradativamente os cards de cima para baixo?» Ao vivo quem faz o
degrade e o motor (js/trama.js, cfg.degrade): ponto a ponto, um limiar ordenado 8x8 escolhe
entre o azul oficial e a cor, e a proporcao de pontos em cor cresce de cima para baixo.
Aqui sai a mesma coisa para a reserva de cada card (sem WebGL e telefone), juntando as
duas reservas que ja existem:

  img/tira-<servico>-bayer.webp       azul (panorama_azul.py)
  img/tira-<servico>-cor-bayer.webp   cor (panorama.py)
  -> img/tira-<servico>-grad-bayer.webp

de e ate sao frações da altura da reserva a partir do alto (padrao .30 e .95, os mesmos
da chamada do motor no index.html)."""

import os, sys
import numpy as np
from PIL import Image

SITE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG = os.path.join(SITE, 'img')
DE = float(sys.argv[1]) if len(sys.argv) > 1 else .30
ATE = float(sys.argv[2]) if len(sys.argv) > 2 else .95


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


for nome in ['carbono', 'iso', 'smeta', 'esg']:
    az = np.asarray(Image.open(os.path.join(IMG, 'tira-%s-bayer.webp' % nome)).convert('RGB'))
    co = np.asarray(Image.open(os.path.join(IMG, 'tira-%s-cor-bayer.webp' % nome)).convert('RGB'))
    H, W = az.shape[:2]
    t = np.clip((np.arange(H) / float(H - 1) - DE) / (ATE - DE), 0, 1); t = t * t * (3 - 2 * t)
    B = bayer(8)[np.arange(H) % 8][:, np.arange(W) % 8]
    cor = t[:, None] > B
    out = np.where(cor[..., None], co, az)
    arq = os.path.join(IMG, 'tira-%s-grad-bayer.webp' % nome)
    Image.fromarray(out.astype(np.uint8)).save(arq, 'WEBP', lossless=True, quality=100, method=6)
    print('%-28s %dx%d  %d KB' % (os.path.basename(arq), W, H, os.path.getsize(arq) // 1024))
