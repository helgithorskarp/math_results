"""Generator-free exact census and integer negative-form checker.

Actual author six-books-3, researcher. Independently implemented domains:
binary F masks, ordered low pairs, all six-subsets, single-edge weights.
The optional --compare-generator mode additionally compares full sets and
every matrix entry. Default verification imports no generator.
"""
from collections import Counter
from itertools import combinations, permutations
from math import gcd
from pathlib import Path
import argparse
import hashlib
import json

HERE = Path(__file__).resolve().parent
P = tuple(combinations(range(6), 2))
POSITION = {edge: k for k, edge in enumerate(P)}
POINT_MAPS = tuple(permutations(range(6)))
LOW_MAPS = tuple(permutations(range(4)))


def need(ok, message):
    if not ok:
        raise RuntimeError(message)


def f_neighbors(mask):
    bits = [0] * 6
    for bit, (u, v) in enumerate(P):
        if mask & (1 << bit):
            bits[u] |= 1 << v
            bits[v] |= 1 << u
    return bits


def transform(mask, point):
    return sum(1 << POSITION[tuple(sorted((point[u], point[v])))]
               for bit, (u, v) in enumerate(P) if mask & (1 << bit))


def formula(mask, stars):
    """Class-by-class pair counts; no general adjacency formula is used."""
    f = f_neighbors(mask)
    low = [sum(1 << x for x in star) for star in stars]
    need(len(stars) == 4 and all(len(set(s)) == 2 for s in stars), 'invalid low pairs')
    need(all(not (f[s[0]] >> s[1] & 1) for s in stars), 'low pair is a red F edge')
    need(all(f[i].bit_count() + sum(x >> i & 1 for x in low) == 3 for i in range(6)),
         'wrong cubic degree')
    a = [[0] * 10 for _ in range(10)]
    for i in range(10):
        a[i][i] = 4 if i < 4 else 5
    for i, j in combinations(range(4), 2):
        a[i][j] = a[j][i] = 2 - (low[i] & low[j]).bit_count()
    for i in range(4):
        for j in range(6):
            value = 0 if low[i] >> j & 1 else 3 - (low[i] & f[j]).bit_count()
            a[i][4 + j] = a[4 + j][i] = value
    for i, j in P:
        common = (f[i] & f[j]).bit_count() + sum(x >> i & 1 and x >> j & 1 for x in low)
        value = (1 if f[i] >> j & 1 else 4) - common
        a[4 + i][4 + j] = a[4 + j][4 + i] = value
    return a


def ordered_profiles(mask):
    f = f_neighbors(mask)
    deficit = [3 - x.bit_count() for x in f]
    nonedges = [edge for edge in P if not (f[edge[0]] >> edge[1] & 1)]
    chosen = []

    def visit():
        if len(chosen) == 4:
            if not any(deficit):
                yield tuple(chosen)
            return
        for u, v in nonedges:
            if deficit[u] and deficit[v]:
                deficit[u] -= 1
                deficit[v] -= 1
                chosen.append((u, v))
                if max(deficit) <= 4 - len(chosen):
                    yield from visit()
                chosen.pop()
                deficit[u] += 1
                deficit[v] += 1
    yield from visit()


