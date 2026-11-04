"""30 modelos de secao para avaliacao (03/11/2026): monta _prova-secoes-modelo.html, com a casca de norma-iso-45001.html.

O arquivo final e prancha local: casa com _prova-*.html no .gitignore e nao sobe. Rodar da raiz do site:
python _ferramentas/secoes-modelo/monta.py
Falha se houver numero de norma sem ISO antes (regra do Leandro) ou imagem que nao existe."""
import pathlib, re, sys

RAIZ = pathlib.Path(__file__).resolve().parents[2]
AQUI = pathlib.Path(__file__).resolve().parent
src = (RAIZ / 'norma-iso-45001.html').read_text(encoding='utf-8')
home = (RAIZ / 'index.html').read_text(encoding='utf-8')
secoes = (AQUI / 'secoes.html').read_text(encoding='utf-8')
css = (AQUI / 'estilo.css').read_text(encoding='utf-8')
js = (AQUI / 'motor.js').read_text(encoding='utf-8')

def acha(marca, texto=src):
    i = texto.find(marca)
    if i < 0: sys.exit(f'marcador nao encontrado: {marca!r}')
    return i

# ----- pecas calculadas
ETAPAS = [('Diagnóstico', 'operação comparada', 'à norma'), ('Plano diretor', 'prazo, líderes de', 'processos e capacitação'),
          ('Implantação', 'processos, indicadores', 'e procedimentos'), ('Auditoria interna', 'e análise crítica', 'pela direção'),
          ('Organização pronta', 'para a certificação', 'ISO 9001:2026')]
etapas = ''
for i, (t, a, b) in enumerate(ETAPAS):
    x = 90 + i * 180
    etapas += (f'<circle class="ifc-aro ifc-aro--f" cx="{x}" cy="66" r="13"/><circle cx="{x}" cy="66" r="3.5" fill="#14304C"/>'
               f'<text class="ifc-svg-n" x="{x}" y="38">0{i+1}</text><text class="ifc-svg-t" x="{x}" y="110">{t}</text>'
               f'<text class="ifc-svg-p" x="{x}" y="132">{a}</text><text class="ifc-svg-p" x="{x}" y="148">{b}</text>')

# ISO Survey 2025, edicao contada no levantamento
SURVEY = [('ISO 9001:2015', 1611729), ('ISO 14001:2015', 739390), ('ISO 45001:2018', 599532),
          ('ISO/IEC 27001', 125622), ('ISO 22000:2018', 68271), ('ISO 50001:2018', 47394)]
barras = ''.join(f'<div class="sm-barra"><b>{n}</b><div><i style="--v:{v/SURVEY[0][1]*100:.2f}%"></i></div>'
                 f'<span>{v:,}</span></div>'.replace(',', '.') for n, v in SURVEY)

POS = [('ISO 37301:2021', 6), ('ISO 37001', 8), ('ISO 39001:2012', 10), ('ISO 9001:2015', 11),
       ('ISO 14001:2015', 24), ('ISO 45001:2018', 28)]
posicoes = ''.join(f'<div class="sm-pos-l"><b>{n}</b><div style="--p:{(p-1)/29*100:.1f}%"><em></em><strong>{p}º</strong></div></div>' for n, p in POS)

# matriz: os dados reais do grafico da home
i_mat = acha('class="qc-mat', home)
NORMAS = [('iso9001', 'ISO 9001'), ('iso14001', 'ISO 14001'), ('iso45001', 'ISO 45001'), ('iso27001', 'ISO/IEC 27001'),
          ('iso22000', 'ISO 22000'), ('iso50001', 'ISO 50001'), ('iso37001', 'ISO 37001'), ('iso39001', 'ISO 39001')]
linhas = re.findall(r'<g class="li" data-s="([^"]+)">(.*?)</g>', home[i_mat:], flags=re.S)
if not linhas: sys.exit('matriz da home nao encontrada')
matriz = '<div class="cab"></div>' + ''.join(f'<div class="cab" data-c="{c}">{r}</div>' for c, r in NORMAS)
for s, corpo in linhas:
    nome = re.search(r'class="rs"[^>]*>([^<]+)<', corpo).group(1)
    tem = set(re.findall(r'class="q[^"]*" data-n="([^"]+)"', corpo))
    matriz += f'<div class="s" data-l="{s}">{nome}</div>'
    for c, r in NORMAS:
        matriz += f'<div data-l="{s}" data-c="{c}" data-txt="{nome} · {r}">{"<i></i>" if c in tem else ""}</div>'
matriz = f'<!--cols-->{matriz}'

m = re.search(r'<svg[^>]*data-pdca.*?</svg>', src, flags=re.S)
if not m: sys.exit('PDCA nao encontrado')
pdca = m.group(0)

