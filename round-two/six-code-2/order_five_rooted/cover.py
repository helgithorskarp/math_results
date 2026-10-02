"""Positive physical transports covering every rooted20 star from one seed."""
import argparse
import hashlib
from itertools import permutations, product
import json
from pathlib import Path
import resource
import time


def need(ok, message):
    if not ok:
        raise ValueError(message)


def encoded(value):
    return (json.dumps(value, sort_keys=True, separators=(',', ':')) + '\n').encode()


def move(word, p):
    return sum(1 << p[i] for i in range(18) if word >> i & 1)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--model', type=Path, required=True)
    parser.add_argument('--roots', type=Path, required=True)
    parser.add_argument('--seed', type=int, required=True)
    parser.add_argument('--work', type=Path, required=True)
    args = parser.parse_args()
    args.work.mkdir(parents=True, exist_ok=True)
    need(not (args.work / 'RESULT.json').exists(), 'refuse completed cover overwrite')
    begin = time.monotonic()
    model_raw, roots_raw = args.model.read_bytes(), args.roots.read_bytes()
    g = tuple(json.loads(model_raw)['permutation'])
    roots = json.loads(roots_raw)
    lookup = {tuple(r['words']): i for i, r in enumerate(roots)}
    need(len(lookup) == len(roots) == 100, 'different rooted carrier')
    seed = tuple(roots[args.seed]['words'])
    fixed = [i for i in range(18) if g[i] == i]
    need(fixed == [0, 16, 17], 'different fixed points')
    remaining = set(range(18)) - set(fixed)
    cycles = []
    while remaining:
        start = min(remaining)
        cycle = [start]
        while g[cycle[-1]] != start:
            cycle.append(g[cycle[-1]])
        need(len(cycle) == 5, 'wrong point cycle')
        cycles.append(tuple(cycle))
        remaining.difference_update(cycle)
    group = set()
    maps = {}
    for order in permutations(range(3)):
        for shifts in product(range(5), repeat=3):
            for swap in range(2):
                p = list(range(18))
                if swap:
                    p[16], p[17] = 17, 16
                for i, cycle in enumerate(cycles):
                    for k, point in enumerate(cycle):
                        p[point] = cycles[order[i]][(k + shifts[i]) % 5]
                p = tuple(p)
                need(sorted(p) == list(range(18)) and p[0] == 0 and
                     all(p[g[i]] == g[p[i]] for i in range(18)), 'not a root-preserving commuting point bijection')
                need(p not in group, 'duplicated centralizer point map')
                group.add(p)
                image = tuple(sorted(move(w, p) for w in seed))
                need(image in lookup, 'centralizer image omitted from rooted carrier')
                ri = lookup[image]
                if ri not in maps:
                    inverse = tuple(p.index(i) for i in range(18))
                    need(tuple(sorted(move(w, inverse) for w in image)) == seed, 'inverse normalization failed')
                    maps[ri] = {'root_index': ri, 'seed_to_root_point_map': p, 'root_to_seed_point_map': inverse}
    need(len(group) == 1500 and set(maps) == set(range(len(roots))), 'actual point maps do not cover every root')
    raw = encoded({'seed_root_index': args.seed, 'seed_words': seed,
                   'point_transports': [maps[i] for i in range(len(roots))]})
    (args.work / 'COVER.json').write_bytes(raw)
    result = {'agent': 'six-code-2', 'role': 'researcher', 'status': 'COMPLETE_POSITIVE_C5_ROOT_TRANSPORT_COVER',
              'model_sha256': hashlib.sha256(model_raw).hexdigest(), 'roots_sha256': hashlib.sha256(roots_raw).hexdigest(),
              'actual_commuting_point_maps': len(group), 'positively_covered_roots': len(maps), 'seed_root_index': args.seed,
              'cover_sha256': hashlib.sha256(raw).hexdigest(), 'seconds': time.monotonic() - begin,
              'peak_RSS_kib': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
              'scope': 'Actual rooted-star point maps, not abstract orbit division. Commuting bijections preserve all physical C5 packings.'}
    (args.work / 'RESULT.json').write_bytes(encoded(result))
    print(json.dumps(result, sort_keys=True), flush=True)


if __name__ == '__main__':
    main()
