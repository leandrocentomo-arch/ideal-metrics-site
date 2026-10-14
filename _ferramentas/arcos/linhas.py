# -*- coding: utf-8 -*-
"""Mapa de linhas da secao Conhecimento (14/10/2026), no lugar dos circulos.

Pedido do Leandro: «repare que temos a interseccao entre temas de gestao e normas, onde uma mesma norma se aplica
para mais do que um tema»; das quatro propostas, a escolhida foi o mapa de linhas («coloque a linha de metro, mas nao
chame de linha de metro»). Nada na pagina fala em metro, estacao ou baldeacao. No mesmo dia:
  «mantenha o mesmo titulo»; «faca uma segunda secao (para testar) como este esquema ficaria na vertical»;
  «para os dois, deixe o nome das normas evidentes»; «deixe as linhas finas»; ao ver no ar, «mais finas, e que sejam
  clicaveis»; «os setores (os temas) mais destacados»; «a fonte esta pequena em comparacao com o resto do site»;
  «vamos ter que tirar a SA 8000 do esquema, nao e mais utilizada»; «nao quero as escritas coloridas»;
  «aprimore a apresentacao, esta bem feia ainda»; «deixe as linhas mais finas, mesmo as principais, e no hover a
  linha principal nao pode passar por cima»; «deixe a largura das normas equalizada: quanto mais igual for a largura
  dos baloes, mais agradavel visualmente»; a ISO 39002 sai (nao e certificavel; fica so na pagina da ISO 39001,
  como treinamento e base para a gestao de riscos de seguranca viaria); depois, «pode ficar mais delicado, agora
  estou achando muito grande em relacao ao site» (letra de 15 para 13, temas de 21 para 17, etiquetas de 28 para 24
  de altura) e «quero efeito de entrada onde, ao visualizar, as normas brotam do tema».
Os circulos foram guardados em Ideal Metrics/secoes-guardadas/conhecimento-circulos.html (python monta.py guardar).

Desenho: «Sistemas de gestao ISO» e o eixo; cada um dos oito temas sai dele como um ramal, a partir da norma ISO que
liga o tema ao sistema de gestao (o mesmo ponto de contato dos circulos). As normas sao ETIQUETAS SOBRE A LINHA, no
desenho das etiquetas da casa (creme, contorno fino, canto de 3 px), todas da MESMA largura (W1; so os dois nomes que
nao cabem, Rainforest Alliance e Observatorio setorial, vao a W2). A norma do encontro com o eixo leva contorno na
tinta e seminegrito. O nome do eixo fica a esquerda dele; os nomes dos ramais, na ponta de cada um. Sem a SA 8000, ESG
e Responsabilidade social nao tem norma comum: viram linhas proprias, numa faixa embaixo com Estudos (a divisao de
inteligencia, linha tracejada em vermelho), cada uma com o nome em cima do comeco da linha. Todo texto na tinta
(#14304C); a cor fica so nas linhas. No hover de um ramal os outros recuam pelo texto e pelo traco, nunca pelo fundo
das etiquetas: o creme delas continua opaco e o eixo nao aparece por cima.

ENTRADA (JS abaixo): quando o mapa entra na tela, o eixo se desenha da esquerda e as normas do encontro aparecem nele;
em seguida cada tema surge no proprio nome e as normas BROTAM DELE: saem do ponto do nome, pequenas e transparentes, e
deslizam pela linha ate o lugar, enquanto a linha cresce do nome ate o eixo. Cada peca leva no style o ponto de onde
brota (--dx, --dy) e o atraso (--d); as linhas, o ponto de onde crescem (--ox, --oy). Sem JS, ou com movimento
reduzido, o mapa aparece pronto.

mapa_h(): eixo horizontal, ramais verticais (a secao da home). mapa_v(): eixo vertical, ramais horizontais (teste)."""

import json, math, os
import arcos

