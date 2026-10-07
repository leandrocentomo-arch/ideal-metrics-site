# -*- coding: utf-8 -*-
"""Prova de fonte: a pagina da ISO 45001 inteira em Geist (06/10/2026, pedido do Leandro).

Gera, sem tocar no original:
  _prova-geist-iso-45001.html   copia de norma-iso-45001.html
  css/_prova-geist-style.css    copia de css/style.css
com a familia trocada nos dois: IBM Plex Sans Condensed e IBM Plex Serif -> Geist, IBM Plex Mono -> Geist Mono.
As duas vem do Google Fonts como fontes variaveis (peso 100 a 900), entao todos os pesos que o site pede existem.
Refazer depois de mexer na pagina: python _ferramentas/prova_geist.py
"""
import re, pathlib

SITE = pathlib.Path(__file__).resolve().parent.parent
ORIG = SITE / 'norma-iso-45001.html'
PROVA = SITE / '_prova-geist-iso-45001.html'
CSS_ORIG = SITE / 'css' / 'style.css'
CSS_PROVA = SITE / 'css' / '_prova-geist-style.css'

FONTES = 'https://fonts.googleapis.com/css2?family=Geist:wght@100..900&family=Geist+Mono:wght@100..900&display=swap'
TROCA = [("IBM Plex Sans Condensed", "Geist"), ("IBM Plex Serif", "Geist"), ("IBM Plex Mono", "Geist Mono"),
         ("IBM Plex Sans", "Geist")]


def trocar(s):
    for a, b in TROCA:
        s = s.replace(a, b)
    return s


def main():
    with open(CSS_ORIG, encoding='utf-8', newline='') as f:
        css = f.read()
    css = '/* PROVA GEIST (06/10/2026): gerado por _ferramentas/prova_geist.py a partir de style.css; nao editar */\n' + trocar(css)
    # a Geist e mais larga que a Plex Condensed: no celular «26/05/2026» a 31 px pedia 207 px num cartao de 164
    css += '\n/* ajuste da prova: numero grande menor no celular */\n@media (max-width:520px){.vi-num b{font-size:23px}}\n'
    with open(CSS_PROVA, 'w', encoding='utf-8', newline='') as f:
        f.write(css)

    with open(ORIG, encoding='utf-8', newline='') as f:
        h = f.read()
    n0 = h.count('IBM Plex')
    h, k = re.subn(r'https://fonts\.googleapis\.com/css2\?family=IBM\+Plex[^"\']*', FONTES, h, count=1)
    assert k == 1, 'link do Google Fonts nao achado'
    h, k = re.subn(r'href="css/style\.css\?v=\d+"', 'href="css/_prova-geist-style.css?v=2"', h, count=1)
    assert k == 1, 'link do style.css nao achado'
    h = trocar(h)
    h = h.replace('<head>', '<head>\n<meta name="robots" content="noindex">', 1)
    h = re.sub(r'<title>', '<title>PROVA Geist · ', h, count=1)
    with open(PROVA, 'w', encoding='utf-8', newline='') as f:
        f.write(h)
    print('ok:', PROVA.name, '(%d citacoes de IBM Plex trocadas na pagina)' % n0, '+', CSS_PROVA.name)


if __name__ == '__main__':
    main()
