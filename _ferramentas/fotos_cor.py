# -*- coding: utf-8 -*-
"""FILTRO EM COR das fotos do site (28/09/2026), a receita que o Leandro calibrou
na aba [ 08 ] Filtro em cor do Spirit. Gera, para cada foto e vaga:

  img/<assunto>-cor-<suf>.webp        a foto EM COR no recorte da vaga (RGB, 900 px
                                      de largura): e o que o motor js/trama.js le
                                      (modo colorido + forte) e trama ao vivo
  img/<assunto>-cor-bayer-<suf>.webp  a reserva ja filtrada e tramada, para quem
                                      nao tem WebGL (e antes de o motor ligar)
  img/banner-ifc-cor.webp             o banner da IFC, RGBA: o alfa e o esvanecimento
                                      creme -> foto da pagina (o motor mistura o
                                      creme DEPOIS da trama, como o Spirit faz)

    python _ferramentas/fotos_cor.py            # tudo
    python _ferramentas/fotos_cor.py qc sv      # so essas vagas
    python _ferramentas/fotos_cor.py ifc

A RECEITA e uma so, aqui e no trama.js (ditherVivo.RECEITA_COR): mudar nos dois.
O TINGIMENTO OFICIAL azul (25/09) continua guardado: tingir.py --bayer, a receita
OFICIAL do Spirit e os arquivos -lum-/-bayer- que este script NAO toca.

A conta, por pixel, e a do Spirit (aba 08) e a do shader `forte` do trama.js:
  Y = luminancia; v = Y^gama; Y2 = sigmoide(v, ctr); Y2 = piso + (1-piso)*Y2 + brilho
  rgb *= Y2/Y; rgb = Y2 + (rgb-Y2)*sat
  sombras: rgb -> sombraCor NA MESMA luminancia, smoothstep(0, sombra, Y2)
  mistura: rgb = mix(rgb, rampa_oficial(Y2), mistura)
  trama: Bayer `matriz`x`matriz` por canal, `niveis` niveis, celula de `celula` px,
         limiar deslocado de `limiar`, ruido de `ruido` no limiar; o nivel mais claro = CREME
  veu: mix(creme, veu) depois da trama (na tira, o lavaRepouso do motor)"""

import os, sys
import numpy as np
from PIL import Image

SITE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG = os.path.join(SITE, 'img')
CRU = os.path.join(os.path.dirname(SITE), '_tingir-fotos', 'FOTOS')

# ---------- a receita (copiada do JSON do Spirit, 28/09/2026) ----------
RECEITA = dict(ctr=1.0, gama=0.68, piso=0.10, brilho=0.0, sat=1.0,
               sombra=0.0, sombraCor=(40, 100, 190), luzCor=(250, 249, 245), luzDe=0.32, luzForca=0.56,
               mistura=0.5, niveis=4, celula=1, matriz=2, limiar=0.0, ruido=0.0, veu=0.13, ifcGama=1.4)
# a 1a receita (28/09, tarde): ctr 1.15 gama .89 piso .21 brilho .08 sat 1.07 sombra .89 mistura .21 niveis 3 matriz 4 limiar 0 ruido .012 veu .17
RAMPA = np.array([[21.2, 50.9, 80.6], [24.2, 56.2, 88.1], [103.0, 146.1, 189.4], [250, 249, 245]]) / 255
CREME = np.array([250, 249, 245]) / 255
LUM = np.array([.2126, .7152, .0722])
def bayer(n):
    m = np.array([[0]])
    while m.shape[0] < n:
        m = np.block([[4 * m, 4 * m + 2], [4 * m + 3, 4 * m + 1]])
    return m
M4 = bayer(4)

