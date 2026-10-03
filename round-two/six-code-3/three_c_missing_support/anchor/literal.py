"""All normalized 6**4 off-diagonal row fillings; no symmetry quotient."""
import argparse
import hashlib
import itertools
import json
import time
from pathlib import Path

CELLS = [(i, j) for i in range(4) for j in range(4) if i != j]
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


def gf4_multiply(a, b):
    # Polynomial representatives 0, 1, z, 1+z, reduced by z*z+z+1.
    result = 0
    while b:
        if b & 1:
            result ^= a
        a <<= 1
        if a & 4:
            a ^= 7
        b >>= 1
    return result


def record(colors):
    require(len(colors) == 12, 'literal twelve-cell coloring')
    for i in range(4):
        row = [colors[k] for k, cell in enumerate(CELLS) if cell[0] == i]
        require(sorted(row) == [s for s in range(4) if s != i], 'row missing its own label')
    missing = []
    for j in range(4):
        column = [colors[k] for k, cell in enumerate(CELLS) if cell[1] == j]
        require(len(set(column)) == 3, 'three distinct column labels')
        missing.append(next(s for s in range(4) if s not in column))
    require(sorted(missing) == list(range(4)), 'actual column-missing permutation')
    classes = [
        [[k for k, cell in enumerate(CELLS) if cell[0] == i] for i in range(4)],
        [[k for k, cell in enumerate(CELLS) if cell[1] == j] for j in range(4)],
        [[k for k, color in enumerate(colors) if color == s] for s in range(4)],
    ]
    for cls in classes:
        require(all(len(triple) == 3 for triple in cls) and
                sorted(k for triple in cls for k in triple) == list(range(12)), 'literal parallel class')
    for a, b in itertools.combinations(range(3), 2):
        require(all(len(set(x) & set(y)) <= 1 for x in classes[a] for y in classes[b]),
                'literal cross-class intersections')
    anchor = [[1, 2, 3, 4, 5]]
    for pair, cls in zip([(1, 2), (1, 3), (2, 3)], classes):
        anchor += [sorted(list(pair) + [6 + k for k in triple]) for triple in cls]
    require(len({tuple(word) for word in anchor}) == 13 and
            all(len(set(word)) == 5 and 0 not in word for word in anchor), 'thirteen distinct words avoiding heavy0')
    require(all(len(set(x) & set(y)) <= 2 for x, y in itertools.combinations(anchor, 2)),
            'literal anchor intersection bound')
    for pair in [(1, 2), (1, 3), (2, 3)]:
        tails = [set(word) - set(pair) for word in anchor if set(pair) <= set(word)]
        require(len(tails) == 5 and sorted(x for tail in tails for x in tail) ==
                [x for x in range(1, 18) if x not in pair], 'five disjoint pair tails; only heavy0 missing')
    return dict(colors=list(colors), classes=classes, column_missing=missing, anchor=anchor)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--output', type=Path, required=True)
    args = ap.parse_args()
    expected = json.loads((Path(__file__).parent / 'EXPECTED.json').read_text())
    baseline = [gf4_multiply(2, i) ^ gf4_multiply(3, j) for i, j in CELLS]
    require(baseline == expected['baseline_colors'], 'classical exact F4 baseline before enumeration')
    baseline_record = record(baseline)
    choices = [list(itertools.permutations([s for s in range(4) if s != i])) for i in range(4)]
    records, coverage = [], []
    for rows in itertools.product(*choices):
        tick()
        colors = [s for row in rows for s in row]
        accepted = all(len({colors[k] for k, cell in enumerate(CELLS) if cell[1] == j}) == 3 for j in range(4))
        coverage.append(int(accepted))
        if accepted:
            records.append(record(colors))
    records.sort(key=lambda r: r['colors'])
    require(len(coverage) == expected['normalized_row_fillings'] and baseline_record in records,
            'whole declared input domain and positive baseline')
    mathematics = dict(domain=1296, coverage=''.join(str(x) for x in coverage), records=records,
                       baseline=baseline_record)
    common = hashlib.sha256(json.dumps(mathematics, sort_keys=True, separators=(',', ':')).encode()).hexdigest()
    result = dict(agent='six-code-3', role='researcher', status='COMPLETE_LITERAL_ROW_FILLINGS',
                  states=STATES, guard_states=500000, guard_seconds=20, mathematics=mathematics,
                  common_math_sha256=common)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + '\n')
    print(json.dumps(dict(status=result['status'], accepted=len(records), states=STATES,
                          common_math_sha256=common), sort_keys=True))


if __name__ == '__main__':
    main()
