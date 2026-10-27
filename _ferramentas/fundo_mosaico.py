"""Fundo em mosaico do Painel de normas (img/fundo-painel-mosaico.webp).
27/10/2026, Leandro: mosaico no estilo do mozayk.design, figuras muito claras, quase da cor do fundo, e mais cheio,
com outras formas. Rodar: python _ferramentas/fundo_mosaico.py  (semente fixa: sempre o mesmo desenho)."""
import random
from pathlib import Path
from PIL import Image, ImageDraw

S, W, H, C = 2, 2400, 1350, 150          # desenha em 2x e reduz (antialias); célula de 150 px
BASE = '#DDE8F4'
CORES = ['#E9F0F8', '#F3F7FB', '#FFFFFF', '#D2E0F0', '#C9DAEE', '#E4ECF6']   # todas a poucos tons do fundo
SAIDA = Path(__file__).resolve().parent.parent / 'img' / 'fundo-painel-mosaico.webp'

def hx(h, a=255):
    h = h.lstrip('#'); return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4)) + (a,)

def peca(d, x0, y0, c, cor):
    f = random.choice(['quadrado', 'triangulo', 'triangulo', 'losango', 'circulo', 'quarto', 'quarto', 'meio', 'faixa', 'miolo'])
    if f == 'quadrado': d.rectangle([x0, y0, x0 + c, y0 + c], fill=cor)
    elif f == 'triangulo':
        d.polygon(random.choice([[(x0, y0), (x0 + c, y0), (x0, y0 + c)], [(x0 + c, y0), (x0 + c, y0 + c), (x0, y0 + c)],
                                 [(x0, y0), (x0 + c, y0 + c), (x0, y0 + c)], [(x0, y0), (x0 + c, y0), (x0 + c, y0 + c)]]), fill=cor)
    elif f == 'losango': d.polygon([(x0 + c / 2, y0), (x0 + c, y0 + c / 2), (x0 + c / 2, y0 + c), (x0, y0 + c / 2)], fill=cor)
    elif f == 'circulo': d.ellipse([x0, y0, x0 + c, y0 + c], fill=cor)
    elif f == 'quarto':   # quarto de círculo com o centro num canto da célula
        cx, cy = random.choice([(x0, y0), (x0 + c, y0), (x0, y0 + c), (x0 + c, y0 + c)])
        ini = {(x0, y0): 0, (x0 + c, y0): 90, (x0 + c, y0 + c): 180, (x0, y0 + c): 270}[(cx, cy)]
        d.pieslice([cx - c, cy - c, cx + c, cy + c], ini, ini + 90, fill=cor)
    elif f == 'meio':     # meio círculo apoiado num lado
        lado = random.choice(['c', 'b', 'e', 'd'])
        if lado == 'c': d.pieslice([x0, y0 - c / 2, x0 + c, y0 + c / 2], 0, 180, fill=cor)
        elif lado == 'b': d.pieslice([x0, y0 + c / 2, x0 + c, y0 + 3 * c / 2], 180, 360, fill=cor)
        elif lado == 'e': d.pieslice([x0 - c / 2, y0, x0 + c / 2, y0 + c], 270, 450, fill=cor)
        else: d.pieslice([x0 + c / 2, y0, x0 + 3 * c / 2, y0 + c], 90, 270, fill=cor)
    elif f == 'faixa': d.rectangle([x0, y0, x0 + c, y0 + c / 2] if random.random() < .5 else [x0, y0, x0 + c / 2, y0 + c], fill=cor)
    else: d.rectangle([x0 + c / 4, y0 + c / 4, x0 + 3 * c / 4, y0 + 3 * c / 4], fill=cor)

def main():
    random.seed(21)
    im = Image.new('RGBA', (W * S, H * S), hx(BASE)); d = ImageDraw.Draw(im)
    for gx in range(W // C + 1):
        for gy in range(H // C + 1):
            if random.random() < .55: peca(d, gx * C * S, gy * C * S, C * S, hx(random.choice(CORES)))
    for x in range(0, W + 1, C): d.line([x * S, 0, x * S, H * S], fill=(255, 255, 255, 140), width=S)
    for y in range(0, H + 1, C): d.line([0, y * S, W * S, y * S], fill=(255, 255, 255, 140), width=S)
    for x in range(0, W + 1, C):
        for y in range(0, H + 1, C):
            if random.random() < .3:
                k = 6 * S; d.line([x * S - k, y * S, x * S + k, y * S], fill=hx('#336699', 90), width=S); d.line([x * S, y * S - k, x * S, y * S + k], fill=hx('#336699', 90), width=S)
    im.resize((W, H), Image.LANCZOS).convert('RGB').save(SAIDA, quality=88)
    print(SAIDA.name, SAIDA.stat().st_size // 1024, 'KB')

if __name__ == '__main__':
    main()
