# -*- coding: utf-8 -*-
"""Setores x normas (09/10/2026). Fonte unica dos dados e gerador.

    python _ferramentas/setores.py

Faz, de forma idempotente:
  1. grava js/setores-dados.js (window.IM_SETORES), lido pelo filtro (js/setores-filtro.js);
  2. reescreve o miolo (<div class="content">) das seis paginas setor-*.html;
  3. poe o filtro na home (secao Setores de atuacao) e em servicos.html, entre marcadores;
  4. poe na home, logo abaixo da frase de «O que fazemos», o mosaico de normas e padroes (js/setores-mosaico.js);
  5. liga css/setores.css nas oito paginas e os scripts onde cabem.

Tres situacoes para cada norma: de um ou mais setores (lista em SETORES), de qualquer setor (TRANSVERSAIS) ou de
nenhum dos seis (as demais). O catalogo inteiro vem do que o proprio site ja cita: implantacao-iso, padroes-mercado,
compliance, NRs, ESG, carbono e seguranca de alimentos. Os textos de abertura, entregas e estudos de cada setor vem de
_ferramentas/setores-textos.json. Norma sem pagina de servico aparece sem link; quando a pagina nascer, basta pôr o
endereco em NORMAS e rodar de novo. Itens # NOVO entraram em 09/10/2026 e # CONFERIR tem descricao a validar."""
import os, re, json

AQUI = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(AQUI)
CSS_V, JS_V = '9', '2'

GRUPOS = [
 ('iso', 'Sistemas de gestão ISO', 'Normas ISO que a organização pode certificar.'),
 ('alimentos', 'Segurança de alimentos', 'Normas, esquemas reconhecidos pela GFSI e programas técnicos.'),
 ('social', 'Social, ética e sustentabilidade', 'Programas e padrões exigidos por clientes, investidores e financiadores.'),
 ('clima', 'Clima e carbono', 'Inventário, pegada, neutralização, metas, créditos e mercado regulado.'),
 ('mercado', 'Programas setoriais e de mercado', 'Exigidos por montadoras, embarcadores, contratantes e órgãos de acreditação.'),
 ('legal', 'Segurança do trabalho e requisitos legais', 'Obrigações legais e regulamentos que sustentam os sistemas acima.'),
]

IMPL, COMP, SEG, PADR, NRS = ('implantacao-iso.html', 'compliance-seguranca-informacao.html', 'seguranca-alimentos.html',
                              'padroes-mercado.html', 'nrs.html')

