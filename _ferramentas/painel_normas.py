# -*- coding: utf-8 -*-
"""Gera dados/painel-normas.json para o painel de normas (painel-normas.html).

Fontes, ambas públicas:
  - ISO Open Data (licença ODC-By 1.0): normas, estágios e comitês.
    https://www.iso.org/open-data.html
  - ISO Survey 2025: certificados válidos por país e norma (planilha no vault).

Uso:  python _ferramentas/painel_normas.py          (baixa a base da ISO)
      python _ferramentas/painel_normas.py --cache  (usa a cópia já baixada)
"""
import json, os, sys, re, datetime, urllib.request

AQUI = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(AQUI)
CACHE = os.path.join(AQUI, '_cache-iso')
SAIDA = os.path.join(SITE, 'dados', 'painel-normas.json')
SURVEY = os.path.join(SITE, '..', '..', '— CQT', '✱ New Standards',
                      'ISO Survey — Certificações por País e Norma', '2025',
                      'ISO Survey 2025 — 1 Certificados e Sites por País.xlsx')
SURVEY_SETORES = SURVEY.replace('1 Certificados e Sites por País', '2 Setores EA por País')   # 27/10: certificados por setor EA
BASE = 'https://isopublicstorageprod.blob.core.windows.net/opendata/_latest'
ARQ = {'deliv': BASE + '/iso_deliverables_metadata/json/iso_deliverables_metadata.jsonl',
       'tc': BASE + '/iso_technical_committees/json/iso_technical_committees.jsonl'}

# Os dez temas do site (GRUPOS de setores.py), com os comitês ISO de cada um.
# Ordem importa: o prefixo mais específico vem antes (TC 207/SC 7 antes de TC 207).
TEMAS = [
    ('clima', 'Clima e carbono', ['ISO/TC 207/SC 7', 'ISO/TC 265']),
    ('ambiente', 'Meio ambiente', ['ISO/TC 207', 'ISO/TC 323', 'ISO/TC 331']),
    ('qualidade', 'Qualidade', ['ISO/TC 176']),
    ('sst', 'Saúde e segurança do trabalho', ['ISO/TC 283']),
    ('viaria', 'Segurança viária', ['ISO/TC 241']),
    ('esg', 'Sustentabilidade e ESG', ['ISO/TC 322', 'ISO/PC 343']),
    ('social', 'Responsabilidade social e cadeia de valor', ['ISO/TC 309/SC 2']),
    ('alimentos', 'Segurança de alimentos', ['ISO/TC 34/SC 17']),
    ('informacao', 'Segurança da informação e privacidade', ['ISO/IEC JTC 1/SC 27', 'ISO/IEC JTC 1/SC 42']),
    ('compliance', 'Compliance, riscos e continuidade', ['ISO/TC 309', 'ISO/TC 262', 'ISO/TC 292']),
    ('conformidade', 'Avaliação da conformidade', ['ISO/CASCO']),
    ('facilities', 'Facilities', ['ISO/TC 267']),
    ('energia', 'Energia', ['ISO/TC 301']),
    ('consultoria', 'Consultoria de gestão', ['ISO/TC 342']),   # 26/10/2026: ISO 20700 (a ISO 10019 segue em Qualidade, é do TC 176/SC 3)
]

# Comissão espelho na ABNT (só as que a Ideal Metrics acompanha; o resto fica em branco).
ABNT = {'ISO/TC 176': 'ABNT/CB-025', 'ISO/TC 207': 'ABNT/CB-038', 'ISO/TC 283': 'ABNT/CEE-109',
        'ISO/TC 241': 'ABNT/CB-016', 'ISO/TC 34/SC 17': 'ABNT/CEE-104', 'ISO/IEC JTC 1/SC 27': 'ABNT/CB-021',
        'ISO/IEC JTC 1/SC 42': 'ABNT/CEE-127', 'ISO/TC 309': 'ABNT/CEE-309', 'ISO/TC 262': 'ABNT/CEE-063',
        'ISO/TC 292': 'ABNT/CEE-063', 'ISO/CASCO': 'ABNT/CB-025', 'ISO/TC 267': 'ABNT/CEE-267', 'ISO/TC 342': 'ABNT/CEE-309',
        'ISO/TC 323': 'ABNT/CEE-323', 'ISO/PC 343': 'ABNT/CEE-256', 'ISO/TC 265': 'ABNT/CB-038'}

