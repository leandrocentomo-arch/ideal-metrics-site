# -*- coding: utf-8 -*-
"""Monta o CSS, o HTML e o JS da secao «Conhecimento» a partir de arcos.py.

    python monta.py previa     grava a previa isolada em scratchpad/passaro/
    python monta.py site       insere no index.html do site

PROFUNDIDADE. Na referencia as quatro camadas deslizam em velocidades
diferentes, e com isso a pilula escorrega para fora do proprio aro nos
extremos da rolagem. Aqui o aro de cada tema e as suas pilulas ficam na MESMA
camada, parada: a norma nunca sai da linha. Quem da a profundidade sao as
outras duas camadas, em sentidos opostos: os discos descem (64) e os aros
soltos sobem (34). Com 30 e 14 o curso medido foi de 7px, invisivel. Com prefers-reduced-motion nada se move."""

import sys, os, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import arcos

CSS = r"""
/* ===== CONHECIMENTO, 21/09/2026: esquema por arcos =====
   Referencia: catalystbehavioral.com/litigation-surveys. Tres camadas: discos
   cheios em #F0EFEA (o creme escurecido 4% da secao Demandas), aros de 1px e os
   rotulos. As normas vao em pilulas SOBRE o aro, no desenho das etiquetas da
   secao Demandas. Aro tracejado = divisao de inteligencia. O aro de cada tema e
   as suas pilulas dividem a mesma camada, parada, para a norma nunca sair da
   linha; a profundidade vem dos discos e dos aros soltos, em sentidos opostos.
   Abaixo de 1000px o esquema vira lista: as pilulas ficariam com menos de 10px. */
.ar-sec{padding:92px var(--lado) 104px;background:var(--mercurio);color:var(--azul)}
.ar-cab{border-top:1px solid var(--fio);padding-top:12px}
.ar-rotulo{margin:0;font-family:var(--mono);font-weight:400;font-size:12px;line-height:1;
  letter-spacing:.02em;text-transform:uppercase;color:var(--azul)}
.ar-linha{display:flex;justify-content:space-between;align-items:flex-end;gap:32px;
  flex-wrap:wrap;margin-top:34px}
.ar-titulo{margin:0;font-family:var(--sans);font-weight:700;font-size:clamp(20px,2.2vw,30px);
  line-height:1.2;letter-spacing:-.012em;color:var(--azul);max-width:24ch;text-wrap:balance}
.ar-legenda{display:flex;gap:26px;margin:0 0 4px;padding:0;list-style:none;
  font-family:var(--mono);font-size:10.5px;letter-spacing:.2em;text-transform:uppercase;
  color:var(--azul-escuro)}
.ar-legenda li{display:flex;align-items:center;gap:10px}
.ar-legenda li::before{content:"";width:26px;border-top:1px solid rgba(20,48,76,.55)}
.ar-legenda .ar-leg-i::before{border-top-style:dashed}
.ar-palco{margin:44px 0 0;position:relative}   /* largura inteira da pagina (21/09) */
.ar-svg{display:block;width:100%;height:auto;overflow:visible}
.ar-svg{position:relative}
/* as manchas sao IMAGEM desenhada pelo motor ditherVivo, o mesmo das fotos da
   primeira secao: trama Bayer na rampa da casa e o rastro do mouse. A imagem tem
   a caixa exata do viewBox, entao cada mancha cai sob o seu circulo. Sem WebGL
   fica a <img> ja tramada. Sem movimento na rolagem: o canvas mede a propria
   caixa, e deslocar a caixa a cada quadro descasaria o rastro do ponteiro. */
.ar-manchas{position:absolute;left:0;top:0;width:100%;height:100%}
.ar-manchas img,.ar-gl{position:absolute;inset:0;width:100%;height:100%;display:block}
.ar-manchas.gl-on img{visibility:hidden}
.ar-soltos circle,.ar-aro{fill:none;stroke:rgba(20,48,76,.10);stroke-width:1;
  vector-effect:non-scaling-stroke;transition:stroke .35s ease}
.ar-soltos circle{stroke:rgba(20,48,76,.09)}
.ar-aro--i{stroke-dasharray:3 5}
.ar-tema{cursor:pointer;transition:opacity .35s ease}
.ar-tema:focus{outline:none}
.ar-alvo{fill:transparent}
.ar-tit{font-family:var(--sans);font-weight:600;font-size:19px;fill:var(--azul);
  text-anchor:middle;dominant-baseline:central}
/* etiqueta no CREME DA PAGINA, var(--mercurio), e nao em branco (21/09): ela
   combina com o fundo da tela. Sobre o creme quem a desenha e o contorno, que
   por isso sobe de 10% para 18%; sobre os discos ela aparece como recorte. */
.ar-pil rect{fill:var(--mercurio);stroke:rgba(20,48,76,.12);stroke-width:1;
  vector-effect:non-scaling-stroke;transition:stroke .35s ease}
.ar-pil text{font-family:var(--sans);font-weight:500;font-size:10.5px;letter-spacing:.01em;
  text-anchor:middle;fill:var(--azul-escuro)}
/* realce: o tema sob o mouse fica, os outros recuam */
.ar-svg:has(.ar-tema:is(:hover,:focus-visible)) .ar-tema:not(:hover):not(:focus-visible){opacity:.34}
.ar-tema:is(:hover,:focus-visible) .ar-pil rect{stroke:rgba(20,48,76,.42)}
.ar-tema:focus-visible .ar-tit{text-decoration:underline;text-underline-offset:4px}
%(HOVER)s
.ar-lista{display:none}
@media (max-width:1000px){
  .ar-sec{padding-top:70px;padding-bottom:78px}
  .ar-svg,.ar-manchas{display:none}
  .ar-palco{margin-top:34px}
  .ar-lista{display:grid;grid-template-columns:1fr 1fr;gap:26px 28px;margin:0;padding:0;list-style:none}
  .ar-item{border-top:1px solid rgba(20,48,76,.16);padding-top:14px}
  .ar-item--i{border-top-style:dashed}
  .ar-item a{font-family:var(--sans);font-weight:600;font-size:18px;line-height:1.25;
    color:var(--azul);text-decoration:none}
  .ar-normas{display:flex;flex-wrap:wrap;gap:6px;margin-top:10px}
  .ar-normas span{font-family:var(--sans);font-weight:500;font-size:11.5px;line-height:1;
    padding:5px 8px;background:var(--mercurio);border:1px solid rgba(20,48,76,.18);
    border-radius:3px;color:var(--azul-escuro)}
}
@media (max-width:600px){ .ar-lista{grid-template-columns:1fr} }
"""

