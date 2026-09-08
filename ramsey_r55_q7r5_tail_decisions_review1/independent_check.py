#!/usr/bin/env python3
"""Independent definition-level audit of the h4001 residual decision package."""

import argparse
import hashlib
import json
from itertools import combinations
from pathlib import Path


CATALOG_SHA256 = "53a46ba21cb16805eb07775b60746f783864388538368955e72cbdae5ae8f4e1"


def require(condition, message):
    if not condition:
        raise ValueError(message)


def decode_graph6(line):
    require(len(line) == 19 and line[0] == "N", "expected graph6 order 15")
    bits = []
    for char in line[1:]:
        value = ord(char) - 63
        require(0 <= value < 64, "invalid graph6 character")
        bits.extend((value >> shift) & 1 for shift in range(5, -1, -1))
    require(not any(bits[105:]), "nonzero graph6 padding")
    core = {}
    cursor = 0
    for right in range(1, 15):
        for left in range(right):
            core[left, right] = bits[cursor]
            cursor += 1
    require(cursor == 105, "graph6 payload length")
    return core


def fixed_edges(core):
    fixed = dict(core)
    for start in (15, 19):
        for edge in combinations(range(start, start + 4), 2):
            fixed[edge] = 0
    return fixed


def variable_map(fixed):
    free = [edge for edge in combinations(range(23), 2) if edge not in fixed]
    require(len(free) == 136, "free-edge count")
    return free, {edge: index + 1 for index, edge in enumerate(free)}


def physical_clauses(fixed, variables):
    clauses = []
    for order, forbidden_color in ((4, 1), (5, 0)):
        for vertices in combinations(range(23), order):
            row = []
            already_safe = False
            for edge in combinations(vertices, 2):
                if edge in fixed:
                    if fixed[edge] != forbidden_color:
                        already_safe = True
                        break
                else:
                    row.append((-1 if forbidden_color else 1) * variables[edge])
            if not already_safe:
                require(row, "fixed forbidden clique")
                clauses.append(row)
    return clauses


def comparator(left, right, next_aux):
    require(len(left) == len(right) and left, "comparator width")
    clauses = []
    prefix = None
    for position, (x_bit, y_bit) in enumerate(zip(left, right)):
        clauses.append(([] if prefix is None else [-prefix]) + [-x_bit, y_bit])
        if position == len(left) - 1:
            continue
        new_prefix = next_aux
        next_aux += 1
        if prefix is not None:
            clauses.append([-new_prefix, prefix])
        clauses.append([-new_prefix, -x_bit, y_bit])
        clauses.append([-new_prefix, x_bit, -y_bit])
        clauses.append(([] if prefix is None else [-prefix]) + [-x_bit, -y_bit, new_prefix])
        clauses.append(([] if prefix is None else [-prefix]) + [x_bit, y_bit, new_prefix])
        prefix = new_prefix
    return clauses, next_aux


def ordering_clauses(variables):
    words = []
    signature = lambda vertex: [variables[i, vertex] for i in range(14, -1, -1)]
    for start in (15, 19):
        for vertex in range(start, start + 3):
            words.append((signature(vertex), signature(vertex + 1)))
    words.append((
        [bit for vertex in range(18, 14, -1) for bit in signature(vertex)],
        [bit for vertex in range(22, 18, -1) for bit in signature(vertex)],
    ))
    clauses = []
    next_aux = 137
    for left, right in words:
        rows, next_aux = comparator(left, right, next_aux)
        clauses.extend(rows)
    require(next_aux == 280 and len(clauses) == 858, "ordering dimensions")
    return clauses


def formula_bytes(core):
    fixed = fixed_edges(core)
    _, variables = variable_map(fixed)
    clauses = physical_clauses(fixed, variables) + ordering_clauses(variables)
    body = "".join(" ".join(map(str, row)) + " 0\n" for row in clauses)
    return f"p cnf 279 {len(clauses)}\n{body}".encode("ascii"), len(clauses)


def complete_graph(core, word):
    fixed = fixed_edges(core)
    free, _ = variable_map(fixed)
    require(isinstance(word, str) and len(word) == 136 and set(word) <= {"0", "1"}, "witness word")
    graph = dict(fixed)
    graph.update({edge: int(word[index]) for index, edge in enumerate(free)})
    return graph


def check_witness(core, word):
    graph = complete_graph(core, word)
    for vertices in combinations(range(23), 4):
        require(not all(graph[edge] == 1 for edge in combinations(vertices, 2)), "red K4 in witness")
    for vertices in combinations(range(23), 5):
        require(not all(graph[edge] == 0 for edge in combinations(vertices, 2)), "blue K5 in witness")
    signatures = {
        vertex: sum(graph[tuple(sorted((core_vertex, vertex)))] << core_vertex for core_vertex in range(15))
        for vertex in range(15, 23)
    }
    for block in (range(15, 19), range(19, 23)):
        values = [signatures[vertex] for vertex in block]
        require(values == sorted(values), "witness block is not normalized")
    block_words = [sum(signatures[vertex] << (15 * offset) for offset, vertex in enumerate(block))
                   for block in (range(15, 19), range(19, 23))]
    require(block_words[0] <= block_words[1], "witness block pair is not normalized")


