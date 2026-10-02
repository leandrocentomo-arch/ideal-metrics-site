# -*- coding: utf-8 -*-
"""A pagina «Gestao de Seguranca Viaria» (seguranca-viaria.html), 02/10/2026.

    python _ferramentas/pagina_viaria.py

E O MOLDE DAS PAGINAS DE SERVICO. O que o Leandro ensinou ao ver a primeira versao (02/10/2026):
  - a pagina VENDE CONSULTORIA: quem entra quer saber se prestamos o servico de apoio a implantacao do sistema
    para a certificacao, nao aprender a norma («aqui nao e uma biblioteca de aprendizado»). O texto abre pelo
    servico e fica em topicos curtos; nada de secao «o que e a norma» nem diagrama didatico de requisitos;
  - a Ideal Metrics IMPLANTA e PREPARA para a certificacao; nao faz auditoria de certificacao, entao a pagina
    nunca diz «ate a auditoria de certificacao»;
  - sem palavra de trocadilho com o tema («percurso», «caminho», «ponto de partida») e sem a rodovia desenhada
    como diagrama; o diagrama de etapas e o de linha fina da pagina do IFC;
  - a linha dos consultores nao fala em «exame de aprovacao»;
  - norma de apoio: so a que ele usa, a ISO 39002 (base de ferramentas como a analise de risco viario);
  - titulo «Aplicacao», nao «Para quem e»;
  - foto do topo: vista aerea de rodovia (drone), sem gente; a primeira tinha um fiscal ao lado de uma viatura
    e foi lida como policial dando multa;
  - cara de infografico: numeros com fonte, fotos aereas, diagrama dos ODS da ONU (os quadros dos ODS ficam nas
    cores oficiais; o resto, na tinta da casa).

A CASCA (cabecalho, menus, navegacao lateral, rodape, scripts) vem da ifc-performance-standards.html; aqui fica
so o miolo. As figuras sao SVG em linha fina, com as classes .ifc-* do css/style.css; o que e so desta pagina
vai num <style> no <head>. As fotos vem do Google Flow e passam pelo _ferramentas/foto_azul.py (as tres da
faixa) e pelo _ferramentas/banner/foto_banner.py (a do topo).

FONTES (conferidas em 02/10/2026):
  - ISO/TC 241 (iso.org/committee/558313): 36 membros participantes; ODS 3, 11 e 12; ISO 39001:2012 e
    Amd 1:2024; ISO/WD 39001.2 (2a edicao, projeto aprovado em 25/03/2026); ISO 39002:2020;
  - OMS, Global status report on road safety 2023: 1,19 milhao de mortes por ano; principal causa de morte
    de 5 a 29 anos;
  - ONU: ODS 3 (meta 3.6, indicador 3.6.1), ODS 11 (meta 11.2), ODS 12 (meta 12.6, leitura nossa: a ISO nao
    aponta meta); Resolucao 74/299 (Segunda Decada de Acao, 2021 a 2030, reducao de 50%);
  - PL 710/2024 (Senado): aprovado no Senado e enviado a Camara;
  - experiencia e formacao: atestado de capacidade tecnica e certificado do curso, na pasta de projetos do vault.
Nomes de cliente nao entram na pagina."""
import os, re, io

SITE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
casca = io.open(os.path.join(SITE, 'ifc-performance-standards.html'), encoding='utf-8', newline='').read()
eol = '\r\n' if '\r\n' in casca else '\n'
s = casca.replace('\r\n', '\n')

ARQ = 'seguranca-viaria.html'
V = '02102026g'                                 # versao das fotos desta pagina
TITULO = 'Gestão da Segurança Viária'
SUB = 'Apoio na implantação do sistema de gestão da segurança viária, para a certificação ISO 39001.'
DESC = ('Consultoria para implantação da ISO 39001: sistema de gestão da segurança viária, análise de risco viário, '
        'metas, indicadores e preparação para a certificação. Para concessionárias de rodovias, frotas e transporte.')

