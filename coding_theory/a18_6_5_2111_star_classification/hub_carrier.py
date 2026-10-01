#!/usr/bin/env python3
"""Complete hub-star carrier, checked by literal maps and incidence signatures.

This classifies only the three quadruples through shortened point zero.
It does not enumerate or exclude completions to twenty quadruples.
"""
from itertools import combinations, permutations, product
from math import factorial
from pathlib import Path
import json
import resource
import time

import carrier as c

from paths import WORK as HERE


def partitions(points):
    """Each unordered partition into triples once, by least unused point."""
    points = tuple(sorted(points))
    if not points:
        yield ()
        return
    for rest in combinations(points[1:], 2):
        block = (points[0],) + rest
        remaining = tuple(z for z in points if z not in block)
        for tail in partitions(remaining):
            yield (block,) + tail


def part_image(partition, point):
    return tuple(sorted(tuple(sorted(point[z] for z in triple)) for triple in partition))


def core_group(record):
    core = tuple(map(tuple, record['core']))
    return tuple(g for g in c.HIGH_GROUP if c.image(core, g) == core)


def point_group(record):
    """Full action on hub-covered neighbors; hub's leaf cohort fixed.

    Omitting permutations of that cohort removes only actions that fix every
    point in a possible hub triple, and hence cannot change prefix orbits.
    """
    core_maps = core_group(record)
    cohorts = record['cohorts']
    matching = record['matching']
    result = []
    for high in core_maps:
        choices = [tuple(permutations(cohorts[high[h]])) for h in (1, 2, 3)]
        for lows in product(*choices):
            for edge_order in permutations(range(len(matching))):
                for flips in product((0, 1), repeat=len(matching)):
                    point = list(range(17))
                    point[:4] = high
                    for h, images in zip((1, 2, 3), lows):
                        for original, target in zip(cohorts[h], images):
                            point[original] = target
                    for edge, target_index, flip in zip(matching, edge_order, flips):
                        target = matching[target_index]
                        point[edge[0]] = target[flip]
                        point[edge[1]] = target[1 - flip]
                    result.append(tuple(point))
    expected = (len(core_maps) * factorial(len(matching)) * 2 ** len(matching)
                * product_factorial(len(cohorts[h]) for h in (1, 2, 3)))
    group = set(result)
    if len(result) != expected or len(group) != expected or tuple(range(17)) not in group:
        raise RuntimeError('hub action size or identity differs')
    leave = tuple(map(tuple, record['leave']))
    for point in result:
        if sorted(point) != list(range(17)) or point[0] != 0 or c.image(leave, point) != leave:
            raise RuntimeError('purported hub action is not a literal leave permutation')
    # A generating set: all structural high maps, adjacent cohort swaps,
    # matching endpoint swaps, and adjacent matching-edge swaps.  These are
    # actual point maps, and their closure is checked entry by entry.
    generators = []
    for high in core_maps:
        point = list(range(17))
        point[:4] = high
        for h in (1, 2, 3):
            for original, target in zip(cohorts[h], cohorts[high[h]]):
                point[original] = target
        generators.append(tuple(point))
    for h in (1, 2, 3):
        for a, b in zip(cohorts[h], cohorts[h][1:]):
            point = list(range(17))
            point[a], point[b] = b, a
            generators.append(tuple(point))
    for a, b in matching:
        point = list(range(17))
        point[a], point[b] = b, a
        generators.append(tuple(point))
    for first, second in zip(matching, matching[1:]):
        point = list(range(17))
        for a, b in zip(first, second):
            point[a], point[b] = b, a
        generators.append(tuple(point))
    for generator in generators:
        if generator not in group:
            raise RuntimeError('hub generator absent from action')
        for point in result:
            if tuple(generator[point[z]] for z in range(17)) not in group:
                raise RuntimeError('hub action not closed under structural generators')
    return tuple(sorted(group))


def product_factorial(sizes):
    result = 1
    for n in sizes:
        result *= factorial(n)
    return result


def signature(partition, record):
    """Independent orbit key from high labels, cohort counts and matching.

    No literal low-point permutations or primary point_group are used.  An
    ordered triple signature specifies each high vertex and each cohort's
    occupancy; the matching records the unordered pair of containing triples
    for each edge.  Equal signatures give an actual cohort/matching bijection.
    """
    keys = []
    for high in core_group(record):
        for ordered in permutations(partition):
            place = {z: i for i, triple in enumerate(ordered) for z in triple}
            rows = []
            for triple in ordered:
                high_vertices = tuple(sorted(high[z] for z in triple if z < 4))
                counts = [0] * 4
                for h in (1, 2, 3):
                    counts[high[h]] = sum(z in triple for z in record['cohorts'][h])
                rows.append((high_vertices, tuple(counts)))
            match = tuple(sorted(tuple(sorted((place[a], place[b])))
                                 for a, b in record['matching']))
            keys.append((tuple(rows), match))
    return min(keys)


def hub_words(partition):
    return tuple(sorted(1 + sum(1 << z for z in triple) for triple in partition))


def shorten_hub(words):
    return tuple(sorted(tuple(z for z in range(1, 17) if w >> z & 1)
                        for w in words if w & 1))


