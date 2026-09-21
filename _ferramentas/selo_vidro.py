# -*- coding: utf-8 -*-
"""Variante «vidro» do selo oficial (Asset 175): azulado bem claro, com reflexo.

O selo oficial nao muda. Sai img/selo-ideal-m-vidro.svg, usado so no canto da
segunda secao da home, e uma copia em «Ideal Metrics Logo/».

TRES CAMADAS DE COR, lidas do proprio arquivo:
  anel, faixa e fundo   os degrades do selo (#315275 a #A3B5C8) sao remapeados
                        pela luminancia para #C9D8E9 a #F5F8FC: azul bem claro
  passaro               o grupo com mais poligonos tem degrade proprio, remapeado
                        para #7F9DBF a #B4C7DC, para nao sumir no miolo claro
  letras e fios         o creme #FAF9F5 (43 formas: texto circular, «ideal.m»,
                        fios) vira #6F8FB3. Creme sobre azul muito claro nao le.

O VIDRO, desenhado no proprio SVG e recortado pelo circulo do selo:
  reflexo    uma elipse no alto com degrade de branco 70% a 0%
  borda      um fio branco a 85% no limite, e um fio azul a 30% logo dentro
A sombra fica no CSS da pagina (drop-shadow), para nao engordar a caixa."""

import re, os, colorsys
import xml.etree.ElementTree as ET

AQUI = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(AQUI)
ORIG = os.path.join(SITE, 'img', 'selo-ideal-m.svg')
SAIDAS = [os.path.join(SITE, 'img', 'selo-ideal-m-vidro.svg'),
          os.path.join(os.path.dirname(SITE), 'Ideal Metrics Logo', 'selo-ideal-m-vidro.svg')]
NS = '{http://www.w3.org/2000/svg}'
XL = '{http://www.w3.org/1999/xlink}'
ET.register_namespace('', 'http://www.w3.org/2000/svg')
ET.register_namespace('xlink', 'http://www.w3.org/1999/xlink')

ESCURO, CLARO = '#315275', '#a3b5c8'          # as pontas dos degrades do original
ANEL = ('#c9d8e9', '#f5f8fc')                 # azul bem claro
PASSARO = ('#7f9dbf', '#b4c7dc')
TINTA = '#6f8fb3'                             # letras e fios


def rgb(h): h = h.lstrip('#'); return [int(h[i:i + 2], 16) for i in (0, 2, 4)]
def hexa(c): return '#%02x%02x%02x' % tuple(int(round(max(0, min(255, v)))) for v in c)
def lum(h): r, g, b = rgb(h); return .2126 * r + .7152 * g + .0722 * b


def remapa(cor, faixa):
    t = (lum(cor) - lum(ESCURO)) / (lum(CLARO) - lum(ESCURO))
    t = max(0.0, min(1.0, t))
    a, b = rgb(faixa[0]), rgb(faixa[1])
    return hexa([a[i] + (b[i] - a[i]) * t for i in range(3)])


def n_poly(e): return sum(1 for x in e.iter() if x.tag == NS + 'polygon')


def main():
    t = ET.parse(ORIG); raiz = t.getroot()
    vb = [float(v) for v in raiz.get('viewBox').split()]
    cx, cy, r = vb[2] / 2, vb[3] / 2, min(vb[2], vb[3]) / 2
    defs = raiz.find(NS + 'defs')
    grad = {g.get('id'): g for g in defs.iter() if g.tag in (NS + 'linearGradient', NS + 'radialGradient')}

    camada = list(raiz.find(NS + 'g'))[0]
    passaro = max(list(camada), key=n_poly)
    ids_passaro = set()
    for e in passaro.iter():
        m = re.match(r'url\(#([^)]+)\)', e.get('fill') or '')
        if m: ids_passaro.add(m.group(1))

    def paradas(gid, seen=None):
        """as paradas do degrade, seguindo xlink:href quando ele herda"""
        g = grad.get(gid)
        if g is None: return []
        st = [s for s in g if s.tag == NS + 'stop']
        if st: return st
        ref = (g.get(XL + 'href') or g.get('href') or '').lstrip('#')
        return paradas(ref) if ref and ref != gid else []

    # degrades do passaro podem herdar de outros: clona para nao pintar o anel junto
    feitos = set()
    for gid in ids_passaro:
        for s in paradas(gid):
            if id(s) in feitos: continue
            s.set('stop-color', remapa(s.get('stop-color'), PASSARO)); feitos.add(id(s))
    for gid in grad:
        for s in paradas(gid):
            if id(s) in feitos: continue
            s.set('stop-color', remapa(s.get('stop-color'), ANEL)); feitos.add(id(s))

    n = 0
    for e in raiz.iter():
        if (e.get('fill') or '').lower() == '#faf9f5':
            e.set('fill', TINTA); n += 1

    # o vidro
    ET.SubElement(defs, NS + 'clipPath', id='vidro-recorte').append(
        ET.Element(NS + 'circle', cx='%.2f' % cx, cy='%.2f' % cy, r='%.2f' % (r - .3)))
    lg = ET.SubElement(defs, NS + 'linearGradient', id='vidro-brilho', x1='0', y1='0', x2='0', y2='1')
    ET.SubElement(lg, NS + 'stop', offset='0', **{'stop-color': '#ffffff', 'stop-opacity': '.72'})
    ET.SubElement(lg, NS + 'stop', offset='.55', **{'stop-color': '#ffffff', 'stop-opacity': '.18'})
    ET.SubElement(lg, NS + 'stop', offset='1', **{'stop-color': '#ffffff', 'stop-opacity': '0'})
    vidro = ET.SubElement(raiz, NS + 'g', id='vidro', **{'clip-path': 'url(#vidro-recorte)'})
    ET.SubElement(vidro, NS + 'ellipse', cx='%.2f' % (cx - r * .08), cy='%.2f' % (cy - r * .62),
                  rx='%.2f' % (r * 1.02), ry='%.2f' % (r * .78), fill='url(#vidro-brilho)')
    ET.SubElement(raiz, NS + 'circle', cx='%.2f' % cx, cy='%.2f' % cy, r='%.2f' % (r - .8),
                  fill='none', stroke='#ffffff', **{'stroke-opacity': '.85', 'stroke-width': '1.2'})
    ET.SubElement(raiz, NS + 'circle', cx='%.2f' % cx, cy='%.2f' % cy, r='%.2f' % (r - 2.2),
                  fill='none', stroke='#6f8fb3', **{'stroke-opacity': '.3', 'stroke-width': '.8'})

    txt = '<?xml version="1.0" encoding="UTF-8"?>\n' + ET.tostring(raiz, encoding='unicode') + '\n'
    for s in SAIDAS:
        open(s, 'w', encoding='utf-8', newline='\n').write(txt)
    print('selo de vidro: %d degrades, %d do passaro, %d formas creme -> %s' % (len(grad), len(ids_passaro), n, TINTA))
    for s in SAIDAS: print('  ->', s.split('Ideal Metrics/')[-1] if 'Ideal Metrics/' in s.replace('\\', '/') else s)


if __name__ == '__main__':
    main()
