#!/usr/bin/env python3
"""six-reviewer-5: collinearity reconstruction and four-block C-star audit.

No researcher module is imported. Python standard library; exact integers only.
Exhaustion limits raise an exception, never a mathematical negative.
"""
import argparse
from collections import Counter
from itertools import combinations
import hashlib
import json
from pathlib import Path
import time


def require(condition, message):
    if not condition:
        raise ValueError(message)


def digest(value):
    return hashlib.sha256((json.dumps(value, separators=(',', ':'))+'\n').encode()).hexdigest()


def multiply(x, y):
    # Polynomial bits modulo X^2+X+1, not a line parametrization.
    product = 0
    for bit in range(2):
        if y & (1 << bit):
            product ^= x << bit
    if product & 4:
        product ^= 7
    return product


def collinear(quad):
    x0, y0 = divmod(quad[0], 4)
    x1, y1 = divmod(quad[1], 4)
    for point in quad[2:]:
        x, y = divmod(point, 4)
        if multiply(x1 ^ x0, y ^ y0) != multiply(y1 ^ y0, x ^ x0):
            return False
    return True


def affine_audit():
    lines = [q for q in combinations(range(16), 4) if collinear(q)]
    pairs = Counter(p for q in lines for p in combinations(q, 2))
    require(len(lines) == 20 and len(pairs) == 120 and set(pairs.values()) == {1},
            'collinearity plane does not partition pairs')
    origin = [q for q in lines if 0 in q]
    require(len(origin) == 5, 'wrong origin pencil')
    # Check every inverse split, including 1+4 and 2+3 splits in both orientations.
    splits = 0
    for count in range(1, 5):
        for assigned in combinations(origin, count):
            assigned = set(assigned)
            quads = [tuple(sorted((set(q)-{0}) | {16})) if q in assigned else q
                     for q in lines]
            incidences = Counter(x for q in quads for x in q)
            require(incidences[16] == count and incidences[0] == 5-count,
                    'split degrees incorrect')
            require(all(incidences[x] == 5 for x in range(1, 16)),
                    'split has additional underreplicated points')
            require(all(len(set(p)&set(q)) <= 1 for p, q in combinations(quads, 2)),
                    'inverse split repeats a pair')
            splits += 1
    axes = {1, 2, 3, 4, 8, 12}
    configurations = set()
    for q in lines:
        if 0 in q:
            continue
        side_a, side_b = set(q)&axes, set(q)-axes
        if len(side_a) != 2:
            continue
        require(len(side_b) == 2, 'wrong direction multiplicities')
        for u in side_b:
            for v in side_a:
                configurations.add((u, v, next(iter(side_b-{u})), next(iter(side_a-{v}))))
    orbit = set()
    maps = set()
    for s in (1, 2, 3):
        for t in (1, 2, 3):
            for swap in (False, True):
                for conjugate in (False, True):
                    mapping = []
                    for point in range(16):
                        x, y = divmod(point, 4)
                        if conjugate:
                            x, y = multiply(x, x), multiply(y, y)
                        if swap:
                            x, y = y, x
                        mapping.append(4*multiply(s, x)+multiply(t, y))
                    require(set(mapping) == set(range(16)), 'nonbijective frame map')
                    require({tuple(sorted(mapping[x] for x in q)) for q in lines} == set(lines),
                            'frame map does not preserve collinearity')
                    maps.add(tuple(mapping))
                    orbit.add(tuple(mapping[x] for x in (11, 4, 14, 1)))
    require(orbit == configurations and len(orbit) == len(maps) == 36,
            'distinguished normal form does not cover all fixed-axis frames')
    axes_lines = {(0, 1, 2, 3), (0, 4, 8, 12)}
    words = [tuple(sorted(({16} | (set(q)-{0}) if q in axes_lines else set(q)) | {17}))
             for q in lines]
    require(all(len(q) == 5 for q in words), 'bad split words')
    require(all(len(set(p)&set(q)) <= 2 for p, q in combinations(words, 2)),
            'split words not a packing')
    return words, {'plane_lines': len(lines), 'pair_partition': len(pairs),
                   'inverse_splits_checked': splits, 'distinguished_frames': len(orbit),
                   'plane_lines_sha256': digest(lines), 'z_star_sha256': digest(words)}