def build_case(record):
    leave = set(map(tuple, record['leave']))
    neighbors = tuple(z for z in range(1, 17) if (0, z) not in leave)
    if len(neighbors) != 9:
        raise RuntimeError('hub covered-neighbor count differs')
    raw = list(partitions(neighbors))
    # Different partition generator: choose three disjoint triples from the
    # 84 possible triples and retain exact nine-point union.
    separate = {tuple(sorted(blocks)) for blocks in combinations(tuple(combinations(neighbors, 3)), 3)
                if len(set().union(*map(set, blocks))) == 9}
    if len(raw) != 280 or len(set(raw)) != 280 or set(raw) != separate:
        raise RuntimeError('independent triple-partition domains differ')
    valid = sorted(q for q in raw if all(edge not in leave
                  for triple in q for edge in combinations(triple, 2)))
    group = point_group(record)
    member_to_rep = {}
    orbits = []
    signature_to_rep = {}
    for partition in valid:
        if partition in member_to_rep:
            continue
        orbit = {part_image(partition, point) for point in group}
        if not orbit <= set(valid) or any(q in member_to_rep for q in orbit):
            raise RuntimeError('bad hub prefix orbit coverage')
        representative = min(orbit)
        if representative != partition:
            raise RuntimeError('noncanonical hub prefix representative')
        key = signature(representative, record)
        if key in signature_to_rep:
            raise RuntimeError('independent signature merges distinct primary orbits')
        signature_to_rep[key] = representative
        for member in orbit:
            member_to_rep[member] = representative
        stabilizer = sum(part_image(representative, point) == representative for point in group)
        if len(orbit) * stabilizer != len(group):
            raise RuntimeError('hub orbit-stabilizer identity differs')
        orbits.append(dict(index=len(orbits), representative=representative, words=hub_words(representative),
                           orbit_size=len(orbit), stabilizer_size=stabilizer,
                           orbit_sha256=c.digest(sorted(orbit))))
    for partition in valid:
        key = signature(partition, record)
        if signature_to_rep.get(key) != member_to_rep.get(partition):
            raise RuntimeError('entrywise independent hub orbit assignment differs')
    if set(member_to_rep) != set(valid) or sum(q['orbit_size'] for q in orbits) != len(valid):
        raise RuntimeError('incomplete hub prefix carrier')
    return dict(index=record['index'], e=record['e'], core=record['core'],
                covered_neighbors=neighbors, raw_partitions=len(raw), valid_partitions=len(valid),
                literal_action_order=len(group), orbit_count=len(orbits), orbits=orbits,
                partition_assignment_sha256=c.digest(sorted(member_to_rep.items())))


def residual_matrix(record, partition):
    """Exact 17-word completion matrix for a specified three-word hub star."""
    leave = set(map(tuple, record['leave']))
    prefix = hub_words(partition)
    blocks = [tuple([0] + list(triple)) for triple in partition]
    covered = set().union(*(set(combinations(block, 2)) for block in blocks))
    if len(covered) != 18 or covered & leave:
        raise RuntimeError('bad fixed hub star')
    required = sorted(set(combinations(range(17), 2)) - leave - covered)
    if len(required) != 102 or any(0 in pair for pair in required):
        raise RuntimeError('bad hub-star residual columns')
    lookup = {edge: i for i, edge in enumerate(required)}
    rows = []
    for block in combinations(range(1, 17), 4):
        pairs = tuple(combinations(block, 2))
        if all(pair in lookup for pair in pairs):
            rows.append((sum(1 << z for z in block), sorted(lookup[pair] for pair in pairs)))
    rows.sort()
    # Independently filter the complete unconditioned matrix using literal
    # intersections with the fixed prefix and with point zero.
    _, original_rows = c.matrix(tuple(sorted(leave)))
    separate = [word for word, _ in original_rows
                if not word & 1 and all((word & old).bit_count() <= 1 for old in prefix)]
    if separate != [word for word, _ in rows]:
        raise RuntimeError('independent residual candidate universe differs')
    return prefix, required, rows


def main():
    started = time.monotonic()
    leaves = json.loads((HERE / 'leave_carrier.json').read_text())
    cases = [build_case(record) for record in leaves['cases']]
    output = dict(agent='six-code-3', role='researcher',
                  status='COMPLETE hub-prefix carrier; twenty-block completions not classified',
                  marked_leave_types=len(cases), hub_prefix_orbits=sum(q['orbit_count'] for q in cases),
                  valid_labeled_prefixes=sum(q['valid_partitions'] for q in cases), cases=cases,
                  checks=['280 literal partitions per leave compared entrywise to independent triple selection',
                          'all point maps checked as actual leave permutations with generator closure',
                          'all valid prefix orbit assignments compared to independent incidence signatures'],
                  seconds=round(time.monotonic() - started, 6),
                  maxrss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    (HERE / 'hub_carrier.json').write_text(json.dumps(output, indent=2) + '\n')
    print(json.dumps({key: value for key, value in output.items() if key != 'cases'}))
    for case in cases:
        print(json.dumps({key: case[key] for key in ('index', 'e', 'valid_partitions',
                                                   'literal_action_order', 'orbit_count')}))


if __name__ == '__main__':
    main()
