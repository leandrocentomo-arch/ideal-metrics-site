"""Ilustrações dos setores para a aba Certificados por setor (img/setores/setor-<id>.webp).
Origem: brochuras/icones/estiloC-sem-feixe/ (coleção C, creme #F3F0E9 embutido). 27/10/2026: creme vira transparente («não deixe a
faixa creme de fundo»), todos na MESMA tela 560 × 150 («menores e mais largas»), assentados embaixo e à esquerda; o fiscal do
Setor público sai por corte («tire aquele guarda»). Rodar: python _ferramentas/setores_img.py"""
import glob, os
from pathlib import Path
from PIL import Image

RAIZ = Path(__file__).resolve().parent.parent
ORIG = RAIZ.parent / 'brochuras' / 'icones' / 'estiloC-sem-feixe'
W, H = 560, 100   # 27/10, 2º: «estão muito grandes, muito altas… uma coisa mais sóbria»
CORTE = {'setor-publico': .885}   # fração da largura que fica (o guarda está na borda direita)

def cremefora(im):
    px = im.load()
    for y in range(im.height):
        for x in range(im.width):
            r, g, b, a = px[x, y]
            d = max(abs(r - 243), abs(g - 240), abs(b - 233))
            if d <= 10: px[x, y] = (r, g, b, 0)
            elif d <= 26: px[x, y] = (r, g, b, int(a * (d - 10) / 16))
    return im

def main():
    for f in sorted(glob.glob(str(ORIG / 'setor-*.png'))):
        n = os.path.basename(f).replace('.png', '').replace('setor-setor-publico', 'setor-publico')
        im = cremefora(Image.open(f).convert('RGBA'))
        if n in CORTE: im = im.crop((0, 0, int(im.width * CORTE[n]), im.height))
        im = im.crop(im.getbbox())
        esc = min((H - 6) / im.height, (W - 6) / im.width)
        im = im.resize((round(im.width * esc), round(im.height * esc)), Image.LANCZOS)
        tela = Image.new('RGBA', (W, H), (0, 0, 0, 0)); tela.paste(im, (0, H - im.height), im)
        tela.save(RAIZ / 'img' / 'setores' / f'{n}.webp', quality=88); print(n, im.size)

if __name__ == '__main__':
    main()