AQUI = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(os.path.dirname(AQUI))
# fora do mapa e da lista do celular (continuam no arcos.py so para os circulos guardados, estado de 13/10/2026):
#   SA 8000, 14/10/2026: «nao e mais utilizada»;
#   ISO 39002, 14/10/2026: guia de boas praticas, nao certificavel; nao entra como norma do tema.
FORA = {'SA 8000', 'ISO 39002'}
FS, PH, BL = 13, 24, 4.6      # etiqueta: corpo da letra, altura e descida da linha de base (unidades do viewBox)
W1, W2 = 104, 138             # as duas larguras de etiqueta (medidas no Edge: ISO/IEC 27001 a 13 seminegrito tem 81)
GAP = 18                      # vao entre etiquetas vizinhas numa linha horizontal
NF, EF, LH = 17, 18, 20       # nome do tema, nome do eixo e entrelinha dos nomes
# ordem dos ramais: a do arcos.py com Saude e seguranca antes de Seguranca viaria, para os ramais longos se
# repartirem entre cima e baixo (carbono, 4 normas, em cima; NRs, 3, embaixo) e o desenho ficar equilibrado
ORDEM = ['qualidade', 'ambiente', 'carbono', 'alimentos', 'compliance', 'nrs', 'viaria', 'si']
FAIXA = [('esg', 'smeta'), ('estudos',)]   # as linhas proprias: Padronizacao numa fileira, Inteligencia na outra
LARG = arcos.larguras()
# 14/10/2026: «e se estes dois ficassem em circulo, com fundo e efeito dos outros; tambem gostaria daquela figura antiga
# de fundo». Os tres da faixa (Responsabilidade social junto, para nao sobrar uma linha solta ao lado de dois circulos):
# (tema, cx, cy a partir do topo da faixa, raio). Os angulos das etiquetas sao os do arcos.py (os dos circulos antigos).
CIRC = [('esg', 300, 150, 104), ('smeta', 578, 112, 78), ('estudos', 846, 176, 90)]
ZH = 300                                   # altura da faixa dos circulos
def ZONA(zt): return (150, zt, 830, ZH)    # a caixa das manchas (x, y, largura, altura): so onde ha disco
def DISCOS_F(zt):                          # as manchas, fora do centro dos aros, como nos antigos
    return [(270, zt + 178, 84), (596, zt + 98, 58), (870, zt + 194, 72)]
FOTO_PROP = 480 / 867.0                    # img/conhecimento-foto-*.webp, a piramide de bonecos (foto.py)
GEO = {}


def _paginas_normas():
    try:
        s = open(os.path.join(SITE, 'js', 'setores-dados.js'), encoding='utf-8').read()
        d = json.loads(s[s.index('{'):s.rindex('}') + 1])
        return {n['nome']: n.get('pagina') for n in d['normas'].values() if n.get('pagina')}
    except Exception:
        return {}


def larg(n):
    """largura da etiqueta: W1 para todas; W2 so para o nome que nao cabe (medido a 12,5 em larguras.json, acima de 90)"""
    return W2 if LARG.get(n, len(n) * 6.6) > 90 else W1


def larg_nome(t, fs=NF):
    """largura de um nome de tema em Plex Condensed 700 (medido no Edge: .45 da letra por caractere), com folga"""
    return len(t) * fs * .47


def titulo2(tit):
    """os nomes dos temas em no maximo duas linhas (o arcos.py tem tres para os circulos)"""
    return tit if len(tit) <= 2 else [' '.join(tit[:-1]), tit[-1]]


def _dados():
    rel, ordem = {}, []
    for tid, pag, div, cx, cy, r, tit, normas in arcos.TEMAS:
        for n, a in normas:
            if n in FORA: continue
            if n not in rel: rel[n] = []; ordem.append(n)
            if tid not in rel[n]: rel[n].append(tid)
            if isinstance(a, str) and a.startswith('cruza:'):
                o = a.split(':')[1]
                if o not in rel[n]: rel[n].append(o)
    tem = {t[0]: t for t in arcos.TEMAS}
    de = {tid: [n for n in ordem if tid in rel[n]] for tid in tem}
    comp = {n for n in ordem if len(rel[n]) > 1}
    sat = [t for t in ORDEM if t in tem]
    assert set(sat) == {t[0] for t in arcos.TEMAS} - {'iso', 'esg', 'smeta', 'estudos'}, sat
    return tem, de, comp, sat


def _vem(dx, dy, d):
    """o style da entrada: de onde a peca brota (relativo ao lugar final) e o atraso"""
    return ' style="--dx:%.1fpx;--dy:%.1fpx;--d:%dms"' % (dx, dy, d)


