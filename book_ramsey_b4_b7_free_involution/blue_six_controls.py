"""Exact author controls for BLUE_SIX.md; no computation is a proof premise.
Actual author: six-books-2, role researcher. Imports no campaign code.
Literal lifts sample arbitrary signs/blocks. The written proof covers all.
"""
import argparse
from itertools import combinations, product
import json
from pathlib import Path
from random import Random

Q = 11
PAIRS = tuple(combinations(range(Q), 2))
I = tuple(range(2, Q))


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def dot(a, b):
    return sum(x * y for x, y in zip(a, b))


def multiply(a, b):
    return [[sum(a[i][k] * b[k][j] for k in range(len(b)))
             for j in range(len(b[0]))] for i in range(len(a))]


def lift(w, s, inside):
    red = [0] * (2 * Q)

    def edge(i, j):
        red[i] |= 1 << j
        red[j] |= 1 << i

    for i in range(Q):
        if inside[i]:
            edge(2 * i, 2 * i + 1)
    for i, j in PAIRS:
        for a, b in product(range(2), repeat=2):
            if w[i][j] == 1 or (w[i][j] == 0 and (a == b) == (s[i][j] == 1)):
                edge(2 * i + a, 2 * j + b)
    blue = [((1 << (2 * Q)) - 1) ^ mask ^ (1 << i) for i, mask in enumerate(red)]
    return red, blue


def pages(red, blue, x, y):
    color_red = bool(red[x] >> y & 1)
    masks = red if color_red else blue
    return color_red, (masks[x] & masks[y]).bit_count()


def positive_control():
    """A genuine joint Gram/action solution, with all H spines within caps.
    The full graph has forbidden active leaf spines; it is not a witness.
    P is 2,3,4 and Q is 5,...,10. Blue is three disjoint P3 components.
    """
    w = [[0] * Q for _ in range(Q)]
    s = [[0] * Q for _ in range(Q)]

    def sign(i, j, value):
        s[i][j] = s[j][i] = value

    p, q = tuple(range(2, 5)), tuple(range(5, 11))
    sign(0, 1, 1)
    for i in I:
        sign(0, i, 1)
        sign(1, i, 1 if i in p else -1)
    for i, j in combinations(p, 2):
        sign(i, j, -1)
    for group, center in enumerate(p):
        other = [i for i in p if i != center]
        for bit in range(2):
            leaf = q[2 * group + bit]
            w[center][leaf] = w[leaf][center] = -1
            sign(other[0], leaf, 1 if bit == 0 else -1)
            sign(other[1], leaf, -1 if bit == 0 else 1)
    cycle = {tuple(sorted((q[i], q[(i + 1) % 6]))) for i in range(6)}
    for i, j in combinations(q, 2):
        sign(i, j, 1 if (i, j) in cycle else -1)
    red, blue = lift(w, s, [0] * Q)
    spines = 0
    for i, j in PAIRS:
        if i >= 2:
            continue
        for a, b in product(range(2), repeat=2):
            is_red, count = pages(red, blue, 2 * i + a, 2 * j + b)
            require(count == (3 if is_red else 6), 'joint positive control has exact H caps')
            spines += 1
    c = [s[i][2:] for i in range(2)]
    u = [sum(row) for row in w]
    k = [[s[i][j] + (3 + u[i] if i == j else 0) for j in I] for i in I]
    require([[dot(a, b) for b in c] for a in c] == [[9, -3], [-3, 9]],
            'feasible two-row Gram target')
    require(multiply(c, k) == [[-value for value in c[1]], [-value for value in c[0]]],
            'feasible joint row action')
    a, b = 2 * q[0], 2 * q[1]
    red_pages = pages(red, blue, a, b if s[q[0]][q[1]] == 1 else b + 1)[1]
    blue_pages = pages(red, blue, a, b + 1 if s[q[0]][q[1]] == 1 else b)[1]
    require(red_pages + blue_pages == 10 and (red_pages > 3 or blue_pages > 6),
            'positive necessary-system solution has forbidden active leaf spine')
    return w, s, spines


def row_normalization_control():
    count = 0
    for p in (-1, 1):
        for first in product((-1, 1), repeat=9):
            for positions in combinations(range(9), 3):
                c = tuple(1 if i in positions else -1 for i in range(9))
                second = tuple(p * a * b for a, b in zip(first, c))
                require(dot(first, second) == -3 * p, 'all Gram row pairs')
                normalized = tuple(p * a * b for a, b in zip(first, second))
                require(normalized == c and sum(normalized) == -3,
                        'both block signs normalize to the three/six split')
                count += 1
    require(count == 86016, 'complete two-row Gram/sign normalization domain')
    return count


def partitions(total, lower=1):
    if total == 0:
        yield ()
    for first in range(lower, total + 1):
        for tail in partitions(total - first, first):
            yield (first,) + tail


