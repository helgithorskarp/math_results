#!/usr/bin/env python3
"""Independent audit of the exact H560 separator boundary relations.

Dense exact geometry is reused from the preceding independent reviewer package;
no target producer or verifier module is imported.  This script independently
checks the separator, positive states, normalization, and both CNF byte streams.
"""

from hashlib import sha256
import importlib.util
from itertools import combinations, product
import json
from pathlib import Path
import sys


HERE = Path(__file__).resolve().parent
REPO = HERE.parent
TARGET = REPO / "hadwiger_nelson_heule560_separator"
GEOMETRY_CHECKER = REPO / "hadwiger_nelson_heule560_left_relation_review1/independent_check.py"
PINNED = {
    "plan.json": "c2d96e718dce323399c495aaf8b8d29c50602cf6ed34da01a15cdb51bde1cd69",
    "certificate.json": "e248abe73717723fb841af94672a23269e1562a0f2f20f6c48059b21ee01a9b3",
    "proof_manifest.json": "63d8118c07b703bb47f978bf3d3e98726c6676c1720b20ed8f9fec1152740c0c",
    "expected.json": "76437d5dc945dbfc896373962a783dd331f2c522354241f2b28b50a9d781691d",
}
GEOMETRY_CHECKER_SHA256 = "1d57c4dc5d81035fea15b3ad6b82b3a336459043781b96412b2f1402c3c9da2e"


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def digest_bytes(data):
    return sha256(data).hexdigest()


def digest_file(path):
    return digest_bytes(path.read_bytes())


def load_dense_geometry_checker():
    require(digest_file(GEOMETRY_CHECKER) == GEOMETRY_CHECKER_SHA256,
            "independent dense-geometry checker hash")
    sys.dont_write_bytecode = True
    spec = importlib.util.spec_from_file_location("review_dense_geometry", GEOMETRY_CHECKER)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def canonical(word):
    mapping = {}
    output = []
    for symbol in word:
        if symbol not in mapping:
            mapping[symbol] = str(len(mapping))
        output.append(mapping[symbol])
    return "".join(output)


def check_colouring(row, vertices, edges, separator):
    text = row["colouring"]
    require(len(text) == len(vertices) and set(text) <= set("0123"), "colour string")
    colours = dict(zip(vertices, text))
    require(all(colours[u] != colours[v] for u, v in edges), "monochromatic exact unit edge")
    state = "".join(colours[vertex] for vertex in separator)
    require(state == row["state"] == canonical(state), "noncanonical or incorrect boundary state")
    return state, len(edges)


def encode_completeness_cnf(vertices, edges, separator, states):
    position = {vertex: index for index, vertex in enumerate(vertices)}

    def variable(vertex, colour):
        return 4 * position[vertex] + colour + 1

    clauses = []
    for vertex in vertices:
        colours = [variable(vertex, colour) for colour in range(4)]
        clauses.append(tuple(colours))
        clauses.extend((-left, -right) for left, right in combinations(colours, 2))
    for u, v in edges:
        for colour in range(4):
            clauses.append((-variable(u, colour), -variable(v, colour)))
    for index, vertex in enumerate(separator):
        for colour in range(1, 4):
            clauses.append(tuple([-variable(vertex, colour)] +
                                 [variable(earlier, colour - 1) for earlier in separator[:index]]))
    base_clauses = len(clauses)
    for state in states:
        clauses.append(tuple(-variable(vertex, int(colour))
                             for vertex, colour in zip(separator, state)))

    payload = bytearray(f"p cnf {4 * len(vertices)} {len(clauses)}\n", "ascii")
    for clause in clauses:
        payload.extend((" ".join(map(str, clause)) + " 0\n").encode("ascii"))
    return bytes(payload), base_clauses


def audit_normalization():
    checks = 0
    for length in range(1, 8):
        for symbols in product("0123", repeat=length):
            word = "".join(symbols)
            rule = all(int(symbol) == 0 or str(int(symbol) - 1) in word[:index]
                       for index, symbol in enumerate(word))
            require(rule == (canonical(word) == word), "first-occurrence rule mismatch")
            checks += 1
    return checks


