# -*- coding: utf-8 -*-
"""Blocos compartilhados do site Ideal Metrics, na arquitetura do mapa estrategico
v1.1: duas divisoes. PADROES E CONFORMIDADE (dez temas, em tres colunas de menu
para caber) e ESTUDOS E PESQUISA APLICADA (quatro temas).

O menu, a navegacao lateral e o rodape sao copiados pagina a pagina no site; aqui
moram numa fonte so, e o aplica.py grava em todas."""
import os, re

SITE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '')

_EOL = {}
def ler(nome):
    """Devolve o texto com LF e guarda o fim de linha de origem. O site e CRLF,
    mas stal/ e lp-carbono/ nao sao: cada arquivo volta como veio."""
    raw = open(os.path.join(SITE, nome), 'rb').read()
    crlf, lf = raw.count(b'\r\n'), raw.count(b'\n')
    assert crlf in (0, lf), nome + ': fim de linha misturado (%d CRLF em %d LF)' % (crlf, lf)
    _EOL[nome] = '\r\n' if crlf else '\n'
    return raw.decode('utf-8').replace('\r\n', '\n')

def gravar(nome, s):
    assert '\r' not in s
    open(os.path.join(SITE, nome), 'wb').write(s.replace('\n', _EOL.get(nome, '\r\n')).encode('utf-8'))

IC = {  # 19/10/2026: icones GEOMETRICOS («quero um padrao de icones geometricos»; os de antes, escudo, gota, xicara, cadeado,
        # eram figurativos e errados: «um icone de seguranca privada para saude e seguranca»). Grade 24, desenho entre 4 e 20,
        # so retas, quadrados, retangulos e triangulos; quadradinho cheio como ponto. Sem o circulo em volta (CSS .mega-icon).
 'camadas':   '<rect x="4" y="9" width="11" height="11"/><rect x="9" y="4" width="11" height="11"/>',
 'obrigacoes': '<rect x="4" y="4" width="16" height="16"/><path d="M8 9h8M8 12h8M8 15h5"/>',
 'barreira': '<rect x="4" y="4" width="6" height="6"/><rect x="14" y="14" width="6" height="6"/><path d="M4 20L20 4"/>',
 'predio': '<rect x="4" y="4" width="16" height="16"/><path d="M4 10h16M4 16h16M10 4v16"/>',
 'cruzquadro': '<rect x="4" y="4" width="16" height="16"/><path d="M12 8v8M8 12h8"/>',
 'perimetro': '<rect x="4" y="4" width="16" height="16"/><rect x="10.5" y="10.5" width="3" height="3"/><path d="M4 12h4M16 12h4M12 4v4M12 16v4"/>',   # 20/10/2026: seguranca da informacao, a informacao no centro do perimetro
 'losango':   '<polygon points="12 4 20 12 12 20 4 12"/><path d="M8 12h8"/>',
 'triangulo': '<polygon points="12 4 20 18 4 18"/><path d="M4 21h16"/>',
 'cruz':      '<path d="M12 4v16M4 12h16"/>',
 'via':       '<path d="M7 4v16M17 4v16M12 6v3M12 11v3M12 16v3"/>',
 'lista':     '<rect x="4" y="5" width="3" height="3"/><rect x="4" y="10.5" width="3" height="3"/><rect x="4" y="16" width="3" height="3"/><path d="M10 6.5h10M10 12h10M10 17.5h10"/>',
 'par':       '<rect x="3" y="8" width="7" height="8"/><rect x="14" y="8" width="7" height="8"/><path d="M10 12h4"/>',
 'grade':     '<rect x="4" y="4" width="6.5" height="6.5"/><rect x="13.5" y="4" width="6.5" height="6.5"/><rect x="4" y="13.5" width="6.5" height="6.5"/><rect x="13.5" y="13.5" width="6.5" height="6.5"/>',
 'faixas':    '<rect x="4" y="4" width="16" height="16"/><path d="M4 9.3h16M4 14.7h16"/>',
 'rede':      '<rect x="4" y="4" width="4" height="4"/><rect x="16" y="4" width="4" height="4"/><rect x="4" y="16" width="4" height="4"/><rect x="16" y="16" width="4" height="4"/><path d="M8 8l8 8M16 8l-8 8"/>',   # SEDEX/SMETA: quatro pontos ligados (a rede); o 3x3 cheio pesava
 'degraus':   '<path d="M4 5h5v5h5v5h6M4 20h16"/>',
 'hexa':      '<polygon points="12 3 20 7.5 20 16.5 12 21 4 16.5 4 7.5"/>',
 'quadrantes': '<rect x="4" y="4" width="16" height="16"/><path d="M12 4v16M4 12h16"/>',
 'documento': '<rect x="5" y="3" width="14" height="18"/><path d="M8 8h8M8 12h8M8 16h5"/>',
 'mira':      '<rect x="5" y="5" width="14" height="14"/><path d="M12 2v3M12 19v3M2 12h3M19 12h3"/><rect x="10.5" y="10.5" width="3" height="3"/>',
 'cubo':      '<polygon points="12 3 20 7.5 20 16.5 12 21 4 16.5 4 7.5"/><path d="M4 7.5l8 4.5 8-4.5M12 12v9"/>',
 'diagonais': '<rect x="4" y="4" width="16" height="16"/><path d="M4 4l16 16M20 4L4 20"/>',
 'pilar':     '<path d="M12 4v16M4 8h16M8 20h8"/>',
 'barras':    '<path d="M6 20v-9M12 20V5M18 20v-6M3 20h18"/>',
 'mapa':      '<rect x="3" y="3" width="18" height="18"/><path d="M3 12h18M12 3v18"/><rect x="10.5" y="10.5" width="3" height="3"/>',
 'elo':       '<rect x="3" y="3" width="6" height="6"/><rect x="15" y="15" width="6" height="6"/><path d="M9 6h6v9"/>',
 'painel':    '<rect x="3" y="4" width="18" height="16"/><path d="M3 10h18M9 10v10M14 14h4M14 17h3"/>',
}

