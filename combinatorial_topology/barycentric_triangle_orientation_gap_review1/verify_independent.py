#!/usr/bin/env python3
"""Independent exact audit of the barycentric triangle-packing theorem.

CPython 3.11+, standard library only.  This does not import target code.
"""

from collections import Counter
from functools import lru_cache
from hashlib import sha256
from itertools import combinations, product
import json


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def normalize(facets, enforce_incidence=True):
    facets = tuple(sorted(tuple(sorted(facet)) for facet in facets))
    require(facets, "nonempty facet family required")
    require(all(len(facet) == 3 and len(set(facet)) == 3 for facet in facets),
            "every facet must have three distinct vertices")
    require(len(set(facets)) == len(facets), "duplicate facet")
    counts = Counter(edge for facet in facets for edge in combinations(facet, 2))
    if enforce_incidence:
        require(max(counts.values()) <= 2, "edge incidence exceeds two")
    return facets


def nonempty_subfaces(facet):
    return {
        frozenset(part)
        for size in range(1, len(facet) + 1)
        for part in combinations(facet, size)
    }


def flag_model(facets):
    """Construct flags and their conflicts directly from graph-edge sharing."""
    facets = normalize(facets)
    flags = []
    triangle_edges = []
    index = {}
    for i, facet in enumerate(facets):
        facet_face = frozenset(facet)
        for edge in combinations(facet, 2):
            edge_face = frozenset(edge)
            for vertex in edge:
                vertex_face = frozenset((vertex,))
                flag = (vertex, tuple(edge), i)
                index[flag] = len(flags)
                flags.append(flag)
                graph_triangle = (vertex_face, edge_face, facet_face)
                triangle_edges.append(frozenset(
                    frozenset(pair) for pair in combinations(graph_triangle, 2)
                ))
    adjacency = [0] * len(flags)
    for i, j in combinations(range(len(flags)), 2):
        if triangle_edges[i] & triangle_edges[j]:
            adjacency[i] |= 1 << j
            adjacency[j] |= 1 << i
    return facets, tuple(flags), tuple(triangle_edges), adjacency, index


def literal_barycentric_audit(facets):
    """Check independently that the graph's 3-cliques are precisely flags."""
    facets, flags, triangle_edges, _, _ = flag_model(facets)
    faces = set()
    for facet in facets:
        faces |= nonempty_subfaces(facet)
    faces = tuple(sorted(faces, key=lambda face: (len(face), tuple(face))))
    graph_edges = {
        frozenset((left, right))
        for left, right in combinations(faces, 2)
        if left < right or right < left
    }
    cliques = {
        frozenset(triple)
        for triple in combinations(faces, 3)
        if all(frozenset(pair) in graph_edges for pair in combinations(triple, 2))
    }
    from_flags = set()
    for edges in triangle_edges:
        vertices = set()
        for edge in edges:
            vertices |= set(edge)
        from_flags.add(frozenset(vertices))
    require(cliques == from_flags and len(cliques) == 6 * len(facets),
            "literal graph triangles differ from flags")
    return len(faces), len(graph_edges), len(cliques)


def orientation_constraints(facets):
    """Return x_i xor x_j = parity constraints from cyclic references."""
    incidence = {}
    for i, (a, b, c) in enumerate(facets):
        directed_starts = (((a, b), a), ((b, c), b), ((a, c), c))
        for edge, start in directed_starts:
            incidence.setdefault(tuple(sorted(edge)), []).append((i, start))
    constraints = []
    for entries in incidence.values():
        if len(entries) == 2:
            (left, start_left), (right, start_right) = entries
            constraints.append((left, right, int(start_left == start_right)))
    return tuple(sorted(constraints))


