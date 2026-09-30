"""Complete mask/CSP generation and incidence-bitset no-edge proof.

No model dump is needed. An elapsed guard raises INCOMPLETE, never a
nonexistence result. Print only the compact deterministic replay manifest.
"""
from collections import Counter
from hashlib import sha256
from itertools import combinations
from pathlib import Path
import argparse
import json
import time

from geometry import classical_design, mask, points, require


def canonical_hash(records):
    return sha256((json.dumps(records, separators=(',', ':')) + '\n').encode()).hexdigest()


def enumerate_records(circles, gap):
    start = time.monotonic()
    design = set(circles)
    records = []
    histogram = Counter()
    eligible = Counter()
    for pts in combinations(range(17), 5):
        require(time.monotonic() - start < 45, 'INCOMPLETE: generation time guard')
        b = mask(pts)
        if b in design:
            continue
        meetings = [(c, (b & c).bit_count()) for c in circles]
        if any(n == 4 and c != gap for c, n in meetings):
            continue
        blockers = [c for c, n in meetings if n >= 3 and c != gap]
        options = [[c ^ (1 << p) for p in pts if c >> p & 1] for c in blockers]
        require(all(len(qs) == 3 for qs in options), 'invalid non-gap blocker')
        before = len(records)
        selected = []

        def visit(remaining):
            if not remaining:
                records.append((b, tuple(sorted(selected))))
                return
            filtered = [[q for q in qs if all((q & r).bit_count() <= 1 for r in selected)]
                        for qs in remaining]
            i = min(range(len(filtered)), key=lambda j: len(filtered[j]))
            tail = filtered[:i] + filtered[i + 1:]
            for q in filtered[i]:
                selected.append(q)
                visit(tail)
                selected.pop()

        visit(options)
        eligible[len(blockers)] += 1
        histogram[(len(blockers), len(records) - before)] += 1
    records.sort()
    require(len(set(records)) == len(records), 'duplicate records')
    census = {'eligible_outsiders': {str(k): v for k, v in sorted(eligible.items())},
              'solution_counts': [{'blockers': k[0], 'solutions': k[1], 'outsiders': n}
                                  for k, n in sorted(histogram.items())],
              'records': len(records), 'records_sha256': canonical_hash(records)}
    return records, census


def no_edges(records):
    """A repeated old triple forbids the outsiders; incompatible distinct
    old4-sets forbid their union. Identical old4-sets are permitted."""
    old_rows = {}
    q_rows = {}
    for i, (b, qs) in enumerate(records):
        bit = 1 << i
        for triple in combinations(points(b), 3):
            t = mask(triple)
            old_rows[t] = old_rows.get(t, 0) | bit
        for q in qs:
            q_rows[q] = q_rows.get(q, 0) | bit
    q_bad = {}
    for q in q_rows:
        bad = 0
        for r, row in q_rows.items():
            if q != r and (q & r).bit_count() > 1:
                bad |= row
        q_bad[q] = bad
    all_records = (1 << len(records)) - 1
    for b, qs in records:
        bad = 0
        for triple in combinations(points(b), 3):
            bad |= old_rows[mask(triple)]
        for q in qs:
            bad |= q_bad[q]
        require((all_records & ~bad) == 0, 'a compatible pair exists')
    return {'contained_old_parts': len(q_rows), 'compatibility_edges': 0}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', type=Path)
    args = parser.parse_args()
    circles, gap = classical_design()
    records, census = enumerate_records(circles, gap)
    result = {'design_blocks': len(circles), 'old_noncircles': 6120, 'gap_circle': gap,
              'design_sha256': canonical_hash(circles), **census, **no_edges(records)}
    if args.check:
        expected = json.loads(args.check.read_text())['generator']
        require(result == expected, 'generator manifest mismatch')
    print(json.dumps(result, sort_keys=True))


if __name__ == '__main__':
    main()
