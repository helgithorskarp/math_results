#!/usr/bin/env python3
"""Independent audit of the cyclic toroidal K_{2,4} thrackle.

This script deliberately does not read the contributor's certificate or import
their constructor/verifier.  It regenerates the rotation system directly from
the displayed cyclic formulas, then uses dart permutations and bit-set
elimination over F_2.
"""

from __future__ import annotations

import hashlib
import itertools
import json
from collections import Counter
from functools import reduce


def edge_name(kind: str, i: int) -> str:
    return f"{kind}{i}"


def crossing(i: int, j: int) -> str:
    return f"x{i}{j}"


def rotate_to_minimum(cycle):
    """Canonicalize a directed cyclic word without reversing its orientation."""
    words = [tuple(cycle[k:] + cycle[:k]) for k in range(len(cycle))]
    return min(words)


def xor_rank(rows):
    """Rank and echelon basis of integer bit vectors over F_2."""
    basis = {}
    for row in rows:
        value = row
        while value:
            pivot = value.bit_length() - 1
            if pivot not in basis:
                basis[pivot] = value
                break
            value ^= basis[pivot]
    return len(basis), basis


def reduce_mod_span(value, basis):
    while value:
        pivot = value.bit_length() - 1
        if pivot not in basis:
            break
        value ^= basis[pivot]
    return value


def make_diagram(indices, mutation=None):
    """Build paths and rotations from the proof's formulas, restricted to indices."""
    indices = tuple(sorted(indices))
    active = set(indices)
    omit = mutation[1] if mutation and mutation[0] == "omit_crossing" else None

    routes = {}
    for i in indices:
        e_crossings = [crossing(i, (i + step) % 4) for step in (2, 3, 1)]
        f_crossings = [crossing((i + step) % 4, i) for step in (1, 3, 2)]
        e_crossings = [
            x for x in e_crossings
            if int(x[2]) in active and (int(x[1]), int(x[2])) != omit
        ]
        f_crossings = [
            x for x in f_crossings
            if int(x[1]) in active and (int(x[1]), int(x[2])) != omit
        ]
        routes[edge_name("e", i)] = ["u", *e_crossings, f"w{i}"]
        routes[edge_name("f", i)] = ["v", *f_crossings, f"w{i}"]

    if mutation and mutation[0] == "swap_route":
        route = routes[mutation[1]]
        route[1], route[2] = route[2], route[1]

    rotations = {
        "u": [routes[edge_name("e", i)][1] for i in indices],
        "v": [routes[edge_name("f", i)][1] for i in indices],
    }
    for i in indices:
        rotations[f"w{i}"] = [
            routes[edge_name("e", i)][-2],
            routes[edge_name("f", i)][-2],
        ]

    present_crossings = sorted(
        {vertex for route in routes.values() for vertex in route if vertex[0] == "x"}
    )
    for x in present_crossings:
        i, j = int(x[1]), int(x[2])
        e_route, f_route = routes[edge_name("e", i)], routes[edge_name("f", j)]
        if x not in e_route or x not in f_route:
            raise AssertionError(f"crossing {x} occurs on only one route")
        ep, fp = e_route.index(x), f_route.index(x)
        a, b = e_route[ep - 1], e_route[ep + 1]
        c, d = f_route[fp - 1], f_route[fp + 1]
        rotations[x] = [a, d, b, c] if (j - i) % 4 == 1 else [a, c, b, d]

    if mutation:
        kind = mutation[0]
        if kind == "nonalternating":
            x = mutation[1]
            a, d, b, c = rotations[x]
            rotations[x] = [a, b, d, c]
        elif kind == "flip_crossing":
            x = mutation[1]
            a, second, b, fourth = rotations[x]
            rotations[x] = [a, fourth, b, second]
        elif kind == "reverse_hub":
            rotations[mutation[1]].reverse()
        elif kind not in {"omit_crossing", "swap_route"}:
            raise ValueError(kind)

    return indices, routes, rotations


