# -*- coding: utf-8 -*-
"""Conferência das normas citadas no site (09/11/2026).

    python _ferramentas/conferir-normas.py

Nasceu depois que a ISO 56002 ficou publicada na lista «Normas que atuamos» sem ninguém ver: a nota em
setores-revisoes.json já dizia que ela era guia, mas nada cruzava os dados com as páginas. Roda no pre-commit do
repositório (.git/hooks/pre-commit) e sai com código 1 quando acha problema. Regras:

  1. FORA_DO_SITE: normas que o Leandro decidiu não anunciar. Nenhum arquivo publicado pode citá-las.
  2. As listas .norm-list de implantacao-iso.html e servicos.html são iguais entre si e iguais a CATALOGO.
  3. Ano da ABNT com prefixo ISO (ex.: «ISO 22000:2019», quando a ISO é 2018 e a NBR é 2019) é erro.
  4. Número de norma sem «ISO» na frente («ISO 9001, 14001 e 45001») é erro (regra de 03/11/2026).

Quando uma norma mudar de edição: atualizar CATALOGO e ANOS aqui, setores-revisoes.json e rodar setores.py.
Edições conferidas em fonte oficial (iso.org, ABNT via normas.com.br, FSSC, IATF, SAI) em 09/11/2026."""
import os, re, sys, subprocess

AQUI = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(AQUI)

FORA_DO_SITE = {   # número: motivo
    '56001': 'gestão da inovação: o Leandro ainda não anuncia (09/11/2026)',
    '56002': 'gestão da inovação: guia, não certificável; retirada do site em 09/11/2026',
}

CATALOGO = [   # a lista «Normas que atuamos», na ordem do site
    'NBR ISO 9001:2026', 'NBR ISO 14001:2026', 'NBR ISO 45001:2018 (2024)', 'NBR ISO 39001:2015', 'NBR ISO 41001:2020',
    'NBR ISO 37001:2025', 'NBR ISO 37301:2021', 'NBR ISO 50001:2018', 'NBR ISO/IEC 27001:2022', 'NBR ISO 55001:2024',
    'NBR ISO 22000:2019', 'FSSC 22000 v7', 'NBR ISO 13485:2016', 'IATF 16949:2016', 'SA8000:2026', 'ISO 21001:2025',
    'NBR ISO/IEC 17025:2017',
]

ANOS = {   # número: (ano da edição ISO vigente, ano da NBR vigente ou None)
    '9001': (2026, 2026), '14001': (2026, 2026), '45001': (2018, 2024), '39001': (2012, 2015), '41001': (2018, 2020),
    '37001': (2025, 2025), '37301': (2021, 2021), '50001': (2018, 2018), '27001': (2022, 2022), '55001': (2024, 2024),
    '22000': (2018, 2019), '13485': (2016, 2016), '21001': (2025, 2020), '17025': (2017, 2017),
}


def publicados():
    saida = subprocess.check_output(['git', 'ls-files', '*.html', '*.js', '*.json'], cwd=SITE, text=True, encoding='utf-8')
    for f in saida.splitlines():
        if f.startswith(('_', 'stal/')) or '/_' in f: continue
        yield f


def texto(f):
    with open(os.path.join(SITE, f), encoding='utf-8', errors='replace') as h: return h.read()


def main():
    erros = []
    listas = {}
    for f in publicados():
        s = texto(f)
        for n, motivo in FORA_DO_SITE.items():
            for m in re.finditer(r'ISO ' + n + r'\b', s):
                erros.append('%s: cita a ISO %s (%s)' % (f, n, motivo)); break
        for m in re.finditer(r'(?<!NBR )(?<!NBR» )ISO (?:/IEC )?(\d{4,5}):(\d{4})', s):
            n, ano = m.group(1), int(m.group(2))
            if n in ANOS and ANOS[n][1] and ano == ANOS[n][1] and ano != ANOS[n][0]:
                erros.append('%s: «%s» usa o ano da NBR com prefixo ISO; escrever NBR ISO %s:%d' % (f, m.group(0), n, ano))
        for m in re.finditer(r'ISO (?:/IEC )?\d{4,5}(?::\d{4})?(?:, \d{4,5}(?::\d{4})?)+|ISO (?:/IEC )?\d{4,5}(?::\d{4})? e \d{4,5}', s):
            erros.append('%s: «%s» tem número de norma sem «ISO» na frente' % (f, m.group(0)))
        if f in ('implantacao-iso.html', 'servicos.html'):
            m = re.search(r'<div class="norm-list">(<p>(?:<a [^>]*>)?(?:NBR |ISO |FSSC |IATF |SA)[^<]*.*?)</div>', s)
            listas[f] = re.findall(r'<p>(?:<a [^>]*>)?([^<]+)', m.group(1)) if m else None
    for f, l in listas.items():
        if l is None: erros.append('%s: lista «Normas que atuamos» não encontrada' % f)
        elif l != CATALOGO:
            dif = [x for x in l if x not in CATALOGO] + ['falta ' + x for x in CATALOGO if x not in l]
            erros.append('%s: lista de normas difere do CATALOGO: %s' % (f, '; '.join(dif) or 'ordem'))
    if erros:
        print('conferir-normas: %d problema(s)' % len(erros))
        for e in erros: print('  - ' + e)
        sys.exit(1)
    print('conferir-normas: ok (%d normas no catálogo)' % len(CATALOGO))


if __name__ == '__main__':
    main()
