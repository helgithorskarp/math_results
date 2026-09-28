#!/usr/bin/env python3
"""Independent symbolic and finite audits of the annular exchange theorem.

No research modules are imported. One plane fixture places one portal vertex
inside each root-active triangular face and adds pendant active/root leaves.
Another reconstructs the 43-vertex rooted-path obstruction from its ears.
"""

from collections import Counter, deque
from itertools import combinations_with_replacement
from random import Random


def edge(adj, u, v):
    assert u != v
    adj[u].add(v)
    adj[v].add(u)


def components(adj, deleted=()):
    unseen = set(range(len(adj))) - set(deleted)
    result = []
    while unseen:
        start = unseen.pop()
        part = {start}
        todo = [start]
        while todo:
            new = adj[todo.pop()] & unseen
            unseen -= new
            part |= new
            todo.extend(new)
        result.append(part)
    return result


def distances(adj, source):
    values = [-1] * len(adj)
    values[source] = 0
    todo = deque([source])
    while todo:
        u = todo.popleft()
        for v in adj[u]:
            if values[v] < 0:
                values[v] = values[u] + 1
                todo.append(v)
    return values


def core(k):
    adj = [set() for _ in range(2 * k + 1)]
    a = lambda i: 1 + i % k
    c = lambda i: 1 + k + i % k
    for i in range(k):
        for u, v in ((0, a(i)), (a(i), a(i+1)), (a(i), c(i)),
                     (a(i), c(i+1)), (c(i), c(i+1))):
            edge(adj, u, v)
    return adj


def abstract(k):
    adj = core(k)
    labels = {0: None}
    for i in range(k):
        labels[1+i] = None if i == 0 else ('a', i)
        labels[1+k+i] = None if i == 0 else ('c', i)
    for i in range(k):
        sector = len(adj)
        adj.append(set())
        for v in (0, 1+i, 1+(i+1) % k):
            edge(adj, sector, v)
        labels[sector] = ('e', i)
        leaf = len(adj)
        adj.append(set())
        edge(adj, leaf, 1+i)
        labels[leaf] = None if i == 0 else ('a', i)
    root_leaf = len(adj)
    adj.append(set())
    edge(adj, root_leaf, 0)
    labels[root_leaf] = None
    assert len(labels) == len(adj)
    return adj, labels


def sides(k, i):
    atoms = {('e', j) for j in range(k)} | {
        (kind, j) for kind in ('a', 'c') for j in range(1, k)}
    left = {(kind, j) for j in range(i) for kind in ('a', 'c', 'e')} & atoms
    right = atoms - left - {('a', i), ('c', i)}
    return left, right


def symbolic_checks(k):
    adj, labels = abstract(k)
    a = lambda i: 1 + i % k
    c = lambda i: 1 + k + i % k
    first = {0, a(0), c(0)}
    core_vertices = set(range(2*k+1))
    checked = identities = 0

    def check(path, left, right):
        nonlocal checked
        assert len(path) - 1 == distances(adj, path[0])[path[-1]]
        for part in components(adj, first | set(path)):
            if part & core_vertices:
                atoms = {labels[v] for v in part}
                assert None not in atoms and (atoms <= left or atoms <= right), (
                    k, path, part, atoms, left, right)
            else:
                assert len(part) == 1
        checked += 1

    for i in range(k):
        lu, ru = sides(k, i)
        lv, rv = lu | {('c', i)}, ru - {('c', (i+1) % k)}
        check((0, a(i), c(i)), lu, ru)
        check((0, a(i), c(i+1)), lv, rv)
        ln, rn = sides(k, i+1)
        plus_left = lv | {('c', (i+1) % k)}
        minus_right = rn | {('c', (i+1) % k)}
        check((a(i), a(i+1), c(i+2)), plus_left, rn)
        check((a(i+1), a(i), c(i)), lv, minus_right)
        atoms = sides(k, 0)[0] | sides(k, 0)[1]
        coefficients = Counter(v for group in (rv, ln, plus_left, minus_right)
                               for v in group)
        assert all(coefficients[v] == 2-int(v in {('a', i), ('a', (i+1) % k)})
                   for v in atoms)
        identities += 1
    check((0, a(0), c(0)), *sides(k, k))
    return adj, checked, identities


