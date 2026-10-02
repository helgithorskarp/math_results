"""Independent literal transfer and all-centralizer-image classification audit.

The producer uses generator BFS; this checker parametrizes all actual commuting
point bijections and expands each representative under every one. It compares
complete sets of literal codes, not aggregate orbit sizes alone.
"""
import argparse
from collections import Counter
from copy import deepcopy
import hashlib
from itertools import combinations, permutations, product
import json
from pathlib import Path
import resource
import time

from physical import encoded, mask, need, points, transport_cover


def moved(words, p):
    bits = [2 ** v for v in p]
    return tuple(sorted(sum(bits[v] for v in ps) for ps in words))


def centralizer(g):
    fixed = [i for i in range(18) if g[i] == i]
    need(fixed == [0, 16, 17], 'wrong actual fixed points')
    cycles = []
    used = set(fixed)
    for start in range(18):
        if start in used:
            continue
        cycle = [start]
        while g[cycle[-1]] != start:
            cycle.append(g[cycle[-1]])
        need(len(cycle) == 5, 'bad physical cycle')
        cycles.append(cycle); used.update(cycle)
    actual = set()
    for order in permutations(range(3)):
        for offsets in product(range(5), repeat=3):
            for fixed_images in permutations(fixed):
                p = list(range(18))
                for source, target in zip(fixed, fixed_images):
                    p[source] = target
                for i, cycle in enumerate(cycles):
                    for k, v in enumerate(cycle):
                        p[v] = cycles[order[i]][(k + offsets[i]) % 5]
                need(sorted(p) == list(range(18)) and all(p[g[v]] == g[p[v]] for v in range(18)),
                     'false physical commuting point bijection')
                actual.add(tuple(p))
    need(len(actual) == 4500, 'incomplete or duplicated centralizer parametrization')
    return sorted(actual)


def class_cover(classification, orbits, universe, seed):
    records = classification['classes']
    need(classification['centralizer_order'] == 4500 and len(records) == len(orbits), 'wrong class inventory cardinality')
    covered = set()
    for index, (r, codes) in enumerate(zip(records, orbits)):
        need(r['class_index'] == index and r['labelled_size'] == len(codes), 'wrong actual orbit size/index')
        representative = tuple(r['representative_words'])
        need(representative == min(codes), 'noncanonical or incorrect representative')
        need(r['representative_degrees'] == [sum(p in points(w) for w in representative) for p in range(18)],
             'wrong representative degrees')
        need(r['seed_completion_indices'] == [i for i, c in enumerate(seed) if tuple(c['words']) in codes],
             'wrong normalized seed class membership')
        need(not codes & covered, 'two claimed classes share a physical code')
        covered.update(codes)
    need(covered == universe, 'centralizer representatives omit or invent physical codes')


