"""Positive classification of all C5 size68 codes with a saturated fixed point.

The complete seed census and actual root transports produce the full labelled
inventory. Actual commuting point generators give centralizer orbits. Generated
full inventories stay in the requested scratch directory, outside publication.
"""
import argparse
from collections import Counter, deque
import hashlib
from itertools import combinations
import json
from pathlib import Path
import resource
import time

from cover import encoded, move, need


def point_generators(g):
    remaining = {p for p in range(18) if g[p] != p}
    cycles = []
    while remaining:
        c = [min(remaining)]
        while g[c[-1]] != c[0]:
            c.append(g[c[-1]])
        need(len(c) == 5, 'wrong moving cycle')
        cycles.append(c)
        remaining.difference_update(c)
    generators = []
    for cycle in cycles:
        p = list(range(18))
        for i, v in enumerate(cycle):
            p[v] = cycle[(i + 1) % 5]
        generators.append(tuple(p))
    for a, b in ((0, 1), (1, 2)):
        p = list(range(18))
        for x, y in zip(cycles[a], cycles[b]):
            p[x], p[y] = y, x
        generators.append(tuple(p))
    for a, b in ((0, 16), (16, 17)):
        p = list(range(18)); p[a], p[b] = b, a
        generators.append(tuple(p))
    for p in generators:
        need(sorted(p) == list(range(18)) and all(p[g[i]] == g[p[i]] for i in range(18)), 'false commuting generator')
    group = {tuple(range(18))}
    queue = deque(group)
    while queue:
        p = queue.popleft()
        for q in generators:
            new = tuple(q[p[i]] for i in range(18))
            if new not in group:
                group.add(new); queue.append(new)
    need(len(group) == 4500, 'generators do not cover the whole centralizer')
    return generators


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--instance', type=Path, default=Path(__file__).parent / 'INSTANCE.json')
    parser.add_argument('--cover', type=Path, required=True)
    parser.add_argument('--completions', type=Path, required=True)
    parser.add_argument('--work', type=Path, required=True)
    args = parser.parse_args()
    args.work.mkdir(parents=True, exist_ok=True)
    need(not (args.work / 'RESULT.json').exists(), 'refuse completed saturation inventory overwrite')
    begin = time.monotonic()
    g = json.loads(args.instance.read_text())['permutation']
    seed = json.loads(args.completions.read_text())
    cover = json.loads(args.cover.read_text())
    need(len(seed) == 32 and len(cover['point_transports']) == 100, 'incomplete supplied census/cover')
    root_zero = set()
    for r in cover['point_transports']:
        p = r['seed_to_root_point_map']
        for code in seed:
            root_zero.add(tuple(sorted(move(w, p) for w in code['words'])))
    need(len(root_zero) == 3200, 'literal root-zero code count differs')
    all_codes = set(root_zero)
    for center in (16, 17):
        p = list(range(18)); p[0], p[center] = center, 0
        all_codes.update(tuple(sorted(move(w, p) for w in words)) for words in root_zero)
    ordered = sorted(all_codes)
    lookup = {words: i for i, words in enumerate(ordered)}
    generators = point_generators(g)
    universe = sorted({w for words in ordered for w in words})
    moves = [{w: move(w, p) for w in universe} for p in generators]
    visited = set()
    classes = []
    for index, representative in enumerate(ordered):
        if index in visited:
            continue
        reached = {index}; queue = deque((index,))
        while queue:
            i = queue.popleft()
            for mapping in moves:
                image = tuple(sorted(mapping[w] for w in ordered[i]))
                need(image in lookup, 'actual centralizer image absent from census')
                j = lookup[image]
                if j not in reached:
                    reached.add(j); queue.append(j)
        need(not reached & visited, 'overlapping centralizer classes')
        visited.update(reached)
        degrees = [sum(w >> p & 1 for w in representative) for p in range(18)]
        classes.append({'class_index': len(classes), 'labelled_size': len(reached),
                        'representative_words': representative, 'representative_degrees': degrees,
                        'seed_completion_indices': [i for i, c in enumerate(seed) if lookup[tuple(c['words'])] in reached]})
    need(visited == set(range(len(ordered))), 'incomplete positive centralizer orbit cover')
    saturated = Counter(sum(sum(w >> p & 1 for w in words) == 20 for p in (0, 16, 17)) for words in ordered)
    profiles = Counter(tuple(sorted(sum(w >> p & 1 for w in words) for p in range(18))) for words in ordered)
    representatives_raw = encoded({'point_generators': generators, 'centralizer_order': 4500, 'classes': classes})
    inventory_raw = encoded(ordered)
    (args.work / 'ALL_CODES.json').write_bytes(inventory_raw)
    (args.work / 'CLASSIFICATION.json').write_bytes(representatives_raw)
    result = {'agent': 'six-code-2', 'role': 'researcher', 'status': 'COMPLETE_GENERATED_SATURATED_FIXED_POINT_LABELLED_68_CODE_CLASSIFICATION',
              'root_zero_labelled_codes': len(root_zero), 'all_labelled_codes': len(ordered),
              'centralizer_order': 4500, 'centralizer_classes': len(classes),
              'class_sizes': [r['labelled_size'] for r in classes],
              'saturated_fixed_point_histogram': sorted(saturated.items()),
              'degree_profile_histogram': sorted(profiles.items()),
              'all_codes_bytes': len(inventory_raw), 'all_codes_sha256': hashlib.sha256(inventory_raw).hexdigest(),
              'classification_sha256': hashlib.sha256(representatives_raw).hexdigest(),
              'seconds': time.monotonic() - begin, 'peak_RSS_kib': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
              'scope': 'Every literal C5 size68 packing with at least one saturated fixed point. Classes are under the centralizer of this specified action; no arbitrary point-isomorphism or unsaturated-fixed-point classification.'}
    (args.work / 'RESULT.json').write_bytes(encoded(result))
    print(json.dumps(result, sort_keys=True), flush=True)


if __name__ == '__main__':
    main()
