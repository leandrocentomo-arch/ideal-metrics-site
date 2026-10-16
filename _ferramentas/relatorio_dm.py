# -*- coding: utf-8 -*-
"""A FOLHA DO PAINEL DEMANDAS (15/10/2026): um relatorio de auditoria «fotografado» e tramado.

    python _ferramentas/relatorio_dm.py

Historia: a folha era um desenho geometrico tramado (gera-folha.py, 19/09); em 15/10 virou um relatorio em vetor
com as letras do site, e o Leandro respondeu «ficou feio, o conteudo deve ser ilegivel, talvez uma foto». Daqui sai a
foto: a pagina do relatorio (estrutura real: cabecalho, indicadores, conformidade por clausula, plano de acao) e
desenhada em SVG com as letras do site, renderizada a 3x, tratada como foto de perto (luz caindo para a direita e para
baixo, foco que se perde para a base) e tramada no TINGIMENTO OFICIAL. O texto fica ilegivel de proposito; os numeros
sao ilustrativos.

Saidas:
  Ideal Metrics/_tingir-fotos/FOTOS/relatorio-auditoria-render.png   o «cru» (a pagina limpa, 900 x 1170)
  img/relatorio-01-lum-dm.webp     a luminancia que o motor trama ao vivo (data-lum)
  img/relatorio-01-bayer-dm.webp   a versao ja tramada (vale sem WebGL, em file:// e no telefone)
A vaga: a caixa da folha no desenho do painel, 300 x 390 (x 190, y 300 do viewBox 1108 x 680)."""
import os, sys
import numpy as np
from PIL import Image, ImageFilter

SITE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IM = os.path.dirname(SITE)
CRU = os.path.join(IM, '_tingir-fotos', 'FOTOS', 'relatorio-auditoria-render.png')
LUM = os.path.join(SITE, 'img', 'relatorio-01-lum-dm.webp')
BAY = os.path.join(SITE, 'img', 'relatorio-01-bayer-dm.webp')
W, H, ESC = 300, 390, 3

L, R = 18, 282
CLAUS = [('4', 'Contexto da organização', 100), ('5', 'Liderança', 100), ('6', 'Planejamento', 86), ('7', 'Apoio', 93),
         ('8', 'Operação', 78), ('9', 'Avaliação de desempenho', 95), ('10', 'Melhoria', 89)]
ACOES = [('nc', 'NC 01 · 8.5.1 Controle da produção', '30 NOV'), ('obs', 'OBS 03 · 6.1 Riscos e oportunidades', '15 DEZ'),
         ('obs', 'OBS 04 · 7.2 Competência', '15 DEZ'), ('obs', 'OBS 05 · 9.1.2 Satisfação do cliente', '20 DEZ')]


def pagina():
    o = ['<text class="mono" x="%d" y="23">RELATÓRIO DE AUDITORIA INTERNA</text>' % L,
         '<text class="mono" x="%d" y="23" text-anchor="end">REV. 02</text>' % R,
         '<path class="fio" d="M%d 32.5H%d"/>' % (L, R),
         '<text class="tit" x="%d" y="55">Sistema de gestão da qualidade</text>' % L,
         '<text class="sub" x="%d" y="70">ISO 9001:2015 · ciclo 2026</text>' % L]
    for x, n, rot in ((L, '142', 'REQUISITOS'), (112, '131', 'CONFORMES'), (206, '11', 'AÇÕES ABERTAS')):
        o.append('<text class="num" x="%d" y="104">%s</text><text class="mono" x="%d" y="117">%s</text>' % (x, n, x, rot))
    o.append('<path class="fio" d="M101.5 86V119M195.5 86V119M%d 131.5H%d"/>' % (L, R))
    o.append('<text class="mono" x="%d" y="150">CONFORMIDADE POR CLÁUSULA</text>' % L)
    y0, h, x0, w = 158, 21, 176, 74
    for i, (n, nome, pct) in enumerate(CLAUS):
        yb, ym = y0 + i * h + 13.5, y0 + i * h + 10.5
        o.append('<text class="mono" x="%d" y="%.1f">%s</text><text class="txt" x="34" y="%.1f">%s</text>' % (L, yb, n, yb, nome))
        o.append('<rect class="trilho" x="%d" y="%.1f" width="%d" height="4" rx="1"/><rect class="barra%s" x="%d" y="%.1f" '
                 'width="%.1f" height="4" rx="1"/><text class="mono" x="%d" y="%.1f" text-anchor="end">%d%%</text>'
                 % (x0, ym - 2, w, ' baixa' if pct < 90 else '', x0, ym - 2, w * pct / 100, R, yb, pct))
        o.append('<path class="fio leve" d="M%d %.1fH%d"/>' % (L, y0 + (i + 1) * h + .5, R))
    o.append('<text class="mono" x="%d" y="328">PLANO DE AÇÃO</text>' % L)
    for k, (cls, txt, prazo) in enumerate(ACOES):
        y = 345 + k * 18
        o.append('<rect class="%s" x="%d" y="%.1f" width="7" height="7" rx="1.5"/><text class="txt" x="31" y="%d">%s</text>'
                 '<text class="mono" x="%d" y="%d" text-anchor="end">%s</text>' % (cls, L, y - 6.5, y, txt, R, y, prazo))
    return '\n'.join(o)


