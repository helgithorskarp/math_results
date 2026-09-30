"""Independent degree-eleven Book Ramsey audit; six-reviewer-1.

CPython 3.11 standard library. No author executable, catalogue, vector pool,
prime, or solver is imported. Adaptive largest-residual degree enumeration
and integer symmetric Schur elimination are the independent proof route.
"""
import argparse
import hashlib
import itertools as it
import json
import math
import random
import sys
from collections import Counter
from fractions import Fraction as Q
from pathlib import Path


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def encoded(value):
    return (json.dumps(value, sort_keys=True, separators=(',', ':')) + '\n').encode()


def edges(n):
    return list(it.combinations(range(n), 2))


def degree_domain(target, fixed=()):
    """Choose the currently largest residual degree, rather than a fixed row."""
    n = len(target)
    require(all(type(d) is int and 0 <= d < n for d in target), 'bad degree target')
    pairs = edges(n)
    index = {e: i for i, e in enumerate(pairs)}
    left = list(target)
    initial = 0
    for a, b in fixed:
        require((a, b) in index and not (initial >> index[a, b] & 1), 'bad fixed edge')
        initial |= 1 << index[a, b]
        left[a] -= 1
        left[b] -= 1
    require(min(left, default=0) >= 0, 'fixed edges exceed target')
    # Fixed vertices must be completely saturated; this rules out duplicate
    # choices of an already-present edge in the adaptive residual problem.
    require(all(left[a] == 0 or left[b] == 0 for a, b in fixed),
            'unsaturated fixed-edge endpoints')
    result = set()
    visits = 0

    def visit(mask):
        nonlocal visits
        visits += 1
        require(visits <= 4000000, 'enumeration operation limit: incomplete')
        active = [i for i, d in enumerate(left) if d]
        if not active:
            require(mask not in result, 'duplicate adaptive terminal')
            result.add(mask)
            return
        if sum(left) & 1 or max(left) >= len(active):
            return
        a = min(active, key=lambda i: (-left[i], i))
        need = left[a]
        options = [i for i in active if i != a]
        left[a] = 0
        for chosen in it.combinations(options, need):
            new = mask
            for b in chosen:
                left[b] -= 1
                new |= 1 << index[tuple(sorted((a, b)))]
            visit(new)
            for b in chosen:
                left[b] += 1
        left[a] = need

    visit(initial)
    for mask in result:
        actual = [0] * n
        for i, (a, b) in enumerate(pairs):
            if mask >> i & 1:
                actual[a] += 1
                actual[b] += 1
        require(actual == list(target), 'wrong terminal degrees')
    return result, visits


def quotient(domain, n, permutations):
    pairs = edges(n)
    index = {e: i for i, e in enumerate(pairs)}
    actions = []
    for p in permutations:
        require(sorted(p) == list(range(n)), 'invalid permutation')
        actions.append(tuple(1 << index[tuple(sorted((p[a], p[b])))] for a, b in pairs))
    remaining = set(domain)
    records = []
    while remaining:
        representative = min(remaining)
        positions = [i for i in range(len(pairs)) if representative >> i & 1]
        orbit = {sum(action[i] for i in positions) for action in actions}
        require(orbit <= remaining, 'orbit overlaps or escapes exact domain')
        require(min(orbit) == representative, 'noncanonical orbit')
        records.append([representative, len(orbit)])
        remaining.difference_update(orbit)
    require(sum(x[1] for x in records) == len(domain), 'incomplete quotient')
    return records, len(actions)


def cores():
    inputs = [([3] * 10, [(0, 1), (0, 2), (0, 3)]),
              ([1] + [3] * 7, []), ([2, 2] + [3] * 6, [])]
    groups = [((0, 1) + front + tail for front in [(2, 3), (3, 2)]
               for tail in it.permutations(range(4, 10))),
              ((0,) + tail for tail in it.permutations(range(1, 8))),
              ((0, 1) + tail for tail in it.permutations(range(2, 8)))]
    records, summaries = [], []
    for family, ((target, fixed), group) in enumerate(zip(inputs, groups)):
        domain, visits = degree_domain(target, fixed)
        current, order = quotient(domain, len(target), group)
        records.append(current)
        digest = hashlib.sha256(''.join(str(x) + '\n' for x in sorted(domain)).encode()).hexdigest()
        summaries.append({'family': family, 'domain_size': len(domain), 'domain_sha256': digest,
                          'adaptive_visits': visits, 'group_order': order,
                          'orbits': len(current), 'records': current})
    return records, summaries


