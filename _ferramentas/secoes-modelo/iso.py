"""Desenhos isometricos dos modelos de secao (04/11/2026). Tudo em SVG, com as cores em variaveis CSS,
para o seletor de acento da prova trocar a cor sem refazer o desenho."""
import math

C, S = math.cos(math.radians(30)), .5


def f(n):
    return f'{n:.2f}'.rstrip('0').rstrip('.')


class Iso:
    def __init__(self, ox, oy, u):
        self.ox, self.oy, self.u = ox, oy, u
        self.s = []
        self.xs, self.ys = [], []

    def p(self, x, y, z=0):
        X, Y = self.ox + (x - y) * C * self.u, self.oy + (x + y) * S * self.u - z * self.u
        self.xs.append(X); self.ys.append(Y)
        return (X, Y)

    def vb(self, e=20, t=20, d=20, b=20):
        """viewBox justo no desenho: nada corta, nada invade a secao vizinha."""
        x0, y0, x1, y1 = min(self.xs) - e, min(self.ys) - t, max(self.xs) + d, max(self.ys) + b
        return f'{f(x0)} {f(y0)} {f(x1 - x0)} {f(y1 - y0)}'

    def pts(self, lista):
        return ' '.join(f'{f(a)},{f(b)}' for a, b in (self.p(*q) for q in lista))

    def poly(self, lista, cls='', extra=''):
        self.s.append(f'<polygon class="{cls}" points="{self.pts(lista)}" {extra}/>')

    def line(self, a, b, cls='fio'):
        (x1, y1), (x2, y2) = self.p(*a), self.p(*b)
        self.s.append(f'<line class="{cls}" x1="{f(x1)}" y1="{f(y1)}" x2="{f(x2)}" y2="{f(y2)}"/>')

    def box(self, x, y, z, dx, dy, dz, topo, frente, lado):
        """Caixa com as 3 faces visiveis. Frente = face y maximo (desce para a direita); lado = face x maximo."""
        self.poly([(x, y, z + dz), (x + dx, y, z + dz), (x + dx, y + dy, z + dz), (x, y + dy, z + dz)], topo)
        self.poly([(x, y + dy, z + dz), (x + dx, y + dy, z + dz), (x + dx, y + dy, z), (x, y + dy, z)], frente)
        self.poly([(x + dx, y, z + dz), (x + dx, y + dy, z + dz), (x + dx, y + dy, z), (x + dx, y, z)], lado)

    def m_frente(self, x, y, z):
        X, Y = self.p(x, y, z)
        return f'matrix({f(C)} {f(S)} 0 1 {f(X)} {f(Y)})'

    def m_lado(self, x, y, z):
        X, Y = self.p(x, y, z)
        return f'matrix({f(C)} {f(-S)} 0 1 {f(X)} {f(Y)})'

    def m_topo(self, x, y, z):
        X, Y = self.p(x, y, z)
        return f'matrix({f(C)} {f(S)} {f(-C)} {f(S)} {f(X)} {f(Y)})'

    def add(self, txt):
        self.s.append(txt)

    def svg(self):
        return ''.join(self.s)


def sombra_defs(id_='smBlur', d=12):
    return f'<defs><filter id="{id_}" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="{d}"/></filter></defs>'