HTML = """<!doctype html><html><head><meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Condensed:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500&display=block" rel="stylesheet">
<style>html,body{margin:0;background:#fff}svg{display:block}
.mono{font-family:'IBM Plex Mono',monospace;font-size:7.2px;letter-spacing:.12em;fill:#14304C}
.tit{font-family:'IBM Plex Sans Condensed',sans-serif;font-weight:600;font-size:15px;fill:#14304C}
.sub{font-family:'IBM Plex Sans Condensed',sans-serif;font-size:9.6px;fill:#315275}
.num{font-family:'IBM Plex Sans Condensed',sans-serif;font-weight:600;font-size:20px;fill:#14304C}
.txt{font-family:'IBM Plex Sans Condensed',sans-serif;font-weight:500;font-size:9.6px;fill:#14304C}
.fio{fill:none;stroke:rgba(20,48,76,.22);stroke-width:1}.fio.leve{stroke:rgba(20,48,76,.12)}
.trilho{fill:rgba(20,48,76,.10)}.barra{fill:#14304C}.barra.baixa{fill:#336699}
.nc{fill:#EF4545}.obs{fill:#336699;fill-opacity:.5}</style></head>
<body><svg width="%d" height="%d" viewBox="0 0 %d %d">%s</svg></body></html>"""


def renderiza():
    from playwright.sync_api import sync_playwright
    with sync_playwright() as pw:
        b = pw.chromium.launch()
        pg = b.new_page(viewport={'width': W, 'height': H}, device_scale_factor=ESC)
        pg.set_content(HTML % (W, H, W, H, pagina()), wait_until='networkidle')
        pg.evaluate('document.fonts.ready'); pg.wait_for_timeout(400)
        pg.screenshot(path=CRU, clip={'x': 0, 'y': 0, 'width': W, 'height': H})
        b.close()


# o desfoque (em px do cru a 3x) e o ganho de tinta: medidos em 15/10/2026 contra o tingimento oficial, que clareia
# (+0,35): sem o ganho, o texto miudo e os fios sumiam e a folha ficava vazia; com desfoque menor, titulo e numeros
# ainda se liam
DESFOCO_TOPO, DESFOCO_BASE, TINTA, LUZ = 6.0, 10.0, 4.2, .09


def foto(im):
    """a pagina limpa vira «foto de perto»: o texto desfocado vira mancha de tinta (ilegivel, mas a estrutura da
    pagina continua lendo como relatorio), o foco se perde para a base e a luz cai para a direita e para baixo"""
    im = im.convert('RGB'); w, h = im.size
    tinta = Image.fromarray((255 - np.asarray(im)).astype(np.uint8))
    perto = np.asarray(tinta.filter(ImageFilter.GaussianBlur(DESFOCO_TOPO)), np.float32) / 255
    longe = np.asarray(tinta.filter(ImageFilter.GaussianBlur(DESFOCO_BASE)), np.float32) / 255
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    t = np.clip((yy / h - .3) / .7, 0, 1); t = t * t * (3 - 2 * t)            # o foco se perde do meio para a base
    d = np.clip((perto * (1 - t[..., None]) + longe * t[..., None]) * TINTA, 0, 1)
    luz = 1 - LUZ * (.45 * xx / w + .55 * yy / h)                               # luz caindo para a direita e para baixo
    return Image.fromarray(np.clip((1 - d) * luz[..., None] * 255, 0, 255).astype(np.uint8), 'RGB')


