# -*- coding: utf-8 -*-
"""Setores x normas (09/10/2026). Fonte unica dos dados e gerador.

    python _ferramentas/setores.py

Faz, de forma idempotente:
  1. grava js/setores-dados.js (window.IM_SETORES), lido pelo filtro (js/setores-filtro.js);
  2. reescreve o miolo (<div class="content">) das nove paginas setor-*.html;
  3. poe o filtro em servicos.html, entre marcadores (na home saiu em 14/10/2026; ali ficam so os dados);
  4. poe na home, logo abaixo da frase de «O que fazemos», o mosaico de normas e padroes (js/setores-mosaico.js);
  5. liga css/setores.css nas oito paginas e os scripts onde cabem.

Tres situacoes para cada norma: de um ou mais setores (lista em SETORES), de qualquer setor (TRANSVERSAIS) ou de
nenhum dos nove (as demais). O catalogo inteiro vem do que o proprio site ja cita: implantacao-iso, padroes-mercado,
compliance, NRs, ESG, carbono e seguranca de alimentos. Os textos de abertura, entregas e estudos de cada setor vem de
_ferramentas/setores-textos.json. Norma sem pagina de servico aparece sem link; quando a pagina nascer, basta pôr o
endereco em NORMAS e rodar de novo. Itens # NOVO entraram em 09/10/2026 e # CONFERIR tem descricao a validar."""
import os, re, json

AQUI = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(AQUI)
CSS_V, JS_V = '75', '20'
# Os dois modelos do grafico ficam gravados aqui. A home usa o de MODELO_HOME; para trocar, mude e rode de novo.
#   'matriz'  = grade de quadrados, setores nas linhas e normas nas colunas, na largura da pagina (modelo de 09/10/2026, 1)
#   'mosaico' = retangulos agrupados com botao por setor, no terco direito, abaixo da frase (modelo de 09/10/2026, 2)
MODELO_HOME = 'matriz'

GRUPOS = [   # 10/10/2026: os dez TEMAS (disciplinas), no lugar dos seis grupos de instrumento. Ver Ideal Metrics/levantamento-setores-normas-temas-2026-10-10.md
 ('qualidade', 'Qualidade', 'Sistema de gestão da qualidade e os padrões de qualidade de cada setor.'),
 ('ambiente', 'Meio ambiente', 'Gestão ambiental, licenciamento, manejo e rastreabilidade da cadeia.'),
 ('sst', 'Saúde e segurança do trabalho', 'Sistema de gestão de SST e as normas regulamentadoras.'),
 ('viaria', 'Segurança viária', 'Sistema de gestão da segurança viária para frotas e para quem administra a via.'),
 ('clima', 'Clima e carbono', 'Inventário, pegada, neutralização, energia, metas, créditos e mercado regulado.'),
 ('esg', 'Sustentabilidade e ESG', 'Avaliação, relato e padrões de desempenho exigidos por investidores e financiadores.'),
 ('social', 'Responsabilidade social e cadeia de valor', 'Auditoria social e ética exigida por clientes e cadeias de suprimento.'),
 ('alimentos', 'Segurança de alimentos', 'Normas, esquemas reconhecidos pela GFSI e programas técnicos.'),
 ('infosec', 'Segurança da informação e privacidade', 'Segurança da informação, privacidade, serviços de TI e inteligência artificial.'),
 ('compliance', 'Compliance, riscos e continuidade', 'Antissuborno, compliance, riscos, continuidade, ativos e programas de mercado.'),
]

IMPL, COMP, SEG, PADR, NRS = ('implantacao-iso.html', 'compliance-seguranca-informacao.html', 'seguranca-alimentos.html',
                              'padroes-mercado.html', 'nrs.html')

