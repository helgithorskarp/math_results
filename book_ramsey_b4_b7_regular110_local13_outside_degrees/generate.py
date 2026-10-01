"""Exact necessary-state census: a local13 root cannot have a size-six miss row.

Actual author six-books-3, researcher. CPython standard library only.
Congruence witness routine reused from our neighborhood-floor source;
weighted-star recursion adapted from our private positive-codegree work.
"""
from collections import Counter
from fractions import Fraction
from itertools import combinations, combinations_with_replacement, permutations
from math import factorial, gcd, lcm
from pathlib import Path
import argparse
import hashlib
import json

HERE = Path(__file__).resolve().parent
PAIRS = tuple(combinations(range(6), 2))
INDEX = {p: k for k, p in enumerate(PAIRS)}
PERM_BITS = tuple(tuple(1 << INDEX[tuple(sorted((p[i], p[j])))]
                       for i, j in PAIRS) for p in permutations(range(6)))


def need(ok, message):
    if not ok:
        raise RuntimeError(message)


def encoded(value):
    return (json.dumps(value, indent=2, sort_keys=True) + '\n').encode()


def state_bytes(index, edges, matrix):
    return (json.dumps([index, edges, matrix], separators=(',', ':')) + '\n').encode()


def rows(mask):
    out = [set() for _ in range(6)]
    for k, (i, j) in enumerate(PAIRS):
        if mask >> k & 1:
            out[i].add(j)
            out[j].add(i)
    return out


def orbit(mask):
    bits = [k for k in range(15) if mask >> k & 1]
    return {sum(image[k] for k in bits) for image in PERM_BITS}


def local_matrix(mask, stars):
    f = rows(mask)
    local = [{4 + x for x in star} for star in stars]
    local += [{4 + j for j in f[i]} | {l for l, star in enumerate(stars) if i in star}
              for i in range(6)]
    h = list(map(len, local))
    need(h == [2] * 4 + [3] * 6, 'wrong local degree sequence')
    return [[h[i] + 2 if i == j else h[i] + h[j] -
             (5 if j in local[i] else 2) - len(local[i] & local[j])
             for j in range(10)] for i in range(10)]


def core_census():
    domain = set()
    for selected in combinations(range(15), 5):
        mask = sum(1 << k for k in selected)
        f = rows(mask)
        if max(map(len, f)) <= 3 and all(len(f[i] & f[j]) <= 1
                                        for i, j in PAIRS if j in f[i]):
            domain.add(mask)
    unseen = set(domain)
    records = []
    while unseen:
        mask = min(unseen)
        images = orbit(mask)
        need(images <= unseen, 'F orbit cover overlaps or omits an eligible graph')
        unseen -= images
        f = rows(mask)
        target = [3 - len(row) for row in f]
        nonedges = [p for p in PAIRS if p[1] not in f[p[0]]]
        profiles = []
        for stars in combinations_with_replacement(nonedges, 4):
            if [sum(i in star for star in stars) for i in range(6)] != target:
                continue
            full = local_matrix(mask, stars)
            if any(x < 0 for row in full for x in row):
                continue
            weight = factorial(4)
            for amount in Counter(stars).values():
                weight //= factorial(amount)
            compatible = all(full[i][j] >= 1 for i, j in combinations(range(4, 10), 2))
            profiles.append({'stars': [list(x) for x in stars],
                             'ordered_low_multiplicity': weight,
                             'all_cubic_row_compatible': compatible})
        records.append({'F_mask': mask, 'orbit_size': len(images),
                        'lambda': target, 'profiles': profiles})
    return domain, records


