"""Separate definition-level audit of the four-blue analytic exclusion.
Author: six-books-2, role researcher. Imports no researcher program.
Blue forms are generated from all four-edge sets, not an input form list.
"""
import argparse
from functools import lru_cache
from itertools import combinations, permutations, product
import json
from pathlib import Path
import random
import time

Q = 11
PAIRS = tuple(combinations(range(Q), 2))


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


@lru_cache(None)
def connected_code(n, edges):
    positions = {edge: i for i, edge in enumerate(combinations(range(n), 2))}
    best = None
    for order in permutations(range(n)):
        mapping = tuple(order.index(i) for i in range(n))
        code = sum(1 << positions[tuple(sorted((mapping[i], mapping[j])))]
                   for i, j in edges)
        if best is None or code < best[0]:
            best = code, mapping
    return best


def canonical_blue(edges):
    neighbors = [set() for _ in range(Q)]
    for i, j in edges:
        neighbors[i].add(j)
        neighbors[j].add(i)
    components = []
    seen = set()
    for root in range(Q):
        if root in seen or not neighbors[root]:
            continue
        stack = [root]
        members = set()
        while stack:
            i = stack.pop()
            if i in members:
                continue
            members.add(i)
            stack.extend(neighbors[i] - members)
        seen |= members
        nodes = tuple(sorted(members))
        local = tuple((nodes.index(i), nodes.index(j)) for i, j in edges if i in members)
        code, permutation = connected_code(len(nodes), tuple(sorted(local)))
        components.append((len(nodes), code, nodes, permutation))
    components.sort(key=lambda item: (item[0], item[1], item[2]))
    key = tuple((n, code) for n, code, _, _ in components)
    mapping = {}
    canonical = []
    offset = 0
    for n, code, nodes, permutation in components:
        mapping.update({v: offset + permutation[i] for i, v in enumerate(nodes)})
        canonical.extend((offset + i, offset + j)
                         for bit, (i, j) in enumerate(combinations(range(n), 2)) if code >> bit & 1)
        offset += n
    for i in range(Q):
        if i not in mapping:
            mapping[i] = offset
            offset += 1
    require(sorted(mapping.values()) == list(range(Q)), "complete canonical permutation")
    return key, tuple(sorted(canonical)), mapping


def generate_blue_forms():
    forms = {}
    traversed = 0
    # A four-edge simple graph has at most eight nonisolated vertices.
    for edges in combinations(tuple(combinations(range(8), 2)), 4):
        key, canonical, _ = canonical_blue(edges)
        forms.setdefault(key, canonical)
        traversed += 1
    require(traversed == 20475 and len(forms) == 11, "complete four-blue form generation")
    return forms, traversed


# Literal two-point neighbor tables, allowing both matching orientations.
TWO = frozenset([0, 1])
OPTIONS = [(frozenset(),), (frozenset([0]), frozenset([1])), (TWO,)]
MATCH_COST = {}
UNIFORM_COST = {}
for i, j in product(range(3), repeat=2):
    match, uniform = set(), set()
    for left, right in product(OPTIONS[i], OPTIONS[j]):
        reverse = frozenset(1 - v for v in right) if j == 1 else right
        match.add((len(left & right), len((TWO - left) & (TWO - reverse))))
        uniform.add((len(left & right) + len(left & reverse),
                     len((TWO - left) & (TWO - right)) + len((TWO - left) & (TWO - reverse))))
    require(len(uniform) == 1, "sign-independent literal uniform sum")
    MATCH_COST[i, j] = match
    UNIFORM_COST[i, j] = next(iter(uniform))


def neighbors(edges):
    result = [set() for _ in range(Q)]
    for i, j in edges:
        result[i].add(j)
        result[j].add(i)
    return result


def relaxed_matching(red, blue):
    types = [[2 if k in red[i] else 0 if k in blue[i] else 1 for k in range(Q)]
             for i in range(Q)]
    for i, j in PAIRS:
        if j in red[i] or j in blue[i]:
            continue
        fixed_r = fixed_b = free = 0
        for k in range(Q):
            if k in (i, j):
                continue
            costs = MATCH_COST[types[i][k], types[j][k]]
            if len(costs) == 2:
                require(costs == {(0, 1), (1, 0)}, "free literal matching costs")
                free += 1
            else:
                a, b = next(iter(costs))
                fixed_r += a
                fixed_b += b
        if not any(fixed_r + r <= 3 and fixed_b + free - r <= 6 for r in range(free + 1)):
            return None
    return types