class _Desenho:
    def __init__(self):
        self.linhas, self.etiq = [], []      # linhas por baixo, etiquetas e nomes por cima
        self.pags = _paginas_normas()
        self.tem, self.de, self.comp, self.sat = _dados()

    # ------------------------------------------------------------ pecas
    def linha(self, x1, y1, x2, y2, cls='ln-linha', pag=None, cresce=None, d=0):
        """cresce: o ponto de onde a linha nasce na entrada (o padrao e o comeco, x1 y1)"""
        ox, oy = cresce or (x1, y1)
        l = ('<line class="%s" x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" style="--ox:%.1fpx;--oy:%.1fpx;--d:%dms"/>'
             % (cls, x1, y1, x2, y2, ox, oy, d))
        if pag:   # «que sejam clicaveis»: a linha leva a pagina do tema; a faixa invisivel de 18 facilita o clique
            l = ('<a class="ln-a" href="%s"><line class="ln-hit" x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f"/>%s</a>'
                 % (pag, x1, y1, x2, y2, l))
        self.linhas.append(l)

    def etiqueta(self, cx, cy, n, ponte=False, de=None, d=0):
        """de: o ponto de onde a etiqueta brota na entrada (sem ele, aparece no proprio lugar)"""
        w = larg(n)
        g = ('<g class="ln-et%s"><rect x="%.1f" y="%.1f" width="%.1f" height="%d" rx="3"/>'
             '<text x="%.1f" y="%.1f" text-anchor="middle">%s</text></g>'
             % (' ln-et-ponte' if ponte else '', cx - w / 2, cy - PH / 2, w, PH, cx, cy + BL, arcos.esc(n)))
        p = self.pags.get(n)
        if p: g = '<a href="%s">%s</a>' % (p, g)
        ox, oy = de or (cx, cy)
        self.etiq.append('<g class="ln-b"%s>%s</g>' % (_vem(ox - cx, oy - cy, d), g))
        return w

    def nome(self, x, y, linhas, pag, anc='middle', cls='ln-nome', dy=0, d=0):
        t = '<text class="%s" x="%.1f" y="%.1f" text-anchor="%s">' % (cls, x, y, anc) + ''.join(
            '<tspan x="%.1f" dy="%s">%s</tspan>' % (x, '0' if k == 0 else LH, arcos.esc(l)) for k, l in enumerate(linhas)) + '</text>'
        if pag: t = '<a href="%s">%s</a>' % (pag, t)
        self.etiq.append('<g class="ln-b ln-b-nome"%s>%s</g>' % (_vem(0, dy, d), t))

    def abre(self, tid, extra=''):
        self._g = '<g class="ln-ramal%s" data-t="%s">' % (extra, tid); self._l0, self._e0 = len(self.linhas), len(self.etiq)

    def fecha(self):
        # o grupo do ramal junta as linhas e as etiquetas dele (para o hover apagar os outros ramais inteiros)
        corpo = self.linhas[self._l0:] + self.etiq[self._e0:]
        del self.linhas[self._l0:]; del self.etiq[self._e0:]
        self.etiq.append(self._g + ''.join(corpo) + '</g>')

    def resto(self, t):
        return [n for n in self.de[t] if n not in self.comp]

    def ponte_de(self, t):
        return [n for n in self.de[t] if n in self.comp][0]

    # ------------------------------------------------------------ as tres linhas proprias, numa faixa embaixo
    def faixa(self, y, x0=None, centro=None, passo=96, d0=0):   # 14/10/2026: «distancia maior» entre as fileiras (era 72)
        """cada fileira de FAIXA lado a lado, com o nome em cima do comeco da linha; x0 alinha a esquerda, centro
        centraliza a fileira. As normas brotam do comeco da linha, embaixo do nome. Devolve o y da ultima linha."""
        j = 0
        for fileira in FAIXA:
            g = []
            for t in fileira:
                normas = self.de[t]
                wl = 14 + sum(larg(n) for n in normas) + GAP * (len(normas) - 1) + 14
                nome = ' '.join(self.tem[t][6])
                g.append((t, normas, wl, nome, max(wl, larg_nome(nome))))
            vao = 64
            total = sum(e[4] for e in g) + vao * (len(g) - 1)
            x = x0 if centro is None else centro - total / 2
            for t, normas, wl, nome, w in g:
                d = d0 + 200 * j; j += 1
                self.abre(t, ' ln-i' if t == 'estudos' else '')
                self.linha(x, y, x + wl, y, pag=self.tem[t][1], d=d)
                self.nome(x, y - 22, [nome], self.tem[t][1], 'start', dy=6, d=d)
                c = x + 14
                for m, n in enumerate(normas):
                    wi = larg(n); self.etiqueta(c + wi / 2, y, n, de=(x + 14, y), d=d + 140 + 90 * m); c += wi + GAP
                self.fecha()
                x += w + vao
            y += passo
        return y - passo

    # ------------------------------------------------------------ 14/10/2026: a faixa de baixo em CIRCULOS
    def circulos(self, zt, d0=0):
        """ESG, Responsabilidade social e Estudos em circulos, como os antigos: o aro fino (Estudos tracejado em
        vermelho), o nome no centro e as normas em etiquetas SOBRE o aro; no mouse o tema cresce 1,3 e as etiquetas
        andam pelo aro ate formar um poligono regular com uma no alto (o carrossel de 24 e 26/09). Por tras, as
        manchas pontilhadas do motor da trama (camadas() e gera_manchas()). Na entrada as normas brotam do centro,
        do nome do tema, ate o aro. zt e o topo da faixa; devolve o fundo dela."""
        aros, temas = [], []
        for k, (t, cx, dy, r) in enumerate(CIRC):
            cy = zt + dy
            div, tit, pag = self.tem[t][2], self.tem[t][6], self.tem[t][1]
            normas = [(n, a) for n, a in self.tem[t][7] if n not in FORA and not isinstance(a, str)]
            d = d0 + 220 * k
            aros.append('<g class="ln-b"%s><circle class="lc-aro%s" data-t="%s" r="%d" style="--cx:%.1fpx;--cy:%.1fpx"/></g>'
                        % (_vem(0, 0, d), ' lc-aro--i' if div == 'i' else '', t, r, cx, cy))
            rot = '%s: %s' % (' '.join(tit), ', '.join(n for n, a in normas))
            o = ['<a class="lc-tema" data-t="%s" href="%s" aria-label="%s" style="--cx:%.1fpx;--cy:%.1fpx">'
                 % (t, pag, arcos.esc(rot), cx, cy), '<circle class="lc-alvo" r="%d"/>' % r]
            y0 = -LH * (len(tit) - 1) / 2.0
            o.append('<g class="ln-b ln-b-nome"%s><text class="lc-tit" x="0" y="%.1f">%s</text></g>'
                     % (_vem(0, 0, d), y0, ''.join('<tspan x="0" dy="%s">%s</tspan>' % ('0' if i == 0 else LH, arcos.esc(l))
                                                   for i, l in enumerate(tit))))
            # o carrossel: no hover as etiquetas vao para as vagas de um poligono regular com uma no alto (-90),
            # mantendo a ordem em volta do aro; entre os encaixes possiveis, o que menos desloca
            n = len(normas); angs = [a for nm, a in normas]
            ordem = sorted(range(n), key=lambda i: angs[i])
            vagas = [-90 + 360.0 * j / n for j in range(n)]
            def dif(a, b): return (a - b + 180) % 360 - 180
            sft = min(range(n), key=lambda q: sum(dif(vagas[j], angs[ordem[(j + q) % n]]) ** 2 for j in range(n)))
            gira = {ordem[(j + sft) % n]: dif(vagas[j], angs[ordem[(j + sft) % n]]) for j in range(n)}
            for m, (nm, a) in enumerate(normas):
                px, py = r * math.cos(math.radians(a)), r * math.sin(math.radians(a)); w = larg(nm)
                o.append('<g class="ln-b"%s><g class="lc-orb" style="--gira:%.1fdeg"><g class="lc-pil"><g class="ln-et">'
                         '<rect x="%.1f" y="%.1f" width="%d" height="%d" rx="3"/><text x="%.1f" y="%.1f" text-anchor="middle">%s</text>'
                         '</g></g></g></g>' % (_vem(-px, -py, d + 160 + 110 * m), gira[m], px - w / 2, py - PH / 2, w, PH,
                                              px, py + BL, arcos.esc(nm)))
            o.append('</a>')
            temas.append(''.join(o))
        self.etiq.append('<g class="lc-aros" aria-hidden="true">' + ''.join(aros) + '</g>')
        self.etiq.append('<g class="lc-temas">' + ''.join(temas) + '</g>')
        return zt + ZH

    def svg(self, vb, cls, rotulo):
        return ('<svg class="ln-svg %s" viewBox="%s" role="group" aria-label="%s">' % (cls, vb, rotulo)
                + '<g class="ln-linhas">' + ''.join(self.linhas) + '</g>' + ''.join(self.etiq) + '</svg>')


