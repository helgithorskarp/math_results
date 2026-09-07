"""Independent exact moments, small physical matrices and full-graph controls."""
from collections import Counter
from itertools import combinations
from copy import deepcopy
from math import comb
from functools import lru_cache
import random
import json
import moments
import independent_moments as independent
import independent_baseline
import baseline
import base_model
import model
from extract import extract, clique
from verify import verify, decode


def require(value, message):
    if not value:
        raise ArithmeticError(message)


def dense_rank(rows):
    a = [list(x) for x in rows]
    r = 0
    for j in range(len(a[0])):
        p = next((i for i in range(r, len(a)) if a[i][j]), None)
        if p is None:
            continue
        a[r], a[p] = a[p], a[r]
        for i in range(r+1, len(a)):
            if a[i][j]:
                a[i] = [x ^ y for x, y in zip(a[i], a[r])]
        r += 1
    return r


def exact_checks():
    result = moments.run()
    checks = 0
    bad = tuple(range(10))+tuple(range(14, 24))
    for marked in (1, 2):
        for z in range(2):
            require(independent.row_event(20, 4, 4, 3, marked, z) == result['rows'][str(marked)][z], 'row count differs')
            checks += 1
        for z in range(3):
            require(independent.column_event(23, 4, 5, marked, z, bad) == result['columns'][str(marked)][z], 'column count differs')
            checks += 1
    require(set(moments.spaces(4)) == set(independent.lattice(4)), 'different subspace lattices')
    require(Counter(len(s) for s in moments.spaces(4)) == {1: 1, 2: 15, 4: 35, 8: 15, 16: 1}, 'wrong lattice dimensions')
    raw, overlap = independent_baseline.stage(20, 23, 4, 4, 5, 1, 2)
    old = baseline.compute()
    require(raw-overlap-old['previous_affine_family'] == result['baseline'], 'baseline differs')
    require(overlap == result['old_complement_overlap'], 'overlap differs')
    # The proof uses exactly this pointwise inequality; up to six row types can have three copies.
    for k in range(7):
        require(k-comb(k, 2) <= int(k > 0), 'Bonferroni inequality failed')
    require(result['removed_lower_bound'] == result['first_moment']-result['second_binomial_moment']-overlap, 'wrong lower bound')
    require(result['remaining_upper_bound']+result['removed_lower_bound'] == result['baseline'], 'wrong upper bound')
    return {'marked_count_comparisons': checks, 'subspace_dimension_counts': [1, 15, 35, 15, 1],
            'pointwise_bonferroni_cases': 7, 'moments': result}


@lru_cache(None)
def row_flag(m, r, ac, threshold, marked, z):
    return moments.row_event(m, r, ac, threshold, marked, z)


@lru_cache(None)
def column_flag(n, r, bc, marked, z, bad):
    return moments.column_event(n, r, bc, marked, z, bad)


def predicted(config):
    m, n, r, ac, bc, az, bz, threshold, bad = config
    values = []
    for marked in (1, 2):
        a = [row_flag(m, r, ac, threshold, marked, z) for z in range(az+1)]
        b = [column_flag(n, r, bc, marked, z, bad) for z in range(bz+1)]
        flags = a[0]*sum(b)+sum(a[1:])*b[0]
        multiplier = 2**r-1 if marked == 1 else comb(2**r-1, 2)
        value, remainder = divmod(flags*multiplier, baseline.group_order(r))
        require(remainder == 0, 'nonintegral small flags')
        values.append(value)
    return values