def inside_flags(red, blue, types):
    sums = []
    for i, j in PAIRS:
        if j in red[i] or j in blue[i]:
            color = int(j in blue[i])
            outside = sum(UNIFORM_COST[types[i][k], types[j][k]][color]
                          for k in range(Q) if k not in (i, j))
            sums.append((i, j, color, outside))
    flags = []
    for bits in product([0, 1], repeat=Q):
        if any(2 * len(red[i] if bits[i] else blue[i]) > (3 if bits[i] else 6) for i in range(Q)):
            continue
        if all(outside + 2 * (bits[i] + bits[j] if color == 0 else 2 - bits[i] - bits[j])
               <= (6 if color == 0 else 12) for i, j, color, outside in sums):
            flags.append(sum(bit << i for i, bit in enumerate(bits)))
    return sorted(flags)


def normalized_record(record):
    blue = tuple(tuple(edge) for edge in record['blue_pairs'])
    red = tuple(tuple(edge) for edge in record['red_pairs'])
    for name, edges in [('blue', blue), ('red', red)]:
        require(len(set(edges)) == len(edges), "duplicate " + name + " edge")
        require(all(len(e) == 2 and all(type(v) is int for v in e) and 0 <= e[0] < e[1] < Q
                    for e in edges), "invalid " + name + " pair")
    require(len(blue) == 4 and len(red) >= 3 and not set(red) & set(blue), "record scope")
    flags = record['flags']
    require(flags and len(set(flags)) == len(flags)
            and all(type(f) is int and 0 <= f < (1 << Q) for f in flags), "invalid flags")
    key, _, mapping = canonical_blue(blue)
    red_key = tuple(sorted(tuple(sorted((mapping[i], mapping[j]))) for i, j in red))
    mapped_flags = sorted(sum((word >> i & 1) << mapping[i] for i in range(Q)) for word in flags)
    return (key, red_key), mapped_flags


def dot(a, b):
    return sum(x * y for x, y in zip(a, b))


