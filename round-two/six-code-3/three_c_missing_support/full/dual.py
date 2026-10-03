"""All pairwise physical isomorphisms allowing class roles, using literal incidence."""
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
    target_first, target_second, _ = systems[0]
    transports, relations = [], []
    for source in range(56):
        physical_maps = []
        for order, row_image in itertools.product(itertools.permutations(range(3)), itertools.permutations(range(4))):
            tick()
            first, second, third = [systems[source][k] for k in order]
            column_image = []
            for col in second:
                missing_source_rows = [r for r, row in enumerate(first) if not (row & col)]
                require(len(missing_source_rows) == 1, 'unique absent source incidence')
                target_row = target_first[row_image[missing_source_rows[0]]]
                missing_target_columns = [c for c, target_col in enumerate(target_second) if not (target_row & target_col)]
                require(len(missing_target_columns) == 1, 'unique forced target column')
                column_image.append(missing_target_columns[0])
            point_image = []
            for p in range(12):
                source_row = next(r for r, row in enumerate(first) if p in row)
                source_col = next(c for c, col in enumerate(second) if p in col)
                target = target_first[row_image[source_row]] & target_second[column_image[source_col]]
                require(len(target) == 1, 'unique incidence-forced actual point')
                point_image.append(next(iter(target)))
            require(sorted(point_image) == list(range(12)), 'whole physical bijection')
            inverse_order = [order.index(k) for k in range(3)]
            c_image = [3 - inverse_order[3 - c] for c in [1, 2, 3]]
            full_image = [0] + c_image + [4, 5] + [6 + p for p in point_image]
            third_image = {frozenset(point_image[p] for p in triple) for triple in third}
            physical_maps.append((order, row_image, full_image, third_image))
        related = []
        for target in range(56):
            any_iso = False
            target_third = set(systems[target][2])
            target_words = {frozenset(w) for w in records[target]['anchor']}
            for order, row_image, full_image, third_image in physical_maps:
                tick()
                if third_image == target_third:
                    require({frozenset(full_image[p] for p in w) for w in records[source]['anchor']} == target_words,
                            'all thirteen physical words, preserving C-pair class roles')
                    any_iso = True
                    transports.append(dict(source=source, class_order=list(order), row_permutation=list(row_image),
                                           point_image=full_image, target=target))
            related.append(str(int(any_iso)))
        relations.append(''.join(related))
    transports.sort(key=lambda t: (t['source'], t['class_order'], t['row_permutation']))
    require(len(transports) == 56 * 144 and
            len({(t['source'], tuple(t['class_order']), tuple(t['row_permutation'])) for t in transports}) == 56 * 144,
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
                       all_transports=transports, fixed_special_points=[0, 4, 5],
                       ordered_parallel_class_roles_preserved=False, C_points_may_permute=True)
    common = hashlib.sha256(json.dumps(mathematics, sort_keys=True, separators=(',', ':')).encode()).hexdigest()
    result = dict(agent='six-code-3', role='researcher', status='COMPLETE_FULL_PAIRWISE_PHYSICAL_ANCHOR_ISOMORPHISMS',
                  mathematics=mathematics, common_math_sha256=common, states=STATES,
                  guard_states=500000, guard_seconds=20)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + '\n')
    print(json.dumps(dict(status=result['status'], orbit_sizes=[len(x) for x in orbits],
                          common_math_sha256=common, states=STATES), sort_keys=True))


if __name__ == '__main__':
    main()