def small_matrices():
    configs = [
        (4, 4, 2, 2, 3, 1, 1, 2, (0, 1, 3, 4)),
        (4, 4, 2, 3, 2, 1, 2, 2, (0, 4)),
        (4, 4, 3, 2, 3, 1, 1, 2, (0, 1, 3, 4)),
        (4, 4, 2, 3, 3, 1, 1, 3, (0, 1, 4)),
        (5, 3, 2, 3, 2, 1, 1, 2, (0, 1, 3)),
        (5, 3, 3, 3, 2, 1, 1, 2, (0, 1, 3)),
        (5, 3, 2, 3, 3, 1, 2, 3, (0, 1, 3)),
        (5, 3, 2, 3, 3, 1, 2, 2, (0, 3)),
    ]
    totals = [[0, 0, 0, 0] for _ in configs]  # family, first moment, second moment, union
    matrices = 0
    for m, n in [(4, 4), (5, 3)]:
        for bits in range(2**(m*n)):
            rows = [tuple((bits >> (i*n+j)) & 1 for j in range(n)) for i in range(m)]
            r = dense_rank(rows)
            matrices += 1
            if r not in (2, 3):
                continue
            columns = list(zip(*rows))
            ra, co = Counter(rows), Counter(columns)
            z1, z2 = ra[(0,)*n], co[(0,)*m]
            if z1 and z2:
                continue
            acmax = max(value for row, value in ra.items() if any(row))
            bcmax = max(value for col, value in co.items() if any(col))
            for index, config in enumerate(configs):
                cm, cn, cr, ac, bc, az, bz, threshold, bad = config
                if (m, n, r) != (cm, cn, cr) or acmax > ac or bcmax > bc or z1 > az or z2 > bz:
                    continue
                # Actual row types and actual physical Hamming weights, no factor labels.
                k = sum(population >= threshold and sum(row) in bad for row, population in ra.items() if any(row))
                totals[index][0] += 1
                totals[index][1] += k
                totals[index][2] += comb(k, 2)
                totals[index][3] += int(k > 0)
    evidence = []
    for config, total in zip(configs, totals):
        m, n, r, ac, bc, az, bz, threshold, bad = config
        require(total[0] == baseline.pair_count(m, n, r, ac, bc, az, bz), 'small baseline differs')
        first, second = predicted(config)
        require([first, second] == total[1:3], 'small physical moment differs')
        require(first-second <= total[3], 'small union bound fails')
        evidence.append({'configuration': config, 'family': total[0], 'first': first, 'second': second, 'union': total[3]})
    return {'exhaustive_binary_matrices': matrices, 'complete_configurations': len(configs), 'evidence': evidence}


def reject(call):
    try:
        call()
    except (ValueError, ArithmeticError):
        return
    raise ArithmeticError('bad input accepted')