def mapa_h():
    """eixo horizontal com o nome a esquerda; ramais verticais alternando para cima e para baixo; a faixa das linhas
    proprias embaixo, alinhada ao comeco do eixo"""
    D = _Desenho(); tem = D.tem
    X0, PY = 16, 40
    eixo = ['Sistemas de', 'gestão ISO']
    XN = X0 + max(larg_nome(l, EF) for l in eixo)         # o nome do eixo, alinhado a direita, termina aqui
    XL = XN + 12                                          # e o eixo comeca aqui
    x1, xf = XL + 16 + W1 / 2, 1366 - W1 / 2              # centros do primeiro e do ultimo ramal
    PX = (xf - x1) / (len(D.sat) - 1)
    xs = [x1 + PX * k for k in range(len(D.sat))]
    # a altura de cada lado sai dos ramais: o mais alto de cima define o eixo; o mais baixo de baixo, a faixa
    def alto(t): return PY * len(D.resto(t)) + 28
    cima = max(alto(t) + 10 + LH * (len(titulo2(tem[t][6])) - 1) + 15 for k, t in enumerate(D.sat) if k % 2 == 0)
    Y0 = 6 + cima + 4
    D.linha(XL, Y0, 1366, Y0, 'ln-eixo', tem['iso'][1])
    D.nome(XN, Y0 - 4, eixo, tem['iso'][1], 'end', 'ln-eixo-nome')
    fundo = Y0
    for k, t in enumerate(D.sat):
        x = xs[k]; s = -1 if k % 2 == 0 else 1; resto = D.resto(t)
        yfim = Y0 + s * alto(t)
        tit = titulo2(tem[t][6])
        d = 520 + 80 * k
        D.abre(t)
        D.linha(x, Y0, x, yfim, pag=tem[t][1], cresce=(x, yfim), d=d)          # cresce do nome ate o eixo
        D.etiqueta(x, Y0, D.ponte_de(t), ponte=True, d=120 + 60 * k)
        n = len(resto)
        for m, nm in enumerate(resto):        # a mais perto do nome brota primeiro
            D.etiqueta(x, Y0 + s * PY * (m + 1), nm, de=(x, yfim), d=d + 140 + 100 * (n - 1 - m))
        D.nome(x, yfim - 10 - LH * (len(tit) - 1) if s < 0 else yfim + 22, tit, tem[t][1], dy=-6 * s, d=d)
        D.fecha()
        if s > 0: fundo = max(fundo, yfim + 22 + LH * (len(tit) - 1))
    # 14/10/2026: a faixa de baixo em circulos (CIRC), com as manchas por tras e a piramide no canto direito, livre
    # abaixo do ramal de Seguranca da informacao
    zt = fundo + 48
    fim = D.circulos(zt, d0=520 + 80 * len(D.sat) + 200)
    t_si = D.sat[-1]
    livre = Y0 + PY * len(D.resto(t_si)) + 28 + 22 + LH * (len(titulo2(tem[t_si][6])) - 1) + 24
    fh = fim - livre; fw = fh * FOTO_PROP
    vb = (10, 6, 1362, fim + 8 - 6)
    GEO.update(vb=vb, zona=ZONA(zt), foto=(1366 - fw, livre, fw, fh), discos=DISCOS_F(zt))
    return D.svg('%d %d %d %d' % vb, 'ln-svg--h', 'Temas de gestão e normas, a partir do sistema de gestão ISO')


