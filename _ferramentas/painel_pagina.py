# -*- coding: utf-8 -*-
"""Monta painel-normas.html: cabeçalho, menus e rodapé copiados de blog.html (o menu.py
regrava os blocos depois), e o miolo do painel daqui. Rodar depois de mudar o miolo:

    python _ferramentas/painel_pagina.py && python _ferramentas/menu.py && python _ferramentas/busca.py
"""
import re, os
import blocos as B

V = '1'   # sobe junto com painel-normas.css / .js
s = B.ler('blog.html')
cab = s[:s.index('<div class="page-banner">')]
rod = s[s.index('<footer class="ft-root'):]
cab = re.sub(r'<title>.*?</title>', '<title>Painel de normas ISO | Ideal Metrics</title>', cab, count=1)
cab, n = re.subn(r'(<link rel="stylesheet" href="css/style\.css\?v=\d+">)',
                 r'\1\n<link rel="stylesheet" href="css/painel-normas.css?v=%s">\n'
                 r'<meta name="description" content="Andamento das normas ISO de sistemas de gestão, sustentabilidade e segurança: estágio, comitê, revisão sistemática e certificados por país. Fonte: ISO Open Data e ISO Survey.">' % V, cab, count=1)
assert n == 1, 'link do style.css não encontrado no blog.html'
rod, n = re.subn(r'(<script src="js/gaveta\.js\?v=\d+" defer></script>)',
                 r'<script src="https://cdnjs.cloudflare.com/ajax/libs/d3/7.9.0/d3.min.js" defer></script>\n'
                 r'<script src="https://cdnjs.cloudflare.com/ajax/libs/topojson/3.0.2/topojson.min.js" defer></script>\n'
                 r'<script src="js/painel-normas.js?v=%s" defer></script>\n\1' % V, rod, count=1)
assert n == 1, 'script gaveta.js não encontrado no blog.html'

ABAS = [('normas', '01', 'Normas por tema'), ('tempo', '02', 'Linha do tempo'), ('mudancas', '03', 'O que mudou'),
        ('revisao', '04', 'Revisão sistemática'), ('mapa', '05', 'Certificados no mundo')]

def filtro(id_, rotulo, k):
    return ('<div class="pn-bloco"><span class="m">%s <span><button data-k="%s" data-on="1">todos</button> · <button data-k="%s" data-on="0">nenhum</button></span></span>'
            '<div id="%s"></div></div>' % (rotulo, k, k, id_))

LUPA = '<svg viewBox="0 0 24 24"><circle cx="11" cy="11" r="8"/><path d="M21 21l-4.35-4.35"/></svg>'
SETA = '<svg viewBox="0 0 24 24"><path d="M5 12h14M13 6l6 6-6 6"/></svg>'

