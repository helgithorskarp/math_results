#!/usr/bin/env python3
"""Exact certificate for cross-edge criticality in the Parts-509 graph.

The graph splits into L={0,...,373} and S={374,...,508}.  This program
classifies all 20*30 pairs (L-interface colour orbit, omitted cross edge).
Positive cases carry explicit four-colouring witnesses.  Negative cases can
carry external DRAT proofs; CNFs and proofs must be kept under /scratch.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import subprocess
import time
from pathlib import Path
from typing import Sequence

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
BASE = ROOT / "hadwiger_nelson_parts509_criticality"
INTERFACE = ROOT / "hadwiger_nelson_parts509_interface_lemma"
FORMAT = "parts509-cross-edge-criticality-v1"
N, SPLIT, K = 509, 374, 4

Edge = tuple[int, int]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for block in iter(lambda: source.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def edge_sha256(edges: Sequence[Edge]) -> str:
    return hashlib.sha256(
        "".join(f"{a} {b}\n" for a, b in edges).encode()
    ).hexdigest()


def load_parts():
    spec = importlib.util.spec_from_file_location("parts509_cross", BASE / "parts509.py")
    mod = importlib.util.module_from_spec(spec)
    if spec.loader is None:
        raise RuntimeError("could not load exact Parts-509 checker")
    spec.loader.exec_module(mod)
    return mod


def load_inputs():
    parts = load_parts()
    points, edges = parts.load_graph(BASE / "parts509.vtx")
    if len(points) != N or len(edges) != 2442:
        raise ValueError("unexpected strict Parts graph")
    L = set(range(SPLIT))
    S = set(range(SPLIT, N))
    ledges = [e for e in edges if e[0] in L and e[1] in L]
    sedges = [e for e in edges if e[0] in S and e[1] in S]
    cross = sorted(
        (a, b) if a in L else (b, a)
        for a, b in edges
        if (a in L) != (b in L)
    )
    if (len(ledges), len(sedges), len(cross)) != (1860, 552, 30):
        raise ValueError("unexpected L/S decomposition")
    interface = json.loads((INTERFACE / "interface_L.json").read_text())
    if interface["class_count"] != 20:
        raise ValueError("unexpected interface class count")
    if interface["cross_edges_L_S"] != [list(edge) for edge in cross]:
        raise ValueError("cross edges disagree with interface certificate")
    return parts, points, edges, ledges, sedges, cross, interface


def color_var(vertex: int, color: int) -> int:
    if not SPLIT <= vertex < N:
        raise ValueError("S vertex out of range")
    return K * (vertex - SPLIT) + color + 1


def case_clauses(
    sedges: Sequence[Edge],
    cross: Sequence[Edge],
    colors_l: Sequence[int],
    omitted_edge_index: int,
) -> list[list[int]]:
    clauses = [
        [color_var(vertex, color) for color in range(K)]
        for vertex in range(SPLIT, N)
    ]
    for a, b in sedges:
        for color in range(K):
            clauses.append([-color_var(a, color), -color_var(b, color)])
    for edge_index, (l_vertex, s_vertex) in enumerate(cross):
        if edge_index != omitted_edge_index:
            clauses.append([-color_var(s_vertex, colors_l[l_vertex])])
    return clauses


def dimacs_bytes(clauses: Sequence[Sequence[int]]) -> bytes:
    header = f"p cnf {K * (N - SPLIT)} {len(clauses)}\n"
    body = "".join(" ".join(map(str, clause)) + " 0\n" for clause in clauses)
    return (header + body).encode()


def extract_s_colors(model: Sequence[int]) -> list[int]:
    positive = {literal for literal in model if literal > 0}
    colors = []
    for vertex in range(SPLIT, N):
        selected = [
            color for color in range(K)
            if color_var(vertex, color) in positive
        ]
        if not selected:
            raise ValueError(f"no selected color at vertex {vertex}")
        colors.append(min(selected))
    return colors


def verify_positive(
    edges: Sequence[Edge],
    omitted: Edge,
    colors_l: Sequence[int],
    colors_s: Sequence[int],
) -> int:
    if len(colors_l) != SPLIT or len(colors_s) != N - SPLIT:
        raise ValueError("malformed coloring witness")
    full = list(colors_l) + list(colors_s)
    if any(color not in range(K) for color in full):
        raise ValueError("color outside 0..3")
    checks = 0
    for edge in edges:
        a, b = edge
        if edge == omitted:
            if full[a] != full[b]:
                raise ValueError(f"omitted edge {edge} endpoints are not equal")
        else:
            checks += 1
            if full[a] == full[b]:
                raise ValueError(f"retained edge {edge} is monochromatic")
    return checks


def write_case_cnf(path: Path, clauses: Sequence[Sequence[int]]) -> str:
    payload = dimacs_bytes(clauses)
    path.write_bytes(payload)
    return hashlib.sha256(payload).hexdigest()


def certify_unsat(cnf: Path, proof: Path, cadical: str, drat_trim: str):
    sat_run = subprocess.run(
        [cadical, "-q", str(cnf), str(proof)],
        capture_output=True,
        text=True,
    )
    if sat_run.returncode != 20:
        raise RuntimeError(
            f"CaDiCaL did not return UNSAT for {cnf.name}: "
            f"exit={sat_run.returncode} stdout={sat_run.stdout[-500:]} "
            f"stderr={sat_run.stderr[-500:]}"
        )
    check = subprocess.run(
        [drat_trim, str(cnf), str(proof)],
        capture_output=True,
        text=True,
    )
    if check.returncode != 0 or "s VERIFIED" not in check.stdout:
        raise RuntimeError(
            f"drat-trim rejected {proof.name}: exit={check.returncode} "
            f"stdout={check.stdout[-500:]} stderr={check.stderr[-500:]}"
        )
    return {
        "proof_file": proof.name,
        "proof_sha256": sha256(proof),
        "proof_bytes": proof.stat().st_size,
        "drat_trim_verified": True,
    }


def validate_certificate(document, proof_dir: Path | None, drat_trim: str | None):
    parts, points, edges, ledges, sedges, cross, interface = load_inputs()
    if document.get("format") != FORMAT:
        raise ValueError("wrong certificate format")
    expected = {
        "source_vtx_sha256": parts.file_sha256(BASE / "parts509.vtx"),
        "strict_edge_sha256": edge_sha256(edges),
        "interface_certificate_sha256": sha256(INTERFACE / "interface_L.json"),
        "vertices": N,
        "strict_edges": 2442,
        "L_edges": 1860,
        "S_edges": 552,
        "cross_edges": 30,
    }
    for field, value in expected.items():
        if document.get(field) != value:
            raise ValueError(f"certificate field {field} disagrees: {document.get(field)!r}")
    if document.get("cross_edge_list") != [list(edge) for edge in cross]:
        raise ValueError("certificate cross-edge list disagrees")
    cases = document.get("cases", [])
    if len(cases) != 20 * 30:
        raise ValueError("certificate must contain 600 cases")
    positive = negative = coloring_checks = proof_bytes = proofs_checked = 0
    leak_classes_by_edge = [[] for _ in cross]
    deleted_edges_by_class = [[] for _ in range(20)]
    for expected_case_index, case in enumerate(cases):
        class_index, edge_index = divmod(expected_case_index, 30)
        if (case.get("class_index"), case.get("omitted_edge_index")) != (
            class_index,
            edge_index,
        ):
            raise ValueError("cases are not in canonical class-major order")
        colors_l = [int(c) for c in interface["classes"][class_index]["witness_colouring_L"]]
        clauses = case_clauses(sedges, cross, colors_l, edge_index)
        cnf_hash = hashlib.sha256(dimacs_bytes(clauses)).hexdigest()
        if case.get("cnf_sha256") != cnf_hash or case.get("clauses") != len(clauses):
            raise ValueError(f"case {class_index},{edge_index}: CNF metadata mismatch")
        if case.get("sat") is True:
            colors_s_text = case.get("witness_colouring_S", "")
            if len(colors_s_text) != N - SPLIT:
                raise ValueError("malformed positive witness")
            colors_s = [int(c) for c in colors_s_text]
            coloring_checks += verify_positive(edges, cross[edge_index], colors_l, colors_s)
            positive += 1
            leak_classes_by_edge[edge_index].append(class_index)
            deleted_edges_by_class[class_index].append(edge_index)
        elif case.get("sat") is False:
            negative += 1
            if proof_dir is not None:
                if not drat_trim:
                    raise ValueError("--drat-trim is required with --proof-dir")
                cnf = proof_dir.parent / "cnfs" / case["cnf_file"]
                proof = proof_dir / case["proof_file"]
                if not cnf.is_file() or not proof.is_file():
                    raise ValueError(f"missing proof material for case {class_index},{edge_index}")
                if sha256(cnf) != cnf_hash:
                    raise ValueError(f"case {class_index},{edge_index}: CNF file hash mismatch")
                if sha256(proof) != case["proof_sha256"]:
                    raise ValueError(f"case {class_index},{edge_index}: proof hash mismatch")
                check = subprocess.run(
                    [drat_trim, str(cnf), str(proof)],
                    capture_output=True,
                    text=True,
                )
                if check.returncode != 0 or "s VERIFIED" not in check.stdout:
                    raise ValueError(f"case {class_index},{edge_index}: proof rejected")
                proof_bytes += proof.stat().st_size
                proofs_checked += 1
        else:
            raise ValueError("case sat field must be Boolean")
    summary = document.get("summary", {})
    expected_summary = {
        "positive_cases": positive,
        "negative_cases": negative,
        "class_positive_counts": [len(row) for row in deleted_edges_by_class],
        "leak_classes_by_cross_edge": leak_classes_by_edge,
        "leaking_cross_edges_by_class": deleted_edges_by_class,
        "classes_with_no_single_edge_leak": [
            index for index, row in enumerate(deleted_edges_by_class) if not row
        ],
    }
    for field, value in expected_summary.items():
        if summary.get(field) != value:
            raise ValueError(f"summary field {field} disagrees")
    if any(not row for row in leak_classes_by_edge):
        raise ValueError("not every cross-edge deletion has a four-coloring witness")
    return {
        "all_checks": True,
        "positive_cases": positive,
        "negative_cases": negative,
        "coloring_edge_checks": coloring_checks,
        "cross_edges_individually_critical": len(cross),
        "classes_with_no_single_edge_leak": expected_summary[
            "classes_with_no_single_edge_leak"
        ],
        "negative_proofs_checked": proofs_checked,
        "proof_bytes_checked": proof_bytes,
    }


def cmd_generate(args):
    from pysat.solvers import Solver

    work = Path(args.work_dir).resolve()
    if not str(work).startswith("/scratch/"):
        raise ValueError("work directory must be under /scratch")
    cnf_dir, proof_dir = work / "cnfs", work / "proofs"
    cnf_dir.mkdir(parents=True, exist_ok=True)
    proof_dir.mkdir(parents=True, exist_ok=True)
    parts, points, edges, ledges, sedges, cross, interface = load_inputs()
    cases = []
    t0 = time.time()
    for class_index, row in enumerate(interface["classes"]):
        colors_l = [int(c) for c in row["witness_colouring_L"]]
        positive_this_class = 0
        for edge_index, omitted in enumerate(cross):
            clauses = case_clauses(sedges, cross, colors_l, edge_index)
            stem = f"class_{class_index:02d}_edge_{edge_index:02d}"
            cnf = cnf_dir / f"{stem}.cnf"
            cnf_hash = write_case_cnf(cnf, clauses)
            with Solver(name=args.solver, bootstrap_with=clauses) as solver:
                sat = solver.solve()
                colors_s = extract_s_colors(solver.get_model()) if sat else None
            case = {
                "class_index": class_index,
                "omitted_edge_index": edge_index,
                "omitted_edge": list(omitted),
                "sat": sat,
                "cnf_file": cnf.name,
                "cnf_sha256": cnf_hash,
                "clauses": len(clauses),
            }
            if sat:
                verify_positive(edges, omitted, colors_l, colors_s)
                case["witness_colouring_S"] = "".join(map(str, colors_s))
                positive_this_class += 1
            else:
                proof = proof_dir / f"{stem}.drat"
                case.update(certify_unsat(cnf, proof, args.cadical, args.drat_trim))
            cases.append(case)
        print(
            f"class={class_index} single_edge_leaks={positive_this_class} "
            f"elapsed={time.time()-t0:.1f}s",
            flush=True,
        )
    leak_classes_by_edge = [[] for _ in cross]
    deleted_edges_by_class = [[] for _ in range(20)]
    for case in cases:
        if case["sat"]:
            ci, ei = case["class_index"], case["omitted_edge_index"]
            leak_classes_by_edge[ei].append(ci)
            deleted_edges_by_class[ci].append(ei)
    document = {
        "format": FORMAT,
        "claim": (
            "All 30 cross edges in the strict Parts-509 L/S decomposition are "
            "individually chromatic-critical; the 600 cases additionally classify "
            "which of the 20 L-interface color orbits leak after each one-edge deletion."
        ),
        "source_vtx_sha256": parts.file_sha256(BASE / "parts509.vtx"),
        "strict_edge_sha256": edge_sha256(edges),
        "interface_certificate_sha256": sha256(INTERFACE / "interface_L.json"),
        "vertices": N,
        "strict_edges": len(edges),
        "L_edges": len(ledges),
        "S_edges": len(sedges),
        "cross_edges": len(cross),
        "cross_edge_list": [list(edge) for edge in cross],
        "cases": cases,
        "summary": {
            "positive_cases": sum(case["sat"] for case in cases),
            "negative_cases": sum(not case["sat"] for case in cases),
            "class_positive_counts": [len(row) for row in deleted_edges_by_class],
            "leak_classes_by_cross_edge": leak_classes_by_edge,
            "leaking_cross_edges_by_class": deleted_edges_by_class,
            "classes_with_no_single_edge_leak": [
                index for index, row in enumerate(deleted_edges_by_class) if not row
            ],
        },
        "generator": {
            "solver": args.solver,
            "cadical_version": subprocess.run(
                [args.cadical, "--version"], capture_output=True, text=True, check=True
            ).stdout.strip(),
            "cadical_binary_sha256": sha256(Path(args.cadical)),
            "drat_trim_binary_sha256": sha256(Path(args.drat_trim)),
            "elapsed_seconds": round(time.time() - t0, 3),
        },
    }
    output = Path(args.output)
    output.write_text(json.dumps(document, indent=1) + "\n")
    print(json.dumps(validate_certificate(document, proof_dir, args.drat_trim), sort_keys=True))
    print(f"wrote {output}")


def cmd_verify(args):
    document = json.loads(Path(args.certificate).read_text())
    proof_dir = Path(args.proof_dir) if args.proof_dir else None
    print(json.dumps(validate_certificate(document, proof_dir, args.drat_trim), sort_keys=True))


def main():
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)
    generate = sub.add_parser("generate")
    generate.add_argument("output")
    generate.add_argument("--work-dir", required=True)
    generate.add_argument("--solver", default="cadical195")
    generate.add_argument("--cadical", required=True)
    generate.add_argument("--drat-trim", required=True)
    generate.set_defaults(func=cmd_generate)
    verify = sub.add_parser("verify")
    verify.add_argument("certificate")
    verify.add_argument("--proof-dir")
    verify.add_argument("--drat-trim")
    verify.set_defaults(func=cmd_verify)
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