# ------------------------------------------------------------ pilha (hierarquia de controles)
def pilha(camadas):
    """camadas: de cima para baixo, (texto, item). A de cima sai na tinta."""
    g = Iso(270, 214, 42)
    LX, LY, A = 9.4, 3.6, 1.14
    n = len(camadas)
    s = [sombra_defs('smBlurP', 14)]
    # sombra e base na cor de acento
    b = Iso(270, 214, 42)
    b.poly([(-1.1, -1.9, -n * A - 1.6), (11.8, -1.9, -n * A - 1.6), (11.8, 7.5, -n * A - 1.6), (-1.1, 7.5, -n * A - 1.6)], 'iso-sombra', 'filter="url(#smBlurP)" transform="translate(10 26)"')
    b.box(-1.1, -1.9, -n * A - 1.6, 12.9, 9.4, 1.6, 'iso-ac-t', 'iso-ac-f', 'iso-ac-l')
    g.s += b.s
    g.xs += b.xs; g.ys += b.ys
    g.poly([(-.1, -.1, -n * A), (LX + .5, -.1, -n * A), (LX + .5, LY + 1, -n * A), (-.1, LY + 1, -n * A)], 'iso-sombra', 'filter="url(#smBlurP)" opacity=".75" transform="translate(6 10)"')
    for i in range(n - 1, -1, -1):
        z = -(i + 1) * A
        esc = i == 0
        g.box(0, 0, z, LX, LY, A - .03, 'iso-tinta-t' if esc else 'iso-cl-t', 'iso-tinta-f' if esc else 'iso-cl-f', 'iso-tinta-l' if esc else 'iso-cl-l')
        t, item = camadas[i]
        cor = 'iso-tx-cl' if esc else 'iso-tx'
        g.add(f'<text class="iso-rot {cor}" transform="{g.m_frente(.38, LY, z + A * .36)}">{t}</text>')
        g.add(f'<text class="iso-rot iso-it {cor}" text-anchor="end" transform="{g.m_frente(LX - .34, LY, z + A * .36)}">{item}</text>')
    s.append(g.svg())
    s.append('</svg>')
    return f'<svg class="iso iso-pilha" viewBox="{g.vb(16, 16, 30, 50)}" role="img" aria-label="Hierarquia de controles em camadas">' + ''.join(s)


# ------------------------------------------------------------ escada (etapas da implantacao)
def _mini(i, w, h):
    """Miolo da placa de cada etapa, em coordenadas locais da face."""
    q = []
    if i == 0:   # diagnostico: comparacao requisito a requisito
        q.append(f'<text class="m-t" x="10" y="16">Diagnóstico</text>')
        for k in range(6):
            y = 30 + k * 13
            q.append(f'<line class="m-f" x1="10" x2="{w*.56:.0f}" y1="{y}" y2="{y}"/><rect class="m-q{" on" if k in (1,2,4) else ""}" x="{w*.66:.0f}" y="{y-4}" width="8" height="8"/><rect class="m-q{" on" if k in (0,3) else ""}" x="{w*.8:.0f}" y="{y-4}" width="8" height="8"/>')
    elif i == 1:  # plano diretor: barras no tempo
        q.append(f'<text class="m-t m-cl" x="10" y="16">Plano diretor</text>')
        for k, (a, b) in enumerate([(0, .3), (.14, .3), (.3, .36), (.5, .3), (.66, .34)]):
            y = 28 + k * 15
            q.append(f'<line class="m-f m-cl" x1="10" x2="{w-10}" y1="{y+9}" y2="{y+9}"/><rect class="m-b{" m-ac" if k == 2 else " m-cl"}" x="{10+a*(w-20):.0f}" y="{y}" width="{b*(w-20):.0f}" height="7"/>')
    elif i == 2:  # implantacao: processos encadeados
        q.append(f'<text class="m-t" x="10" y="16">Implantação</text>')
        cx = [w * .2, w * .5, w * .8]
        for k, x in enumerate(cx):
            q.append(f'<rect class="m-c{" on" if k == 1 else ""}" x="{x-16:.0f}" y="30" width="32" height="20"/>')
            if k: q.append(f'<line class="m-f" x1="{cx[k-1]+16:.0f}" x2="{x-16:.0f}" y1="40" y2="40"/>')
        q.append(f'<path class="m-f m-n" d="M{cx[1]:.0f} 50V62M{cx[0]:.0f} 62H{cx[2]:.0f}M{cx[0]:.0f} 62V72M{cx[2]:.0f} 62V72"/>')
        for x in (cx[0], cx[2]):
            q.append(f'<rect class="m-c" x="{x-16:.0f}" y="72" width="32" height="18"/>')
    elif i == 3:  # auditoria interna: lista de verificacao
        q.append(f'<text class="m-t" x="10" y="16">Auditoria interna</text>')
        for k in range(5):
            y = 30 + k * 14
            q.append(f'<rect class="m-q on" x="10" y="{y-4}" width="8" height="8"/><line class="m-f" x1="26" x2="{w-12-(k%3)*18}" y1="{y}" y2="{y}"/>')
    else:         # empresa pronta: losango
        q.append(f'<text class="m-t" x="10" y="16">Pronta para</text><text class="m-t" x="10" y="28">a certificação</text>')
        cx, cy = w / 2, h * .62
        q.append(f'<polygon class="m-l" points="{cx},{cy-26} {cx+26},{cy} {cx},{cy+26} {cx-26},{cy}"/><polygon class="m-l on" points="{cx},{cy-11} {cx+11},{cy} {cx},{cy+11} {cx-11},{cy}"/>')
    return ''.join(q)