def local(family, mask):
    pairs = edges(10 if family == 0 else 8)
    additions = []
    for i, (a, b) in enumerate(pairs):
        if mask >> i & 1:
            if family == 0:
                if (a, b) != (0, 1):
                    additions.append((a, b))
            else:
                additions.append((a + 2, b + 2))
    if family == 0:
        additions += [(0, 10), (1, 10)]
    else:
        additions += [(0, 1), (0, 10), (1, 10), (0, 2), (1, 2 if family == 1 else 3)]
    red = [0] * 11
    for a, b in additions:
        require(not (red[a] >> b & 1), 'duplicate local edge')
        red[a] |= 1 << b
        red[b] |= 1 << a
    require([r.bit_count() for r in red] == [3] * 10 + [2], 'wrong local degrees')
    return red


def gram(red, t):
    """Solve the page-count equations directly from bitset neighborhoods."""
    blue = [((1 << 11) - 1) ^ r ^ (1 << i) for i, r in enumerate(red)]
    S = [[t[i] if i == j else 0 for j in range(11)] for i in range(11)]
    for a, b in edges(11):
        if red[a] >> b & 1:
            entry = 3 - (1 + (red[a] & red[b]).bit_count()) - (10 - t[a] - t[b])
        else:
            entry = 6 - (blue[a] & blue[b]).bit_count()
        S[a][b] = S[b][a] = entry
    return S


def quadratic(A, w):
    return sum(w[i] * w[j] * A[i][j] for i in range(len(A)) for j in range(len(A)))