# Página de serviço do site para a norma (número base -> arquivo).
PAGINA = {'9001': 'norma-iso-9001.html', '14001': 'norma-iso-14001.html', '45001': 'norma-iso-45001.html',
          '39001': 'seguranca-viaria.html', '22000': 'seguranca-alimentos.html',
          '27001': 'compliance-seguranca-informacao.html', '37001': 'compliance-seguranca-informacao.html',
          '37301': 'compliance-seguranca-informacao.html', '14064-1': 'carbono-inventario-gee.html',
          '14067': 'carbono-pegada-produto.html', '14068-1': 'carbono-neutralizacao.html'}

# Abas do ISO Survey -> número da norma no painel.
SURVEY_ABAS = {'ISO 9001': '9001', 'ISO 14001': '14001', 'ISO 45001': '45001', 'ISO IEC 27001': '27001',
               'ISO 22000': '22000', 'ISO 13485': '13485', 'ISO 50001': '50001', 'ISO IEC 20000-1': '20000-1',
               'ISO 37001': '37001', 'ISO 22301': '22301', 'ISO 39001': '39001', 'ISO 28000': '28000',
               'ISO 37301': '37301', 'ISO 41001': '41001', 'ISO IEC 42001': '42001', 'ISO 44001': '44001',
               'ISO 21001': '21001', 'ISO 55001': '55001', 'ISO 20121': '20121', 'ISO 22716': '22716'}


def baixa(chave):
    os.makedirs(CACHE, exist_ok=True)
    destino = os.path.join(CACHE, chave + '.jsonl')
    if '--cache' not in sys.argv or not os.path.exists(destino):
        req = urllib.request.Request(ARQ[chave], headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=300) as r, open(destino, 'wb') as f:
            f.write(r.read())
    with open(destino, encoding='utf-8') as f:
        return [json.loads(l) for l in f if l.strip()]


def tema_de(comite):
    for chave, _, prefixos in TEMAS:
        for p in prefixos:
            if comite == p or comite.startswith(p + '/'):
                return chave
    return None


def comite_raiz(comite):
    """ISO/TC 207/SC 7 -> ISO/TC 207 (para achar a comissão ABNT)."""
    for k in sorted(ABNT, key=len, reverse=True):
        if comite == k or comite.startswith(k + '/'):
            return ABNT[k]
    return ''


def numero_base(ref):
    """'ISO/FDIS 28022' -> '28022'; 'ISO 14064-1:2018' -> '14064-1'."""
    m = re.search(r'(\d{3,5}(?:-\d+)?)', ref.split(':')[0])
    return m.group(1) if m else ''


def fase(stage):
    """Agrupa o código harmonizado da ISO nas fases que o painel mostra."""
    if stage is None:
        return None
    g, s = divmod(stage, 100)
    if g == 95:
        return 'retirada'  # norma retirada (95.99) ou em retirada: só no histórico
    if s == 98:
        return None  # projeto cancelado: fora do painel
    if g in (0, 10):
        return 'proposta'
    if g == 20:
        return 'preparacao'
    if g == 30:
        return 'comite'
    if g == 40:
        return 'consulta'
    if g == 50:
        return 'aprovacao'
    if g == 60 and s < 60:
        return 'aprovacao'
    if g == 90:
        return 'revisao' if s in (20, 60, 92) else 'publicada'
    if g == 95:
        return 'retirada'
    return 'publicada'


ALIAS = {'Chinese Taipei': 'TW', 'Korea (the Republic of)': 'KR', 'Korea (the Democratic People’s Republic of)': 'KP',
         'Türkiye': 'TR', 'Netherlands (Kingdom of the)': 'NL', 'Netherlands Antilles': None, 'Western Sahara*': 'EH',
         'Holy See (the)': 'VA', 'Palestine, State of': 'PS', 'Kosovo': 'XK', 'Lao People’s Democratic Republic (the)': 'LA',
         'Bonaire, Sint Eustatius and Saba': 'BQ', 'Falkland Islands (the) [Malvinas]': 'FK'}


