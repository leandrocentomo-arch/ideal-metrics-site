# -*- coding: utf-8 -*-
"""A pagina «Gestao de Seguranca Viaria» (seguranca-viaria.html), 02/10/2026.

    python _ferramentas/pagina_viaria.py

Pedido do Leandro: pagina voltada a implantacao da ISO 39001, curta («um resumo de como implementamos»),
com os termos que as pessoas buscam, as normas de apoio, as tendencias da norma, a experiencia em concessao
rodoviaria e a formacao de Auditor Lider; uma figura no estilo das da pagina do IFC, mas que mostre uma rodovia;
ligada ao card 07 da home. Serve de molde para as proximas paginas de servico.

A CASCA (cabecalho, menus, navegacao lateral, rodape, scripts) vem da ifc-performance-standards.html; aqui fica
so o miolo. As duas figuras sao SVG em linha fina, com as classes .ifc-* que ja estao no css/style.css.
A foto do banner (img/banner-viaria-lum.webp) vem do Google Flow e do _ferramentas/banner/foto_banner.py.

FONTES (conferidas em 02/10/2026):
  - catalogo do ISO/TC 241 (iso.org/committee/558313): ISO 39001:2012 e Amd 1:2024; ISO/WD 39001.2 (2a edicao,
    projeto aprovado em 25/03/2026, minuta de trabalho); ISO 39002:2020; ISO 39003:2023; ISO 39004:2026;
    ISO/AWI 39005; ISO/AWI TR 39009;
  - ABNT NBR ISO 39001:2015 (secao 6.3 e Anexo B), no vault, pasta do TC 241;
  - PL 710/2024 (Portal do Transito, 26/12/2024): aprovado no Senado, em analise na Camara;
  - experiencia e formacao: atestado de capacidade tecnica e certificado do curso, na pasta de projetos do vault.
Nomes de cliente nao entram na pagina."""
import os, re, io

SITE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
casca = io.open(os.path.join(SITE, 'ifc-performance-standards.html'), encoding='utf-8', newline='').read()
eol = '\r\n' if '\r\n' in casca else '\n'
s = casca.replace('\r\n', '\n')

ARQ = 'seguranca-viaria.html'
TITULO = 'Gestão de Segurança Viária'
DESC = ('Consultoria para implantação da ISO 39001: sistema de gestão da segurança viária, análise de risco viário, '
        'fatores de desempenho e preparação para a certificação. Para concessionárias de rodovias, frotas e transporte.')

# ---------------------------------------------------------------- figura 1: a rodovia do percurso
PASSOS = [('01', 'Diagnóstico', 'a operação contra', 'a ISO 39001'),
          ('02', 'Plano diretor', 'prazo, responsável', 'e capacitação'),
          ('03', 'Implantação', 'risco viário, metas', 'e controles'),
          ('04', 'Auditoria interna', 'e análise crítica', 'pela direção'),
          ('05', 'Certificação', 'apoio na auditoria', 'do organismo')]
f1 = ['<figure class="ifc-fig">',
      '<svg viewBox="0 0 1100 215" role="img" aria-label="Percurso da implantação, desenhado como uma rodovia: diagnóstico, plano diretor, implantação, auditoria interna e certificação">',
      '<rect x="20" y="52" width="1060" height="56" fill="rgba(20,48,76,.06)"/>',
      '<line class="ifc-linha" x1="20" y1="52" x2="1080" y2="52"/>',
      '<line class="ifc-linha" x1="20" y1="108" x2="1080" y2="108"/>',
      '<line class="ifc-linha" x1="20" y1="80" x2="1080" y2="80" stroke-dasharray="16 12"/>',
      '<path class="ifc-linha" d="M1052 68l12 12-12 12"/>']
for i, (n, t, p1, p2) in enumerate(PASSOS):
    x = 110 + i * 220
    f1 += ['<circle class="ifc-aro ifc-aro--f" cx="%d" cy="80" r="13"/>' % x,
           '<circle cx="%d" cy="80" r="3.5" fill="#14304C"/>' % x,
           '<text class="ifc-svg-n" x="%d" y="36">%s</text>' % (x, n),
           '<text class="ifc-svg-t" x="%d" y="140">%s</text>' % (x, t),
           '<text class="ifc-svg-p" x="%d" y="162">%s</text>' % (x, p1),
           '<text class="ifc-svg-p" x="%d" y="178">%s</text>' % (x, p2)]