# ---------- as fotos e as vagas (os mesmos recortes das -lum- de hoje) ----------
FONTE = {
    'industria': 'Petrochemical-Plant.jpg', 'energia': 'GHG.jpg', 'alimentos': 'wp9571086.jpg',
    'logistica': 'Container.jpg', 'tecnologia': 'AdobeStock_465836401-1-scaled.jpeg', 'saude': '02.jpg',
    'etica-auditoria': 'Coworkers_talking_in_factory_2K_20260917192906.jpeg',
    'lago-industria': 'Industrial_plant_reflecting_in_lake_2K_20260917203841.jpeg',
    'refinaria': 'refinaria-campo-ceu.jpg',
    # 29/09: as quatro fotos feitas no Google Flow (Nano Banana 2) para a tira de teste
    'flow-carbono': 'flow-gestao-carbono-4-recorte.jpg',   # 29/09: a 4a, recortada para o lago ocupar 1/4 como no ESG (o cru inteiro e -4.jpg); antes -2 (chamine) e a 1a
    'flow-iso': 'flow-implantacao-iso-6-recorte.jpg',   # 30/09: a 6a (escritorio baixo, pessoas e coleta seletiva); piso cortado 7%, ceu esticado; cru = -6.jpg
   #   # 30/09: a 5a (fabrica de vidro, linha vista pela janela); antes -4-recorte
   #   # 30/09: a 4a (tres colegas e o tablet), chao cortado e ceu esticado; o cru e -4.jpg
   #   # 30/09: a 3a (linha coberta com o inspetor); antes -2 (predio de vidro)
   #   # 29/09: a 2a (o predio de vidro); a 1a era flow-implantacao-iso.jpg
    'flow-smeta': 'flow-smeta-2.jpg',   # 29/09: a 2a, SEM recorte (a descida de 9% foi desfeita a pedido); o -recorte fica no disco   # 29/09: a 2a (operarios chegando ao portao); a 1a era flow-smeta.jpg
    'flow-esg': 'flow-gestao-carbono-3.jpg',   # 29/09: o lago claro (nome do arquivo cru ficou -carbono-3, era para o ESG); a 1a era flow-esg-sustentabilidade.jpg
}
# vaga -> (largura da reserva, altura da reserva, [(assunto, arquivo-base, ax, ay)])
# qc: a coluna da tira; os recortes foram casados com as -lum-qc de hoje (foto_coluna.py)
VAGAS = {
    'qc': (633, 788, [('energia', 'energia', 1.0, 1.0), ('industria', 'refinaria', 0.6, 1.0),
                      ('etica-auditoria', 'etica-auditoria', 0.9, 0.5), ('lago-industria', 'lago-industria', 0.9, 0.0)]),
    'sv': (562, 397, [(a, a, .5, .5) for a in ['industria', 'energia', 'alimentos', 'logistica', 'tecnologia', 'saude']]),
    'df': (562, 380, [(a, a, .5, .5) for a in ['industria', 'logistica', 'tecnologia']]),
    'st': (562, 422, [(a, a, .5, .5) for a in ['industria', 'logistica', 'alimentos', 'saude', 'tecnologia', 'energia']]),
    'nt': (900, 506, [(a, a, .5, .5) for a in ['tecnologia', 'industria', 'alimentos', 'logistica']]),
    # 29/09: a tira de teste com as fotos do Flow (mesma vaga da qc, sem espelhar)
    # 30/09: a ISO ancora na BASE (ay=1), para os pes nao serem cortados; o recorte dela ja vem espelhado
    'fl': (633, 788, [(a, a, .5, .5) for a in ['flow-carbono', 'flow-iso', 'flow-smeta', 'flow-esg']]),
}
COR_W = 900          # largura da foto em cor que o motor le


def enquadrar(im, W, H, ax=.5, ay=.5):
    w, h = im.size; e = max(W / w, H / h)
    cw, ch = int(round(W / e)), int(round(H / e))
    x0 = int(round((w - cw) * ax)); y0 = int(round((h - ch) * ay))
    return im.crop((x0, y0, x0 + cw, y0 + ch)).resize((W, H), Image.LANCZOS)


def curva(Y, R, gama_extra=None):
    if gama_extra: Y = np.power(np.maximum(Y, 0), gama_extra)
    v = np.clip(np.power(np.maximum(Y, 0), R['gama']), 1e-6, 1 - 1e-6)
    a, b = np.power(v, R['ctr']), np.power(1 - v, R['ctr'])
    return np.clip(R['piso'] + (1 - R['piso']) * a / (a + b) + R['brilho'], 0, 1)


def rampa(v):
    x = np.clip(v * 3, 0, 3); i = np.minimum(x.astype(int), 2); f = (x - i)[..., None]
    return RAMPA[i] * (1 - f) + RAMPA[i + 1] * f


def filtrar(rgb, R, gama_extra=None):
    """rgb em 0..1 (H, W, 3) -> rgb filtrado, ANTES da trama"""
    Y = rgb @ LUM
    Y2 = curva(Y, R, gama_extra)
    out = rgb * (Y2 / np.maximum(Y, 1e-3))[..., None]
    out = Y2[..., None] + (out - Y2[..., None]) * R['sat']
    SC = np.array(R['sombraCor']) / 255
    az = SC[None, None, :] * (Y2 / max(SC @ LUM, 1e-3))[..., None]
    t = np.clip(Y2 / max(R['sombra'], 1e-6), 0, 1); s = (t * t * (3 - 2 * t))[..., None]
    out = az * (1 - s) + out * s
    if R.get('luzForca', 0) > 0:      # as luzes: a partir de luzDe, para luzCor na mesma luminancia
        LC = np.array(R['luzCor']) / 255
        lz = LC[None, None, :] * (Y2 / max(LC @ LUM, 1e-3))[..., None]
        t2 = np.clip((Y2 - R['luzDe']) / max(1 - R['luzDe'], 1e-6), 0, 1); l = (t2 * t2 * (3 - 2 * t2))[..., None] * R['luzForca']
        out = out * (1 - l) + lz * l
    if R['mistura'] > 0:
        out = out * (1 - R['mistura']) + rampa(Y2) * R['mistura']
    return np.clip(out, 0, 1)


