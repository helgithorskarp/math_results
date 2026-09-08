"""Exact weighted induction and explicit lower-bound graphs. No solver."""
from fractions import Fraction
from itertools import combinations, product
import json
from pathlib import Path


def derive():
    bounds = {}
    rows = []
    for total in range(2, 9):
        for a in range(1, 5):
            b = total - a
            if not 1 <= b <= 4:
                continue
            prior = [(Fraction(f, p*q), p, q)
                     for (p, q), f in bounds.items() if p <= a and q <= b]
            rho = max((x[0] for x in prior), default=Fraction(0))
            perfect = int(a*b*rho)
            ps = [p for p in product(range(1, a), repeat=5)
                  if all(p[i]+p[(i+1) % 5] <= a for i in range(5))]
            qs = [q for q in product(range(1, b), repeat=5)
                  if all(q[i]+q[(i+2) % 5] <= b for i in range(5))]
            best, maximizers = 0, []
            for p in ps:
                for q in qs:
                    value = sum(bounds[p[i], q[i]] for i in range(5))
                    if value > best:
                        best, maximizers = value, []
                    if value == best:
                        maximizers.append([list(p), list(q)])
            bound = max(1, perfect, best)
            bounds[a, b] = bound
            rows.append({
                'omega': a, 'alpha': b, 'upper': bound,
                'rho': [rho.numerator, rho.denominator],
                'rho_attainers': [[p, q] for r, p, q in prior if r == rho],
                'perfect_upper': perfect, 'c5_upper': best,
                'c5_population_count': len(ps)*len(qs),
                'c5_maximizers': maximizers,
            })
    return {'rows': rows, 'max_good_order': bounds[4, 4],
            'excluded_core_order': bounds[4, 4]+1,
            'target_order': 43, 'arbitrary_outside_vertices': 17,
            'c5_population_checks': sum(r['c5_population_count'] for r in rows)}


def witnesses(table):
    rows = {(r['omega'], r['alpha']): r for r in table['rows']}

    def graph(a, b):
        if a == 1:
            return b, set(), {'kind': 'independent', 'n': b}
        if b == 1:
            return a, set(combinations(range(a), 2)), {'kind': 'clique', 'n': a}
        row = rows[a, b]
        if row['c5_upper'] != row['upper']:
            raise ValueError('No attaining construction')
        p, q = row['c5_maximizers'][0]
        parts, edges, offset, trees = [], set(), 0, []
        for x, y in zip(p, q):
            n, child, tree = graph(x, y)
            parts.append(list(range(offset, offset+n)))
            edges.update((u+offset, v+offset) for u, v in child)
            offset += n
            trees.append(tree)
        for i in range(5):
            for u in parts[i]:
                for v in parts[(i+1) % 5]:
                    edges.add(tuple(sorted((u, v))))
        return offset, edges, {'kind': 'cycle5', 'children': trees}

    answer = []
    for a in range(1, 5):
        for b in range(1, 5):
            n, edges, tree = graph(a, b)
            word = sum(1 << k for k, uv in enumerate(combinations(range(n), 2))
                       if uv in edges)
            width = max(1, (n*(n-1)//2+3)//4)
            answer.append({'omega': a, 'alpha': b, 'n': n,
                           'red_bits_hex': format(word, '0%dx' % width),
                           'tree': tree})
    return {'bit_order': 'low bits for lexicographic unordered pairs',
            'graphs': answer}


if __name__ == '__main__':
    import sys
    table = derive()
    value = witnesses(table) if sys.argv[1:] == ['--witnesses'] else table
    if sys.argv[1:] not in ([], ['--witnesses']):
        raise SystemExit('usage: derive.py [--witnesses]')
    print(json.dumps(value, indent=2, sort_keys=True))