def obstruction_controls():
    rows = tuple(product([-1, 1], repeat=6))
    pairs = attempts = triples = 0
    for a, b in product(rows, repeat=2):
        if dot(a, b) != 0:
            continue
        pairs += 1
        for c in rows:
            attempts += 1
            triples += int(dot(a, c) == dot(b, c) == 0)
    require((pairs, attempts, triples) == (1280, 81920, 0), "all six-sign triples")
    four = [(1, 1, 1, 1), (1, 1, -1, -1), (1, -1, 1, -1)]
    require(all(dot(a, b) == 0 for a, b in combinations(four, 2)), "order-four positive control")
    blue = {(0, 1), (1, 2), (2, 3), (3, 4)}
    red = {(0, 3), (1, 3), (1, 4)}
    graphs = spine_checks = gram_checks = 0
    for seed in range(32):
        rng = random.Random(seed)
        signs = {edge: rng.choice([-1, 1]) for edge in PAIRS if edge not in blue | red}
        row = {i: tuple(signs[min(i, h), max(i, h)] for h in range(5, Q)) for i in (0, 1, 3)}
        for inside_two, outside_bit, outside_form in product([0, 1], [0, 1], range(4)):
            inside = [0, 0, inside_two, 0, 0] + [outside_bit] * 6
            red_blocks, blue_blocks = set(red), set(blue)
            for position, edge in enumerate(combinations(range(5, Q), 2)):
                # The local path-core lemma leaves these fifteen blocks arbitrary.
                kind = (None if outside_form == 0 else 2 if outside_form == 1
                        else 0 if outside_form == 2 else (position + seed) % 3)
                if kind == 2:
                    red_blocks.add(edge)
                elif kind == 0:
                    blue_blocks.add(edge)
            nr = [set() for _ in range(22)]
            for i, bit in enumerate(inside):
                if bit:
                    nr[2 * i].add(2 * i + 1)
                    nr[2 * i + 1].add(2 * i)
            for i, j in PAIRS:
                for a, b in product([0, 1], repeat=2):
                    if (i, j) in red_blocks or ((i, j) not in blue_blocks and
                                               (a == b) == (signs.get((i, j)) == 1)):
                        nr[2 * i + a].add(2 * j + b)
                        nr[2 * j + b].add(2 * i + a)
            nb = [set(range(22)) - {i} - nr[i] for i in range(22)]
            violations = 0
            for edge, cap in [((0, 1), 6), ((0, 3), 3), ((1, 3), 3)]:
                i, j = edge
                color = nb if edge in blue else nr
                pages = [len(color[2 * i] & color[2 * j + b]) for b in [0, 1]]
                require(sum(pages) == 2 * cap, "literal saturated sum")
                require(pages[0] - pages[1] == dot(row[i], row[j]), "literal Gram difference")
                violations += sum(value > cap for value in pages)
                spine_checks += 2
                gram_checks += 1
            require(violations > 0, "every sampled lift has an explicit forbidden spine")
            graphs += 1
    return {'ordered_orthogonal_six_sign_pairs': pairs,
            'six_sign_third_row_attempts': attempts, 'orthogonal_six_sign_triples': triples,
            'order_four_positive_control': True, 'deterministic_lifted_graphs': graphs,
            'literal_spine_checks': spine_checks, 'literal_Gram_difference_checks': gram_checks,
            'every_sample_has_explicit_book_spine': True, 'sample_sign_seeds': 32,
            'inside_patterns_per_seed': 4, 'outside_block_patterns_per_seed_and_inside': 4,
            'full_matching_sign_enumeration': False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--compare-records', type=Path, required=True)
    args = parser.parse_args()
    start = time.monotonic()
    forms, traversed = generate_blue_forms()
    cases = {}
    survivors = {}
    for key, edges in sorted(forms.items()):
        blue = neighbors(edges)
        # Minimum red uniform-page sum with every other nonblue link matching.
        candidates = [edge for edge in PAIRS if edge not in edges and
                      sum(UNIFORM_COST[int(k not in blue[edge[0]]), int(k not in blue[edge[1]])][0]
                          for k in range(Q) if k not in edge) <= 6]
        count = {'all_red_subsets': 0, 'at_least_three_red_subsets': 0,
                 'matching_budget_pass': 0, 'necessary_red_survivors': 0, 'inside_flag_survivors': 0}
        for bits in product([0, 1], repeat=len(candidates)):
            count['all_red_subsets'] += 1
            if sum(bits) < 3:
                continue
            count['at_least_three_red_subsets'] += 1
            red_edges = tuple(e for e, bit in zip(candidates, bits) if bit)
            red = neighbors(red_edges)
            types = relaxed_matching(red, blue)
            if types is None:
                continue
            count['matching_budget_pass'] += 1
            flags = inside_flags(red, blue, types)
            if flags:
                count['necessary_red_survivors'] += 1
                count['inside_flag_survivors'] += len(flags)
                record = {'blue_pairs': edges, 'red_pairs': red_edges, 'flags': flags}
                record_key, normalized_flags = normalized_record(record)
                require(record_key not in survivors, "duplicate independently generated survivor")
                survivors[record_key] = normalized_flags
        cases[key] = count
    reference = json.loads(args.compare_records.read_text())
    expected_records = {}
    for record in reference:
        key, flags = normalized_record(record)
        require(key not in expected_records, "duplicate reference survivor")
        expected_records[key] = flags
    require(survivors == expected_records, "all survivor and flag entries must match")
    expected = json.loads(Path(__file__).with_name('four_blue_expected.json').read_text())
    expected_cases = {}
    for case in expected['cases']:
        key, _, _ = canonical_blue(case['blue_pairs'])
        expected_cases[key] = {k: case[k] for k in next(iter(cases.values()))}
    require(cases == expected_cases, "every independently generated case diagnostic")
    require(sum(c['all_red_subsets'] for c in cases.values()) == 586
            and sum(c['at_least_three_red_subsets'] for c in cases.values()) == 408,
            "complete arbitrary-red candidate domain")
    require(len(survivors) == 1 and sum(len(flags) for flags in survivors.values()) == 128,
            "unique necessary P5 shape with all flags")
    controls = obstruction_controls()
    result = {'agent': 'six-books-2', 'role': 'researcher', 'complete': True,
              'generated_labeled_four_blue_edge_sets': traversed, 'generated_unlabeled_blue_forms': len(forms),
              'all_red_subsets': 586, 'at_least_three_red_subsets': 408,
              'matching_budget_pass': sum(c['matching_budget_pass'] for c in cases.values()),
              'necessary_red_survivors': len(survivors), 'inside_flag_survivors': 128,
              'all_survivor_flag_entries_match': True, 'all_case_diagnostics_match': True,
              'literal_page_tables': True, 'obstruction_controls': controls,
              'validation_not_theorem_premise': True, 'full_matching_sign_enumeration': False,
              'wall_seconds': time.monotonic() - start}
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
