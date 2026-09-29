"""Independent exact audit of the planar four-menu mass/transversal gap."""

from collections import Counter
from itertools import combinations, combinations_with_replacement, permutations, product


POINTS = tuple(combinations(range(4), 2))
N = len(POINTS)
EDGES = tuple((i, j) for i, j in combinations(range(N), 2) if set(POINTS[i]) & set(POINTS[j]))
EDGE_SET = {frozenset(e) for e in EDGES}


def opposite_pairs():
    return tuple((i, j) for i, j in combinations(range(N), 2) if not set(POINTS[i]) & set(POINTS[j]))


def orient_face(face, xyz):
    a, b, c = (xyz[v] for v in face)
    u = tuple(b[i] - a[i] for i in range(3))
    v = tuple(c[i] - a[i] for i in range(3))
    cross = (u[1] * v[2] - u[2] * v[1], u[2] * v[0] - u[0] * v[2], u[0] * v[1] - u[1] * v[0])
    center = tuple(a[i] + b[i] + c[i] for i in range(3))
    if sum(cross[i] * center[i] for i in range(3)) < 0:
        return face[0], face[2], face[1]
    return face


def check_embedding():
    opposite = opposite_pairs()
    assert len(opposite) == 3
    xyz = {}
    for axis, (plus, minus) in enumerate(opposite):
        p = [0, 0, 0]
        p[axis] = 1
        xyz[plus] = tuple(p)
        p[axis] = -1
        xyz[minus] = tuple(p)
    faces = [orient_face(face, xyz) for face in product(*opposite)]
    assert len(faces) == 8
    darts = Counter((a, b) for x, y, z in faces for a, b in ((x, y), (y, z), (z, x)))
    assert len(darts) == 2 * len(EDGES)
    assert all(darts[u, v] == darts[v, u] == 1 for u, v in EDGES)
    assert N - len(EDGES) + len(faces) == 2
    # The face link of each vertex is one four-cycle.
    for x in range(N):
        nxt = {}
        for face in faces:
            if x in face:
                pos = face.index(x)
                nxt[face[(pos - 1) % 3]] = face[(pos + 1) % 3]
        assert len(nxt) == 4
        start = min(nxt)
        walk = [start]
        for _ in range(4):
            walk.append(nxt[walk[-1]])
        assert walk[-1] == start and len(set(walk[:-1])) == 4
    return len(faces)


def distances():
    adj = [[] for _ in range(N)]
    for u, v in EDGES:
        adj[u].append(v)
        adj[v].append(u)
    result = []
    for source in range(N):
        d = [N + 1] * N
        d[source] = 0
        queue = [source]
        for u in queue:
            for v in adj[u]:
                if d[v] == N + 1:
                    d[v] = d[u] + 1
                    queue.append(v)
        result.append(d)
    return result


def components(deleted):
    remaining = set(range(N)) - set(deleted)
    answer = []
    while remaining:
        seed = min(remaining)
        remaining.remove(seed)
        comp = {seed}
        stack = [seed]
        while stack:
            u = stack.pop()
            for a, b in EDGES:
                v = b if a == u else a if b == u else None
                if v in remaining:
                    remaining.remove(v)
                    comp.add(v)
                    stack.append(v)
        answer.append(frozenset(comp))
    return answer


def all_geodesics():
    d = distances()
    answer = []
    for order in range(1, N + 1):
        for path in permutations(range(N), order):
            if order > 1 and path[0] > path[-1]:
                continue
            if any(frozenset((u, v)) not in EDGE_SET for u, v in zip(path, path[1:])):
                continue
            if order - 1 == d[path[0]][path[-1]]:
                answer.append(path)
    assert len(answer) == 30
    return answer


def check_gap(paths):
    all_pairs = list(combinations_with_replacement(paths, 2))
    assert len(all_pairs) == 465
    # Every pair gets its residual components recomputed from all twelve edges.
    pair_components = {}
    for p, q in all_pairs:
        pair_components[p, q] = components(set(p) | set(q))
    assert len(pair_components) == 465

    cs = []
    menu = []
    for label in range(4):
        c = frozenset(i for i, pair in enumerate(POINTS) if label in pair)
        s = sorted(set(range(N)) - c)
        assert len(c) == len(s) == 3
        p, q = (s[0], s[1]), (s[1], s[2])
        assert p in paths and q in paths
        assert pair_components[p, q] == [c]
        cs.append(c)
        menu.append((p, q))

    assert all(len(a & b) == 1 for a, b in combinations(cs, 2))
    assert all(sum(v in c for c in cs) == 2 for v in range(N))
    assert all(not all(s & c for c in cs) for s in (set(p) | set(q) for p, q in menu))
    tested = 0
    for masses in product(range(3), repeat=N):
        total = sum(masses)
        assert any(2 * sum(masses[v] for v in c) <= total for c in cs)
        tested += 1
    assert tested == 729
    return len(all_pairs), len(menu), tested


if __name__ == "__main__":
    assert N == 6 and len(EDGES) == 12
    faces = check_embedding()
    paths = all_geodesics()
    pair_count, menu_count, mass_count = check_gap(paths)
    print(f"octahedron: vertices={N} edges={len(EDGES)} faces={faces}")
    print(f"all_geodesics={len(paths)} all_pairs={pair_count} prescribed_pairs={menu_count}")
    print(f"sampled_mass_vectors={mass_count} fractional_gap=yes PASS")