def mapa_v():
    """eixo vertical com o nome em cima; ramais horizontais alternando para a direita e para a esquerda, com o nome
    em cima do ramal, junto do eixo (na ponta nao cabia); a faixa das linhas proprias embaixo, centralizada (teste)"""
    D = _Desenho(); tem = D.tem
    XC, Y1, PY = 700, 130, 76
    ys = [Y1 + PY * k for k in range(len(D.sat))]
    D.linha(XC, Y1 - 50, XC, ys[-1] + 50, 'ln-eixo', tem['iso'][1])
    D.nome(XC, Y1 - 64, ['Sistemas de gestão ISO'], tem['iso'][1], 'middle', 'ln-eixo-nome')
    for k, t in enumerate(D.sat):
        y = ys[k]; s = 1 if k % 2 == 0 else -1; resto = D.resto(t)
        ponte = D.ponte_de(t)
        x0 = XC + s * (W1 / 2 + GAP)          # comeco do ramal depois da norma do encontro: o nome fica em cima dele
        x = x0; centros = []
        for nm in resto:
            w = larg(nm); centros.append(x + s * w / 2); x += s * (w + GAP)
        xfim = x + s * 12
        d = 520 + 80 * k
        D.abre(t); D.linha(XC, y, xfim, y, pag=tem[t][1], d=d)
        D.etiqueta(XC, y, ponte, ponte=True, d=120 + 60 * k)
        for m, (c, nm) in enumerate(zip(centros, resto)):
            D.etiqueta(c, y, nm, de=(x0, y), d=d + 140 + 100 * m)
        D.nome(x0, y - 22, [' '.join(tem[t][6])], tem[t][1], 'start' if s > 0 else 'end', dy=6, d=d)
        D.fecha()
    yl = D.faixa(ys[-1] + 160, centro=XC, d0=520 + 80 * len(D.sat) + 200)
    return D.svg('10 40 1362 %d' % (yl + 18 - 40), 'ln-svg--v', 'Temas de gestão e normas, versão vertical')


def css_aros():
    """no hover do tema, o aro dele (que mora na camada de baixo) cresce junto, escurece e fica inteiro"""
    return '\n'.join('.ln-svg:has(.lc-tema[data-t="%s"]:is(:hover,:focus-visible)) .lc-aro[data-t="%s"]'
                     '{transform:translate(var(--cx),var(--cy)) scale(1.3);stroke:%s;opacity:1}'
                     % (t, t, 'var(--im-vermelho,#EF4545)' if t == 'estudos' else 'rgba(20,48,76,.5)') for t, x, y, r in CIRC) + '\n'


def _pct(x, y, w, h):
    X, Y, W, H = GEO['vb']
    return 'left:%.3f%%;top:%.3f%%;width:%.3f%%;height:%.3f%%' % ((x - X) / W * 100, (y - Y) / H * 100, w / W * 100, h / H * 100)


