"""Independent binary census and literal certificate verifier.

Author: six-books-3, researcher. No generator or predecessor-code imports.
Determinants use modular column elimination, independently cross-checked
by the signed subset recurrence for each nonempty core/budget case.
Negative-form certificates are checked by direct integer multiplication.
"""
from collections import Counter
from itertools import combinations, permutations
from math import gcd, isqrt
from pathlib import Path
import hashlib
import json

HERE = Path(__file__).resolve().parent
PRIOR = HERE.parent / 'book_ramsey_b4_b7_degree11_leaf_reduction/expected.json'
PRIOR_HASH = '84ede53e93669f86db7ab7c512d5732e7fdc44ef95f4c72ff0f5caa8861e8f3f'
KINDS = ('simple', 'parallel_shared', 'parallel_distinct')


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def encoded(value):
    return (json.dumps(value, separators=(',', ':'), sort_keys=True) + '\n').encode()


def mask_hash(masks):
    return hashlib.sha256(''.join(str(x) + '\n' for x in sorted(masks)).encode()).hexdigest()


def binary_domain(n, target, present=(), absent=()):
    pairs = list(combinations(range(n), 2))
    present, absent = set(present), set(absent)
    require(not present & absent and present | absent <= set(pairs), 'bad fixed edges')
    used = [0] * n
    future = [0] * n
    initial = 0
    free = []
    for bit, (a, b) in enumerate(pairs):
        if (a, b) in present:
            used[a] += 1
            used[b] += 1
            initial |= 1 << bit
        elif (a, b) not in absent:
            free.append((bit, a, b))
            future[a] += 1
            future[b] += 1
    require(all(used[i] <= target[i] <= used[i] + future[i] for i in range(n)),
            'impossible initial degrees')
    terminals = []

    def visit(k, mask):
        if k == len(free):
            require(used == target, 'bad binary terminal')
            terminals.append(mask)
            return
        bit, a, b = free[k]
        future[a] -= 1
        future[b] -= 1
        if used[a] + future[a] >= target[a] and used[b] + future[b] >= target[b]:
            visit(k + 1, mask)
        if used[a] < target[a] and used[b] < target[b]:
            used[a] += 1
            used[b] += 1
            if used[a] + future[a] >= target[a] and used[b] + future[b] >= target[b]:
                visit(k + 1, mask | (1 << bit))
            used[a] -= 1
            used[b] -= 1
        future[a] += 1
        future[b] += 1

    visit(0, initial)
    require(len(terminals) == len(set(terminals)), 'duplicate binary terminal')
    return set(terminals)


def normalized_cubic(n):
    return binary_domain(n, [3] * n, ((0, 1), (0, 2), (0, 3)),
                         [(0, j) for j in range(4, n)])


def cover(domain, records, n, point_permutations):
    pairs = list(combinations(range(n), 2))
    index = {edge: bit for bit, edge in enumerate(pairs)}
    actions = [[1 << index[tuple(sorted((points[a], points[b])))] for a, b in pairs]
               for points in point_permutations]
    covered = set()
    previous = -1
    for record in records:
        require(isinstance(record, list) and len(record) == 2, 'malformed orbit record')
        mask, size = record
        require(type(mask) is int and 0 <= mask < (1 << len(pairs)), 'bad orbit mask')
        require(type(size) is int and size > 0 and mask > previous, 'bad orbit order or size')
        previous = mask
        positions = [bit for bit in range(len(pairs)) if mask >> bit & 1]
        orbit = {sum(action[bit] for bit in positions) for action in actions}
        require(mask == min(orbit) and len(orbit) == size, 'noncanonical or incorrect orbit size')
        require(orbit <= domain and not orbit & covered, 'orbit outside domain or overlapping')
        covered.update(orbit)
    require(covered == domain, 'orbit union differs entrywise from binary domain')
    return len(actions)