def census(expected):
    domain = []
    for mask in range(1 << 15):
        if mask.bit_count() != 5:
            continue
        f = f_neighbors(mask)
        if max(x.bit_count() for x in f) <= 3 and all((f[u] & f[v]).bit_count() <= 1
                    for bit, (u, v) in enumerate(P) if mask >> bit & 1):
            domain.append(mask)
    need(len(domain) == expected['eligible_labeled_F'], 'F domain size mismatch')
    digest = hashlib.sha256(''.join(str(x) + '\n' for x in domain).encode()).hexdigest()
    need(digest == expected['F_domain_sha256'], 'F domain mismatch')
    owner = {}
    declared = {}
    for rec in expected['catalog']:
        rep = rec['F_mask']
        images = {}
        for point in POINT_MAPS:
            image = transform(rep, point)
            if image not in images:
                inverse = tuple(point.index(i) for i in range(6))
                images[image] = inverse
        need(rep == min(images) and len(images) == rec['orbit_size'], 'invalid F orbit representative')
        need(not (set(images) & set(owner)), 'overlapping F orbits')
        for image, inverse in images.items():
            owner[image] = (rep, inverse)
        need(rec['lambda'] == [3 - x.bit_count() for x in f_neighbors(rep)], 'lambda mismatch')
        declared[rep] = {tuple(tuple(x) for x in p['stars']): p for p in rec['profiles']}
        need(len(declared[rep]) == len(rec['profiles']), 'duplicate declared profile')
    need(set(owner) == set(domain), 'incomplete F orbit cover')
    need(len(expected['catalog']) == expected['F_orbits'], 'F orbit count mismatch')
    observed = Counter()
    labeled = 0
    entry_comparisons = 0
    for mask in domain:
        rep, point = owner[mask]
        for stars in ordered_profiles(mask):
            a = formula(mask, stars)
            if any(x < 0 for row in a for x in row):
                continue
            mapped = [tuple(sorted(point[i] for i in s)) for s in stars]
            low_order = sorted(range(4), key=lambda i: mapped[i])
            canonical = tuple(mapped[i] for i in low_order)
            need(canonical in declared[rep], 'uncovered labeled local core')
            image = [low_order.index(i) for i in range(4)] + [4 + point[i] for i in range(6)]
            b = formula(rep, canonical)
            need(all(a[i][j] == b[image[i]][image[j]] for i in range(10) for j in range(10)),
                 'core relabeling changes a matrix entry')
            observed[(rep, canonical)] += 1
            labeled += 1
            entry_comparisons += 100
    need(labeled == expected['labeled_local_cores'], 'labeled core census mismatch')
    need(len(observed) == expected['normalized_profiles'], 'normalized profile count mismatch')
    for rec in expected['catalog']:
        rep = rec['F_mask']
        need({key[1] for key in observed if key[0] == rep} == set(declared[rep]), 'profile cover mismatch')
        for stars, profile in declared[rep].items():
            need(observed[(rep, stars)] == rec['orbit_size'] * profile['ordered_low_multiplicity'],
                 'profile multiplicity mismatch')
            a = formula(rep, stars)
            flag = all(a[i][j] >= 1 for i, j in combinations(range(4, 10), 2))
            need(flag == profile['all_cubic_row_compatible'], 'all-cubic row compatibility mismatch')
    return observed, {'labeled_local_cores_replayed': labeled,
                      'core_matrix_entries_compared': entry_comparisons}


def case_base(case):
    a = formula(case['F_mask'], case['stars'])
    row = set(case['row'])
    need(len(row) == 6 and row <= set(range(10)), 'invalid distinguished row')
    base = [[a[i][j] - int(i in row and j in row) for j in range(10)] for i in range(10)]
    need(all(x >= 0 for r in base for x in r), 'invalid row entry capacity')
    degrees = [sum(r) - 4 * r[i] for i, r in enumerate(base)]
    need(min(degrees) >= 0 and sum(degrees) == 16, 'invalid necessary slack degrees')
    need(degrees == case['slack_degrees'], 'slack degree mismatch')
    return base, degrees


def chosen_row_map(mask, stars, row, target):
    tf = target['F_mask']
    ts = [tuple(x) for x in target['stars']]
    target_row = set(target['row'])
    for point in POINT_MAPS:
        if transform(mask, point) != tf:
            continue
        if {4 + point[i - 4] for i in row if i >= 4} != {i for i in target_row if i >= 4}:
            continue
        mapped = [tuple(sorted(point[i] for i in s)) for s in stars]
        if sorted(mapped) != sorted(ts):
            continue
        for low in LOW_MAPS:
            if {low[i] for i in row if i < 4} != {i for i in target_row if i < 4}:
                continue
            if all(mapped[i] == ts[low[i]] for i in range(4)):
                return list(low) + [4 + point[i] for i in range(6)]
    return None


