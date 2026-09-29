"""Exact sparse-mass check on an implicitly unit-subdivided planar graph.

Python 3.11+, standard library only. All arithmetic is integer.
"""

import json
from collections import Counter
from heapq import heappop, heappush
from pathlib import Path


DATA = json.loads(Path(__file__).with_name("certificate.json").read_text())


def icosahedron_faces():
    faces = []
    for i in range(5):
        u, v = 1 + i, 1 + (i + 1) % 5
        a, b = 6 + i, 6 + (i + 1) % 5
        faces += [(0, u, v), (v, u, a), (v, a, b), (11, b, a)]
    return sorted(set(tuple(sorted(face)) for face in faces))


def check_sphere(faces, core_edges):
    assert len(faces) == 20 and len(core_edges) == 30
    occurrence = Counter(
        tuple(sorted((face[i], face[(i + 1) % 3])))
        for face in faces for i in range(3)
    )
    assert set(occurrence) == set(core_edges)
    assert all(n == 2 for n in occurrence.values())
    assert 12 - 30 + 20 == 2
    for center in range(12):
        link = {}
        for face in faces:
            if center not in face:
                continue
            a, b = (v for v in face if v != center)
            link.setdefault(a, set()).add(b)
            link.setdefault(b, set()).add(a)
        assert all(len(neighbors) == 2 for neighbors in link.values())
        visited, queue = set(), [next(iter(link))]
        for u in queue:
            if u in visited:
                continue
            visited.add(u)
            queue.extend(link[u] - visited)
        assert len(visited) == len(link)


def construct():
    faces = icosahedron_faces()
    core_edges = [(u, v) for u, v, _ in DATA["core_edges"]]
    check_sphere(faces, core_edges)
    edges = [(u, v, length) for u, v, length in DATA["core_edges"]]
    for f, face in enumerate(faces):
        for u in face:
            length = DATA["parent_length"] if u == DATA["parents"][f] else DATA["nonparent_length"]
            edges.append((12 + f, u, length))
    assert len(edges) == 90
    assert all(length > 0 for _, _, length in edges)
    total_vertices = 32 + sum(length - 1 for _, _, length in edges)
    assert total_vertices == 1151795
    original_edge = {frozenset((u, v)): j for j, (u, v, _) in enumerate(edges)}
    assert len(original_edge) == 90

    raw_mass = {int(v): w for v, w in DATA["mass_atoms"].items()}
    marked_edges = sorted(v - 32 for v in raw_mass if v >= 32)
    label = {j: 32 + i for i, j in enumerate(marked_edges)}
    compressed = [set() for _ in range(32 + len(marked_edges))]
    adjacency = [dict() for _ in compressed]
    for j, (u, v, length) in enumerate(edges):
        if j in label:
            z = label[j]
            sections = [(u, z, length // 2), (z, v, length - length // 2)]
        else:
            sections = [(u, v, length)]
        for a, b, section_length in sections:
            assert section_length >= 1
            adjacency[a][b] = section_length
            adjacency[b][a] = section_length
            compressed[a].add(b)
            compressed[b].add(a)
    mass = [0] * len(compressed)
    for v, w in raw_mass.items():
        mass[v if v < 32 else label[v - 32]] = w
    assert sum(mass) == 29 and len(marked_edges) == 16
    return edges, original_edge, label, adjacency, compressed, mass, total_vertices


def distance(adjacency, source, target):
    infinity = 10**20
    dist = [infinity] * len(adjacency)
    dist[source] = 0
    heap = [(0, source)]
    while heap:
        d, u = heappop(heap)
        if d != dist[u]:
            continue
        if u == target:
            return d
        for v, length in adjacency[u].items():
            if d + length < dist[v]:
                dist[v] = d + length
                heappush(heap, (dist[v], v))
    raise AssertionError("disconnected graph")


def check_path(path, adjacency):
    assert len(set(path)) == len(path)
    length = sum(adjacency[u][v] for u, v in zip(path, path[1:]))
    assert length == distance(adjacency, path[0], path[-1])


def component_masses(compressed, mass, paths):
    gone = set().union(*(set(path) for path in paths))
    seen = set(gone)
    out = []
    for start in range(len(compressed)):
        if start in seen:
            continue
        queue = [start]
        seen.add(start)
        amount = 0
        for u in queue:
            amount += mass[u]
            for v in compressed[u] - seen:
                seen.add(v)
                queue.append(v)
        out.append(amount)
    return sorted((w for w in out if w), reverse=True)


def main():
    edges, edge_index, label, adjacency, compressed, mass, order = construct()
    def expand_original_path(path):
        expanded = [path[0]]
        for u, v in zip(path, path[1:]):
            j = edge_index[frozenset((u, v))]
            if j in label:
                expanded.append(label[j])
            expanded.append(v)
        return expanded

    menu_masses = []
    for a, b in DATA["positive_pairs"]:
        paths = [expand_original_path(a), expand_original_path(b)]
        for path in paths:
            check_path(path, adjacency)
        menu_masses.append(max(component_masses(compressed, mass, paths)))
    assert len(menu_masses) == 15 and min(menu_masses) >= 15
    assert sum(sorted(mass, reverse=True)[:4]) == 8

    def decode(v):
        return v if v < 32 else label[v - 32]
    rescue = [[decode(v) for v in path] for path in DATA["rescue_pair"]]
    for path in rescue:
        check_path(path, adjacency)
    rescue_masses = component_masses(compressed, mass, rescue)
    assert max(rescue_masses) == 14
    print(f"planar_unit_subdivision_vertices={order} compressed_vertices={len(compressed)}")
    print(f"mass_total={sum(mass)} top_four={sum(sorted(mass, reverse=True)[:4])}")
    print("menu_largest_components=" + ",".join(map(str, menu_masses)))
    print("rescue_component_masses=" + ",".join(map(str, rescue_masses)))
    print("PASS")


if __name__ == "__main__":
    main()
