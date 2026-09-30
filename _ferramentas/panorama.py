# -*- coding: utf-8 -*-
"""A TIRA DA HOME COMO UMA FOTO SO (30/09/2026).

    python _ferramentas/panorama.py <foto.jpg> [<foto-direita.jpg>] --ordem carbono,iso,smeta,esg
                                    [--alvo 0.66] [--espelhar] [--prova]

Os quatro cards da tira mostram UMA panoramica continua: cada card e uma janela de
um quarto da largura. A foto vem do Google Flow, que so gera ate 16:9; a tira tem
de 2,40:1 (telas ate 1400 px) a 3,33:1 (1920 px). Este script transforma o que o
Flow entrega no que o site usa:

  img/tira-panorama-cor.webp            a MESTRA, 2,40:1, em cor: e a textura que o
                                        motor (js/trama.js, cfg.panorama) prende a
                                        tira inteira e trama ao vivo
  img/tira-<servico>-cor-bayer.webp     um quarto por card, 633 x 788, ja filtrado e
                                        tramado: a reserva sem WebGL e o telefone

COMO A MESTRA E MONTADA.
  1. Uma foto (16:9) ou duas metades lado a lado (esquerda, direita).
  2. O ceu e medido e clareado pelo mesmo metodo do ceu_comum.py.
  3. A «linha do telhado» e a altura mediana em que o ceu acaba, coluna a coluna
     (a chamine, mais alta, nao entra na conta). Ela vai para --alvo da altura da
     mestra (0,66 = cenario no terco de baixo). O ceu que faltar em cima e esticado
     da faixa limpa do alto; o chao que sobrar embaixo e cortado.
  4. O motor mostra a mestra sempre na largura inteira da tira e corta o que sobra
     pelo ALTO; o chao fica. Por isso a mestra tem a proporcao da tira MAIS ESTREITA
     (2,40:1): em tela larga some ceu, nunca cenario.

--pe diz onde o predio encosta no piso (fracao da altura da foto de entrada): dali para
baixo o piso e alisado. Nas telas de 1792 x 1008 desta tira, o pe esta em 820/1008 = 0,8135.

--teto fixa a linha do telhado (fracao da altura da foto de entrada). Desde 30/09 a tira usa
--teto 0.514, a mediana medida antes do telhado em shed do SMETA, para a cena nao descer.

--ordem diz que servico esta em cada quarto, da esquerda para a direita; so da nome
aos arquivos de reserva."""

import os, sys
import numpy as np
from PIL import Image, ImageOps

SITE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG = os.path.join(SITE, 'img')
sys.path.insert(0, os.path.join(SITE, '_ferramentas'))
import ceu_comum, fotos_cor

RAZAO = 2.40            # largura / altura da mestra = a tira mais estreita do desktop
LARG_MAX = 3200
CARD_W, CARD_H = 633, 788


def skyline(mask):
    """linha, por coluna, onde o ceu acaba (primeiro pixel que nao e ceu, de cima para baixo)"""
    H, W = mask.shape
    nao = ~mask
    # uma coluna so conta como «acabou o ceu» quando ha 6 pixels seguidos sem ceu
    k = 6; run = np.zeros((H, W), bool); acc = np.zeros(W, int)
    for y in range(H):
        acc = np.where(nao[y], acc + 1, 0); run[y] = acc >= k
    tem = run.any(axis=0)
    return np.where(tem, run.argmax(axis=0) - (k - 1), H)


