#!/usr/bin/env python3
"""Exact next-star normalization for leave5, hub-prefix0.

The remaining nine neighbors of high point1 are seven interchangeable leaves
of point0 and the two points15,16 whose pair is already covered.  Its three
remaining quadruples partition these neighbors into triples.  Points15,16
must occur separately.  All210 permitted partitions are carried to one
specified partition by actual permutations of the seven point0 leaves.
"""
from itertools import combinations
import json
from pathlib import Path
import resource
import subprocess
import time

import carrier as c
import hub_carrier as h

from paths import WORK as HERE


def covered_pairs(words):
    return set().union(*(set(combinations([z for z in range(17) if word >> z & 1], 2))
                         for word in words))


def remaining_neighbors(record, fixed, point):
    forbidden = set(map(tuple, record['leave'])) | covered_pairs(fixed)
    return tuple(z for z in range(17) if z != point and tuple(sorted((point, z))) not in forbidden)


def normalize(record, fixed, partition):
    cohort = tuple(record['cohorts'][0])
    leaves = (15, 16)
    point = list(range(17))
    remaining = set(cohort)
    for special, target in zip(leaves, ((4, 5), (6, 7))):
        triple = next(q for q in partition if special in q)
        original = sorted(set(triple) - {special})
        if len(original) != 2 or not set(original) <= remaining:
            raise RuntimeError('bad distinguished remaining triple')
        for a, b in zip(original, target):
            point[a] = b
        remaining.difference_update(original)
    for a, b in zip(sorted(remaining), (8, 9, 10)):
        point[a] = b
    if sorted(point) != list(range(17)) or c.image(record['leave'], point) != tuple(map(tuple, record['leave'])):
        raise RuntimeError('next-star transport not a literal leave permutation')
    mapped = sorted(sum(1 << point[z] for z in range(17) if word >> z & 1) for word in fixed)
    if mapped != sorted(fixed):
        raise RuntimeError('next-star transport changes original hub prefix')
    return tuple(point)


def matrix(record, fixed):
    leave = set(map(tuple, record['leave']))
    covered = covered_pairs(fixed)
    if len(fixed) != 6 or len(set(fixed)) != 6 or len(covered) != 36 or covered & leave:
        raise RuntimeError('bad six-quadruple prefix')
    required = sorted(set(combinations(range(17), 2)) - leave - covered)
    if len(required) != 84 or any(set(pair) & {0, 1} for pair in required):
        raise RuntimeError('bad twice-conditioned residual columns')
    lookup = {pair: i for i, pair in enumerate(required)}
    rows = []
    for points in combinations(range(2, 17), 4):
        pairs = tuple(combinations(points, 2))
        if all(pair in lookup for pair in pairs):
            rows.append((sum(1 << z for z in points), sorted(lookup[pair] for pair in pairs)))
    rows.sort()
    _, original = c.matrix(tuple(sorted(leave)))
    separate = [word for word, _ in original if not word & 3
                and all((word & old).bit_count() <= 1 for old in fixed)]
    if separate != [word for word, _ in rows]:
        raise RuntimeError('independent twice-conditioned candidate domain differs')
    return required, rows


def main():
    started = time.monotonic()
    record = json.loads((HERE / 'leave_carrier.json').read_text())['cases'][5]
    prefix = tuple(json.loads((HERE / 'hub_carrier.json').read_text())['cases'][5]['orbits'][0]['words'])
    neighbors = remaining_neighbors(record, prefix, 1)
    expected = tuple(range(4, 11)) + (15, 16)
    if neighbors != expected:
        raise RuntimeError('next-star neighbor domain differs')
    forbidden = set(map(tuple, record['leave'])) | covered_pairs(prefix)
    raw = list(h.partitions(neighbors))
    valid = [q for q in raw if all(pair not in forbidden for triple in q for pair in combinations(triple, 2))]
    # Separate construction: choose two low neighbors for15, two of the
    # remaining five for16, and use the remaining three as the last triple.
    separate = set()
    cohort = tuple(record['cohorts'][0])
    for first in combinations(cohort, 2):
        for second in combinations(tuple(z for z in cohort if z not in first), 2):
            final = tuple(z for z in cohort if z not in first and z not in second)
            separate.add(tuple(sorted((tuple(sorted(first + (15,))), tuple(sorted(second + (16,))), final))))
    canonical = tuple(sorted(((4, 5, 15), (6, 7, 16), (8, 9, 10))))
    if len(raw) != 280 or len(valid) != 210 or set(valid) != separate:
        raise RuntimeError('independent next-star partition carriers differ')
    maps = []
    for partition in valid:
        point = normalize(record, prefix, partition)
        if h.part_image(partition, point) != canonical:
            raise RuntimeError('next-star normalization misses canonical prefix')
        maps.append(point)
    next_words = tuple(sorted(2 + sum(1 << z for z in triple) for triple in canonical))
    fixed = tuple(sorted(prefix + next_words))
    required, rows = matrix(record, fixed)
    inp = HERE / 'twice_5_0.input'
    lines = [f'{len(required)} {len(rows)} 6']
    lines.extend(str(word) + ' ' + ' '.join(map(str, columns)) for word, columns in rows)
    lines += ['1', '0 0']
    inp.write_text('\n'.join(lines) + '\n')
    outputs = []
    report = dict(agent='six-code-3', role='researcher', index=5, prefix_index=0,
                  status='COMPLETE next-star normalization; residual cover census pending',
                  fixed_prefix=fixed, next_star_points=neighbors, raw_partitions=280,
                  valid_partitions=210, next_star_orbits=1,
                  transport_maps_sha256=c.digest(maps), partition_domain_sha256=c.digest(sorted(valid)),
                  candidates=len(rows), columns=len(required), matrix_sha256=c.digest([required, rows]))
    for kernel in ('fullcover', 'dlx'):
        out = HERE / ('twice_5_0_' + kernel + '.jsonl')
        result = subprocess.run([str(HERE / kernel), str(inp), str(out)],
                                capture_output=True, text=True, timeout=20)
        if result.returncode:
            report.update(status='INCOMPLETE residual cover census; normalization remains complete',
                          incomplete_kernel=kernel, stderr=result.stderr)
            break
        answer = json.loads(out.read_text())
        if answer['index'] != 0 or not answer['covers']:
            raise RuntimeError('unexpected empty twice-conditioned completion family')
        for words in answer['covers']:
            star = tuple(sorted(fixed + tuple(words)))
            c.validate_star(star, list(map(tuple, record['leave'])))
            if len(words) != 14 or set(q for q in star if q & 2) != set(q for q in fixed if q & 2):
                raise RuntimeError('twice-conditioned completion differs from next-star prefix')
        if outputs and answer['covers'] != outputs[0]['covers']:
            raise RuntimeError('twice-conditioned censuses differ entry by entry')
        outputs.append(answer)
    if len(outputs) == 2:
        report.update(status='COMPLETE both exhaustive residual cover censuses agree entrywise',
                      covers=len(outputs[0]['covers']), primary_nodes=outputs[0]['nodes'],
                      sparse_nodes=outputs[1]['nodes'], output_sha256=c.digest(outputs[0]['covers']),
                      first_hub_normal_form_covers=210 * len(outputs[0]['covers']),
                      witness=sorted(fixed + tuple(outputs[0]['covers'][0])))
    report.update(seconds=round(time.monotonic() - started, 6),
                  parent_maxrss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
                  child_maxrss_kib=resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss)
    (HERE / 'twice_5_0.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report))


if __name__ == '__main__':
    main()
