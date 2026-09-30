"""Generate an exact branch/color certificate using integer triple incidence.

Python 3.11+, standard library. This program does not consume an orbit database.
The separate verifier reconstructs the graph using sets of points and checks
each certificate inference without running this search.
"""
from itertools import combinations
from pathlib import Path
import json
import time

G = tuple(5 * (i // 5) + (i + 1) % 5 if i < 15 else i for i in range(18))


def act(word):
    return sum(1 << G[i] for i in range(18) if word >> i & 1)


def points(word):
    return tuple(i for i in range(18) if word >> i & 1)


def make_model():
    seen = set()
    full = []
    fixed = []
    for b in combinations(range(18), 5):
        w = sum(1 << i for i in b)
        if w in seen:
            continue
        orbit = set()
        x = w
        while x not in orbit:
            orbit.add(x)
            x = act(x)
        if x != w:
            raise ValueError('orbit failed to close')
        seen.update(orbit)
        if len(orbit) == 1:
            fixed.append(w)
        elif all((a & b).bit_count() <= 2 for a, b in combinations(orbit, 2)):
            full.append(tuple(sorted(orbit, key=points)))
    full.sort(key=lambda o: tuple(map(points, o)))
    rows = []
    for orbit in full:
        triples = {sum(1 << p for p in t) for w in orbit
                   for t in combinations(points(w), 3)}
        if len(triples) != 50:
            raise ValueError('admissible orbit has repeated triple')
        rows.append(triples)
    return full, fixed, rows


def graph(rows):
    return [sum(1 << j for j, b in enumerate(rows) if i != j and not a & b)
            for i, a in enumerate(rows)]


def clique_list(adjacency, target):
    result = []

    def visit(choice, candidates):
        if len(choice) == target:
            result.append(choice)
            return
        if candidates.bit_count() < target - len(choice):
            return
        while candidates:
            bit = candidates & -candidates
            candidates ^= bit
            v = bit.bit_length() - 1
            visit(choice + (v,), candidates & adjacency[v])

    visit((), (1 << len(adjacency)) - 1)
    return result


def certify(adjacency, target):
    nodes = 0
    started = time.monotonic()

    def color(p):
        classes = []
        while p:
            available = p
            cls = []
            while available:
                bit = available & -available
                v = bit.bit_length() - 1
                cls.append(v)
                p ^= bit
                available ^= bit
                available &= ~adjacency[v]
            classes.append(cls)
        return classes

    def visit(p, need):
        nonlocal nodes
        nodes += 1
        if time.monotonic() - started > 20:
            raise TimeoutError('incomplete certificate: 20 second guard')
        if need == 0:
            raise ValueError('target clique found; exclusion is false')
        if p.bit_count() < need:
            return {'small': True}
        classes = color(p)
        node = {'colors': classes, 'children': []}
        for cls in reversed(classes[need - 1:]):
            for v in reversed(cls):
                node['children'].append(visit(p & adjacency[v], need - 1))
                p &= ~(1 << v)
        return node

    tree = visit((1 << len(adjacency)) - 1, target)
    return tree, nodes


def main():
    full, fixed, rows = make_model()
    ids = [i for i, orbit in enumerate(full) if orbit[0] >> 17 & 1]
    links = clique_list(graph([rows[i] for i in ids]), 4)
    representative = tuple(ids[i] for i in links[0])
    covered = set().union(*(rows[i] for i in representative))
    residual = [i for i, row in enumerate(rows) if not row & covered]
    adjacency = graph([rows[i] for i in residual])
    proof, nodes = certify(adjacency, 10)
    data = {'format': 'c5-multiway-color-v1', 'representative': representative,
            'residual': residual, 'target': 10, 'tree': proof}
    destination = Path(__file__).resolve().parent / 'certificate.json'
    destination.write_text(json.dumps(data, separators=(',', ':')) + '\n')
    print(json.dumps({'full_orbits': len(full), 'fixed_orbits': len(fixed),
                      'through_point17_orbits': len(ids), 'links': len(links),
                      'representative': representative, 'residual': len(residual),
                      'certificate_nodes': nodes,
                      'certificate_bytes': destination.stat().st_size}, indent=2))


if __name__ == '__main__':
    main()