# id: (nome, descricao, grupo, pagina do servico ou None)
NORMAS = {
 # sistemas de gestao ISO
 'iso9001': ('ISO 9001', 'Gestão da qualidade', 'qualidade', 'norma-iso-9001.html'),
 'iso14001': ('ISO 14001', 'Gestão ambiental', 'ambiente', 'norma-iso-14001.html'),
 'iso45001': ('ISO 45001', 'Saúde e segurança ocupacional', 'sst', 'norma-iso-45001.html'),
 'iso39001': ('ISO 39001', 'Segurança viária', 'viaria', 'seguranca-viaria.html'),
 'iso41001': ('ISO 41001', 'Gestão de facilities', 'qualidade', IMPL),
 'iso37001': ('ISO 37001', 'Gestão antissuborno', 'compliance', COMP),
 'iso37301': ('ISO 37301', 'Gestão de compliance', 'compliance', COMP),
 'iso56002': ('ISO 56002', 'Gestão da inovação', 'qualidade', IMPL),
 'iso50001': ('ISO 50001', 'Gestão de energia', 'clima', IMPL),
 'iso55001': ('ISO 55001', 'Gestão de ativos', 'compliance', IMPL),
 'iso27001': ('ISO/IEC 27001', 'Segurança da informação', 'infosec', COMP),
 'iso27701': ('ISO/IEC 27701', 'Gestão da privacidade da informação', 'infosec', None),
 'iso200001': ('ISO/IEC 20000-1', 'Gestão de serviços de TI', 'infosec', None),
 'iso42001': ('ISO/IEC 42001', 'Gestão de sistemas de inteligência artificial', 'infosec', None),            # NOVO
 'iso13485': ('ISO 13485', 'Gestão da qualidade de dispositivos médicos', 'qualidade', IMPL),
 'iso15189': ('ISO 15189', 'Qualidade e competência de laboratórios clínicos', 'qualidade', None),
 'iso14971': ('ISO 14971', 'Gestão de riscos de dispositivos médicos', 'qualidade', None),
 'iso28000': ('ISO 28000', 'Gestão de segurança, nascida na cadeia de suprimentos', 'compliance', None),
 'iso29001': ('ISO 29001', 'Gestão da qualidade em petróleo, petroquímica e gás natural', 'qualidade', None),
 'iso21001': ('ISO 21001', 'Gestão de organizações educacionais', 'qualidade', IMPL),
 'iso17025': ('ISO/IEC 17025', 'Competência de laboratórios de ensaio e calibração', 'qualidade', IMPL),
 'iso22301': ('ISO 22301', 'Continuidade de negócios', 'compliance', COMP),
 'iso31000': ('ISO 31000', 'Gestão de riscos', 'compliance', COMP),
 # seguranca de alimentos
 'iso22000': ('ISO 22000', 'Gestão da segurança de alimentos', 'alimentos', SEG),
 'fssc22000': ('FSSC 22000', 'Certificação reconhecida pela GFSI', 'alimentos', SEG),
 'brcgs': ('BRCGS', 'Padrão global de segurança de alimentos', 'alimentos', PADR),
 'ifs': ('IFS Food', 'Padrão de segurança de alimentos reconhecido pela GFSI', 'alimentos', None),            # NOVO
 'sqf': ('SQF', 'Padrão de segurança e qualidade de alimentos reconhecido pela GFSI', 'alimentos', None),    # NOVO
 'haccp': ('HACCP / APPCC', 'Análise de perigos e pontos críticos de controle', 'alimentos', SEG),
 'ppr': ('PPR', 'Programas de pré-requisitos', 'alimentos', SEG),
 'fooddefense': ('Food Defense', 'Proteção contra contaminação intencional', 'alimentos', SEG),
 # social, etica e sustentabilidade
 'smeta': ('SEDEX / SMETA', 'Auditoria ética da cadeia de suprimentos', 'social', 'sedex-smeta.html'),
 'sa8000': ('SA 8000', 'Responsabilidade social no trabalho', 'social', IMPL),
 'ifc': ('IFC Performance Standards', 'Padrão ambiental e social de bancos de desenvolvimento e financiadores', 'esg', 'ifc-performance-standards.html'),
 'ecovadis': ('EcoVadis', 'Avaliação de desempenho em sustentabilidade', 'esg', PADR),
 'fsc': ('FSC', 'Forest Stewardship Council, manejo florestal', 'ambiente', PADR),
 'rainforest': ('Rainforest Alliance', 'Selo de certificação agrícola sustentável', 'ambiente', PADR),
 'abntpr1004': ('ABNT PR 1004-1', 'Operação segura em organizações durante pandemias (diretrizes gerais, 2020)', 'compliance', PADR),
 'abntpr2030': ('ABNT PR 2030', 'ESG: conceitos, relato e avaliação', 'esg', 'esg.html'),
 # clima e carbono
 'ghgprotocol': ('GHG Protocol', 'Inventário de emissões e Programa Brasileiro GHG Protocol', 'clima', 'carbono-inventario-gee.html'),
 'iso14064': ('ISO 14064', 'Inventário e verificação de gases de efeito estufa', 'clima', 'carbono-inventario-gee.html'),
 'iso14067': ('ISO 14067', 'Pegada de carbono de produto', 'clima', 'carbono-pegada-produto.html'),
 'iso14040': ('ISO 14040', 'Avaliação do ciclo de vida', 'clima', 'carbono-pegada-produto.html'),
 'iso14025': ('ISO 14025', 'Declaração ambiental de produto', 'clima', 'carbono-pegada-produto.html'),
 'iso14068': ('ISO 14068', 'Neutralidade de carbono (sucessora da PAS 2060)', 'clima', 'carbono-neutralizacao.html'),   # 09/10/2026: a ISO 14068:2026 substituiu a 14068-1:2023
 'cdp': ('CDP', 'Relato ambiental a investidores e clientes', 'clima', 'carbono-inventario-gee.html'),
 'gri': ('GRI', 'Relato de sustentabilidade', 'esg', 'carbono-inventario-gee.html'),
 'sbti': ('SBTi', 'Metas de redução baseadas na ciência', 'clima', 'carbono-descarbonizacao.html'),
 'verra': ('Verra (VCS)', 'Padrão de créditos de carbono', 'clima', 'carbono-creditos.html'),
 'goldstandard': ('Gold Standard', 'Padrão de créditos de carbono', 'clima', 'carbono-creditos.html'),
 'sbce': ('SBCE', 'Sistema Brasileiro de Comércio de Emissões (Lei 15.042/2024)', 'clima', 'carbono-mercado-regulado.html'),
 'cbam': ('CBAM', 'Ajuste de carbono na fronteira da União Europeia', 'clima', 'carbono-mercado-regulado.html'),
 # programas setoriais e de mercado
 'iatf16949': ('IATF 16949', 'Qualidade na cadeia automotiva (autopeças)', 'qualidade', IMPL),
 'sassmaq': ('SASSMAQ', 'Avaliação de segurança, saúde, meio ambiente e qualidade no transporte de químicos (Abiquim)', 'compliance', None),
 'atuacao': ('Atuação Responsável', 'Programa da Abiquim para a indústria química', 'compliance', PADR),
 'oea': ('OEA', 'Operador Econômico Autorizado, programa da Receita Federal para a cadeia logística', 'compliance', None),   # NOVO
 'ona': ('ONA', 'Acreditação de serviços de saúde (Organização Nacional de Acreditação)', 'qualidade', None),             # NOVO
 # seguranca do trabalho e requisitos legais
 'nr01': ('NR-01 / PGR', 'Gerenciamento de riscos ocupacionais', 'sst', NRS),
 'nr10': ('NR-10', 'Segurança em instalações elétricas', 'sst', NRS),
 'nr12': ('NR-12', 'Segurança em máquinas e equipamentos', 'sst', NRS),
 'nr17': ('NR-17', 'Ergonomia', 'sst', NRS),
 'nr37': ('NR-37', 'Segurança e saúde em plataformas de petróleo', 'sst', NRS),
 'esocial': ('e-Social SST', 'Auditoria dos dados de saúde e segurança do trabalho', 'sst', NRS),
 'iso31022': ('ISO 31022', 'Gestão de riscos legais', 'compliance', NRS),
 'lgpd': ('LGPD', 'Proteção de dados pessoais (Lei 13.709/2018)', 'infosec', COMP),
 'eudr': ('EUDR', 'Regulamento da União Europeia contra o desmatamento', 'ambiente', 'estudos-regulatorios.html'),
 # 10/10/2026: entraram com o setor novo agro e florestal (PBQP-H, NR-18 e NR-35 sairam com Construcao). Sem entrada em
 # setores-revisoes.json ate a revisao vigente ser conferida em fonte primaria.
 'cerflor': ('Cerflor / PEFC', 'Certificação florestal brasileira, reconhecida pelo PEFC', 'ambiente', None),
 'rtrs': ('RTRS', 'Soja responsável (Round Table on Responsible Soy)', 'ambiente', None),
 'bonsucro': ('Bonsucro', 'Cana-de-açúcar e derivados produzidos de forma sustentável', 'ambiente', None),
 'globalgap': ('GlobalG.A.P.', 'Boas práticas agrícolas na produção primária', 'ambiente', None),
}

