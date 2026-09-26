"""Definition-level checks of four near misses; needs only the standard library."""
import argparse
from collections import Counter
from functools import lru_cache
import hashlib
import importlib.util
from itertools import combinations, product
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
POINTS = tuple(product(range(5), repeat=3))
DOMAIN_SHA256 = '02727db9fb02d60a8597f84329f7376bba2c43422d63241da1c251fde97e4eb2'
INDICES = (1634, 9786, 17600, 19590)


def require(condition, message):
    if not condition:
        raise ValueError(message)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def number(p):
    return 25*p[0] + 5*p[1] + p[2]


@lru_cache(None)
def lines():
    """Two distinct points determine a line; no direction catalogue is imported."""
    return tuple(sorted({tuple(sorted(number(tuple((a+t*(b-a)) % 5
                            for a, b in zip(p, q))) for t in range(5)))
                         for p, q in combinations(POINTS, 2)}))


@lru_cache(None)
def planes():
    normals = [p for p in POINTS if any(p) and next(v for v in p if v) == 1]
    return tuple(tuple(i for i, p in enumerate(POINTS)
                       if sum(a*b for a, b in zip(n, p)) % 5 == h)
                 for n in normals for h in range(5))


def determinant(A):
    a, b, c = A
    return (a[0]*(b[1]*c[2]-b[2]*c[1])
            - a[1]*(b[0]*c[2]-b[2]*c[0])
            + a[2]*(b[0]*c[1]-b[1]*c[0])) % 5


def transform(A, b, p):
    return number(tuple((sum(c*d for c, d in zip(row, POINTS[p]))+h) % 5
                        for row, h in zip(A, b)))


