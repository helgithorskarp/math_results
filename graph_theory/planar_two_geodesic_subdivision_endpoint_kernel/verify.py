"""Exact small-case audit of the subdivision endpoint-kernel lemma.

Python 3.11+, standard library only. This audit does not replace the proof.
"""

import json
from heapq import heappop, heappush
from pathlib import Path


def build(n, edges, positive_positions, two_sided=True):
    """Expand small integer edges, then compress zero-mass chains.

    positive_positions contains (edge_index, offset_from_first_endpoint).
    """
    assert all(0 <= u < n and 0 <= v < n and u != v and L >= 1 for u, v, L in edges)
    assert len({frozenset((u, v)) for u, v, _ in edges}) == len(edges)
    unit_edges = []
    original_paths = []
    next_vertex = n
    for u, v, length in edges:
        interior = list(range(next_vertex, next_vertex + length - 1))
        next_vertex += length - 1
        path = [u] + interior + [v]
        original_paths.append(path)
        unit_edges.extend(zip(path, path[1:]))
    retained = set(range(n))
    for edge_id, offset in positive_positions:
        path = original_paths[edge_id]
        assert 1 <= offset < len(path) - 1
        retained.add(path[offset])

    chains = []
    for path in original_paths:
        starts = [i for i, v in enumerate(path) if v in retained]
        assert starts[0] == 0 and starts[-1] == len(path) - 1
        for a, b in zip(starts, starts[1:]):
            chains.append(path[a:b + 1])

    keep = set(retained)
    for chain in chains:
        if len(chain) > 2:
            keep.add(chain[1])
            if two_sided:
                keep.add(chain[-2])
    keep = sorted(keep)
    position = {v: i for i, v in enumerate(keep)}
    kernel_edges = []
    for chain in chains:
        stops = [i for i, v in enumerate(chain) if v in position]
        for a, b in zip(stops, stops[1:]):
            kernel_edges.append((position[chain[a]], position[chain[b]], b - a))
    unit_adj = [dict() for _ in range(next_vertex)]
    kernel_adj = [dict() for _ in keep]
    for u, v in unit_edges:
        unit_adj[u][v] = unit_adj[v][u] = 1
    for u, v, length in kernel_edges:
        kernel_adj[u][v] = kernel_adj[v][u] = length
    assert len(unit_edges) == sum(L for _, _, L in edges)
    assert len(kernel_edges) <= 3 * len(chains)
    return unit_adj, kernel_adj, keep, position, retained, chains


def distances(adjacency, source):
    inf = 10**15
    d = [inf] * len(adjacency)
    d[source] = 0
    heap = [(0, source)]
    while heap:
        length, u = heappop(heap)
        if length != d[u]:
            continue
        for v, weight in adjacency[u].items():
            if length + weight < d[v]:
                d[v] = length + weight
                heappush(heap, (d[v], v))
    return d


def geodesic_signatures(adjacency, full_labels, retained, chains):
    """Enumerate every shortest path between all endpoint pairs."""
    all_distances = [distances(adjacency, s) for s in range(len(adjacency))]
    chain_at_interior = {
        v: j for j, chain in enumerate(chains) for v in chain[1:-1]
    }
    signatures = set()
    geodesics = 0
    for source in range(len(adjacency)):
        for target in range(source, len(adjacency)):
            stack = [(source, (source,))]
            while stack:
                u, path = stack.pop()
                if u == target:
                    geodesics += 1
                    labels = [full_labels[v] for v in path]
                    deleted = frozenset(v for v in labels if v in retained)
                    cuts = frozenset(chain_at_interior[v] for v in labels if v in chain_at_interior)
                    signatures.add((deleted, cuts))
                    continue
                for v, length in adjacency[u].items():
                    if (all_distances[source][u] + length == all_distances[source][v]
                            and all_distances[source][v] + all_distances[v][target]
                            == all_distances[source][target]):
                        stack.append((v, path + (v,)))
                assert len(stack) < 100000
    return signatures, geodesics, all_distances