# id: (nome, descricao, grupo, pagina do servico ou None)
NORMAS = {
 # sistemas de gestao ISO
 'iso9001': ('ISO 9001', 'Gestão da qualidade', 'iso', 'norma-iso-9001.html'),
 'iso14001': ('ISO 14001', 'Gestão ambiental', 'iso', 'norma-iso-14001.html'),
 'iso45001': ('ISO 45001', 'Saúde e segurança ocupacional', 'iso', 'norma-iso-45001.html'),
 'iso39001': ('ISO 39001', 'Segurança viária', 'iso', 'seguranca-viaria.html'),
 'iso41001': ('ISO 41001', 'Gestão de facilities', 'iso', IMPL),
 'iso37001': ('ISO 37001', 'Gestão antissuborno', 'iso', COMP),
 'iso37301': ('ISO 37301', 'Gestão de compliance', 'iso', COMP),
 'iso56002': ('ISO 56002', 'Gestão da inovação', 'iso', IMPL),
 'iso50001': ('ISO 50001', 'Gestão de energia', 'iso', IMPL),
 'iso55001': ('ISO 55001', 'Gestão de ativos', 'iso', IMPL),
 'iso27001': ('ISO/IEC 27001', 'Segurança da informação', 'iso', COMP),
 'iso27701': ('ISO/IEC 27701', 'Gestão da privacidade da informação', 'iso', None),
 'iso200001': ('ISO/IEC 20000-1', 'Gestão de serviços de TI', 'iso', None),
 'iso42001': ('ISO/IEC 42001', 'Gestão de sistemas de inteligência artificial', 'iso', None),            # NOVO
 'iso13485': ('ISO 13485', 'Gestão da qualidade de dispositivos médicos', 'iso', IMPL),
 'iso15189': ('ISO 15189', 'Qualidade e competência de laboratórios clínicos', 'iso', None),
 'iso14971': ('ISO 14971', 'Gestão de riscos de dispositivos médicos', 'iso', None),
 'iso28000': ('ISO 28000', 'Segurança da cadeia de suprimentos', 'iso', None),
 'iso29001': ('ISO 29001', 'Gestão da qualidade em petróleo, petroquímica e gás natural', 'iso', None),
 'iso21001': ('ISO 21001', 'Gestão de organizações educacionais', 'iso', IMPL),
 'iso17025': ('ISO/IEC 17025', 'Competência de laboratórios de ensaio e calibração', 'iso', IMPL),
 'iso22301': ('ISO 22301', 'Continuidade de negócios', 'iso', COMP),
 'iso31000': ('ISO 31000', 'Gestão de riscos', 'iso', COMP),
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
 'ifc': ('IFC Performance Standards', 'Padrão ambiental e social de bancos de desenvolvimento e financiadores', 'social', 'ifc-performance-standards.html'),
 'ecovadis': ('EcoVadis', 'Avaliação de desempenho em sustentabilidade', 'social', PADR),
 'fsc': ('FSC', 'Forest Stewardship Council, manejo florestal', 'social', PADR),
 'rainforest': ('Rainforest Alliance', 'Selo de certificação agrícola sustentável', 'social', PADR),
 'iqg': ('IQG', 'Programa de mercado', 'social', PADR),                                                        # CONFERIR descricao
 'abntpr1004': ('ABNT PR 1004-1', 'Prática recomendada da ABNT (2020)', 'social', PADR),                       # CONFERIR descricao
 'abntpr2030': ('ABNT PR 2030', 'ESG: conceitos, relato e avaliação', 'social', 'esg.html'),
 # clima e carbono
 'ghgprotocol': ('GHG Protocol', 'Inventário de emissões e Programa Brasileiro GHG Protocol', 'clima', 'carbono-inventario-gee.html'),
 'iso14064': ('ISO 14064', 'Inventário e verificação de gases de efeito estufa', 'clima', 'carbono-inventario-gee.html'),
 'iso14067': ('ISO 14067', 'Pegada de carbono de produto', 'clima', 'carbono-pegada-produto.html'),
 'iso14040': ('ISO 14040', 'Avaliação do ciclo de vida', 'clima', 'carbono-pegada-produto.html'),
 'iso14025': ('ISO 14025', 'Declaração ambiental de produto', 'clima', 'carbono-pegada-produto.html'),
 'iso14068': ('ISO 14068-1', 'Neutralidade de carbono', 'clima', 'carbono-neutralizacao.html'),
 'pas2060': ('PAS 2060', 'Neutralidade de carbono', 'clima', 'carbono-neutralizacao.html'),
 'cdp': ('CDP', 'Relato ambiental a investidores e clientes', 'clima', 'carbono-inventario-gee.html'),
 'gri': ('GRI', 'Relato de sustentabilidade', 'clima', 'carbono-inventario-gee.html'),
 'sbti': ('SBTi', 'Metas de redução baseadas na ciência', 'clima', 'carbono-descarbonizacao.html'),
 'verra': ('Verra (VCS)', 'Padrão de créditos de carbono', 'clima', 'carbono-creditos.html'),
 'goldstandard': ('Gold Standard', 'Padrão de créditos de carbono', 'clima', 'carbono-creditos.html'),
 'sbce': ('SBCE', 'Sistema Brasileiro de Comércio de Emissões (Lei 15.042/2024)', 'clima', 'carbono-mercado-regulado.html'),
 'cbam': ('CBAM', 'Ajuste de carbono na fronteira da União Europeia', 'clima', 'carbono-mercado-regulado.html'),
 # programas setoriais e de mercado
 'iatf16949': ('IATF 16949', 'Qualidade na cadeia automotiva (autopeças)', 'mercado', IMPL),
 'sassmaq': ('SASSMAQ', 'Avaliação de segurança, saúde, meio ambiente e qualidade no transporte de químicos (Abiquim)', 'mercado', None),
 'atuacao': ('Atuação Responsável', 'Programa da Abiquim para a indústria química', 'mercado', PADR),
 'oea': ('OEA', 'Operador Econômico Autorizado, programa da Receita Federal para a cadeia logística', 'mercado', None),   # NOVO
 'ona': ('ONA', 'Acreditação de serviços de saúde (Organização Nacional de Acreditação)', 'mercado', None),             # NOVO
 # seguranca do trabalho e requisitos legais
 'nr01': ('NR-01 / PGR', 'Gerenciamento de riscos ocupacionais', 'legal', NRS),
 'nr10': ('NR-10', 'Segurança em instalações elétricas', 'legal', NRS),
 'nr12': ('NR-12', 'Segurança em máquinas e equipamentos', 'legal', NRS),
 'nr17': ('NR-17', 'Ergonomia', 'legal', NRS),
 'nr37': ('NR-37', 'Segurança e saúde em plataformas de petróleo', 'legal', NRS),
 'esocial': ('e-Social SST', 'Auditoria dos dados de saúde e segurança do trabalho', 'legal', NRS),
 'iso31022': ('ISO 31022', 'Gestão de riscos legais', 'legal', NRS),
 'lgpd': ('LGPD', 'Proteção de dados pessoais (Lei 13.709/2018)', 'legal', COMP),
 'eudr': ('EUDR', 'Regulamento da União Europeia contra o desmatamento', 'legal', 'estudos-regulatorios.html'),
}