def psd_rank(original):
    """Positive integer Schur pivots, or a pulled-back integer negative form."""
    n = len(original)
    require(all(len(r) == n and all(type(x) is int for x in r) for r in original),
            'invalid exact symmetric matrix')
    require(all(original[i][j] == original[j][i] for i in range(n) for j in range(n)),
            'asymmetric matrix')
    A = [r[:] for r in original]
    labels = list(range(n))
    history = []
    previous = 1

    def negative(free):
        w = [Q(0)] * n
        for i, x in free.items():
            w[i] = Q(x)
        for i, pivot, row in reversed(history):
            w[i] = -sum(value * w[j] for j, value in row) / pivot
        denominator = math.lcm(*(x.denominator for x in w))
        vector = [int(x * denominator) for x in w]
        divisor = math.gcd(*vector)
        require(divisor > 0, 'zero negative witness')
        vector = [x // divisor for x in vector]
        if next(x for x in vector if x) < 0:
            vector = [-x for x in vector]
        value = quadratic(original, vector)
        require(value < 0, 'Schur witness fails literal original quadratic form')
        return {'psd': False, 'negative_vector': vector, 'negative_value': value,
                'positive_pivots': len(history)}

    while A:
        for i in range(len(A)):
            if A[i][i] < 0:
                return negative({labels[i]: 1})
        for i in range(len(A)):
            if A[i][i] == 0:
                for j in range(len(A)):
                    if A[i][j]:
                        b, c = A[i][j], A[j][j]
                        return negative({labels[i]: -(abs(c) + 1) * (1 if b > 0 else -1),
                                         labels[j]: 1})
        p = next((i for i in range(len(A)) if A[i][i] > 0), None)
        if p is None:
            require(all(x == 0 for r in A for x in r), 'nonzero zero-diagonal residual')
            return {'psd': True, 'rank': len(history)}
        keep = [i for i in range(len(A)) if i != p]
        pivot = A[p][p]
        history.append((labels[p], pivot, [(labels[i], A[p][i]) for i in keep]))
        B = []
        for i in keep:
            row = []
            for j in keep:
                numerator = pivot * A[i][j] - A[i][p] * A[p][j]
                require(numerator % previous == 0, 'inexact positive Bareiss division')
                row.append(numerator // previous)
            B.append(row)
        A = B
        labels = [labels[i] for i in keep]
        previous = pivot
    return {'psd': True, 'rank': len(history)}


def permutation_det(A):
    n = len(A)
    value = 0
    for p in it.permutations(range(n)):
        term = math.prod(A[i][p[i]] for i in range(n))
        parity = sum(p[i] > p[j] for i in range(n) for j in range(i + 1, n))
        value += -term if parity & 1 else term
    return value


def controls():
    for n, count in [(4, 1), (6, 7), (8, 553)]:
        domain, _ = degree_domain([3] * n, [(0, 1), (0, 2), (0, 3)])
        require(len(domain) == count, 'small cubic control')
    tested = 0
    for entries in it.product([-1, 0, 1], repeat=6):
        A = [[0] * 3 for _ in range(3)]
        for x, (i, j) in zip(entries, [(0, 0), (0, 1), (0, 2), (1, 1), (1, 2), (2, 2)]):
            A[i][j] = A[j][i] = x
        minors = [(len(c), permutation_det([[A[i][j] for j in c] for i in c]))
                  for k in range(1, 4) for c in it.combinations(range(3), k)]
        answer = psd_rank(A)
        require(answer['psd'] == all(d >= 0 for _, d in minors), 'principal-minor PSD disagreement')
        if answer['psd']:
            require(answer['rank'] == max([0] + [k for k, d in minors if d]), 'principal-minor rank disagreement')
        tested += 1
    rejected = 0
    for A in [[[1, 2], [1, 1]], [[1, 2]], [[1.0]], [[True]]]:
        try:
            psd_rank(A)
        except RuntimeError:
            rejected += 1
        else:
            raise RuntimeError('malformed control accepted')
    for z in range(12):
        k = (z - 4) * (z - 5) // 2
        require(-k <= z - 4 <= 1 + k, 'scalar miss bound')
    return {'principal_minor_matrices': tested, 'malformed_matrices_rejected': rejected,
            'normalized_cubic_counts': [1, 7, 553], 'integer_miss_sizes': 12}


def literal_host_control(red, seed):
    """Independent full-host decoding controls, not valid Ramsey witnesses."""
    rng = random.Random(28000 + seed)
    host = [set(j for j in range(11) if r >> j & 1) | {11} for r in red]
    host += [set(range(11))] + [set() for _ in range(10)]
    misses = []
    for b in range(10):
        points = list(range(11))
        rng.shuffle(points)
        miss = set(points[:(seed + 7 * b) % 12])
        misses.append(miss)
        for a in set(range(11)) - miss:
            host[a].add(12 + b)
            host[12 + b].add(a)
    for b, c in edges(10):
        if rng.getrandbits(1):
            host[12 + b].add(12 + c)
            host[12 + c].add(12 + b)
    blue = [set(range(22)) - r - {i} for i, r in enumerate(host)]
    t = [sum(i in m for m in misses) for i in range(11)]
    S = gram(red, t)
    epsilon = {}
    actual = [[sum(i in m and j in m for m in misses) for j in range(11)] for i in range(11)]
    for i, j in edges(11):
        epsilon[i, j] = (3 - len(host[i] & host[j]) if j in host[i]
                         else 6 - len(blue[i] & blue[j]))
        require(S[i][j] - epsilon[i, j] == actual[i][j], 'literal full-host Gram equation')
    F = sum((len(m) - 3) * (len(m) - 4) // 2 for m in misses)
    K = sum((len(m) - 4) * (len(m) - 5) // 2 for m in misses)
    U = sum(epsilon.values())
    UR = sum(x for (i, j), x in epsilon.items() if red[i] >> j & 1)
    triangle = sum((red[i] & red[j]).bit_count() for i, j in edges(11) if red[i] >> j & 1) // 3
    induced = sum(sum(red[i] >> j & 1 for i, j in it.combinations(sorted(m), 2)) for m in misses)
    require(U + F + t[10] == 10, 'first literal budget')
    require(3 * (U + K + triangle) + UR + induced == 22 - 4 * t[10], 'second literal budget')
    require(sum(t) == 40 + F - K, 'literal miss conservation')
    for i in range(11):
        ui = sum(len(m) - 4 for m in misses if i in m)
        require(sum(actual[i]) == 4 * t[i] + ui, 'literal Gram row sum')
        require(len(host[i]) == 11 + red[i].bit_count() - t[i], 'full-degree decoding')


def run(pilot=0):
    checks = controls()
    records, domains = cores()
    pairs = edges(11)
    totals = []
    stream = []
    classified = 0
    witness_max = 0
    psd_survivors = []
    literal_controls = 0
    for family, core_records in enumerate(records):
        for mask, _ in core_records:
            literal_host_control(local(family, mask), literal_controls)
            literal_controls += 1
    checks['literal_full_hosts'] = literal_controls
    checks['literal_A_spines'] = 55 * literal_controls
    for delta in [2, 1, 0]:
        for U in range(3 - delta):
            K = 2 - delta - U
            counts = Counter({k: 0 for k in ['eligible_cores', 'states', 'nonnegative', 'row_pass',
                                             'row_pass_negative', 'row_pass_rank11',
                                             'row_fail_negative', 'row_fail_rank11', 'row_fail_psd_rank10',
                                             'entry_fail_negative', 'entry_fail_rank11', 'entry_fail_psd_rank10',
                                             'unchecked']})
            for family, core_records in enumerate(records):
                for mask, _ in core_records:
                    red = local(family, mask)
                    triangles = sum((red[i] & red[j]).bit_count() for i, j in pairs
                                    if red[i] >> j & 1) // 3
                    if triangles > delta:
                        continue
                    counts['eligible_cores'] += 1
                    eligible = [i for i, (a, b) in enumerate(pairs)
                                if triangles < delta or not (red[a] >> b & 1)]
                    slack_choices = list(it.combinations_with_replacement(eligible, U))
                    placements = ([tuple([i] * 2) for i in range(10)] + list(it.combinations(range(10), 2))
                                  if delta == 2 else [(i,) for i in range(10)] if delta else [()])
                    for placement in placements:
                        t = [4] * 11
                        for i in placement:
                            t[i] += 1
                        S0 = gram(red, t)
                        for slack in slack_choices:
                            S = [r[:] for r in S0]
                            for index in slack:
                                a, b = pairs[index]
                                S[a][b] -= 1
                                S[b][a] -= 1
                            key = (delta, U, K, family, mask, tuple(t), slack)
                            matrix_hash = hashlib.sha256(encoded(S)).hexdigest()
                            stream.append((key, matrix_hash))
                            counts['states'] += 1
                            nonnegative = all(x >= 0 for r in S for x in r)
                            if nonnegative:
                                counts['nonnegative'] += 1
                            u = [sum(r) - 4 * ti for r, ti in zip(S, t)]
                            row_pass = (nonnegative and all(-K <= ui <= ti + K for ui, ti in zip(u, t))
                                        and (K != 0 or all(ui <= 6 - U for ui in u))
                                        and sum(u) == 5 * (6 - U) - 3 * K)
                            if row_pass:
                                counts['row_pass'] += 1
                            if pilot and classified >= pilot:
                                counts['unchecked'] += 1
                                continue
                            classified += 1
                            result = psd_rank(S)
                            prefix = 'entry_fail' if not nonnegative else 'row_pass' if row_pass else 'row_fail'
                            if not result['psd']:
                                counts[prefix + '_negative'] += 1
                                witness_max = max(witness_max, max(map(abs, result['negative_vector'])))
                            elif result['rank'] == 11:
                                counts[prefix + '_rank11'] += 1
                            elif row_pass:
                                psd_survivors.append([list(key), result['rank']])
                            else:
                                counts[prefix + '_psd_rank10'] += 1
            totals.append({'Delta': delta, 'U': U, 'K': K, 'counts': dict(counts)})
    require(not psd_survivors, 'a row-pass PSD rank-at-most-ten survivor: exclusion unproved')
    if not pilot:
        require(classified == len(stream) and all(
            c['counts']['entry_fail_negative'] + c['counts']['row_fail_negative'] +
            c['counts']['row_pass_negative'] == c['counts']['states'] for c in totals),
            'not every candidate has a checked negative form: stronger lemma unproved')
    canonical = hashlib.sha256()
    for record in sorted(stream):
        canonical.update(encoded(record))
    return {'agent': 'six-reviewer-1', 'role': 'independent mathematical reviewer',
            'schema': 'degree11-independent-schur-v1',
            'status': 'PILOT_INCOMPLETE' if pilot else 'COMPLETE', 'controls': checks,
            'domains': domains, 'cases': totals, 'classified_matrices': classified,
            'max_primitive_negative_vector_entry': witness_max,
            'all_state_and_matrix_stream_sha256': canonical.hexdigest(),
            'total': {k: sum(c['counts'][k] for c in totals) for k in totals[0]['counts']},
            'survivors': psd_survivors}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--pilot', type=int, default=0, help='classify only this many matrices; result is INCOMPLETE')
    parser.add_argument('--check', type=Path, help='compare complete canonical stdout with compact expected file')
    args = parser.parse_args()
    require(args.pilot >= 0 and not (args.pilot and args.check), 'bad pilot/check request')
    value = encoded(run(args.pilot))
    if args.check:
        require(args.check.read_bytes() == value, 'canonical expected output mismatch')
    sys.stdout.buffer.write(value)
