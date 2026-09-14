#!/usr/bin/env python3
"""Different exact edge decision: modular exclusions plus polynomial products.

Imports no construction or verification code. Does not audit the imported
minimum-order theorems or the historical positive-parent refutations.
"""
from fractions import Fraction
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parent

def need(ok, message):
    if not ok:
        raise ValueError(message)

def mult(a, b):
    out = [0]*8
    for i, x in enumerate(a):
        if x:
            for j, y in enumerate(b):
                factor = 1
                for bit, radicand in enumerate((3, 5, 11)):
                    if (i & j) & (1 << bit):
                        factor *= radicand
                out[i ^ j] += x*y*factor
    return out

def main():
    manifest = json.loads((ROOT/'manifest.json').read_text())
    for p, h in manifest['inputs'].items():
        need(sha256((REPO/p).read_bytes()).hexdigest() == h, 'input hash')
    rows = []
    for line in (REPO/'hadwiger_nelson_parts509_completion_census_degree9/points.tsv').read_text().splitlines():
        if line and not line.startswith('#'):
            v = [3*int(x) for x in line.split()]
            rows.append((tuple(v[:8]), tuple(v[8:])))
    data = json.loads((REPO/'hadwiger_nelson_parts509_pair_replacement_classification/certificate.json').read_text())
    ids = sorted({i for r in data['records'] for i in r['A']})
    q = json.loads((REPO/'hadwiger_nelson_parts509_swap_closure/completion_points.json').read_text())['points']
    points = dict(enumerate(rows))
    for i in ids+[523, 619]:
        axes = []
        for axis in ('x', 'y'):
            v = [288*Fraction(x) for x in q[i][axis]]
            need(all(x.denominator == 1 for x in v), 'denominator')
            axes.append(tuple(map(int, v)))
        points[509+i] = tuple(axes)
    need(len(points) == len(set(points.values())) == 530, 'physical point count')
    prime = 1321
    need(all(prime % n for n in range(2, 37)), 'prime')
    roots = [next(x for x in range(prime) if x*x % prime == d) for d in (3, 5, 11)]
    basis = []
    for mask in range(8):
        v = 1
        for bit, root in enumerate(roots):
            if mask & (1 << bit):
                v = v*root % prime
        basis.append(v)
    # The denominator is invertible; a nonzero reduced norm difference
    # therefore proves that the characteristic-zero distance is not one.
    need(288 % prime != 0, 'invertible scale')
    images = {v: tuple(sum(x*r for x, r in zip(axis, basis)) % prime for axis in p)
              for v, p in points.items()}
    target = 288**2
    edges = []
    excluded = exact = 0
    for a, b in combinations(sorted(points), 2):
        dx = images[a][0]-images[b][0]
        dy = images[a][1]-images[b][1]
        if (dx*dx+dy*dy-target) % prime:
            excluded += 1
            continue
        answer = [0]*8
        for axis in range(2):
            d = [x-y for x, y in zip(points[a][axis], points[b][axis])]
            sq = mult(d, d)
            answer = [x+y for x, y in zip(answer, sq)]
        exact += 1
        if answer == [target]+[0]*7:
            edges.append((a, b))
    need(len(edges) == 2582 and excluded+exact == 140185, 'all-pairs result')
    cert = json.loads((ROOT/'certificate.json').read_text())
    expected = json.loads((ROOT/'EXPECTED.json').read_text())
    output = []
    for k, record in enumerate(cert['cases']):
        labels = [v for v in sorted(points) if v not in record['omitted'] and
                  (k == 1 or v not in (1032, 1128))]
        word = record['four_colouring']
        need(len(word) == len(labels) and set(word) <= set('0123'), 'word domain')
        col = dict(zip(labels, word))
        selected = [(a, b) for a, b in edges if a in col and b in col]
        need(all(col[a] != col[b] for a, b in selected), 'monochromatic edge')
        h = sha256(''.join(f'{a} {b}\n' for a, b in selected).encode()).hexdigest()
        need(h == expected['cases'][k]['edge_sha256'], 'independent edge identity')
        output.append({'vertices': len(labels), 'edges': len(selected), 'edge_sha256': h})
    print(json.dumps({'all_checks': True, 'prime': prime, 'roots': roots,
                      'modular_nonunit_exclusions': excluded, 'exact_polynomial_decisions': exact,
                      'whole_edges': len(edges), 'cases': output}, indent=2, sort_keys=True))

if __name__ == '__main__':
    main()
