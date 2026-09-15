#!/usr/bin/env python3
"""Exact verifier for cyclic equilateral three-copy gluings of EI17."""

from __future__ import annotations

from collections import Counter
from fractions import Fraction as F
from itertools import combinations
import argparse
import hashlib
import importlib
import json
from pathlib import Path
import sys


HERE = Path(__file__).resolve().parent
SOURCE = HERE.parent / "hadwiger_nelson_ei17_common_pair"
DEPENDENCIES = {
    "intervals.py": "0fb646ef2fccf68334e6c0d80d1b2f7210a73a1f0135030a15ccf02c1d5b3ce7",
    "seed.py": "9ec359a35d352b1947d87516df918135eb83658a2125ccfc6515dcbff907e833",
    "seed_edges.json": "b77a3a242467f2c1ed3f047914492e70a0da9cbe6ca8234941c8dd008e25e450",
    "seed_midpoint.json": "fb712ad09168fa51814556641f31280acc8ad1e71a17a9878d1cfd55eeb96565",
}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def load_source():
    for name, expected in DEPENDENCIES.items():
        actual = hashlib.sha256((SOURCE / name).read_bytes()).hexdigest()
        require(actual == expected, f"changed EI17 dependency: {name}")
    sys.path.insert(0, str(SOURCE))
    try:
        intervals = importlib.import_module("intervals")
        seed = importlib.import_module("seed")
    finally:
        sys.path.pop(0)
    return intervals, seed


intervals, seed = load_source()
I = intervals.I
Q = intervals.Q


def cadd(a, b):
    return a[0] + b[0], a[1] + b[1]


def csub(a, b):
    return a[0] - b[0], a[1] - b[1]


def cmul(a, b):
    return a[0] * b[0] - a[1] * b[1], a[0] * b[1] + a[1] * b[0]


def cconj(a):
    return a[0], -a[1]


def exact_point(x, y):
    return I.rational(x), I.rational(y)


def cyclic_map(z, zeta):
    return cadd(exact_point(1, 0), cmul(zeta, z))


def source_frame(points, edge, reverse, reflected):
    i, j = edge[::-1] if reverse else edge
    delta = csub(points[j], points[i])
    multiplier = delta if reflected else cconj(delta)
    result = []
    for point in points:
        local = csub(point, points[i])
        if reflected:
            local = cconj(local)
        result.append(cmul(multiplier, local))
    # These replacements are exact consequences of |delta|=1, and avoid
    # dependency widening in the interval expression delta*conj(delta).
    result[i] = exact_point(0, 0)
    result[j] = exact_point(1, 0)
    return (i, j), result


def cyclic_copies(points, edge, reverse, reflected):
    anchor, first = source_frame(points, edge, reverse, reflected)
    half = I.rational(F(1, 2))
    sqrt3 = I.rational(3).sqrt()
    zeta = (-half, sqrt3 * half)
    a = exact_point(0, 0)
    b = exact_point(1, 0)
    c = (half, sqrt3 * half)
    second = [cyclic_map(z, zeta) for z in first]
    third = [cyclic_map(z, zeta) for z in second]
    i, j = anchor
    first[i], first[j] = a, b
    second[i], second[j] = b, c
    third[i], third[j] = c, a
    return anchor, (tuple(first), tuple(second), tuple(third))


def separated(a, b):
    return a.hi < b.lo or b.hi < a.lo


def interval_gap_from_one(value):
    if value.contains(1):
        return None
    return max(value.lo - Q, Q - value.hi)