def tramar(rgb, R, veu=None, fade=None):
    H, W = rgb.shape[:2]; n = R['niveis'] - 1; cel = R['celula']
    yy, xx = np.mgrid[0:H, 0:W]
    cy, cx = (yy // cel).astype(int), (xx // cel).astype(int)
    if cel != 1:
        rgb = rgb[np.minimum(H - 1, (cy * cel).astype(int)), np.minimum(W - 1, (cx * cel).astype(int))]
    M = bayer(int(R.get('matriz', 4))); mn = M.shape[0]
    T = ((M[cy % mn, cx % mn] + .5) / (mn * mn))[..., None] - R.get('limiar', 0)
    if R.get('ruido', 0):
        rs = np.random.RandomState(7)          # o mesmo ruido a cada rodada (arquivo estavel)
        T = T + (rs.random_sample((H, W, 1)) - .5) * R['ruido']
    k = np.clip(np.floor(rgb * n + T), 0, n) / n
    k = k * CREME                              # o nivel mais claro e o CREME do site, nao o branco
    v = R['veu'] if veu is None else veu
    vv = np.full((H, W, 1), v)
    if fade is not None:
        vv = 1 - fade[..., None] * (1 - v)
    return k * (1 - vv) + CREME * vv


def salvar_rgb(arr, caminho, lossless=False, quality=90):
    im = Image.fromarray((np.clip(arr, 0, 1) * 255).round().astype(np.uint8), 'RGB')
    if lossless: im.save(caminho, lossless=True, quality=100, method=6)
    else: im.save(caminho, quality=quality, method=6)
    return os.path.getsize(caminho) // 1024


def vaga(suf):
    W, H, fotos = VAGAS[suf]
    for assunto, base, ax, ay in fotos:
        arq = FONTE[base]
        # 30/09: na tira (vaga fl) vale a versao com o CEU COMUM, se existir (ceu_comum.py)
        ceu = os.path.splitext(arq)[0] + '-ceu.jpg'
        if suf == 'fl' and os.path.exists(os.path.join(CRU, ceu)): arq = ceu
        src = Image.open(os.path.join(CRU, arq)).convert('RGB')
        # a foto em cor, no recorte da vaga, para o motor
        CH = int(round(COR_W * H / W))
        cor = enquadrar(src, COR_W, CH, ax, ay)
        n1 = '%s-cor-%s.webp' % (assunto, suf)
        cor.save(os.path.join(IMG, n1), quality=92, method=6)
        # a reserva: filtrada e tramada no tamanho da vaga
        rgb = np.asarray(enquadrar(src, W, H, ax, ay), np.float64) / 255
        n2 = '%s-cor-bayer-%s.webp' % (assunto, suf)
        kb = salvar_rgb(tramar(filtrar(rgb, RECEITA), RECEITA), os.path.join(IMG, n2), lossless=True)
        print('%-34s %dx%d  |  %-40s %dx%d  %d KB' % (n1, COR_W, CH, n2, W, H, kb))


def ifc():
    """o banner da IFC: 3:1, corte a 30% do topo (foto_banner.py), RGBA com o alfa
    = esvanecimento (creme a esquerda, foto inteira de 78% para a direita)"""
    LARG, ALT, INICIO, FIM, TOPO = 2400, 800, .30, .78, .30
    im = Image.open(os.path.join(CRU, 'refinaria-rio-ifc.jpg')).convert('RGB')
    w, h = im.size
    if w / h > 3:
        nw = round(h * 3); x0 = (w - nw) // 2; im = im.crop((x0, 0, x0 + nw, h))
    else:
        nh = round(w / 3); y0 = min(max(0, round(h * TOPO)), h - nh); im = im.crop((0, y0, w, y0 + nh))
    im = im.resize((LARG, ALT), Image.LANCZOS)
    rgb = np.asarray(im, np.float64) / 255
    # a gama propria da IFC, so na luminancia (como o Spirit: Y^gama antes da curva)
    Y = rgb @ LUM; Yg = np.power(Y, RECEITA['ifcGama'])
    rgb = np.clip(rgb * (Yg / np.maximum(Y, 1e-3))[..., None], 0, 1)
    x = (np.arange(LARG) + .5) / LARG
    t = np.clip((x - INICIO) / (FIM - INICIO), 0, 1); t = t * t * (3 - 2 * t)
    alfa = np.broadcast_to(t[None, :], (ALT, LARG))
    rgba = np.dstack([rgb, alfa])
    Image.fromarray((rgba * 255).round().astype(np.uint8), 'RGBA').save(
        os.path.join(IMG, 'banner-ifc-cor.webp'), quality=92, method=6)
    # uma prova filtrada e tramada, so para conferir a olho (nao entra no site)
    prova = tramar(filtrar(rgb, RECEITA), RECEITA, fade=alfa)
    salvar_rgb(prova, os.path.join(IMG, '_prova-banner-ifc-cor.webp'))
    print('banner-ifc-cor.webp %dx%d RGBA (alfa = esvanecimento), gama %.2f' % (LARG, ALT, RECEITA['ifcGama']))


if __name__ == '__main__':
    pedidos = [a for a in sys.argv[1:] if not a.startswith('-')] or list(VAGAS) + ['ifc']
    for p in pedidos:
        if p == 'ifc': ifc()
        else: vaga(p)