def cases(catalog):
    for rec in catalog:
        for profile in rec['profiles']:
            if profile['all_cubic_row_compatible']:
                yield {'kind': 'zero_low', 'F_mask': rec['F_mask'],
                       'stars': profile['stars'], 'row': list(range(4, 10))}
    for kind, stars, f, row in [
        ('three_low', [(0, 1), (0, 2), (1, 2), (3, 5)],
         [(0, 3), (1, 4), (2, 5), (3, 4), (4, 5)], [0, 1, 2, 7, 8, 9]),
        ('four_low_cross_cycle', [(0, 2), (0, 3), (1, 2), (1, 3)],
         [(0, 4), (1, 4), (2, 5), (3, 5), (4, 5)], [0, 1, 2, 3, 8, 9]),
        ('four_low_within_pairs', [(0, 1), (1, 2), (2, 3), (0, 3)],
         [(0, 4), (1, 4), (2, 5), (3, 5), (4, 5)], [0, 1, 2, 3, 8, 9])]:
        yield {'kind': kind, 'F_mask': sum(1 << INDEX[e] for e in f),
               'stars': [list(x) for x in stars], 'row': row}


def base_and_degrees(case):
    full = local_matrix(case['F_mask'], case['stars'])
    a = [int(i in case['row']) for i in range(10)]
    base = [[full[i][j] - a[i] * a[j] for j in range(10)] for i in range(10)]
    lam = [3 - len(x) for x in rows(case['F_mask'])]
    degrees = [2 - 2 * a[i] for i in range(4)] + [2 + lam[i] - 2 * a[4 + i] for i in range(6)]
    need(all(x >= 0 for r in base for x in r) and min(degrees) >= 0,
         'invalid distinguished-row normalization')
    need([sum(r) - 4 * r[i] for i, r in enumerate(base)] == degrees,
         'incident slack bridge failed')
    need(sum(degrees) == 16, 'wrong total slack degree')
    return base, degrees


def weighted_stars(degrees, capacities):
    """Decide a vertex's entire remaining star before processing the next."""
    remaining = list(degrees)
    edges = []

    def visit():
        i = next((i for i, d in enumerate(remaining) if d), None)
        if i is None:
            yield tuple(edges)
            return
        amount = remaining[i]
        neighbors = [j for j in range(i + 1, len(degrees))
                     if remaining[j] and capacities[i][j] > 0]
        if sum(min(remaining[j], capacities[i][j]) for j in neighbors) < amount:
            return
        remaining[i] = 0

        def distribute(k, left):
            if k == len(neighbors):
                if left == 0:
                    yield from visit()
                return
            j = neighbors[k]
            future = sum(min(remaining[v], capacities[i][v]) for v in neighbors[k + 1:])
            for weight in range(max(0, left - future), min(left, remaining[j], capacities[i][j]) + 1):
                remaining[j] -= weight
                if weight:
                    edges.append((i, j, weight))
                yield from distribute(k + 1, left - weight)
                if weight:
                    edges.pop()
                remaining[j] += weight
        yield from distribute(0, amount)
        remaining[i] = amount
    yield from visit()


def residual(base, edges):
    out = [r[:] for r in base]
    for i, j, w in edges:
        out[i][j] -= w
        out[j][i] -= w
    need(all(x >= 0 for r in out for x in r), 'negative residual entry')
    need(all(sum(r) == 4 * r[i] for i, r in enumerate(out)), 'residual row sum failed')
    return out


