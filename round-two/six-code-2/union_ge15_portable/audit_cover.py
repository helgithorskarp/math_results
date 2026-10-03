"""Independent physical all-quartet/actual-map audit. six-code-2, researcher.

Imports no cover producer. Fresh literal subsets select the entire domain;
every actual map is checked against all68 D words, and every supplied
target is checked as the actual four-parent image. State units preserve
the prior physical audit: one per quartet, map and covered target.
"""
import argparse
from collections import Counter
import hashlib
from itertools import combinations
import json
from pathlib import Path
import resource
import time
from physical_helpers import encoded, operations_guard, point_set, require


def actual_action(permutation, blocks):
    require(len(permutation) == 18 and all(type(v) is int for v in permutation) and
            sorted(permutation) == list(range(18)) and permutation[17] == 17,
            'actual y-fixed point bijection')
    images = tuple(frozenset(permutation[v] for v in block) for block in blocks)
    require(set(images) == set(blocks), 'actual whole physicalD image')
    lookup = {block: i for i, block in enumerate(blocks)}
    return tuple(lookup[block] for block in images)


def check_target(canonical, target, action):
    require(len(target) == 4 and all(type(v) is int for v in target) and
            0 <= target[0] < target[1] < target[2] < target[3] < 68,
            'physical distinct quartet domain')
    require(tuple(sorted(action[v] for v in canonical)) == target,
            'actual physical quartet image differs')


def mark(seen, target):
    require(target not in seen, 'duplicate physical target')
    seen.add(target)


def complete(actual, expected):
    require(actual == expected, 'entire physical union-at-least15 domain differs')


def reject(label, callback, reason):
    try:
        callback()
    except ValueError as exc:
        require(str(exc) == reason, 'unexpected physical control rejection')
        return {'control': label, 'reason': reason}
    raise ValueError('physical semantic damage accepted: ' + label)


