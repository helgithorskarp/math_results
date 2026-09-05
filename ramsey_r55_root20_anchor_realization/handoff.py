#!/usr/bin/env python3
"""Encode the concrete neighborhood as units and residual affine data for K_43."""
import argparse
from itertools import combinations
import json
from pathlib import Path


def build(doc):
    red = {tuple(e) for e in doc["red_edges"]}
    mapping = [1, 2] + list(range(3, 11)) + list(range(19, 25)) + list(range(35, 39))
    signatures = [-1] * 3 + [1] * 8 + [2] * 8 + [3] * 6 + [4] * 10 + [5] * 4 + [6] * 4
    edges = list(combinations(range(3, 43), 2))
    index = {e: j + 1 for j, e in enumerate(edges)}
    fixed = {(u, v): True if v < 3 else bool(signatures[v] & (1 << u))
             for u in range(3) for v in range(u + 1, 43)}
    units = []
    for u, v in combinations(range(20), 2):
        pair = tuple(sorted((mapping[u], mapping[v])))
        color = (u, v) in red
        if pair in index:
            units.append(index[pair] if color else -index[pair])
        fixed[pair] = color
    units.sort(key=abs)
    residual = [(20 if v < 3 else 21) - sum(c for e, c in fixed.items() if v in e)
                for v in range(43)]
    profiles = []
    for root in range(3):
        for color in (True, False):
            domain = [v for v in range(43) if v != root and
                      fixed[tuple(sorted((root, v)))] == color]
            target = 92 if color else 107
            target_red = target if color else len(domain) * (len(domain) - 1) // 2 - target
            pairs = list(combinations(domain, 2))
            known_red = sum(fixed[e] for e in pairs if e in fixed)
            unknown = [index[e] for e in pairs if e not in fixed]
            profiles.append({"root": root, "color": "red" if color else "blue",
                             "order": len(domain), "same_color_target": target,
                             "red_target": target_red, "known_red": known_red,
                             "remaining_variables": unknown, "red_rhs": target_red - known_red})
    unknown = [e for e in edges if e not in fixed]
    invisible = sum(signatures[u] ^ signatures[v] == 7 for u, v in unknown)
    return {"format": "root20-to-r55-affine-handoff-v1", "global_vertex_map": mapping,
            "central_units": units, "fixed_central_variables": len(units),
            "remaining_central_variables": len(unknown), "remaining_visible_variables": len(unknown) - invisible,
            "remaining_invisible_variables": invisible, "fixed_red_edges": sum(fixed.values()),
            "remaining_red_edges": 450 - sum(fixed.values()), "residual_degrees": residual,
            "exceptional_profiles": profiles,
            "status": "UNSOLVED_EXTENSION_INTERFACE_NOT_A_FEASIBILITY_CERTIFICATE"}


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--graph", type=Path, default=Path(__file__).with_name("GRAPH.json"))
    p.add_argument("--output", type=Path, required=True)
    args = p.parse_args()
    result = build(json.loads(args.graph.read_text()))
    args.output.write_text(json.dumps(result, sort_keys=True, indent=2) + "\n")
    print(json.dumps({k: result[k] for k in ("status", "fixed_central_variables", "remaining_central_variables",
                                            "remaining_visible_variables", "remaining_invisible_variables")}, sort_keys=True))


if __name__ == "__main__":
    main()