def core(kind, mask):
    red = [set() for _ in range(11)]
    if kind == 0:
        for bit, (a, b) in enumerate(combinations(range(10), 2)):
            if mask >> bit & 1:
                red[a].add(b)
                red[b].add(a)
        require(red[0] == {1, 2, 3} and all(len(row) == 3 for row in red[:10]),
                'simple suppressed core not normalized cubic')
        red[0].remove(1)
        red[1].remove(0)
        red[0].add(10)
        red[1].add(10)
        red[10] = {0, 1}
    else:
        for a, b in [(0, 1), (0, 10), (1, 10), (0, 2), (1, 2 if kind == 1 else 3)]:
            red[a].add(b)
            red[b].add(a)
        for bit, (a, b) in enumerate(combinations(range(8), 2)):
            if mask >> bit & 1:
                red[a + 2].add(b + 2)
                red[b + 2].add(a + 2)
    require(list(map(len, red)) == [3] * 10 + [2], 'bad reconstructed core degrees')
    require(all(i not in red[i] and all(i in red[j] for j in red[i]) for i in range(11)),
            'nonsimple or asymmetric core')
    return red


def literal_gram(red, t):
    blue = [set(range(11)) - red[i] - {i} for i in range(11)]
    S = [[0] * 11 for _ in range(11)]
    for i in range(11):
        S[i][i] = t[i]
    for i, j in combinations(range(11), 2):
        if j in red[i]:
            # One page is the root; ten outside vertices are available.
            entry = 3 - 1 - len(red[i] & red[j]) - (10 - t[i] - t[j])
        else:
            entry = 6 - len(blue[i] & blue[j])
        S[i][j] = S[j][i] = entry
    return S


def subset_determinant(A, modulus):
    n = len(A)
    options = [[(j, x) for j, x in enumerate(row) if x] for row in A]
    values = [0] * (1 << n)
    values[0] = 1
    for mask in range(1 << n):
        row = mask.bit_count()
        if row == n or values[mask] == 0:
            continue
        for col, entry in options[row]:
            if mask >> col & 1:
                continue
            sign = -1 if (mask >> (col + 1)).bit_count() % 2 else 1
            target = mask | (1 << col)
            values[target] = (values[target] + sign * values[mask] * entry) % modulus
    return values[-1]


def column_determinant(A, prime):
    """Scale and subtract columns over the verified prime field."""
    B = [[entry % prime for entry in row] for row in A]
    determinant = 1
    n = len(B)
    for k in range(n):
        col = next((j for j in range(k, n) if B[k][j] != 0), None)
        if col is None:
            return 0
        if col != k:
            for row in B:
                row[k], row[col] = row[col], row[k]
            determinant = -determinant
        pivot = B[k][k]
        determinant = determinant * pivot % prime
        inverse = pow(pivot, -1, prime)
        normalized = [B[i][k] * inverse % prime for i in range(k + 1, n)]
        for j in range(k + 1, n):
            factor = B[k][j]
            if factor:
                for offset, i in enumerate(range(k + 1, n)):
                    B[i][j] = (B[i][j] - factor * normalized[offset]) % prime
            B[k][j] = 0
    return determinant % prime


def check_certificate(record, S):
    require(isinstance(record, list) and len(record) == 6, 'bad certificate length')
    kind, mask, marked, tag, payload, expected = record
    require(all(type(x) is int for x in (kind, mask, marked, tag)), 'bad certificate key or tag')
    if tag == 0:
        require(type(payload) is int and payload > 1, 'bad determinant modulus')
        require(type(expected) is int and 0 < expected < payload, 'bad determinant residue')
        require(subset_determinant(S, payload) == expected, 'determinant certificate rejected')
    elif tag == 1:
        require(isinstance(payload, list) and len(payload) == 11 and
                all(type(x) is int for x in payload), 'malformed negative vector')
        require(gcd(*payload) == 1 and next((x for x in payload if x), 0) > 0,
                'vector not nonzero primitive normalized integer')
        value = sum(payload[i] * S[i][j] * payload[j] for i in range(11) for j in range(11))
        require(type(expected) is int and value == expected < 0, 'negative-form certificate rejected')
    else:
        raise RuntimeError('unknown certificate tag')


