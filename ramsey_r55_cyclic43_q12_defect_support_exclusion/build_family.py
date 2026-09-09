#!/usr/bin/env python3
"""Build one exact defect-support repair subcube around cyclic q12 source 51."""
from collections import Counter
from itertools import combinations
from pathlib import Path
import argparse
import hashlib
import json

N = 43
M = 903
SOURCE_INDEX = 51
INPUT_SHA256 = "4803b2e40dba06c0f82c3d23cbd5ae0a9127da0db24e5655971fff179fb68ec3"
LENGTHS = {1, 2, 7, 10, 12, 13, 14, 16, 18, 20, 21}


def need(test, message):
    if not test:
        raise ValueError(message)


def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def source_graph(path):
    path = Path(path)
    need(sha256(path) == INPUT_SHA256, "pinned cyclic input")
    data = json.loads(path.read_text())
    rows = data["complete_additional_objective_12_rotation_representatives"]
    need(len(rows) == 238, "238 certified source representatives")
    edges = list(combinations(range(N), 2))
    need(len(edges) == M, "903 physical edges")
    colors = [min(v - u, N - v + u) in LENGTHS for u, v in edges]
    toggles = rows[SOURCE_INDEX]
    need(toggles == [200, 273, 308, 497, 525, 672, 693, 798, 812, 837,
                     893, 897, 900, 902], "selected source identity")
    for edge in toggles:
        colors[edge] = not colors[edge]
    return edges, colors, toggles


def build(input_path, cnf_path, core_path, certificate_path, metadata_path):
    edges, colors, toggles = source_graph(input_path)
    edge_id = {edge: index for index, edge in enumerate(edges)}
    defects = []
    support = set()
    for vertices in combinations(range(N), 5):
        members = [edge_id[edge] for edge in combinations(vertices, 2)]
        red = sum(colors[edge] for edge in members)
        if red in (0, 10):
            defects.append({"vertices": list(vertices), "color": int(red == 10)})
            support.update(members)
    need(len(defects) == 12, "objective 12 source")
    need(Counter(row["color"] for row in defects) == {1: 12},
         "selected source has 12 red defects")
    support = sorted(support)
    need(len(support) == 60, "minimum defect support dimension")
    variable = {edge: index + 1 for index, edge in enumerate(support)}

    clauses = set()
    unit_witnesses = {}
    raw_red = raw_blue = 0
    for vertices in combinations(range(N), 5):
        members = [edge_id[edge] for edge in combinations(vertices, 2)]
        free = [edge for edge in members if edge in variable]
        fixed = [edge for edge in members if edge not in variable]
        if all(colors[edge] for edge in fixed):
            clause = tuple(sorted((-variable[edge] for edge in free), key=abs))
            need(clause, "fixed red K5 outside support")
            clauses.add(clause)
            raw_red += 1
        if all(not colors[edge] for edge in fixed):
            clause = tuple(sorted((variable[edge] for edge in free), key=abs))
            need(clause, "fixed blue K5 outside support")
            clauses.add(clause)
            if len(free) == 1 and free[0] not in unit_witnesses:
                unit_witnesses[free[0]] = list(vertices)
            raw_blue += 1
    ordered = sorted(clauses, key=lambda clause: (len(clause), clause))
    need(all(clause and len(clause) == len(set(clause)) for clause in ordered),
         "nonempty normalized clauses")
    cnf = "p cnf {} {}\n".format(len(support), len(ordered))
    cnf += "".join(" ".join(map(str, clause)) + " 0\n" for clause in ordered)
    Path(cnf_path).write_text(cnf)
    widths = Counter(map(len, ordered))
    need(set(unit_witnesses) == set(support), "all support edges have blue unit witnesses")
    red_vertices = defects[0]["vertices"]
    red_edges = [edge_id[edge] for edge in combinations(red_vertices, 2)]
    need(all(edge in variable and colors[edge] for edge in red_edges),
         "red conflict witness")
    red_clause = tuple(-variable[edge] for edge in red_edges)
    core_clauses = [(variable[edge],) for edge in support] + [red_clause]
    core = "p cnf {} {}\n".format(len(support), len(core_clauses))
    core += "".join(" ".join(map(str, clause)) + " 0\n"
                    for clause in core_clauses)
    Path(core_path).write_text(core)
    certificate = {
        "status": "UNIT_PROPAGATION_REFUTATION",
        "forced_red_edges": [
            {"variable": variable[edge], "edge_index": edge,
             "edge": list(edges[edge]), "blue_five_witness": unit_witnesses[edge]}
            for edge in support
        ],
        "red_five_witness": red_vertices,
        "red_conflict_clause": list(red_clause),
        "core_clauses": len(core_clauses),
        "core_sha256": hashlib.sha256(core.encode()).hexdigest(),
    }
    certificate_text = json.dumps(certificate, indent=2, sort_keys=True) + "\n"
    Path(certificate_path).write_text(certificate_text)
    metadata = {
        "status": "BUILT_EXACT_CYCLIC_Q12_DEFECT_SUPPORT_FAMILY",
        "source_index": SOURCE_INDEX,
        "source_toggles": toggles,
        "source_objective": len(defects),
        "source_defects": defects,
        "support_edge_count": len(support),
        "family_assignment_count": 1 << len(support),
        "support_edges": [list(edges[edge]) for edge in support],
        "support_edge_indices": support,
        "variables": len(support),
        "raw_red_constraints": raw_red,
        "raw_blue_constraints": raw_blue,
        "deduplicated_clauses": len(ordered),
        "width_histogram": {str(width): widths[width] for width in sorted(widths)},
        "cnf_bytes": len(cnf.encode()),
        "cnf_sha256": hashlib.sha256(cnf.encode()).hexdigest(),
        "core_bytes": len(core.encode()),
        "core_sha256": hashlib.sha256(core.encode()).hexdigest(),
        "certificate_bytes": len(certificate_text.encode()),
        "certificate_sha256": hashlib.sha256(certificate_text.encode()).hexdigest(),
        "input_sha256": INPUT_SHA256,
    }
    Path(metadata_path).write_text(json.dumps(metadata, indent=2, sort_keys=True) + "\n")
    print(json.dumps(metadata, sort_keys=True))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path)
    parser.add_argument("cnf", type=Path)
    parser.add_argument("core", type=Path)
    parser.add_argument("certificate", type=Path)
    parser.add_argument("metadata", type=Path)
    args = parser.parse_args()
    build(args.input, args.cnf, args.core, args.certificate, args.metadata)
