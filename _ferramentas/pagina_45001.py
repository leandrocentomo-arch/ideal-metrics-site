# -*- coding: utf-8 -*-
"""Pagina norma-iso-45001.html no molde da seguranca-viaria (02/10/2026).

    python _ferramentas/pagina_45001.py

Pedido do Leandro: «achei muito pouco conteudo»; «toda pagina comeca pela frase maior, depois um texto, depois
diagramas e o conteudo atual»; «vamos fazer com a ISO 45001». Regras em CLAUDE.md, «Padroes canonicos».
Troca so o miolo (.content); cabecalho, menus, faixa e rodape ficam como estao na pagina.

Fatos e fontes:
- Credencial: Lead Auditor ISO 45001 (memoria user-leandro-competencia-auditor).
- NR-01, GRO e PGR (Portaria SEPRT 6.730/2020); riscos psicossociais pela Portaria MTE 1.419/2024, com fiscalizacao
  punitiva desde 26/05/2026: vault, — CQT/✱ Padroes/Gestao de Perigos e Riscos de SST/.
- ISO 45001 em revisao: ISO/DIS 45001 (ed. 2), votacao encerrada em 09/09/2026, publicacao prevista no 1o semestre de 2027;
  ISO 45001:2018/Amd 1:2024 (acoes climaticas). iso.org, conferido em 05/10/2026.
- 742.214 acidentes de trabalho notificados em 2024: Observatorio de Seguranca e Saude no Trabalho (MPT e OIT).
- 542.527 certificados ISO 45001 em 2024, 190.429 em 2020: ISO Survey 2024.
- Hierarquia de controle: ISO 45001, 8.1.2, alineas a) a e)."""
import io, os, re

SITE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ARQ = 'norma-iso-45001.html'

# ---------------------------------------------------------------- diagrama 1: a ISO 45001 e as NRs no mesmo sistema
PARES = [('5.4 · Consulta e participação', 'NR-05 · CIPA'),
         ('6.1.2 · Perigos e riscos', 'NR-01 · GRO: inventário e plano de ação'),
         ('7.2 · Competência', 'NR-10, NR-12, NR-33, NR-35 · capacitação'),
         ('8.2 · Emergências', 'NR-01 · preparação para emergências'),
         ('9.1 · Monitoramento', 'NR-07 · PCMSO · NR-09 · exposições'),
         ('10.2 · Incidentes e ação corretiva', 'NR-01 · análise de acidentes e doenças')]