def primitive(vector):
    scale = lcm(*(x.denominator for x in vector))
    out = [int(x * scale) for x in vector]
    divisor = gcd(*out)
    need(divisor > 0, 'zero vector')
    out = [x // divisor for x in out]
    if next(x for x in out if x) < 0:
        out = [-x for x in out]
    return out


def quadratic(a, vector):
    return sum(a[i][j] * vector[i] * vector[j]
               for i in range(len(a)) for j in range(len(a)))


def negative_vector(original):
    n = len(original)
    a = [[Fraction(x) for x in row] for row in original]
    columns = [[Fraction(i == j) for i in range(n)] for j in range(n)]
    for k in range(n):
        pivot = a[k][k]
        if pivot < 0:
            out = primitive(columns[k])
            need(quadratic(original, out) < 0, 'invalid negative pivot witness')
            return out
        if pivot == 0:
            j = next((j for j in range(k + 1, n) if a[k][j]), None)
            if j is not None:
                cross = a[k][j]
                multiple = -(1 if cross > 0 else -1) * (int(abs(a[j][j]) / (2 * abs(cross))) + 1)
                out = primitive([multiple * x + y for x, y in zip(columns[k], columns[j])])
                need(quadratic(original, out) < 0, 'invalid zero pivot witness')
                return out
            continue
        multipliers = {j: a[k][j] / pivot for j in range(k + 1, n)}
        for j, multiplier in multipliers.items():
            columns[j] = [x - multiplier * y for x, y in zip(columns[j], columns[k])]
        for i in range(k + 1, n):
            for j in range(i, n):
                a[i][j] -= a[k][i] * multipliers[j]
                a[j][i] = a[i][j]
    raise RuntimeError('unexpected positive semidefinite survivor')


def run():
    domain, catalog = core_census()
    records, certs = [], []
    totals = Counter()
    whole_hash = hashlib.sha256()
    for index, case in enumerate(cases(catalog)):
        base, degrees = base_and_degrees(case)
        states = sorted(weighted_stars(degrees, base))
        need(len(states) == len(set(states)), 'duplicate slack state')
        pool = []
        digest = hashlib.sha256()
        for edges in states:
            matrix = residual(base, edges)
            data = state_bytes(index, edges, matrix)
            digest.update(data)
            whole_hash.update(data)
            if not any(quadratic(matrix, v) < 0 for v in pool):
                pool.append(negative_vector(matrix))
            need(any(quadratic(matrix, v) < 0 for v in pool), 'uncovered residual matrix')
        records.append(dict(case, index=index, slack_degrees=degrees, states=len(states),
                            state_matrix_sha256=digest.hexdigest(), vectors=len(pool)))
        certs.append({'index': index, 'vectors': pool})
        totals[case['kind']] += len(states)
    cert_bytes = encoded({'dimension': 10, 'records': certs})
    vectors = [v for r in certs for v in r['vectors']]
    result = {'agent': 'six-books-3', 'role': 'researcher',
              'claim_scope': 'A ten-regular valid 22-vertex host with local degrees 2^4,3^6 has no size-six miss row.',
              'five_edge_F_subsets': 3003, 'eligible_labeled_F': len(domain),
              'F_domain_sha256': hashlib.sha256(''.join(str(x) + '\n' for x in sorted(domain)).encode()).hexdigest(),
              'F_orbits': len(catalog), 'catalog': catalog,
              'normalized_profiles': sum(len(r['profiles']) for r in catalog),
              'labeled_local_cores': sum(r['orbit_size'] * sum(p['ordered_low_multiplicity'] for p in r['profiles']) for r in catalog),
              'cases': records, 'selected_configurations': len(records),
              'states_by_case_kind': dict(sorted(totals.items())), 'states': sum(totals.values()),
              'negative_forms': sum(totals.values()), 'state_matrix_sha256': whole_hash.hexdigest(),
              'negative_vectors': len(vectors),
              'negative_vector_max_abs_entry': max(abs(x) for v in vectors for x in v),
              'negative_vectors_sha256': hashlib.sha256(cert_bytes).hexdigest(),
              'survivors': 0}
    return result, cert_bytes


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--write-certificates', action='store_true')
    args = parser.parse_args()
    result, certs = run()
    data = encoded(result)
    if args.write_certificates:
        (HERE / 'expected.json').write_bytes(data)
        (HERE / 'negative_vectors.json').write_bytes(certs)
    else:
        need((HERE / 'expected.json').read_bytes() == data, 'expected summary mismatch')
        need((HERE / 'negative_vectors.json').read_bytes() == certs, 'certificate mismatch')
    print(json.dumps({k: v for k, v in result.items() if k not in ('catalog', 'cases')}, sort_keys=True))


if __name__ == '__main__':
    main()
