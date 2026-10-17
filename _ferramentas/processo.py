# -*- coding: utf-8 -*-
"""A secao «Processo» da home (index.html, [IM.3]) como DIAGRAMA, 14/10/2026.

    python _ferramentas/processo.py        reescreve o diagrama na pagina implantacao-iso.html (idempotente)
    (17/10/2026: saiu da home; antes ficava no index.html como a secao [IM.3])

Historia: eram cinco cartoes empilhados que se inclinavam na rolagem; no mesmo dia foram para a horizontal («encaixando
um card do lado do outro») e o Leandro nao gostou: «nao ficou bom, teria como trocar isso por um diagrama bem feito?».

O DIAGRAMA, na linha fina do site (a das etapas das paginas de servico e a do mapa da secao Conhecimento):
  - duas linhas paralelas: em baixo, o PROCESSO DO CLIENTE, com as cinco etapas em nos; em cima, o CONSULTOR DA IDEAL
    METRICS, que desce ate cada etapa por um fio (a frase da secao: «conduzimos cada etapa com o consultor dentro do
    processo do cliente»; o titulo: «Ao lado em cada etapa»);
  - em cada etapa: o numero (mono) em cima, o nome (17, negrito) e duas linhas curtas embaixo, tiradas dos cartoes;
  - embaixo, a chave «cerca de 6 meses», o prazo que as paginas de servico ja publicam («Cerca de 6 meses: do
    diagnostico a certificacao»).
  Nada de trocadilho nem de objeto do tema como desenho. Todo texto na tinta; a cor fica so no fio do consultor.

ENTRADA: a mesma do mapa da secao Conhecimento (linhas.py): o SVG leva a classe .ln-svg, as linhas .ln-linha/.ln-eixo
com --ox/--oy/--d e as pecas .ln-b com --dx/--dy/--d; o JS da entrada (o «CONHECIMENTO: entrada do mapa», inserido pelo
monta.py) toca nos dois sentidos da rolagem. As linhas se desenham da esquerda, os fios descem do consultor e cada
etapa sobe do seu no. Esse CSS e esse JS moram no bloco da secao Conhecimento: se ela sair, a entrada daqui para.

No celular (ate 880 px) o desenho da lugar a uma lista numerada com o mesmo conteudo."""

import os, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(AQUI)

TITULO = 'Ao lado em cada etapa'
FRASE = 'Do diagnóstico à certificação, conduzimos cada etapa com o consultor dentro do processo do cliente.'
# (numero, nome, linha 1, linha 2): o conteudo dos cartoes antigos, encurtado para caber embaixo do no
ETAPAS = [('01', 'Diagnóstico', 'Situação atual e gaps', 'em relação às normas'),
          ('02', 'Planejamento', 'Responsáveis, prazos e', 'entregas por visita'),
          ('03', 'Implantação', 'Sistema de gestão integrado', 'à rotina da operação'),
          ('04', 'Auditoria interna', 'Verificação da conformidade', 'e preparação para a certificação'),
          ('05', 'Certificação', 'Acompanhamento da auditoria', 'até o certificado emitido')]
# o texto inteiro de cada etapa, para a lista do celular e para quem le a tela
TEXTO = ['Análise da situação atual e identificação de gaps em relação às normas.',
         'Plano de implantação com responsáveis, prazos e entregas por visita.',
         'Construção do sistema de gestão integrado à rotina da operação.',
         'Verificação da conformidade e preparação para a certificação.',
         'Acompanhamento da auditoria do organismo certificador até o certificado emitido.']
PRAZO = 'Cerca de 6 meses'

W = 1362                                  # o mesmo viewBox do mapa da secao Conhecimento (1 unidade ~ 1 px a 1536)
XL, XR = 16, 1346                         # comeco e fim das duas linhas
X1, XN = 300, 1300                        # o primeiro e o ultimo no
YC, YP = 66, 146                          # a linha do consultor e a do processo
YT, YD = 200, 228                         # nome e primeira linha da descricao (a segunda vai 18 abaixo)
YK = 302                                  # a chave do prazo
H = 342


def esc(s):
    return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;')


