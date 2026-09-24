# -*- coding: utf-8 -*-
"""SECAO DE TESTE: o mosaico do Conhecimento com poligonos no lugar dos circulos.

    python teste_poligonos.py          insere (ou troca) a secao de teste logo abaixo do Conhecimento
    python teste_poligonos.py --tirar  remove a secao de teste e as imagens dela

24/09/2026: o Leandro perguntou se pentagonos ou hexagonos (nada de quadrado ou
triangulo) ficariam melhores que os circulos. A secao de teste repete o mosaico
com tres formas trocaveis por botao: hexagono, pentagono e octogono.

REGRAS DA GEOMETRIA
  - centros, temas, normas e titulos sao os do arcos.py: so muda o contorno
    (excecao: se um par que cruza deixa de se cruzar, o menor anda ate o
    encontro; hoje so Seguranca de alimentos, 4 a 5 unidades);
  - raio do poligono = media entre inscrito e circunscrito no circulo original,
    para a forma nao encolher nem invadir o vizinho;
  - etiqueta propria vai para o vertice ou meio de lado mais proximo do angulo
    que ela tinha no circulo (alinhamento pela propria forma);
  - etiqueta compartilhada vai para o encontro dos dois contornos, como antes;
  - as manchas tambem viram poligonos, na mesma trama (imagem tramada fixa,
    sem o rastro do mouse: e so para comparar a forma).

Se o arcos.py mudar e o monta.py rodar de novo, rodar este depois: o monta
reinsere o Conhecimento antes de Servicos, e este volta a ficar logo abaixo."""

import math, os, re, sys
import numpy as np
from PIL import Image, ImageDraw

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import arcos, manchas

SITE = os.path.dirname(os.path.dirname(AQUI))
INI, FIM = '<!-- TESTE POLIGONOS: inicio -->', '<!-- TESTE POLIGONOS: fim -->'
# (id, rotulo, lados, angulo do primeiro vertice)
# rotacoes escolhidas por varredura: as unicas sem etiqueta sobre titulo (pentagono inclinado 18 graus;
# octogono com vertice em cima, 1 grau fora do eixo para a SMETA 7.0 nao encostar no titulo)
FORMAS = [('hex', 'Hexágono', 6, -90), ('pent', 'Pentágono', 5, -72), ('oct', 'Octógono', 8, -91)]
LARG = 1800


def fator(n):
    return (1 + 1 / math.cos(math.pi / n)) / 2


def vertices(cx, cy, r, n, rot):
    R = r * fator(n)
    return [(cx + R * math.cos(math.radians(rot + 360.0 * k / n)),
             cy + R * math.sin(math.radians(rot + 360.0 * k / n))) for k in range(n)]


def ancoras(cx, cy, r, n, rot):
    v = vertices(cx, cy, r, n, rot)
    out = []
    for k in range(n):
        a, b = v[k], v[(k + 1) % n]
        out += [a, ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2)]
    return out


def ang(cx, cy, p):
    return math.degrees(math.atan2(p[1] - cy, p[0] - cx))


def dif(a, b):
    return abs((a - b + 180) % 360 - 180)


def encontro(pa, pb, lado):
    pts = []
    for i in range(len(pa)):
        p1, p2 = pa[i], pa[(i + 1) % len(pa)]
        for j in range(len(pb)):
            q1, q2 = pb[j], pb[(j + 1) % len(pb)]
            d = (p2[0] - p1[0]) * (q2[1] - q1[1]) - (p2[1] - p1[1]) * (q2[0] - q1[0])
            if abs(d) < 1e-9:
                continue
            t = ((q1[0] - p1[0]) * (q2[1] - q1[1]) - (q1[1] - p1[1]) * (q2[0] - q1[0])) / d
            u = ((q1[0] - p1[0]) * (p2[1] - p1[1]) - (q1[1] - p1[1]) * (p2[0] - p1[0])) / d
            if 0 <= t <= 1 and 0 <= u <= 1:
                pts.append((p1[0] + t * (p2[0] - p1[0]), p1[1] + t * (p2[1] - p1[1])))
    assert pts, 'os contornos nao se cruzam'
    return max(pts, key=lambda q: q[1]) if lado == 'baixo' else min(pts, key=lambda q: q[1])


