# -*- coding: utf-8 -*-
"""Duas alternativas para a secao «Conhecimento», inseridas LOGO ABAIXO da atual
para o Leandro escolher. Mesmo conteudo (arcos.TEMAS), mesma linguagem do site.

  B  GRADE       dez cartoes em 5 x 2, titulo e normas em etiquetas. Nada se
                 sobrepoe; no celular vira 2 x 5 e depois 1 coluna.
  C  RODA        um anel com os dez temas como pontos na volta; o tema
                 escolhido (mouse, toque ou teclado) abre as normas no centro.
                 Abaixo de 760px vira a lista simples.

    python variantes.py site      insere/atualiza as duas (idempotente)
    python variantes.py tirar     remove as duas

Depois da escolha: a vencedora vira a secao oficial e este arquivo sai."""

import sys, os, re, json, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import arcos

SITE = ("C:/Users/Leandro Centomo/OneDrive/\u00c1rea de Trabalho/CQT\u2014Inbox\u2014Fast/"
        "Primeiro-Vault/Ideal Metrics/ideal-metrics-site/")
INI, FIM = '<!-- ===== VARIANTES CONHECIMENTO (B e C) ===== -->', '<!-- ===== fim VARIANTES CONHECIMENTO ===== -->'
INI_CSS, FIM_CSS = '/* ===== VARIANTES CONHECIMENTO (B e C) ===== */', '/* ===== fim VARIANTES CONHECIMENTO ===== */'

CSS = r"""
/* B: a grade */
.cb-sec{padding:92px var(--lado) 104px;background:var(--mercurio);color:var(--azul)}
.cb-cab{border-top:1px solid var(--fio);padding-top:12px}
.cb-grade{display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:1px;margin-top:44px;
  background:rgba(20,48,76,.14);border:1px solid rgba(20,48,76,.14)}
.cb-cel{background:var(--mercurio);padding:26px 22px 28px;display:flex;flex-direction:column;gap:16px;
  min-height:214px;text-decoration:none;color:inherit;transition:background .35s ease}
.cb-cel:hover,.cb-cel:focus-visible{background:#F0EFEA;outline:none}
.cb-cel--i{background-image:repeating-linear-gradient(135deg,transparent 0 7px,rgba(20,48,76,.05) 7px 8px)}
.cb-num{font-family:var(--mono);font-size:10.5px;letter-spacing:.2em;color:var(--azul-escuro)}
.cb-tit{font-family:var(--sans);font-weight:600;font-size:19px;line-height:1.2;letter-spacing:-.01em;margin:0}
.cb-normas{display:flex;flex-wrap:wrap;gap:6px;margin-top:auto}
.cb-normas span{font-family:var(--sans);font-weight:500;font-size:11.5px;line-height:1;padding:6px 8px;
  background:var(--branco);border:1px solid rgba(20,48,76,.14);border-radius:3px;color:var(--azul-escuro)}
@media (max-width:1180px){ .cb-grade{grid-template-columns:repeat(2,minmax(0,1fr))} .cb-cel{min-height:0} }
@media (max-width:600px){ .cb-grade{grid-template-columns:1fr} }

/* C: a roda */
.cc-sec{padding:92px var(--lado) 104px;background:var(--mercurio);color:var(--azul)}
.cc-cab{border-top:1px solid var(--fio);padding-top:12px}
.cc-palco{position:relative;max-width:940px;margin:36px auto 0}
.cc-svg{display:block;width:100%;height:auto;overflow:visible}
.cc-anel{fill:none;stroke:rgba(20,48,76,.18);stroke-width:1;vector-effect:non-scaling-stroke}
.cc-anel--i{stroke-dasharray:3 5}
.cc-pt{cursor:pointer}
.cc-pt circle{fill:var(--mercurio);stroke:rgba(20,48,76,.45);stroke-width:1.2;vector-effect:non-scaling-stroke;transition:fill .3s,stroke .3s}
.cc-pt text{font-family:var(--sans);font-weight:500;font-size:14px;fill:var(--azul);transition:font-weight .1s}
.cc-pt:focus{outline:none}
.cc-pt.cc-on circle{fill:var(--azul);stroke:var(--azul)}
.cc-pt.cc-on text{font-weight:700}
.cc-centro{position:absolute;left:50%;top:50%;width:min(300px,42%);transform:translate(-50%,-50%);text-align:center}
.cc-centro-rot{font-family:var(--mono);font-size:10.5px;letter-spacing:.2em;text-transform:uppercase;color:var(--azul-escuro);margin:0 0 10px}
.cc-centro-tit{font-family:var(--sans);font-weight:700;font-size:clamp(20px,2.2vw,28px);line-height:1.15;letter-spacing:-.012em;margin:0 0 16px;text-wrap:balance}
.cc-centro-normas{display:flex;flex-wrap:wrap;justify-content:center;gap:6px}
.cc-centro-normas span{font-family:var(--sans);font-weight:500;font-size:12px;line-height:1;padding:6px 9px;
  background:var(--branco);border:1px solid rgba(20,48,76,.14);border-radius:3px;color:var(--azul-escuro)}
.cc-centro a{display:inline-block;margin-top:18px;font-family:var(--mono);font-size:10.5px;letter-spacing:.2em;
  text-transform:uppercase;color:var(--azul);text-decoration:none;border-bottom:1px solid var(--fio);padding-bottom:3px}
.cc-lista{display:none}
@media (max-width:760px){ .cc-palco{display:none} .cc-lista{display:block} }
"""