def _linha(x1, y1, x2, y2, cls, d, ox=None, oy=None):
    ox = x1 if ox is None else ox; oy = y1 if oy is None else oy
    return ('<line class="%s" x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" style="--ox:%.1fpx;--oy:%.1fpx;--d:%d"/>'
            % (cls, x1, y1, x2, y2, ox, oy, d))


def _b(conteudo, dx, dy, d):
    return '<g class="ln-b" style="--dx:%.1fpx;--dy:%.1fpx;--d:%d">%s</g>' % (dx, dy, d, conteudo)


def svg():
    passo = (XN - X1) / (len(ETAPAS) - 1)
    o = ['<svg class="ln-svg pr-svg" viewBox="0 0 %d %d" role="img" aria-label="%s">'
         % (W, H, esc('As cinco etapas, do diagnóstico à certificação, com o consultor da Ideal Metrics em cada uma: '
                      + '; '.join('%s %s' % (n, t) for n, t, a, b in ETAPAS)))]
    # as duas linhas, desenhadas da esquerda, e os seus nomes em cima do comeco
    o.append(_linha(XL, YC, XR, YC, 'ln-linha pr-consultor', 60))
    o.append(_linha(XL, YP, XR, YP, 'ln-eixo', 0))
    o.append(_b('<text class="pr-rot" x="%d" y="%d">Consultor da Ideal Metrics</text>' % (XL, YC - 14), 0, 6, 60))
    o.append(_b('<text class="pr-rot" x="%d" y="%d">Processo do cliente</text>' % (XL, YP - 14), 0, 6, 0))
    for k, (n, t, a, b) in enumerate(ETAPAS):
        x = X1 + passo * k
        d = 380 + 230 * k
        # o fio do consultor desce ate a etapa
        o.append(_linha(x, YC, x, YP - 10, 'ln-linha pr-fio', d))
        o.append(_b('<circle class="pr-ponto" cx="%.1f" cy="%d" r="3.2"/>' % (x, YC), 0, 0, d))
        o.append(_b('<text class="pr-n" x="%.1f" y="%d">%s</text>' % (x, YC - 14, n), 0, 6, d))
        o.append(_b('<circle class="pr-no" cx="%.1f" cy="%d" r="10"/><circle class="pr-no-c" cx="%.1f" cy="%d" r="3.2"/>'
                    % (x, YP, x, YP), 0, 0, d + 120))
        # nome e descricao sobem do no
        o.append(_b('<text class="pr-t" x="%.1f" y="%d">%s</text>'
                    '<text class="pr-p" x="%.1f" y="%d">%s</text><text class="pr-p" x="%.1f" y="%d">%s</text>'
                    % (x, YT, esc(t), x, YD, esc(a), x, YD + 21, esc(b)), 0, YP - YT, d + 180))
    # a chave do prazo, do primeiro ao ultimo no
    dk = 380 + 230 * len(ETAPAS) + 100
    o.append(_linha(X1, YK, XN, YK, 'ln-linha pr-chave', dk))
    o.append(_linha(X1, YK - 6, X1, YK, 'ln-linha pr-chave', dk))
    o.append(_linha(XN, YK - 6, XN, YK, 'ln-linha pr-chave', dk, XN, YK))
    o.append(_b('<text class="pr-rot pr-rot--meio" x="%.1f" y="%d">%s</text>' % ((X1 + XN) / 2, YK + 22, esc(PRAZO)), 0, -6, dk + 200))
    o.append('</svg>')
    return ''.join(o)


def secao():
    lista = '\n'.join('      <li><span class="pr-li-n">%s</span><b>%s</b><span>%s</span></li>' % (n, esc(t), esc(TEXTO[k]))
                      for k, (n, t, a, b) in enumerate(ETAPAS))
    return '\n'.join([
        '<!-- ===== processo ===== -->',
        '<!-- gerada por _ferramentas/processo.py: editar la e rodar de novo -->',
        '<section class="pr-sec" id="pr-processo" aria-labelledby="pr-titulo">',
        '  <div class="pr-label">',
        '    <span>Processo</span>',
        '    <span aria-hidden="true">[IM.3]</span>',
        '  </div>',
        '  <h2 class="pr-titulo" id="pr-titulo">%s</h2>' % TITULO,
        '  <p class="pr-frase">%s</p>' % FRASE,
        '  <div class="pr-rola">' + svg() + '</div>',
        '  <ol class="pr-lista">',
        lista,
        '  </ol>',
        '  <p class="pr-lista-prazo">%s, do diagnóstico à certificação.</p>' % PRAZO,
        '</section>',
        '',
        '',
    ])


