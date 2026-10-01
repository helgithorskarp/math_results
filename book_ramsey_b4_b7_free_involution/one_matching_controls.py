"""Exact author controls for ONE_MATCHING.md; no finite theorem premise.
Actual author six-books-2, role researcher. Standard library, no campaign imports.
Three cubic templates and sampled markings do not classify all skeletons.
"""
import argparse
from itertools import combinations, product
import json
from pathlib import Path
from random import Random

N = 10
PAIRS = tuple(combinations(range(N), 2))
TRIPLES = tuple(combinations(range(N), 3))


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def matrix(edges, diagonal=None):
    result = [[0] * N for _ in range(N)]
    for i, j in edges:
        result[i][j] = result[j][i] = 1
    if diagonal is not None:
        for i, value in enumerate(diagonal):
            result[i][i] = value
    return result


def multiply(a, b):
    return [[sum(a[i][k] * b[k][j] for k in range(N))
             for j in range(N)] for i in range(N)]


def add(a, b):
    return [[x + y for x, y in zip(ar, br)] for ar, br in zip(a, b)]


def templates():
    cycle = {tuple(sorted((i, (i + 1) % 10))) for i in range(10)}
    ladder = cycle | {(i, i + 5) for i in range(5)}
    petersen = ({tuple(sorted((i, (i + 1) % 5))) for i in range(5)}
                | {(i, i + 5) for i in range(5)}
                | {tuple(sorted((5 + i, 5 + (i + 2) % 5))) for i in range(5)})
    split = set(combinations(range(4), 2)) | {(i, j) for i in range(4, 7) for j in range(7, 10)}
    return [('Petersen', petersen), ('ten_cycle_opposite_matching', ladder), ('K4_disjoint_K33', split)]


def system(a_edges, r_edges, d_edges, inside):
    require(len(a_edges) == 15 and all(sum(i in e for e in a_edges) == 3 for i in range(N)),
            'template is simple cubic')
    require(r_edges <= a_edges and d_edges <= set(PAIRS) - a_edges, 'disjoint correct markings')
    a = matrix(a_edges)
    e = matrix(set(PAIRS) - a_edges)
    c = matrix(((set(PAIRS) - a_edges) | r_edges) - d_edges, inside)
    red_degrees = [sum(i in edge for edge in r_edges) for i in range(N)]
    blue_degrees = [sum(i in edge for edge in d_edges) for i in range(N)]
    q_aaa = q_aad = q_add = 0
    mark_counts = set()
    for i, j, k in TRIPLES:
        edges = [(i, j), (i, k), (j, k)]
        a_count = sum(edge in a_edges for edge in edges)
        if a_count == 3:
            q = sum(edge in r_edges for edge in edges)
            q_aaa += 6 - 2 * q + q * (q - 1) // 2
            mark_counts.add(q)
        elif a_count == 2 and any(edge in d_edges for edge in edges):
            q_aad += 2 - sum(edge in r_edges for edge in edges)
        elif a_count == 1 and sum(edge in d_edges for edge in edges) == 2:
            q_add += 1
    q_inside = sum(r * flag for r, flag in zip(red_degrees, inside))
    q_parts = [q_aaa, q_aad, q_add, q_inside]
    m = add(multiply(a, a), multiply(c, c))
    total = sum(m[i][j] for i, j in a_edges)
    require(min(q_parts) >= 0, 'nonnegative triangle/inside components')
    require(total == 60 + 4 * len(r_edges) - 6 * len(d_edges) + sum(q_parts),
            'aggregate matrix versus independently counted triple identity')
    f_blue = [[1 - c[i][j] for j in range(N)] for i in range(N)]
    return {'A': a, 'E': e, 'C': c, 'M': m, 'Q_parts': q_parts,
            'red_degree': red_degrees, 'blue_degree': blue_degrees,
            'red_cross': add(multiply(a, c), multiply(c, a)),
            'blue_same': add(multiply(e, e), multiply(f_blue, f_blue)),
            'blue_cross': add(multiply(e, f_blue), multiply(f_blue, e)),
            'AAA_mark_counts': mark_counts}


def literal_lift(a_edges, r_edges, d_edges, inside, h_inside):
    """Build literal two-point blocks, independently of matrix products."""
    red = [set() for _ in range(22)]

    def edge(i, j):
        red[i].add(j)
        red[j].add(i)

    for i, flag in enumerate([*inside, h_inside]):
        if flag:
            edge(2 * i, 2 * i + 1)
    for i in range(N):
        edge(20, 2 * i)
        edge(21, 2 * i + 1)
    for i, j in PAIRS:
        for x, y in product(range(2), repeat=2):
            if (i, j) in r_edges or ((i, j) not in d_edges and (x == y) == ((i, j) in a_edges)):
                edge(2 * i + x, 2 * j + y)
    blue = [set(range(22)) - {i} - red[i] for i in range(22)]
    return red, blue


