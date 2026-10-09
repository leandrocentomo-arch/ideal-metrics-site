# -*- coding: utf-8 -*-
"""Setores x normas (09/10/2026). Fonte unica dos dados e gerador.

    python _ferramentas/setores.py

Faz, de forma idempotente:
  1. grava js/setores-dados.js (window.IM_SETORES), lido pelo filtro (js/setores-filtro.js);
  2. reescreve o miolo (<div class="content">) das seis paginas setor-*.html na estrutura nova;
  3. poe o filtro na home (secao Setores de atuacao) e em servicos.html, entre marcadores;
  4. liga css/setores.css nas oito paginas e os dois scripts nas duas que levam o filtro.

Os textos de abertura, entregas e estudos de cada setor vem de _ferramentas/setores-textos.json (extraidos das paginas
antigas, editaveis). Norma sem pagina de servico aparece sem link; quando a pagina nascer, basta pôr o endereco em
NORMAS e rodar de novo. Itens marcados # NOVO entraram em 09/10/2026 e pedem a conferencia do Leandro."""
import os, re, json

AQUI = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(AQUI)
CSS_V, JS_V = '7', '1'

TIPOS = [('gestao', 'Sistemas de gestão', 'Normas ISO que a organização pode certificar.'),
         ('mercado', 'Esquemas e programas de mercado', 'Exigidos por redes, montadoras, embarcadores, contratantes e órgãos de acreditação.'),
         ('tecnico', 'Requisitos técnicos e legais', 'Obrigações legais e programas técnicos que sustentam os sistemas acima.')]

# id: (nome, descricao, tipo, pagina do servico ou None)
NORMAS = {
 'iso9001':  ('ISO 9001', 'Gestão da qualidade', 'gestao', 'norma-iso-9001.html'),
 'iso14001': ('ISO 14001', 'Gestão ambiental', 'gestao', 'norma-iso-14001.html'),
 'iso45001': ('ISO 45001', 'Saúde e segurança ocupacional', 'gestao', 'norma-iso-45001.html'),
 'iso39001': ('ISO 39001', 'Segurança viária', 'gestao', 'seguranca-viaria.html'),
 'iso22000': ('ISO 22000', 'Gestão da segurança de alimentos', 'gestao', 'seguranca-alimentos.html'),
 'iso27001': ('ISO/IEC 27001', 'Segurança da informação', 'gestao', 'compliance-seguranca-informacao.html'),
 'iso27701': ('ISO/IEC 27701', 'Gestão da privacidade da informação', 'gestao', None),
 'iso200001': ('ISO/IEC 20000-1', 'Gestão de serviços de TI', 'gestao', None),
 'iso42001': ('ISO/IEC 42001', 'Gestão de sistemas de inteligência artificial', 'gestao', None),            # NOVO
 'iso56002': ('ISO 56002', 'Gestão da inovação', 'gestao', 'implantacao-iso.html'),
 'iso50001': ('ISO 50001', 'Gestão de energia', 'gestao', 'implantacao-iso.html'),
 'iso14064': ('ISO 14064', 'Inventário de gases de efeito estufa', 'gestao', 'carbono-inventario-gee.html'),
 'iso13485': ('ISO 13485', 'Gestão da qualidade de dispositivos médicos', 'gestao', 'implantacao-iso.html'),
 'iso15189': ('ISO 15189', 'Qualidade e competência de laboratórios clínicos', 'gestao', None),
 'iso14971': ('ISO 14971', 'Gestão de riscos de dispositivos médicos', 'gestao', None),
 'iso28000': ('ISO 28000', 'Segurança da cadeia de suprimentos', 'gestao', None),
 'iso29001': ('ISO 29001', 'Gestão da qualidade em petróleo, petroquímica e gás natural', 'gestao', None),
 'iatf16949': ('IATF 16949', 'Qualidade na cadeia automotiva (autopeças)', 'mercado', 'implantacao-iso.html'),
 'fssc22000': ('FSSC 22000', 'Certificação reconhecida pela GFSI', 'mercado', 'seguranca-alimentos.html'),
 'brcgs': ('BRCGS', 'Padrão global de segurança de alimentos', 'mercado', 'padroes-mercado.html'),
 'ifs': ('IFS Food', 'Padrão de segurança de alimentos reconhecido pela GFSI', 'mercado', None),                # NOVO
 'sqf': ('SQF', 'Padrão de segurança e qualidade de alimentos reconhecido pela GFSI', 'mercado', None),        # NOVO
 'sassmaq': ('SASSMAQ', 'Avaliação de segurança, saúde, meio ambiente e qualidade no transporte de químicos (Abiquim)', 'mercado', None),
 'oea': ('OEA', 'Operador Econômico Autorizado, programa da Receita Federal para a cadeia logística', 'mercado', None),   # NOVO
 'ona': ('ONA', 'Acreditação de serviços de saúde (Organização Nacional de Acreditação)', 'mercado', None),     # NOVO
 'haccp': ('HACCP / APPCC', 'Análise de perigos e pontos críticos de controle', 'tecnico', 'seguranca-alimentos.html'),
 'ppr': ('PPR', 'Programas de pré-requisitos', 'tecnico', 'seguranca-alimentos.html'),
 'fooddefense': ('Food Defense', 'Proteção contra contaminação intencional', 'tecnico', 'seguranca-alimentos.html'),
 'nr10': ('NR-10', 'Segurança em instalações elétricas', 'tecnico', 'nrs.html'),
 'nr12': ('NR-12', 'Segurança em máquinas e equipamentos', 'tecnico', 'nrs.html'),
 'nr37': ('NR-37', 'Segurança e saúde em plataformas de petróleo', 'tecnico', 'nrs.html'),
}

