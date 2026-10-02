"""Check positive point maps and separating invariants by physical triples.

The original eight-representative coverage theorem is a stated dependency.
This checker trusts no negative permutation-search result.
"""
import argparse
from copy import deepcopy
from itertools import combinations
import hashlib
import json
from pathlib import Path
import resource
import time


def require(ok, message):
    if not ok:
        raise ValueError(message)


def encoded(value):
    return (json.dumps(value, sort_keys=True, separators=(',', ':')) + '\n').encode()


def certify(classes, g, certificate):
    require(len(classes) == 8 and [r['class_index'] for r in classes] == list(range(8)), 'wrong eight-base carrier')
    require(sorted(g) == list(range(18)), 'invalid point action')
    physical = {sum(1 << p for p in ps): frozenset(combinations(ps, 3))
                for ps in combinations(range(18), 5)}
    require(len(physical) == 8568, 'wrong physical universe')
    invariants = []
    for r in classes:
        base = r['representative_words']
        require(base == sorted(set(base)) and len(base) == 68 and all(w in physical for w in base), 'invalid base')
        owners = {}
        for i, w in enumerate(base):
            for triple in physical[w]:
                require(triple not in owners, 'base reuses a triple')
                owners[triple] = i
        moved = {sum(1 << g[p] for p in range(18) if w & (1 << p)) for w in base}
        require(moved == set(base), 'base lacks the prescribed invariance')
        require(any(sum(bool(w & (1 << p)) for w in base) == 20 for p in range(18) if g[p] == p),
                'base lacks a saturated fixed point')
        hist = [0] * 69
        for w, triples in physical.items():
            if w not in set(base):
                hist[len({owners[t] for t in triples if t in owners})] += 1
        require(sum(hist) == 8500, 'incomplete outside physical-word carrier')
        invariants.append({'class_index': r['class_index'], 'exactly_one_blocker_outside_words': hist[1],
                           'full_blocker_size_histogram': [[i, n] for i, n in enumerate(hist) if n]})
    require(invariants == certificate['invariants'], 'incorrect physical separating invariants')
    groups = certificate['point_isomorphism_groups_within_given_family']
    require(groups == [[0, 1, 2, 3], [4], [5], [6], [7]], 'incorrect proposed type partition')
    require(len({invariants[group[0]]['exactly_one_blocker_outside_words'] for group in groups}) == 5,
            'five proposed types are not separated')
    for group in groups:
        require(len({invariants[i]['exactly_one_blocker_outside_words'] for i in group}) == 1,
                'merged classes have different invariants')
    maps = certificate['point_transports_from_class_zero']
    require([r['target_class'] for r in maps] == [0, 1, 2, 3], 'missing positive type transports')
    for row in maps:
        p = row['point_map']
        require(sorted(p) == list(range(18)), 'point map is not a bijection')
        target = {sum(1 << p[i] for i in range(18) if w & (1 << i))
                  for w in classes[0]['representative_words']}
        require(target == set(classes[row['target_class']]['representative_words']), 'point map fails physical equality')
    sizes = [sum(classes[i]['labelled_size'] for i in group) for group in groups]
    require(sizes == certificate['labelled_group_sizes_within_given_family'], 'wrong induced labelled type sizes')
    return {'point_isomorphism_types_within_given_family': 5, 'groups': groups,
            'labelled_group_sizes_within_given_family': sizes,
            'one_blocker_invariant_for_each_type': [invariants[group[0]]['exactly_one_blocker_outside_words'] for group in groups],
            'exact_physical_word_checks': 8 * 8568, 'exact_positive_point_maps': 4}


def main():
    parser = argparse.ArgumentParser()
    root = Path(__file__).parent
    parser.add_argument('--classification', type=Path, default=root / 'CLASSIFICATION.json')
    parser.add_argument('--instance', type=Path, default=root / 'INSTANCE.json')
    parser.add_argument('--certificate', type=Path, default=root / 'TYPE_CERTIFICATE.json')
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    require(not args.output.exists(), 'require a new audit output')
    begin = time.monotonic()
    raw = args.classification.read_bytes()
    classes = json.loads(raw)['classes']
    g = json.loads(args.instance.read_bytes())['permutation']
    certificate = json.loads(args.certificate.read_bytes())
    require(hashlib.sha256(raw).hexdigest() == certificate['input_classification_sha256'], 'fixture provenance mismatch')
    result = certify(classes, g, certificate)
    damages = []
    for name in ('false_point_map', 'missing_point_map', 'false_invariant', 'false_type_partition', 'false_labelled_size', 'invalid_base_word'):
        c = deepcopy(certificate)
        bs = deepcopy(classes)
        if name == 'false_point_map':
            c['point_transports_from_class_zero'][1]['point_map'][1] = 0
        elif name == 'missing_point_map':
            c['point_transports_from_class_zero'].pop()
        elif name == 'false_invariant':
            c['invariants'][5]['exactly_one_blocker_outside_words'] += 1
        elif name == 'false_type_partition':
            c['point_isomorphism_groups_within_given_family'][-2].append(7)
        elif name == 'false_labelled_size':
            c['labelled_group_sizes_within_given_family'][0] += 1
        elif name == 'invalid_base_word':
            bs[0]['representative_words'][0] = 0
        try:
            certify(bs, g, c)
        except (ValueError, IndexError, KeyError):
            damages.append(name)
        else:
            raise ValueError('accepted semantic damage: ' + name)
    require(time.monotonic() - begin < 60, 'INCOMPLETE initial 60-second type audit guard')
    result.update({'agent': 'six-code-2', 'role': 'researcher',
                   'status': 'COMPLETE_INDEPENDENT_PHYSICAL_TYPE_AUDIT',
                   'input_classification_sha256': hashlib.sha256(raw).hexdigest(),
                   'semantic_damage_rejections': damages, 'seconds': time.monotonic() - begin,
                   'peak_RSS_kib': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
                   'initial_whole_guard_seconds': 60})
    args.output.write_bytes(encoded(result))
    print(json.dumps(result, sort_keys=True))


if __name__ == '__main__':
    main()