def temas(n, rot):
    """os temas do arcos.py; se um par que cruza de proposito deixa de se cruzar
    na forma nova (o poligono encolhe na diagonal), o vizinho anda em direcao ao
    eixo ate os contornos se encontrarem, mais 4 unidades"""
    T = [list(t) for t in arcos.TEMAS]
    por = {t[0]: t for t in T}
    for par in arcos.CRUZAM:
        a, b = sorted(par, key=lambda x: por[x][5], reverse=True)   # a = o maior, fica
        A, B = por[a], por[b]
        extra = None
        for passo in range(0, 200):
            try:
                encontro(vertices(A[3], A[4], A[5], n, rot), vertices(B[3], B[4], B[5], n, rot), 'baixo')
                if extra is None:
                    extra = 0
                    if passo == 0:
                        break
                extra += 1
                if extra > 4:
                    break
            except AssertionError:
                pass
            d = math.hypot(B[3] - A[3], B[4] - A[4])
            B[3] -= (B[3] - A[3]) / d; B[4] -= (B[4] - A[4]) / d
    return [tuple(t) for t in T]


def titulos(L, TT):
    base = {t['tema']: t for t in arcos.titulos(L)}
    out = []
    for t, o in zip(TT, arcos.TEMAS):
        b = base[t[0]]; dx, dy = t[3] - o[3], t[4] - o[4]
        out.append(dict(tema=t[0], x0=b['x0'] + dx, x1=b['x1'] + dx, y0=b['y0'] + dy, y1=b['y1'] + dy))
    return out


def pilulas(L, n, rot):
    larg = {(p['tema'], p['txt']): p['w'] for p in arcos.pilulas(L)}
    TT = temas(n, rot)
    polig = {t[0]: vertices(t[3], t[4], t[5], n, rot) for t in TT}
    out = []
    for tid, pag, div, cx, cy, r, tit, normas in TT:
        # as compartilhadas primeiro, para as proprias nao ocuparem o lugar delas
        for txt, a in normas:
            if isinstance(a, str):
                _, par, lado = a.split(':')
                x, y = encontro(polig[tid], polig[par], lado)
                out.append(dict(tema=tid, txt=txt, x=x, y=y, cruza=par, w=larg[(tid, txt)]))
    for p in out:
        caixa(p)
    for tid, pag, div, cx, cy, r, tit, normas in TT:
        livres = [q for q in ancoras(cx, cy, r, n, rot)]
        for txt, a in normas:
            if isinstance(a, str):
                continue
            # o ponto mais perto do angulo original que nao bate em titulo nem em outra etiqueta
            escolha = None
            for q in sorted(livres, key=lambda q: dif(ang(cx, cy, q), a)):
                p = caixa(dict(tema=tid, txt=txt, x=q[0], y=q[1], cruza=None, w=larg[(tid, txt)]))
                if len(colisoes(L, out + [p], TT)) == len(colisoes(L, out, TT)):
                    escolha = (q, p); break
            if escolha is None:
                q = min(livres, key=lambda q: dif(ang(cx, cy, q), a))
                escolha = (q, caixa(dict(tema=tid, txt=txt, x=q[0], y=q[1], cruza=None, w=larg[(tid, txt)])))
            livres.remove(escolha[0])
            out.append(escolha[1])
    return out


def caixa(p):
    p.update(x0=p['x'] - p['w'] / 2, x1=p['x'] + p['w'] / 2,
             y0=p['y'] - arcos.PIL_H / 2, y1=p['y'] + arcos.PIL_H / 2)
    return p


def colisoes(L, P, TT, folga=6):
    T = titulos(L, TT)
    ruim = []
    bate = lambda a, b: not (a['x1'] + folga <= b['x0'] or b['x1'] + folga <= a['x0'] or
                             a['y1'] + folga <= b['y0'] or b['y1'] + folga <= a['y0'])
    for i in range(len(P)):
        for j in range(i + 1, len(P)):
            if bate(P[i], P[j]):
                ruim.append('%s / %s' % (P[i]['txt'], P[j]['txt']))
        for t in T:
            if bate(P[i], t):
                ruim.append('%s / titulo %s' % (P[i]['txt'], t['tema']))
    return ruim


def limites(L, P, n, rot, TT, margem=10):
    xs, ys = [], []
    for t in TT:
        for x, y in vertices(t[3], t[4], t[5], n, rot):
            xs.append(x); ys.append(y)
    for cx, cy, r in arcos.DISCOS:
        for x, y in vertices(cx, cy, r, n, rot):
            xs.append(x); ys.append(y)
    for p in P:
        xs += [p['x0'], p['x1']]; ys += [p['y0'], p['y1']]
    x0, y0 = min(xs) - margem, min(ys) - margem
    return x0, y0, max(xs) + margem - x0, max(ys) + margem - y0