CX, CY, R = 470, 330, 232


def temas():
    """os temas na ordem do TEMAS, com numero, titulo em uma linha e normas"""
    out = []
    for k, (tid, pag, div, cx, cy, r, tit, normas) in enumerate(arcos.TEMAS, 1):
        out.append(dict(id=tid, pag=pag, div=div, n=k, tit=' '.join(tit), normas=arcos.normas_de(tid)))
    return out


def grade():
    T = temas()
    o = ['<section class="cb-sec" id="conhecimento-b" aria-labelledby="cb-titulo">',
         '  <div class="cb-cab"><p class="ar-rotulo">Conhecimento / opção B: grade</p>',
         '  <div class="ar-linha"><h2 class="ar-titulo" id="cb-titulo">Cada tema, com as normas e os padrões que aplicamos</h2>',
         '  <ul class="ar-legenda"><li>Padronização</li><li class="ar-leg-i">Inteligência</li></ul></div></div>',
         '  <div class="cb-grade">']
    for t in T:
        o.append('    <a class="cb-cel%s" href="%s"><span class="cb-num">%02d</span><h3 class="cb-tit">%s</h3>'
                 '<span class="cb-normas">%s</span></a>'
                 % (' cb-cel--i' if t['div'] == 'i' else '', t['pag'], t['n'], arcos.esc(t['tit']),
                    ''.join('<span>%s</span>' % arcos.esc(n) for n in t['normas'])))
    o += ['  </div>', '</section>']
    return '\n'.join(o)


