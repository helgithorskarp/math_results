"""Complete exact replacement records and graphs for two missing circles.

All arithmetic is integral. The three cases cover gap-pair intersections
0,1,2; verify_two_gap.py independently checks their normalization and
rebuilds the entire enumeration. No full generated corpus is written.
"""
from collections import Counter
from hashlib import sha256
from itertools import combinations
from pathlib import Path
import argparse
import json
import time

from geometry import classical_design, mask, points, require


def digest(records):
    return sha256((json.dumps(records, separators=(',', ':')) + '\n').encode()).hexdigest()


def enumerate_masks(circles, gaps):
    start = time.monotonic()
    circle_set = set(circles)
    gaps = set(gaps)
    records = []
    eligible = Counter()
    histogram = Counter()
    nodes = 0
    tested = 0
    for pts in combinations(range(17), 5):
        require(time.monotonic() - start < 45, 'INCOMPLETE: generation time guard')
        b = mask(pts)
        if b in circle_set:
            continue
        tested += 1
        meetings = [(c, (b & c).bit_count()) for c in circles if c not in gaps]
        if any(n >= 4 for c, n in meetings):
            continue
        blockers = [c for c, n in meetings if n == 3]
        options = [[c ^ (1 << p) for p in pts if c >> p & 1] for c in blockers]
        require(all(len(qs) == 3 for qs in options), 'incorrect mandatory alternatives')
        selected = []
        before = len(records)

        def visit(remaining):
            nonlocal nodes
            nodes += 1
            if nodes % 1024 == 0:
                require(time.monotonic() - start < 45, 'INCOMPLETE: generation time guard')
                require(len(records) <= 40000, 'INCOMPLETE: record-count guard')
            if not remaining:
                records.append((b, tuple(sorted(selected))))
                return
            filtered = [[q for q in qs if all((q & r).bit_count() <= 1 for r in selected)]
                        for qs in remaining]
            i = min(range(len(filtered)), key=lambda j: len(filtered[j]))
            if not filtered[i]:
                return
            tail = filtered[:i] + filtered[i + 1:]
            for q in filtered[i]:
                selected.append(q)
                visit(tail)
                selected.pop()

        visit(options)
        eligible[len(blockers)] += 1
        histogram[(len(blockers), len(records) - before)] += 1
    records.sort()
    require(tested == 6120 and len(set(records)) == len(records),
            'incorrect old-set coverage or duplicate record')
    return records, {'records': len(records), 'records_sha256': digest(records),
                     'eligible_outsiders': {str(k): v for k, v in sorted(eligible.items())},
                     'solution_counts': [{'mandatory_circles': k[0], 'assignments': k[1],
                                         'outsiders': v} for k, v in sorted(histogram.items())]}


def graph_masks(records):
    start = time.monotonic()
    n = len(records)
    require(n <= 40000, 'INCOMPLETE: graph memory guard')
    old_rows = {}
    q_records = {}
    for i, (b, qs) in enumerate(records):
        bit = 1 << i
        for triple in combinations(points(b), 3):
            t = mask(triple)
            old_rows[t] = old_rows.get(t, 0) | bit
        for q in qs:
            q_records[q] = q_records.get(q, 0) | bit
    q_bad = {}
    for q in q_records:
        bad = 0
        for r, vertices in q_records.items():
            if r != q and (q & r).bit_count() > 1:
                bad |= vertices
        q_bad[q] = bad
    universe = (1 << n) - 1
    adjacency = []
    for b, qs in records:
        bad = 0
        for triple in combinations(points(b), 3):
            bad |= old_rows[mask(triple)]
        for q in qs:
            bad |= q_bad[q]
        adjacency.append(universe & ~bad)
    edges = 0
    graph_digest = sha256()
    width = (n + 7) // 8
    for i, row in enumerate(adjacency):
        require(time.monotonic() - start < 45, 'INCOMPLETE: graph time guard')
        require(not row >> i & 1, 'self-loop')
        graph_digest.update(row.to_bytes(width, 'little'))
        later = row & ~((1 << (i + 1)) - 1)
        while later:
            bit = later & -later
            j = bit.bit_length() - 1
            require(adjacency[j] >> i & 1, 'asymmetric graph')
            require(not row & adjacency[j], 'compatible triple exists')
            edges += 1
            later ^= bit
    require(2 * edges == sum(row.bit_count() for row in adjacency), 'incomplete edge census')
    return adjacency, {'vertices': n, 'old_parts': len(q_records), 'edges': edges,
                       'triangles': 0, 'graph_sha256': graph_digest.hexdigest()}


def generate():
    circles, gap = classical_design()
    cases = []
    for intersection, second in ((0, 1828), (1, 5169), (2, 362)):
        require(second in circles and (second & gap).bit_count() == intersection,
                'incorrect gap representative')
        gaps = sorted((gap, second))
        records, census = enumerate_masks(circles, gaps)
        _, graph = graph_masks(records)
        cases.append({'gap_intersection': intersection, 'gaps': gaps,
                      'enumeration': census, 'graph': graph})
    return {'design_blocks': len(circles), 'design_sha256': digest(circles),
            'first_gap': gap, 'cases': cases}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', type=Path)
    args = parser.parse_args()
    result = generate()
    if args.check is not None:
        expected = json.loads(args.check.read_text())
        require(result == expected['generator'], 'two-gap manifest mismatch')
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
