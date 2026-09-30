#!/usr/bin/env python3
"""Small exact validation of the ordinary pair-completion replacement.

No search over full codes or census of twenty-word links is performed.
The upper62 theorem is an external input, not re-proved here.
"""
import argparse
from collections import Counter
from hashlib import sha256
from itertools import combinations, permutations, product
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
U, V, A, B = 17, 16, 14, 15
D = tuple(range(16))


def require(condition, message):
    if not condition:
        raise ValueError(message)


def encoded(value):
    return (json.dumps(value, sort_keys=True, separators=(',', ':')) + '\n').encode('ascii')


def pairs(points):
    return set(combinations(sorted(points), 2))


def template(kind):
    if kind == 'middle':
        core = ((V, A), (V, B))
        leaves = ((V, range(8)), (A, range(8, 11)), (B, range(11, 14)))
        isolated = ()
    elif kind == 'end':
        core = ((V, A), (A, B))
        leaves = ((V, range(9)), (A, (9, 10)), (B, (11, 12, 13)))
        isolated = ()
    elif kind == 'triangle':
        core = ((V, A), (V, B), (A, B))
        leaves = ((V, range(8)), (A, (8, 9)), (B, (10, 11)))
        isolated = ((12, 13),)
    else:
        raise ValueError('unknown core')
    leave = {tuple(sorted(p)) for p in core + isolated}
    leave.update(tuple(sorted((x, y))) for x, ys in leaves for y in ys)
    degrees = Counter(x for edge in leave for x in edge)
    require(len(leave) == 16, 'sixteen link-leave edges')
    require(all(degrees[x] == (10 if x == V else 4 if x in (A, B) else 1)
                for x in range(17)), 'link-leave degrees')
    thirds = tuple(x for x in D if tuple(sorted((V, x))) not in leave)
    partitions = {tuple(sorted((part, tuple(x for x in thirds if x not in part))))
                  for part in combinations(thirds, 3)}
    require(len(thirds) == 6 and len(partitions) == 10, 'all shared-tail partitions')
    valid = {p for p in partitions if not any(pairs(t) & leave for t in p)}
    return leave, thirds, valid


def symmetries(kind, leave):
    groups = {'middle': ((8, 9, 10), (11, 12, 13)),
              'end': ((9, 10), (11, 12, 13)),
              'triangle': ((8, 9), (10, 11), (12, 13))}[kind]
    result = set()
    for choices in product(*(permutations(g) for g in groups)):
        for swap in range(1 if kind == 'end' else 2):
            p = list(range(18))
            for group, choice in zip(groups, choices):
                for x, y in zip(group, choice):
                    p[x] = y
            if swap:
                exchange = {A: B, B: A}
                exchange.update(zip(groups[0], groups[1]))
                exchange.update(zip(groups[1], groups[0]))
                p = [exchange.get(y, y) for y in p]
            result.add(tuple(p))
    for p in result:
        require(len(set(p)) == 18 and p[U] == U and p[V] == V, 'actual permutation')
        require({tuple(sorted((p[x], p[y]))) for x, y in leave} == leave,
                'leave permutation preserves edges')
    require(all(tuple(p[q[x]] for x in range(18)) in result for p in result for q in result),
            'permutation group closure')
    return sorted(result)


def components(vertices, edges):
    todo = set(vertices)
    result = []
    while todo:
        current = {min(todo)}
        boundary = set(current)
        while boundary:
            neighbors = {y for x in boundary for e in edges if x in e for y in e}
            boundary = neighbors - current
            current |= boundary
        todo -= current
        result.append(tuple(sorted(current)))
    return sorted(result)