f1 += ['</svg>', '<figcaption>O percurso, do diagnóstico à certificação</figcaption>', '</figure>']
FIG1 = '\n'.join(f1)

# ---------------------------------------------------------------- figura 2: as tres faixas dos fatores de desempenho
FAIXAS = [('Exposição ao risco', 'Quanto a operação circula',
           ['distância percorrida · volume de tráfego · volume de produto ou serviço']),
          ('Resultados intermediários', 'Onde a gestão atua',
           ['velocidade segura · via adequada ao veículo e à carga · planejamento do percurso · cinto e capacete',
            'aptidão do condutor (fadiga, distração, álcool) · condição do veículo · habilitação · resposta pós-sinistro']),
          ('Resultados finais', 'O que a norma quer reduzir',
           ['mortes e lesões graves em sinistros de trânsito'])]
f2 = ['<figure class="ifc-fig">',
      '<svg viewBox="0 0 1100 250" role="img" aria-label="Os fatores de desempenho da segurança viária em três faixas de uma rodovia: exposição ao risco, resultados intermediários e resultados finais">',
      '<rect x="20" y="16" width="1060" height="216" fill="rgba(20,48,76,.06)"/>',
      '<line class="ifc-linha" x1="20" y1="16" x2="1080" y2="16"/>',
      '<line class="ifc-linha" x1="20" y1="232" x2="1080" y2="232"/>',
      '<line class="ifc-linha" x1="20" y1="88" x2="1080" y2="88" stroke-dasharray="16 12"/>',
      '<line class="ifc-linha" x1="20" y1="160" x2="1080" y2="160" stroke-dasharray="16 12"/>']
for i, (rot, tit, linhas) in enumerate(FAIXAS):
    y = 16 + i * 72
    f2 += ['<text class="ifc-svg-n" style="text-anchor:start" x="44" y="%d">%s</text>' % (y + 30, rot.upper()),
           '<text class="ifc-svg-t" style="text-anchor:start" x="44" y="%d">%s</text>' % (y + 51, tit),
           '<path class="ifc-linha" d="M1048 %dl10 10-10 10"/>' % (y + 26)]
    y0 = y + (41 if len(linhas) == 1 else 32)
    for k, l in enumerate(linhas):
        f2.append('<text class="ifc-svg-p" style="text-anchor:start" x="318" y="%d">%s</text>' % (y0 + k * 18, l))
f2 += ['</svg>', '<figcaption>Fatores de desempenho da segurança viária (ISO 39001, seção 6.3)</figcaption>', '</figure>']
FIG2 = '\n'.join(f2)

# ---------------------------------------------------------------- o miolo
CEL = [('Ponto de partida', 'Diagnóstico e plano diretor',
        'Leitura da operação contra os requisitos da ISO 39001: contexto, partes interessadas, legislação de trânsito e de transporte, e o que o sistema de gestão atual já resolve. O resultado é um plano com prazo, responsável e esforço por lacuna.'),
       ('Risco', 'Análise de risco viário',
        'Perigos por rota, trecho, veículo, condutor e jornada, com critério de severidade e probabilidade. A avaliação de perigos de rota e o plano de viagem saem dessa matriz.'),
       ('Desempenho', 'Fatores de desempenho, metas e indicadores',
        'Escolha dos fatores que a operação controla ou influencia, com meta e indicador para cada um: velocidade, aptidão do condutor, condição do veículo, planejamento do percurso e resposta pós-sinistro.'),
       ('Operação', 'Controles operacionais e emergência',
        'Procedimentos para condutores, frota, jornada e contratadas, mais o plano de atendimento a emergências de segurança viária.'),
       ('Aprendizado', 'Investigação de sinistros e incidentes',
        'Método de investigação com análise de causa e ação corretiva, com retorno aos fatores de desempenho. Cada ocorrência altera o sistema.'),
       ('Verificação', 'Auditoria interna e preparação para a certificação',
        'Formação de auditores internos, auditoria completa do sistema, análise crítica pela direção e acompanhamento da auditoria do organismo certificador.')]