def escada():
    g = Iso(92, 462, 34)
    PASSO_Y, PASSO_Z, N = 4.4, 1.05, 5
    LX = 9.2
    s = [sombra_defs('smBlurE', 16)]
    y_base = 4.4
    # sombra do conjunto
    g.poly([(-.4, -PASSO_Y * (N - 1) - .3, 0), (LX + 1, -PASSO_Y * (N - 1) - .3, 0), (LX + 1, y_base + .7, 0), (-.4, y_base + .7, 0)], 'iso-sombra', 'filter="url(#smBlurE)" transform="translate(16 34)"')
    for i in range(N - 1, -1, -1):
        y0 = -i * PASSO_Y
        ztopo = (i + 1) * PASSO_Z
        # corpo do degrau
        g.box(0, y0, 0, LX, PASSO_Y, ztopo - .22, 'iso-cl-t', 'iso-cl-f', 'iso-cl-l')
        # chapa escura do piso
        g.box(0, y0, ztopo - .22, LX, PASSO_Y, .22, 'iso-tinta-t', 'iso-tinta-f', 'iso-tinta-l')
        # placa em pe
        px, py, pw, ph, pe = 1.05, y0 + 1.5, 6.6, 5.1, .22
        esc = i == 1
        g.poly([(px + .2, py + pe, ztopo), (px + pw + .5, py + pe, ztopo), (px + pw + .5, py + pe + 1.1, ztopo), (px + .2, py + pe + 1.1, ztopo)], 'iso-sombra2')
        g.box(px, py, ztopo, pw, pe, ph, 'iso-tinta-t' if esc else 'iso-br-t', 'iso-tinta-f' if esc else 'iso-br-f', 'iso-tinta-l' if esc else 'iso-br-l')
        # miolo da placa, mapeado na face
        lw, lh = pw * g.u, ph * g.u
        esc_cls = ' m-esc' if esc else ''
        g.add(f'<g class="m{esc_cls}" transform="{g.m_frente(px, py + pe, ztopo + ph)}">{_mini(i, lw, lh)}</g>')
        # numero em relevo, no pe da placa
        X, Y = g.p(px + pw + .28, py + pe + .55, ztopo + .1)
        for k in range(5, 0, -1):
            g.add(f'<text class="iso-num iso-num-s" text-anchor="end" transform="matrix({f(C)} {f(S)} 0 1 {f(X + k*.8)} {f(Y - k*.46)})">0{i+1}</text>')
        g.add(f'<text class="iso-num" text-anchor="end" transform="matrix({f(C)} {f(S)} 0 1 {f(X)} {f(Y)})">0{i+1}</text>')
    # etiqueta presa na lateral
    ex, ey, ez = LX, -PASSO_Y * 1.05, .55
    g.poly([(ex, ey + 2.6, ez + 1.7), (ex, ey - 2.6, ez + 1.7 + 0), (ex, ey - 2.6, ez), (ex, ey + 2.6, ez)], 'iso-ac-t')
    g.add(f'<text class="iso-rot iso-tx-on" transform="{g.m_lado(ex, ey + 2.3, ez + 1.02)}">ISO 9001:2026</text>')
    g.add(f'<text class="iso-mini iso-tx-on" transform="{g.m_lado(ex, ey + 2.3, ez + .48)}">Etapas para implantação</text>')
    s.append(g.svg())
    s.append('</svg>')
    return f'<svg class="iso iso-escada" viewBox="{g.vb(16, 12, 30, 60)}" role="img" aria-label="Cinco etapas da implantação em uma escada">' + ''.join(s)


