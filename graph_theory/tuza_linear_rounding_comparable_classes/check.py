"""Exact replay and definition-level checks, using only the standard library.

This is an author audit, not independent peer review or formal verification.
The finite output does not determine the universal existence threshold.
"""
from collections import Counter
from copy import deepcopy
from fractions import Fraction as Q
from itertools import combinations, combinations_with_replacement
from math import comb, isqrt
from pathlib import Path
import hashlib
import json
import random

import switching as S


def require(ok, message):
    if not ok:
        raise ValueError(message)


def pair(a, b):
    return (a, b) if a <= b else (b, a)


def pairs(row):
    return [pair(row[i], row[j]) for i in range(len(row)) for j in range(i + 1, len(row))]


def digest(value):
    return hashlib.sha256(json.dumps(value, separators=(',', ':'), sort_keys=True).encode()).hexdigest()


def reconstruct_initial(sizes, counts):
    classes, start = [], 0
    for size in sizes:
        classes.append(list(range(start, start + size)))
        start += size
    rows, patterns = [], []
    for p, m in sorted(counts.items()):
        # Generate the consecutive cyclic role stream separately in every class.
        streams = {i: [classes[i][j % sizes[i]] for j in range(m * p.count(i))] for i in set(p)}
        cursor = Counter()
        for _ in range(m):
            row = []
            for i in p:
                row.append(streams[i][cursor[i]])
                cursor[i] += 1
            rows.append(row)
            patterns.append(p)
    return rows, patterns


def check_roles(rows, patterns, sizes, counts, support):
    parent = [i for i, size in enumerate(sizes) for _ in range(size)]
    require(len(rows) == len(patterns) == sum(counts.values()), 'wrong component number')
    actual_counts, role_counts = Counter(patterns), Counter()
    require(actual_counts == Counter(counts), 'wrong type counts')
    for row, p in zip(rows, patterns):
        require(len(row) == len(p) and len(set(row)) == len(row), 'nonsimple component')
        require(all(type(v) is int and 0 <= v < len(parent) for v in row), 'invalid vertex')
        require(tuple(parent[v] for v in row) == p, 'wrong vertex type')
        require(set(pairs(p)) <= set(support), 'unsupported component')
        for v in row:
            role_counts[p, v] += 1
    offset = 0
    for i, size in enumerate(sizes):
        for p, m in counts.items():
            q, r = divmod(m * p.count(i), size)
            for local in range(size):
                require(role_counts[p, offset + local] == q + int(local < r), 'unbalanced vertex-pattern roles')
        offset += size
    return role_counts


