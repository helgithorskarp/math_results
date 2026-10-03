"""Independent literal triple-partition enumeration on twelve named cells."""
import argparse
import hashlib
import itertools
import json
import time
from pathlib import Path

START = time.monotonic()
STATES = 0


def require(condition, message):
    if not condition:
        raise ValueError(message)


def tick():
    global STATES
    STATES += 1
    if STATES > 500000 or time.monotonic() - START > 20:
        raise RuntimeError('INCOMPLETE: original500000/20 guard')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--output', type=Path, required=True)
    args = ap.parse_args()
    expected = json.loads((Path(__file__).parent / 'EXPECTED.json').read_text())
    points = list(range(12))
    coordinates = {p: (p // 3, [j for j in range(4) if j != p // 3][p % 3]) for p in points}
    first = [tuple(p for p in points if coordinates[p][0] == r) for r in range(4)]
    second = [tuple(p for p in points if coordinates[p][1] == c) for c in range(4)]
    # Begin with literal 3-subsets, not color arrays or row permutations.
    candidates = []
    for triple in itertools.combinations(points, 3):
        tick()
        if all(len(set(triple) & set(t)) <= 1 for t in first + second):
            candidates.append(frozenset(triple))
    partitions = []

    def visit(remaining, chosen):
        tick()
        if not remaining:
            require(len(chosen) == 4, 'entire third parallel class')
            partitions.append(chosen)
            return
        pivot = min(remaining)
        for triple in candidates:
            if pivot in triple and triple <= remaining:
                visit(remaining - triple, chosen + [triple])

    visit(frozenset(points), [])
    records = []
    for partition in partitions:
        tick()
        # Labels are assigned after the whole physical partition was constructed.
        by_missing_row = {}
        for triple in partition:
            missing = [r for r in range(4) if not (set(first[r]) & set(triple))]
            require(len(missing) == 1 and missing[0] not in by_missing_row, 'missing-row perfect matching')
            by_missing_row[missing[0]] = sorted(triple)
        require(sorted(by_missing_row) == list(range(4)), 'all four missing rows')
        third = [by_missing_row[r] for r in range(4)]
        colors = [next(r for r in range(4) if p in third[r]) for p in points]
        missing_columns = [next(r for r in range(4) if not (set(t) & set(third[r]))) for t in second]
        require(sorted(missing_columns) == list(range(4)), 'actual missing-column matching')
        classes = [[list(t) for t in first], [list(t) for t in second], third]
        anchor = [[1, 2, 3, 4, 5]]
        for pair, cls in zip([(1, 2), (1, 3), (2, 3)], classes):
            for triple in cls:
                anchor.append(sorted(list(pair) + [6 + p for p in triple]))
        require(all(len(set(x) & set(y)) <= 2 for x, y in itertools.combinations(anchor, 2)),
                'literal constructed thirteen-word subpacking')
        records.append(dict(colors=colors, classes=classes, column_missing=missing_columns, anchor=anchor))
    records.sort(key=lambda r: r['colors'])
    require(len({tuple(r['colors']) for r in records}) == len(records), 'partition enumeration has no duplicates')
    # Independently rank normalized rows in base six by counting lexicographic permutations.
    rows = [[s for s in range(4) if s != r] for r in range(4)]
    coverage = ['0'] * expected['normalized_row_fillings']
    for rec in records:
        index = 0
        for r in range(4):
            actual = rec['colors'][3 * r:3 * r + 3]
            require(sorted(actual) == rows[r], 'normalization after partition search')
            rank = sum(1 for perm in itertools.permutations(rows[r]) if tuple(perm) < tuple(actual))
            index = 6 * index + rank
        require(coverage[index] == '0', 'unique complete mask index')
        coverage[index] = '1'
    baseline = next((r for r in records if r['colors'] == expected['baseline_colors']), None)
    require(baseline is not None, 'classical F4 literal control survives independent partition enumeration')
    mathematics = dict(domain=1296, coverage=''.join(coverage), records=records, baseline=baseline)
    common = hashlib.sha256(json.dumps(mathematics, sort_keys=True, separators=(',', ':')).encode()).hexdigest()
    result = dict(agent='six-code-3', role='researcher', status='COMPLETE_LITERAL_TRIPLE_PARTITIONS',
                  candidate_triples=len(candidates), physical_partitions=len(partitions), states=STATES,
                  guard_states=500000, guard_seconds=20, mathematics=mathematics, common_math_sha256=common)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + '\n')
    print(json.dumps(dict(status=result['status'], accepted=len(records), states=STATES,
                          common_math_sha256=common), sort_keys=True))


if __name__ == '__main__':
    main()
