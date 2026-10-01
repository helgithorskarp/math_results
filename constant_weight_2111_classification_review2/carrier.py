"""Reviewer-owned marked leave carrier and generator-walk hub normalization.

No author executable code is imported. Structural leave generators and Schreier
stabilizers replace the author's enumeration of all full point maps.
"""
from collections import deque
from itertools import combinations, permutations
from math import factorial, prod
from hashlib import sha256
import json
import time

N = 17
IDENTITY = tuple(range(N))
PAIRS = tuple(combinations(range(N), 2))
CORE_PAIRS = tuple(combinations(range(4), 2))
HIGH = tuple((0,) + p for p in permutations((1, 2, 3)))
PROFILE = (3, 4, 4, 4) + (5,) * 13

def require(ok, message):
    if not ok:
        raise ValueError(message)

def digest(value):
    return sha256(json.dumps(value, sort_keys=True, separators=(',', ':')).encode()).hexdigest()

def points(word):
    return tuple(z for z in range(N) if word >> z & 1)

def word(points_):
    return sum(1 << z for z in points_)

def image_edges(edges, point):
    return tuple(sorted(tuple(sorted((point[a], point[b]))) for a, b in edges))

def image_word(w, point):
    return sum(1 << point[z] for z in points(w))

def image_star(star, point):
    return tuple(sorted(image_word(w, point) for w in star))

def image_partition(partition, point):
    return tuple(sorted(tuple(sorted(point[z] for z in triple)) for triple in partition))

def compose(a, b):
    return tuple(a[b[z]] for z in range(N))

def inverse(point):
    result = [0] * N
    for z, target in enumerate(point):
        result[target] = z
    return tuple(result)

