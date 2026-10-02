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
- ISO 45001 em revisao, DIS em 2026: mesma pasta (marco regulatorio).
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
f = ['<figure class="ifc-fig">',
     '<svg viewBox="0 0 900 300" role="img" aria-label="A ISO 45001 e as Normas Regulamentadoras no mesmo sistema">',
     '<text class="ifc-svg-n" x="165" y="22">ISO 45001</text>',
     '<text class="ifc-svg-n" x="735" y="22">NORMAS REGULAMENTADORAS</text>']
for i, (iso, nr) in enumerate(PARES):
    y = 40 + i * 44; cy = y + 17
    f += ['<rect class="ifc-aro ifc-aro--f" x="1" y="%d" width="329" height="34" rx="3"/>' % y,
          '<rect class="ifc-aro ifc-aro--f" x="570" y="%d" width="329" height="34" rx="3"/>' % y,
          '<text class="ifc-svg-t" x="165" y="%d">%s</text>' % (cy + 5, iso),
          '<text class="ifc-svg-t" x="735" y="%d">%s</text>' % (cy + 5, nr),
          '<line class="ifc-linha" x1="336" y1="%d" x2="564" y2="%d"/>' % (cy, cy),
          '<circle cx="336" cy="%d" r="3.5" fill="#14304C"/>' % cy,
          '<circle cx="564" cy="%d" r="3.5" fill="#14304C"/>' % cy]
f += ['</svg>', '<figcaption>A ISO 45001 e as NRs no mesmo sistema</figcaption>', '</figure>']
FIG_NR = '\n'.join(f)

# ---------------------------------------------------------------- diagrama 2: a hierarquia de controle (ISO 45001, 8.1.2)
NIVEIS = ['Eliminar o perigo', 'Substituir processo, material ou equipamento', 'Controles de engenharia e reorganização do trabalho',
          'Controles administrativos, inclusive treinamento', 'Equipamento de proteção individual']
f = ['<figure class="ifc-fig">',
     '<svg viewBox="0 0 900 250" role="img" aria-label="Hierarquia de controle da ISO 45001, do mais eficaz ao menos eficaz">']
for i, t in enumerate(NIVEIS):
    w = 900 - i * 110; x = (900 - w) / 2; y = 10 + i * 46
    f += ['<rect class="ifc-aro ifc-aro--f" x="%.1f" y="%d" width="%.1f" height="38" rx="3"/>' % (x + 1, y, w - 2),
          '<text class="ifc-svg-n" x="%.1f" y="%d">0%d</text>' % (x + 26, y + 23, i + 1),
          '<text class="ifc-svg-t" x="450" y="%d">%s</text>' % (y + 24, t)]
f += ['</svg>', '<figcaption>Hierarquia de controle: do mais eficaz ao menos eficaz (ISO 45001, 8.1.2)</figcaption>', '</figure>']
FIG_HC = '\n'.join(f)

# ---------------------------------------------------------------- numeros
NUMS = [('742 mil', 'acidentes de trabalho notificados no Brasil em 2024'),
        ('542 mil', 'certificados ISO 45001 no mundo em 2024'),
        ('2,8 vezes', 'o número de certificados ISO 45001 de 2020 para 2024'),
        ('26/05/2026', 'riscos psicossociais cobrados na fiscalização da NR-01')]
nums = ('<div class="vi-nums">\n' + '\n'.join('  <div class="vi-num"><b>%s</b><span>%s</span></div>' % n for n in NUMS) + '\n</div>\n'
        '<p class="vi-fonte">Fontes: Observatório de Segurança e Saúde no Trabalho (MPT e OIT), 2024 · ISO Survey 2024 · Portaria MTE 1.419/2024.</p>')

MIOLO = '''<p class="abre">A Ideal Metrics apoia a sua organização na implantação do <strong>sistema de gestão de saúde e segurança ocupacional</strong> e na preparação para a <strong>certificação ISO 45001</strong>.</p>
<p>O trabalho começa pelos perigos reais da operação: tarefas, máquinas, produtos químicos, trabalho em altura e em espaço confinado, contratadas e a rotina de cada área. Levantamos o que já existe, mostramos o que falta para a norma e para as NRs, e montamos com a sua equipe o inventário de riscos, os controles, a consulta aos trabalhadores e a rotina que o organismo certificador vai verificar.</p>
<p>Um sistema de gestão de saúde e segurança ocupacional traz para o mesmo lugar o que as Normas Regulamentadoras já exigem: o gerenciamento de riscos ocupacionais da NR-01, com o inventário de riscos e o plano de ação, o PCMSO da NR-07, a CIPA da NR-05 e as NRs da operação. O resultado são menos acidentes e afastamentos, e evidência organizada para a fiscalização, os clientes e o organismo certificador.</p>

__FIG_NR__

__FIG_HC__

<hr class="section-divider">
<h3>O que o sistema traz</h3>
<div class="fact-grid">
  <div class="pos-card"><h4>Redução de acidentes</h4><p>Perigos identificados e riscos controlados na origem.</p></div>
  <div class="pos-card"><h4>Conformidade com NRs</h4><p>Alinhamento com as Normas Regulamentadoras aplicáveis.</p></div>
  <div class="pos-card"><h4>Cultura de segurança</h4><p>Engajamento das equipes e da liderança.</p></div>
  <div class="pos-card"><h4>Menos passivos</h4><p>Menos afastamentos, multas e passivos trabalhistas.</p></div>
</div>

<hr class="section-divider">
<h3>Como a Ideal Metrics implanta</h3>
<div class="numbered-items">
<div class="numbered-item"><div class="num">01</div><div><h4>Levantamento de perigos</h4><p>Identificação de perigos e avaliação de riscos ocupacionais.</p></div></div>
<div class="numbered-item"><div class="num">02</div><div><h4>Estruturação do sistema</h4><p>Controles, documentação e integração com as NRs.</p></div></div>
<div class="numbered-item"><div class="num">03</div><div><h4>Treinamento</h4><p>Capacitação das equipes e da CIPA.</p></div></div>
<div class="numbered-item"><div class="num">04</div><div><h4>Auditoria interna</h4><p>Verificação da conformidade antes da certificação.</p></div></div>
<div class="numbered-item"><div class="num">05</div><div><h4>Preparação para a certificação</h4><p>Acompanhamento até a certificação e na tratativa dos achados.</p></div></div>
</div>

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
<li><strong>Norma em revisão:</strong> a ISO 45001 está em revisão, com o texto em consulta (DIS) em 2026. Quem implanta agora já sai preparado para a transição.</li>
</ul>

<hr class="section-divider">
<p>A certificação é concedida por organismo acreditado. Para implantar a ISO 45001 na sua operação, <a href="contato.html">fale com a gente</a>.</p>
'''
for k, v in (('__FIG_NR__', FIG_NR), ('__FIG_HC__', FIG_HC), ('__NUMS__', nums)):
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
