"""Simultaneous row/column/color S4 relabelings of all validated physical anchors."""
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
    root = Path(__file__).parent
    inp = json.loads((root / 'INPUT.json').read_text())
    expected = json.loads((root / 'EXPECTED.json').read_text())
    records = inp['records']
    digest = hashlib.sha256(json.dumps(inp, sort_keys=True, separators=(',', ':')).encode()).hexdigest()
    require(digest == expected['input_math_sha256'] and len(records) == 56, 'whole completed input')
    cells = [(i, j) for i in range(4) for j in range(4) if i != j]
    point_at = {cell: p for p, cell in enumerate(cells)}
    by_colors = {tuple(r['colors']): i for i, r in enumerate(records)}
    relations, transports = [], []
    for source, rec in enumerate(records):
        images = set()
        for perm in itertools.permutations(range(4)):
            tick()
            point_image = [point_at[(perm[i], perm[j])] for i, j in cells]
            colors = [None] * 12
            for old, new in enumerate(point_image):
                colors[new] = perm[rec['colors'][old]]
            require(tuple(colors) in by_colors, 'entire normalized domain closed under exact relabelings')
            target = by_colors[tuple(colors)]
            full_image = list(range(6)) + [6 + p for p in point_image]
            actual_words = sorted(sorted(full_image[p] for p in w) for w in rec['anchor'])
            require(actual_words == sorted(records[target]['anchor']), 'every word and named special point transported')
            images.add(target)
            transports.append(dict(source=source, row_permutation=list(perm), point_image=full_image, target=target))
        relations.append(''.join('1' if j in images else '0' for j in range(56)))
    unseen = set(range(56))
    orbits = []
    while unseen:
        representative = min(unseen)
        orbit = [j for j in range(56) if relations[representative][j] == '1']
        require(set(orbit) <= unseen and all(relations[j] == relations[representative] for j in orbit),
                'whole disjoint equivalence components')
        orbits.append(orbit)
        unseen -= set(orbit)
    mathematics = dict(cases=56, input_math_sha256=digest, equivalence=relations, orbits=orbits,
                       all_transports=transports, fixed_special_points=list(range(6)),
                       ordered_parallel_class_roles_preserved=True)
    common = hashlib.sha256(json.dumps(mathematics, sort_keys=True, separators=(',', ':')).encode()).hexdigest()
    result = dict(agent='six-code-3', role='researcher', status='COMPLETE_SIMULTANEOUS_S4_ANCHOR_RELABELINGS',
                  mathematics=mathematics, common_math_sha256=common, states=STATES,
                  guard_states=500000, guard_seconds=20)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + '\n')
    print(json.dumps(dict(status=result['status'], orbit_sizes=[len(x) for x in orbits],
                          common_math_sha256=common, states=STATES), sort_keys=True))


if __name__ == '__main__':
    main()
