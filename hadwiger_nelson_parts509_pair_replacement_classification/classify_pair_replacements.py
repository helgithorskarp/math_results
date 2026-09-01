#!/usr/bin/env python3
"""Classify the 63 Parts-509 two-delete/two-add candidates.

The candidate list is the ``pairs_with_U_eq2`` field of the sibling
two-point-augmentation certificate.  Geometry is reconstructed exactly in
Q(sqrt(3),sqrt(5),sqrt(11)); SAT is used only by ``search``.  ``verify``
checks every stored colouring without a solver and can rebuild every CNF.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import itertools
import json
import re
import sys
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
BASE = ROOT / "hadwiger_nelson_parts509_criticality"
SWAP = ROOT / "hadwiger_nelson_parts509_swap_closure"
PAIR = ROOT / "hadwiger_nelson_parts509_pair_closure"
N = 509
K = 4
FORMAT = "parts509-pair-replacement-classification-v1"


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def squared_distance(parts, p, q):
    dx = parts.f_sub(p[0], q[0])
    dy = parts.f_sub(p[1], q[1])
    return parts.f_add(parts.f_sq(dx), parts.f_sq(dy))


def load_exact_data():
    parts = load_module("pair_replacement_parts509", BASE / "parts509.py")
    sys.path.insert(0, str(SWAP))
    kfield = load_module("pair_replacement_kfield", SWAP / "kfield.py")
    points, base_edges = parts.load_graph(BASE / "parts509.vtx")
    completion = json.loads((SWAP / "completion_points.json").read_text())
    qpoints = [
        (kfield.from_strings(row["x"]), kfield.from_strings(row["y"]))
        for row in completion["points"]
    ]
    pair_cert = json.loads((PAIR / "pair_certificate.json").read_text())
    candidates = pair_cert["pairs_with_U_eq2"]
    if len(candidates) != 63:
        raise ValueError(f"expected 63 candidates, found {len(candidates)}")
    if len({tuple(row["A"]) for row in candidates}) != len(candidates):
        raise ValueError("duplicate candidate pairs")
    return parts, points, sorted(base_edges), completion, qpoints, pair_cert, candidates


def reconstruct_candidates():
    parts, points, base_edges, completion, qpoints, pair_cert, candidates = load_exact_data()
    used_q = sorted({q for row in candidates for q in row["A"]})
    exact_neighbors = {}
    for q in used_q:
        qp = qpoints[q]
        if qp in points:
            raise ValueError(f"completion point q={q} duplicates a base point")
        nb = tuple(v for v, p in enumerate(points) if squared_distance(parts, qp, p) == parts.ONE)
        listed = tuple(completion["points"][q]["neighbors"])
        if nb != listed:
            raise ValueError(f"exact neighbourhood mismatch for q={q}")
        exact_neighbors[q] = nb

    graphs = []
    for index, row in enumerate(candidates):
        q1, q2 = row["A"]
        u, v = row["U"]
        if qpoints[q1] == qpoints[q2] or u == v:
            raise ValueError(f"degenerate candidate {index}")
        retained = [w for w in range(N) if w not in (u, v)]
        old_to_new = {w: i for i, w in enumerate(retained)}
        edges = [
            (old_to_new[a], old_to_new[b])
            for a, b in base_edges
            if a in old_to_new and b in old_to_new
        ]
        for offset, q in enumerate((q1, q2)):
            x = len(retained) + offset
            edges.extend((old_to_new[w], x) for w in exact_neighbors[q] if w in old_to_new)
        qq_edge = squared_distance(parts, qpoints[q1], qpoints[q2]) == parts.ONE
        if qq_edge:
            edges.append((len(retained), len(retained) + 1))
        edges = sorted((min(a, b), max(a, b)) for a, b in edges)
        if len(set(edges)) != len(edges):
            raise ValueError(f"duplicate edge in candidate {index}")
        graphs.append(
            {
                "index": index,
                "A": [q1, q2],
                "U": [u, v],
                "retained": retained,
                "edges": edges,
                "qq_edge": qq_edge,
            }
        )
    return graphs, pair_cert, base_edges, exact_neighbors


def triangle(edges):
    adj = [set() for _ in range(N)]
    for a, b in edges:
        adj[a].add(b)
        adj[b].add(a)
    for a, b in edges:
        common = adj[a] & adj[b]
        if common:
            return a, b, min(common)
    raise ValueError("candidate has no triangle")


def color_var(v: int, c: int) -> int:
    return K * v + c + 1


def clauses_for(edges):
    clauses = []
    for v in range(N):
        clauses.append([color_var(v, c) for c in range(K)])
        for c, d in itertools.combinations(range(K), 2):
            clauses.append([-color_var(v, c), -color_var(v, d)])
    for a, b in edges:
        for c in range(K):
            clauses.append([-color_var(a, c), -color_var(b, c)])
    for c, v in enumerate(triangle(edges)):
        clauses.append([color_var(v, c)])
    return clauses


def dimacs_bytes(edges):
    clauses = clauses_for(edges)
    lines = [f"p cnf {N * K} {len(clauses)}\n"]
    lines.extend(" ".join(map(str, clause)) + " 0\n" for clause in clauses)
    return "".join(lines).encode("ascii")


def validate_coloring(edges, coloring):
    if len(coloring) != N or any(c not in range(K) for c in coloring):
        raise ValueError("invalid colouring alphabet or length")
    for a, b in edges:
        if coloring[a] == coloring[b]:
            raise ValueError(f"monochromatic edge {(a, b)}")


def command_search(out_path: Path, solver_name: str):
    from pysat.solvers import Solver

    graphs, pair_cert, base_edges, exact_neighbors = reconstruct_candidates()
    records = []
    for graph in graphs:
        clauses = clauses_for(graph["edges"])
        with Solver(name=solver_name, bootstrap_with=clauses) as solver:
            sat = solver.solve()
            model = solver.get_model() if sat else None
        record = {
            "index": graph["index"],
            "A": graph["A"],
            "U": graph["U"],
            "edges": len(graph["edges"]),
            "qq_edge": graph["qq_edge"],
            "cnf_sha256": sha256_bytes(dimacs_bytes(graph["edges"])),
        }
        if sat:
            positive = {lit for lit in model if lit > 0}
            coloring = [next(c for c in range(K) if color_var(v, c) in positive) for v in range(N)]
            validate_coloring(graph["edges"], coloring)
            record["status"] = "4-colorable"
            record["coloring"] = "".join(map(str, coloring))
        else:
            record["status"] = "solver-reported-not-4-colorable"
        records.append(record)
        print(
            f"{graph['index']:02d} A={graph['A']} U={graph['U']} "
            f"edges={record['edges']} status={record['status']}",
            flush=True,
        )
    cert = {
        "format": FORMAT,
        "base_coordinate_sha256": sha256_file(BASE / "parts509.vtx"),
        "completion_points_sha256": sha256_file(SWAP / "completion_points.json"),
        "pair_certificate_sha256": sha256_file(PAIR / "pair_certificate.json"),
        "base_edge_sha256": load_module("pair_replacement_parts509_hash", BASE / "parts509.py").edge_sha256(base_edges),
        "candidate_count": len(records),
        "used_completion_points": len(exact_neighbors),
        "solver": solver_name,
        "records": records,
    }
    out_path.write_text(json.dumps(cert, sort_keys=True, separators=(",", ":")) + "\n")
    print(
        json.dumps(
            {
                "candidate_count": len(records),
                "colorable": sum(r["status"] == "4-colorable" for r in records),
                "solver_reported_unsat": sum(r["status"] != "4-colorable" for r in records),
                "certificate_sha256": sha256_file(out_path),
            },
            sort_keys=True,
        )
    )


def command_verify(cert_path: Path, cnf_dir: Path | None):
    graphs, pair_cert, base_edges, exact_neighbors = reconstruct_candidates()
    cert = json.loads(cert_path.read_text())
    if cert.get("format") != FORMAT:
        raise ValueError("unexpected certificate format")
    expected_hashes = {
        "base_coordinate_sha256": sha256_file(BASE / "parts509.vtx"),
        "completion_points_sha256": sha256_file(SWAP / "completion_points.json"),
        "pair_certificate_sha256": sha256_file(PAIR / "pair_certificate.json"),
    }
    for key, expected in expected_hashes.items():
        if cert.get(key) != expected:
            raise ValueError(f"{key} mismatch")
    if cert.get("candidate_count") != 63 or len(cert.get("records", [])) != 63:
        raise ValueError("candidate count mismatch")
    colorable = unsat = edge_checks = 0
    for graph, record in zip(graphs, cert["records"]):
        for key in ("index", "A", "U", "qq_edge"):
            if record.get(key) != graph[key]:
                raise ValueError(f"record {graph['index']} {key} mismatch")
        if record.get("edges") != len(graph["edges"]):
            raise ValueError(f"record {graph['index']} edge count mismatch")
        cnf = dimacs_bytes(graph["edges"])
        if record.get("cnf_sha256") != sha256_bytes(cnf):
            raise ValueError(f"record {graph['index']} CNF hash mismatch")
        if cnf_dir is not None:
            cnf_dir.mkdir(parents=True, exist_ok=True)
            (cnf_dir / f"candidate_{graph['index']:02d}.cnf").write_bytes(cnf)
        if record["status"] == "4-colorable":
            coloring = [int(ch) for ch in record["coloring"]]
            validate_coloring(graph["edges"], coloring)
            colorable += 1
            edge_checks += len(graph["edges"])
        elif record["status"] in ("solver-reported-not-4-colorable", "certified-not-4-colorable"):
            if record["status"] == "certified-not-4-colorable":
                for key in (
                    "drat_proof_sha256",
                    "drat_proof_bytes",
                    "drat_core_lemmas",
                    "drat_total_lemmas",
                    "drat_resolution_steps",
                ):
                    if not isinstance(record.get(key), (str if key.endswith("sha256") else int)):
                        raise ValueError(f"record {graph['index']} missing {key}")
            unsat += 1
        else:
            raise ValueError(f"record {graph['index']} unknown status")
    print(f"all_checks=true candidates=63 colorable={colorable} solver_reported_unsat={unsat}")
    print(
        f"used_completion_points={len(exact_neighbors)} coloring_edge_checks={edge_checks} "
        f"certificate_sha256={sha256_file(cert_path)}"
    )


def command_attach_proofs(source: Path, proof_dir: Path, log_dir: Path, output: Path):
    cert = json.loads(source.read_text())
    if cert.get("format") != FORMAT:
        raise ValueError("unexpected certificate format")
    attached = 0
    total_bytes = total_core = total_resolution = 0
    for record in cert["records"]:
        if record["status"] == "4-colorable":
            continue
        index = record["index"]
        proof = proof_dir / f"candidate_{index:02d}.drat"
        report_path = log_dir / f"candidate_{index:02d}.drat-trim.log"
        report = report_path.read_text(errors="replace")
        if "s VERIFIED" not in report:
            raise ValueError(f"candidate {index}: drat-trim did not report VERIFIED")
        match = re.search(r"(\d+) of (\d+) lemmas in core using (\d+) resolution steps", report)
        if match is None:
            raise ValueError(f"candidate {index}: cannot parse drat-trim statistics")
        core, lemmas, resolutions = map(int, match.groups())
        record["status"] = "certified-not-4-colorable"
        record["drat_proof_sha256"] = sha256_file(proof)
        record["drat_proof_bytes"] = proof.stat().st_size
        record["drat_core_lemmas"] = core
        record["drat_total_lemmas"] = lemmas
        record["drat_resolution_steps"] = resolutions
        attached += 1
        total_bytes += proof.stat().st_size
        total_core += core
        total_resolution += resolutions
    if attached != 60:
        raise ValueError(f"expected 60 proof reports, found {attached}")
    cert["proof_system"] = "DRAT"
    cert["proof_generator"] = "CaDiCaL sc2021"
    cert["proof_checker"] = "drat-trim"
    cert["proof_summary"] = {
        "verified_proofs": attached,
        "total_proof_bytes": total_bytes,
        "total_core_lemmas": total_core,
        "total_resolution_steps": total_resolution,
        "minimum_core_lemmas": min(r["drat_core_lemmas"] for r in cert["records"] if r["status"] == "certified-not-4-colorable"),
        "maximum_core_lemmas": max(r["drat_core_lemmas"] for r in cert["records"] if r["status"] == "certified-not-4-colorable"),
    }
    output.write_text(json.dumps(cert, sort_keys=True, separators=(",", ":")) + "\n")
    print(json.dumps({**cert["proof_summary"], "certificate_sha256": sha256_file(output)}, sort_keys=True))


def main():
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)
    p = sub.add_parser("search")
    p.add_argument("output", type=Path)
    p.add_argument("--solver", default="cadical195")
    p = sub.add_parser("verify")
    p.add_argument("certificate", type=Path)
    p.add_argument("--write-cnfs", type=Path)
    p = sub.add_parser("attach-proofs")
    p.add_argument("source", type=Path)
    p.add_argument("proof_dir", type=Path)
    p.add_argument("log_dir", type=Path)
    p.add_argument("output", type=Path)
    args = parser.parse_args()
    if args.command == "search":
        command_search(args.output, args.solver)
    elif args.command == "verify":
        command_verify(args.certificate, args.write_cnfs)
    else:
        command_attach_proofs(args.source, args.proof_dir, args.log_dir, args.output)


if __name__ == "__main__":
    main()
