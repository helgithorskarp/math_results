#!/usr/bin/env python3
"""Independent exact audit of the total-graph fixed-point theorem.

CPython 3.11+, standard library only.  This checker imports no target code,
fixtures, or expected output.  It exhausts every labelled simple graph on at
most five vertices and every subgroup of its full automorphism group.  Fixed
spaces are constructed directly from invariant barycentric supports, and
their F_2 homology is compared with the representation-sphere prediction.

The finite census corroborates the fragile reductions and smallest cases; it
does not prove the universal equivariant homotopy equivalence.
"""

from collections import Counter, deque
from hashlib import sha256
from itertools import combinations, permutations, product
import argparse
import json
from pathlib import Path


def require(condition, message):
    if not condition:
        raise ValueError(message)


def edge_set(edges):
    return frozenset(tuple(sorted(edge)) for edge in edges)


def compose(left, right):
    """Permutation composition left after right."""
    return tuple(left[right[i]] for i in range(len(left)))


def parity(values):
    return sum(values[i] > values[j]
               for i in range(len(values)) for j in range(i + 1, len(values))) % 2


def oriented(face):
    require(len(set(face)) == len(face), "repeated oriented vertex")
    return tuple(sorted(face)), -1 if parity(face) else 1


def generated_subgroup(n, generators):
    identity = tuple(range(n))
    generators = tuple(dict.fromkeys(generators))
    seen = {identity}
    queue = deque([identity])
    while queue:
        current = queue.popleft()
        for generator in generators:
            candidate = compose(generator, current)
            if candidate not in seen:
                seen.add(candidate)
                queue.append(candidate)
    return frozenset(seen)


def all_subgroups(group):
    n = len(next(iter(group)))
    identity = tuple(range(n))
    start = frozenset((identity,))
    known = {start}
    queue = deque([start])
    ordered_group = tuple(sorted(group))
    while queue:
        subgroup = queue.popleft()
        for generator in ordered_group:
            if generator in subgroup:
                continue
            enlarged = generated_subgroup(n, tuple(subgroup) + (generator,))
            if enlarged not in known:
                require(enlarged <= group, "generated elements left automorphism group")
                known.add(enlarged)
                queue.append(enlarged)
    return tuple(sorted(known, key=lambda h: (len(h), tuple(sorted(h)))))


def automorphisms(n, edges):
    answer = []
    for permutation in permutations(range(n)):
        image = edge_set((permutation[u], permutation[v]) for u, v in edges)
        if image == edges:
            answer.append(permutation)
    return frozenset(answer)


def adjacency(n, edges):
    result = [set() for _ in range(n)]
    for u, v in edges:
        result[u].add(v)
        result[v].add(u)
    return result


def is_clique(vertices, adjacent):
    return all(v in adjacent[u] for u, v in combinations(vertices, 2))


def clique_faces(n, edges):
    """All nonempty cliques, grouped by dimension."""
    adjacent = adjacency(n, edges)
    levels = []

    def extend(prefix, candidates):
        for index, vertex in enumerate(candidates):
            face = prefix + (vertex,)
            while len(levels) < len(face):
                levels.append([])
            levels[len(face) - 1].append(face)
            extend(face, tuple(other for other in candidates[index + 1:]
                               if other in adjacent[vertex]))

    extend((), tuple(range(n)))
    return levels


def permutation_orbits(n, group):
    unseen = set(range(n))
    answer = []
    while unseen:
        seed = min(unseen)
        orbit = frozenset(permutation[seed] for permutation in group)
        require(orbit <= unseen, "orbit partition overlap")
        unseen -= orbit
        answer.append(tuple(sorted(orbit)))
    return tuple(answer)


def fixed_support_faces(n, edges, group):
    """Clique-orbit support model of the geometric fixed space."""
    adjacent = adjacency(n, edges)
    orbits = tuple(orbit for orbit in permutation_orbits(n, group)
                   if is_clique(orbit, adjacent))
    support_edges = []
    for i, j in combinations(range(len(orbits)), 2):
        if is_clique(orbits[i] + orbits[j], adjacent):
            support_edges.append((i, j))
    return clique_faces(len(orbits), edge_set(support_edges))


def rank_binary(columns):
    pivots = {}
    for value in columns:
        while value:
            pivot = value.bit_length() - 1
            if pivot not in pivots:
                pivots[pivot] = value
                break
            value ^= pivots[pivot]
    return len(pivots)


