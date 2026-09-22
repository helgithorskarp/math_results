"""Exact identification-template and forest checks; no asymptotic inference."""
from collections import Counter
from fractions import Fraction
from hashlib import sha256
from itertools import product
import json


def require(value, message):
    if not value:
        raise ValueError(message)


def edge(a, b):
    return tuple(sorted((a, b)))


def partitions(n, distinct_roots=False):
    def extend(prefix, maximum):
        if len(prefix) == n:
            yield tuple(prefix)
            return
        for label in range(maximum + 2):
            yield from extend(prefix + [label], max(maximum, label))
    yield from extend([0, 1], 1) if distinct_roots else extend([0], 0)


def forest_and_charge(base, endpoints, rows, edges, vertices, virtual=False):
    """Build a tree and check it by disjoint-set cycle detection."""
    root = min(base)
    forest = set() if virtual else {edge(root, a) for a in base - {root}}
    for x in endpoints - base:
        choices = [e for e in edges if x in e and any(a in base for a in e if a != x)]
        require(choices, 'endpoint has no predecessor edge')
        forest.add(min(choices))
    centers = {row['z'] for row in rows if row['type'] != 'E'}
    for z in centers - base - endpoints:
        choices = [e for e in edges if z in e and any(x in endpoints for x in e if x != z)]
        require(choices, 'pure center has no endpoint edge')
        forest.add(min(choices))  # Once per distinct center, including reused centers.
    require(forest <= edges, 'forest uses an unrequired edge')
    augmented = set(forest)
    vertex_set = set(vertices)
    if virtual:
        extra = max(vertex_set) + 1
        augmented |= {edge(extra, a) for a in base}
        vertex_set.add(extra)
    parent = {x: x for x in vertex_set}
    def find(x):
        while parent[x] != x:
            x = parent[x]
        return x
    for a, b in sorted(augmented):
        a, b = find(a), find(b)
        require(a != b, 'constructed forest contains a cycle')
        parent[a] = b
    require(len({find(x) for x in vertex_set}) == 1, 'forest is disconnected')
    require(len(augmented) == len(vertex_set) - 1, 'tree edge count')
    charges = Counter()
    degenerate = 0
    for row in rows:
        ty, z = row['type'], row['z']
        if ty == 'E':
            continue
        x = row['x']
        if ty == 'NT' and x in base:
            degenerate += 1
            continue
        choices = {edge(z, x)}
        if ty == 'NN':
            choices.add(edge(z, row['y']))
        choices -= forest
        require(choices, 'nondegenerate failure has no nonforest edge')
        charges[min(choices)] += 1
    require(not charges or max(charges.values()) <= 4, 'edge received more than four charges')
    return len(edges - forest), degenerate, max(charges.values(), default=0)


def finish(base, endpoints, rows, edges, labels, anchors, first, virtual=False):
    K = len(rows)
    h = sum(row['type'] == 'E' for row in rows)
    t = sum({'E': 0, 'NN': 2, 'NT': 1}[row['type']] for row in rows)
    v, e = len(set(labels)), len(edges)
    s = len(base) - 1 if first else 0
    beta = e - v + (2 if virtual else 1)
    ell = (2 if virtual else 1 + s) + K + t - h - v
    require(beta >= 0 and ell >= 0, 'negative cycle or identification count')
    computed, degenerate, max_charge = forest_and_charge(
        base, endpoints, rows, edges, set(labels), virtual)
    require(computed == beta, 'cycle rank differs from nonforest edge count')
    require(ell >= degenerate, 'degenerate NT role missing from surplus')
    require(K - h <= 4 * beta + ell, 'charging inequality failed')
    for c in (Fraction(15, 32), Fraction(1, 2)):
        if first:
            require(s + t <= 4 * K - 3 * h, 'star role count')
            exponent = Fraction(2 * v - (K + 1) - e, 2) - c * (s + t)
            bound = Fraction(1, 2) + K * (Fraction(15, 8) - 4 * c)
        else:
            require(t <= 2 * (K - h), 'pair role count')
            exponent = Fraction(2 * v - K - e, 2) - c * t
            bound = 2 + K * (Fraction(7, 8) - 2 * c)
        require(exponent <= bound, 'counting exponent exceeds claimed bound')
    return (v, e, s, t, h, beta, ell, degenerate, max_charge)


def star(types, labels):
    require(types and all(t in {'E', 'NN', 'NT'} for t in types), 'invalid role type')
    require(len(labels) == 1 + sum({'E': 1, 'NN': 5, 'NT': 4}[t] for t in types),
            'star label count')
    b, at = labels[0], 1
    base, endpoints, edges, rows = {b}, set(), set(), []
    anchors = Counter({b: 1})
    for ty in types:
        if ty == 'E':
            z = labels[at]
            at += 1
            base.add(z)
            rows.append({'type': ty, 'z': z})
        else:
            a, aa = labels[at:at + 2]
            at += 2
            base |= {a, aa}
            if ty == 'NN':
                x, y, z = labels[at:at + 3]
                at += 3
                row = {'type': ty, 'a': a, 'aa': aa, 'x': x, 'y': y, 'z': z}
            else:
                z, x = labels[at:at + 2]
                at += 2
                row = {'type': ty, 'a': a, 'aa': aa, 'x': x, 'z': z}
            rows.append(row)
        anchors[z] += 1
    if max(anchors.values()) >= 3:
        return None
    edges |= {edge(b, a) for a in base - {b}}
    for row in rows:
        ty, z = row['type'], row['z']
        if ty == 'E':
            continue
        x = row['x']
        if z in base or z == x:
            return None
        if ty == 'NN':
            y = row['y']
            if x == y or z == y:
                return None
            moves = ((row['a'], x), (row['aa'], y))
            edges.add(edge(z, y))
        else:
            moves = ((row['a'], z), (row['aa'], x))
        for a, target in moves:
            if target in base and a != target:
                return None
            endpoints.add(target)
            if a != target:
                edges.add(edge(a, target))
        edges.add(edge(z, x))
    return finish(base, endpoints, rows, edges, labels, anchors, first=True)


