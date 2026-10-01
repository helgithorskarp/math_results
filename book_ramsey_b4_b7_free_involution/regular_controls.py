"""Exact author controls for REGULAR.md, not a new finite theorem premise.
Actual author six-books-2, researcher. Python standard library only.
The regular corollary imports the reviewed positive-codegree theorem.
"""
import argparse
from itertools import combinations, product
import json
from pathlib import Path
from random import Random


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def pair(i, j):
    return tuple(sorted((i, j)))


P10 = tuple(combinations(range(10), 2))
P11 = tuple(combinations(range(11), 2))
P22 = tuple(combinations(range(22), 2))


def lift(r, d, positive, flags):
    """Literal four-entry orbit blocks, without matrix products."""
    require(len(flags) == 11 and set(flags) <= {0, 1}, 'binary inside flags')
    require(r <= set(P11) and d <= set(P11) and positive <= set(P11), 'edge domain')
    require(not (r & d or r & positive or d & positive), 'disjoint block types')
    red = [set() for _ in range(22)]
    for v, w in P22:
        i, x = divmod(v, 2)
        j, y = divmod(w, 2)
        if i == j:
            is_red = flags[i] == 1
        else:
            e = (i, j)
            is_red = e in r or (e not in d and (x == y) == (e in positive))
        if is_red:
            red[v].add(w)
            red[w].add(v)
    return red


def triangles(red):
    """Literal unordered vertex triples, independent of edge-page sums."""
    return [t for t in combinations(range(len(red)), 3)
            if t[1] in red[t[0]] and t[2] in red[t[0]] and t[2] in red[t[1]]]


def switched(red, flags):
    pi = [2 * i + (x ^ flags[i]) for i in range(11) for x in range(2)]
    result = [set() for _ in range(22)]
    for v in range(22):
        result[pi[v]] = {pi[w] for w in red[v]}
    return result


def cubic_templates():
    petersen = ({pair(i, (i + 1) % 5) for i in range(5)}
                | {(i, i + 5) for i in range(5)}
                | {pair(5 + i, 5 + (i + 2) % 5) for i in range(5)})
    ladder = {pair(i, (i + 1) % 10) for i in range(10)} | {(i, i + 5) for i in range(5)}
    split = set(combinations(range(4), 2)) | {(i, j) for i in range(4, 7) for j in range(7, 10)}
    return [('Petersen', petersen), ('ten_cycle_opposite_matching', ladder),
            ('K4_disjoint_K33', split)]


def normalized_control(a, r, d, inside, h_inside):
    require(len(a) == 15 and all(sum(i in e for e in a) == 3 for i in range(10)), 'cubic skeleton')
    require(r <= a and d <= set(P10) - a, 'normalized markings')
    positive = (a - r) | {(i, 10) for i in range(10)}
    red = lift(r, d, positive, inside + [h_inside])
    blue = [set(range(22)) - {i} - red[i] for i in range(22)]
    a_neighbors = [{j for j in range(10) if j != i and pair(i, j) in a} for i in range(10)]
    c_rows = [{j for j in range(10) if 2 * j + 1 in red[2 * i]} for i in range(10)]
    m_entries = {(i, j): len(a_neighbors[i] & a_neighbors[j]) + len(c_rows[i] & c_rows[j])
                 for i, j in a}
    ta = len(triangles(a_neighbors))
    literal = triangles(red)
    parts = [0, 0, 0]
    for t in literal:
        if any(v >= 20 for v in t):
            require(sum(v >= 20 for v in t) == 1, 'no triangle with both h points')
            parts[0] += 1
        elif len({v % 2 for v in t}) == 1:
            parts[1] += 1
        else:
            parts[2] += 1
    require(parts == [30, 2 * ta, 2 * sum(len(c_rows[i] & c_rows[j]) for i, j in a)],
            'literal disjoint triangle classes')
    require(len(literal) == 30 + 2 * sum(m_entries.values()) - 4 * ta,
            'triangle-budget identity versus literal vertex triples')
    require(sum(len(red[v] & red[w]) for v, w in P22 if w in red[v]) == 3 * len(literal),
            'triangle-edge page handshake')
    for i, j in a:
        require(len(red[2 * i] & red[2 * j]) == 1 + m_entries[i, j], 'same-layer red spine')
        require(len(red[2 * i + 1] & red[2 * j + 1]) == 1 + m_entries[i, j], 'other-layer red spine')
    for i in range(10):
        for x, y in product(range(2), repeat=2):
            v, w = 20 + x, 2 * i + y
            color = red if w in red[v] else blue
            require(len(color[v] & color[w]) == (3 if color is red else 6), 'saturated h spine')
    if max(m_entries.values()) <= 2:
        require(len(literal) <= 90 - 4 * ta, 'necessary-cap triangle bound')
    rng = Random(30000 + 100 * len(r) + len(d) + 100000 * h_inside)
    changed = switched(red, [rng.randrange(2) for _ in range(10)] + [0])
    normalization = [int(2 * i not in changed[20]) for i in range(10)] + [0]
    require(switched(changed, normalization) == red, 'switch normalization restores all adjacency')
    return {'triangles': len(literal), 'A_triangles': ta, 'max_M': max(m_entries.values()),
            'max_red_pages': max(len(red[v] & red[w]) for v, w in P22 if w in red[v])}


