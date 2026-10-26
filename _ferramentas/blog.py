# -*- coding: utf-8 -*-
"""Blog da Ideal Metrics (17/10/2026): os posts do blog da CQT (cqt-br.com, Wix) como se fossem da Ideal Metrics, com as
datas de quando foram publicados na CQT.

    python _ferramentas/blog.py

Le _ferramentas/blog-posts.json (um item por post: arquivo, titulo, data, categoria, foto, blocos do texto) e regrava:
  - a grade de cartoes do blog.html (entre <div class="blog-grid"> e o </section> dela), cada cartao com a foto no
    motor da trama e o link para o post;
  - uma pagina por post, <arquivo>.html, com o cabecalho, os menus e o rodape copiados do proprio blog.html.
Depois: python _ferramentas/busca.py. As fotos sao as do site (img/), tramadas: blog-01 a blog-06 vieram das capas do
blog da CQT (crus em _tingir-fotos/FOTOS/b83354_*.png, niveis esticados e gama 2,0 a 2,2 no foto_azul.py, 640x480);
os posts sem foto no Wix (lá so tinham o logo da CQT) usam fotos ja tramadas do site, pelo tema."""
import os, re, json, html

AQUI = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(AQUI)
V = '18102026e'
MES = ['jan.', 'fev.', 'mar.', 'abr.', 'mai.', 'jun.', 'jul.', 'ago.', 'set.', 'out.', 'nov.', 'dez.']
MOTOR = r"""<script>
/* blog: as fotos passam pelo motor da trama, no tom azul do site */
(function(){
  if(!window.ditherVivo) return;
  [].forEach.call(document.querySelectorAll('.bl-quadro'), function(q){
    var im = q.querySelector('img'); if(!im) return;
    window.ditherVivo({brilhoTom:0.35, gama:0.88, ctr:1.55, escuro:0.35, lavaRepouso:0.12, raiz:q, planos:[{el:q, lum:im.getAttribute('data-lum')}], classeCanvas:'bl-gl', revelar:'visivel',
      cores:[[21.2,50.9,80.6],[24.2,56.2,88.1],[103.0,146.1,189.4],[250,249,245]], pincel:.7, zoomHover:1.035});
  });
})();
</script>"""


def data_br(iso):
    # dd-mmm-aaaa, regra do Leandro de 26/10/2026 («formato da data sempre dd-mmm-aaaa»)
    a, m, d = iso.split('-')
    return '%02d-%s-%s' % (int(d), MES[int(m) - 1].rstrip('.'), a)


def e(t):
    return html.escape(t, quote=False)


def leitura(p):
    n = sum(len(x.split()) for _, x in p['blocos'])
    return max(1, round(n / 200))


def quadro(p, classe=''):
    return ('<div class="bl-quadro%s"><img src="img/%s.webp?v=%s" data-lum="img/%s.webp?v=%s" alt="" loading="lazy"></div>'
            % (classe, p['foto'], V, p['lum'], V))


def capa(p):
    """18/10/2026: «a figura na pagina tem que ficar inteira». A capa do post leva a proporcao da propria foto (a do
    arquivo de luminancia), limitada a 460 px de altura pela largura; a foto nova da aba [ 12 ] do Spirit traz uma capa
    inteira propria (campos capa e capa_lum, gerados pelo blog_fotos.py), sem o corte 8:3 do cartao."""
    from PIL import Image
    f, l = p.get('capa', p['foto']), p.get('capa_lum', p['lum'])
    w, h = Image.open(os.path.join(SITE, 'img', l + '.webp')).size
    return ('<div class="bl-quadro bl-capa" style="aspect-ratio:%d / %d;max-width:calc(460px * %d / %d)">'
            '<img src="img/%s.webp?v=%s" data-lum="img/%s.webp?v=%s" alt="" loading="lazy"></div>' % (w, h, w, h, f, V, l, V))


# 18/10/2026: «faca um banner diferente para a pagina de conteudo» (trama sem foto, mais baixa): blog.html e os posts
BANNER = '<div class="page-banner bl-banner" data-lum="img/banner-conteudo-lum.webp?v=%s">' % V