def controls():
    require(len(binary_domain(3, [1, 1, 0])) == 1, 'small binary control failed')
    for n, count in ((4, 1), (6, 7), (8, 553)):
        require(len(normalized_cubic(n)) == count, 'small normalized cubic control failed')
    require(subset_determinant([[0, 1], [1, 0]], 101) == 100, 'determinant sign control')
    require(subset_determinant([[1, 2], [2, 4]], 101) == 0, 'singular determinant control')
    identity = [[int(i == j) for j in range(11)] for i in range(11)]
    check_certificate([0, 0, 1, 0, 101, 1], identity)
    indefinite = [row[:] for row in identity]
    indefinite[0][0] = -1
    check_certificate([0, 0, 1, 1, [1] + [0] * 10, -1], indefinite)
    bad = [([0, 0, 1, 0, 101, 2], identity),
           ([0, 0, 1, 1, [0] * 11, -1], indefinite),
           ([0, 0, 1, 1, [1] + [0] * 10, 1], indefinite),
           ([0, 0, 1, 7, 101, 1], identity)]
    for record, matrix in bad:
        try:
            check_certificate(record, matrix)
        except RuntimeError:
            continue
        raise RuntimeError('forged certificate accepted')


def audit_pages(local, seed):
    full = [set(row) | {11} for row in local] + [set(range(11))] + [set() for _ in range(10)]
    misses = []
    for b in range(10):
        z = 4 if b < 4 else 5
        offset = (seed + 3 * b) % 11
        miss = {(offset + j) % 11 for j in range(z)}
        misses.append(miss)
        for i in set(range(11)) - miss:
            full[i].add(12 + b)
            full[12 + b].add(i)
    for b in range(10):
        for c in ((b + 1) % 10, (b + 5) % 10):
            full[12 + b].add(12 + c)
            full[12 + c].add(12 + b)
    blue = [set(range(22)) - full[i] - {i} for i in range(22)]
    t = [sum(i in row for row in misses) for i in range(11)]
    forced = literal_gram(local, t)
    epsilon = [[0] * 11 for _ in range(11)]
    for i, j in combinations(range(11), 2):
        slack = (3 - len(full[i] & full[j]) if j in full[i]
                 else 6 - len(blue[i] & blue[j]))
        joint = sum(i in row and j in row for row in misses)
        require(joint == forced[i][j] - slack, 'literal saturated-spine formula control failed')
        epsilon[i][j] = epsilon[j][i] = slack
    actual = [[sum(i in row and j in row for row in misses) for j in range(11)]
              for i in range(11)]
    for i in range(11):
        u = sum(len(row) - 4 for row in misses if i in row)
        require(sum(actual[i]) == 4 * t[i] + u and 0 <= u <= min(6, t[i]),
                'literal miss-row identity control failed')
    U = sum(epsilon[i][j] for i, j in combinations(range(11), 2))
    F = sum((len(row) - 3) * (len(row) - 4) // 2 for row in misses)
    K = sum((len(row) - 4) * (len(row) - 5) // 2 for row in misses)
    triangles = sum(len(local[i] & local[j]) for i in range(11) for j in local[i]) // 6
    UR = sum(epsilon[i][j] for i, j in combinations(range(11), 2) if j in local[i])
    Q = sum(sum(j in row for i in row for j in local[i]) // 2 for row in misses)
    require(U + F + t[10] == 10 and 3 * (U + K + triangles) + UR + Q == 22 - 4 * t[10],
            'literal budget control failed')


def baseline():
    raw = (HERE / 'baseline21.rows').read_bytes()
    require(hashlib.sha256(raw).hexdigest() ==
            '4f1dd2bc743590a0553107936656e469db6e7d742db0456d697353ce50aac5ec', 'baseline changed')
    lines = raw.decode().splitlines()
    require(len(lines) == 21 and all(len(row) == 21 and set(row) <= {'0', '1'} for row in lines),
            'malformed baseline rows')
    red = [sum(1 << j for j, entry in enumerate(row) if entry == '1') for row in lines]
    require(all(not (red[i] >> i & 1) for i in range(21)) and
            all((red[i] >> j & 1) == (red[j] >> i & 1) for i in range(21) for j in range(21)),
            'nonsimple baseline')
    blue = [((1 << 21) - 1) ^ red[i] ^ (1 << i) for i in range(21)]
    return {'red_edges': sum(x.bit_count() for x in red) // 2,
            'red_degree_histogram': {str(d): n for d, n in sorted(Counter(x.bit_count() for x in red).items())},
            'red_spine_max': max((red[i] & red[j]).bit_count() for i, j in combinations(range(21), 2)
                                 if red[i] >> j & 1),
            'blue_spine_max': max((blue[i] & blue[j]).bit_count() for i, j in combinations(range(21), 2)
                                  if blue[i] >> j & 1)}


def run():
    controls()
    prior_bytes = PRIOR.read_bytes()
    require(hashlib.sha256(prior_bytes).hexdigest() == PRIOR_HASH, 'prior table changed')
    prior = json.loads(prior_bytes)
    expected = json.loads((HERE / 'expected.json').read_text())
    witness_bytes = (HERE / 'negative_vectors.json').read_bytes()
    orbit_bytes = (HERE / 'parallel_orbits.json').read_bytes()
    require(hashlib.sha256(witness_bytes).hexdigest() == expected['negative_vectors_sha256'],
            'negative vector hash mismatch')
    require(hashlib.sha256(orbit_bytes).hexdigest() == expected['parallel_orbits_sha256'],
            'parallel orbit hash mismatch')
    witness_data, orbit_data = json.loads(witness_bytes), json.loads(orbit_bytes)
    require(witness_data['schema'] == 'degree11-negative-vector-pools-v1' and
            orbit_data['schema'] == 'parallel-residual-orbits-v1', 'unknown input schema')
    records = [[[r['mask'], r['orbit_size']] for r in prior['records']],
               orbit_data['shared'], orbit_data['distinct']]
    simple = normalized_cubic(10)
    points = [(0, 1) + front + tail for front in ((2, 3), (3, 2))
              for tail in permutations(range(4, 10))]
    group = cover(simple, records[0], 10, points)
    require({'normalized_labeled_count': len(simple), 'oriented_cores': len(records[0]),
             'group_size': group, 'domain_sha256': mask_hash(simple), 'input_sha256': PRIOR_HASH}
            == expected['simple_census'], 'simple census summary mismatch')
    for kind, target, prefix in ((1, [1] + [3] * 7, (0,)), (2, [2, 2] + [3] * 6, (0, 1))):
        domain = binary_domain(8, target)
        points = [prefix + tail for tail in permutations(range(len(prefix), 8))]
        group = cover(domain, records[kind], 8, points)
        require({'kind': KINDS[kind], 'labeled_count': len(domain), 'domain_sha256': mask_hash(domain),
                 'group_size': group, 'oriented_cores': len(records[kind])}
                == expected['parallel_censuses'][kind - 1], 'parallel census summary mismatch')
    pools = {}
    core_keys = {(kind, mask) for kind, cases in enumerate(records) for mask, _ in cases}
    for record in witness_data['records']:
        require(isinstance(record, list) and len(record) == 3 and
                all(type(x) is int for x in record[:2]), 'malformed vector-pool key')
        key = tuple(record[:2])
        require(key in core_keys and key not in pools, 'unknown or duplicate pool key')
        vectors = record[2]
        require(isinstance(vectors, list) and vectors, 'empty or malformed pool')
        for vector in vectors:
            require(isinstance(vector, list) and len(vector) == 11 and
                    all(type(x) is int for x in vector), 'malformed pool vector')
            require(gcd(*vector) == 1 and next((x for x in vector if x), 0) > 0,
                    'vector not primitive normalized nonzero integer')
        require(vectors == sorted(vectors) and len(set(map(tuple, vectors))) == len(vectors),
                'unsorted or repeated pool vector')
        pools[key] = vectors
    require(len(pools) == expected['vector_pools'] and
            sum(map(len, pools.values())) == expected['distinct_vectors'], 'pool counts differ')
    used_pools = set()
    pairs = list(combinations(range(11), 2))
    modulus = expected['rank_modulus']
    require(type(modulus) is int and modulus == 2147483647, 'unexpected rank modulus')
    require(modulus % 2 == 1 and
            all(modulus % d for d in range(3, isqrt(modulus) + 1, 2)),
            'rank modulus not prime by complete trial division')
    summaries = []
    audited = set()
    cross_checked = set()
    for delta in (2, 1, 0):
        for U in range(3 - delta):
            K = 2 - delta - U
            counts = Counter({key: 0 for key in ('eligible_core_occurrences', 'column_slack_states',
                                                'nonnegative_gram', 'row_bounds', 'rank_certificates',
                                                'negative_form_certificates')})
            family_counts = []
            for kind, cases in enumerate(records):
                eligible = 0
                for index, (mask, _) in enumerate(cases):
                    red = core(kind, mask)
                    key = (kind, mask)
                    if key not in audited:
                        audit_pages(red, index + kind * 148)
                        audited.add(key)
                    T = sum(len(red[i] & red[j]) for i in range(11) for j in red[i]) // 6
                    if T > delta:
                        continue
                    eligible += 1
                    # Build each slack vector by explicit spine indices. With
                    # two units the first index is at most the second, so
                    # repetitions and every pair of distinct spines occur once.
                    slacks = ([()] if U == 0 else [(i,) for i in range(55)] if U == 1 else
                              [(i, j) for i in range(55) for j in range(i, 55)])
                    for marked_mask in range(1 << 10):
                        size = marked_mask.bit_count()
                        if (delta == 2 and size not in (1, 2) or
                            delta == 1 and size != 1 or delta == 0 and size != 0):
                            continue
                        increment = 2 if delta == 2 and size == 1 else 1
                        t = [4 + increment * (marked_mask >> i & 1) for i in range(11)]
                        S0 = literal_gram(red, t)
                        for selected in slacks:
                            if T == delta and any(pairs[spine][1] in red[pairs[spine][0]]
                                                  for spine in selected):
                                continue
                            counts['column_slack_states'] += 1
                            S = [row[:] for row in S0]
                            for spine in selected:
                                i, j = pairs[spine]
                                S[i][j] -= 1
                                S[j][i] -= 1
                            if any(value < 0 for row in S for value in row):
                                continue
                            counts['nonnegative_gram'] += 1
                            u = [sum(row) - 4 * ti for row, ti in zip(S, t)]
                            if any(value < -K or value > ti + K for value, ti in zip(u, t)):
                                continue
                            if K == 0 and any(value > 6 - U for value in u):
                                continue
                            if sum(u) != 5 * (6 - U) - 3 * K:
                                continue
                            counts['row_bounds'] += 1
                            residue = column_determinant(S, modulus)
                            comparison_key = (delta, U, K, kind, mask)
                            if comparison_key not in cross_checked:
                                require(residue == subset_determinant(S, modulus),
                                        'column/subset determinant cross-check differs')
                                cross_checked.add(comparison_key)
                            if residue != 0:
                                counts['rank_certificates'] += 1
                                continue
                            require(key in pools, 'missing negative-vector pool')
                            witness = next((w for w in pools[key] if
                                            sum(w[i] * S[i][j] * w[j] for i in range(11)
                                                for j in range(11)) < 0), None)
                            require(witness is not None, 'no negative witness for rank-check survivor')
                            used_pools.add(key)
                            counts['negative_form_certificates'] += 1
                counts['eligible_core_occurrences'] += eligible
                family_counts.append(eligible)
            summaries.append({'Delta': delta, 'U': U, 'K': K,
                              'eligible_by_family': family_counts, 'counts': dict(counts)})
    require(used_pools == set(pools) and len(audited) == 177, 'unused pool or incomplete core audit')
    totals = {key: sum(x['counts'][key] for x in summaries) for key in summaries[0]['counts']}
    require(summaries == expected['cases'] and totals == expected['total'], 'case counts differ')
    require(baseline() == expected['baseline'], 'known21 baseline differs')
    require(expected['schema'] == 'degree11-unrestricted-gram-summary-v1', 'unknown summary schema')
    print(encoded(expected).decode(), end='')
    return {'subset_comparison_matrices': len(cross_checked), 'complete_states': totals['column_slack_states']}


if __name__ == '__main__':
    run()
