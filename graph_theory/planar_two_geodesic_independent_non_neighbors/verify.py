#!/usr/bin/env python3
"""Exact checks of explicit decomposition certificates; not a graph census."""
from collections import defaultdict, deque
from hashlib import sha256
from itertools import combinations
from pathlib import Path
import argparse
import json


def edge(a, b):
    return tuple(sorted((a, b)))


def boundary(face):
    return [edge(a, b) for a, b in zip(face, face[1:] + face[:1])]


def dissect(m, rounds):
    faces = [list(range(1, m + 1))]
    for step in range(rounds):
        candidates = [i for i, f in enumerate(faces) if len(f) >= 4]
        if not candidates:
            break
        i = candidates[step % len(candidates)]
        f = faces.pop(i)
        shift = step % len(f)
        f = f[shift:] + f[:shift]
        k = 2 + step % (len(f) - 3)
        faces.extend([f[:k + 1], [f[0]] + f[k:]])
    return faces


def polygon_fixture(m, rounds, variant):
    faces = dissect(m, rounds)
    base_edges = set(e for f in faces for e in boundary(f))
    actual = set(base_edges)
    if variant == 3:
        actual = set()
    elif variant % 2:
        actual = {e for e in actual if (e[0] + 3 * e[1]) % 3 == 0}
    actual.update((0, v) for v in range(1, m + 1))
    next_vertex = m + 1
    centers = {}
    for i, f in enumerate(faces):
        if variant != 2 or i % 2 == 0:
            centers[i] = next_vertex
            actual.update(edge(next_vertex, v) for v in f)
            next_vertex += 1
    triangles, bags = [], []
    for i, f in enumerate(faces):
        for j in range(1, len(f) - 1):
            tri = frozenset((f[0], f[j], f[j + 1]))
            triangles.append(tri)
            bags.append(set(tri) | {0} | ({centers[i]} if i in centers else set()))
    owners = defaultdict(list)
    for i, tri in enumerate(triangles):
        for e in combinations(sorted(tri), 2):
            owners[e].append(i)
    tree = [(v[0], v[1]) for v in owners.values() if len(v) == 2]
    if variant:
        for a, b in sorted(base_edges)[::max(1, len(base_edges) // 4)]:
            for _ in range(2):
                x = next_vertex
                next_vertex += 1
                actual.update([edge(x, a), edge(x, b)])
                parent = owners[edge(a, b)][0]
                tree.append((parent, len(bags)))
                bags.append({0, x, a, b})
        x = next_vertex
        next_vertex += 1
        actual.add(edge(x, 1))
        parent = next(i for i, tri in enumerate(triangles) if 1 in tri)
        tree.append((parent, len(bags)))
        bags.append({0, x, 1})
    # A separate geometric consistency check of the polygon input.
    diagonals = base_edges - set(boundary(list(range(1, m + 1))))
    assert all(not (a < c < b < d or c < a < d < b)
               for (a, b), (c, d) in combinations(diagonals, 2))
    counts = defaultdict(int)
    for f in faces:
        for e in boundary(f):
            counts[e] += 1
    assert all(counts[e] == (2 if e in diagonals else 1) for e in base_edges)
    assert len(faces) == len(diagonals) + 1
    return {
        'name': f'polygon_{m}_{rounds}_{variant}',
        'n': next_vertex, 'edges': sorted(actual), 'root': 0,
        'bags': bags, 'tree': tree,
    }


def small_fixture(b):
    # Several independent centers with repeated neighborhoods, |N(root)|<=2.
    edges = {(0, v) for v in range(1, b + 1)}
    bags = [{0} | set(range(1, b + 1))]
    tree = []
    n = b + 1
    if b:
        for neighbors in [[1], list(range(1, b + 1))] * 3:
            edges.update(edge(n, v) for v in neighbors)
            tree.append((0, len(bags)))
            bags.append({0, n} | set(neighbors))
            n += 1
    return {'name': f'small_{b}', 'n': n, 'edges': sorted(edges), 'root': 0,
            'bags': bags, 'tree': tree}


def dominating_edge_fixture(m):
    # Start with a cone over a maximal outerplanar polygon. Insert vertex s
    # into face (root,1,2), then delete root-1 and root-2. Planarity is preserved.
    faces = dissect(m, m - 3)
    assert all(len(f) == 3 for f in faces)
    es = {e for f in faces for e in boundary(f)}
    es.update((0, v) for v in range(3, m + 1))
    s = m + 1
    es.update({(0, s), (1, s), (2, s)})
    owners = defaultdict(list)
    for i, f in enumerate(faces):
        for e in boundary(f):
            owners[e].append(i)
    tree = [(x[0], x[1]) for x in owners.values() if len(x) == 2]
    return {'name': f'dominating_edge_{m}', 'n': m + 2, 'edges': sorted(es),
            'root': 0, 'dominating_edge': [0, s],
            'bags': [set(f) | {0, s} for f in faces], 'tree': tree}


def adjacency(n, edges):
    adj = [set() for _ in range(n)]
    for a, b in edges:
        assert 0 <= a < b < n
        adj[a].add(b)
        adj[b].add(a)
    return adj


def bfs_path(adj, start, end):
    prev = {start: None}
    queue = deque([start])
    while end not in prev:
        v = queue.popleft()
        for w in sorted(adj[v]):
            if w not in prev:
                prev[w] = v
                queue.append(w)
    path = [end]
    while path[-1] != start:
        path.append(prev[path[-1]])
    return list(reversed(path))


def cover(adj, root, bag):
    if len(bag) == 5:
        outsiders = [x for x in bag if x != root and x not in adj[root]]
        if len(outsiders) == 1:
            x = outsiders[0]
            a, b, c = sorted(bag - {root, x})
            if {a, b, c} <= adj[root] & adj[x]:
                return [[root, a, x], [b, c] if c in adj[b] else [b, root, c]]
        for middle in sorted(bag):
            for a, b in combinations(sorted(bag & adj[middle]), 2):
                if b not in adj[a]:
                    c, d = sorted(bag - {a, middle, b})
                    return [[a, middle, b], bfs_path(adj, c, d)]
        raise AssertionError('Five-vertex bag has no induced P3')
    assert len(bag) <= 4
    vs = sorted(bag)
    return [bfs_path(adj, vs[i], vs[min(i + 1, len(vs) - 1)])
            for i in range(0, len(vs), 2)]


def distances(n, edges):
    # Independent of the witness constructor's BFS.
    d = [[n + 1] * n for _ in range(n)]
    for v in range(n):
        d[v][v] = 0
    for a, b in edges:
        d[a][b] = d[b][a] = 1
    for k in range(n):
        for i in range(n):
            for j in range(n):
                d[i][j] = min(d[i][j], d[i][k] + d[k][j])
    return d


def check_paths(paths, adj, dist, required):
    assert len(paths) <= 2
    deleted = set()
    for p in paths:
        assert p and len(p) == len(set(p))
        assert all(b in adj[a] for a, b in zip(p, p[1:]))
        assert len(p) - 1 == dist[p[0]][p[-1]]
        deleted.update(p)
    assert required <= deleted
    return deleted


def components(n, edges, removed):
    # Union-find rather than the tree traversal used to select a centroid.
    parent = list(range(n))
    def find(v):
        while parent[v] != v:
            parent[v] = parent[parent[v]]
            v = parent[v]
        return v
    for a, b in edges:
        if a not in removed and b not in removed:
            parent[find(a)] = find(b)
    groups = defaultdict(set)
    for v in range(n):
        if v not in removed:
            groups[find(v)].add(v)
    return list(groups.values())


def check_decomposition(n, edges, bags, tree):
    t = len(bags)
    assert t >= 1 and len(tree) == t - 1
    assert len(components(t, tree, set())) == 1
    assert set.union(*bags) == set(range(n))
    for a, b in edges:
        assert any({a, b} <= bag for bag in bags)
    for v in range(n):
        occurrences = {i for i, bag in enumerate(bags) if v in bag}
        internal = sum(a in occurrences and b in occurrences for a, b in tree)
        assert internal == len(occurrences) - 1


def choose_centroid(bags, tree, masses):
    loads = [0] * len(bags)
    for v, mass in enumerate(masses):
        loads[next(i for i, bag in enumerate(bags) if v in bag)] += mass
    adj = adjacency(len(bags), [edge(a, b) for a, b in tree])
    total = sum(masses)
    for center in range(len(bags)):
        seen = {center}
        largest = 0
        for start in sorted(adj[center]):
            if start in seen:
                continue
            stack, weight = [start], 0
            seen.add(start)
            while stack:
                v = stack.pop()
                weight += loads[v]
                for w in adj[v] - seen:
                    seen.add(w)
                    stack.append(w)
            largest = max(largest, weight)
        if 2 * largest <= total:
            return center
    raise AssertionError('No centroid')


def mass_vectors(n):
    yield [0] * n
    yield [1] * n
    yield [(v * v + 3 * v + 1) % 11 for v in range(n)]
    yield [int(v % 3 == 0) * 13 for v in range(n)]
    for heavy in range(n):
        yield [int(v == heavy) for v in range(n)]


def rejected(call):
    try:
        call()
    except AssertionError:
        return True
    return False


def run():
    fixtures = [small_fixture(b) for b in range(3)]
    fixtures.extend(polygon_fixture(m, rounds, variant)
                    for m in [3, 4, 5, 8, 12, 20, 31]
                    for rounds in sorted({0, max(0, m // 3), max(0, m - 3)})
                    for variant in range(4))
    fixtures.extend(dominating_edge_fixture(m) for m in [12, 20])
    records, witness_digest = [], sha256()
    totals = {'bags': 0, 'five_vertex_bags': 0, 'mass_assignments': 0}
    for f in fixtures:
        n, es, r, bags, tree = (f[k] for k in ['n', 'edges', 'root', 'bags', 'tree'])
        adj = adjacency(n, es)
        if 'dominating_edge' in f:
            u, v = f['dominating_edge']
            assert v in adj[u] and adj[u] | adj[v] == set(range(n))
            assert all(len(neighbors) < n - 1 for neighbors in adj)
        else:
            outside = set(range(n)) - adj[r] - {r}
            assert all(b not in outside for a in outside for b in adj[a])
        check_decomposition(n, es, bags, tree)
        d = distances(n, es)
        covers = [cover(adj, r, bag) for bag in bags]
        for bag, paths in zip(bags, covers):
            check_paths(paths, adj, d, bag)
        assignments = 0
        for masses in mass_vectors(n):
            center = choose_centroid(bags, tree, masses)
            deleted = check_paths(covers[center], adj, d, bags[center])
            remaining = components(n, es, deleted)
            assert all(2 * sum(masses[v] for v in comp) <= sum(masses)
                       for comp in remaining)
            witness_digest.update(json.dumps([f['name'], masses, center,
                                             covers[center]], separators=(',', ':')).encode())
            assignments += 1
        fives = sum(len(bag) == 5 for bag in bags)
        totals['bags'] += len(bags)
        totals['five_vertex_bags'] += fives
        totals['mass_assignments'] += assignments
        records.append({'fixture': f['name'], 'n': n, 'edges': len(es),
                        'bags': len(bags), 'five_vertex_bags': fives,
                        'mass_assignments': assignments})
    # A fill chord is not automatically an edge of the original graph.
    bipyramid = polygon_fixture(5, 0, 0)
    adj = adjacency(bipyramid['n'], bipyramid['edges'])
    d = distances(bipyramid['n'], bipyramid['edges'])
    controls = {
        'reject_missing_original_edge': rejected(lambda: check_paths([[1, 3]], adj, d, {1, 3})),
        'reject_nonshortest_original_walk': rejected(lambda: check_paths([[1, 2, 3, 4]], adj, d, {1, 4})),
        'reject_uncovered_vertex': rejected(lambda: check_paths([[0, 1]], adj, d, {0, 1, 2})),
        'reject_missing_decomposition_edge': rejected(lambda: check_decomposition(
            3, [(0, 1), (1, 2)], [{0, 1}, {0, 2}], [(0, 1)])),
        'reject_disconnected_occurrences': rejected(lambda: check_decomposition(
            3, [(0, 1), (1, 2)], [{0, 1}, {1, 2}, {0, 2}], [(0, 1), (1, 2)])),
    }
    assert all(controls.values())
    # Disconnected extension: isolated heavy/light vertices and zero masses.
    disconnected_checks = 0
    for masses in [[1, 1, 1, 1, 20], [5, 0, 2, 1, 1], [0] * 5, [1] * 5]:
        es = [(0, 1), (0, 2)]
        total = sum(masses)
        if any(2 * masses[v] > total for v in [3, 4]):
            deleted = {next(v for v in [3, 4] if 2 * masses[v] > total)}
        else:
            deleted = {0, 1, 2}  # The ambient geodesic 1-0-2.
        assert all(2 * sum(masses[v] for v in comp) <= total
                   for comp in components(5, es, deleted))
        disconnected_checks += 1
    return {'status': 'PASS', 'fixtures': len(fixtures), **totals,
            'disconnected_mass_checks': disconnected_checks,
            'invalid_controls_rejected': controls,
            'witness_digest_sha256': witness_digest.hexdigest(), 'records': records}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    result = run()
    if args.check:
        expected = json.loads(Path(__file__).with_name('expected.json').read_text())
        assert result == expected, 'Output differs from expected.json'
        print('PASS:', result['fixtures'], 'fixtures;', result['bags'], 'bag covers;',
              result['mass_assignments'], 'mass assignments; 5 invalid controls rejected')
    else:
        print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
