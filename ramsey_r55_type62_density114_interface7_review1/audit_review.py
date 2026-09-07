#!/usr/bin/env python3
"""Third-path audit of the interface-7/type-62/density-114 exclusion.

No module from the reviewed package is imported.  This checker rebuilds all
physical templates, checks a fresh full proof replay, and independently emits
and refutes ten formulas by literal five-set substitution.
"""

import argparse
import hashlib
import itertools
import json
from pathlib import Path
import shutil
import subprocess


TARGET = "ramsey_r55_type62_density114_interface7"
UPSTREAM = "ramsey_r55_dense_degree23_hub_classification"
CLASSIFICATION = "ramsey_r55_type62_density114_interface6"
TARGET_SUMS_SHA256 = "8de143656d904da2f615cbc4ae40416473ed784ce2fcdadd5a125022459b2995"
INPUTS_SHA256 = "8e17676c21e4b9c5b03c21e6fdba25d9d9325b77d0f1ee4f2718681c7db2fca2"
CLASSIFICATION_SHA256 = "39491fe6f15eb2ff887c0985cbbe50cced364a27047b7ead39427125f5b86cf8"
TUPLE_STREAM_SHA256 = "84f53e3e52093fd4a466251c12f3ae2e937f5f1166eeb372c08b52b9851fdec8"
TEMPLATE_STREAM_SHA256 = "6f4ba3b05d524e0d2fe1f537026c1dc09ef9bc5dc47d686162805529e66a373a"
MANIFEST_SHA256 = "897ad1057ba5b1e492ac50944afb4895c476b2709f57454b474ccbed9a1ffeef"
SAMPLES = ((0, 0), (0, 1), (127, 0), (424, 1), (848, 0),
           (848, 1), (1272, 0), (1695, 1), (1696, 0), (1696, 1))
PAIRS = tuple(itertools.combinations(range(43), 2))


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def pinned_json(path, expected):
    raw = path.read_bytes()
    require(sha256(raw) == expected, f"identity mismatch: {path}")
    return json.loads(raw)


def check_source(source):
    package = source / TARGET
    sums = package / "SHA256SUMS"
    require(sha256(sums.read_bytes()) == TARGET_SUMS_SHA256,
            "target checksum list changed")
    names = []
    for line in sums.read_text().splitlines():
        expected, name = line.split("  ", 1)
        path = package / name
        require(path.is_file() and sha256(path.read_bytes()) == expected,
                f"target source changed: {name}")
        names.append(name)
    require(len(names) == len(set(names)) == 10, "unexpected target checksum scope")