VER, ESC_M = '14102026', 1.4               # versao das imagens das manchas e pixels por unidade do viewBox


def camadas():
    """as duas camadas por baixo do mapa horizontal (rodar depois de mapa_h): as manchas dos circulos e a piramide.
    As classes .ar-manchas e .ar-foto sao as que o MOTOR do monta.py procura para o ditherVivo."""
    zx, zy, zw, zh = GEO['zona']; fx, fy, fw, fh = GEO['foto']
    return ('<div class="ar-manchas" aria-hidden="true" style="%s"><img src="img/conhecimento-faixa-bayer.webp?v=%s" '
            'data-lum="img/conhecimento-faixa-lum.webp?v=%s" alt="" width="%d" height="%d" loading="lazy" decoding="async"></div>'
            % (_pct(zx, zy, zw, zh), VER, VER, round(zw * ESC_M), round(zh * ESC_M))
            + '<div class="ar-foto" aria-hidden="true" style="%s"><img src="img/conhecimento-foto-bayer.webp?v=7" '
            'data-lum="img/conhecimento-foto-lum.webp?v=7" alt="" width="480" height="867" loading="lazy" decoding="async"></div>'
            % _pct(fx, fy, fw, fh))


def gera_manchas():
    """as manchas da faixa em imagem, para o motor: a mesma receita do manchas.py (tom 0,965 dentro do disco, creme
    puro fora), na caixa da ZONA"""
    import numpy as np
    from PIL import Image
    import manchas as M
    zx, zy, zw, zh = GEO['zona']
    W, H = round(zw * ESC_M), round(zh * ESC_M)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float64)
    ux, uy = (xx + .5) / ESC_M + zx, (yy + .5) / ESC_M + zy
    alvo = np.ones((H, W))
    for cx, cy, r in GEO['discos']:
        alvo = np.where((ux - cx) ** 2 + (uy - cy) ** 2 <= r * r, np.minimum(alvo, M.TOM_AZUL), alvo)
    lum = np.where(alvo < 1, M.lum_para(M.TOM_AZUL), 1.0)
    img = os.path.join(SITE, 'img')
    Image.fromarray((lum * 255).round().astype(np.uint8), 'L').save(os.path.join(img, 'conhecimento-faixa-lum.webp'), lossless=True)
    m4 = np.array([[0, 8, 2, 10], [12, 4, 14, 6], [3, 11, 1, 9], [15, 7, 13, 5]])
    T = (m4[yy.astype(int) % 4, xx.astype(int) % 4] + .5) / 16
    k = np.clip(np.floor(M.tom((lum * 255).round() / 255) * 3 + T), 0, 3).astype(int)
    Image.fromarray(M.CORES[k].round().astype(np.uint8), 'RGB').save(os.path.join(img, 'conhecimento-faixa-bayer.webp'), lossless=True)
    print('manchas da faixa: %d x %d' % (W, H))


FRASE = 'Cada tema parte do sistema de gestão pela norma ISO que os une.'


def bloco(svg, extra='', camadas=''):
    return '\n'.join(['  <div class="ln%s">' % extra,
                      '    <p class="ln-frase">%s</p>' % FRASE,
                      '    <div class="ln-rola">' + camadas + svg + '</div>',
                      '  </div>'])


