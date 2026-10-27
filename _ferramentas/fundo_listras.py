"""Fundo do Painel de normas em listras verticais (img/fundo-painel-listras.webp).
27/10/2026, Leandro: «tente fazer um monte de linhas geométricas simétricas uma ao lado da outra, de várias cores da empresa»
e «faça na vertical». Listras de larguras variadas, espelhadas no meio (simétricas), nas cores da marca, com predominância
dos tons claros. Rodar: python _ferramentas/fundo_listras.py  (semente fixa)."""
import random
from pathlib import Path
from PIL import Image, ImageDraw

RAIZ = Path(__file__).resolve().parent.parent
W, H = 2400, 1350
CORES = ['#FAF9F5', '#FAF9F5', '#EEF3F9', '#E2ECF7', '#D3E2F2', '#C4D8EE', '#B3CDEA', '#9FC5F0']   # 27/10, 2º: «menos contrastes, e mais claras» (sem tinta nem azul forte)

def hx(h): h = h.lstrip('#'); return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))

def main():
    random.seed(9)
    metade, x = [], 0
    while x < W / 2:
        w = random.choice([8, 14, 22, 30, 44, 60, 84]); metade.append((w, random.choice(CORES))); x += w
    im = Image.new('RGB', (W, H), hx('#FAF9F5')); d = ImageDraw.Draw(im)
    x = W / 2
    for w, c in metade:                                   # do meio para fora, nos dois lados: simetria em espelho
        d.rectangle([x, 0, x + w, H], fill=hx(c)); d.rectangle([W - x - w, 0, W - x, H], fill=hx(c)); x += w
    saida = RAIZ / 'img' / 'fundo-painel-listras.webp'; im.save(saida, quality=88)
    print(saida.name, saida.stat().st_size // 1024, 'KB')

if __name__ == '__main__':
    main()
