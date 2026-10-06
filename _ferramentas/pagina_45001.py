# -*- coding: utf-8 -*-
"""Pagina norma-iso-45001.html na ESTRUTURA GERAL de pagina de servico (05/10/2026).

    python _ferramentas/pagina_45001.py

Ordem aprovada pelo Leandro em 05/10/2026: abertura (com diagrama e chamada de contato) -> por que implantar agora
(numeros, linha do tempo da nova edicao, o que muda) -> o que fazemos (as nove ferramentas, por clausula) -> como
implantamos (cinco etapas + como trabalhamos) -> por que a Ideal Metrics -> aplicacao (fotos) -> a ISO 45001 na pratica
(ISO x NRs, hierarquia de controle, indicadores) -> perguntas frequentes -> normas de referencia -> contato.
«Gosto de diagramas, tabelas de comparacoes; nao gosto de texto pesado, aqui nao e Wikipedia; a pagina traz acima de
tudo uma boa apresentacao da Ideal Metrics.» Troca so o miolo (.content), o css da pagina e o script das fotos;
cabecalho, menus, faixa e rodape ficam como estao. Idempotente.

Fatos e fontes (tudo conferido em 05/10/2026):
- ISO 45001:2018 (iso.org 63787), Amd 1:2024 «Climate action changes» (88428, 2024-02). ISO/DIS 45001 ed. 2 (89698):
  revisao aprovada 2024-05-31; CD em consulta 2025-07-22 a 2025-09-20; CIB para ir a DIS 2026-03-18 a 2026-04-13,
  93% a favor, 81 votos, ABNT sim (ISO/TC 283 N 762, Form 8A); DIS registrado 2026-04-17; votacao 2026-06-16 a
  2026-09-09; «expected to replace ISO 45001:2018 in the first half of 2027». O prefacio do DIS ainda traz a lista
  de mudancas em branco («[insert once complete]»): a tabela compara os sumarios e o texto das clausulas lidas.
- Clausulas do DIS lidas no texto: 4.1 (mudanca climatica), 4.2 (diversidade dos trabalhadores), 6.1.2 (perigos
  psicossociais, clima), 6.3 Planning of changes (nova), 8.1.3 Occupational health (nova), 8.1.4 Return to work (nova),
  8.1.5 Management of change, 8.1.6 Externally provided (era 8.1.4 Aquisicao), 9.3.1-9.3.3, 10.1 Continual
  improvement / 10.2 Nonconformity and corrective action (era 10.2 Incidente, NC e acao corretiva / 10.3).
- Indicadores: ISO 45004:2024, 6.5.2 e Tabela 3 (proativos: treinamento, preocupacoes e sugestoes dos trabalhadores;
  reativos: taxas de lesoes, doencas, incidentes, nao conformidades).
- Hierarquia de controle: ISO 45001, 8.1.2. Figura 1 (PDCA): introducao 0.3/0.4 da norma.
- Prazo de transicao da edicao de 2018: tres anos (IAF). O da nova edicao sai do IAF depois da publicacao.
- NR-01, GRO e PGR; riscos psicossociais pela Portaria MTE 1.419/2024, fiscalizacao desde 26/05/2026.
- Numeros: 742.214 acidentes notificados em 2024 (Observatorio de SST, MPT e OIT); 542.527 certificados ISO 45001 em
  2024 e 190.429 em 2020 (ISO Survey 2024).
- Como trabalhamos: os quatro fatos da pagina como-trabalhamos.html (homens/dia, ~6 meses, ate 5 visitas/mes, Teams).
- Credencial: Lead Auditor ISO 45001 (memoria user-leandro-competencia-auditor). Sem nome de cliente."""
import io, os, re

SITE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ARQ = 'norma-iso-45001.html'
V = '05102026a'                                  # versao das fotos desta pagina
CONFERIDO = '05/10/2026'