def construct(chosen, words):
    a, z, u, c = 16, 17, 11, 14
    vertices = set(range(18))-{a}
    side_b = set(range(1, 16))-{1, 2, 3, 4, 8, 12}
    leftover = tuple(sorted({2, 3, 8, 12}-set(chosen)))
    leave = {tuple(sorted((z, x))) for x in side_b|{0}}
    leave |= {tuple(sorted(e)) for e in [(u, z), (u, c), (u, 4), (u, 1),
                                          (c, z), (c, chosen[0]), (c, chosen[1]), leftover]}
    degree = Counter(x for e in leave for x in e)
    require(len(leave) == 16 and all(degree[x] == (10 if x == z else 4 if x in {u, c} else 1)
                                   for x in vertices), 'incomplete leave graph')
    fixed = [(1, 2, 3, z), (4, 8, 12, z)]
    covered = {p for q in fixed for p in combinations(q, 2)}
    conflict = sorted(leave & covered)
    if conflict:
        return None, None, {'case': list(chosen), 'status': 'FIXED_BLOCK_LEAVE_CONFLICT',
                            'conflicting_pairs': conflict}
    rows = sorted(set(combinations(sorted(vertices), 2))-leave-covered)
    require(len(rows) == 108 and all(z not in p for p in rows), 'wrong residual rows')
    triples = {triple for word in words for triple in combinations(word, 3)}
    columns = []
    rowset = set(rows)
    for q in combinations(range(16), 4):
        word = tuple(sorted(q+(a,)))
        passes_triples = all(t not in triples for t in combinations(word, 3))
        require(passes_triples == all(len(set(word)&set(w)) <= 2 for w in words),
                'triple compatibility differs from direct intersections')
        if set(combinations(q, 2)) <= rowset and passes_triples:
            columns.append(q)
    return rows, columns, {'case': list(chosen), 'candidate_quads': len(columns),
                           'rows_sha256': digest(rows), 'candidate_quads_sha256': digest(columns)}


def star_cover(rows, columns, center=14, seconds=45, node_limit=1000000):
    """Enumerate center's complete star; memoized residual pair partitions.

    Each center quad uses three different center-neighbors. At a star state,
    branch on the least unused neighbor and all eligible triples containing it.
    Each full star appears exactly once. Then prohibit all other center quads.
    Residual state is just its uncovered-pair mask; available quads are derived
    afresh by containment, so memoization omits no information.
    """
    start = time.monotonic()
    rows = sorted(rows)
    index = {p: i for i, p in enumerate(rows)}
    edges = [sum(1 << index[p] for p in combinations(q, 2)) for q in columns]
    star = [i for i, q in enumerate(columns) if center in q]
    ordinary = [i for i, q in enumerate(columns) if center not in q]
    neighbors = sorted({next(x for x in pair if x != center) for pair in rows if center in pair})
    require(len(neighbors) % 3 == 0, 'center cannot have an integral replication')
    triples = {i: frozenset(columns[i])-{center} for i in star}
    by_point = {p: [i for i in star if p in triples[i]] for p in neighbors}
    row_options = [[i for i in ordinary if edges[i] >> j & 1] for j in range(len(rows))]
    failed = set()
    nodes = star_states = classes = residual_calls = cache_hits = zero_leaves = 0
    stream = hashlib.sha256()

    def budget():
        nonlocal nodes
        nodes += 1
        if nodes > node_limit or (nodes % 64 == 0 and time.monotonic()-start > seconds):
            raise TimeoutError('INCOMPLETE: C-star enumeration limit')

    def residual(remaining):
        nonlocal residual_calls, cache_hits, zero_leaves
        budget()
        residual_calls += 1
        if not remaining:
            return []
        if remaining in failed:
            cache_hits += 1
            return None
        scan = remaining
        best = None
        while scan:
            low = scan & -scan
            j = low.bit_length()-1
            options = [i for i in row_options[j] if edges[i] & remaining == edges[i]]
            if not options:
                zero_leaves += 1
                failed.add(remaining)
                return None
            if best is None or len(options) < len(best):
                best = options
            scan ^= low
        for i in best:
            witness = residual(remaining ^ edges[i])
            if witness is not None:
                return [i]+witness
        failed.add(remaining)
        return None

    full = (1 << len(rows))-1

    def center_star(unused, selected, used):
        nonlocal star_states, classes
        budget()
        star_states += 1
        if not unused:
            require(len(selected)*3 == len(neighbors), 'star incomplete')
            classes += 1
            stream.update((' '.join(str(i) for i in selected)+'\n').encode())
            witness = residual(full ^ used)
            return selected+witness if witness is not None else None
        first = min(unused)
        for i in by_point[first]:
            if triples[i] <= unused:
                require(not (used & edges[i]), 'star repeats a pair')
                result = center_star(unused-triples[i], selected+[i], used | edges[i])
                if result is not None:
                    return result
        return None

    witness = center_star(frozenset(neighbors), [], 0)
    report = {'status': 'WITNESS' if witness is not None else 'COMPLETE_NO_COVER',
              'center': center, 'center_neighbors': len(neighbors), 'center_quads': len(star),
              'center_star_states': star_states, 'complete_center_stars': classes,
              'residual_calls': residual_calls, 'memo_hits': cache_hits,
              'zero_option_leaves': zero_leaves, 'memo_states': len(failed), 'nodes': nodes,
              'star_stream_sha256': stream.hexdigest()}
    if witness is not None:
        quads = [columns[i] for i in witness]
        counts = Counter(p for q in quads for p in combinations(q, 2))
        require(set(counts) == set(rows) and set(counts.values()) == {1}, 'invalid returned cover')
        report['quadruples'] = quads
    return report