def replay_sparse(sizes, counts, support, certificate):
    rows, patterns = reconstruct_initial(sizes, counts)
    initial_roles = check_roles(rows, patterns, sizes, counts, support)
    multiplicity = Counter(e for row in rows for e in pairs(row))
    degrees = Counter(v for e, m in multiplicity.items() for v in e for _ in range(m))
    D = max(degrees.values(), default=0)
    require(certificate['maximum_degree'] == D, 'incorrect degree bound')
    margins = []
    for p, m in counts.items():
        r = max(initial_roles[p, v] for v in range(sum(sizes)))
        for i in set(p):
            margin = p.count(i) * m - (4 * D + 5) * r
            require(margin > 0, 'uncertified sparse-switch instance')
            margins.append(margin)
    excess = sum(max(value - 1, 0) for value in multiplicity.values())
    require(excess == certificate['initial_excess'], 'incorrect initial excess')
    first_excess = excess
    for cid, pos, did, slot in certificate['trace']:
        require(0 <= cid < len(rows) and 0 <= did < len(rows) and cid != did, 'invalid component ids')
        p = patterns[cid]
        require(patterns[did] == p, 'switch changes pattern')
        require(0 <= pos < len(p) and 0 <= slot < len(p) and p[pos] == p[slot], 'switch changes role type')
        old = [rows[cid].copy(), rows[did].copy()]
        new = [old[0].copy(), old[1].copy()]
        new[0][pos], new[1][slot] = new[1][slot], new[0][pos]
        require(all(len(set(row)) == len(row) for row in new), 'switch introduces repeated vertex')
        fresh = ([pair(new[0][pos], v) for j, v in enumerate(new[0]) if j != pos] +
                 [pair(new[1][slot], v) for j, v in enumerate(new[1]) if j != slot])
        require(len(fresh) == len(set(fresh)) and all(multiplicity[e] == 0 for e in fresh),
                'switch creates old or repeated pair')
        affected = set(e for row in old + new for e in pairs(row))
        before = sum(max(multiplicity[e] - 1, 0) for e in affected)
        for row in old:
            for e in pairs(row):
                multiplicity[e] -= 1
        for row in new:
            for e in pairs(row):
                multiplicity[e] += 1
        after = sum(max(multiplicity[e] - 1, 0) for e in affected)
        require(after < before, 'conflict statistic did not decrease')
        excess += after - before
        rows[cid], rows[did] = new
    require(excess == 0 and all(value <= 1 for value in multiplicity.values()), 'unrepaired pair conflict')
    literal = Counter(e for row in rows for e in pairs(row))
    require(all(value == 1 for value in literal.values()), 'final edge family not simple')
    require({e: z for e, z in multiplicity.items() if z} == dict(literal), 'replay count state mismatch')
    require(rows == certificate['components'] and patterns == certificate['patterns'], 'replay differs from producer')
    require(check_roles(rows, patterns, sizes, counts, support) == initial_roles, 'roles changed')
    return {
        'vertices': sum(sizes), 'patterns': len(counts), 'components': len(rows),
        'edges': len(literal), 'initial_excess': first_excess,
        'replayed_switches': len(certificate['trace']), 'maximum_degree': D,
        'minimum_candidate_margin': min(margins),
        'components_sha256': digest(rows), 'trace_sha256': digest(certificate['trace']),
    }, set(literal)


def check_degrees(edges, left, forbidden, right=None):
    degree = list(left) + ([] if right is None else list(right))
    require(len(edges) == len(set(edges)), 'repeated realization edge')
    require(all(0 <= a < b < len(degree) for a, b in edges), 'invalid realization edge')
    require(not (set(edges) & set(forbidden)), 'forbidden edge used')
    if right is not None:
        require(all(a < len(left) <= b for a, b in edges), 'wrong bipartite parts')
    actual = Counter(v for e in edges for v in e)
    require([actual[i] for i in range(len(degree))] == degree, 'wrong realized degrees')


