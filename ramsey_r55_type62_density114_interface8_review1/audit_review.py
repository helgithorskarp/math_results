#!/usr/bin/env python3
"""Independent audit of the interface-8/type-62/density-114 exclusion.

This program deliberately does not import code from the reviewed package.  It
reconstructs the physical templates from the pinned mathematical inputs,
checks every case against a fresh full replay, and directly encodes and
refutes a stratified sample of the 40-vertex kernels.
"""

import argparse
import hashlib
import itertools
import json
from pathlib import Path
import shutil
import subprocess


TARGET = "ramsey_r55_type62_density114_interface8"
UPSTREAM = "ramsey_r55_dense_degree23_hub_classification"
CLASSIFICATION = "ramsey_r55_type62_density114_interface6"
TARGET_SUMS_SHA256 = "58115d3877d2ce5660c9bd5921d4f6c3f121b351d117299f7619a949a1aa8fa4"
INPUTS_SHA256 = "8e17676c21e4b9c5b03c21e6fdba25d9d9325b77d0f1ee4f2718681c7db2fca2"
CLASSIFICATION_SHA256 = "39491fe6f15eb2ff887c0985cbbe50cced364a27047b7ead39427125f5b86cf8"
TUPLE_STREAM_SHA256 = "84f53e3e52093fd4a466251c12f3ae2e937f5f1166eeb372c08b52b9851fdec8"
TEMPLATE_STREAM_SHA256 = "14f68e5f54aff43826d29057fc543b7db09a535aab910c3026680cd8e6995e25"
MANIFEST_SHA256 = "fd983b33f500c896939d566c7ef87731545e85c6e68ed4879310c2966b65c577"
SAMPLES = ((0, 0), (0, 1), (127, 0), (424, 1), (848, 0),
           (848, 1), (1272, 0), (1695, 1), (1696, 0), (1696, 1))
PAIRS = tuple(itertools.combinations(range(43), 2))


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def read_pinned_json(path, expected_hash):
    raw = path.read_bytes()
    require(digest(raw) == expected_hash, f"identity mismatch: {path}")
    return json.loads(raw)


def check_target_package(source):
    package = source / TARGET
    sums = package / "SHA256SUMS"
    require(digest(sums.read_bytes()) == TARGET_SUMS_SHA256,
            "reviewed package checksum list changed")
    listed = []
    for line in sums.read_text().splitlines():
        expected, name = line.split("  ", 1)
        path = package / name
        require(path.is_file() and digest(path.read_bytes()) == expected,
                f"reviewed source changed: {name}")
        listed.append(name)
    require(len(listed) == 10 and len(set(listed)) == 10,
            "unexpected reviewed package checksum scope")


