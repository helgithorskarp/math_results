"""Complete point-map, inverse/generator composition checks."""
import argparse
import copy
import hashlib
import itertools
import json
import time
from collections import Counter
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


def check_transport(transport, records):
    tick()
    source, target = transport['source'], transport['target']
    require(type(source) is int and type(target) is int and 0 <= source < 56 and 0 <= target < 56,
            'actual transport endpoint domain')
    image = transport['point_image']
    require(len(image) == 18 and sorted(image) == list(range(18)) and image[0] == 0 and image[4:6] == [4, 5]
            and sorted(image[1:4]) == [1, 2, 3], 'entire point bijection, heavy/B labels fixed and all C labels carried')
    perm = transport['row_permutation']
    require(sorted(perm) == list(range(4)), 'row member bijection')
    order = transport['class_order']
    require(sorted(order) == list(range(3)), 'entire class-role permutation')
    for cls in range(3):
        left = {frozenset(image[p + 6] - 6 for p in t) for t in records[source]['classes'][order[cls]]}
        right = {frozenset(t) for t in records[target]['classes'][cls]}
        require(left == right, 'all twelve physical triples with every class role carried')
    for r in range(4):
        require({image[p + 6] - 6 for p in records[source]['classes'][order[0]][r]} ==
                set(records[target]['classes'][0][perm[r]]), 'declared row-member map is literal')
    require({frozenset(image[p] for p in w) for w in records[source]['anchor']} ==
            {frozenset(w) for w in records[target]['anchor']}, 'all thirteen anchor words transported')


def check_math(math, records):
    transports = math['all_transports']
    require(math['cases'] == 56 and len(transports) == 8064 and
            math['fixed_special_points'] == [0, 4, 5] and not math['ordered_parallel_class_roles_preserved']
            and math['C_points_may_permute'],
            'whole exact transport domain and retained labels')
    permutations = list(itertools.permutations(range(4)))
    orders = list(itertools.permutations(range(3)))
    require([(t['source'], tuple(t['class_order']), tuple(t['row_permutation'])) for t in transports] ==
            [(s, o, p) for s in range(56) for o in orders for p in permutations],
            'all56 systems, six class-role orders and24 row-member permutations')
    for t in transports:
        check_transport(t, records)
    table = {(t['source'], tuple(t['class_order']), tuple(t['row_permutation'])): t for t in transports}
    by_image = {(t['source'], tuple(t['point_image'])): t for t in transports}
    require(len(by_image) == 8064, 'all raw descriptors give distinct actual point maps per source')
    generators = [((0, 1, 2), (1, 0, 2, 3)), ((0, 1, 2), (0, 2, 1, 3)),
                  ((0, 1, 2), (0, 1, 3, 2)), ((1, 0, 2), (0, 1, 2, 3)),
                  ((0, 2, 1), (0, 1, 2, 3))]
    for first in transports:
        tick()
        inverse = [first['point_image'].index(p) for p in range(18)]
        back = by_image.get((first['target'], tuple(inverse)))
        require(back is not None and back['target'] == first['source'], 'every entire physical inverse and endpoint')
        for order, rows in generators:
            tick()
            second = table[first['target'], order, rows]
            composition = tuple(second['point_image'][p] for p in first['point_image'])
            direct = by_image.get((first['source'], composition))
            require(direct is not None and direct['target'] == second['target'],
                    'entire composed actual point map under each exact generator')
    relation = []
    for source in range(56):
        targets = {t['target'] for t in transports if t['source'] == source}
        relation.append(''.join(str(int(target in targets)) for target in range(56)))
    require(math['equivalence'] == relation, 'all3136 physical pairwise equivalence bits')
    unseen = set(range(56))
    groups = []
    while unseen:
        source = min(unseen)
        group = [target for target in range(56) if relation[source][target] == '1']
        require(set(group) <= unseen and all(relation[t] == relation[source] for t in group),
                'exact disjoint equivalence classes')
        groups.append(group)
        unseen -= set(group)
    require(math['orbits'] == groups, 'all whole physical orbits')
    return groups


def cycle_type(perm):
    remaining, lengths = set(range(4)), []
    while remaining:
        p, n = min(remaining), 0
        while p in remaining:
            remaining.remove(p)
            n += 1
            p = perm[p]
        lengths.append(n)
    return sorted(lengths)


def main():
    ap = argparse.ArgumentParser()
    for name in ['literal', 'dual', 'expected', 'output']:
        ap.add_argument('--' + name, type=Path, required=True)
    a = ap.parse_args()
    inp = json.loads((Path(__file__).parent / 'INPUT.json').read_text())
    expected = json.loads(a.expected.read_text())
    left, right = [json.loads(p.read_text()) for p in [a.literal, a.dual]]
    require(left['mathematics'] == right['mathematics'], 'all whole physical maps, orbits and3136 bits')
    math = left['mathematics']
    digest = hashlib.sha256(json.dumps(inp, sort_keys=True, separators=(',', ':')).encode()).hexdigest()
    common = hashlib.sha256(json.dumps(math, sort_keys=True, separators=(',', ':')).encode()).hexdigest()
    require(digest == expected['input_math_sha256'] == math['input_math_sha256'] and
            common == left['common_math_sha256'] == right['common_math_sha256'], 'entire input and common record hashes')
    records = inp['records']
    groups = check_math(math, records)
    summaries = []
    for group in groups:
        types = {tuple(cycle_type(records[i]['column_missing'])) for i in group}
        require(len(types) == 1, 'whole missing-matching cycle invariant within each exact orbit')
        representative = group[0]
        stabilizers = [t for t in math['all_transports'] if t['source'] == representative and t['target'] == representative]
        require(len(group) * len(stabilizers) == 144, 'actual total isomorphism/fiber count')
        summaries.append(dict(representative_index=representative, orbit_size=len(group),
                              stabilizer_size=len(stabilizers), column_matching_cycle_type=list(next(iter(types))),
                              representative=records[representative]))
    rejected = []
    for name, damage in [('move named heavy0', lambda t: t['point_image'].__setitem__(0, 6)),
                         ('false endpoint', lambda t: t.__setitem__('target', (t['target'] + 1) % 56)),
                         ('duplicate row image', lambda t: t['row_permutation'].__setitem__(0, t['row_permutation'][1]))]:
        t = copy.deepcopy(math['all_transports'][0])
        damage(t)
        try:
            check_transport(t, records)
        except (ValueError, IndexError, KeyError):
            rejected.append(name)
        else:
            raise ValueError('damaged transport accepted: ' + name)
    damaged = copy.deepcopy(math)
    damaged['all_transports'].pop()
    try:
        check_math(damaged, records)
    except ValueError:
        rejected.append('lost whole actual transport')
    else:
        raise ValueError('missing transport survived')
    result = dict(agent='six-code-3', role='researcher', status='COMPLETE_FULL_PHYSICAL_ANCHOR_CLASSIFICATION_CHECK',
                  cases=56, actual_transports=8064, complete_pairwise_bits=3136,
                  common_math_sha256=common, source_input_math_sha256=digest, whole_orbit_summaries=summaries,
                  semantic_rejections=rejected, states=STATES, guard_states=500000, guard_seconds=20,
                  ordinary_bridge_formalized=False, independent_person_review=False,
                  ambient_packing_automorphisms_assumed=False, light_hub_placements_completed=False)
    a.output.write_text(json.dumps(result, indent=2, sort_keys=True) + '\n')
    print(json.dumps(dict(status=result['status'], orbit_sizes=[len(g) for g in groups], states=STATES,
                          common_math_sha256=common), sort_keys=True))


if __name__ == '__main__':
    main()
