#!/usr/bin/env python3
"""Packing isomorphism classes, checked by generator walks and full images.

All point permutations fix point0, the unique replication-three point.
Within a fixed leave/hub prefix the full group is its action on the nine
covered neighbors times arbitrary permutations of the point0 leaf cohort.
Every corpus has independent bitset/DLX cover evidence.  The final corpus
uses the separately checked210-to-one next-star carrier, not a guarded raw
cover run.  Search and orbit audit guards remain200000 nodes/ten seconds.
"""
from collections import deque
from itertools import combinations, permutations
import json
from math import factorial
from pathlib import Path
import resource
import time

import carrier as c
import hub_carrier as h
import second_hub as s

from paths import WORK as HERE
IDENTITY = tuple(range(17))


def guarded(nodes, started):
    if nodes > 200000 or time.monotonic() - started > 10:
        raise RuntimeError('INCOMPLETE orbit node/time guard; no classification')


def word_image(word, point):
    result = 0
    while word:
        bit = word & -word
        result |= 1 << point[bit.bit_length() - 1]
        word ^= bit
    return result


def star_image(star, point):
    return tuple(sorted(word_image(word, point) for word in star))


def small_generators(group):
    """Derive a generating set and check its complete closure equals group."""
    started = time.monotonic()
    ambient = set(group)
    closed = {IDENTITY}
    generators = []
    nodes = 0
    for candidate in sorted(ambient):
        if candidate in closed:
            continue
        generators.append(candidate)
        queue = deque(closed)
        while queue:
            point = queue.popleft()
            nodes += 1
            guarded(nodes, started)
            for generator in generators:
                result = tuple(generator[point[z]] for z in range(17))
                if result not in ambient:
                    raise RuntimeError('stabilizer generator escapes literal group')
                if result not in closed:
                    closed.add(result)
                    queue.append(result)
    if closed != ambient:
        raise RuntimeError('incomplete prefix-stabilizer generators')
    return generators


def load_corpus(index, prefix_index, leaves, carrier):
    record = leaves[index]
    prefix = tuple(carrier[index]['orbits'][prefix_index]['words'])
    if index != 5:
        primary = json.loads((HERE / f'hub_{index}_{prefix_index}_fullcover.jsonl').read_text())
        independent = json.loads((HERE / f'hub_{index}_{prefix_index}_dlx.jsonl').read_text())
        if primary['covers'] != independent['covers']:
            raise RuntimeError('corpus differs from independent cover replay')
        corpus = {tuple(sorted(prefix + tuple(words))) for words in primary['covers']}
        if len(corpus) != len(primary['covers']):
            raise RuntimeError('repeated primary corpus star')
        return corpus
    twice = json.loads((HERE / 'twice_5_0.json').read_text())
    if twice['status'] != 'COMPLETE both exhaustive residual cover censuses agree entrywise':
        raise RuntimeError('incomplete next-star corpus')
    primary = json.loads((HERE / 'twice_5_0_fullcover.jsonl').read_text())
    independent = json.loads((HERE / 'twice_5_0_dlx.jsonl').read_text())
    if primary['covers'] != independent['covers']:
        raise RuntimeError('next-star independent corpus differs')
    normalized = [tuple(sorted(tuple(twice['fixed_prefix']) + tuple(words))) for words in primary['covers']]
    forbidden = set(map(tuple, record['leave'])) | s.covered_pairs(prefix)
    partitions = [part for part in h.partitions(s.remaining_neighbors(record, prefix, 1))
                  if all(edge not in forbidden for triple in part for edge in combinations(triple, 2))]
    if len(partitions) != 210:
        raise RuntimeError('next-star expansion carrier differs')
    corpus = set()
    started = time.monotonic()
    nodes = 0
    for partition in partitions:
        point = s.normalize(record, prefix, partition)
        inverse = tuple(point.index(z) for z in range(17))
        for star in normalized:
            transported = star_image(star, inverse)
            c.validate_star(transported, list(map(tuple, record['leave'])))
            if transported in corpus:
                raise RuntimeError('next-star transported corpora overlap')
            corpus.add(transported)
            nodes += 1
            if nodes % 256 == 0:
                guarded(nodes, started)
    if len(corpus) != 210 * len(normalized):
        raise RuntimeError('next-star multiplicity reconstruction differs')
    return corpus