def relabel(red, bits):
    permutation = [2 * i + (x ^ bits[i]) for i in range(11) for x in range(2)]
    changed = [set() for _ in range(22)]
    for v in range(22):
        changed[permutation[v]] = {permutation[j] for j in red[v]}
    return changed


def check_literal(a_edges, r_edges, d_edges, inside, h_inside, s, rng):
    red, blue = literal_lift(a_edges, r_edges, d_edges, inside, h_inside)
    counts = {'h_cross_spines': 0, 'I_layer_spines': 0, 'I_cross_spines_including_inside': 0,
              'h_inside_spines': 0, 'normalized_adjacency_rows': 0}
    for v in range(22):
        require({j ^ 1 for j in red[v]} == red[v ^ 1], 'literal full color involution')
    for i in range(N):
        ri, bi = s['red_degree'][i], s['blue_degree'][i]
        require(len(red[2 * i]) == len(red[2 * i + 1]) == 10 + ri - bi + inside[i],
                'actual red degree')
        matching_sum = sum(1 if edge in a_edges else -1 for edge in PAIRS
                           if i in edge and edge not in r_edges and edge not in d_edges)
        require(matching_sum + 3 + ri - bi == 0, 'single-H normalized row action')
        for x, y in product(range(2), repeat=2):
            v, w = 20 + x, 2 * i + y
            masks = red if w in red[v] else blue
            require(len(masks[v] & masks[w]) == (3 if masks is red else 6), 'exact h spine caps')
            counts['h_cross_spines'] += 1
    for i, j in PAIRS:
        for bit in range(2):
            v, w = 2 * i + bit, 2 * j + bit
            is_red = w in red[v]
            masks = red if is_red else blue
            predicted = 1 + (s['M'][i][j] if is_red else s['blue_same'][i][j])
            require(len(masks[v] & masks[w]) == predicted, 'literal same-layer page identity')
            counts['I_layer_spines'] += 1
    for i, j in product(range(N), repeat=2):
        v, w = 2 * i, 2 * j + 1
        is_red = w in red[v]
        masks = red if is_red else blue
        predicted = s['red_cross'][i][j] if is_red else s['blue_cross'][i][j]
        require(len(masks[v] & masks[w]) == predicted, 'literal cross-layer page identity')
        if i == j:
            require(predicted == 2 * (s['red_degree'][i] if is_red else s['blue_degree'][i]),
                    'literal arbitrary-color inside pages')
        counts['I_cross_spines_including_inside'] += 1
    masks = red if h_inside else blue
    require(len(masks[20] & masks[21]) == 0, 'h inside spine has zero pages')
    require(len(red[20]) == len(red[21]) == 10 + h_inside, 'arbitrary h inside degree')
    require(sum(map(len, red)) // 2 == 110 + 2 * (len(r_edges) - len(d_edges)) + sum(inside) + h_inside,
            'actual total red edges')
    counts['h_inside_spines'] += 1
    changed = relabel(red, [rng.randrange(2) for _ in range(11)])
    normalize = [int(2 * i not in changed[20]) for i in range(N)] + [0]
    restored = relabel(changed, normalize)
    require(restored == red, 'normalization recovers all red adjacency rows')
    counts['normalized_adjacency_rows'] += 22
    require(sum(counts[k] for k in counts if 'spines' in k) == 231, 'all22-vertex spines audited')
    return counts


def positive_control():
    x, y, u, v = range(3), range(3, 6), range(6, 8), range(8, 10)
    r_edges = {(i, i + 3) for i in x}
    a_edges = r_edges | {(i, j) for i in x for j in u} | {(i, j) for i in y for j in v}
    d_edges = {(i, 3 + (i + 1) % 3) for i in x} | {(i, j) for i in u for j in v}
    s = system(a_edges, r_edges, d_edges, [0] * N)
    require(s['Q_parts'] == [0] * 4 and all(s['M'][i][j] == 2 for i, j in a_edges),
            'joint aggregate and individual-red-layer equality positive control')
    require(all(s['red_cross'][i][j] == 4 for i, j in r_edges), 'forbidden isolated-red cross spines')
    require(all(r + b > 0 for r, b in zip(s['red_degree'], s['blue_degree'])),
            'positive control uniform support ten')
    for h_inside in range(2):
        check_literal(a_edges, r_edges, d_edges, [0] * N, h_inside, s, Random(h_inside))
    return {'explicit_A_edges': [list(e) for e in sorted(a_edges)],
            'explicit_R_edges': [list(e) for e in sorted(r_edges)],
            'explicit_D_edges': [list(e) for e in sorted(d_edges)], 'all_I_inside_blue': True,
            'Q_parts': s['Q_parts'], 'all_fifteen_A_entries_equal_two': True,
            'both_h_inside_colors': True, 'literal_positive_control_spines': 462,
            'uniform_support': 10, 'isolated_red_cross_pages': [4, 4, 4],
            'not_valid_full_witness': True}