miolo = '''<main class="pn" id="painel">
  <div class="pn-cab">
    <div>
      <span class="m">Estudos e pesquisa aplicada · painel · base da ISO de <span id="pn-gerado">…</span></span>
      <h1>Painel de normas ISO</h1>
      <p class="pn-sub">Andamento das normas de sistemas de gestão, sustentabilidade e segurança nos comitês que a Ideal Metrics acompanha: estágio de cada projeto, comitê responsável, revisões em curso e certificados válidos por país.</p>
    </div>
    <div class="pn-abas" role="tablist">%s</div>
  </div>

  <aside class="pn-lado" aria-label="Busca e filtros">
    <div class="pn-busca"><input id="pn-q" type="search" placeholder="Número, título ou comitê" aria-label="Buscar norma" autocomplete="off">%s</div>
    %s
    %s
    %s
    <div class="pn-bloco"><label class="pn-op"><input type="checkbox" id="f-pagina"> <span>Só normas com serviço da Ideal Metrics</span></label></div>
    <p class="pn-fonte">Fontes: <a href="https://www.iso.org/open-data.html" target="_blank" rel="noopener">ISO Open Data</a>, licença ODC-By 1.0, atualizada semanalmente neste painel; ISO Survey 2025 (certificados em 31/12/2025). Os textos de escopo são da ISO, em inglês. Os documentos de comitê não são públicos e não estão aqui.</p>
  </aside>

  <section class="pn-main">
    <div class="pn-vista ativa" id="v-normas" role="tabpanel">
      <div class="pn-topo"><h2>Normas por tema</h2><span class="m" id="pn-total"></span>
        <div class="pn-ord"><span class="m" style="padding:4px 6px 0 0">ordem</span><button data-ord="num" aria-pressed="true">número</button><button data-ord="fase" aria-pressed="false">estágio</button><button data-ord="data" aria-pressed="false">publicação</button></div></div>
      <ul class="pn-lista" id="pn-lista"></ul>
    </div>
    <div class="pn-vista" id="v-tempo" role="tabpanel">
      <div class="pn-topo"><h2>Linha do tempo das normas-chave</h2><span class="m">edições publicadas e projetos em curso</span></div>
      <div class="lt-cab"><span class="m">norma</span><div class="lt-anos" id="lt-anos"></div></div>
      <div id="lt-corpo"></div>
      <div class="lt-leg"><span><i></i>edição em vigor</span><span><i class="ant"></i>edição anterior</span><span><i class="dev"></i>projeto em desenvolvimento (posição = hoje)</span><span>Clique na marca para abrir a ficha.</span></div>
    </div>
    <div class="pn-vista" id="v-mudancas" role="tabpanel">
      <div class="pn-topo"><h2>O que mudou</h2><span class="m">comparação semanal da base da ISO</span></div>
      <div id="md-corpo"></div>
      <p class="md-nota">A ISO não publica a data em que cada projeto muda de estágio. Este painel compara a base a cada semana e registra a diferença na data da comparação. Movimentos dos últimos 180 dias.</p>
    </div>
    <div class="pn-vista" id="v-revisao" role="tabpanel">
      <div class="pn-topo"><h2>Revisão sistemática</h2><span class="m" id="rv-total"></span></div>
      <p class="md-nota" style="margin:14px 0 4px">Norma em revisão sistemática continua válida. O resultado da consulta pode ser manter, revisar ou cancelar; quando há projeto de nova edição em curso, ele aparece na linha.</p>
      <ul class="pn-lista" id="rv-corpo"></ul>
    </div>
    <div class="pn-vista" id="v-mapa" role="tabpanel">
      <div class="pn-topo"><h2>Certificados no mundo</h2><span class="m">ISO Survey 2025 · certificados acreditados válidos</span></div>
      <div class="mp-grid">
        <div>
          <div class="mp-sel" id="mp-sel"></div>
          <div class="mp-mapa" id="mp-mapa"><div class="mp-dica" id="mp-dica"></div></div>
          <div class="mp-esc" id="mp-esc"></div>
        </div>
        <div class="mp-lado" id="mp-lado"></div>
      </div>
    </div>
  </section>
</main>
<div class="pn-veu" id="pn-veu"></div>
<aside class="pn-det" id="pn-det" aria-label="Ficha da norma"><button class="fechar" aria-label="Fechar"><svg viewBox="0 0 24 24" fill="none"><path d="M5 5l14 14M19 5L5 19"/></svg></button></aside>
''' % (''.join('<button role="tab" data-aba="%s" aria-selected="%s"><span class="m">[ %s ]</span>%s</button>' % (a, 'true' if i == 0 else 'false', n, r) for i, (a, n, r) in enumerate(ABAS)),
       LUPA, filtro('f-temas', 'Tema', 'temas'), filtro('f-fases', 'Estágio', 'fases'), filtro('f-tipos', 'Tipo de documento', 'tipos'))

B._EOL['painel-normas.html'] = '\r\n'
B.gravar('painel-normas.html', cab + miolo + rod)
print('painel-normas.html gravado')
