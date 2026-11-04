# -*- coding: utf-8 -*-
"""04/11/2026, Leandro: «quero coloque estas secoes no spirit». Grava o catalogo que a aba Secoes do Spirit abre.

Saida: Ideal Metrics/ideal-metrics-spirit-secoes-dados.js, com o documento inteiro das secoes numa string, para rodar num
iframe sem depender do site: letras, CSS, imagens e scripts embutidos. Sem cabecalho, menu e rodape do site. Links relativos
vao para o site no ar, em aba nova (<base>). Chamado pelo monta.py, entao toda montagem da prancha atualiza o catalogo.
"""
import base64, json, re

MIME = {'.webp': 'image/webp', '.png': 'image/png', '.jpg': 'image/jpeg', '.svg': 'image/svg+xml'}
AJUSTES = """
html{scroll-behavior:auto}
.sm-acento{display:none}
.sm-sec{scroll-margin-top:0}
.sm-pg{--pg:max(600px,calc(100svh - 33px));scroll-margin-top:0}
.sm-sec[hidden]{display:none}
"""


def fontes(raiz):
    saida = []
    for bloco in re.findall(r'@font-face\s*\{.*?\}', (raiz / 'css' / 'fontes.css').read_text(encoding='utf-8'), flags=re.S):
        m = re.search(r'url\(\.\./(fonts/ibm-plex-(?:mono|sans-condensed)-\d+-latin\.woff2)\)', bloco)
        if m:
            b64 = base64.b64encode((raiz / m.group(1)).read_bytes()).decode('ascii')
            saida.append(bloco.replace(m.group(0), f'url(data:font/woff2;base64,{b64})'))
    return '\n'.join(saida)


def grava(secoes, cabeca, js, fams, raiz):
    def embute(mt):
        p = raiz / mt.group(2)
        b64 = base64.b64encode(p.read_bytes()).decode('ascii')
        return f'{mt.group(1)}="data:{MIME[p.suffix]};base64,{b64}"'
    corpo = re.sub(r'(src|data-lum)="(img/[^"?]+)(?:\?[^"]*)?"', embute, secoes)
    site = (raiz / 'css' / 'style.css').read_text(encoding='utf-8').replace("url('../img/CQT Sistemas da Qualidade.png')", 'none')
    estilos = ''.join(re.findall(r'<style[^>]*>.*?</style>', cabeca, flags=re.S))
    trama = (raiz / 'js' / 'trama.js').read_text(encoding='utf-8')
    doc = ('<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
           '<base href="https://idealmetrics.org/" target="_blank">'
           '<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:ital,wght@1,400&display=swap" rel="stylesheet">'
           f'<style>{fontes(raiz)}\n{site}</style>{estilos}<style>{AJUSTES}</style></head><body>{corpo}'
           f'<script>{trama}</script><script>{js}</script></body></html>')
    if re.search(r'(?:src|data-lum)="img/', doc):
        raise SystemExit('spirit: sobrou imagem por endereco relativo no catalogo')
    itens = [{'id': f'm{n:02d}', 'n': f'{n:02d}', 'f': f, 'nome': nome} for f, lista in fams.items() for n, nome in lista]
    itens.sort(key=lambda i: i['n'])
    dados = json.dumps({'itens': itens, 'doc': doc}, ensure_ascii=False, separators=(',', ':'))
    # o arquivo pode ir embutido num <script> na copia da Talita: nada aqui pode fechar a tag nem abrir comentario
    dados = dados.replace('</', '<\\/').replace('<!--', '<\\!--')
    destino = raiz.parent / 'ideal-metrics-spirit-secoes-dados.js'
    destino.write_text('/* gerado por ideal-metrics-site/_ferramentas/secoes-modelo/spirit.py; nao editar a mao */\nwindow.IM_SECOES = ' + dados + ';\n', encoding='utf-8')
    print('spirit:', destino.name, destino.stat().st_size // 1024, 'KB;', len(itens), 'secoes')
