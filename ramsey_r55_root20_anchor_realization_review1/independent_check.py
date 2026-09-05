#!/usr/bin/env python3
"""Independent exact checker for the marked R55 root-neighborhood handoff.

This checker imports no reviewed module.  It reconstructs the two-colouring
from the explicit edge list, exhausts all relevant cliques, and derives the
43-vertex partial graph and every affine handoff field using a closed-form
central-pair index rather than the reviewed generator's lookup table.
"""

from argparse import ArgumentParser
from copy import deepcopy
from hashlib import sha256
from itertools import combinations
import json
from math import comb
from pathlib import Path


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def read_json(path):
    return json.loads(path.read_text())


def file_record(path):
    data = path.read_bytes()
    return {"bytes": len(data), "sha256": sha256(data).hexdigest()}


def local_graph(document):
    require(set(document) == {"n", "red_edges"}, "graph schema")
    require(type(document["n"]) is int and document["n"] == 20, "graph order")
    raw = document["red_edges"]
    require(type(raw) is list and raw == sorted(raw), "canonical edge ordering")
    red = set()
    for row in raw:
        require(type(row) is list and len(row) == 2, "edge width")
        require(all(type(v) is int for v in row), "integer endpoints")
        u, v = row
        require(0 <= u < v < 20, "edge bounds")
        require((u, v) not in red, "duplicate edge")
        red.add((u, v))
    require(len(red) == 92, "red edge count")

    def is_red(u, v):
        return tuple(sorted((u, v))) in red

    neighborhoods = [{v for v in range(20) if v != u and is_red(u, v)}
                     for u in range(20)]
    require(neighborhoods[0] == {1, 10, 11, 12, 13, 14, 15}, "marked u neighborhood")
    require(neighborhoods[1] == {0, 16, 17, 18, 19}, "marked v neighborhood")
    require((neighborhoods[0] - {1}).isdisjoint(neighborhoods[1] - {0}),
            "marked common red neighbor")

    red_k4 = [vertices for vertices in combinations(range(20), 4)
              if all(is_red(u, v) for u, v in combinations(vertices, 2))]
    blue_k5 = [vertices for vertices in combinations(range(20), 5)
               if all(not is_red(u, v) for u, v in combinations(vertices, 2))]
    require(not red_k4, "red K4")
    require(not blue_k5, "blue K5")

    return red, is_red, [len(row) for row in neighborhoods]


def signature_masks():
    masks = {}
    for vertices, mask in ((range(3, 11), 1), (range(11, 19), 2),
                           (range(19, 25), 3), (range(25, 35), 4),
                           (range(35, 39), 5), (range(39, 43), 6)):
        for vertex in vertices:
            masks[vertex] = mask
    require(len(masks) == 40 and set(masks) == set(range(3, 43)), "signature partition")
    return masks


def central_index(u, v):
    """One-based lexicographic index of 3 <= u < v <= 42."""
    require(3 <= u < v <= 42, "central pair bounds")
    rows_before = u - 3
    return rows_before * 39 - rows_before * (rows_before - 1) // 2 + (v - u)


