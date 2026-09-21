# -*- coding: utf-8 -*-
"""A barra de topo da HOME em todas as paginas internas.

    python _ferramentas/barra.py

O Leandro pediu o cabecalho igual em todas as paginas (21/09/2026). Ate entao
as internas tinham um cabecalho proprio (.header, com o mega-menu «Todos os
servicos») e uma tarja vermelha; a home tem a tarja creme com a data mais a
.barra (monograma solto, seis links, botao Menu que abre o veu).

O QUE ESTE SCRIPT FAZ, em cada pagina interna:
  1. troca o bloco <div class="tarja">...</header> pelo bloco da home (tarja,
     barra, veu-menu), lido do proprio index.html: a home continua a fonte;
  2. poe um espacador de 92px (26 da tarja + 66 da barra, as duas fixas) no
     lugar do cabecalho, que era estatico;
  3. garante o <script src="js/barra.js"> antes de </body>.
E, uma vez: extrai do index.html o CSS da tarja/barra/veu para css/style.css
(entre marcadores; apaga as regras antigas .tarja de la) e o JS para js/barra.js.

Idempotente: rodar de novo so reescreve com o que estiver na home.
O mega-menu sai do cabecalho; os 14 temas seguem no rodape e na navegacao
lateral, que blocos.py continua gerando."""

import os, re, glob

SITE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INI, FIM = '/* ===== BARRA DA HOME (gerado por _ferramentas/barra.py) ===== */', '/* ===== fim BARRA DA HOME ===== */'
_EOL = {}


def ler(p):
    raw = open(p, 'rb').read()
    crlf, lf = raw.count(b'\r\n'), raw.count(b'\n')
    assert crlf in (0, lf), p + ': fim de linha misturado'
    _EOL[p] = '\r\n' if crlf else '\n'
    return raw.decode('utf-8').replace('\r\n', '\n')


def gravar(p, s):
    assert '\r' not in s
    open(p, 'wb').write(s.replace('\n', _EOL.get(p, '\r\n')).encode('utf-8'))


def bloco_css(home):
    """as regras da tarja, barra e veu, copiadas da home"""
    linhas = home.split('\n')
    def faixa(ini_re, fim_re):
        a = next(i for i, l in enumerate(linhas) if re.match(ini_re, l))
        b = next(i for i in range(a + 1, len(linhas)) if re.match(fim_re, linhas[i]))
        return '\n'.join(linhas[a:b])
    veu = faixa(r'\.veu-menu\{', r'\.veu-menu \.selo-mono\{')
    # a regra .selo-mono ocupa duas linhas: leva ate fechar a chave, senao a
    # chave aberta engole o resto da folha (foi o que aconteceu na 1a rodada)
    i = next(i for i, l in enumerate(linhas) if l.startswith('.veu-menu .selo-mono{'))
    j = i
    while sum(l.count('{') - l.count('}') for l in linhas[i:j + 1]) > 0: j += 1
    veu += '\n' + '\n'.join(linhas[i:j + 1])
    a = next(i for i, l in enumerate(linhas) if l.startswith('.tarja{position'))
    b = next(i for i in range(a, len(linhas)) if linhas[i].startswith('@media (max-width') and '.barra-nav' in linhas[i] or linhas[i].startswith('@media (max-width:880px){ .barra'))
    # ate a ultima @media da barra (tres seguidas)
    while b + 1 < len(linhas) and linhas[b + 1].startswith('@media') and 'barra' in linhas[b + 1]: b += 1
    # e ate a ultima FECHAR: na home ela continua nas linhas seguintes
    while sum(l.count('{') - l.count('}') for l in linhas[a:b + 1]) > 0: b += 1
    barra = '\n'.join(linhas[a:b + 1])
    assert barra.count('{') == barra.count('}') and veu.count('{') == veu.count('}')
    return veu + '\n' + barra


def bloco_html(home):
    a = home.index('<div class="tarja" role="note">')
    b = home.index('</nav>', home.index('<nav class="veu-menu"')) + len('</nav>')
    return home[a:b]


def bloco_js(home):
    def entre(ini, fim):
        a = home.index(ini); b = home.index(fim, a)
        return home[a:b]
    scramble = entre('// scramble do modelo', '// cursor')
    rolou = entre('// ===== a placa da marca encolhe ao rolar =====', '})();') + '})();'
    tarja = re.search(r'/\* tarja: data do dia.*?\}\)\(\);', home).group(0)
    return ('/* barra da home nas paginas internas. Gerado por _ferramentas/barra.py a\n'
            '   partir do index.html: a home continua a fonte. */\n' + scramble + rolou + '\n' + tarja + '\n')


def main():
    home = ler(os.path.join(SITE, 'index.html'))
    css, html, js = bloco_css(home), bloco_html(home), bloco_js(home)
    assert '.barra{position:fixed' in css and '.veu-menu{' in css and '.tarja{position:fixed' in css
    assert 'id="abreMenu2"' in html and 'veuMenu' in html

    # css/style.css: tira as regras antigas da tarja vermelha, poe o bloco da home
    p = os.path.join(SITE, 'css', 'style.css'); s = ler(p)
    s = re.sub(re.escape(INI) + r'.*?' + re.escape(FIM) + r'\n?', '', s, flags=re.S)
    s = re.sub(r'\.tarja \{.*?\n\}\n\.tarja span \{.*?\n\}\n@media \(max-width: 768px\) \{\n  \.tarja[^\n]*\n  \.tarja span[^\n]*\n\}\n', '', s, flags=re.S)
    s = s.rstrip('\n') + '\n\n' + INI + '\n' + css + '\n.barra-espaco{height:92px}\n' + FIM + '\n'
    gravar(p, s); print('css/style.css: bloco da barra da home')

    os.makedirs(os.path.join(SITE, 'js'), exist_ok=True)
    p = os.path.join(SITE, 'js', 'barra.js'); _EOL[p] = '\n'; gravar(p, js); print('js/barra.js')

    n = 0
    for p in sorted(glob.glob(os.path.join(SITE, '*.html'))):
        nome = os.path.basename(p)
        if nome == 'index.html' or nome.startswith('index-'): continue
        s = ler(p)
        m = re.search(r'<div class="tarja"(?: role="note")?>.*?</header>(?:\n<nav class="veu-menu".*?</nav>)?(?:\n<div class="barra-espaco"[^>]*></div>)?', s, flags=re.S)
        if not m: print('  pulada (sem cabecalho reconhecido):', nome); continue
        s = s[:m.start()] + html + '\n<div class="barra-espaco" aria-hidden="true"></div>' + s[m.end():]
        if 'js/barra.js' not in s:
            assert s.count('</body>') == 1
            s = s.replace('</body>', '<script src="js/barra.js"></script>\n</body>', 1)
        gravar(p, s); n += 1
    print('%d paginas com a barra da home' % n)


if __name__ == '__main__':
    main()