# normas em destaque na pagina de cada setor (lista curada). Quem esta em TRANSVERSAIS vale para todos os setores,
# mesmo sem aparecer na lista: o grafico, o filtro e o mosaico mostram em todos.
SETORES = [   # 10/10/2026: nove setores (aprovados pelo Leandro)
 ('industria', 'setor-industria.html', ['iso9001', 'iso14001', 'iso45001', 'iatf16949', 'iso50001', 'iso13485', 'iso22000', 'atuacao', 'iso37301', 'iso14064', 'iso14067', 'cbam', 'sbce', 'nr12', 'nr10', 'smeta', 'fsc', 'iso17025']),
 ('transporte', 'setor-transporte-rodovias.html', ['iso9001', 'iso14001', 'iso45001', 'iso39001', 'iso37001', 'iso37301', 'iso55001', 'iso22301', 'iso28000', 'sassmaq', 'oea']),   # 10/10: concessao de rodovia e transporte (CNAE 5221-4/00, secao H; EA 31)
 ('facilities', 'setor-facilities.html', ['iso41001', 'iso9001', 'iso14001', 'iso45001', 'iso55001', 'iso50001', 'iso22301', 'nr01', 'nr10', 'iso14064']),   # 10/10 (noite): no lugar de Construcao («nao trabalho com isso»); ISO 41001 e a especialidade do Leandro
 ('alimentos', 'setor-alimentos.html', ['iso9001', 'iso14001', 'iso45001', 'iso22000', 'fssc22000', 'haccp', 'ppr', 'brcgs', 'ifs', 'sqf', 'fooddefense', 'smeta', 'iso50001', 'eudr', 'rainforest']),
 ('agro', 'setor-agro-florestal.html', ['iso9001', 'iso14001', 'iso45001', 'fsc', 'cerflor', 'rtrs', 'bonsucro', 'globalgap', 'rainforest', 'eudr', 'iso14064', 'iso14067', 'smeta']),
 ('saude', 'setor-saude.html', ['iso9001', 'iso14001', 'iso45001', 'iso13485', 'iso14971', 'iso15189', 'iso27001', 'ona', 'lgpd']),
 ('energia', 'setor-energia.html', ['iso9001', 'iso14001', 'iso45001', 'iso50001', 'iso55001', 'iso29001', 'iso37001', 'nr10', 'nr37', 'iso14064', 'sbce', 'cbam']),
 ('tecnologia', 'setor-tecnologia.html', ['iso9001', 'iso14001', 'iso45001', 'iso27001', 'iso27701', 'iso200001', 'iso42001', 'iso22301', 'lgpd', 'iso56002']),
 ('servicos', 'setor-servicos-setor-publico.html', ['iso9001', 'iso14001', 'iso45001', 'iso37001', 'iso37301', 'iso21001', 'iso17025', 'sa8000', 'smeta', 'nr01', 'lgpd']),
]

