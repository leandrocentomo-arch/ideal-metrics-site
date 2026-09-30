# -*- coding: utf-8 -*-
"""O MESMO CEU nas fotos da tira da home (30/09/2026).

    python _ferramentas/ceu_comum.py            # as quatro fotos da tira
    python _ferramentas/ceu_comum.py --prova    # so a folha antes/depois, sem gravar

«Garanta que as quatro fotos tenham o mesmo ceu, achei o da ISO um pouco mais escuro»
e «quero um ceu ligeiramente mais claro». Cada foto veio de uma geracao do Google
Flow, com o seu proprio entardecer: a da ISO e mais azul e escura, a do ESG e quase
creme. Aqui o ceu de todas passa a ser UM SO.

COMO. Nada e recortado nem colado: e uma correcao de cor que so pega no ceu.
  1. Acha o ceu de cada foto: desce linha a linha a partir do topo, seguindo a cor
     dominante da linha (o degrade muda devagar); pixel de ceu e o que esta perto
     dessa cor. Para quando menos de 15% da linha ainda e ceu.
  2. Mede o ceu LOCAL (media borrada so dos pixels de ceu): e o que a foto tem ali,
     sem a chamine, o vapor ou o telhado.
  3. O ceu COMUM e um perfil vertical unico: a media dos perfis das fotos, alisada,
     e clareada em CLAREAR na direcao do creme do site.
  4. Em cada pixel: cor += (ceu comum na linha) - (ceu local), com peso 1 no ceu e
     caindo a 0 conforme a cor se afasta do ceu (predio, chamine, gente). O vapor
     fica: ele e mais claro que o ceu em volta, e a diferenca e preservada.

As fotos cruas nao sao tocadas: sai <nome>-ceu.jpg ao lado, e o fotos_cor.py usa
esse arquivo. Rodar de novo depois de trocar qualquer uma das quatro fotos."""

import os, sys
import numpy as np
from PIL import Image, ImageFilter

SITE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CRU = os.path.join(os.path.dirname(SITE), '_tingir-fotos', 'FOTOS')
sys.path.insert(0, os.path.join(SITE, '_ferramentas'))

CLAREAR = 0.14          # «ligeiramente mais claro»: quanto o ceu comum anda na direcao do creme
CREME = np.array([250, 249, 245], np.float64)
PERTO = 22              # distancia (maior canal) para um pixel contar como ceu, na medida
PESO_DE, PESO_ATE = 26, 78   # a correcao vale 1 ate PESO_DE de distancia do ceu local e 0 de PESO_ATE em diante
LISO, LONGE = 3.0, 80   # desvio local maximo para «liso», e distancia maxima da cor da linha
SIGMA = 38              # borrado do ceu local, em px de uma foto de 896 de largura


def _blur(a, sigma):
    """gaussiana separavel em numpy (a PIL so borra 8 bits)"""
    r = int(sigma * 3); x = np.arange(-r, r + 1); k = np.exp(-x * x / (2.0 * sigma * sigma)); k /= k.sum()
    pad = np.pad(a, ((r, r), (0, 0)) + ((0, 0),) * (a.ndim - 2), mode='edge')
    a = sum(pad[i:i + a.shape[0]] * k[i] for i in range(2 * r + 1))
    pad = np.pad(a, ((0, 0), (r, r)) + ((0, 0),) * (a.ndim - 2), mode='edge')
    return sum(pad[:, i:i + a.shape[1]] * k[i] for i in range(2 * r + 1))


def medir(a):
    """a: H x W x 3 float. Devolve (mascara de ceu, perfil por linha, ultima linha de ceu)."""
    H, W = a.shape[:2]
    perfil = np.zeros((H, 3)); mask = np.zeros((H, W), bool)
    cor = np.median(a[0], axis=0); fim = 0
    for y in range(H):
        d = np.abs(a[y] - cor).max(axis=1)
        m = d < PERTO
        if m.mean() < 0.15: break
        cor = np.median(a[y][m], axis=0)
        perfil[y] = cor; mask[y] = m; fim = y
    # 2a passada: o ceu tambem e o que e LISO e nao esta longe da cor da linha. Pega o
    # degrade horizontal (a faixa esverdeada do lago, o canto mais claro), que a cor da
    # linha sozinha deixava de fora e que por isso sobrava como mancha.
    m1 = _blur(a, 2.0); m2 = _blur(a * a, 2.0)
    liso = np.sqrt(np.maximum(m2 - m1 * m1, 0)).max(axis=2) < LISO
    longe = np.abs(a - perfil[:, None, :]).max(axis=2)
    linhas = (np.arange(H) <= fim)[:, None]
    mask = linhas & (mask | (liso & (longe < LONGE)))
    return mask, perfil, fim


