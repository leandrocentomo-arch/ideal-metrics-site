# -*- coding: utf-8 -*-
"""19/10/2026: base tecnica de busca do site («pode fazer o item 1 inteiro»).

Em cada pagina viva (*.html da raiz, fora index-*, _prova*, apelidos com http-equiv refresh):
  meta description (se faltar, vem da frase de abertura ou do primeiro paragrafo), canonical em https://idealmetrics.org/,
  Open Graph + Twitter card, JSON-LD (Organization na home, Service nas paginas de servico, FAQPage onde ha .faq,
  BlogPosting nos posts, BreadcrumbList onde ha migalha).
Tudo entra entre <!-- seo --> e <!-- /seo -->, logo depois do <title>; rodar de novo substitui o bloco (idempotente).
Tambem escreve sitemap.xml e robots.txt. Rodar: python _ferramentas/seo.py (da raiz do site).
"""
import os, re, json, glob, html, subprocess
RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); os.chdir(RAIZ)
HOST = 'https://idealmetrics.org/'
OG_IMG = HOST + 'img/og-ideal-metrics.png?v=19102026a'
SERVICOS = set('''implantacao-iso norma-iso-9001 norma-iso-14001 norma-iso-45001 norma-iso-27001 norma-iso-22000 norma-iso-41001 norma-iso-37001 norma-iso-37301 seguranca-viaria compliance-seguranca-informacao suporte
padroes-mercado ifc-performance-standards sedex-smeta gestao-carbono esg seguranca-alimentos nrs inspecoes produtos-inspecionamos
estudos-pesquisa estudos-regulatorios estudos-setoriais observatorio-setorial rastreabilidade-cadeia
carbono-agro carbono-creditos carbono-descarbonizacao carbono-inventario-gee carbono-mercado-regulado carbono-neutralizacao carbono-pegada-produto'''.split())
# descricoes escritas a mao onde a frase de abertura ficou curta ou nao diz o servico (a chave e o arquivo)
DESCRICOES = {
    'servicos.html': 'Todos os serviços da Ideal Metrics: implantação de normas ISO, padrões de mercado, gestão de carbono, ESG, segurança de alimentos, NRs, inspeções e estudos e pesquisa aplicada.',
    'contato.html': 'Contato com a equipe técnica da Ideal Metrics: e-mail info@idealmetrics.org e WhatsApp. Consultoria em normas ISO, gestão de carbono e inspeções da qualidade.',
    'norma-iso-9001.html': 'Consultoria para implantação da ISO 9001:2026: sistema de gestão da qualidade, do diagnóstico à preparação para a certificação. Equipe em atuação desde 1998.',
    'norma-iso-14001.html': 'Consultoria para implantação da NBR ISO 14001:2026: sistema de gestão ambiental, do diagnóstico à preparação para a certificação. Equipe em atuação desde 1998.',
    'norma-iso-27001.html': 'Consultoria para implantação da NBR ISO/IEC 27001:2022: gestão da segurança da informação, riscos, Declaração de Aplicabilidade, Anexo A e LGPD no mesmo sistema.',
    'norma-iso-37301.html': 'Consultoria para implantação da NBR ISO 37301:2021: sistema de gestão de compliance, obrigações, riscos, canal de preocupações e programa de integridade.',
    'norma-iso-37001.html': 'Consultoria para implantação da NBR ISO 37001:2025: sistema de gestão antissuborno, riscos de suborno, due diligence, controles e canal de denúncias.',
    'norma-iso-41001.html': 'Consultoria para implantação da NBR ISO 41001:2020: sistema de gestão de facility management, estratégia e planos de FM, níveis de serviço, fornecedores e indicadores.',
    'norma-iso-22000.html': 'Consultoria para implantação da NBR ISO 22000:2019: sistema de gestão de segurança de alimentos, PPR, análise de perigos, plano HACCP e base para a FSSC 22000.',
    'norma-iso-45001.html': 'Consultoria para implantação da NBR ISO 45001:2018: sistema de gestão de saúde e segurança ocupacional, GRO e NRs no mesmo sistema, preparação para a certificação.',
    'produtos-inspecionamos.html': 'Produtos que a Ideal Metrics inspeciona: treze categorias, verificadas na fábrica e antes do embarque, no Brasil e no exterior.',
    'inspecoes.html': 'Inspeção de produtos e de fábricas na fonte fornecedora, no Brasil e no exterior: funcionamento, estado, embalagem e quantidade conferidos antes do embarque.',
    'rastreabilidade-cadeia.html': 'Rastreabilidade de cadeia: estudos que comprovam a origem do que a organização compra, como exigem os regulamentos de cadeia de fornecimento.',
    'blog-sedex-smeta.html': 'SEDEX SMETA: o que é a auditoria social e ética e como a Ideal Metrics apoia a organização na preparação.',
    'blog-consultoria-fsc.html': 'Certificação FSC: o que o padrão exige e como a Ideal Metrics apoia a organização a se tornar referência em sustentabilidade.',
}
NAO_INDEXAR = {'painel-placas.html'}   # pagina de trabalho (placas da tira), fora do sitemap e com noindex
MESES = {'jan': 1, 'fev': 2, 'mar': 3, 'abr': 4, 'mai': 5, 'jun': 6, 'jul': 7, 'ago': 8, 'set': 9, 'out': 10, 'nov': 11, 'dez': 12}
ORG = {"@type": "Organization", "name": "Ideal Metrics", "url": HOST, "logo": HOST + 'img/logo-ideal-m-escuro.svg?v=11102026b',
       "email": "info@idealmetrics.org", "address": {"@type": "PostalAddress", "addressRegion": "SP", "addressCountry": "BR"}}