# valem para qualquer setor: normas genericas de sistema de gestao, programas de cadeia, clima e requisitos legais gerais
TRANSVERSAIS = ['iso9001', 'iso14001', 'iso45001', 'iso27001', 'iso27701', 'iso50001', 'iso56002', 'iso14064', 'iso28000',
                'iso37001', 'iso37301', 'iso55001', 'iso22301', 'iso31000', 'iso31022', 'smeta', 'sa8000', 'ifc',
                'ecovadis', 'abntpr1004', 'abntpr2030', 'ghgprotocol', 'iso14067', 'iso14040', 'iso14025',
                'iso14068', 'cdp', 'gri', 'sbti', 'verra', 'goldstandard', 'nr01', 'nr17', 'esocial', 'lgpd']
# 10/10/2026: ISO 39001, ISO/IEC 20000-1 e ISO/IEC 42001 sairam das transversais. O ISO Survey 2025 mostra 96% da
# 20000-1 e 92% da 42001 em TI, e a 39001 em transporte (50%) e construcao (17%): ficam so nos setores em destaque.

# 10/10/2026: a linha «Outros setores» acabou; facilities, educacao e laboratorios entraram em Servicos e setor publico
FORA = {}

# id: (designacao com a revisao vigente, titulo oficial em portugues ou, sem ele, no original). Conferido em fonte
# primaria; o arquivo _ferramentas/setores-revisoes.json guarda a fonte de cada linha. Sem entrada, o grafico mostra
# o nome e a descricao de NORMAS.
REVISOES_ARQ = os.path.join(AQUI, 'setores-revisoes.json')
REVISOES = json.load(open(REVISOES_ARQ, encoding='utf-8')) if os.path.exists(REVISOES_ARQ) else {}


def info(k):
    r = REVISOES.get(k) or {}
    return (r.get('designacao') or NORMAS[k][0], r.get('titulo') or NORMAS[k][1])


TEXTOS = json.load(open(os.path.join(AQUI, 'setores-textos.json'), encoding='utf-8'))
ORDEM_G = [g[0] for g in GRUPOS]


def ler(p):
    with open(os.path.join(SITE, p), encoding='utf-8', newline='') as f: return f.read()


def gravar(p, s):
    with open(os.path.join(SITE, p), 'w', encoding='utf-8', newline='') as f: f.write(s)


def ordem():
    return sorted(NORMAS, key=lambda k: (ORDEM_G.index(NORMAS[k][2]), list(NORMAS).index(k)))


def setores_da(k):
    return [i for i, _, ns in SETORES if k in ns]


def dados_js():
    setores = [{'id': i, 'nome': TEXTOS[i]['nome'], 'pagina': pg, 'resumo': TEXTOS[i]['resumo'], 'normas': ns} for i, pg, ns in SETORES]
    normas = {k: {'nome': v[0], 'desc': v[1], 'grupo': v[2], 'pagina': v[3], 'setores': setores_da(k), 'todos': k in TRANSVERSAIS, 'fora': FORA.get(k, '')}
              for k, v in NORMAS.items()}
    obj = {'setores': setores, 'normas': normas, 'ordemNormas': ordem(), 'transversais': TRANSVERSAIS,
           'grupos': [{'id': g, 'nome': n} for g, n, _ in GRUPOS]}
    return ('/* Gerado por _ferramentas/setores.py (09/10/2026). Nao editar a mao. */\n'
            'window.IM_SETORES=' + json.dumps(obj, ensure_ascii=False, separators=(',', ':')) + ';\n')


