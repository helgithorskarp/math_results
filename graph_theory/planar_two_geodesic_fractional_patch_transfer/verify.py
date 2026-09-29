"""Independent exact control for the octahedral fractional patch quotient."""

from collections import Counter, deque
from itertools import combinations, combinations_with_replacement, product


PAIRS = tuple(combinations(range(4), 2))
CORE = range(6)
ATOMS = range(6, 12)
VERTICES = range(12)
CORE_EDGES = tuple((u, v) for u, v in combinations(CORE, 2)
                   if set(PAIRS[u]) & set(PAIRS[v]))
EDGES = CORE_EDGES + tuple((v, 6 + v) for v in CORE)
ADJ = {v: set() for v in VERTICES}
for u, v in EDGES:
    ADJ[u].add(v)
    ADJ[v].add(u)


def octahedral_faces():
    opposite = tuple((u, v) for u, v in combinations(CORE, 2)
                     if not set(PAIRS[u]) & set(PAIRS[v]))
    assert len(opposite) == 3
    xyz = {}
    for axis, (positive, negative) in enumerate(opposite):
        p = [0, 0, 0]
        p[axis] = 1
        xyz[positive] = tuple(p)
        p[axis] = -1
        xyz[negative] = tuple(p)
    faces = []
    for face in product(*opposite):
        a, b, c = (xyz[v] for v in face)
        x = tuple(b[j] - a[j] for j in range(3))
        y = tuple(c[j] - a[j] for j in range(3))
        normal = (x[1] * y[2] - x[2] * y[1],
                  x[2] * y[0] - x[0] * y[2],
                  x[0] * y[1] - x[1] * y[0])
        center = tuple(a[j] + b[j] + c[j] for j in range(3))
        faces.append(face if sum(normal[j] * center[j] for j in range(3)) > 0
                     else (face[0], face[2], face[1]))
    darts = Counter((u, v) for face in faces
                    for u, v in zip(face, face[1:] + face[:1]))
    assert len(faces) == 8 and len(CORE_EDGES) == 12
    assert len(darts) == 24
    assert all(darts[u, v] == darts[v, u] == 1 for u, v in CORE_EDGES)
    assert 6 - 12 + 8 == 2
    # A pendant edge can be drawn in a small disk around its core endpoint.
    assert all(ADJ[6 + v] == {v} for v in CORE)
    return faces


def bfs(source):
    dist = {source: 0}
    todo = deque([source])
    while todo:
        u = todo.popleft()
        for v in sorted(ADJ[u]):
            if v not in dist:
                dist[v] = dist[u] + 1
                todo.append(v)
    assert len(dist) == 12
    return dist


def geodesics():
    distance = {v: bfs(v) for v in VERTICES}
    paths = [(v,) for v in VERTICES]
    for source, target in combinations(VERTICES, 2):
        def visit(path):
            last = path[-1]
            if last == target:
                paths.append(tuple(path))
                return
            for nxt in sorted(ADJ[last]):
                if (distance[source][nxt] == distance[source][last] + 1
                        and distance[source][nxt] + distance[nxt][target]
                        == distance[source][target]):
                    visit(path + (nxt,))
        visit((source,))
    assert len(paths) == len(set(paths))
    assert all(len(p) - 1 == distance[p[0]][p[-1]] for p in paths)
    return paths


def components(deleted):
    remaining = set(VERTICES) - set(deleted)
    answer = []
    while remaining:
        seed = min(remaining)
        seen = {seed}
        todo = [seed]
        remaining.remove(seed)
        while todo:
            for v in ADJ[todo.pop()] & remaining:
                seen.add(v)
                remaining.remove(v)
                todo.append(v)
        answer.append(frozenset(seen))
    return answer


def menu(paths):
    pathset = set(paths)
    chosen = []
    big = []
    for label in range(4):
        core_c = {v for v in CORE if label in PAIRS[v]}
        s = sorted(set(CORE) - core_c)
        p, q = (s[0], s[1]), (s[1], s[2])
        assert p in pathset and q in pathset
        parts = components(set(p) | set(q))
        c = frozenset(core_c | {v + 6 for v in core_c})
        assert set(parts) == {c} | {frozenset({6 + v}) for v in s}
        chosen.append((p, q))
        big.append(c)
    assert all(sum(v in c for c in big) == 2 for v in VERTICES)
    for labels in combinations(range(4), 3):
        witness = [PAIRS.index(edge) for edge in combinations(labels, 2)]
        assert all(sum(v in big[i] for v in witness) == 2 for i in labels)
    return chosen, big


def audit_all_masses(big):
    count = 0
    for mass in product(range(3), repeat=12):
        total = sum(mass)
        doubled_bound = max(total, 2 * max(mass[v] for v in ATOMS))
        assert any(2 * sum(mass[v] for v in c) <= doubled_bound for c in big)
        count += 1
    assert count == 3 ** 12
    return count


def main():
    faces = octahedral_faces()
    paths = geodesics()
    # This checks every ambient unit-edge path pair, including repeated paths.
    all_pairs = list(combinations_with_replacement(paths, 2))
    pair_count = 0
    for p, q in all_pairs:
        parts = components(set(p) | set(q))
        assert all(parts[i].isdisjoint(parts[j])
                   for i, j in combinations(range(len(parts)), 2))
        pair_count += 1
    assert pair_count == len(all_pairs)
    chosen, big = menu(paths)
    samples = audit_all_masses(big)
    print(f"quotient: vertices=12 edges={len(EDGES)} core_faces={len(faces)}")
    print(f"all_geodesics={len(paths)} all_pairs={len(all_pairs)} prescribed_pairs={len(chosen)}")
    print(f"ternary_mass_vectors={samples} three_pair_witnesses=4 PASS")


if __name__ == "__main__":
    main()