# ------------------------------------------------------------ planta em linha fina
def planta(marcas=False):
    """Linha fina; fundo em currentColor do painel: --fundo tampa o que fica atras."""
    g = Iso(250, 340, 13.2)
    r = []

    def ell(cx, cy, cz, raio):
        X, Y = g.p(cx, cy, cz)
        return X, Y, raio * 1.2247 * g.u, raio * .7071 * g.u

    def cilindro(x, y, z0, z1, raio, aneis=(), tampa=True):
        X0, Y0, rx, ry = ell(x, y, z0, raio)
        X1, Y1, _, _ = ell(x, y, z1, raio)
        r.append(f'<path class="pl-t" d="M{f(X0-rx)} {f(Y0)}A{f(rx)} {f(ry)} 0 0 0 {f(X0+rx)} {f(Y0)}L{f(X1+rx)} {f(Y1)}A{f(rx)} {f(ry)} 0 0 0 {f(X1-rx)} {f(Y1)}Z"/>')
        for z in aneis:
            X, Y, _, _ = ell(x, y, z, raio)
            r.append(f'<path class="pl-f" d="M{f(X-rx)} {f(Y)}A{f(rx)} {f(ry)} 0 0 0 {f(X+rx)} {f(Y)}"/>')
        if tampa:
            r.append(f'<ellipse class="pl-t" cx="{f(X1)}" cy="{f(Y1)}" rx="{f(rx)}" ry="{f(ry)}"/>')

    def domo(x, y, z, raio, alt):
        X, Y, rx, ry = ell(x, y, z, raio)
        r.append(f'<path class="pl-t" d="M{f(X-rx)} {f(Y)}C{f(X-rx)} {f(Y-alt*g.u)} {f(X+rx)} {f(Y-alt*g.u)} {f(X+rx)} {f(Y)}A{f(rx)} {f(ry)} 0 0 1 {f(X-rx)} {f(Y)}Z"/>')
        r.append(f'<path class="pl-f" d="M{f(X-rx)} {f(Y)}A{f(rx)} {f(ry)} 0 0 0 {f(X+rx)} {f(Y)}"/>')

    def cano(pontos, e=7):
        d = 'M' + 'L'.join('{} {}'.format(*map(f, g.p(*q))) for q in pontos)
        r.append(f'<path class="pl-c1" stroke-width="{e}" d="{d}"/><path class="pl-c2" stroke-width="{e-1.5}" d="{d}"/>')

    def caixa(x, y, z, dx, dy, dz):
        a = lambda *q: g.pts(q)
        r.append(f'<polygon class="pl-t" points="{a((x,y+dy,z+dz),(x+dx,y+dy,z+dz),(x+dx,y+dy,z),(x,y+dy,z))}"/>')
        r.append(f'<polygon class="pl-t" points="{a((x+dx,y,z+dz),(x+dx,y+dy,z+dz),(x+dx,y+dy,z),(x+dx,y,z))}"/>')
        r.append(f'<polygon class="pl-t" points="{a((x,y,z+dz),(x+dx,y,z+dz),(x+dx,y+dy,z+dz),(x,y+dy,z+dz))}"/>')

    def fio(a, b, cls='pl-f'):
        (x1, y1), (x2, y2) = g.p(*a), g.p(*b)
        r.append(f'<line class="{cls}" x1="{f(x1)}" y1="{f(y1)}" x2="{f(x2)}" y2="{f(y2)}"/>')

    # --- torre, atras
    cilindro(4.5, -7.5, 0, 25, 3.1, aneis=[3, 7, 11, 15, 19, 23], tampa=False)
    domo(4.5, -7.5, 25, 3.1, 1.6)
    cilindro(4.5, -7.5, 0, 1.4, 3.9, tampa=True)
    # escada de marinheiro na torre
    for z in range(2, 24, 1):
        fio((6.8, -5.2, z), (7.6, -4.4, z))
    fio((6.8, -5.2, 2), (6.8, -5.2, 24)); fio((7.6, -4.4, 2), (7.6, -4.4, 24))
    # --- cano da torre descendo ate a base
    cano([(4.5, -4.2, 17.5), (4.5, -1.6, 17.5), (4.5, -1.6, 8), (2.4, 1.4, 8)], 8)
    cano([(6.8, -5.4, 12), (8.6, -3.6, 12), (8.6, -3.6, 6), (8.6, 1.2, 6)], 6.5)
    # --- estrutura da base
    bx, by, bw, bd = -9, 0, 20, 13
    h1, h2 = 3.4, 8.4
    # colunas de tras
    for (cx, cy) in [(bx, by), (bx + 10, by), (bx + bw, by)]:
        fio((cx, cy, 0), (cx, cy, h2), 'pl-e')
    # piso do andar
    caixa(bx, by, h1, bw, bd, .6)
    for k in range(1, 10):
        fio((bx + k * bw / 10, by, h1 + .6), (bx + k * bw / 10, by + bd, h1 + .6))
    for k in range(1, 6):
        fio((bx, by + k * bd / 6, h1 + .6), (bx + bw, by + k * bd / 6, h1 + .6))
    # vasos em cima do piso
    cilindro(-5.2, 4.2, h1 + .6, h1 + 6.2, 2.2, aneis=[h1 + 2, h1 + 4.2])
    cilindro(.2, 3.8, h1 + .6, h1 + 4.2, 1.7, aneis=[h1 + 2.2])
    caixa(4.4, 2.2, h1 + .6, 5, 3, 2.8)
    for k in range(1, 5):
        fio((4.4 + k, 5.2, h1 + .6), (4.4 + k, 5.2, h1 + 3.4))
    # canos sobre o piso
    cano([(-5.2, 4.2, h1 + 6.4), (-5.2, 4.2, h1 + 8.6), (.2, 4.2, h1 + 8.6), (.2, 4.2, h1 + 4.4)], 6.5)
    cano([(.2, 3.8, h1 + 5.8), (6.4, 3.8, h1 + 5.8), (6.4, 3.8, h1 + 3.4)], 5.5)
    # colunas da frente e guarda-corpo
    for (cx, cy) in [(bx, by + bd), (bx + 10, by + bd), (bx + bw, by + bd), (bx + bw, by + bd / 2)]:
        fio((cx, cy, 0), (cx, cy, h1), 'pl-e')
    for (a, b) in [((bx, by + bd), (bx + bw, by + bd)), ((bx + bw, by + bd), (bx + bw, by))]:
        for z in (h1 + 1.5, h1 + 3):
            fio((*a, z), (*b, z))
    for k in range(0, 11, 2):
        fio((bx + k * 2, by + bd, h1 + .6), (bx + k * 2, by + bd, h1 + 3))
    for k in range(0, 7, 2):
        fio((bx + bw, by + bd - k * bd / 6, h1 + .6), (bx + bw, by + bd - k * bd / 6, h1 + 3))
    # travamentos
    fio((bx, by + bd, 0), (bx + 10, by + bd, h1)); fio((bx + 10, by + bd, 0), (bx + bw, by + bd, h1))
    # bomba e cano no chao
    caixa(13, 6, 0, 3.2, 2.2, 2)
    cano([(11, 7, 1), (13, 7, 1)], 5)
    cano([(16.2, 7, 1.2), (20, 7, 1.2), (20, 7, 3.4)], 5)
    # sapatas
    for (cx, cy) in [(bx, by + bd), (bx + 10, by + bd), (bx + bw, by + bd)]:
        caixa(cx - .6, cy - .6, 0, 1.2, 1.2, .3)
    # cacamba de residuos, no chao, a frente
    caixa(2, 16, 0, 5, 3, 2)
    for k in (1, 2, 3, 4):
        fio((2 + k, 19, 0), (2 + k, 19, 2))
    if marcas:
        for n, q in enumerate([(4.5, -7.5, 23), (-5.2, 4.2, h1 + 6.2), (6.9, 3.7, h1 + 3.4), (14.6, 7, 2), (4.5, 17.5, 2)], 1):
            X, Y = g.p(*q)
            r.append(f'<g class="mk2" data-p="{n}" tabindex="0" transform="translate({f(X)} {f(Y)})"><polygon points="0,-11 11,0 0,11 -11,0"/><text y="3.6" text-anchor="middle">{n}</text></g>')
    return f'<svg class="iso-planta" viewBox="-8 -38 428 572" role="img" aria-label="Unidade industrial em linha fina">{"".join(r)}</svg>'