def derive_handoff(graph_document):
    red, is_red, degrees = local_graph(graph_document)
    masks = signature_masks()
    mapping = [1, 2] + list(range(3, 11)) + list(range(19, 25)) + list(range(35, 39))
    require(len(mapping) == 20 and len(set(mapping)) == 20, "embedding cardinality")

    known = [[None] * 43 for _ in range(43)]

    def assign(u, v, color):
        require(u != v, "loop")
        if u > v:
            u, v = v, u
        if known[u][v] is not None:
            require(known[u][v] is color, "conflicting prescribed edge")
        known[u][v] = known[v][u] = color

    # The exceptional roots form a red triangle and every root-to-central
    # colour is specified by the six nonempty, nonfull signature cells.
    for u, v in combinations(range(3), 2):
        assign(u, v, True)
    for root in range(3):
        for vertex, mask in masks.items():
            assign(root, vertex, bool(mask & (1 << root)))

    # Install the entire marked local graph as root 0's red neighborhood.
    for i, j in combinations(range(20), 2):
        assign(mapping[i], mapping[j], is_red(i, j))

    # Verify that the local marked pair agrees with the declared signatures.
    require(mapping == [1, 2] + sorted(v for v, mask in masks.items() if mask & 1),
            "red-neighborhood embedding")

    all_central_pairs = list(combinations(range(3, 43), 2))
    require(len(all_central_pairs) == 780, "central pair count")
    indices = {central_index(u, v) for u, v in all_central_pairs}
    require(indices == set(range(1, 781)), "closed-form variable-index bijection")

    units = []
    remaining = []
    invisible = []
    for u, v in all_central_pairs:
        index = central_index(u, v)
        color = known[u][v]
        if color is None:
            remaining.append((u, v))
            # Such an edge is visible in a root-neighborhood constraint iff
            # its endpoints agree in at least one signature bit.
            if all(bool(masks[u] & (1 << root)) != bool(masks[v] & (1 << root))
                   for root in range(3)):
                invisible.append((u, v))
        else:
            units.append(index if color else -index)

    fixed_red = sum(known[u][v] is True for u, v in combinations(range(43), 2))
    target_degrees = [20, 20, 20] + [21] * 40
    residual_degrees = [target_degrees[u] - sum(color is True for color in known[u])
                        for u in range(43)]
    require(sum(residual_degrees) == 2 * (450 - fixed_red), "residual handshake")
    require(all(0 <= residual_degrees[u] <=
                sum(known[u][v] is None for v in range(43) if v != u)
                for u in range(43)), "individual degree box")

    profiles = []
    profile_summary = []
    for root in range(3):
        for color in (True, False):
            domain = sorted(v for v in range(43) if v != root and known[root][v] is color)
            require(len(domain) == (20 if color else 22), "profile neighborhood order")
            same_color_target = 92 if color else 107
            red_target = same_color_target if color else comb(len(domain), 2) - same_color_target
            pairs = list(combinations(domain, 2))
            known_red = sum(known[u][v] is True for u, v in pairs)
            variables = [central_index(u, v) for u, v in pairs if known[u][v] is None]
            row = {"root": root, "color": "red" if color else "blue",
                   "order": len(domain), "same_color_target": same_color_target,
                   "red_target": red_target, "known_red": known_red,
                   "remaining_variables": variables, "red_rhs": red_target - known_red}
            profiles.append(row)
            profile_summary.append({"root": root, "color": row["color"],
                                    "order": len(domain), "known_red": known_red,
                                    "red_rhs": row["red_rhs"],
                                    "unknown_count": len(variables)})

    expected = {
        "format": "root20-to-r55-affine-handoff-v1",
        "global_vertex_map": mapping,
        "central_units": units,
        "fixed_central_variables": len(units),
        "remaining_central_variables": len(remaining),
        "remaining_visible_variables": len(remaining) - len(invisible),
        "remaining_invisible_variables": len(invisible),
        "fixed_red_edges": fixed_red,
        "remaining_red_edges": 450 - fixed_red,
        "residual_degrees": residual_degrees,
        "exceptional_profiles": profiles,
        "status": "UNSOLVED_EXTENSION_INTERFACE_NOT_A_FEASIBILITY_CERTIFICATE",
    }

    core = {0, *mapping}
    require(len(core) == 21, "fixed core order")
    fully_fixed = 0
    monochromatic_fixed = []
    for vertices in combinations(range(43), 5):
        colors = [known[u][v] for u, v in combinations(vertices, 2)]
        if None not in colors:
            fully_fixed += 1
            require(set(vertices) <= core, "fully fixed five-set outside core")
            if all(colors) or not any(colors):
                monochromatic_fixed.append(vertices)
    require(fully_fixed == comb(21, 5) == 20349, "fully fixed five-set census")
    require(not monochromatic_fixed, "monochromatic fixed five-set")

    outside = set(range(43)) - core
    require(len(outside) == 22, "outside-core count")
    require(all(sum(known[u][v] is not None for v in range(43) if v != u) == 3
                for u in outside), "outside vertex has extra fixed edge")

    report = {
        "local_order": 20,
        "local_red_edges": len(red),
        "local_degrees": degrees,
        "red_four_sets_checked": comb(20, 4),
        "blue_five_sets_checked": comb(20, 5),
        "red_k4": 0,
        "blue_k5": 0,
        "global_five_sets_checked": comb(43, 5),
        "fully_fixed_five_sets": fully_fixed,
        "fixed_core_order": len(core),
        "fixed_core_monochromatic_k5": 0,
        "fixed_central_variables": len(units),
        "remaining_central_variables": len(remaining),
        "remaining_visible_variables": len(remaining) - len(invisible),
        "remaining_invisible_variables": len(invisible),
        "fixed_red_edges": fixed_red,
        "remaining_red_edges": 450 - fixed_red,
        "residual_degree_sum": sum(residual_degrees),
        "profile_summary": profile_summary,
        "extension_feasibility_claimed": False,
    }
    return expected, report


def verify_pair(graph_document, handoff_document):
    expected, report = derive_handoff(graph_document)
    require(handoff_document == expected, "handoff differs from independent derivation")
    return report


def main():
    parser = ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--report", type=Path, required=True)
    args = parser.parse_args()
    graph_path = args.source / "GRAPH.json"
    handoff_path = args.source / "HANDOFF.json"
    graph = read_json(graph_path)
    handoff = read_json(handoff_path)
    report = verify_pair(graph, handoff)

    rejected = []

    def reject(name, candidate_graph, candidate_handoff):
        try:
            verify_pair(candidate_graph, candidate_handoff)
        except AssertionError:
            rejected.append(name)
        else:
            raise AssertionError("independent checker accepted corruption: " + name)

    bad_graph = deepcopy(graph)
    bad_graph["red_edges"].pop()
    reject("missing_graph_edge", bad_graph, handoff)
    for name, edit in (
        ("unit_sign", lambda x: x["central_units"].__setitem__(0, -x["central_units"][0])),
        ("embedding", lambda x: x["global_vertex_map"].__setitem__(2, 11)),
        ("residual_degree", lambda x: x["residual_degrees"].__setitem__(3, x["residual_degrees"][3] + 1)),
        ("profile_rhs", lambda x: x["exceptional_profiles"][2].__setitem__("red_rhs", 72)),
        ("visible_count", lambda x: x.__setitem__("remaining_visible_variables", 502)),
    ):
        bad_handoff = deepcopy(handoff)
        edit(bad_handoff)
        reject(name, graph, bad_handoff)

    report.update({
        "all_checks_passed": True,
        "format": "r55-root20-review1-v1",
        "graph": file_record(graph_path),
        "handoff": file_record(handoff_path),
        "independent_corruptions_rejected": rejected,
        "target_graph_claimed": False,
    })
    args.report.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    print(json.dumps(report, sort_keys=True))


if __name__ == "__main__":
    main()
