"""Independent physical audit of every D/y-fixed image and covered h6 target.

six-code-2, researcher. No producer imports. Points are named1..18.
This verifies the full finite image domain, never a full automorphism group.
"""
import argparse
from operations import check_operations
import hashlib
from itertools import combinations
import json
from pathlib import Path
import resource
import time


def need(ok, message):
    if not ok:
        raise ValueError(message)


def encoded(value):
    return (json.dumps(value, sort_keys=True, separators=(',', ':')) + '\n').encode()


def physical(w, length, weight):
    need(type(w) is int and 0 <= w < 1 << length and w.bit_count() == weight, 'physical word domain')
    return frozenset(v + 1 for v in range(length) if w >> v & 1)


def literal(points):
    return sum(1 << (v - 1) for v in points)


def main():
    parser = argparse.ArgumentParser()
    for key in ('parent', 'cover', 'witness', 'known-seeds', 'spec', 'work'):
        parser.add_argument('--' + key, type=Path, required=True)
    args = parser.parse_args()
    need(not args.work.exists(), 'fresh h6 physical point audit directory')
    args.work.mkdir(parents=True)
    begin, states = time.monotonic(), 0

    def guard():
        check_operations()
        need(time.monotonic() - begin < 60 and states <= 2000000,
             'INCOMPLETE original60s/two-million h6 physical point audit')

    parent_raw = args.parent.read_bytes()
    need(hashlib.sha256(parent_raw).hexdigest() == '32e66195e3252e2a50a2d6c55ed7d9af9a8693e7f7121276aeca1474f80c3758',
         'literal D fixture bytes')
    old = tuple(physical(w, 17, 5) for w in sorted(json.loads(parent_raw)['words']))
    old_set = set(old)
    triples = [t for w in old for t in combinations(sorted(w), 3)]
    need(len(old) == len(old_set) == 68 and len(triples) == len(set(triples)) == 680 and
         set(triples) == set(combinations(range(1, 18), 3)), 'physical whole Steiner partition')
    spec_raw = args.spec.read_bytes(); spec = json.loads(spec_raw)
    need(spec['literal_parent_sha256'] == hashlib.sha256(parent_raw).hexdigest() and
         not spec['full_group_order_assumed'] and not spec['minimal_orbit_classification_assumed'],
         'literal physical specification scope')
    q = physical(spec['noncontained_q'], 17, 4)
    extras = tuple(physical(w, 17, 5) for w in spec['extra_empty_parents'])
    need(len(extras) == len(set(extras)) == 2, 'physical specified extra pair')
    blockers = {b for b in old if len(b & q) >= 3}
    holes = blockers | set(extras)
    need(len(blockers) == 4 and len(holes) == 6 and holes <= old_set and not any(q <= b for b in old),
         'physical canonical h6 boundary')

    def check_map(p):
        need(len(p) == 18 and all(type(v) is int for v in p) and sorted(p) == list(range(18)) and p[17] == 17,
             'physical actual point bijection')
        def image(w):
            return frozenset(p[v - 1] + 1 for v in w)
        images = [image(w) for w in old]
        need(set(images) == old_set, 'physical whole D image')
        iq, ie, ih = image(q), tuple(sorted(literal(image(b)) for b in extras)), {image(b) for b in holes}
        need({b for b in old if len(b & iq) >= 3} | {physical(w, 17, 5) for w in ie} == ih and len(ih) == 6,
             'physical transported six-parent boundary')
        return (literal(iq), *ie), images, sorted(literal(b) for b in ih)

    raw = args.cover.read_bytes(); data = json.loads(raw)
    need(data['status'] == 'COMPLETE_POSITIVE_ACTUAL_POINT_IMAGES_OF_ONE_LITERAL_H6_PAIR' and
         data['parent_sha256'] == hashlib.sha256(parent_raw).hexdigest() and data['noncontained_q'] == literal(q) and
         data['spec_sha256'] == hashlib.sha256(spec_raw).hexdigest() and
         data['additional_empty_parents'] == sorted(literal(b) for b in extras) and
         data['hole_words'] == sorted(literal(b) for b in holes) and
         not data['full_automorphism_order_assumed'] and not data['minimal_orbits_assumed'], 'physical point cover scope')
    maps = data['point_maps']
    need(len(maps) == len({tuple(p) for p in maps}) == data['generated_map_count'] == spec['expected_generated_actual_maps'],
         'physical distinct point map domain')
    actual, images, trace = set(), [], hashlib.sha256()
    for i, p in enumerate(maps):
        target, old_images, hole_images = check_map(p)
        actual.add(target); images.append(target)
        trace.update(encoded([i, [sorted(w) for w in old_images], list(target), hole_images]))
        states += 1
        if i % 128 == 0:
            guard()

    def check_target(row):
        need(len(row) == 4 and all(type(v) is int for v in row) and 0 <= row[3] < len(maps),
             'physical target row domain')
        need(tuple(row[:3]) == images[row[3]], 'physical target image differs')
        return tuple(row[:3])

    def check_domain(rows):
        targets = [check_target(row) for row in rows]
        need(len(targets) == len(set(targets)), 'physical target duplicates')
        need(set(targets) == actual, 'whole physical target domain omitted')
        return targets

    targets = check_domain(data['targets']); states += len(targets)
    need(data['target_count'] == len(targets), 'physical target count differs')
    stable_pairs = sorted({target[1:] for target in actual if target[0] == literal(q)})
    need([list(pair) for pair in stable_pairs] == data['Q15_stabilizer_extra_pairs'], 'physical Q15 pair coverage differs')
    witness_raw = args.witness.read_bytes(); witness = json.loads(witness_raw)
    words = tuple(physical(w, 18, 5) for w in witness['words'])
    need(len(words) == len(set(words)) == 69 and all(len(u & v) <= 2 for u, v in combinations(words, 2)),
         'physical positive69 packing')
    occupied = [t for w in words for t in combinations(sorted(w), 3)]
    need(len(occupied) == len(set(occupied)) == 690, 'physical positive69 triples')
    represented, noncontained = set(), []
    for word in words:
        if 18 not in word:
            continue
        tail = word - {18}; owners = [b for b in old if tail <= b]
        if owners:
            need(len(owners) == 1 and owners[0] not in represented, 'positive represented-parent uniqueness')
            represented.add(owners[0])
        else:
            noncontained.append(tail)
    removed = old_set - set(words)
    caps = [w for w in words if 18 not in w and w not in old_set]
    need(noncontained == [q] and removed - represented == holes and len(caps) == 6 and len(removed) == len(represented) + 6,
         'physical positive69 boundary')
    seeds_raw = args.known_seeds.read_bytes(); seed_data = json.loads(seeds_raw)
    known_pairs = [tuple(pair) for pair in seed_data['distinct_h6_extra_pairs']]
    need(len(known_pairs) == len(set(known_pairs)) == 10, 'known ten literal pair domain')
    covered = sorted(set(known_pairs) & set(stable_pairs)); remaining = sorted(set(known_pairs) - set(stable_pairs))

    def rejects(label, callback, expected):
        try:
            callback()
        except ValueError as error:
            need(str(error) == expected, 'unintended point control rejection')
            return label
        raise ValueError('point damage accepted')

    bad = list(range(18)); bad[0] = bad[1]
    controls = [rejects('nonbijective-map', lambda: check_map(bad), 'physical actual point bijection')]
    bad = list(range(18)); bad[0], bad[1] = bad[1], bad[0]
    controls.append(rejects('bijective-wholeD-failure', lambda: check_map(bad), 'physical whole D image'))
    wrong = list(data['targets'][0]); wrong[1] = next(literal(b) for b in old if literal(b) not in wrong[1:3])
    controls.append(rejects('wrong-target-image', lambda: check_target(wrong), 'physical target image differs'))
    controls.append(rejects('omitted-valid-target', lambda: check_domain(data['targets'][:-1]), 'whole physical target domain omitted'))
    duplicated = data['targets'][:-1] + [data['targets'][0]]
    controls.append(rejects('duplicated-target', lambda: check_domain(duplicated), 'physical target duplicates'))
    guard()
    record = {'agent': 'six-code-2', 'role': 'researcher',
              'status': 'COMPLETE_PHYSICAL_ACTUAL_IMAGES_OF_ONE_LITERAL_H6_PAIR',
              'noncontained_q': literal(q), 'extra_empty_parents': sorted(literal(b) for b in extras), 'actual_maps': len(maps),
              'actual_targets': len(actual), 'distinct_Q_images': len({target[0] for target in actual}),
              'Q15_extra_pairs': stable_pairs, 'known_ten_pairs_covered': covered, 'known_ten_pairs_remaining': remaining,
              'whole_D_word_images_checked': len(maps) * 68, 'whole_H_parent_images_checked': len(maps) * 6,
              'whole_Q_images_checked': len(maps), 'map_target_state_units': states,
              'cover_sha256': hashlib.sha256(raw).hexdigest(), 'parent_sha256': hashlib.sha256(parent_raw).hexdigest(),
              'literal_full_image_trace_sha256': trace.hexdigest(),
              'actual_target_domain_sha256': hashlib.sha256(encoded(sorted(actual))).hexdigest(),
              'known_seed_inventory_sha256': hashlib.sha256(seeds_raw).hexdigest(),
              'positive69_witness_sha256': hashlib.sha256(witness_raw).hexdigest(),
              'positive69_parameters': {'s': 6, 'a': len(represented), 'R': len(removed), 't': 1, 'h': 6},
              'positive69_pairs': 2346, 'positive69_triples': 690, 'semantic_controls': controls,
              'ordinary_transport_bridge_formalized': False, 'independent_person_review': 'pending',
              'full_group_order_or_minimal_orbits_assumed': False, 'all_h6_pairs_or_global_endpoint_claim': False}
    rb = encoded(record); (args.work / 'EXACT_RESULT.json').write_bytes(rb)
    execution = {'seconds': time.monotonic() - begin, 'peak_RSS_kib': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
                 'original_seconds': 60, 'original_states': 2000000,
                 'exact_bytes': len(rb), 'exact_sha256': hashlib.sha256(rb).hexdigest()}
    (args.work / 'EXECUTION.json').write_bytes(encoded(execution))
    print(json.dumps(execution, sort_keys=True), flush=True)


if __name__ == '__main__':
    main()