def graph6(record):
    require(isinstance(record, str) and record and
            all(63 <= ord(char) <= 126 for char in record), "graph6 characters")
    n = ord(record[0]) - 63
    require(n == 22, "interface order")
    bit_count = n * (n - 1) // 2
    bits = []
    for char in record[1:]:
        value = ord(char) - 63
        bits.extend((value >> shift) & 1 for shift in range(5, -1, -1))
    require(len(bits) == ((bit_count + 5) // 6) * 6 and not any(bits[bit_count:]),
            "graph6 length or padding")
    edges = set()
    cursor = 0
    for high in range(n):
        for low in range(high):
            if bits[cursor]:
                edges.add((low, high))
            cursor += 1
    require(len(edges) == 109, "interface edge count")
    return edges


def markings(edges):
    neighbors = tuple(v for v in range(21) if (v, 21) in edges)
    require(neighbors == (16, 17, 18, 19, 20), "hub neighborhood")
    pattern = {(0, 2), (0, 3), (0, 4), (1, 2), (1, 3)}
    induced = {edge for edge in edges if edge[0] in neighbors and edge[1] in neighbors}
    result = []
    for order in itertools.permutations(neighbors):
        image = {tuple(sorted((order[u], order[v]))) for u, v in pattern}
        if image == induced:
            result.append(order)
    require(result == [(16, 17, 18, 19, 20), (16, 17, 19, 18, 20)],
            "complete type-62 marking set")
    return result


def has_clique(adjacency, size, universe):
    def search(candidates, needed):
        if needed == 0:
            return True
        while candidates.bit_count() >= needed:
            bit = candidates & -candidates
            candidates ^= bit
            vertex = bit.bit_length() - 1
            if search(candidates & adjacency[vertex], needed - 1):
                return True
        return False
    return search(universe, size)


def classification_rows(certificate):
    family = certificate.get("family", {})
    rows = family.get("representatives", [])
    require(certificate.get("column_domain") == 7225 and
            certificate.get("cross_edges") == 36 and family.get("type") == 62 and
            family.get("edges") == 114 and family.get("labeled_count") == 461584 and
            family.get("full_tuple_sha256") == TUPLE_STREAM_SHA256 and len(rows) == 1697,
            "classification metadata")
    require({row.get("orbit_size") for row in rows} == {272} and
            sum(row["orbit_size"] for row in rows) == 461584,
            "classification orbit partition")
    require(len({tuple(row.get("columns", ())) for row in rows}) == 1697,
            "duplicate classification representatives")

    residues = {1, 2, 4, 8, 9, 13, 15, 16}
    s_edges = {(0, 2), (0, 3), (0, 4), (1, 2), (1, 3)}
    profiles = {}
    for row in rows:
        columns = row.get("columns")
        require(isinstance(columns, list) and len(columns) == 5 and
                all(type(column) is int and 0 <= column < (1 << 17) for column in columns)
                and sum(column.bit_count() for column in columns) == 36,
                "classification attachment columns")
        profile = tuple(sorted(column.bit_count() for column in columns))
        profiles[profile] = profiles.get(profile, 0) + 1

        red = [0] * 23  # r=0, S=1..5, Paley T=6..22
        for s in range(1, 6):
            red[0] |= 1 << s
            red[s] |= 1
        for u, v in s_edges:
            u, v = u + 1, v + 1
            red[u] |= 1 << v
            red[v] |= 1 << u
        for u, v in itertools.combinations(range(17), 2):
            if (u - v) % 17 in residues:
                u2, v2 = u + 6, v + 6
                red[u2] |= 1 << v2
                red[v2] |= 1 << u2
        for s, column in enumerate(columns, 1):
            for t in range(17):
                if column >> t & 1:
                    vertex = t + 6
                    red[s] |= 1 << vertex
                    red[vertex] |= 1 << s
        require(sum(mask.bit_count() for mask in red) // 2 == 114,
                "representative density")
        require(red[0].bit_count() == 5 and
                sum(mask.bit_count() == 5 for mask in red) == 1,
                "representative unique hub")
        universe = (1 << 23) - 1
        blue = [universe ^ (1 << vertex) ^ red[vertex] for vertex in range(23)]
        require(not has_clique(red, 4, universe), "red K4 in representative")
        require(not has_clique(blue, 5, universe), "blue K5 in representative")
    require(profiles == {(5, 7, 8, 8, 8): 51, (6, 6, 8, 8, 8): 86,
                         (6, 7, 7, 8, 8): 795, (7, 7, 7, 7, 8): 765},
            "classification size profiles")
    return rows


def template(edges, mark, columns):
    fixed = {}

    def put(u, v, color):
        pair = tuple(sorted((u, v)))
        require(u != v and (pair not in fixed or fixed[pair] == int(color)),
                "inconsistent fixed colors")
        fixed[pair] = int(color)

    for pair in itertools.combinations(range(22), 2):
        put(*pair, pair in edges)
    for vertex in range(43):
        if vertex != 22:
            put(22, vertex, vertex < 22)
    for vertex in range(23, 43):
        put(21, vertex, vertex < 40)
    residues = {1, 2, 4, 8, 9, 13, 15, 16}
    for u, v in itertools.combinations(range(17), 2):
        put(u + 23, v + 23, (u - v) % 17 in residues)
    for s, vertex in enumerate(mark):
        for t in range(17):
            put(vertex, t + 23, columns[s] >> t & 1)
    raw = bytes(48 + fixed[pair] if pair in fixed else 50 for pair in PAIRS)
    free = [pair for pair, value in zip(PAIRS, raw) if value == 50]
    active = [pair for pair in free if pair[1] < 40]
    outside = [pair for pair in free if pair[1] >= 40]
    require(len(free) == 389 and len(active) == 272 and len(outside) == 117,
            "physical free/support counts")
    require(all(u < 16 and 23 <= v < 40 for u, v in active),
            "active support is not A by T")
    j_vertices = (22,) + mark + tuple(range(23, 40))
    require(sum(fixed[tuple(sorted(pair))]
                for pair in itertools.combinations(j_vertices, 2)) == 114,
            "physical J density")
    return raw, fixed


def literal_cnf(fixed):
    variables = {pair: index for index, pair in enumerate(
        (pair for pair in PAIRS if pair not in fixed), 1)}
    require(len(variables) == 389, "variable count")
    clauses = set()
    for vertices in itertools.combinations(range(40), 5):
        pairs = tuple(itertools.combinations(vertices, 2))
        colors = tuple(fixed.get(pair) for pair in pairs)
        if 1 not in colors:
            clauses.add(tuple(variables[pair] for pair, color in zip(pairs, colors)
                              if color is None))
        if 0 not in colors:
            clauses.add(tuple(-variables[pair] for pair, color in zip(pairs, colors)
                              if color is None))
    used = {abs(literal) for clause in clauses for literal in clause}
    expected = {index for pair, index in variables.items() if pair[1] < 40}
    require(used == expected and len(used) == 272, "literal CNF support")
    body = "".join(" ".join(map(str, clause)) + " 0\n" for clause in sorted(clauses))
    return f"p cnf 389 {len(clauses)}\n".encode() + body.encode(), len(clauses)


def prove(cnf, scratch, stem, kissat, drat_trim):
    cnf_path = scratch / f"{stem}.cnf"
    proof_path = scratch / f"{stem}.drat"
    cnf_path.write_bytes(cnf)
    solved = subprocess.run([kissat, "--time=30", str(cnf_path), str(proof_path)],
                            stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT,
                            timeout=45)
    require(solved.returncode == 20, f"sample not UNSAT: {stem}")
    checked = subprocess.run([drat_trim, str(cnf_path), str(proof_path)],
                             text=True, capture_output=True, timeout=120)
    require(checked.returncode == 0 and "s VERIFIED" in checked.stdout,
            f"sample proof rejected: {stem}")
    proof_bytes = proof_path.stat().st_size
    require(proof_bytes > 0, f"empty sample proof: {stem}")
    cnf_path.unlink()
    proof_path.unlink()
    return proof_bytes


def replay_audit(replay, expected_templates):
    cohort = replay / "cohort"
    manifest_raw = (cohort / "manifest.json").read_bytes()
    require(sha256(manifest_raw) == MANIFEST_SHA256, "manifest identity")
    manifest = json.loads(manifest_raw)
    runs = json.loads((cohort / "runs.json").read_bytes())
    result = json.loads((cohort / "result.json").read_bytes())
    keys = [[7, 62, j, k] for j in range(1697) for k in range(2)]
    require(len(manifest) == len(runs) == 3394 and
            [row["key"] for row in manifest] == [row["key"] for row in runs] == keys,
            "complete ordered replay cohort")
    require([{field: row[field] for field in
              ("key", "variables", "clauses", "cnf_sha256", "matrix_sha256")}
             for row in runs] == manifest, "run/manifest projection")
    require(result == {"complete_cases": 3394, "interface": 7,
                       "kernel_edge_variables": 272, "kernel_vertices": 40,
                       "manifest_sha256": MANIFEST_SHA256,
                       "new_global_hub_deficiency_lower_bound": 9,
                       "physical_free_edges": 389,
                       "status": "VERIFIED_COMPLETE_INTERFACE7_TYPE62_DENSITY114_EXCLUSION",
                       "unconstrained_outside_edges": 117}, "terminal replay result")
    clauses = []
    matrices = set()
    formulas = set()
    proofs = set()
    proof_bytes = 0
    for row, run, raw in zip(manifest, runs, expected_templates):
        key = tuple(row["key"])
        stem = "-".join(map(str, key))
        saved = (cohort / f"{stem}.matrix").read_bytes()
        require(saved == raw and sha256(raw) == row["matrix_sha256"],
                f"matrix mismatch: {stem}")
        require(row["variables"] == 389 and 19141 <= row["clauses"] <= 19391,
                f"formula dimensions: {stem}")
        require((cohort / f"{stem}.solver.log").read_text().rstrip().endswith("c exit 20"),
                f"solver terminal status: {stem}")
        require("s VERIFIED" in (cohort / f"{stem}.check.log").read_text(),
                f"checker terminal status: {stem}")
        require(run["proof_bytes"] > 0 and len(run["proof_sha256"]) == 64,
                f"proof checkpoint: {stem}")
        clauses.append(row["clauses"])
        matrices.add(row["matrix_sha256"])
        formulas.add(row["cnf_sha256"])
        proofs.add(run["proof_sha256"])
        proof_bytes += run["proof_bytes"]
    require(min(clauses) == 19141 and max(clauses) == 19391 and
            sum(clauses) == 65281067, "clause census")
    require(len(matrices) == len(formulas) == len(proofs) == 3394,
            "artifact distinctness census")
    require(proof_bytes == 88359373, "proof-byte census")
    return {tuple(row["key"]): row for row in manifest}, proof_bytes


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--replay", type=Path, required=True)
    parser.add_argument("--scratch", type=Path, required=True)
    parser.add_argument("--kissat", required=True)
    parser.add_argument("--drat-trim", required=True)
    args = parser.parse_args()
    source = args.source.resolve()
    replay = args.replay.resolve()
    scratch = args.scratch.resolve()
    require(not scratch.exists(), "scratch directory must be new")
    scratch.mkdir(parents=True)
    try:
        check_source(source)
        inputs = pinned_json(source / UPSTREAM / "inputs.json", INPUTS_SHA256)
        certificate = pinned_json(source / CLASSIFICATION / "certificate.json",
                                   CLASSIFICATION_SHA256)
        edges = graph6(inputs["interfaces"][7])
        marks = markings(edges)
        rows = classification_rows(certificate)
        expected_templates = []
        fixed_samples = {}
        stream = hashlib.sha256()
        for j, row in enumerate(rows):
            for k, mark in enumerate(marks):
                key = (7, 62, j, k)
                raw, fixed = template(edges, mark, row["columns"])
                expected_templates.append(raw)
                stream.update((" ".join(map(str, key)) + "\n").encode())
                stream.update(bytes(value - 48 for value in raw))
                if (j, k) in SAMPLES:
                    fixed_samples[key] = fixed
        require(len(set(expected_templates)) == 3394, "template distinctness")
        require(stream.hexdigest() == TEMPLATE_STREAM_SHA256, "template stream identity")
        manifest, replay_proof_bytes = replay_audit(replay, expected_templates)

        sample_clauses = 0
        sample_proof_bytes = 0
        for j, k in SAMPLES:
            key = (7, 62, j, k)
            cnf, count = literal_cnf(fixed_samples[key])
            require(count == manifest[key]["clauses"] and
                    sha256(cnf) == manifest[key]["cnf_sha256"],
                    f"independent formula mismatch: {key}")
            sample_clauses += count
            sample_proof_bytes += prove(cnf, scratch, "-".join(map(str, key)),
                                        args.kissat, args.drat_trim)

        enumeration = json.loads((replay / "enumeration.json").read_bytes())
        classification = json.loads((replay / "classification.json").read_bytes())
        require(enumeration == {"type": 62, "columns": 7225,
                                "outer_pairs": 793798, "c4_pairs": 194750300,
                                "labeled_tuples": 461584}, "enumeration replay")
        require(classification.get("status") ==
                "VERIFIED_COMPLETE_TYPE62_DENSITY114_CLASSIFICATION" and
                classification.get("classes") == 1697 and
                classification.get("labeled_tuples") == 461584 and
                classification.get("full_tuple_sha256") == TUPLE_STREAM_SHA256 and
                classification.get("paley_automorphisms") == 136 and
                classification.get("s_automorphisms") == 2 and
                classification.get("all_rigid") is True and
                classification.get("all_unique_hub") is True,
                "classification audit replay")

        report = {
            "status": "VERIFIED_REVIEW_CHECKPOINT_INTERFACE7_DENSITY114",
            "reviewed_source_commit": "65f3bb69ccba42a11b29d812cabc3e674fdbe0f9",
            "classification": {
                "classes": 1697,
                "labeled_tuples": 461584,
                "orbit_size": 272,
                "all_representatives_directly_checked_R45_23": True,
                "complete_tuple_stream_sha256": TUPLE_STREAM_SHA256,
            },
            "interface": {"number": 7, "vertices": 22, "red_edges": 109,
                          "type62_markings": 2},
            "cohort": {
                "cases": 3394,
                "physical_free_edges": 389,
                "kernel_variables_used": 272,
                "outside_variables_unused": 117,
                "clauses_min": 19141,
                "clauses_max": 19391,
                "clauses_total": 65281067,
                "all_saved_matrices_reconstructed": True,
                "all_solver_logs_unsat": True,
                "all_checker_logs_verified": True,
                "full_replay_proof_bytes": replay_proof_bytes,
                "manifest_sha256": MANIFEST_SHA256,
                "template_stream_sha256": TEMPLATE_STREAM_SHA256,
            },
            "independent_cnf_sample": {
                "cases": len(SAMPLES),
                "keys": [[7, 62, j, k] for j, k in SAMPLES],
                "clauses_total": sample_clauses,
                "all_hashes_match": True,
                "all_new_drat_proofs_verified": True,
                "new_proof_bytes": sample_proof_bytes,
            },
            "scope": {
                "new_interface7_density114_exclusion": "accepted",
                "ramsey_5_5_lower_bound_changed": False,
                "combined_interface6_7_8_requires_separate_interface6_review": True,
            },
        }
        print(json.dumps(report, indent=2, sort_keys=True))
    finally:
        shutil.rmtree(scratch, ignore_errors=True)


if __name__ == "__main__":
    main()
