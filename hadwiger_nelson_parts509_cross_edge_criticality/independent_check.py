#!/usr/bin/env python3
"""Independent standard-library checker for the cross-edge certificate.

This checker imports none of the generator or exact-coordinate code.  It reads
the previously committed canonical strict edge manifest, replays every positive
colouring, rebuilds every CNF byte-for-byte, and optionally checks every DRAT
proof with an external drat-trim binary.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
EDGE_FILE = ROOT / "hadwiger_nelson_parts509_degree10_replacements" / "edges.json"
INTERFACE_FILE = ROOT / "hadwiger_nelson_parts509_interface_lemma" / "interface_L.json"
VTX_FILE = ROOT / "hadwiger_nelson_parts509_criticality" / "parts509.vtx"
FORMAT = "parts509-cross-edge-criticality-v1"
N, SPLIT, K = 509, 374, 4


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for block in iter(lambda: source.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def edge_sha256(edges):
    payload = "".join(f"{a} {b}\n" for a, b in edges).encode()
    return hashlib.sha256(payload).hexdigest()


def color_var(vertex, color):
    return K * (vertex - SPLIT) + color + 1


def case_cnf_bytes(sedges, cross, colors_l, omitted_index):
    clauses = [
        [color_var(vertex, color) for color in range(K)]
        for vertex in range(SPLIT, N)
    ]
    for a, b in sedges:
        for color in range(K):
            clauses.append([-color_var(a, color), -color_var(b, color)])
    for edge_index, (l_vertex, s_vertex) in enumerate(cross):
        if edge_index != omitted_index:
            clauses.append([-color_var(s_vertex, colors_l[l_vertex])])
    header = f"p cnf {K * (N - SPLIT)} {len(clauses)}\n"
    body = "".join(" ".join(map(str, clause)) + " 0\n" for clause in clauses)
    return (header + body).encode(), len(clauses)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("certificate", nargs="?", default=HERE / "certificate.json")
    parser.add_argument("--proof-dir")
    parser.add_argument("--drat-trim")
    args = parser.parse_args()

    edges = [tuple(edge) for edge in json.loads(EDGE_FILE.read_text())]
    if len(edges) != 2442 or edges != sorted(edges) or len(set(edges)) != len(edges):
        raise ValueError("malformed canonical strict edge manifest")
    L, S = set(range(SPLIT)), set(range(SPLIT, N))
    ledges = [edge for edge in edges if edge[0] in L and edge[1] in L]
    sedges = [edge for edge in edges if edge[0] in S and edge[1] in S]
    cross = sorted(
        (a, b) if a in L else (b, a)
        for a, b in edges
        if (a in L) != (b in L)
    )
    if (len(ledges), len(sedges), len(cross)) != (1860, 552, 30):
        raise ValueError("wrong decomposition")
    interface = json.loads(INTERFACE_FILE.read_text())
    certificate = json.loads(Path(args.certificate).read_text())
    if certificate["format"] != FORMAT:
        raise ValueError("wrong format")
    metadata = {
        "source_vtx_sha256": sha256(VTX_FILE),
        "strict_edge_sha256": edge_sha256(edges),
        "interface_certificate_sha256": sha256(INTERFACE_FILE),
        "vertices": N,
        "strict_edges": 2442,
        "L_edges": 1860,
        "S_edges": 552,
        "cross_edges": 30,
        "cross_edge_list": [list(edge) for edge in cross],
    }
    for key, expected in metadata.items():
        if certificate.get(key) != expected:
            raise ValueError(f"metadata mismatch: {key}")

    # Independently replay all 20 committed L witnesses before using them.
    colors_l_by_class = []
    for class_index, row in enumerate(interface["classes"]):
        colors_l = [int(c) for c in row["witness_colouring_L"]]
        if len(colors_l) != SPLIT or any(colors_l[a] == colors_l[b] for a, b in ledges):
            raise ValueError(f"invalid L witness {class_index}")
        colors_l_by_class.append(colors_l)

    cases = certificate.get("cases", [])
    if len(cases) != 600:
        raise ValueError("expected 600 cases")
    leak_classes_by_edge = [[] for _ in cross]
    leaking_edges_by_class = [[] for _ in range(20)]
    positive = negative = coloring_edge_checks = proof_bytes = proofs_checked = 0
    proof_dir = Path(args.proof_dir) if args.proof_dir else None
    if proof_dir is not None and not args.drat_trim:
        raise ValueError("--drat-trim is required with --proof-dir")

    for case_number, case in enumerate(cases):
        class_index, edge_index = divmod(case_number, 30)
        if case["class_index"] != class_index or case["omitted_edge_index"] != edge_index:
            raise ValueError("noncanonical case order")
        if case["omitted_edge"] != list(cross[edge_index]):
            raise ValueError("omitted edge mismatch")
        colors_l = colors_l_by_class[class_index]
        cnf_payload, clause_count = case_cnf_bytes(sedges, cross, colors_l, edge_index)
        cnf_hash = hashlib.sha256(cnf_payload).hexdigest()
        if case["cnf_sha256"] != cnf_hash or case["clauses"] != clause_count:
            raise ValueError(f"CNF mismatch in case {class_index},{edge_index}")
        if case["sat"]:
            colors_s = [int(c) for c in case["witness_colouring_S"]]
            if len(colors_s) != N - SPLIT or any(c not in range(K) for c in colors_s):
                raise ValueError("malformed S witness")
            colors = colors_l + colors_s
            omitted = cross[edge_index]
            if colors[omitted[0]] != colors[omitted[1]]:
                raise ValueError("omitted edge endpoints differ")
            for edge in edges:
                if edge != omitted:
                    coloring_edge_checks += 1
                    if colors[edge[0]] == colors[edge[1]]:
                        raise ValueError(
                            f"positive case {class_index},{edge_index} conflicts on {edge}"
                        )
            positive += 1
            leak_classes_by_edge[edge_index].append(class_index)
            leaking_edges_by_class[class_index].append(edge_index)
        else:
            negative += 1
            if proof_dir is not None:
                cnf = proof_dir.parent / "cnfs" / case["cnf_file"]
                proof = proof_dir / case["proof_file"]
                if cnf.read_bytes() != cnf_payload:
                    raise ValueError("external CNF bytes differ")
                if sha256(proof) != case["proof_sha256"]:
                    raise ValueError("proof hash mismatch")
                checked = subprocess.run(
                    [args.drat_trim, str(cnf), str(proof)],
                    capture_output=True,
                    text=True,
                )
                if checked.returncode != 0 or "s VERIFIED" not in checked.stdout:
                    raise ValueError(f"proof rejected in case {class_index},{edge_index}")
                proof_bytes += proof.stat().st_size
                proofs_checked += 1

    expected_summary = {
        "positive_cases": positive,
        "negative_cases": negative,
        "class_positive_counts": [len(row) for row in leaking_edges_by_class],
        "leak_classes_by_cross_edge": leak_classes_by_edge,
        "leaking_cross_edges_by_class": leaking_edges_by_class,
        "classes_with_no_single_edge_leak": [
            class_index
            for class_index, edge_indices in enumerate(leaking_edges_by_class)
            if not edge_indices
        ],
    }
    for key, expected in expected_summary.items():
        if certificate["summary"].get(key) != expected:
            raise ValueError(f"summary mismatch: {key}")
    if any(not classes for classes in leak_classes_by_edge):
        raise ValueError("some cross edge lacks a deletion witness")
    print("all_checks=true")
    print(f"strict_unit_pairs={len(edges)} L_edges={len(ledges)} S_edges={len(sedges)} cross_edges={len(cross)}")
    print(f"positive_cases={positive} negative_cases={negative}")
    print(f"coloring_edge_checks={coloring_edge_checks}")
    print(f"cross_edges_individually_critical={len(cross)}")
    print(f"classes_with_no_single_edge_leak={expected_summary['classes_with_no_single_edge_leak']}")
    print(f"negative_proofs_checked={proofs_checked}")
    print(f"proof_bytes_checked={proof_bytes}")


if __name__ == "__main__":
    main()