# ------------------------------------------------------------ blocos do sistema integrado
def integrado():
    g = Iso(380, 228, 30)
    s = [sombra_defs('smBlurI', 14)]
    LX, LY = 11, 11
    g.poly([(-.6, -.6, -3.6), (LX + .8, -.6, -3.6), (LX + .8, LY + .8, -3.6), (-.6, LY + .8, -3.6)], 'iso-sombra', 'filter="url(#smBlurI)" transform="translate(10 26)"')
    # base comum, cor de acento
    g.box(0, 0, -3.6, LX, LY, 1.5, 'iso-ac-t', 'iso-ac-f', 'iso-ac-l')
    g.add(f'<text class="iso-rot iso-tx-on" transform="{g.m_frente(.4, LY, -3.6 + .52)}">Estrutura comum, itens 4 a 10</text>')
    g.add(f'<text class="iso-rot iso-tx-on" transform="{g.m_lado(LX, LY - .4, -3.6 + .52)}">Sistema de gestão integrado</text>')
    # fios tracejados de explosao + tres blocos
    blocos = [('ISO 9001', 'Clientes e produtos', .8, .8), ('ISO 14001', 'Aspectos ambientais', 6.6, .8), ('ISO 45001', 'Perigos e riscos', 3.7, 6.2)]
    ordem = sorted(blocos, key=lambda b: b[2] + b[3])
    for nome, tema, x, y in ordem:
        dx, dy, dz = 4.0, 4.0, 2.0
        z0 = 1.1
        for (a, b) in [(x, y + dy), (x + dx, y + dy), (x + dx, y)]:
            g.line((a, b, -2.1), (a, b, z0), 'iso-trac')
        g.box(x, y, z0, dx, dy, dz, 'iso-br-t', 'iso-cl-f', 'iso-cl-l')
        g.add(f'<text class="iso-top" text-anchor="middle" transform="{g.m_topo(x + dx / 2, y + dy / 2 + .2, z0 + dz)}">{nome}</text>')
        g.add(f'<text class="iso-mini iso-tx" transform="{g.m_frente(x + .22, y + dy, z0 + .7)}">{tema}</text>')
    s.append(g.svg())
    s.append('</svg>')
    return f'<svg class="iso iso-int" viewBox="{g.vb(16, 16, 30, 50)}" role="img" aria-label="Núcleo comum do sistema de gestão integrado e três normas">' + ''.join(s)