def ceu_local(a, mask, sigma):
    m = mask.astype(np.float64)
    num = _blur(a * m[..., None], sigma); den = _blur(m, sigma)
    return num / np.maximum(den, 1e-4)[..., None], den


def perfil_comum(perfis, fins, H):
    """media dos perfis onde cada foto ainda tem ceu; alisada; clareada"""
    T = np.zeros((H, 3)); n = np.zeros(H)
    for p, f in zip(perfis, fins):
        T[:f + 1] += p[:f + 1]; n[:f + 1] += 1
    ult = np.max(np.nonzero(n)[0])
    T[:ult + 1] /= n[:ult + 1, None]; T[ult + 1:] = T[ult]
    r = 30; x = np.arange(-r, r + 1); k = np.exp(-x * x / (2.0 * 14 * 14)); k /= k.sum()
    pad = np.pad(T, ((r, r), (0, 0)), mode='edge')
    T = sum(pad[i:i + H] * k[i] for i in range(2 * r + 1))
    return T * (1 - CLAREAR) + CREME * CLAREAR


def aplicar(a, mask, fim, T, sigma):
    H, W = a.shape[:2]
    L, den = ceu_local(a, mask, sigma)
    dist = np.abs(a - L).max(axis=2)
    t = np.clip((dist - PESO_DE) / float(PESO_ATE - PESO_DE), 0, 1)
    w = 1 - t * t * (3 - 2 * t)
    w = np.maximum(w, _blur(mask.astype(np.float64), 1.5))     # todo o ceu medido entra inteiro
    w *= np.clip(den / 0.12, 0, 1)                    # longe de qualquer ceu medido, nada muda
    # abaixo do fim do ceu a correcao some em 40 linhas (agua e chao ficam como estao)
    yy = np.arange(H)[:, None]; w *= np.clip((fim + 40 - yy) / 40.0, 0, 1)
    return np.clip(a + (T[:, None, :] - L) * w[..., None], 0, 255), w


def unificar(caminhos, gravar=True):
    fotos = [np.asarray(Image.open(c).convert('RGB'), np.float64) for c in caminhos]
    H = fotos[0].shape[0]
    assert all(f.shape[0] == H for f in fotos), 'as fotos precisam ter a mesma altura: %s' % [f.shape for f in fotos]
    med = [medir(f) for f in fotos]
    T = perfil_comum([m[1] for m in med], [m[2] for m in med], H)
    saidas = []
    for c, f, (mask, perfil, fim) in zip(caminhos, fotos, med):
        out, w = aplicar(f, mask, fim, T, SIGMA * f.shape[1] / 896.0)
        dest = os.path.splitext(c)[0] + '-ceu.jpg'
        if gravar: Image.fromarray(out.round().astype(np.uint8), 'RGB').save(dest, quality=95)
        antes = perfil[[int(H * .1), int(H * .4)]].round().astype(int).tolist()
        print('%-42s ceu ate %2.0f%%  | antes (10%%, 40%%) %s  -> comum %s' % (
            os.path.basename(c), 100.0 * fim / H, antes, T[[int(H * .1), int(H * .4)]].round().astype(int).tolist()))
        saidas.append((f, out, dest))
    return saidas, T


def folha(saidas, caminho):
    n = len(saidas); h = 420
    tiras = []
    for k in (0, 1):
        linha = [Image.fromarray(s[k].round().astype(np.uint8), 'RGB') for s in saidas]
        linha = [im.resize((int(im.width * h / im.height), h), Image.LANCZOS) for im in linha]
        L = Image.new('RGB', (sum(i.width for i in linha), h), 'white'); x = 0
        for im in linha: L.paste(im, (x, 0)); x += im.width
        tiras.append(L)
    F = Image.new('RGB', (tiras[0].width, 2 * h + 10), 'white')
    F.paste(tiras[0], (0, 0)); F.paste(tiras[1], (0, h + 10)); F.save(caminho, quality=90)


if __name__ == '__main__':
    import fotos_cor
    nomes = [fotos_cor.FONTE[a] for a in ['flow-carbono', 'flow-iso', 'flow-smeta', 'flow-esg']]
    saidas, T = unificar([os.path.join(CRU, n) for n in nomes], gravar='--prova' not in sys.argv)
    prova = os.path.join(os.path.dirname(os.path.dirname(SITE)), 'tmp', 'ceu-comum-prova.jpg')
    os.makedirs(os.path.dirname(prova), exist_ok=True); folha(saidas, prova); print('prova:', prova)
