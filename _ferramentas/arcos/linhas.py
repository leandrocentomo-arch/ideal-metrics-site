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

ENTRADA NOS DOIS SENTIDOS (JS abaixo). 14/10/2026: primeiro tocava uma vez so; depois ficou presa a rolagem, mas
«ficou muito rapido, mal da pra ver»; o pedido era outro: «que o efeito funcione quando estamos indo de cima pra baixo
na pagina, e tambem o inverso, quando estamos indo de baixo para cima». Agora a entrada corre no TEMPO (3 s; era 3,6, «pode ser 20% mais rapido») toda
vez que o mapa entra na tela, venha de cima ou de baixo, e volta ao comeco quando ele sai inteiro de vista. O eixo se
desenha da esquerda e as normas do encontro aparecem nele; em seguida cada tema surge no proprio nome e as normas
BROTAM DELE: saem do ponto do nome, pequenas e transparentes, e deslizam pela linha ate o lugar, enquanto a linha
cresce do nome ate o eixo. O JS so poe no SVG o progresso --p (0 a 1); cada peca leva no style o ponto de onde brota
(--dx, --dy) e a sua vez na linha do tempo (--d, em milesimos de 3100); as linhas, o ponto de onde crescem (--ox,
--oy). O CSS faz a conta. Sem JS, ou com movimento reduzido, --p fica 1 e o mapa aparece pronto.

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
# 14/10/2026: as tres linhas proprias passaram por circulos («e se estes dois ficassem em circulo») e por ramais
# verticais («tire os circulos, organize em fluxo») e voltaram a horizontal («acho que fica melhor na horizontal»):
# a faixa (FAIXA) centralizada, como na versao vertical, com o nome em cima do comeco de cada linha. A piramide de
# bonecos que voltou junto com os circulos saiu no mesmo dia («pode tirar esta figura»).


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
    return ' style="--dx:%.1fpx;--dy:%.1fpx;--d:%d"' % (dx, dy, d)