def main():
    for filename, expected in PINNED.items():
        require(digest_file(TARGET / filename) == expected, f"target file hash: {filename}")
    plan = json.loads((TARGET / "plan.json").read_text())
    certificate = json.loads((TARGET / "certificate.json").read_text())
    manifest = json.loads((TARGET / "proof_manifest.json").read_text())
    dense = load_dense_geometry_checker()
    geometry_plan = dict(plan)
    geometry_plan["optional_order"] = certificate["optional_large"]
    geometry = dense.reconstruct_geometry(geometry_plan)

    mandatory = geometry["mandatory"]
    optional = geometry["optional"]
    large = geometry["large"]
    small = geometry["small"]
    edges = geometry["edges"]
    separator = geometry["separator"]
    cross = [(u, v) if u in large else (v, u)
             for u, v in edges if (u in large) != (v in large)]

    require(certificate["separator"] == separator, "separator identity")
    require(certificate["optional_large"] == sorted(large & optional), "large optionals")
    require(not any(u in separator and v in separator for u, v in edges), "separator not independent")
    require({u for u, _ in cross} == set(separator), "separator does not cover cross edges")
    matching = [tuple(edge) for edge in certificate["cross_matching"]]
    require(len(matching) == 19 and all(edge in cross for edge in matching), "cross matching edges")
    require(len({vertex for edge in matching for vertex in edge}) == 38, "cross matching not disjoint")
    require(certificate["record_improvement"] is False and
            certificate["whole560_family_closed"] is False, "scope flags")

    reports = {}
    state_sets = {}
    positive_checks = 0
    for name, support in (("mandatory", mandatory & large), ("full", large)):
        block = certificate["blocks"][name]
        vertices = sorted(support)
        block_edges = [(u, v) for u, v in edges if u in support and v in support]
        require(block["vertices"] == vertices, f"{name} block vertices")
        states = []
        for row in block["states"]:
            state, checked = check_colouring(row, vertices, block_edges, separator)
            states.append(state)
            positive_checks += checked
        require(states == sorted(set(states)), f"{name} states not sorted and unique")
        cnf, base_clauses = encode_completeness_cnf(vertices, block_edges, separator, states)
        require(digest_bytes(cnf) == manifest[name]["cnf_sha256"] and
                len(cnf) == manifest[name]["cnf_bytes"], f"{name} CNF identity")
        state_stream = ("\n".join(states) + "\n").encode()
        state_sets[name] = set(states)
        reports[name] = {
            "vertices": len(vertices),
            "edges": len(block_edges),
            "states": len(states),
            "variables": 4 * len(vertices),
            "base_clauses": base_clauses,
            "complete_clauses": base_clauses + len(states),
            "cnf_bytes": len(cnf),
            "cnf_sha256": digest_bytes(cnf),
            "state_sha256": digest_bytes(state_stream),
            "proof_bytes": manifest[name]["proof_bytes"],
            "proof_sha256": manifest[name]["proof_sha256"],
            "drat_replay_in_this_script": False,
        }

    require(state_sets["full"] < state_sets["mandatory"], "boundary relation inclusion")
    right = small | set(separator)
    result = {
        "status": "INDEPENDENTLY_VERIFIED_SCOPED_INTERMEDIATE_RESULT",
        "geometry": {
            "host_pairs_checked": 632 * 631 // 2,
            "seed_vertices": len(mandatory | optional),
            "seed_edges": len(edges),
            "large_vertices": len(large),
            "small_vertices": len(small),
            "cross_edges": len(cross),
            "separator_vertices": len(separator),
            "cross_matching_edges": len(matching),
            "right_block_vertices": len(right),
            "right_block_edges": sum(u in right and v in right for u, v in edges),
            "mandatory_right_vertices": len(right & mandatory),
            "mandatory_right_edges": sum(u in right & mandatory and v in right & mandatory
                                         for u, v in edges),
            "optional_large": sorted(optional & large),
            "optional_right_count": len(optional & small),
        },
        "boundary_relations": reports,
        "positive_unit_edge_checks": positive_checks,
        "lost_states_when_all_nine_present": len(state_sets["mandatory"] - state_sets["full"]),
        "normalization_words_checked": audit_normalization(),
        "unconstrained_palette_orbits": (4**19 + 6 * 2**19 + 8) // 24,
        "complete_boundary_relations_drat_replay_in_this_script": False,
        "whole_560_family_closed": False,
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