# ====================================================================== CSS so desta pagina
CSS = '''<style>
/* 45001 css: fotos, tabelas, linha do tempo e perguntas (05/10/2026) */
.vi-fotos{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:14px;margin:22px 0 28px}
.vi-foto{margin:0}
.vi-quadro{position:relative;aspect-ratio:4/3;overflow:hidden;background:var(--color-bg-alt)}
.vi-quadro img,.vi-gl{position:absolute;inset:0;width:100%;height:100%;display:block}
.vi-quadro img{object-fit:cover}
.vi-quadro.gl-on img{visibility:hidden}
.vi-foto figcaption{font-family:'IBM Plex Mono',monospace;font-size:10.5px;letter-spacing:.2em;text-transform:uppercase;color:var(--color-primary);margin-top:10px}
.im-tab{width:100%;border:1px solid rgba(20,48,76,.14);border-radius:3px;border-collapse:separate;border-spacing:0;margin:22px 0 28px;font-size:14px;line-height:1.35;color:var(--color-primary)}
.im-tab th{font-family:'IBM Plex Mono',monospace;font-size:10.5px;font-weight:500;letter-spacing:.16em;text-transform:uppercase;color:var(--mid-gray);text-align:left;padding:12px 14px 10px;border-bottom:1px solid rgba(20,48,76,.14)}
.im-tab td{padding:11px 14px;border-top:1px solid rgba(20,48,76,.14);vertical-align:top;height:60px}   /* linhas da MESMA altura: duas linhas de texto cabem; uma so ganha o mesmo espaco */
.content h4.vi-sub{margin:28px 0 6px}   /* subtitulo dentro da secao: 28 px do bloco de cima, como o resto do site */
.im-tab tr:first-child td{border-top:0}
.im-tab td.n{font-family:'IBM Plex Mono',monospace;font-size:10.5px;letter-spacing:.14em;color:var(--mid-gray);white-space:nowrap;padding-top:13px}
.im-tab td b{font-weight:600}
.im-tab--c2 td:first-child{width:36%}
.im-rolo{overflow-x:auto;margin:0 -2px}
.vi-4{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:8px;margin:22px 0 28px}
.vi-faq{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:8px;margin:22px 0 28px}
.content .vi-chamada{margin:22px 0 0;font-size:15px}
@media (max-width:760px){
  .vi-fotos,.vi-4,.vi-faq{grid-template-columns:1fr}
  /* tabela vira cartoes: uma linha por registro, o rotulo da coluna acima de cada valor */
  .im-tab thead{display:none}
  .im-tab,.im-tab tbody,.im-tab tr,.im-tab td{display:block;width:100%;box-sizing:border-box}
  .im-tab tr{border-top:1px solid rgba(20,48,76,.14);padding:12px 14px 14px}
  .im-tab tr:first-child{border-top:0}
  .im-tab td{border:0;padding:0;height:auto}
  .im-tab td.n{padding:0 0 4px}
  .im-tab td[data-th]::before{content:attr(data-th);display:block;font-family:'IBM Plex Mono',monospace;font-size:10px;letter-spacing:.14em;text-transform:uppercase;color:var(--mid-gray);margin:9px 0 2px}
  /* diagrama largo rola de lado em vez de encolher o texto; a coluna de conteudo nao estica com ele */
  .page-layout>*,.content{min-width:0}
  .content .vi-rola{overflow-x:auto;-webkit-overflow-scrolling:touch;padding-bottom:4px;max-width:100%}
  .content .vi-rola svg{min-width:var(--vi-min,0px)}
}
/* fim 45001 css */
</style>'''

# ====================================================================== diagramas em linha fina
def fig(linhas, legenda, w, h, aria):
    """figura de linha fina. No celular o diagrama nao encolhe abaixo de uma largura legivel: a figura rola de lado
    (css .vi-rola desta pagina). Largo (900) para no minimo 700 px; os outros, 480."""
    minimo = min(w, 700 if w >= 850 else 480)
    return '\n'.join(['<figure class="ifc-fig vi-rola">',
                      '<svg viewBox="0 0 %d %d" style="max-width:%dpx;--vi-min:%dpx" role="img" aria-label="%s">' % (w, h, w, minimo, aria)] + linhas +
                     ['</svg>', '<figcaption>%s</figcaption>' % legenda, '</figure>'])


def caixa(x, y, w, h, linhas, num=None):
    """caixa de linha fina com texto centrado; num = rotulo mono acima do texto"""
    cx = x + w / 2; out = ['<rect class="ifc-aro ifc-aro--f" x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="3"/>' % (x, y, w, h)]
    n = len(linhas); y0 = y + h / 2 - (n - 1) * 8 + 4 + (5 if num else 0)
    if num: out.append('<text class="ifc-svg-n" x="%.1f" y="%.1f">%s</text>' % (cx, y0 - 15, num))
    for i, t in enumerate(linhas):
        out.append('<text class="ifc-svg-t" x="%.1f" y="%.1f">%s</text>' % (cx, y0 + i * 16, t))
    return out


def seta(x1, y1, x2, y2):
    import math
    a = math.atan2(y2 - y1, x2 - x1); L = 6
    p1 = (x2 - L * math.cos(a - .5), y2 - L * math.sin(a - .5)); p2 = (x2 - L * math.cos(a + .5), y2 - L * math.sin(a + .5))
    return ['<line class="ifc-linha" x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f"/>' % (x1, y1, x2, y2),
            '<polyline class="ifc-linha" points="%.1f,%.1f %.1f,%.1f %.1f,%.1f"/>' % (p1[0], p1[1], x2, y2, p2[0], p2[1])]


# ---------------------------------------------------------------- 1. como a ISO 45001 organiza o sistema (Figura 1 da norma, PDCA)
import math
CX, CY, R = 500, 218, 150                             # o anel do ciclo (raio folgado: o circulo central nao cobre os blocos laterais)
L = ['<rect class="ifc-aro" x="0.5" y="10" width="899" height="404" rx="3"/>',
     '<text class="ifc-svg-n" x="20" y="31" style="text-anchor:start">CONTEXTO DA ORGANIZAÇÃO (4)</text>']