# ordem, pagina e normas de cada setor (as seis paginas ja existiam; as normas novas estao marcadas)
SETORES = [
 ('industria', 'setor-industria.html', ['iso9001', 'iatf16949', 'iso14001', 'iso45001', 'iso50001', 'iso14064', 'nr12', 'nr10']),
 ('logistica', 'setor-logistica.html', ['iso9001', 'iso39001', 'iso14001', 'iso45001', 'iso28000', 'sassmaq', 'oea']),
 ('alimentos', 'setor-alimentos.html', ['iso22000', 'fssc22000', 'haccp', 'brcgs', 'ppr', 'fooddefense', 'ifs', 'sqf']),
 ('saude', 'setor-saude.html', ['iso13485', 'iso9001', 'iso15189', 'iso14971', 'iso27001', 'ona']),
 ('tecnologia', 'setor-tecnologia.html', ['iso27001', 'iso27701', 'iso200001', 'iso9001', 'iso56002', 'iso42001']),
 ('energia', 'setor-energia.html', ['iso50001', 'iso29001', 'iso14001', 'iso45001', 'nr37', 'iso14064']),
]

TEXTOS = json.load(open(os.path.join(AQUI, 'setores-textos.json'), encoding='utf-8'))


def ler(p):
    with open(os.path.join(SITE, p), encoding='utf-8', newline='') as f: return f.read()


def gravar(p, s):
    with open(os.path.join(SITE, p), 'w', encoding='utf-8', newline='') as f: f.write(s)


def dados_js():
    setores = [{'id': i, 'nome': TEXTOS[i]['nome'], 'pagina': pg, 'resumo': TEXTOS[i]['resumo'], 'normas': ns} for i, pg, ns in SETORES]
    normas = {k: {'nome': v[0], 'desc': v[1], 'tipo': v[2], 'pagina': v[3]} for k, v in NORMAS.items()}
    ordem = sorted(NORMAS, key=lambda k: ([t[0] for t in TIPOS].index(NORMAS[k][2]), list(NORMAS).index(k)))
    obj = {'setores': setores, 'normas': normas, 'ordemNormas': ordem}
    return ('/* Gerado por _ferramentas/setores.py (09/10/2026). Nao editar a mao. */\n'
            'window.IM_SETORES=' + json.dumps(obj, ensure_ascii=False, separators=(',', ':')) + ';\n')


def cartao_norma(k):
    nome, desc, _, pg = NORMAS[k]
    if pg:
        return ('<a class="pos-card pos-card--link" href="%s"><h4>%s</h4><p>%s</p><span class="pos-more">Ver serviço &rarr;</span></a>' % (pg, nome, desc))
    return '<div class="pos-card"><h4>%s</h4><p>%s</p></div>' % (nome, desc)