def graph_data(routes, rotations):
    segment_owner = {}
    for owner, route in routes.items():
        if len(route) != len(set(route)):
            raise AssertionError(f"original edge {owner} repeats a planarization vertex")
        for a, b in zip(route, route[1:]):
            segment = tuple(sorted((a, b)))
            if segment in segment_owner:
                raise AssertionError(f"planarization segment {segment} has two owners")
            segment_owner[segment] = owner

    neighbors = {vertex: [] for vertex in rotations}
    for a, b in segment_owner:
        if a not in neighbors or b not in neighbors:
            raise AssertionError(f"missing rotation at endpoint of {(a, b)}")
        neighbors[a].append(b)
        neighbors[b].append(a)
    for vertex, rotation in rotations.items():
        if len(rotation) != len(set(rotation)) or set(rotation) != set(neighbors[vertex]):
            raise AssertionError(f"rotation does not equal incident darts at {vertex}")
    return segment_owner


def face_cycles(rotations, segments):
    successor = {}
    for vertex, rotation in rotations.items():
        for k, neighbor in enumerate(rotation):
            successor[(neighbor, vertex)] = (vertex, rotation[(k + 1) % len(rotation)])

    darts = {(a, b) for segment in segments for a, b in (segment, segment[::-1])}
    if set(successor) != darts or set(successor.values()) != darts:
        raise AssertionError("face map is not a permutation of all directed segments")

    unseen, faces = set(darts), []
    while unseen:
        start = min(unseen)
        face, dart = [], start
        while dart in unseen:
            unseen.remove(dart)
            face.append(dart[0])
            dart = successor[dart]
        if dart != start:
            raise AssertionError("face walk merged into an earlier orbit")
        faces.append(rotate_to_minimum(face))
    return tuple(sorted(faces))


def shift_vertex(vertex, amount):
    if vertex in {"u", "v"}:
        return vertex
    if vertex.startswith("w"):
        return f"w{(int(vertex[1]) + amount) % 4}"
    if vertex.startswith("x"):
        return crossing((int(vertex[1]) + amount) % 4,
                        (int(vertex[2]) + amount) % 4)
    raise ValueError(vertex)


def proof_face_table():
    """Expand the four orbit representatives printed in the prose proof."""
    representatives = [
        (4, ["u", "x02", "x12", "w1", "x31"]),
        (4, ["x02", "x03", "v", "x10", "x12"]),
        (4, ["x03", "x02", "w2", "x23"]),
        (2, ["x01", "x03", "x23", "x21"]),
    ]
    expanded = set()
    observed_orbit_sizes = []
    for claimed_size, representative in representatives:
        orbit = {
            rotate_to_minimum([shift_vertex(vertex, amount) for vertex in representative])
            for amount in range(4)
        }
        observed_orbit_sizes.append(len(orbit))
        if len(orbit) != claimed_size:
            raise AssertionError("claimed face-orbit size is wrong")
        expanded.update(orbit)
    if len(expanded) != 14:
        raise AssertionError("proof face table does not contain fourteen distinct walks")
    return tuple(sorted(expanded)), observed_orbit_sizes


def expected_pair_meeting(first, second):
    a, i = first[0], int(first[1:])
    b, j = second[0], int(second[1:])
    if a == b == "e":
        return {"u"}
    if a == b == "f":
        return {"v"}
    if a == "f":
        a, b, i, j = b, a, j, i
    return {f"w{i}"} if i == j else {crossing(i, j)}


def crossing_alternates(x, rotations, routes):
    owners = []
    for neighbor in rotations[x]:
        segment = tuple(sorted((x, neighbor)))
        owner = next(
            edge for edge, route in routes.items()
            if any(tuple(sorted(pair)) == segment for pair in zip(route, route[1:]))
        )
        owners.append(owner[0])
    return all(owners[k] != owners[(k + 1) % 4] for k in range(4))


def boundary_rows(faces, segment_index):
    rows = []
    for face in faces:
        bits = 0
        for a, b in zip(face, face[1:] + face[:1]):
            bits ^= 1 << segment_index[tuple(sorted((a, b)))]
        rows.append(bits)
    return rows