# ------------------------------------------------------------ matriz em relevo
def matriz_relevo(setores, normas, tem):
    """setores: [(id, nome)], normas: [(id, rotulo)], tem: {(setor, norma): 'q' destaque | 'q t' qualquer setor}."""
    ns, nn = len(setores), len(normas)
    u = 34
    g = Iso(250 + ns * 0 + 4, 150, u)
    s = [sombra_defs('smBlurM', 12)]
    g.poly([(0, 0, -.5), (nn * 1.6, 0, -.5), (nn * 1.6, ns * 1.3, -.5), (0, ns * 1.3, -.5)], 'iso-sombra', 'filter="url(#smBlurM)" transform="translate(8 20)"')
    g.box(0, 0, -.45, nn * 1.6, ns * 1.3, .45, 'iso-cl-t', 'iso-cl-f', 'iso-cl-l')
    for j in range(nn + 1):
        g.line((j * 1.6, 0, 0), (j * 1.6, ns * 1.3, 0), 'iso-grade')
    for i in range(ns + 1):
        g.line((0, i * 1.3, 0), (nn * 1.6, i * 1.3, 0), 'iso-grade')
    for i, (sid, _) in enumerate(setores):
        for j, (nid, _) in enumerate(normas):
            k = tem.get((sid, nid))
            if not k:
                continue
            x, y = j * 1.6 + .32, i * 1.3 + .2
            if k == 'q':
                g.box(x, y, 0, .96, .9, .78, 'iso-ac-t', 'iso-ac-f', 'iso-ac-l')
            else:
                g.box(x, y, 0, .96, .9, .22, 'iso-br-t', 'iso-tinta-f2', 'iso-tinta-l2')
    # rotulos por ultimo, para nenhum bloco cobrir
    for j, (_, r) in enumerate(normas):
        X, Y = g.p(j * 1.6 + .86, -.85, 0)
        g.add(f'<text class="iso-mini iso-tx" transform="matrix({f(C)} {f(-S)} 0 1 {f(X)} {f(Y)})" data-c="{normas[j][0]}">{r}</text>')
    for i, (sid, nome) in enumerate(setores):
        X, Y = g.p(-.85, i * 1.3 + .72, 0)
        g.add(f'<text class="iso-mini iso-tx" text-anchor="end" transform="matrix({f(C)} {f(S)} 0 1 {f(X)} {f(Y)})">{nome}</text>')
    s.append(g.svg())
    s.append('</svg>')
    return f'<svg class="iso iso-mat" viewBox="{g.vb(150, 90, 100, 40)}" role="img" aria-label="Matriz de setores e normas em relevo">' + ''.join(s)