def cartao_norma(k):
    nome, desc, _, pg = NORMAS[k]
    if pg:
        return '<a class="pos-card pos-card--link" href="%s"><h4>%s</h4><p>%s</p><span class="pos-more">Ver serviço &rarr;</span></a>' % (pg, nome, desc)
    return '<div class="pos-card"><h4>%s</h4><p>%s</p></div>' % (nome, desc)


def chip_norma(k):
    nome, desc, _, pg = NORMAS[k]
    return '<li title="%s">%s</li>' % (desc, ('<a href="%s">%s</a>' % (pg, nome)) if pg else nome)


# 17/10/2026: «dentro da divisao industria, pode colocar servicos de inspecoes (este tipo de servico faz parte da
# industria)». Servicos (nao normas) que entram na pagina do setor, logo depois das certificacoes. Textos das
# descricoes vem da propria pagina inspecoes.html.
SERVICOS_SETOR = {
 'industria': ('Serviços de inspeção', [
   ('Inspeção pré-embarque', 'Lote verificado depois da produção e antes do carregamento, contra a especificação acordada.', 'inspecoes.html'),
   ('Monitoramento de carregamento', 'Embarque acompanhado da conferência inicial ao lacre do container.', 'inspecoes.html'),
   ('Inspeção de fábrica', 'Infraestrutura, processos e sistema de gestão do fornecedor avaliados no local.', 'inspecoes.html'),
   ('Produtos inspecionados', 'Abrangência de produtos que a equipe de inspeção verifica.', 'produtos-inspecionamos.html')]),
}


def miolo(i, pg, normas):
    """Pagina de setor enxuta (11/10/2026, pedido do Leandro: «menos conteudo escrito» e as explicacoes num FAQ no fim).
    Abertura de uma frase e paragrafo curto; cartoes das normas por tema, so com o rotulo do grupo; recolhivel das
    transversais; entregas de uma linha; uma linha para os estudos (a lista de `estudos` do json fica guardada, fora da
    pagina); perguntas frequentes (campo `faq`) no componente unico do site (.faq / .faq-item); outros setores; contato."""
    t = TEXTOS[i]
    h = ['<div class="content">',
         '<p class="abre">%s</p>' % t['abre'],
         '<p>%s</p>' % t['para'],
         '<h3>Certificações e reconhecimentos do setor</h3>']
    for g, rot, _sub in GRUPOS:
        ks = [k for k in normas if NORMAS[k][2] == g]
        if not ks: continue
        h.append('<div class="stp-grupo"><span>%s</span><em>%02d</em></div>' % (rot, len(ks)))
        h.append('<div class="stp-grade">')
        h.extend('  ' + cartao_norma(k) for k in ks)
        h.append('</div>')
    if i in SERVICOS_SETOR:
        rot, itens = SERVICOS_SETOR[i]
        h.append('<div class="stp-grupo"><span>%s</span><em>%02d</em></div>' % (rot, len(itens)))
        h.append('<div class="stp-grade">')
        h.extend('  <a class="pos-card pos-card--link" href="%s"><h4>%s</h4><p>%s</p><span class="pos-more">Ver serviço &rarr;</span></a>'
                 % (hr, t2, d) for t2, d, hr in itens)
        h.append('</div>')
    tr = [k for k in ordem() if k in TRANSVERSAIS and k not in normas]
    h.append('<details class="stp-transv"><summary><span>Valem para qualquer setor</span><em>%02d</em></summary>' % len(tr))
    h.append('<ul class="stp-chips">' + ''.join(chip_norma(k) for k in tr) + '</ul></details>')
    h.append('<h3>O que a Ideal Metrics entrega</h3>')
    h.append('<div class="numbered-items">')
    for n, (tit, txt) in enumerate(t['entregas'], 1):
        h.append('<div class="numbered-item"><div class="num">%02d</div><div><h4>%s</h4><p>%s</p></div></div>' % (n, tit, txt))
    h.append('</div>')
    h.append('<p>Estudos e pesquisa aplicada para o setor: <a href="estudos-pesquisa.html">divisão de Estudos e Pesquisa Aplicada</a>. Método de trabalho: <a href="como-trabalhamos.html">Como trabalhamos</a>.</p>')
    h.append('<h3 id="perguntas">Perguntas frequentes</h3>')
    h.append('<div class="faq">')
    h.extend('  <details class="faq-item"><summary>%s</summary><p>%s</p></details>' % (q, r) for q, r in t['faq'])
    h.append('</div>')
    h.append('<h3>Outros setores</h3>')
    h.append('<div class="stp-outros">')
    for j, pg2, _ in SETORES:
        if j != i: h.append('  <a href="%s"><b>%s</b><span>Ver setor</span></a>' % (pg2, TEXTOS[j]['nome']))
    h.append('</div>')
    h.append('<a href="contato.html" class="link-arrow">Contato com a equipe técnica &rarr;</a>')
    h.append('</div>')
    return '\n'.join(h)