grade = '<div class="ifc-grade">\n' + '\n'.join(
    '  <div class="ifc-cel"><span class="ifc-rot">%s</span><h4>%s</h4><p>%s</p></div>' % c for c in CEL) + '\n</div>'

MIOLO = '''<p>A Ideal Metrics implanta o <strong>sistema de gestão da segurança viária</strong> da <strong>ISO 39001</strong> em organizações que operam, usam ou influenciam o sistema viário: concessionárias de rodovias, transportadoras de cargas, operadores de transporte de passageiros e empresas com frota própria ou terceirizada. É o caminho para quem busca a <strong>certificação ISO 39001</strong>, precisa reduzir sinistros de trânsito na operação ou tem a norma como exigência de contrato.</p>

<h3>Como implantamos a ISO 39001</h3>
__FIG1__

__GRADE__

<ul>
<li><strong>Experiência em concessão rodoviária de grande porte:</strong> implantação do sistema de gestão da segurança viária em concessionária de rodovias, até a certificação ISO 39001.</li>
<li><strong>Consultor com formação internacional:</strong> curso de Auditor Líder (Lead Auditor) em ISO 39001, com exame de aprovação.</li>
<li><strong>Integração com o que já existe:</strong> a ISO 39001 tem a mesma estrutura das <a href="norma-iso-9001.html">ISO 9001</a>, <a href="norma-iso-14001.html">ISO 14001</a> e <a href="norma-iso-45001.html">ISO 45001</a>. Política, objetivos, auditoria e análise crítica são aproveitados.</li>
<li><strong>Equipe em atuação desde 1998:</strong> em normas de gestão, saúde e segurança, meio ambiente e programas setoriais.</li>
</ul>

<hr class="section-divider">
<h3>O que é a ISO 39001</h3>
<p>A <strong>ISO 39001</strong> (no Brasil, ABNT NBR ISO 39001:2015) define os requisitos de um sistema de gestão da segurança viária. O objetivo é reduzir e, no limite, eliminar <strong>mortes e lesões graves</strong> em sinistros de trânsito sobre os quais a organização tem controle ou influência. A norma se apoia na abordagem de <strong>Sistema Seguro</strong>, a mesma da <strong>Visão Zero</strong>: o erro humano é previsto, e vias, veículos, velocidades e resposta ao sinistro são geridos para que ele não custe uma vida.</p>
<p>A norma não lista soluções técnicas. Ela exige que a organização escolha os seus <strong>fatores de desempenho da segurança viária</strong>, defina metas e prove resultado.</p>
__FIG2__

<hr class="section-divider">
<h3>Normas de apoio que usamos</h3>
<p>As ferramentas do sistema são montadas com as normas que cercam a ISO 39001.</p>
<ul>
<li><strong>ISO 31000:2018 · Gestão de riscos:</strong> a base do método da análise de risco viário.</li>
<li><strong>ISO 39002:2020 · Segurança no deslocamento casa-trabalho:</strong> boas práticas para o programa de trajeto dos empregados.</li>
<li><strong>ISO 39004:2026 · Serviços por plataforma digital:</strong> boas práticas de segurança viária para entregas e transporte por aplicativo.</li>
<li><strong>ISO 39003:2023 · Veículos autônomos:</strong> considerações éticas de segurança, para operações com direção automatizada.</li>
<li><strong>ISO/IEC TS 17021-7:2014 · Competência de auditores:</strong> referência para formar os auditores internos de segurança viária.</li>
</ul>

<hr class="section-divider">
<h3>O que está mudando na segurança viária</h3>
<ul>
<li><strong>Revisão da ISO 39001:</strong> a segunda edição está em elaboração no ISO/TC 241. O projeto foi aprovado em março de 2026 e está na fase de minuta de trabalho. A edição de 2012 vale até a publicação da nova.</li>
<li><strong>Clima no sistema de gestão:</strong> a emenda ISO 39001:2012/Amd 1:2024 incluiu a mudança climática na análise de contexto e de partes interessadas.</li>
<li><strong>Infraestrutura classificada por nível de segurança:</strong> o ISO/TC 241 desenvolve a ISO 39005, um quadro de classificação do nível de segurança da infraestrutura viária.</li>
<li><strong>Exigência em contrato e em lei:</strong> contratos de concessão rodoviária já trazem a certificação ISO 39001 como obrigação com prazo. O PL 710/2024, aprovado no Senado e enviado à Câmara dos Deputados, obriga a administração de rodovias a adotar sistemas de gestão de qualidade e de segurança.</li>
<li><strong>Meta de redução à metade:</strong> a Segunda Década de Ação pela Segurança no Trânsito da ONU (2021 a 2030) e o PNATRANS (Lei 13.614/2018) trabalham com a redução das mortes no trânsito pela metade.</li>
</ul>
<p>Acompanhamos a revisão da norma e sinalizamos, no diagnóstico, o que tende a mudar. Situação das normas conferida no catálogo da ISO em outubro de 2026.</p>

<hr class="section-divider">
<h3>Para quem é</h3>
<ul>
<li>Concessionárias de rodovias e operadores de infraestrutura viária.</li>
<li>Transportadoras de cargas e operadores logísticos.</li>
<li>Transporte de passageiros: urbano, rodoviário e fretamento.</li>
<li>Empresas com frota própria ou terceirizada e equipes que dirigem a trabalho.</li>
<li>Embarcadores que exigem segurança viária dos transportadores contratados.</li>
</ul>

<hr class="section-divider">
<p>A segurança viária conversa com o que a organização já tem: a <a href="norma-iso-45001.html">ISO 45001</a> trata o deslocamento como risco ocupacional, e o <a href="nrs.html">atendimento às NRs</a> cobre a jornada e a aptidão do condutor. Veja também a <a href="implantacao-iso.html">implantação de sistemas de gestão ISO</a>.</p>
<p>Para avaliar o caminho da sua operação, <a href="contato.html">fale com a gente</a>.</p>
'''.replace('__FIG1__', FIG1).replace('__FIG2__', FIG2).replace('__GRADE__', grade)

