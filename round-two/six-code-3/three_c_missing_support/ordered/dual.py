"""All pairwise physical class isomorphisms via literal block incidence, not colors."""
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
    digest = hashlib.sha256(json.dumps(inp, sort_keys=True, separators=(',', ':')).encode()).hexdigest()
    records = inp['records']
    require(digest == expected['input_math_sha256'] and len(records) == 56, 'whole completed physical input')
    systems = [[list(map(frozenset, cls)) for cls in r['classes']] for r in records]
    # The first two classes have identical named cells in every input, so the
    # incidence-forced map can be computed once for each prospective row map.
    first, second, _ = systems[0]
    physical_maps = []
    for row_image in itertools.permutations(range(4)):
        tick()
        column_image = []
        for col in second:
            missing_source_rows = [r for r, row in enumerate(first) if not (row & col)]
            require(len(missing_source_rows) == 1, 'unique absent source incidence')
            target_row = first[row_image[missing_source_rows[0]]]
            missing_target_columns = [c for c, target_col in enumerate(second) if not (target_row & target_col)]
            require(len(missing_target_columns) == 1, 'unique forced target column')
            column_image.append(missing_target_columns[0])
        point_image = []
        for p in range(12):
            source_row = next(r for r, row in enumerate(first) if p in row)
            source_col = next(c for c, col in enumerate(second) if p in col)
            target = first[row_image[source_row]] & second[column_image[source_col]]
            require(len(target) == 1, 'unique incidence-forced actual point')
            point_image.append(next(iter(target)))
        require(sorted(point_image) == list(range(12)), 'whole physical bijection')
        physical_maps.append((row_image, point_image))
    transports, relations = [], []
    for source in range(56):
        related = []
        for target in range(56):
            any_iso = False
            target_third = set(systems[target][2])
            target_words = {frozenset(w) for w in records[target]['anchor']}
            for row_image, point_image in physical_maps:
                tick()
                third_image = {frozenset(point_image[p] for p in triple) for triple in systems[source][2]}
                if third_image == target_third:
                    full_image = list(range(6)) + [6 + p for p in point_image]
                    require({frozenset(full_image[p] for p in w) for w in records[source]['anchor']} == target_words,
                            'all thirteen physical words, preserving C-pair class roles')
                    any_iso = True
                    transports.append(dict(source=source, row_permutation=list(row_image),
                                           point_image=full_image, target=target))
            related.append(str(int(any_iso)))
        relations.append(''.join(related))
    transports.sort(key=lambda t: (t['source'], t['row_permutation']))
    require(len(transports) == 56 * 24 and len({(t['source'], tuple(t['row_permutation'])) for t in transports}) == 56 * 24,
            'every distinct physical isomorphism and its unique target')
    unseen, orbits = set(range(56)), []
    while unseen:
        seed = min(unseen)
        component = [t for t in range(56) if relations[seed][t] == '1']
        require(set(component) <= unseen and all(relations[t] == relations[seed] for t in component),
                'whole physical equivalence classes')
        orbits.append(component)
        unseen -= set(component)
    mathematics = dict(cases=56, input_math_sha256=digest, equivalence=relations, orbits=orbits,
                       all_transports=transports, fixed_special_points=list(range(6)),
                       ordered_parallel_class_roles_preserved=True)
    common = hashlib.sha256(json.dumps(mathematics, sort_keys=True, separators=(',', ':')).encode()).hexdigest()
    result = dict(agent='six-code-3', role='researcher', status='COMPLETE_PAIRWISE_PHYSICAL_ANCHOR_ISOMORPHISMS',
                  mathematics=mathematics, common_math_sha256=common, states=STATES,
                  guard_states=500000, guard_seconds=20)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + '\n')
    print(json.dumps(dict(status=result['status'], orbit_sizes=[len(x) for x in orbits],
                          common_math_sha256=common, states=STATES), sort_keys=True))


if __name__ == '__main__':
    main()
