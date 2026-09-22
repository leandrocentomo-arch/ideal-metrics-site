# -*- coding: utf-8 -*-
"""O favicon do site: o passaro oficial sobre o VIDRO CREME do monograma do menu.

    python _ferramentas/favicon.py

22/09/2026, a pedido do Leandro: «a mesma textura usada no monograma, faca o
fundo do favicon, coloque o passaro novo». Ate entao o favicon era so o passaro,
sem fundo.

FUNDO. As mesmas tres camadas do cartao .barra-marca (index.html):
  degrade   #F9F9F6 -> #EEF0F0 -> #DCE3E9, na diagonal, claro no alto a esquerda
  reflexo   branco 72% -> 18% -> 0, de cima para baixo
  borda     fio branco 85% por dentro, mais um fio azul-tinta a 16% por fora,
            que no cartao e a linha --fio; sem ele o quadrado some na aba clara
Cantos arredondados (raio 14 em 100), como os icones de aba.

PASSARO. Os caminhos de img/passaro-ideal-m.svg (familia oficial 172 a 178,
com o ajuste do passaro), em #14304C, sem mudar nada no desenho: 84% da largura,
centrado.

SAIDA na raiz do site:
  favicon.svg            o vetor, que o navegador usa quando pode
  favicon-32.png         32 x 32, para quem nao le SVG
  apple-touch-icon.png   180 x 180, tela inicial do iPhone
Os PNG saem do proprio SVG, renderizados pelo Chromium do Playwright.
Nas paginas, os tres links levam ?v=<data> para a aba nao guardar o antigo."""

import os, re

SITE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PASSARO = os.path.join(SITE, 'img', 'passaro-ideal-m.svg')


def svg():
    fonte = open(PASSARO, encoding='utf-8').read()
    vb = [float(v) for v in re.search(r'viewBox="([^"]+)"', fonte).group(1).split()]
    corpo = re.search(r'<g id="Layer_1-2"[^>]*>(.*)</g>\s*</svg>', fonte, re.S).group(1).strip()
    esc = 84 / vb[2]
    alt = vb[3] * esc
    tx, ty = 8 - vb[0] * esc, (100 - alt) / 2 - vb[1] * esc
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">\n'
            '<defs>\n'
            '<linearGradient id="v" x1="0" y1="0" x2="1" y2="1">'
            '<stop offset="0" stop-color="#F9F9F6"/><stop offset=".5" stop-color="#EEF0F0"/>'
            '<stop offset="1" stop-color="#DCE3E9"/></linearGradient>\n'
            '<linearGradient id="r" x1="0" y1="0" x2="0" y2="1">'
            '<stop offset="0" stop-color="#fff" stop-opacity=".72"/>'
            '<stop offset=".55" stop-color="#fff" stop-opacity=".18"/>'
            '<stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>\n'
            '</defs>\n'
            '<rect x=".5" y=".5" width="99" height="99" rx="14" fill="url(#v)" stroke="#14304C" stroke-opacity=".16"/>\n'
            '<rect x=".5" y=".5" width="99" height="99" rx="14" fill="url(#r)"/>\n'
            '<rect x="2" y="2" width="96" height="96" rx="12.5" fill="none" stroke="#fff" stroke-opacity=".85"/>\n'
            '<g transform="translate(%.3f %.3f) scale(%.5f)">\n%s\n</g>\n</svg>\n'
            % (tx, ty, esc, corpo))


def png(fonte_svg):
    from playwright.sync_api import sync_playwright
    html = ('<html><body style="margin:0;background:transparent">'
            '<img id="i" src="data:image/svg+xml;base64,%s" style="display:block">'
            '</body></html>')
    import base64
    b64 = base64.b64encode(fonte_svg.encode('utf-8')).decode('ascii')
    with sync_playwright() as p:
        nav = p.chromium.launch(channel='chrome')
        for lado, nome in ((32, 'favicon-32.png'), (180, 'apple-touch-icon.png')):
            pg = nav.new_page(viewport={'width': lado, 'height': lado})
            pg.set_content(html % b64)
            pg.evaluate("s => { const i = document.getElementById('i'); i.width = s; i.height = s; }", lado)
            pg.wait_for_timeout(200)
            pg.locator('#i').screenshot(path=os.path.join(SITE, nome), omit_background=True)
            pg.close()
            print(nome, lado)
        nav.close()


def main():
    s = svg()
    open(os.path.join(SITE, 'favicon.svg'), 'w', encoding='utf-8', newline='\n').write(s)
    print('favicon.svg', len(s), 'bytes')
    png(s)


if __name__ == '__main__':
    main()