def miolo(i, pg, normas):
    t = TEXTOS[i]; nome = t['nome']
    h = ['<div class="content">',
         '<p class="abre">%s</p>' % t['abre'],
         '<p>%s</p>' % t['para'],
         '<h3>Certificações e reconhecimentos do setor</h3>',
         '<p class="stp-nota">Programas que clientes, contratantes e órgãos reguladores esperam das organizações do setor. A Ideal Metrics implanta cada um e prepara a organização para a avaliação. Os cartões com seta levam à página do serviço.</p>']
    for tipo, rot, sub in TIPOS:
        ks = [k for k in normas if NORMAS[k][2] == tipo]
        if not ks: continue
        h.append('<div class="stp-grupo"><span>%s</span><em>%02d</em></div>' % (rot, len(ks)))
        h.append('<p class="stp-nota">%s</p>' % sub)
        h.append('<div class="stp-grade">')
        h.extend('  ' + cartao_norma(k) for k in ks)
        h.append('</div>')
    h.append('<h3>O que a Ideal Metrics entrega</h3>')
    h.append('<div class="numbered-items">')
    for n, (tit, txt) in enumerate(t['entregas'], 1):
        h.append('<div class="numbered-item"><div class="num">%02d</div><div><h4>%s</h4><p>%s</p></div></div>' % (n, tit, txt))
    h.append('</div>')
    h.append('<p><a href="como-trabalhamos.html">Veja como trabalhamos</a>.</p>')
    h.append('<h3>Estudos e pesquisa aplicada para o setor</h3>')
    h.append('<ul>')
    h.extend('  <li>%s</li>' % e for e in t['estudos'])
    h.append('</ul>')
    h.append('<p><a href="estudos-pesquisa.html">Conheça a divisão de estudos e pesquisa aplicada</a>.</p>')
    h.append('<h3>Outros setores</h3>')
    h.append('<div class="stp-outros">')
    for j, pg2, _ in SETORES:
        if j != i: h.append('  <a href="%s"><b>%s</b><span>Ver setor</span></a>' % (pg2, TEXTOS[j]['nome']))
    h.append('</div>')
    h.append('<a href="contato.html" class="link-arrow">Fale com a nossa equipe técnica &rarr;</a>')
    h.append('</div>')
    return '\n'.join(h)


def liga_css(s):
    tag = '<link rel="stylesheet" href="css/setores.css?v=%s">' % CSS_V
    s = re.sub(r'<link rel="stylesheet" href="css/setores\.css\?v=\d+">\n?', '', s)
    return s.replace('</head>', tag + '\n</head>', 1)


def relacao():
    """09/10/2026: grafico estatico (SVG) da relacao setor x norma, logo abaixo da frase de «O que fazemos» na home.
    Linhas = setores, colunas = normas agrupadas por tipo; um quadrado liga o setor a norma. So quadrados e linha fina
    (sem circulos). Rotulo de linha leva a pagina do setor; rotulo de coluna, a pagina do servico quando existe.
    js/setores-matriz.js acende a linha e a coluna sob o mouse."""
    PASSO, QUAD, ROT_L, TOPO, LIN_H, GAP = 19, 13, 112, 128, 25, 14
    cols = []                                    # (id, x do centro)
    x = ROT_L; grupos = []
    CURTO = {'gestao': 'Sistemas de gestão', 'mercado': 'Mercado', 'tecnico': 'Técnico e legal'}
    for tipo, _rot, _ in TIPOS:
        rot = CURTO[tipo]
        ids = [k for k in dados_ordem() if NORMAS[k][2] == tipo]
        x0 = x
        for k in ids:
            cols.append((k, x + PASSO / 2)); x += PASSO
        grupos.append((rot, x0, x - 2))
        x += GAP
    larg = int(x - GAP + 6); alt = TOPO + LIN_H * len(SETORES) + 4
    esc = lambda s: s.replace('&', '&amp;')
    o = ['<figure class="qc-mat" aria-labelledby="qcMatTit">',
         '  <div class="qc-mat-topo"><span id="qcMatTit">Normas e padrões por setor</span><span>[ IM.S ]</span></div>',
         '  <div class="qc-mat-rola"><svg viewBox="0 0 %d %d" width="%d" height="%d" role="img" aria-label="Grade que liga cada setor às normas e padrões aplicáveis">' % (larg, alt, larg, alt)]
    for rot, x0, x1 in grupos:
        o.append('    <g class="gr"><text x="%s" y="11">%s</text><path d="M%s 17H%s"/></g>' % (x0, esc(rot), x0, x1))
    for k, cx in cols:
        nome, _, _, pg = NORMAS[k]
        txt = '<text transform="translate(%s %s) rotate(-90)">%s</text>' % (cx + 3.5, TOPO - 8, esc(nome))
        o.append('    <g class="co" data-n="%s">%s</g>' % (k, ('<a href="%s">%s</a>' % (pg, txt)) if pg else txt))
    for r, (i, pg, normas) in enumerate(SETORES):
        y = TOPO + r * LIN_H
        o.append('    <g class="li" data-s="%s"><path class="fio" d="M0 %s H%s"/><a href="%s"><text class="rs" x="0" y="%s">%s</text></a>' % (i, y, larg, pg, y + 17, esc(TEXTOS[i]['nome'])))
        for k, cx in cols:
            if k in normas:
                o.append('      <rect class="q" data-n="%s" x="%s" y="%s" width="%d" height="%d" rx="3"><title>%s: %s</title></rect>' % (k, cx - QUAD / 2, y + (LIN_H - QUAD) / 2, QUAD, QUAD, esc(TEXTOS[i]['nome']), esc(NORMAS[k][0])))
            else:
                o.append('      <rect class="v" x="%s" y="%s" width="2" height="2"/>' % (cx - 1, y + LIN_H / 2 - 1))
        o.append('    </g>')
    o.append('    <path class="fio" d="M0 %s H%s"/>' % (TOPO + LIN_H * len(SETORES), larg))
    o.append('  </svg></div>')
    o.append('  <figcaption>Cada quadrado liga um setor a uma norma ou padrão. Passe o mouse ou toque para ler a linha e a coluna; os nomes levam às páginas.</figcaption>')
    o.append('</figure>')
    return '<!-- relacao setor norma -->\n' + '\n'.join(o) + '\n<!-- fim relacao setor norma -->'