def roda():
    T = temas()
    n = len(T)
    o = ['<section class="cc-sec" id="conhecimento-c" aria-labelledby="cc-titulo">',
         '  <div class="cc-cab"><p class="ar-rotulo">Conhecimento / opção C: roda</p>',
         '  <div class="ar-linha"><h2 class="ar-titulo" id="cc-titulo">Cada tema, com as normas e os padrões que aplicamos</h2>',
         '  <ul class="ar-legenda"><li>Padronização</li><li class="ar-leg-i">Inteligência</li></ul></div></div>',
         '  <div class="cc-palco">',
         '  <svg class="cc-svg" viewBox="0 0 940 660" aria-label="Roda dos temas">',
         '    <circle class="cc-anel" cx="%d" cy="%d" r="%d"/>' % (CX, CY, R),
         '    <circle class="cc-anel cc-anel--i" cx="%d" cy="%d" r="%d"/>' % (CX, CY, R + 14)]
    for k, t in enumerate(T):
        a = -math.pi / 2 + 2 * math.pi * k / n
        rr = R + 14 if t['div'] == 'i' else R
        x, y = CX + rr * math.cos(a), CY + rr * math.sin(a)
        lx, ly = CX + (R + 40) * math.cos(a), CY + (R + 40) * math.sin(a)
        anc = 'middle' if abs(math.cos(a)) < .2 else ('start' if math.cos(a) > 0 else 'end')
        o.append('    <g class="cc-pt" data-t="%s" tabindex="0" role="button" aria-label="%s">'
                 '<circle cx="%.1f" cy="%.1f" r="7"/><text x="%.1f" y="%.1f" text-anchor="%s" dominant-baseline="central">%s</text></g>'
                 % (t['id'], arcos.esc(t['tit']), x, y, lx, ly, anc, arcos.esc(t['tit'])))
    o += ['  </svg>',
          '  <div class="cc-centro" aria-live="polite"><p class="cc-centro-rot" id="cc-rot"></p>'
          '<h3 class="cc-centro-tit" id="cc-tit"></h3><div class="cc-centro-normas" id="cc-normas"></div>'
          '<a id="cc-link" href="#">Ver o tema</a></div>',
          '  </div>',
          arcos.lista().replace('ar-lista', 'ar-lista cc-lista'),
          '</section>']
    dados = {t['id']: dict(tit=t['tit'], normas=t['normas'], pag=t['pag'], n=t['n'], div=t['div']) for t in T}
    js = """<script>
(function(){
  var D=%s, pts=[].slice.call(document.querySelectorAll('#conhecimento-c .cc-pt')), atual=null;
  function mostra(id){ if(id===atual) return; atual=id; var d=D[id];
    pts.forEach(function(p){ p.classList.toggle('cc-on', p.getAttribute('data-t')===id); });
    document.getElementById('cc-rot').textContent=(d.n<10?'0':'')+d.n+' / '+(d.div==='i'?'Inteligência':'Padronização');
    document.getElementById('cc-tit').textContent=d.tit;
    document.getElementById('cc-normas').innerHTML=d.normas.map(function(n){return '<span>'+n+'</span>';}).join('');
    document.getElementById('cc-link').setAttribute('href',d.pag); }
  pts.forEach(function(p){ var id=p.getAttribute('data-t');
    p.addEventListener('mouseenter',function(){mostra(id);}); p.addEventListener('focus',function(){mostra(id);});
    p.addEventListener('click',function(){mostra(id);});
    p.addEventListener('keydown',function(e){ if(e.key==='Enter'||e.key===' '){ e.preventDefault(); location.href=D[id].pag; } }); });
  mostra(pts[0].getAttribute('data-t'));
})();
</script>""" % json.dumps(dados, ensure_ascii=False)
    return '\n'.join(o) + '\n' + js


def escreve(t, bloco_html, bloco_css):
    t = re.sub(re.escape(INI) + r'.*?' + re.escape(FIM) + r'\n', '', t, flags=re.S)
    t = re.sub(re.escape(INI_CSS) + r'.*?' + re.escape(FIM_CSS) + r'\n', '', t, flags=re.S)
    if bloco_html:
        anc = '<section class="sv" id="servicos" aria-labelledby="sv-h2">'
        assert t.count(anc) == 1
        t = t.replace(anc, INI + '\n' + bloco_html + '\n' + FIM + '\n\n' + anc, 1)
        anc_css = '/* ===== fim CONHECIMENTO ===== */'
        assert t.count(anc_css) == 1
        t = t.replace(anc_css, anc_css + '\n' + INI_CSS + bloco_css + FIM_CSS + '\n', 1)
    return t


def main(modo):
    p = SITE + 'index.html'
    raw = open(p, 'rb').read(); eol = '\r\n' if raw.count(b'\r\n') else '\n'
    t = raw.decode('utf-8').replace('\r\n', '\n')
    if modo == 'site':
        t = escreve(t, grade() + '\n\n' + roda(), CSS)
        print('variantes B (grade) e C (roda) inseridas abaixo da secao Conhecimento')
    else:
        t = escreve(t, '', '')
        print('variantes removidas')
    open(p, 'wb').write(t.replace('\n', eol).encode('utf-8'))


if __name__ == '__main__':
    main(sys.argv[1] if len(sys.argv) > 1 else 'site')