# o anel em quatro arcos, cada um terminando numa seta no sentido horario (entre uma caixa e a seguinte)
for k in range(4):
    a0 = math.radians(-90 + 90 * k + 16); a1 = math.radians(-90 + 90 * (k + 1) - 16)
    x0, y0 = CX + R * math.cos(a0), CY + R * math.sin(a0); x1, y1 = CX + R * math.cos(a1), CY + R * math.sin(a1)
    L.append('<path class="ifc-linha" d="M%.1f,%.1f A%d,%d 0 0 1 %.1f,%.1f"/>' % (x0, y0, R, R, x1, y1))
    tx, ty = -math.sin(a1), math.cos(a1)                # tangente no sentido horario
    nx, ny = math.cos(a1), math.sin(a1)
    L.append('<polyline class="ifc-linha" points="%.1f,%.1f %.1f,%.1f %.1f,%.1f"/>' % (x1 - 7 * tx + 4 * nx, y1 - 7 * ty + 4 * ny, x1, y1, x1 - 7 * tx - 4 * nx, y1 - 7 * ty - 4 * ny))
# as quatro caixas nos pontos cardeais do anel; o rotulo mono diz a fase
L += caixa(CX - 100, CY - R - 23, 200, 46, ['Planejamento (6)'], 'P · PLANEJAR')
L += caixa(CX + R - 75, CY - 31, 150, 62, ['Suporte (7)', 'e operação (8)'], 'D · FAZER')
L += caixa(CX - 100, CY + R - 23, 200, 46, ['Avaliação de desempenho (9)'], 'C · CHECAR')
L += caixa(CX - R - 70, CY - 23, 140, 46, ['Melhoria (10)'], 'A · AGIR')
# no centro, quem sustenta o ciclo
L += ['<circle class="ifc-aro ifc-aro--f" cx="%d" cy="%d" r="62"/>' % (CX, CY),
      '<text class="ifc-svg-t" x="%d" y="%d">Liderança e</text>' % (CX, CY - 12), '<text class="ifc-svg-t" x="%d" y="%d">participação dos</text>' % (CX, CY + 4),
      '<text class="ifc-svg-t" x="%d" y="%d">trabalhadores (5)</text>' % (CX, CY + 20)]
# entradas a esquerda, resultados a direita
L += caixa(16, CY - 86, 196, 50, ['Questões internas', 'e externas (4.1)'])
L += caixa(16, CY + 36, 196, 50, ['Trabalhadores e outras', 'partes interessadas (4.2)'])
L += seta(212, CY - 61, CX - R - 74, CY - 61 + 24) + seta(212, CY + 61, CX - R - 74, CY + 61 - 24)
L += seta(CX + R + 79, CY, 754, CY)
L += caixa(756, CY - 36, 128, 72, ['Resultados', 'pretendidos', 'do sistema'])
FIG_PDCA = fig(L, 'Como a ISO 45001 organiza o sistema (Figura 1 da norma)', 900, 424,
               'Como a ISO 45001 organiza o sistema: no contexto da organização, o ciclo planejar, fazer, checar e agir gira em torno da liderança e da participação dos trabalhadores, das questões e partes interessadas aos resultados pretendidos')

# ---------------------------------------------------------------- 2. linha do tempo da nova edicao
MARCOS = [('mar 2018', 'Publicação da', '1ª edição'),
          ('fev 2024', 'Emenda 1:', 'ações climáticas'),
          ('mai 2024', 'Revisão', 'aprovada'),
          ('jul 2025', 'Texto do comitê', 'em consulta (CD)'),
          ('abr 2026', 'Comitê aprova', 'o DIS (93%)'),
          ('set 2026', 'Votação do DIS', 'encerrada'),
          ('1º sem. 2027', 'Publicação', 'prevista'),
          ('depois', 'Transição: prazo', 'definido pelo IAF')]
L = ['<line class="ifc-linha" x1="60" y1="70" x2="790" y2="70"/>',
     '<line class="ifc-linha" x1="790" y1="70" x2="860" y2="70" stroke-dasharray="4 4"/>']
for i, (data, a, b) in enumerate(MARCOS):
    x = 60 + i * 110; futuro = i >= 6
    L += ['<circle class="ifc-aro ifc-aro--f" cx="%d" cy="70" r="11"%s/>' % (x, ' stroke-dasharray="3 3"' if futuro else ''),
          ('<circle cx="%d" cy="70" r="3.5" fill="#14304C"/>' % x) if not futuro else '<circle class="ifc-aro" cx="%d" cy="70" r="3.5"/>' % x,
          '<text class="ifc-svg-n" x="%d" y="42">%s</text>' % (x, data.upper()),
          '<text class="ifc-svg-p" x="%d" y="108">%s</text>' % (x, a), '<text class="ifc-svg-p" x="%d" y="124">%s</text>' % (x, b)]