def build_conservative_graph(points, source_edges, edge, reverse, reflected):
    anchor, copies = cyclic_copies(points, edge, reverse, reflected)
    i, j = anchor
    labels = [(copy, vertex) for copy in range(3) for vertex in range(17)]
    label_boxes = [copies[copy][vertex] for copy, vertex in labels]

    special = {
        (0, i): "A", (2, j): "A",
        (0, j): "B", (1, i): "B",
        (1, j): "C", (2, i): "C",
    }
    group_key = [special.get(label, label) for label in labels]
    group_names = []
    for key in group_key:
        if key not in group_names:
            group_names.append(key)
    group_of = tuple(group_names.index(key) for key in group_key)
    groups = tuple(tuple(k for k, group in enumerate(group_of) if group == g)
                   for g in range(len(group_names)))
    require(len(groups) == 48 and sorted(map(len, groups)) == [1] * 45 + [2] * 3,
            "wrong declared cyclic collision pattern")

    collision_gap = None
    for left, right in combinations(range(len(labels)), 2):
        if group_of[left] == group_of[right]:
            d2 = intervals.squared_distance(label_boxes[left], label_boxes[right])
            require(not d2.contains(1), "declared collision could also be unit-separated")
            continue
        gaps = []
        for x, y in zip(label_boxes[left], label_boxes[right]):
            if x.hi < y.lo:
                gaps.append(y.lo - x.hi)
            elif y.hi < x.lo:
                gaps.append(x.lo - y.hi)
        require(gaps, "undeclared collision not excluded")
        local = max(gaps)
        collision_gap = local if collision_gap is None else min(collision_gap, local)

    edge_set = set()
    unit_gap = None
    for ga, gb in combinations(range(len(groups)), 2):
        possible = False
        local_gaps = []
        for la in groups[ga]:
            for lb in groups[gb]:
                d2 = intervals.squared_distance(label_boxes[la], label_boxes[lb])
                gap = interval_gap_from_one(d2)
                if gap is None:
                    possible = True
                else:
                    local_gaps.append(gap)
        if possible:
            edge_set.add((ga, gb))
        else:
            local = min(local_gaps)
            unit_gap = local if unit_gap is None else min(unit_gap, local)

    inherited = set()
    addresses = []
    for copy in range(3):
        address = tuple(group_of[17 * copy + vertex] for vertex in range(17))
        addresses.append(address)
        require(len(set(address)) == 17, "one EI17 copy collided internally")
        for u, v in source_edges:
            physical = tuple(sorted((address[u], address[v])))
            inherited.add(physical)
            require(physical in edge_set, "inherited source edge missing from enclosure")
    extras = tuple(sorted(edge_set - inherited))
    return {
        "source_edge": list(edge),
        "anchor_order": list(anchor),
        "reverse": reverse,
        "reflected": reflected,
        "groups": groups,
        "addresses": tuple(addresses),
        "edges": tuple(sorted(edge_set)),
        "inherited_edges": tuple(sorted(inherited)),
        "extra_edges": extras,
        "collision_gap": collision_gap,
        "unit_gap": unit_gap,
        "boxes": tuple(label_boxes),
    }


def separation_counts(vertex_count, edges):
    """Return articulation/bridge counts by an elementary independent test."""
    adjacency = [set() for _ in range(vertex_count)]
    for a, b in edges:
        adjacency[a].add(b)
        adjacency[b].add(a)

    def components(removed_vertex=None, removed_edge=None):
        seen = set()
        count = 0
        for start in range(vertex_count):
            if start == removed_vertex or start in seen:
                continue
            count += 1
            stack = [start]
            seen.add(start)
            while stack:
                vertex = stack.pop()
                for neighbour in adjacency[vertex]:
                    if neighbour == removed_vertex or neighbour in seen:
                        continue
                    if removed_edge is not None and tuple(sorted((vertex, neighbour))) == removed_edge:
                        continue
                    seen.add(neighbour)
                    stack.append(neighbour)
        return count

    require(components() == 1, "inherited cyclic union is disconnected")
    articulations = sum(components(removed_vertex=v) > 1 for v in range(vertex_count))
    bridges = sum(components(removed_edge=edge) > 1 for edge in edges)
    return articulations, bridges


def enumerate_source_colourings(source_edges):
    adjacency = [set() for _ in range(17)]
    for a, b in source_edges:
        adjacency[a].add(b)
        adjacency[b].add(a)
    colour = [-1] * 17
    result = []

    def visit(maximum):
        if all(value >= 0 for value in colour):
            require(maximum == 3, "EI17 unexpectedly coloured with fewer than four colours")
            result.append(tuple(colour))
            return
        left = [v for v in range(17) if colour[v] < 0]
        v = max(left, key=lambda x: (
            len({colour[w] for w in adjacency[x] if colour[w] >= 0}),
            len(adjacency[x]), -x))
        forbidden = {colour[w] for w in adjacency[v] if colour[w] >= 0}
        for value in range(min(3, maximum + 1) + 1):
            if value not in forbidden:
                colour[v] = value
                visit(max(maximum, value))
        colour[v] = -1

    visit(-1)
    return tuple(result)