# 02/10/2026: UMA lista para os tres menus (topo, celular e lateral). Cada item: (arquivo, rotulo, icone).
# O rotulo junta o tema e a norma na mesma linha («Qualidade · ISO 9001»), para a pagina ser achada pelos dois nomes.
MENU = [
 ('Sistemas de gestão', [
   ('implantacao-iso.html', 'Implantação ISO', 'camadas'),
   ('norma-iso-9001.html', 'Qualidade · ISO 9001', 'losango'),
   ('norma-iso-14001.html', 'Meio ambiente · ISO 14001', 'triangulo'),
   ('norma-iso-45001.html', 'Saúde e segurança · ISO 45001', 'cruz'),
   ('seguranca-viaria.html', 'Segurança viária · ISO 39001', 'via'),      # 02/10: sistema de gestao ISO, sai de «Seguranca e inspecao»
   ('norma-iso-27001.html', 'Segurança da informação · ISO/IEC 27001', 'perimetro'),   # 20/10/2026: pagina de norma propria
   ('norma-iso-37301.html', 'Compliance · ISO 37301', 'obrigacoes'),
   ('norma-iso-37001.html', 'Antissuborno · ISO 37001', 'barreira'),
   ('norma-iso-41001.html', 'Facilities · ISO 41001', 'predio'),
   ('compliance-seguranca-informacao.html', 'Compliance e segurança da informação', 'lista'),
   ('suporte.html', 'Suporte ao sistema de gestão', 'par'),
   ]),
 ('Padrões e sustentabilidade', [
   ('padroes-mercado.html', 'Padrões de mercado', 'grade'),
   ('ifc-performance-standards.html', 'IFC Performance Standards', 'faixas'),
   ('sedex-smeta.html', 'SEDEX/SMETA', 'rede'),
   ('gestao-carbono.html', 'Gestão de carbono', 'degraus'),
   ('esg.html', 'ESG', 'hexa'),
   ]),
 ('Segurança e inspeção', [
   ('norma-iso-22000.html', 'Segurança de alimentos · ISO 22000', 'cruzquadro'),
   ('seguranca-alimentos.html', 'Segurança de alimentos', 'quadrantes'),
   ('nrs.html', 'Atendimento a NRs', 'documento'),
   ('inspecoes.html', 'Inspeções', 'mira'),
   ('produtos-inspecionamos.html', 'Produtos que inspecionamos', 'cubo'),
   ]),
 ('Estudos e pesquisa aplicada', [
   ('estudos-pesquisa.html', 'Visão geral', 'diagonais'),
   ('estudos-regulatorios.html', 'Estudos regulatórios', 'pilar'),
   ('estudos-setoriais.html', 'Estudos setoriais', 'barras'),
   ('observatorio-setorial.html', 'Observatório setorial', 'mapa'),
   ('rastreabilidade-cadeia.html', 'Rastreabilidade de cadeia', 'elo'),
   ('painel-normas.html', 'Painel de normas ISO', 'painel'),      # 17/10: estágio, comitê, revisão e certificados por país (ISO Open Data + ISO Survey)
   ]),
]

