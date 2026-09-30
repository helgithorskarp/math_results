"""Exact generation for the regular-110 neighborhood floor.

Actual author: six-books-3, researcher. CPython 3.11+, standard library.
No solver, floating point, connectivity filter, or host symmetry assumption.
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
PAIR_INDEX = {p: i for i, p in enumerate(PAIRS)}
PERM_BITS = tuple(tuple(1 << PAIR_INDEX[tuple(sorted((p[a], p[b])))]
                        for a, b in PAIRS) for p in permutations(range(6)))
TRIPLES = tuple((0,) + t for t in combinations(range(1, 6), 2))


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def encoded(value):
    return (json.dumps(value, indent=2, sort_keys=True) + '\n').encode()


def rows(mask):
    r = [set() for _ in range(6)]
    for k, (a, b) in enumerate(PAIRS):
        if mask >> k & 1:
            r[a].add(b)
            r[b].add(a)
    return r


def orbit(mask):
    bits = [k for k in range(15) if mask >> k & 1]
    return {sum(p[k] for k in bits) for p in PERM_BITS}


MULTIGRAPHS = {}


def three_edges(degrees):
    if degrees not in MULTIGRAPHS:
        out = []
        for edges in combinations_with_replacement(range(15), 3):
            d = [0] * 6
            for k in edges:
                a, b = PAIRS[k]
                d[a] += 1
                d[b] += 1
            if tuple(d) == degrees:
                out.append(edges)
        MULTIGRAPHS[degrees] = tuple(out)
    return MULTIGRAPHS[degrees]


def primitive(vector):
    scale = lcm(*(x.denominator for x in vector))
    out = [int(x * scale) for x in vector]
    divisor = gcd(*out)
    require(divisor > 0, 'zero vector')
    out = [x // divisor for x in out]
    if next(x for x in out if x) < 0:
        out = [-x for x in out]
    return out


def quadratic(a, vector):
    return sum(a[i][j] * vector[i] * vector[j]
               for i in range(len(a)) for j in range(len(a)))


def negative_vector(original):
    """Track exact symmetric congruence and return an integer negative form."""
    n = len(original)
    a = [[Fraction(x) for x in row] for row in original]
    columns = [[Fraction(i == j) for i in range(n)] for j in range(n)]
    for k in range(n):
        pivot = a[k][k]
        if pivot < 0:
            out = primitive(columns[k])
            require(quadratic(original, out) < 0, 'invalid negative pivot witness')
            return out
        if pivot == 0:
            j = next((j for j in range(k + 1, n) if a[k][j]), None)
            if j is not None:
                cross = a[k][j]
                multiple = -(1 if cross > 0 else -1) * (int(abs(a[j][j]) / (2 * abs(cross))) + 1)
                out = primitive([multiple * x + y for x, y in zip(columns[k], columns[j])])
                require(quadratic(original, out) < 0, 'invalid zero pivot witness')
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


def local_rows(frows, stars):
    r = [set() for _ in range(10)]
    for a in range(6):
        r[4 + a].update(4 + b for b in frows[a])
    for low, k in enumerate(stars, 1):
        for a in PAIRS[k]:
            r[low].add(4 + a)
            r[4 + a].add(low)
    require([len(x) for x in r] == [0, 2, 2, 2, 3, 3, 3, 3, 3, 3],
            'incorrect local degrees')
    return r


def full_gram(r, slack):
    h = list(map(len, r))
    eps = Counter(slack)
    s = [[0] * 10 for _ in range(10)]
    for i in range(10):
        s[i][i] = h[i] + 2
        for j in range(i + 1, 10):
            e = eps[PAIR_INDEX[(i - 4, j - 4)]] if i >= 4 else 0
            v = h[i] + h[j] - (5 if j in r[i] else 2) - len(r[i] & r[j]) - e
            s[i][j] = s[j][i] = v
    require(all(sum(row) == 4 * (h[i] + 2) for i, row in enumerate(s)),
            'full Gram row-sum identity failed')
    return s


def residual_gram(s, triple):
    group = set(triple)
    out = [row[1:] for row in s[1:]]
    for i in range(4, 10):
        for j in range(4, 10):
            if (i - 4 in group) == (j - 4 in group):
                out[i - 1][j - 1] -= 1
    require(all(row[i] == 4 for i, row in enumerate(out)), 'residual diagonal failed')
    require(all(sum(row) == 16 for row in out), 'residual row sum failed')
    return out


def controls():
    counts = Counter()
    for steps in combinations(range(1, 11), 5):
        red = [{(i + sign * step) % 22 for sign in (-1, 1) for step in steps}
               for i in range(22)]
        blue = [set(range(22)) - red[i] - {i} for i in range(22)]
        a, b = sorted(red[0]), sorted(blue[0])
        local = [red[i] & set(a) for i in a]
        h = list(map(len, local))
        miss = [set(a) - red[j] for j in b]
        t = [sum(i in row for row in miss) for i in a]
        require(t == [x + 2 for x in h], 'regular columns failed')
        counts['column_identities'] += 10
        for j, row in zip(b, miss):
            require(len(red[j] & set(b)) == len(row), 'outside degree failed')
            counts['outside_degree_identities'] += 1
        epsilon = [[0] * 10 for _ in range(10)]
        for i, j in combinations(range(10), 2):
            common = len(local[i] & local[j])
            slack = (3 - len(red[a[i]] & red[a[j]]) if a[j] in red[a[i]]
                     else 6 - len(blue[a[i]] & blue[a[j]]))
            epsilon[i][j] = epsilon[j][i] = slack
            forced = h[i] + h[j] - (5 if a[j] in red[a[i]] else 2) - common - slack
            require(forced == sum(a[i] in row and a[j] in row for row in miss),
                    'forced pair identity failed')
            counts['pair_identities'] += 1
        psi = sum((len(row) - 4) * (len(row) - 5) // 2 for row in miss)
        u = sum(epsilon[i][j] for i, j in combinations(range(10), 2))
        require(2 * (u + psi) == -120 + 8 * sum(h) - sum(x * x for x in h),
                'scalar identity failed')
        counts['scalar_budgets'] += 1
        for i in range(10):
            excess = sum(len(row) - 4 for row in miss if a[i] in row)
            neighbor_h = sum(h[j] for j in range(10) if a[j] in local[i])
            require(sum(epsilon[i]) == 3 * h[i] + sum(h) - 24 - neighbor_h - excess,
                    'incident slack identity failed')
            counts['incident_slack_identities'] += 1
        counts['controls'] += 1
    # Exact finite validation of the second, analytic branch.
    pairs = tuple(combinations(range(4), 2))
    counts['bipartite_profiles'] = 0
    for stars in combinations_with_replacement(range(6), 6):
        degrees = [0] * 4
        for k in stars:
            for v in pairs[k]:
                degrees[v] += 1
        if degrees != [3] * 4:
            continue
        low = [set(pairs[k]) for k in stars]
        require(sum(3 for x in low for v in range(4) if v not in x) == 36,
                'mixed incidence demand failed')
        for four in combinations(range(10), 4):
            lows = [x for x in four if x < 6]
            highs = {x - 6 for x in four if x >= 6}
            if any(low[x] & highs for x in lows):
                continue
            if any(low[x] == low[y] for x, y in combinations(lows, 2)):
                continue
            require(len(highs) in (0, 1, 4), 'forbidden row composition')
            require(len(lows) * len(highs) <= 3, 'mixed row contribution exceeds three')
            counts['bipartite_admissible_four_sets'] += 1
        counts['bipartite_profiles'] += 1
    # Baseline red complement of the primary 21-vertex matrix.
    data = (HERE / 'baseline21.rows').read_bytes()
    lines = data.decode().splitlines()
    require(len(lines) == 21 and all(len(x) == 21 and set(x) <= {'0', '1'} for x in lines),
            'bad baseline dimensions')
    red = [{j for j, x in enumerate(row) if x == '1'} for row in lines]
    require(all(i not in red[i] and all((j in red[i]) == (i in red[j]) for j in range(21))
                for i in range(21)), 'bad baseline adjacency')
    blue = [set(range(21)) - red[i] - {i} for i in range(21)]
    require(sum(map(len, red)) == 186, 'wrong baseline edge count')
    require(max(len(red[i] & red[j]) for i in range(21) for j in red[i]) == 3,
            'wrong baseline red cap')
    require(max(len(blue[i] & blue[j]) for i in range(21) for j in blue[i]) == 6,
            'wrong baseline blue cap')
    return dict(sorted(counts.items())), hashlib.sha256(data).hexdigest()


def run():
    control_counts, baseline_sha = controls()
    valid = set()
    for edges in combinations(range(15), 6):
        mask = sum(1 << k for k in edges)
        r = rows(mask)
        if max(map(len, r)) <= 3 and all(len(r[a] & r[b]) <= 1
                for k, (a, b) in enumerate(PAIRS) if mask >> k & 1):
            valid.add(mask)
    uncovered = set(valid)
    reps = []
    while uncovered:
        mask = min(uncovered)
        images = orbit(mask)
        require(images <= valid and images <= uncovered, 'invalid F orbit cover')
        uncovered.difference_update(images)
        reps.append((mask, len(images)))
    counts, weighted = Counter(), Counter()
    records, certificates = [], []
    matrix_hash = hashlib.sha256()
    for mask, orbit_size in reps:
        r = rows(mask)
        deficits = tuple(3 - len(x) for x in r)
        multigraphs = three_edges(deficits)
        stars_records = []
        for stars in multigraphs:
            if any(mask >> k & 1 for k in stars):
                continue
            low_multiplicity = factorial(3)
            for frequency in Counter(stars).values():
                low_multiplicity //= factorial(frequency)
            weight = orbit_size * low_multiplicity
            stars_records.append({'stars': list(stars), 'low_label_multiplicity': low_multiplicity})
            counts['local_cores_after_F_and_S3_normalization'] += 1
            weighted['labeled_local_cores'] += weight
            j = local_rows(r, stars)
            pool = []
            for slack in multigraphs:
                s = full_gram(j, slack)
                for triple in TRIPLES:
                    counts['states'] += 1
                    weighted['states'] += weight
                    residual = residual_gram(s, triple)
                    matrix_hash.update(encoded([mask, stars, slack, triple, residual]))
                    if any(x < 0 for row in s for x in row):
                        status = 'full_negative_entry'
                    elif any(x < 0 for row in residual for x in row):
                        status = 'residual_negative_entry'
                    else:
                        status = 'negative_quadratic_form'
                    # Every matrix has a checked negative form. Incidence
                    # entry tests classify diagnostics, not the obstruction.
                    if not any(quadratic(residual, vector) < 0 for vector in pool):
                        pool.append(negative_vector(residual))
                    counts['negative_forms_checked'] += 1
                    weighted['negative_forms_checked'] += weight
                    counts[status] += 1
                    weighted[status] += weight
            certificates.append({'F_mask': mask, 'stars': list(stars), 'vectors': pool})
        records.append({'F_mask': mask, 'orbit_size': orbit_size, 'deficits': list(deficits),
                        'slack_multigraphs': len(multigraphs), 'cores': stars_records})
    cert_bytes = encoded({'dimension': 9, 'records': certificates})
    vectors = [v for rec in certificates for v in rec['vectors']]
    result = {'agent': 'six-books-3', 'role': 'researcher', 'claim_scope':
              'Every valid ten-regular graph on 22 vertices has at least 13 red edges in every red neighborhood.',
              'F_six_edge_labeled': 5005, 'F_after_necessary_cuts': len(valid),
              'F_orbits': len(reps), 'F_domain_sha256':
              hashlib.sha256(''.join(str(x)+'\n' for x in sorted(valid)).encode()).hexdigest(),
              'records': records, 'normalized_state_counts': dict(sorted(counts.items())),
              'labeled_state_counts': dict(sorted(weighted.items())),
              'state_matrix_sha256': matrix_hash.hexdigest(), 'negative_vector_count': len(vectors),
              'negative_vector_max_abs_entry': max(abs(x) for v in vectors for x in v),
              'negative_vectors_sha256': hashlib.sha256(cert_bytes).hexdigest(),
              'control_counts': control_counts, 'baseline21_rows_sha256': baseline_sha,
              'remaining_local_histograms_n0_n2_n3': [[0,0,10],[0,2,8],[0,4,6],[1,1,8]],
              'regular_red_triangle_interval': [96,110], 'survivors': 0}
    require(counts['states'] == sum(counts[k] for k in
            ['full_negative_entry', 'residual_negative_entry', 'negative_quadratic_form']),
            'incomplete state accounting')
    return result, cert_bytes


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--write-certificates', action='store_true',
                        help='replace the two compact generated certificates')
    args = parser.parse_args()
    result, certificates = run()
    data = encoded(result)
    if args.write_certificates:
        (HERE / 'expected.json').write_bytes(data)
        (HERE / 'negative_vectors.json').write_bytes(certificates)
    else:
        require((HERE / 'expected.json').read_bytes() == data, 'expected summary mismatch')
        require((HERE / 'negative_vectors.json').read_bytes() == certificates,
                'negative-vector certificate mismatch')
    print(data.decode(), end='')


if __name__ == '__main__':
    main()
