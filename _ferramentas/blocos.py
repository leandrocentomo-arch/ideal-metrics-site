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

IC = {  # icones do mega-menu, os mesmos tracos finos que o site ja usa
 'check':   '<path d="M9 12l2 2 4-4"/><circle cx="12" cy="12" r="10"/>',
 'escudo':  '<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>',
 'cadeado': '<rect x="4" y="11" width="16" height="10"/><path d="M8 11V7a4 4 0 018 0v4"/>',
 'grade':   '<rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/><rect x="3" y="14" width="7" height="7"/><rect x="14" y="14" width="7" height="7"/>',
 'relogio': '<circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/>',
 'hexa':    '<polygon points="12 2 22 8.5 22 15.5 12 22 2 15.5 2 8.5"/>',
 'pessoa':  '<path d="M16 21v-2a4 4 0 00-4-4H5a4 4 0 00-4 4v2"/><circle cx="8.5" cy="7" r="4"/><path d="M20 8v6M23 11h-6"/>',
 'lupa':    '<circle cx="11" cy="11" r="8"/><path d="M21 21l-4.35-4.35"/>',
 'caixa':   '<path d="M21 16V8a2 2 0 00-1-1.73l-7-4a2 2 0 00-2 0l-7 4A2 2 0 003 8v8a2 2 0 001 1.73l7 4a2 2 0 002 0l7-4A2 2 0 0021 16z"/>',
 'folha':   '<path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8z"/><polyline points="14 2 14 8 20 8"/>',
 'xicara':  '<path d="M18 8h1a4 4 0 010 8h-1"/><path d="M2 8h16v9a4 4 0 01-4 4H6a4 4 0 01-4-4V8z"/><path d="M6 1v3M10 1v3M14 1v3"/>',
 'balanca': '<path d="M12 3v18M5 21h14M5 7h14"/><path d="M5 7l-3 7a3 3 0 006 0zM19 7l-3 7a3 3 0 006 0z"/>',
 'barras':  '<path d="M4 20V10M10 20V4M16 20v-8M22 20H2"/>',
 'radar':   '<circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="5"/><path d="M12 12l7-7"/>',
 'elos':    '<path d="M10 13a5 5 0 007 0l3-3a5 5 0 00-7-7l-1 1"/><path d="M14 11a5 5 0 00-7 0l-3 3a5 5 0 007 7l1-1"/>',
}

# (rotulo da coluna, [(arquivo, rotulo no menu, icone)])
MENU = [
 ('Sistemas de gestão', [
   ('implantacao-iso.html', 'Implantação ISO', 'check'),
   ('compliance-seguranca-informacao.html', 'Compliance e segurança da informação', 'cadeado'),
   ('suporte.html', 'Suporte ao sistema de gestão', 'escudo')]),
 ('Padrões e sustentabilidade', [
   ('padroes-mercado.html', 'Padrões de mercado', 'grade'),
   ('sedex-smeta.html', 'SEDEX/SMETA', 'pessoa'),
   ('gestao-carbono.html', 'Gestão de carbono', 'relogio'),
   ('esg.html', 'ESG', 'hexa')]),
 ('Segurança e inspeção', [
   ('seguranca-alimentos.html', 'Segurança de alimentos', 'xicara'),
   ('nrs.html', 'Atendimento a NRs', 'folha'),
   ('inspecoes.html', 'Inspeções de produto e de fábrica', 'lupa'),
   ('produtos-inspecionamos.html', 'Produtos que inspecionamos', 'caixa')]),
 ('Estudos e pesquisa aplicada', [
   ('estudos-regulatorios.html', 'Estudos regulatórios', 'balanca'),
   ('estudos-setoriais.html', 'Estudos setoriais e políticas públicas', 'barras'),
   ('observatorio-setorial.html', 'Observatório setorial', 'radar'),
   ('rastreabilidade-cadeia.html', 'Rastreabilidade de cadeia', 'elos')]),
]

def mega():
    cols = []
    for titulo, itens in MENU:
        links = '\n'.join(
            '          <a href="%s"><span class="mega-icon"><svg viewBox="0 0 24 24">%s</svg></span>%s</a>' % (f, IC[i], r)
            for f, r, i in itens)
        cols.append('        <div class="mega-menu-col">\n          <h4>%s</h4>\n%s\n        </div>' % (titulo, links))
    return '<div class="mega-menu">\n' + '\n'.join(cols) + '\n      </div>'

# navegacao lateral: as mesmas quatro colunas, mais as normas e o institucional
LATERAL = [
 ('Sistemas de gestão', [('implantacao-iso.html', 'Implantação ISO'), ('norma-iso-9001.html', 'ISO 9001'),
   ('norma-iso-14001.html', 'ISO 14001'), ('norma-iso-45001.html', 'ISO 45001'),
   ('compliance-seguranca-informacao.html', 'Compliance e segurança da informação'),
   ('suporte.html', 'Suporte ao sistema de gestão')]),
 ('Padrões e sustentabilidade', [('padroes-mercado.html', 'Padrões de mercado'),
   ('ifc-performance-standards.html', 'IFC Performance Standards'), ('sedex-smeta.html', 'SEDEX/SMETA'),
   ('gestao-carbono.html', 'Gestão de carbono'), ('esg.html', 'ESG')]),
 ('Segurança e inspeção', [('seguranca-alimentos.html', 'Segurança de alimentos'), ('nrs.html', 'Atendimento a NRs'),
   ('inspecoes.html', 'Inspeções'), ('produtos-inspecionamos.html', 'Produtos que inspecionamos')]),
 ('Estudos e pesquisa aplicada', [('estudos-pesquisa.html', 'Visão geral'), ('estudos-regulatorios.html', 'Estudos regulatórios'),
   ('estudos-setoriais.html', 'Estudos setoriais'), ('observatorio-setorial.html', 'Observatório setorial'),
   ('rastreabilidade-cadeia.html', 'Rastreabilidade de cadeia')]),
 ('Institucional', [('index.html', 'Página inicial'), ('servicos.html', 'Todos os serviços'), ('sobre.html', 'Quem somos'),
   ('como-trabalhamos.html', 'Como trabalhamos'), ('clientes.html', 'Clientes de destaque'),
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

RE_MEGA  = re.compile(r'<div class="mega-menu">.*?</div>\n      </div>', re.S)
RE_LAT   = re.compile(r'<nav class="sidenav".*?</nav>', re.S)
RE_FT_AB = re.compile(r'    <ul class="ft-col ft-col-a" role="menu">.*?</ul>\n    <ul class="ft-col ft-col-b" role="menu">.*?</ul>', re.S)