xh = 60 + 5 * 110 + 30                                   # hoje: entre a votacao encerrada e a publicacao
L += ['<line class="ifc-linha" x1="%d" y1="52" x2="%d" y2="88"/>' % (xh, xh), '<text class="ifc-svg-n" x="%d" y="150">HOJE · OUT 2026</text>' % xh]
FIG_LINHA = fig(L, 'A nova edição da ISO 45001: de onde veio e quando chega', 900, 165,
                'Linha do tempo da revisão da ISO 45001: primeira edição em 2018, emenda em 2024, revisão aprovada em 2024, texto do comitê em 2025, DIS aprovado e votado em 2026, publicação prevista para o primeiro semestre de 2027 e transição depois')

# ---------------------------------------------------------------- 3. as cinco etapas da implantacao (as mesmas de toda pagina)
# 05/10: «o diagrama de como implantamos esta identico a linha do tempo, faca diferente». Vira CRONOGRAMA: as cinco
# etapas em barras sobre os seis meses tipicos de projeto (como-trabalhamos.html: «projetos de cerca de 6 meses"),
# com o que corre em paralelo; a ultima etapa e um marco (losango) no fim do sexto mes.
PASSOS = [('01', 'Diagnóstico', 'a operação contra a norma e as NRs', 0.0, 1.0),
          ('02', 'Plano diretor', 'prazo, responsável e capacitação', 0.75, 1.75),
          ('03', 'Implantação', 'perigos, controles, PAE e indicadores', 1.5, 5.0),
          ('04', 'Auditoria interna', 'e análise crítica pela direção', 4.75, 5.75),
          ('05', 'Organização pronta', 'para a certificação ISO 45001', 6.0, 6.0)]
