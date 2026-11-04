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
js = (AQUI / 'motor.js').read_text(encoding='utf-8') + '\n' + (AQUI / 'deitada.js').read_text(encoding='utf-8') + '\n' + (AQUI / 'plana.js').read_text(encoding='utf-8') + '\n' + (AQUI / 'paginas.js').read_text(encoding='utf-8')
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

# ----- grade deitada: os dados reais do grafico da home, com setor, tema e pagina de setores-dados.js
i_mat = acha('class="qc-mat', home)
mat = home[i_mat:acha('fim relacao setor norma', home)]
dd = (RAIZ / 'js' / 'setores-dados.js').read_text(encoding='utf-8')
dd = json.loads(dd[dd.index('{'):dd.rindex('}') + 1])
TEMA_CURTO = {'qualidade': 'Qualidade', 'ambiente': 'Meio ambiente', 'sst': 'Saúde e segurança', 'viaria': 'Segurança viária', 'clima': 'Clima e carbono',
              'esg': 'ESG', 'social': 'Social e cadeia', 'alimentos': 'Segurança de alimentos', 'infosec': 'Segurança da informação', 'compliance': 'Compliance e riscos'}
ord_g = [g['id'] for g in dd['grupos']]
colunas = re.findall(r'<g class="co" data-n="([^"]+)" data-rev="([^"]*)" data-tit="([^"]*)">(.*?)</g>', mat, flags=re.S)
if len(colunas) != len(dd['ordemNormas']): sys.exit('colunas da grade da home diferentes de setores-dados.js')
def pagina_norma(nid):
    num = re.match(r'iso(\d+)$', nid)
    if num and (RAIZ / f'norma-iso-{num.group(1)}.html').exists(): return f'norma-iso-{num.group(1)}.html'
    return dd['normas'][nid].get('pagina') or ''
M_N = [{'id': n, 'l': re.search(r'>([^<]+)</text>', c).group(1), 'rev': r, 'tit': t, 'g': ord_g.index(dd['normas'][n]['grupo']), 'p': pagina_norma(n)} for n, r, t, c in colunas]
ordem_ok = [x['g'] for x in M_N]
if ordem_ok != sorted(ordem_ok): sys.exit('colunas da home fora da ordem dos temas')
por_s = {s['id']: s for s in dd['setores']}
M_S, M_M = [], []
for sid, corpo in re.findall(r'<g class="li" data-s="([^"]+)">(.*?)</g>', mat, flags=re.S):
    M_S.append({'id': sid, 'c': re.search(r'class="rs"[^>]*>([^<]+)<', corpo).group(1), 'n': por_s[sid]['nome'], 'r': por_s[sid]['resumo'], 'p': por_s[sid]['pagina']})
    rel = {nn: cl for cl, nn in re.findall(r'class="(q[^"]*)" data-n="([^"]+)"', corpo)}
    M_M.append(''.join({'q': '2', 'q t': '1'}.get(rel.get(x['id'], ''), '0') for x in M_N))