def controls(lines_words, baseline):
    results = []
    for name, quads, n, center in (
            ('affine_plane', [tuple(sorted((set(w)-{17}-{16}) | ({0} if 16 in w else set())))
                             for w in lines_words], 16, 14),
            ('published_69_word_point_0', [tuple(x for x in word if x != 0)
                 for word in baseline if 0 in word], 18, 14)):
        if name == 'published_69_word_point_0':
            require(len(quads) == 20, 'published positive fixture not saturated')
            vertices = list(range(1, n))
        else:
            vertices = list(range(n))
        rows = {p for q in quads for p in combinations(q, 2)}
        require(len(rows) == 6*len(quads), 'fixture repeats pairs')
        columns = [q for q in combinations(vertices, 4) if set(combinations(q, 2)) <= rows]
        report = star_cover(rows, columns, center=center)
        require(report['status'] == 'WITNESS', 'C-star search rejects positive control')
        results.append({'fixture': name, 'quadruples': len(report['quadruples']),
                        'nodes': report['nodes'], 'complete_center_stars': report['complete_center_stars']})
    return results


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--baseline', type=Path, required=True)
    parser.add_argument('--expected', type=Path)
    parser.add_argument('--write', type=Path)
    args = parser.parse_args()
    words, affine = affine_audit()
    baseline_lines = args.baseline.read_text().splitlines()
    require(all(len(line) == 18 and set(line) <= {'0', '1'} for line in baseline_lines),
            'baseline words must be eighteen binary digits')
    baseline = [tuple(i for i, bit in enumerate(line) if bit == '1')
                for line in baseline_lines]
    require(len(baseline) == 69 and all(len(w) == 5 and max(w) < 18 for w in baseline),
            'bad baseline code')
    require(all(len(set(p)&set(q)) <= 2 for p, q in combinations(baseline, 2)),
            'baseline does not have distance six')
    results = []
    for chosen in combinations((2, 3, 8, 12), 2):
        rows, columns, report = construct(chosen, words)
        if rows is not None:
            report.update(star_cover(rows, columns))
            require(report['status'] == 'COMPLETE_NO_COVER', 'packing obstruction not verified')
        results.append(report)
    output = {'reviewer': 'six-reviewer-5', 'role': 'independent mathematical reviewer',
              'method': 'determinant collinearity; forbidden triples; C-centered four-block stars; memoized residual pair masks',
              'affine': affine, 'cases': results, 'positive_controls': controls(words, baseline),
              'total_complete_C_stars': sum(r.get('complete_center_stars', 0) for r in results),
              'all_six_cases_complete': True, 'global_72_word_exclusion': False}
    if args.expected:
        require(json.loads(args.expected.read_text()) == json.loads(json.dumps(output)),
                'compact expected evidence differs')
    if args.write:
        args.write.write_text(json.dumps(output, indent=2, sort_keys=True)+'\n')
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