def pts(v, cx=0, cy=0):
    return ' '.join('%.1f,%.1f' % (x - cx, y - cy) for x, y in v)


def svg(L, P, n, rot, caixa, TT):
    o = ['<svg class="ar-svg" viewBox="%.1f %.1f %.1f %.1f" aria-label="Temas e normas (teste)">' % caixa,
         '<g class="ar-temas">']
    for tid, pag, div, cx, cy, r, tit, normas in TT:
        v = pts(vertices(cx, cy, r, n, rot), cx, cy)
        o.append('<a class="ar-tema" data-t="%s" href="%s" style="--cx:%.1fpx;--cy:%.1fpx">' % (tid, pag, cx, cy))
        o.append('<polygon class="ar-aro%s" points="%s" aria-hidden="true"/>' % (' ar-aro--i' if div == 'i' else '', v))
        o.append('<polygon class="ar-alvo" points="%s"/>' % v)
        y0 = -arcos.LH_TIT * (len(tit) - 1) / 2.0
        o.append('<text class="ar-tit" x="0" y="%.1f" aria-hidden="true">' % y0 +
                 ''.join('<tspan x="0" dy="%s">%s</tspan>' % ('0' if k == 0 else arcos.LH_TIT, arcos.esc(l))
                         for k, l in enumerate(tit)) + '</text>')
        for p in (p for p in P if p['tema'] == tid or p['cruza'] == tid):
            eco = p['tema'] != tid
            attrs = ' data-dono="%s" data-par="%s"' % (p['tema'], p['cruza']) if p['cruza'] else ''
            o.append('<g class="ar-pil%s"%s aria-hidden="true"><rect x="%.1f" y="%.1f" width="%.1f" height="%d" rx="3"/>'
                     '<text x="%.1f" y="%.1f">%s</text></g>'
                     % (' ar-pil--eco' if eco else '', attrs, p['x0'] - cx, p['y0'] - cy, p['w'], arcos.PIL_H,
                        p['x'] - cx, p['y'] - cy + 3.7, arcos.esc(p['txt'])))
        o.append('</a>')
    o.append('</g></svg>')
    return '\n'.join(o)


def manchas_img(fid, n, rot, caixa):
    x0, y0, w, h = caixa
    H = int(round(LARG * h / w)); s = LARG / w
    alvo = np.ones((H, LARG))
    for cx, cy, r in arcos.DISCOS:
        m = Image.new('L', (LARG, H), 0)
        ImageDraw.Draw(m).polygon([((x - x0) * s, (y - y0) * s) for x, y in vertices(cx, cy, r, n, rot)], fill=255)
        dentro = np.asarray(m) > 127
        ja = dentro & (alvo < 1)
        t = manchas.TOM_AZUL
        alvo = np.where(ja, np.minimum(alvo, t) - manchas.CRUZA, np.where(dentro, np.minimum(alvo, t), alvo))
    lum = np.ones_like(alvo)
    for t in np.unique(alvo):
        if t < 1:
            lum[alvo == t] = manchas.lum_para(t)
    yy, xx = np.mgrid[0:H, 0:LARG]
    m4 = np.array([[0, 8, 2, 10], [12, 4, 14, 6], [3, 11, 1, 9], [15, 7, 13, 5]])
    T = (m4[yy % 4, xx % 4] + .5) / 16
    k = np.clip(np.floor(manchas.tom((lum * 255).round() / 255) * 3 + T), 0, 3).astype(int)
    nome = 'teste-poligono-%s-bayer.webp' % fid
    Image.fromarray(manchas.CORES[k].round().astype(np.uint8), 'RGB').save(os.path.join(SITE, 'img', nome), lossless=True)
    return nome, H


ESTILO = """<style>
/* TESTE 24/09: botoes de troca da forma; some com --tirar */
.pt-troca{display:flex;gap:6px;margin:0 0 2px}
.pt-troca button{font-family:var(--mono);font-size:10.5px;letter-spacing:.2em;text-transform:uppercase;
  padding:8px 12px;border:1px solid rgba(20,48,76,.22);border-radius:3px;background:transparent;
  color:var(--azul-escuro);cursor:pointer}
.pt-troca button[aria-pressed="true"]{background:var(--azul);border-color:var(--azul);color:var(--mercurio)}
.pt-forma[hidden]{display:none}
.ar-teste .ar-alvo{fill:transparent}
</style>"""

