"""Exact finite audits of nonisometric induced-tree terminals."""

from collections import deque
from itertools import combinations


def facial_walks(rotation):
    unseen = {(u, v) for u, row in enumerate(rotation) for v in row}
    faces = []
    while unseen:
        first = min(unseen)
        dart = first
        face = []
        while True:
            assert dart in unseen
            unseen.remove(dart)
            u, v = dart
            face.append(dart)
            order = rotation[v]
            dart = (v, order[(order.index(u) - 1) % len(order)])
            if dart == first:
                break
        faces.append(face)
    return faces


def insert_facial_edge(rotation, a, b):
    face = next((face for face in facial_walks(rotation)
                 if a in {v for _, v in face} and b in {v for _, v in face}), None)
    assert face is not None and b not in rotation[a]
    for vertex, other in ((a, b), (b, a)):
        incoming = next(u for u, v in face if v == vertex)
        rotation[vertex].insert(rotation[vertex].index(incoming), other)


def family(r):
    # The octahedron rotation and parallel 0-a-b-1 insertion follow the
    # published isometric-tree family; the two new leaf-to-guard edges are
    # placed into common facial walks and change its metric conclusion.
    rotation = [[1, 4, 3, 5], [2, 4, 0, 5], [3, 4, 1, 5],
                [0, 4, 2, 5], [0, 1, 2, 3], [0, 3, 2, 1]]
    gadgets = []
    for _ in range(r):
        a, b = len(rotation), len(rotation) + 1
        rotation[0].insert(rotation[0].index(1) + 1, a)
        rotation[1].insert(rotation[1].index(0), b)
        rotation.extend([[0, b], [a, 1]])
        vertices = [a, b]
        leaves = []
        for center in (a, a, b, b):
            previous = center
            for _ in range(2):
                v = len(rotation)
                position = len(rotation[previous]) - 1 if previous == center else len(rotation[previous])
                rotation[previous].insert(position, v)
                rotation.append([previous])
                vertices.append(v)
                previous = v
            leaves.append(previous)
        gadgets.append((vertices, leaves))
    for _, (A, _, B, _) in gadgets:
        insert_facial_edge(rotation, 0, A)
        insert_facial_edge(rotation, 1, B)
    return rotation, gadgets


def adjacency(rotation):
    rows = [set(row) for row in rotation]
    assert all(len(row) == len(rows[u]) and u not in rows[u]
               for u, row in enumerate(rotation))
    assert all(u in rows[v] for v, row in enumerate(rows) for u in row)
    return rows


def edge_set(rows):
    return {frozenset((u, v)) for u, row in enumerate(rows) for v in row if u < v}


def bfs(rows, source):
    dist = [None] * len(rows)
    dist[source] = 0
    todo = deque([source])
    while todo:
        u = todo.popleft()
        for v in rows[u]:
            if dist[v] is None:
                dist[v] = dist[u] + 1
                todo.append(v)
    return dist


def tree_path(rows, start, finish):
    parent = {start: None}
    todo = [start]
    for u in todo:
        if u == finish:
            break
        for v in rows[u]:
            if v not in parent:
                parent[v] = u
                todo.append(v)
    assert finish in parent
    result = [finish]
    while result[-1] != start:
        result.append(parent[result[-1]])
    result.reverse()
    return result


def components(rows, subset):
    unseen = set(subset)
    result = []
    while unseen:
        root = min(unseen)
        unseen.remove(root)
        comp = {root}
        todo = [root]
        while todo:
            u = todo.pop()
            for v in rows[u] & unseen:
                unseen.remove(v)
                comp.add(v)
                todo.append(v)
        result.append(comp)
    return result


def audit_family(r):
    rotation, gadgets = family(r)
    rows = adjacency(rotation)
    n = len(rows)
    edges = edge_set(rows)
    faces = facial_walks(rotation)
    assert (n, len(edges), len(faces)) == (6 + 10 * r, 12 + 13 * r, 8 + 3 * r)
    assert n - len(edges) + len(faces) == 2
    assert sum(map(len, faces)) == 2 * len(edges)
    assert len(components(rows, range(n))) == 1
    residuals = components(rows, range(4, n))
    assert {frozenset(c) for c in residuals} == (
        {frozenset((4,)), frozenset((5,))} |
        {frozenset(vertices) for vertices, _ in gadgets})
    for vertices, (A, Aprime, B, Bprime) in gadgets:
        tree = set(vertices)
        internal = [row & tree if u in tree else set() for u, row in enumerate(rows)]
        assert len(tree) == 10
        assert len(edge_set(internal)) == 9
        assert len(components(internal, tree)) == 1
        assert sum(len(internal[u]) == 1 for u in tree) == 4
        first = tree_path(internal, A, Aprime)
        second = tree_path(internal, B, Bprime)
        assert set(first) | set(second) == tree
        assert len(first) == len(second) == 5
        assert bfs(rows, A)[Aprime] == 4
        assert bfs(rows, B)[Bprime] == 4
        assert bfs(internal, A)[B] == 5 and bfs(rows, A)[B] == 3
        # This is an exact pair search in the intact finite gadget; it
        # does not assume the displayed pairing in advance.
        eligible = []
        for u in tree:
            dist = bfs(rows, u)
            for v in tree:
                if u <= v:
                    path = tree_path(internal, u, v)
                    if len(path) - 1 == dist[v]:
                        eligible.append(set(path))
        assert any(p | q == tree for p, q in combinations(eligible, 2))
    return n, len(edges), len(faces), rotation, gadgets


def audit_profiles(rotation, gadgets):
    assert len(gadgets) == 1
    vertices, (A, Aprime, B, Bprime) = gadgets[0]
    rows = adjacency(rotation)
    tree = set(vertices)
    internal = [row & tree if u in tree else set() for u, row in enumerate(rows)]
    first = tree_path(internal, A, Aprime)
    second = tree_path(internal, B, Bprime)
    mutable = edge_set(internal) | {
        frozenset((0, vertices[0])), frozenset((1, vertices[1])),
        frozenset((0, A)), frozenset((1, B)),
    }
    assert len(mutable) == 13
    fixed = edge_set(rows) - mutable
    mutable = sorted(mutable, key=lambda e: tuple(sorted(e)))
    checked_components = 0
    for mask in range(1 << len(mutable)):
        chosen = fixed | {e for i, e in enumerate(mutable) if mask & (1 << i)}
        subrows = [set() for _ in rows]
        for edge in chosen:
            u, v = tuple(edge)
            subrows[u].add(v)
            subrows[v].add(u)
        for component in components(subrows, tree):
            checked_components += 1
            pieces = []
            for path in (first, second):
                indices = [i for i, u in enumerate(path) if u in component]
                if not indices:
                    continue
                assert indices == list(range(indices[0], indices[-1] + 1))
                piece = path[indices[0]:indices[-1] + 1]
                assert all(v in subrows[u] for u, v in zip(piece, piece[1:]))
                assert bfs(subrows, piece[0])[piece[-1]] == len(piece) - 1
                pieces.append(set(piece))
            assert set().union(*pieces) == component
    return 1 << len(mutable), checked_components


def main():
    for r in (1, 2, 5):
        n, m, f, rotation, gadgets = audit_family(r)
        print(f"gadgets={r} vertices={n} edges={m} faces={f} "
              "planar=YES nonisometric=YES cover=YES")
        if r == 1:
            profiles, checked = audit_profiles(rotation, gadgets)
            print(f"deletion_profiles={profiles} checked_components={checked} PASS")
    print("PASS")


if __name__ == "__main__":
    main()
