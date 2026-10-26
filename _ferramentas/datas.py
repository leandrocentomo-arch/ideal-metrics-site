# -*- coding: utf-8 -*-
"""Datas do site em dd-mmm-aaaa (26/10/2026, Leandro: «formato da data "sempre" dd-mmm-aaaa»).

Troca, no TEXTO visivel das paginas vivas (o mesmo criterio do seo.py: *.html da raiz, fora index-*, _* e apelidos com
refresh), toda data dd/mm/aaaa por dd-mmm-aaaa (15/04/2026 -> 15-abr-2026) e o intervalo dd/mm a dd/mm/aaaa por
dd-mmm a dd-mmm-aaaa. Nao toca em <style>, <script>, comentario nem atributo (href, src, data-*): o JSON-LD sai de novo
pelo seo.py. Mes/ano solto (07/2026) NAO e trocado, porque no site ele tambem e numero de documento (NT nº 07/2026);
o script lista onde aparece, para conferir a mao.
Idempotente. Rodar da raiz: python _ferramentas/datas.py  (depois: python _ferramentas/seo.py e python _ferramentas/busca.py)
"""
import re, glob

MES = ['jan', 'fev', 'mar', 'abr', 'mai', 'jun', 'jul', 'ago', 'set', 'out', 'nov', 'dez']
CRU = re.compile(r'(<!--.*?-->|<style\b.*?</style>|<script\b.*?</script>|<[^>]+>)', re.S | re.I)
INTERVALO = re.compile(r'\b(\d{2})/(\d{2}) a (\d{2})/(\d{2})/(\d{4})\b')
DATA = re.compile(r'(?<![\d/])(\d{2})/(\d{2})/(\d{4})(?![\d/])')
MES_ANO = re.compile(r'(?<![\d/.])(0[1-9]|1[0-2])/(20\d\d)(?![\d/])')


def mes(m):
    n = int(m)
    return MES[n - 1] if 1 <= n <= 12 else None


def troca_texto(s):
    def intervalo(m):
        a, b = mes(m.group(2)), mes(m.group(4))
        return m.group(0) if not (a and b) else '%s-%s a %s-%s-%s' % (m.group(1), a, m.group(3), b, m.group(5))

    def data(m):
        a = mes(m.group(2))
        return m.group(0) if not a else '%s-%s-%s' % (m.group(1), a, m.group(3))
    return DATA.sub(data, INTERVALO.sub(intervalo, s))


def paginas():
    for f in sorted(glob.glob('*.html')):
        if f.startswith('index-') or f.startswith('_'):
            continue
        t = open(f, 'rb').read().decode('utf-8')
        if 'http-equiv="refresh"' in t:
            continue
        yield f, t


if __name__ == '__main__':
    total, conferir = 0, []
    for f, t in paginas():
        partes = CRU.split(t)
        novo = ''.join(p if i % 2 else troca_texto(p) for i, p in enumerate(partes))
        n = sum(1 for i, p in enumerate(partes) if not i % 2 for _ in DATA.finditer(p)) + \
            sum(1 for i, p in enumerate(partes) if not i % 2 for _ in INTERVALO.finditer(p))
        for i, p in enumerate(CRU.split(novo)):
            if not i % 2:
                conferir += ['%s: %s' % (f, p[max(0, m.start() - 40):m.end() + 10].strip()) for m in MES_ANO.finditer(p)]
        if novo != t:
            open(f, 'w', encoding='utf-8', newline='').write(novo)
            total += n
            print('%-44s %d' % (f, n))
    print('datas trocadas:', total)
    if conferir:
        print('mes/ano solto, conferir a mao:')
        for c in conferir:
            print('  ', c)
