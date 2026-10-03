"""All normalized class-role permutations and their24 actual row-member maps."""
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
        for order, perm in itertools.product(itertools.permutations(range(3)), itertools.permutations(range(4))):
            tick()
            chosen_classes = [rec['classes'][k] for k in order]
            absent_second = [next(a for a in range(4) if not (set(chosen_classes[0][a]) & set(t)))
                             for t in chosen_classes[1]]
            absent_third = [next(a for a in range(4) if not (set(chosen_classes[0][a]) & set(t)))
                            for t in chosen_classes[2]]
            point_image = []
            colors = [None] * 12
            for old in range(12):
                memberships = [next(a for a, t in enumerate(cls) if old in t) for cls in chosen_classes]
                new = point_at[(perm[memberships[0]], perm[absent_second[memberships[1]]])]
                point_image.append(new)
                colors[new] = perm[absent_third[memberships[2]]]
            require(tuple(colors) in by_colors, 'entire normalized domain closed under exact relabelings')
            target = by_colors[tuple(colors)]
            pairs = [{1, 2}, {1, 3}, {2, 3}]
            c_image = next(cp for cp in itertools.permutations([1, 2, 3])
                           if all({cp[p - 1] for p in pairs[order[k]]} == pairs[k] for k in range(3)))
            full_image = [0] + list(c_image) + [4, 5] + [6 + p for p in point_image]
            actual_words = sorted(sorted(full_image[p] for p in w) for w in rec['anchor'])
            require(actual_words == sorted(records[target]['anchor']), 'every word and named special point transported')
            images.add(target)
            transports.append(dict(source=source, class_order=list(order), row_permutation=list(perm),
                                   point_image=full_image, target=target))
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
                       all_transports=transports, fixed_special_points=[0, 4, 5],
                       ordered_parallel_class_roles_preserved=False, C_points_may_permute=True)
    common = hashlib.sha256(json.dumps(mathematics, sort_keys=True, separators=(',', ':')).encode()).hexdigest()
    result = dict(agent='six-code-3', role='researcher', status='COMPLETE_FULL_NORMALIZED_ANCHOR_RELABELINGS',
                  mathematics=mathematics, common_math_sha256=common, states=STATES,
                  guard_states=500000, guard_seconds=20)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + '\n')
    print(json.dumps(dict(status=result['status'], orbit_sizes=[len(x) for x in orbits],
                          common_math_sha256=common, states=STATES), sort_keys=True))


if __name__ == '__main__':
    main()
