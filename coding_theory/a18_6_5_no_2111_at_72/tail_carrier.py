"""Exact shared-tail quotient for all ordered pairs of the eight stars.

The centers x,y share three words, hence three disjoint three-point tails.
All tail bijections form a 1296-element carrier. Literal automorphisms of
the first and second stars act on its left and right. Every resulting
orbit is independently checked by all pairs of actual point maps.
"""
from collections import deque
from itertools import permutations, product
from pathlib import Path
import hashlib
import json
import resource
import time

from paths import BASE, WORK
ROOT = WORK
SOURCE = BASE
IDENTITY = tuple(range(17))


def digest(value):
    return hashlib.sha256(json.dumps(value, separators=(',', ':'), sort_keys=True).encode()).hexdigest()


def guard(nodes, started):
    if nodes > 200000 or time.monotonic() - started > 10:
        raise RuntimeError('INCOMPLETE carrier node/time guard')


def canonical_domain():
    triples = ((0, 1, 2), (3, 4, 5), (6, 7, 8))
    primary = set()
    for groups in permutations(triples):
        for choices in product(*(list(permutations(g)) for g in groups)):
            primary.add(sum(choices, ()))
    separate = set()
    allowed = set(map(frozenset, triples))
    for first in range(9):
        started = time.monotonic()
        nodes = 0
        for remainder in permutations([x for x in range(9) if x != first]):
            nodes += 1
            if nodes % 512 == 0:
                guard(nodes, started)
            point = (first,) + remainder
            if all(frozenset(point[i:i+3]) in allowed for i in (0, 3, 6)):
                separate.add(point)
        guard(nodes, started)
    if primary != separate or len(primary) != 1296:
        raise RuntimeError('independent nine-point tail carriers differ')
    return sorted(primary)


def generators(group):
    group = set(group)
    closed = {IDENTITY}
    answer = []
    for point in sorted(group):
        if point in closed:
            continue
        answer.append(point)
        queue = deque(closed)
        while queue:
            old = queue.popleft()
            for generator in answer:
                new = tuple(generator[old[i]] for i in range(17))
                if new not in group:
                    raise RuntimeError('literal automorphism group is not closed')
                if new not in closed:
                    closed.add(new)
                    queue.append(new)
    if closed != group:
        raise RuntimeError('incomplete automorphism generator closure')
    return answer


def stars():
    expected = json.loads((SOURCE / 'expected.json').read_text())
    audit = json.loads((ROOT / 'automorphism_audit.json').read_text())
    if not audit['status'].startswith('COMPLETE'):
        raise RuntimeError('literal automorphism census is incomplete')
    if audit['expected_sha256'] != hashlib.sha256((SOURCE / 'expected.json').read_bytes()).hexdigest():
        raise RuntimeError('automorphism input fingerprint differs')
    result = []
    for family in expected['packing_families']:
        for orbit in family['orbits']:
            words = orbit['representative']
            shared = sorted(w for w in words if w & 1)
            triples = [tuple(i for i in range(1, 17) if w >> i & 1) for w in shared]
            tail = sorted(set().union(*map(set, triples)))
            free = sorted(set(range(1, 17)) - set(tail))
            auto = [tuple(p) for p in audit['cases'][len(result)]['automorphisms']]
            if len(shared) != 3 or len(tail) != 9 or len(free) != 7:
                raise RuntimeError('shared-tail input has wrong sizes')
            for p in auto:
                transported = {sum(1 << p[i] for i in range(17) if w >> i & 1) for w in words}
                if p[0] != 0 or len(set(p)) != 17 or transported != set(words):
                    raise RuntimeError('input point map fails literal star preservation')
            result.append(dict(class_index=len(result), words=words, triples=triples,
                               tail=tail, free=free, automorphisms=auto,
                               generators=generators(auto)))
    if len(result) != 8:
        raise RuntimeError('eight star inputs required')
    return result


def pair_carrier(first, second, canonical):
    started = time.monotonic()
    source = second['tail']
    index = {u: i for i, u in enumerate(source)}
    target = first['tail']
    domain = set()
    for order in permutations(first['triples']):
        for choices in product(*(list(permutations(g)) for g in order)):
            point = dict(zip(sum(second['triples'], ()), sum(choices, ())))
            domain.add(tuple(point[u] for u in source))
    literal = set()
    flattened_source = sum(second['triples'], ())
    flattened_target = sum(first['triples'], ())
    for q in canonical:
        point = {flattened_source[u]: flattened_target[q[u]] for u in range(9)}
        literal.add(tuple(point[u] for u in source))
    if domain != literal or len(domain) != 1296:
        raise RuntimeError('literal star tail carrier differs from independent domain')
    seen = set()
    orbits = []
    nodes = 0
    for representative in sorted(domain):
        if representative in seen:
            continue
        orbit = {representative}
        queue = deque(orbit)
        while queue:
            old = queue.popleft()
            nodes += 1
            if nodes % 128 == 0:
                guard(nodes, started)
            images = [tuple(p[v] for v in old) for p in first['generators']]
            images += [tuple(old[index[p[u]]] for u in source) for p in second['generators']]
            for image in images:
                if image not in domain:
                    raise RuntimeError('point-map generator escapes tail carrier')
                if image not in orbit:
                    orbit.add(image)
                    queue.append(image)
        independently = {tuple(a[representative[index[b[u]]]] for u in source)
                         for a in first['automorphisms'] for b in second['automorphisms']}
        order = len(first['automorphisms']) * len(second['automorphisms'])
        if orbit != independently or orbit & seen or order % len(orbit):
            raise RuntimeError('literal full-group orbit check differs')
        seen.update(orbit)
        orbits.append(dict(index=len(orbits), representative=representative,
                           orbit_size=len(orbit), full_action_order=order,
                           partial_stabilizer_order=order // len(orbit),
                           orbit_sha256=digest(sorted(orbit))))
    guard(nodes, started)
    if seen != domain or sum(q['orbit_size'] for q in orbits) != 1296:
        raise RuntimeError('incomplete tail orbit partition')
    return dict(first=first['class_index'], second=second['class_index'], orbits=orbits,
                tail_maps=1296, orbit_count=len(orbits), nodes=nodes,
                carrier_sha256=digest(sorted(domain)), seconds=round(time.monotonic()-started, 6))


def run():
    started = time.monotonic()
    canonical = canonical_domain()
    inputs = stars()
    result = dict(agent='six-code-3', role='researcher', status='INCOMPLETE',
                  stars=inputs, canonical_tail_domain_sha256=digest(canonical), pairs=[])
    output = ROOT / 'tail_carrier.json'
    output.write_text(json.dumps(result, indent=2)+'\n')
    for first in inputs:
        for second in inputs:
            entry = pair_carrier(first, second, canonical)
            result['pairs'].append(entry)
        output.write_text(json.dumps(result, indent=2)+'\n')
        print('first', first['class_index'], 'orbit counts',
              [q['orbit_count'] for q in result['pairs'][-8:]], flush=True)
    result.update(status='COMPLETE shared-tail orbit classification; compatibility not yet checked',
                  total_orbits=sum(q['orbit_count'] for q in result['pairs']),
                  total_tail_maps=64*1296, seconds=round(time.monotonic()-started, 6),
                  maxrss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    output.write_text(json.dumps(result, indent=2)+'\n')
    print(result['status'], result['total_orbits'])
    return result


if __name__ == '__main__':
    run()
