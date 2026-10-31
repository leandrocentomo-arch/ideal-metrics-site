# -*- coding: utf-8 -*-
"""Certificados no Brasil pelo Inmetro (Certifiq): grava dados/inmetro-certifiq.json para a aba «Certificados no Brasil»
do Painel de normas (31/10/2026, Leandro: «coloque a opção de abrir o mapa do Brasil de certificados por estado e por setor»).

Fonte: Certifiq, sistema público do Inmetro com os certificados emitidos no Brasil por organismos acreditados pelo Inmetro
(só ABNT NBR ISO 9001 e ABNT NBR ISO 14001). Relatórios públicos, sem login:
  - Grafico/CertificadosValidosBrasil: certificados válidos na data, dentro e fora do SBAC (números embutidos no HTML);
  - Consulta/CertificacoesValidasConcedidas: certificados válidos por setor IAF (os 39 setores EA do ISO Survey);
  - Consulta/CertificadosConcedidosUF: empresas certificadas ou recertificadas por estado, ano a ano. A contagem por unidade de
    negócio (planta) seria a mais fiel ao mapa, mas o Certifiq tem unidades cadastradas em poucos certificados (31/10/2026: 331
    unidades contra 11.402 empresas na ISO 9001), então fica por empresa, no estado do cadastro dela. O Certifiq não dá os
    válidos por estado; a soma dos três últimos anos (o ciclo de um certificado) é a aproximação, e o painel diz isso.
O servidor é lento: cada consulta por estado é de um ano só (com todos os anos ele passa de 90 s e cai).

Uso: python _ferramentas/inmetro_certifiq.py          (da raiz do site)
     python _ferramentas/inmetro_certifiq.py --setores  (refaz só os setores no JSON que já existe)
"""
import datetime, html, json, os, re, sys, time
import requests

BASE = 'https://certifiq.inmetro.gov.br/'
NORMAS = {'9001': ('1', '5', 'ABNT NBR ISO 9001:2015'), '14001': ('3', '6', 'ABNT NBR ISO 14001:2015')}
SAIDA = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'dados', 'inmetro-certifiq.json')
# 31/10/2026, «no schedule, no painel do Spirit, entre também a base do Inmetro, que levantamos semanalmente»: cada rodada
# acrescenta uma linha (data, válidos e soma por estado) ao histórico, que a aba [ 11 ] Radar do Spirit mostra
HIST = os.path.join(os.path.dirname(SAIDA), 'inmetro-historico.json')

s = requests.Session(); s.headers['User-Agent'] = 'Mozilla/5.0 (Ideal Metrics, painel de normas)'


def pega(url, **kw):
    for tentativa in range(3):
        try:
            r = s.request('POST' if 'data' in kw else 'GET', BASE + url, timeout=300, **kw)
            r.raise_for_status()
            if 'Houve um erro na aplica' in r.text:
                raise RuntimeError('erro do Certifiq em ' + url)
            return r.text
        except Exception as e:
            print('  tentativa', tentativa + 1, 'falhou:', e); time.sleep(5)
    raise SystemExit('Certifiq não respondeu: ' + url)


def token(url):
    return re.search(r'name="__RequestVerificationToken"[^>]*value="([^"]+)"', pega(url)).group(1)


def tabela(h):
    t = re.findall(r'<table.*?</table>', h, re.S)
    if not t:
        return []
    return [[html.unescape(re.sub(r'<[^>]+>', '', c)).strip() for c in re.findall(r'<t[hd][^>]*>(.*?)</t[hd]>', row, re.S)]
            for row in re.findall(r'<tr.*?</tr>', t[0], re.S)]


def num(x):
    x = re.sub(r'[^\d]', '', x or '')
    return int(x) if x else 0


def validos_brasil():
    h = pega('Grafico/CertificadosValidosBrasil')
    cats = re.findall(r"'(ABNT NBR ISO [^']+)'", h)
    ser = {n: [int(v) for v in d.split(',')] for d, n in re.findall(r"data:\s*\[([\d,\s]+)\],\s*name:\s*'([^']+)'", h)}
    out = {}
    for k, (_, _, nome) in NORMAS.items():
        i = cats.index(nome)
        out[k] = {'sbac': ser['No SBAC'][i], 'fora': ser['Fora do SBAC'][i], 'total': ser['No SBAC'][i] + ser['Fora do SBAC'][i]}
    return out