def cover_rows(observed, cases):
    counts, covered = Counter(), set()
    candidate_rows = 0
    for mask, stars in sorted(observed):
        a = formula(mask, stars)
        for row_tuple in combinations(range(10), 6):
            row = set(row_tuple)
            if any(a[i][j] == 0 for i, j in combinations(row_tuple, 2)):
                continue
            candidate_rows += 1
            k = len(row & set(range(4)))
            counts[str(k)] += 1
            need(k in (0, 3, 4), 'uncovered low-point composition')
            targets = [c for c in cases if (c['kind'] == 'zero_low' if k == 0 else
                         c['kind'] == 'three_low' if k == 3 else c['kind'].startswith('four_low'))]
            found = False
            for case in targets:
                if k == 0:
                    if mask != case['F_mask'] or stars != tuple(tuple(x) for x in case['stars']):
                        continue
                    image = list(range(10))
                else:
                    image = chosen_row_map(mask, stars, row, case)
                    if image is None:
                        continue
                target_base, target_degrees = case_base(case)
                base = [[a[i][j] - int(i in row and j in row) for j in range(10)] for i in range(10)]
                degrees = [sum(r) - 4 * r[i] for i, r in enumerate(base)]
                need(sorted(image) == list(range(10)), 'nonbijective selected-row relabeling')
                need(all(base[i][j] == target_base[image[i]][image[j]]
                         for i in range(10) for j in range(10)), 'row relabeling changes a residual entry')
                need(all(degrees[i] == target_degrees[image[i]] for i in range(10)),
                     'row relabeling changes the slack degrees')
                covered.add(case['index'])
                found = True
                break
            need(found, 'selected row missing from the 42-case cover')
    need(covered == set(range(len(cases))), 'unused or missing selected configurations')
    return {'admissible_six_point_rows_replayed': candidate_rows,
            'selected_rows_by_low_count': dict(sorted(counts.items())),
            'selected_configurations_covered': len(covered)}


def single_edge_weights(degrees, capacities):
    """Decide successive edge weights, with remaining-capacity pruning."""
    pairs = [(u, v, capacities[u][v]) for u, v in combinations(range(10), 2)
             if capacities[u][v] and degrees[u] and degrees[v]]
    n = len(pairs)
    future = [[0] * 10 for _ in range(n + 1)]
    pending = [[[] for _ in range(10)] for _ in range(n + 1)]
    for k in range(n - 1, -1, -1):
        u, v, cap = pairs[k]
        future[k] = future[k + 1][:]
        future[k][u] += cap
        future[k][v] += cap
        pending[k] = [r[:] for r in pending[k + 1]]
        pending[k][u].append((v, cap))
        pending[k][v].append((u, cap))
    remaining = list(degrees)
    chosen = []

    def visit(k):
        if any(remaining[i] > future[k][i] for i in range(10)):
            return
        if k == n:
            if not any(remaining):
                yield tuple(chosen)
            return
        u, v, cap = pairs[k]
        if k == 0 or pairs[k - 1][0] != u:
            if any(remaining[i] > sum(min(c, remaining[j]) for j, c in pending[k][i])
                   for i in range(10) if remaining[i]):
                return
        lo = max(0, remaining[u] - future[k + 1][u], remaining[v] - future[k + 1][v])
        hi = min(cap, remaining[u], remaining[v])
        for weight in range(lo, hi + 1):
            remaining[u] -= weight
            remaining[v] -= weight
            if weight:
                chosen.append((u, v, weight))
            yield from visit(k + 1)
            if weight:
                chosen.pop()
            remaining[u] += weight
            remaining[v] += weight
    yield from visit(0)


def validate_vectors(cert, cases):
    need(cert.get('dimension') == 10 and len(cert.get('records', [])) == len(cases), 'invalid certificate dimensions')
    for index, rec in enumerate(cert['records']):
        need(rec.get('index') == index and isinstance(rec.get('vectors'), list), 'invalid certificate case')
        need(len(rec['vectors']) == cases[index]['vectors'], 'certificate vector count mismatch')
        for v in rec['vectors']:
            need(isinstance(v, list) and len(v) == 10 and all(type(x) is int for x in v),
                 'malformed integer vector')
            need(any(v) and gcd(*v) == 1 and next(x for x in v if x) > 0, 'nonprimitive or zero vector')


def literal_residual(base, degrees, edges):
    used = [0] * 10
    out = [r[:] for r in base]
    for u, v, weight in edges:
        need(0 <= u < v < 10 and type(weight) is int and 0 < weight <= base[u][v], 'bad slack edge')
        used[u] += weight
        used[v] += weight
        out[u][v] -= weight
        out[v][u] -= weight
    need(used == degrees, 'wrong literal slack degrees')
    need(all(x >= 0 for r in out for x in r), 'negative literal residual entry')
    need(all(sum(r) == 4 * r[i] for i, r in enumerate(out)), 'literal row-sum bridge failed')
    return out


def qform(a, v):
    return sum(a[i][i] * v[i] * v[i] for i in range(10)) + 2 * sum(
        a[i][j] * v[i] * v[j] for i, j in combinations(range(10), 2))


def check_forms(matrix, vectors):
    need(any(qform(matrix, v) < 0 for v in vectors), 'matrix has no strict negative-form witness')


