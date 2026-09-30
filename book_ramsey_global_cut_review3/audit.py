#!/usr/bin/env python3
"""six-reviewer-3: independent literal-page and restricted-domain audit.

Standard-library exact arithmetic. No researcher executable is imported.
Input fixtures and compact survivor certificates are explicitly attributed.
See REVIEW.md for completeness proofs and the external literature boundary.
"""
import argparse
from collections import Counter
from fractions import Fraction
from hashlib import sha256
from itertools import combinations, product
import json
from math import comb, lcm
from pathlib import Path


def require(ok, reason):
    if not ok:
        raise ValueError(reason)


def decode(rows):
    n = len(rows)
    require(all(len(row) == n and set(row) <= {'0', '1'} for row in rows),
            'invalid binary square')
    require(all(rows[i][i] == '0' for i in range(n)), 'nonzero diagonal')
    require(all(rows[i][j] == rows[j][i] for i, j in combinations(range(n), 2)),
            'asymmetric input')
    return [{j for j, x in enumerate(row) if x == '1'} for row in rows]


def edge(adj, i, j):
    adj[i].add(j)
    adj[j].add(i)


def literal_identities(local, mode):
    require(sorted(map(len, local)) == [2] + [3] * 10, 'wrong local degrees')
    A = set(range(11))
    x = next(i for i in A if len(local[i]) == 2)
    adj = [v.copy() for v in local] + [set() for _ in range(11)]
    for i in A:
        edge(adj, 11, i)
    # Every miss size appears, including both ends. These are identity controls,
    # possibly with negative capacities, not valid Ramsey colorings.
    for b in range(10):
        size = (b + mode) % 12
        order = sorted(A, key=lambda i: ((5 * i + 3 * b + mode) % 11, i))
        for i in A - set(order[:size]):
            edge(adj, i, 12 + b)
    for b, c in combinations(range(10), 2):
        if (b * 7 + c * 11 + mode) % 7 < 3:
            edge(adj, 12 + b, 12 + c)
    blue = [set(range(22)) - {i} - adj[i] for i in range(22)]
    Z = [A - adj[b] for b in range(12, 22)]
    t = [sum(i in z for z in Z) for i in A]
    eps = {}
    for i, j in combinations(range(11), 2):
        color, cap = (adj, 3) if j in adj[i] else (blue, 6)
        eps[i, j] = cap - len(color[i] & color[j])
    U = sum(eps.values())
    UR = sum(eps[i, j] for i, j in eps if j in local[i])
    F = sum((len(z) - 3) * (len(z) - 4) // 2 for z in Z)
    K = sum((len(z) - 4) * (len(z) - 5) // 2 for z in Z)
    Q = sum(sum(j in local[i] for i, j in combinations(sorted(z), 2)) for z in Z)
    T = sum(b in local[a] and c in local[a] and c in local[b]
            for a, b, c in combinations(range(11), 3))
    require(U + F + t[x] == 10, 'first residual budget')
    require(sum(t) == 40 + F - K, 'miss conservation')
    require(3 * (U + K + T) + UR + Q == 22 - 4 * t[x], 'second budget')
    row_errors = []
    for i in range(11):
        h = len(local[i])
        require(len(adj[i]) == 11 + h - t[i], 'degree bridge')
        ei = sum(eps[min(i, j), max(i, j)] for j in A - {i})
        ui = sum(len(z) - 4 for z in Z if i in z)
        Pt = sum(t[j] for j in local[i])
        Ph = sum(len(local[j]) for j in local[i])
        left = (3 - h) * t[i] - Pt
        right = 5 * h - h * h + 2 - 2 * Ph - ei - ui
        require(left == right, 'row identity, +2 included')
        row_errors.append(left - (right - 2))
        for j in A - {i}:
            S = sum(i in z and j in z for z in Z)
            common = len(local[i] & local[j])
            if j in local[i]:
                expected = t[i] + t[j] - 8 - common
            else:
                expected = h + len(local[j]) - 3 - common
            require(S == expected - eps[min(i, j), max(i, j)], 'pair-miss identity')
    require(set(row_errors) == {2}, 'missing +2 mutation was not detected')
    return [T, U, UR, F, K, Q, t[x], sum(t)]


def inverse(matrix):
    n = len(matrix)
    aug = [[Fraction(x) for x in row] + [Fraction(i == j) for j in range(n)]
           for i, row in enumerate(matrix)]
    for col in range(n):
        pivot = next((i for i in range(col, n) if aug[i][col]), None)
        require(pivot is not None, 'singular incidence Gram')
        aug[col], aug[pivot] = aug[pivot], aug[col]
        p = aug[col][col]
        aug[col] = [x / p for x in aug[col]]
        for i in range(n):
            if i != col:
                p = aug[i][col]
                aug[i] = [x - p * y for x, y in zip(aug[i], aug[col])]
    return [row[n:] for row in aug]


def column_domain(H):
    # Orthogonal projection via (N N^T)^(-1), independent of triangle propagation.
    gram = [[sum(i in e and j in e for e in H) for j in range(7)] for i in range(7)]
    inv = inverse(gram)
    denominator = lcm(*(x.denominator for row in inv for x in row))
    integer_inv = [[int(x * denominator) for x in row] for row in inv]
    retained = []
    for chosen in combinations(range(14), 6):
        chosen = set(chosen)
        rhs = [sum(i in H[j] for j in chosen) for i in range(7)]
        numerators = [sum(a * b for a, b in zip(row, rhs)) for row in integer_inv]
        if all(numerators[a] + numerators[b] == denominator * (j in chosen)
               for j, (a, b) in enumerate(H)):
            retained.append(sum(1 << j for j in chosen))
    require(len(retained) == 7, 'incidence-image binary domain')
    return sorted(retained), denominator


PAIRS7 = list(combinations(range(7), 2))
ALL22 = (1 << 22) - 1


def template(Q):
    H = [e for e in PAIRS7 if e not in Q]
    adj = [0] * 22

    def add(i, j):
        adj[i] |= 1 << j
        adj[j] |= 1 << i

    for b in range(7):
        add(0, 15 + b)
    for a, c in combinations(range(14), 2):
        if not set(H[a]) & set(H[c]):
            add(1 + a, 1 + c)
    for a, b in product(range(14), range(7)):
        if not set(H[a]) & set(Q[b]):
            add(1 + a, 15 + b)
    return H, adj


def verify_book(adj, spine, pages):
    i, j = spine
    red = bool(adj[i] >> j & 1)
    require(len(set(spine + pages)) == len(spine + pages), 'repeated book vertex')
    require(len(pages) == (4 if red else 7), 'incorrect book order')
    for p in pages:
        require(bool(adj[i] >> p & 1) == red and bool(adj[j] >> p & 1) == red,
                'page is not common in spine color')


def uniform_case(Q, reference):
    require(Q == sorted(set(Q)) and len(Q) == 7 and
            all(0 <= a < b < 7 for a, b in Q) and
            all(sum(i in e for e in Q) == 2 for i in range(7)),
            'invalid simple two-regular complement')
    H, base = template(Q)
    columns, denominator = column_domain(H)
    literal_columns = sorted(sum(((base[1+a] >> (15+b)) & 1) << a for a in range(14))
                             for b in range(7))
    require(columns == literal_columns == reference['column_masks'], 'column set differs')
    P = [sum((bool(set(H[a]) & set(H[b])) and a != b) << b for b in range(14))
         for a in range(14)]
    for a, b in product(range(14), repeat=2):
        gram_entry = (base[1+a] & base[1+b] & (ALL22 ^ ((1 << 15)-1))).bit_count()
        predicted = 3 + 6*(a == b) + ((P[a] >> b) & 1) - (P[a] & P[b]).bit_count()
        require(gram_entry == predicted, 'uniform incidence Gram bridge')
    # A red B-pair already has root0 and all its red A-pages. If there are
    # three A-pages it is impossible before any B-edges are chosen.
    allowed = [p for p, (b, c) in enumerate(PAIRS7)
               if (base[15+b] & base[15+c] & ((1 << 15) - 2)).bit_count() <= 2]
    require(len(allowed) in (14, 17), 'static forbidden-edge reduction')
    supplied_records = {r[0]: r for r in reference['book_records']}
    require(len(supplied_records) == len(reference['book_records']), 'duplicate survivor mask')
    survivors = []
    root_count = 0
    records = []
    cross_spines = 0
    for reduced in range(1 << len(allowed)):
        adj = base.copy()
        mask = 0
        for bidx, p in enumerate(allowed):
            if reduced >> bidx & 1:
                b, c = PAIRS7[p]
                adj[15+b] |= 1 << (15+c)
                adj[15+c] |= 1 << (15+b)
                mask |= 1 << p
        if any((adj[0] & adj[15+b]).bit_count() > 3 for b in range(7)):
            continue
        root_count += 1
        blue = [ALL22 ^ adj[i] ^ (1 << i) for i in range(22)]
        valid = True
        for b, c in PAIRS7:
            i, j = 15+b, 15+c
            color, cap = (adj, 3) if adj[i] >> j & 1 else (blue, 6)
            if (color[i] & color[j]).bit_count() > cap:
                valid = False
                break
        if not valid:
            continue
        survivors.append(mask)
        red_bad = blue_bad = 0
        for a, b in product(range(1, 15), range(15, 22)):
            red = bool(adj[a] >> b & 1)
            color, cap = (adj, 3) if red else (blue, 6)
            common = color[a] & color[b]
            cross_spines += 1
            if common.bit_count() > cap:
                red_bad += red
                blue_bad += not red
                book = [p for p in range(22) if common >> p & 1][:cap+1]
                verify_book(adj, [a, b], book)
        require(red_bad + blue_bad > 0, 'valid completion survived')
        records.append([mask, red_bad, blue_bad])
        require(mask in supplied_records, 'missing survivor certificate')
        supplied = supplied_records[mask]
        require([mask, red_bad, blue_bad] == supplied[:3], 'literal defect count differs')
        verify_book(adj, supplied[3], supplied[4])
    require(sorted(survivors) == sorted(r[0] for r in reference['book_records']),
            'complete finite survivor set differs')
    by_edges = Counter(mask.bit_count() for mask in survivors)
    return {'allowed_B_edges': len(allowed), 'enumerated_subsets': 1 << len(allowed),
            'root_permitted_in_restricted_domain': root_count,
            'B_pair_survivors_by_edges': [[k, v] for k, v in sorted(by_edges.items())],
            'B_pair_survivors': len(survivors), 'valid_completions': 0,
            'cross_spines_checked': cross_spines, 'weight_six_columns_tested': comb(14, 6),
            'incidence_Gram_entries_checked': 196,
            'image_columns': columns, 'Gram_inverse_denominator': denominator,
            'defect_records_sha256': sha256(json.dumps(sorted(records), separators=(',', ':')).encode()).hexdigest()}


def region_states(n, sizes):
    # Pair of subsets described only by their two sizes and intersection.
    # Weight is its exact count of labeled realizations, no symmetry quotient.
    for a, b in product(sizes, repeat=2):
        for common in range(max(0, a+b-n), min(a, b)+1):
            yield (a, b, common, comb(n, a) * comb(a, common) * comb(n-a, b-common))


def joint_root():
    result = []
    for k in (10, 11):
        states = degree_pass = cap_pass = final_pass = 0
        for V, X, D in product(region_states(8, [1]),
                               region_states(k-3, [0, 1]),
                               region_states(13-k, range(14-k))):
            weight = V[3] * X[3] * D[3]
            states += weight
            da = 3 + V[0] + X[0] + D[0]
            db = 3 + V[1] + X[1] + D[1]
            if min(da, db) < 7:
                continue
            degree_pass += weight
            codegree = 2 + V[2] + X[2] + D[2]
            if codegree > 3:
                continue
            cap_pass += weight
            require(k == 10 and da == db == 7 and codegree == 3,
                    'unexpected joint-root remaining state')
            # Capacity cut at the degree7 root a, red neighbor b.
            if db - 1 - codegree >= 6:
                final_pass += weight
        require(final_pass == 0, 'joint-root capacity contradiction fails')
        # c=0: largest possible red union in each region; each endpoint
        # has precisely2 V neighbors and at most2 X neighbors.
        common_blue_min = 8 - min(8, 4) + (k-3) - min(k-3, 4)
        require(common_blue_min > 6, 'blue joint-root case survived')
        result.append({'exceptional_degree': k, 'red_case_subset_pairs': states,
                       'degree_pass': degree_pass, 'red_spine_pass': cap_pass,
                       'degree7_capacity_pass': final_pass,
                       'blue_case_minimum_pages': common_blue_min})
    return result


def boundary_checks():
    upper = []
    max_edges = 0
    for n7, n8, n9, n11 in product(range(23), repeat=4):
        n10 = 22 - n7 - n8 - n9 - n11
        if n10 < 0:
            continue
        twice = 7*n7 + 8*n8 + 9*n9 + 10*n10 + 11*n11
        if twice % 2 or 98*n11 > 3*twice:
            continue
        if n11 and (not n9 or n7 or twice < 212):
            continue
        max_edges = max(max_edges, twice // 2)
        if twice == 224:
            upper.append([n7, n8, n9, n10, n11])
    require(sorted(upper) == [[0, 0, 1, 16, 5], [0, 0, 2, 14, 6]] and max_edges == 112,
            'universal upper edge/histogram cut')
    local = []
    lower = []
    # Enumerate weak degree-count partitions directly, rather than 4^10 vectors.
    for n8, n9 in product(range(11), repeat=2):
        n10 = 10 - n8 - n9
        deficiency = 2*n8 + n9
        if n10 < 0 or deficiency > 2:
            continue
        local.append([n8, n9, n10])
        if deficiency == 2:
            lower.append([0, n8, n9+7, n10+4, 1])
    require(sorted(lower) == [[0, 0, 9, 12, 1], [0, 1, 7, 13, 1]], '106 equality histograms')
    # Literal small simple-graph test of component orders1,3,5.
    component_counts = {}
    for n in (1, 3, 5):
        pairs = list(combinations(range(n), 2))
        count = 0
        for mask in range(1 << len(pairs)):
            adj = [set() for _ in range(n)]
            for bit, (a, b) in enumerate(pairs):
                if mask >> bit & 1:
                    edge(adj, a, b)
            if sorted(map(len, adj)) != [2] + [3]*(n-1):
                continue
            if not any(b in adj[a] and c in adj[a] and c in adj[b]
                       for a, b, c in combinations(range(n), 3)):
                count += 1
        require(count == 0, 'small triangle-free component counterexample')
        component_counts[str(n)] = count
    require([z for z in range(12) if (z-4)*(z-5)//2 <= 2] == [3, 4, 5, 6],
            'miss size boundary')
    load_cuts = {}
    for d in (8, 9, 10):
        feasible = [(m, p) for m in range(7) for p in range(m+1)
                    if (d == 9 or p == 0) and 6*m-p <= 3*d]
        load_cuts[str(d)] = max(m for m, p in feasible)
    require(load_cuts == {'8': 4, '9': 5, '10': 5}, 'proved high-vertex load cuts')
    return {'upper_edges': max_edges, '112_histograms': sorted(upper),
            '106_histograms_with_degree11': sorted(lower), 'local_cubic_neighbor_histograms': sorted(local),
            'small_triangle_free_exceptional_component_counts': component_counts,
            'maximum_high_degree_neighbors_by_full_degree': load_cuts}


def audit(data):
    require(data['schema'] == 'book-global-cut-review3-v1', 'wrong input schema')
    stream = sha256()
    triangles = Counter()
    controls = 0
    for fixture in data['local_fixtures']:
        local = decode(fixture['rows'])
        for mode in range(24):
            values = literal_identities(local, mode)
            stream.update(json.dumps(values, separators=(',', ':')).encode() + b'\n')
            triangles[values[0]] += 1
            controls += 1
    require(controls == 144, 'identity control count')
    cases = {}
    canonical_Q = {'C7': sorted(tuple(sorted((i, (i+1) % 7))) for i in range(7)),
                   'C3+C4': [(0, 1), (0, 2), (1, 2), (3, 4), (3, 6), (4, 5), (5, 6)]}
    require({case['name'] for case in data['uniform_templates']} == set(canonical_Q)
            and len(data['uniform_templates']) == 2, 'template coverage')
    for case in data['uniform_templates']:
        Q = [tuple(e) for e in case['Q_edges']]
        require(Q == canonical_Q[case['name']], 'template is not the canonical point graph')
        cases[case['name']] = uniform_case(Q, case)
    return {'agent': 'six-reviewer-3', 'role': 'independent mathematical reviewer',
            'literal_identity_graphs': controls, 'pair_identities': controls*55,
            'row_identities': controls*11, 'missing_plus_two_detected_rows': controls*11,
            'local_triangle_histogram': [[k, v] for k, v in sorted(triangles.items())],
            'identity_stream_sha256': stream.hexdigest(), 'joint_root': joint_root(),
            'boundaries': boundary_checks(), 'uniform_dependency': cases}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--emit', action='store_true', help='print independently computed compact output')
    args = parser.parse_args()
    root = Path(__file__).resolve().parent
    result = audit(json.loads((root / 'INPUT.json').read_text()))
    if not args.emit:
        require(result == json.loads((root / 'expected.json').read_text()), 'expected output differs')
    print(json.dumps(result, sort_keys=True, separators=(',', ':')))