def texto(h):
    h = re.sub(r'(?is)<(script|style).*?</\1>', '', h); h = re.sub(r'<[^>]+>', ' ', h)
    return re.sub(r'\s+', ' ', html.unescape(h)).strip()
def corta(s, n=155):
    if len(s) <= n: return s
    s = s[:n].rsplit(' ', 1)[0].rstrip(',;:')
    return s + ('' if s.endswith('.') else '.')
def esc(s): return html.escape(s, quote=True)

def descricao(t, blog):
    m = re.search(r'(?is)<p class="abre">(.*?)</p>', t)
    if m: return corta(texto(m.group(1)))
    if blog:
        m = re.search(r'(?is)<div class="bl-texto">\s*<p>(.*?)</p>', t)
        if m: return corta(texto(m.group(1)))
    m = re.search(r'(?is)<div class="content">(.*?)</div>', t)
    if m:
        p = re.search(r'(?is)<p(?: class="[^"]*")?>(.*?)</p>', m.group(1))
        if p and len(texto(p.group(1))) > 40: return corta(texto(p.group(1)))
    h1 = re.search(r'(?is)<h1[^>]*>(.*?)</h1>\s*(?:<p>(.*?)</p>)?', t)
    if h1: return corta(' · '.join(x for x in (texto(h1.group(1)), texto(h1.group(2) or '')) if x) + ' | Ideal Metrics')
    return 'Ideal Metrics: consultoria em normas ISO, padrões internacionais, gestão de carbono e inspeções da qualidade.'

def faq(t):
    itens = re.findall(r'(?is)<details class="faq-item"><summary>(.*?)</summary>(.*?)</details>', t)
    return [{"@type": "Question", "name": texto(q), "acceptedAnswer": {"@type": "Answer", "text": texto(a)}} for q, a in itens]