def verify_truncation(sizes, support, z, alpha, certificate):
    d, N = len(sizes), sum(sizes)
    M = comb(d + 2, 3) + comb(d + 1, 2)
    lam, B = 8 * M / alpha, M * (6 / alpha + 2)
    require(certificate['M'] == M and certificate['lambda'] == lam and certificate['B'] == B, 'wrong constants')
    U = certificate['U']
    require(U-1 < lam+B <= U and N >= 4*lam, 'wrong truncation regime')
    capacity = {e: (sizes[e[0]] * (sizes[e[0]]-1)//2 if e[0] == e[1]
                    else sizes[e[0]]*sizes[e[1]]) for e in support}
    load = Counter()
    for p, value in z.items():
        require(value >= 0 and set(pairs(p)) <= set(support), 'unsupported profile')
        for e in pairs(p):
            load[e] += value
    require(all(load[e] == capacity[e] for e in support), 'profile capacity mismatch')
    m = certificate['counts']
    require(set(m) == set(z), 'missing pattern count')
    for p, value in z.items():
        scaled = (1-lam/N)*value
        if scaled < N:
            require(m[p] == 0, 'tiny coordinate was retained')
        else:
            require(type(m[p]) is int and m[p] <= scaled < m[p]+1 and m[p] >= N,
                    'incorrect retained coordinate')
        require(0 <= scaled-m[p] < N, 'linear cutoff loss failure')
    target = Counter()
    for p, count in m.items():
        for e in pairs(p):
            target[e] += count
    segments, type_sums = 0, {}
    for i, rows in enumerate(certificate['blocks']):
        require(sizes[i] >= alpha*N, 'class too small')
        end, total_roles, deficit_sums = 0, Counter(), Counter()
        for row in rows:
            require(row['start'] == end < row['stop'] <= sizes[i], 'compressed interval gap')
            length = row['stop'] - end
            end = row['stop']
            actual = Counter()
            require(set(row['roles']) == {p for p in m if m[p] and i in p}, 'role support mismatch')
            for p, role in row['roles'].items():
                require(type(role) is int and role >= 0, 'noninteger role')
                require(abs(Q(role) - Q(m[p]*p.count(i), sizes[i])) < 1, 'roles not balanced')
                total_roles[p] += length*role
                chosen = p.index(i)
                for j in range(len(p)):
                    if j != chosen:
                        actual[pair(i, p[j])] += role
            require(dict(actual) == row['degree'], 'local role incidence mismatch')
            require(set(row['deficit']) == {e for e in support if i in e}, 'deficit support mismatch')
            for e, value in row['deficit'].items():
                pdeg = sizes[i]-1 if e == (i, i) else sizes[e[1] if e[0] == i else e[0]]
                require(value == pdeg-actual[e] and 2*M <= value <= U, 'deficit bound failure')
                require((1-lam/N)*pdeg-B <= actual[e] <= (1-lam/N)*pdeg+2*M, 'degree estimate failure')
                deficit_sums[e] += length*value
            segments += 1
        require(end == sizes[i], 'incomplete compressed partition')
        require(all(total_roles[p] == m[p]*p.count(i) for p in m), 'wrong total roles')
        for e, value in deficit_sums.items():
            factor = 2 if e == (i, i) else 1
            require(value == factor*(capacity[e]-target[e]), 'global deficit identity failure')
            if factor == 2:
                require(value % 2 == 0, 'internal parity failure')
            type_sums[i, e] = value
    for i, j in support:
        if i != j:
            require(type_sums[i, (i, j)] == type_sums[j, (i, j)], 'cross-pair imbalance')
    return segments