def betti_mod_two(levels):
    if not levels:
        return ()
    ranks = [0]
    for dimension in range(1, len(levels)):
        row = {face: index for index, face in enumerate(levels[dimension - 1])}
        columns = []
        for face in levels[dimension]:
            value = 0
            for index in range(len(face)):
                value ^= 1 << row[face[:index] + face[index + 1:]]
            columns.append(value)
        ranks.append(rank_binary(columns))
    ranks.append(0)
    answer = [len(levels[k]) - ranks[k] - ranks[k + 1]
              for k in range(len(levels))]
    require(all(value >= 0 for value in answer), "negative Betti number")
    while answer and answer[-1] == 0:
        answer.pop()
    return tuple(answer)


def graph_triangles(n, edges):
    adjacent = adjacency(n, edges)
    return tuple(triangle for triangle in combinations(range(n), 3)
                 if is_clique(triangle, adjacent))


def total_graph(n, edges, group):
    ordered_edges = tuple(sorted(edges))
    edge_index = {edge: n + index for index, edge in enumerate(ordered_edges)}
    total_edges = set(edges)
    for edge in ordered_edges:
        for vertex in edge:
            total_edges.add(tuple(sorted((vertex, edge_index[edge]))))
    for left, right in combinations(ordered_edges, 2):
        if set(left) & set(right):
            total_edges.add((edge_index[left], edge_index[right]))
    induced = {}
    for permutation in group:
        image = list(permutation)
        image.extend(edge_index[tuple(sorted((permutation[u], permutation[v])))]
                     for u, v in ordered_edges)
        induced[permutation] = tuple(image)
    return n + len(ordered_edges), edge_set(total_edges), ordered_edges, edge_index, induced


def triangle_orbit_counts(triangles, group):
    vertex_count = len(next(iter(group)))
    global_orbits = permutation_orbits(vertex_count, group)
    counts = [0, 0, 0]
    for triangle in triangles:
        triangle_set = set(triangle)
        if all({permutation[v] for v in triangle} == triangle_set
               for permutation in group):
            number = sum(bool(triangle_set & set(orbit)) for orbit in global_orbits)
            require(1 <= number <= 3, "wrong invariant-triangle orbit count")
            counts[number - 1] += 1
    return tuple(counts)


def audit_face_classification(n, edges, total_n, total_edges, ordered_edges):
    """Check every clique against the four human face types."""
    edge_of_vertex = {n + index: edge for index, edge in enumerate(ordered_edges)}
    triangles = {frozenset(triangle) for triangle in graph_triangles(n, edges)}
    faces = clique_faces(total_n, total_edges)
    face_count = 0
    deleted_count = 0
    for level in faces:
        for face in level:
            face_count += 1
            originals = tuple(v for v in face if v < n)
            represented = tuple(edge_of_vertex[v] for v in face if v >= n)
            in_original = not represented
            in_incidence = (len(originals) == 2 and len(represented) == 1
                            and frozenset(originals) == frozenset(represented[0]))
            common_star = any(set(originals) <= {center}
                              and all(center in edge for edge in represented)
                              for center in range(n))
            deleted = (not originals and len(represented) == 3
                       and frozenset(v for edge in represented for v in edge)
                       in triangles)
            require(in_original or in_incidence or common_star or deleted,
                    ("unclassified total-graph clique", n, edges, face))
            if deleted:
                deleted_count += 1
                face_set = set(face)
                require(not any(face_set < set(superface)
                                for later in faces[len(face):]
                                for superface in later),
                        "edge-only triangle is not maximal")
    require(deleted_count == len(triangles), "deleted triangle count mismatch")
    return face_count


def boundary(chain):
    result = Counter()
    for face, coefficient in chain.items():
        for index in range(len(face)):
            result[face[:index] + face[index + 1:]] += coefficient * (-1) ** index
    return {face: coefficient for face, coefficient in result.items() if coefficient}


def octahedral_cycle(triangle, edge_index):
    opposite = [edge_index[tuple(v for v in triangle if v != triangle[i])]
                for i in range(3)]
    answer = Counter()
    for choices in product((0, 1), repeat=3):
        raw = tuple(opposite[i] if choices[i] else triangle[i] for i in range(3))
        face, sign = oriented(raw)
        answer[face] += sign * (-1) ** (3 - sum(choices))
    return {face: coefficient for face, coefficient in answer.items() if coefficient}