def weight_word(points):
    return ''.join(str(sum(p//5 == i for p in points)) for i in range(25))


def gauge(word):
    for a, b, c in combinations([i for i, n in enumerate(word) if n == '4'], 3):
        # Three quotient points span an affine plane exactly when this is nonzero.
        if determinant(((a//5, a % 5, 1), (b//5, b % 5, 1),
                        (c//5, c % 5, 1))):
            return a, b, c
    raise ValueError('missing gauge triple')


def formula(word):
    """Reconstruct the author's clause order using five-bit word enumeration."""
    require(len(word) == 25 and all(c in '01234' for c in word), 'invalid weights')
    clauses = [[-p-1 for p in line] for line in lines()]
    subsets = [tuple(i for i in range(5) if bits[i])
               for bits in product((0, 1), repeat=5)]
    for i, char in enumerate(word):
        n = int(char)
        for k, sign in ((n+1, -1), (6-n, 1)):
            for subset in sorted(s for s in subsets if len(s) == k):
                clauses.append([sign*(5*i+j+1) for j in subset])
    clauses.extend([[-5*i-1] for i in gauge(word)])
    return clauses


def dimacs(clauses):
    return (f'p cnf 125 {len(clauses)}\n'
            + ''.join(' '.join(map(str, c))+' 0\n' for c in clauses)).encode('ascii')


def falsified(clauses, points):
    chosen = {p+1 for p in points}
    return [i for i, c in enumerate(clauses)
            if not any((v > 0) == (abs(v) in chosen) for v in c)]


def check_quotient(record):
    word = record['weights']
    w = list(map(int, word))
    require(sum(w) == 71, 'wrong total weight')
    planar_points = tuple(product(range(5), repeat=2))
    quotient_lines = {tuple(sorted(5*((p[0]+t*(q[0]-p[0])) % 5)
                                  +(p[1]+t*(q[1]-p[1])) % 5 for t in range(5)))
                      for p, q in combinations(planar_points, 2)}
    require(len(quotient_lines) == 30, 'wrong quotient line count')
    require(all(7 <= sum(w[i] for i in L) <= 16 for L in quotient_lines),
            'quotient plane bounds')
    rows = [sum(w[5*i:5*i+5]) for i in range(5)]
    columns = [sum(w[j::5]) for j in range(5)]
    require([rows, columns] == record['profiles'], 'profile mismatch')
    require(all(w[i] <= 3 and w[5*i] <= 3 for i in range(5)), 'zero-axis bound')
    require(5*w[0] <= rows[0]+columns[0]-7, 'intersection-fiber bound')


def positive70(record):
    """Delete the two-line intersection and explicitly normalize its new gauge."""
    points = set(record['points']) - {record['added_image']}
    require(len(points) == 70, 'wrong 70-point control size')
    require(not any(set(L) <= points for L in lines()), '70-point control has a line')
    word = weight_word(points)
    g = gauge(word)
    holes = [next(z for z in range(5) if 5*i+z not in points) for i in g]
    fits = [(a, b, c) for a, b, c in product(range(5), repeat=3)
            if all((a*(i//5)+b*(i % 5)+c) % 5 == h for i, h in zip(g, holes))]
    require(len(fits) == 1, 'gauge interpolation is not unique')
    a, b, c = fits[0]
    normalized = sorted(5*(p//5)+(p % 5-a*(p//25)-b*((p//5) % 5)-c) % 5
                        for p in points)
    require(not falsified(formula(word), normalized), 'gauged 70-point model rejected')
    return word, normalized


def check_fixture(record, seeds):
    points = record['points']
    require(points == sorted(set(points)) and len(points) == 71
            and all(type(p) is int and 0 <= p < 125 for p in points), 'invalid point list')
    chosen = set(points)
    A, b = record['affine_matrix'], record['affine_offset']
    require(determinant(A) != 0 and len({transform(A, b, p) for p in range(125)}) == 125,
            'singular affine map')
    seed = seeds[record['seed_name']]
    require(len(seed) == len(set(seed)) == 70 and record['added'] not in seed,
            'invalid source construction')
    require(not any(set(L) <= set(seed) for L in lines()), 'source seed is not line-free')
    require(points == sorted(transform(A, b, p) for p in seed+[record['added']]),
            'construction map mismatch')
    require(transform(A, b, record['added']) == record['added_image'], 'added point mismatch')
    full = [list(L) for L in lines() if set(L) <= chosen]
    require(full == record['full_lines'] and len(full) == 2, 'wrong complete-line list')
    require(set(full[0]) & set(full[1]) == {record['added_image']}, 'intersection mismatch')
    require(weight_word(points) == record['weights'], 'fiber occupancies mismatch')
    check_quotient(record)
    require(list(gauge(record['weights'])) == record['gauge'], 'wrong gauge')
    require(all(5*i not in chosen for i in record['gauge']), 'gauge holes are not zero')
    cnf = formula(record['weights'])
    bad = record['removed_clause_indices']
    require(bad == falsified(cnf, points) and len(bad) == 2 and max(bad) < 775,
            'falsified clauses are not exactly the specified two line clauses')
    require(digest(dimacs(cnf)) == record['original_cnf_sha256'], 'formula identity mismatch')
    require(not falsified([c for i, c in enumerate(cnf) if i not in bad], points),
            'two-clause weakening is not satisfied')
    # Each single restoration invalidates this particular assignment.
    # UNSAT of the whole single-omission formula is separately proved by replay.py.
    require(all(falsified([c for i, c in enumerate(cnf) if i != j], points)
                for j in bad), 'a single restoration did not reject the planted assignment')
    word70, _ = positive70(record)
    sizes = Counter(sum(p in chosen for p in H) for H in planes())
    require({str(k): v for k, v in sorted(sizes.items())} == record['plane_histogram'],
            'plane histogram mismatch')
    return {'index': record['index'], 'type': record['type'], 'size': 71,
            'full_lines': 2, 'original_clauses': len(cnf),
            'removed_clause_indices': bad, 'quotient_plane_bounds_pass': True,
            'spatial_plane_range': [min(sizes), max(sizes)],
            'positive70_cnf_sha256': digest(dimacs(formula(word70)))}


def load_fixtures():
    records = json.loads((HERE/'fixtures.json').read_text())
    require(tuple(r['index'] for r in records) == INDICES, 'incomplete or reordered controls')
    seeds = {r['name']: r['points'] for r in json.loads((HERE/'seeds.json').read_text())}
    return records, seeds


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--out', type=Path, required=True)
    parser.add_argument('--author', type=Path, help='Optional decision71 directory for live integration')
    parser.add_argument('--domain', type=Path, help='Optional completely regenerated orbits.json')
    args = parser.parse_args()
    records, seeds = load_fixtures()
    require(len(lines()) == 775 and len(planes()) == 155, 'incorrect geometry counts')
    results = [check_fixture(r, seeds) for r in records]
    if args.domain:
        data = args.domain.read_bytes()
        require(digest(data) == DOMAIN_SHA256, 'unverified domain')
        domain = json.loads(data)
        for r in records:
            require(domain[r['index']]['type'] == r['type']
                    and domain[r['index']]['weights'] == r['weights'], 'wrong catalogue index')
    if args.author:
        spec = importlib.util.spec_from_file_location('audited_point_model', args.author/'point_model.py')
        author = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(author)
        for r in records:
            f, g = author.generate(r['weights'])
            require(f.clauses == formula(r['weights']) and list(g) == r['gauge'],
                    'author formula disagrees')
            try:
                author.decode_and_check(r['weights'], [p+1 for p in r['points']])
            except ValueError as exc:
                require('affine line' in str(exc), 'near miss rejected for an unexpected reason')
            else:
                raise ValueError('author decoder accepted a 71-point near miss')
            word70, points70 = positive70(r)
            f70, _ = author.generate(word70)
            require(not falsified(f70.clauses, points70), 'author rejected positive model')
            require(author.decode_and_check(word70, [p+1 for p in points70]) == points70,
                    'author changed a positive control')
    summary = {'status': 'FOUR_EXPLICIT_TWO_LINE_CONTROLS_VERIFIED', 'fixtures': results,
               'positive70_controls': 4, 'source_seeds': 3,
               'all_71_positive_controls_are_weakened_formulas': True,
               'minimality_proofs_replayed': False, 'global_exact_proof_accepted': False,
               'author_integration_checked': bool(args.author),
               'complete_domain_identity_checked': bool(args.domain),
               'fixtures_sha256': digest((HERE/'fixtures.json').read_bytes())}
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(summary, indent=2)+'\n')
    print(json.dumps(summary, indent=2))


if __name__ == '__main__':
    main()
