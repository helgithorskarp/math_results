#!/usr/bin/env python3
"""Independent physical verifier for all 238 defect-support UP refutations."""
from collections import Counter, defaultdict
from itertools import combinations
from pathlib import Path
import argparse
import csv
import hashlib
import json

N = 43
M = 903
INPUT_SHA256 = "4803b2e40dba06c0f82c3d23cbd5ae0a9127da0db24e5655971fff179fb68ec3"
LENGTHS = {1, 2, 7, 10, 12, 13, 14, 16, 18, 20, 21}


def need(condition, message):
    if not condition:
        raise ValueError(message)


def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def enumerate_five_cliques(adjacency):
    """List K5s by bitset recursion, independently of five-subset scanning."""
    answer = []

    def extend(prefix, candidates, remaining):
        if candidates.bit_count() < remaining:
            return
        if remaining == 0:
            answer.append(tuple(prefix))
            return
        while candidates.bit_count() >= remaining:
            bit = candidates & -candidates
            candidates ^= bit
            vertex = bit.bit_length() - 1
            extend(prefix + [vertex], candidates & adjacency[vertex], remaining - 1)

    extend([], (1 << N) - 1, 5)
    return answer


def source_data(input_path, source_index, rows, edges, edge_id, base):
    colors = base.copy()
    for edge in rows[source_index]:
        need(0 <= edge < M, "toggle range")
        colors[edge] ^= True
    red_adjacency = [0] * N
    blue_adjacency = [0] * N
    for edge, (u, v) in enumerate(edges):
        adjacency = red_adjacency if colors[edge] else blue_adjacency
        adjacency[u] |= 1 << v
        adjacency[v] |= 1 << u
    red_defects = enumerate_five_cliques(red_adjacency)
    blue_defects = enumerate_five_cliques(blue_adjacency)
    need(len(red_defects) + len(blue_defects) == 12,
         f"source {source_index}: objective")
    support = set()
    for vertices in red_defects + blue_defects:
        support.update(edge_id[pair] for pair in combinations(vertices, 2))
    return colors, red_defects, blue_defects, support


def candidate_clauses(vertices, support, colors, edge_id):
    members = [edge_id[pair] for pair in combinations(vertices, 2)]
    free = [edge for edge in members if edge in support]
    fixed = [edge for edge in members if edge not in support]
    need(free, "proof witness has no free edge")
    clauses = []
    if all(colors[edge] for edge in fixed):
        clauses.append((0, free))  # avoid red K5: some free edge must be blue
    if all(not colors[edge] for edge in fixed):
        clauses.append((1, free))  # avoid blue K5: some free edge must be red
    need(clauses, "proof witness is not a physical reduced Ramsey clause")
    return clauses


def read_proof(path):
    proof = defaultdict(list)
    with Path(path).open(newline="") as stream:
        reader = csv.DictReader(stream, delimiter="\t")
        need(reader.fieldnames == ["source", "step", "kind", "edge_index", "value",
                                   "v0", "v1", "v2", "v3", "v4"],
             "proof header")
        for row in reader:
            source = int(row["source"])
            need(0 <= source < 238, "proof source range")
            proof[source].append(row)
    need(set(proof) == set(range(238)), "proof source coverage")
    return proof


