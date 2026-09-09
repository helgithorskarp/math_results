"""Independent weighted-tuple enumeration; imports no producer module."""
from fractions import Fraction
from itertools import product
from pathlib import Path
import json
import sys

def need(value, message):
    if not value:
        raise ValueError(message)

def check(path):
    data = json.loads(Path(path).read_text())
    pins = json.loads((Path(__file__).resolve().parent / 'PINS.json').read_text())
    masks = [3, 5, 9, 6, 10, 12]
    def conflict(xs):
        return any((xs[i] & s) == s and (xs[j] & (15-s)) == 15-s
                   for i in range(len(xs)) for j in range(i+1, len(xs)) for s in masks)
    hist = [0]*15
    for x in range(15):
        for y in range(15):
            hist[x & y] += 1
    need(hist == [3**(4-z.bit_count())-2 for z in range(15)], 'intersection weights')
    counts = {}
    for m in (1, 2, 3, 4):
        count = 0
        for xs in product(range(15), repeat=m):
            if not conflict(xs):
                weight = 1
                for z in xs:
                    weight *= hist[z]
                count += weight
        counts[m] = count
        level = data['levels'][m-1]
        need(level['m'] == m and level['allowed'] == count and level['total'] == 15**(2*m), 'tuple count')
        # Also check the certificate's entire state table directly, rather than its recurrence.
        state_counts = {}
        for xs in product(range(15), repeat=m):
            if conflict(xs):
                continue
            pairs = [3, 5, 9, 6, 10, 12]
            state = sum(1 << k for k, s in enumerate(pairs) if any(z & s == s for z in xs))
            weight = 1
            for z in xs:
                weight *= hist[z]
            state_counts[state] = state_counts.get(state, 0) + weight
        need(level['states'] == [[s, v] for s, v in sorted(state_counts.items())], 'all states')
    literal = sum(not conflict([x & y, z & w]) for x,y,z,w in product(range(15), repeat=4))
    need(literal == counts[2], 'four endpoint-star exhaustion')
    # Root multisets counted by coefficient recurrence, not binomial formula.
    def multisets(values, length):
        c = [1]+[0]*length
        for _ in range(values):
            for j in range(1, length+1):
                c[j] += c[j-1]
        return c[length]
    old = new = old_comp = new_comp = Fraction(0)
    affected = 0
    for pin, c in zip(pins['classes'], data['classes'], strict=True):
        q, r, n = pin['q'], pin['r'], pin['n']
        need(c['q'] == q and c['r'] == r and c['core_count'] == pin['core_count'], 'class identity')
        per = multisets(1998, r-1)*multisets(1931, q-r)
        for i in range(1, q):
            for j in range(i+1, q):
                per *= 37823 if (i < r) == (j < r) else 35714
        for _ in range(q*n):
            per *= 15
        f = Fraction(counts[{8:4, 9:2}[q]], 15**(2*{8:4, 9:2}[q]))**r if q in (8,9) else Fraction(1)
        need(per == pin['per_task'] == c['per_task'], 'physical product')
        need(per*f == c['retained_per_task'], 'class retained')
        need(Fraction(**c['retained_fraction']) == f, 'fraction')
        need(c['clauses_per_task'] == (36*r if q == 8 else 6*r if q == 9 else 0), 'clause count')
        mult = pin['core_count']
        old += per*mult
        new += per*mult*f
        alive = mult-(518 if (q,r)==(7,5) else 0)
        degree = Fraction(**pins['q8_degree_bounds'][str(r)]) if q == 8 else Fraction(1)
        old_comp += alive*per*degree
        new_comp += alive*per*min(f,degree)
        if q in (8,9):
            affected += mult
    need(old == data['old_carrier'] == pins['old_carrier'], 'old sum')
    need(new == data['new_carrier'], 'new sum')
    need(Fraction(**data['removed_fraction']) == (old-new)/old, 'removed fraction')
    need(Fraction(**data['old_composite_upper']) == old_comp, 'old composite')
    need(Fraction(**data['new_composite_upper']) == new_comp, 'new composite')
    need(Fraction(**data['composite_upper_decrease']) == (old_comp-new_comp)/old_comp, 'composite reduction')
    need(20*(old-new) >= old and data['gate'] == 'PASS', 'five-percent gate')
    need(data['affected_tasks'] == affected == 2187234, 'affected tasks')
    need(data['remaining_whole_tasks'] == 2188660 and data['new_task_decisions'] == 0 and data['target_found'] is False, 'claim status')
    return {'status':'INDEPENDENT_COUNT_PASS', 'weighted_tuples':sum(15**m for m in range(1,5)), 'literal_star_tuples':15**4}

if __name__ == '__main__':
    print(json.dumps(check(sys.argv[1]), sort_keys=True))