def liga_css(s):
    tag = '<link rel="stylesheet" href="css/setores.css?v=%s">' % CSS_V
    s = re.sub(r'<link rel="stylesheet" href="css/setores\.css\?v=\d+">\n?', '', s)
    return s.replace('</head>', tag + '\n</head>', 1)


def matriz():
    """Modelo 1 do grafico da home: grade estatica (SVG), setores nas linhas e normas nas colunas, agrupadas; um
    quadrado liga o setor a norma. Ultima linha = o que vale para qualquer setor (quadrado mais claro). Largura da
    pagina inteira. So quadrados e linha fina (sem circulos). Rotulo de linha leva a pagina do setor; rotulo de coluna, a
    pagina do servico quando existe. js/setores-matriz.js acende a linha e a coluna sob o mouse."""
    PASSO, QUAD, ROT_L, TOPO, LIN_H, GAP = 19, 13, 206, 172, 25, 14   # 10/10: rotulo de linha mais largo (nove setores)
    CURTO_G = {'qualidade': 'Qualidade', 'ambiente': 'Meio ambiente', 'sst': 'Saúde e segurança', 'viaria': 'Segurança viária', 'clima': 'Clima e carbono',
               'esg': 'ESG', 'social': 'Social e cadeia', 'alimentos': 'Segurança de alimentos', 'infosec': 'Segurança da informação', 'compliance': 'Compliance e riscos'}
    CURTO_S = {'industria': 'Indústria', 'facilities': 'Facilities', 'transporte': 'Transporte e rodovias', 'alimentos': 'Alimentos',
               'agro': 'Agro e florestal', 'saude': 'Saúde', 'energia': 'Energia e utilities', 'tecnologia': 'Tecnologia e financeiro', 'servicos': 'Serviços e setor público'}
    CURTO_N = {'ifc': 'IFC Perf. Standards', 'fooddefense': 'Food Defense', 'atuacao': 'Atuação Responsável'}
    cols = []; x = ROT_L; grupos = []
    for g, _rot, _ in GRUPOS:
        ids = [k for k in ordem() if NORMAS[k][2] == g]
        x0 = x
        for k in ids:
            cols.append((k, x + PASSO / 2)); x += PASSO
        grupos.append((CURTO_G[g], x0, x - 2))
        x += GAP
    linhas = list(SETORES)   # 10/10: sem a linha «Outros setores»
    larg = int(x - GAP + 6); alt = TOPO + LIN_H * len(linhas) + 4
    esc = lambda s: s.replace('&', '&amp;')
    o = ['<figure class="qc-mat" id="qcMat" aria-labelledby="qcMatTit">',
         '  <div class="qc-mat-topo"><span id="qcMatTit">Normas e padrões por setor</span><span>[ IM.S ]</span></div>',
         '  <div class="qc-mat-rola"><svg viewBox="0 0 %d %d" width="%d" height="%d" role="img" aria-label="Grade que liga cada setor às normas e padrões aplicáveis">' % (larg, alt, larg, alt)]
    # 12/10/2026: «os nomes que nao couberam nas colunas ficam acima, com um pequeno traco indicando a que se referem».
    # O rotulo (mono 9,5 px, entreletra ,14em: ~7,05 px por letra) que nao cabe ate o rotulo do grupo seguinte sobe para
    # uma linha nova acima dos rotulos (CHAMA px a mais no alto); um traco sai de um quadradinho na linha do grupo, sobe e
    # vai para a direita ate o rotulo (so quadrados e retas, como o resto do grafico). Rotulos de chamada nao se encostam:
    # cada um comeca depois do anterior.
    CHAMA = 22
    cabe_n = lambda rot, x0, x1: len(rot) * 7.05 <= (x1 + 2 + GAP - x0) - 10
    chamadas = [(rot, x0, x1) for rot, x0, x1 in grupos if not cabe_n(rot, x0, x1)]
    dy = CHAMA if chamadas else 0
    if dy:
        o[-1] = o[-1].replace('viewBox="0 0 %d %d" width="%d" height="%d"' % (larg, alt, larg, alt),
                              'viewBox="0 0 %d %d" width="%d" height="%d"' % (larg, alt + dy, larg, alt + dy))
        fim_ant = -1e9
        for rot, x0, x1 in chamadas:
            xa = x0 + min(8, (x1 - x0) / 2); xl = max(xa + 14, fim_ant + 18)
            fim_ant = xl + 4 + len(rot) * 7.05
            o.append('    <g class="gr chama"><rect x="%.1f" y="%.1f" width="3" height="3"/><path class="tr" d="M%.1f %.1fV7.5H%.1f"/>'
                     '<text x="%.1f" y="11">%s</text></g>' % (xa - 1.5, dy + 15.5, xa, dy + 15.5, xl, xl + 4, esc(rot)))
        o.append('    <g transform="translate(0 %d)">' % dy)
    for rot, x0, x1 in grupos:
        if (rot, x0, x1) in chamadas:
            o.append('    <g class="gr"><path d="M%s 17H%s"/></g>' % (x0, x1))
        else:
            o.append('    <g class="gr"><text x="%s" y="11">%s</text><path d="M%s 17H%s"/></g>' % (x0, esc(rot), x0, x1))
    for k, cx in cols:
        nome, _, _, pg = NORMAS[k]
        txt = '<text transform="translate(%s %s) rotate(-90)">%s</text>' % (cx + 3.5, TOPO - 8, esc(CURTO_N.get(k, nome)))
        dz, tt = info(k)
        o.append('    <g class="co" data-n="%s" data-rev="%s" data-tit="%s">%s</g>' % (k, esc(dz).replace('"', '&quot;'), esc(tt).replace('"', '&quot;'), ('<a href="%s">%s</a>' % (pg, txt)) if pg else txt))
    for r, (i, pg, normas) in enumerate(linhas):
        y = TOPO + r * LIN_H
        rot = ('<a href="%s"><text class="rs" x="0" y="%s">%s</text></a>' % (pg, y + 17, esc(CURTO_S.get(i, TEXTOS[i]['nome'])))) if pg else \
              '<text class="rs" x="0" y="%s">Outros setores</text>' % (y + 17)
        o.append('    <g class="li" data-s="%s"><path class="fio" d="M0 %s H%s"/>%s' % (i, y, larg, rot))
        for k, cx in cols:
            nome_s = TEXTOS[i]['nome'] if pg else FORA.get(k, 'Outros setores')
            if k in normas:
                o.append('      <rect class="q" data-n="%s" x="%s" y="%s" width="%d" height="%d" rx="3"><title>%s: %s</title></rect>' % (k, cx - QUAD / 2, y + (LIN_H - QUAD) / 2, QUAD, QUAD, esc(nome_s), esc(NORMAS[k][0])))
            elif pg and k in TRANSVERSAIS:
                o.append('      <rect class="q t" data-n="%s" x="%s" y="%s" width="%d" height="%d" rx="3"><title>%s: %s (vale para qualquer setor)</title></rect>' % (k, cx - QUAD / 2, y + (LIN_H - QUAD) / 2, QUAD, QUAD, esc(nome_s), esc(NORMAS[k][0])))
            else:
                o.append('      <rect class="v" x="%s" y="%s" width="2" height="2"/>' % (cx - 1, y + LIN_H / 2 - 1))
        o.append('    </g>')
    o.append('    <path class="fio" d="M0 %s H%s"/>' % (TOPO + LIN_H * len(linhas), larg))
    if dy: o.append('    </g>')
    o.append('  </svg></div>')
    o.append('  <button class="qc-mat-aba" id="qcMatAba" type="button" aria-expanded="false" aria-controls="qcMat">'
             '<svg viewBox="0 0 22 14" aria-hidden="true"><path d="M3 0l3 3-3 3-3-3zM11 0l3 3-3 3-3-3zM19 0l3 3-3 3-3-3zM3 8l3 3-3 3-3-3zM11 8l3 3-3 3-3-3zM19 8l3 3-3 3-3-3z"/></svg>'
             '<span class="qc-mat-aba-txt"><b>[ %02d ]</b>&nbsp;&nbsp;<i class="qc-mat-abre">Expandir</i><i class="qc-mat-fecha">Recolher</i></span></button>' % len(cols))
    o.append('  <p class="qc-mat-info" id="qcMatInfo" aria-live="polite"></p>')
    o.append('</figure>')
    return '<!-- relacao setor norma -->\n' + '\n'.join(o) + '\n<!-- fim relacao setor norma -->'