CSS = r"""
/* 14/10/2026: o mapa de linhas no lugar dos circulos (_ferramentas/arcos/linhas.py). Linhas finas e clicaveis, com
   traco fixo em px de tela (non-scaling-stroke): eixo de 1 px na tinta, ramais de .6 px no azul, Estudos tracejado
   em vermelho; faixa invisivel de 18 para o clique. Normas em etiquetas de largura unica sobre a linha, no desenho
   das etiquetas da casa, 13 medio; a do encontro com o eixo com contorno na tinta e seminegrito; temas em 17
   negrito; todo texto na tinta, sem cor. No hover de um ramal os outros recuam pelo texto e pelo traco; o fundo
   das etiquetas fica opaco, para o eixo nunca passar por cima delas. */
.ln{margin:28px 0 0}
.ln-frase{margin:0 0 10px;max-width:62ch;font-family:var(--sans);font-size:16px;line-height:1.4;color:var(--azul);text-wrap:pretty}
.ln-rola{overflow-x:auto}
.ln-svg{display:block;width:100%;height:auto}
.ln-svg line,.ln-svg rect{vector-effect:non-scaling-stroke}
.ln-eixo{stroke:#14304C;stroke-width:1;stroke-linecap:round}
.ln-linha{stroke:#336699;stroke-width:.6;stroke-linecap:round;fill:none;transition:stroke .2s ease,stroke-width .2s ease,opacity .3s ease}
.ln-hit{stroke:transparent;stroke-width:18;fill:none;pointer-events:stroke;vector-effect:none}
.ln-a{cursor:pointer}
.ln-a:is(:hover,:focus-visible) .ln-linha{stroke:#14304C;stroke-width:1}
.ln-a:is(:hover,:focus-visible) .ln-eixo{stroke-width:1.4}
.ln-i .ln-linha{stroke:var(--im-vermelho,#EF4545);stroke-width:.8;stroke-dasharray:4 4;stroke-linecap:butt}
.ln-et rect{fill:#FAF9F5;stroke:#14304C;stroke-opacity:.26;stroke-width:.6;transition:fill .2s ease,stroke-opacity .3s ease}
.ln-et text{font-family:var(--sans);font-size:13px;font-weight:500;fill:#14304C;transition:opacity .3s ease}
.ln-et-ponte rect{stroke-opacity:1;stroke-width:.8}
.ln-et-ponte text{font-weight:600}
.ln-svg a:is(:hover,:focus-visible) .ln-et rect{fill:#FFFFFF;stroke-opacity:1}
.ln-nome,.ln-eixo-nome{font-family:var(--sans);font-weight:700;fill:#14304C;transition:opacity .3s ease}
.ln-nome{font-size:17px}
.ln-eixo-nome{font-size:18px}
.ln-svg a:is(:hover,:focus-visible) .ln-nome,.ln-svg a:is(:hover,:focus-visible) .ln-eixo-nome{text-decoration:underline}
.ln-svg a:focus{outline:none}
.ln-svg:has(.ln-ramal:hover) .ln-ramal:not(:hover) :is(text,.ln-linha){opacity:.28}
.ln-svg:has(.ln-ramal:hover) .ln-ramal:not(:hover) rect{stroke-opacity:.1}
/* ENTRADA: o JS poe .ln-anima (estado de antes) e, quando o mapa entra na tela, .ln-vivo. As linhas crescem a partir
   de --ox/--oy; cada etiqueta e cada nome saem de --dx/--dy (o ponto do nome do tema), pequenos e transparentes, e
   deslizam ate o lugar, com o atraso --d. O recuo do hover mexe no texto e no traco, que sao outros elementos. */
.ln-anima :is(.ln-linha,.ln-eixo){transform-box:view-box;transform-origin:var(--ox) var(--oy);transform:scale(.001);stroke-opacity:0}
.ln-anima .ln-b{opacity:0;transform-box:fill-box;transform-origin:center;transform:translate(var(--dx),var(--dy)) scale(.35)}
.ln-anima .ln-b-nome{transform:translate(var(--dx),var(--dy))}
/* stroke-opacity: sem ele a ponta redonda da linha ainda nao crescida aparece como um ponto antes da hora */
.ln-anima.ln-vivo :is(.ln-linha,.ln-eixo){transform:none;stroke-opacity:1;
  transition:transform .9s cubic-bezier(.3,.7,.2,1) var(--d,0ms),stroke-opacity 0s linear var(--d,0ms),stroke .2s ease,stroke-width .2s ease,opacity .3s ease}
.ln-anima.ln-vivo .ln-b{opacity:1;transform:none;
  transition:opacity .5s ease var(--d,0ms),transform .8s cubic-bezier(.2,.8,.2,1) var(--d,0ms)}
.ar-sec--teste{border-top:1px dashed rgba(20,48,76,.3)}
/* 14/10/2026: a faixa de baixo em CIRCULOS, com o fundo e o efeito dos antigos (guardados em secoes-guardadas):
   manchas pontilhadas do motor da trama por tras (.ar-manchas, opacas, so na caixa dos discos), a piramide de
   bonecos no canto direito (.ar-foto), aro fino (Estudos tracejado em vermelho), o tema cresce 1,3 no mouse e as
   etiquetas andam pelo aro ate o poligono regular com uma no alto; os outros temas recuam pelo texto. */
.ln-rola{position:relative}
.ln-rola .ln-svg{position:relative;z-index:1}
/* o motor pinta creme opaco e a secao (z-index 1) fica por cima da grade-guia do body::before: dentro das manchas e
   da piramide a mesma grade e redesenhada por cima do canvas, presa a janela (background-attachment:fixed), para as
   linhas verticais do site nao sumirem ali */
.ln-rola :is(.ar-manchas,.ar-foto)::after{content:"";position:absolute;inset:0;pointer-events:none;
  background-image:linear-gradient(to right,rgba(20,48,76,.08) 1px,transparent 1px);
  background-size:calc((100% - 2 * var(--lado)) / 6) 100%;background-position:var(--lado) 0;
  background-position:round(var(--lado),1px) 0;background-attachment:fixed}   /* round: a caixa do body::before cai no pixel inteiro */
.ln-rola .ar-manchas{position:absolute;z-index:0;opacity:.9;transition:opacity .35s ease}
.ln-rola:has(.lc-tema:is(:hover,:focus-visible)) .ar-manchas{opacity:.72}
.ar-manchas img,.ar-gl{position:absolute;inset:0;width:100%;height:100%;display:block}
.ar-manchas.gl-on img{visibility:hidden}
.ln-rola .ar-foto{position:absolute;z-index:0;overflow:hidden}
.ar-foto img,.af-gl{position:absolute;inset:0;width:100%;height:100%;display:block;object-fit:cover}
.ar-foto.gl-on img{visibility:hidden}
.lc-aro{fill:none;stroke:rgba(20,48,76,.24);stroke-width:.6;vector-effect:non-scaling-stroke;
  transform:translate(var(--cx),var(--cy)) scale(1);transition:transform .45s cubic-bezier(.2,.7,.2,1),stroke .35s ease,opacity .35s ease}
.lc-aro--i{stroke:var(--im-vermelho,#EF4545);stroke-dasharray:3 5}
.ln-svg:has(.lc-tema:is(:hover,:focus-visible)) .lc-aro{opacity:.34}
.lc-tema{cursor:pointer;transform:translate(var(--cx),var(--cy)) scale(1);transition:transform .45s cubic-bezier(.2,.7,.2,1)}
.lc-tema:is(:hover,:focus-visible){transform:translate(var(--cx),var(--cy)) scale(1.3)}
.lc-tema:focus{outline:none}
.lc-tema:focus-visible .lc-tit{text-decoration:underline}
.lc-alvo{fill:transparent}
.lc-tit{font-family:var(--sans);font-weight:700;font-size:17px;fill:#14304C;text-anchor:middle;dominant-baseline:central;transition:opacity .35s ease}
.lc-orb{transform-box:view-box;transform-origin:0 0;transform:rotate(0deg);transition:transform 1.6s cubic-bezier(.16,.8,.2,1)}
.lc-orb .lc-pil{transform-box:fill-box;transform-origin:center;transform:rotate(0deg);transition:transform 1.6s cubic-bezier(.16,.8,.2,1)}
.lc-tema:is(:hover,:focus-visible) .lc-orb{transform:rotate(var(--gira,0deg))}
.lc-tema:is(:hover,:focus-visible) .lc-orb .lc-pil{transform:rotate(calc(-1 * var(--gira,0deg)))}
.ln-svg:has(.lc-tema:is(:hover,:focus-visible)) .lc-tema:not(:hover):not(:focus-visible) :is(.lc-tit,.ln-et text){opacity:.3}
.ln-svg:has(.lc-tema:is(:hover,:focus-visible)) .lc-tema:not(:hover):not(:focus-visible) rect{stroke-opacity:.1}
@media (prefers-reduced-motion:reduce){ .lc-tema,.lc-orb,.lc-orb .lc-pil{transition:none}
  .lc-tema:is(:hover,:focus-visible) :is(.lc-orb,.lc-orb .lc-pil){transform:none} }
@media (max-width:1000px){ .ln-rola{display:none} .ar-sec--teste{display:none} }
"""

