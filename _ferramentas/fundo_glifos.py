"""Fundo do Painel de normas com o glifo da Ideal Metrics (img/fundo-painel-glifos.webp).
27/10/2026, Leandro: «tente os glifos, tente fazer um azul mais vívido de fundo» e, em seguida, «quando digo glifo, quero
dizer esse»: o GLIFO é o símbolo dos seis losangos (2 fileiras de 3) das etiquetas Guia e Navegação (js/gaveta.js), não os
símbolos do mosaico. Rodar: python _ferramentas/fundo_glifos.py  (semente fixa)."""
import random, re
from pathlib import Path
import fitz
from PIL import Image, ImageChops

RAIZ = Path(__file__).resolve().parent.parent
W, H, C = 2400, 1350, 150
FUNDO = ('#2E6FC7', '#5C9BE8')                       # azul vívido, diagonal
TONS = [('#FFFFFF', .30), ('#FFFFFF', .18), ('#D3E2F2', .40), ('#9FC5F0', .55), ('#FFFFFF', .45), ('#1F57A8', .35)]

GLIFO = 'M3 0l3 3-3 3-3-3zM11 0l3 3-3 3-3-3zM19 0l3 3-3 3-3-3zM3 8l3 3-3 3-3-3zM11 8l3 3-3 3-3-3zM19 8l3 3-3 3-3-3z'   # viewBox 22 × 14, igual ao js/gaveta.js

def main():
    random.seed(33)
    p = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
]   # o degradê é feito no PIL: o MuPDF não pinta gradiente de SVG
    grade = ''.join(f'M{x} 0V{H}' for x in range(0, W + 1, C)) + ''.join(f'M0 {y}H{W}' for y in range(0, H + 1, C))
    p.append(f'<path d="{grade}" stroke="#FFFFFF" stroke-opacity=".12" stroke-width="1" fill="none"/>')
    cruz = ''.join(f'M{x-6} {y}H{x+6}M{x} {y-6}V{y+6}' for x in range(0, W + 1, C) for y in range(0, H + 1, C) if random.random() < .35)
    p.append(f'<path d="{cruz}" stroke="#FFFFFF" stroke-opacity=".45" stroke-width="1.2" fill="none"/>')
    for gx in range(W // C + 1):
        for gy in range(H // C + 1):
            if random.random() > .45: continue
            k = random.choice([2.5, 2.5, 4, 4, 6.5, 10])    # glifo de 55 a 220 px de largura
            gw, gh = 22 * k, 14 * k
            ox = gx * C + (C - gw) / 2; oy = gy * C + (C - gh) / 2
            cor, a = random.choice(TONS)
            p.append(f'<path d="{GLIFO}" transform="translate({ox:.1f} {oy:.1f}) scale({k})" fill="{cor}" fill-opacity="{a}"/>')
    p.append('</svg>')
    doc = fitz.open(stream=''.join(p).encode(), filetype='svg')
    pix = doc[0].get_pixmap(alpha=True)
    glif = Image.frombytes('RGBa', (pix.width, pix.height), pix.samples).convert('RGBA')   # MuPDF entrega pré-multiplicado
    v = Image.linear_gradient('L').resize((W, H)); hz = v.transpose(Image.Transpose.ROTATE_90).resize((W, H)).transpose(Image.Transpose.FLIP_LEFT_RIGHT)
    hx = lambda h: tuple(int(h.lstrip('#')[i:i + 2], 16) for i in (0, 2, 4))
    im = Image.composite(Image.new('RGB', (W, H), hx(FUNDO[1])), Image.new('RGB', (W, H), hx(FUNDO[0])), ImageChops.add(v, hz, scale=2)).convert('RGBA')
    im.alpha_composite(glif); im = im.convert('RGB')
    saida = RAIZ / 'img' / 'fundo-painel-glifos.webp'; im.save(saida, quality=88)
    print(saida.name, im.size, saida.stat().st_size // 1024, 'KB')

if __name__ == '__main__':
    main()