# normas de cada setor (as seis paginas ja existiam; ver # NOVO acima)
SETORES = [
 ('industria', 'setor-industria.html', ['iso9001', 'iatf16949', 'iso14001', 'iso45001', 'iso50001', 'iso14064', 'nr12', 'nr10', 'atuacao']),
 ('logistica', 'setor-logistica.html', ['iso9001', 'iso39001', 'iso14001', 'iso45001', 'iso28000', 'sassmaq', 'oea']),
 ('alimentos', 'setor-alimentos.html', ['iso22000', 'fssc22000', 'haccp', 'brcgs', 'ppr', 'fooddefense', 'ifs', 'sqf', 'eudr']),
 ('saude', 'setor-saude.html', ['iso13485', 'iso9001', 'iso15189', 'iso14971', 'iso27001', 'ona']),
 ('tecnologia', 'setor-tecnologia.html', ['iso27001', 'iso27701', 'iso200001', 'iso9001', 'iso56002', 'iso42001']),
 ('energia', 'setor-energia.html', ['iso50001', 'iso29001', 'iso14001', 'iso45001', 'nr37', 'iso14064']),
]

# valem para qualquer setor (nao pertencem a um setor so)
TRANSVERSAIS = ['iso41001', 'iso37001', 'iso37301', 'iso55001', 'iso22301', 'iso31000', 'iso31022', 'smeta', 'sa8000', 'ifc',
                'ecovadis', 'fsc', 'rainforest', 'iqg', 'abntpr1004', 'abntpr2030', 'ghgprotocol', 'iso14067', 'iso14040',
                'iso14025', 'iso14068', 'pas2060', 'cdp', 'gri', 'sbti', 'verra', 'goldstandard', 'sbce', 'cbam',
                'nr01', 'nr17', 'esocial', 'lgpd']
# ISO 21001 (educacao) e ISO/IEC 17025 (laboratorios) ficam fora dos seis setores: nem lista de setor nem transversal.

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
    normas = {k: {'nome': v[0], 'desc': v[1], 'grupo': v[2], 'pagina': v[3], 'setores': setores_da(k), 'todos': k in TRANSVERSAIS}
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


def miolo(i, pg, normas):
    t = TEXTOS[i]
    h = ['<div class="content">',
         '<p class="abre">%s</p>' % t['abre'],
         '<p>%s</p>' % t['para'],
         '<h3>Certificações e reconhecimentos do setor</h3>',
         '<p class="stp-nota">Programas que clientes, contratantes e órgãos reguladores esperam das organizações do setor. A Ideal Metrics implanta cada um e prepara a organização para a avaliação. Os cartões com seta levam à página do serviço.</p>']
    for g, rot, sub in GRUPOS:
        ks = [k for k in normas if NORMAS[k][2] == g]
        if not ks: continue
        h.append('<div class="stp-grupo"><span>%s</span><em>%02d</em></div>' % (rot, len(ks)))
        h.append('<p class="stp-nota">%s</p>' % sub)
        h.append('<div class="stp-grade">')
        h.extend('  ' + cartao_norma(k) for k in ks)
        h.append('</div>')
    tr = [k for k in ordem() if k in TRANSVERSAIS]
    h.append('<details class="stp-transv"><summary><span>Valem para qualquer setor</span><em>%02d</em></summary>' % len(tr))
    h.append('<p class="stp-nota">Padrões que a Ideal Metrics atende em organizações de qualquer setor, como SEDEX/SMETA, IFC, EcoVadis, normas de carbono e a LGPD.</p>')
    h.append('<ul class="stp-chips">' + ''.join(chip_norma(k) for k in tr) + '</ul></details>')
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
            conteudo = ('<a href="%s">%s</a>' % (pg, nome)) if pg else nome
            o.append('    <li data-s="%s" title="%s">%s</li>' % (ds, desc.replace('"', '&quot;'), conteudo))
        o.append('  </ul></div>')
    o.append('  <figcaption>Escolha um setor: o quadro escuro é o que vale só para ele; o contorno, o que vale para qualquer setor. Os nomes levam às páginas dos serviços.</figcaption>')
    o.append('</figure>')
    return '<!-- relacao setor norma -->\n' + '\n'.join(o) + '\n<!-- fim relacao setor norma -->'


def poe_mosaico(s):
    s = re.sub(r'[ \t]*<!-- relacao setor norma -->.*?<!-- fim relacao setor norma -->\n?', '', s, flags=re.S)
    ancora = '<figure class="qc-temas"'
    assert s.count(ancora) == 1
    s = s.replace(ancora, mosaico() + '\n          ' + ancora, 1)
    s = re.sub(r'<script src="js/setores-(?:matriz|mosaico)\.js[^>]*></script>\n?', '', s)
    return s.replace('</body>', '<script src="js/setores-mosaico.js?v=%s"></script>\n</body>' % JS_V, 1)


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
    s = ler('index.html')
    s = liga_css(s)
    s = poe_filtro(s, '<p class="st-lead">Atendemos os mais diversos segmentos produtivos.</p>', True)
    s = poe_mosaico(s)
    gravar('index.html', s)
    s = ler('servicos.html')
    s = liga_css(s)
    s = poe_filtro(s, '<h2>PADRÕES E CONFORMIDADE</h2>', False)
    gravar('servicos.html', s)
    print('ok: %d setores, %d normas, %d transversais' % (len(SETORES), len(NORMAS), len(TRANSVERSAIS)))


if __name__ == '__main__':
    main()
