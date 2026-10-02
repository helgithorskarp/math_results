"""Regenerate the full physical orbit model from a compact literal fixture.

Standard library, no previous private pilot, solver, field implementation or
generic star classification required. The literal68 baseline is prior art.
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


def mask(ps):
    return sum(1 << p for p in ps)


def moved(word, g):
    return sum(1 << g[p] for p in range(18) if word >> p & 1)


def orbit(word, g):
    result = {word}
    w = moved(word, g)
    while w != word:
        need(w not in result, 'bad physical orbit')
        result.add(w)
        w = moved(w, g)
    return tuple(sorted(result))


def triples(word):
    return tuple(mask(ps) for ps in combinations([p for p in range(18) if word >> p & 1], 3))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--instance', type=Path, default=Path(__file__).parent / 'INSTANCE.json')
    parser.add_argument('--work', type=Path, required=True)
    args = parser.parse_args()
    args.work.mkdir(parents=True, exist_ok=True)
    need(not (args.work / 'RESULT.json').exists(), 'refuse completed model overwrite')
    begin = time.monotonic()
    instance_raw = args.instance.read_bytes()
    fixture = json.loads(instance_raw)
    g = tuple(fixture['permutation'])
    baseline = tuple(fixture['classical68_words'])
    need(sorted(g) == list(range(18)), 'bad point permutation')
    point_orbits = tuple(sorted({orbit(1 << p, g) for p in range(18)}))
    need(sorted(map(len, point_orbits)) == [1, 1, 1, 5, 5, 5], 'different order5 cycle type')
    physical_triples = tuple(sorted(mask(ps) for ps in combinations(range(18), 3)))
    triple_orbits = tuple(sorted({orbit(t, g) for t in physical_triples}))
    need(Counter(map(len, triple_orbits)) == {1: 1, 5: 163}, 'triple-orbit universe mismatch')
    resource_index = {t: i for i, ts in enumerate(triple_orbits) for t in ts}
    physical_words = tuple(sorted(mask(ps) for ps in combinations(range(18), 5)))
    word_orbits = tuple(sorted({orbit(w, g) for w in physical_words}))
    need(Counter(map(len, word_orbits)) == {1: 3, 5: 1713}, 'word-orbit universe mismatch')
    long_rows, short_rows = [], []
    rejected = 0
    for ws in word_orbits:
        coverage = Counter(t for w in ws for t in triples(w))
        if set(coverage.values()) != {1}:
            rejected += 1
            continue
        resources = tuple(sorted({resource_index[t] for t in coverage}))
        need(set(coverage) == {t for i in resources for t in triple_orbits[i]}, 'incomplete occupied resource')
        row = {'words': ws, 'resources': resources}
        if len(ws) == 5:
            need(len(resources) == 10, 'wrong long-orbit resources')
            long_rows.append(row)
        else:
            need(len(resources) == 2, 'wrong singleton resource')
            short_rows.append(row)
    need(len(baseline) == len(set(baseline)) == 68 and baseline == tuple(sorted(baseline)), 'wrong literal baseline size')
    need(all(0 <= w < 2 ** 17 and w.bit_count() == 5 for w in baseline), 'baseline not on17 points')
    covered = Counter(t for w in baseline for t in triples(w))
    need(set(covered) == {mask(ps) for ps in combinations(range(17), 3)} and set(covered.values()) == {1},
         'baseline is not a physical S(3,5,17)')
    need({moved(w, g) for w in baseline} == set(baseline), 'baseline notC5 preserved')
    long_ids = [i for i, r in enumerate(long_rows) if set(r['words']) <= set(baseline)]
    short_ids = [i for i, r in enumerate(short_rows) if set(r['words']) <= set(baseline)]
    need(len(long_ids) == 13 and len(short_ids) == 3, 'baseline orbit decomposition mismatch')
    data = {'agent': 'six-code-2', 'role': 'researcher', 'permutation': g,
            'point_orbits': point_orbits, 'triple_orbits': triple_orbits,
            'admissible_five_word_orbits': long_rows, 'invariant_one_word_orbits': short_rows,
            'baseline_long_orbit_indices': long_ids, 'baseline_short_orbit_indices': short_ids}
    raw = encoded(data)
    (args.work / 'ORBIT_MODEL.json').write_bytes(raw)
    (args.work / 'BASELINE68.json').write_bytes(encoded({'words': baseline, 'status': 'REPRODUCED_PRIOR_ART_ONLY'}))
    result = {'agent': 'six-code-2', 'role': 'researcher', 'status': 'COMPLETE_SELF_CONTAINED_PHYSICAL_C5_MODEL',
              'instance_sha256': hashlib.sha256(instance_raw).hexdigest(), 'model_sha256': hashlib.sha256(raw).hexdigest(),
              'physical_words': len(physical_words), 'all_word_orbits': len(word_orbits),
              'rejected_internal_conflict_orbits': rejected, 'admissible_long_orbits': len(long_rows),
              'invariant_words': len(short_rows), 'triple_orbits': len(triple_orbits), 'prior_baseline_words': len(baseline),
              'seconds': time.monotonic() - begin, 'peak_RSS_kib': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
              'solver_used': False, 'scope': 'Full orbit model and prior68 witness validation, not a new lower bound.'}
    (args.work / 'RESULT.json').write_bytes(encoded(result))
    print(json.dumps(result, sort_keys=True), flush=True)


if __name__ == '__main__':
    main()
