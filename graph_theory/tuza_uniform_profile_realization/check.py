"""Definition-level checks of compact certificates and finite proof identities.

Standard library only. These checks do not certify Keevash's existence theorem
or provide its threshold. No assertion statements are used as validity gates.
"""
from collections import Counter
from copy import deepcopy
from fractions import Fraction as Q
from itertools import combinations, combinations_with_replacement, permutations, product
from math import comb, prod
from pathlib import Path
import json
import random
import sys

import construct as C


def require(ok, message):
    if not ok:
        raise ValueError(message)


def ij(a, b):
    return (min(a, b), max(a, b))


def literal_pattern(pattern):
    return Counter(ij(pattern[a], pattern[b]) for a in range(len(pattern))
                   for b in range(a + 1, len(pattern)))


def literal_local(pattern, i):
    role = pattern.index(i)
    return Counter(ij(i, pattern[j]) for j in range(len(pattern)) if j != role)


def profile_check(record):
    # Rebuild support from the prose, without trusting producer support fields.
    support = {(i, j) for i in range(8) for j in range(i, 8)}
    support |= {(i, 8 + b) for i in range(8) for b in range(3) if i & (1 << b)}
    allowed = {t for t in combinations_with_replacement(range(11), 3)
               if all(ij(t[a], t[b]) in support for a in range(3) for b in range(a + 1, 3))}
    rows = record['profile']
    x = {tuple(r['types']): Q(r['weight']) for r in rows}
    require(len(rows) == len(x) and set(x) == allowed, 'incomplete profile support')
    require(min(x.values()) == Q(1, 26), 'wrong positive profile margin')
    load = Counter()
    for t, value in x.items():
        for e, a in literal_pattern(t).items():
            load[e] += value * a
    require(all(load[e] == (Q(1, 2) if e[0] == e[1] else 1) for e in support),
            'profile edge capacity failure')
    require(sum(x.values()) == Q(44, 3), 'profile total failure')
    return sorted(support), x


def packing_check(record, support):
    sizes = record['sizes']
    require(sizes == [5] + [4] * 10, 'wrong unequal graph')
    parent = [i for i, size in enumerate(sizes) for _ in range(size)]
    edges = {ij(a, b) for a in range(len(parent)) for b in range(a + 1, len(parent))
             if ij(parent[a], parent[b]) in support}
    used = Counter()
    for row in record['packing']:
        require(len(row) == 3 and len(set(row)) == 3, 'malformed triangle')
        require(all(type(v) is int and 0 <= v < len(parent) for v in row), 'bad vertex')
        for e in combinations(sorted(row), 2):
            require(e in edges, 'nonedge in packing')
            used[e] += 1
    require(set(used) == edges and all(value == 1 for value in used.values()),
            'packing not an edge partition')
    return {'vertices': len(parent), 'edges': len(edges), 'triangles': len(record['packing'])}