def decode_graph6(record):
    """Decode a small graph6 record using a streaming six-bit reader."""
    require(isinstance(record, str) and record, "empty graph6 record")
    require(all(63 <= ord(char) <= 126 for char in record),
            "invalid graph6 character")
    n = ord(record[0]) - 63
    require(n == 22, "interface 8 does not have order 22")
    needed = n * (n - 1) // 2
    payload = []
    for char in record[1:]:
        word = ord(char) - 63
        payload.extend((word >> shift) & 1 for shift in range(5, -1, -1))
    require(len(payload) == ((needed + 5) // 6) * 6 and not any(payload[needed:]),
            "invalid graph6 length or padding")
    edges = set()
    cursor = 0
    for high in range(n):
        for low in range(high):
            if payload[cursor]:
                edges.add((low, high))
            cursor += 1
    require(cursor == needed and len(edges) == 109, "interface edge count")
    return edges


def type62_markings(edges):
    hub = 21
    neighbors = tuple(v for v in range(hub) if (v, hub) in edges)
    require(neighbors == (16, 17, 18, 19, 20), "unexpected hub neighborhood")
    pattern = {(0, 2), (0, 3), (0, 4), (1, 2), (1, 3)}
    induced = {edge for edge in edges if edge[0] in neighbors and edge[1] in neighbors}
    marks = []
    for order in itertools.permutations(neighbors):
        image = {tuple(sorted((order[u], order[v]))) for u, v in pattern}
        if image == induced:
            marks.append(order)
    require(marks == [(16, 17, 18, 19, 20), (16, 17, 19, 18, 20)],
            "the two type-62 markings changed")
    return marks


def has_clique(adjacency, size, universe):
    """Exact bit-set clique decision, independent of the reviewed enumerators."""
    def search(candidates, remaining):
        if remaining == 0:
            return True
        while candidates.bit_count() >= remaining:
            bit = candidates & -candidates
            candidates ^= bit
            vertex = bit.bit_length() - 1
            if search(candidates & adjacency[vertex], remaining - 1):
                return True
        return False
    return search(universe, size)


def audit_classification(certificate):
    family = certificate.get("family", {})
    reps = family.get("representatives", [])
    require(family.get("type") == 62 and family.get("edges") == 114,
            "classification family metadata")
    require(certificate.get("cross_edges") == 36 and certificate.get("column_domain") == 7225,
            "classification density metadata")
    require(family.get("labeled_count") == 461584 and len(reps) == 1697,
            "classification cardinality")
    require(family.get("full_tuple_sha256") == TUPLE_STREAM_SHA256,
            "classification tuple stream identity")
    require(sum(row.get("orbit_size", 0) for row in reps) == 461584 and
            {row.get("orbit_size") for row in reps} == {272},
            "classification orbit partition")

    residues = {1, 2, 4, 8, 9, 13, 15, 16}
    s_edges = {(0, 2), (0, 3), (0, 4), (1, 2), (1, 3)}
    profiles = {}
    unique_rows = set()
    for row in reps:
        columns = row.get("columns")
        require(isinstance(columns, list) and len(columns) == 5 and
                all(type(column) is int and 0 <= column < (1 << 17) for column in columns),
                "invalid attachment columns")
        require(sum(column.bit_count() for column in columns) == 36,
                "wrong attachment density")
        unique_rows.add(tuple(columns))
        profile = tuple(sorted(column.bit_count() for column in columns))
        profiles[profile] = profiles.get(profile, 0) + 1

        # Canonical J has r=0, S=1..5 and the Paley vertices 6..22.
        red = [0] * 23
        for s in range(1, 6):
            red[0] |= 1 << s
            red[s] |= 1
        for u, v in s_edges:
            u += 1
            v += 1
            red[u] |= 1 << v
            red[v] |= 1 << u
        for u, v in itertools.combinations(range(17), 2):
            if (u - v) % 17 in residues:
                a, b = u + 6, v + 6
                red[a] |= 1 << b
                red[b] |= 1 << a
        for s, column in enumerate(columns, 1):
            for t in range(17):
                if column >> t & 1:
                    v = t + 6
                    red[s] |= 1 << v
                    red[v] |= 1 << s
        require(sum(bits.bit_count() for bits in red) // 2 == 114,
                "representative does not have 114 red edges")
        require([bits.bit_count() for bits in red].count(5) == 1 and
                red[0].bit_count() == 5, "representative hub is not unique")
        all_vertices = (1 << 23) - 1
        blue = [all_vertices ^ (1 << v) ^ red[v] for v in range(23)]
        require(not has_clique(red, 4, all_vertices), "red K4 in classified J")
        require(not has_clique(blue, 5, all_vertices), "blue K5 in classified J")

    require(len(unique_rows) == 1697, "duplicate classification representatives")
    require(profiles == {(5, 7, 8, 8, 8): 51, (6, 6, 8, 8, 8): 86,
                         (6, 7, 7, 8, 8): 795, (7, 7, 7, 7, 8): 765},
            "classification profile census")
    return reps


def physical_template(edges, mark, columns):
    """Build all 903 colors from the graph-theoretic decomposition."""
    fixed = {}

    def assign(u, v, color):
        pair = (u, v) if u < v else (v, u)
        color = int(color)
        require(pair not in fixed or fixed[pair] == color, "inconsistent mathematical pins")
        fixed[pair] = color

    for pair in itertools.combinations(range(22), 2):
        assign(*pair, pair in edges)
    for vertex in range(43):
        if vertex != 22:
            assign(22, vertex, vertex < 22)
    for vertex in range(23, 43):
        assign(21, vertex, vertex < 40)
    residues = {1, 2, 4, 8, 9, 13, 15, 16}
    for u, v in itertools.combinations(range(17), 2):
        assign(u + 23, v + 23, (u - v) % 17 in residues)
    for s_index, s_vertex in enumerate(mark):
        for t in range(17):
            assign(s_vertex, t + 23, columns[s_index] >> t & 1)

    raw = bytes(48 + fixed[pair] if pair in fixed else 50 for pair in PAIRS)
    free = [pair for pair, value in zip(PAIRS, raw) if value == 50]
    require(len(free) == 389, "wrong number of physical free pairs")
    active = [pair for pair in free if pair[1] < 40]
    outside = [pair for pair in free if pair[1] >= 40]
    require(len(active) == 272 and len(outside) == 117,
            "wrong active/outside support split")
    require(all(u < 16 and 23 <= v < 40 for u, v in active),
            "kernel support is not exactly A by T")

    j = (22,) + mark + tuple(range(23, 40))
    red_edges = sum(fixed[tuple(sorted(pair))] for pair in itertools.combinations(j, 2))
    require(red_edges == 114, "reconstructed J does not have density 114")
    return raw, fixed


def direct_cnf(fixed):
    """Substitute every one of C(40,5) vertex sets literally."""
    variables = {pair: index for index, pair in enumerate(
        (pair for pair in PAIRS if pair not in fixed), 1)}
    require(len(variables) == 389, "direct encoder variable count")
    clauses = set()
    used = set()
    for vertices in itertools.combinations(range(40), 5):
        pairs = tuple(itertools.combinations(vertices, 2))
        values = tuple(fixed.get(pair) for pair in pairs)
        if 1 not in values:  # Could be an all-blue K5.
            clause = tuple(variables[pair] for pair, value in zip(pairs, values) if value is None)
            clauses.add(clause)
        if 0 not in values:  # Could be an all-red K5.
            clause = tuple(-variables[pair] for pair, value in zip(pairs, values) if value is None)
            clauses.add(clause)
    for clause in clauses:
        used.update(map(abs, clause))
    expected_used = {index for pair, index in variables.items() if pair[1] < 40}
    require(used == expected_used and len(used) == 272,
            "direct formula does not use exactly the kernel support")
    body = "".join(" ".join(map(str, clause)) + " 0\n" for clause in sorted(clauses))
    data = f"p cnf 389 {len(clauses)}\n".encode() + body.encode()
    return data, len(clauses)


def check_native_proof(cnf, scratch, stem, kissat, drat_trim):
    cnf_path = scratch / f"{stem}.cnf"
    proof_path = scratch / f"{stem}.drat"
    cnf_path.write_bytes(cnf)
    solved = subprocess.run([kissat, "--time=30", str(cnf_path), str(proof_path)],
                            stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT,
                            timeout=45)
    require(solved.returncode == 20, f"sample {stem} was not proved UNSAT")
    checked = subprocess.run([drat_trim, str(cnf_path), str(proof_path)],
                             text=True, capture_output=True, timeout=120)
    require(checked.returncode == 0 and "s VERIFIED" in checked.stdout,
            f"sample {stem} DRAT proof rejected")
    size = proof_path.stat().st_size
    require(size > 0, f"sample {stem} emitted an empty proof")
    cnf_path.unlink()
    proof_path.unlink()
    return size


def audit_replay(replay, expected_templates, manifest_by_key):
    cohort = replay / "cohort"
    manifest_raw = (cohort / "manifest.json").read_bytes()
    require(digest(manifest_raw) == MANIFEST_SHA256, "fresh replay manifest identity")
    manifest = json.loads(manifest_raw)
    runs = json.loads((cohort / "runs.json").read_bytes())
    result = json.loads((cohort / "result.json").read_bytes())
    expected_keys = [[8, 62, j, k] for j in range(1697) for k in range(2)]
    require(len(manifest) == len(runs) == 3394, "fresh replay cohort length")
    require([row.get("key") for row in manifest] == expected_keys and
            [row.get("key") for row in runs] == expected_keys,
            "fresh replay keys are not the complete ordered cohort")
    require([{key: row[key] for key in ("key", "variables", "clauses", "cnf_sha256", "matrix_sha256")}
             for row in runs] == manifest, "run checkpoint differs from manifest")
    require(result == {"complete_cases": 3394, "interface": 8,
                       "kernel_edge_variables": 272, "kernel_vertices": 40,
                       "manifest_sha256": MANIFEST_SHA256,
                       "new_global_hub_deficiency_lower_bound": 9,
                       "physical_free_edges": 389,
                       "status": "VERIFIED_COMPLETE_INTERFACE8_TYPE62_DENSITY114_EXCLUSION",
                       "unconstrained_outside_edges": 117},
            "fresh replay terminal result")

    proof_bytes = 0
    proof_hashes = set()
    clause_counts = []
    cnf_hashes = set()
    matrix_hashes = set()
    for row, raw in zip(manifest, expected_templates):
        key = tuple(row["key"])
        stem = "-".join(map(str, key))
        saved = (cohort / f"{stem}.matrix").read_bytes()
        require(saved == raw and digest(raw) == row["matrix_sha256"],
                f"physical matrix mismatch at {stem}")
        require(row["variables"] == 389 and 19150 <= row["clauses"] <= 19352,
                f"formula dimensions at {stem}")
        require((cohort / f"{stem}.solver.log").read_text().rstrip().endswith("c exit 20"),
                f"missing UNSAT terminal log at {stem}")
        require("s VERIFIED" in (cohort / f"{stem}.check.log").read_text(),
                f"missing proof-check terminal log at {stem}")
        run = runs[len(clause_counts)]
        require(run["proof_bytes"] > 0 and len(run["proof_sha256"]) == 64,
                f"invalid proof checkpoint at {stem}")
        proof_bytes += run["proof_bytes"]
        proof_hashes.add(run["proof_sha256"])
        clause_counts.append(row["clauses"])
        cnf_hashes.add(row["cnf_sha256"])
        matrix_hashes.add(row["matrix_sha256"])
        manifest_by_key[key] = row
    require(sum(clause_counts) == 65279286 and min(clause_counts) == 19150 and
            max(clause_counts) == 19352, "formula clause census")
    require(len(cnf_hashes) == len(matrix_hashes) == 3394,
            "cohort matrices or formulas are not pairwise distinct")
    # A DRAT trace contains learned clauses rather than an input-formula header;
    # the same trace may validly refute more than one related formula.
    require(len(proof_hashes) == 3378, "fresh replay proof-hash census")
    require(proof_bytes == 162683102, "fresh replay proof byte census")
    return manifest, proof_bytes


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True,
                        help="checkout of math_source_code_open at ea9d87a2552b...")
    parser.add_argument("--replay", type=Path, required=True,
                        help="fresh output of the reviewed reproduce.py command")
    parser.add_argument("--scratch", type=Path, required=True,
                        help="new reviewer-owned scratch directory")
    parser.add_argument("--kissat", required=True)
    parser.add_argument("--drat-trim", required=True)
    args = parser.parse_args()
    source = args.source.resolve()
    replay = args.replay.resolve()
    scratch = args.scratch.resolve()
    require(not scratch.exists(), "scratch path must be new")
    scratch.mkdir(parents=True)
    try:
        check_target_package(source)
        inputs = read_pinned_json(source / UPSTREAM / "inputs.json", INPUTS_SHA256)
        certificate = read_pinned_json(source / CLASSIFICATION / "certificate.json",
                                       CLASSIFICATION_SHA256)
        edges = decode_graph6(inputs["interfaces"][8])
        marks = type62_markings(edges)
        representatives = audit_classification(certificate)

        expected_templates = []
        template_digest = hashlib.sha256()
        fixed_by_key = {}
        for j, row in enumerate(representatives):
            for k, mark in enumerate(marks):
                key = (8, 62, j, k)
                raw, fixed = physical_template(edges, mark, row["columns"])
                expected_templates.append(raw)
                template_digest.update((" ".join(map(str, key)) + "\n").encode())
                template_digest.update(bytes(value - 48 for value in raw))
                if (j, k) in SAMPLES:
                    fixed_by_key[key] = fixed
        require(len(set(expected_templates)) == 3394, "physical templates are not distinct")
        require(template_digest.hexdigest() == TEMPLATE_STREAM_SHA256,
                "independently reconstructed template stream changed")

        manifest_by_key = {}
        _, proof_bytes = audit_replay(replay, expected_templates, manifest_by_key)
        sample_clause_total = 0
        new_proof_bytes = 0
        for j, k in SAMPLES:
            key = (8, 62, j, k)
            cnf, clauses = direct_cnf(fixed_by_key[key])
            expected = manifest_by_key[key]
            require(clauses == expected["clauses"] and digest(cnf) == expected["cnf_sha256"],
                    f"independent CNF differs at {key}")
            sample_clause_total += clauses
            new_proof_bytes += check_native_proof(
                cnf, scratch, "-".join(map(str, key)), args.kissat, args.drat_trim)

        enumeration = json.loads((replay / "enumeration.json").read_bytes())
        classification = json.loads((replay / "classification.json").read_bytes())
        require(enumeration == {"type": 62, "columns": 7225, "outer_pairs": 793798,
                                "c4_pairs": 194750300, "labeled_tuples": 461584},
                "full independent enumeration checkpoint")
        require(classification.get("status") ==
                "VERIFIED_COMPLETE_TYPE62_DENSITY114_CLASSIFICATION" and
                classification.get("classes") == 1697 and
                classification.get("labeled_tuples") == 461584 and
                classification.get("full_tuple_sha256") == TUPLE_STREAM_SHA256 and
                classification.get("paley_automorphisms") == 136 and
                classification.get("s_automorphisms") == 2 and
                classification.get("all_rigid") is True and
                classification.get("all_unique_hub") is True,
                "classification replay checkpoint")

        report = {
            "status": "VERIFIED_REVIEW_CHECKPOINT_INTERFACE8_DENSITY114",
            "reviewed_source_commit": "ea9d87a2552b2b6147d4b702aadd54f2674da271",
            "classification": {
                "classes": 1697,
                "labeled_tuples": 461584,
                "orbit_size": 272,
                "all_representatives_directly_checked_R45_23": True,
                "complete_tuple_stream_sha256": TUPLE_STREAM_SHA256,
            },
            "interface": {"number": 8, "vertices": 22, "red_edges": 109,
                          "type62_markings": 2},
            "cohort": {
                "cases": 3394,
                "physical_free_edges": 389,
                "kernel_variables_used": 272,
                "outside_variables_unused": 117,
                "clauses_min": 19150,
                "clauses_max": 19352,
                "clauses_total": 65279286,
                "all_saved_matrices_reconstructed": True,
                "all_solver_logs_unsat": True,
                "all_checker_logs_verified": True,
                "full_replay_proof_bytes": proof_bytes,
                "manifest_sha256": MANIFEST_SHA256,
                "template_stream_sha256": TEMPLATE_STREAM_SHA256,
            },
            "independent_cnf_sample": {
                "cases": len(SAMPLES),
                "keys": [[8, 62, j, k] for j, k in SAMPLES],
                "clauses_total": sample_clause_total,
                "all_hashes_match": True,
                "all_new_drat_proofs_verified": True,
                "new_proof_bytes": new_proof_bytes,
            },
            "scope": {
                "new_interface8_density114_exclusion": "accepted",
                "combined_interface6_7_8_corollary_imports_unreviewed_interface7": True,
                "ramsey_5_5_lower_bound_changed": False,
            },
        }
        print(json.dumps(report, indent=2, sort_keys=True))
    finally:
        shutil.rmtree(scratch, ignore_errors=True)


if __name__ == "__main__":
    main()
