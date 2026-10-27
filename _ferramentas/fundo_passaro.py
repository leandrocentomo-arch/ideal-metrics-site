"""Fundo do Painel de normas com o pássaro da Ideal Metrics (img/fundo-painel-passaro.webp).
27/10/2026, Leandro: «colocar o pássaro da Ideal Metrics de fundo, mais claro, com a impressão de estar iluminado assim
como o globo… o resto do fundo com um azul mais claro». Pássaro = img/passaro-ideal-m.svg (grupo do 18Asset 253), nunca
redesenhado: só a silhueta vira máscara e recebe luz. Rodar: python _ferramentas/fundo_passaro.py"""
from pathlib import Path
import fitz
from PIL import Image, ImageChops, ImageDraw, ImageFilter

RAIZ = Path(__file__).resolve().parent.parent
W, H = 2400, 1350
LARG = 1750                       # largura do pássaro no fundo
CENTRO = (1330, 690)              # um pouco à direita, atrás do globo e da lista

def hx(h): h = h.lstrip('#'); return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))

def degrade(w, h, c0, c1):
    v = Image.linear_gradient('L').resize((w, h)); hz = v.transpose(Image.Transpose.ROTATE_90).resize((w, h)).transpose(Image.Transpose.FLIP_LEFT_RIGHT)
    lin = ImageChops.add(v, hz, scale=2)   # diagonal: claro no alto à esquerda, mais azul embaixo à direita
    return Image.composite(Image.new('RGB', (w, h), hx(c1)), Image.new('RGB', (w, h), hx(c0)), lin)

def mascara():
    doc = fitz.open(RAIZ / 'img' / 'passaro-ideal-m.svg'); pg = doc[0]
    z = LARG / pg.rect.width
    pix = pg.get_pixmap(matrix=fitz.Matrix(z, z), alpha=True)
    im = Image.frombytes('RGBA', (pix.width, pix.height), pix.samples)
    return im.split()[3]

def main():
    fundo = degrade(W, H, '#D3E3F4', '#A6C3E3')
    # duas manchas muito suaves para o vidro ter o que desfocar
    luz = Image.new('L', (W, H), 0); d = ImageDraw.Draw(luz)
    d.ellipse([-300, -400, 1100, 700], fill=150); d.ellipse([1700, 800, 2800, 1700], fill=90)
    luz = luz.filter(ImageFilter.GaussianBlur(220))
    fundo = Image.composite(Image.new('RGB', (W, H), (255, 255, 255)), fundo, luz)

    m = mascara(); mw, mh = m.size; x0, y0 = CENTRO[0] - mw // 2, CENTRO[1] - mh // 2
    M = Image.new('L', (W, H), 0); M.paste(m, (x0, y0))
    # sombra suave embaixo e à direita (dá volume, como a sombra do globo)
    sombra = ImageChops.offset(M, 18, 26).filter(ImageFilter.GaussianBlur(26)).point(lambda v: v * .5)
    fundo = Image.composite(Image.new('RGB', (W, H), hx('#6E93BC')), fundo, sombra)
    # brilho em volta (o pássaro «aceso»)
    halo = M.filter(ImageFilter.GaussianBlur(40)).point(lambda v: min(255, v * .9))
    fundo = Image.composite(Image.new('RGB', (W, H), (255, 255, 255)), fundo, halo)
    # corpo: luz radial vindo do alto à esquerda, branco → azul muito claro
    corpo = Image.radial_gradient('L').resize((int(mw * 1.6), int(mh * 1.9)))
    cg = Image.new('L', (W, H), 255); cg.paste(corpo, (x0 - int(mw * .35), y0 - int(mh * .55)))
    pele = Image.composite(Image.new('RGB', (W, H), hx('#C8DBEF')), Image.new('RGB', (W, H), (255, 255, 255)), cg)
    fundo = Image.composite(pele, fundo, M)
    # fio de luz na borda de cima (aresta iluminada)
    aresta = ImageChops.subtract(M, ImageChops.offset(M, 0, 5)).filter(ImageFilter.GaussianBlur(1.2))
    fundo = Image.composite(Image.new('RGB', (W, H), (255, 255, 255)), fundo, aresta)
    saida = RAIZ / 'img' / 'fundo-painel-passaro.webp'
    fundo.save(saida, quality=88); print(saida.name, saida.stat().st_size // 1024, 'KB')

if __name__ == '__main__':
    main()