def verify_roles(sizes, support, profile, alpha, cert):
    N, d = sum(sizes), len(sizes)
    M = comb(d + 2, 3) + comb(d + 1, 2)
    lam, U = 8 * M / alpha, cert['U']
    require(cert['M'] == M and cert['lambda'] == lam, 'wrong role constants')
    require(U - 1 < lam + 4 * M <= U, 'wrong U')
    b = {e: (sizes[e[0]] * (sizes[e[0]] - 1) // 2 if e[0] == e[1]
             else sizes[e[0]] * sizes[e[1]]) for e in support}
    load = Counter()
    for p, value in profile.items():
        require(value > 0 and set(literal_pattern(p)) <= set(support), 'invalid profile pattern')
        for e, a in literal_pattern(p).items():
            load[e] += a * value
    require(all(load[e] == b[e] for e in support), 'inexact role input profile')
    m = cert['counts']
    require(set(m) == set(profile), 'missing role pattern')
    for p, value in profile.items():
        scaled = (1 - lam / N) * value
        require(type(m[p]) is int and 0 < m[p] <= scaled < m[p] + 1, 'incorrect profile floor')
    desired = Counter()
    for p, value in m.items():
        for e, a in literal_pattern(p).items():
            desired[e] += a * value
    totals = {}
    segments = 0
    for i, rows in enumerate(cert['blocks']):
        require(sizes[i] >= alpha * N and sizes[i] >= 8 * (U + 1) ** 2, 'insufficient part size')
        start, roles, deficits = 0, Counter(), Counter()
        for row in rows:
            require(row['start'] == start < row['stop'] <= sizes[i], 'role partition gap')
            length = row['stop'] - start
            start = row['stop']
            expected_degree = Counter()
            require(set(row['roles']) == {p for p in m if i in p}, 'wrong role support')
            for p, count in row['roles'].items():
                require(type(count) is int and count >= 0, 'bad role count')
                require(abs(Q(count) - Q(m[p] * p.count(i), sizes[i])) < 1, 'unbalanced roles')
                roles[p] += count * length
                for e, a in literal_local(p, i).items():
                    expected_degree[e] += count * a
            require(dict(expected_degree) == row['degree'], 'incorrect local role incidence')
            require(set(row['deficit']) == {e for e in support if i in e}, 'wrong deficit support')
            for e, r in row['deficit'].items():
                pdeg = sizes[i] - 1 if e == (i, i) else sizes[e[1] if e[0] == i else e[0]]
                require(r == pdeg - expected_degree[e] and 1 <= r <= U, 'bad complement degree')
                deficits[e] += r * length
            segments += 1
        require(start == sizes[i], 'incomplete role partition')
        require(all(roles[p] == m[p] * p.count(i) for p in m), 'role total mismatch')
        for e, value in deficits.items():
            multiplicity = 2 if e == (i, i) else 1
            require(value == multiplicity * (b[e] - desired[e]), 'complement degree sum mismatch')
            if multiplicity == 2:
                require(value % 2 == 0, 'odd internal complement')
            totals[i, e] = value
    for i, j in support:
        if i != j:
            require(totals[i, (i, j)] == totals[j, (i, j)], 'unequal cross sums')
    return segments


def check_edge_list(edges, left, right=None):
    require(len(edges) == len(set(edges)), 'repeated degree edge')
    if right is None:
        require(all(0 <= a < b < len(left) for a, b in edges), 'simple edge invalid')
        degree = Counter(v for e in edges for v in e)
        require([degree[v] for v in range(len(left))] == left, 'simple degree mismatch')
    else:
        require(all(0 <= a < len(left) and 0 <= b < len(right) for a, b in edges), 'bipartite edge invalid')
        dl, dr = Counter(a for a, b in edges), Counter(b for a, b in edges)
        require([dl[v] for v in range(len(left))] == left, 'left degree mismatch')
        require([dr[v] for v in range(len(right))] == right, 'right degree mismatch')


def verify_lattice(target, coefficients, support, singleton=None):
    actual = Counter()
    for t, z in coefficients.items():
        require(type(z) is int and set(literal_pattern(t)) <= set(support), 'invalid lattice term')
        vector = literal_pattern(t) if singleton is None else literal_local(t, singleton)
        for e, a in vector.items():
            actual[e] += z * a
    require(all(actual[e] == target.get(e, 0) for e in set(actual) | set(target)), 'lattice identity failure')


