"""Exact unrestricted degree-eleven Gram obstruction certificate generator.

Author: six-books-3, researcher. Python 3.11+ standard library only.
Neighbor-subset census; integer Bareiss and rational congruence discovery.
The separate verifier imports none of this file.
"""
from collections import Counter
from fractions import Fraction
from itertools import combinations, combinations_with_replacement, permutations
from math import gcd, lcm
from pathlib import Path
import argparse
import hashlib
import json

HERE = Path(__file__).resolve().parent
PRIOR = HERE.parent / 'book_ramsey_b4_b7_degree11_leaf_reduction/expected.json'
PRIOR_HASH = '84ede53e93669f86db7ab7c512d5732e7fdc44ef95f4c72ff0f5caa8861e8f3f'
KINDS = ('simple', 'parallel_shared', 'parallel_distinct')
PAIRS8 = list(combinations(range(8), 2))
INDEX8 = {edge: k for k, edge in enumerate(PAIRS8)}


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def encoded(value):
    return (json.dumps(value, separators=(',', ':'), sort_keys=True) + '\n').encode()


def mask_hash(masks):
    return hashlib.sha256(''.join(str(x) + '\n' for x in sorted(masks)).encode()).hexdigest()


def residual_domain(target):
    remaining = list(target)
    answers = []

    def visit(i, mask):
        if i == 8:
            require(not any(remaining), 'bad residual terminal')
            answers.append(mask)
            return
        need = remaining[i]
        options = [j for j in range(i + 1, 8) if remaining[j] > 0]
        for choice in combinations(options, need):
            remaining[i] = 0
            new_mask = mask
            for j in choice:
                remaining[j] -= 1
                new_mask |= 1 << INDEX8[(i, j)]
            positive = sum(d > 0 for d in remaining[i + 1:])
            if all(d <= positive - 1 for d in remaining[i + 1:] if d > 0):
                visit(i + 1, new_mask)
            for j in choice:
                remaining[j] += 1
            remaining[i] = need

    visit(0, 0)
    require(len(answers) == len(set(answers)), 'duplicate residual terminal')
    return sorted(answers)


def orbit_records(domain, prefix):
    actions = []
    for tail in permutations(range(len(prefix), 8)):
        points = prefix + tail
        actions.append([1 << INDEX8[tuple(sorted((points[a], points[b])))]
                        for a, b in PAIRS8])
    unseen = set(domain)
    records = []
    while unseen:
        representative = min(unseen)
        edges = [k for k in range(28) if representative >> k & 1]
        orbit = {sum(action[k] for k in edges) for action in actions}
        require(orbit <= unseen, 'orbit outside domain or intersects earlier orbit')
        unseen.difference_update(orbit)
        records.append([representative, len(orbit)])
    require(sum(size for _, size in records) == len(domain), 'incomplete orbit cover')
    return records


def local_matrix(kind, mask):
    P = [[0] * 11 for _ in range(11)]
    if kind == 0:
        edges = [(a, b) for k, (a, b) in enumerate(combinations(range(10), 2))
                 if mask >> k & 1 and (a, b) != (0, 1)]
        edges += [(0, 10), (1, 10)]
    else:
        edges = [(0, 1), (0, 10), (1, 10), (0, 2), (1, 2 if kind == 1 else 3)]
        edges += [(a + 2, b + 2) for k, (a, b) in enumerate(PAIRS8) if mask >> k & 1]
    for a, b in edges:
        require(not P[a][b], 'duplicate local edge')
        P[a][b] = P[b][a] = 1
    require(list(map(sum, P)) == [3] * 10 + [2], 'wrong local degrees')
    return P


def forced_gram(P, marked):
    t = [4] * 11
    for i in marked:
        t[i] += 2 if len(marked) == 1 else 1
    h = list(map(sum, P))
    common = [[sum(P[i][a] * P[a][j] for a in range(11)) for j in range(11)]
              for i in range(11)]
    S = [[t[i] if i == j else
          (t[i] + t[j] - 8 - common[i][j] if P[i][j]
           else h[i] + h[j] - 3 - common[i][j])
          for j in range(11)] for i in range(11)]
    return t, S


