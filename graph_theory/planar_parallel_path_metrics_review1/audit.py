"""Independent audit of the 20-vertex parallel-path metric controls.

Run from the repository root with Python 3.11 or later. No target imports.
"""

from collections import deque
from hashlib import sha256
from itertools import combinations
from heapq import heappop, heappush


def edge(u, v):
    return tuple(sorted((u, v)))


def vertices(i, j):
    return 2 + (i % 6) * 3 + j


def topology():
    edges = set()
    for i in range(6):
        column = [0] + [vertices(i, j) for j in range(3)] + [1]
        edges.update(edge(u, v) for u, v in zip(column, column[1:]))
        for j in range(3):
            edges.add(edge(vertices(i, j), vertices(i + 1, j)))
            if j < 2:
                if (i + j) % 2 == 0:
                    edges.add(edge(vertices(i, j), vertices(i + 1, j + 1)))
                else:
                    edges.add(edge(vertices(i + 1, j), vertices(i, j + 1)))
    assert len(edges) == 54
    return edges


def graph(cost):
    adj = [[] for _ in range(20)]
    for (u, v), length in cost.items():
        assert length > 0
        adj[u].append((v, length))
        adj[v].append((u, length))
    return adj


def distance_matrix(cost):
    adj = graph(cost)
    output = []
    for start in range(20):
        d = [10**12] * 20
        d[start] = 0
        heap = [(0, start)]
        while heap:
            dist, u = heappop(heap)
            if dist != d[u]:
                continue
            for v, length in adj[u]:
                if dist + length < d[v]:
                    d[v] = dist + length
                    heappush(heap, (d[v], v))
        output.append(d)
    return output


def components(cost, removed):
    adj = graph(cost)
    unseen = set(range(20)) - set(removed)
    result = []
    while unseen:
        start = unseen.pop()
        part = {start}
        queue = deque([start])
        while queue:
            u = queue.popleft()
            for v, _ in adj[u]:
                if v in unseen:
                    unseen.remove(v)
                    part.add(v)
                    queue.append(v)
        result.append(part)
    return result


def check_shortest(path, cost, distances):
    assert len(path) == len(set(path))
    assert sum(cost[edge(u, v)] for u, v in zip(path, path[1:])) == distances[path[0]][path[-1]]


def score(cut, cost, mass):
    return max((sum(mass[v] for v in part) for part in components(cost, cut)), default=0)


def branch_cover(p, q, cost):
    halves = []
    for branch in (p, q):
        coords = [0]
        for u, v in zip(branch, branch[1:]):
            coords.append(coords[-1] + cost[edge(u, v)])
        total = coords[-1]
        left = max(i for i, x in enumerate(coords) if 2 * x <= total)
        right = min(i for i, x in enumerate(coords) if 2 * x >= total)
        halves.append((branch[:left + 1], branch[right:]))
    (p_left, p_right), (q_left, q_right) = halves
    return (tuple(reversed(p_left)) + tuple(q_left[1:]),
            tuple(p_right) + tuple(reversed(q_right))[1:])


def digest_number(*items):
    return int.from_bytes(sha256(':'.join(map(str, items)).encode()).digest()[:8], 'big')


def longitudinal_metric(edges):
    branches = [tuple([0] + [vertices(i, j) for j in range(3)] + [1])
                for i in range(6)]
    core = {}
    for p in branches:
        for u, v in zip(p, p[1:]):
            core[edge(u, v)] = 1 + digest_number('price', 6, 3, 1, u, v) % 31
    dh = distance_matrix(core)
    cost = dict(core)
    for i in range(6):
        for j in range(3):
            x, y = vertices(i, j), vertices(i + 1, j)
            cost[edge(x, y)] = dh[x][y] + digest_number('slack', 1, x, y) % 5
            if j < 2:
                x, y = ((vertices(i, j), vertices(i + 1, j + 1))
                        if (i + j) % 2 == 0 else
                        (vertices(i + 1, j), vertices(i, j + 1)))
                cost[edge(x, y)] = dh[x][y] + digest_number('slack', 1, x, y) % 5
    assert set(cost) == edges
    dg = distance_matrix(cost)
    assert dg == dh
    return cost, dg, branches


