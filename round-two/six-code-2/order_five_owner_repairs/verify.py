"""Exact positive ownership/color certificate checker; no search is trusted.

Reconstruct every physical word and blocker carrier by point intersections.
Check the global radius-four field, regenerate every sparse radius-five
exception and validate its complete positive five-coloring. The old base
census is a separate stated dependency, with actual point maps checked here.
"""
import argparse
from collections import Counter, defaultdict
from itertools import combinations
import hashlib
import json
import math
from pathlib import Path
import resource
import time


def require(ok, message):
    if not ok:
        raise ValueError(message)


def encoded(value):
    return (json.dumps(value, sort_keys=True, separators=(',', ':')) + '\n').encode()


def proper_owner_coloring(words, colors, blockers, points, deleted):
    require(set(colors) == set(words), 'positive coloring has wrong vertex carrier')
    require(all(colors[w] in blockers[w] and colors[w] in deleted for w in words),
            'color is not a removed blocker')
    for a, b in combinations(words, 2):
        if len(points[a] & points[b]) <= 2:
            require(colors[a] != colors[b], 'compatible vertices receive the same color')


def semantic_controls(points):
    # These controls exercise the actual coloring criterion, not file hashes.
    a, b = next((a, b) for a, b in combinations(sorted(points), 2) if len(points[a] & points[b]) <= 2)
    tests = [('wrong_owner', [a], {a: 1}, {a: frozenset([0])}, frozenset([0])),
             ('compatible_collision', [a, b], {a: 0, b: 0},
              {a: frozenset([0]), b: frozenset([0])}, frozenset([0])),
             ('omitted_vertex', [a, b], {a: 0}, {a: frozenset([0]), b: frozenset([1])}, frozenset([0, 1])),
             ('unremoved_color', [a], {a: 0}, {a: frozenset([0])}, frozenset([1]))]
    rejected = []
    for name, words, colors, blockers, deleted in tests:
        try:
            proper_owner_coloring(words, colors, blockers, points, deleted)
        except ValueError:
            rejected.append(name)
        else:
            raise ValueError('semantic coloring damage accepted: ' + name)
    proper_owner_coloring([a, b], {a: 0, b: 1},
                          {a: frozenset([0]), b: frozenset([1])}, points, frozenset([0, 1]))
    return rejected