JS = ""   # sem profundidade por rolagem: as manchas agora sao do motor ditherVivo

# chamada do motor, inserida DENTRO do IIFE que define ditherVivo (ele nao e global)
MOTOR = r"""  /* ---------------- CONHECIMENTO: as manchas por tras dos aros ---------------- */
  (function(){
    var m = document.querySelector('.ar-manchas'); if(!m) return;
    var im = m.querySelector('img'); if(!im) return;
    ditherVivo({raiz:m, planos:[{el:m, lum:im.getAttribute('data-lum')}], classeCanvas:'ar-gl', revelar:'visivel',
      cores:[[21.2,50.9,80.6],[24.2,56.2,88.1],[103.0,146.1,189.4],[250,249,245]], pincel:.7});
  })();
  /* ---------------- fim CONHECIMENTO manchas ---------------- */
"""


def svg(L):
    """o SVG do arcos.py com as camadas de profundidade separadas"""
    T = arcos.TEMAS
    o = ['<svg class="ar-svg" viewBox="%.1f %.1f %.1f %.1f" aria-label="Temas e normas da Ideal Metrics">'
         % arcos.limites(L)]
    if arcos.AROS_SOLTOS:
        o.append('<g class="ar-camada ar-soltos" data-ar-vel="-34" aria-hidden="true">')
        o += ['<circle cx="%d" cy="%d" r="%d"/>' % c for c in arcos.AROS_SOLTOS]
        o.append('</g>')
    o.append('<g class="ar-temas">')
    P = arcos.pilulas(L)
    for tid, pag, div, cx, cy, r, tit, normas in T:
        rot = '%s: %s' % (' '.join(tit), ', '.join(n for n, a in normas))
        o.append('<circle class="ar-aro%s" data-t="%s" cx="%d" cy="%d" r="%d" aria-hidden="true"/>'
                 % (' ar-aro--i' if div == 'i' else '', tid, cx, cy, r))
    for tid, pag, div, cx, cy, r, tit, normas in T:
        rot = '%s: %s' % (' '.join(tit), ', '.join(arcos.normas_de(tid)))
        o.append('<a class="ar-tema" data-t="%s" href="%s" aria-label="%s">' % (tid, pag, arcos.esc(rot)))
        o.append('<circle class="ar-alvo" cx="%d" cy="%d" r="%d"/>' % (cx, cy, r))
        y0 = cy - arcos.LH_TIT * (len(tit) - 1) / 2.0
        o.append('<text class="ar-tit" x="%d" y="%.1f" aria-hidden="true">' % (cx, y0) +
                 ''.join('<tspan x="%d" dy="%s">%s</tspan>' % (cx, '0' if k == 0 else arcos.LH_TIT, arcos.esc(l))
                         for k, l in enumerate(tit)) + '</text>')
        for p in (p for p in P if p['tema'] == tid):
            o.append('<g class="ar-pil" aria-hidden="true"><rect x="%.1f" y="%.1f" width="%.1f" height="%d" rx="3"/>'
                     '<text x="%.1f" y="%.1f">%s</text></g>'
                     % (p['x0'], p['y0'], p['w'], arcos.PIL_H, p['x'], p['y'] + 3.7, arcos.esc(p['txt'])))
        o.append('</a>')
    o.append('</g></svg>')
    return '\n'.join(o)


