#!/usr/bin/env python3
"""Independent exact audit for the six-excess flag-sphere transfer.

The checker imports no reviewed module.  It reconstructs graph/face/gamma
identities, enumerates the critical degree profiles, and directly checks the
two-antipode recurrence on nonsuspension fixtures through excess six.
"""

from fractions import Fraction as Q
from hashlib import sha256
from itertools import combinations
from json import dumps
from math import comb
from pathlib import Path
import sys


def require(condition, message):
    if not condition:
        raise ValueError(message)


def choose(n, k):
    return comb(n, k) if 0 <= k <= n else 0


def multiply(a, b):
    result = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            result[i + j] += x * y
    return result


def gamma_from_face_counts(face_counts, d):
    h = [
        sum((-1) ** (k - j) * choose(d - j, k - j) * face_counts[j]
            for j in range(min(k, len(face_counts) - 1) + 1))
        for k in range(d + 1)
    ]
    gamma = []
    for k in range(d // 2 + 1):
        gamma.append(h[k] - sum(
            gamma[j] * choose(d - 2 * j, k - j) for j in range(k)
        ))
    reconstructed = [
        sum(gamma[j] * choose(d - 2 * j, k - j) for j in range(len(gamma)))
        for k in range(d + 1)
    ]
    require(reconstructed == h, "gamma basis reconstruction failed")
    return gamma


def cycle(length):
    graph = [set() for _ in range(length)]
    for vertex in range(length):
        other = (vertex + 1) % length
        graph[vertex].add(other)
        graph[other].add(vertex)
    return graph


def zero_sphere():
    return [set(), set()]


def join(left, right):
    n, m = len(left), len(right)
    graph = [set(neighbors) | set(range(n, n + m)) for neighbors in left]
    graph += [
        {n + neighbor for neighbor in neighbors} | set(range(n))
        for neighbors in right
    ]
    return graph


def subdivide_edge(graph, u, v):
    require(v in graph[u], "subdivision edge absent")
    graph = [set(neighbors) for neighbors in graph]
    common = graph[u] & graph[v]
    graph[u].remove(v)
    graph[v].remove(u)
    new_vertex = len(graph)
    new_neighbors = common | {u, v}
    for neighbor in new_neighbors:
        graph[neighbor].add(new_vertex)
    graph.append(set(new_neighbors))
    return graph


def induced(graph, vertices):
    vertices = sorted(vertices)
    index = {vertex: i for i, vertex in enumerate(vertices)}
    return [
        {index[neighbor] for neighbor in graph[vertex] if neighbor in index}
        for vertex in vertices
    ]


def face_counts(graph):
    # Incremental clique enumeration.  Flag faces are graph cliques.
    faces = [frozenset()]
    for vertex in range(len(graph)):
        faces += [
            face | {vertex}
            for face in faces
            if all(neighbor in graph[vertex] for neighbor in face)
        ]
    d = max(map(len, faces))
    counts = [sum(len(face) == size for face in faces) for size in range(d + 1)]
    return counts, len(faces)


def complement_degrees(graph):
    return [len(graph) - 1 - len(neighbors) for neighbors in graph]


def pad(values, length):
    return list(values) + [0] * (length - len(values))


def recurrence_fixtures():
    # Begin with an edge subdivision of Sigma C5, then join successive C5s.
    graph = subdivide_edge(join(cycle(5), zero_sphere()), 0, 5)
    rows = []
    for ell in range(2, 7):
        counts, number_faces = face_counts(graph)
        d = len(counts) - 1
        require(len(graph) == 2 * d + ell and d == 2 * ell - 1,
                "near-maximal fixture parameters failed")
        gamma = gamma_from_face_counts(counts, d)
        expected = multiply([1, 2], [choose(ell - 2, j) for j in range(ell - 1)])
        require(gamma == expected, "near-maximal gamma polynomial failed")

        degrees = complement_degrees(graph)
        require(min(degrees) == 2, "near-maximal fixture has wrong polar size")
        vertex = degrees.index(2)
        antipodes = [u for u in range(len(graph)) if u != vertex and u not in graph[vertex]]
        require(len(antipodes) == 2 and antipodes[1] in graph[antipodes[0]],
                "two-antipode configuration failed")

        link_graph = induced(graph, graph[vertex])
        edge_link_vertices = graph[antipodes[0]] & graph[antipodes[1]]
        edge_link_graph = induced(graph, edge_link_vertices)
        link_counts, _ = face_counts(link_graph)
        edge_link_counts, _ = face_counts(edge_link_graph)
        gamma_link = gamma_from_face_counts(link_counts, d - 1)
        gamma_edge_link = gamma_from_face_counts(edge_link_counts, d - 2)
        recurrence = [
            pad(gamma_link, len(gamma))[i]
            + (gamma_edge_link[i - 1] if 0 < i <= len(gamma_edge_link) else 0)
            for i in range(len(gamma))
        ]
        require(recurrence == gamma, "two-antipode gamma recurrence failed")
        require(gamma_link == [choose(ell - 1, j) for j in range(ell)],
                "link is not the expected pentagon join")
        expected_edge = [choose(ell - 2, j) for j in range(ell - 1)]
        require(gamma_edge_link == expected_edge,
                "equator is not the expected suspended pentagon join")

        rows.append({
            "ell": ell,
            "d": d,
            "vertices": len(graph),
            "faces_including_empty": number_faces,
            "gamma": gamma,
            "link_gamma": gamma_link,
            "edge_link_gamma": gamma_edge_link,
        })
        graph = join(graph, cycle(5))
    return rows


def direct_counts(graph):
    edges = sum(map(len, graph)) // 2
    triangles = sum(
        v in graph[u] and w in graph[u] and w in graph[v]
        for u, v, w in combinations(range(len(graph)), 3)
    )
    return edges, triangles


def complement(graph):
    vertices = set(range(len(graph)))
    return [vertices - {v} - graph[v] for v in range(len(graph))]


def gamma_low_from_graph(graph, d):
    edges, triangles = direct_counts(graph)
    faces = [1, len(graph), edges, triangles]
    h = [
        sum((-1) ** (k - j) * choose(d - j, k - j) * faces[j]
            for j in range(k + 1))
        for k in range(4)
    ]
    gamma = []
    for k in range(4):
        gamma.append(h[k] - sum(
            gamma[j] * choose(d - 2 * j, k - j) for j in range(k)
        ))
    return gamma


def lcg_bits(seed):
    state = seed
    while True:
        state = (6364136223846793005 * state + 1442695040888963407) & ((1 << 64) - 1)
        yield state


def identity_audit():
    stream = lcg_bits(0x6E1CE55)
    cases = links = 0
    for d in range(6, 19):
        for ell in range(0, 9):
            n = 2 * d + ell
            for threshold in (1, 3, 6):
                missing = [set() for _ in range(n)]
                for u, v in combinations(range(n), 2):
                    if next(stream) % 11 < threshold:
                        missing[u].add(v)
                        missing[v].add(u)
                graph = complement(missing)
                gamma = gamma_low_from_graph(graph, d)
                q = [len(row) for row in missing]
                m, triangles_h = direct_counts(missing)
                a, b = gamma[2], gamma[3]
                require(gamma[1] == ell, "random identity excess failed")
                require(a == d + Q(ell * (ell + 5), 2) - m,
                        "random gamma2 identity failed")
                predicted_b = Q((ell + 4) * (6 * d + ell * ell + 11 * ell), 6)
                predicted_b += sum(Q(value * (value - ell - 5), 2) for value in q)
                predicted_b -= triangles_h
                require(b == predicted_b, "random gamma3 identity failed")
                local_sum = 0
                for vertex in range(n):
                    link_graph = induced(graph, graph[vertex])
                    link_gamma = gamma_low_from_graph(link_graph, d - 1)
                    antipodes = missing[vertex]
                    tv = sum(v in missing[u] for u, v in combinations(antipodes, 2))
                    predicted = a + ell + 2 + Q(q[vertex] * (q[vertex] - 2 * ell - 7), 2)
                    predicted += sum(q[u] for u in antipodes) - tv
                    require(link_gamma[2] == predicted, "random local identity failed")
                    local_sum += link_gamma[2]
                    links += 1
                require(local_sum == (2 * d - 8) * a + 3 * b,
                        "random summed-link identity failed")
                residual = sum((value - 3) * (ell + 1 - value) for value in q)
                k_value = Q(ell * (ell * ell + 3 * ell + 20 - 12 * d), 6)
                require(b == a + k_value - Q(residual, 2) - triangles_h,
                        "random degree-budget identity failed")
                cases += 1
    return {"new_seed": "0x6e1ce55", "graph_instances": cases,
            "individual_link_instances": links, "maximum_d": 18,
            "maximum_ell": 8}


def compositions(total, length):
    if length == 1:
        yield (total,)
        return
    for first in range(total + 1):
        for tail in compositions(total - first, length - 1):
            yield (first,) + tail


def critical_profiles():
    summary = {}
    total = 0
    for d in range(8, 13):
        n = 2 * d + 6
        survivors = []
        tested = 0
        for counts in compositions(n, 5):
            tested += 1
            twice_edges = sum((degree + 3) * count for degree, count in enumerate(counts))
            if twice_edges % 2:
                continue
            degree_excess = sum(degree * count for degree, count in enumerate(counts))
            a = d + 33 - twice_edges // 2
            b0 = 10 * d + 170 + sum(
                Q(q * (q - 11), 2) * counts[q - 3] for q in range(3, 8)
            )
            require(b0 < 0, "gamma3 upper bound is not negative")
            s0 = (2 * d - 8) * a + 3 * b0
            if s0 >= 0:
                require(d == 8 and degree_excess <= 4 and counts[0] > 0,
                        "unexpected structural-profile survivor")
                require(1 + Q(degree_excess, 2) <= 3,
                        "cubic-link upper bound exceeds three")
                survivors.append({
                    "degree_counts_3_to_7": list(counts),
                    "D": degree_excess,
                    "gamma2": a,
                    "S_at_T0": int(s0),
                })
        total += tested
        summary[str(d)] = {"profiles_tested": tested, "survivors": survivors}
    require(len(summary["8"]["survivors"]) == 4, "wrong d=8 survivor count")
    require(all(not summary[str(d)]["survivors"] for d in range(9, 13)),
            "survivor above d=8")
    return {"total_profiles_tested": total, "by_dimension": summary}


def endpoint_logic():
    # Coefficients not handled by gamma_2/gamma_3 are exactly the two LN
    # endpoint slots gamma_{ell-1}, gamma_ell, or vanish.
    rows = []
    for ell in range(0, 7):
        uncontrolled = [i for i in range(2, ell + 1) if i not in {2, 3, ell - 1, ell}]
        rows.append({"ell": ell, "interior_indices_beyond_gamma2_gamma3": uncontrolled})
    require(not any(row["interior_indices_beyond_gamma2_gamma3"] for row in rows[:6]),
            "ell at most five has an uncovered coefficient")
    require(rows[6]["interior_indices_beyond_gamma2_gamma3"] == [4],
            "ell six should leave only gamma4 for structural induction")
    return rows


def main():
    result = {
        "status": "PASS",
        "identity_audit": identity_audit(),
        "critical_profiles": critical_profiles(),
        "two_antipode_fixtures": recurrence_fixtures(),
        "endpoint_logic": endpoint_logic(),
        "trust_boundary": (
            "Exact finite identities and explicit flag-sphere fixtures only. "
            "The Labbé-Nevo and Davis-Okun inputs, the two finite base theorems, "
            "and the universal induction are audited mathematically rather than proved here."
        ),
    }
    return result


if __name__ == "__main__":
    if len(sys.argv) > 2:
        raise SystemExit("usage: independent_check.py [EXPECTED_OUTPUT.json]")
    encoded = (dumps(main(), indent=2, sort_keys=True) + "\n").encode()
    if len(sys.argv) == 2:
        expected = Path(sys.argv[1]).read_bytes()
        require(encoded == expected, "output differs from expected output")
    print(dumps({"status": "PASS", "sha256": sha256(encoded).hexdigest()}, sort_keys=True))