def montar(caminhos, alvo=0.66, espelhar=False, pe=None, teto_fixo=None):
    ims = [Image.open(c).convert('RGB') for c in caminhos]
    if len(ims) == 2:                                   # duas metades: mesma altura, lado a lado
        h = max(i.height for i in ims)                  # a metade menor (download 1K) sobe; a mestra nao perde resolucao
        ims = [i.resize((round(i.width * h / i.height), h), Image.LANCZOS) for i in ims]
        im = Image.new('RGB', (ims[0].width + ims[1].width, h)); im.paste(ims[0], (0, 0)); im.paste(ims[1], (ims[0].width, 0))
    else:
        im = ims[0]
    if espelhar: im = ImageOps.mirror(im)
    if im.width > LARG_MAX: im = im.resize((LARG_MAX, round(im.height * LARG_MAX / im.width)), Image.LANCZOS)
    a = np.asarray(im, np.float64); H, W = a.shape[:2]

    mask, perfil, fim = ceu_comum.medir(a)
    sk = skyline(mask)
    teto = int(np.median(sk)); topo = int(sk.min())
    if teto_fixo is not None:                           # um telhado novo alto (o shed do SMETA) puxa a mediana para cima e desce a cena toda
        print('  telhado medido a %.0f%%, fixado em %.1f%% (--teto)' % (100.0 * teto / H, 100.0 * teto_fixo)); teto = int(round(teto_fixo * H))
    print('entrada %dx%d | ceu ate %.0f%% | telhado (mediana) a %.0f%% | ponto mais alto a %.0f%%' % (W, H, 100.0 * fim / H, 100.0 * teto / H, 100.0 * topo / H))

    HM = int(round(W / RAZAO)); a_px = int(round(alvo * HM))
    chao = H - teto                                     # o que ha do telhado para baixo
    if chao < HM - a_px:                                # falta chao: o telhado desce (nao se inventa chao)
        a_px = HM - chao; print('  pouco chao na foto: o telhado vai a %.0f%% da mestra' % (100.0 * a_px / HM))
    base = teto + (HM - a_px)                           # ultima linha da foto que entra (exclusiva)
    falta = a_px - teto                                 # linhas de ceu que a foto nao tem

    # O CEU DA MESTRA e um perfil vertical unico e liso, do alto ate o telhado: o perfil
    # medido na foto (0..teto) ESTICADO para a altura nova (0..a_px). Estica-se o PERFIL,
    # nao os pixels: a chamine e o vapor ficam do tamanho que tem. Abaixo do telhado (o
    # ceu que aparece entre os tanques) o perfil segue na escala da foto.
    ys = np.arange(HM, dtype=np.float64)
    fonte = np.where(ys < a_px, ys * teto / float(max(a_px, 1)), teto + (ys - a_px))
    fonte = np.clip(fonte, 0, fim)
    Tm = np.stack([np.interp(fonte, np.arange(fim + 1), perfil[:fim + 1, c]) for c in range(3)], axis=1)
    r = 40; x = np.arange(-r, r + 1); k = np.exp(-x * x / (2.0 * 18 * 18)); k /= k.sum()
    pad = np.pad(Tm, ((r, r), (0, 0)), mode='edge'); Tm = sum(pad[i:i + HM] * k[i] for i in range(2 * r + 1))
    Tm = Tm * (1 - ceu_comum.CLAREAR) + ceu_comum.CREME * ceu_comum.CLAREAR

    if falta >= 0:
        T = Tm[falta:falta + H] if falta + H <= HM else np.vstack([Tm[falta:], np.repeat(Tm[-1:], falta + H - HM, 0)])
        corr, _ = ceu_comum.aplicar(a, mask, fim, T, ceu_comum.SIGMA * W / 896.0)
        alto = np.repeat(Tm[:falta][:, None, :], W, axis=1)
        # um grao leve no ceu novo, para ele nao sair mais liso que o resto
        rs = np.random.RandomState(11); alto = alto + rs.normal(0, 1.2, alto.shape[:2])[..., None]
        m = np.vstack([alto, corr[:base]])
        print('  ceu novo: %d linhas (perfil esticado; chamine e vapor no tamanho da foto)' % falta)
    else:
        T = np.vstack([np.repeat(Tm[:1], -falta, 0), Tm])[:H]
        corr, _ = ceu_comum.aplicar(a, mask, fim, T, ceu_comum.SIGMA * W / 896.0)
        m = corr[-falta:base]
    assert m.shape[0] == HM, (m.shape, HM)

    if pe is not None:
        # O PISO. As telas de base tinham o piso em ladrilho espelhado (desenha um
        # zigue-zague) e o piso de verdade so sob o escritorio. Aqui o piso todo vai
        # para a cor mediana de cada linha, guardando 25% da textura; o que se afasta
        # muito dessa cor (pes, sombras, o pe dos tanques) fica como esta.
        y0 = falta + int(round(pe * H)) + 8
        if 0 < y0 < HM:
            faixa = m[y0:]
            med = np.median(faixa, axis=1)[:, None, :]
            dev = faixa - med
            mag = np.abs(dev).max(axis=2)
            t = np.clip((mag - 16) / 28.0, 0, 1); fica = (t * t * (3 - 2 * t))[..., None]
            m[y0:] = med + dev * (fica + (1 - fica) * 0.25)
            print('  piso alisado a partir da linha %d (%.0f%% da mestra)' % (y0, 100.0 * y0 / HM))
    print('mestra %dx%d (%.2f:1) | telhado a %.0f%% | ponto mais alto a %.0f%%' % (W, HM, W / float(HM), 100.0 * a_px / HM, 100.0 * (a_px - (teto - topo)) / HM))
    return np.clip(m, 0, 255)


