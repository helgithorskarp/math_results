#!/usr/bin/env python3
"""Independent bounded word audit and exhaustive fixed-spoke control check."""

from collections import Counter, deque
from itertools import combinations, product
import json
from pathlib import Path


CONTROL = Path(__file__).resolve().parents[1] / "planar_two_geodesic_selected_spoke_annuli" / "control.json"


def admissible(word):
    k = word.count("A") + word.count("D")
    m = word.count("C") + word.count("D")
    if min(k, m) < 3:
        return False
    for symbol, cap in (("A", k - 2), ("C", m - 2)):
        for q in range(len(word)):
            if word[q] != symbol or word[q - 1] == symbol:
                continue
            run = 0
            while run < len(word) and word[(q + run) % len(word)] == symbol:
                run += 1
            if run > cap:
                return False
    return True


def annulus(word):
    k = word.count("A") + word.count("D")
    m = word.count("C") + word.count("D")
    i = j = 0
    states = []
    cross = set()
    for ch in word:
        states.append((i, j))
        cross.add((i, j))
        if ch in "AD":
            i = (i + 1) % k
        if ch in "CD":
            j = (j + 1) % m
    assert (i, j) == (0, 0)
    assert len(cross) == len(word)
    adj = [set() for _ in range(1 + k + m)]
    def edge(a, b):
        adj[a].add(b)
        adj[b].add(a)
    for a in range(k):
        edge(0, 1 + a)
        edge(1 + a, 1 + (a + 1) % k)
    for c in range(m):
        edge(1 + k + c, 1 + k + (c + 1) % m)
    for a, c in cross:
        edge(1 + a, 1 + k + c)
    return k, m, states, cross, adj


def bfs_distance(adj, s, t):
    distance = [-1] * len(adj)
    distance[s] = 0
    queue = deque([s])
    while queue:
        u = queue.popleft()
        if u == t:
            return distance[u]
        for v in adj[u]:
            if distance[v] < 0:
                distance[v] = distance[u] + 1
                queue.append(v)
    return None


def word_audit():
    count = Counter()
    for n in range(6, 11):
        for letters in product("ACD", repeat=n):
            word = "".join(letters)
            if not admissible(word):
                continue
            k, m, states, cross, adj = annulus(word)
            count["words"] += 1
            dad = []
            for q, ch in enumerate(word):
                a, c = states[q]
                if ch == "D":
                    assert (a, (c + 1) % m) not in cross
                    assert ((a + 1) % k, c) not in cross
                    count["D"] += 1
                if ch == "A" and word[q - 1] != "A" and word[(q + 1) % n] != "A":
                    if word[(q + 1) % n] == "C":
                        assert (a, (c + 1) % m) not in cross
                    if word[q - 1] == "C":
                        assert ((a + 1) % k, (c - 1) % m) not in cross
                if ch == "A" and word[q - 1] == word[(q + 1) % n] == "D":
                    dad.append(q)
                    assert {x for x, y in cross if y == c} == {a, (a + 1) % k}
                    assert {y for x, y in cross if x == a} == {c}
                    assert {y for x, y in cross if x == (a + 1) % k} == {c}
            for anchor in dad:
                rotated = word[anchor:] + word[:anchor]
                _, _, shifted, _, shifted_adj = annulus(rotated)
                assert shifted[0] == (0, 0)
                for q, ch in enumerate(rotated):
                    if ch != "A" or rotated[q - 1] != "D" or rotated[(q + 1) % n] != "D":
                        continue
                    a, c = shifted[q]
                    if c == 0:
                        continue
                    if c == 1:
                        assert a == 2
                    elif c == m - 1:
                        assert a == k - 2
                    else:
                        assert bfs_distance(shifted_adj, 2, 1 + k + c) == 3
                        count["far_DAD"] += 1
                    count["ordered_DAD_pairs"] += 1
    assert count["words"] > 0 and count["far_DAD"] > 0
    return count


def control_graph(data):
    assert data["block_sizes"] == [2] * 5
    adj = [set() for _ in range(16)]
    faces = []
    def edge(a, b):
        adj[a].add(b)
        adj[b].add(a)
    outer = list(range(1, 11))
    inner = list(range(11, 16))
    for j, a in enumerate(outer):
        b = outer[(j + 1) % 10]
        edge(0, a)
        edge(a, b)
        faces.append((0, a, b))
    for j, c in enumerate(inner):
        a, b = outer[2 * j:2 * j + 2]
        d = inner[(j + 1) % 5]
        nxt = outer[(2 * j + 2) % 10]
        edge(c, d)
        edge(a, c)
        edge(b, c)
        faces.extend(((a, c, b), (b, c, d, nxt)))
    faces.append(tuple(inner))
    assert len(faces) == 21
    for triple in data["stack_faces"]:
        matches = [f for f in faces if len(f) == 3 and set(f) == set(triple)]
        assert len(matches) == 1
        faces.remove(matches[0])
        z = len(adj)
        adj.append(set())
        for a in triple:
            edge(z, a)
        faces.extend(((z, triple[0], triple[1]),
                      (z, triple[1], triple[2]),
                      (z, triple[2], triple[0])))
    face_edges = Counter(tuple(sorted((f[q], f[(q + 1) % len(f)])))
                         for f in faces for q in range(len(f)))
    graph_edges = {tuple(sorted((a, b))) for a, ns in enumerate(adj) for b in ns}
    assert set(face_edges) == graph_edges
    assert all(v == 2 for v in face_edges.values())
    assert len(adj) == 52 and len(graph_edges) == 143 and len(faces) == 93
    assert len(adj) - len(graph_edges) + len(faces) == 2
    return adj