def coherent_after_deletion(facet_count, constraints, deleted):
    deleted = set(deleted)
    graph = [[] for _ in range(facet_count)]
    for left, right, parity in constraints:
        graph[left].append((right, parity))
        graph[right].append((left, parity))
    labels = {}
    for root in range(facet_count):
        if root in deleted or root in labels:
            continue
        labels[root] = 0
        queue = [root]
        for current in queue:
            for neighbor, parity in graph[current]:
                if neighbor in deleted:
                    continue
                wanted = labels[current] ^ parity
                if neighbor in labels:
                    if labels[neighbor] != wanted:
                        return None
                else:
                    labels[neighbor] = wanted
                    queue.append(neighbor)
    return labels


def minimum_deletion(facet_count, constraints):
    for size in range(facet_count + 1):
        for deleted in combinations(range(facet_count), size):
            labels = coherent_after_deletion(facet_count, constraints, deleted)
            if labels is not None:
                return deleted, labels
    raise RuntimeError("deletion enumeration exhausted")


def minimum_violations(facet_count, constraints):
    return min(
        sum((((assignment >> left) ^ (assignment >> right)) & 1) != parity
            for left, right, parity in constraints)
        for assignment in range(1 << facet_count)
    )


def exact_independence_number(adjacency):
    """Definition-level include/exclude recurrence with safe leaf reductions."""
    calls = 0

    @lru_cache(None)
    def solve(mask):
        nonlocal calls
        calls += 1
        if not mask:
            return 0
        remaining = mask
        branch_vertex = -1
        maximum_degree = -1
        while remaining:
            bit = remaining & -remaining
            vertex = bit.bit_length() - 1
            degree = (adjacency[vertex] & mask).bit_count()
            if degree == 0:
                return 1 + solve(mask ^ bit)
            if degree == 1:
                # Some maximum independent set contains a leaf: swap out its
                # unique neighbor if necessary.
                return 1 + solve(mask & ~bit & ~adjacency[vertex])
            if degree > maximum_degree:
                branch_vertex = vertex
                maximum_degree = degree
            remaining ^= bit
        bit = 1 << branch_vertex
        excluding = solve(mask ^ bit)
        including = 1 + solve(mask & ~bit & ~adjacency[branch_vertex])
        return max(excluding, including)

    value = solve((1 << len(adjacency)) - 1)
    return value, calls


def reference_starts(facet):
    a, b, c = facet
    return {(a, b): a, (b, c): b, (a, c): c}


def greedy_witness(facets, flags, triangle_edges, adjacency, index, deleted, labels):
    deleted = set(deleted)
    chosen = []
    occupied = 0
    for i, facet in enumerate(facets):
        if i in deleted:
            continue
        starts = reference_starts(facet)
        for edge in combinations(facet, 2):
            edge = tuple(edge)
            wanted = starts[edge]
            if labels[i]:
                wanted = next(vertex for vertex in edge if vertex != wanted)
            flag_index = index[(wanted, edge, i)]
            require(not (adjacency[flag_index] & occupied),
                    "coherent retained triples conflict")
            chosen.append(flag_index)
            occupied |= 1 << flag_index

    # Reverse facet order and prefer the lexicographically last pair.  This
    # intentionally differs from the target implementation's choice rule.
    for i in sorted(deleted, reverse=True):
        block = [j for j, (_, _, owner) in enumerate(flags) if owner == i]
        available = [j for j in block if not (adjacency[j] & occupied)]
        require(len(available) >= 3, "fewer than three locally available flags")
        candidates = [pair for pair in combinations(available, 2)
                      if not (adjacency[pair[0]] & (1 << pair[1]))]
        require(candidates, "local completion has no independent pair")
        pair = candidates[-1]
        for flag_index in pair:
            require(not (adjacency[flag_index] & occupied), "greedy conflict")
            chosen.append(flag_index)
            occupied |= 1 << flag_index

    used_graph_edges = set()
    for flag_index in chosen:
        require(not (used_graph_edges & triangle_edges[flag_index]),
                "constructed packing shares a graph edge")
        used_graph_edges |= set(triangle_edges[flag_index])
    return tuple(sorted(chosen))