if len(M_S) != 9: sys.exit('grade da home sem os nove setores')
dados_md = json.dumps({'S': M_S, 'N': M_N, 'G': [{'id': g, 'n': TEMA_CURTO[g]} for g in ord_g], 'M': M_M}, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/')
temas_md = '<button type="button" role="tab" data-g="-1" aria-selected="true">Todos os temas</button>' + ''.join(f'<button type="button" role="tab" data-g="{k}" aria-selected="false">{TEMA_CURTO[g]}</button>' for k, g in enumerate(ord_g))

# ----- grade reta (modelo 31): mesma geometria da grade da home, com as colunas em grupos para o filtro por tema
cab_h = mat[mat.index('<svg'):mat.index('<g class="co"')]
chamas = ''.join(re.findall(r'<g class="gr chama">.*?</g>', cab_h, flags=re.S))
grupos = ''.join(re.findall(r'<g class="gr">.*?</g>', cab_h, flags=re.S))
def plana():
    s = [f'<svg class="mg-svg" viewBox="0 0 1770 510" tabindex="0" role="img" aria-label="Grade que liga cada setor às normas e padrões. Setas do teclado percorrem as casas; o detalhe aparece na ficha."><g class="mg-grs">{chamas}</g><g transform="translate(0 73)"><g class="mg-grs">{grupos}</g>']
    s.append('<g class="mg-gt"><text x="238" y="11"></text><path d=""/></g>')
    for i, x in enumerate(M_S):
        s.append(f'<g class="mg-li" style="--i:{i}"><path class="fio" d="M0 {190 + i * 27} H1770"/><text class="rs" x="0" y="{208 + i * 27}">{x["c"]}</text></g>')
    s.append('<path class="fio" d="M0 433 H1770"/>')
    for j, c in enumerate(M_N):
        X = 238 + j * 20 + c['g'] * 14
        cel = ''
        for i in range(len(M_S)):
            k = M_M[i][j]
            y = 197 + i * 27
            if k == '0': cel += f'<rect class="v" style="--i:{i}" data-s="{i}" y="{y + 5.5}" width="2" height="2"/>'
            else: cel += f'<rect class="q{" t" if k == "1" else ""}" style="--i:{i}" data-s="{i}" x="3.5" y="{y}" height="13" rx="3"/>'
        s.append(f'<g class="mg-co" data-x="{X}" style="--j:{j};transform:translateX({X}px)"><text style="transform:translate(13.5px,182px) rotate(-90deg)">{c["l"]}</text>{cel}</g>')
    return ''.join(s) + '</g></svg>'

# ----- paginas inteiras 37 e 38: setores e temas lidos da mesma fonte da grade da home; icones na gramatica do IC de blocos.py
IC_S = {'industria': '<path d="M3 20V10l5 3v-3l5 3v-3l5 3V4h3v16zM3 20h18"/>', 'transporte': '<path d="M8 3 4 21M16 3l4 18M12 4v3M12 10v4M12 17v3"/>',
        'facilities': '<path d="M6 3h12v18H6zM6 9h12M6 15h12M12 3v18"/>', 'alimentos': '<path d="M5 8h14v13H5zM8 8V3h8v5M5 13h14"/>',
        'agro': '<path d="M12 3 6 12h12zM12 8 4 20h16zM12 20v2"/>', 'saude': '<path d="M9 3h6v6h6v6h-6v6H9v-6H3V9h6z"/>',
        'energia': '<path d="M12 3 7 21M12 3l5 18M6 7h12M8.5 13h7M4 12l2-5M20 12l-2-5"/>', 'tecnologia': '<path d="M7 7h10v10H7zM10 7V3M14 7V3M10 21v-4M14 21v-4M3 10h4M3 14h4M21 10h-4M21 14h-4"/>',
        'servicos': '<path d="M3 15h6v6H3zM15 15h6v6h-6zM9 3h6v6H9zM12 9v3M6 15v-3h12v3"/>'}
IC_T = {'qualidade': '<polygon points="12 4 20 12 12 20 4 12"/><path d="M8 12h8"/>', 'ambiente': '<polygon points="12 4 20 18 4 18"/><path d="M4 21h16"/>',
        'sst': '<path d="M12 4v16M4 12h16"/>', 'viaria': '<path d="M7 4v16M17 4v16M12 6v3M12 11v3M12 16v3"/>', 'clima': '<path d="M4 5h5v5h5v5h6M4 20h16"/>',
        'esg': '<polygon points="12 3 20 7.5 20 16.5 12 21 4 16.5 4 7.5"/>', 'social': '<rect x="4" y="4" width="4" height="4"/><rect x="16" y="4" width="4" height="4"/><rect x="4" y="16" width="4" height="4"/><rect x="16" y="16" width="4" height="4"/><path d="M8 8l8 8M16 8l-8 8"/>',
        'alimentos': '<rect x="4" y="4" width="16" height="16"/><path d="M12 4v16M4 12h16"/>', 'infosec': '<rect x="4" y="4" width="16" height="16"/><rect x="10.5" y="10.5" width="3" height="3"/><path d="M4 12h4M16 12h4M12 4v4M12 16v4"/>',
        'compliance': '<rect x="4" y="4" width="16" height="16"/><path d="M8 9h8M8 12h8M8 15h5"/>'}
pg_setores = ''.join(f'<a class="pc pc-s" data-i="{k}" href="{s["pagina"]}"><div class="cm pts pc-f"><svg viewBox="0 0 24 24" class="ic" aria-hidden="true">{IC_S[s["id"]]}</svg></div><div><div class="pc-a"><h3>{s["nome"]}</h3><i>{k:03d}</i></div><p>{s["resumo"]}</p></div></a>' for k, s in enumerate(dd['setores'], 1))
def pg_tema(k, g):
    linhas = ''
    for nid in [n for n in dd['ordemNormas'] if dd['normas'][n]['grupo'] == g][:5]:
        p, nome = pagina_norma(nid), dd['normas'][nid]['nome']
        linhas += f'<a href="{p}">{nome}</a>' if p else f'<span>{nome}</span>'
    return f'<article class="pc pc-t" data-i="{k}"><div class="pc-a"><h3>{TEMA_CURTO[g]}</h3><i>{k:03d}</i></div><div class="cm pts pc-f"><svg viewBox="0 0 24 24" class="ic" aria-hidden="true">{IC_T[g]}</svg></div><div class="pc-ln">{linhas}</div></article>'
pg_temas = ''.join(pg_tema(k, g) for k, g in enumerate(ord_g, 1))

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
                     '{{DADOS_MD}}': dados_md, '{{TEMAS_MD}}': temas_md, '{{PLANA}}': plana(), '{{PG_SETORES}}': pg_setores, '{{PG_TEMAS}}': pg_temas, '{{PROCESSO}}': processo, '{{GLIFO}}': glifo,
                     '{{BARRA}}': iso.barras('ISO-9001-2026')}.items():
    if marca not in secoes: sys.exit(f'falta {marca}')
    secoes = secoes.replace(marca, valor)

