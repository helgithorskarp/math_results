"""Bit-mask/connected-frame exact producer. six-code-2, researcher."""
from itertools import combinations
from pathlib import Path
import json
import time

from common import construct_input, mask, move, guard, require, compact_manifest


def run(given):
    start = time.monotonic()
    generated = construct_input()
    require(generated == given, 'input differs from exact field construction')
    circles, root = set(given['design_circles']), given['root_word']
    require(len(circles) == 68 and all(c.bit_count() == 5 for c in circles), 'wrong design size')
    covered = [mask(t) for c in circles for t in combinations([p for p in range(17) if c >> p & 1], 3)]
    require(len(covered) == len(set(covered)) == 680
            and set(covered) == {mask(t) for t in combinations(range(17), 3)}, 'not Steiner')
    contained = {mask(t) for c in circles for t in combinations([p for p in range(17) if c >> p & 1], 4)}
    words = {mask(t) for t in combinations(range(17), 4)} - contained
    require(len(contained) == 340 and len(words) == 2040 and root in words, 'bad four-part inventory')
    orbit, queue = {root}, [root]
    for p in given['actual_transport_generators']:
        require(sorted(p) == list(range(17)) and {move(c, p) for c in circles} == circles,
                'invalid actual transport map')
    for word in queue:
        for p in given['actual_transport_generators']:
            image = move(word, p)
            if image not in orbit:
                orbit.add(image)
                queue.append(image)
        guard(start, len(queue))
    require(orbit == words, 'actual group is not transitive on four-parts')
    owners = {q: {c for c in circles if (c & q).bit_count() >= 3} for q in words}
    require(all(len(v) == 4 for v in owners.values()), 'a four-part has wrong forced owners')
    partners = sorted(q for q in words if (q & root).bit_count() <= 1
                      and len(owners[q] & owners[root]) == 1)
    edges = {p for p in combinations(partners, 2) if (p[0] & p[1]).bit_count() <= 1
             and len(owners[p[0]] & owners[p[1]]) == 1}
    adjacency = {q: {v for v in partners if tuple(sorted((q, v))) in edges} for q in partners}
    current, states, levels = {(q,) for q in partners}, len(partners), []
    for level in range(2, 5):
        following = set()
        for family in sorted(current):
            for q in set().union(*(adjacency[v] for v in family)) - set(family):
                if all((q & v).bit_count() <= 1 for v in family):
                    root_owners = [next(iter(owners[v] & owners[root])) for v in (*family, q)]
                    if len(set(root_owners)) == len(root_owners):
                        following.add(tuple(sorted((*family, q))))
            guard(start, states + len(following))
        current = following
        states += len(current)
        levels.append([level, len(current)])
    # Every disconnected graph on four vertices with >=3 edges is a triangle
    # plus an isolated vertex. Connected graphs were covered above.
    disconnected = set()
    for a, b in sorted(edges):
        for c in sorted(adjacency[a] & adjacency[b]):
            if c <= b:
                continue
            triangle = (a, b, c)
            for q in partners:
                if q in triangle or any(q in adjacency[v] for v in triangle):
                    continue
                family = tuple(sorted((*triangle, q)))
                if all((v & w).bit_count() <= 1 for v, w in combinations(family, 2)):
                    labels = [next(iter(owners[v] & owners[root])) for v in family]
                    if len(set(labels)) == 4:
                        disconnected.add(family)
            guard(start, states + len(disconnected))
    frames = sorted(current | disconnected)
    frames = [f for f in frames if sum(tuple(p) in edges for p in combinations(f, 2)) >= 3]
    opposites = sorted(q for q in words if (q & root).bit_count() <= 1 and not owners[q] & owners[root])
    neighbors = {q: {z for z in opposites if (q & z).bit_count() <= 1
                     and len(owners[q] & owners[z]) == 1} for q in partners}
    negative, tested, gap_histogram, degree_histogram = set(), 0, {}, {}
    for frame in frames:
        gaps = set().union(*(owners[q] for q in (root, *frame)))
        gap_histogram[str(len(gaps))] = gap_histogram.get(str(len(gaps)), 0) + 1
        degrees = tuple(sorted(len(adjacency[q] & set(frame)) for q in frame))
        key = ','.join(map(str, degrees))
        degree_histogram[key] = degree_histogram.get(key, 0) + 1
        needed = max(0, len(gaps) + 4 - 13)
        candidates = set().union(*(set.intersection(*(neighbors[q] for q in selection))
                                  for selection in combinations(frame, needed))) if needed else set(opposites)
        for z in sorted(candidates):
            tested += 1
            guard(start, tested)
            if all((z & q).bit_count() <= 1 for q in frame) and len(gaps | owners[z]) <= 13:
                negative.add(tuple(sorted((root, *frame, z))))
        guard(start)
    sharp = given['sharp_four_parts']
    require(len(sharp) == len(set(sharp)) == 6 and set(sharp) <= words
            and all((q & r).bit_count() <= 1 for q, r in combinations(sharp, 2)), 'bad sharp family')
    sharp_gaps = sorted(set().union(*(owners[q] for q in sharp)))
    code = sorted((circles - set(sharp_gaps)) | {q | (1 << 17) for q in sharp})
    require(len(sharp_gaps) == 14 and len(code) == 60
            and all(w.bit_count() == 5 for w in code)
            and all((u & v).bit_count() <= 2 for u, v in combinations(code, 2)), 'bad sharp code')
    guard(start)
    return {'input': given, 'noncontained': sorted(words), 'orbit': sorted(orbit),
            'partners': partners, 'edges': sorted(edges), 'frames': frames,
            'frame_gap_histogram': gap_histogram, 'frame_degree_histogram': degree_histogram,
            'negative_carrier': sorted(negative), 'sharp_gap_cost': len(sharp_gaps),
            'sharp_gaps': sharp_gaps, 'sharp_code': code,
            'execution': {'complete': True, 'seconds': time.monotonic() - start,
                          'connected_levels': levels, 'accepted_connected_states': states,
                          'disconnected_frames': len(disconnected), 'opposite_candidates_tested': tested}}


if __name__ == '__main__':
    data = run(json.loads((Path(__file__).parent / 'input.json').read_text()))
    require(not data['negative_carrier'], 'a family with gap cost <=13 exists')
    print(json.dumps({'manifest': compact_manifest(data), 'execution': data['execution']}, indent=2))
