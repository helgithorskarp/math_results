#!/usr/bin/env python3
"""C3-square action cover and complete primary-variable Ramsey formulas."""
from itertools import combinations, combinations_with_replacement, product
from pathlib import Path
import hashlib
import json

ROOT = Path(__file__).resolve().parent
FORMS = ((1, 0), (0, 1), (1, 1), (1, 2))


def require(ok, message):
    if not ok:
        raise ValueError(message)


def info(path):
    digest = hashlib.sha256()
    with path.open('rb') as stream:
        while chunk := stream.read(1024*1024):
            digest.update(chunk)
    return {'bytes': path.stat().st_size, 'sha256': digest.hexdigest()}


def cases():
    rows = []
    for a in range(11):
        for c in range(5):
            for b in combinations_with_replacement(range(4), 4):
                if a+3*sum(b)+9*c == 43 and all(a+3*x <= 10 for x in b):
                    rows.append({'index': len(rows), 'a': a, 'b': list(b), 'c': c})
    require(len(rows) == 18, 'action count')
    return rows


def action(case):
    """Translations on fixed points, four quotient kernels and regular copies."""
    points = [('fixed', i) for i in range(case['a'])]
    for line, count in enumerate(case['b']):
        for copy in range(count):
            points.extend(('quotient', line, copy, t) for t in range(3))
    for copy in range(case['c']):
        points.extend(('regular', copy, u, v) for u, v in product(range(3), repeat=2))
    require(len(points) == 43 and len(set(points)) == 43, 'vertex count')
    ids = {p: i for i, p in enumerate(points)}
    permutations = []
    for x, y in product(range(3), repeat=2):
        image = []
        for p in points:
            if p[0] == 'fixed':
                q = p
            elif p[0] == 'quotient':
                _, line, copy, t = p
                u, v = FORMS[line]
                q = ('quotient', line, copy, (t+u*x+v*y) % 3)
            else:
                _, copy, u, v = p
                q = ('regular', copy, (u+x) % 3, (v+y) % 3)
            image.append(ids[q])
        permutations.append(image)
    return permutations


def edge_orbits(case):
    permutations = action(case)
    representatives = {}
    for a, b in combinations(range(43), 2):
        representative = min(tuple(sorted((p[a], p[b]))) for p in permutations)
        representatives[a, b] = representative
    names = {p: i+1 for i, p in enumerate(sorted(set(representatives.values())))}
    return {p: names[r] for p, r in representatives.items()}


def ramsey_clauses(ids, vertices=range(43)):
    clauses = set()
    for five in combinations(vertices, 5):
        clause = tuple(sorted({ids[e] for e in combinations(five, 2)}))
        clauses.add(clause)
        clauses.add(tuple(-v for v in reversed(clause)))
    return clauses


def generate(case, path):
    require(case in cases(), 'case outside cover')
    ids = edge_orbits(case)
    clauses = ramsey_clauses(ids)
    ramsey = len(clauses)
    clauses.add((1,))  # Global complementation, with no extra automorphism.
    ordered = sorted(clauses, key=lambda c: (len(c), c))
    nv = max(ids.values())
    with path.open('w') as stream:
        stream.write(f'p cnf {nv} {len(ordered)}\n')
        for clause in ordered:
            stream.write(' '.join(map(str, clause))+' 0\n')
    return dict(info(path), variables=nv, clauses=len(ordered), ramsey_clauses=ramsey)


def classify():
    # Independently enumerate ordered multiplicities by total orbit sizes.
    labeled = set()
    for c in range(5):
        for a in range(44-9*c):
            remaining = 43-9*c-a
            if remaining % 3:
                continue
            total = remaining//3
            for b0 in range(total+1):
                for b1 in range(total-b0+1):
                    for b2 in range(total-b0-b1+1):
                        bs = (b0, b1, b2, total-b0-b1-b2)
                        if all(a+3*x <= 10 for x in bs):
                            labeled.add((a, bs, c))
    # GL(2,3) acts as the full symmetric group on the four projective lines.
    lines = [frozenset((t*u % 3, t*v % 3) for t in range(3)) for u, v in FORMS]
    linear_actions = set()
    matrices = 0
    for a, b, c, d in product(range(3), repeat=4):
        if (a*d-b*c) % 3 == 0:
            continue
        matrices += 1
        permutation = tuple(lines.index(frozenset(((a*x+b*y) % 3, (c*x+d*y) % 3)
                                                   for x, y in line)) for line in lines)
        linear_actions.add(permutation)
    require(matrices == 48 and len(linear_actions) == 24, 'projective action is not S4')
    canonical = set()
    for a, bs, c in labeled:
        transformed = {tuple(bs[p[i]] for i in range(4)) for p in linear_actions}
        require(min(transformed) == tuple(sorted(bs)), 'sorting does not represent the full GL orbit')
        canonical.add((a, min(transformed), c))
    expected = {(r['a'], tuple(r['b']), r['c']) for r in cases()}
    require(canonical == expected, 'independent action cover mismatch')
    reports = []
    for case in cases():
        permutations = action(case)
        require(len({tuple(p) for p in permutations}) == 9, 'action not faithful')
        require(permutations[0] == list(range(43)), 'identity action')
        for i, p in enumerate(permutations):
            require(sorted(p) == list(range(43)), 'not a permutation')
            for j, q in enumerate(permutations):
                x, y = divmod(i, 3)
                u, v = divmod(j, 3)
                require([p[q[t]] for t in range(43)] == permutations[3*((x+u) % 3)+(y+v) % 3],
                        'translation group law')
        fixed = [sum(p[v] == v for v in range(43)) for p in permutations[1:]]
        theoretical = sorted([case['a']+3*b for b in case['b'] for _ in range(2)])
        require(sorted(fixed) == theoretical and max(fixed) <= 10, 'fixed-point count')
        ids = edge_orbits(case)
        sizes = {i: list(ids.values()).count(i) for i in set(ids.values())}
        require(all(n in (1, 3, 9) for n in sizes.values()) and sum(sizes.values()) == 903, 'edge orbits')
        reports.append(dict(case, fixed_points_nonidentity=fixed, edge_orbits=len(sizes),
                            edge_orbit_size_histogram={str(s): list(sizes.values()).count(s) for s in (1, 3, 9)}))
    return {'ordered_multiplicity_types': len(labeled), 'inequivalent_types': len(cases()),
            'invertible_matrices': matrices, 'projective_permutations': len(linear_actions), 'cases': reports}


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--report', type=Path)
    args = parser.parse_args()
    report = classify()
    if args.report:
        args.report.write_text(json.dumps(report, indent=2, sort_keys=True)+'\n')
    print(json.dumps(report, sort_keys=True))
