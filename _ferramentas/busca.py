# -*- coding: utf-8 -*-
"""O indice da busca do site: busca-indice.json.

    python _ferramentas/busca.py

O Leandro pediu «um campo para busca no menu, uma super busca, qualquer tema»
(23/09/2026). O site e estatico e nao tem servidor para consultar, entao a busca
roda no navegador sobre um indice pronto, gerado aqui.

PARA CADA PAGINA publicada entram:
  t   titulo (a <h1> do banner; se faltar, o <title>)
  d   a chamada do banner, que serve de descricao no resultado
  h   os titulos internos (h2, h3, h4) e as etiquetas em <strong>, juntos
  c   o corpo em texto puro, cortado em 4000 caracteres
  u   o endereco

FICA DE FORA: index.html (a home ja e o destino de tudo), as paginas soltas
lp-carbono e stal, o painel de placas e a pagina de redirecionamento.
O JSON sai compacto, sem espacos, e hoje pesa cerca de 160 KB, e so baixa quando a pessoa digita."""

import json, os, re, subprocess

SITE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FORA = {'index.html', 'painel-placas.html', 'pegada-carbono.html'}


def texto(html):
    h = re.sub(r'(?is)<(script|style|nav|footer|header)[^>]*>.*?</\1>', ' ', html)
    h = re.sub(r'(?is)<div class="tarja".*?</div>', ' ', h)
    h = re.sub(r'(?s)<[^>]+>', ' ', h)
    h = (h.replace('&nbsp;', ' ').replace('&amp;', '&').replace('&ccedil;', 'ç').replace('&atilde;', 'ã')
          .replace('&otilde;', 'õ').replace('&aacute;', 'á').replace('&eacute;', 'é').replace('&oacute;', 'ó')
          .replace('&uacute;', 'ú').replace('&iacute;', 'í').replace('&ecirc;', 'ê').replace('&ocirc;', 'ô')
          .replace('&acirc;', 'â').replace('&middot;', '·').replace('&gt;', '>').replace('&lt;', '<'))
    return re.sub(r'\s+', ' ', h).strip()


def pagina(caminho):
    html = open(os.path.join(SITE, caminho), encoding='utf-8').read()
    m = re.search(r'(?is)<div class="page-banner"[^>]*>\s*<h1>(.*?)</h1>\s*<p>(.*?)</p>', html)
    if m:
        t, d = texto(m.group(1)), texto(m.group(2))
    else:
        t = texto(re.search(r'(?is)<title>(.*?)</title>', html).group(1)).split('|')[0].strip()
        d = ''
    corpo = html[html.index('<div class="content">'):] if '<div class="content">' in html else html
    titulos = [texto(x) for x in re.findall(r'(?is)<h[234][^>]*>(.*?)</h[234]>', corpo)]
    fortes = [texto(x) for x in re.findall(r'(?is)<strong>(.*?)</strong>', corpo)]
    c = texto(corpo)
    return {'u': caminho, 't': t, 'd': d,
            'h': ' · '.join(dict.fromkeys(x for x in titulos + fortes if x))[:600],
            'c': c[:4000]}


def main():
    saida = subprocess.run(['git', 'ls-files', '*.html'], cwd=SITE, capture_output=True, text=True).stdout
    paginas = [p for p in saida.split('\n') if p and '/' not in p and p not in FORA]
    indice = [pagina(p) for p in sorted(paginas)]
    dst = os.path.join(SITE, 'busca-indice.json')
    open(dst, 'w', encoding='utf-8').write(json.dumps(indice, ensure_ascii=False, separators=(',', ':')))
    print('busca-indice.json: %d paginas, %.1f KB' % (len(indice), os.path.getsize(dst) / 1024))


if __name__ == '__main__':
    main()