def reject(test, value):
    try:
        test(value)
    except (ValueError, KeyError, IndexError):
        return
    raise ValueError('semantic class damage accepted')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--instance', type=Path, default=Path(__file__).parent / 'INSTANCE.json')
    parser.add_argument('--roots', type=Path, required=True)
    parser.add_argument('--cover', type=Path, required=True)
    parser.add_argument('--completions', type=Path, required=True)
    parser.add_argument('--saturation', type=Path, required=True)
    parser.add_argument('--work', type=Path, required=True)
    args = parser.parse_args()
    args.work.mkdir(parents=True, exist_ok=True)
    need(not (args.work / 'AUDIT.json').exists(), 'refuse completed saturation audit overwrite')
    begin = time.monotonic()
    fixture = json.loads(args.instance.read_text()); g = fixture['permutation']
    seed = json.loads(args.completions.read_text())
    cover = json.loads(args.cover.read_text())
    roots = json.loads(args.roots.read_text())
    root = sorted(w for w in fixture['classical68_words'] if w & 1)
    transport_cover(g, roots, cover, root)
    root_zero = set()
    for r in cover['point_transports']:
        p = r['seed_to_root_point_map']
        need(sorted(p) == list(range(18)) and p[0] == 0, 'wrong actual root transfer')
        for c in seed:
            root_zero.add(moved([points(w) for w in c['words']], p))
    need(len(root_zero) == 3200, 'not exactly32 literal completions per100 roots')
    expected = set(root_zero)
    for center in (16, 17):
        p = list(range(18)); p[0], p[center] = center, 0
        need(all(p[g[i]] == g[p[i]] for i in range(18)), 'center exchange does not commute')
        expected.update(moved([points(w) for w in c], p) for c in root_zero)
    inventory_raw = (args.saturation / 'ALL_CODES.json').read_bytes()
    records = json.loads(inventory_raw)
    need(records == list(map(list, sorted(expected))), 'full labelled inventory omitted, duplicated or invented a code')
    physical_words = {w for c in expected for w in c}
    cached_points = {w: points(w) for w in physical_words}
    cached_triples = {w: frozenset(combinations(sorted(cached_points[w]), 3)) for w in physical_words}
    degree_profiles = Counter(); saturation_hist = Counter()
    for code in expected:
        need(len(code) == len(set(code)) == 68, 'bad code size')
        occupied = set()
        for w in code:
            need(0 <= w < 2 ** 18 and len(points(w)) == 5 and not occupied & cached_triples[w],
                 'nonphysical code word or repeated physical triple')
            occupied.update(cached_triples[w])
        need(moved([cached_points[w] for w in code], g) == code, 'literal code violates C5 invariance')
        degrees = [0] * 18
        for w in code:
            for p in cached_points[w]:
                degrees[p] += 1
        degree_profiles[tuple(sorted(degrees))] += 1
        saturated = [p for p in (0, 16, 17) if degrees[p] == 20]
        need(saturated, 'false saturated-fixed-point inclusion')
        saturation_hist[len(saturated)] += 1
    classification_raw = (args.saturation / 'CLASSIFICATION.json').read_bytes()
    classification = json.loads(classification_raw)
    group = centralizer(g)
    need(all(tuple(p) in group for p in classification['point_generators']), 'false producer point generator')
    orbits = []
    for r in classification['classes']:
        ps = [points(w) for w in r['representative_words']]
        orbits.append({moved(ps, p) for p in group})
        need(time.monotonic() - begin < 60, 'INCOMPLETE initial60s literal centralizer audit guard')
    class_cover(classification, orbits, expected, seed)
    damages = []
    broken = deepcopy(classification); broken['classes'].pop()
    reject(lambda value: class_cover(value, orbits, expected, seed), broken); damages.append('omitted_class')
    broken = deepcopy(classification); broken['classes'][0]['labelled_size'] += 1
    reject(lambda value: class_cover(value, orbits, expected, seed), broken); damages.append('wrong_class_size')
    broken = deepcopy(classification); broken['classes'][0]['representative_words'][0] ^= 1
    reject(lambda value: class_cover(value, orbits, expected, seed), broken); damages.append('false_representative')
    broken = deepcopy(classification); broken['classes'][0]['seed_completion_indices'].append(32)
    reject(lambda value: class_cover(value, orbits, expected, seed), broken); damages.append('false_seed_class_membership')
    broken = deepcopy(classification); broken['classes'][0]['representative_degrees'][0] += 1
    reject(lambda value: class_cover(value, orbits, expected, seed), broken); damages.append('false_representative_degree')
    reject(lambda value: need(value == list(map(list, sorted(expected))), 'inventory mismatch'), records[:-1])
    damages.append('omitted_labelled_code')
    result = {'agent': 'six-code-2', 'role': 'researcher',
              'status': 'COMPLETE_INDEPENDENT_FULL_PHYSICAL_68_INVENTORY_AND_ALL_CENTRALIZER_IMAGE_AUDIT',
              'root_zero_codes': len(root_zero), 'all_labelled_codes': len(expected),
              'literal_codes_triple_and_invariance_checked': len(expected),
              'all_actual_commuting_permutations': len(group), 'centralizer_classes': len(orbits),
              'class_sizes': [len(c) for c in orbits],
              'every_actual_representative_point_image_tried': len(group) * len(orbits),
              'saturated_fixed_point_histogram': sorted(saturation_hist.items()),
              'degree_profile_histogram': sorted(degree_profiles.items()),
              'all_codes_sha256': hashlib.sha256(inventory_raw).hexdigest(),
              'classification_sha256': hashlib.sha256(classification_raw).hexdigest(),
              'semantic_damage_rejections': damages, 'solver_used_or_trusted': False,
              'initial_whole_guard_seconds': 60, 'seconds': time.monotonic() - begin,
              'peak_RSS_kib': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
              'scope': 'Whole saturated-fixed-point68 carrier, entry-level physical equality and complete centralizer image classes. No general point-isomorphism or no-saturated-fixed-point classification.'}
    (args.work / 'AUDIT.json').write_bytes(encoded(result))
    print(json.dumps(result, sort_keys=True), flush=True)


if __name__ == '__main__':
    main()