def triples_partitions(neighbors):
    """Choose two disjoint triples, obtain the third as their complement."""
    neighbors = tuple(sorted(neighbors))
    require(len(neighbors) == 9 and len(set(neighbors)) == 9, 'nine distinct neighbors required')
    universe = frozenset(neighbors)
    triples = tuple(combinations(neighbors, 3))
    result = set()
    for a in triples:
        remaining = universe - set(a)
        for b in combinations(sorted(remaining), 3):
            c = tuple(sorted(remaining - set(b)))
            if a < b < c:
                result.add((a, b, c))
    require(len(result) == factorial(9) // (factorial(3) ** 4) == 280, 'incomplete triple partition carrier')
    return tuple(sorted(result))

def covered_pairs(words):
    return frozenset(pair for w in words for pair in combinations(points(w), 2))

def check_star(words, leave=None):
    require(len(words) == len(set(words)) == 20, 'twenty distinct words required')
    require(all(type(w) is int and 0 <= w < 1 << N and w.bit_count() == 4 for w in words), 'invalid four-point words')
    require(all((a & b).bit_count() <= 1 for a, b in combinations(words, 2)), 'pair conflict')
    require(tuple(sum(w >> z & 1 for w in words) for z in range(N)) == PROFILE, 'wrong literal replication profile')
    actual = frozenset(PAIRS) - covered_pairs(words)
    require(len(actual) == 16, 'wrong literal leave size')
    if leave is not None:
        require(actual == frozenset(leave), 'literal leave mismatch')
    return actual

def generators(record, include_hub_leaves=False):
    """All high maps and adjacent cohort/matching transpositions generate G."""
    core, cohorts, matching = record['core'], record['cohorts'], record['matching']
    high_maps = tuple(p for p in HIGH if image_edges(core, p) == core)
    result = set()
    for high in high_maps:
        point = list(IDENTITY)
        point[:4] = high
        for h in range(4):
            require(len(cohorts[h]) == len(cohorts[high[h]]), 'high image cohort dimensions differ')
            for z, target in zip(cohorts[h], cohorts[high[h]]):
                point[z] = target
        result.add(tuple(point))
    for h in range(0 if include_hub_leaves else 1, 4):
        for a, b in zip(cohorts[h], cohorts[h][1:]):
            point = list(IDENTITY)
            point[a], point[b] = b, a
            result.add(tuple(point))
    for a, b in matching:
        point = list(IDENTITY)
        point[a], point[b] = b, a
        result.add(tuple(point))
    for a, b in zip(matching, matching[1:]):
        point = list(IDENTITY)
        for z, target in zip(a, b):
            point[z], point[target] = target, z
        result.add(tuple(point))
    result.discard(IDENTITY)
    for point in result:
        require(sorted(point) == list(range(N)) and point[0] == 0 and image_edges(record['leave'], point) == record['leave'], 'false leave generator')
        if not include_hub_leaves:
            require(all(point[z] == z for z in cohorts[0]), 'omitted cohort was moved')
    order = len(high_maps) * prod(factorial(len(cohorts[h])) for h in range(0 if include_hub_leaves else 1, 4)) * factorial(len(matching)) * 2 ** len(matching)
    return tuple(sorted(result)), order

def leave_carrier():
    domain = tuple(core for e in (3, 4, 5) for core in combinations(CORE_PAIRS, e))
    require(len(domain) == 41, 'marked high domain size differs')
    unseen = set(domain)
    cores = []
    while unseen:
        core = min(unseen, key=lambda q: (len(q), q))
        orbit = {image_edges(core, p) for p in HIGH}
        require(orbit <= unseen, 'marked core orbit is incomplete/overlapping')
        unseen.difference_update(orbit)
        cores.append((core, len(orbit)))
    require([sum(len(core) == e for core, _ in cores) for e in (3, 4, 5)] == [6, 4, 2], 'wrong marked high orbit counts')
    result = []
    for index, (core, orbit_size) in enumerate(cores):
        cohorts, leave, low = [], list(core), 4
        for h, degree in enumerate((7, 4, 4, 4)):
            size = degree - sum(h in edge for edge in core)
            cohort = tuple(range(low, low + size))
            cohorts.append(cohort)
            leave.extend((h, z) for z in cohort)
            low += size
        matching = tuple((z, z + 1) for z in range(low, N, 2))
        leave.extend(matching)
        leave = tuple(sorted(leave))
        require(len(leave) == len(set(leave)) == 16 and len(matching) == len(core) - 3, 'leave carrier dimensions')
        require(tuple(sum(z in edge for edge in leave) for z in range(N)) == (7, 4, 4, 4) + (1,) * 13, 'leave degree mismatch')
        result.append(dict(index=index, core=core, e=len(core), orbit_size=orbit_size, cohorts=tuple(cohorts), matching=matching, leave=leave))
    return result

def hub_orbits(record):
    start = time.monotonic()
    neighbors = tuple(z for z in range(1, N) if (0, z) not in record['leave'])
    domain = set(p for p in triples_partitions(neighbors) if all(pair not in record['leave'] for triple in p for pair in combinations(triple, 2)))
    gens, order = generators(record)
    unseen, result, states = set(domain), [], 0
    while unseen:
        rep = min(unseen)
        transports = {rep: IDENTITY}
        queue = deque([rep])
        stabilizers = set()
        while queue:
            partition = queue.popleft()
            states += 1
            require(states <= 200000 and time.monotonic() - start <= 10, 'INCOMPLETE hub orbit guard')
            for gen in gens:
                target = image_partition(partition, gen)
                require(target in domain, 'generator leaves hub domain')
                path = compose(gen, transports[partition])
                if target not in transports:
                    transports[target] = path
                    queue.append(target)
                schreier = compose(inverse(transports[target]), path)
                require(image_partition(rep, schreier) == rep, 'false Schreier stabilizer')
                if schreier != IDENTITY:
                    stabilizers.add(schreier)
        orbit = set(transports)
        require(orbit <= unseen and order % len(orbit) == 0, 'hub orbit overlap/order mismatch')
        unseen.difference_update(orbit)
        result.append(dict(index=len(result), representative=rep, words=tuple(sorted(1 + word(t) for t in rep)), orbit_size=len(orbit), stabilizer_order=order // len(orbit), orbit_sha256=digest(sorted(orbit)), stabilizer_generators=tuple(sorted(stabilizers))))
    require(sum(o['orbit_size'] for o in result) == len(domain), 'hub carrier coverage incomplete')
    return dict(index=record['index'], valid_partitions=len(domain), group_order=order, generators=len(gens), states=states, orbits=result)

def matrix(leave, prefix):
    occupied = covered_pairs(prefix)
    require(len(occupied) == 6 * len(prefix) and not occupied & set(leave), 'prefix pair conflict')
    remaining = tuple(sorted(set(PAIRS) - set(leave) - occupied))
    available = set(remaining)
    columns = tuple(sorted(word(q) for q in combinations(range(N), 4) if set(combinations(q, 2)) <= available))
    lookup = {pair: i for i, pair in enumerate(remaining)}
    canonical = [(w, sorted(lookup[pair] for pair in combinations(points(w), 2))) for w in columns]
    require(len(remaining) + 6 * len(prefix) == 120 and len(columns) <= 1334, 'matrix dimensions')
    return remaining, columns, digest([remaining, canonical])

def second_prefix(record, prefix):
    forbidden = set(record['leave']) | set(covered_pairs(prefix))
    neighbors = tuple(z for z in range(N) if z != 1 and tuple(sorted((1, z))) not in forbidden)
    partitions = tuple(q for q in triples_partitions(neighbors) if all(pair not in forbidden for t in q for pair in combinations(t, 2)))
    require(neighbors == tuple(range(4, 11)) + (15, 16) and len(partitions) == 210, 'second-point partition dimensions')
    canonical = ((4, 5, 15), (6, 7, 16), (8, 9, 10))
    canonical = tuple(sorted(canonical))
    maps = []
    for partition in partitions:
        point = list(IDENTITY)
        used = set()
        for special, targets in ((15, (4, 5)), (16, (6, 7))):
            triple = next(t for t in partition if special in t)
            originals = tuple(z for z in triple if z != special)
            require(len(originals) == 2 and set(originals) <= set(record['cohorts'][0]) and not set(originals) & used, 'bad special triple')
            used.update(originals)
            for z, target in zip(originals, targets):
                point[z] = target
        for z, target in zip(sorted(set(record['cohorts'][0]) - used), (8, 9, 10)):
            point[z] = target
        point = tuple(point)
        require(sorted(point) == list(range(N)) and image_edges(record['leave'], point) == record['leave'] and image_star(prefix, point) == prefix and image_partition(partition, point) == canonical, 'false second-point transport')
        maps.append(point)
    fixed = tuple(sorted(prefix + tuple(2 + word(t) for t in canonical)))
    require(len(fixed) == 6, 'second prefix cardinality')
    return fixed, partitions, tuple(maps)
