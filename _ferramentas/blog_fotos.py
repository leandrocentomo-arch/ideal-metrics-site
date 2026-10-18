# -*- coding: utf-8 -*-
"""As fotos do blog pela receita da aba [ 12 ] Blog do Spirit (18/10/2026).

    python _ferramentas/blog_fotos.py <receita.json>

A receita e o JSON de «copiar receita para o Claude»: {"tipo": "blog", "vaga": [720, 270], "fotos": [{"post", "foto",
"zoom", "px", "py", "gama"}, ...]}. Para cada foto:
  - acha o arquivo cru pelo nome em _tingir-fotos/FOTOS ou em Downloads; o que vier de Downloads e copiado para FOTOS
    (o cru mora la para sempre, regra da pasta);
  - gera img/<post>-bayer.webp e img/<post>-lum.webp no tingimento azul (foto_azul.py, vaga 8:3, mesmo recorte do Spirit);
  - aponta o post para elas no blog-posts.json.
Depois sobe o ?v= das fotos no blog.py e regrava o blog (python _ferramentas/blog.py)."""
import os, sys, json, shutil, subprocess, datetime, re

AQUI = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(AQUI)
FOTOS = os.path.join(os.path.dirname(SITE), '_tingir-fotos', 'FOTOS')
DOWN = os.path.join(os.path.expanduser('~'), 'Downloads')


def acha(nome):
    for pasta in (FOTOS, DOWN):
        f = os.path.join(pasta, nome)
        if os.path.isfile(f):
            if pasta == DOWN:
                shutil.copy2(f, os.path.join(FOTOS, nome)); print('  copiado de Downloads para FOTOS:', nome)
                f = os.path.join(FOTOS, nome)
            return f
    sys.exit('foto crua nao achada em FOTOS nem em Downloads: %s' % nome)


def main():
    R = json.load(open(sys.argv[1], encoding='utf-8'))
    assert R.get('tipo') == 'blog', 'receita nao e da aba [ 12 ] Blog'
    W, H = R.get('vaga', [720, 270])
    p_json = os.path.join(AQUI, 'blog-posts.json')
    posts = json.load(open(p_json, encoding='utf-8'))
    por = {p['arquivo']: p for p in posts}
    for f in R['fotos']:
        p = por.get(f['post'])
        assert p, 'post desconhecido: %s' % f['post']
        print(f['post'])
        cru = acha(f['foto'])
        subprocess.run([sys.executable, os.path.join(AQUI, 'foto_azul.py'), cru, f['post'], '--larg', str(W), '--alt', str(H),
                        '--px', str(f.get('px', 50)), '--py', str(f.get('py', 50)), '--zoom', str(f.get('zoom', 1)),
                        '--gama', str(f.get('gama', 1))], check=True)
        # 18/10/2026: «a figura na pagina tem que ficar inteira»: a capa do post e a foto INTEIRA (sem o corte 8:3 do
        # cartao), 760 de largura na proporcao do proprio arquivo, com a mesma exposicao
        from PIL import Image
        w, h = Image.open(cru).size
        subprocess.run([sys.executable, os.path.join(AQUI, 'foto_azul.py'), cru, f['post'] + '-capa', '--larg', '760',
                        '--alt', str(round(760 * h / w)), '--gama', str(f.get('gama', 1))], check=True)
        p['foto'], p['lum'], p['cru'] = f['post'] + '-bayer', f['post'] + '-lum', f['foto']
        p['capa'], p['capa_lum'] = f['post'] + '-capa-bayer', f['post'] + '-capa-lum'
    json.dump(posts, open(p_json, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    p_blog = os.path.join(AQUI, 'blog.py')
    t = open(p_blog, encoding='utf-8').read()
    t = re.sub(r"^V = '\d+'", "V = '%s'" % datetime.datetime.now().strftime('%d%m%Y%H%M'), t, count=1, flags=re.M)
    open(p_blog, 'w', encoding='utf-8', newline='').write(t)
    subprocess.run([sys.executable, p_blog], check=True)


if __name__ == '__main__':
    main()