def audit_integral_signs(n, edges, group, total_edges, edge_index, induced):
    adjacent = adjacency(n + len(edges), total_edges)
    cycles = {triangle: octahedral_cycle(triangle, edge_index)
              for triangle in graph_triangles(n, edges)}
    sign_checks = 0
    for triangle, chain in cycles.items():
        require(not boundary(chain), "octahedral chain has nonzero boundary")
        require(all(is_clique(face, adjacent) for face in chain),
                "octahedral chain uses a nonface")
        edge_face, edge_sign = oriented(tuple(
            edge_index[tuple(v for v in triangle if v != triangle[i])]
            for i in range(3)))
        require(chain.get(edge_face) == edge_sign,
                "relative edge-only coefficient is not one")
        for permutation in group:
            mapped = Counter()
            for face, coefficient in chain.items():
                image, face_sign = oriented(tuple(induced[permutation][v] for v in face))
                mapped[image] += coefficient * face_sign
            target_triangle, triangle_sign = oriented(tuple(permutation[v]
                                                          for v in triangle))
            expected = cycles[target_triangle]
            mapped = {face: coefficient for face, coefficient in mapped.items()
                      if coefficient}
            require(mapped == {face: triangle_sign * coefficient
                               for face, coefficient in expected.items()},
                    "signed triangle module action failed")
            sign_checks += 1
    return len(cycles), sign_checks


def predicted_betti(a_betti, counts):
    answer = list(a_betti) + [0] * max(0, 3 - len(a_betti))
    for dimension, number in enumerate(counts):
        answer[dimension] += number
    while answer and answer[-1] == 0:
        answer.pop()
    return tuple(answer)


def encode_group(group):
    return ";".join(",".join(map(str, permutation))
                    for permutation in sorted(group))


def evaluate_case(n, edges, subgroup, total_n, total_edges, triangles, induced):
    induced_subgroup = frozenset(induced[permutation] for permutation in subgroup)
    a_betti = betti_mod_two(fixed_support_faces(n, edges, subgroup))
    x_betti = betti_mod_two(fixed_support_faces(total_n, total_edges,
                                                induced_subgroup))
    counts = triangle_orbit_counts(triangles, subgroup)
    require(x_betti == predicted_betti(a_betti, counts),
            ("fixed-space prediction failed", n, edges, subgroup,
             a_betti, x_betti, counts))
    return a_betti, x_betti, counts


def named_controls():
    cases = []

    def add(name, n, edges, generators, expected_a, expected_x, expected_counts):
        edges = edge_set(edges)
        group = generated_subgroup(n, generators)
        automorphism_group = automorphisms(n, edges)
        require(group <= automorphism_group, name + " has a nonautomorphism")
        total_n, total_edges, _, _, induced = total_graph(n, edges, automorphism_group)
        result = evaluate_case(n, edges, group, total_n, total_edges,
                               graph_triangles(n, edges), induced)
        require(result == (expected_a, expected_x, expected_counts),
                ("named control mismatch", name, result))
        cases.append({"name": name, "A": list(result[0]), "X": list(result[1]),
                      "m1_m2_m3": list(result[2])})

    add("empty_graph", 0, (), ((),), (), (), (0, 0, 0))
    add("K2_endpoint_swap", 2, ((0, 1),), ((1, 0),), (1,), (1,), (0, 0, 0))
    k3 = tuple(combinations(range(3), 2))
    add("K3_trivial", 3, k3, (tuple(range(3)),), (1,), (1, 0, 1), (0, 0, 1))
    add("K3_transposition", 3, k3, ((1, 0, 2),), (1,), (1, 1), (0, 1, 0))
    add("K3_three_cycle", 3, k3, ((1, 2, 0),), (1,), (2,), (1, 0, 0))
    add("K3_full_symmetric", 3, k3, ((1, 0, 2), (1, 2, 0)),
        (1,), (2,), (1, 0, 0))
    two_triangles = tuple(combinations((0, 1, 2), 2)) + tuple(
        combinations((3, 4, 5), 2))
    add("two_triangles_exchanged", 6, two_triangles,
        ((3, 4, 5, 0, 1, 2),), (), (), (0, 0, 0))
    k4 = tuple(combinations(range(4), 2))
    add("K4_three_cycle", 4, k4, ((1, 2, 0, 3),), (1,), (2,), (1, 0, 0))
    diamond = ((0, 1), (0, 2), (1, 2), (0, 3), (1, 3))
    add("diamond_triangle_swap", 4, diamond, ((0, 1, 3, 2),),
        (1,), (1,), (0, 0, 0))
    square = ((0, 1), (1, 2), (2, 3), (0, 3))
    add("C4_reflection", 4, square, ((0, 3, 2, 1),), (2,), (2,), (0, 0, 0))
    return cases