# Figura 1 da ISO 9001:2026, o desenho que ja esta na pagina da norma
s9 = (RAIZ / 'norma-iso-9001.html').read_text(encoding='utf-8')
i9 = acha('<figcaption>Elementos de um único processo', s9)
ini9 = s9.rfind('<svg', 0, i9)
if ini9 < 0: sys.exit('Figura 1 nao encontrada')
processo = s9[ini9:s9.rfind('</svg>', 0, i9) + 6]

# glifo: seis losangos, 2 fileiras de 3 (viewBox 0 0 22 14)
glifo = ''.join(f'<polygon points="{x} {y-3} {x+3} {y} {x} {y+3} {x-3} {y}"/>' for y in (3.5, 10.5) for x in (3.5, 11, 18.5))

for marca, valor in {'{{ETAPAS}}': etapas, '{{BARRAS}}': barras, '{{POSICOES}}': posicoes, '{{MATRIZ}}': matriz,
                     '{{PDCA}}': pdca, '{{PROCESSO}}': processo, '{{GLIFO}}': glifo}.items():
    if marca not in secoes: sys.exit(f'falta {marca}')
    secoes = secoes.replace(marca, valor)
secoes = secoes.replace('class="sm-mat" id="smMat"', f'class="sm-mat" id="smMat" style="--cols:{len(NORMAS)}"').replace('<!--cols-->', '')

# ----- numera, etiqueta e indice
secoes = re.sub(r'<!--.*?-->', '', secoes, count=1, flags=re.S)
partes = list(re.finditer(r'<section class="(sm-sec[^"]*)" data-fam="([^"]+)" data-nome="([^"]+)">', secoes))
if len(partes) != 30: sys.exit(f'{len(partes)} secoes; o pedido e 30')
fams, n = {}, 0
def etiqueta(mt):
    global n
    n += 1
    fams.setdefault(mt.group(2), []).append((n, mt.group(3)))
    return (f'<section class="{mt.group(1)}" id="m{n:02d}"><div class="sm-tag"><b>Modelo {n:02d}</b><span>{mt.group(2)} · {mt.group(3)}</span></div>')
secoes = re.sub(r'<section class="(sm-sec[^"]*)" data-fam="([^"]+)" data-nome="([^"]+)">', etiqueta, secoes)
indice = ''.join(f'<div><h2>{f}</h2>' + ''.join(f'<a href="#m{i:02d}" title="{t}"><i>{i:02d}</i>{t}</a>' for i, t in its) + '</div>' for f, its in fams.items())
topo = f'<div class="sm-topo"><h1>Modelos de seção</h1><p>Prova local · fora do site</p><div class="sm-ind">{indice}</div></div>'

# ----- casca: mesma barra, rodape e scripts da pagina molde
i_banner, i_ft = acha('<div class="page-banner"'), acha('<footer class="ft-root')
cabeca, cauda = src[:i_banner], src[i_ft:]
cabeca = re.sub(r'<!-- seo -->.*?<!-- /seo -->', '<meta name="robots" content="noindex, nofollow">', cabeca, flags=re.S)
cabeca = re.sub(r'<title>.*?</title>', '<title>Modelos de seção | Ideal Metrics</title>', cabeca, flags=re.S)
cabeca = re.sub(r'<meta name="description"[^>]*>', '', cabeca)
cabeca = cabeca.replace('</style>', css + '\n</style>', 1)
cauda = cauda.replace('<script src="js/gaveta.js', '<script>\n' + js + '\n</script>\n<script src="js/gaveta.js', 1)
corpo = cabeca + topo + secoes + cauda

# ----- conferencias
NUM = r'(?:9001|14001|45001|39001|39002|27001|37001|37301|22000|41001|50001|19011|20700|10019|14064|14067|14068|13485|22301|55001|42001|45004)'
for fonte, nome in ((secoes, 'secoes'), (topo, 'topo')):
    for mt in re.finditer(r'(?<![\d.\-])' + NUM + r'\b', fonte):
        antes = fonte[max(0, mt.start() - 12):mt.start()]
        if antes.endswith(('iso', 'iso-')): continue   # chave de dado (data-c="iso...") ou endereco de pagina
        if not re.search(r'ISO(/IEC)? $', antes): sys.exit(f'NUMERO SEM ISO em {nome}: ...{fonte[max(0,mt.start()-40):mt.end()+10]}')
for bruto in set(re.findall(r'(?:src|data-lum)="(img/[^"?]+)', secoes)):
    if not (RAIZ / bruto).exists(): sys.exit(f'imagem nao existe: {bruto}')
if '—' in secoes + topo: sys.exit('travessao no texto')

(RAIZ / '_prova-secoes-modelo.html').write_text(corpo, encoding='utf-8')
print('_prova-secoes-modelo.html', len(corpo), 'bytes;', n, 'modelos;', {f: len(v) for f, v in fams.items()})