def audit_case(name, n, edges, positive_positions):
    unit, kernel, keep, position, retained, chains = build(n, edges, positive_positions)
    full_signatures, full_paths, full_distances = geodesic_signatures(
        unit, list(range(len(unit))), retained, chains
    )
    kernel_signatures, kernel_paths, kernel_distances = geodesic_signatures(
        kernel, keep, retained, chains
    )
    for u in keep:
        for v in keep:
            assert full_distances[u][v] == kernel_distances[position[u]][position[v]]
    assert full_signatures == kernel_signatures, (full_signatures - kernel_signatures,
                                                   kernel_signatures - full_signatures)
    print(f"{name}: unit={len(unit)} kernel={len(kernel)} "
          f"full_paths={full_paths} kernel_paths={kernel_paths} "
          f"signatures={len(full_signatures)}")
    return full_signatures


def large_example_counts():
    source = Path(__file__).parents[1] / "planar_two_geodesic_sparse_subdivision_probe" / "certificate.json"
    data = json.loads(source.read_text())
    marked = {int(v) - 32 for v in data["mass_atoms"] if int(v) >= 32}
    lengths = [item[2] for item in data["core_edges"]]
    faces = []
    for i in range(5):
        u, v = 1 + i, 1 + (i + 1) % 5
        a, b = 6 + i, 6 + (i + 1) % 5
        faces += [(0, u, v), (v, u, a), (v, a, b), (11, b, a)]
    faces = sorted(set(tuple(sorted(face)) for face in faces))
    assert len(faces) == 20
    for f in range(20):
        lengths.extend(data["parent_length"] if u == data["parents"][f]
                       else data["nonparent_length"] for u in faces[f])
    assert len(lengths) == 90 and len(marked) == 16
    pieces = []
    for j, length in enumerate(lengths):
        if j in marked:
            pieces += [length // 2, length - length // 2]
        else:
            pieces.append(length)
    assert len(pieces) == 106 and min(pieces) >= 3
    assert 32 + sum(length - 1 for length in lengths) == 1151795
    compressed_vertices = 32 + len(marked)
    kernel_vertices = compressed_vertices + 2 * len(pieces)
    kernel_edges = 3 * len(pieces)
    assert (kernel_vertices, kernel_edges) == (260, 318)
    print(f"large_example: unit=1151795 sparse=48 endpoint_kernel={kernel_vertices} "
          f"kernel_edges={kernel_edges}")


def main():
    triangle = [(0, 1, 6), (1, 2, 1), (0, 2, 1)]
    full = audit_case("triangle", 3, triangle, [])
    # Endpoints on the same long chain admit both a direct geodesic
    # and an equally short detour through all three retained vertices.
    assert (frozenset(), frozenset((0,))) in full
    assert (frozenset((0, 1, 2)), frozenset((0,))) in full
    one_sided = build(3, triangle, [], two_sided=False)
    one_sided_signatures, _, _ = geodesic_signatures(
        one_sided[1], one_sided[2], one_sided[4], one_sided[5]
    )
    target = (frozenset((1, 2)), frozenset((0,)))
    assert target in full and target not in one_sided_signatures
    reversed_triangle = [(1, 0, 6), (1, 2, 1), (0, 2, 1)]
    reversed_full = build(3, reversed_triangle, [])
    reversed_one_sided = build(3, reversed_triangle, [], two_sided=False)
    reverse_target = (frozenset((0, 2)), frozenset((0,)))
    assert reverse_target in geodesic_signatures(
        reversed_full[1], reversed_full[2], reversed_full[4], reversed_full[5]
    )[0]
    assert reverse_target not in geodesic_signatures(
        reversed_one_sided[1], reversed_one_sided[2],
        reversed_one_sided[4], reversed_one_sided[5]
    )[0]
    print("triangle_both_one_sided_orientations_miss_a_signature=True")

    audit_case("supported_square", 4,
               [(0, 1, 8), (1, 2, 6), (2, 3, 9), (3, 0, 5), (0, 2, 11)],
               [(0, 3), (2, 4), (4, 5)])
    audit_case("supported_path", 3, [(0, 1, 7), (1, 2, 8)], [(0, 3)])
    large_example_counts()
    print("PASS")


if __name__ == "__main__":
    main()