def degree_control():
    domain = [p for p in partitions(12) if len(p) <= 11]
    retained = [p for p in domain if len(p) + sum(d >= 3 for d in p) >= 10]
    expected = [(1,) * 10 + (2,), (1,) * 9 + (3,), (1,) * 8 + (2, 2),
                (1,) * 8 + (4,), (1,) * 7 + (2, 3), (1,) * 6 + (3, 3)]
    require(len(domain) == 76 and retained == expected, 'the six written degree sequences')
    return {'all_partitions': len(domain), 'degree_sum': 12, 'maximum_parts': 11,
            'v_plus_h_at_least_ten': [list(p) for p in retained], 'nongraphical_sequences_included': True}


def equality_shape_control():
    choices = tuple(combinations(range(6), 2))
    retained = 0
    for rows in product(choices, repeat=3):
        columns = [sum(i in row for row in rows) for i in range(6)]
        if all(c % 2 == 1 for c in columns):
            require(columns == [1] * 6, 'six edges force one neighbor per Q column')
            require(len(set().union(*map(set, rows))) == 6, 'three disjoint blue leaf pairs')
            retained += 1
    require(retained == 90, 'all ordered partitions of six leaves into three pairs')
    return {'row_degree_two_matrices': len(choices) ** 3,
            'all_columns_odd': retained, 'all_have_three_shared_blue_leaf_pairs': True}


def path_control():
    blue_edges = {(0, 1), (1, 2), (2, 3), (4, 5), (6, 7), (8, 9)}
    blue = [set() for _ in range(Q)]
    for i, j in blue_edges:
        blue[i].add(j)
        blue[j].add(i)
    candidates = [e for e in PAIRS if e not in blue_edges
                  and len(blue[e[0]] | blue[e[1]]) >= 3]
    require(len(candidates) == 12 and all(3 not in e for e in candidates),
            'path leaf has no possible red pair')
    for word in range(1 << len(candidates)):
        w = [[0] * Q for _ in range(Q)]
        for i, j in blue_edges:
            w[i][j] = w[j][i] = -1
        for bit, (i, j) in enumerate(candidates):
            if word >> bit & 1:
                w[i][j] = w[j][i] = 1
        require(w[1][3] == 0 and sum(w[1][i] * w[i][3] for i in range(Q)) == 1,
                'every red subset has the same impossible matching W-square entry')
    return {'permitted_red_candidates': [list(e) for e in candidates], 'all_red_subsets': 1 << len(candidates),
            'every_matching_path_entry_is_one': True}


def seven_blue_two_row_control():
    """Overcovers the three written seven-blue boundary cases without signs."""
    p, q = tuple(range(3)), tuple(range(3, 9))
    pairs = tuple(combinations(q, 2))

    def shared_leaves(edges):
        neighbors = [set() for _ in range(9)]
        for i, j in edges:
            neighbors[i].add(j)
            neighbors[j].add(i)
        return any(sum(len(neighbors[j]) == 1 for j in neighbors[i]) >= 2 for i in range(9))

    count_a = count_b = count_c = domain_c = 0
    for rows in product(pairs, repeat=3):
        columns = [sum(i in row for row in rows) for i in q]
        if columns != [1] * 6:
            continue
        cross = {(i, j) for i, row in zip(p, rows) for j in row}
        for extra in combinations(p, 2):
            require(shared_leaves(cross | {extra}), 'one extra P-P blue pair forces shared leaves')
            count_a += 1
        for extra in combinations(q, 2):
            require(shared_leaves(cross | {extra}), 'one extra Q-Q blue pair forces shared leaves')
            count_b += 1
    for red_p, red_q in product(p, q):
        others = [i for i in p if i != red_p]
        for first in combinations([i for i in q if i != red_q], 3):
            for second, third in product(pairs, repeat=2):
                domain_c += 1
                rows = {red_p: first, others[0]: second, others[1]: third}
                columns = [sum(i in row for row in rows.values()) + int(i == red_q) for i in q]
                if not all(c % 2 == 1 for c in columns):
                    continue
                require(sorted(columns) == [1, 1, 1, 1, 1, 3], 'unique three-link Q column')
                edges = {(i, j) for i, row in rows.items() for j in row}
                require(shared_leaves(edges), 'one P-Q red pair forces shared blue leaves')
                count_c += 1
    require((count_a, count_b, domain_c) == (270, 1350, 40500), 'seven-blue boundary domain counts')
    require(count_c > 0, 'nonvacuous third necessary unsigned domain')
    return {'one_P_P_blue_pair_cases': count_a, 'one_Q_Q_blue_pair_cases': count_b,
            'one_P_Q_red_pair_domain': domain_c, 'odd_Q_columns_in_third_case': count_c,
            'all_retained_cases_have_shared_blue_leaves': True}