def triangle_controls():
    domains = lifts = cap_controls = 0
    a_triangle_values = set()
    for template_id, (_, a) in enumerate(cubic_templates()):
        for nr, nb in product(range(16), range(31)):
            rng = Random(77113 + template_id * 10000 + nr * 101 + nb)
            r = set(rng.sample(sorted(a), nr))
            d = set(rng.sample(sorted(set(P10) - a), nb))
            inside = [rng.randrange(2) for _ in range(10)]
            domains += 1
            for h_inside in range(2):
                result = normalized_control(a, r, d, inside, h_inside)
                a_triangle_values.add(result['A_triangles'])
                cap_controls += int(result['max_M'] <= 2)
                lifts += 1
    # Sharp control for the triangle budget only; its red cross spines fail.
    r = {(i, i + 3) for i in range(3)}
    a = r | {(i, j) for i in range(3) for j in (6, 7)} | {(i, j) for i in range(3, 6) for j in (8, 9)}
    d = {(i, 3 + (i + 1) % 3) for i in range(3)} | {(i, j) for i in (6, 7) for j in (8, 9)}
    sharp = normalized_control(a, r, d, [0] * 10, 0)
    require(sharp == {'triangles': 90, 'A_triangles': 0, 'max_M': 2, 'max_red_pages': 6},
            'sharp necessary triangle budget is not a valid Ramsey witness')
    require(domains == 1488 and lifts == 2976, 'stated template and density coverage')
    return {'templates': [name for name, _ in cubic_templates()], 'marking_samples': domains,
            'both_h_inside_colors': True, 'literal_lifts': lifts + 1,
            'literal_vertex_triples_per_lift': 1540, 'triangle_edge_handshakes': lifts + 1,
            'literal_same_layer_red_spines': 30 * (lifts + 1),
            'literal_saturated_h_spines': 40 * (lifts + 1),
            'restored_adjacency_rows': 22 * (lifts + 1),
            'A_triangle_values_seen': sorted(a_triangle_values),
            'sampled_lifts_meeting_same_layer_red_caps': cap_controls,
            'sharp_necessary_budget_control': sharp, 'all_cubic_skeletons_enumerated': False}


def local_controls():
    matching = uniform = inside_checks = degree_checks = 0
    for seed in range(24):
        rng = Random(18307 + seed)
        types = [rng.randrange(4) for _ in P11]
        if seed < 4:
            types = [seed] * len(P11)
        r = {e for e, c in zip(P11, types) if c == 0}
        d = {e for e, c in zip(P11, types) if c == 1}
        positive = {e for e, c in zip(P11, types) if c == 2}
        for flag_kind in range(3):
            flags = ([flag_kind] * 11 if flag_kind < 2 else [rng.randrange(2) for _ in range(11)])
            red = lift(r, d, positive, flags)
            blue = [set(range(22)) - {i} - red[i] for i in range(22)]
            w = [[int(pair(i, j) in r) - int(pair(i, j) in d) if i != j else 0
                  for j in range(11)] for i in range(11)]
            dn = [{j for j in range(11) if j != i and pair(i, j) in d} for i in range(11)]
            for i in range(11):
                ri, bi = sum(i in e for e in r), len(dn[i])
                require(len(red[2 * i]) == len(red[2 * i + 1]) == 10 + ri - bi + flags[i],
                        'literal red degree')
                degree_checks += 2
                color = red if flags[i] else blue
                require(len(color[2 * i] & color[2 * i + 1]) == 2 * (ri if flags[i] else bi),
                        'literal inside pages')
                inside_checks += 1
            for i, j in P11:
                if (i, j) in r:
                    actual = sum(len(red[2 * i] & red[2 * j + y]) for y in range(2))
                    cost = sum((1 + w[i][k]) * (1 + w[j][k])
                               for k in range(11) if k not in (i, j)) + 2 * (flags[i] + flags[j])
                    require(actual == cost, 'literal uniform-red two-spine sum')
                    require(actual >= 9 - len(dn[i] | dn[j]) + 2 * (flags[i] + flags[j]),
                            'enhanced neighborhood-union lower bound')
                    if actual <= 6:
                        require(len(dn[i] | dn[j]) >= 3 + 2 * (flags[i] + flags[j]),
                                'enhanced necessary candidate bound')
                    uniform += 1
                elif (i, j) not in d:
                    rp = bp = None
                    for y in range(2):
                        v, z = 2 * i, 2 * j + y
                        if z in red[v]:
                            rp = len(red[v] & red[z])
                        else:
                            bp = len(blue[v] & blue[z])
                    require(rp is not None and bp is not None, 'opposite-color matching spines')
                    require(rp + bp == 9 + sum(w[i][k] * w[j][k] for k in range(11)),
                            'matching square versus literal page sum')
                    matching += 1
    return {'literal_lifts': 72, 'literal_red_degree_checks': degree_checks,
            'literal_inside_spines': inside_checks, 'uniform_red_enhanced_union_checks': uniform,
            'matching_combined_square_checks': matching}


