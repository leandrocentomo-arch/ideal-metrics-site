"""Fundo do Painel de normas: manchas azuis desfocadas sobre CREME (img/fundo-painel-creme.webp).
27/10/2026, Leandro, depois de mosaico, pássaro e glifos: «não ficou legal, vamos voltar mais para esse [o de manchas], mas
vamos deixar uma cor clara de fundo, o creme não teria como ser né?». Mesma receita das manchas do vidro (elipses nas cores
da marca, desfoque de 150 px), agora sobre o creme do site #FAF9F5, com as manchas concentradas e o creme sobrando entre elas.
Rodar: python _ferramentas/fundo_manchas.py  (semente fixa)."""
import random
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter

RAIZ = Path(__file__).resolve().parent.parent
W, H = 2400, 1350
CREME = '#FAF9F5'
MANCHAS = [('#9FC5F0', 5, 330), ('#4F86C6', 3, 260), ('#336699', 2, 210), ('#D3E2F2', 5, 380), ('#6E93BC', 1, 200)]

def hx(h): h = h.lstrip('#'); return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))

def main():
    random.seed(12)
    im = Image.new('RGB', (W, H), hx(CREME)); d = ImageDraw.Draw(im)
    for cor, n, r in MANCHAS:
        for _ in range(n):
            x, y = random.randint(-100, W + 100), random.randint(-100, H + 100)
            rx, ry = random.randint(int(r * .7), r), random.randint(int(r * .5), int(r * .9))
            d.ellipse([x - rx, y - ry, x + rx, y + ry], fill=hx(cor))
    im = im.filter(ImageFilter.GaussianBlur(150))
    saida = RAIZ / 'img' / 'fundo-painel-creme.webp'; im.save(saida, quality=88)
    print(saida.name, saida.stat().st_size // 1024, 'KB')

if __name__ == '__main__':
    main()