def gravar(m, ordem, prefixo='tira'):
    HM, W = m.shape[:2]
    mestra = Image.fromarray(m.round().astype(np.uint8), 'RGB')
    dest = os.path.join(IMG, '%s-panorama-cor.webp' % prefixo)
    mestra.save(dest, quality=90, method=6)
    print('%s  %d KB' % (os.path.basename(dest), os.path.getsize(dest) // 1024))
    R = fotos_cor.RECEITA
    for i, nome in enumerate(ordem):
        q = mestra.crop((round(i * W / 4.0), 0, round((i + 1) * W / 4.0), HM))
        q = q.resize((CARD_W, round(q.height * CARD_W / q.width)), Image.LANCZOS)
        q = q.crop((0, q.height - CARD_H, CARD_W, q.height)) if q.height >= CARD_H else q.resize((CARD_W, CARD_H), Image.LANCZOS)
        rgb = np.asarray(q, np.float64) / 255
        arq = os.path.join(IMG, '%s-%s-cor-bayer.webp' % (prefixo, nome))
        kb = fotos_cor.salvar_rgb(fotos_cor.tramar(fotos_cor.filtrar(rgb, R), R), arq, lossless=True)
        print('  %-34s %dx%d  %d KB' % (os.path.basename(arq), CARD_W, CARD_H, kb))
    return dest


if __name__ == '__main__':
    args = sys.argv[1:]
    def opt(nome, padrao, tipo=str):
        if nome in args:
            i = args.index(nome); v = tipo(args[i + 1]); del args[i:i + 2]; return v
        return padrao
    alvo = opt('--alvo', 0.66, float); ordem = opt('--ordem', 'carbono,iso,smeta,esg').split(',')
    prefixo = opt('--prefixo', 'tira')
    teto_fixo = opt('--teto', None, float)   # fixa a linha do telhado (fracao da altura), em vez da mediana medida
    pe = opt('--pe', None, float)       # onde o predio encosta no piso, em fracao da altura da foto (alisa o piso dali para baixo)
    espelhar = '--espelhar' in args; prova = '--prova' in args
    fotos = [x for x in args if not x.startswith('--')]
    m = montar(fotos, alvo, espelhar, pe, teto_fixo)
    if prova:
        p = os.path.join(os.path.dirname(os.path.dirname(SITE)), 'tmp', 'panorama-prova.jpg')
        os.makedirs(os.path.dirname(p), exist_ok=True)
        im = Image.fromarray(m.round().astype(np.uint8), 'RGB'); im.thumbnail((1800, 1800)); im.save(p, quality=88); print('prova:', p)
    else:
        gravar(m, ordem, prefixo)
