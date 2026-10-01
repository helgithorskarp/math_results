"""Literal owner-role and triple-owner verifier. six-code-2, researcher.

No producer import, field arithmetic or connected-frame census is trusted.
Each of the42 graph patterns on four owner labels with >=3 edges is a
separate finite case with unchanged40000-state/45-second guards.
"""
from itertools import combinations
from pathlib import Path
import json
import time

from common import guard, require, compact_manifest


def bits(word, n=17):
    require(type(word) is int and 0 <= word < 1 << n, 'invalid point mask')
    return frozenset(p for p in range(n) if word >> p & 1)


def encode(points):
    return sum(1 << p for p in points)


def run(given):
    start = time.monotonic()
    raw = given['design_circles']
    design = [bits(c) for c in raw]
    require(len(design) == len(set(design)) == 68 and all(len(c) == 5 for c in design), 'invalid design')
    triples = {}
    for circle in design:
        for t in combinations(sorted(circle), 3):
            require(frozenset(t) not in triples, 'repeated design triple')
            triples[frozenset(t)] = circle
    require(set(triples) == {frozenset(t) for t in combinations(range(17), 3)}, 'missing design triple')
    words = [frozenset(q) for q in combinations(range(17), 4) if not any(set(q) <= c for c in design)]
    root = bits(given['root_word'])
    require(len(words) == 2040 and root in words, 'invalid noncontained domain')
    orbit, queue = {root}, [root]
    for p in given['actual_transport_generators']:
        require(sorted(p) == list(range(17))
                and {frozenset(p[x] for x in c) for c in design} == set(design), 'invalid actual map')
    for word in queue:
        for p in given['actual_transport_generators']:
            image = frozenset(p[x] for x in word)
            if image not in orbit:
                orbit.add(image)
                queue.append(image)
        guard(start, len(queue))
    require(orbit == set(words), 'transport orbit is not the whole domain')
    owners = {q: frozenset(triples[frozenset(t)] for t in combinations(sorted(q), 3)) for q in words}
    require(all(len(v) == 4 for v in owners.values()), 'repeated owner of a noncontained word')
    partners = sorted((q for q in words if len(q & root) <= 1 and len(owners[q] & owners[root]) == 1),
                      key=encode)
    edges = sorted(tuple(sorted((encode(a), encode(b)))) for a, b in combinations(partners, 2)
                   if len(a & b) <= 1 and len(owners[a] & owners[b]) == 1)
    groups = [[q for q in partners if owners[q] & owners[root] == {c}]
              for c in sorted(owners[root], key=encode)]
    require(len(groups) == 4 and sum(map(len, groups)) == len(partners)
            and set().union(*map(set, groups)) == set(partners), 'invalid owner partition')
    labels = list(combinations(range(4), 2))
    frames, pattern_stats = set(), []
    for pattern in range(64):
        if pattern.bit_count() < 3:
            continue
        case_start, states = time.monotonic(), 0
        required_edges = {pair for index, pair in enumerate(labels) if pattern >> index & 1}
        before = len(frames)
        def visit(chosen):
            nonlocal states
            states += 1
            guard(case_start, states)
            index = len(chosen)
            if index == 4:
                frames.add(tuple(sorted(encode(q) for q in chosen)))
                return
            for q in groups[index]:
                if all(len(q & r) <= 1 and len(owners[q] & owners[r]) == int((i, index) in required_edges)
                       for i, r in enumerate(chosen)):
                    visit(chosen + [q])
        visit([])
        guard(case_start, states)
        pattern_stats.append({'pattern': pattern, 'edges': len(required_edges),
                              'states': states, 'frames': len(frames) - before})
    # Every root-opposite word is tested literally against each five-word frame.
    # Do not use the producer's intersections of sharing-neighbor candidate sets.
    by_mask = {encode(q): q for q in words}
    opposites = [q for q in words if len(q & root) <= 1 and not owners[q] & owners[root]]
    negative, gap_histogram, degree_histogram, case_stats = set(), {}, {}, []
    for frame in sorted(frames):
        family = [root, *(by_mask[q] for q in frame)]
        gaps = set().union(*(owners[q] for q in family))
        gap_histogram[str(len(gaps))] = gap_histogram.get(str(len(gaps)), 0) + 1
        tails = family[1:]
        key = ','.join(map(str, sorted(sum(len(owners[q] & owners[r]) == 1 for r in tails if r != q)
                                        for q in tails)))
        degree_histogram[key] = degree_histogram.get(key, 0) + 1
        case_start, tests = time.monotonic(), 0
        for q in opposites:
            tests += 1
            guard(case_start, tests)
            if len(gaps | owners[q]) <= 13 and all(len(q & r) <= 1 for r in tails):
                negative.add(tuple(sorted([given['root_word'], *frame, encode(q)])))
        case_stats.append(tests)
    sharp = [bits(q) for q in given['sharp_four_parts']]
    require(len(sharp) == len(set(sharp)) == 6 and all(q in words for q in sharp)
            and all(len(a & b) <= 1 for a, b in combinations(sharp, 2)), 'invalid sharp parts')
    sharp_gaps = set().union(*(owners[q] for q in sharp))
    code = sorted((set(design) - sharp_gaps) | {q | {17} for q in sharp}, key=encode)
    require(len(sharp_gaps) == 14 and len(code) == len(set(code)) == 60
            and all(len(c) == 5 for c in code)
            and all(len(a & b) <= 2 for a, b in combinations(code, 2)), 'invalid sharp code')
    return {'input': given, 'noncontained': sorted(map(encode, words)), 'orbit': sorted(map(encode, orbit)),
            'partners': sorted(map(encode, partners)), 'edges': edges, 'frames': sorted(frames),
            'frame_gap_histogram': gap_histogram, 'frame_degree_histogram': degree_histogram,
            'negative_carrier': sorted(negative), 'sharp_gap_cost': len(sharp_gaps),
            'sharp_gaps': sorted(map(encode, sharp_gaps)), 'sharp_code': sorted(map(encode, code)),
            'execution': {'complete': True, 'seconds': time.monotonic() - start,
                          'patterns': pattern_stats, 'literal_owner_group_sizes': list(map(len, groups)),
                          'opposites_per_frame': len(opposites), 'opposite_tests_sum': sum(case_stats)}}


if __name__ == '__main__':
    root = Path(__file__).parent
    data = run(json.loads((root / 'input.json').read_text()))
    require(not data['negative_carrier'], 'a family with gap cost <=13 exists')
    require(compact_manifest(data) == json.loads((root / 'manifest.json').read_text()),
            'replay differs from expected manifest')
    print(json.dumps({'manifest': compact_manifest(data), 'execution': data['execution']}, indent=2))
