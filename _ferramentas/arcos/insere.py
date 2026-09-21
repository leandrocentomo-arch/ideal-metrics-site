# -*- coding: utf-8 -*-
"""Insere a secao «Conhecimento» no index.html do site, de forma IDEMPOTENTE:
rodar duas vezes troca a versao anterior pela nova, sem duplicar nada.

Tres pecas, tres ancoras:
  CSS   antes da regra `.sv{display:grid;` (a secao Servicos), entre marcadores
  HTML  antes de <section class="sv" id="servicos">
  JS    antes de </body>

A secao nova e a [ IM.2 ]; Servicos passa a [ IM.3 ].
O fim de linha do arquivo e preservado (o index e CRLF)."""

import re

SITE = ("C:/Users/Leandro Centomo/OneDrive/\u00c1rea de Trabalho/CQT\u2014Inbox\u2014Fast/"
        "Primeiro-Vault/Ideal Metrics/ideal-metrics-site/")
FIM_CSS = '/* ===== fim CONHECIMENTO ===== */'


def no_site(css, secao, js, motor=''):
    p = SITE + 'index.html'
    raw = open(p, 'rb').read()
    crlf, lf = raw.count(b'\r\n'), raw.count(b'\n')
    assert crlf in (0, lf), 'fim de linha misturado'
    eol = '\r\n' if crlf else '\n'
    t = raw.decode('utf-8').replace('\r\n', '\n')

    # tira a versao anterior, se houver
    t = re.sub(r'/\* ===== CONHECIMENTO, .*?' + re.escape(FIM_CSS) + r'\n', '', t, flags=re.S)
    t = re.sub(r'<section class="ar-sec" id="conhecimento".*?</section>\n\n', '', t, flags=re.S)
    t = re.sub(r'<script>\n/\* CONHECIMENTO: .*?</script>\n', '', t, flags=re.S)

    ancora_css = '.sv{display:grid;'
    assert t.count(ancora_css) == 1, 'ancora do CSS: %d' % t.count(ancora_css)
    t = t.replace(ancora_css, css.strip('\n') + '\n' + FIM_CSS + '\n' + ancora_css, 1)

    ancora_html = '<section class="sv" id="servicos" aria-labelledby="sv-h2">'
    assert t.count(ancora_html) == 1
    t = t.replace(ancora_html, secao + '\n\n' + ancora_html, 1)

    # sem script (a profundidade por rolagem saiu em 21/09) nada entra: senao
    # cada rodada deixaria uma linha em branco a mais antes de </body>
    if js.strip():
        assert t.count('</body>') == 1
        t = t.replace('</body>', js.strip('\n') + '\n</body>', 1)

    # o motor das manchas entra dentro do IIFE do ditherVivo, antes da moldura
    # de noticias, entre marcadores proprios
    t = re.sub(r'  /\* -+ CONHECIMENTO: as manchas.*?fim CONHECIMENTO manchas -+ \*/\n', '', t, flags=re.S)
    if motor:
        ancora = '  /* ---------------- a moldura de noticias'
        assert t.count(ancora) == 1, 'ancora do motor: %d' % t.count(ancora)
        t = t.replace(ancora, motor + ancora, 1)

    if 'Serviços / [ IM.2 ]' in t:
        t = t.replace('Serviços / [ IM.2 ]', 'Serviços / [ IM.3 ]', 1)

    assert '\r' not in t
    open(p, 'wb').write(t.replace('\n', eol).encode('utf-8'))
    print('index.html: secao Conhecimento antes de Servicos; Servicos e a IM.3')
