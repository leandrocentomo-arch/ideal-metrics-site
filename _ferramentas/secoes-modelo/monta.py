"""30 modelos de secao para avaliacao, 2a rodada (04/11/2026): monta _prova-secoes-modelo.html, com a casca de norma-iso-45001.html.

O arquivo final e prancha local: casa com _prova-*.html no .gitignore e nao sobe. Rodar da raiz do site:
python _ferramentas/secoes-modelo/monta.py
Falha se houver numero de norma sem ISO antes (regra do Leandro), imagem que nao existe ou travessao."""
import json, pathlib, re, sys

AQUI = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI))
import iso

RAIZ = AQUI.parents[1]
src = (RAIZ / 'norma-iso-45001.html').read_text(encoding='utf-8')
home = (RAIZ / 'index.html').read_text(encoding='utf-8')
secoes = (AQUI / 'secoes.html').read_text(encoding='utf-8')
css = (AQUI / 'estilo.css').read_text(encoding='utf-8')
js = (AQUI / 'motor.js').read_text(encoding='utf-8')
painel = json.loads((RAIZ / 'dados' / 'painel-normas.json').read_text(encoding='utf-8'))


def acha(marca, texto=src):
    i = texto.find(marca)
    if i < 0: sys.exit(f'marcador nao encontrado: {marca!r}')
    return i


def milhar(n):
    return f'{n:,}'.replace(',', '.')


def surv(k):
    s = painel['survey'][k]
    br = s['paises'].get('BR', 0)
    pos = sorted(s['paises'].values(), reverse=True).index(br) + 1
    return s['total'], br, pos


# ----- fichas: dados conferidos em iso.org / ABNT / ISO Survey (ver a prancha)
NORMAS = [
    dict(t='a', num='ISO 9001', rev='ISO 9001:2026', tema='Gestão da qualidade', sub='Sistemas de gestão da qualidade. Requisitos', pub='16-set-2026', ed='6ª edição',
         com='ISO/TC 176/SC 2', abnt='ABNT NBR ISO 9001:2026', ad='13-out-2026', fim='30-set-2029', fimr='Fim da transição', sk='9001', cod='ISO-9001-2026'),
    dict(t='b', num='ISO 14001', rev='ISO 14001:2026', tema='Gestão ambiental', sub='Sistemas de gestão ambiental. Requisitos com orientações para uso', pub='15-abr-2026', ed='4ª edição',
         com='ISO/TC 207/SC 1', abnt='ABNT NBR ISO 14001:2026', ad='08-jul-2026', fim='30-abr-2029', fimr='Fim da transição', sk='14001', cod='ISO-14001-2026'),
    dict(t='c', num='ISO 45001', rev='ISO 45001:2018', tema='Saúde e segurança', sub='Sistemas de gestão de saúde e segurança ocupacional. Requisitos com orientações para uso', pub='12-mar-2018', ed='1ª edição',
         com='ISO/TC 283', abnt='ABNT NBR ISO 45001:2024', ad='2024', fim='Em revisão', fimr='Situação', sk='45001', cod='ISO-45001-2018'),
]
glifo = ''.join(f'<polygon points="{x} {y-3} {x+3} {y} {x} {y+3} {x-3} {y}"/>' for y in (3.5, 10.5) for x in (3.5, 11, 18.5))
fichas, fichas3 = '', ''
for n in NORMAS:
    tot, br, pos = surv(n['sk'])
    fichas += f'''<div class="fc-p{' on' if n['t'] == 'c' else ''}" data-t="{n['t']}" role="tabpanel">
  <div class="fc-g">
    <div><p class="fc-ob">Norma</p><p class="fc-n">{n['num']}</p><p class="fc-c">Catálogo de normas<br>Ideal Metrics</p><h3 class="fc-t">{n['tema']}</h3><p class="fc-s">{n['sub']}</p></div>
    <div class="ob" aria-hidden="true"><div class="ob-l"></div><div class="ob-m"></div><div class="ob-e"><div><small>{n['rev']}</small></div><div><em>Catálogo nº</em><b>{n['num']}</b></div><div class="z"><small>{n['com']}<br>{n['ed']}</small><i></i></div></div></div>
    <div class="fc-d"><ul class="carimbo"><li>Ideal Metrics</li><li>Catálogo</li><li>Norma</li></ul><dl><div><dt>Revisão</dt><dd>{n['rev']}</dd></div><div><dt>No Brasil</dt><dd>{n['abnt']}</dd></div><div><dt>Comitê</dt><dd>{n['com']}</dd></div></dl></div>
  </div>
  <dl class="fc-z"><div><dt>Publicação</dt><dd>{n['pub']}</dd></div><div><dt>{n['fimr']}</dt><dd>{n['fim']}</dd></div><div><dt>Certificados no mundo</dt><dd>{milhar(tot)}</dd></div><div><dt>Certificados no Brasil</dt><dd>{milhar(br)}, {pos}º</dd></div>{iso.barras(n['cod'])}<i class="ac-q"></i></dl>
</div>'''
    fichas3 += f'''<article><div class="a"><span>Norma</span><span>{n['ed']}</span></div><h3>{n['num']}</h3><p class="s">{n['tema']}</p>
<dl><div><dt>Revisão</dt><dd>{n['rev']}</dd></div><div><dt>Publicação</dt><dd>{n['pub']}</dd></div><div><dt>{n['fimr']}</dt><dd>{n['fim']}</dd></div><div><dt>Comitê</dt><dd>{n['com']}</dd></div><div><dt>Certificados</dt><dd>{milhar(tot)}</dd></div></dl>
<div class="z">{iso.barras(n['cod'], 24)}<i></i></div></article>'''