# ----- numera, etiqueta e indice
secoes = re.sub(r'<!--.*?-->', '', secoes, flags=re.S)
partes = list(re.finditer(r'<section class="(sm-sec[^"]*)" data-fam="([^"]+)" data-nome="([^"]+)">', secoes))
if len(partes) != 38: sys.exit(f'{len(partes)} secoes; sao 41 numeros menos os 3 retirados')
# 04/11/2026: o 04, o 08 e o 10 sairam a pedido; o numero de cada modelo nao muda, porque e por ele que o Leandro se refere a cada um
SAIRAM = {4, 8, 10}
fams, n = {}, 0
def etiqueta(mt):
    global n
    n += 1
    while n in SAIRAM: n += 1
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
cabeca = cabeca.replace('</head>', '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:ital,wght@1,400&display=swap" rel="stylesheet">\n</head>', 1)
cabeca = cabeca.replace('</style>', css + '\n</style>', 1)
cauda = cauda.replace('<script src="js/gaveta.js', '<script>\n' + js + '\n</script>\n<script src="js/gaveta.js', 1)
corpo = cabeca + topo + secoes + cauda

# ----- conferencias
NUM = r'(?:9001|14001|45001|39001|39002|27001|37001|37301|22000|41001|50001|19011|20700|10019|14064|14067|14068|13485|22301|55001|42001|45004)'
for fonte, nome in ((secoes, 'secoes'), (topo, 'topo')):
    for mt in re.finditer(r'(?<![\d.\-])' + NUM + r'\b', fonte):
        antes = fonte[max(0, mt.start() - 12):mt.start()]
        if antes.endswith(('iso', 'iso-', 'ISO-', 'fssc', 'FSSC ')): continue   # chave de dado, endereco de pagina; FSSC 22000 e outro esquema, nao norma ISO
        if not re.search(r'ISO(/IEC)? $', antes): sys.exit(f'NUMERO SEM ISO em {nome}: ...{fonte[max(0,mt.start()-40):mt.end()+10]}')
for bruto in set(re.findall(r'(?:src|data-lum)="(img/[^"?]+)', secoes)):
    if not (RAIZ / bruto).exists(): sys.exit(f'imagem nao existe: {bruto}')
if '—' in secoes + topo: sys.exit('travessao no texto')

(RAIZ / '_prova-secoes-modelo.html').write_text(corpo, encoding='utf-8')
print('_prova-secoes-modelo.html', len(corpo), 'bytes;', n, 'modelos;', {f: len(v) for f, v in fams.items()})
import spirit
spirit.grava(secoes, cabeca, js, fams, RAIZ)