def classify_case(index, prefix_index, leaves, carrier):
    started = time.monotonic()
    record = leaves[index]
    partition = tuple(map(tuple, carrier[index]['orbits'][prefix_index]['representative']))
    subgroup = tuple(point for point in h.point_group(record) if h.part_image(partition, point) == partition)
    if len(subgroup) != carrier[index]['orbits'][prefix_index]['stabilizer_size']:
        raise RuntimeError('literal prefix stabilizer order differs')
    generators = small_generators(subgroup)
    cohort = tuple(record['cohorts'][0])
    for a, b in zip(cohort, cohort[1:]):
        point = list(IDENTITY)
        point[a], point[b] = b, a
        generators.append(tuple(point))
    group_order = len(subgroup) * factorial(len(cohort))
    corpus = load_corpus(index, prefix_index, leaves, carrier)
    words = set().union(*map(set, corpus))
    word_maps = [{word: word_image(word, point) for word in words} for point in generators]
    seen = set()
    orbits = []
    bfs_started = time.monotonic()
    nodes = 0
    for representative in sorted(corpus):
        if representative in seen:
            continue
        orbit = {representative}
        queue = deque([representative])
        while queue:
            star = queue.popleft()
            nodes += 1
            if nodes % 256 == 0:
                guarded(nodes, bfs_started)
            for mapping in word_maps:
                transported = tuple(sorted(mapping[word] for word in star))
                if transported not in corpus:
                    raise RuntimeError('point generator escapes complete literal corpus')
                if transported not in orbit:
                    orbit.add(transported)
                    queue.append(transported)
        if orbit & seen:
            raise RuntimeError('generator orbit overlap')
        # Different orbit construction: all literal17-point permutations in
        # the full stabilizer, not walks through generator images.
        full_started = time.monotonic()
        full_nodes = 0
        separate = set()
        for low_images in permutations(cohort):
            for small in subgroup:
                point = list(small)
                for original, target in zip(cohort, low_images):
                    point[original] = target
                separate.add(star_image(representative, point))
                full_nodes += 1
                if full_nodes % 256 == 0:
                    guarded(full_nodes, full_started)
        guarded(full_nodes, full_started)
        if full_nodes != group_order or separate != orbit or group_order % len(orbit):
            raise RuntimeError('full point-image orbit differs entrywise from generator orbit')
        seen.update(orbit)
        orbits.append(dict(index=len(orbits), representative=representative, orbit_size=len(orbit),
                           packing_automorphism_order=group_order // len(orbit),
                           orbit_sha256=c.digest(sorted(orbit)),
                           literal_group_images=full_nodes))
    if seen != corpus:
        raise RuntimeError('packing orbit carrier incomplete')
    return dict(index=index, prefix_index=prefix_index, status='COMPLETE',
                fixed_hub_words=h.hub_words(partition), full_prefix_group_order=group_order,
                generators=len(generators), cover_count=len(corpus), generator_visit_nodes=nodes,
                corpus_sha256=c.digest(sorted(corpus)), packing_orbits=len(orbits), orbits=orbits,
                seconds=round(time.monotonic() - started, 6))


def main():
    started = time.monotonic()
    leaves = json.loads((HERE / 'leave_carrier.json').read_text())['cases']
    carrier = json.loads((HERE / 'hub_carrier.json').read_text())['cases']
    feasibility = json.loads((HERE / 'hub_feasibility.json').read_text())
    if feasibility['status'] != 'COMPLETE HUB-PREFIX FEASIBILITY CLASSIFICATION':
        raise RuntimeError('hub feasibility exclusions incomplete')
    cases = []
    for positive in feasibility['positives']:
        case = classify_case(positive['index'], positive['prefix_index'], leaves, carrier)
        cases.append(case)
        print(json.dumps({key: case[key] for key in ('index', 'prefix_index', 'cover_count',
                                                   'packing_orbits', 'full_prefix_group_order', 'seconds')}), flush=True)
        report = dict(agent='six-code-3', role='researcher',
                      status='COMPLETE PACKING ISOMORPHISM CLASSIFICATION' if len(cases) == 6
                              else 'PARTIAL PACKING ISOMORPHISM CLASSIFICATION',
                      replication_profile=[3, 4, 4, 4] + [5] * 13,
                      cases=cases, packing_isomorphism_classes=sum(q['packing_orbits'] for q in cases),
                      first_hub_normal_form_covers=sum(q['cover_count'] for q in cases),
                      seconds=round(time.monotonic() - started, 6),
                      maxrss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
        (HERE / 'packing_classes.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({key: value for key, value in report.items() if key != 'cases'}), flush=True)


if __name__ == '__main__':
    main()