# ----- calendario 2026 a 2029
MES = dict(jan=0, fev=1, mar=2, abr=3, mai=4, jun=5, jul=6, ago=7, set=8, out=9, nov=10, dez=11)


def pos_data(d):
    dia, mes, ano = d.split('-')
    return ((int(ano) - 2026) * 12 + MES[mes] + (int(dia) - 1) / 30) / 48 * 100


cal = '<div class="cal-a"><span>2026</span><span>2027</span><span>2028</span><span>2029</span></div>'
for rev, pub, abnt, fim in [('ISO 9001:2026', '16-set-2026', '13-out-2026', '30-set-2029'), ('ISO 14001:2026', '15-abr-2026', '08-jul-2026', '30-abr-2029')]:
    a, c, b = pos_data(pub), pos_data(fim), pos_data(abnt)
    cal += (f'<div class="cal-r"><b>{rev}</b><div class="cal-t"><i class="tr2" style="left:{a:.2f}%;width:{c-a:.2f}%"></i>'
            f'<i class="cal-m" style="left:{a:.2f}%;font-style:normal"><span>{pub}</span></i>'
            f'<i class="cal-m ch fim" style="left:{c:.2f}%;font-style:normal"><span>{fim}</span></i></div></div>')

# ----- numeros e escala
SURVEY = [('ISO 9001', '9001'), ('ISO 14001', '14001'), ('ISO 45001', '45001'), ('ISO/IEC 27001', '27001'), ('ISO 22000', '22000'), ('ISO 50001', '50001')]
maior = surv('9001')[0]
numeros = ''
for r, k in SURVEY:
    tot, br, _ = surv(k)
    numeros += f'<div class="nu-l"><span class="n">{r}</span><b>{milhar(tot)}<i></i></b><span class="pt2" style="width:{tot/maior*100:.1f}%"></span><span class="br">{milhar(br)}</span></div>'

POS = [('ISO 37301:2021', 6), ('ISO 37001', 8), ('ISO 39001:2012', 10), ('ISO 9001:2015', 11), ('ISO 14001:2015', 24), ('ISO 45001:2018', 28)]
escala = '<div class="ep-c"><span>Norma</span><div class="ep-p">' + ''.join(f'<span>{i}</span>' if i in (1, 5, 10, 15, 20, 25, 30) else '<span></span>' for i in range(1, 31)) + '</div><span></span></div>'
for r, p in POS:
    bol = ''.join(f'<i class="{"on" if i == p else "ate" if i < p else ""}"></i>' for i in range(1, 31))
    escala += f'<div class="ep-l"><span class="n">{r}</span><div class="ep-p">{bol}</div><b>{p}º</b></div>'

# ----- matriz: os dados reais do grafico da home
i_mat = acha('class="qc-mat', home)
COLS = [('iso9001', 'ISO 9001'), ('iso14001', 'ISO 14001'), ('iso45001', 'ISO 45001'), ('iso27001', 'ISO/IEC 27001'),
        ('iso22000', 'ISO 22000'), ('iso50001', 'ISO 50001'), ('iso37001', 'ISO 37001'), ('iso39001', 'ISO 39001')]
linhas = re.findall(r'<g class="li" data-s="([^"]+)">(.*?)</g>', home[i_mat:], flags=re.S)
if not linhas: sys.exit('matriz da home nao encontrada')
setores, tem = [], {}
for s, corpo in linhas:
    setores.append((s, re.search(r'class="rs"[^>]*>([^<]+)<', corpo).group(1)))
    for cl, nn in re.findall(r'class="(q[^"]*)" data-n="([^"]+)"', corpo):
        tem[(s, nn)] = cl

