#!/usr/bin/env python3
"""Definition-level checker for the selected defect-support family and core."""
from collections import Counter
from itertools import combinations
from pathlib import Path
import argparse
import csv
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


def digest(data):
    return hashlib.sha256(data).hexdigest()


def graph(input_path):
    raw = Path(input_path).read_bytes()
    need(digest(raw) == INPUT_SHA256, "input identity")
    representatives = json.loads(raw)[
        "complete_additional_objective_12_rotation_representatives"]
    need(len(representatives) == 238, "source count")
    edges = list(combinations(range(N), 2))
    colors = [min(v - u, N - v + u) in LENGTHS for u, v in edges]
    toggles = representatives[SOURCE_INDEX]
    need(toggles == [200, 273, 308, 497, 525, 672, 693, 798, 812, 837,
                     893, 897, 900, 902], "source toggles")
    for edge in toggles:
        colors[edge] ^= True
    return representatives, edges, colors, toggles


def defects_and_support(edges, colors):
    edge_id = {edge: index for index, edge in enumerate(edges)}
    defects = []
    support = set()
    for vertices in combinations(range(N), 5):
        members = tuple(edge_id[edge] for edge in combinations(vertices, 2))
        red = sum(colors[edge] for edge in members)
        if red == 0 or red == 10:
            defects.append((vertices, int(red == 10)))
            support.update(members)
    need(len(defects) == 12 and Counter(color for vertices, color in defects) == {1: 12},
         "selected objective and colors")
    need(len(support) == 60, "selected support dimension")
    return edge_id, defects, sorted(support)


def expected_formula(edge_id, colors, support):
    variables = {edge: index + 1 for index, edge in enumerate(support)}
    clauses = set()
    raw_red = raw_blue = 0
    for vertices in combinations(range(N), 5):
        members = tuple(edge_id[edge] for edge in combinations(vertices, 2))
        free = tuple(edge for edge in members if edge in variables)
        fixed = tuple(edge for edge in members if edge not in variables)
        if all(colors[edge] for edge in fixed):
            need(free, "fixed red K5")
            clauses.add(tuple(sorted((-variables[edge] for edge in free), key=abs)))
            raw_red += 1
        if all(not colors[edge] for edge in fixed):
            need(free, "fixed blue K5")
            clauses.add(tuple(sorted((variables[edge] for edge in free), key=abs)))
            raw_blue += 1
    clauses = sorted(clauses, key=lambda clause: (len(clause), clause))
    return variables, clauses, raw_red, raw_blue


def parse_cnf(path):
    lines = Path(path).read_text().splitlines()
    need(lines, "empty CNF")
    header = lines[0].split()
    need(len(header) == 4 and header[:2] == ["p", "cnf"], "CNF header")
    variables, count = map(int, header[2:])
    need(count == len(lines) - 1, "CNF clause count")
    clauses = []
    for line in lines[1:]:
        values = list(map(int, line.split()))
        need(values and values[-1] == 0 and 0 not in values[:-1], "CNF row")
        clause = tuple(values[:-1])
        need(all(abs(literal) <= variables for literal in clause), "CNF variable")
        need(len(clause) == len(set(clause)) and not any(-x in clause for x in clause),
             "CNF normalized clause")
        clauses.append(clause)
    return variables, clauses


def check_census(path, representatives):
    rows = list(csv.DictReader(Path(path).open(), delimiter="\t"))
    need(len(rows) == len(representatives) == 238, "census row count")
    required = {"index", "toggles", "defects", "red_defects", "blue_defects",
                "support_edges"}
    need(set(rows[0]) == required, "census fields")
    for index, row in enumerate(rows):
        need(int(row["index"]) == index, "census index")
        need(int(row["toggles"]) == len(representatives[index]), "toggle count")
        need(int(row["defects"]) == 12, "census objective")
    chosen = min(rows, key=lambda row: (int(row["support_edges"]), int(row["index"])))
    need(int(chosen["index"]) == SOURCE_INDEX and int(chosen["support_edges"]) == 60,
         "deterministic minimum-support selection")
    return rows