def component_completion(edges):
    """Separate recognizer for the cubic/two-triangle degree profiles."""
    degree = Counter(x for e in edges for x in e)
    if set(degree.values()) == {3}:
        comp = components(degree, edges)
        if len(comp) == 2 and all(len(c) == 4 and pairs(c) <= edges for c in comp):
            return [tuple(comp)]
    hubs = [x for x, value in degree.items() if value == 6]
    if len(hubs) == 1 and all(value in (3, 6) for value in degree.values()):
        hub = hubs[0]
        rest = {e for e in edges if hub not in e}
        comp = components(set(degree) - {hub}, rest)
        if len(comp) == 2 and all(len(c) == 3 and pairs(c) <= rest for c in comp):
            lines = tuple(sorted(tuple(sorted((hub,) + c)) for c in comp))
            if pairs(lines[0]) | pairs(lines[1]) == edges:
                return [lines]
    return []


def carrier_checks():
    records = []
    summary = []
    for kind in ('middle', 'end', 'triangle'):
        leave, thirds, valid = template(kind)
        maps = symmetries(kind, leave)
        remaining = set(valid)
        count = 0
        while remaining:
            tails = min(remaining)
            orbit = {tuple(sorted(tuple(sorted(p[x] for x in t)) for t in tails)) for p in maps}
            require(orbit <= remaining, 'disjoint actual partition orbits')
            remaining -= orbit
            count += 1
            fixed = tuple(tuple(sorted((V,) + t)) for t in tails)
            used = pairs(fixed[0]) | pairs(fixed[1])
            require(len(used) == 12 and not used & leave, 'two legal shared words')
            covered = pairs(range(17)) - leave - used
            require(len(covered) == 108 and all(V not in e for e in covered), 'eighteen-word pair domain')
            missing = pairs(D) - covered
            cliques = [q for q in combinations(D, 4) if pairs(q) <= missing]
            completions = [tuple(sorted((q, r))) for q, r in combinations(cliques, 2)
                           if not pairs(q) & pairs(r) and pairs(q) | pairs(r) == missing]
            require(completions == component_completion(missing), 'two completion recognizers agree')
            records.append({'kind': kind, 'shared_tails': tails, 'orbit_size': len(orbit),
                            'missing_edges': sorted(missing), 'four_cliques': cliques,
                            'two_line_completions': completions})
        summary.append({'kind': kind, 'valid_partitions': len(valid),
                        'checked_permutations': len(maps), 'partition_orbits': count})
    require([(s['valid_partitions'], s['checked_permutations'], s['partition_orbits']) for s in summary]
            == [(10, 72, 2), (1, 12, 1), (6, 16, 2)], 'complete five-case carrier')
    require([len(c['two_line_completions']) for c in records] == [1, 0, 1, 0, 0],
            'exact completion classification')
    return summary, records


def gf4_product(a, b):
    result = 0
    while b:
        if b & 1:
            result ^= a
        b >>= 1
        a <<= 1
        if a & 4:
            a ^= 7
    return result


def field_plane():
    result = [frozenset(4*x + (gf4_product(m, x) ^ c) for x in range(4))
              for m in range(4) for c in range(4)]
    result += [frozenset(4*x + y for y in range(4)) for x in range(4)]
    counts = Counter(e for line in result for e in pairs(line))
    require(len(result) == len(set(result)) == 20 and len(counts) == 120
            and set(counts.values()) == {1}, 'positive field plane')
    return result


def validate_lines(lines, tails):
    require(len(lines) == len(tails) == 2, 'two lines and tails')
    require(all(len(q) == 4 and q <= set(D) for q in lines), 'four-point old lines')
    require(len(lines[0] & lines[1]) <= 1, 'edge-disjoint missing cliques')
    require(all(len(t) == 3 and t < q for q, t in zip(lines, tails)), 'three-point line tails')
    require(not tails[0] & tails[1], 'disjoint shared tails')


