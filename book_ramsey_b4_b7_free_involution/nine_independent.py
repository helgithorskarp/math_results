"""Separate definition-level checker for the three-red/six-blue reduction.
Author: six-books-2, role researcher. Imports no campaign program.
Generates connected components directly, rather than adding a sixth edge.
"""
import argparse
from functools import lru_cache
from itertools import combinations, permutations, product
import json
from pathlib import Path
import time

Q = 11
PAIRS = tuple(combinations(range(Q), 2))


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


@lru_cache(None)
def connected_code(n, edges):
    degrees = [sum(i in edge for edge in edges) for i in range(n)]
    groups = [tuple(i for i in range(n) if degrees[i] == d) for d in sorted(set(degrees))]
    positions = {edge: bit for bit, edge in enumerate(combinations(range(n), 2))}
    best = None
    # Isomorphisms preserve degrees. Put the classes in ascending degree order,
    # then minimize over every order within each class.
    for choices in product(*(permutations(group) for group in groups)):
        order = tuple(i for group in choices for i in group)
        mapping = tuple(order.index(i) for i in range(n))
        code = sum(1 << positions[tuple(sorted((mapping[i], mapping[j])))] for i, j in edges)
        if best is None or code < best[0]:
            best = code, mapping
    return best


def canonical_blue(edges):
    neighbor = [set() for _ in range(Q)]
    for i, j in edges:
        neighbor[i].add(j)
        neighbor[j].add(i)
    components, seen = [], set()
    for root in range(Q):
        if root in seen or not neighbor[root]:
            continue
        members, stack = set(), [root]
        while stack:
            i = stack.pop()
            if i not in members:
                members.add(i)
                stack.extend(neighbor[i] - members)
        seen |= members
        nodes = tuple(sorted(members))
        local = tuple(sorted((nodes.index(i), nodes.index(j)) for i, j in edges if i in members))
        code, permutation = connected_code(len(nodes), local)
        components.append((len(nodes), code, nodes, permutation))
    components.sort(key=lambda item: item[:3])
    key = tuple((n, code) for n, code, _, _ in components)
    mapping, canonical, offset = {}, [], 0
    for n, code, nodes, permutation in components:
        mapping.update({v: offset + permutation[i] for i, v in enumerate(nodes)})
        canonical.extend((offset + i, offset + j)
                         for bit, (i, j) in enumerate(combinations(range(n), 2)) if code >> bit & 1)
        offset += n
    for i in range(Q):
        if i not in mapping:
            mapping[i] = offset
            offset += 1
    require(sorted(mapping.values()) == list(range(Q)), 'complete canonical permutation')
    return key, tuple(sorted(canonical)), mapping


def connected(n, edges):
    neighbor = [set() for _ in range(n)]
    for i, j in edges:
        neighbor[i].add(j)
        neighbor[j].add(i)
    visited, stack = set(), [0]
    while stack:
        i = stack.pop()
        if i not in visited:
            visited.add(i)
            stack.extend(neighbor[i] - visited)
    return len(visited) == n