def secao(L):
    return '\n'.join([
        '<section class="ar-sec" id="conhecimento" aria-labelledby="ar-titulo">',
        '  <div class="ar-cab">',
        '    <p class="ar-rotulo">Conhecimento / [ IM.2 ]</p>',
        '    <div class="ar-linha">',
        '      <h2 class="ar-titulo" id="ar-titulo">Cada tema, com as normas e os padrões que aplicamos</h2>',
        '      <ul class="ar-legenda"><li>Padronização</li><li class="ar-leg-i">Inteligência</li></ul>',
        '    </div>',
        '  </div>',
        '  <div class="ar-palco">',
        '    <div class="ar-manchas" aria-hidden="true"><img src="img/conhecimento-manchas-bayer.webp" '
        'data-lum="img/conhecimento-manchas-lum.webp" alt="" width="1800" height="%d" loading="lazy" decoding="async"></div>'
        % round(1800 * arcos.limites(L)[3] / arcos.limites(L)[2]),
        svg(L),
        arcos.lista(),
        '  </div>',
        '</section>',
    ])


def css():
    return CSS.replace('%(HOVER)s', arcos.css_hover())


PREVIA = """<!doctype html><html lang="pt-BR"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>previa arcos</title>
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500&family=IBM+Plex+Sans+Condensed:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>
:root{--azul:#14304C;--azul-escuro:#315275;--fio:rgba(20,48,76,.2);--lado:clamp(28px,4vw,64px);
  --mercurio:#FAF9F5;--branco:#FFFFFF;--mono:'IBM Plex Mono',monospace;--sans:'IBM Plex Sans Condensed',sans-serif}
body{margin:0;background:var(--mercurio)}
.antes,.depois{height:140px;background:var(--mercurio)}
%s
</style></head><body><div class="antes"></div>
%s
<div class="depois"></div>
%s
</body></html>"""

if __name__ == '__main__':
    L = arcos.larguras()
    assert not arcos.colisoes(L), arcos.colisoes(L)
    modo = sys.argv[1] if len(sys.argv) > 1 else 'previa'
    if modo == 'previa':
        dst = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'passaro', 'arcos-previa.html')
        open(dst, 'w', encoding='utf-8').write(PREVIA % (css(), secao(L), JS))
        print('previa ->', dst)
    elif modo == 'site':
        import insere, manchas
        manchas.main()
        insere.no_site(css(), secao(L), JS, MOTOR)