def main():
    edges = topology()
    marked = {3, 5, 7, 9, 11, 13, 15, 17, 19}
    cheap_pairs = ((0, 2), (0, 8), (0, 14), (1, 4), (1, 10), (1, 16),
                   (2, 5), (2, 6), (3, 18), (4, 7), (4, 18),
                   (6, 9), (6, 10), (8, 11), (8, 12), (10, 13),
                   (12, 15), (12, 16), (14, 17), (14, 18), (16, 19))
    cheap = {edge(*x) for x in cheap_pairs}
    assert cheap <= edges
    cost = {e: (1 if e in cheap else 22) for e in edges}
    d = distance_matrix(cost)
    helical = ((0, 2, 6, 10, 1), (0, 8, 12, 16, 1), (0, 14, 18, 4, 1))
    mass = [int(v in marked) for v in range(20)]
    for i, j in combinations(range(3), 2):
        assert score(set(helical[i]) | set(helical[j]), cost, mass) == 6
    witness = ((3, 18, 4, 1, 10, 6, 9),
               (3, 18, 4, 1, 16, 12, 15))
    for path in witness:
        check_shortest(path, cost, d)
    assert score(set(witness[0]) | set(witness[1]), cost, mass) == 3
    cuts = 0
    for cut in combinations(range(20), 4):
        assert score(cut, cost, mass) >= 5
        cuts += 1
    assert cuts == 4845

    longitudinal, dg, branches = longitudinal_metric(edges)
    all_mass = [1] * 20
    covers = 0
    for i, j in combinations(range(6), 2):
        paths = branch_cover(branches[i], branches[j], longitudinal)
        assert set(paths[0]) | set(paths[1]) == set(branches[i]) | set(branches[j])
        for p in paths:
            check_shortest(p, longitudinal, dg)
        covers += 1
    intervals = [[{v for v in range(20) if dg[s][v] + dg[v][t] == dg[s][t]}
                  for t in range(20)] for s in range(20)]
    triangles = [tri for tri in combinations(range(20), 3)
                 if all(edge(u, v) in edges for u, v in combinations(tri, 2))]
    assert len(triangles) == 36
    max_interval = max(len(x) for row in intervals for x in row)
    max_facial = max(len(set().union(*(intervals[s][v] for v in tri)))
                     for s in range(20) for tri in triangles)
    assert (max_interval, max_facial) == (12, 17)
    scope_witness = ((3, 2, 0, 8), (4, 1, 10, 9))
    for p in scope_witness:
        check_shortest(p, longitudinal, dg)
    assert score(set(scope_witness[0]) | set(scope_witness[1]), longitudinal, all_mass) == 9
    # The cyclic-median proof actually allows any branch to be fixed first.
    for fixed in range(6):
        order = [(fixed + k) % 6 for k in range(1, 6)]
        weights = [((3 * i + fixed) % 7) + 1 for i in range(6)]
        outside = sum(weights[i] for i in order)
        running = 0
        for other in order:
            running += weights[other]
            if 2 * running >= outside:
                break
        vertex_mass = [0, 0] + [weights[i] for i in range(6) for _ in range(3)]
        paths = branch_cover(branches[fixed], branches[other], longitudinal)
        for p in paths:
            check_shortest(p, longitudinal, dg)
        assert 2 * score(set(paths[0]) | set(paths[1]), longitudinal, vertex_mass) <= 3 * outside
    print('control: branch_pairs=3 max_remaining=6 four_cuts=4845 positive_max=3')
    print(f'longitudinal: covers={covers} triangles={len(triangles)} '
          f'max_interval={max_interval} max_facial_union={max_facial} '
          'uniform_separator_max=9')


if __name__ == '__main__':
    main()
