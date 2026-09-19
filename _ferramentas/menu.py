# -*- coding: utf-8 -*-
"""Regrava o menu, a navegacao lateral e as colunas do rodape em todas as paginas.

O site nao tem gerador: esses tres blocos sao copiados pagina a pagina. A fonte
unica deles e o blocos.py, ao lado deste arquivo. Para incluir, tirar ou renomear
uma pagina no menu: editar MENU, LATERAL e RODAPE no blocos.py e rodar

    python _ferramentas/menu.py

Pode rodar quantas vezes quiser: o resultado e sempre o mesmo. As paginas de
laboratorio (index-*, painel-placas) e a home, que tem menu proprio, ficam de fora."""
import glob, os, re
import blocos as B

LAB = re.compile(r'^(index-.*|painel-placas)\.html$')
n = 0
for p in sorted(glob.glob(B.SITE + '*.html')):
    f = os.path.basename(p)
    if LAB.match(f) or f == 'index.html': continue
    s = B.ler(f); antes = s
    if B.RE_MEGA.search(s):  s = B.RE_MEGA.sub(lambda m: B.mega(), s, count=1)
    if B.RE_LAT.search(s):   s = B.RE_LAT.sub(lambda m, f=f: B.lateral(f), s, count=1)
    if B.RE_FT_AB.search(s): s = B.RE_FT_AB.sub(lambda m: B.rodape_colunas(), s, count=1)
    if s != antes: B.gravar(f, s); n += 1
print('%d pagina(s) regravada(s)' % n)