# ------------------------------------------------------------ codigo de barras (Code 39 de verdade)
_C39 = dict(zip('0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ-. *', '''nnnwwnwnn wnnwnnnnw nnwwnnnnw wnwwnnnnn nnnwwnnnw wnnwwnnnn nnwwwnnnn nnnwnnwnw wnnwnnwnn nnwwnnwnn
wnnnnwnnw nnwnnwnnw wnwnnwnnn nnnnwwnnw wnnnwwnnn nnwnwwnnn nnnnnwwnw wnnnnwwnn nnwnnwwnn nnnnwwwnn wnnnnnnww nnwnnnnww wnwnnnnwn nnnnwnnww wnnnwnnwn nnwnwnnwn nnnnnnwww wnnnnnwwn nnwnnnwwn nnnnwnwwn wwnnnnnnw nwwnnnnnw wwwnnnnnn nwnnwnnnw wwnnwnnnn nwwnwnnnn nwnnnnwnw wwnnnnwnn nwwnnnwnn nwnnwnwnn'''.split()))


def barras(txt, altura=30, nar=1.1, lar=2.8):
    x, s = 0, []
    for ch in f'*{txt}*':
        for i, b in enumerate(_C39[ch]):
            w = lar if b == 'w' else nar
            if i % 2 == 0:
                s.append(f'<rect x="{f(x)}" width="{f(w)}" height="{altura}"/>')
            x += w
        x += nar
    return f'<svg class="sm-bar" viewBox="0 0 {f(x)} {altura}" aria-hidden="true" preserveAspectRatio="none">{"".join(s)}</svg>'