SCRIPT = """<script>
/* TESTE 24/09: troca da forma e tema em hover para a frente */
(function(){
  var s = document.getElementById('conhecimento-teste'); if(!s) return;
  var bs = s.querySelectorAll('.pt-troca button'), fs = s.querySelectorAll('.pt-forma');
  bs.forEach(function(b){ b.addEventListener('click', function(){
    bs.forEach(function(x){ x.setAttribute('aria-pressed', x === b ? 'true' : 'false'); });
    fs.forEach(function(f){ f.hidden = f.getAttribute('data-forma') !== b.getAttribute('data-forma'); });
  }); });
  s.querySelectorAll('.ar-temas').forEach(function(g){
    g.addEventListener('mouseover', function(e){
      var t = e.target.closest('.ar-tema'); if(t && t !== g.lastElementChild) g.appendChild(t);
    });
  });
})();
</script>"""


def secao(L):
    o = [INI, '<section class="ar-sec ar-teste" id="conhecimento-teste" aria-label="Teste do mosaico com polígonos">',
         ESTILO, '  <div class="ar-cab">', '    <p class="ar-rotulo">Teste / [ IM.2 com polígonos ]</p>',
         '    <div class="ar-linha">',
         '      <h2 class="ar-titulo">O mesmo mosaico, com polígonos no lugar dos círculos</h2>',
         '      <div class="pt-troca">' + ''.join(
             '<button type="button" data-forma="%s" aria-pressed="%s">%s</button>' % (f, 'true' if k == 0 else 'false', rot)
             for k, (f, rot, n, a) in enumerate(FORMAS)) + '</div>',
         '    </div>', '  </div>']
    for k, (fid, rot_txt, n, rot) in enumerate(FORMAS):
        P = pilulas(L, n, rot)
        TT = temas(n, rot)
        mov = ['%s %+.0f,%+.0f' % (t[0], t[3] - o[3], t[4] - o[4]) for t, o in zip(TT, arcos.TEMAS) if t[3:5] != o[3:5]]
        print('%-4s centros movidos: %s' % (fid, mov or 'nenhum'))
        ruim = colisoes(L, P, TT)
        print('%-4s colisoes: %d %s' % (fid, len(ruim), ruim))
        caixa = limites(L, P, n, rot, TT)
        nome, H = manchas_img(fid, n, rot, caixa)
        o += ['  <div class="ar-corpo pt-forma" data-forma="%s"%s>' % (fid, '' if k == 0 else ' hidden'),
              '  <div class="ar-palco">',
              '    <div class="ar-manchas" aria-hidden="true"><img src="img/%s?v=1" alt="" width="%d" height="%d" loading="lazy" decoding="async"></div>'
              % (nome, LARG, H),
              svg(L, P, n, rot, caixa, TT), '  </div>',
              '  <div class="ar-foto" aria-hidden="true"><img src="img/conhecimento-foto-bayer.webp?v=7" alt="" width="480" height="867" loading="lazy" decoding="async"></div>',
              '  </div>']
    o += ['</section>', SCRIPT, FIM]
    return '\n'.join(o)


def main(tirar=False):
    p = os.path.join(SITE, 'index.html')
    raw = open(p, 'rb').read()
    eol = '\r\n' if raw.count(b'\r\n') else '\n'
    t = raw.decode('utf-8').replace('\r\n', '\n')
    t = re.sub(re.escape(INI) + r'.*?' + re.escape(FIM) + r'\n\n', '', t, flags=re.S)
    if tirar:
        for f, _, _, _ in FORMAS:
            q = os.path.join(SITE, 'img', 'teste-poligono-%s-bayer.webp' % f)
            if os.path.exists(q):
                os.remove(q)
        print('secao de teste removida')
    else:
        m = re.search(r'<section class="ar-sec" id="conhecimento".*?</section>\n\n', t, flags=re.S)
        assert m, 'secao Conhecimento nao encontrada'
        t = t[:m.end()] + secao(arcos.larguras()) + '\n\n' + t[m.end():]
        print('secao de teste inserida logo abaixo do Conhecimento')
    open(p, 'wb').write(t.replace('\n', eol).encode('utf-8'))


if __name__ == '__main__':
    main('--tirar' in sys.argv)