CSS = r"""/* ===== secao: processo ===== */
/* 14/10/2026: o DIAGRAMA das cinco etapas no lugar dos cartoes (gerado por _ferramentas/processo.py; editar la).
   Duas linhas paralelas em linha fina: o processo do cliente com as etapas em nos e, em cima, o consultor da Ideal
   Metrics, que desce ate cada etapa. A entrada e a do mapa da secao Conhecimento (.ln-svg, .ln-b, .ln-linha). */
.pr-sec{position:relative;z-index:1;color:var(--azul);padding:18px var(--lado) 110px}
.pr-label{display:flex;justify-content:space-between;font-family:var(--mono);font-weight:400;font-size:12px;line-height:1;
  letter-spacing:0;text-transform:uppercase}
.pr-titulo{margin:72px 0 0;font-family:var(--sans);font-weight:700;font-size:clamp(20px,2.2vw,30px);line-height:1.2;
  letter-spacing:-.012em;color:var(--azul);max-width:40ch;text-wrap:balance}
.pr-frase{margin:12px 0 0;max-width:62ch;font-family:var(--sans);font-size:16px;line-height:1.4;color:var(--azul);text-wrap:pretty}
.pr-rola{margin:44px 0 0}
.pr-svg{display:block;width:100%;height:auto;overflow:visible}
.pr-svg .ln-linha.pr-chave{stroke:rgba(20,48,76,.4)}
.pr-ponto{fill:#336699}
.pr-no{fill:#FAF9F5;stroke:#14304C;stroke-width:.8;vector-effect:non-scaling-stroke}
.pr-no-c{fill:#14304C}
.pr-n,.pr-rot{font-family:var(--mono);font-size:11px;font-weight:400;letter-spacing:.14em;text-transform:uppercase;fill:#14304C}
.pr-n{text-anchor:middle}
.pr-rot--meio{text-anchor:middle}
.pr-t{font-family:var(--sans);font-size:17px;font-weight:700;fill:#14304C;text-anchor:middle}
.pr-p{font-family:var(--sans);font-size:13px;font-weight:500;fill:#14304C;text-anchor:middle}
.pr-lista,.pr-lista-prazo{display:none}
@media (max-width:880px){
  .pr-sec{padding-bottom:70px}
  .pr-titulo{margin-top:48px}
  .pr-rola{display:none}
  .pr-lista{display:block;margin:30px 0 0;padding:0;list-style:none;border-left:1px solid #336699}
  .pr-lista li{position:relative;padding:0 0 22px 22px}
  .pr-lista li::before{content:"";position:absolute;left:-4px;top:5px;width:7px;height:7px;border-radius:50%;background:#336699}
  .pr-li-n{display:block;font-family:var(--mono);font-size:11px;letter-spacing:.14em;color:var(--azul)}
  .pr-lista b{display:block;margin:4px 0 4px;font-family:var(--sans);font-size:18px;font-weight:700;color:var(--azul)}
  .pr-lista li>span:last-child{display:block;font-family:var(--sans);font-size:15px;line-height:1.35;color:var(--azul)}
  .pr-lista-prazo{display:block;margin:6px 0 0;font-family:var(--mono);font-size:11px;letter-spacing:.14em;text-transform:uppercase;color:var(--azul)}
}

"""

JS = """// ===== processo =====
// 14/10/2026: sem JS proprio: a entrada do diagrama e a do mapa da secao Conhecimento (todas as .ln-svg)

"""


def troca_entre(t, ini, fim, novo):
    i, j = t.index(ini), t.index(fim)
    assert i < j and t.count(ini) == 1 and t.count(fim) == 1, (ini, fim)
    return t[:i] + novo + t[j:]