def census(max_vertices):
    digest = sha256()
    subgroup_cache = {}
    statistics = Counter()
    automorphism_histogram = Counter()
    subgroup_histogram = Counter()
    for n in range(max_vertices + 1):
        possible_edges = tuple(combinations(range(n), 2))
        for mask in range(1 << len(possible_edges)):
            edges = edge_set(possible_edges[index]
                             for index in range(len(possible_edges))
                             if mask & (1 << index))
            statistics["labelled_graphs"] += 1
            group = automorphisms(n, edges)
            automorphism_histogram[len(group)] += 1
            cache_key = (n, tuple(sorted(group)))
            if cache_key not in subgroup_cache:
                subgroup_cache[cache_key] = all_subgroups(group)
            subgroups = subgroup_cache[cache_key]
            subgroup_histogram[len(subgroups)] += 1
            total_n, total_edges, ordered_edges, edge_index, induced = total_graph(
                n, edges, group)
            statistics["total_graph_faces"] += audit_face_classification(
                n, edges, total_n, total_edges, ordered_edges)
            cycles, signs = audit_integral_signs(
                n, edges, group, total_edges, edge_index, induced)
            statistics["integer_cycles"] += cycles
            statistics["integer_sign_checks"] += signs
            triangles = graph_triangles(n, edges)
            for subgroup in subgroups:
                a_betti, x_betti, counts = evaluate_case(
                    n, edges, subgroup, total_n, total_edges, triangles, induced)
                statistics["graph_subgroup_pairs"] += 1
                record = (n, mask, encode_group(subgroup), a_betti, x_betti, counts)
                digest.update((repr(record) + "\n").encode())
    return {
        "max_vertices": max_vertices,
        "labelled_graphs": statistics["labelled_graphs"],
        "graph_subgroup_pairs": statistics["graph_subgroup_pairs"],
        "total_graph_faces_classified": statistics["total_graph_faces"],
        "integer_cycles_checked": statistics["integer_cycles"],
        "integer_sign_checks": statistics["integer_sign_checks"],
        "entry_digest_sha256": digest.hexdigest(),
        "automorphism_order_histogram": {str(key): automorphism_histogram[key]
                                         for key in sorted(automorphism_histogram)},
        "subgroup_count_histogram": {str(key): subgroup_histogram[key]
                                     for key in sorted(subgroup_histogram)},
    }


def run(max_vertices):
    require(max_vertices == 5, "frozen audit requires --max-vertices 5")
    return {
        "schema": 1,
        "method": "all labelled simple graphs and every automorphism subgroup",
        "coefficient_field": 2,
        "census": census(max_vertices),
        "named_controls": named_controls(),
        "trust_boundary": (
            "Finite exact corroboration; the universal equivariant homotopy "
            "equivalence rests on the reviewed human proof."),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--max-vertices", type=int, default=5)
    parser.add_argument("--emit", action="store_true")
    args = parser.parse_args()
    result = run(args.max_vertices)
    if args.emit:
        print(json.dumps(result, indent=2, sort_keys=True))
        return
    expected_path = Path(__file__).with_name("expected.json")
    expected = json.loads(expected_path.read_text())
    require(result == expected, "frozen expected output mismatch")
    print(json.dumps({
        "status": "PASS",
        "labelled_graphs": result["census"]["labelled_graphs"],
        "graph_subgroup_pairs": result["census"]["graph_subgroup_pairs"],
        "entry_digest_sha256": result["census"]["entry_digest_sha256"],
        "expected_sha256": sha256(expected_path.read_bytes()).hexdigest(),
    }, sort_keys=True))


if __name__ == "__main__":
    main()
