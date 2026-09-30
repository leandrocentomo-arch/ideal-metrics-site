# -*- coding: utf-8 -*-
"""A PAGINA AZUL (index-azul.html) sai da home atual (30/09/2026).

    python _ferramentas/pagina_azul.py

«Os ajustes que fizer aqui, faca tambem, identicos, para o site com as fotos azuis.» A
index-azul.html (so no disco, no .gitignore) e a index.html com todas as fotos no TINGIMENTO
OFICIAL AZUL. Em vez de editar as duas a mao, esta ferramenta gera a azul a partir da home:

  1. as trocas de linha de _ferramentas/pagina_azul_pares.json (Servicos, Diferenciais,
     Setores e noticias: arquivos -cor- para -bayer-/-lum-, chamadas sem emCor), tiradas da
     primeira versao da pagina azul, montada e conferida em 30/09;
  2. a tira: reservas tira-<servico>-bayer.webp e textura tira-panorama-lum.webp (as duas do
     _ferramentas/panorama_azul.py) e a chamada do motor no modo azul (sem emCor, veu .12);
  3. titulo «(azul)» e o comentario no topo.

Ordem para refazer tudo: panorama.py -> panorama_azul.py -> pagina_azul.py. Uma troca que nao
achar a linha e avisada (a home mudou ali; rever o par)."""
import os, re, json
SITE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
s = open(os.path.join(SITE, 'index.html'), encoding='utf-8').read()
pares = json.load(open(os.path.join(SITE, '_ferramentas', 'pagina_azul_pares.json'), encoding='utf-8'))
falhas = 0
for p in pares:
    if 'inserir_depois_de' in p:
        ancora = p['inserir_depois_de'] + '\n'
        if s.count(ancora) != 1: print('AVISO: ancora do comentario nao achada'); falhas += 1; continue
        s = s.replace(ancora, ancora + '\n'.join(p['linhas']) + '\n', 1); continue
    de, para = '\n'.join(p['de']), '\n'.join(p['para'])
    if de.strip() == 'zoomHover:1.03}));':              # so o da chamada das noticias
        i = s.find("classeCanvas:'nt-gl'")
        j = s.find(de, i)
        if i < 0 or j < 0: print('AVISO: fecho da chamada das noticias'); falhas += 1; continue
        s = s[:j] + para + s[j + len(de):]; continue
    n = s.count(de)
    if n == 0: print('AVISO: linha nao achada:', p['de'][0][:90]); falhas += 1; continue
    s = s.replace(de, para, 1)
# a tira
s, n1 = re.subn(r'img/tira-(carbono|iso|smeta|esg)-cor-bayer\.webp\?v=([0-9a-z]+)', r'img/tira-\1-bayer.webp?v=\2', s)
s, n2 = re.subn(r'data-lum="img/tira-panorama-cor\.webp\?v=([0-9a-z]+)"', r'data-lum="img/tira-panorama-lum.webp?v=\1"', s)
i = s.find('pecaTira = ditherVivo(ditherVivo.emCor({')
j = s.find('}));', i)
if i < 0 or j < 0: print('AVISO: chamada da tira'); falhas += 1
else:
    bloco = s[i:j + 4]
    novo = bloco.replace('ditherVivo(ditherVivo.emCor({', 'ditherVivo({', 1)
    # 30/09 (noite): «um tom a mais de escuro, esta estourado; antes havia texto sobre as fotos,
    # agora nao ha»: brilho do tom .20 (o oficial e .35) e sem o veu creme de repouso (era .12)
    novo = novo.replace('lavaHover:.88', 'brilhoTom:.20, lavaRepouso:0, lavaHover:.88', 1)
    novo = novo[:-4] + '});'
    s = s[:i] + novo + s[j + 4:]
open(os.path.join(SITE, 'index-azul.html'), 'w', encoding='utf-8', newline='\n').write(s)
print('index-azul.html: %d trocas, tira %d/%d arquivos, %d avisos' % (len(pares), n1, n2, falhas))