def mega():
    cols = []
    for titulo, itens in MENU:
        links = '\n'.join('    <a href="%s"><span class="mega-icon"><svg viewBox="0 0 24 24">%s</svg></span>%s</a>' % (f, IC[i], r) for f, r, i in itens)
        cols.append('  <div class="mega-menu-col">\n    <h4>%s</h4>\n%s\n  </div>' % (titulo, links))
    return '<div class="mega-menu" id="megaMenu" aria-label="Todos os serviços">\n' + '\n'.join(cols) + '\n</div>'

def veu():
    """O mapa de temas do menu do celular (o «Todos os serviços» do veu)."""
    cols = ['  <div><h3>%s</h3>%s</div>' % (titulo, ''.join('<a href="%s">%s</a>' % (f, r) for f, r, i in itens)) for titulo, itens in MENU]
    return '  <div class="veu-mapa" id="veuMapa" aria-label="Todos os temas" hidden>\n' + '\n'.join(cols) + '\n  </div>'

# navegacao lateral: as mesmas colunas do menu, mais o institucional
LATERAL = [(t, [(f, r) for f, r, i in itens]) for t, itens in MENU] + [
 ('Institucional', [('index.html', 'Página inicial'), ('servicos.html', 'Todos os serviços'), ('sobre.html', 'Quem somos'),
   ('como-trabalhamos.html', 'Como trabalhamos'),   # 19/10/2026: Clientes de destaque saiu (pagina retirada)
   ('blog.html', 'Conteúdo'), ('contato.html', 'Contato')]),
]

def lateral(pagina):
    g = []
    for n, (titulo, itens) in enumerate(LATERAL, 1):
        links = '\n'.join('    <a href="%s"%s>%s</a>' % (f, ' class="active" aria-current="page"' if f == pagina else '', r)
                          for f, r in itens)
        g.append('  <div class="sn-group">\n    <div class="sn-num">%02d</div>\n    <h5>%s</h5>\n%s\n  </div>' % (n, titulo, links))
    return '<nav class="sidenav" aria-label="Navegação do site">\n  <div class="sn-title">Navegação</div>\n' + '\n'.join(g) + '\n</nav>'

def ent(t):   # o rodape do site usa entidades; mantenho o costume da casa
    for a, b in (('ç', '&ccedil;'), ('ã', '&atilde;'), ('õ', '&otilde;'), ('ú', '&uacute;'), ('é', '&eacute;'), ('í', '&iacute;')):
        t = t.replace(a, b)
    return t

RODAPE = [
 ('a', [('servicos.html', 'Todos os serviços'), ('implantacao-iso.html', 'Implantação ISO'),
        ('compliance-seguranca-informacao.html', 'Compliance e segurança da informação'),
        ('suporte.html', 'Suporte ao sistema de gestão'), ('nrs.html', 'Atendimento a NR(s)'),
        ('inspecoes.html', 'Inspeções')]),
 ('b', [('padroes-mercado.html', 'Padrões de mercado'), ('sedex-smeta.html', 'SEDEX/SMETA'),
        ('gestao-carbono.html', 'Gestão de carbono'), ('esg.html', 'ESG'),
        ('seguranca-alimentos.html', 'Segurança de alimentos'), ('estudos-pesquisa.html', 'Estudos e pesquisa aplicada')]),
]

def rodape_colunas():
    out = []
    for letra, itens in RODAPE:
        li = '\n'.join('      <li role="none"><a role="menuitem" href="%s">%s</a></li>' % (f, ent(r)) for f, r in itens)
        out.append('    <ul class="ft-col ft-col-%s" role="menu">\n%s\n    </ul>' % (letra, li))
    return '\n'.join(out)

LEGAL_VELHO  = '© 2026 Centomo &amp; Consultores Ltda · CNPJ 02.569.436/0001-21'
LEGAL_NOVO   = '© 2026 Ideal Metrics Ltda · CNPJ 69.202.916/0001-20'
CRED_VELHO   = 'Ideal Metrics · Desde 1998 · São Paulo, Brasil'
CRED_NOVO    = 'Ideal Metrics · Equipe em atuação desde 1998 · São Paulo, Brasil'

RE_MEGA  = re.compile(r'<div class="mega-menu" id="megaMenu"[^>]*>\n.*?\n</div>', re.S)
RE_VEU   = re.compile(r'  <div class="veu-mapa" id="veuMapa"[^>]*>\n.*?\n  </div>', re.S)
RE_LAT   = re.compile(r'<nav class="sidenav".*?</nav>', re.S)
RE_FT_AB = re.compile(r'    <ul class="ft-col ft-col-a" role="menu">.*?</ul>\n    <ul class="ft-col ft-col-b" role="menu">.*?</ul>', re.S)