def main():
    parser = argparse.ArgumentParser()
    for name in ('parent', 'spec', 'cover', 'work'):
        parser.add_argument('--' + name, type=Path, required=True)
    args = parser.parse_args()
    require(not args.work.exists(), 'new physical domain audit directory required')
    args.work.mkdir(parents=True)
    start, states = time.monotonic(), 0

    def guard():
        operations_guard()
        require(time.monotonic() - start < 60 and states <= 2_000_000,
                'INCOMPLETE original60s/two-million physical domain states')

    raw = args.parent.read_bytes()
    spec = json.loads(args.spec.read_bytes())
    require(hashlib.sha256(raw).hexdigest() == spec['literal_parent_sha256'], 'exact physicalD bytes')
    words = tuple(sorted(json.loads(raw)['words']))
    blocks = tuple(point_set(w, 5) for w in words)
    triples = [triple for block in blocks for triple in combinations(sorted(block), 3)]
    require(len(blocks) == len(set(blocks)) == 68 and
            len(triples) == len(set(triples)) == 680 and
            set(triples) == set(combinations(range(17), 3)), 'whole physical Steiner partition')
    physical, counts, digest = set(), Counter(), hashlib.sha256()
    for target in combinations(range(68), 4):
        states += 1
        a, b, c, d = target
        union_size = len(blocks[a] | blocks[b] | blocks[c] | blocks[d])
        if union_size >= 15:
            physical.add(target)
            counts[str(union_size)] += 1
            digest.update(encoded([list(target), union_size]))
        if states % 4096 == 0:
            guard()
    require(states == spec['whole_parent_quartets'] and len(physical) == spec['physical_targets'] and
            dict(counts) == spec['physical_target_union_counts'], 'whole fresh physical domain counts')
    cover_raw = args.cover.read_bytes()
    cover = json.loads(cover_raw)
    require(cover['status'] == 'COMPLETE_POSITIVE_ACTUAL_POINT_MAPS_NO_PACKING_ABSENCE' and
            cover['parent_sha256'] == hashlib.sha256(raw).hexdigest() and
            cover['parent_words'] == list(words), 'whole positive cover scope')
    maps = cover['point_maps']
    require(len(maps) == len({tuple(p) for p in maps}) == spec['expected_generated_actual_maps'],
            'distinct actual map packet domain')
    actions = []
    for permutation in maps:
        states += 1
        actions.append(actual_action(permutation, blocks))
        if states % 256 == 0:
            guard()
    require([c['component'] for c in cover['cases']] == [c['component'] for c in spec['cases']],
            'whole representative packet domain')
    covered, bindings, first_target = set(), [], None
    lookup = {word: i for i, word in enumerate(words)}
    for packet, expected in zip(cover['cases'], spec['cases']):
        require(packet['hole_words'] == expected['hole_words'] and
                packet['union_points'] == expected['union_points'] and
                len(packet['targets']) == expected['targets'], 'literal representative scope')
        canonical = tuple(lookup[w] for w in expected['hole_words'])
        require(len(set(canonical)) == 4 and
                len(frozenset().union(*(blocks[i] for i in canonical))) == expected['union_points'],
                'physical representative union')
        case_digest, previous = hashlib.sha256(), None
        for record in packet['targets']:
            states += 1
            require(len(record) == 5 and type(record[4]) is int and 0 <= record[4] < len(maps),
                    'actual target-map record domain')
            target, map_id = tuple(record[:4]), record[4]
            require(previous is None or previous < target, 'strict whole target order')
            previous = target
            check_target(canonical, target, actions[map_id])
            mark(covered, target)
            require(target in physical, 'actual target outside fresh physical domain')
            case_digest.update(encoded(record))
            if first_target is None:
                first_target = (canonical, target, actions[map_id])
            if states % 1024 == 0:
                guard()
        bindings.append({'component': expected['component'], 'hole_words': expected['hole_words'],
                         'union_points': expected['union_points'], 'targets': len(packet['targets']),
                         'all_actual_target_maps_sha256': case_digest.hexdigest()})
    complete(covered, physical)
    require(cover['target_count'] == len(covered) and cover['generated_map_count'] == len(maps),
            'whole cover header counts')
    canonical, target, action = first_target
    nonbijective = list(range(18)); nonbijective[0] = nonbijective[1]
    bad_d = list(range(18)); bad_d[0], bad_d[1] = bad_d[1], bad_d[0]
    require({frozenset(bad_d[v] for v in block) for block in blocks} != set(blocks),
            'wholeD control is genuinely damaged')
    other_target = next(t for t in sorted(physical) if t != target)
    controls = [
        reject('nonbijective-point-map', lambda: actual_action(nonbijective, blocks),
               'actual y-fixed point bijection'),
        reject('bijective-map-failing-wholeD', lambda: actual_action(bad_d, blocks),
               'actual whole physicalD image'),
        reject('wrong-physical-target-image', lambda: check_target(canonical, other_target, action),
               'actual physical quartet image differs'),
        reject('duplicated-actual-target', lambda: mark(set(covered), target), 'duplicate physical target'),
        reject('omitted-valid-domain-target', lambda: complete(covered - {target}, physical),
               'entire physical union-at-least15 domain differs')]
    guard()
    result = {'agent': 'six-code-2', 'role': 'researcher',
              'status': 'COMPLETE_ALL72165_PHYSICAL_UNION_GE15_ACTUAL_POINT_COVER',
              'parent_sha256': hashlib.sha256(raw).hexdigest(),
              'cover_sha256': hashlib.sha256(cover_raw).hexdigest(),
              'whole_physical_quartets': 814385, 'physical_D_words': 68, 'physical_D_triples': 680,
              'selected_physical_targets': len(physical), 'union_counts': dict(counts),
              'fresh_domain_sha256': digest.hexdigest(), 'actual_point_maps': len(maps),
              'whole_D_word_images': 68 * len(maps), 'physical_parent_images': 4 * len(covered),
              'cases': bindings, 'proof_states': states, 'semantic_controls': controls,
              'full_automorphism_order_assumed': False, 'minimal_orbits_assumed': False,
              'formalized': False, 'all_algorithms_same_author': True,
              'independent_person_review': 'pending',
              'scope': 'Coverage and transport only; cap certificates and ordinary restriction/gluing supply bounds.'}
    b = encoded(result)
    (args.work / 'EXACT_RESULT.json').write_bytes(b)
    execution = {'seconds': time.monotonic() - start,
                 'peak_RSS_kib': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
                 'exact_result_sha256': hashlib.sha256(b).hexdigest(), 'exact_result_bytes': len(b),
                 'initial_seconds': 60, 'initial_states': 2000000}
    (args.work / 'EXECUTION.json').write_bytes(encoded(execution))
    print(json.dumps(execution, sort_keys=True))


if __name__ == '__main__':
    main()