CSS = '''<style>
/* so desta pagina: numeros, fotos e textos dos diagramas */
.vi-nums{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:8px;margin:22px 0 8px}
.vi-num{background:var(--color-bg-alt);border:1px solid rgba(20,48,76,.14);border-radius:3px;padding:18px 18px 16px}
.vi-num b{display:block;font:700 31px/1 'IBM Plex Sans Condensed',sans-serif;color:var(--color-primary);letter-spacing:-.01em;white-space:nowrap}
.vi-num span{display:block;margin-top:9px;font-size:14px;line-height:1.3;color:var(--color-primary)}
.content p.vi-fonte{font-family:'IBM Plex Mono',monospace;font-size:10.5px;line-height:1.6;letter-spacing:.04em;margin:8px 0 0}
.content .vi-nums + p.vi-fonte{margin-bottom:28px}   /* 02/10: a fonte dos numeros fica junto deles; a lista que vem depois, a 28 px */
.vi-fotos{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:14px;margin:22px 0 28px}
.vi-foto{margin:0}
.vi-quadro{position:relative;aspect-ratio:4/3;overflow:hidden;background:var(--color-bg-alt)}
.vi-quadro img,.vi-gl{position:absolute;inset:0;width:100%;height:100%;display:block}
.vi-quadro img{object-fit:cover}
.vi-quadro.gl-on img{visibility:hidden}
.vi-foto figcaption{font-family:'IBM Plex Mono',monospace;font-size:10.5px;letter-spacing:.2em;text-transform:uppercase;color:var(--color-primary);margin-top:10px}
.vi-ods{margin:22px 0 28px}
.vi-ods-linha{display:flex;flex-wrap:wrap;align-items:center;gap:16px}
.vi-ods-bt{appearance:none;-webkit-appearance:none;border:0;padding:0;background:none;cursor:pointer;width:128px;line-height:0;border-radius:3px;
  transition:transform .35s cubic-bezier(.4,0,.2,1),box-shadow .3s}
.vi-ods-bt img{width:100%;height:auto;display:block;border-radius:3px}
.vi-ods-bt:hover,.vi-ods-bt:focus-visible{transform:translateY(-4px);outline:none}
.vi-ods-bt.on{transform:translateY(-4px);box-shadow:0 0 0 3px var(--color-bg-alt),0 0 0 4px #14304C}
.vi-ods-dica{font-family:'IBM Plex Mono',monospace;font-size:10.5px;letter-spacing:.14em;text-transform:uppercase;color:var(--color-primary);margin-left:8px}
.vi-ods-painel{display:grid;grid-template-rows:0fr;transition:grid-template-rows .45s cubic-bezier(.4,0,.2,1)}
.vi-ods-painel.on{grid-template-rows:1fr}
.vi-ods-painel>div{overflow:hidden;min-height:0}
.vi-ods-sub{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:8px;margin-top:28px}
@media (max-width:760px){.vi-nums{grid-template-columns:repeat(2,minmax(0,1fr))}.vi-fotos{grid-template-columns:1fr}.vi-ods-sub{grid-template-columns:1fr}.vi-ods-bt{width:96px}.vi-ods-dica{flex-basis:100%;margin-left:0}}
</style>'''

# ---------------------------------------------------------------- o que fazemos (grade de seis, uma linha cada)
CEL = [('01', 'Diagnóstico e plano diretor', 'O que falta para a ISO 39001, com prazo e responsável.'),
       ('02', 'Análise de risco viário', 'Perigos por rota, veículo, condutor e jornada.'),
       ('03', 'Metas e indicadores', 'Fatores de desempenho da segurança viária, com meta para cada um.'),
       ('04', 'Procedimentos e emergência', 'Controles para condutores, frota e contratadas, e plano de emergência.'),
       ('05', 'Investigação de sinistros', 'Método de análise de causa e ação corretiva.'),
       ('06', 'Auditoria interna', 'Formação de auditores, auditoria interna e análise crítica pela direção.')]
grade = '<div class="ifc-grade">\n' + '\n'.join(
    '  <div class="ifc-cel"><span class="ifc-rot">%s</span><h4>%s</h4><p>%s</p></div>' % c for c in CEL) + '\n</div>'

# ---------------------------------------------------------------- as etapas (linha fina, como na pagina do IFC)
PASSOS = [('01', 'Diagnóstico', 'a operação contra', 'a ISO 39001'),
          ('02', 'Plano diretor', 'prazo, responsável', 'e capacitação'),
          ('03', 'Implantação', 'risco viário, metas', 'e controles'),
          ('04', 'Auditoria interna', 'e análise crítica', 'pela direção'),
          ('05', 'Organização pronta', 'para a certificação', 'ISO 39001')]