# 15/10/2026, noite: a foto do Google Flow (o Leandro gerou: «Audit report on desk»), no lugar do desenho «fotografado»,
# que «nao esta legal». Recorte com um pouco da mesa nos cantos; correcao de exposicao SO desta foto (o papel cinza-claro
# virava creme no tingimento e so as barras sobravam): niveis 80 a 240 e gama 2,6; e um desfoque a mais para os numeros
# grandes nao se lerem. Nao e outro tingimento: depois disso entra o oficial.
FLOW = os.path.join(IM, '_tingir-fotos', 'FOTOS', 'Audit_report_on_desk_20261015225448.jpg')
FLOW_CORTE, FLOW_NIVEIS, FLOW_GAMA, FLOW_DESFOCO = (250, 0, 939, 896), (80, 240), 2.6, 2.5
LUM2 = os.path.join(SITE, 'img', 'relatorio-02-lum-dm.webp')
BAY2 = os.path.join(SITE, 'img', 'relatorio-02-bayer-dm.webp')


def da_foto():
    a = np.asarray(Image.open(FLOW).convert('RGB').crop(FLOW_CORTE), np.float32)
    bp, wp = FLOW_NIVEIS
    a = np.clip((a - bp) / (wp - bp), 0, 1) ** FLOW_GAMA
    im = Image.fromarray((a * 255).astype(np.uint8), 'RGB').resize((W * ESC, H * ESC), Image.LANCZOS)
    return im.filter(ImageFilter.GaussianBlur(FLOW_DESFOCO))


# 15/10/2026, noite: «acho que devemos voltar para um desenho abstrato mesmo» e, em seguida, «mas tem que ser na trama
# azul». A pagina do relatorio SEM letras (cada texto e um traco na largura que teria), desenhada aqui, renderizada a 3x
# e tramada no TINGIMENTO OFICIAL, como as fotos (relatorio-03). Os tons saem mais fortes que no vetor (.85/.42/.20 la)
# porque o tingimento clareia +0,35: com os do vetor os tracos claros sumiam.
CRU3 = os.path.join(IM, '_tingir-fotos', 'FOTOS', 'relatorio-abstrato-render.png')
LUM3 = os.path.join(SITE, 'img', 'relatorio-03-lum-dm.webp')
BAY3 = os.path.join(SITE, 'img', 'relatorio-03-bayer-dm.webp')
ABS_T1, ABS_T2, ABS_T3, ABS_FIO, ABS_GAMA = 1.0, .75, .48, .45, 1.6
# «nao queria o fim cortado»: a pagina inteira dentro do painel. 300 x 375 (era 300 x 390 cortada pela base), no desenho
# do painel em x 190, y 275 (termina em 650, 30 acima da base do painel, que e 680)
ABS_H = 375