def check_cleanup(parent, original, removed, core, alpha):
    require(removed <= original, 'cleanup removes nonedge')
    residual = original - removed
    degree = Counter(v for e in residual for v in e)
    require(all(value % 2 == 0 for value in degree.values()), 'cleanup leaves odd degree')
    require(len(residual) % 3 == 0, 'cleanup leaves edge residue')
    k = sum(i < core for i in parent)
    require(len(removed) <= len(parent) - k + k // 2 + 5, 'cleanup cost')
    deleted_degree = Counter(v for e in removed for v in e)
    require(max(deleted_degree.values(), default=0) <= int(1 / alpha) + 4, 'cleanup maximum degree')
    return residual


def main(path):
    record = json.loads(Path(path).read_text())
    support, x = profile_check(record['positive_profile'])
    packing = packing_check(record['unequal_decomposition'], support)
    inverse = C.split_right_inverse(support, 8)
    row_sums = Counter()
    for e, column in inverse.items():
        # Rational right inverse is separate from integer-lattice witnesses.
        result = Counter()
        for t, z in column.items():
            require(t in x, 'right inverse unsupported')
            row_sums[t] += abs(z)
            for f, a in literal_pattern(t).items():
                result[f] += a * z
        require(all(result[f] == int(e == f) for f in support), 'right inverse failure')
    require(max(row_sums.values()) <= 2, 'right inverse norm too large')
    require(Q(2001, 10**6) < Q(1, 104), 'box cross bound')
    require(Q(10005, 10**7) + Q(1001, 2000000) < Q(1, 104), 'box loop bound')
    require(Q(999, 11011) >= Q(1, 12), 'box part bound')
    require(Q(1, 52) / Q(11011, 1000)**2 >= Q(1, 7000), 'box profile bound')
    box_cases = 0
    for offset in ([-1] * 11, [1] * 11, [(-1)**i for i in range(11)]):
        t = 1000
        sizes = [t + v for v in offset]
        b = C.capacities(sizes, support)
        new = dict(x)
        for e, column in inverse.items():
            delta = Q(b[e], t*t) - (Q(1, 2) if e[0] == e[1] else 1)
            for triangle, z in column.items():
                new[triangle] += delta * z
        require(min(new.values()) >= Q(1, 52), 'box positivity')
        require(all(sum(literal_pattern(p)[e] * z for p, z in new.items()) == Q(b[e], t*t)
                    for e in support), 'box capacity')
        box_cases += 1

    mixed, segments, role_instances = 0, 0, []
    min_mass = Q(1)
    for d in range(1, 4):
        pairs = list(combinations_with_replacement(range(d), 2))
        for mask in range(1 << len(pairs)):
            es = [e for j, e in enumerate(pairs) if mask >> j & 1]
            sizes = [10**12 + 100003 * i for i in range(d)]
            ts = C.triangles(d, es)
            b = C.capacities(sizes, es)
            profile = {}
            if ts:
                row = {e: sum(literal_pattern(p)[e] for p in ts) for e in es}
                common = min(Q(b[e], 2 * row[e]) for e in es if row[e])
                profile.update({p: common for p in ts})
            profile.update({e: b[e] - sum(literal_pattern(p)[e] * z for p, z in profile.items())
                            for e in es})
            alpha = Q(1, 2*d)
            cert = C.compressed_roles(sizes, es, profile, alpha)
            segments += verify_roles(sizes, es, profile, alpha, cert)
            if profile:
                min_mass = min(min_mass, min(profile.values()) / sum(sizes)**2)
            role_instances.append((sizes, es, profile, alpha, cert))
            mixed += 1
    # All-triangle complete graph profiles, with no spare coordinates and large denominators.
    for d in range(1, 5):
        sizes = [10**12 + 101*i for i in range(d)]
        N = sum(sizes)
        es = list(combinations_with_replacement(range(d), 2))
        profile = {t: Q(prod(comb(sizes[i], t.count(i)) for i in set(t)), N-2)
                   for t in C.triangles(d, es)}
        alpha = Q(1, 2*d)
        cert = C.compressed_roles(sizes, es, profile, alpha)
        segments += verify_roles(sizes, es, profile, alpha, cert)
        role_instances.append((sizes, es, profile, alpha, cert))

    rng = random.Random(20260924)
    degree_cases = 0
    for U in range(1, 6):
        n = 8 * (U + 1)**2
        for mode in range(6):
            ds = ([1] * n if mode == 0 else [U] * n if mode == 1 else
                  [rng.randint(1, U) for _ in range(n)])
            if sum(ds) % 2:
                j = next((i for i, z in enumerate(ds) if z < U), None)
                if j is None:
                    ds[0] -= 1
                else:
                    ds[j] += 1
            require(all(1 <= v <= U for v in ds), 'invalid degree test')
            check_edge_list(C.realize_simple(ds), ds)
            right = ds.copy()
            rng.shuffle(right)
            # Redistribute degrees to exercise unequal degree multisets, preserving sums.
            for _ in range(n):
                a, b = rng.randrange(n), rng.randrange(n)
                if a != b and right[a] > 1 and right[b] < U:
                    right[a] -= 1
                    right[b] += 1
            check_edge_list(C.realize_bipartite(ds, right), ds, right)
            degree_cases += 2

    lattice_templates, global_cases, local_cases = 0, 0, 0
    lattice_fixture = None
    for d in range(1, 5):
        for core in range(1, d + 1):
            for neighborhoods in product(range(1, 1 << core), repeat=d-core):
                es = list(combinations_with_replacement(range(core), 2))
                es += [(i, core+j) for j, mask in enumerate(neighborhoods)
                       for i in range(core) if mask >> i & 1]
                es = sorted(es)
                # A spanning tree repairs arbitrary type parities.
                tree = [(0, i) for i in range(1, core)]
                tree += [(min(i for i in range(core) if mask >> i & 1), core+j)
                         for j, mask in enumerate(neighborhoods)]
                for _ in range(6):
                    b = {e: rng.randrange(-20, 21) for e in es}
                    for parent, child in reversed(tree):
                        if sum(v * e.count(child) for e, v in b.items()) % 2:
                            b[(parent, child)] += 1
                    b[(0, 0)] += -sum(b.values()) % 3
                    coefficients = C.split_lattice(core, d, es, b)
                    verify_lattice(b, coefficients, es)
                    global_cases += 1
                    lattice_fixture = (b, coefficients, es)
                for i in range(d):
                    target = {e: rng.randrange(-20, 21) for e in es if i in e}
                    first = next(iter(target))
                    target[first] += sum(target.values()) % 2
                    coefficients = C.singleton_lattice(core, i, target)
                    verify_lattice(target, coefficients, es, i)
                    local_cases += 1
                lattice_templates += 1

    # Direct padded-embedding enumeration catches normalization and automorphisms.
    # Four core vertices, two tag-left, three tag-right; one isolated core role.
    tag_a, tags = C.tag_edges(5, 3)
    require(tag_a == 2 and len(tags) == 5, 'tag edge count')
    L = 4 * 3 * 2 * 1 * 2 * 3
    weight = Q(2 * 3, L)
    core_load, tag_load = Counter(), Counter()
    restricted_core, restricted_tag = Counter(), Counter()
    embeddings = 0
    for image in permutations(range(4), 4):
        tri = list(combinations(sorted(image[:3]), 2))
        for tag in tags:
            embeddings += 1
            for e in tri:
                core_load[e] += weight
            tag_load[tag] += weight
            if (0, 1) not in tri:
                for e in tri:
                    restricted_core[e] += weight
                restricted_tag[tag] += weight
    require(set(core_load.values()) == {Q(5, 2)}, 'padded original normalization')
    require(set(tag_load.values()) == {Q(1)}, 'padded tag normalization')
    require(set(restricted_tag.values()) == {Q(1, 2)}, 'restricted tag normalization')
    require(restricted_core[(0, 1)] == 0 and restricted_core[(2, 3)] == Q(5, 2),
            'restricted original normalization')
    tag_cases = 0
    for N in range(2, 14):
        for m in range(1, N*N + 1):
            a, tags2 = C.tag_edges(m, N)
            require(a == (m+N-1)//N and len(tags2) == m, 'tag construction count')
            missing = {(i, j) for i in range(a) for j in range(N)} - tags2
            require(max(Counter(j for i, j in missing).values(), default=0) <= 1,
                    'tag right degree')
            require(max(Counter(i for i, j in missing).values(), default=0) <= (N+a-1)//a,
                    'tag left degree')
            tag_cases += 1

    cleanup_cases, cleanup_fixture = 0, None
    for t in range(3, 14):
        for offset in range(3):
            sizes = [t + int(i % 3 == offset) for i in range(11)]
            alpha = Q(min(sizes), sum(sizes))
            parent, original, removed = C.split_cleanup(sizes, support, 8)
            residual = check_cleanup(parent, original, removed, 8, alpha)
            typed = Counter(ij(parent[a], parent[b]) for a, b in residual)
            coefficients = C.split_lattice(8, 11, support, typed)
            verify_lattice(typed, coefficients, support)
            cleanup_cases += 1
            cleanup_fixture = (parent, original, removed, alpha)

    negative = []
    def reject(name, fn):
        try:
            fn()
        except (ValueError, KeyError, TypeError):
            negative.append(name)
        else:
            raise ValueError('negative control accepted: ' + name)
    bad_profile = deepcopy(record['positive_profile'])
    bad_profile['profile'][0]['weight'] = str(Q(bad_profile['profile'][0]['weight']) + 1)
    reject('overloaded profile', lambda: profile_check(bad_profile))
    bad_packing = deepcopy(record['unequal_decomposition'])
    bad_packing['packing'].append(bad_packing['packing'][0])
    reject('duplicate packing triangle', lambda: packing_check(bad_packing, support))
    sizes, es, z, alpha, cert = role_instances[-1]
    damaged = deepcopy(cert)
    p = next(iter(damaged['blocks'][0][0]['roles']))
    damaged['blocks'][0][0]['roles'][p] += 1
    reject('changed role count', lambda: verify_roles(sizes, es, z, alpha, damaged))
    damaged2 = deepcopy(cert)
    damaged2['blocks'][0][0]['degree'][(0, 0)] += 1
    reject('incorrect internal incidence', lambda: verify_roles(sizes, es, z, alpha, damaged2))
    reject('repeated graph edge', lambda: check_edge_list([(0, 1), (0, 1)], [2, 2]))
    b, coefficients, es = lattice_fixture
    wrong = dict(coefficients)
    wrong[(0, 0, 0)] = wrong.get((0, 0, 0), 0) + 1
    reject('damaged signed lattice witness', lambda: verify_lattice(b, wrong, es))
    parent, original, removed, alpha = cleanup_fixture
    damaged_removed = removed - {next(iter(removed))}
    reject('parity cleanup edge restored', lambda: check_cleanup(parent, original, damaged_removed, 8, alpha))
    reject('wrong embedding normalization', lambda: require(
        all(2*z == 1 for z in tag_load.values()), 'tag load not one'))

    return {
        'status': 'PASS', 'certificate_scope': 'finite identities and witnesses; universal existence is imported',
        'positive_profile': {'types': 150, 'margin': '1/26', 'mass': '44/3',
                             'right_inverse_columns': len(inverse), 'right_inverse_row_norm': str(max(row_sums.values())),
                             'varying_box_checks': box_cases, 'alpha': '1/12', 'epsilon': '1/7000'},
        'unequal_decomposition': packing,
        'compressed_roles': {'mixed_templates': mixed, 'complete_graph_profiles': 4,
                             'total_segments': segments, 'minimum_tested_class_size': 10**12,
                             'small_mixed_minimum_mass_over_N_squared': str(min_mass)},
        'degree_realizations': degree_cases,
        'split_lattices': {'templates': lattice_templates, 'global_witnesses': global_cases,
                           'singleton_witnesses': local_cases},
        'tag_checks': {'literal_constructions': tag_cases, 'padded_embeddings': embeddings,
                       'removed_original_edge_test': True},
        'cleanup_instances': cleanup_cases,
        'negative_controls': negative,
    }


if __name__ == '__main__':
    certificate = sys.argv[1] if len(sys.argv) > 1 else Path(__file__).with_name('CERTIFICATES.json')
    print(json.dumps(main(certificate), indent=2, sort_keys=True))