def homology_audit(indices, routes, faces, segment_index):
    face_rank, boundary_basis = xor_rank(boundary_rows(faces, segment_index))
    vertices = {v for route in routes.values() for v in route}
    adjacency = {vertex: set() for vertex in vertices}
    for a, b in segment_index:
        adjacency[a].add(b)
        adjacency[b].add(a)
    unseen, component_count = set(vertices), 0
    while unseen:
        component_count += 1
        stack = [unseen.pop()]
        while stack:
            for neighbor in adjacency[stack.pop()]:
                if neighbor in unseen:
                    unseen.remove(neighbor)
                    stack.append(neighbor)
    v_count, e_count, f_count = len(vertices), len(segment_index), len(faces)
    d1_rank = v_count - component_count
    betti = [component_count, e_count - d1_rank - face_rank, f_count - face_rank]

    base = indices[0]
    path_vectors = {}
    for i in indices:
        bits = 0
        for owner in (edge_name("e", i), edge_name("f", i)):
            for a, b in zip(routes[owner], routes[owner][1:]):
                bits ^= 1 << segment_index[tuple(sorted((a, b)))]
        path_vectors[i] = bits
    relative = {
        i: reduce_mod_span(path_vectors[i] ^ path_vectors[base], boundary_basis)
        for i in indices
    }
    return betti, face_rank, relative, boundary_basis


def audit(indices, mutation=None, require_thrackle=True):
    indices, routes, rotations = make_diagram(indices, mutation)
    segments = graph_data(routes, rotations)

    edge_pairs = list(itertools.combinations(sorted(routes), 2))
    bad_pairs = []
    for first, second in edge_pairs:
        actual = set(routes[first]) & set(routes[second])
        expected = expected_pair_meeting(first, second)
        if actual != expected:
            bad_pairs.append((first, second, sorted(actual), sorted(expected)))

    x_vertices = sorted(vertex for vertex in rotations if vertex.startswith("x"))
    bad_crossings = [x for x in x_vertices if not crossing_alternates(x, rotations, routes)]
    if require_thrackle and (bad_pairs or bad_crossings):
        reason = "pair incidence" if bad_pairs else "nonalternating crossing"
        raise AssertionError(reason)

    faces = face_cycles(rotations, segments)
    segment_index = {segment: k for k, segment in enumerate(sorted(segments))}
    betti, face_rank, relative, boundary_basis = homology_audit(
        indices, routes, faces, segment_index
    )
    chi = len(rotations) - len(segments) + len(faces)
    if chi % 2:
        raise AssertionError("closed orientable ribbon surface has odd Euler characteristic")
    genus = 1 - chi // 2
    if betti != [1, 2 * genus, 1]:
        raise AssertionError("cellular homology disagrees with Euler genus")

    face_words = ["-".join(face) for face in faces]
    digest = hashlib.sha256("\n".join(face_words).encode()).hexdigest()
    return {
        "indices": list(indices),
        "vertices": len(rotations),
        "segments": len(segments),
        "faces": len(faces),
        "face_lengths": dict(sorted(Counter(map(len, faces)).items())),
        "face_digest_sha256": digest,
        "euler_characteristic": chi,
        "genus": genus,
        "betti_f2": betti,
        "boundary_rank_f2": face_rank,
        "relative_class_remainders": {str(i): hex(relative[i]) for i in indices},
        "relative_classes_distinct": len(set(relative.values())) == len(indices),
        "relative_classes_xor_zero": reduce_mod_span(
            reduce(int.__xor__, relative.values(), 0),
            boundary_basis,
        ) == 0,
        "edge_pairs": len(edge_pairs),
        "bad_pair_incidence_count": len(bad_pairs),
        "bad_crossing_count": len(bad_crossings),
    }


def tiny_ribbon_self_tests():
    path_rotations = {"a": ["b"], "b": ["a", "c"], "c": ["b"]}
    path_segments = {("a", "b"): "ab", ("b", "c"): "bc"}
    path_faces = face_cycles(path_rotations, path_segments)
    assert len(path_faces) == 1 and len(path_faces[0]) == 4

    triangle_rotations = {"a": ["b", "c"], "b": ["c", "a"], "c": ["a", "b"]}
    triangle_segments = {("a", "b"): "ab", ("a", "c"): "ac", ("b", "c"): "bc"}
    triangle_faces = face_cycles(triangle_rotations, triangle_segments)
    assert sorted(map(len, triangle_faces)) == [3, 3]
    return {"path_tree": {"V": 3, "E": 2, "F": 1, "genus": 0},
            "triangle": {"V": 3, "E": 3, "F": 2, "genus": 0}}