def migalha(t, url):
    m = re.search(r'(?is)<div class="breadcrumb">(.*?)</div>', t)
    if not m: return None
    itens = []
    for a, nome in re.findall(r'(?is)<a href="([^"]+)">(.*?)</a>', m.group(1)):
        itens.append((HOST + ('' if a == 'index.html' else a), texto(nome)))
    fim = texto(re.sub(r'(?is)<a[^>]*>.*?</a>', '', m.group(1))).strip('> ').strip()
    if fim: itens.append((url, fim))
    return {"@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n, "item": u} for i, (u, n) in enumerate(itens)]}

def bloco(f, t):
    blog = f.startswith('blog-') and f != 'blog.html'
    nome = f[:-5]
    url = HOST if f == 'index.html' else HOST + f
    titulo = texto(re.search(r'(?is)<title>(.*?)</title>', t).group(1))
    desc_existente = re.search(r'<meta name="description" content="([^"]*)"', t)
    if f in DESCRICOES and desc_existente:   # a escrita a mao vence a que a pagina trazia
        t = t.replace(desc_existente.group(0), '<meta name="description" content="%s">' % esc(DESCRICOES[f]))
    desc = DESCRICOES.get(f) or (html.unescape(desc_existente.group(1)) if desc_existente else descricao(t, blog))
    if f in NAO_INDEXAR and 'name="robots"' not in t: L0 = ['<meta name="robots" content="noindex">']
    else: L0 = []
    h1 = re.search(r'(?is)<h1[^>]*>(.*?)</h1>', t); h1 = texto(h1.group(1)) if h1 else titulo.split('|')[0].strip()
    L = ['<!-- seo -->'] + L0
    if not desc_existente: L.append('<meta name="description" content="%s">' % esc(desc))
    L += ['<link rel="canonical" href="%s">' % url,
          '<meta property="og:type" content="%s">' % ('article' if blog else 'website'),
          '<meta property="og:site_name" content="Ideal Metrics">', '<meta property="og:locale" content="pt_BR">',
          '<meta property="og:title" content="%s">' % esc(titulo), '<meta property="og:description" content="%s">' % esc(desc),
          '<meta property="og:url" content="%s">' % url, '<meta property="og:image" content="%s">' % OG_IMG,
          '<meta property="og:image:width" content="1200">', '<meta property="og:image:height" content="630">',
          '<meta name="twitter:card" content="summary_large_image">']
    grafo = []
    if f == 'index.html':
        grafo.append(dict(ORG, **{"@type": "Organization", "description": desc}))
        grafo.append({"@type": "WebSite", "name": "Ideal Metrics", "url": HOST})
    if nome in SERVICOS:
        grafo.append({"@type": "Service", "name": h1, "description": desc, "url": url, "provider": ORG, "areaServed": {"@type": "Country", "name": "Brasil"}, "serviceType": h1})
    if blog:
        m = re.search(r'<p class="bl-meta">(.*?)</p>', t); data = None
        if m:
            d = re.search(r'(\d{1,2}) de (\w{3})\.? de (\d{4})', texto(m.group(1)))
            if d: data = '%s-%02d-%02d' % (d.group(3), MESES[d.group(2).lower()], int(d.group(1)))
        post = {"@type": "BlogPosting", "headline": h1, "description": desc, "url": url, "mainEntityOfPage": url, "image": OG_IMG,
                "author": {"@type": "Organization", "name": "Equipe Técnica Ideal Metrics"}, "publisher": ORG, "inLanguage": "pt-BR"}
        if data: post["datePublished"] = data
        grafo.append(post)
    q = faq(t)
    if q: grafo.append({"@type": "FAQPage", "mainEntity": q})
    b = migalha(t, url)
    if b: grafo.append(b)
    if grafo:
        js = json.dumps({"@context": "https://schema.org", "@graph": grafo}, ensure_ascii=False).replace('</', '<\\/')
        L.append('<script type="application/ld+json">%s</script>' % js)
    L.append('<!-- /seo -->')
    return '\n'.join(L), desc, [g["@type"] for g in grafo], t

def paginas():
    for f in sorted(glob.glob('*.html')):
        if f.startswith('index-') or f.startswith('_'): continue
        t = open(f, 'rb').read().decode('utf-8')
        if 'http-equiv="refresh"' in t: continue
        yield f, t

def lastmod(f):
    try: return subprocess.check_output(['git', 'log', '-1', '--format=%cs', '--', f], text=True).strip() or None
    except Exception: return None

if __name__ == '__main__':
    urls = []
    for f, t in paginas():
        crlf = '\r\n' in t; t = t.replace('\r\n', '\n')
        t = re.sub(r'\n?<!-- seo -->.*?<!-- /seo -->', '', t, flags=re.S)
        if f == 'index.html': t = t.replace('<meta name="robots" content="noindex">\n', '')   # 19/10/2026: a home estava com noindex
        b, desc, tipos, t = bloco(f, t)
        t, n = re.subn(r'(</title>)', r'\1\n' + b.replace('\\', '\\\\'), t, count=1); assert n == 1, f
        open(f, 'wb').write((t.replace('\n', '\r\n') if crlf else t).encode('utf-8'))
        if f not in NAO_INDEXAR: urls.append((HOST if f == 'index.html' else HOST + f, lastmod(f)))
        print('%-42s %3d  %s' % (f, len(desc), ','.join(tipos)))
    sm = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for u, d in urls: sm.append('  <url><loc>%s</loc>%s</url>' % (u, '<lastmod>%s</lastmod>' % d if d else ''))
    sm.append('</urlset>'); open('sitemap.xml', 'w', encoding='utf-8', newline='\n').write('\n'.join(sm) + '\n')
    open('robots.txt', 'w', encoding='utf-8', newline='\n').write('User-agent: *\nAllow: /\nDisallow: /_esbocos/\nDisallow: /_ferramentas/\nDisallow: /index-\nDisallow: /_prova-\n\nSitemap: %ssitemap.xml\n' % HOST)
    print('sitemap:', len(urls), 'urls')