CSS_PAGINA = r"""
/* 17/10/2026: o diagrama do Processo saiu da home e veio para Implantacao ISO («esta parte tem que ficar dentro da
   implantacao de normas ISO»). No mesmo dia: «tem que ter efeito de entrada, tem que ficar no comeco, a parte escrita
   um pouco mais distante, um do outro, mesmo que tenha que mexer no menu lateral»: fica no TOPO da pagina, entre a
   migalha e o menu lateral, na largura toda (1240, a mesma do .page-layout), com a entrada do mapa da home. */
.pr-topo{max-width:1240px;margin:0 auto;padding:56px 40px 0;color:var(--azul)}
.pr-topo-rot{display:flex;justify-content:space-between;font-family:var(--mono);font-size:12px;letter-spacing:.14em;
  text-transform:uppercase;color:var(--azul);border-top:1px solid rgba(20,48,76,.16);padding-top:16px}
.pr-topo .pr-frase{margin:28px 0 0;max-width:62ch;font-family:var(--sans);font-size:18px;line-height:1.45;color:var(--azul)}
.pr-topo .pr-rola{margin:40px 0 0}
.pr-topo + .page-layout{padding-top:72px}
.pr-svg{display:block;width:100%;height:auto;overflow:visible}
.pr-svg line{vector-effect:non-scaling-stroke}
.pr-svg .ln-eixo{stroke:#14304C;stroke-width:.6;stroke-linecap:round}
.pr-svg .ln-linha{stroke:#336699;stroke-width:.6;stroke-linecap:round;fill:none}
.pr-svg .ln-linha.pr-chave{stroke:rgba(20,48,76,.4)}
.pr-ponto{fill:#336699}
.pr-no{fill:#FAF9F5;stroke:#14304C;stroke-width:.8;vector-effect:non-scaling-stroke}
.pr-no-c{fill:#14304C}
.pr-n,.pr-rot{font-family:var(--mono);font-size:12px;font-weight:400;letter-spacing:.14em;text-transform:uppercase;fill:#14304C}
.pr-n,.pr-rot--meio{text-anchor:middle}
.pr-t{font-family:var(--sans);font-size:18px;font-weight:700;fill:#14304C;text-anchor:middle}
.pr-p{font-family:var(--sans);font-size:14px;font-weight:500;fill:#14304C;text-anchor:middle}
/* a entrada (a mesma do mapa da home, _ferramentas/arcos/linhas.py): o script leva --p de 0 a 1 em 3 s quando o desenho
   entra na tela; as linhas crescem a partir de --ox/--oy e cada peca sobe do seu no */
.ln-svg{--p:1}
.ln-svg :is(.ln-linha,.ln-eixo){--t:clamp(0, calc((var(--p) * 3100 - var(--d)) / 900), 1);
  transform-box:view-box;transform-origin:var(--ox) var(--oy);
  transform:scale(calc(.001 + .999 * var(--t) * (2 - var(--t))));stroke-opacity:calc(var(--t) * 40)}
.ln-b{--t:clamp(0, calc((var(--p) * 3100 - var(--d)) / 800), 1);--e:calc(var(--t) * (2 - var(--t)));
  opacity:var(--t);transform-box:fill-box;transform-origin:center;
  transform:translate(calc(var(--dx) * (1 - var(--e))), calc(var(--dy) * (1 - var(--e)))) scale(calc(.35 + .65 * var(--e)))}
.pr-lista,.pr-lista-prazo{display:none}
@media (max-width:880px){
  .pr-topo{padding:40px 20px 0}
  .pr-topo .pr-rola{display:none}
  .pr-topo + .page-layout{padding-top:40px}
  .pr-lista{display:block;margin:24px 0 0;padding:0;list-style:none;border-left:1px solid #336699}
  .pr-lista li{position:relative;padding:0 0 22px 22px}
  .pr-lista li::before{content:"";position:absolute;left:-4px;top:5px;width:7px;height:7px;border-radius:50%;background:#336699}
  .pr-li-n{display:block;font-family:var(--mono);font-size:11px;letter-spacing:.14em;color:var(--azul)}
  .pr-lista b{display:block;margin:4px 0;font-family:var(--sans);font-size:18px;font-weight:700;color:var(--azul)}
  .pr-lista li>span:last-child{display:block;font-family:var(--sans);font-size:15px;line-height:1.35;color:var(--azul)}
  .pr-lista-prazo{display:block;margin:6px 0 0;font-family:var(--mono);font-size:11px;letter-spacing:.14em;text-transform:uppercase;color:var(--azul)}
}
"""