def geodesic_masks(adj):
    n = len(adj)
    all_masks = set()
    distances = []
    for s in range(n):
        d = [-1] * n
        d[s] = 0
        queue = deque([s])
        while queue:
            u = queue.popleft()
            for v in adj[u]:
                if d[v] < 0:
                    d[v] = d[u] + 1
                    queue.append(v)
        assert all(x >= 0 for x in d)
        distances.append(d)
        paths = [set() for _ in range(n)]
        paths[s].add(1 << s)
        for u in sorted(range(n), key=lambda v: d[v]):
            for v in adj[u]:
                if d[v] == d[u] + 1:
                    paths[v].update(mask | 1 << v for mask in paths[u])
        for t in range(s, n):
            all_masks.update(paths[t])
    return distances, all_masks


def max_residual_mass(adj, masses, removed):
    remaining = set(range(len(adj))) - removed
    maximum = 0
    while remaining:
        seed = remaining.pop()
        todo = [seed]
        mass = masses[seed]
        while todo:
            u = todo.pop()
            new = adj[u] & remaining
            remaining.difference_update(new)
            todo.extend(new)
            mass += sum(masses[v] for v in new)
        maximum = max(maximum, mass)
    return maximum


def control_audit():
    data = json.loads(CONTROL.read_text())
    adj = control_graph(data)
    n = len(adj)
    masses = [0] * n
    for v, w in data["positive_weights"]:
        assert masses[v] == 0 and w > 0
        masses[v] = w
    assert sum(masses) == 37 and all(masses[v] == 0 for v in range(16))
    d, masks = geodesic_masks(adj)
    core_adj = [adj[v] & set(range(16)) for v in range(16)]
    for s in range(16):
        for t in range(16):
            assert bfs_distance(core_adj, s, t) == d[s][t]
    def path_set(path):
        assert len(set(path)) == len(path)
        assert all(v in adj[u] for u, v in zip(path, path[1:]))
        assert len(path) - 1 == d[path[0]][path[-1]]
        return set(path)
    fixed = path_set(data["prescribed_path"])
    assert len(masks) == 3489
    optimum = min(max_residual_mass(adj, masses,
                                    fixed | {v for v in range(n) if mask >> v & 1})
                  for mask in masks)
    free = set().union(*(path_set(p) for p in data["free_paths"]))
    assert optimum == 19 and max_residual_mass(adj, masses, free) == 14
    assert max_residual_mass(adj, masses,
                             fixed | path_set((10, 9, 8, 34))) == 19
    # Derive aggregate DAD-sector masses from the literal outside components.
    unseen = set(range(16, n))
    sector_mass = {}
    while unseen:
        seed = unseen.pop()
        part = {seed}
        todo = [seed]
        while todo:
            u = todo.pop()
            new = (adj[u] & set(range(16, n))) & unseen
            unseen.difference_update(new)
            part.update(new)
            todo.extend(new)
        boundary = set().union(*(adj[v] for v in part)) - part
        assert len(part) == 12 and 0 in boundary and len(boundary) == 3
        kept = part | boundary
        for z in sorted(part, reverse=True):
            later = adj[z] & kept
            assert len(later) <= 3
            assert all(y in adj[x] for x, y in combinations(later, 2))
            kept.remove(z)
        a, b = sorted(boundary - {0})
        assert b == a + 1 and a % 2 == 1
        sector_mass[(a - 1) // 2] = sum(masses[v] for v in part)
    assert sorted(sector_mass.values()) == [9, 14, 14]
    selected_optima = []
    for j, mass in sector_mass.items():
        if mass != max(sector_mass.values()):
            continue
        spoke = path_set((0, 1 + 2 * j, 11 + j))
        best = min(max_residual_mass(adj, masses,
                                     spoke | {v for v in range(n) if mask >> v & 1})
                   for mask in masks)
        assert 2 * best <= sum(masses)
        selected_optima.append(best)
    assert len(selected_optima) == 2
    return len(masks), optimum, sorted(selected_optima)


def main():
    c = word_audit()
    masks, optimum, selected = control_audit()
    print(f"words={c['words']} D_steps={c['D']} ordered_DAD_pairs={c['ordered_DAD_pairs']} "
          f"far_DAD={c['far_DAD']} control_geodesic_sets={masks} "
          f"fixed_optimum={optimum} selected_optima={selected} free_largest=14 PASS")


if __name__ == "__main__":
    main()