# 02/10: caixas na largura do texto mais longo da coluna (182 e 234 px medidos) + 24 px de cada lado
PAD, LIGA = 24, 120
WL, WR = 182 + 2 * PAD, 234 + 2 * PAD
XR = WL + LIGA; W = XR + WR
f = ['<figure class="ifc-fig">',
     '<svg viewBox="0 0 %d 300" style="max-width:%dpx" role="img" aria-label="A ISO 45001 e as Normas Regulamentadoras no mesmo sistema">' % (W + 1, W + 1),
     '<text class="ifc-svg-n" x="%d" y="22">ISO 45001</text>' % (WL // 2),
     '<text class="ifc-svg-n" x="%d" y="22">NORMAS REGULAMENTADORAS</text>' % (XR + WR // 2)]
for i, (iso, nr) in enumerate(PARES):
    y = 40 + i * 44; cy = y + 17
    f += ['<rect class="ifc-aro ifc-aro--f" x="0.5" y="%d" width="%d" height="34" rx="3"/>' % (y, WL),
          '<rect class="ifc-aro ifc-aro--f" x="%.1f" y="%d" width="%d" height="34" rx="3"/>' % (XR + .5, y, WR),
          '<text class="ifc-svg-t" x="%d" y="%d">%s</text>' % (WL // 2, cy + 5, iso),
          '<text class="ifc-svg-t" x="%d" y="%d">%s</text>' % (XR + WR // 2, cy + 5, nr),
          '<line class="ifc-linha" x1="%d" y1="%d" x2="%d" y2="%d"/>' % (WL + 6, cy, XR - 6, cy),
          '<circle cx="%d" cy="%d" r="3.5" fill="#14304C"/>' % (WL + 6, cy),
          '<circle cx="%d" cy="%d" r="3.5" fill="#14304C"/>' % (XR - 6, cy)]
f += ['</svg>', '<figcaption>A ISO 45001 e as NRs no mesmo sistema</figcaption>', '</figure>']
FIG_NR = '\n'.join(f)

# ---------------------------------------------------------------- diagrama 2: a hierarquia de controle (ISO 45001, 8.1.2)
NIVEIS = ['Eliminar o perigo', 'Substituir processo, material ou equipamento', 'Controles de engenharia e reorganização do trabalho',
          'Controles administrativos, inclusive treinamento', 'Equipamento de proteção individual']
# 02/10: cada degrau na largura do proprio texto + numero e folga (texto medido: 92, 249, 287, 265, 197 px), e a escada
# continua descendo 28 px de cada lado
TXT = [92, 249, 287, 265, 197]
req = [t + 2 * 56 for t in TXT]
larg = [0] * 5; larg[4] = req[4]
for i in range(3, -1, -1):
    larg[i] = max(req[i], larg[i + 1] + 56)
W = larg[0] + 2
f = ['<figure class="ifc-fig">',
     '<svg viewBox="0 0 %d 250" style="max-width:%dpx" role="img" aria-label="Hierarquia de controle da ISO 45001, do mais eficaz ao menos eficaz">' % (W, W)]
for i, t in enumerate(NIVEIS):
    w = larg[i]; x = (W - w) / 2; y = 10 + i * 46
    f += ['<rect class="ifc-aro ifc-aro--f" x="%.1f" y="%d" width="%d" height="38" rx="3"/>' % (x, y, w),
          '<text class="ifc-svg-n" x="%.1f" y="%d">0%d</text>' % (x + 26, y + 23, i + 1),
          '<text class="ifc-svg-t" x="%.1f" y="%d">%s</text>' % (W / 2, y + 24, t)]
f += ['</svg>', '<figcaption>Hierarquia de controle: do mais eficaz ao menos eficaz (ISO 45001, 8.1.2)</figcaption>', '</figure>']
FIG_HC = '\n'.join(f)

# ---------------------------------------------------------------- 05/10/2026: a ESTRUTURA GERAL de pagina de servico
# (proposta aprovada pelo Leandro: abertura, o que o sistema passa a medir, o que fazemos, como implantamos, por que a
# Ideal Metrics, aplicacao, por que implantar agora, bloco do tema, normas de referencia, contato).

# diagrama: o que o sistema passa a medir (linha fina, tres caixas, como na seguranca viaria)
MEDE = [('01', 'Perigos e riscos', ['Físicos, químicos e biológicos', 'Ergonômicos e de acidentes', 'Psicossociais (NR-01)']),
        ('02', 'Controles', ['Eliminar e substituir', 'Engenharia e organização', 'Administrativos e EPI']),
        ('03', 'Resultado', ['Acidentes e doenças', 'Dias de afastamento', 'Objetivos e metas'])]
TXT_M = [141, 122, 99]            # texto mais longo de cada caixa, medido no navegador (getComputedTextLength)
PAD, SETA = 24, 46
xs, x = [], 0.5
for w in TXT_M:
    xs.append(x); x += w + 2 * PAD + SETA
W = int(xs[-1] + TXT_M[-1] + 2 * PAD + 1)
f = ['<figure class="ifc-fig">',
     '<svg viewBox="0 0 %d 200" style="max-width:%dpx" role="img" aria-label="O que o sistema passa a medir: perigos e riscos, controles e resultado">' % (W, W)]
for (num, tit, linhas), x0, tw in zip(MEDE, xs, TXT_M):
    w = tw + 2 * PAD; cx = x0 + w / 2
    f += ['<rect class="ifc-aro ifc-aro--f" x="%.1f" y="10" width="%d" height="188" rx="3"/>' % (x0, w),
          '<text class="ifc-svg-n" x="%.1f" y="42">%s</text>' % (cx, num),
          '<text class="ifc-svg-t" x="%.1f" y="70">%s</text>' % (cx, tit),
          '<line class="ifc-linha" x1="%.1f" y1="88" x2="%.1f" y2="88"/>' % (cx - 30, cx + 30)]
    f += ['<text class="ifc-svg-p" x="%.1f" y="%d">%s</text>' % (cx, 122 + i * 26, t) for i, t in enumerate(linhas)]
for k in range(2):
    x1 = xs[k] + TXT_M[k] + 2 * PAD + 4; x2 = xs[k + 1] - 4
    f += ['<line class="ifc-linha" x1="%.1f" y1="135" x2="%.1f" y2="135"/>' % (x1, x2),
          '<polyline class="ifc-linha" points="%.1f,129 %.1f,135 %.1f,141"/>' % (x2 - 6, x2, x2 - 6)]
f += ['</svg>', '<figcaption>O que o sistema passa a medir</figcaption>', '</figure>']
FIG_MEDE = '\n'.join(f)

# as cinco etapas, as mesmas de toda pagina de implantacao; so a linha de baixo muda com a norma
PASSOS = [('01', 'Diagnóstico', 'a operação contra', 'a ISO 45001 e as NRs'),
          ('02', 'Plano diretor', 'prazo, responsável', 'e capacitação'),
          ('03', 'Implantação', 'perigos, controles', 'e indicadores'),
          ('04', 'Auditoria interna', 'e análise crítica', 'pela direção'),
          ('05', 'Organização pronta', 'para a certificação', 'ISO 45001')]
f = ['<figure class="ifc-fig">',
     '<svg viewBox="0 0 900 170" role="img" aria-label="As cinco etapas da implantação: diagnóstico, plano diretor, implantação, auditoria interna e organização pronta para a certificação">',
     '<line class="ifc-linha" x1="90" y1="66" x2="810" y2="66"/>']
for i, (n, t, p1, p2) in enumerate(PASSOS):
    x = 90 + i * 180
    f += ['<circle class="ifc-aro ifc-aro--f" cx="%d" cy="66" r="13"/>' % x,
          '<circle cx="%d" cy="66" r="3.5" fill="#14304C"/>' % x,
          '<text class="ifc-svg-n" x="%d" y="38">%s</text>' % (x, n),
          '<text class="ifc-svg-t" x="%d" y="110">%s</text>' % (x, t),
          '<text class="ifc-svg-p" x="%d" y="132">%s</text>' % (x, p1),
          '<text class="ifc-svg-p" x="%d" y="148">%s</text>' % (x, p2)]
f += ['</svg>', '<figcaption>As cinco etapas da implantação</figcaption>', '</figure>']
FIG_PASSOS = '\n'.join(f)

# o que fazemos: seis cards, uma linha cada (processos, metodologias, indicadores)
CEL = [('01', 'Diagnóstico e plano diretor', 'O que falta para a ISO 45001 e para as NRs, com prazo e responsável.'),
       ('02', 'Perigos e riscos', 'Inventário de riscos e plano de ação do GRO da NR-01, com os riscos psicossociais.'),
       ('03', 'Controles e procedimentos', 'Hierarquia de controle, permissões de trabalho e preparação para emergências.'),
       ('04', 'Consulta e participação', 'Trabalhadores, CIPA e contratadas dentro do sistema.'),
       ('05', 'Indicadores e investigação', 'Objetivos e metas de saúde e segurança, e análise de causa de incidentes.'),
       ('06', 'Auditoria interna', 'Formação de auditores, auditoria interna e análise crítica pela direção.')]
GRADE = '<div class="ifc-grade">\n' + '\n'.join(
    '  <div class="ifc-cel"><span class="ifc-rot">%s</span><h4>%s</h4><p>%s</p></div>' % c for c in CEL) + '\n</div>'

# ---------------------------------------------------------------- numeros
NUMS = [('742 mil', 'acidentes de trabalho notificados no Brasil em 2024'),
        ('542 mil', 'certificados ISO 45001 no mundo em 2024'),
        ('2,8 vezes', 'o número de certificados ISO 45001 de 2020 para 2024'),
        ('26/05/2026', 'riscos psicossociais cobrados na fiscalização da NR-01')]
nums = ('<div class="vi-nums">\n' + '\n'.join('  <div class="vi-num"><b>%s</b><span>%s</span></div>' % n for n in NUMS) + '\n</div>\n'
        '<p class="vi-fonte">Fontes: Observatório de Segurança e Saúde no Trabalho (MPT e OIT), 2024 · ISO Survey 2024 · Portaria MTE 1.419/2024.</p>')

MIOLO = '''<p class="abre">A Ideal Metrics apoia a sua organização na implantação do sistema de gestão de saúde e segurança ocupacional e na preparação para a certificação ISO 45001.</p>
<p>O trabalho começa pelos perigos reais da operação: tarefas, máquinas, produtos químicos, trabalho em altura e em espaço confinado, contratadas e a rotina de cada área. Levantamos o que já existe, mostramos o que falta para a norma e para as NRs, e montamos com a sua equipe o inventário de riscos, os controles, a consulta aos trabalhadores e a rotina que o organismo certificador vai verificar.</p>
<p>O sistema passa a medir os perigos de cada atividade, a eficácia dos controles e o resultado: acidentes, doenças e dias de afastamento. Com esses números, a direção decide onde agir, e a organização chega à certificação com evidência para a fiscalização, os clientes e o organismo certificador.</p>

__FIG_MEDE__

__FIG_HC__

<hr class="section-divider">
<h3>O que fazemos</h3>
__GRADE__

<hr class="section-divider">
<h3>Como implantamos</h3>
__FIG_PASSOS__

<hr class="section-divider">
<h3>Por que a Ideal Metrics</h3>
<ul>
<li><strong>Consultores:</strong> formação internacional de Auditor Líder (Lead Auditor) em ISO 45001.</li>
<li><strong>NRs no mesmo sistema:</strong> GRO e PGR da NR-01, inclusive os riscos psicossociais, PCMSO e CIPA integrados à ISO 45001.</li>
<li><strong>Hierarquia de controle aplicada:</strong> eliminar, substituir, controlar na fonte e só então o equipamento de proteção individual.</li>
<li><strong>Sistema integrado:</strong> a ISO 45001 entra no sistema que já atende <a href="norma-iso-9001.html">ISO 9001</a> e <a href="norma-iso-14001.html">ISO 14001</a>.</li>
<li><strong>Equipe em atuação desde 1998.</strong></li>
</ul>

<hr class="section-divider">
<h3>Aplicação</h3>
<ul>
<li>Indústrias com máquinas, produtos químicos, trabalho em altura e em espaço confinado.</li>
<li>Construção, montagem e manutenção, com contratadas no mesmo local.</li>
<li>Logística, armazenagem e operações com frota.</li>
<li>Empresas de serviço com equipes nas instalações dos clientes.</li>
<li>Organizações que precisam revisar o PGR para os riscos psicossociais.</li>
</ul>

<hr class="section-divider">
<h3>Por que implantar agora</h3>
__NUMS__
<ul>
<li><strong>Riscos psicossociais:</strong> desde 26/05/2026 a fiscalização cobra a avaliação dos fatores de risco psicossociais no gerenciamento de riscos da NR-01. Quem tem o sistema implantado já tem o processo para incluí-los no inventário.</li>
<li><strong>Exigência de contratantes:</strong> a qualificação de fornecedores e de contratadas costuma pedir gestão de saúde e segurança com evidência.</li>
<li><strong>Norma em revisão:</strong> __REVISAO__</li>
</ul>

<hr class="section-divider">
<h3>ISO 45001 e as Normas Regulamentadoras</h3>
<p>Um sistema de gestão de saúde e segurança ocupacional traz para o mesmo lugar o que as NRs já exigem: o GRO da NR-01, com o inventário de riscos e o plano de ação, o PCMSO da NR-07, a CIPA da NR-05 e as NRs da operação.</p>
__FIG_NR__

<hr class="section-divider">
<h3>Normas de referência</h3>
<ul>
__NORMAS__
</ul>
<p class="vi-fonte">Situação das normas conferida no catálogo da ISO (iso.org) em 05/10/2026.</p>

<hr class="section-divider">
<p>A certificação é concedida por organismo acreditado. Para implantar a ISO 45001 na sua operação, <a href="contato.html">fale com a gente</a>.</p>
'''
# 05/10: conferido no iso.org em 05/10/2026: ISO 45001:2018 (63787) com a Amd 1:2024 «Climate action changes» (88428,
# publicada em 2024-02); ISO/DIS 45001, edicao 2 (89698), estagio 40.60, votacao encerrada em 2026-09-09, «expected to
# replace ISO 45001:2018 in the first half of 2027».
REVISAO = ('a segunda edição da ISO 45001 teve o texto em consulta (DIS) votado em setembro de 2026 e deve ser publicada '
           'no primeiro semestre de 2027. Quem implanta agora já sai preparado para a transição.')
NORMAS = ['ISO 45001:2018, com a Emenda 1:2024 (ações climáticas): sistemas de gestão de saúde e segurança ocupacional.',
          'ISO/DIS 45001: a segunda edição, com publicação prevista para o primeiro semestre de 2027.',
          'NR-01: gerenciamento de riscos ocupacionais (GRO e PGR), com os fatores de risco psicossociais (Portaria MTE 1.419/2024).',
          'NR-05 (CIPA), NR-07 (PCMSO) e as NRs da operação.']
for k, v in (('__FIG_NR__', FIG_NR), ('__FIG_HC__', FIG_HC), ('__NUMS__', nums), ('__FIG_MEDE__', FIG_MEDE), ('__FIG_PASSOS__', FIG_PASSOS),
             ('__GRADE__', GRADE), ('__REVISAO__', REVISAO), ('__NORMAS__', '\n'.join('<li>%s</li>' % n for n in NORMAS))):
    MIOLO = MIOLO.replace(k, v)
for palavra in ('percurso', 'caminho', 'Ponto de partida', 'exame', 'auditoria de certificação', 'Para quem é', 'A norma traz', '<p>Ela ', '<p>Ele '):
    assert palavra not in MIOLO, 'palavra vetada no texto: ' + palavra

P = os.path.join(SITE, ARQ)
s = io.open(P, encoding='utf-8', newline='').read()
eol = '\r\n' if '\r\n' in s else '\n'
s = s.replace('\r\n', '\n')
i = s.index('<div class="content">') + len('<div class="content">')
j = s.index('</div>\n</div>\n<footer')
s = s[:i] + '\n' + MIOLO + s[j:]
io.open(P, 'w', encoding='utf-8', newline='').write(s.replace('\n', eol))
print('%s: %d bytes' % (ARQ, len(s)))