def codigo_pais(nome):
    """Nome do ISO Survey -> (alpha2, numérico do mapa world-atlas)."""
    import pycountry
    n = nome.strip().replace('’', "'")
    if nome in ALIAS:
        a2 = ALIAS[nome]
        if not a2:
            return None, None
        c = pycountry.countries.get(alpha_2=a2)
        return a2, (c.numeric if c else None)
    limpo = re.sub(r'\s*\((the|Islamic Republic of|Plurinational State of|Bolivarian Republic of|Federated States of|the Republic of|the Democratic Republic of the|Kingdom of the)\)', '', n)
    limpo = re.sub(r'^(.*), (the )?(United Republic of|State of)$', r'\1', limpo).strip()
    for tent in (n, limpo, limpo.split(',')[0]):
        try:
            c = pycountry.countries.lookup(tent)
            return c.alpha_2, c.numeric
        except LookupError:
            pass
    try:
        cs = pycountry.countries.search_fuzzy(limpo)
        return cs[0].alpha_2, cs[0].numeric
    except LookupError:
        return None, None


def survey():
    try:
        import openpyxl
    except ImportError:
        print('openpyxl ausente: mapa sem dados'); return {}
    if not os.path.exists(SURVEY):
        print('planilha do ISO Survey não encontrada:', SURVEY); return {}
    wb = openpyxl.load_workbook(SURVEY, read_only=True, data_only=True)
    out = {}
    for aba, num in SURVEY_ABAS.items():
        if aba not in wb.sheetnames:
            continue
        ws = wb[aba]
        titulo = None
        paises = {}
        for i, row in enumerate(ws.iter_rows(values_only=True)):
            if i == 0:
                titulo = row[0]
                continue
            if i == 1 or not row or not row[0]:
                continue
            nome, cert = row[0], row[1]
            if isinstance(cert, (int, float)) and cert > 0 and str(nome).strip().lower() != 'total':
                nome = str(nome).strip()
                if nome not in CODIGOS:
                    CODIGOS[nome] = codigo_pais(nome)
                a2, numd = CODIGOS[nome]
                if not a2:
                    SEM_CODIGO.add(nome); continue
                paises[a2] = paises.get(a2, 0) + int(cert)
                NUMERICO[a2] = numd
                NOMES[a2] = nome
        if paises:
            out[num] = {'titulo': titulo, 'paises': paises, 'total': sum(paises.values())}
    if SEM_CODIGO:
        print('países sem código (fora do mapa):', sorted(SEM_CODIGO))
    return out


CODIGOS, NUMERICO, NOMES, SEM_CODIGO = {}, {}, {}, set()


def survey_setores():
    """27/10/2026: planilha 2 do ISO Survey, certificados por setor EA (39 setores) e por país. Sai, por norma, o total
    mundial de cada setor e o do Brasil; os nomes dos 39 setores vão uma vez só."""
    try:
        import openpyxl
    except ImportError:
        return {}
    if not os.path.exists(SURVEY_SETORES):
        print('planilha de setores do ISO Survey não encontrada:', SURVEY_SETORES); return {}
    wb = openpyxl.load_workbook(SURVEY_SETORES, read_only=True, data_only=True)
    out, nomes = {}, None
    for aba, num in SURVEY_ABAS.items():
        if aba not in wb.sheetnames:
            continue
        linhas = [r for r in wb[aba].iter_rows(values_only=True) if any(c is not None for c in r)]
        if len(linhas) < 4:
            continue
        nomes = nomes or [str(c).strip() for c in linhas[2][1:40]]
        mundo, br = [0] * 39, [0] * 39
        for r in linhas[3:]:
            if not r[0] or 'total' in str(r[0]).lower():
                continue
            for i in range(39):
                v = r[i + 1]
                if isinstance(v, (int, float)) and v > 0:
                    mundo[i] += int(v)
                    if str(r[0]).strip() == 'Brazil':
                        br[i] += int(v)
        if sum(mundo):
            out[num] = {'mundo': mundo, 'br': br}
    return {'setores': nomes, 'normas': out} if out else {}