def finite_space_self_test():
    maxima = {}
    for dimension in (0, 2, 4):
        vectors = range(1 << dimension)
        maxima[str(dimension)] = len(set(vectors))
        assert maxima[str(dimension)] == 2 ** dimension
    equality_ok = True
    vectors = (0, 1, 2, 3)
    for ordering in itertools.permutations(vectors):
        if ordering[0] ^ ordering[1] != ordering[2] ^ ordering[3]:
            equality_ok = False
            break
    assert equality_ok
    return {"maximum_distinct_vectors_by_dimension": maxima,
            "all_24_torus_orderings_have_complementary_pair_equality": equality_ok}


def main():
    tiny = tiny_ribbon_self_tests()
    finite = finite_space_self_test()

    subdrawings = {}
    for size in range(1, 5):
        audits = [audit(subset) for subset in itertools.combinations(range(4), size)]
        expected_genus = 0 if size == 1 else 1
        assert all(item["genus"] == expected_genus for item in audits)
        assert all(item["relative_classes_distinct"] for item in audits)
        subdrawings[str(size)] = {
            "subset_count": len(audits),
            "genera": sorted({item["genus"] for item in audits}),
            "face_counts": sorted({item["faces"] for item in audits}),
            "all_pair_incidence_checks_pass": all(not item["bad_pair_incidence_count"] for item in audits),
            "all_crossing_alternation_checks_pass": all(not item["bad_crossing_count"] for item in audits),
        }

    full = audit(range(4))
    assert (full["vertices"], full["segments"], full["faces"], full["genus"]) == (18, 32, 14, 1)
    assert full["face_lengths"] == {4: 6, 5: 8}
    assert full["edge_pairs"] == 28
    assert full["relative_classes_distinct"] and full["relative_classes_xor_zero"]
    _, full_routes, full_rotations = make_diagram(range(4))
    reconstructed_faces = face_cycles(full_rotations, graph_data(full_routes, full_rotations))
    printed_faces, orbit_sizes = proof_face_table()
    assert reconstructed_faces == printed_faces

    mutations = {}
    for name, mutation in {
        "nonalternating_x01": ("nonalternating", "x01"),
        "omitted_independent_pair_x01": ("omit_crossing", (0, 1)),
    }.items():
        try:
            audit(range(4), mutation)
        except AssertionError as error:
            mutations[name] = {"rejected": True, "reason": str(error)}
        else:
            raise AssertionError(f"mutation {name} unexpectedly passed")

    for name, mutation in {
        "alternate_but_flipped_x01": ("flip_crossing", "x01"),
        "reversed_u_rotation": ("reverse_hub", "u"),
        "swapped_first_two_crossings_on_e0": ("swap_route", "e0"),
    }.items():
        mutated = audit(range(4), mutation)
        assert mutated["genus"] != 1 or mutated["face_digest_sha256"] != full["face_digest_sha256"]
        mutations[name] = {
            "still_local_thrackle_data": True,
            "genus": mutated["genus"],
            "faces": mutated["faces"],
            "face_digest_changed": mutated["face_digest_sha256"] != full["face_digest_sha256"],
        }

    report = {
        "schema": "independent-torus-thrackle-review-v1",
        "reads_contributor_certificate": False,
        "tiny_ribbon_self_tests": tiny,
        "finite_vector_space_self_test": finite,
        "all_induced_subdrawings": subdrawings,
        "full_k24": full,
        "printed_face_table": {
            "matches_reconstructed_faces_exactly": True,
            "orbit_sizes": orbit_sizes,
            "directed_darts_covered": sum(map(len, printed_faces)),
        },
        "adversarial_mutations": mutations,
    }
    print(json.dumps(report, sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