def por_setor(tipo, padrao):
    u = 'Consulta/CertificacoesValidasConcedidas'
    d = {'__RequestVerificationToken': token(u), 'TipoConsulta': '0', 'TipoClassificacaoFiltroRelatorio': '1', 'ContarValidos': 'True',
         'IsCodigoNace': 'False', 'IdTipoAcreditacao': tipo, 'IdPadraoNormativo': padrao, 'BuscarCertificacoesValidasConcedidas': ''}
    linhas = tabela(pega(u, data=d))
    out = []   # agrupado pela seção NACE (A a U): «X - (v2.0) DESCRIÇÃO» vira «Descrição», em caixa de frase
    for l in linhas[1:]:
        if len(l) >= 3 and re.fullmatch(r'[A-Z]', l[0]):
            nome = re.sub(r'^[A-Z]\s*-\s*\(v[\d.]+\)\s*', '', l[1]).strip().lower()
            out.append({'codigo': l[0], 'setor': nome[:1].upper() + nome[1:], 'n': num(l[-1])})
    return out


def por_uf(tipo, padrao, ano):
    u = 'Consulta/CertificadosConcedidosUF'
    d = {'__RequestVerificationToken': token(u), 'TipoConsulta': '2', 'PorEmpresa': 'True', 'Sbac': '',   # 31/10: por EMPRESA. Testado por unidade de negócio no mesmo dia: o Certifiq só tem unidades em poucos certificados (331 na 9001 contra 11.402 empresas), então não serve para o mapa
         'IdTipoAcreditacao': tipo,
         'IdPadraoNormativo': padrao, 'PorAno': 'True', 'AnoInicial': str(ano), 'AnoFinal': str(ano), 'BuscarCertificacoesEmitidasUf': ''}
    out = {}
    for l in tabela(pega(u, data=d))[1:]:
        if len(l) >= 2 and re.fullmatch(r'[A-Z]{2}', l[0]):
            out[l[0]] = num(l[1])
    return out


def main():
    hoje = datetime.date.today()
    anos = [hoje.year - 2, hoje.year - 1, hoje.year]
    dados = {'fonte': 'Inmetro, Certifiq (certifiq.inmetro.gov.br)', 'gerado': hoje.isoformat(), 'anos_uf': anos, 'normas': {}}
    print('válidos no Brasil'); val = validos_brasil()
    for k, (tipo, padrao, nome) in NORMAS.items():
        print(k, 'setores'); setores = por_setor(tipo, padrao)
        uf = {}
        for a in anos:
            print(k, 'estados', a); uf[str(a)] = por_uf(tipo, padrao, a)
        soma = {}
        for a in uf.values():
            for sigla, n in a.items():
                soma[sigla] = soma.get(sigla, 0) + n
        dados['normas'][k] = {'nome': nome, 'validos': val[k], 'setores': setores, 'uf_ano': uf, 'uf': soma}
        print(' ', k, 'válidos', val[k]['total'], '· soma por estado', sum(soma.values()), '· setores', len(setores))
    with open(SAIDA, 'w', encoding='utf-8') as f:
        json.dump(dados, f, ensure_ascii=False, separators=(',', ':'))
    print('gravado', SAIDA)
    try:
        hist = json.load(open(HIST, encoding='utf-8'))
    except FileNotFoundError:
        hist = []
    hist = [h for h in hist if h.get('data') != dados['gerado']]
    hist.append({'data': dados['gerado'], 'normas': {k: dict(n['validos'], uf=sum(n['uf'].values())) for k, n in dados['normas'].items()}})
    hist.sort(key=lambda h: h['data'])
    json.dump(hist, open(HIST, 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
    print('histórico:', len(hist), 'rodadas')


if __name__ == '__main__':
    if '--setores' in sys.argv:
        d = json.load(open(SAIDA, encoding='utf-8'))
        for k, (tipo, padrao, _) in NORMAS.items():
            d['normas'][k]['setores'] = por_setor(tipo, padrao); print(k, len(d['normas'][k]['setores']), 'setores')
        json.dump(d, open(SAIDA, 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
    else:
        main()