def mosaico():
    """Grafico da home: todas as normas e padroes em retangulos, agrupados; os botoes acendem o que vale para o setor.
    Escuro = especifico do setor; contorno forte = vale para qualquer setor. So retangulos, sem circulos."""
    o = ['<figure class="qc-mos" id="qcMos">',
         '  <div class="qc-mos-topo"><span>Normas e padrões que atendemos</span><span>[ IM.S ]</span></div>',
         '  <div class="qc-mos-bt" role="group" aria-label="Acender as normas de um setor">',
         '    <button type="button" data-s="" aria-pressed="true">Todos</button>']
    for i, _, _ in SETORES:
        o.append('    <button type="button" data-s="%s" aria-pressed="false">%s</button>' % (i, TEXTOS[i]['nome']))
    o.append('  </div>')
    for g, rot, _ in GRUPOS:
        ks = [k for k in ordem() if NORMAS[k][2] == g]
        o.append('  <div class="qc-mos-grupo"><h4><span>%s</span><em>%02d</em></h4><ul>' % (rot, len(ks)))
        for k in ks:
            nome, desc, _, pg = NORMAS[k]
            ds = '*' if k in TRANSVERSAIS else (' '.join(setores_da(k)) or '-')
            desc = desc + (' (só para ' + FORA[k].lower() + ')' if k in FORA else '')
            conteudo = ('<a href="%s">%s</a>' % (pg, nome)) if pg else nome
            o.append('    <li data-s="%s" title="%s">%s</li>' % (ds, desc.replace('"', '&quot;'), conteudo))
        o.append('  </ul></div>')
    o.append('  <figcaption>Com um setor selecionado, o quadro escuro é o que vale só para ele; o contorno, o que vale para qualquer setor. Os nomes levam às páginas dos serviços.</figcaption>')
    o.append('</figure>')
    return '<!-- relacao setor norma -->\n' + '\n'.join(o) + '\n<!-- fim relacao setor norma -->'


