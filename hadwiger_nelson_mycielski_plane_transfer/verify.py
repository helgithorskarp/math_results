"""Independent, definition-level integer certificate checker. No producer imports."""
import argparse
from collections import defaultdict
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def require(value, message):
    if not value:
        raise ValueError(message)


def graph(x):
    require(type(x) is dict and set(x) == {'vertices', 'edges'}, 'Bad graph fields')
    n = x['vertices']
    require(type(n) is int and n >= 0, 'Bad vertex count')
    require(type(x['edges']) is list, 'Bad edge array')
    seen = set()
    for e in x['edges']:
        require(type(e) is list and len(e) == 2, 'Bad edge row')
        a, b = e
        require(type(a) is int and type(b) is int and 0 <= a < b < n, 'Bad edge labels')
        require((a, b) not in seen, 'Duplicate edge')
        seen.add((a, b))
    require(x['edges'] == [list(e) for e in sorted(seen)], 'Unsorted edges')
    return n, seen


def check_square_certificate(g, cert):
    """Generic sufficient obstruction for any graph; no Mycielski assumption."""
    n, edges = graph(g)
    require(type(cert) is dict and set(cert) == {'walk', 'multiplier', 'faces'}, 'Bad obstruction fields')
    walk, mult, faces = cert['walk'], cert['multiplier'], cert['faces']
    require(type(walk) is list and len(walk) >= 3 and len(walk) % 2 == 1, 'Not an odd walk')
    require(type(mult) is int and mult != 0, 'Bad multiplier')
    require(type(faces) is list and faces, 'Missing faces')
    chain = defaultdict(int)
    def accumulate(vertices, factor):
        require(all(type(a) is int and 0 <= a < n for a in vertices), 'Bad walk label')
        for a, b in zip(vertices, vertices[1:] + vertices[:1]):
            e = (min(a, b), max(a, b))
            require(e in edges, 'Walk uses a nonedge')
            chain[e] += factor if a < b else -factor
    accumulate(walk, -mult)
    for f in faces:
        require(type(f) is list and len(f) == 5, 'Bad face row')
        c, *vertices = f
        require(type(c) is int and c != 0, 'Bad face coefficient')
        accumulate(vertices, c)
    require(all(c == 0 for c in chain.values()), 'Square-chain identity fails')
    return {'vertices': n, 'edges': len(edges), 'odd_walk_length': len(walk),
            'multiplier': mult, 'square_terms': len(faces), 'edge_incidence_checks': len(walk)+4*len(faces)}


def check_case(x):
    require(type(x) is dict and set(x) == {'base', 'layers', 'graph', 'kind', 'certificate'}, 'Bad case fields')
    n, base = graph(x['base'])
    r = x['layers']
    require(type(r) is int and r >= 1, 'Bad layer count')
    m, edges = graph(x['graph'])
    require(m == r*n+1, 'Bad lift order')
    # Inspect each pair using the defining adjacency predicate, independently
    # of the producer's edge-insertion loops.
    for a, b in combinations(range(m), 2):
        if b == r*n:
            wanted = a >= (r-1)*n
        else:
            j, u = divmod(a, n)
            k, v = divmod(b, n)
            wanted = (min(u, v), max(u, v)) in base and (j == k == 0 or k == j+1)
        require(((a, b) in edges) == wanted, 'Wrong lifted adjacency')
    if x['kind'] == 'obstruction':
        report = check_square_certificate(x['graph'], x['certificate'])
    elif x['kind'] == 'polygon_map':
        c = x['certificate']
        require(type(c) is dict and set(c) == {'cycle_order', 'map', 'base_bipartition'}, 'Bad map fields')
        size, word, bip = c['cycle_order'], c['map'], c['base_bipartition']
        require(type(size) is int and size == 2*r+1, 'Wrong polygon order')
        require(type(word) is list and len(word) == m and all(type(v) is int and 0 <= v < size for v in word), 'Bad polygon map')
        require(type(bip) is list and len(bip) == n and all(type(v) is int and v in (0, 1) for v in bip), 'Bad bipartition')
        require(all(bip[a] != bip[b] for a, b in base), 'Improper bipartition')
        require(all((word[a]-word[b]) % size in (1, size-1) for a, b in edges), 'Map does not preserve edges')
        report = {'vertices': m, 'edges': len(edges), 'polygon_order': size,
                  'edge_incidence_checks': len(edges)}
    else:
        raise ValueError('Unknown case kind')
    return {'kind': x['kind'], 'base_vertices': n, 'layers': r, **report}


def verify(x):
    require(type(x) is dict and set(x) == {'schema', 'cases'}, 'Bad document fields')
    require(x['schema'] == 'mycielski-plane-transfer-v1', 'Wrong schema')
    require(type(x['cases']) is list and x['cases'], 'Missing cases')
    return {'cases': [check_case(c) for c in x['cases']]}


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--certificate', type=Path, default=ROOT/'certificate.json')
    p.add_argument('--check-expected', action='store_true')
    args = p.parse_args()
    raw = args.certificate.read_bytes()
    out = verify(json.loads(raw))
    out['certificate_sha256'] = sha256(raw).hexdigest()
    if args.check_expected:
        require(out == json.loads((ROOT/'expected.json').read_text()), 'Expected report differs')
    print(json.dumps(out, sort_keys=True, indent=2))


if __name__ == '__main__':
    main()
