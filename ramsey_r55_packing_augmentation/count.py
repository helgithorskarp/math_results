"""Exact physical carrier count for the declared 1-to-2 packing rule."""
from collections import Counter
from fractions import Fraction as F
from itertools import combinations
from math import comb
from pathlib import Path
import json

HERE = Path(__file__).resolve().parent

def rat(x):
    return {'numerator': x.numerator, 'denominator': x.denominator}

def calculate():
    pins = json.loads((HERE / 'PINS.json').read_text())
    pairs = [sum(1 << i for i in s) for s in combinations(range(4), 2)]
    opposite = [pairs.index(15 ^ s) for s in pairs]
    weights = Counter()
    for x in range(15):
        for y in range(15):
            z = x & y
            weights[sum(1 << i for i, s in enumerate(pairs) if z & s == s)] += 1
    state = {0: 1}
    levels = []
    for m in range(1, 5):
        nxt = Counter()
        for a, v in state.items():
            for b, w in weights.items():
                reverse = sum(1 << opposite[i] for i in range(6) if b >> i & 1)
                if not a & reverse:
                    nxt[a | b] += v * w
        state = dict(nxt)
        levels.append({'m': m, 'allowed': sum(state.values()), 'total': 225 ** m,
                       'states': [[s, v] for s, v in sorted(state.items())]})
    p = {x['m']: F(x['allowed'], x['total']) for x in levels}
    classes = []
    old = new = old_composite = new_composite = F(0)
    for c in pins['classes']:
        q, r, n = c['q'], c['r'], c['n']
        a, b = r - 1, q - r
        per = (comb(1998+a-1, a) * comb(1931+b-1, b)
               * 37823 ** (comb(a, 2)+comb(b, 2)) * 35714 ** (a*b) * 15 ** (q*n))
        if per != c['per_task']:
            raise ValueError('carrier pin mismatch')
        mult = c['core_count']
        frac = p[{8: 4, 9: 2}[q]] ** r if q in (8, 9) else F(1)
        kept_per = per * frac
        if kept_per.denominator != 1:
            raise ValueError('noninteger carrier')
        old += mult * per
        new += mult * kept_per
        alive = mult - (518 if (q, r) == (7, 5) else 0)
        degree = F(**pins['q8_degree_bounds'][str(r)]) if q == 8 else F(1)
        old_composite += alive * per * degree
        new_composite += alive * per * min(degree, frac)
        classes.append(dict(q=q, r=r, core_count=mult, per_task=per,
                            retained_per_task=kept_per.numerator,
                            retained_fraction=rat(frac), clauses_per_task=(36*r if q == 8 else 6*r if q == 9 else 0)))
    if old.denominator != 1 or new.denominator != 1:
        raise ValueError('noninteger sum')
    if 20 * (old-new) < old:
        raise ValueError('declared five-percent gate failed')
    return dict(levels=levels, classes=classes, old_carrier=old.numerator,
                new_carrier=new.numerator, removed_fraction=rat((old-new)/old),
                old_composite_upper=rat(old_composite), new_composite_upper=rat(new_composite),
                composite_upper_decrease=rat((old_composite-new_composite)/old_composite),
                affected_tasks=sum(c['core_count'] for c in classes if c['q'] in (8,9)),
                remaining_whole_tasks=2188660, new_task_decisions=0,
                target_found=False, gate='PASS')

if __name__ == '__main__':
    print(json.dumps(calculate(), indent=2, sort_keys=True))