def pair(types, labels, predecessor_bits):
    require(types and all(t in {'E', 'NN', 'NT'} for t in types), 'invalid role type')
    require(len(labels) == 2 + sum({'E': 1, 'NN': 3, 'NT': 2}[t] for t in types),
            'pair label count')
    require(labels[0] != labels[1], 'pair roots must be distinct')
    require(len(predecessor_bits) == 2 * sum(t != 'E' for t in types), 'predecessor count')
    require(all(x in (0, 1) for x in predecessor_bits), 'invalid predecessor bit')
    base, roots = set(labels[:2]), labels[:2]
    endpoints, edges, rows, anchors = set(), set(), [], Counter()
    at, bit = 2, 0
    for ty in types:
        if ty == 'E':
            z = labels[at]
            at += 1
            if z not in base:
                return None
            rows.append({'type': ty, 'z': z})
        else:
            if ty == 'NN':
                x, y, z = labels[at:at + 3]
                at += 3
                if x == y or z in (x, y):
                    return None
                targets = (x, y)
                edges.add(edge(z, y))
                row = {'type': ty, 'z': z, 'x': x, 'y': y}
            else:
                z, x = labels[at:at + 2]
                at += 2
                if z == x:
                    return None
                targets = (z, x)
                row = {'type': ty, 'z': z, 'x': x}
            if z in base:
                return None
            for target in targets:
                a = roots[predecessor_bits[bit]]
                bit += 1
                if target in base and a != target:
                    return None
                endpoints.add(target)
                if target != a:
                    edges.add(edge(a, target))
            edges.add(edge(z, x))
            rows.append(row)
        anchors[z] += 1
    if max(anchors.values()) >= 3:
        return None
    return finish(base, endpoints, rows, edges, labels, anchors, first=False, virtual=True)


def run():
    counts = Counter()
    digest = sha256()
    for K in (1, 2):
        for types in product(('E', 'NN', 'NT'), repeat=K):
            size = 1 + sum({'E': 1, 'NN': 5, 'NT': 4}[t] for t in types)
            for labels in partitions(size):
                counts['star_partitions'] += 1
                result = star(types, labels)
                if result is not None:
                    counts['valid_star_templates'] += 1
                    counts['cycle_free_star_templates'] += result[5] == 0
                    counts['degenerate_star_templates'] += result[7] > 0
                    digest.update(json.dumps(['star', types, labels, result],
                                             separators=(',', ':')).encode() + b'\n')
            size = 2 + sum({'E': 1, 'NN': 3, 'NT': 2}[t] for t in types)
            for labels in partitions(size, distinct_roots=True):
                for bits in product((0, 1), repeat=2 * sum(t != 'E' for t in types)):
                    counts['pair_partitions_with_predecessors'] += 1
                    result = pair(types, labels, bits)
                    if result is not None:
                        counts['valid_pair_templates'] += 1
                        counts['cycle_free_pair_templates'] += result[5] == 0
                        counts['degenerate_pair_templates'] += result[7] > 0
                        digest.update(json.dumps(['pair', types, labels, bits, result],
                                                 separators=(',', ':')).encode() + b'\n')
    reused = star(('NN', 'NN'), (0, 0, 0, 0, 1, 2, 0, 0, 1, 3, 2))
    require(reused is not None, 'reused-center control rejected')
    cycle_free = star(('NT',), (0, 0, 0, 1, 0))
    require(cycle_free is not None and cycle_free[5] == 0 and cycle_free[7] == 1,
            'degenerate NT control')
    four = star(('NT',) * 4, (0, 0, 0, 1, 2, 0, 0, 1, 2,
                             0, 0, 2, 1, 0, 0, 2, 1))
    require(four is not None and four[-1] == 4, 'four-charge control')
    rejected = 0
    for action in (lambda: star(('BAD',), (0, 1)),
                   lambda: star(('NN',), (0, 1)),
                   lambda: pair(('E',), (0, 0, 0), ()),
                   lambda: pair(('NT',), (0, 1, 2, 3), (2, 0))):
        try:
            action()
        except ValueError:
            rejected += 1
        else:
            raise ValueError('malformed template accepted')
    return {'counts': dict(sorted(counts.items())), 'records_sha256': digest.hexdigest(),
            'controls': {'reused_center': reused, 'cycle_free_NT': cycle_free,
                         'four_charges_on_one_edge': four}, 'rejections': rejected}