def dados_ordem():
    return sorted(NORMAS, key=lambda k: ([t[0] for t in TIPOS].index(NORMAS[k][2]), list(NORMAS).index(k)))


def poe_relacao(s):
    s = re.sub(r'[ \t]*<!-- relacao setor norma -->.*?<!-- fim relacao setor norma -->\n?', '', s, flags=re.S)
    ancora = '<figure class="qc-temas"'
    assert s.count(ancora) == 1
    s = s.replace(ancora, relacao() + '\n          ' + ancora, 1)
    s = re.sub(r'<script src="js/setores-matriz\.js[^>]*></script>\n?', '', s)
    return s.replace('</body>', '<script src="js/setores-matriz.js?v=%s"></script>\n</body>' % JS_V, 1)


FILTRO = '''<!-- filtro setor norma -->
<section class="stf" id="stf" aria-labelledby="stfTit">
  <div class="stf-topo">
    <h3 class="stf-tit" id="stfTit">Encontre pelo setor ou pela norma</h3>
    <div class="stf-modos" role="tablist" aria-label="Modo de busca">
      <button type="button" class="stf-modo" role="tab" data-modo="setor" aria-selected="true">Por setor</button>
      <button type="button" class="stf-modo" role="tab" data-modo="norma" aria-selected="false">Por norma</button>
    </div>
  </div>
  <div class="stf-chips"></div>
  <div class="stf-res" aria-live="polite"></div>
</section>
<!-- fim filtro setor norma -->'''

SCRIPTS = ('<script src="js/setores-dados.js?v=%s"></script>\n<script src="js/setores-filtro.js?v=%s"></script>' % (JS_V, JS_V))


def poe_filtro(s, ancora, depois):
    """ancora: texto antes do qual (ou depois do qual, se depois=True) o filtro entra"""
    s = re.sub(r'<!-- filtro setor norma -->.*?<!-- fim filtro setor norma -->\n?', '', s, flags=re.S)
    s = re.sub(r'<script src="js/setores-dados\.js[^>]*></script>\n?<script src="js/setores-filtro\.js[^>]*></script>\n?', '', s)
    assert s.count(ancora) == 1, ancora
    s = s.replace(ancora, ancora + '\n' + FILTRO if depois else FILTRO + '\n' + ancora, 1)
    return s.replace('</body>', SCRIPTS + '\n</body>', 1)


def main():
    gravar('js/setores-dados.js', dados_js())
    for i, pg, normas in SETORES:
        s = ler(pg)
        a = s.find('<div class="content">'); b = s.find('</div>\n</div>\n<footer', a)
        assert a > 0 and b > a, pg
        s = s[:a] + miolo(i, pg, normas) + s[b:]
        gravar(pg, liga_css(s))
    # home: depois da frase da secao Setores de atuacao
    s = ler('index.html')
    s = liga_css(s)
    s = poe_filtro(s, '<p class="st-lead">Atendemos os mais diversos segmentos produtivos.</p>', True)
    s = poe_relacao(s)
    gravar('index.html', s)
    s = ler('servicos.html')
    s = liga_css(s)
    s = poe_filtro(s, '<h2>PADRÕES E CONFORMIDADE</h2>', False)
    gravar('servicos.html', s)
    print('ok: %d setores, %d normas' % (len(SETORES), len(NORMAS)))


if __name__ == '__main__':
    main()