def generate_forms():
    catalog = {e: {} for e in range(1, 7)}
    domains = []
    for n in range(2, 8):
        pairs = tuple(combinations(range(n), 2))
        for e in range(n - 1, min(6, len(pairs)) + 1):
            traversed = connected_count = 0
            for edges in combinations(pairs, e):
                traversed += 1
                if not connected(n, edges):
                    continue
                connected_count += 1
                code, _ = connected_code(n, edges)
                canonical = tuple(pair for bit, pair in enumerate(pairs) if code >> bit & 1)
                catalog[e].setdefault((n, code), canonical)
            domains.append({'vertices': n, 'edges': e, 'edge_sets': traversed,
                            'connected_labeled_graphs': connected_count})
    sizes = {e: len(forms) for e, forms in catalog.items()}
    require({e: sizes[e] for e in range(1, 6)} == {1: 1, 2: 1, 3: 3, 4: 5, 5: 12},
            'earlier small connected catalogs')
    components = sorted((e, n, code, edges) for e, forms in catalog.items()
                        for (n, code), edges in forms.items())
    forms = {}

    def assemble(start, remaining, offset, edges):
        if remaining == 0:
            key, canonical, _ = canonical_blue(tuple(sorted(edges)))
            require(key not in forms, 'unique connected-component multiset')
            forms[key] = canonical
            return
        for index in range(start, len(components)):
            e, n, _, local = components[index]
            if e > remaining:
                break
            if offset + n > Q:
                continue
            assemble(index, remaining - e, offset + n,
                     edges + [(i + offset, j + offset) for i, j in local])

    assemble(0, 6, 0, [])
    require(len(forms) == 67, 'complete six-edge component assemblies')
    return forms, domains, sizes


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
    blue = tuple(tuple(e) for e in record['blue_pairs'])
    red = tuple(tuple(e) for e in record['red_pairs'])
    for name, edges in [('blue', blue), ('red', red)]:
        require(len(set(edges)) == len(edges)
                and all(len(e) == 2 and all(type(v) is int for v in e)
                        and 0 <= e[0] < e[1] < Q for e in edges), 'valid ' + name + ' pairs')
    require(len(blue) == 6 and len(red) == 3 and not set(red) & set(blue), 'record scope')
    flags = record['flags']
    require(flags and len(set(flags)) == len(flags)
            and all(type(f) is int and 0 <= f < 1 << Q for f in flags), 'valid flags')
    key, _, mapping = canonical_blue(blue)
    red_key = tuple(sorted(tuple(sorted((mapping[i], mapping[j]))) for i, j in red))
    mapped_flags = sorted(sum((word >> i & 1) << mapping[i] for i in range(Q)) for word in flags)
    return (key, red_key), mapped_flags


def compare_records(actual, reference):
    expected = {}
    for record in reference:
        key, flags = normalized_record(record)
        require(key not in expected, 'unique reference survivor')
        expected[key] = flags
    require(actual == expected, 'all survivor and flag entries must match')


def analytic_template(record):
    red = {tuple(e) for e in record['red_pairs']}
    blue = {tuple(e) for e in record['blue_pairs']}
    neighbor = neighbors(blue)
    components, seen = [], set()
    for root in range(Q):
        if root in seen or not neighbor[root]:
            continue
        nodes, stack = set(), [root]
        while stack:
            i = stack.pop()
            if i not in nodes:
                nodes.add(i)
                stack.extend(neighbor[i] - nodes)
        seen |= nodes
        components.append(nodes)
    require(sorted(map(len, components)) == [2, 2, 5], 'P5 and two outside K2 components')
    core = next(nodes for nodes in components if len(nodes) == 5)
    ends = sorted(i for i in core if len(neighbor[i]) == 1)
    require(len(ends) == 2 and sorted(len(neighbor[i]) for i in core) == [1, 1, 2, 2, 2],
            'five-orbit path')
    for end in ends:
        order = [end]
        while len(order) < 5:
            next_nodes = neighbor[order[-1]] - set(order)
            require(len(next_nodes) == 1, 'unique path continuation')
            order.append(next(iter(next_nodes)))
        mapping = dict(enumerate(order))
        if {tuple(sorted((mapping[i], mapping[j])))
            for i, j in [(0, 3), (1, 3), (1, 4)]} != red:
            continue
        outside = set(range(Q)) - core
        require(all(tuple(sorted((i, j))) not in red | blue for i in core for j in outside),
                'every core-to-outside block matching')
        outside_blue = sorted(edge for edge in blue if edge[0] in outside)
        require(len(outside_blue) == 2 and len({i for edge in outside_blue for i in edge}) == 4,
                'two disjoint outside blue pairs')
        flags = [word for word in range(1 << Q)
                 if all(not (word >> mapping[i] & 1) for i in [0, 1, 3, 4])
                 and all(sum(word >> i & 1 for i in edge) >= 1 for edge in outside_blue)]
        require(flags == sorted(record['flags']), 'every local-path-template flag entry')
        require(len(flags) == 72, 'three times three times eight inside assignments')
        return {'name': 'path_with_two_outside_blue_edges',
                'core_to_original_orbits': order,
                'outside_original_orbits': sorted(outside),
                'outside_blue_pairs': outside_blue,
                'inside_flags': len(flags), 'all_core_to_outside_blocks_matching': True}
    raise RuntimeError('necessary survivor not covered by the local path obstruction')


