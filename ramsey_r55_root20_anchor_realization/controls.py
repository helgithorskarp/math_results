#!/usr/bin/env python3
"""Witness and affine-handoff corruption controls; no solver or generator import."""
import argparse
from copy import deepcopy
from itertools import combinations
import json
from pathlib import Path
import verify


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--source", type=Path, default=Path(__file__).resolve().parent)
    p.add_argument("--report", type=Path, required=True)
    args = p.parse_args()
    graph = json.loads((args.source / "GRAPH.json").read_text())
    handoff = json.loads((args.source / "HANDOFF.json").read_text())
    verify.handoff_check(graph, handoff)
    rejected = []

    def reject(name, doc, data):
        try:
            verify.handoff_check(doc, data)
        except ValueError:
            rejected.append(name)
        else:
            raise ValueError("accepted corruption: " + name)

    for name in ("wrong_order", "duplicate_edge", "deleted_edge", "root_incidence"):
        doc = deepcopy(graph)
        if name == "wrong_order":
            doc["n"] = 21
        elif name == "duplicate_edge":
            doc["red_edges"].append(doc["red_edges"][-1])
        elif name == "deleted_edge":
            doc["red_edges"].pop()
        else:
            doc["red_edges"].remove([0, 1])
            doc["red_edges"].append([0, 2])
            doc["red_edges"].sort()
        reject(name, doc, handoff)
    # Preserve 92 edges and every distinguished incidence, but create an actual
    # forbidden clique away from the roots. The compensating edits are outside it.
    for color, size, name in ((True, 4, "red_k4_at_fixed_edge_count"),
                              (False, 5, "blue_k5_at_fixed_edge_count")):
        red = {tuple(e) for e in graph["red_edges"]}
        inside = set(combinations(range(2, 2 + size), 2))
        if color:
            added = inside - red
            red.update(inside)
            outside = sorted(e for e in red - inside if min(e) >= 2)
            red.difference_update(outside[:len(added)])
        else:
            removed = inside & red
            red.difference_update(inside)
            outside = [e for e in combinations(range(2, 20), 2) if e not in red and e not in inside]
            red.update(outside[:len(removed)])
        verify.require(len(red) == 92, "bad clique-control construction")
        reject(name, {"n": 20, "red_edges": [list(e) for e in sorted(red)]}, handoff)
    for name in ("unit_sign", "missing_unit", "wrong_embedding", "residual_degree",
                 "profile_rhs", "profile_variable", "unknown_count"):
        data = deepcopy(handoff)
        if name == "unit_sign":
            data["central_units"][0] *= -1
        elif name == "missing_unit":
            data["central_units"].pop()
        elif name == "wrong_embedding":
            data["global_vertex_map"][2] = 11
        elif name == "residual_degree":
            data["residual_degrees"][3] += 1
        elif name == "profile_rhs":
            data["exceptional_profiles"][2]["red_rhs"] += 1
        elif name == "profile_variable":
            data["exceptional_profiles"][2]["remaining_variables"].pop()
        else:
            data["remaining_visible_variables"] -= 1
        reject(name, graph, data)
    result = {"status": "PASSED", "corruptions_rejected": len(rejected), "rejected": rejected,
              "clique_controls_preserve_edge_count_and_root_incidences": True}
    args.report.write_text(json.dumps(result, sort_keys=True, indent=2) + "\n")
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