JS = r"""<script>
/* CONHECIMENTO: entrada do mapa de linhas (_ferramentas/arcos/linhas.py). O mapa nasce pronto; com JS e sem
   movimento reduzido, ganha .ln-anima (estado de antes) e, quando um quarto dele entra na tela, .ln-vivo: o eixo se
   desenha e as normas brotam dos temas. Uma vez so. */
(function(){
  /* os circulos da faixa: o tema sob o mouse vai para o fim do grupo, para crescer por cima dos vizinhos */
  var g = document.querySelector('#conhecimento .lc-temas');
  if(g){ var frente = function(e){ var t = e.target.closest && e.target.closest('.lc-tema'); if(t && t !== g.lastElementChild) g.appendChild(t); };
    g.addEventListener('mouseover', frente); g.addEventListener('focusin', frente); }
  var ss = document.querySelectorAll('.ln-svg');
  if(!ss.length || !('IntersectionObserver' in window) || matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  /* terminada a entrada, as classes saem: o mapa fica no estado normal e o hover nao herda os atrasos dela */
  var io = new IntersectionObserver(function(es){
    es.forEach(function(e){ if(e.isIntersecting){ var s = e.target; s.classList.add('ln-vivo'); io.unobserve(s);
      setTimeout(function(){ s.classList.remove('ln-anima', 'ln-vivo'); }, 4500); } });
  }, {threshold:.25});
  for(var i = 0; i < ss.length; i++){ ss[i].classList.add('ln-anima'); io.observe(ss[i]); }
})();
</script>"""
