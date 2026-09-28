# -*- coding: utf-8 -*-
"""Gera img/monograma-ideal-m-prata.svg a partir do monograma oficial vigente.

    python _ferramentas/monograma_prata.py

24/09/2026: «uma cor mais escura e o monograma em prata». O arquivo prata que
existia era de 08/09, com o passaro antigo; ninguem o usava. O conteudo e
trocado, o nome fica (regra da casa: trocar conteudo, nao nome).

Receita: a geometria de monograma-ideal-m-limpo.svg (sem a placa), com TODO
preenchimento na MESMA prata, um degrade so em userSpaceOnUse sobre a caixa
inteira da marca, no angulo de 26 graus. E a «Prata» do painel Spirit
(MATERIAIS: #A9AAAA #D1D2D3 #FFFFFF #D1D2D3 #A9AAAA, 26 graus). Passaro e
letras no mesmo material: regra dura do Leandro."""

import math, os, re

SITE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ORIGEM = os.path.join(SITE, 'img', 'monograma-ideal-m-limpo.svg')
DESTINO = os.path.join(SITE, 'img', 'monograma-ideal-m-prata.svg')
PARADAS = [(0, '#A9AAAA'), (.2, '#D1D2D3'), (.5, '#FFFFFF'), (.8, '#D1D2D3'), (1, '#A9AAAA')]
ANGULO = 26

s = open(ORIGEM, encoding='utf-8').read()
w, h = [float(v) for v in re.search(r'viewBox="0 0 ([\d.]+) ([\d.]+)"', s).groups()]
cx, cy = w / 2, h / 2
dx, dy = math.cos(math.radians(ANGULO)), math.sin(math.radians(ANGULO))
meio = (w * abs(dx) + h * abs(dy)) / 2
x1, y1, x2, y2 = cx - dx * meio, cy - dy * meio, cx + dx * meio, cy + dy * meio
grad = ('<defs><linearGradient id="prata" gradientUnits="userSpaceOnUse" x1="%.2f" y1="%.2f" x2="%.2f" y2="%.2f">%s'
        '</linearGradient></defs>' % (x1, y1, x2, y2,
                                      ''.join('<stop offset="%g" stop-color="%s"/>' % p for p in PARADAS)))
cores = set(c.upper() for c in re.findall(r'fill="(#[0-9A-Fa-f]{3,6})"', s))
assert cores == {'#14304C'}, cores          # o oficial e uma cor so; se mudar, rever a receita
s = re.sub(r'fill="#14304[cC]"', 'fill="url(#prata)"', s)   # 28/09: o Asset 182 escreve o hex em minusculas
s = re.sub(r'(<svg[^>]*>)', r'\1' + grad, s, count=1)
open(DESTINO, 'w', encoding='utf-8', newline='\n').write(s)
print('prata:', DESTINO, '| %d preenchimentos' % s.count('url(#prata)'))