def partitions(total, length, lower=1, upper=3):
    """All sorted positive degree lists, without selecting final patterns."""
    if length == 0:
        if total == 0:
            yield ()
        return
    for first in range(lower, upper + 1):
        if first * length <= total <= first + upper * (length - 1):
            for rest in partitions(total - first, length - 1, first, upper):
                yield (first,) + rest


def degree_controls():
    raw_masks = eligible = attachments = zero_inside = center_domains = degree_lists = 0
    summaries = {}
    for r in range(8):
        for deg in partitions(2 * r, 11):
            degree_lists += 1
            k3 = deg.count(3)
            for bits in product(range(2), repeat=11):
                raw_masks += 1
                if any(bit and degree != 1 for bit, degree in zip(bits, deg)) or sum(bits) % 2:
                    continue
                eligible += 1
                f = sum(bits)
                if f > 3 * k3:
                    continue
                attachments += 1
                key = (r, deg.count(1), deg.count(2), k3, f)
                summaries[key] = summaries.get(key, 0) + 1
                blue = [x + bit for x, bit in zip(deg, bits)]
                if f == 0:
                    require(deg.count(1) > r and all(blue[i] == 1 for i, x in enumerate(deg) if x == 1),
                            'too many red leaves, each a blue leaf')
                    zero_inside += 1
                else:
                    require(f == 2 and r == 7 and deg.count(3) == deg.count(2) == 1,
                            'all remaining low-density degree/inside cases')
                    x = deg.index(3)
                    eps_leaves = {i for i, bit in enumerate(bits) if bit}
                    allowed = set(range(11)) - {x} - eps_leaves
                    for neighbors in combinations(sorted(allowed), 3):
                        center_domains += 1
                        require(sum(blue[j] == 1 for j in neighbors) >= 2,
                                'every possible center D row has two blue leaves')
    equality = [list(deg) for deg in partitions(16, 11)]
    require(len(equality) == 3, 'sixteen-total equality degree domain')
    # Direct type-pair union audit: a red-inside leaf only meets a blue trivalent type.
    types = [(1, 2, 1), (1, 1, 0), (2, 2, 0), (3, 3, 0)]
    neighbors = [list(t) for t in types if 2 + t[1] >= 3 + 2 * (1 + t[2])]
    require(neighbors == [[3, 3, 0]], 'red-inside leaf neighbor type from full union bound')
    require(22 * 13 > 3 * 90 and (22 * 13 + 2) // 3 == 96, 'imported regular triangle floor')
    return {'generated_red_degree_lists': degree_lists,
            'all_literal_inside_masks': raw_masks, 'inside_type_and_parity_masks': eligible,
            'masks_after_leaf_attachment_bound': attachments,
            'all_blue_inside_leaf_count_exclusions': zero_inside,
            'red_inside_center_neighbor_lists_excluded': center_domains,
            'low_density_profiles': [dict(zip(['r', 'k1', 'k2', 'k3', 'F', 'literal_flag_words'],
                                             (*key, count))) for key, count in sorted(summaries.items())],
            'red_inside_leaf_possible_neighbor_type': neighbors,
            'sixteen_total_equality_sorted_degrees': equality,
            'regular_triangle_floor_imported_not_proved_by_controls': 96}


def run():
    return {'agent': 'six-books-2', 'role': 'researcher', 'complete': True,
            'written_proof': 'REGULAR.md', 'controls_not_new_theorem_premise': True,
            'regular_corollary_imports_reviewed_computer_assisted_codegree_theorem': True,
            'triangle_budget_has_no_computational_premise': True,
            'triangle_controls': triangle_controls(), 'local_spine_controls': local_controls(),
            'degree_inside_controls': degree_controls(), 'full_host_or_sign_census': False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--emit', action='store_true', help='regenerate without reading the expected fixture')
    args = parser.parse_args()
    actual = run()
    if not args.emit:
        expected = json.loads(Path(__file__).with_name('regular_expected.json').read_text())
        require(actual == expected, 'exact fixture mismatch')
    print(json.dumps(actual, indent=2))


if __name__ == '__main__':
    main()