def baseline():
    data = (HERE / 'baseline21.rows').read_bytes()
    need(hashlib.sha256(data).hexdigest() == '4f1dd2bc743590a0553107936656e469db6e7d742db0456d697353ce50aac5ec',
         'baseline hash mismatch')
    lines = data.decode().splitlines()
    need(len(lines) == 21 and all(len(s) == 21 and set(s) <= {'0', '1'} for s in lines), 'bad baseline dimensions')
    red = [{j for j, x in enumerate(s) if x == '1'} for s in lines]
    need(all(i not in red[i] and all((j in red[i]) == (i in red[j]) for j in range(21))
             for i in range(21)), 'bad baseline adjacency')
    blue = [set(range(21)) - r - {i} for i, r in enumerate(red)]
    need(sum(map(len, red)) == 186, 'wrong baseline size')
    need(max(len(red[i] & red[j]) for i, j in combinations(range(21), 2) if j in red[i]) == 3,
         'baseline red cap failed')
    need(max(len(blue[i] & blue[j]) for i, j in combinations(range(21), 2) if j in blue[i]) == 6,
         'baseline blue cap failed')
    return 'verified existing 21-vertex construction, not a new construction'


def run(compare=False):
    expected = json.loads((HERE / 'expected.json').read_text())
    cert_bytes = (HERE / 'negative_vectors.json').read_bytes()
    need(hashlib.sha256(cert_bytes).hexdigest() == expected['negative_vectors_sha256'], 'certificate hash mismatch')
    cert = json.loads(cert_bytes)
    cases = expected['cases']
    need([c['index'] for c in cases] == list(range(len(cases))), 'invalid case indexing')
    validate_vectors(cert, cases)
    observed, stats = census(expected)
    stats.update(cover_rows(observed, cases))
    if compare:
        import generate
        actual_cases = list(generate.cases(expected['catalog']))
        need(len(actual_cases) == len(cases), 'generator case count mismatch')
        for i, c in enumerate(cases):
            need(all(actual_cases[i][k] == c[k] for k in ('kind', 'F_mask', 'stars', 'row')), 'generator case mismatch')
    total = Counter()
    whole_hash = hashlib.sha256()
    entries = 0
    for case, rec in zip(cases, cert['records']):
        base, degrees = case_base(case)
        states = sorted(single_edge_weights(degrees, base))
        need(len(states) == len(set(states)) == case['states'], 'slack state census mismatch')
        if compare:
            genbase, gendeg = generate.base_and_degrees(case)
            need(base == genbase and degrees == gendeg, 'generator base or degree mismatch')
            genstates = sorted(generate.weighted_stars(gendeg, genbase))
            need(states == genstates, 'complete slack state sets differ')
        digest = hashlib.sha256()
        for edges in states:
            matrix = literal_residual(base, degrees, edges)
            check_forms(matrix, rec['vectors'])
            if compare:
                need(matrix == generate.residual(genbase, edges), 'generator residual matrix entry mismatch')
                entries += 100
            data = (json.dumps([case['index'], edges, matrix], separators=(',', ':')) + '\n').encode()
            digest.update(data)
            whole_hash.update(data)
            total[case['kind']] += 1
        need(digest.hexdigest() == case['state_matrix_sha256'], 'case matrix hash mismatch')
    need(dict(sorted(total.items())) == expected['states_by_case_kind'], 'state-kind totals mismatch')
    need(sum(total.values()) == expected['states'] == expected['negative_forms'], 'state totals mismatch')
    need(whole_hash.hexdigest() == expected['state_matrix_sha256'], 'global matrix hash mismatch')
    vectors = [v for rec in cert['records'] for v in rec['vectors']]
    need(len(vectors) == expected['negative_vectors'] and max(abs(x) for v in vectors for x in v) ==
         expected['negative_vector_max_abs_entry'], 'certificate statistics mismatch')
    stats.update({'agent': 'six-books-3', 'role': 'researcher', 'complete': True,
                  'states': sum(total.values()), 'negative_forms': sum(total.values()),
                  'vectors': len(vectors), 'survivors': 0, 'baseline': baseline(),
                  'generator_comparison': compare, 'residual_matrix_entries_compared': entries,
                  'state_matrix_sha256': whole_hash.hexdigest()})
    return stats


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--compare-generator', action='store_true')
    args = parser.parse_args()
    print(json.dumps(run(args.compare_generator), sort_keys=True))


if __name__ == '__main__':
    main()