# Figura 1 da ISO 9001:2026, o desenho que ja esta na pagina da norma
s9 = (RAIZ / 'norma-iso-9001.html').read_text(encoding='utf-8')
i9 = acha('<figcaption>Elementos de um único processo', s9)
ini9 = s9.rfind('<svg', 0, i9)
if ini9 < 0: sys.exit('Figura 1 nao encontrada')
processo = s9[ini9:s9.rfind('</svg>', 0, i9) + 6]

CAMADAS = [('Eliminação', 'a)'), ('Substituição', 'b)'), ('Controles de engenharia', 'c)'), ('Controles administrativos', 'd)'), ('EPI', 'e)')]
planta = iso.planta()
for marca, valor in {'{{FICHAS}}': fichas, '{{FICHAS3}}': fichas3, '{{CAL}}': cal, '{{NUMEROS}}': numeros, '{{ESCALA}}': escala,
                     '{{PILHA}}': iso.pilha(CAMADAS), '{{ESCADA}}': iso.escada(), '{{INTEGRADO}}': iso.integrado(), '{{PLANTA}}': planta, '{{PLANTA_M}}': iso.planta(True),
                     '{{RELEVO}}': iso.matriz_relevo(setores, COLS, tem), '{{PROCESSO}}': processo, '{{GLIFO}}': glifo,
                     '{{BARRA}}': iso.barras('ISO-9001-2026')}.items():
    if marca not in secoes: sys.exit(f'falta {marca}')
    secoes = secoes.replace(marca, valor)

# ----- numera, etiqueta e indice
secoes = re.sub(r'<!--.*?-->', '', secoes, flags=re.S)
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
topo = f'<div class="sm-topo"><h1>Modelos de seção</h1><p>Prova local · fora do site · 2ª rodada</p><div class="sm-ind">{indice}</div></div>'

# ----- casca: mesma barra, rodape e scripts da pagina molde
i_banner, i_ft = acha('<div class="page-banner"'), acha('<footer class="ft-root')
cabeca, cauda = src[:i_banner], src[i_ft:]
cabeca = re.sub(r'<!-- seo -->.*?<!-- /seo -->', '<meta name="robots" content="noindex, nofollow">', cabeca, flags=re.S)
cabeca = re.sub(r'<title>.*?</title>', '<title>Modelos de seção | Ideal Metrics</title>', cabeca, flags=re.S)
cabeca = re.sub(r'<meta name="description"[^>]*>', '', cabeca)
# italico do mono e serifa so na prova: o site hospeda as proprias fontes e estas ainda nao estao em fonts/
cabeca = cabeca.replace('</head>', '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:ital,wght@1,400&family=IBM+Plex+Serif:wght@300&display=swap" rel="stylesheet">\n</head>', 1)
cabeca = cabeca.replace('</style>', css + '\n</style>', 1)
cauda = cauda.replace('<script src="js/gaveta.js', '<script>\n' + js + '\n</script>\n<script src="js/gaveta.js', 1)
corpo = cabeca + topo + secoes + cauda

# ----- conferencias
NUM = r'(?:9001|14001|45001|39001|39002|27001|37001|37301|22000|41001|50001|19011|20700|10019|14064|14067|14068|13485|22301|55001|42001|45004)'
for fonte, nome in ((secoes, 'secoes'), (topo, 'topo')):
    for mt in re.finditer(r'(?<![\d.\-])' + NUM + r'\b', fonte):
        antes = fonte[max(0, mt.start() - 12):mt.start()]
        if antes.endswith(('iso', 'iso-', 'ISO-')): continue   # chave de dado, endereco de pagina
        if not re.search(r'ISO(/IEC)? $', antes): sys.exit(f'NUMERO SEM ISO em {nome}: ...{fonte[max(0,mt.start()-40):mt.end()+10]}')
for bruto in set(re.findall(r'(?:src|data-lum)="(img/[^"?]+)', secoes)):
    if not (RAIZ / bruto).exists(): sys.exit(f'imagem nao existe: {bruto}')
if '—' in secoes + topo: sys.exit('travessao no texto')

(RAIZ / '_prova-secoes-modelo.html').write_text(corpo, encoding='utf-8')
print('_prova-secoes-modelo.html', len(corpo), 'bytes;', n, 'modelos;', {f: len(v) for f, v in fams.items()})