X0, MES, Y0, LIN = 270, 100, 46, 46               # coluna de rotulos ate 270 (o losango do fim cabe no 900); seis meses de 100 px; linhas de 46 px
L = []
for m in range(7):                                 # grade dos meses
    x = X0 + m * MES
    L.append('<line class="ifc-aro" x1="%d" y1="%d" x2="%d" y2="%d"/>' % (x, Y0 - 12, x, Y0 + 5 * LIN - 6))
    if m < 6: L.append('<text class="ifc-svg-n" x="%d" y="%d">MÊS %d</text>' % (x + MES // 2, Y0 - 20, m + 1))
for i, (n, t, sub, a, b) in enumerate(PASSOS):
    y = Y0 + i * LIN; cy = y + 17
    L += ['<text class="ifc-svg-n" x="0" y="%d" style="text-anchor:start">%s</text>' % (cy - 2, n),
          '<text class="ifc-svg-t" x="30" y="%d" style="text-anchor:start">%s</text>' % (cy - 3, t),
          '<text class="ifc-svg-p" x="30" y="%d" style="text-anchor:start">%s</text>' % (cy + 13, sub)]
    if b > a:
        L.append('<rect x="%.1f" y="%d" width="%.1f" height="22" rx="3" fill="rgba(51,102,153,.22)" stroke="rgba(20,48,76,.35)" stroke-width="1" vector-effect="non-scaling-stroke"/>'
                 % (X0 + a * MES + 3, cy - 11, (b - a) * MES - 6))
    else:
        xm = X0 + a * MES
        L.append('<polygon points="%.1f,%d %.1f,%d %.1f,%d %.1f,%d" fill="#14304C"/>' % (xm, cy - 11, xm + 11, cy, xm, cy + 11, xm - 11, cy))
FIG_PASSOS = fig(L, 'As cinco etapas num projeto típico de 6 meses', 900, Y0 + 5 * LIN,
                 'Cronograma típico de 6 meses: diagnóstico no primeiro mês, plano diretor do fim do primeiro ao segundo mês, implantação do segundo ao quinto mês, auditoria interna e análise crítica no fim do quinto e no sexto mês, e a organização pronta para a certificação no fim do sexto mês')

# ---------------------------------------------------------------- 4. a ISO 45001 e as NRs no mesmo sistema
PARES = [('5.4 · Consulta e participação', 'NR-05 · CIPA'),
         ('6.1.2 · Perigos e riscos', 'NR-01 · GRO: inventário e plano de ação'),
         ('7.2 · Competência', 'NR-10, NR-12, NR-33, NR-35 · capacitação'),
         ('8.2 · Emergências', 'NR-01 · preparação para emergências'),
         ('9.1 · Monitoramento', 'NR-07 · PCMSO · NR-09 · exposições'),
         ('10.2 · Incidentes e ação corretiva', 'NR-01 · análise de acidentes e doenças')]
PAD, LIGA = 24, 120
WL, WR = 182 + 2 * PAD, 234 + 2 * PAD
XR = WL + LIGA; W = XR + WR
L = ['<text class="ifc-svg-n" x="%d" y="22">ISO 45001</text>' % (WL // 2), '<text class="ifc-svg-n" x="%d" y="22">NORMAS REGULAMENTADORAS</text>' % (XR + WR // 2)]
for i, (iso, nr) in enumerate(PARES):
    y = 40 + i * 44; cy = y + 17
    L += ['<rect class="ifc-aro ifc-aro--f" x="0.5" y="%d" width="%d" height="34" rx="3"/>' % (y, WL),
          '<rect class="ifc-aro ifc-aro--f" x="%.1f" y="%d" width="%d" height="34" rx="3"/>' % (XR + .5, y, WR),
          '<text class="ifc-svg-t" x="%d" y="%d">%s</text>' % (WL // 2, cy + 5, iso), '<text class="ifc-svg-t" x="%d" y="%d">%s</text>' % (XR + WR // 2, cy + 5, nr),
          '<line class="ifc-linha" x1="%d" y1="%d" x2="%d" y2="%d"/>' % (WL + 6, cy, XR - 6, cy),
          '<circle cx="%d" cy="%d" r="3.5" fill="#14304C"/>' % (WL + 6, cy), '<circle cx="%d" cy="%d" r="3.5" fill="#14304C"/>' % (XR - 6, cy)]
FIG_NR = fig(L, 'A ISO 45001 e as NRs no mesmo sistema', W + 1, 300, 'A ISO 45001 e as Normas Regulamentadoras no mesmo sistema')

# ---------------------------------------------------------------- 5. a hierarquia de controle (ISO 45001, 8.1.2)
NIVEIS = ['Eliminar o perigo', 'Substituir processo, material ou equipamento', 'Controles de engenharia e reorganização do trabalho',
          'Controles administrativos, inclusive treinamento', 'Equipamento de proteção individual']
TXT = [92, 249, 287, 265, 197]
req = [t + 2 * 56 for t in TXT]
larg = [0] * 5; larg[4] = req[4]
for i in range(3, -1, -1):
    larg[i] = max(req[i], larg[i + 1] + 56)
W = larg[0] + 2; L = []
for i, t in enumerate(NIVEIS):
    w = larg[i]; x = (W - w) / 2; y = 10 + i * 46
    L += ['<rect class="ifc-aro ifc-aro--f" x="%.1f" y="%d" width="%d" height="38" rx="3"/>' % (x, y, w),
          '<text class="ifc-svg-n" x="%.1f" y="%d">0%d</text>' % (x + 26, y + 23, i + 1), '<text class="ifc-svg-t" x="%.1f" y="%d">%s</text>' % (W / 2, y + 24, t)]
FIG_HC = fig(L, 'Hierarquia de controle: do mais eficaz ao menos eficaz (ISO 45001, 8.1.2)', W, 250, 'Hierarquia de controle da ISO 45001, do mais eficaz ao menos eficaz')

# ====================================================================== tabelas
def tabela(cab, linhas, cls='', col_n=True, rot_de=2):
    """tabela de linha fina; a primeira coluna pode ser o numero da clausula (mono). No celular cada linha vira um
    cartao e, da coluna rot_de em diante, o rotulo do cabecalho aparece acima do valor (data-th)."""
    h = ['<div class="im-rolo"><table class="im-tab%s">' % ((' ' + cls) if cls else ''), '<thead><tr>' + ''.join('<th>%s</th>' % c for c in cab) + '</tr></thead>', '<tbody>']
    for ln in linhas:
        cels = ''
        for k, c in enumerate(ln):
            if col_n and k == 0: cels += '<td class="n">%s</td>' % c
            elif k >= rot_de and cab[k]: cels += '<td data-th="%s">%s</td>' % (cab[k], c)
            else: cels += '<td>%s</td>' % c
        h.append('<tr>' + cels + '</tr>')
    h += ['</tbody></table></div>']
    return '\n'.join(h)


# as nove ferramentas (lista do Leandro, 05/10/2026), cada uma na clausula da ISO 45001:2018 e com o que a organizacao recebe
FERRAMENTAS = [('6.2 · 9.1', 'Objetivos, metas e indicadores de SST', 'Objetivos com meta, indicador e responsável, e o painel de acompanhamento.'),
               ('6.1.3 · 9.1.2', 'Interpretação e atendimento legal', 'Matriz de requisitos legais, com a evidência de cada obrigação e a avaliação da conformidade.'),
               ('6.1.2 · 8.1.2', 'Identificação de perigos e controle de riscos', 'Inventário de riscos e plano de ação do GRO da NR-01, com os riscos psicossociais.'),
               ('8.1', 'Controles operacionais alinhados às NRs', 'Procedimentos, permissões de trabalho e os controles das NRs da operação.'),
               ('7.2 · 7.3', 'Treinamento do pessoal', 'Matriz de competências, treinamentos realizados e registros.'),
               ('8.2', 'Plano de atendimento a emergências (PAE)', 'PAE, equipes de resposta, simulados e registros.'),
               ('9.2', 'Auditoria interna', 'Auditores internos formados, programa de auditoria e relatório.'),
               ('9.3', 'Análise crítica pela direção', 'Reunião com as entradas da norma, decisões e registro.'),
               ('10.2', 'Tratamento de não conformidades', 'Investigação de incidentes, causa, ação corretiva e verificação da eficácia.')]
TAB_FERR = tabela(['Cláusula', 'Ferramenta', 'O que a organização recebe'], [(c, '<b>%s</b>' % f, e) for c, f, e in FERRAMENTAS])

# o que muda da edicao de 2018 para a nova (sumarios e texto do DIS, lidos em 05/10/2026)
MUDA = [('4.1', 'Mudança climática', 'Entra pela Emenda 1:2024', 'No texto: a organização determina se a mudança climática é questão pertinente'),
        ('4.2', 'Diversidade dos trabalhadores', 'Sem menção', 'Considerada ao determinar necessidades e expectativas'),
        ('6.1.2', 'Perigos psicossociais e climáticos', 'Psicossociais na lista de perigos', 'Psicossociais detalhados; eventos climáticos extremos entram na lista'),
        ('6.3', 'Planejamento de mudanças', 'Só a gestão da mudança, na operação (8.1.3)', 'Cláusula nova: riscos avaliados antes de qualquer mudança'),
        ('8.1.3', 'Saúde ocupacional', 'Sem cláusula própria', 'Cláusula nova: prevenção, detecção precoce e acesso a serviços de saúde'),
        ('8.1.4', 'Retorno ao trabalho', 'Sem cláusula própria', 'Cláusula nova: reintegração após lesão ou doença, com ajuste de funções'),
        ('8.1.6', 'Contratadas e fornecedores', '8.1.4 Aquisição, contratados e terceirização', 'Processos, produtos e serviços providos externamente, com grau de controle pelo risco'),
        ('9.3', 'Análise crítica pela direção', 'Um bloco único', 'Entradas e resultados em subcláusulas próprias'),
        ('10', 'Melhoria', '10.2 Incidente, não conformidade e ação corretiva; 10.3 Melhoria contínua', 'Melhoria contínua passa a 10.1; não conformidade e ação corretiva, a 10.2')]
TAB_MUDA = tabela(['Cláusula', 'Tema', 'ISO 45001:2018', 'ISO/DIS 45001 (nova edição)'], [(c, '<b>%s</b>' % t, a, b) for c, t, a, b in MUDA])

# indicadores proativos e reativos (ISO 45004:2024, Tabela 3)
TAB_IND = tabela(['', 'Indicadores proativos', 'Indicadores reativos'], col_n=False, rot_de=1, linhas=
                 [('O que medem', 'Ações que influenciam o desempenho futuro', 'Resultados e eventos passados'),
                  ('Exemplos', 'Treinamento dos trabalhadores em perigos e controles, com a eficácia verificada; preocupações e sugestões registradas pelos trabalhadores',
                   'Taxas de lesões, doenças ocupacionais, incidentes e não conformidades')])

# ====================================================================== numeros, fotos, como trabalhamos, perguntas
NUMS = [('742 mil', 'acidentes de trabalho notificados no Brasil em 2024'),
        ('542 mil', 'certificados ISO 45001 no mundo em 2024'),
        ('2,8 vezes', 'o número de certificados ISO 45001 de 2020 para 2024'),
        ('26/05/2026', 'riscos psicossociais cobrados na fiscalização da NR-01')]
NUMS_HTML = ('<div class="vi-nums">\n' + '\n'.join('  <div class="vi-num"><b>%s</b><span>%s</span></div>' % n for n in NUMS) + '\n</div>\n'
             '<p class="vi-fonte">Fontes: Observatório de Segurança e Saúde no Trabalho (MPT e OIT), 2024 · ISO Survey 2024 · Portaria MTE 1.419/2024.</p>')

FOTOS = [('sso-industria', 'Indústria de processo'), ('viaria-frota', 'Logística e frota'), ('sso-armazenagem', 'Armazenagem e portos')]
FOTOS_HTML = '<div class="vi-fotos">\n' + '\n'.join(
    '  <figure class="vi-foto"><div class="vi-quadro"><img src="img/%s-bayer.webp?v=%s" data-lum="img/%s-lum.webp?v=%s" alt="" loading="lazy"></div><figcaption>%s</figcaption></figure>'
    % (n, V, n, V, leg) for n, leg in FOTOS) + '\n</div>'
for n, _ in FOTOS:
    for t in ('lum', 'bayer'):
        assert os.path.exists(os.path.join(SITE, 'img', '%s-%s.webp' % (n, t))), 'falta a foto img/%s-%s.webp (rodar _ferramentas/foto_azul.py)' % (n, t)

MODELO = [('01', 'Consultoria por homens/dia', 'Dias dimensionados ao que o projeto exige.'),
          ('02', 'Cerca de 6 meses', 'Do diagnóstico à organização pronta para a certificação.'),
          ('03', 'Até 5 visitas por mês', 'Presença na operação, na frequência que o cronograma pede.'),
          ('04', 'Reuniões online', 'Entre as visitas, pelo Microsoft Teams, com registro do que foi tratado.')]
MODELO_HTML = '<div class="vi-4">\n' + '\n'.join('  <div class="ifc-cel"><span class="ifc-rot">%s</span><h4>%s</h4><p>%s</p></div>' % m for m in MODELO) + '\n</div>'

FAQ = [('Quanto tempo leva a implantação?', 'Cerca de 6 meses, do diagnóstico à organização pronta para a certificação. O prazo depende do porte da operação e do que já existe.'),
       ('Quem participa pela organização?', 'A direção, a área de segurança (SESMT), a CIPA e os líderes de área. A Ideal Metrics conduz, e a equipe constrói o sistema junto.'),
       ('O que o organismo certificador verifica?', 'Na primeira fase, a documentação e a prontidão. Na segunda, o sistema em funcionamento, com a auditoria interna e a análise crítica já realizadas.'),
       ('A ISO 45001 se integra à ISO 9001 e à ISO 14001?', 'Sim. As três têm a mesma estrutura, e política, riscos, auditoria interna e análise crítica podem ser um processo só.')]
FAQ_HTML = '<div class="vi-faq">\n' + '\n'.join('  <div class="ifc-cel"><h4>%s</h4><p>%s</p></div>' % f for f in FAQ) + '\n</div>'

NORMAS = ['ISO 45001:2018, com a Emenda 1:2024 (ações climáticas): sistemas de gestão de saúde e segurança ocupacional.',
          'ISO/DIS 45001: a segunda edição, com publicação prevista para o primeiro semestre de 2027.',
          'ISO 45004:2024: diretrizes para a avaliação do desempenho de saúde e segurança ocupacional.',
          'NR-01: gerenciamento de riscos ocupacionais (GRO e PGR), com os fatores de risco psicossociais (Portaria MTE 1.419/2024).',
          'NR-05 (CIPA), NR-07 (PCMSO) e as NRs da operação.']

# ====================================================================== o miolo
MIOLO = '''<p class="abre">A Ideal Metrics apoia a sua organização na implantação do sistema de gestão de saúde e segurança ocupacional e na preparação para a certificação ISO 45001.</p>
<p>O trabalho começa pelos perigos reais da operação: tarefas, máquinas, produtos químicos, trabalho em altura e em espaço confinado, contratadas e a rotina de cada área. Levantamos o que já existe, mostramos o que falta para a norma e para as NRs, e montamos com a sua equipe o sistema que o organismo certificador vai verificar.</p>

__FIG_PDCA__
<p class="vi-chamada">Para falar do seu projeto, <a href="contato.html">fale com a gente</a>.</p>

<hr class="section-divider">
<h3>Por que implantar agora</h3>
__NUMS__
__FIG_LINHA__
<p class="vi-fonte">Fontes: catálogo da ISO (iso.org) e ISO/TC 283, formulário 8A N 762, abril de 2026, conferidos em __CONFERIDO__. Na edição de 2018, o IAF deu três anos para a transição.</p>
<h4 class="vi-sub">O que muda na nova edição</h4>
__TAB_MUDA__
<p class="vi-fonte">Comparação dos sumários e do texto do ISO/DIS 45001 (2026) com a ISO 45001:2018. O texto está em votação, e a lista oficial de mudanças ainda não foi publicada pela ISO.</p>
<ul>
<li><strong>Riscos psicossociais:</strong> desde 26/05/2026 a fiscalização cobra a avaliação dos fatores de risco psicossociais no gerenciamento de riscos da NR-01. Quem tem o sistema implantado já tem o processo para incluí-los no inventário.</li>
<li><strong>Exigência de contratantes:</strong> a qualificação de fornecedores e de contratadas costuma pedir gestão de saúde e segurança com evidência.</li>
<li><strong>Nova edição em 2027:</strong> quem implanta agora pela edição de 2018 já sai com saúde ocupacional, retorno ao trabalho e planejamento de mudanças no sistema, e faz a transição sem refazer o trabalho.</li>
</ul>

<hr class="section-divider">
<h3>O que fazemos</h3>
<p>Nove ferramentas, cada uma ligada à cláusula da ISO 45001 que a exige, e o que fica na organização ao fim do projeto.</p>
__TAB_FERR__

<hr class="section-divider">
<h3>Como implantamos</h3>
__FIG_PASSOS__
<h4 class="vi-sub">Como trabalhamos</h4>
__MODELO__
<p class="vi-chamada">O modelo completo está em <a href="como-trabalhamos.html">Como trabalhamos</a>.</p>

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
__FOTOS__
<ul>
<li>Indústrias com máquinas, produtos químicos, trabalho em altura e em espaço confinado.</li>
<li>Construção, montagem e manutenção, com contratadas no mesmo local.</li>
<li>Logística, armazenagem e operações com frota.</li>
<li>Empresas de serviço com equipes nas instalações dos clientes.</li>
<li>Organizações que precisam revisar o PGR para os riscos psicossociais.</li>
</ul>

<hr class="section-divider">
<h3>A ISO 45001 na prática</h3>
<p>Um sistema de gestão de saúde e segurança ocupacional traz para o mesmo lugar o que as NRs já exigem: o GRO da NR-01, com o inventário de riscos e o plano de ação, o PCMSO da NR-07, a CIPA da NR-05 e as NRs da operação.</p>
__FIG_NR__
__FIG_HC__
<h4 class="vi-sub">Os indicadores que o sistema acompanha</h4>
__TAB_IND__
<p class="vi-fonte">Fonte: ISO 45004:2024, Tabela 3.</p>

<hr class="section-divider">
<h3>Perguntas frequentes</h3>
__FAQ__

<hr class="section-divider">
<h3>Normas de referência</h3>
<ul>
__NORMAS__
</ul>
<p class="vi-fonte">Situação das normas conferida no catálogo da ISO (iso.org) em __CONFERIDO__.</p>

<hr class="section-divider">
<p>A certificação é concedida por organismo acreditado. Para implantar a ISO 45001 na sua operação, <a href="contato.html">fale com a gente</a>.</p>
'''
for k, v in (('__FIG_PDCA__', FIG_PDCA), ('__FIG_LINHA__', FIG_LINHA), ('__FIG_PASSOS__', FIG_PASSOS), ('__FIG_NR__', FIG_NR), ('__FIG_HC__', FIG_HC),
             ('__NUMS__', NUMS_HTML), ('__TAB_MUDA__', TAB_MUDA), ('__TAB_FERR__', TAB_FERR), ('__TAB_IND__', TAB_IND), ('__MODELO__', MODELO_HTML),
             ('__FOTOS__', FOTOS_HTML), ('__FAQ__', FAQ_HTML), ('__NORMAS__', '\n'.join('<li>%s</li>' % n for n in NORMAS)), ('__CONFERIDO__', CONFERIDO)):
    MIOLO = MIOLO.replace(k, v)
assert '__' not in re.sub(r'<[^>]+>', '', MIOLO).replace('__', '__'), 'marcador sem troca'
for palavra in ('percurso', 'Percurso', 'caminho', 'ponto de partida', 'Ponto de partida', 'exame', 'auditoria de certificação', 'Para quem',
                'A norma traz', '<p>Ela ', '<p>Ele ', 'não certificamos', 'fundada em 1998', 'Fundada em 1998'):
    assert palavra not in MIOLO, 'palavra vetada no texto: ' + palavra

JS = '''<script>
/* 45001 js: as fotos desta pagina passam pelo motor da trama, no tom azul do site */
(function(){
  if(!window.ditherVivo) return;
  [].forEach.call(document.querySelectorAll('.vi-quadro'), function(q){
    var im = q.querySelector('img'); if(!im) return;
    window.ditherVivo({brilhoTom:0.35, gama:0.88, ctr:1.55, escuro:0.35, lavaRepouso:0.12, raiz:q, planos:[{el:q, lum:im.getAttribute('data-lum')}], classeCanvas:'vi-gl', revelar:'visivel',
      cores:[[21.2,50.9,80.6],[24.2,56.2,88.1],[103.0,146.1,189.4],[250,249,245]], pincel:.7, zoomHover:1.035});
  });
})();
/* fim 45001 js */
</script>'''

# ====================================================================== monta
P = os.path.join(SITE, ARQ)
s = io.open(P, encoding='utf-8', newline='').read()
eol = '\r\n' if '\r\n' in s else '\n'
s = s.replace('\r\n', '\n')
s = re.sub(r'\n?<style>\n/\* 45001 css.*?/\* fim 45001 css \*/\n</style>', '', s, flags=re.S)
s = re.sub(r'\n?<script>\n/\* 45001 js.*?/\* fim 45001 js \*/\n</script>', '', s, flags=re.S)
assert s.count('</head>') == 1
s = s.replace('</head>', CSS + '\n</head>')
i = s.index('<div class="content">') + len('<div class="content">')
j = s.index('</div>\n</div>\n<footer')
s = s[:i] + '\n' + MIOLO + s[j:]
m = re.search(r'<script src="js/banner\.js\?v=\d+"></script>', s)       # a tag do banner.js, seja qual for a versao
assert m and len(re.findall(r'<script src="js/banner\.js\?v=\d+"></script>', s)) == 1
s = s[:m.end()] + '\n' + JS + s[m.end():]
io.open(P, 'w', encoding='utf-8', newline='').write(s.replace('\n', eol))
print('%s: %d bytes' % (ARQ, len(s)))
