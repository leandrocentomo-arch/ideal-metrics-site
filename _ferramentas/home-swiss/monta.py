"""Home no estilo suico (03/11/2026): monta index-swiss.html a partir do index.html vivo.

Fica da home atual: <head> e CSS, tarja, barra, menu em veu, a TIRA PANORAMICA (o mosaico de 8 cards)
e o letreiro; depois do letreiro entram as secoes novas (secoes-a.html), a secao Conhecimento da home
(o mapa de linhas, copiado como esta), as secoes novas da parte b, e o contato e o rodape de sempre.
O CSS novo (estilo.css) entra no fim do <style> do head; o script do motor (motor.js) entra antes do
js/busca.js, depois do js/trama.js. Rodar da raiz do site: python _ferramentas/home-swiss/monta.py
O index-swiss.html e rascunho e nao entra no repositorio (.gitignore)."""
import pathlib, re, sys

RAIZ = pathlib.Path(__file__).resolve().parents[2]
AQUI = pathlib.Path(__file__).resolve().parent
src = (RAIZ / 'index.html').read_text(encoding='utf-8')

def acha(marca, texto=src, n=1):
    i = -1
    for _ in range(n):
        i = texto.find(marca, i + 1)
        if i < 0: sys.exit(f'marcador nao encontrado: {marca!r}')
    return i

i_abre = acha('<div class="qc-abre">')                      # comeco da Frentes: tudo antes fica
i_ar   = acha('<section class="ar-sec" id="conhecimento"')  # mapa de linhas
i_nl   = acha('<!-- ===== newsletter e contato ===== -->')   # o do CSS e /* ... */, nao conta
cabeca = src[:i_abre]
ar     = src[i_ar:i_nl].replace('[ IM.3 ]', '[ 05 ]')
cauda  = src[i_nl:]

css  = (AQUI / 'estilo.css').read_text(encoding='utf-8')
js   = (AQUI / 'motor.js').read_text(encoding='utf-8')
sec_a = (AQUI / 'secoes-a.html').read_text(encoding='utf-8')
sec_b = (AQUI / 'secoes-b.html').read_text(encoding='utf-8')

# fecha a .qc-sec logo depois do letreiro (a Frentes, que a fechava, saiu)
cabeca = cabeca.rstrip() + '\n  </section>\n\n'
# CSS novo no fim do <style> do head
cabeca = cabeca.replace('</style>', css + '\n</style>', 1)
# rascunho: fora dos buscadores
cabeca = cabeca.replace('<meta name="description"', '<meta name="robots" content="noindex, nofollow">\n<meta name="description"', 1)
cabeca = cabeca.replace('<title>Ideal Metrics</title>', '<title>Ideal Metrics · home suíça (rascunho)</title>', 1)

corpo = cabeca + sec_a + '\n' + ar + '\n' + sec_b + '\n' + cauda
# o motor das fotos novas: depois do js/trama.js
corpo = corpo.replace('<script src="js/busca.js', '<script>\n' + js + '\n</script>\n<script src="js/busca.js', 1)

out = RAIZ / 'index-swiss.html'
out.write_text(corpo, encoding='utf-8')
print(out.name, len(corpo), 'bytes;', corpo.count('<section'), 'secoes')
