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
  como treinamento e base para a gestao de riscos de seguranca viaria).
Os circulos foram guardados em Ideal Metrics/secoes-guardadas/conhecimento-circulos.html (python monta.py guardar).

Desenho: «Sistemas de gestao ISO» e o eixo; cada um dos oito temas sai dele como um ramal, a partir da norma ISO que
liga o tema ao sistema de gestao (o mesmo ponto de contato dos circulos). As normas sao ETIQUETAS SOBRE A LINHA, no
desenho das etiquetas da casa (creme, contorno fino, canto de 3 px), todas da MESMA largura (120; so os dois nomes
que nao cabem, Rainforest Alliance e Observatorio setorial, vao a 158). A norma do encontro com o eixo leva contorno
na tinta e negrito. O nome do eixo fica a esquerda dele; os nomes dos ramais, na ponta de cada um. Sem a SA 8000, ESG e
Responsabilidade social nao tem norma comum: viram linhas proprias, numa faixa embaixo com Estudos (a divisao de
inteligencia, linha tracejada em vermelho), cada uma com o nome em cima do comeco da linha. Todo texto na tinta
(#14304C); a cor fica so nas linhas. No hover de um ramal os outros recuam pelo texto e pelo traco, nunca pelo fundo
das etiquetas: o creme delas continua opaco e o eixo nao aparece por cima.

mapa_h(): eixo horizontal, ramais verticais (a secao da home). mapa_v(): eixo vertical, ramais horizontais (teste)."""

import json, os
import arcos

AQUI = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(os.path.dirname(AQUI))
# fora do mapa e da lista do celular (continuam no arcos.py so para os circulos guardados, estado de 13/10/2026):
#   SA 8000, 14/10/2026: «nao e mais utilizada»;
#   ISO 39002, 14/10/2026: guia de boas praticas, nao certificavel; nao entra como norma do tema.
FORA = {'SA 8000', 'ISO 39002'}
FS, PH = 15, 28               # etiqueta: corpo da letra e altura (unidades do viewBox)
W1, W2 = 120, 158             # as duas larguras de etiqueta (medidas no Edge: ISO/IEC 27001 em negrito tem 96)
GAP = 22                      # vao entre etiquetas vizinhas numa linha horizontal
# ordem dos ramais: a do arcos.py com Saude e seguranca antes de Seguranca viaria, para os ramais longos se
# repartirem entre cima e baixo (carbono, 4 normas, em cima; NRs, 3, embaixo) e o desenho ficar equilibrado
ORDEM = ['qualidade', 'ambiente', 'carbono', 'alimentos', 'compliance', 'nrs', 'viaria', 'si']
FAIXA = [('esg', 'smeta'), ('estudos',)]   # as linhas proprias: Padronizacao numa fileira, Inteligencia na outra
LARG = arcos.larguras()


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


def larg_nome(t, fs=21):
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


class _Desenho:
    def __init__(self):
        self.linhas, self.etiq = [], []      # linhas por baixo, etiquetas e nomes por cima
        self.pags = _paginas_normas()
        self.tem, self.de, self.comp, self.sat = _dados()

    # ------------------------------------------------------------ pecas
    def linha(self, x1, y1, x2, y2, cls='ln-linha', pag=None):
        l = '<line class="%s" x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f"/>' % (cls, x1, y1, x2, y2)
        if pag:   # «que sejam clicaveis»: a linha leva a pagina do tema; a faixa invisivel de 18 facilita o clique
            l = ('<a class="ln-a" href="%s"><line class="ln-hit" x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f"/>%s</a>'
                 % (pag, x1, y1, x2, y2, l))
        self.linhas.append(l)

    def etiqueta(self, cx, cy, n, ponte=False):
        w = larg(n)
        g = ('<g class="ln-et%s"><rect x="%.1f" y="%.1f" width="%.1f" height="%d" rx="3"/>'
             '<text x="%.1f" y="%.1f" text-anchor="middle">%s</text></g>'
             % (' ln-et-ponte' if ponte else '', cx - w / 2, cy - PH / 2, w, PH, cx, cy + 5.2, arcos.esc(n)))
        p = self.pags.get(n)
        self.etiq.append('<a href="%s">%s</a>' % (p, g) if p else g)
        return w

    def nome(self, x, y, linhas, pag, anc='middle', cls='ln-nome', passo=24):
        t = '<text class="%s" x="%.1f" y="%.1f" text-anchor="%s">' % (cls, x, y, anc) + ''.join(
            '<tspan x="%.1f" dy="%s">%s</tspan>' % (x, '0' if k == 0 else passo, arcos.esc(l)) for k, l in enumerate(linhas)) + '</text>'
        self.etiq.append('<a href="%s">%s</a>' % (pag, t) if pag else t)

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
    def faixa(self, y, x0=None, centro=None, passo=88):
        """cada fileira de FAIXA lado a lado, com o nome em cima do comeco da linha; x0 alinha a esquerda, centro
        centraliza a fileira. Devolve o y da ultima linha."""
        for fileira in FAIXA:
            g = []
            for t in fileira:
                normas = self.de[t]
                wl = 18 + sum(larg(n) for n in normas) + GAP * (len(normas) - 1) + 18
                nome = ' '.join(self.tem[t][6])
                g.append((t, normas, wl, nome, max(wl, larg_nome(nome))))
            vao = 80
            total = sum(e[4] for e in g) + vao * (len(g) - 1)
            x = x0 if centro is None else centro - total / 2
            for t, normas, wl, nome, w in g:
                self.abre(t, ' ln-i' if t == 'estudos' else '')
                self.linha(x, y, x + wl, y, pag=self.tem[t][1])
                c = x + 18
                for n in normas:
                    wi = larg(n); self.etiqueta(c + wi / 2, y, n); c += wi + GAP
                self.nome(x, y - 30, [nome], self.tem[t][1], 'start')
                self.fecha()
                x += w + vao
            y += passo
        return y - passo

    def svg(self, vb, cls, rotulo):
        return ('<svg class="ln-svg %s" viewBox="%s" role="group" aria-label="%s">' % (cls, vb, rotulo)
                + '<g class="ln-linhas">' + ''.join(self.linhas) + '</g>' + ''.join(self.etiq) + '</svg>')


def mapa_h():
    """eixo horizontal com o nome a esquerda; ramais verticais alternando para cima e para baixo; a faixa das linhas
    proprias embaixo, alinhada ao comeco do eixo"""
    D = _Desenho(); tem = D.tem
    X0, PY = 16, 46
    eixo = ['Sistemas de', 'gestão ISO']
    XN = X0 + max(larg_nome(l, 22) for l in eixo)        # o nome do eixo, alinhado a direita, termina aqui
    XL = XN + 14                                          # e o eixo comeca aqui
    x1, xf = XL + 16 + W1 / 2, 1366 - W1 / 2              # centros do primeiro e do ultimo ramal
    PX = (xf - x1) / (len(D.sat) - 1)
    xs = [x1 + PX * k for k in range(len(D.sat))]
    # a altura de cada lado sai dos ramais: o mais alto de cima define o eixo; o mais baixo de baixo, a faixa
    def alto(t): return PY * len(D.resto(t)) + 34
    cima = max(alto(t) + 12 + 24 * (len(titulo2(tem[t][6])) - 1) + 18 for k, t in enumerate(D.sat) if k % 2 == 0)
    Y0 = 6 + cima + 4
    D.linha(XL, Y0, 1366, Y0, 'ln-eixo', tem['iso'][1])
    D.nome(XN, Y0 - 5, eixo, tem['iso'][1], 'end', 'ln-eixo-nome')
    fundo = Y0
    for k, t in enumerate(D.sat):
        x = xs[k]; s = -1 if k % 2 == 0 else 1; resto = D.resto(t)
        yfim = Y0 + s * alto(t)
        tit = titulo2(tem[t][6])
        D.abre(t); D.linha(x, Y0, x, yfim, pag=tem[t][1])
        for m, n in enumerate(resto): D.etiqueta(x, Y0 + s * PY * (m + 1), n)
        D.etiqueta(x, Y0, D.ponte_de(t), ponte=True)
        D.nome(x, yfim - 12 - 24 * (len(tit) - 1) if s < 0 else yfim + 28, tit, tem[t][1])
        D.fecha()
        if s > 0: fundo = max(fundo, yfim + 28 + 24 * (len(tit) - 1))
    yl = D.faixa(fundo + 92, x0=XL)
    return D.svg('10 6 1362 %d' % (yl + 22 - 6), 'ln-svg--h', 'Temas de gestão e normas, a partir do sistema de gestão ISO')


def mapa_v():
    """eixo vertical com o nome em cima; ramais horizontais alternando para a direita e para a esquerda, com o nome
    em cima do ramal, junto do eixo (na ponta nao cabia); a faixa das linhas proprias embaixo, centralizada (teste)"""
    D = _Desenho(); tem = D.tem
    XC, Y1, PY = 700, 150, 92
    ys = [Y1 + PY * k for k in range(len(D.sat))]
    D.linha(XC, Y1 - 60, XC, ys[-1] + 60, 'ln-eixo', tem['iso'][1])
    D.nome(XC, Y1 - 78, ['Sistemas de gestão ISO'], tem['iso'][1], 'middle', 'ln-eixo-nome')
    for k, t in enumerate(D.sat):
        y = ys[k]; s = 1 if k % 2 == 0 else -1; resto = D.resto(t)
        ponte = D.ponte_de(t)
        x = XC + s * (W1 / 2 + GAP); centros = []
        for n in resto:
            w = larg(n); centros.append(x + s * w / 2); x += s * (w + GAP)
        xfim = x + s * 12
        D.abre(t); D.linha(XC, y, xfim, y, pag=tem[t][1])
        for c, n in zip(centros, resto): D.etiqueta(c, y, n)
        D.etiqueta(XC, y, ponte, ponte=True)
        D.nome(XC + s * (W1 / 2 + GAP), y - 27, [' '.join(tem[t][6])], tem[t][1], 'start' if s > 0 else 'end')
        D.fecha()
    yl = D.faixa(ys[-1] + 160, centro=XC)
    return D.svg('10 40 1362 %d' % (yl + 22 - 40), 'ln-svg--v', 'Temas de gestão e normas, versão vertical')


FRASE = 'Cada tema parte do sistema de gestão pela norma ISO que os une.'


def bloco(svg, extra=''):
    return '\n'.join(['  <div class="ln%s">' % extra,
                      '    <p class="ln-frase">%s</p>' % FRASE,
                      '    <div class="ln-rola">' + svg + '</div>',
                      '  </div>'])


CSS = r"""
/* 14/10/2026: o mapa de linhas no lugar dos circulos (_ferramentas/arcos/linhas.py). Linhas finas e clicaveis, com
   traco fixo em px de tela (non-scaling-stroke): eixo de 1 px na tinta, ramais de .6 px no azul, Estudos tracejado
   em vermelho; faixa invisivel de 18 para o clique. Normas em etiquetas de largura unica sobre a linha, no desenho
   das etiquetas da casa, 15 seminegrito; a do encontro com o eixo com contorno na tinta e negrito; temas em 21
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
.ln-i .ln-linha{stroke:var(--im-vermelho,#EF4545);stroke-width:.8;stroke-dasharray:5 5;stroke-linecap:butt}
.ln-et rect{fill:#FAF9F5;stroke:#14304C;stroke-opacity:.28;stroke-width:.7;transition:fill .2s ease,stroke-opacity .3s ease}
.ln-et text{font-family:var(--sans);font-size:15px;font-weight:600;fill:#14304C;transition:opacity .3s ease}
.ln-et-ponte rect{stroke-opacity:1;stroke-width:.9}
.ln-et-ponte text{font-weight:700}
.ln-svg a:is(:hover,:focus-visible) .ln-et rect{fill:#FFFFFF;stroke-opacity:1}
.ln-nome,.ln-eixo-nome{font-family:var(--sans);font-weight:700;fill:#14304C;transition:opacity .3s ease}
.ln-nome{font-size:21px}
.ln-eixo-nome{font-size:22px}
.ln-svg a:is(:hover,:focus-visible) .ln-nome,.ln-svg a:is(:hover,:focus-visible) .ln-eixo-nome{text-decoration:underline}
.ln-svg a:focus{outline:none}
.ln-svg:has(.ln-ramal:hover) .ln-ramal:not(:hover) :is(text,.ln-linha){opacity:.28}
.ln-svg:has(.ln-ramal:hover) .ln-ramal:not(:hover) rect{stroke-opacity:.1}
.ar-sec--teste{border-top:1px dashed rgba(20,48,76,.3)}
@media (max-width:1000px){ .ln-rola{display:none} .ar-sec--teste{display:none} }
"""