def abstrato():
    o = ['<rect class="t2" x="%d" y="19" width="104" height="3" rx="1"/><rect class="t2" x="%d" y="19" width="22" height="3" rx="1"/>' % (L, R - 22),
         '<path class="fio" d="M%d 32.5H%d"/>' % (L, R),
         '<rect class="t1" x="%d" y="45" width="148" height="8" rx="1.5"/>' % L,
         '<rect class="t3" x="%d" y="62" width="92" height="4" rx="1"/>' % L]
    for x, w, wl in ((L, 34, 44), (112, 34, 40), (206, 22, 56)):
        o.append('<rect class="t1" x="%d" y="84" width="%d" height="14" rx="2"/><rect class="t3" x="%d" y="106" width="%d" height="3" rx="1"/>' % (x, w, x, wl))
    o.append('<path class="fio" d="M101.5 82V115M195.5 82V115M%d 127.5H%d"/>' % (L, R))
    o.append('<rect class="t2" x="%d" y="141" width="98" height="3" rx="1"/>' % L)
    rot, pct = (92, 46, 62, 30, 44, 104, 50), (100, 100, 86, 93, 78, 95, 89)
    y0, h, x0, w = 151, 19, 176, 74
    for i in range(7):
        ym = y0 + i * h + 9.5
        o.append('<rect class="t3" x="%d" y="%.1f" width="6" height="3" rx="1"/><rect class="t3" x="34" y="%.1f" width="%d" height="4" rx="1"/>'
                 % (L, ym - 1.5, ym - 2, rot[i]))
        o.append('<rect class="trilho" x="%d" y="%.1f" width="%d" height="4" rx="1"/><rect class="%s" x="%d" y="%.1f" width="%.1f" height="4" rx="1"/>'
                 '<rect class="t3" x="%d" y="%.1f" width="14" height="3" rx="1"/>'
                 % (x0, ym - 2, w, 'baixa' if pct[i] < 90 else 't1', x0, ym - 2, w * pct[i] / 100, R - 14, ym - 1.5))
        o.append('<path class="fio leve" d="M%d %.1fH%d"/>' % (L, y0 + (i + 1) * h + .5, R))
    o.append('<rect class="t2" x="%d" y="300" width="58" height="3" rx="1"/>' % L)
    for k, (cls, wt) in enumerate((('nc', 132), ('obs', 146), ('obs', 96))):
        y = 314 + k * 16
        o.append('<rect class="%s" x="%d" y="%d" width="7" height="7" rx="1.5"/><rect class="t3" x="31" y="%.1f" width="%d" height="4" rx="1"/>'
                 '<rect class="t3" x="%d" y="%.1f" width="22" height="3" rx="1"/>' % (cls, L, y, y + 1.5, wt, R - 22, y + 2))
    estilo = ('.t1{fill:#14304C;fill-opacity:%s}.t2{fill:#14304C;fill-opacity:%s}.t3{fill:#14304C;fill-opacity:%s}'
              '.fio{fill:none;stroke:#14304C;stroke-opacity:%s;stroke-width:1}.fio.leve{stroke-opacity:%s}'
              '.trilho{fill:#14304C;fill-opacity:.12}.baixa{fill:#336699}.nc{fill:#14304C}.obs{fill:#336699;fill-opacity:.7}'
              % (ABS_T1, ABS_T2, ABS_T3, ABS_FIO, ABS_FIO * .6))
    html = ('<!doctype html><html><head><meta charset="utf-8"><style>html,body{margin:0;background:#fff}svg{display:block}%s</style></head>'
            '<body><svg width="%d" height="%d" viewBox="0 0 %d %d">%s</svg></body></html>' % (estilo, W, ABS_H, W, ABS_H, '\n'.join(o)))
    from playwright.sync_api import sync_playwright
    with sync_playwright() as pw:
        b = pw.chromium.launch()
        pg = b.new_page(viewport={'width': W, 'height': ABS_H}, device_scale_factor=ESC)
        pg.set_content(html); pg.wait_for_timeout(200)
        pg.screenshot(path=CRU3, clip={'x': 0, 'y': 0, 'width': W, 'height': ABS_H})
        b.close()
    a = np.asarray(Image.open(CRU3).convert('RGB'), np.float32) / 255
    return Image.fromarray((np.clip(a, 0, 1) ** ABS_GAMA * 255).astype(np.uint8), 'RGB')


def main():
    sys.path.insert(0, os.path.join(IM, '_tingir-fotos'))
    import tingir
    if '--flow' not in sys.argv and '--desenho' not in sys.argv:   # o desenho abstrato tramado (relatorio-03), o que vale
        lum = abstrato()
        lum.save(LUM3, 'WEBP', quality=92)
        tingir.bayer(lum, largura=W).save(BAY3, 'WEBP', lossless=True)
        print('lum:', LUM3, lum.size); print('bayer:', BAY3, Image.open(BAY3).size)
        return
    if '--desenho' in sys.argv:   # o desenho «fotografado» das 21h (relatorio-01), guardado
        if '--sem-render' not in sys.argv or not os.path.exists(CRU):
            renderiza()
        lum, lp, bp = foto(Image.open(CRU)), LUM, BAY
    else:                         # a foto do Flow (relatorio-02), a que vale
        lum, lp, bp = da_foto(), LUM2, BAY2
    lum.save(lp, 'WEBP', quality=90)
    tingir.bayer(lum, largura=W).save(bp, 'WEBP', lossless=True)
    print('lum:', lp, lum.size); print('bayer:', bp, Image.open(bp).size)


if __name__ == '__main__':
    main()