def estrutura(s):
    """A frase de «O que fazemos» fecha a coluna do texto; o grafico entra na linha inteira logo abaixo; a figura dos
    temas e o logo vertical passam para a cauda (terco direito). Idempotente."""
    if 'qc-abre-cauda' in s: return s
    i = s.index('<p class="qc-lead"'); j = s.index('</p>', i) + 4
    return s[:j] + '\n        </div>\n        <div class="qc-abre-cauda">' + s[j:]


def poe_relacao(s):
    s = estrutura(s)
    s = re.sub(r'[ \t]*<!-- relacao setor norma -->.*?<!-- fim relacao setor norma -->\n?', '', s, flags=re.S)
    ancora = '        <div class="qc-abre-cauda">'
    assert s.count(ancora) == 1
    bloco, js = (matriz(), 'setores-matriz') if MODELO_HOME == 'matriz' else (mosaico(), 'setores-mosaico')
    s = s.replace(ancora, bloco + '\n' + ancora, 1)
    s = re.sub(r'<script src="js/setores-(?:matriz|mosaico)\.js[^>]*></script>\n?', '', s)
    return s.replace('</body>', '<script src="js/%s.js?v=%s"></script>\n</body>' % (js, JS_V), 1)


FILTRO = '''<!-- filtro setor norma -->
<section class="stf" id="stf" aria-labelledby="stfTit">
  <div class="stf-topo">
    <h3 class="stf-tit" id="stfTit">Busca por setor ou por norma</h3>
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


DADOS = '<script src="js/setores-dados.js?v=%s"></script>' % JS_V


def poe_filtro(s, ancora, depois, filtro=True):
    """filtro=False (a home, desde 14/10/2026: «pode tirar esta parte, Busca por setor ou por norma»): tira o filtro e
    o script dele, mas deixa os dados, que a grade dos setores do Guia (js/guia-foto.js, js/guia-rota.js) usa.
    Tira tambem as copias repetidas dos dois scripts que ficaram de rodadas antigas (com CRLF o padrao antigo nao
    casava e cada rodada deixava mais um par)."""
    s = re.sub(r'<!-- filtro setor norma -->.*?<!-- fim filtro setor norma -->\r?\n?', '', s, flags=re.S)
    s = re.sub(r'(?:<script src="js/setores-(?:dados|filtro)\.js[^>]*></script>\s*)+', '', s)
    if not filtro:
        return s.replace('</body>', DADOS + '\n</body>', 1)
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
    s = ler('index.html')
    s = liga_css(s)
    s = poe_filtro(s, '<p class="st-lead">Atendemos os mais diversos segmentos produtivos.</p>', True, filtro=False)
    s = poe_relacao(s)
    gravar('index.html', s)
    s = ler('servicos.html')
    s = liga_css(s)
    s = poe_filtro(s, '<h2>PADRÕES E CONFORMIDADE</h2>', False)
    gravar('servicos.html', s)
    print('ok: %d setores, %d normas, %d transversais' % (len(SETORES), len(NORMAS), len(TRANSVERSAIS)))


if __name__ == '__main__':
    main()