def check(input_path, census_path, family_path, core_path, certificate_path,
          metadata_path):
    representatives, edges, colors, toggles = graph(input_path)
    check_census(census_path, representatives)
    edge_id, defects, support = defects_and_support(edges, colors)
    variables, clauses, raw_red, raw_blue = expected_formula(edge_id, colors, support)
    got_variables, got_clauses = parse_cnf(family_path)
    need(got_variables == 60 and got_clauses == clauses, "complete family formula")
    need(len(clauses) == 600 and raw_red == 12 and raw_blue == 2538,
         "formula counts")

    certificate_bytes = Path(certificate_path).read_bytes()
    certificate = json.loads(certificate_bytes)
    need(certificate["status"] == "UNIT_PROPAGATION_REFUTATION",
         "certificate status")
    rows = certificate["forced_red_edges"]
    need(len(rows) == 60, "60 forcing witnesses")
    need({row["edge_index"] for row in rows} == set(support), "forcing support cover")
    expected_units = []
    for row in rows:
        edge = row["edge_index"]
        need(row["variable"] == variables[edge] and row["edge"] == list(edges[edge]),
             "forcing edge identity")
        vertices = row["blue_five_witness"]
        need(len(vertices) == 5 and len(set(vertices)) == 5
             and vertices == sorted(vertices), "blue witness vertices")
        members = [edge_id[pair] for pair in combinations(vertices, 2)]
        need(edge in members, "forcing edge absent from witness")
        need([member for member in members if member in variables] == [edge],
             "blue witness has another free edge")
        need(all(not colors[member] for member in members if member != edge),
             "blue witness fixed pair is not blue")
        expected_units.append((variables[edge],))

    red_vertices = certificate["red_five_witness"]
    need(tuple(red_vertices) == defects[0][0], "red witness choice")
    red_edges = [edge_id[pair] for pair in combinations(red_vertices, 2)]
    need(all(edge in variables and colors[edge] for edge in red_edges),
         "red witness is not an all-free source defect")
    red_clause = tuple(-variables[edge] for edge in red_edges)
    need(certificate["red_conflict_clause"] == list(red_clause), "red conflict clause")
    expected_core = expected_units + [red_clause]
    core_variables, core_clauses = parse_cnf(core_path)
    need(core_variables == 60 and core_clauses == expected_core, "61-clause physical core")
    need(all(clause in set(clauses) for clause in core_clauses),
         "physical core is not a subset of the complete family formula")
    assignment = {unit[0]: True for unit in expected_units}
    need(len(assignment) == 60 and not any(
        (literal > 0) == assignment[abs(literal)] for literal in red_clause),
        "unit propagation does not falsify red clause")

    core_bytes = Path(core_path).read_bytes()
    family_bytes = Path(family_path).read_bytes()
    need(certificate["core_clauses"] == 61
         and certificate["core_sha256"] == digest(core_bytes), "certificate core binding")
    metadata = json.loads(Path(metadata_path).read_text())
    need(metadata["status"] == "BUILT_EXACT_CYCLIC_Q12_DEFECT_SUPPORT_FAMILY",
         "metadata status")
    expected_fields = {
        "source_index": SOURCE_INDEX, "source_toggles": toggles,
        "source_objective": 12, "support_edge_count": 60,
        "family_assignment_count": 1 << 60, "variables": 60,
        "raw_red_constraints": raw_red, "raw_blue_constraints": raw_blue,
        "deduplicated_clauses": len(clauses), "cnf_bytes": len(family_bytes),
        "cnf_sha256": digest(family_bytes), "core_bytes": len(core_bytes),
        "core_sha256": digest(core_bytes), "certificate_bytes": len(certificate_bytes),
        "certificate_sha256": digest(certificate_bytes), "input_sha256": INPUT_SHA256,
    }
    for key, value in expected_fields.items():
        need(metadata.get(key) == value, "metadata field " + key)
    need(metadata["support_edge_indices"] == support, "metadata support indices")
    need(metadata["support_edges"] == [list(edges[edge]) for edge in support],
         "metadata support pairs")
    need(metadata["source_defects"] == [
        {"vertices": list(vertices), "color": color} for vertices, color in defects],
         "metadata defects")
    widths = Counter(map(len, clauses))
    need(metadata["width_histogram"] == {str(k): widths[k] for k in sorted(widths)},
         "metadata widths")
    result = {
        "status": "VERIFIED_COMPLETE_DEFECT_SUPPORT_FAMILY_UNSAT",
        "source_index": SOURCE_INDEX,
        "source_objective": 12,
        "support_edges": 60,
        "assignments_excluded": 1 << 60,
        "ramsey_clauses_in_complete_formula": 600,
        "physical_core_clauses": 61,
        "blue_unit_witnesses": 60,
        "red_conflict_witnesses": 1,
        "solver_trust": False,
        "good43_candidates": 0,
    }
    print(json.dumps(result, sort_keys=True))
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path)
    parser.add_argument("census", type=Path)
    parser.add_argument("family", type=Path)
    parser.add_argument("core", type=Path)
    parser.add_argument("certificate", type=Path)
    parser.add_argument("metadata", type=Path)
    args = parser.parse_args()
    check(args.input, args.census, args.family, args.core, args.certificate,
          args.metadata)