def colour_permutation(source_a, source_b, target_a, target_b):
    require(source_a != source_b and target_a != target_b, "edge colours must differ")
    mapping = {source_a: target_a, source_b: target_b}
    remaining_source = [c for c in range(4) if c not in mapping]
    remaining_target = [c for c in range(4) if c not in mapping.values()]
    for a, b in zip(remaining_source, remaining_target):
        mapping[a] = b
    return tuple(mapping[c] for c in range(4))


def structural_extension(word, graph):
    i, j = graph["anchor_order"]
    a, b = word[i], word[j]
    c = next(value for value in range(4) if value not in (a, b))
    p1 = colour_permutation(a, b, b, c)
    p2 = colour_permutation(a, b, c, a)
    copy_words = (word, tuple(p1[value] for value in word), tuple(p2[value] for value in word))
    physical = [-1] * 48
    for address, copy_word in zip(graph["addresses"], copy_words):
        for vertex, colour in zip(address, copy_word):
            require(physical[vertex] in (-1, colour), "cyclic anchor colours disagree")
            physical[vertex] = colour
    require(all(colour >= 0 for colour in physical), "uncoloured physical point")
    require(all(physical[u] != physical[v] for u, v in graph["edges"]),
            "structural extension is improper")
    return tuple(physical)


def complete_input_extensions(graph, colourings):
    base_indices = graph["addresses"][0]
    base_at = {physical: source for source, physical in enumerate(base_indices)}
    new_vertices = tuple(v for v in range(48) if v not in base_at)
    new_at = {physical: local for local, physical in enumerate(new_vertices)}
    adjacency = [set() for _ in range(48)]
    for a, b in graph["edges"]:
        adjacency[a].add(b)
        adjacency[b].add(a)
    new_adjacency = [tuple(new_at[w] for w in adjacency[v] if w in new_at)
                     for v in new_vertices]
    base_neighbours = [tuple(base_at[w] for w in adjacency[v] if w in base_at)
                       for v in new_vertices]
    cache = {}

    def extension(initial):
        if initial in cache:
            return cache[initial]

        def visit(domains):
            domains = list(domains)
            queue = [v for v, domain in enumerate(domains) if domain.bit_count() == 1]
            seen = set()
            while queue:
                v = queue.pop()
                if v in seen:
                    continue
                seen.add(v)
                bit = domains[v]
                for w in new_adjacency[v]:
                    if domains[w] == bit:
                        return None
                    if domains[w] & bit and domains[w].bit_count() > 1:
                        domains[w] &= ~bit
                        if not domains[w]:
                            return None
                        if domains[w].bit_count() == 1:
                            queue.append(w)
            choices = [v for v, domain in enumerate(domains) if domain.bit_count() > 1]
            if not choices:
                return tuple(domain.bit_length() - 1 for domain in domains)
            v = min(choices, key=lambda x: (domains[x].bit_count(), -len(new_adjacency[x]), x))
            mask = domains[v]
            while mask:
                bit = mask & -mask
                mask -= bit
                branch = list(domains)
                branch[v] = bit
                answer = visit(tuple(branch))
                if answer is not None:
                    return answer
            return None

        answer = visit(initial)
        cache[initial] = answer
        return answer

    digest = hashlib.sha256()
    checked = 0
    for word in colourings:
        initial = []
        for neighbours in base_neighbours:
            forbidden = 0
            for source_vertex in neighbours:
                forbidden |= 1 << word[source_vertex]
            initial.append(15 & ~forbidden)
        initial = tuple(initial)
        require(all(initial), "complete source colouring has an empty new domain")
        answer = extension(initial)
        require(answer is not None, "complete source colouring does not extend")
        require(all(domain & (1 << colour) for domain, colour in zip(initial, answer)),
                "extension violates a base-contact domain")
        require(all(answer[v] != answer[w]
                    for v in range(len(answer)) for w in new_adjacency[v] if v < w),
                "extension violates a new--new edge")
        digest.update(bytes(word) + b"|" + bytes(answer) + b"\n")
        checked += 1
    return checked, len(cache), digest.hexdigest()


def compact_graph_record(graph):
    return {
        "source_edge": graph["source_edge"],
        "anchor_order": graph["anchor_order"],
        "reverse": graph["reverse"],
        "reflected": graph["reflected"],
        "physical_points": len(graph["groups"]),
        "conservative_edges": len(graph["edges"]),
        "conservative_extra_edges": len(graph["extra_edges"]),
        "extra_edges": [list(edge) for edge in graph["extra_edges"]],
    }


