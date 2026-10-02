"""All physical C5-invariant degree20 stars rooted at fixed point0.

Each star consists of four pair-disjoint orbits of five four-subsets on
the other17 points. No rooted-star classification, quotient, or solver is
an input. Initial60s whole-run guard; incomplete output proves no absence.
"""
import argparse
from collections import Counter
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


def moved(word, g):
    return sum(1 << g[p] for p in range(18) if word >> p & 1)


def orbit(word, g):
    seen = {word}
    w = moved(word, g)
    while w != word:
        need(w not in seen, 'point-map orbit fails to close')
        seen.add(w)
        w = moved(w, g)
    return tuple(sorted(seen))


def pairs(word):
    return tuple(sum(1 << p for p in ps) for ps in combinations([p for p in range(18) if word >> p & 1], 2))


def packing_star(words):
    need(len(words) == len(set(words)) == 20, 'wrong rooted star count')
    need(all(0 <= w < 2 ** 18 and w.bit_count() == 5 and w & 1 for w in words), 'nonphysical root word')
    need(all((a & b).bit_count() <= 2 for a, b in combinations(words, 2)), 'rooted star repeats a physical triple')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--model', type=Path, required=True)
    parser.add_argument('--baseline', type=Path, required=True)
    parser.add_argument('--work', type=Path, required=True)
    args = parser.parse_args()
    args.work.mkdir(parents=True, exist_ok=True)
    need(not (args.work / 'RESULT.json').exists(), 'refuse completed evidence overwrite')
    begin = time.monotonic()
    raw = args.model.read_bytes()
    need(hashlib.sha256(raw).hexdigest() == '69001d299854fb599b7a6446dd4410e8fd7355bdf498e2ed894fcdd911404500', 'different C5 physical model')
    data = json.loads(raw)
    g = tuple(data['permutation'])
    need(sorted(g) == list(range(18)) and g[0] == 0, 'bad fixed-root permutation')
    point_orbits = sorted({orbit(1 << p, g) for p in range(18)})
    need(sorted(map(len, point_orbits)) == [1, 1, 1, 5, 5, 5], 'different C5 cycle type')
    nonroot = tuple(range(1, 18))
    physical_pairs = tuple(sorted(sum(1 << p for p in ps) for ps in combinations(nonroot, 2)))
    pair_orbits = tuple(sorted({orbit(p, g) for p in physical_pairs}))
    need(Counter(map(len, pair_orbits)) == {1: 1, 5: 27}, 'wrong physical pair-orbit universe')
    pair_index = {p: i for i, ps in enumerate(pair_orbits) for p in ps}
    physical = tuple(sorted(sum(1 << p for p in ps) for ps in combinations(nonroot, 4)))
    all_orbits = tuple(sorted({orbit(w, g) for w in physical}))
    need(len(physical) == 2380 and len(all_orbits) == 476 and all(len(ws) == 5 for ws in all_orbits),
         'incomplete physical four-subset universe')
    rows = []
    rejected = 0
    for ws in all_orbits:
        covered = Counter(p for w in ws for p in pairs(w))
        if set(covered.values()) != {1}:
            rejected += 1
            continue
        used = tuple(sorted({pair_index[p] for p in covered}))
        need(len(used) == 6 and all(len(pair_orbits[i]) == 5 for i in used), 'wrong admissible pair resources')
        need(set(covered) == {p for i in used for p in pair_orbits[i]}, 'row omits part of a used pair orbit')
        rows.append({'four_subsets': ws, 'pair_orbit_resources': used})
    bits = tuple(sum(1 << i for i in r['pair_orbit_resources']) for r in rows)
    adjacency = tuple(sum(1 << j for j in range(len(rows)) if i != j and not a & bits[j]) for i, a in enumerate(bits))
    root_choices = []
    nodes = 0

    def visit(domain, selected):
        nonlocal nodes
        nodes += 1
        if nodes % 4096 == 0 and time.monotonic() - begin > 60:
            (args.work / 'partial.json').write_bytes(encoded({'status': 'INCOMPLETE_NO_FRONTIER_ABSENCE', 'complete_choices': root_choices}))
            raise TimeoutError('INCOMPLETE initial60s whole-root-enumeration guard')
        if len(selected) == 4:
            root_choices.append(selected)
            need(len(root_choices) <= 100000, 'INCOMPLETE initial100000-root storage guard')
            return
        while domain:
            if len(selected) + domain.bit_count() < 4:
                return
            bit = domain & -domain
            domain ^= bit
            v = bit.bit_length() - 1
            visit(domain & adjacency[v], selected + (v,))

    visit((1 << len(rows)) - 1, ())
    roots = []
    for selected in root_choices:
        words = tuple(sorted(w | 1 for i in selected for w in rows[i]['four_subsets']))
        packing_star(words)
        roots.append({'orbit_indices': selected, 'words': words,
                      'degrees': tuple(sum(w >> p & 1 for w in words) for p in range(18))})
    need(roots and len(roots) == len({tuple(r['words']) for r in roots}), 'missing or duplicate actual rooted star')
    baseline = json.loads(args.baseline.read_text())['words']
    baseline_star = tuple(w for w in baseline if w & 1)
    packing_star(baseline_star)
    baseline_indices = [i for i, r in enumerate(roots) if tuple(r['words']) == baseline_star]
    need(len(baseline_indices) == 1, 'known classical68 degree20 star omitted from carrier')
    orbit_raw = encoded({'pair_orbits': pair_orbits, 'admissible_rows': rows})
    roots_raw = encoded(roots)
    (args.work / 'ROOT_ORBITS.json').write_bytes(orbit_raw)
    (args.work / 'ROOTS.json').write_bytes(roots_raw)
    result = {'agent': 'six-code-2', 'role': 'researcher', 'status': 'COMPLETE_ALL_LITERAL_C5_ROOTED20_STARS',
              'model_sha256': hashlib.sha256(raw).hexdigest(), 'physical_four_subsets': len(physical),
              'all_four_subset_orbits': len(all_orbits), 'internal_pair_conflict_orbits': rejected,
              'admissible_five_quadruple_orbits': len(rows), 'pair_orbits': len(pair_orbits),
              'compatible_row_pairs': sum(a.bit_count() for a in adjacency) // 2,
              'actual_rooted20_stars': len(roots), 'baseline_root_index': baseline_indices[0],
              'root_orbits_sha256': hashlib.sha256(orbit_raw).hexdigest(), 'roots_sha256': hashlib.sha256(roots_raw).hexdigest(),
              'root_choice_DFS_nodes': nodes, 'root_fixed_neighbor_degree_histogram': sorted(Counter((r['degrees'][16], r['degrees'][17]) for r in roots).items()),
              'initial_whole_guard_seconds': 60, 'initial_max_roots_storage_guard': 100000,
              'seconds': time.monotonic() - begin, 'peak_RSS_kib': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
              'scope': 'Every literal C5-invariant20-word star at root0 for the supplied5^3*1^3 permutation. No residual completion bound or global70 absence.'}
    (args.work / 'RESULT.json').write_bytes(encoded(result))
    print(json.dumps(result, sort_keys=True), flush=True)


if __name__ == '__main__':
    main()