f1 = ['<figure class="ifc-fig">',
      '<svg viewBox="0 0 1100 200" role="img" aria-label="As cinco etapas da implantação: diagnóstico, plano diretor, implantação, auditoria interna e organização pronta para a certificação">',
      '<line class="ifc-linha" x1="110" y1="66" x2="990" y2="66"/>']
for i, (n, t, p1, p2) in enumerate(PASSOS):
    x = 110 + i * 220
    f1 += ['<circle class="ifc-aro ifc-aro--f" cx="%d" cy="66" r="13"/>' % x,
           '<circle cx="%d" cy="66" r="3.5" fill="#14304C"/>' % x,
           '<text class="ifc-svg-n" x="%d" y="38">%s</text>' % (x, n),
           '<text class="ifc-svg-t" x="%d" y="110">%s</text>' % (x, t),
           '<text class="ifc-svg-p" x="%d" y="132">%s</text>' % (x, p1),
           '<text class="ifc-svg-p" x="%d" y="148">%s</text>' % (x, p2)]
f1 += ['</svg>', '<figcaption>As cinco etapas da implantação</figcaption>', '</figure>']
FIG1 = '\n'.join(f1)

# ---------------------------------------------------------------- numeros
NUMS = [('1,19 milhão', 'de mortes no trânsito por ano, no mundo'),
        ('5 a 29 anos', 'faixa de idade em que o trânsito é a principal causa de morte'),
        ('50%', 'de redução de mortes e feridos até 2030: a meta da ONU'),
        ('36 países', 'participam do comitê da ISO que mantém a ISO 39001')]
nums = ('<div class="vi-nums">\n' + '\n'.join('  <div class="vi-num"><b>%s</b><span>%s</span></div>' % n for n in NUMS) + '\n</div>\n'
        '<p class="vi-fonte">Fontes: OMS, Global status report on road safety 2023 · Assembleia Geral da ONU, Resolução 74/299 · ISO/TC 241, outubro de 2026.</p>')

# ---------------------------------------------------------------- a ISO 39001 e os ODS da ONU
# 02/10 (3a volta): «use os logos oficiais do ODS, com efeito de abrir e ler os subelementos». Os tres icones
# sao os oficiais em portugues (ONU Brasil, brasil.un.org, img/ods-NN.svg), sem alteracao; um clique abre o
# painel com a meta, o indicador e a ligacao com a ISO 39001. A linha de aviso e a que a ONU pede para uso
# informativo dos icones.
ODS = [('03', 'ODS 3: Saúde e bem-estar',
        [('Meta 3.6', 'Reduzir pela metade as mortes e os ferimentos por acidentes em estradas.'),
         ('Indicador 3.6.1', 'Taxa de mortalidade por acidentes de trânsito.'),
         ('Na ISO 39001', 'É o resultado final que o sistema mede e reduz: mortes e lesões graves.')]),
       ('11', 'ODS 11: Cidades e comunidades sustentáveis',
        [('Meta 11.2', 'Até 2030, transporte seguro, acessível e sustentável para todos, com melhoria da segurança rodoviária.'),
         ('Indicador 11.2.1', 'Proporção da população com acesso adequado a transporte público.'),
         ('Na ISO 39001', 'Operação de vias e de transporte com os riscos viários sob controle.')]),
       ('12', 'ODS 12: Consumo e produção responsáveis',
        [('Meta 12.6', 'Empresas com práticas sustentáveis e com essa informação nos seus relatórios.'),
         ('Indicador 12.6.1', 'Número de empresas que publicam relatórios de sustentabilidade.'),
         ('Na ISO 39001', 'Metas e indicadores de segurança viária prontos para o relatório de sustentabilidade.')])]
o = ['<div class="vi-ods">', '  <div class="vi-ods-linha" role="tablist" aria-label="ODS ligados à ISO 39001">']
for k, (n, alt, _) in enumerate(ODS):
    o.append('    <button class="vi-ods-bt%s" type="button" role="tab" id="ods-t%s" aria-controls="ods-p%s" aria-selected="%s"><img src="img/ods-%s.svg?v=%s" alt="%s" width="720" height="720"></button>'
             % (' on' if k == 0 else '', n, n, 'true' if k == 0 else 'false', n, V, alt))