def main():
    fixture = json.loads(Path(__file__).with_name('FIXTURES.json').read_text())
    sparse_results, total_switches = [], 0
    negative_fixture = integrated = None
    for entry in fixture['sparse_instances']:
        sizes = entry['sizes']
        d, N = len(sizes), sum(sizes)
        support = {(i, i) for i in entry['clique_types']} | {tuple(e) for e in entry['cross_pairs']}
        ts = [t for t in combinations_with_replacement(range(d), 3) if set(pairs(t)) <= support]
        counts = {p: N for p in ts + sorted(support)}
        certificate = S.sparse_pack(sizes, counts)
        result, used = replay_sparse(sizes, counts, support, certificate)
        result['name'] = entry['name']
        sparse_results.append(result)
        total_switches += result['replayed_switches']
        if negative_fixture is None:
            negative_fixture = (sizes, counts, support, certificate)
        if entry['name'] == 'balanced_two_cliques':
            integrated = (sizes, support, used)

    rng = random.Random(fixture['degree_seed'])
    degree_cases, augmentations = 0, Counter()
    degree_fixture = None
    for U in range(1, 5):
        for radius in range(3):
            D = 2*radius
            n = 8*(U+1)*(D+U+1)+12
            n += n % 2
            forbidden = {pair(v, (v+s) % n) for v in range(n) for s in range(1, radius+1)}
            ds = [rng.randint(1, U) for _ in range(n)]
            if sum(ds) % 2:
                j = next((i for i, value in enumerate(ds) if value < U), None)
                if j is None:
                    ds[0] -= 1
                else:
                    ds[j] += 1
            result, stats = S.avoid_degree_lists(ds, forbidden)
            check_degrees(result, ds, forbidden)
            augmentations.update(stats)
            degree_cases += 1
            if forbidden:
                degree_fixture = (result, ds, forbidden)
            nr = n + int(U > 1)
            left = [U] * n
            q, r = divmod(sum(left), nr)
            right = [q+int(i<r) for i in range(nr)]
            blocked = {(a, n+(a+s) % nr) for a in range(n) for s in range(D)}
            result, stats = S.avoid_degree_lists(left, blocked, right)
            check_degrees(result, left, blocked, right)
            augmentations.update(stats)
            degree_cases += 1
    result, stats = S.avoid_degree_lists([2]*130, set())
    check_degrees(result, [2]*130, set())
    require(stats.get('single_vertex_augmentations', 0) > 0, 'single-deficiency branch untested')
    augmentations.update(stats)
    degree_cases += 1

    # Compose the two lemmas on one literal host, with degree two in each type pair.
    sizes, support, used = integrated
    offsets = [0, sizes[0]]
    remainder = set()
    for i, j in sorted(support):
        if i == j:
            forbidden = {(a-offsets[i], b-offsets[i]) for a, b in used
                         if offsets[i] <= a < b < offsets[i]+sizes[i]}
            result, stats = S.avoid_degree_lists([2]*sizes[i], forbidden)
            check_degrees(result, [2]*sizes[i], forbidden)
            remainder.update((a+offsets[i], b+offsets[i]) for a, b in result)
        else:
            forbidden = {(a-offsets[i], sizes[i]+b-offsets[j]) for a, b in used
                         if offsets[i] <= a < offsets[i]+sizes[i] and offsets[j] <= b < offsets[j]+sizes[j]}
            result, stats = S.avoid_degree_lists([2]*sizes[i], forbidden, [2]*sizes[j])
            check_degrees(result, [2]*sizes[i], forbidden, [2]*sizes[j])
            remainder.update((a+offsets[i], b-sizes[i]+offsets[j]) for a, b in result)
        augmentations.update(stats)
    require(not remainder & used, 'two stages share an edge')
    require(set(Counter(v for e in remainder for v in e).values()) == {4}, 'integrated deletion degree')

    mixed, segments, truncation_fixture = 0, 0, None
    retained, dropped = 0, 0
    for d in range(1, 4):
        all_edges = list(combinations_with_replacement(range(d), 2))
        for mask in range(1 << len(all_edges)):
            support = [e for k, e in enumerate(all_edges) if mask >> k & 1]
            sizes = [10**10+1009*i for i in range(d)]
            N = sum(sizes)
            ts = [t for t in combinations_with_replacement(range(d), 3) if set(pairs(t)) <= set(support)]
            magnitudes = [Q(1), Q(N,4), Q(3*N,2), Q(N*isqrt(N),10), Q(N*N,10000)]
            z = {t: magnitudes[j % len(magnitudes)] for j, t in enumerate(ts)}
            load = Counter()
            for t, value in z.items():
                for e in pairs(t):
                    load[e] += value
            for e in support:
                capacity = comb(sizes[e[0]],2) if e[0] == e[1] else sizes[e[0]]*sizes[e[1]]
                z[e] = capacity-load[e]
                require(z[e] > 0, 'invalid audit profile')
            alpha = Q(1,2*d)
            cert = S.truncated_roles(sizes, support, z, alpha)
            segments += verify_truncation(sizes, support, z, alpha, cert)
            retained += sum(value > 0 for value in cert['counts'].values())
            dropped += sum(value == 0 and z[p] > 0 for p, value in cert['counts'].items())
            truncation_fixture = (sizes, support, z, alpha, cert)
            mixed += 1

    boundary = []
    for t in fixture['boundary_scales']:
        k = t*t
        for sign in (-1, 1):
            l = t*t-1+sign*t
            N = k+l
            require(min(k,l)*3 >= N, 'boundary class-size bound')
            support = [(0,0),(0,1)]
            if sign == -1:
                z = {(0,0,0):Q(t**3,6), (0,0,1):Q(k*l,2), (0,0):Q(0), (0,1):Q(0)}
                W = z[0,0,0]+z[0,0,1]
                require(3*W == comb(k,2)+k*l, 'decomposition optimum upper bound')
                small = z[0,0,0]
            else:
                z = {(0,0,0):Q(0), (0,0,1):Q(comb(k,2)), (0,0):Q(0), (0,1):Q(t**3)}
                require(z[0,0,1] == comb(k,2), 'core-edge optimum upper bound')
                small = z[0,1]
            cert = S.truncated_roles([k,l], support, z, Q(1,3))
            segments += verify_truncation([k,l], support, z, Q(1,3), cert)
            require(small > N and small/N**2 < Q(1,t), 'intermediate mass scaling')
            boundary.append({'t':t,'side':sign,'N':N,'small_mass':str(small),
                             'small_mass_over_N_squared':str(small/N**2)})

    band_cases = 0
    for M in range(1,17):
        levels = [Q(1,2**j) for j in range(M+2)]
        for values in ([levels[j] for j in range(1,M+1)],
                       [levels[j] for j in range(2,M+2)],
                       [Q(0)]*M,
                       [(levels[j]+levels[j+1])/2 for j in range(1,M+1)]):
            j = S.empty_band(values, levels)
            require(all(v >= levels[j] or v < levels[j+1] for v in values), 'invalid dense/sparse split')
            band_cases += 1

    negatives = []
    def reject(name, fn):
        try:
            fn()
        except (ValueError, KeyError, TypeError, IndexError):
            negatives.append(name)
        else:
            raise ValueError('negative control accepted: '+name)
    sizes, counts, support, cert = negative_fixture
    bad = deepcopy(cert)
    a,b,c,d = bad['trace'][0]
    bad['trace'][0] = (a,b,a,b)
    reject('same-component swap', lambda: replay_sparse(sizes,counts,support,bad))
    bad2 = deepcopy(cert)
    first = bad2['trace'][0]
    different = next(i for i,p in enumerate(bad2['patterns']) if p != bad2['patterns'][first[0]])
    bad2['trace'][0] = (first[0],first[1],different,0)
    reject('different-pattern swap', lambda: replay_sparse(sizes,counts,support,bad2))
    bad3 = deepcopy(cert)
    bad3['components'][0][1] = bad3['components'][0][0]
    reject('corrupt final component', lambda: replay_sparse(sizes,counts,support,bad3))
    result,ds,forbidden = degree_fixture
    reject('forbidden edge inserted', lambda: check_degrees(result+[next(iter(forbidden))],ds,forbidden))
    reject('repeated realization edge', lambda: check_degrees(result+[result[0]],ds,forbidden))
    sizes,support,z,alpha,cert = truncation_fixture
    altered = deepcopy(cert)
    p = next(p for p in z if z[p] > 0 and cert['counts'][p] == 0)
    altered['counts'][p] = sum(sizes)-1
    reject('tiny coordinate retained', lambda: verify_truncation(sizes,support,z,alpha,altered))
    altered2 = deepcopy(cert)
    p = next(iter(altered2['blocks'][0][0]['roles']))
    altered2['blocks'][0][0]['roles'][p] += 1
    reject('wrong local role count', lambda: verify_truncation(sizes,support,z,alpha,altered2))
    bad_profile = dict(z)
    p = next(p for p in z if len(p)==2)
    bad_profile[p] += 1
    reject('incorrect spare capacity', lambda: verify_truncation(sizes,support,bad_profile,alpha,cert))

    return {
        'status':'PASS',
        'scope':'exact finite constructive bridges; universal dense completion is imported and unformalized',
        'sparse_instances':sparse_results, 'total_replayed_switches':total_switches,
        'forbidden_degree_instances':degree_cases,
        'degree_construction_operations':dict(sorted(augmentations.items())),
        'integrated_sparse_and_remainder':{'vertices':sum(integrated[0]),'sparse_edges':len(integrated[2]),
                                           'remainder_edges':len(remainder),'remainder_maximum_degree':4,
                                           'remainder_sha256':digest(sorted(remainder))},
        'compressed_role_checks':{'mixed_templates':mixed,'boundary_profiles':len(boundary),
                                  'total_intervals':segments,'retained_coordinates_in_mixed_tests':retained,
                                  'positive_dropped_coordinates_in_mixed_tests':dropped},
        'intermediate_optimum_profiles':boundary,
        'threshold_endpoint_checks':band_cases, 'negative_controls':negatives,
    }


if __name__ == '__main__':
    print(json.dumps(main(), indent=2, sort_keys=True))