def mass_checks(adj, k, rng):
    a = lambda i: 1 + i % k
    c = lambda i: 1 + k + i % k
    first = {0, a(0), c(0)}
    core_vertices = set(range(2*k+1))
    outside = components(adj, core_vertices)
    assert all(len(part) == 1 for part in outside)
    candidates = []
    for i in range(k):
        candidates.extend(((0,a(i),c(i)), (0,a(i),c(i+1)),
                           (a(i),a(i+1),c(i+2)), (a(i+1),a(i),c(i))))
    checked = 0
    for j in range(90):
        mass = [0 if j == 0 else rng.randrange(6) for _ in adj]
        total = sum(mass)
        dropped = sum(mass[next(iter(part))] for part in outside
                      if not ((set(adj[next(iter(part))]) & core_vertices) - first))
        represented = total - sum(mass[v] for v in first) - dropped
        largest = max((sum(mass[v] for v in part) for part in outside), default=0)
        bound_twice = max(represented, 2*largest)
        assert any(all(2*sum(mass[v] for v in part) <= bound_twice
                       for part in components(adj, first | set(q)))
                   for q in candidates)
        checked += 1
    return checked


def add_cone_gadget(adj, active_left, active_right):
    local = {0: 0, 4: active_left, 5: active_right}
    internal = set()
    for v in range(1, 13):
        if v not in local:
            local[v] = len(adj)
            internal.add(len(adj))
            adj.append(set())
    old_edges = ((1,2), (2,3), (1,3))
    paths = ((1,4,5,6,2), (2,7,8,9,3), (3,10,11,12,1))
    for u, v in old_edges:
        edge(adj, local[u], local[v])
    for path in paths:
        for u, v in zip(path, path[1:]):
            edge(adj, local[u], local[v])
    boundary = (1,4,5,6,2,7,8,9,3,10,11,12)
    for v in boundary:
        edge(adj, 0, local[v])
    return internal


def rooted_fixture():
    adj = core(6)
    pieces = [add_cone_gadget(adj, 1+i, 1+(i+1) % 6) for i in (0,2,4)]
    assert len(adj) == 43 and sorted(map(len, pieces)) == [10,10,10]
    assert {frozenset(c) for c in components(adj, set(range(13)))} == {
        frozenset(part) for part in pieces}
    d = distances(adj, 0)
    paths = [(0,)]
    todo = [(0,)]
    while todo:
        path = todo.pop()
        for v in sorted(adj[path[-1]]):
            if d[v] == len(path):
                new = path + (v,)
                paths.append(new)
                todo.append(new)
    assert len(paths) == len(set(paths)) == 49
    pairs = list(combinations_with_replacement(paths, 2))
    optimum = min(max(map(len, components(adj, set(p) | set(q))), default=0)
                  for p, q in pairs)
    assert len(pairs) == 1225 and optimum == 23
    first, second = (0,1,7), (3,4,11)
    assert len(first)-1 == distances(adj, first[0])[first[-1]]
    assert len(second)-1 == distances(adj, second[0])[second[-1]]
    witness = max(map(len, components(adj, set(first) | set(second))))
    assert witness == 14
    return len(paths), len(pairs), optimum, witness


def main():
    rng = Random(20260928)
    cuts = identities = masses = 0
    for k in range(3, 11):
        adj, current_cuts, current_identities = symbolic_checks(k)
        cuts += current_cuts
        identities += current_identities
        masses += mass_checks(adj, k, rng)
    paths, pairs, optimum, witness = rooted_fixture()
    print(f'abstract_annuli=8 symbolic_cuts={cuts} coefficient_identities={identities} '
          f'exact_mass_assignments={masses} rooted_paths={paths} rooted_pairs={pairs} '
          f'rooted_optimum={optimum} unrooted_witness={witness}')


if __name__ == '__main__':
    main()
