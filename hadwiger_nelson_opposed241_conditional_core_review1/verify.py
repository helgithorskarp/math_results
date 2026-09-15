#!/usr/bin/env python3
"""Independent exact review of the opposed-B214 241-point conditional core.

The target's four-coefficient norm test and singleton-domain search are not
imported.  Geometry is rebuilt in an eight-term multiquadratic basis, while
conditional colourability is decided by direct DSATUR assignment search.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from itertools import combinations, product
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
TARGET = ROOT / "hadwiger_nelson_opposed241_conditional_core"
B_SOURCE = ROOT / "hadwiger_nelson_nonmono159_214_lowden2/points214.tsv"
PARTS_SOURCE = ROOT / "hadwiger_nelson_parts373_receiver_relation/points.tsv"

PINNED = {
    TARGET / "certificate.json":
        "37e1397276f931ee1b9b63f4ca5c343a2ac129fa3b1c6d526e4c151031a750e4",
    B_SOURCE:
        "97c9b3a964ed19874ae3fe932eb8c085fd637f618d2481fffaebbd1fbae55c2f",
    PARTS_SOURCE:
        "f69ce1adef2f47c666f57c5e2096cb766fbc16654d75e3b24fbf0f5913d5be50",
}

PRIMES = (3, 5, 11)
BASIS_SIZE = 8
SCALE = 36
UNIT_SQUARED = (SCALE * SCALE,) + (0,) * 7
BAD = "0121212203"
COLOUR_ORDER = (3, 1, 0, 2)


def need(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def stream_hash(rows) -> str:
    return sha256(("\n".join(rows) + "\n").encode("ascii"))


def basis_product(first: int, second: int) -> tuple[int, int]:
    common = first & second
    coefficient = 1
    for bit, prime in enumerate(PRIMES):
        if common & (1 << bit):
            coefficient *= prime
    return coefficient, first ^ second


PRODUCT_TABLE = tuple(
    tuple(basis_product(first, second) for second in range(BASIS_SIZE))
    for first in range(BASIS_SIZE)
)


def multiply(first: tuple[int, ...], second: tuple[int, ...]) -> tuple[int, ...]:
    out = [0] * BASIS_SIZE
    for i, a in enumerate(first):
        if not a:
            continue
        for j, b in enumerate(second):
            if b:
                factor, mask = PRODUCT_TABLE[i][j]
                out[mask] += factor * a * b
    return tuple(out)


def squared_distance(first, second) -> tuple[int, ...]:
    dx = tuple(a - b for a, b in zip(first[0], second[0], strict=True))
    dy = tuple(a - b for a, b in zip(first[1], second[1], strict=True))
    xx = multiply(dx, dx)
    yy = multiply(dy, dy)
    return tuple(a + b for a, b in zip(xx, yy, strict=True))


def exact_edges(points) -> list[tuple[int, int]]:
    return [
        (first, second)
        for first, second in combinations(range(len(points)), 2)
        if squared_distance(points[first], points[second]) == UNIT_SQUARED
    ]


def flat_point(row: tuple[int, int, int, int]):
    a, b, c, d = row
    x = [0] * BASIS_SIZE
    y = [0] * BASIS_SIZE
    x[0], x[5] = a, b
    y[1], y[4] = c, d
    return tuple(x), tuple(y)


def golomb():
    rows = (
        (0, 0, 0, 0), (36, 0, 0, 0), (18, 0, 18, 0),
        (-18, 0, 18, 0), (-36, 0, 0, 0), (-18, 0, -18, 0),
        (18, 0, -18, 0), (6, 0, 0, 6), (-3, -3, 3, -3),
        (-3, 3, -3, -3),
    )
    return [flat_point(row) for row in rows]


def read_b214():
    points = []
    for line in B_SOURCE.read_text(encoding="ascii").splitlines():
        if not line or line.startswith("#"):
            continue
        row = tuple(map(int, line.split()))
        need(len(row) == 16, "B214 coordinate arity")
        need(all(row[i] == 0 for i in range(16)
                 if i not in (0, 5, 9, 12)), "B214 point outside E")
        points.append((tuple(3 * value for value in row[:8]),
                       tuple(3 * value for value in row[8:])))
    need(len(points) == 214 and len(set(points)) == 214, "B214 order")
    return points


def shift_b214(points, reflected: bool):
    out = []
    for x, y in points:
        xx = tuple(-value for value in x) if reflected else x
        translation = 18 if reflected else -18
        xx = (xx[0] + translation,) + xx[1:]
        out.append((xx, y))
    return out


def merge_blocks(*blocks):
    points = []
    index = {}
    maps = []
    for block in blocks:
        image = []
        for point in block:
            if point not in index:
                index[point] = len(points)
                points.append(point)
            image.append(index[point])
        maps.append(image)
    return points, maps


def target_point_hash(points) -> str:
    order = (0, 1, 4, 5)
    need(all(axis[i] == 0 for point in points for axis in point
             for i in range(BASIS_SIZE) if i not in order),
         "point outside target four-term subbasis")
    return stream_hash(
        " ".join(map(str,
                     tuple(point[0][i] for i in order)
                     + tuple(point[1][i] for i in order)))
        for point in points
    )


def edge_hash(edges) -> str:
    return stream_hash(f"{first} {second}" for first, second in edges)


def proper(word: str, vertices: int, edges, omitted=None) -> bool:
    if not isinstance(word, str) or len(word) != vertices:
        return False
    for vertex, colour in enumerate(word):
        if vertex == omitted:
            if colour != "-":
                return False
        elif colour not in "0123":
            return False
    return all(first == omitted or second == omitted
               or word[first] != word[second] for first, second in edges)


def adjacency(vertices: int, edges):
    out = [set() for _ in range(vertices)]
    for first, second in edges:
        out[first].add(second)
        out[second].add(first)
    return out


def canonical_golomb_patterns(edges):
    patterns = []
    for tail in product(range(4), repeat=7):
        word = (0, 1, 2) + tail
        if all(word[first] != word[second] for first, second in edges):
            patterns.append("".join(map(str, word)))
    return patterns


def colour_dsat(vertices: int, edges, pins, drop=None):
    """Exhaustive direct-assignment search; DSATUR affects order only."""
    kept = [edge for edge in edges if edge != drop]
    adj = adjacency(vertices, kept)
    colours = [-1] * vertices
    used = [0] * vertices
    nodes = 0

    for vertex, colour in pins.items():
        need(0 <= vertex < vertices and 0 <= colour < 4, "pin range")
        need(colours[vertex] in (-1, colour), "contradictory pins")
        colours[vertex] = colour
    if any(colours[first] == colours[second] != -1 for first, second in kept):
        return None, 0
    for vertex, colour in enumerate(colours):
        if colour < 0:
            continue
        bit = 1 << colour
        for neighbour in adj[vertex]:
            if colours[neighbour] < 0:
                used[neighbour] |= bit

    def search(remaining):
        nonlocal nodes
        nodes += 1
        if not remaining:
            return True

        selected = -1
        selected_key = None
        for vertex in range(vertices):
            if colours[vertex] >= 0:
                continue
            available = 15 & ~used[vertex]
            if not available:
                return False
            key = (used[vertex].bit_count(), len(adj[vertex]), -vertex)
            if selected_key is None or key > selected_key:
                selected = vertex
                selected_key = key

        for colour in COLOUR_ORDER:
            bit = 1 << colour
            if used[selected] & bit:
                continue
            colours[selected] = colour
            changed = []
            for neighbour in adj[selected]:
                if colours[neighbour] < 0 and not used[neighbour] & bit:
                    used[neighbour] |= bit
                    changed.append(neighbour)
            if search(remaining - 1):
                return True
            for neighbour in changed:
                used[neighbour] &= ~bit
            colours[selected] = -1
        return False

    found = search(sum(colour < 0 for colour in colours))
    word = "".join(map(str, colours)) if found else None
    return word, nodes


def cut_vertices_after(adj, removed):
    vertices = len(adj)
    banned = set(removed)
    discovery = [-1] * vertices
    low = [0] * vertices
    parent = [-1] * vertices
    cuts = set()
    clock = 0
    components = 0

    def visit(vertex):
        nonlocal clock
        discovery[vertex] = low[vertex] = clock
        clock += 1
        children = 0
        for neighbour in adj[vertex]:
            if neighbour in banned:
                continue
            if discovery[neighbour] < 0:
                parent[neighbour] = vertex
                children += 1
                visit(neighbour)
                low[vertex] = min(low[vertex], low[neighbour])
                if parent[vertex] < 0 and children > 1:
                    cuts.add(vertex)
                elif parent[vertex] >= 0 and low[neighbour] >= discovery[vertex]:
                    cuts.add(vertex)
            elif neighbour != parent[vertex]:
                low[vertex] = min(low[vertex], discovery[neighbour])

    for vertex in range(vertices):
        if vertex not in banned and discovery[vertex] < 0:
            components += 1
            visit(vertex)
    return components, cuts


def connectivity_census(vertices: int, edges):
    adj = adjacency(vertices, edges)
    components, articulations = cut_vertices_after(adj, ())
    pair_cuts = []
    triple_cuts = set()
    for first, second in combinations(range(vertices), 2):
        count, cuts = cut_vertices_after(adj, (first, second))
        if count != 1:
            pair_cuts.append((first, second))
        else:
            triple_cuts.update(tuple(sorted((first, second, third)))
                               for third in cuts)
    minimum_degree = min(map(len, adj))
    witness_vertex = min(i for i, row in enumerate(adj)
                         if len(row) == minimum_degree)
    upper_cut = sorted(adj[witness_vertex])
    need(components == 1 and not articulations, "base connectivity")
    need(not pair_cuts and not triple_cuts, "separator below four")
    need(minimum_degree == 4 and len(upper_cut) == 4,
         "four-cut upper bound")
    remaining_components, _ = cut_vertices_after(adj, upper_cut)
    need(remaining_components > 1, "neighbour set is not a four-cut")
    return {
        "vertex_connectivity": 4,
        "articulations": [],
        "pair_separator_candidates_checked": vertices * (vertices - 1) // 2,
        "pair_separators": 0,
        "triple_separator_candidates_covered":
            vertices * (vertices - 1) * (vertices - 2) // 6,
        "triple_separators": 0,
        "four_cut_witness_vertex": witness_vertex,
        "four_cut_witness": upper_cut,
    }


def conditional_cnf(vertices: int, edges, bad=BAD) -> bytes:
    clauses = []
    for vertex in range(vertices):
        clauses.append([4 * vertex + colour + 1 for colour in range(4)])
        clauses.extend([-4 * vertex - first - 1, -4 * vertex - second - 1]
                       for first, second in combinations(range(4), 2))
    clauses.extend([-4 * first - colour - 1, -4 * second - colour - 1]
                   for first, second in edges for colour in range(4))
    clauses.extend([[4 * vertex + int(colour) + 1]
                    for vertex, colour in enumerate(bad)])
    rows = [f"p cnf {4 * vertices} {len(clauses)}"]
    rows.extend(" ".join(map(str, clause)) + " 0" for clause in clauses)
    return ("\n".join(rows) + "\n").encode("ascii")


def native_budget(core_points):
    rows = []
    for line in PARTS_SOURCE.read_text(encoding="ascii").splitlines():
        if not line or line.startswith("#"):
            continue
        row = tuple(map(int, line.split()))
        need(len(row) == 16, "Parts coordinate arity")
        rows.append(row)
    need(len(rows) == 509, "Parts fixture order")
    host_rows = [row for index, row in enumerate(rows[:374]) if index != 310]
    need(len(host_rows) == 373 and len(set(host_rows)) == 373,
         "Parts373 host order")
    need(all(row[index] == 0 for row in host_rows for index in range(16)
             if index not in (0, 5, 9, 12)), "Parts host outside E")

    host_common = {tuple(3 * value for value in row): index
                   for index, row in enumerate(host_rows)}
    core_common = []
    for x, y in core_points:
        core_common.append(tuple(8 * value for value in x + y))
    overlaps = [(index, host_common[row]) for index, row in enumerate(core_common)
                if row in host_common]
    need([host for index, host in overlaps if index < 10]
         == [0, 153, 150, 169, 166, 161, 158, 53, 65, 59],
         "native Golomb role")
    need(len(overlaps) == 137, "native overlap count")
    return {
        "host_points": 373,
        "shared_points": len(overlaps),
        "new_points": len(core_points) - len(overlaps),
        "merged_points": len(host_rows) + len(core_points) - len(overlaps),
        "all_coordinates_in_E": True,
        "receiver_relation_queried": False,
        "closure_uses_reviewed_whole_field_theorem": True,
    }


def run():
    for path, digest in PINNED.items():
        need(sha256(path.read_bytes()) == digest, f"input hash: {path.name}")
    certificate = json.loads((TARGET / "certificate.json").read_text())
    need(certificate.get("schema") == "opposed241-conditional-core-v1",
         "certificate schema")

    g = golomb()
    b214 = read_b214()
    b214_edges = exact_edges(b214)
    need(len(b214_edges) == 977, "B214 edge count")
    left = shift_b214(b214, False)
    right = shift_b214(b214, True)
    source, maps = merge_blocks(g, left, right)
    source_edges = exact_edges(source)
    need((len(source), len(source_edges)) == (343, 1782),
         "opposed-B214 source census")
    need(target_point_hash(source)
         == "8e44b5746cc16badb0ddc6db1bb33d5d64baa088f0715a175632977c5d371a13",
         "source point stream")

    source_ids = certificate["source_ids"]
    need(source_ids == sorted(set(source_ids))
         and source_ids[:10] == list(range(10))
         and len(source_ids) == 241 and source_ids[-1] < len(source),
         "source labels")
    points = [source[index] for index in source_ids]
    edges = exact_edges(points)
    need(len(points) == len(set(points)) == 241 and len(edges) == 991,
         "core geometry")
    point_digest = target_point_hash(points)
    edge_digest = edge_hash(edges)
    need(point_digest == certificate["point_sha256"], "core point stream")
    need(edge_digest == certificate["edge_sha256"], "core edge stream")

    g_edges = exact_edges(g)
    patterns = canonical_golomb_patterns(g_edges)
    need(len(g_edges) == 18 and len(patterns) == 95, "Golomb census")
    need(BAD in patterns and certificate["bad_word"] == BAD, "bad input")
    need(not any(all(word[first] != word[second] for first, second in g_edges)
                 for tail in product(range(3), repeat=7)
                 for word in [(0, 1, 2) + tail]), "Golomb 3-colouring")

    need(proper(certificate["proper4"], 241, edges), "proper four-word")
    need(certificate["proper4"][:10] == "0121212023",
         "surviving complete input")
    need(proper(certificate["proper5"].replace("4", "0"), 241, [])
         and len(certificate["proper5"]) == 241
         and set(certificate["proper5"]) == set("01234")
         and all(certificate["proper5"][first] != certificate["proper5"][second]
                 for first, second in edges), "proper five-word")

    deletion_words = certificate["deletion_words"]
    need(set(deletion_words) == {str(vertex) for vertex in range(10, 241)},
         "private vertex witness labels")
    for vertex in range(10, 241):
        word = deletion_words[str(vertex)]
        need(word[:10] == BAD and proper(word, 241, edges, vertex),
             f"private vertex deletion witness {vertex}")

    source_to_core = {source_id: index
                      for index, source_id in enumerate(source_ids)}
    left_source = set(maps[1])
    right_source = set(maps[2])
    left_core = {source_to_core[index] for index in left_source
                 if index in source_to_core}
    right_core = {source_to_core[index] for index in right_source
                  if index in source_to_core}
    need(left_core | right_core == set(range(241)), "piece union")
    inherited = [edge for edge in edges
                 if ({source_ids[edge[0]], source_ids[edge[1]]} <= left_source
                     or {source_ids[edge[0]], source_ids[edge[1]]} <= right_source)]
    inherited_set = set(inherited)
    contacts = [edge for edge in edges if edge not in inherited_set]
    need((len(left_core), len(right_core), len(left_core & right_core),
          len(contacts)) == (121, 176, 56, 47), "piece/contact census")
    need(all((first in left_core - right_core
              and second in right_core - left_core)
             or (second in left_core - right_core
                 and first in right_core - left_core)
             for first, second in contacts), "private contact endpoints")

    without_contacts = certificate["without_private_contacts_word"]
    need(without_contacts[:10] == BAD
         and proper(without_contacts, 241, inherited),
         "all-contact deletion witness")
    need(any(without_contacts[first] == without_contacts[second]
             for first, second in contacts), "contact witness colors full core")

    for block_index, key in ((1, "isolated_left_word"),
                             (2, "isolated_right_word")):
        word = certificate[key]
        need(proper(word, 214, b214_edges), f"{key} proper")
        inverse_map = {source_vertex: b_vertex
                       for b_vertex, source_vertex in enumerate(maps[block_index])}
        need("".join(word[inverse_map[index]] for index in range(10)) == BAD,
             f"{key} input")

    pins = {vertex: int(colour) for vertex, colour in enumerate(BAD)}
    base_word, base_nodes = colour_dsat(241, edges, pins)
    need(base_word is None, "forbidden input extends to core")

    critical = []
    redundant = []
    witness_rows = []
    deletion_nodes = 0
    for edge in contacts:
        word, nodes = colour_dsat(241, edges, pins, drop=edge)
        deletion_nodes += nodes
        if word is None:
            redundant.append(edge)
        else:
            need(word[:10] == BAD and proper(word, 241,
                 [candidate for candidate in edges if candidate != edge]),
                 f"edge-deletion witness {edge}")
            need(word[edge[0]] == word[edge[1]],
                 f"deleted edge not used {edge}")
            critical.append(edge)
            witness_rows.append(f"{edge[0]} {edge[1]} {word}")
    need(len(critical) == 43 and redundant
         == [(66, 191), (74, 186), (97, 186), (97, 226)],
         "private contact edge classification")

    connectivity = connectivity_census(241, edges)
    cnf_digest = sha256(conditional_cnf(241, edges))
    need(cnf_digest == certificate["core_cnf_sha256"], "conditional CNF")

    left_bad = "".join(without_contacts[index] for index in sorted(left_core))
    left_good = "".join(certificate["proper4"][index]
                        for index in sorted(left_core))
    left_edges_local = [(first, second) for first, second in inherited
                        if first in left_core and second in left_core]
    need(len(left_bad) == len(left_good) == 121
         and all(without_contacts[first] != without_contacts[second]
                 for first, second in left_edges_local)
         and all(certificate["proper4"][first]
                 != certificate["proper4"][second]
                 for first, second in left_edges_local),
         "strict left projection witnesses")

    return {
        "status": "ACCEPTED_INDEPENDENT_CONDITIONAL_CORE_REVIEW",
        "target_commit": "eb1263c7f9ac2b80120cd9521a6f99d2da435a7b",
        "points": len(points),
        "complete_unit_edges": len(edges),
        "all_pairs": len(points) * (len(points) - 1) // 2,
        "point_hash": point_digest,
        "edge_hash": edge_digest,
        "conditional_cnf_hash": cnf_digest,
        "chromatic_number": 4,
        "golomb_edges": len(g_edges),
        "canonical_complete_inputs": len(patterns),
        "excluded_input": BAD,
        "surviving_input": certificate["proper4"][:10],
        "independent_conditional_search": {
            "algorithm": "direct_dsat_assignment_no_singleton_propagation",
            "nodes": base_nodes,
            "satisfiable": False,
        },
        "relative_private_vertex_minimality": {
            "checked_positive_witnesses": len(deletion_words),
            "scope": "induced subsets containing the ten fixed input vertices",
        },
        "pieces": {
            "left_points": len(left_core),
            "right_points": len(right_core),
            "shared_points": len(left_core & right_core),
            "private_contacts": len(contacts),
            "all_contacts_deleted_is_satisfiable": True,
            "strict_left_input_projection_loss": True,
        },
        "private_contact_edge_classification": {
            "conditionally_critical": len(critical),
            "individually_redundant": [list(edge) for edge in redundant],
            "search_nodes": deletion_nodes,
            "sat_witness_stream_sha256": stream_hash(witness_rows),
        },
        "connectivity": connectivity,
        "native_role_budget": native_budget(points),
        "full_core_input_relation_enumerated": False,
        "global_minimum_claim": False,
        "five_chromatic_or_record_candidate": False,
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--check-expected", action="store_true")
    args = parser.parse_args()
    result = run()
    if args.check_expected:
        need(result == json.loads((HERE / "EXPECTED.json").read_text()),
             "expected output")
    print(json.dumps(result, indent=2, sort_keys=True))