def cover_and_fractional_audit(facets, triangle_edges):
    cover = {
        frozenset((frozenset((vertex,)), frozenset(facet)))
        for facet in facets for vertex in facet
    }
    require(len(cover) == 3 * len(facets), "wrong vertex-facet cover size")
    require(all(cover & set(edges) for edges in triangle_edges), "uncovered flag")
    loads = Counter(edge for edges in triangle_edges for edge in edges)
    require(max(loads.values()) <= 2, "half-weight packing is infeasible")
    require(len(triangle_edges) == 6 * len(facets), "wrong flag count")


def analyze_family(facets):
    facets, flags, triangle_edges, adjacency, index = flag_model(facets)
    constraints = orientation_constraints(facets)
    deleted, labels = minimum_deletion(len(facets), constraints)
    kappa = len(deleted)
    violations = minimum_violations(len(facets), constraints)
    require(violations == kappa, "vertex and edge frustration disagree")
    witness = greedy_witness(facets, flags, triangle_edges, adjacency, index,
                             deleted, labels)
    alpha, calls = exact_independence_number(adjacency)
    require(alpha == len(witness) == 3 * len(facets) - kappa,
            "exact packing differs from orientation-defect formula")
    cover_and_fractional_audit(facets, triangle_edges)
    return {
        "facets": len(facets),
        "kappa": kappa,
        "packing": alpha,
        "cover": 3 * len(facets),
        "deleted": list(deleted),
        "witness": list(witness),
        "mis_calls": calls,
    }


TRIANGLES6 = tuple(combinations(range(6), 3))
PAIRS6 = tuple(combinations(range(6), 2))
PAIR_INDEX6 = {edge: i for i, edge in enumerate(PAIRS6)}
USES6 = tuple(tuple(PAIR_INDEX6[edge] for edge in combinations(facet, 2))
              for facet in TRIANGLES6)


def enumerate_six_label_families():
    capacities = [0] * len(PAIRS6)
    families = []

    def generate(position, mask, selected):
        if position == len(TRIANGLES6):
            if mask:
                families.append((mask, tuple(selected)))
            return
        generate(position + 1, mask, selected)
        used = USES6[position]
        if all(capacities[pair] < 2 for pair in used):
            for pair in used:
                capacities[pair] += 1
            selected.append(position)
            generate(position + 1, mask | (1 << position), selected)
            selected.pop()
            for pair in used:
                capacities[pair] -= 1

    generate(0, 0, [])
    families.sort()
    histogram = Counter()
    digest = sha256()
    total_calls = 0
    for mask, selected in families:
        facets = tuple(TRIANGLES6[i] for i in selected)
        row = analyze_family(facets)
        histogram[(row["facets"], row["kappa"], row["packing"])] += 1
        total_calls += row["mis_calls"]
        digest.update(json.dumps([mask, row], separators=(",", ":")).encode())
        digest.update(b"\n")
    expected_histogram = {
        (1, 0, 3): 20, (2, 0, 6): 190, (3, 0, 9): 1080,
        (4, 0, 12): 3870, (5, 0, 15): 8532, (5, 1, 14): 72,
        (6, 0, 18): 10230, (6, 1, 17): 840,
        (7, 0, 21): 5460, (7, 1, 20): 1560,
        (8, 0, 24): 1035, (8, 1, 23): 630,
        (9, 2, 25): 120, (10, 3, 27): 12,
    }
    require(len(families) == 33651, "incomplete six-label family enumeration")
    require(dict(histogram) == expected_histogram, "family histogram changed")
    return {
        "families": len(families),
        "exact_MIS_instances": len(families),
        "MIS_recurrence_calls": total_calls,
        "histogram": {f"f={f},k={k},a={a}": count
                      for (f, k, a), count in sorted(histogram.items())},
        "entrywise_sha256": digest.hexdigest(),
    }


