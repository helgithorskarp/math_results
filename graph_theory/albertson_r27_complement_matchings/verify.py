#!/usr/bin/env python3
"""Exact checks for the Albertson r=27 complement-matching note."""

from itertools import combinations


def edge(a, b):
    return frozenset((a, b))


def add_clique(edges, vertices):
    for a, b in combinations(vertices, 2):
        edges.add(edge(a, b))


def displayed_equality_graph(k, sizes):
    assert len(sizes) == 3 and all(x > 0 for x in sizes)
    assert sum(sizes) == k - 1

    A = [f"a{i}" for i in range(k - 2)]
    S = []
    for part, size in enumerate(sizes, 1):
        S.append([f"s{part}_{i}" for i in range(size)])
    C = [f"c{i}" for i in range(1, 4)]
    vertices = A + [x for part in S for x in part] + C
    edges = set()

    add_clique(edges, A)
    add_clique(edges, [x for part in S for x in part])
    for i in range(3):
        for x in A + S[i]:
            edges.add(edge(C[i], x))
    return vertices, edges, A, S, C


def connected_complement(vertices, edges):
    adjacency = {v: set() for v in vertices}
    for a, b in combinations(vertices, 2):
        if edge(a, b) not in edges:
            adjacency[a].add(b)
            adjacency[b].add(a)
    seen = {vertices[0]}
    stack = [vertices[0]]
    while stack:
        stack.extend(adjacency[stack.pop()] - seen)
        seen.update(stack)
    return len(seen) == len(vertices)


def verify_topological_certificate(edges, A, S, C, k):
    branch = A + C[:2]
    assert len(branch) == k
    missing = []
    for x, y in combinations(branch, 2):
        if edge(x, y) not in edges:
            missing.append((x, y))
    assert missing == [(C[0], C[1])]

    path = [C[0], S[0][0], S[1][0], C[1]]
    assert all(edge(x, y) in edges for x, y in zip(path, path[1:]))
    assert not (set(path[1:-1]) & set(branch))


def verify_frontier_arithmetic():
    k = 27
    cases_53 = []
    for m in (713, 714, 715):
        complement_edges = 53 * 52 // 2 - m
        deficit = 26 * 53 - 2 * complement_edges
        low_vertices = 53 - deficit
        cases_53.append((m, complement_edges, deficit, low_vertices))
    assert cases_53 == [
        (713, 665, 48, 5),
        (714, 664, 50, 3),
        (715, 663, 52, 1),
    ]

    m = k * k - 3
    complement_edges = 54 * 53 // 2 - m
    deficit = 27 * 54 - 2 * complement_edges
    low_vertices = 54 - deficit
    assert (m, complement_edges, deficit, low_vertices) == (726, 705, 48, 6)
    return cases_53, (m, complement_edges, deficit, low_vertices)


def verify_displayed_family():
    k = 27
    checked = 0
    for s1 in range(1, k - 2):
        for s2 in range(1, k - 1 - s1):
            s3 = k - 1 - s1 - s2
            if s3 < 1:
                continue
            vertices, edges, A, S, C = displayed_equality_graph(k, (s1, s2, s3))
            degrees = {
                v: sum(edge(v, w) in edges for w in vertices if w != v)
                for v in vertices
            }
            excess = 2 * len(edges) - (k - 1) * len(vertices)
            assert len(vertices) == 2 * k
            assert len(edges) == k * k - 3
            assert min(degrees.values()) == k - 1
            assert excess == 2 * (k - 3)
            assert connected_complement(vertices, edges)
            verify_topological_certificate(edges, A, S, C, k)
            checked += 1
    assert checked == 300
    return checked


def main():
    cases_53, case_54 = verify_frontier_arithmetic()
    checked = verify_displayed_family()
    print("PASS: exact complement-deficit arithmetic")
    for m, complement_edges, deficit, low_vertices in cases_53:
        print(
            f"  n=53 m={m}: e(H)={complement_edges}, "
            f"deficit={deficit}, low vertices >= {low_vertices}"
        )
    m, complement_edges, deficit, low_vertices = case_54
    print(
        f"  n=54 m={m}: e(H)={complement_edges}, "
        f"deficit={deficit}, low vertices >= {low_vertices}"
    )
    print(
        "PASS: all "
        f"{checked} ordered positive (|S1|,|S2|,|S3|) triples "
        "in the displayed equality family have the explicit TK_27 certificate"
    )


if __name__ == "__main__":
    main()
