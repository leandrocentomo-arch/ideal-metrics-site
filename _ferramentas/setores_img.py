"""Ilustrações dos setores para a aba Certificados por setor (img/setores/setor-<id>.webp).
27/10/2026, 3ª versão («faça aquele modelo de única linha, volte ao tamanho das ilustrações que estavam antes»): desenho de LINHA
CONTÍNUA (coleção B, só o traço em #14304C), dos vetores brochuras/icones/setor-<nome>.svg (vetorizados em 25/10), na tela
560 × 300 assentados embaixo e à esquerda. Comércio e serviços vem de brochuras/icones/linha-comercio.png (Flow, 27/10) quando
existir. Rodar: python _ferramentas/setores_img.py"""
import glob, os
from pathlib import Path
import fitz
from PIL import Image, ImageFilter

RAIZ = Path(__file__).resolve().parent.parent
ICONES = RAIZ.parent / 'brochuras' / 'icones'
W, H = 560, 170   # 27/10, 4º: «linhas mais finas, menores, mais largos, espaço maior acima»: faixa mais baixa, desenho até 150 px de altura
NOMES = {'setor-setor-publico': 'setor-publico'}

def svg_para_rgba(svg, largura):
    doc = fitz.open(svg); pg = doc[0]; z = largura / pg.rect.width
    pix = pg.get_pixmap(matrix=fitz.Matrix(z, z), alpha=True)
    return Image.frombytes('RGBa', (pix.width, pix.height), pix.samples).convert('RGBA')

def assenta(im, nome):
    im = im.crop(im.getbbox())
    esc = min((H - 20) / im.height, (W - 8) / im.width)   # 20 px de ar em cima
    im = im.resize((round(im.width * esc), round(im.height * esc)), Image.LANCZOS)
    a = Image.blend(im.split()[3].filter(ImageFilter.MinFilter(3)), im.split()[3], .7)   # 27/10, 5º: «ficaram muito finos»: meio-termo, só 30% do afinamento
    im = Image.merge('RGBA', (Image.new('L', im.size, 51), Image.new('L', im.size, 102), Image.new('L', im.size, 153), a))   # azul #336699
    tela = Image.new('RGBA', (W, H), (0, 0, 0, 0)); tela.paste(im, (0, H - im.height), im)
    tela.save(RAIZ / 'img' / 'setores' / f'{nome}.webp', quality=88); print(nome, im.size)

def main():
    for f in sorted(glob.glob(str(ICONES / 'setor-*.svg'))):
        n = os.path.basename(f)[:-4]; assenta(svg_para_rgba(f, W * 2), NOMES.get(n, n))
    extra = ICONES / 'linha-comercio.png'
    if extra.exists():
        im = Image.open(extra).convert('RGBA'); px = im.load()
        for y in range(im.height):   # fundo branco/creme do Flow vira transparente, traço fica
            for x in range(im.width):
                r, g, b, a = px[x, y]; lum = (r + g + b) / 3
                if lum > 236: px[x, y] = (51, 102, 153, 0)
                else: k = max(0, min(255, int((236 - lum) * 1.6))); px[x, y] = (51, 102, 153, k)
        assenta(im, 'setor-comercio')

if __name__ == '__main__':
    main()