def main():
    parser = argparse.ArgumentParser()
    root = Path(__file__).resolve().parent
    parser.add_argument('--classification', type=Path, default=root / 'CLASSIFICATION.json')
    parser.add_argument('--point-maps', type=Path, default=root / 'POINT_MAPS.json')
    parser.add_argument('--four', type=Path, default=root / 'OWNERS_FOUR.json')
    parser.add_argument('--five', type=Path, default=root / 'COLORS_FIVE.json')
    parser.add_argument('--work', type=Path, required=True)
    args = parser.parse_args()
    require(not args.work.exists(), 'require a new certificate-verification directory')
    args.work.mkdir(parents=True)
    begin = time.monotonic()
    raw = args.classification.read_bytes()
    classes = json.loads(raw)['classes']
    four_raw = args.four.read_bytes()
    five_raw = args.five.read_bytes()
    four = json.loads(four_raw)
    five = json.loads(five_raw)
    require(len(classes) == 8 and [c['class_index'] for c in classes] == list(range(8)), 'wrong original base carrier')
    require(four['radius'] == 4 and five['radius'] == 5 and
            [c['class_index'] for c in four['cases']] == [0, 4, 5, 6, 7] and
            [c['class_index'] for c in five['cases']] == [0, 4, 5, 6, 7], 'wrong ownership certificate carriers')
    maps = json.loads(args.point_maps.read_bytes())
    require([r['target_class'] for r in maps] == [0, 1, 2, 3], 'incomplete positive point transports')
    for row in maps:
        p = row['point_map']
        require(sorted(p) == list(range(18)), 'point map is not bijective')
        image = {sum(1 << p[i] for i in range(18) if word & (1 << i))
                 for word in classes[0]['representative_words']}
        require(image == set(classes[row['target_class']]['representative_words']), 'false positive base transport')
    points = {sum(1 << p for p in ps): frozenset(ps) for ps in combinations(range(18), 5)}
    require(len(points) == 8568, 'incomplete physical word universe')
    g = [0, 8, 3, 11, 6, 14, 5, 13, 12, 4, 15, 7, 10, 2, 9, 1, 16, 17]
    for r in classes:
        base = r['representative_words']
        require(len(base) == len(set(base)) == 68 and all(w in points for w in base), 'invalid original representative')
        require(all(len(points[a] & points[b]) <= 2 for a, b in combinations(base, 2)), 'invalid original packing')
        require({sum(1 << g[i] for i in points[w]) for w in base} == set(base), 'original base is not g-invariant')
        require(any(sum(p in points[w] for w in base) == 20 for p in (0, 16, 17)),
                'original base has no saturated fixed point')
    cases = []
    for c4, c5 in zip(four['cases'], five['cases']):
        ci = c4['class_index']
        require(c5['class_index'] == ci, 'incorrect case correspondence')
        base = classes[ci]['representative_words']
        require(base == sorted(set(base)) and len(base) == 68 and all(w in points for w in base), 'invalid base words')
        require(all(len(points[a] & points[b]) <= 2 for a, b in combinations(base, 2)), 'base is not a packing')
        blockers = {w: frozenset(i for i, b in enumerate(base) if len(points[w] & points[b]) > 2)
                    for w in points}
        outside = set(points) - set(base)
        require(all(blockers[w] for w in outside), 'appendable outside word')
        eligible_four = {w for w in outside if len(blockers[w]) <= 4}
        rows4 = c4['owners']
        field = dict(rows4)
        require(len(rows4) == len(field) and set(field) == eligible_four, 'incomplete or invented radius-four field')
        require(all(field[w] in blockers[w] for w in field), 'four-field owner is not a blocker')
        field.update({w: i for i, w in enumerate(base)})
        groups = defaultdict(list)
        for w, owner in field.items():
            groups[owner].append(w)
        pairs_tested = four_cooccurring_pairs = 0
        collision_carriers = set()
        for group in groups.values():
            for a, b in combinations(group, 2):
                pairs_tested += 1
                union = blockers[a] | blockers[b]
                compatible = len(points[a] & points[b]) <= 2
                if len(union) <= 4:
                    four_cooccurring_pairs += 1
                    require(not compatible, 'radius-four ownership collision')
                if len(union) <= 5 and compatible:
                    require(len(union) == 5, 'invalid collision carrier')
                    collision_carriers.add(union)
        eligible_five = {w for w in outside if len(blockers[w]) == 5}
        rows5 = c5['five_blocker_word_owners']
        new_owners = dict(rows5)
        require(len(rows5) == len(new_owners) and set(new_owners) == eligible_five,
                'incomplete or invented five-blocker word assignments')
        require(all(new_owners[w] in blockers[w] for w in new_owners), 'new-word owner is not a blocker')
        full_carriers = {blockers[w] for w in eligible_five}
        critical = full_carriers | collision_carriers
        recolor = {}
        for deleted_indices, word, owner in c5['conditional_recolorings']:
            deleted = frozenset(deleted_indices)
            require(len(deleted_indices) == len(deleted) == 5 and all(0 <= i < 68 for i in deleted),
                    'invalid conditional deletion carrier')
            require(deleted not in recolor, 'duplicate conditional recoloring')
            require(word in eligible_four and owner in blockers[word] and owner != field[word],
                    'invalid or ineffective recoloring')
            recolor[deleted] = (word, owner)
        require(set(recolor) == collision_carriers, 'conditional recolorings omit or invent collision carriers')
        buckets = defaultdict(list)
        for w, s in blockers.items():
            if len(s) <= 5:
                buckets[s].append(w)
        digest = hashlib.sha256()
        hist = Counter()
        local_pair_tests = 0
        for deleted in sorted(critical, key=lambda s: sum(1 << i for i in s)):
            require(time.monotonic() - begin < 60, 'INCOMPLETE initial 60-second exact certificate guard')
            ds = sorted(deleted)
            words = sorted(w for n in range(6) for subset in combinations(ds, n)
                           for w in buckets.get(frozenset(subset), ()))
            require(all(base[i] in words for i in deleted), 'missing deleted old word')
            colors = {w: field[w] if len(blockers[w]) <= 4 else new_owners[w] for w in words}
            if deleted in recolor:
                w, owner = recolor[deleted]
                require(w in colors, 'conditional recolored vertex outside complete domain')
                colors[w] = owner
            proper_owner_coloring(words, colors, blockers, points, deleted)
            require(all(colors[base[i]] == i for i in deleted), 'deleted-old-word color changed')
            local_pair_tests += math.comb(len(words), 2)
            hist[len(words)] += 1
            digest.update(encoded([ds, words, 5]))
        case = {'class_index': ci, 'every_physical_word': len(points),
                'four_field_outside_words': len(eligible_four), 'five_blocker_words': len(eligible_five),
                'five_blocker_carriers': len(full_carriers), 'same_owner_collision_carriers': len(collision_carriers),
                'critical_anchors': len(critical), 'all_five_deletion_anchors': math.comb(68, 5),
                'noncritical_anchors_colored_by_four_field': math.comb(68, 5) - len(critical),
                'four_field_same_owner_pair_tests': pairs_tested, 'four_field_cooccurring_pair_tests': four_cooccurring_pairs,
                'local_coloring_pair_tests': local_pair_tests,
                'critical_domain_size_histogram': sorted(hist.items()),
                'ordered_critical_anchor_domain_maximum_sha256': digest.hexdigest(),
                'sharp_maximum_packing': 68}
        cases.append(case)
    controls = semantic_controls(points)
    exact = {'agent': 'six-code-2', 'role': 'researcher', 'status': 'COMPLETE_POSITIVE_OWNERSHIP_AND_SPARSE_FIVE_COLOR_CERTIFICATE_AUDIT',
             'input_classification_sha256': hashlib.sha256(raw).hexdigest(),
             'input_four_certificate_sha256': hashlib.sha256(four_raw).hexdigest(),
             'input_five_certificate_sha256': hashlib.sha256(five_raw).hexdigest(),
             'point_transports_checked': 4, 'five_type_five_deletion_anchors': 5 * math.comb(68, 5),
             'original_eight_representatives_literally_checked': 8,
             'original_eight_base_five_deletion_anchors_covered_by_actual_maps': 8 * math.comb(68, 5),
             'all_critical_anchors_literally_colored': sum(c['critical_anchors'] for c in cases),
             'four_field_same_owner_pair_tests': sum(c['four_field_same_owner_pair_tests'] for c in cases),
             'four_field_cooccurring_pair_tests': sum(c['four_field_cooccurring_pair_tests'] for c in cases),
             'local_coloring_pair_tests': sum(c['local_coloring_pair_tests'] for c in cases),
             'cases': cases, 'semantic_damage_rejections': controls,
             'sharp_maximum_packing_retaining_at_least_63_base_words': 68}
    encoded_exact = encoded(exact)
    expected = root / 'EXPECTED.json'
    if expected.exists():
        require(json.loads(expected.read_bytes()) == json.loads(encoded_exact), 'whole exact record differs')
    (args.work / 'EXACT_RESULT.json').write_bytes(encoded_exact)
    execution = {'agent': 'six-code-2', 'role': 'researcher', 'status': exact['status'],
                 'seconds': time.monotonic() - begin, 'peak_RSS_kib': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
                 'initial_whole_guard_seconds': 60, 'exact_result_bytes': len(encoded_exact),
                 'exact_result_sha256': hashlib.sha256(encoded_exact).hexdigest()}
    (args.work / 'EXECUTION.json').write_bytes(encoded(execution))
    print(json.dumps(execution, sort_keys=True))


if __name__ == '__main__':
    main()