JS_PAGINA = r"""<script>
/* a entrada do diagrama (copia do script do mapa da home, _ferramentas/arcos/linhas.py): toca toda vez que o desenho
   entra na tela, descendo ou subindo; com movimento reduzido nada roda e o CSS deixa --p em 1 */
(function(){
  var ss = [].slice.call(document.querySelectorAll('.pr-topo .ln-svg'));
  if(!ss.length || !('IntersectionObserver' in window) || matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  var DUR = 3000;
  ss.forEach(function(s){
    var p = 0, t0 = 0, raf = 0, tocou = false;
    function poe(){ s.style.setProperty('--p', p.toFixed(4)); }
    function passo(t){ if(!t0) t0 = t - p * DUR; p = Math.min(1, (t - t0) / DUR); poe(); raf = p < 1 ? requestAnimationFrame(passo) : 0; }
    function toca(){ if(tocou) return; tocou = true; t0 = 0; raf = requestAnimationFrame(passo); }
    function zera(){ if(raf) cancelAnimationFrame(raf); raf = 0; tocou = false; p = 0; poe(); }
    poe();
    new IntersectionObserver(function(es){ es.forEach(function(e){ if(!e.isIntersecting) zera(); else if(e.intersectionRatio >= .35) toca(); }); },
      {threshold:[0, .35]}).observe(s);
  });
})();
</script>"""


def bloco_pagina():
    lista = '\n'.join('  <li><span class="pr-li-n">%s</span><b>%s</b><span>%s</span></li>' % (n, esc(t), esc(TEXTO[k]))
                      for k, (n, t, a, b) in enumerate(ETAPAS))
    return '\n'.join(['<!-- ===== processo (gerado por _ferramentas/processo.py: editar la e rodar de novo) ===== -->',
                      '<style>' + CSS_PAGINA + '</style>',
                      '<section class="pr-topo" aria-labelledby="pr-topo-t">',
                      '<p class="pr-topo-rot"><span id="pr-topo-t">Etapas da implantação</span><span>[ %s ]</span></p>' % PRAZO.upper(),
                      '<p class="pr-frase">%s</p>' % FRASE,
                      '<div class="pr-rola">' + svg() + '</div>',
                      '<ol class="pr-lista">', lista, '</ol>',
                      '<p class="pr-lista-prazo">%s, do diagnóstico à certificação.</p>' % PRAZO,
                      '</section>',
                      JS_PAGINA,
                      '<!-- ===== fim processo ===== -->'])


def main():
    """17/10/2026: o diagrama vive no TOPO da pagina de Implantacao ISO, entre a migalha e o .page-layout (menu lateral
    e texto), entre os marcadores do bloco (idempotente). Na primeira vez, sai de onde estava (abaixo de «Etapas da
    implantacao», no meio do texto) e o titulo «Etapas da implantacao» do texto sai junto (virou o rotulo do bloco)."""
    p = os.path.join(SITE, 'implantacao-iso.html')
    raw = open(p, 'rb').read(); crlf = b'\r\n' in raw
    t = raw.decode('utf-8').replace('\r\n', '\n')
    ini, fim = '<!-- ===== processo (gerado', '<!-- ===== fim processo ===== -->'
    if ini in t:
        i, j = t.index(ini), t.index(fim) + len(fim)
        t = t[:i] + t[j:].lstrip('\n')
    t = t.replace('<hr class="section-divider">\n\n<h3>Etapas da implantação</h3>\n', '', 1)
    a = '<div class="page-layout">'
    assert t.count(a) == 1
    t = t.replace(a, bloco_pagina() + '\n' + a, 1)
    open(p, 'wb').write((t.replace('\n', '\r\n') if crlf else t).encode('utf-8'))
    print('implantacao-iso.html: diagrama do Processo no topo')


if __name__ == '__main__':
    main()