o.append('    <span class="vi-ods-dica">Clique num ODS para abrir a meta e o indicador</span>')
o.append('  </div>')
for k, (n, alt, sub) in enumerate(ODS):
    o.append('  <div class="vi-ods-painel%s" role="tabpanel" id="ods-p%s" aria-labelledby="ods-t%s"><div><div class="vi-ods-sub">' % (' on' if k == 0 else '', n, n))
    for rot, txt in sub:
        o.append('    <div class="ifc-cel"><span class="ifc-rot">%s</span><p>%s</p></div>' % (rot, txt))
    o.append('  </div></div></div>')
o.append('</div>')
FIG3 = '\n'.join(o)

# ---------------------------------------------------------------- fotos (vista aerea, Google Flow, tingimento azul)
# 02/10 (3a volta): «prefiro estrada fora de area urbana ou de matagal»: praca de pedagio vista de cima,
# entroncamento com viadutos em terreno aberto e patio de frota (os nomes de arquivo ficaram os da 2a volta)
FOTOS = [('viaria-rodovia', 'Concessões rodoviárias'),
         ('viaria-trevo', 'Infraestrutura viária'),
         ('viaria-frota', 'Frotas e logística')]
fotos = '<div class="vi-fotos">\n' + '\n'.join(
    '  <figure class="vi-foto"><div class="vi-quadro"><img src="img/%s-bayer.webp?v=%s" data-lum="img/%s-lum.webp?v=%s" alt="" loading="lazy"></div><figcaption>%s</figcaption></figure>'
    % (n, V, n, V, leg) for n, leg in FOTOS) + '\n</div>'
for n, _ in FOTOS:
    for t in ('lum', 'bayer'):
        assert os.path.exists(os.path.join(SITE, 'img', '%s-%s.webp' % (n, t))), 'falta a foto img/%s-%s.webp (rodar _ferramentas/foto_azul.py)' % (n, t)

# ---------------------------------------------------------------- o miolo: curto, em topicos, com o peso no servico
MIOLO = '''<p>A Ideal Metrics apoia a sua organização na implantação do <strong>sistema de gestão da segurança viária</strong> e na preparação para a <strong>certificação ISO 39001</strong>.</p>

<h3>O que fazemos</h3>
__GRADE__

__FIG1__

<h3>Por que a Ideal Metrics</h3>
<ul>
<li><strong>Experiência em concessão rodoviária de grande porte:</strong> sistema implantado e certificado na ISO 39001.</li>
<li><strong>Consultores:</strong> formação internacional de Auditor Líder (Lead Auditor) em ISO 39001.</li>
<li><strong>Ferramentas prontas:</strong> análise de risco viário e demais instrumentos montados com apoio da ISO 39002.</li>
<li><strong>Sistema integrado:</strong> a ISO 39001 entra no sistema que já atende <a href="norma-iso-9001.html">ISO 9001</a>, <a href="norma-iso-14001.html">ISO 14001</a> e <a href="norma-iso-45001.html">ISO 45001</a>.</li>
<li><strong>Equipe em atuação desde 1998.</strong></li>
</ul>

<hr class="section-divider">
<h3>Aplicação</h3>
__FOTOS__
<ul>
<li>Concessionárias de rodovias e operadores de infraestrutura viária.</li>
<li>Transportadoras de cargas e operadores logísticos.</li>
<li>Transporte de passageiros: urbano, rodoviário e fretamento.</li>
<li>Empresas com frota própria ou terceirizada.</li>
<li>Embarcadores que exigem segurança viária dos transportadores contratados.</li>
</ul>

<hr class="section-divider">
<h3>Por que implantar agora</h3>
__NUMS__
<ul>
<li><strong>Exigência de contrato:</strong> concessões rodoviárias já trazem a certificação ISO 39001 como obrigação com prazo.</li>
<li><strong>Exigência em lei:</strong> o PL 710/2024, aprovado no Senado, obriga a administração de rodovias a ter sistema de gestão de qualidade e de segurança.</li>
<li><strong>Norma em revisão:</strong> a segunda edição da ISO 39001 está em elaboração. Quem implanta agora já sai preparado para a transição.</li>
</ul>

<hr class="section-divider">
<h3>ISO 39001 e os ODS da ONU</h3>
<p>Com o sistema implantado, a organização mostra resultado em três Objetivos de Desenvolvimento Sustentável.</p>
__FIG3__
<p class="vi-fonte">A ISO relaciona a norma aos ODS 3, 11 e 12. No ODS 12 ela não indica meta: a 12.6 é a leitura da Ideal Metrics. O prazo da meta 3.6 foi renovado para 2030 pela Resolução 74/299 da ONU.</p>
<p class="vi-fonte">Ícones dos ODS: Nações Unidas, <a href="https://www.un.org/sustainabledevelopment/" target="_blank" rel="noopener">un.org/sustainabledevelopment</a>. O conteúdo desta página não foi aprovado pelas Nações Unidas e não reflete as opiniões das Nações Unidas, de seus funcionários ou dos Estados-Membros.</p>

<hr class="section-divider">
<p>Para implantar a ISO 39001 na sua operação, <a href="contato.html">fale com a gente</a>.</p>
'''
for k, v in (('__NUMS__', nums), ('__FIG1__', FIG1), ('__FIG3__', FIG3), ('__GRADE__', grade), ('__FOTOS__', fotos)):
    MIOLO = MIOLO.replace(k, v)