def bareiss(A):
    A = [row[:] for row in A]
    previous = 1
    sign = 1
    for k in range(len(A) - 1):
        if A[k][k] == 0:
            r = next((r for r in range(k + 1, len(A)) if A[r][k]), None)
            if r is None:
                return 0
            A[k], A[r] = A[r], A[k]
            sign = -sign
        pivot = A[k][k]
        for i in range(k + 1, len(A)):
            for j in range(k + 1, len(A)):
                numerator = pivot * A[i][j] - A[i][k] * A[k][j]
                require(numerator % previous == 0, 'inexact Bareiss division')
                A[i][j] = numerator // previous
            A[i][k] = 0
        previous = pivot
    return sign * A[-1][-1]


def primitive(vector):
    scale = lcm(*(x.denominator for x in vector))
    values = [int(x * scale) for x in vector]
    common = gcd(*values)
    require(common > 0, 'zero negative vector')
    values = [x // common for x in values]
    if next(x for x in values if x) < 0:
        values = [-x for x in values]
    return values


def negative_vector(original):
    A = [[Fraction(x) for x in row] for row in original]
    basis = [[Fraction(i == j) for j in range(11)] for i in range(11)]
    for k in range(11):
        if A[k][k] < 0:
            return primitive(basis[k])
        if A[k][k] == 0:
            j = next((j for j in range(k + 1, 11) if A[k][j]), None)
            if j is not None:
                m = (abs(A[j][j]) + 1) / (2 * abs(A[k][j]))
                sign = 1 if A[k][j] > 0 else -1
                return primitive([m * a - sign * b for a, b in zip(basis[k], basis[j])])
            continue
        pivot = A[k][k]
        factors = {i: A[i][k] / pivot for i in range(k + 1, 11)}
        for i in range(k + 1, 11):
            basis[i] = [a - factors[i] * b for a, b in zip(basis[i], basis[k])]
        for i in range(k + 1, 11):
            for j in range(k + 1, 11):
                A[i][j] -= A[i][k] * A[k][j] / pivot
    raise RuntimeError('a positive-semidefinite survivor needs a new argument')


def baseline():
    rows = (HERE / 'baseline21.rows').read_text().splitlines()
    require(len(rows) == 21 and all(len(row) == 21 for row in rows), 'malformed baseline')
    red = [{j for j, value in enumerate(row) if value == '1'} for row in rows]
    require(all(set(row) <= {'0', '1'} for row in rows), 'invalid baseline entry')
    require(all(i not in red[i] for i in range(21)), 'baseline loops')
    require(all((j in red[i]) == (i in red[j]) for i in range(21) for j in range(21)),
            'asymmetric baseline')
    blue = [set(range(21)) - red[i] - {i} for i in range(21)]
    return {'red_edges': sum(map(len, red)) // 2,
            'red_degree_histogram': {str(d): n for d, n in sorted(Counter(map(len, red)).items())},
            'red_spine_max': max(len(red[i] & red[j]) for i, j in combinations(range(21), 2)
                                 if j in red[i]),
            'blue_spine_max': max(len(blue[i] & blue[j]) for i, j in combinations(range(21), 2)
                                  if j in blue[i])}


def run(write):
    require(hashlib.sha256(PRIOR.read_bytes()).hexdigest() == PRIOR_HASH, 'prior table changed')
    prior = json.loads(PRIOR.read_text())
    domains = [residual_domain([1] + [3] * 7), residual_domain([2, 2] + [3] * 6)]
    parallel = [orbit_records(domains[0], (0,)), orbit_records(domains[1], (0, 1))]
    records = [[[r['mask'], r['orbit_size']] for r in prior['records']]] + parallel
    pairs = list(combinations(range(11), 2))
    modulus = 2147483647
    pools = {}
    summaries = []
    for delta in (2, 1, 0):
        for U in range(3 - delta):
            K = 2 - delta - U
            counts = Counter({key: 0 for key in ('eligible_core_occurrences', 'column_slack_states',
                                                'nonnegative_gram', 'row_bounds', 'rank_certificates',
                                                'negative_form_certificates')})
            family_counts = []
            for kind, cases in enumerate(records):
                eligible = 0
                for mask, _ in cases:
                    P = local_matrix(kind, mask)
                    T = sum(P[i][j] * P[i][k] * P[j][k] for i, j, k in combinations(range(11), 3))
                    if T > delta:
                        continue
                    eligible += 1
                    allowed = [spine for spine, (i, j) in enumerate(pairs)
                               if not P[i][j] or T < delta]
                    slacks = list(combinations_with_replacement(allowed, U))
                    choices = ([(i,) for i in range(10)] + list(combinations(range(10), 2))
                               if delta == 2 else [(i,) for i in range(10)] if delta else [()])
                    for marked in choices:
                        t, S0 = forced_gram(P, marked) if delta == 2 else forced_gram(P, ())
                        if delta == 1:
                            t = [4 + int(i in marked) for i in range(11)]
                            h = list(map(sum, P))
                            S0 = [[t[i] if i == j else
                                   (t[i] + t[j] - 8 - sum(P[i][a] * P[a][j] for a in range(11))
                                    if P[i][j] else h[i] + h[j] - 3 -
                                    sum(P[i][a] * P[a][j] for a in range(11)))
                                   for j in range(11)] for i in range(11)]
                        for selected in slacks:
                            counts['column_slack_states'] += 1
                            S = [row[:] for row in S0]
                            for spine in selected:
                                i, j = pairs[spine]
                                S[i][j] -= 1
                                S[j][i] -= 1
                            if any(value < 0 for row in S for value in row):
                                continue
                            counts['nonnegative_gram'] += 1
                            u = [sum(S[i]) - 4 * t[i] for i in range(11)]
                            if any(not -K <= u[i] <= t[i] + K for i in range(11)):
                                continue
                            if K == 0 and any(value > 6 - U for value in u):
                                continue
                            if sum(u) != 5 * (6 - U) - 3 * K:
                                continue
                            counts['row_bounds'] += 1
                            determinant = bareiss(S)
                            if determinant:
                                require(determinant % modulus != 0, 'chosen rank modulus needs replacement')
                                counts['rank_certificates'] += 1
                            else:
                                w = negative_vector(S)
                                value = sum(w[i] * S[i][j] * w[j] for i in range(11) for j in range(11))
                                require(value < 0, 'negative vector failed literal check')
                                pools.setdefault((kind, mask), set()).add(tuple(w))
                                counts['negative_form_certificates'] += 1
                counts['eligible_core_occurrences'] += eligible
                family_counts.append(eligible)
            summaries.append({'Delta': delta, 'U': U, 'K': K,
                              'eligible_by_family': family_counts, 'counts': dict(counts)})
    witnesses = {'schema': 'degree11-negative-vector-pools-v1',
                 'records': [[kind, mask, [list(w) for w in sorted(vectors)]]
                             for (kind, mask), vectors in sorted(pools.items())]}
    orbit = {'schema': 'parallel-residual-orbits-v1', 'shared': parallel[0], 'distinct': parallel[1]}
    totals = {key: sum(x['counts'][key] for x in summaries) for key in summaries[0]['counts']}
    summary = {'schema': 'degree11-unrestricted-gram-summary-v1', 'baseline': baseline(),
               'simple_census': {'normalized_labeled_count': prior['normalized_labeled_count'],
                                 'oriented_cores': len(records[0]), 'group_size': 1440,
                                 'domain_sha256': prior['domain_sha256'], 'input_sha256': PRIOR_HASH},
               'parallel_censuses': [{'kind': KINDS[kind + 1], 'labeled_count': len(domain),
                                     'domain_sha256': mask_hash(domain), 'group_size': group,
                                     'oriented_cores': len(parallel[kind])}
                                    for kind, (domain, group) in enumerate(zip(domains, (5040, 720)))],
               'cases': summaries, 'total': totals, 'rank_modulus': modulus,
               'vector_pools': len(pools), 'distinct_vectors': sum(map(len, pools.values())),
               'negative_vectors_sha256': hashlib.sha256(encoded(witnesses)).hexdigest(),
               'parallel_orbits_sha256': hashlib.sha256(encoded(orbit)).hexdigest()}
    for name, value in [('negative_vectors.json', witnesses), ('parallel_orbits.json', orbit), ('expected.json', summary)]:
        if write:
            (HERE / name).write_bytes(encoded(value))
        else:
            require((HERE / name).read_bytes() == encoded(value), 'reproduction mismatch: ' + name)
    print(encoded(summary).decode(), end='')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write', action='store_true', help='regenerate compact certificate and expected files')
    run(parser.parse_args().write)
