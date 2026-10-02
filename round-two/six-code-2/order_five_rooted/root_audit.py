"""Independent physical-pair join census of every C5 rooted20 star.

No producer import. Every physical four-subset orbit is regenerated as
frozensets. Two disjoint compatible pair blocks join to enumerate four
rows exactly once, without the producer's recursive graph clique walk.
"""
import argparse
from collections import Counter
from copy import deepcopy
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


def points(word):
    return frozenset(p for p in range(18) if word >> p & 1)


def mask(ps):
    return sum(2 ** p for p in ps)


def orbit(ps, g):
    result = {ps}
    next_set = frozenset(g[p] for p in ps)
    while next_set != ps:
        need(next_set not in result, 'permutation orbit did not close')
        result.add(next_set)
        next_set = frozenset(g[p] for p in next_set)
    return frozenset(result)


def star(words):
    need(len(words) == len(set(words)) == 20, 'root star cardinality mismatch')
    pair_set = set()
    for w in words:
        ps = points(w)
        need(len(ps) == 5 and 0 in ps and 0 <= w < 2 ** 18, 'nonphysical root word')
        for pair in combinations(sorted(ps - {0}), 2):
            need(pair not in pair_set, 'repeated rooted physical pair')
            pair_set.add(pair)
    need(len(pair_set) == 120, 'wrong root pair coverage')


def expected_orbits(g):
    physical_pairs = tuple(combinations(range(1, 18), 2))
    pair_index = {frozenset(ps): i for i, ps in enumerate(physical_pairs)}
    pair_orbits = sorted(tuple(sorted(mask(ps) for ps in ts))
                         for ts in {orbit(frozenset(ps), g) for ps in physical_pairs})
    resource_index = {w: i for i, ws in enumerate(pair_orbits) for w in ws}
    actual = {orbit(frozenset(ps), g) for ps in combinations(range(1, 18), 4)}
    need(len(actual) == 476 and all(len(ws) == 5 for ws in actual), 'actual four-orbit universe mismatch')
    expected, physical_bitsets = [], []
    for ws in sorted(actual, key=lambda ws: tuple(sorted(mask(ps) for ps in ws))):
        if any(len(a & b) >= 2 for a, b in combinations(ws, 2)):
            continue
        covered = {frozenset(ps) for w in ws for ps in combinations(sorted(w), 2)}
        need(len(covered) == 30, 'eligible orbit repeats physical pair')
        expected.append({'four_subsets': sorted(mask(w) for w in ws),
                         'pair_orbit_resources': sorted({resource_index[mask(ps)] for ps in covered})})
        physical_bitsets.append(sum(2 ** pair_index[ps] for ps in covered))
    return {'pair_orbits': list(map(list, pair_orbits)), 'admissible_rows': expected}, tuple(physical_bitsets)


def inventory(roots, actual):
    keys = [tuple(r['words']) for r in roots]
    need(len(keys) == len(set(keys)) and set(keys) == set(actual), 'missing, duplicate or invented actual rooted star')
    for r in roots:
        star(r['words'])


def reject(test, value):
    try:
        test(value)
    except (ValueError, KeyError, IndexError):
        return True
    raise ValueError('semantic damage accepted')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--model', type=Path, required=True)
    parser.add_argument('--production', type=Path, required=True)
    parser.add_argument('--work', type=Path, required=True)
    args = parser.parse_args()
    args.work.mkdir(parents=True, exist_ok=True)
    need(not (args.work / 'AUDIT.json').exists(), 'refuse completed audit overwrite')
    begin = time.monotonic()
    raw = args.model.read_bytes()
    model = json.loads(raw)
    g = tuple(model['permutation'])
    need(sorted(g) == list(range(18)) and g[0] == 0, 'bad fixed-root permutation')
    expected, occupied = expected_orbits(g)
    actual_orbits = json.loads((args.production / 'ROOT_ORBITS.json').read_text())
    need(actual_orbits == expected, 'every literal row and physical pair resource must match')
    pairblocks = [(a, b, occupied[a] | occupied[b]) for a, b in combinations(range(len(occupied)), 2)
                  if not occupied[a] & occupied[b]]
    positive = []
    trials = 0
    for (a, b, left), (c, d, right) in combinations(pairblocks, 2):
        trials += 1
        if trials % 8192 == 0 and time.monotonic() - begin > 60:
            raise TimeoutError('INCOMPLETE initial60s whole independent pair-join guard')
        if b < c and not left & right:
            words = tuple(sorted(w | 1 for i in (a, b, c, d) for w in expected['admissible_rows'][i]['four_subsets']))
            star(words)
            positive.append(words)
    need(positive and len(positive) == len(set(positive)), 'pair join created duplicate root')
    roots = json.loads((args.production / 'ROOTS.json').read_text())
    inventory(roots, positive)
    root_sets = sorted(positive)
    damage_names = []
    broken = deepcopy(roots); broken.pop()
    reject(lambda value: inventory(value, positive), broken); damage_names.append('omitted_root')
    broken = deepcopy(roots); broken[1] = deepcopy(broken[0])
    reject(lambda value: inventory(value, positive), broken); damage_names.append('duplicate_root')
    broken = deepcopy(actual_orbits); broken['admissible_rows'].pop()
    reject(lambda value: need(value == expected, 'row mismatch'), broken); damage_names.append('omitted_physical_row')
    broken = deepcopy(actual_orbits); broken['admissible_rows'][0]['pair_orbit_resources'].pop()
    reject(lambda value: need(value == expected, 'pair mismatch'), broken); damage_names.append('omitted_pair_resource')
    reject(star, list(positive[0][:-1]) + [positive[0][0]]); damage_names.append('duplicate_star_word')
    record_raw = encoded(root_sets)
    (args.work / 'ACTUAL_ROOTS.json').write_bytes(record_raw)
    output = {'agent': 'six-code-2', 'role': 'researcher', 'status': 'COMPLETE_INDEPENDENT_PHYSICAL_PAIR_JOIN_ROOT_CENSUS',
              'model_sha256': hashlib.sha256(raw).hexdigest(), 'admissible_rows': len(occupied),
              'actual_rooted20_stars': len(positive), 'compatible_pair_blocks': len(pairblocks),
              'every_unordered_pair_block_join_tried': trials, 'actual_roots_sha256': hashlib.sha256(record_raw).hexdigest(),
              'root_fixed_neighbor_degree_histogram': sorted(Counter((sum(w >> 16 & 1 for w in ws),
                                                                    sum(w >> 17 & 1 for w in ws)) for ws in positive).items()),
              'semantic_damage_rejections': damage_names, 'initial_whole_guard_seconds': 60,
              'seconds': time.monotonic() - begin, 'peak_RSS_kib': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
              'scope': 'Every physical C5-invariant degree20 star at root0, not a residual completion or70 absence claim.'}
    (args.work / 'AUDIT.json').write_bytes(encoded(output))
    print(json.dumps(output, sort_keys=True), flush=True)


if __name__ == '__main__':
    main()
