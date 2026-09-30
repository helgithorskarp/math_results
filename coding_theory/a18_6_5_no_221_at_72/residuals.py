#!/usr/bin/env python3
"""Complete mixed residual maxima after both cover engines finish a shape."""
import argparse
from itertools import combinations
import importlib.util
import json
from pathlib import Path
import resource
import time
import helpers as p
from census import save

HERE = p.WORK
spec = importlib.util.spec_from_file_location('oldverify', p.SOURCE / 'verify.py')
v = importlib.util.module_from_spec(spec)
spec.loader.exec_module(v)


def run(shape):
    started = time.monotonic()
    census = json.loads((HERE / f'census_s{shape}.json').read_text())
    replay = json.loads((HERE / f'replay_s{shape}.json').read_text())
    if len(census['completed_models']) != census['c_orbits'] or len(replay['completed_models']) != census['c_orbits']:
        raise RuntimeError('INCOMPLETE second-star census/replay')
    if census['definition_sha256'] != replay['definition_sha256']:
        raise RuntimeError('cover replay definition mismatch')
    templates = json.loads((HERE / 'first_star_templates.json').read_text())
    template = templates[shape]
    groups = json.loads((HERE / f'c_orbits_s{shape}.json').read_text())['groups']
    domain = set()
    for model in census['completed_models']:
        for positive in model['positives']:
            domain.update(p.m.transport(positive['star'], permutation) for permutation in groups)
    seen = set()
    orbits = []
    for star in sorted(domain):
        if star in seen:
            continue
        orbit = {p.m.transport(star, permutation) for permutation in groups}
        if not orbit <= domain or orbit & seen or star != min(orbit):
            raise RuntimeError('joint-star orbit mismatch')
        seen.update(orbit)
        orbits.append((star, len(orbit)))
    if seen != domain:
        raise RuntimeError('missing joint-star orbit')
    records = []
    for i, (star, orbit_size) in enumerate(orbits):
        fixed = sorted(set([w | (1 << 17) for w in template['star']] + list(star)))
        if len(fixed) != 37 or any((a & b).bit_count() > 2 for a, b in combinations(fixed, 2)):
            raise RuntimeError('invalid37-word joint star')
        candidates = [sum(1 << z for z in q) for q in combinations(range(1, 17), 5)
                      if all((sum(1 << z for z in q) & word).bit_count() <= 2 for word in fixed)]
        adjacency = [sum(1 << j for j, u in enumerate(candidates)
                         if j != k and (w & u).bit_count() <= 2)
                     for k, w in enumerate(candidates)]
        best, nodes = p.m.maximum(adjacency)
        literal_fixed = [frozenset(p.points(w)) for w in fixed]
        literal_candidates = [frozenset(q) for q in combinations(range(1, 17), 5)
                              if all(len(frozenset(q) & word) <= 2 for word in literal_fixed)]
        if [sum(1 << z for z in q) for q in literal_candidates] != candidates:
            raise RuntimeError('independent residual candidates mismatch')
        by_triple = {}
        conflicts = [set() for _ in candidates]
        for k, q in enumerate(literal_candidates):
            for triple in combinations(sorted(q), 3):
                by_triple.setdefault(triple, []).append(k)
        for ids in by_triple.values():
            for a, b in combinations(ids, 2):
                conflicts[a].add(b)
                conflicts[b].add(a)
        if any((b in conflicts[a]) != (len(q & r) > 2)
               for (a, q), (b, r) in combinations(enumerate(literal_candidates), 2)):
            raise RuntimeError('literal/triple conflict graph mismatch')
        exists, check_nodes = v.independent_set_at_least(conflicts, len(best) + 1)
        if exists:
            raise RuntimeError('residual maximum disagrees with binary replay')
        words = sorted(fixed + [candidates[k] for k in best])
        if len(words) != 37 + len(best) or any(w.bit_count() != 5 for w in words) or any(
                (a & b).bit_count() > 2 for a, b in combinations(words, 2)):
            raise RuntimeError('bad attaining packing')
        for center, expected in [(17, [2, 2, 1]), (0, [2, 1, 1, 1])]:
            if sum(w >> center & 1 for w in words) != 20:
                raise RuntimeError('wrong attaining point degree')
            deficits = sorted((5 - sum((w >> center & 1) and (w >> z & 1) for w in words)
                               for z in range(18) if z != center), reverse=True)
            if [k for k in deficits if k] != expected:
                raise RuntimeError('wrong attaining deficit row')
        record = dict(index=i, orbit_size=orbit_size, star=star, candidates=len(candidates),
                      candidate_sha256=p.digest(candidates), residual_maximum=len(best),
                      packing_maximum=len(words), maximum_nodes=nodes, binary_nodes=check_nodes,
                      attaining_words=words)
        records.append(record)
        save(HERE / f'residual_s{shape}.json', dict(status='INCOMPLETE', completed=len(records),
             total_orbits=len(orbits), records=records))
        print(json.dumps({k: z for k, z in record.items() if k not in ('star', 'attaining_words')}), flush=True)
    result = dict(agent='six-code-3', role='researcher', shape=shape, status='COMPLETE',
                  raw_second_stars=len(domain), joint_star_orbits=len(orbits), records=records,
                  sharp_restricted_maximum=max(d['packing_maximum'] for d in records),
                  maximum_nodes=sum(d['maximum_nodes'] for d in records),
                  max_case_maximum_nodes=max(d['maximum_nodes'] for d in records),
                  binary_nodes=sum(d['binary_nodes'] for d in records),
                  max_case_binary_nodes=max(d['binary_nodes'] for d in records),
                  seconds=round(time.monotonic() - started, 6),
                  maxrss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    save(HERE / f'residual_s{shape}.json', result)
    print(json.dumps({k: z for k, z in result.items() if k != 'records'}), flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--shape', type=int, choices=range(3), required=True)
    args = parser.parse_args()
    run(args.shape)