def build_report(progress=False):
    points, source_report = seed.certify()
    source_edges = tuple(map(tuple, json.loads((SOURCE / "seed_edges.json").read_text())))
    require(len(source_edges) == 31, "wrong EI17 source edge count")
    colourings = enumerate_source_colourings(source_edges)
    require(len(colourings) == 85088, "unexpected EI17 colour-orbit count")

    graphs = []
    collision_gap = None
    unit_gap = None
    for number, edge in enumerate(source_edges):
        for reverse in (False, True):
            for reflected in (False, True):
                graph = build_conservative_graph(points, source_edges, edge, reverse, reflected)
                graphs.append(graph)
                collision_gap = graph["collision_gap"] if collision_gap is None else min(collision_gap, graph["collision_gap"])
                unit_gap = graph["unit_gap"] if unit_gap is None else min(unit_gap, graph["unit_gap"])
        if progress and (number + 1) % 10 == 0:
            print(f"geometry {number + 1}/{len(source_edges)}", file=sys.stderr, flush=True)

    require(len(graphs) == 124, "incomplete cyclic frame enumeration")
    contactful = [graph for graph in graphs if graph["extra_edges"]]
    require(len(contactful) == 8, "unexpected contactful-frame count")
    require(all(len(graph["extra_edges"]) == 3 for graph in contactful),
            "unexpected conservative cross-contact count")
    separation_profiles = Counter(
        separation_counts(48, graph["inherited_edges"]) for graph in graphs)
    require(separation_profiles == {(0, 0): 124},
            "the source-incidence union became separable")

    # The inherited-edge-only cases all have the same elementary extension
    # formula.  Check it for every complete source colouring on one such graph.
    plain = next(graph for graph in graphs if not graph["extra_edges"])
    structural_hash = hashlib.sha256()
    for word in colourings:
        witness = structural_extension(word, plain)
        structural_hash.update(bytes(word) + b"|" + bytes(witness) + b"\n")

    relation_records = []
    for graph in contactful:
        checked, states, witness_hash = complete_input_extensions(graph, colourings)
        relation_records.append({
            **compact_graph_record(graph),
            "complete_source_colourings_extended": checked,
            "distinct_initial_domain_states": states,
            "extension_witness_sha256": witness_hash,
        })

    geometry_digest = hashlib.sha256()
    for number, graph in enumerate(graphs):
        geometry_digest.update(f"F {number}\n".encode())
        for group in graph["groups"]:
            geometry_digest.update(("G " + " ".join(map(str, group)) + "\n").encode())
        for edge in graph["edges"]:
            geometry_digest.update(f"E {edge[0]} {edge[1]}\n".encode())

    report = {
        "verified": True,
        "source": source_report,
        "source_vertices": 17,
        "source_edges": 31,
        "source_colour_orbits_modulo_global_permutation": len(colourings),
        "labelled_cyclic_frames": len(graphs),
        "physical_points_each": 48,
        "conservative_edge_count_histogram": dict(sorted(Counter(len(g["edges"]) for g in graphs).items())),
        "conservative_extra_edge_histogram": dict(sorted(Counter(len(g["extra_edges"]) for g in graphs).items())),
        "contactful_frames": len(contactful),
        "plain_frames": len(graphs) - len(contactful),
        "inherited_union_articulation_bridge_histogram": {
            f"{articulations},{bridges}": count
            for (articulations, bridges), count in sorted(separation_profiles.items())
        },
        "plain_complete_source_colourings_extended_by_formula": len(colourings),
        "plain_extension_witness_sha256": structural_hash.hexdigest(),
        "contactful_complete_source_extension_checks": len(contactful) * len(colourings),
        "contactful_relation_records": relation_records,
        "all_complete_source_colourings_extend": True,
        "all_complete_physical_graphs_four_colourable": True,
        "all_complete_physical_graphs_chromatic_number": 4,
        "complete_input_loss_found": False,
        "record_candidate": False,
        "geometry_stream_sha256": geometry_digest.hexdigest(),
        "coordinate_separation_lower_units_1e_minus_12": collision_gap * 10**12 // Q,
        "squared_unit_exclusion_gap_lower_units_1e_minus_12": unit_gap * 10**12 // Q,
    }
    return json.loads(json.dumps(report))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check-expected", action="store_true")
    parser.add_argument("--progress", action="store_true")
    args = parser.parse_args()
    report = build_report(args.progress)
    if args.check_expected:
        expected = json.loads((HERE / "EXPECTED.json").read_text())
        require(report == expected, "result does not match EXPECTED.json")
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