def cartao(p):
    return ('    <a class="blog-card" href="%s.html" data-category="%s">\n'
            '      <div class="blog-card-img">%s<span class="category">%s</span></div>\n'
            '      <p class="author">Equipe Técnica Ideal Metrics &middot; %s</p>\n'
            '      <h3>%s</h3>\n'
            '    </a>' % (p['arquivo'], p['categoria'], quadro(p), e(p['rotulo']).upper(), data_br(p['data']), e(p['titulo'])))


def corpo(p):
    out, lista = [], False
    for t, x in p['blocos']:
        if t == 'li' and not lista:
            out.append('<ul>'); lista = True
        if t != 'li' and lista:
            out.append('</ul>'); lista = False
        if t == 'li':
            out.append('  <li>%s</li>' % e(x))
        elif t == 'h':
            out.append('<h3>%s</h3>' % e(x))
        elif t == 'fonte':
            out.append('<p class="bl-fonte">%s</p>' % e(x))
        else:
            out.append('<p>%s</p>' % e(x))
    if lista:
        out.append('</ul>')
    return '\n'.join(out)


def main():
    posts = json.load(open(os.path.join(AQUI, 'blog-posts.json'), encoding='utf-8'))
    posts.sort(key=lambda p: p['data'], reverse=True)
    p_blog = os.path.join(SITE, 'blog.html')
    raw = open(p_blog, 'rb').read(); crlf = b'\r\n' in raw
    t = raw.decode('utf-8').replace('\r\n', '\n')

    # 1. a grade do blog.html
    i = t.index('  <div class="blog-grid">'); j = t.index('</section>', i)
    grade = '  <div class="blog-grid">\n' + '\n'.join(cartao(p) for p in posts) + '\n  </div>\n'
    t = t[:i] + grade + t[j:]
    t = re.sub(r'<script>\n/\* blog: as fotos passam pelo motor.*?</script>\n', '', t, flags=re.S)
    t = t.replace('<script src="js/gaveta.js', MOTOR + '\n<script src="js/gaveta.js', 1)
    t = re.sub(r'<div class="page-banner[^"]*"[^>]*>', BANNER, t, count=1)
    open(p_blog, 'wb').write((t.replace('\n', '\r\n') if crlf else t).encode('utf-8'))

    # 2. uma pagina por post, na casca do blog.html
    a = t.index('<div class="page-banner'); b = t.index('</section>', a) + len('</section>')
    for k, p in enumerate(posts):
        outros = [q for q in posts if q is not p][:3]
        miolo = (BANNER + '<h1>%s</h1><p>%s</p></div>\n'
                 '<div class="breadcrumb"><a href="index.html">Página Inicial</a> &gt; <a href="blog.html">Conteúdo</a> &gt; %s</div>\n'
                 '<section class="bl-post">\n<article class="bl-artigo">\n'
                 '<p class="bl-meta">Equipe Técnica Ideal Metrics &middot; %s &middot; %d min de leitura &middot; %s</p>\n'
                 '%s\n<div class="bl-texto">\n%s\n</div>\n'
                 '<p class="bl-volta"><a href="blog.html">&larr; Todo o conteúdo</a></p>\n</article>\n'
                 '<aside class="bl-mais" aria-label="Outros posts"><p class="bl-mais-rot">Outros posts</p>\n<div class="blog-grid bl-mais-grade">\n%s\n</div></aside>\n'
                 '</section>') % (e(p['titulo']), e(p['rotulo']), e(p['titulo']), data_br(p['data']), leitura(p), e(p['rotulo']),
                                  capa(p), corpo(p), '\n'.join(cartao(q) for q in outros))
        s = t[:a] + miolo + t[b:]
        s = re.sub(r'<title>.*?</title>', '<title>%s | Conteúdo | Ideal Metrics</title>' % e(p['titulo']), s, count=1)
        open(os.path.join(SITE, p['arquivo'] + '.html'), 'wb').write((s.replace('\n', '\r\n') if crlf else s).encode('utf-8'))
        print(p['data'], p['arquivo'] + '.html')


if __name__ == '__main__':
    main()
