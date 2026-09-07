"""Exhaustive small cases and adversarial controls, not a proof by sampling."""
from collections import Counter
from copy import deepcopy
from fractions import Fraction as F
from itertools import combinations, product
import json
from pathlib import Path
import generate as p
import verify as v


def formal_sum(points):
    result = Counter()
    for a, b in zip(points, points[1:]+points[:1]):
        d = tuple(y-x for x, y in zip(a, b))
        v.require(any(d), 'Zero edge')
        sign = 1 if next(x for x in d if x) > 0 else -1
        result[tuple(sign*x for x in d)] += sign
    return {d: c for d, c in result.items() if c}


def main():
    totals = Counter()
    for n in range(6):
        pairs = list(combinations(range(n), 2))
        for bits in range(1 << len(pairs)):
            edges = [e for i, e in enumerate(pairs) if bits >> i & 1]
            # Exhaust every two-colour word, independently of producer BFS.
            bip = any(all(((word >> a) ^ (word >> b)) & 1 for a, b in edges)
                      for word in range(1 << n))
            base = p.canonical_graph(n, edges)
            totals['base_graphs'] += 1
            for r in range(1, 5):
                case = p.produce(base, r)
                v.require((case['kind'] == 'polygon_map') == bip, 'Wrong bipartite verdict')
                v.check_case(case)
                totals['lift_cases'] += 1
                totals[case['kind']] += 1

    # Check both order-budget boundaries and a tall lift. The universal
    # theorem is proved by the telescoping identity, not these finite checks.
    boundaries = []
    for k, r in [(3, 169), (169, 3), (253, 2), (507, 1)]:
        c = p.produce(p.canonical_graph(k, [(i, (i+1) % k) for i in range(k)]), r)
        boundaries.append(v.check_case(c))

    fixture = p.fixture()
    c = fixture['cases'][1]
    signed = deepcopy(c['certificate'])
    signed['multiplier'] *= -3
    for face in signed['faces']:
        face[0] *= -3
    v.check_square_certificate(c['graph'], signed)
    n = c['graph']['vertices']
    relabel = lambda a: n-1-a
    g = p.canonical_graph(n, [[relabel(a), relabel(b)] for a, b in c['graph']['edges']])
    z = deepcopy(c['certificate'])
    z['walk'] = list(map(relabel, z['walk']))
    z['faces'] = [[f[0]] + list(map(relabel, f[1:])) for f in z['faces']]
    v.check_square_certificate(g, z)

    # Two independent exact geometric controls: rational plane unit walks,
    # including both possible collapsed diagonals, and a spatial countercase.
    directions = {(-F(1), F(0))}
    for t in map(F, ['0', '1', '-1', '2', '-2', '1/2', '-1/2', '3', '-3']):
        directions.add(((1-t*t)/(1+t*t), 2*t/(1+t*t)))
    origin = (F(0), F(0))
    geometric = Counter()
    for a, b in product(sorted(directions), repeat=2):
        for kind, walk in [
            ('parallelogram', [origin, a, tuple(x+y for x, y in zip(a, b)), b]),
            ('first_diagonal_collapsed', [origin, a, origin, b]),
            ('second_diagonal_collapsed', [a, origin, b, origin])]:
            v.require(all(sum((x-y)**2 for x, y in zip(s, t)) == 1
                          for s, t in zip(walk, walk[1:]+walk[:1])), 'Nonunit control')
            v.require(not formal_sum(walk), 'Plane square failed formal cancellation')
            geometric[kind] += 1
    tetra = [(1, 1, 1), (1, -1, -1), (-1, 1, -1), (-1, -1, 1)]
    v.require(all(sum((x-y)**2 for x, y in zip(a, b)) == 8 for a, b in combinations(tetra, 2)), 'Bad spatial control')
    v.require(bool(formal_sum(tetra)), 'Dimension boundary was lost')

    malformed = []
    def bad(change):
        x = deepcopy(c)
        change(x)
        malformed.append(x)
    bad(lambda x: x['certificate'].update(multiplier=0))
    bad(lambda x: x['certificate'].update(multiplier=True))
    bad(lambda x: x['certificate'].update(multiplier=3))
    bad(lambda x: x['certificate']['faces'].pop())
    bad(lambda x: x['certificate']['faces'][0].__setitem__(0, -1))
    bad(lambda x: x['certificate']['faces'][0].__setitem__(1, n))
    bad(lambda x: x['certificate']['walk'].pop())
    bad(lambda x: x['certificate']['walk'].__setitem__(0, x['certificate']['walk'][1]))
    bad(lambda x: x['graph']['edges'].pop())
    bad(lambda x: x['graph']['edges'].append(x['graph']['edges'][0]))
    bad(lambda x: x['graph']['edges'][0].__setitem__(1, 0))
    bad(lambda x: x.update(layers=0))
    bad(lambda x: x.update(kind='unknown'))
    bad(lambda x: x['base']['edges'].pop())
    bad(lambda x: x['certificate']['faces'][0].append(0))
    for x in malformed:
        try:
            v.check_case(x)
        except ValueError:
            pass
        else:
            raise ValueError('Accepted corrupt obstruction')
    positive = deepcopy(fixture['cases'][4])
    positive['certificate']['map'] = [0]*positive['graph']['vertices']
    try:
        v.check_case(positive)
    except ValueError:
        pass
    else:
        raise ValueError('Accepted constant edge map')
    # The even-cycle chain identity is real but cannot be used as an odd
    # obstruction. This protects against overextending to bipartite bases.
    even = p.canonical_graph(10, [(i, (i+1) % 10) for i in range(10)])
    try:
        v.check_square_certificate(p.lift(even, 2), p.square_witness(10, 2, list(range(10))))
    except ValueError:
        pass
    else:
        raise ValueError('Accepted even-cycle obstruction')
    out = {'small_exhaustive': dict(totals), 'boundary_cases': boundaries,
           'rational_unit_quadrilaterals': dict(geometric),
           'signed_coefficient_and_relabelled_certificates': 2,
           'spatial_failure_control': True, 'malformed_inputs_rejected': len(malformed)+2}
    expected = Path(__file__).with_name('controls_expected.json')
    if expected.exists():
        v.require(out == json.loads(expected.read_text()), 'Controls changed')
    print(json.dumps(out, sort_keys=True, indent=2))


if __name__ == '__main__':
    main()