# ---------------------------------------------------------------- monta
s, n = re.subn(r'<title>.*?</title>', '<title>%s | ISO 39001 | Ideal Metrics</title>\n<meta name="description" content="%s">' % (TITULO, DESC), s, count=1)
assert n == 1
s, n = re.subn(r'<div class="page-banner"[^>]*>.*?</div>',
               '<div class="page-banner" data-lum="img/banner-viaria-lum.webp?v=1"><h1>%s</h1><p>Implantação da ISO 39001: sistema de gestão da segurança viária para reduzir mortes e lesões graves no trânsito, do diagnóstico à auditoria de certificação.</p></div>' % TITULO,
               s, count=1, flags=re.S)
assert n == 1
s, n = re.subn(r'<div class="breadcrumb">.*?</div>',
               '<div class="breadcrumb"><a href="index.html">Página Inicial</a> &gt; <a href="servicos.html">Todos os serviços</a> &gt; Gestão de segurança viária</div>', s, count=1, flags=re.S)
assert n == 1
s = s.replace('<a href="ifc-performance-standards.html" class="active" aria-current="page">IFC Performance Standards</a>',
              '<a href="ifc-performance-standards.html">IFC Performance Standards</a>')
# a navegacao lateral marca esta pagina (o link ja esta na casca, posto pelo menu do site)
x = '    <a href="seguranca-viaria.html">Segurança viária</a>'
assert s.count(x) == 1, 'falta o link da pagina na navegacao lateral da casca'
s = s.replace(x, '    <a href="seguranca-viaria.html" class="active" aria-current="page">Segurança viária</a>')
i = s.index('<div class="content">') + len('<div class="content">')
j = s.index('</div>\n</div>\n<footer')
s = s[:i] + '\n' + MIOLO + s[j:]
io.open(os.path.join(SITE, ARQ), 'w', encoding='utf-8', newline='').write(s.replace('\n', eol))
print('%s: %d bytes' % (ARQ, len(s)))