class _Desenho:
    def __init__(self):
        self.linhas, self.etiq = [], []      # linhas por baixo, etiquetas e nomes por cima
        self.pags = _paginas_normas()
        self.tem, self.de, self.comp, self.sat = _dados()

    # ------------------------------------------------------------ pecas
    def linha(self, x1, y1, x2, y2, cls='ln-linha', pag=None, cresce=None, d=0):
        """cresce: o ponto de onde a linha nasce na entrada (o padrao e o comeco, x1 y1)"""
        ox, oy = cresce or (x1, y1)
        l = ('<line class="%s" x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" style="--ox:%.1fpx;--oy:%.1fpx;--d:%d"/>'
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

    def svg(self, vb, cls, rotulo):
        return ('<svg class="ln-svg %s" viewBox="%s" role="group" aria-label="%s">' % (cls, vb, rotulo)
                + '<g class="ln-linhas">' + ''.join(self.linhas) + '</g>' + ''.join(self.etiq) + '</svg>')


def mapa_h():
    """eixo horizontal com o nome a esquerda; ramais verticais alternando para cima e para baixo; embaixo, a faixa das
    linhas proprias, centralizada"""
    D = _Desenho(); tem = D.tem
    X0, PY = 16, 40
    eixo = ['Sistemas de', 'gestão ISO']
    XN = X0 + max(larg_nome(l, EF) for l in eixo)         # o nome do eixo, alinhado a direita, termina aqui
    XL = XN + 12                                          # e o eixo comeca aqui
    XR = 1366 - 150                                       # 17/10/2026: «um pouco menos de distância entre as normas, para não ocupar toda a largura»
    x1, xf = XL + 16 + W1 / 2, XR - W1 / 2                # centros do primeiro e do ultimo ramal
    PX = (xf - x1) / (len(D.sat) - 1)
    xs = [x1 + PX * k for k in range(len(D.sat))]
    # a altura de cada lado sai dos ramais: o mais alto de cima define o eixo; o mais baixo de baixo, a faixa
    def alto(t): return PY * len(D.resto(t)) + 28
    cima = max(alto(t) + 10 + LH * (len(titulo2(tem[t][6])) - 1) + 15 for k, t in enumerate(D.sat) if k % 2 == 0)
    Y0 = 6 + cima + 4
    D.linha(XL, Y0, XR, Y0, 'ln-eixo', tem['iso'][1])
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
    # as linhas proprias na faixa horizontal, CENTRALIZADA como na versao vertical («como feito no modulo vertical»),
    # 116 abaixo dos ramais e 96 entre as fileiras («distancia maior»)
    fim = D.faixa(fundo + 116, centro=(XL + XR) / 2, d0=520 + 80 * len(D.sat) + 200) + PH / 2 + 2
    vb = (10, 6, 1362, fim + 8 - 6)
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


FRASE = 'Temas por gestão e normas'   # 17/10/2026, pedido do Leandro (era «Cada tema parte do sistema de gestão pela norma ISO que os une.»)


LEGENDA = '<ul class="ar-legenda"><li>Padronização</li><li class="ar-leg-i">Inteligência</li></ul>'   # 17/10/2026: na linha da frase


def bloco(svg, extra='', camadas=''):
    return '\n'.join(['  <div class="ln%s">' % extra,
                      '    <div class="ln-topo"><p class="ln-frase">%s</p>%s</div>' % (FRASE, LEGENDA),
                      '    <div class="ln-rola">' + camadas + svg + '</div>',
                      '  </div>'])


CSS = r"""
/* 14/10/2026: o mapa de linhas no lugar dos circulos (_ferramentas/arcos/linhas.py). Linhas finas e clicaveis, com
   traco fixo em px de tela (non-scaling-stroke): eixo de .6 px na tinta, ramais de .6 px no azul, Estudos tracejado
   em vermelho; faixa invisivel de 18 para o clique. Normas em etiquetas de largura unica sobre a linha, no desenho
   das etiquetas da casa, 13 medio; a do encontro com o eixo so com o contorno na tinta, mesma letra; temas em 17
   negrito; todo texto na tinta, sem cor. No hover de um ramal os outros recuam pelo texto e pelo traco; o fundo
   das etiquetas fica opaco, para o eixo nunca passar por cima delas. */
.ln{margin:28px 0 0}
.ln-topo{display:flex;justify-content:space-between;align-items:baseline;gap:24px 40px;flex-wrap:wrap;margin:0 0 64px}
.ln-topo .ar-legenda{margin:0}
.ln-frase{margin:0;max-width:62ch;font-family:var(--sans);font-size:16px;line-height:1.4;color:var(--azul);text-wrap:pretty}
.ln-rola{overflow-x:auto}
.ln-svg{display:block;width:100%;height:auto}
.ln-svg line,.ln-svg rect{vector-effect:non-scaling-stroke}
.ln-eixo{stroke:#14304C;stroke-width:.6;stroke-linecap:round}   /* 14/10/2026: «as linhas do centro mais finas» (era 1) */
.ln-linha{stroke:#336699;stroke-width:.6;stroke-linecap:round;fill:none;transition:stroke .2s ease,stroke-width .2s ease,opacity .3s ease}
.ln-hit{stroke:transparent;stroke-width:18;fill:none;pointer-events:stroke;vector-effect:none}
.ln-a{cursor:pointer}
.ln-a:is(:hover,:focus-visible) .ln-linha{stroke:#14304C;stroke-width:1}
.ln-a:is(:hover,:focus-visible) .ln-eixo{stroke-width:1}
.ln-i .ln-linha{stroke:var(--im-vermelho,#EF4545);stroke-width:.8;stroke-dasharray:4 4;stroke-linecap:butt}
.ln-et rect{fill:#FAF9F5;stroke:#14304C;stroke-opacity:.26;stroke-width:.6;transition:fill .2s ease,stroke-opacity .3s ease}
.ln-et text{font-family:var(--sans);font-size:13px;font-weight:500;fill:#14304C;transition:opacity .3s ease}
.ln-et-ponte rect{stroke-opacity:1;stroke-width:.6}   /* 14/10/2026: «todas as normas com a mesma escrita»: sem negrito; contorno fino */
.ln-svg a:is(:hover,:focus-visible) .ln-et rect{fill:#FFFFFF;stroke-opacity:1}
.ln-nome,.ln-eixo-nome{font-family:var(--sans);font-weight:700;fill:#14304C;transition:opacity .3s ease}
.ln-nome{font-size:17px}
.ln-eixo-nome{font-size:18px}
.ln-svg a:is(:hover,:focus-visible) .ln-nome,.ln-svg a:is(:hover,:focus-visible) .ln-eixo-nome{text-decoration:underline}
.ln-svg a:focus{outline:none}
.ln-svg:has(.ln-ramal:hover) .ln-ramal:not(:hover) :is(text,.ln-linha){opacity:.28}
.ln-svg:has(.ln-ramal:hover) .ln-ramal:not(:hover) rect{stroke-opacity:.1}
/* ENTRADA: --p (0 a 1) vem do JS, que o leva de 0 a 1 em 3 s quando o mapa entra na tela; sem ele, 1. Cada peca anda de 0 a 1 (--t) na sua janela da linha do
   tempo de 3100: comeca em --d e dura 800 (as linhas, 900), com saida suave t(2 - t). As linhas crescem a partir de
   --ox/--oy (stroke-opacity zero antes de comecar: sem ele a ponta redonda apareceria como um ponto); etiquetas e nomes
   saem de --dx/--dy, pequenos e transparentes. Sem transicao: quem anda e o --p. O recuo do hover mexe no texto e
   no traco (opacity), que nao sao os mesmos elementos nem as mesmas propriedades. */
.ln-svg{--p:1}
.ln-svg :is(.ln-linha,.ln-eixo){--t:clamp(0, calc((var(--p) * 3100 - var(--d)) / 900), 1);
  transform-box:view-box;transform-origin:var(--ox) var(--oy);
  transform:scale(calc(.001 + .999 * var(--t) * (2 - var(--t))));stroke-opacity:calc(var(--t) * 40)}
.ln-b{--t:clamp(0, calc((var(--p) * 3100 - var(--d)) / 800), 1);--e:calc(var(--t) * (2 - var(--t)));
  opacity:var(--t);transform-box:fill-box;transform-origin:center;
  transform:translate(calc(var(--dx) * (1 - var(--e))), calc(var(--dy) * (1 - var(--e)))) scale(calc(.35 + .65 * var(--e)))}
.ln-b-nome{transform:translate(calc(var(--dx) * (1 - var(--e))), calc(var(--dy) * (1 - var(--e))))}
@media (max-width:1000px){ .ln-rola{display:none} }
"""

JS = r"""<script>
/* CONHECIMENTO: entrada do mapa de linhas nos DOIS SENTIDOS (_ferramentas/arcos/linhas.py). Toda vez que um
   mapa entra na tela (35% dele a vista), descendo ou subindo a pagina, o progresso --p corre de 0 a 1 em 3 s;
   quando o mapa sai inteiro de vista, --p volta a 0 e a entrada fica pronta para tocar de novo. Com movimento
   reduzido nada roda e o CSS deixa --p em 1. */
(function(){
  var ss = [].slice.call(document.querySelectorAll('.ln-svg'));
  if(!ss.length || !('IntersectionObserver' in window) || matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  var DUR = 3000;   /* 14/10/2026: «20% mais rapido» (era 3600) */
  ss.forEach(function(s){
    var p = 0, t0 = 0, raf = 0, tocou = false;
    function poe(){ s.style.setProperty('--p', p.toFixed(4)); }
    function passo(t){ if(!t0) t0 = t - p * DUR; p = Math.min(1, (t - t0) / DUR); poe();
      raf = p < 1 ? requestAnimationFrame(passo) : 0; }
    function toca(){ if(tocou) return; tocou = true; t0 = 0; raf = requestAnimationFrame(passo); }
    function zera(){ if(raf) cancelAnimationFrame(raf); raf = 0; tocou = false; p = 0; poe(); }
    poe();
    new IntersectionObserver(function(es){ es.forEach(function(e){
      if(!e.isIntersecting) zera(); else if(e.intersectionRatio >= .35) toca(); });
    }, {threshold:[0, .35]}).observe(s);
  });
})();
</script>"""