for palavra in ('percurso', 'Percurso', 'caminho', 'Ponto de partida', 'exame', 'auditoria de certificação', 'Para quem é'):
    assert palavra not in MIOLO and palavra not in SUB, 'palavra vetada no texto: ' + palavra

JS = '''<script>
/* as fotos desta pagina passam pelo motor da trama, no tom azul do site */
(function(){
  if(!window.ditherVivo) return;
  [].forEach.call(document.querySelectorAll('.vi-quadro'), function(q){
    var im = q.querySelector('img'); if(!im) return;
    window.ditherVivo({brilhoTom:0.35, gama:0.88, ctr:1.55, escuro:0.35, lavaRepouso:0.12, raiz:q, planos:[{el:q, lum:im.getAttribute('data-lum')}], classeCanvas:'vi-gl', revelar:'visivel',
      cores:[[21.2,50.9,80.6],[24.2,56.2,88.1],[103.0,146.1,189.4],[250,249,245]], pincel:.7, zoomHover:1.035});   /* o mesmo efeito de mouse das fotos da home */
  });
})();
/* os ODS: um clique abre o painel do icone e fecha os outros */
(function(){
  var bts = document.querySelectorAll('.vi-ods-bt');
  [].forEach.call(bts, function(b){ b.addEventListener('click', function(){
    [].forEach.call(bts, function(x){ var on = x === b; x.classList.toggle('on', on); x.setAttribute('aria-selected', on ? 'true' : 'false');
      document.getElementById(x.getAttribute('aria-controls')).classList.toggle('on', on); }); }); });
})();
</script>'''

# ---------------------------------------------------------------- monta
s, n = re.subn(r'<title>.*?</title>', '<title>%s | ISO 39001 | Ideal Metrics</title>\n<meta name="description" content="%s">' % (TITULO, DESC), s, count=1)
assert n == 1
assert s.count('</head>') == 1
s = s.replace('</head>', CSS + '\n</head>')
s, n = re.subn(r'<div class="page-banner"[^>]*>.*?</div>',
               '<div class="page-banner" data-lum="img/banner-viaria-lum.webp?v=%s"><h1>%s</h1><p>%s</p></div>' % (V, TITULO, SUB),
               s, count=1, flags=re.S)
assert n == 1
s, n = re.subn(r'<div class="breadcrumb">.*?</div>',
               '<div class="breadcrumb"><a href="index.html">Página Inicial</a> &gt; <a href="servicos.html">Todos os serviços</a> &gt; Gestão da segurança viária</div>', s, count=1, flags=re.S)
assert n == 1
s = s.replace('<a href="ifc-performance-standards.html" class="active" aria-current="page">IFC Performance Standards</a>',
              '<a href="ifc-performance-standards.html">IFC Performance Standards</a>')
# a navegacao lateral marca esta pagina (o link ja esta na casca, posto pelo menu do site)
x = '    <a href="seguranca-viaria.html">Segurança viária · ISO 39001</a>'
assert s.count(x) == 1, 'falta o link da pagina na navegacao lateral da casca'
s = s.replace(x, '    <a href="seguranca-viaria.html" class="active" aria-current="page">Segurança viária · ISO 39001</a>')
i = s.index('<div class="content">') + len('<div class="content">')
j = s.index('</div>\n</div>\n<footer')
s = s[:i] + '\n' + MIOLO + s[j:]
x = '<script src="js/banner.js?v=3"></script>'
assert s.count(x) == 1
s = s.replace(x, x + '\n' + JS)
io.open(os.path.join(SITE, ARQ), 'w', encoding='utf-8', newline='').write(s.replace('\n', eol))
print('%s: %d bytes' % (ARQ, len(s)))