def controls():
    rng = random.Random(43201013)
    support = list(range(1, 16))
    low = support+[1, 2, 4, 6, 8, 10, 12, 14]
    high = support+[1, 3, 5, 7, 9, 11, 2, 4]
    a3 = support+[1, 1, 2, 3, 4]
    a4 = support+[1, 1, 1, 2, 3]
    b_multi = support+[4, 4, 4, 8, 8, 8, 12, 12]
    a_two = list(range(1, 15))+[1, 1, 2, 2, 3, 4]
    a_three = list(range(1, 12))+[1, 1, 2, 2, 3, 3, 4, 5, 6]
    cases = [(a3, low, 1), (a4, low, 1), (a3, high, 1), (a4, high, 1),
             (a_two, b_multi, 2), (a_three, b_multi, 3)]
    certificates = basis_changes = corruptions = 0
    histogram = Counter()
    fixture = None
    for a, b, k in cases:
        for trial in range(12):
            data = {'rows': a[:], 'columns': b[:], 'internal_hex': format(rng.getrandbits(443), '0111x')}
            rng.shuffle(data['rows']); rng.shuffle(data['columns'])
            status = model.classify(data)
            require(status['baseline'] and not status['keep'] and len(status['violations']) == k, 'wrong physical branch')
            graph, cert = extract(data)
            require(verify(graph, cert) == 'VERIFIED_PHYSICAL_MONOCHROMATIC_FIVE', 'invalid physical certificate')
            certificates += 1
            histogram[k] += 1
            if fixture is None:
                fixture = {'parameters': data, 'graph': graph, 'certificate': cert}
            # Dense rows reconstruct the filter independently from the graph bytes.
            adj = decode(graph)
            contacts = Counter(tuple(adj[i][j] for j in range(20, 43)) for i in range(20))
            physical_k = sum(pop >= 3 and not 10 <= sum(row) <= 13 for row, pop in contacts.items())
            require(physical_k == k, 'physical type count differs')
            while True:
                basis = [rng.randrange(16) for _ in range(4)]
                if base_model.rank(basis) == 4:
                    break
            def f(x):
                result = 0
                for j in range(4):
                    if (x >> j) & 1:
                        result ^= basis[j]
                return result
            dual = {y: next(z for z in range(16) if all(base_model.dot(f(1 << j), z) == ((y >> j) & 1) for j in range(4))) for y in range(16)}
            changed = {'rows': [f(x) for x in data['rows']], 'columns': [dual[y] for y in data['columns']], 'internal_hex': data['internal_hex']}
            transformed = model.classify(changed)
            require(model.physical(changed) == graph and transformed['baseline'] and not transformed['keep'], 'basis change lost graph')
            require(sorted((v['multiplicity'], v['red_contacts']) for v in transformed['violations']) == sorted((v['multiplicity'], v['red_contacts']) for v in status['violations']), 'basis change altered contacts')
            basis_changes += 1
            badcert = deepcopy(cert)
            badcert['color'] = 'red' if cert['color'] == 'blue' else 'blue'
            reject(lambda: verify(graph, badcert)); corruptions += 1
            u, v = cert['vertices'][:2]
            index = list(combinations(range(43), 2)).index((u, v))
            badgraph = dict(graph, red_hex=format(int(graph['red_hex'], 16) ^ (1 << index), '0226x'))
            reject(lambda: verify(badgraph, cert)); corruptions += 1
    # Both endpoints of the permitted contact interval must stay in the generator.
    boundary = [(10, support+[1, 3, 2, 4, 6, 8, 10, 12]),
                (13, support+[1, 3, 5, 7, 9, 2, 4, 6])]
    for t, b in boundary:
        for a in (a3, a4):
            data = {'rows': a, 'columns': b, 'internal_hex': '0'*111}
            status = model.classify(data)
            require(status == {'baseline': True, 'keep': True, 'violations': []}, 'boundary incorrectly removed')
            require(sum(base_model.dot(1, y) for y in b) == t, 'boundary contacts wrong')
            reject(lambda: extract(data)); corruptions += 1
    # Coordinate map inherited verbatim, checked on the actual new fixture.
    data = fixture['parameters']; basebits = int(model.physical(data)['red_hex'], 16)
    for i, pair in enumerate(base_model.INTERNAL):
        changed = dict(data, internal_hex=format(int(data['internal_hex'], 16) ^ (1 << i), '0111x'))
        delta = int(model.physical(changed)['red_hex'], 16) ^ basebits
        require(delta == 1 << base_model.PAIRS.index(pair), 'wrong internal coordinate')
        require(model.classify(changed) == model.classify(data), 'internal edge affected sieve')
    adj = decode(fixture['graph'])
    for i, x in enumerate(data['rows']):
        for j, y in enumerate(data['columns']):
            require(adj[i][20+j] == bool(sum(((x >> k) & 1)*((y >> k) & 1) for k in range(4)) % 2), 'wrong cross coordinate')
    for bad in [{}, dict(data, extra=1), dict(data, rows=[0]*20), dict(data, internal_hex='f'*111)]:
        reject(lambda: model.classify(bad)); corruptions += 1
    return {'physical_certificates': certificates, 'violation_count_histogram': dict(histogram),
            'basis_changes': basis_changes, 'retained_endpoint_cases': 4,
            'internal_coordinates': 443, 'cross_coordinates': 460,
            'rejected_corruptions_or_out_of_scope': corruptions, 'fixture': fixture}


def primitive_controls():
    comparisons = 0
    pairs = list(combinations(range(5), 2))
    for bits in range(2**10):
        for color in (0, 1):
            rows = [0]*5
            for k, (u, v) in enumerate(pairs):
                if ((bits >> k) & 1) == color:
                    rows[u] |= 1 << v
                    rows[v] |= 1 << u
            for size in range(1, 6):
                found = clique(rows, 31, size)
                literal = any(all((rows[u] >> v) & 1 for u, v in combinations(vs, 2)) for vs in combinations(range(5), size))
                require((found is not None) == literal, 'clique primitive differs')
                if found is not None:
                    require(len(found) == size and all((rows[u] >> v) & 1 for u, v in combinations(found, 2)), 'wrong clique output')
                comparisons += 1
    require(20-3 < 18 and 23-13 == 10, 'physical contact bound arithmetic')
    return {'literal_clique_comparisons': comparisons}


def run():
    return {'status': 'VERIFIED_RANK4_CONTACT_SIEVE', 'exact': exact_checks(),
            'small': small_matrices(), 'physical': controls(), 'primitive': primitive_controls()}


if __name__ == '__main__':
    print(json.dumps(run(), indent=2, sort_keys=True))
