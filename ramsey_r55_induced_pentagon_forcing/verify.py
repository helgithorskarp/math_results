"""Verify just the literal five-vertex obstruction; imports no proof code."""
import argparse
import itertools
import json
from pathlib import Path


def verify(data, cert):
    n = data['n']
    if type(n) is not int or n < 5:
        raise ValueError('order')
    e = set()
    for pair in data['edges']:
        if len(pair) != 2 or any(type(x) is not int for x in pair):
            raise ValueError('edge')
        u, v = pair
        if not 0 <= u < v < n or (u, v) in e:
            raise ValueError('edge order/duplicate')
        e.add((u, v))
    q = cert['vertices']
    if len(q) != 5 or len(set(q)) != 5 or any(type(x) is not int or not 0 <= x < n for x in q):
        raise ValueError('five labels')
    reds = [tuple(sorted(p)) for p in itertools.combinations(q, 2) if tuple(sorted(p)) in e]
    if cert['kind'] == 'monochromatic5':
        if cert['color'] not in ('red', 'blue') or len(reds) != (10 if cert['color'] == 'red' else 0):
            raise ValueError('monochromatic claim')
    elif cert['kind'] == 'induced_C5':
        if len(reds) != 5 or any(sum(v in p for p in reds) != 2 for v in q):
            raise ValueError('induced cycle claim')
    else:
        raise ValueError('kind')
    return {'status': 'VERIFIED_PHYSICAL_FIVE_VERTEX_OBSTRUCTION',
            'kind': cert['kind'], 'vertices': q, 'red_pairs': len(reds)}


if __name__ == '__main__':
    p = argparse.ArgumentParser(); p.add_argument('graph', type=Path); p.add_argument('certificate', type=Path)
    a = p.parse_args()
    print(json.dumps(verify(json.loads(a.graph.read_text()), json.loads(a.certificate.read_text())), sort_keys=True, indent=2))