def main():
    tcs = baixa('tc')
    tc_id = {t['reference']: t['id'] for t in tcs}
    tc_nome = {t['reference']: (t.get('title') or {}).get('en', '') for t in tcs}
    normas, historico = [], []
    for r in baixa('deliv'):
        if r['deliverableType'] in ('R', 'ISP', 'DATA', 'TTA') or r.get('supplementType'):
            continue
        comite = r.get('ownerCommittee') or ''
        t = tema_de(comite)
        f = fase(r.get('currentStage'))
        if t and f == 'retirada' and r.get('publicationDate'):
            # edição antiga, retirada: só para a linha do tempo
            historico.append({'id': r['id'], 'ref': r['reference'], 'num': numero_base(r['reference']), 'pub': r['publicationDate']})
        if not t or not f or f == 'retirada':
            continue
        titulo = (r.get('title') or {}).get('en') or ''
        if titulo.startswith('Title missing'):
            continue
        st = r['currentStage']
        normas.append({
            'id': r['id'], 'ref': r['reference'], 'num': numero_base(r['reference']),
            'tipo': r['deliverableType'], 'titulo': titulo, 'tema': t, 'fase': f,
            'est': '%02d.%02d' % divmod(st, 100), 'comite': comite,
            'tcid': tc_id.get(comite) or tc_id.get('/'.join(comite.split('/')[:2])),
            'tcnome': tc_nome.get(comite, ''), 'abnt': comite_raiz(comite),
            'pub': r.get('publicationDate'), 'ed': r.get('edition'),
            'pag': (r.get('pages') or {}).get('en'), 'ics': r.get('icsCode'),
            'subst': r.get('replaces'), 'substpor': r.get('replacedBy'),
            'escopo': re.sub(r'<[^>]+>', ' ', (r.get('scope') or {}).get('en') or '').strip()[:900] or None,
        })
    for n in normas:
        n['pagina'] = PAGINA.get(n['num'])
    dados = {
        'gerado': datetime.date.today().isoformat(),
        'fontes': {'iso': 'ISO Open Data, licença ODC-By 1.0 (iso.org/open-data.html)',
                   'survey': 'ISO Survey 2025, certificados válidos em 31-dez-2025'},
        'temas': [{'id': k, 'nome': n} for k, n, _ in TEMAS],
        'normas': sorted(normas, key=lambda n: (n['num'], n['ref'])),
        'historico': sorted(historico, key=lambda n: (n['num'], n['pub'])),
        'survey': survey(),
        'setores': survey_setores(),
    }
    # Tabela alpha2 -> id numérico do world-atlas e nome em inglês, uma vez só.
    dados['paises'] = {a2: {'n': NUMERICO.get(a2), 'nome': NOMES.get(a2)} for a2 in NOMES}
    os.makedirs(os.path.dirname(SAIDA), exist_ok=True)
    mudancas(dados)
    with open(SAIDA, 'w', encoding='utf-8') as f:
        json.dump(dados, f, ensure_ascii=False, separators=(',', ':'))
    print('normas:', len(normas), '| survey:', len(dados['survey']), '| bytes:', os.path.getsize(SAIDA))


MUD = os.path.join(SITE, 'dados', 'painel-mudancas.json')


def mudancas(novo):
    """Compara com a base anterior e acumula o que mudou (180 dias) em painel-mudancas.json.
    A ISO não publica a data de cada estágio; a data registrada é a da comparação."""
    hoje = novo['gerado']
    log = {'itens': []}
    if os.path.exists(MUD):
        log = json.load(open(MUD, encoding='utf-8'))
    def grava():
        log['desde'] = log.get('desde') or hoje
        log['atualizado'] = hoje
        json.dump(log, open(MUD, 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
    if not os.path.exists(SAIDA):
        return grava()
    velho = json.load(open(SAIDA, encoding='utf-8'))
    if velho.get('gerado') == hoje:
        return grava()  # rodou duas vezes no mesmo dia: não compara de novo
    antes = {n['id']: n for n in velho['normas']}
    itens = [i for i in log['itens'] if i['data'] != hoje]
    for n in novo['normas']:
        a = antes.get(n['id'])
        if not a:
            itens.append({'data': hoje, 'id': n['id'], 'ref': n['ref'], 'tipo': 'nova', 'de': None, 'para': n['est'], 'fase': n['fase'], 'tema': n['tema']})
        elif a['est'] != n['est']:
            itens.append({'data': hoje, 'id': n['id'], 'ref': n['ref'], 'tipo': 'estagio', 'de': a['est'], 'para': n['est'], 'fase': n['fase'], 'tema': n['tema']})
    ids = {n['id'] for n in novo['normas']}
    for i, a in antes.items():
        if i not in ids:
            itens.append({'data': hoje, 'id': i, 'ref': a['ref'], 'tipo': 'saiu', 'de': a['est'], 'para': None, 'fase': a['fase'], 'tema': a['tema']})
    limite = (datetime.date.fromisoformat(hoje) - datetime.timedelta(days=180)).isoformat()
    log['itens'] = [i for i in itens if i['data'] >= limite]
    grava()
    print('mudanças registradas hoje:', sum(1 for i in log['itens'] if i['data'] == hoje))


if __name__ == '__main__':
    main()
