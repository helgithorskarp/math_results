"""Exact author audit with definition-level certificate checks.

Only the constructors are imported. Verification uses literal edge sets,
incidences, colors and rational profile equations; it does not invoke the
dense existence theorem or certify its universal hypotheses by finite tests.
"""
from collections import Counter, defaultdict
from copy import deepcopy
from fractions import Fraction as Q
from hashlib import sha256
from itertools import combinations, combinations_with_replacement
import json
from math import ceil, comb, floor
import random

from constructions import balanced, edge_color, external_counts, independent_extension, realize_degrees
from sparse_avoid import sparse_pack


def check(ok, message):
    if not ok:
        raise ValueError(message)


def pairs(row):
    return [tuple(sorted(e)) for e in combinations(row, 2)]


def digest(value):
    return sha256(json.dumps(value, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


def verify_coloring(n, edges, colored):
    check(len(edges) == len(set(edges)), 'repeated input edge')
    check(len(colored) == len(edges), 'color certificate length')
    check({(a, b) for a, b, c in colored} == set(edges), 'color certificate edge set')
    deg = Counter(v for e in edges for v in e)
    bound = max(deg.values(), default=0) + 1
    seen = set()
    for a, b, c in colored:
        check(type(a) is int and type(b) is int and 0 <= a < b < n, 'invalid colored edge')
        check(type(c) is int and 0 <= c < bound, 'color exceeds Delta+1')
        check((a, c) not in seen and (b, c) not in seen, 'color conflict')
        seen.update(((a, c), (b, c)))


def verify_degrees(left, right, forbidden, edges):
    targets = left + ([] if right is None else right)
    n = len(targets)
    check(len(edges) == len(set(edges)), 'repeated realization edge')
    check(not set(edges) & set(forbidden), 'forbidden edge used')
    degrees = [0] * n
    for a, b in edges:
        check(type(a) is int and type(b) is int and 0 <= a < b < n, 'invalid realization edge')
        if right is not None:
            check(a < len(left) <= b, 'wrong bipartite pair')
        degrees[a] += 1
        degrees[b] += 1
    check(degrees == targets, 'wrong prescribed degree')


def core_profile(sizes, loops, cross, small_sizes, neighborhoods, mode='uniform'):
    """Feasible rational profile, using actual type triangle counts."""
    n, d = sum(sizes), len(sizes)
    support = {(i, i) for i in loops} | {tuple(sorted(e)) for e in cross}
    capacities = {e: Q(comb(sizes[e[0]], 2) if e[0] == e[1]
                       else sizes[e[0]] * sizes[e[1]]) for e in support}
    triangle_mass = {}
    for t in combinations_with_replacement(range(d), 3):
        if set(pairs(t)) <= support:
            count = 1
            for i, k in Counter(t).items():
                count *= comb(sizes[i], k)
            triangle_mass[t] = Q(count, 4 * max(1, n - 2))
    external = {}
    for h, sh in enumerate(small_sizes):
        for i, j in sorted(support):
            if i in neighborhoods[h] and j in neighborhoods[h]:
                if mode == 'saturated_bipartite':
                    check(i != j, 'saturated fixture has internal edge')
                    z = Q(sh * min(sizes[i], sizes[j]))
                else:
                    z = sh * capacities[i, j] / max(1, n - 1)
                external[h, i, j] = z
    if mode == 'tiny_coordinate':
        key = min(external)
        h = key[0]
        sh, c = small_sizes[h], d + 2
        cutoff = 12 * (sum(small_sizes) + 1)
        small = Q((cutoff - 1) * sh, sh - c)
        check(small < external[key], 'tiny fixture does not reduce mass')
        external[key] = small
    spare = capacities.copy()
    for t, mass in triangle_mass.items():
        for e in pairs(t):
            spare[e] -= mass
    for (h, i, j), mass in external.items():
        spare[i, j] -= mass
    check(all(v >= 0 for v in spare.values()), 'core capacity exceeded')
    for h, sh in enumerate(small_sizes):
        for i in neighborhoods[h]:
            incidence = sum(((a == i) + (b == i)) * z for (g, a, b), z in external.items() if g == h)
            check(incidence <= sh * sizes[i], 'spoke capacity exceeded')
    return support, capacities, triangle_mass, external, spare


def verify_extension(sizes, loops, cross, small_sizes, neighborhoods, profile, witness):
    n, d, r = sum(sizes), len(sizes), len(small_sizes)
    labels = [i for i, size in enumerate(sizes) for _ in range(size)]
    offsets = [sum(sizes[:i]) for i in range(d)]
    small_offsets = [n + sum(small_sizes[:h]) for h in range(r)]
    host_support = {(i, i) for i in loops} | {tuple(sorted(e)) for e in cross}
    s, c, cutoff = sum(small_sizes), d + 2, 12 * (sum(small_sizes) + 1)
    expected = {}
    for key, z in profile.items():
        h, i, j = key
        check((i, j) in host_support and i in neighborhoods[h] and j in neighborhoods[h], 'unsupported profile pattern')
        sh = small_sizes[h]
        scaled = (Q(sh - c, sh) * z) if sh > c else Q(0)
        integer = scaled.numerator // scaled.denominator
        expected[key] = integer if integer >= cutoff else 0
    check(witness['counts'] == expected, 'wrong exceptional rounding')
    used, seen_core, incidence, observed = set(), set(), Counter(), Counter()
    expected_triangles = []
    for h, rows in enumerate(witness['colored_edges']):
        edges = [(a, b) for a, b, color in rows]
        verify_coloring(n, edges, rows)
        for a, b, color in rows:
            e = tuple(sorted((labels[a], labels[b])))
            check(e in host_support, 'unsupported core edge')
            check(set(e) <= set(neighborhoods[h]), 'wrong independent neighborhood')
            check(0 <= color < small_sizes[h], 'unavailable independent vertex')
            check((a, b) not in seen_core, 'core edge repeated across classes')
            seen_core.add((a, b))
            observed[h, *e] += 1
            incidence[h, e, a] += 1
            incidence[h, e, b] += 1
            expected_triangles.append((a, b, small_offsets[h] + color))
    check(witness['triangles'] == expected_triangles, 'triangle decoding mismatch')
    for row in witness['triangles']:
        check(len(set(row)) == 3, 'triangle repeated vertex')
        for e in pairs(row):
            check(e not in used, 'triangle edge repeated')
            used.add(e)
    for key, m in expected.items():
        h, i, j = key
        check(observed[key] == m, 'wrong triangle type count')
        e = (i, j)
        for a in set(e):
            total = m * e.count(a)
            low, rem = divmod(total, sizes[a])
            for k in range(sizes[a]):
                v = offsets[a] + k
                check(incidence[h, e, v] == low + (k < rem), 'unbalanced type-degree certificate')
    by_type = Counter()
    for a, b in seen_core:
        e = tuple(sorted((labels[a], labels[b])))
        by_type[e] += 1
    actual = Counter((tuple(sorted((labels[a], labels[b]))), v)
                     for a, b in seen_core for v in (a, b))
    max_discrepancy = Q(0)
    for e, m in by_type.items():
        for i in set(e):
            average = Q(e.count(i) * m, sizes[i])
            for v in range(offsets[i], offsets[i] + sizes[i]):
                deviation = abs(actual[e, v] - average)
                check(deviation <= r, 'combined discrepancy bound')
                max_discrepancy = max(max_discrepancy, deviation)
    degree = Counter(v for e in seen_core for v in e)
    check(max(degree.values(), default=0) <= s, 'combined deletion maximum degree')
    loss = sum(profile.values()) - len(witness['triangles'])
    bound = Q(r * c * n, 2) + 12 * r * (d * (d + 1) // 2) * (s + 1)
    check(0 <= loss <= bound, 'external linear loss bound')
    return {'core_vertices': n, 'independent_vertices': s,
            'triangles': len(witness['triangles']), 'max_deleted_degree': max(degree.values(), default=0),
            'max_type_discrepancy': str(max_discrepancy), 'exact_loss': str(loss),
            'counts': [[*key, m] for key, m in sorted(expected.items())],
            'triangles_sha256': digest(witness['triangles']),
            'colored_edges_sha256': digest(witness['colored_edges'])}, sorted(seen_core)


def verify_sparse(sizes, counts, forbidden, witness):
    n = sum(sizes)
    offsets = [sum(sizes[:i]) for i in range(len(sizes))]
    rows, patterns = [], []
    for p, m in sorted(counts.items()):
        for t in range(m):
            slots = Counter()
            row = []
            for i in p:
                row.append(offsets[i] + (t * p.count(i) + slots[i]) % sizes[i])
                slots[i] += 1
            rows.append(row)
            patterns.append(p)
    initial_roles = Counter((p, v) for p, row in zip(patterns, rows) for v in row)
    multiplicity = Counter(e for row in rows for e in pairs(row))
    fixed = set(forbidden)
    potential = sum(max(0, k - 1) for k in multiplicity.values()) + sum(multiplicity[e] for e in fixed)
    initial = potential
    for cid, pos, did, slot in witness['trace']:
        check(all(type(x) is int for x in (cid, pos, did, slot)), 'noninteger sparse trace')
        check(0 <= cid < len(rows) and 0 <= did < len(rows), 'invalid sparse component index')
        check(0 <= pos < len(rows[cid]) and 0 <= slot < len(rows[did]), 'invalid sparse role index')
        check(cid != did and patterns[cid] == patterns[did], 'bad sparse pattern swap')
        check(patterns[cid][pos] == patterns[did][slot], 'bad sparse role type')
        before = [list(rows[cid]), list(rows[did])]
        after = deepcopy(before)
        after[0][pos], after[1][slot] = after[1][slot], after[0][pos]
        check(all(len(set(row)) == len(row) for row in after), 'sparse repeated vertex')
        old = Counter(e for row in before for e in pairs(row))
        new = Counter(e for row in after for e in pairs(row))
        new_incident = [tuple(sorted((row[position], v)))
                        for row, position in zip(after, (pos, slot))
                        for k, v in enumerate(row) if k != position]
        check(len(new_incident) == len(set(new_incident)), 'repeated replacement edge')
        check(all(multiplicity[e] == 0 and e not in fixed for e in new_incident),
              'replacement incident edge was already present')
        touched = set(old) | set(new)
        previous = sum(max(0, multiplicity[e] - 1) + (multiplicity[e] if e in fixed else 0) for e in touched)
        for e, k in (new - old).items():
            check(multiplicity[e] == 0 and e not in fixed and k == 1, 'nonfresh replacement edge')
        multiplicity.subtract(old)
        multiplicity.update(new)
        current = sum(max(0, multiplicity[e] - 1) + (multiplicity[e] if e in fixed else 0) for e in touched)
        check(current < previous, 'sparse conflict did not decrease')
        potential += current - previous
        rows[cid], rows[did] = after
    check(rows == witness['components'], 'wrong final sparse components')
    check(patterns == witness['patterns'], 'wrong final sparse patterns')
    check(potential == 0 and max(multiplicity.values(), default=0) <= 1, 'remaining sparse conflict')
    check(not any(multiplicity[e] for e in fixed), 'sparse forbidden overlap')
    check(Counter((p, v) for p, row in zip(patterns, rows) for v in row) == initial_roles,
          'changed sparse local role')
    return {'initial_potential': initial, 'replayed_swaps': len(witness['trace']),
            'components': len(rows), 'edges': sum(k for k in multiplicity.values()),
            'components_sha256': digest(rows), 'trace_sha256': digest(witness['trace'])}, sorted(e for e, k in multiplicity.items() if k)


def coloring_audit():
    stats, instances = Counter(), 0
    canonical = sha256()
    for n in range(7):
        possible = list(combinations(range(n), 2))
        for mask in range(1 << len(possible)):
            edges = [e for j, e in enumerate(possible) if mask >> j & 1]
            colored, operations = edge_color(n, edges)
            verify_coloring(n, edges, colored)
            canonical.update(json.dumps([n, mask, colored], separators=(',', ':')).encode())
            stats.update(operations)
            instances += 1
    rng = random.Random(20260924)
    extra = 0
    for n in range(7, 49):
        for density in (1, 3, 5, 7, 9):
            edges = [e for e in combinations(range(n), 2) if rng.randrange(10) < density]
            colored, operations = edge_color(n, edges)
            verify_coloring(n, edges, colored)
            canonical.update(json.dumps([n, density, colored], separators=(',', ':')).encode())
            stats.update(operations)
            extra += 1
    check(stats['kempe_full_fan'] and stats['kempe_prefix_fan'], 'unexercised Kempe branch')
    return {'all_labeled_graphs_through_six_vertices': instances,
            'seeded_larger_graphs': extra, 'seed': 20260924,
            'certificate_stream_sha256': canonical.hexdigest(), 'operations': dict(sorted(stats.items()))}


def degree_audit():
    stats, records, zeros = Counter(), [], 0
    for s in (1, 2, 3, 5, 8):
        for bipartite in (False, True):
            a, b = 48 * (s + 1) + 3, 48 * (s + 1) + 10
            for mode in range(3):
                m = 12 * (s + 1) + mode if mode < 2 else a * s // (1 if bipartite else 2)
                left = balanced(m if bipartite else 2 * m, a)
                right = balanced(m, b) if bipartite else None
                if bipartite:
                    forbidden = sorted({(i, a + (i + k) % b) for i in range(a) for k in range(s)})
                else:
                    forbidden = sorted({tuple(sorted((i, (i + k) % a)))
                                        for i in range(a) for k in range(1, s // 2 + 1)})
                result, operations = realize_degrees(left, forbidden, right, scale=s)
                verify_degrees(left, right, forbidden, result)
                check(max(left) - min(left) <= 1 and (right is None or max(right) - min(right) <= 1), 'degree fixture not balanced')
                zeros += any(x == 0 for x in left + ([] if right is None else right))
                stats.update(operations)
                records.append([s, bipartite, mode, len(result), digest(result)])
    return {'instances': len(records), 'instances_with_zero_targets': zeros,
            'operations': dict(sorted(stats.items())), 'certificates_sha256': digest(records)}


def compressed_core_roles(sizes, loops, cross, small_sizes, neighborhoods, mode='uniform', thin=False):
    support, capacities, core, external, spare = core_profile(
        sizes, loops, cross, small_sizes, neighborhoods, mode)
    n, d, A = sum(sizes), len(sizes), len(small_sizes)
    if thin and core:
        t = min(core)
        old = core[t]
        core[t] = min(old, Q(n, 2))
        for e in pairs(t):
            spare[e] += old - core[t]
    counts = external_counts(d, small_sizes, external)
    deleted = {e: sum(m for (h, i, j), m in counts.items() if (i, j) == e) for e in support}
    y = dict(core)
    for e in support:
        y[e] = spare[e] + sum(z - counts[h, i, j] for (h, i, j), z in external.items() if (i, j) == e)
    for e in support:
        check(sum(pairs(p).count(e) * mass for p, mass in y.items()) == capacities[e] - deleted[e],
              'wrong residual capacity identity')
    alpha = Q(1, 2 * d)
    check(min(sizes) >= alpha * n, 'compressed class proportion fails')
    M = comb(d + 2, 3) + comb(d + 1, 2)
    lam = 8 * (M + A) / alpha
    B = M * (6 / alpha + 2)
    U = ceil(lam + B + A)
    check(n >= 4 * lam and sum(small_sizes) <= alpha * n / 4, 'compressed scale too small')
    theta = 1 - lam / n
    m = {p: (floor(theta * mass) if floor(theta * mass) >= n else 0) for p, mass in y.items()}
    intervals, deficit_sum = 0, Counter()
    range_min, range_max = U, 0
    for i, size in enumerate(sizes):
        incident = sorted(e for e in support if i in e)
        points = {0, size}
        for p, number in m.items():
            if i in p:
                points.add(number * p.count(i) % size)
        for (h, a, b), number in counts.items():
            if i in (a, b):
                points.add(number * (int(a == i) + int(b == i)) % size)
        cuts = sorted(points)
        for lo, hi in zip(cuts, cuts[1:]):
            check(lo < hi, 'empty compressed interval')
            intervals += 1
            target = Counter()
            for p, number in m.items():
                if i not in p:
                    continue
                low, rem = divmod(number * p.count(i), size)
                roles = low + (lo < rem)
                slot = p.index(i)
                for j, typ in enumerate(p):
                    if j != slot:
                        target[tuple(sorted((i, typ)))] += roles
            for e in incident:
                original = size - 1 if e[0] == e[1] else sizes[e[1] if e[0] == i else e[0]]
                removed = 0
                for (h, a, b), number in counts.items():
                    if (a, b) == e:
                        low, rem = divmod(number * e.count(i), size)
                        removed += low + (lo < rem)
                average_removed = Q(e.count(i) * deleted[e], size)
                check(abs(removed - average_removed) <= A, 'compressed deletion imbalance')
                residual_average = original - average_removed
                check(residual_average >= alpha * n / 2, 'residual average too small')
                check(theta * residual_average - B <= target[e] <= theta * residual_average + 2 * M,
                      'core role bound fails')
                deficit = original - removed - target[e]
                check(1 <= deficit <= U, 'complement degree out of range')
                range_min, range_max = min(range_min, deficit), max(range_max, deficit)
                deficit_sum[i, e] += (hi - lo) * deficit
    for e in support:
        remaining = capacities[e] - deleted[e] - sum(pairs(p).count(e) * number for p, number in m.items())
        for i in set(e):
            check(deficit_sum[i, e] == e.count(i) * remaining, 'complement incidence mismatch')
        if e[0] == e[1]:
            check(deficit_sum[e[0], e] % 2 == 0, 'odd internal complement')
        else:
            check(deficit_sum[e[0], e] == deficit_sum[e[1], e], 'unequal complement sides')
    W = sum(core.values())
    packed = sum(number for p, number in m.items() if len(p) == 3)
    check(W - packed <= (lam / 6 + M) * n, 'core linear loss bound')
    return {'intervals': intervals, 'core_order': n, 'small_order': sum(small_sizes),
            'complement_degree_range': [range_min, range_max] if deficit_sum else None,
            'U': U, 'positive_dropped_core_coordinates': sum(m[p] == 0 and y[p] > 0 for p in y)}


def compressed_audit():
    records = []
    for d in range(1, 4):
        possible = list(combinations(range(d), 2))
        for loopmask in range(1 << d):
            loops = [i for i in range(d) if loopmask >> i & 1]
            for crossmask in range(1 << len(possible)):
                cross = [e for j, e in enumerate(possible) if crossmask >> j & 1]
                for t in (100, 1000):
                    sizes = [t ** 4 + i * t ** 2 for i in range(d)]
                    small = [t ** 3, t ** 2 + 1]
                    neighborhoods = [list(range(d)), list(range(0, d, 2))]
                    row = compressed_core_roles(sizes, loops, cross, small, neighborhoods, thin=True)
                    records.append(row)
    check(len(records) == 148, 'wrong number of mixed-template scales')
    return {'mixed_templates': 74, 'scales_per_template': 2,
            'profiles': len(records), 'total_intervals': sum(r['intervals'] for r in records),
            'minimum_core_order': min(r['core_order'] for r in records),
            'maximum_core_order': max(r['core_order'] for r in records),
            'positive_dropped_core_coordinates': sum(r['positive_dropped_core_coordinates'] for r in records),
            'profile_records_sha256': digest(records)}


def hierarchy_audit():
    """Check finite-band arithmetic using illustrative rational tolerances.

    These are NOT computed dense-design tolerances or existence thresholds.
    """
    from itertools import product
    tested = 0
    for r in range(1, 5):
        alpha = Q(1, 3)
        eps, tolerances = [Q(1)], []
        for j in range(r + 1):
            a = min(alpha, eps[j]) / (r + 1)
            eta = a ** 2 / 100
            tolerances.append(eta)
            eps.append(min(eps[j] / 4, eta / (4 * r)))
        choices = [Q(0), *eps, *((eps[j] + eps[j + 1]) / 2 for j in range(r + 1))]
        for ratios in product(choices, repeat=r):
            j = next(j for j in range(r + 1)
                     if not any(eps[j + 1] <= x < eps[j] for x in ratios))
            large = [x for x in ratios if x >= eps[j]]
            small = [x for x in ratios if x < eps[j + 1]]
            check(len(large) + len(small) == r, 'unclassified size ratio')
            augmented = 1 + sum(large)
            aj = min(alpha, eps[j]) / (r + 1)
            check(augmented <= r + 1 and alpha >= aj * augmented, 'core proportion after absorption')
            check(all(x >= aj * augmented for x in large), 'absorbed class too small')
            check(sum(small) <= tolerances[j] * augmented, 'small classes exceed tolerance')
            tested += 1
    return {'exact_endpoint_and_midpoint_tuples': tested,
            'maximum_independent_type_count': 4,
            'tolerances': 'illustrative rational values only, not Keevash constants'}


def multiplicity_audit():
    checks = []
    for n in range(3, 25):
        edges = list(combinations(range(n), 2))
        colored, _ = edge_color(n, edges)
        verify_coloring(n, edges, colored)
        check(all(c < n for _, _, c in colored), 'multiplicity cap exceeded')
        used = set()
        for a, b, c in colored:
            for e in pairs((a, b, n + c)):
                check(e not in used, 'recolored cap repeats a spoke')
                used.add(e)
        mass = [{e: Q((e[0] + (2 * h + 1) * e[1]) % 5, 10) for e in edges} for h in range(2)]
        check(all(sum(row[e] for row in mass) <= 1 for e in edges), 'fractional core overload')
        for row in mass:
            for u in range(n):
                after = sum(z for e, z in row.items() if u in e) / n
                check(after <= Q(n - 1, n) < 1, 'fractional cap spoke load')
        sharp = n % 2 == 1
        if sharp:
            check((n - 1) * (n // 2) < len(edges), 'odd complete-graph matching obstruction fails')
        checks.append([n, len(edges), max(c for _, _, c in colored) + 1, sharp])
    return {'complete_core_witnesses': len(checks), 'fractional_reweighting_instances': 2 * len(checks),
            'odd_core_cap_obstructions': sum(row[-1] for row in checks),
            'records_sha256': digest(checks)}


def exact_triangle_cover(n, core_edges, sizes, neighborhoods):
    """Small direct hitting-set search on the actual expanded graph."""
    edges = set(core_edges)
    offset = n
    for size, neighbors in zip(sizes, neighborhoods):
        edges.update((u, v) for u in neighbors for v in range(offset, offset + size))
        offset += size
    triangles = [tuple(sorted(pairs(row))) for row in combinations(range(offset), 3)
                 if all(e in edges for e in pairs(row))]
    if not triangles:
        return 0
    covers = {e: 0 for e in edges}
    for j, row in enumerate(triangles):
        for e in row:
            covers[e] |= 1 << j
    best = len(core_edges)
    memo = {}

    def search(uncovered, chosen):
        nonlocal best
        if not uncovered:
            best = min(best, chosen)
            return
        if chosen >= best or memo.get(uncovered, best) <= chosen:
            return
        memo[uncovered] = chosen
        j = (uncovered & -uncovered).bit_length() - 1
        options = sorted(triangles[j], key=lambda e: -(covers[e] & uncovered).bit_count())
        for e in options:
            search(uncovered & ~covers[e], chosen + 1)

    search((1 << len(triangles)) - 1, 0)
    return best


def cover_cap_audit():
    records = []
    for n in (3, 4):
        possible = list(combinations(range(n), 2))
        for mask in range(1 << len(possible)):
            core = [e for j, e in enumerate(possible) if mask >> j & 1]
            neighborhoods = [list(range(n)), list(range(n - 1))]
            for sizes in ([n + 2, 1], [1, n + 3], [n + 2, n + 3], [n - 1, n + 1]):
                capped = [min(s, n) for s in sizes]
                original = exact_triangle_cover(n, core, sizes, neighborhoods)
                reduced = exact_triangle_cover(n, core, capped, neighborhoods)
                check(original == reduced, 'triangle cover changed under cap')
                records.append([n, mask, sizes, original])
    return {'expanded_graph_pairs': len(records), 'direct_exact_cover_solves': 2 * len(records),
            'core_orders': [3, 4], 'records_sha256': digest(records)}


def negative_audit(fixture, profile, witness, forbidden, sparse_counts, sparse):
    names = []

    def rejects(name, callback):
        try:
            callback()
        except (ValueError, KeyError, IndexError):
            names.append(name)
        else:
            raise ValueError('negative control accepted: ' + name)

    sizes, n = fixture['sizes'], sum(fixture['sizes'])
    colored = witness['colored_edges'][0]
    edges = [(a, b) for a, b, c in colored]
    bad = list(colored)
    a, b, c = bad[0]
    bad[0] = a, b, n
    rejects('color beyond palette', lambda: verify_coloring(n, edges, bad))
    adjacency = defaultdict(list)
    for k, (a, b, c) in enumerate(colored):
        adjacency[a].append(k)
        adjacency[b].append(k)
    u = next(v for v, ks in adjacency.items() if len(ks) >= 2)
    first, second = adjacency[u][:2]
    bad2 = list(colored)
    a, b, _ = bad2[second]
    bad2[second] = a, b, bad2[first][2]
    rejects('adjacent equal colors', lambda: verify_coloring(n, edges, bad2))
    damaged = deepcopy(witness)
    damaged['triangles'].pop()
    verify_args = (sizes, fixture['loops'], fixture['cross'], fixture['small_sizes'], fixture['neighborhoods'], profile)
    rejects('missing exceptional triangle', lambda: verify_extension(*verify_args, damaged))
    damaged2 = deepcopy(witness)
    key = min(damaged2['counts'])
    damaged2['counts'][key] += 1
    rejects('wrong rounded type count', lambda: verify_extension(*verify_args, damaged2))
    damaged3 = deepcopy(witness)
    damaged3['colored_edges'][1][0] = damaged3['colored_edges'][0][0]
    rejects('core edge reused across independent types', lambda: verify_extension(*verify_args, damaged3))
    bad_sparse = deepcopy(sparse)
    cid, pos, did, slot = bad_sparse['trace'][0]
    bad_sparse['trace'][0] = cid, pos, cid, pos
    rejects('same-component forbidden switch', lambda: verify_sparse(sizes, sparse_counts, forbidden, bad_sparse))
    bad_sparse2 = deepcopy(sparse)
    bad_sparse2['components'][0][0] = bad_sparse2['components'][0][1]
    rejects('corrupt final sparse component', lambda: verify_sparse(sizes, sparse_counts, forbidden, bad_sparse2))
    rejects('forbidden realization edge', lambda: verify_degrees([1, 1], None, [(0, 1)], [(0, 1)]))
    rejects('odd internal degree sum', lambda: realize_degrees([1, 1, 1], [], enforce_bound=False))
    rejects('imbalanced degree prescription', lambda: realize_degrees([0, 0, 2, 2], [], enforce_bound=False))
    rejects('insufficient side size', lambda: realize_degrees([1] * 48, [], scale=1))
    rejects('positive count below cutoff', lambda: realize_degrees([1, 1] + [0] * 94, [], scale=1))
    return names


FIXTURES = [
    {'name': 'one_clique_two_extensions', 'sizes': [1009], 'loops': [0], 'cross': [],
     'small_sizes': [7, 9], 'neighborhoods': [[0], [0]], 'mode': 'uniform'},
    {'name': 'unequal_cliques', 'sizes': [1200, 1207], 'loops': [0, 1], 'cross': [[0, 1]],
     'small_sizes': [11, 12], 'neighborhoods': [[0, 1], [0, 1]], 'mode': 'uniform'},
    {'name': 'mixed_core_distinct_neighborhoods', 'sizes': [1801, 1811, 1823], 'loops': [0, 2],
     'cross': [[0, 1], [0, 2], [1, 2]], 'small_sizes': [14, 17, 3],
     'neighborhoods': [[0, 1], [0, 2], [0, 1, 2]], 'mode': 'uniform'},
    {'name': 'dropped_intermediate_edge_type', 'sizes': [1200, 1207], 'loops': [0, 1], 'cross': [[0, 1]],
     'small_sizes': [11, 12], 'neighborhoods': [[0, 1], [0, 1]], 'mode': 'tiny_coordinate'},
    {'name': 'bipartite_core_spoke_saturation', 'sizes': [1296, 1311], 'loops': [], 'cross': [[0, 1]],
     'small_sizes': [13, 9, 1], 'neighborhoods': [[0, 1], [0, 1], [0, 1]], 'mode': 'saturated_bipartite'},
]


def run():
    color = coloring_audit()
    degree = degree_audit()
    records, all_degree, all_color = [], Counter(), Counter()
    first = None
    for fixture in FIXTURES:
        params = {k: v for k, v in fixture.items() if k != 'name'}
        support, capacities, core, profile, spare = core_profile(**params)
        witness = independent_extension(fixture['sizes'], fixture['small_sizes'], profile)
        checked, forbidden = verify_extension(fixture['sizes'], fixture['loops'], fixture['cross'],
                                              fixture['small_sizes'], fixture['neighborhoods'], profile, witness)
        checked['name'] = fixture['name']
        records.append(checked)
        all_degree.update(witness['degree_operations'])
        all_color.update(witness['coloring_operations'])
        if first is None:
            first = fixture, profile, witness, forbidden
    fixture, profile, witness, forbidden = first
    sizes = fixture['sizes']
    n = sum(sizes)
    sparse_counts = {(0, 0): n, (0, 0, 0): n}
    sparse = sparse_pack(sizes, sparse_counts, forbidden)
    sparse_record, sparse_edges = verify_sparse(sizes, sparse_counts, forbidden, sparse)
    combined = sorted(set(forbidden) | set(sparse_edges))
    deg = Counter(v for e in combined for v in e)
    remainder, ops = realize_degrees([2] * n, combined, scale=max(deg.values()))
    verify_degrees([2] * n, None, combined, remainder)
    sparse_record.update({'forbidden_edges': len(forbidden), 'remainder_edges': len(remainder),
                          'remainder_sha256': digest(remainder), 'remainder_operations': ops})
    negative = negative_audit(fixture, profile, witness, forbidden, sparse_counts, sparse)
    return {'status': 'PASS', 'coloring': color, 'near_regular_avoidance': degree,
            'independent_extension_instances': records,
            'extension_degree_operations': dict(sorted(all_degree.items())),
            'extension_coloring_operations': dict(sorted(all_color.items())),
            'integrated_forbidden_sparse_and_remainder': sparse_record,
            'compressed_core_roles': compressed_audit(),
            'class_hierarchy': hierarchy_audit(),
            'multiplicity_cap': multiplicity_audit(),
            'triangle_cover_cap': cover_cap_audit(),
            'negative_controls': negative,
            'scope': 'finite elementary constructions only; no universal dense-design or threshold computation'}


if __name__ == '__main__':
    print(json.dumps(run(), sort_keys=True, indent=2))