def local_completion_audit():
    cycle = [0] * 6
    for i in range(6):
        cycle[i] = (1 << ((i - 1) % 6)) | (1 << ((i + 1) % 6))
    passed = 0
    for pattern in product((-1, 0, 1), repeat=3):
        forbidden = 0
        for side, endpoint in enumerate(pattern):
            if endpoint >= 0:
                forbidden |= 1 << (2 * side + endpoint)
        available = [i for i in range(6) if not (forbidden >> i & 1)]
        require(len(available) >= 3, "local count below three")
        require(any(not (cycle[left] & (1 << right))
                    for left, right in combinations(available, 2)),
                "local pattern has no independent pair")
        passed += 1
    return passed


def fixtures_and_failures():
    mobius_band = [(0, 1, 2), (0, 1, 3), (0, 2, 4),
                   (1, 3, 4), (2, 3, 4)]
    projective_plane = [(0, 1, 2), (0, 1, 3), (0, 2, 4), (0, 3, 5),
                        (0, 4, 5), (1, 2, 5), (1, 3, 4), (1, 4, 5),
                        (2, 3, 4), (2, 3, 5)]
    fixtures = {
        "single_facet": [(0, 1, 2)],
        "two_disjoint_facets": [(0, 1, 2), (3, 4, 5)],
        "two_facets_touching_at_vertex": [(0, 1, 2), (0, 3, 4)],
        "tetrahedron_boundary": list(combinations(range(4), 3)),
        "minimal_five_facet_defect": mobius_band,
        "projective_plane": projective_plane,
        "defect_plus_disjoint_facet": mobius_band + [(5, 6, 7)],
    }
    rows = {}
    for name, facets in fixtures.items():
        row = analyze_family(facets)
        row["literal_barycentric"] = literal_barycentric_audit(facets)
        rows[name] = row
    require(rows["minimal_five_facet_defect"]["kappa"] == 1,
            "five-facet adversary lost")
    require(rows["projective_plane"]["kappa"] == 3,
            "projective-plane defect changed")
    require(rows["defect_plus_disjoint_facet"]["kappa"] == 1,
            "component additivity failed")

    malformed = [[], [(0, 1)], [(0, 0, 1)],
                 [(0, 1, 2), (2, 1, 0)],
                 [(0, 1, 2), (0, 1, 3), (0, 1, 4)]]
    rejected = 0
    for facets in malformed:
        try:
            normalize(facets)
        except RuntimeError:
            rejected += 1
    require(rejected == len(malformed), "malformed input accepted")

    # When three facets share one edge, eight explicit graph edges cover all
    # eighteen flags, disproving the 3f covering formula outside the premise.
    book = normalize([(0, 1, 2), (0, 1, 3), (0, 1, 4)], False)
    book_faces = set()
    for facet in book:
        book_faces |= nonempty_subfaces(facet)
    common = frozenset((0, 1))
    cover = {
        frozenset((frozenset((vertex,)), common)) for vertex in (0, 1)
    }
    for facet in book:
        third = next(vertex for vertex in facet if vertex not in (0, 1))
        facet_face = frozenset(facet)
        for endpoint in (0, 1):
            cover.add(frozenset((frozenset((endpoint, third)), facet_face)))
    flags = []
    for facet in book:
        for edge in combinations(facet, 2):
            for vertex in edge:
                triangle = (frozenset((vertex,)), frozenset(edge), frozenset(facet))
                flags.append({frozenset(pair) for pair in combinations(triangle, 2)})
    require(len(cover) == 8 and all(cover & triangle for triangle in flags),
            "three-page book counterexample failed")
    return {"fixtures": rows, "malformed_rejections": rejected,
            "three_page_book_cover": 8, "false_3f_value": 9}


def main():
    evidence = {
        "six_label_exhaustive": enumerate_six_label_families(),
        "local_side_patterns": local_completion_audit(),
        "adversarial": fixtures_and_failures(),
    }
    canonical = json.dumps(evidence, sort_keys=True, separators=(",", ":")).encode()
    output = {
        "status": "VERIFIED",
        "evidence_sha256": sha256(canonical).hexdigest(),
        "evidence": evidence,
    }
    print(json.dumps(output, sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