def check_run(run_root, lines, rows, cores):
    replay = json.loads((run_root / "REPLAY.json").read_text())
    require(replay["status"] == "REPRODUCED_ALL_640_TAIL_DECISIONS", "replay status")
    require(replay["cases"] == 640 and replay["sat"] == 122 and replay["unsat"] == 518, "replay counts")
    total_proof_bytes = 0
    published_proof_hash_matches = 0
    digest_rows = []
    for index, expected in enumerate(rows):
        directory = run_root / f"canonical-{index:04d}"
        actual = json.loads((directory / "result.json").read_text())
        require(actual["index"] == index and actual["core"] == lines[index], "replay identity")
        formula, _ = formula_bytes(cores[index])
        require((directory / "tail.cnf").read_bytes() == formula, "replay CNF bytes")
        if expected["tail_status"] == "SAT":
            require(actual["status"] == "SAT", "replayed SAT status")
            check_witness(cores[index], actual["free_edges"])
            evidence_hash = hashlib.sha256(actual["free_edges"].encode()).hexdigest()
        else:
            require(actual["status"] == "UNSAT_CHECKED", "replayed UNSAT status")
            proof_path = directory / actual["proof_file"]
            proof_hash = hashlib.sha256(proof_path.read_bytes()).hexdigest()
            require(proof_hash == actual["proof_sha256"], "replay proof digest")
            total_proof_bytes += proof_path.stat().st_size
            published_proof_hash_matches += int(proof_hash == expected["proof_sha256"])
            evidence_hash = proof_hash
        digest_rows.append(f"{index}:{actual['status']}:{actual['cnf_sha256']}:{evidence_hash}")
    return {
        "fresh_replay_status": replay["status"],
        "fresh_replay_seconds": replay["seconds"],
        "fresh_replay_unsat_checked": replay["unsat"],
        "fresh_replay_sat": replay["sat"],
        "fresh_replay_proof_bytes": total_proof_bytes,
        "published_proof_hash_matches": published_proof_hash_matches,
        "fresh_replay_evidence_digest": hashlib.sha256(("\n".join(digest_rows) + "\n").encode()).hexdigest(),
        "checker_sha256": replay["checker_sha256"],
        "python_sat": replay["python_sat"],
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--catalog", required=True)
    parser.add_argument("--target", default=str(Path(__file__).resolve().parents[1] / "ramsey_r55_q7r5_tail_decisions"))
    parser.add_argument("--run")
    args = parser.parse_args()

    catalog_raw = Path(args.catalog).read_bytes()
    require(hashlib.sha256(catalog_raw).hexdigest() == CATALOG_SHA256, "catalog SHA-256")
    lines = catalog_raw.decode("ascii").splitlines()
    require(len(lines) == 640 and len(set(lines)) == 640, "catalog record count")
    target = Path(args.target)
    rows = json.loads((target / "RESULTS.json").read_text())
    witnesses = json.loads((target / "TAIL_WITNESSES.json").read_text())
    tasks = json.loads((target / "TASKS.json").read_text())
    require(len(rows) == 640 and [row["index"] for row in rows] == list(range(640)), "result rows")

    cores = []
    statuses = {"SAT": [], "UNSAT": []}
    total_clauses = 0
    for index, (line, row) in enumerate(zip(lines, rows)):
        core = decode_graph6(line)
        for vertices in combinations(range(15), 4):
            colors = {core[edge] for edge in combinations(vertices, 2)}
            require(colors == {0, 1}, "catalog record is not Ramsey(4,4;15)")
        formula, clause_count = formula_bytes(core)
        require(hashlib.sha256(formula).hexdigest() == row["cnf_sha256"], "CNF SHA-256")
        require(clause_count == row["clauses"], "CNF clause count")
        require(row["tail_status"] in statuses, "unexpected status")
        statuses[row["tail_status"]].append(index)
        total_clauses += clause_count
        cores.append(core)

    require(set(witnesses) == {str(index) for index in statuses["SAT"]}, "witness key set")
    for key, word in witnesses.items():
        check_witness(cores[int(key)], word)
    require(tasks["excluded_core_indices"] == statuses["UNSAT"], "excluded task interface")
    require(tasks["retained_core_indices"] == statuses["SAT"], "retained task interface")
    require(tasks["remaining_global_tasks"] == 2_189_178 - len(statuses["UNSAT"]), "global task arithmetic")

    report = {
        "status": "INDEPENDENT_H4001_AUDIT_PASSED",
        "catalog_records": len(lines),
        "catalog_records_distinct": len(set(lines)),
        "core_ramsey_checks": 640,
        "cnf_sha256_matches": 640,
        "cnf_clauses_rebuilt": total_clauses,
        "tail_unsat_table_entries": len(statuses["UNSAT"]),
        "tail_sat_witnesses_checked": len(statuses["SAT"]),
        "physical43_tasks_remaining": tasks["remaining_global_tasks"],
        "good43_constructed": False,
    }
    if args.run:
        report.update(check_run(Path(args.run), lines, rows, cores))
    print(json.dumps(report, sort_keys=True))


if __name__ == "__main__":
    main()
