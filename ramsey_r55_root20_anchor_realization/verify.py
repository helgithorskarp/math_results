#!/usr/bin/env python3
"""Solver-free definition-level witness and handoff checker; no producer imports."""
import argparse
import hashlib
from itertools import combinations
import json
from pathlib import Path


def require(ok, message):
    if not ok:
        raise ValueError(message)


def graph_check(doc):
    require(set(doc) == {"n", "red_edges"} and type(doc["n"]) is int and doc["n"] == 20, "graph schema")
    raw = doc["red_edges"]
    require(type(raw) is list and raw == sorted(raw), "edge list order")
    rows = [0] * 20
    for edge in raw:
        require(type(edge) is list and len(edge) == 2 and all(type(v) is int for v in edge), "edge syntax")
        u, v = edge
        require(0 <= u < v < 20 and not (rows[u] >> v & 1), "edge bounds / duplicate")
        rows[u] |= 1 << v
        rows[v] |= 1 << u
    require(sum(r.bit_count() for r in rows) == 184, "red edge count")
    require(rows[0] == (1 << 1) + sum(1 << v for v in range(10, 16)), "first distinguished neighborhood")
    require(rows[1] == (1 << 0) + sum(1 << v for v in range(16, 20)), "second distinguished neighborhood")

    def recursive(color, size):
        adj = rows if color else [((1 << 20) - 1) ^ r ^ (1 << v) for v, r in enumerate(rows)]
        out = []
        def visit(prefix, candidates):
            if len(prefix) == size:
                out.append(prefix)
                return
            while candidates.bit_count() >= size - len(prefix):
                bit = candidates & -candidates
                candidates ^= bit
                v = bit.bit_length() - 1
                visit(prefix + (v,), candidates & adj[v])
        visit((), (1 << 20) - 1)
        return out

    for color, size in ((True, 4), (False, 5)):
        literal = [s for s in combinations(range(20), size)
                   if all(bool(rows[u] >> v & 1) == color for u, v in combinations(s, 2))]
        require(literal == recursive(color, size), "literal / recursive mismatch")
        require(not literal, "forbidden local clique")
    return rows


def handoff_check(doc, claimed):
    rows = graph_check(doc)
    # Construct each global vertex's three incidences as sets, not producer bit masks.
    cells = [(range(3, 11), {0}), (range(11, 19), {1}), (range(19, 25), {0, 1}),
             (range(25, 35), {2}), (range(35, 39), {0, 2}), (range(39, 43), {1, 2})]
    signatures = {v: frozenset(s) for vertices, s in cells for v in vertices}
    mapping = [1, 2] + sorted(v for v, s in signatures.items() if 0 in s)
    require(claimed["global_vertex_map"] == mapping, "global embedding map")
    inverse = {v: i for i, v in enumerate(mapping)}
    known = [[None] * 43 for _ in range(43)]
    for u, v in combinations(range(43), 2):
        color = None
        if u < 3:
            color = True if v < 3 else u in signatures[v]
        if u in inverse and v in inverse:
            actual = bool(rows[inverse[u]] >> inverse[v] & 1)
            require(color is None or actual == color, "local / fixed incidence conflict")
            color = actual
        known[u][v] = known[v][u] = color
    edges = list(combinations(range(3, 43), 2))
    units = [j if known[u][v] else -j for j, (u, v) in enumerate(edges, 1) if known[u][v] is not None]
    require(claimed["central_units"] == units, "central units / exact coverage")
    remaining = [(u, v) for u, v in edges if known[u][v] is None]
    invisible = [e for e in remaining if signatures[e[0]].isdisjoint(signatures[e[1]]) and
                 signatures[e[0]] | signatures[e[1]] == frozenset(range(3))]
    fixed_red = sum(known[u][v] is True for u, v in combinations(range(43), 2))
    degrees = [(20 if u < 3 else 21) - sum(x is True for x in known[u]) for u in range(43)]
    expected = {"format": "root20-to-r55-affine-handoff-v1", "global_vertex_map": mapping,
                "central_units": units, "fixed_central_variables": len(units),
                "remaining_central_variables": len(remaining), "remaining_visible_variables": len(remaining) - len(invisible),
                "remaining_invisible_variables": len(invisible), "fixed_red_edges": fixed_red,
                "remaining_red_edges": 450 - fixed_red, "residual_degrees": degrees,
                "exceptional_profiles": [],
                "status": "UNSOLVED_EXTENSION_INTERFACE_NOT_A_FEASIBILITY_CERTIFICATE"}
    for root in range(3):
        for color in (True, False):
            domain = {v for v in range(43) if known[root][v] is color}
            pairs = list(combinations(sorted(domain), 2))
            target = 92 if color else 107
            red_target = target if color else len(pairs) - target
            fixed_count = sum(known[u][v] is True for u, v in pairs)
            variables = [j for j, (u, v) in enumerate(edges, 1) if u in domain and v in domain and known[u][v] is None]
            expected["exceptional_profiles"].append({"root": root, "color": "red" if color else "blue",
                                                    "order": len(domain), "same_color_target": target,
                                                    "red_target": red_target, "known_red": fixed_count,
                                                    "remaining_variables": variables, "red_rhs": red_target - fixed_count})
    require(claimed == expected, "full handoff data mismatch")
    require(sum(degrees) == 2 * (450 - fixed_red), "residual handshaking")
    require(all(0 <= degrees[v] <= sum(x is None for w, x in enumerate(known[v]) if w != v)
                for v in range(43)), "individual residual degree boxes")
    # Every outside vertex has only its three E incidences fixed, so any fully
    # colored five-set lies in {0} union N_R(0). Check that entire 21-vertex graph.
    core = [0] + mapping
    for five in combinations(core, 5):
        colors = [known[u][v] for u, v in combinations(five, 2)]
        require(None not in colors and any(colors) and not all(colors), "fixed 21-vertex K5")
    profile_summary = [{k: r[k] for k in ("root", "color", "order", "known_red", "red_rhs")}
                       | {"unknown_count": len(r["remaining_variables"])} for r in expected["exceptional_profiles"]]
    return {"status": "WITNESS_AND_HANDOFF_VERIFIED", "local_order": 20, "local_red_edges": 92,
            "local_degrees": [r.bit_count() for r in rows], "red_k4": 0, "blue_k5": 0,
            "checked_21_vertex_five_sets": 20349,
            "fixed_central_variables": len(units), "remaining_central_variables": len(remaining),
            "remaining_visible_variables": len(remaining) - len(invisible), "remaining_invisible_variables": len(invisible),
            "fixed_red_edges": fixed_red, "remaining_red_edges": 450 - fixed_red,
            "exceptional_profile_summary": profile_summary,
            "remaining_extension": "UNSOLVED; degree boxes and row identities are not simultaneous feasibility"}


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--graph", type=Path, default=Path(__file__).with_name("GRAPH.json"))
    p.add_argument("--handoff", type=Path, default=Path(__file__).with_name("HANDOFF.json"))
    p.add_argument("--report", type=Path, required=True)
    args = p.parse_args()
    result = handoff_check(json.loads(args.graph.read_text()), json.loads(args.handoff.read_text()))
    result["graph_sha256"] = hashlib.sha256(args.graph.read_bytes()).hexdigest()
    result["handoff_sha256"] = hashlib.sha256(args.handoff.read_bytes()).hexdigest()
    args.report.write_text(json.dumps(result, sort_keys=True, indent=2) + "\n")
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