def interface_check(kind, lines, markers):
    tails = tuple(q - {a} for q, a in zip(lines, markers))
    validate_lines(lines, tails)
    plane = field_plane()
    require(all(q in plane for q in lines), 'fixture missing lines')
    rest = [q for q in plane if q not in lines]
    star = [q | {U} for q in rest] + [t | {U, V} for t in tails]
    require(len(star) == len(set(star)) == 20 and all(len(w) == 5 for w in star), 'positive star')
    require(all(len(x & y) <= 2 for x, y in combinations(star, 2)), 'positive star intersections')
    replication = Counter(x for w in star for x in w)
    deficit = [(x, 5 - replication[x]) for x in range(17) if replication[x] < 5]
    expected = [(V, 3)] + sorted(Counter(markers).items())
    require(sorted(deficit) == sorted(expected), 'fixture deficit row')
    missing = pairs(D) - set().union(*(pairs(q) for q in rest))
    require(missing == pairs(lines[0]) | pairs(lines[1]), 'fixture completion domain')
    remaining_v = 0
    residual = 0
    conflicts = 0
    triples = tuple({tuple(sorted((a,) + p)) for p in combinations(sorted(t), 2)}
                    for a, t in zip(markers, tails))
    require(len(triples[0] | triples[1]) == 6, 'six distinct charging triples')
    for points in combinations(D, 4):
        q = frozenset(points)
        if all(len(q & t) <= 1 for t in tails):
            remaining_v += 1
            require(all(len(q & line) <= 2 for line in lines), 'all remaining-v compatibility')
    for points in combinations(D, 5):
        word = frozenset(points)
        if all(len(word & t) <= 2 for t in tails):
            residual += 1
            bad = any(len(word & line) >= 3 for line in lines)
            charges = {triple for ts in triples for triple in ts if set(triple) <= word}
            require(bad == bool(charges), 'exact six-triple residual conflict interface')
            conflicts += bad
    return {'kind': kind, 'lines': [sorted(q) for q in lines], 'markers': markers,
            'shared_tails': [sorted(t) for t in tails], 'deficit_row': sorted(deficit),
            'positive_star_sha256': sha256(encoded(sorted(sorted(w) for w in star))).hexdigest(),
            'remaining_v_quadruples_checked': remaining_v,
            'residual_five_sets_checked': residual, 'potential_conflicting_five_sets': conflicts,
            'charging_triples': sorted(triples[0] | triples[1]),
            'discarded_packing_words_upper_bound': 6}


def run():
    summary, records = carrier_checks()
    vertical = frozenset((0, 1, 2, 3))
    parallel = frozenset((4, 5, 6, 7))
    horizontal = frozenset((0, 4, 8, 12))
    fixtures = [interface_check('disjoint_lines', (vertical, parallel), (0, 4)),
                interface_check('shared_marker', (vertical, horizontal), (0, 0)),
                interface_check('marker_in_other_tail', (vertical, horizontal), (1, 0))]
    rejected = 0
    malformed = [((vertical, frozenset((0, 1, 4, 5))),
                  (frozenset((1, 2, 3)), frozenset((0, 4, 5)))),
                 ((vertical, horizontal),
                  (frozenset((0, 1, 2)), frozenset((0, 4, 8))))]
    for lines, tails in malformed:
        try:
            validate_lines(lines, tails)
        except ValueError:
            rejected += 1
    require(rejected == 2, 'malformed completion controls')
    return {'agent': 'six-code-1', 'role': 'researcher',
            'status': 'EXACT_SMALL_VALIDATION', 'carrier_summary': summary,
            'normalized_pair_cases': records, 'positive_completion_fixtures': fixtures,
            'malformed_completions_rejected': rejected,
            'upper62_is_imported': True, 'full_first_star_census_completed': False,
            'global_72_word_exclusion': False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write-expected', action='store_true')
    args = parser.parse_args()
    report = run()
    expected = HERE / 'pair_completion_expected.json'
    if args.write_expected:
        expected.write_bytes(encoded(report))
    else:
        require(encoded(report) == encoded(json.loads(expected.read_text())),
                'compact expected report mismatch')
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