def verify(input_path, census_path, proof_path):
    need(sha256(input_path) == INPUT_SHA256, "pinned input identity")
    data = json.loads(Path(input_path).read_text())
    rows = data["complete_additional_objective_12_rotation_representatives"]
    need(len(rows) == 238, "source representative count")
    edges = list(combinations(range(N), 2))
    need(len(edges) == M, "physical edge count")
    edge_id = {edge: index for index, edge in enumerate(edges)}
    base = [min(v - u, N - v + u) in LENGTHS for u, v in edges]

    with Path(census_path).open(newline="") as stream:
        census = list(csv.DictReader(stream, delimiter="\t"))
    expected_fields = ["index", "toggles", "red_defects", "blue_defects",
                       "support_edges", "proof_assignments", "core_clauses", "status"]
    need(len(census) == 238 and census[0].keys() == dict.fromkeys(expected_fields).keys(),
         "census shape")
    proof = read_proof(proof_path)

    support_histogram = Counter()
    core_histogram = Counter()
    total_assignments = 0
    proof_rows = 0
    for source_index, census_row in enumerate(census):
        need(int(census_row["index"]) == source_index, "census index order")
        need(int(census_row["toggles"]) == len(rows[source_index]),
             f"source {source_index}: toggle count")
        colors, red_defects, blue_defects, support = source_data(
            input_path, source_index, rows, edges, edge_id, base)
        expected = {
            "red_defects": len(red_defects),
            "blue_defects": len(blue_defects),
            "support_edges": len(support),
        }
        for field, value in expected.items():
            need(int(census_row[field]) == value,
                 f"source {source_index}: census {field}")

        trace = proof[source_index]
        need([int(row["step"]) for row in trace] == list(range(len(trace))),
             f"source {source_index}: proof step order")
        need(len(trace) >= 2 and trace[-1]["kind"] == "CONFLICT"
             and all(row["kind"] == "ASSIGN" for row in trace[:-1]),
             f"source {source_index}: trace termination")
        assignment = {}
        for step, row in enumerate(trace):
            vertices = tuple(int(row[f"v{i}"]) for i in range(5))
            need(vertices == tuple(sorted(set(vertices)))
                 and len(vertices) == 5 and 0 <= vertices[0] and vertices[-1] < N,
                 f"source {source_index} step {step}: witness vertices")
            clauses = candidate_clauses(vertices, support, colors, edge_id)
            if row["kind"] == "ASSIGN":
                edge = int(row["edge_index"])
                value = int(row["value"])
                need(edge in support and edge not in assignment and value in (0, 1),
                     f"source {source_index} step {step}: declared assignment")
                valid = False
                for satisfying_value, free in clauses:
                    unset = [item for item in free if item not in assignment]
                    false_so_far = all(
                        item not in assignment or assignment[item] != satisfying_value
                        for item in free)
                    if (false_so_far and unset == [edge]
                            and value == satisfying_value):
                        valid = True
                need(valid, f"source {source_index} step {step}: not unit propagation")
                assignment[edge] = value
            else:
                need(int(row["edge_index"]) == -1 and int(row["value"]) == -1,
                     f"source {source_index}: conflict sentinel")
                need(any(all(item in assignment and assignment[item] != satisfying_value
                             for item in free)
                         for satisfying_value, free in clauses),
                     f"source {source_index}: final clause is not false")

        need(int(census_row["proof_assignments"]) == len(assignment),
             f"source {source_index}: assignment count")
        need(int(census_row["core_clauses"]) == len(trace),
             f"source {source_index}: core size")
        need(census_row["status"] == "UP_UNSAT",
             f"source {source_index}: status")
        support_histogram[len(support)] += 1
        core_histogram[len(trace)] += 1
        total_assignments += 1 << len(support)
        proof_rows += len(trace)

    result = {
        "status": "VERIFIED_ALL_238_DEFECT_SUPPORT_FAMILIES_UP_UNSAT",
        "source_representatives": 238,
        "up_unsat": 238,
        "up_open": 0,
        "support_min": min(support_histogram),
        "support_max": max(support_histogram),
        "support_histogram": {str(key): support_histogram[key]
                              for key in sorted(support_histogram)},
        "core_clauses_min": min(core_histogram),
        "core_clauses_max": max(core_histogram),
        "proof_rows": proof_rows,
        "indexed_assignment_total": total_assignments,
        "solver_trust": False,
        "good43_candidates": 0,
    }
    print(json.dumps(result, sort_keys=True))
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path)
    parser.add_argument("census", type=Path)
    parser.add_argument("proof", type=Path)
    arguments = parser.parse_args()
    verify(arguments.input, arguments.census, arguments.proof)