def main():
    import copy
    from math import comb

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--compare-records', type=Path, required=True)
    args = parser.parse_args()
    started = time.monotonic()
    forms, domains, catalog_sizes = generate_forms()
    require(all(c['edge_sets'] == comb(comb(c['vertices'], 2), c['edges']) for c in domains),
            'every labeled connected-generation domain complete')
    cases, survivors, records, candidate_sets = {}, {}, [], {}
    for key, edges in sorted(forms.items()):
        blue = neighbors(edges)
        # Assign every nonblue block the minimum red-neighbor set (matching).
        # Literal two-spine red sums then give an independent candidate cut.
        candidates = [edge for edge in PAIRS if edge not in edges and
                      sum(UNIFORM_COST[int(k not in blue[edge[0]]), int(k not in blue[edge[1]])][0]
                          for k in range(Q) if k not in edge) <= 6]
        _, _, mapping = canonical_blue(edges)
        candidate_sets[key] = tuple(sorted(tuple(sorted((mapping[i], mapping[j])))
                                           for i, j in candidates))
        count = {'red_triples': 0, 'support_pass': 0, 'matching_pass': 0,
                 'necessary_survivors': 0, 'inside_flag_survivors': 0}
        for red_edges in combinations(candidates, 3):
            count['red_triples'] += 1
            red = neighbors(red_edges)
            if len({i for i in range(Q) if red[i] or blue[i]}) < 9:
                continue
            count['support_pass'] += 1
            types = relaxed_matching(red, blue)
            if types is None:
                continue
            count['matching_pass'] += 1
            flags = inside_flags(red, blue, types)
            if flags:
                count['necessary_survivors'] += 1
                count['inside_flag_survivors'] += len(flags)
                record = {'blue_pairs': edges, 'red_pairs': red_edges, 'flags': flags}
                record_key, mapped_flags = normalized_record(record)
                require(record_key not in survivors, 'unique separate survivor')
                survivors[record_key] = mapped_flags
                records.append(record)
        cases[key] = count
    reference = json.loads(args.compare_records.read_text())
    compare_records(survivors, reference)
    expected = json.loads(Path(__file__).with_name('nine_expected.json').read_text())
    expected_cases, expected_candidates = {}, {}
    for case in expected['cases']:
        key, _, mapping = canonical_blue(tuple(tuple(e) for e in case['blue_pairs']))
        require(key not in expected_cases, 'unique reference blue form')
        expected_cases[key] = {k: case[k] for k in next(iter(cases.values()))}
        expected_candidates[key] = tuple(sorted(tuple(sorted((mapping[i], mapping[j])))
                                                for i, j in case['red_candidates']))
    require(cases == expected_cases, 'every independently generated case diagnostic')
    require(candidate_sets == expected_candidates, 'every red-candidate position agrees')
    templates = [analytic_template(record) for record in records]
    require(len(survivors) == 1 and sum(len(f) for f in survivors.values()) == 72,
            'complete one-pattern/72-flag reduction')
    # Exercise the freshly computed comparison boundary, without regenerating
    # the same domain twice. These are malformed evidence, not graph witnesses.
    corrupted = copy.deepcopy(reference)
    old = corrupted[0]['flags'][0]
    replacement = next(old ^ (1 << bit) for bit in range(Q)
                       if (old ^ (1 << bit)) not in corrupted[0]['flags'])
    corrupted[0]['flags'][0] = replacement
    rejected = 0
    for bad in [corrupted, reference[1:]]:
        try:
            compare_records(survivors, bad)
        except RuntimeError as exc:
            require(str(exc) == 'all survivor and flag entries must match',
                    'targeted corruption rejected specifically for entry mismatch')
            rejected += 1
        else:
            raise RuntimeError('corrupted reference accepted')
    result = {'agent': 'six-books-2', 'role': 'researcher', 'complete': True,
              'blue_forms': len(forms), 'connected_catalog_sizes_by_edge_count': catalog_sizes,
              'connected_generation_domains': domains,
              'connected_labeled_edge_sets': sum(c['edge_sets'] for c in domains),
              'red_triples': sum(c['red_triples'] for c in cases.values()),
              'support_pass': sum(c['support_pass'] for c in cases.values()),
              'matching_pass': sum(c['matching_pass'] for c in cases.values()),
              'necessary_survivors': len(survivors), 'inside_flag_survivors': 72,
              'every_case_diagnostic_matches': True, 'every_survivor_flag_entry_matches': True,
              'every_red_candidate_position_matches': True, 'analytic_templates': templates,
              'targeted_corruptions_rejected': rejected, 'degree_theorem_used': False,
              'full_matching_sign_enumeration': False, 'wall_seconds': time.monotonic() - started}
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