def literal_controls():
    counts = {'lifts': 0, 'matching_spines': 0, 'H_matching_spines': 0,
              'H_inside_spines': 0, 'cross_action_residual_entries': 0,
              'H_Gram_residual_entries': 0, 'uniform_spine_sums': 0,
              'switched_lift_rows': 0}
    for pattern, seed, bsign, inside_word in product(range(4), range(8), (-1, 1), range(4)):
        rng = Random(seed)
        w = [[0] * Q for _ in range(Q)]
        s = [[0] * Q for _ in range(Q)]
        for i, j in PAIRS:
            value = 0 if i < 2 else (0, 1, -1, rng.choice((-1, 0, 1)))[pattern]
            w[i][j] = w[j][i] = value
            if value == 0:
                s[i][j] = s[j][i] = bsign if (i, j) == (0, 1) else rng.choice((-1, 1))
        inside = [inside_word >> i & 1 if i < 2 else rng.randrange(2) for i in range(Q)]
        red, blue = lift(w, s, inside)
        u = [sum(row) for row in w]
        w2, s2 = multiply(w, w), multiply(s, s)
        for i, j in PAIRS:
            if w[i][j] == 0:
                for a, b in product(range(2), repeat=2):
                    is_red, actual = pages(red, blue, 2 * i + a, 2 * j + b)
                    signed = u[i] + u[j] + s[i][j] * s2[i][j]
                    require(2 * actual == 9 + w2[i][j] + (signed if is_red else -signed),
                            'literal general matching-page identity')
                    counts['matching_spines'] += 1
                    if i < 2:
                        counts['H_matching_spines'] += 1
                if i < 2:
                    a = 2 * i
                    red_endpoint = 2 * j + int(s[i][j] == -1)
                    blue_endpoint = 2 * j + int(s[i][j] == 1)
                    require(pages(red, blue, a, red_endpoint)[1]
                            + pages(red, blue, a, blue_endpoint)[1] == 9,
                            'H matching pairs have fixed nine-page combined sum')
            else:
                color = w[i][j] == 1
                masks = red if color else blue
                actual = sum((masks[2 * i] & masks[2 * j + a]).bit_count() for a in range(2))
                outside = sum((1 + (w[i][k] if color else -w[i][k]))
                              * (1 + (w[j][k] if color else -w[j][k]))
                              for k in range(Q) if k not in (i, j))
                extra = 2 * (inside[i] + inside[j] if color else 2 - inside[i] - inside[j])
                require(actual == outside + extra, 'literal uniform sums including inside colors')
                counts['uniform_spine_sums'] += 1
        c = [s[h][2:] for h in range(2)]
        k = [[s[i][j] + (3 + u[i] if i == j else 0) for j in I] for i in I]
        ck = multiply(c, k)
        for h, i in product(range(2), I):
            residual = ck[h][i - 2] + bsign * c[1 - h][i - 2]
            red_pages = pages(red, blue, 2 * h, 2 * i + int(s[h][i] == -1))[1]
            require(residual == 2 * s[h][i] * (red_pages - 3),
                    'literal cross-row action residual')
            counts['cross_action_residual_entries'] += 1
        rhh = pages(red, blue, 0, 2 + int(bsign == -1))[1]
        require(dot(c[0], c[1]) + 3 * bsign == 2 * bsign * (rhh - 3),
                'literal two-row Gram residual')
        counts['H_Gram_residual_entries'] += 1
        for h in range(2):
            require(pages(red, blue, 2 * h, 2 * h + 1)[1] == 0,
                    'H inside edges have no pages at either inside color')
            counts['H_inside_spines'] += 1
        switches = [rng.choice((-1, 1)) for _ in range(Q)]
        switched = [[switches[i] * s[i][j] * switches[j] for j in range(Q)] for i in range(Q)]
        sr, _ = lift(w, switched, inside)
        permutation = [2 * i + (a ^ int(switches[i] == -1))
                       for i in range(Q) for a in range(2)]
        for v in range(2 * Q):
            image_mask = sum(1 << permutation[j] for j in range(2 * Q) if red[v] >> j & 1)
            require(sr[permutation[v]] == image_mask, 'switching is a full color-preserving relabeling')
            counts['switched_lift_rows'] += 1
        counts['lifts'] += 1
    require(counts['lifts'] == 256 and counts['H_matching_spines'] == 19456
            and counts['cross_action_residual_entries'] == 4608,
            'complete deterministic literal-control domain')
    return counts


def run_controls():
    _, _, positive_spines = positive_control()
    return {'agent': 'six-books-2', 'role': 'researcher', 'complete': True,
            'written_analytic_proof': 'BLUE_SIX.md',
            'controls_not_theorem_premise': True,
            'two_row_Gram_normalizations': row_normalization_control(),
            'joint_Gram_action_positive_control': True,
            'positive_control_H_spines_at_exact_caps': positive_spines,
            'positive_control_is_not_valid_full_witness': True,
            'literal_controls': literal_controls(), 'degree_budget': degree_control(),
            'six_blue_equality_shape': equality_shape_control(),
            'seven_blue_two_row_boundary': seven_blue_two_row_control(),
            'P4_plus_three_blue_edges': path_control(),
            'sample_outside_blocks': ['all_matching', 'all_red', 'all_blue', 'mixed'],
            'full_matching_sign_enumeration': False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--emit', action='store_true', help='regenerate without reading the compact fixture')
    args = parser.parse_args()
    actual = run_controls()
    if not args.emit:
        expected = json.loads(Path(__file__).with_name('blue_six_expected.json').read_text())
        require(actual == expected, 'exact expected-summary mismatch')
    print(json.dumps(actual, indent=2))


if __name__ == '__main__':
    main()
