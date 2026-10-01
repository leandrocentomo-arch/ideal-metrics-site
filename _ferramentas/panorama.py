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

--ceu-creme mescla o ceu no creme da pagina (#FAF9F5): creme exato no alto, degrade ate o ceu da foto
no horizonte. Testado em 30/09 e REPROVADO pelo Leandro («volte ao azul que era»): a tira usa
--alvo 0.705 (menos rua) SEM --ceu-creme. A opcao fica aqui guardada.

--ceu-azul K puxa o perfil do ceu K do caminho para AZUL (168,192,250). A tira usa 0.7.
--ceu-claro K, depois, clareia K do caminho para (250,250,255). A tira usa 0.2.
--ceu-plano deixa o ceu num tom so (o do alto), sem a faixa de manchas perto do horizonte.
--tom D,F gira os azuis D graus e multiplica a saturacao deles por F (girar_tom); --ceu-cor R,G,B
da ao ceu plano uma cor exata. Testado em 30/09 (noite), «como as outras fotos» (--tom -25,2 --ceu-cor
25,185,240) e desfeito («volte o azul claro como estava»): a tira usa o comando SEM --tom e --ceu-cor.
Comando da tira desde 30/09 (tarde): --alvo 0.724 --pe 0.8135 --teto 0.514 --ceu-azul 0.7 --ceu-claro 0.2 --ceu-plano

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
AZUL = np.array([168, 192, 250], np.float64)   # o azul para onde --ceu-azul puxa o perfil do ceu


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


def montar(caminhos, alvo=0.66, espelhar=False, pe=None, teto_fixo=None, creme=False, azul=0.0, claro=0.0, plano=False, tom=None, ceu_cor=None, limpo=0.0):
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
    if tom: a = girar_tom(a, *tom)

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
    if azul:                                            # 30/09: «o ceu mais azulado»
        Tm = Tm * (1 - azul) + AZUL * azul
    if claro:                                           # 30/09: «a cor do ceu um pouco mais clara»
        Tm = Tm * (1 - claro) + np.array([250.0, 250.0, 255.0]) * claro
    if plano:
        # 30/09: «os cards estao com esta mancha de fundo». O ceu clareava perto do horizonte e
        # cruzava o limiar de um nivel da trama: ali a textura da foto virava manchas creme numa
        # faixa atravessando a tira. Ceu num tom so, o do alto; o vapor continua (e residuo).
        # o tom e o do ALTO (linhas 0..120): a media das linhas 100..400 caiu em cima do limiar
        # da trama e o ruido fino da foto virou mancha no ceu inteiro
        Tm = np.repeat((np.array(ceu_cor, np.float64) if ceu_cor else Tm[0:120].mean(axis=0))[None, :], Tm.shape[0], axis=0)
        print('  ceu num tom so: %s' % Tm[0].round().astype(int).tolist())

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
    if creme:
        lim = falta + int(round(pe * H)) if pe is not None else HM
        m = ceu_creme(m, Tm, lim)
    if plano:
        lim = falta + int(round(pe * H)) if pe is not None else HM
        m = ceu_liso(m, Tm, lim)
    if limpo and plano:
        # 01/10: --ceu-limpo K. Acima do telhado, o que desvia ATE K tons do ceu chapado vira o ceu (o Flow deixa
        # fantasmas de 1 a 3 tons que a trama realca em fios e manchas); vapor e fumaca desviam muito mais e ficam
        ceu0 = Tm[0]
        alto = m[:a_px]
        d = np.abs(alto - ceu0).max(axis=2)
        t = np.clip((limpo * 1.6 - d) / (limpo * 0.6), 0, 1)[..., None]
        m[:a_px] = alto * (1 - t) + ceu0 * t
        print('  ceu limpo: %d px encostados no ceu (desvio ate %g)' % (int((t[..., 0] > .5).sum()), limpo))
    print('mestra %dx%d (%.2f:1) | telhado a %.0f%% | ponto mais alto a %.0f%%' % (W, HM, W / float(HM), 100.0 * a_px / HM, 100.0 * (a_px - (teto - topo)) / HM))
    return np.clip(m, 0, 255)


def girar_tom(a, desloc, fsat):
    """30/09: «corrija a cor da panoramica para ficar como as outras fotos». Medido: 79% da cena
    tem tom entre 210 e 240 graus (mediana 226, azul-violeta do entardecer do Flow) e saturacao
    mediana 59; nas fotos de Servicos, 81 a 90% ficam entre 180 e 210 graus (medianas 195 a 204,
    azul-ciano) e a saturacao mediana e 164. Os azuis giram `desloc` graus e a saturacao deles
    multiplica por `fsat`; peso 1 entre 180 e 260 graus, rampa de 20 graus para fora (amarelos,
    vermelhos e as janelas acesas nao andam). A luminosidade (V) fica."""
    import cv2
    H = cv2.cvtColor(np.clip(a, 0, 255).astype(np.uint8), cv2.COLOR_RGB2HSV_FULL).astype(np.float64)
    h = H[..., 0] * 360 / 256.0
    w = np.clip(np.minimum((h - 160) / 20.0, (280 - h) / 20.0), 0, 1)
    H[..., 0] = ((h + desloc * w) % 360) * 256 / 360.0
    H[..., 1] = np.clip(H[..., 1] * (1 + (fsat - 1) * w), 0, 255)
    out = cv2.cvtColor(np.clip(np.rint(H), 0, 255).astype(np.uint8), cv2.COLOR_HSV2RGB_FULL).astype(np.float64)
    print('  tom: azuis %+.0f graus, saturacao x%.2f' % (desloc, fsat))
    return out


def ceu_liso(m, Tm, lim, perto=16, de=5.0, ate=15.0):
    """CEU LISO (30/09/2026: «os cards estao com esta mancha de fundo»). No ceu (o que esta perto
    do tom do ceu e se liga ao alto da foto) a textura fina das nuvens do Flow cruzava o limiar
    de um nivel da trama e virava manchas. Aqui o residuo pequeno (|luz| < de) vai a zero e o
    grande (vapor, |luz| > ate) fica inteiro, com rampa suave entre os dois."""
    import cv2
    HM = m.shape[0]
    T = Tm[:HM][:, None, :]
    res = m - T
    lum = res.mean(axis=2)
    linhas = (np.arange(HM) < lim)[:, None]
    regiao = (((np.abs(res).max(axis=2) < perto) | (lum > 3)) & linhas).astype(np.uint8)
    n, lab = cv2.connectedComponents(regiao, connectivity=4)
    ceu = np.isin(lab, np.unique(lab[0][lab[0] > 0]))
    ceu = cv2.erode(ceu.astype(np.uint8), np.ones((3, 3), np.uint8)) > 0     # nao encosta nas bordas dos objetos
    # sobre as chamines (mestra x < 1200) o corte e brando: as pontas tenues do vapor ficam
    W_ = m.shape[1]; xs = np.arange(W_)[None, :]
    de_ = np.where(xs < 1200, 1.5, de); ate_ = np.where(xs < 1200, 5.0, ate)
    k = np.clip((np.abs(lum) - de_) / (ate_ - de_), 0, 1); k = k * k * (3 - 2 * k)
    k = cv2.GaussianBlur(k.astype(np.float32), (0, 0), 1.2)
    novo = T + res * k[..., None]
    out = m.copy(); out[ceu] = novo[ceu]
    print('  ceu liso: %.0f%% da mestra; textura fina tirada, vapor mantido' % (100.0 * ceu.mean()))
    return out


def ceu_creme(m, Tm, lim, perto=13, borda=20, Y0=450, Y1=920, D1=14):
    """O CEU SE MESCLA NO CREME DA PAGINA (30/09/2026).
    1a volta (creme chapado, vapor invertido em cinza) nao ficou boa. Agora e um DEGRADE: creme
    exato no alto (a tira emenda no fundo da pagina sem linha) e o ceu da foto voltando aos
    poucos ate o horizonte (linha Y1, logo acima dos telhados), com o vapor natural.
    Ceu = o que esta perto do perfil do ceu da linha (Tm) E se liga ao alto da foto; o vapor
    entra junto. Objetos (tanques, chamines, moinhos, telhados) ficam intactos: o tanque mais
    claro fica a 28 niveis do ceu. Na trama em cor (sat 1), tom quente 2 a 4 niveis abaixo do
    creme vira pontinho amarelo: por isso a cor do ceu sai de uma rampa pela luminosidade, que
    esfria sem deixar o azul cair antes do vermelho (ver o fim da funcao)."""
    import cv2
    HM = m.shape[0]
    T = Tm[:HM][:, None, :]
    res = m - T
    dist = np.abs(res).max(axis=2)
    lum = res.mean(axis=2)
    linhas = (np.arange(HM) < lim)[:, None]
    vapor = (lum > 3) & (res.min(axis=2) > -4) & linhas
    regiao = (((dist < perto) | vapor) & linhas).astype(np.uint8)
    n, lab = cv2.connectedComponents(regiao, connectivity=4)
    topo = np.unique(lab[0][lab[0] > 0])
    ceu = np.isin(lab, topo)
    perto_ceu = cv2.dilate(ceu.astype(np.uint8), np.ones((5, 5), np.uint8)) > 0
    w = np.where(vapor, 1.0, np.clip((borda - dist) / float(borda - perto + 1), 0, 1)) * perto_ceu
    w = cv2.GaussianBlur(w.astype(np.float32), (0, 0), 0.8)[..., None]
    t = np.clip((np.arange(HM) - Y0) / float(Y1 - Y0), 0, 1); t = (t * t * (3 - 2 * t))[:, None, None]
    creme = ceu_comum.CREME[None, None, :]
    alvo = creme * (1 - t) + m * t
    out = m * (1 - w) + alvo * w
    # rampa de cor do ceu pela luminosidade: vermelho e verde descem, o azul fica no alto: o ceu
    # esfria aos poucos, sem degrau e sem amarelo.
    reg = w[..., 0] > 0.01
    L = out[reg].mean(axis=1)
    Lc = ceu_comum.CREME.mean()                                       # 248: a luminosidade do creme
    d = np.maximum(Lc - L, 0)
    d = np.where(d < 1.5, 0, d)                                       # o que e quase creme vira creme exato
    # A trama 2x2 nao tem meio-termo entre o creme e o 1o nivel (25% dos pontos): um degrade
    # continuo vira uma FAIXA. Na passagem (d de 0 a D1) cada pixel sorteia: fica creme ou ja
    # e o ceu de d = D1, com chance d/D1. A densidade de pontinhos sobe sem linha, como na trama.
    # o sorteio e feito em graos de 2x2 alinhados: a WebP guarda a cor em blocos de 2x2 e, com
    # sorteio pixel a pixel, inventava pontinhos amarelo-esverdeados na passagem
    rs = np.random.RandomState(7)
    HM_, W_ = m.shape[:2]
    grao = rs.random_sample(((HM_ + 1) // 2, (W_ + 1) // 2)).repeat(2, axis=0).repeat(2, axis=1)[:HM_, :W_]
    sorteio = grao[reg]
    passa = (d > 0) & (d < D1)
    d = np.where(passa, np.where(sorteio < d / D1, D1, 0), d)
    # fora do creme exato o azul vai ao maximo (255) e so desce depois de 25 niveis: a trama mistura
    # o quase-branco com o creme das luzes e o azul, no limite, cairia primeiro (pontinho amarelo)
    out[reg] = np.stack([250 - 1.3 * d, 249 - 1.15 * d, np.where(d > 0, 255 - 1.0 * np.maximum(d - 25, 0), 245)], axis=1)
    quase = reg & (np.abs(out - creme).max(axis=2) < 0.5)   # (so para o relatorio)
    print('  ceu mesclado no creme: regiao %.0f%% da mestra, creme exato em %.0f%%, degrade das linhas %d a %d' % (100.0 * ceu.mean(), 100.0 * quase.mean(), Y0, Y1))
    return out


def gravar(m, ordem, prefixo='tira'):
    HM, W = m.shape[:2]
    mestra = Image.fromarray(m.round().astype(np.uint8), 'RGB')
    dest = os.path.join(IMG, '%s-panorama-cor.webp' % prefixo)
    mestra.save(dest, quality=90, method=6)
    print('%s  %d KB' % (os.path.basename(dest), os.path.getsize(dest) // 1024))
    R = fotos_cor.RECEITA
    # 30/09 (noite): a RESERVA CONTINUA. Sem o motor (file://, sem WebGL) cada card mostrava o seu
    # recorte e a panoramica nao emendava. A mestra inteira, filtrada e tramada, vai de fundo da tira
    # (CSS .sh-tira--flow:not(.gl-on)), presa como o motor: largura toda, chao na base.
    rgb = np.asarray(mestra, np.float64) / 255
    arq = os.path.join(IMG, '%s-panorama-cor-bayer.webp' % prefixo)
    # SEM a trama: reduzida na tela, a trama de 1 px vira moire; a reserva vai so no tom (a trama e do motor)
    kb = fotos_cor.salvar_rgb(fotos_cor.filtrar(rgb, R), arq, quality=90)
    print('  %-34s %dx%d  %d KB' % (os.path.basename(arq), W, HM, kb))
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
    creme = '--ceu-creme' in args          # 30/09: o ceu vira o creme da pagina
    azul = opt('--ceu-azul', 0.0, float)   # 30/09: quanto o ceu vai para o AZUL (0 a 1); a tira usa 0.7
    claro = opt('--ceu-claro', 0.0, float) # 30/09: depois do azul, quanto o ceu clareia para o branco-azulado; a tira usa 0.2
    plano = '--ceu-plano' in args          # 30/09: ceu num tom so (sem a faixa de manchas perto do horizonte)
    t_ = opt('--tom', None)                # 30/09: «como as outras fotos»: desloc,fsat (ex. -25,2)
    tom = tuple(float(v) for v in t_.split(',')) if t_ else None
    c_ = opt('--ceu-cor', None)            # 30/09: com --ceu-plano, a cor exata do ceu (R,G,B)
    ceu_cor = tuple(float(v) for v in c_.split(',')) if c_ else None
    limpo = opt('--ceu-limpo', 0.0, float)   # 01/10: encosta no ceu o que desvia ate K tons (a tira2 usa 6)
    pe = opt('--pe', None, float)       # onde o predio encosta no piso, em fracao da altura da foto (alisa o piso dali para baixo)
    espelhar = '--espelhar' in args; prova = '--prova' in args
    fotos = [x for x in args if not x.startswith('--')]
    m = montar(fotos, alvo, espelhar, pe, teto_fixo, creme, azul, claro, plano, tom, ceu_cor, limpo)
    if prova:
        p = os.path.join(os.path.dirname(os.path.dirname(SITE)), 'tmp', 'panorama-prova.jpg')
        os.makedirs(os.path.dirname(p), exist_ok=True)
        im = Image.fromarray(m.round().astype(np.uint8), 'RGB'); im.thumbnail((1800, 1800)); im.save(p, quality=88); print('prova:', p)
    else:
        gravar(m, ordem, prefixo)
