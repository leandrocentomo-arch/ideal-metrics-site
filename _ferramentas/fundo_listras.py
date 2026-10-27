"""Fundo do Painel de normas em listras verticais (img/fundo-painel-listras.webp).
27/10/2026, Leandro: «tente fazer um monte de linhas geométricas simétricas uma ao lado da outra, de várias cores da empresa»
e «faça na vertical». Listras de larguras variadas, espelhadas no meio (simétricas), nas cores da marca, com predominância
dos tons claros. Rodar: python _ferramentas/fundo_listras.py  (semente fixa)."""
import random
from pathlib import Path
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter

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
    # 27/10, «os gaps fossem nada mesmo, só a cor de fundo»: o vidro passa a ser o fundo de cada placa (attachment fixed), com
    # as listras JÁ foscas: 22 px de desfoque na tela ≈ 34 px nesta imagem (2400 px cobrindo ~1536 px css) e saturação 1,35
    fosco = ImageEnhance.Color(im.filter(ImageFilter.GaussianBlur(34))).enhance(1.35)
    # 27/10, 3º: «na parte de baixo da área glass, deixe menos azul as listras, mais próximas ao creme»: a partir de 40% da
    # altura o creme vai cobrindo as listras até 85% na base
    rampa = Image.new('L', (1, H)); rampa.putdata([0 if y < H * .4 else int(217 * ((y - H * .4) / (H * .6)) ** 1.2) for y in range(H)])
    fosco = Image.composite(Image.new('RGB', (W, H), hx('#FAF9F5')), fosco, rampa.resize((W, H)))
    saida = RAIZ / 'img' / 'fundo-painel-listras-fosco.webp'; fosco.save(saida, quality=88)
    print(saida.name, saida.stat().st_size // 1024, 'KB')

if __name__ == '__main__':
    main()