def red_shape_control():
    counts = {'three_isolated_edges': 0, 'path_two_plus_isolated_edge': 0,
              'red_triangle': 0, 'red_star': 0, 'red_path_four': 0}
    for es in combinations(tuple(combinations(range(6), 2)), 3):
        degree = [sum(i in edge for edge in es) for i in range(6)]
        isolated_edge = any(degree[i] == degree[j] == 1 for i, j in es)
        positive = sorted(d for d in degree if d)
        if isolated_edge:
            kind = 'three_isolated_edges' if positive == [1] * 6 else 'path_two_plus_isolated_edge'
        elif positive == [2, 2, 2]:
            kind = 'red_triangle'
        elif positive == [1, 1, 1, 3]:
            kind = 'red_star'
        else:
            require(positive == [1, 1, 2, 2], 'remaining written three-edge form is P4')
            kind = 'red_path_four'
        counts[kind] += 1
    require(counts == {'three_isolated_edges': 15, 'path_two_plus_isolated_edge': 180,
                       'red_triangle': 20, 'red_star': 60, 'red_path_four': 180},
            'complete stated three-edge control domain')
    return {'all_three_edge_sets_on_six_vertices': 455, 'shape_counts': counts,
            'only_star_or_path_after_written_cuts': True}


def core_degree_control():
    results = {}
    for name, r, edges in [('star', [3, 1, 1, 1], [(0, 1), (0, 2), (0, 3)]),
                           ('path', [1, 2, 2, 1], [(0, 1), (1, 2), (2, 3)])]:
        kept = []
        for b in product(range(4), repeat=4):
            t = [x - y for x, y in zip(b, r)]
            if any(t[i] + t[j] != 0 for i, j in edges) or 14 - sum(b) < 6:
                continue
            kept.append(list(b))
        expected = [[2, 2, 2, 2], [3, 1, 1, 1]] if name == 'star' else [[0, 3, 1, 2], [1, 2, 2, 1], [2, 1, 3, 0]]
        require(kept == expected, 'complete written core blue-degree possibilities')
        results[name] = kept
    require(all(b[0] - 1 + b[3] - 1 == 0 for b in results['path']),
            'extra A path chord cannot have t sum two')
    return {'core_domains_per_shape': 256, 'five_retained_degree_patterns': results,
            'path_extra_chord_impossible': True}


def run():
    counts = {'h_cross_spines': 0, 'I_layer_spines': 0, 'I_cross_spines_including_inside': 0,
              'h_inside_spines': 0, 'normalized_adjacency_rows': 0}
    domain = lifts = 0
    triangle_marks = set()
    for template_id, (name, a_edges) in enumerate(templates()):
        for nr, nb in product(range(16), range(31)):
            rng = Random(template_id * 10000 + nr * 100 + nb)
            r_edges = set(rng.sample(sorted(a_edges), nr))
            d_edges = set(rng.sample(sorted(set(PAIRS) - a_edges), nb))
            inside = [rng.randrange(2) for _ in range(N)]
            s = system(a_edges, r_edges, d_edges, inside)
            triangle_marks |= s['AAA_mark_counts']
            domain += 1
            for h_inside in range(2):
                row = check_literal(a_edges, r_edges, d_edges, inside, h_inside, s, rng)
                for key in counts:
                    counts[key] += row[key]
                lifts += 1
    require(domain == 1488 and lifts == 2976 and triangle_marks == set(range(4)),
            'complete stated sampled density/template domain')
    return {'agent': 'six-books-2', 'role': 'researcher', 'complete': True,
            'written_analytic_proof': 'ONE_MATCHING.md', 'controls_not_theorem_premise': True,
            'cubic_templates': [name for name, _ in templates()], 'red_density_counts': 16,
            'blue_density_counts': 31, 'sampled_markings_per_density_per_template': 1,
            'nonnegative_scalar_identity_controls': domain, 'AAA_red_mark_counts_seen': sorted(triangle_marks),
            'literal_lifts': lifts, 'literal_counts': counts,
            'literal_full_spines': 231 * lifts, 'joint_equality_positive_control': positive_control(),
            'red_shape_control': red_shape_control(), 'core_degree_control': core_degree_control(),
            'all_cubic_skeletons_enumerated': False, 'full_matching_sign_enumeration': False,
            'normalization_and_sign_coverage_are_written_not_sampled_inferences': True}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--emit', action='store_true', help='regenerate without reading the compact fixture')
    args = parser.parse_args()
    actual = run()
    if not args.emit:
        expected = json.loads(Path(__file__).with_name('one_matching_expected.json').read_text())
        require(actual == expected, 'complete exact expected-summary mismatch')
    print(json.dumps(actual, indent=2))


if __name__ == '__main__':
    main()
