#!/usr/bin/env python3
"""Generate and verify the Parts-509 degree-four obstruction classification.

All solver products are directed to /scratch.  The compact JSON certificate
contains only directly checkable SAT witnesses.  The generated classification
CNF is intended for a separately checked DRAT refutation.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from pathlib import Path
import subprocess


N = 509
K = 4
DEGREE_FOUR = (310, 313, 316, 319, 322, 325)
ALLOWED_MASKS = (1, 2, 4, 8, 9, 16, 18, 32, 36)
PINNED_TRIANGLE = (0, 149, 152)
FORMAT = "parts509-degree4-obstruction-classification-v1"
EXPECTED_EDGE_SHA256 = "5a95127767cb370f25f5865f057cab9b4a7ee9a72e2f73ad126ae390d71d487c"


def color_var(vertex: int, color: int) -> int:
    return K * vertex + color + 1


def blocked_var(index: int) -> int:
    return N * K + index + 1


def canonical_edge_bytes(edges: list[tuple[int, int]]) -> bytes:
    return "".join(f"{u} {v}\n" for u, v in edges).encode("ascii")


def load_graph(edge_path: Path) -> tuple[list[tuple[int, int]], list[set[int]]]:
    raw = json.loads(edge_path.read_text(encoding="utf-8"))
    edges = sorted(tuple(sorted(map(int, e))) for e in raw)
    assert len(edges) == len(set(edges)) == 2442
    assert hashlib.sha256(canonical_edge_bytes(edges)).hexdigest() == EXPECTED_EDGE_SHA256
    adj = [set() for _ in range(N)]
    for u, v in edges:
        assert 0 <= u < v < N
        adj[u].add(v)
        adj[v].add(u)
    assert tuple(v for v in range(N) if len(adj[v]) == 4) == DEGREE_FOUR
    assert all(not (adj[v] & set(DEGREE_FOUR)) for v in DEGREE_FOUR)
    return edges, adj


def base_clauses(edges: list[tuple[int, int]], adj: list[set[int]]) -> list[list[int]]:
    removed = set(DEGREE_FOUR)
    core = [v for v in range(N) if v not in removed]
    clauses: list[list[int]] = []
    for v in core:
        clauses.append([color_var(v, c) for c in range(K)])
        for c, d in itertools.combinations(range(K), 2):
            clauses.append([-color_var(v, c), -color_var(v, d)])
    for u, v in edges:
        if u in removed or v in removed:
            continue
        for c in range(K):
            clauses.append([-color_var(u, c), -color_var(v, c)])
    assert all(y in adj[x] for x, y in itertools.combinations(PINNED_TRIANGLE, 2))
    for c, v in enumerate(PINNED_TRIANGLE):
        clauses.append([color_var(v, c)])
    # Truth-table reification.  Since each core vertex has exactly one color,
    # exactly one assignment row is active for each deleted vertex.
    for i, deleted in enumerate(DEGREE_FOUR):
        neighbors = sorted(adj[deleted])
        assert len(neighbors) == K
        b = blocked_var(i)
        for assignment in itertools.product(range(K), repeat=K):
            prefix = [-color_var(neighbors[j], assignment[j]) for j in range(K)]
            is_blocked = len(set(assignment)) == K
            clauses.append(prefix + ([b] if is_blocked else [-b]))
    return clauses


def exact_mask_clauses(mask: int) -> list[list[int]]:
    return [
        [blocked_var(i) if mask & (1 << i) else -blocked_var(i)]
        for i in range(len(DEGREE_FOUR))
    ]


def exclude_mask_clause(mask: int) -> list[int]:
    return [
        -blocked_var(i) if mask & (1 << i) else blocked_var(i)
        for i in range(len(DEGREE_FOUR))
    ]


def write_dimacs(path: Path, clauses: list[list[int]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="ascii") as handle:
        handle.write(f"p cnf {N * K + len(DEGREE_FOUR)} {len(clauses)}\n")
        for clause in clauses:
            handle.write(" ".join(map(str, clause)) + " 0\n")


def parse_solution(path: Path, core: list[int]) -> tuple[list[int], int]:
    positive: set[int] = set()
    status = None
    for line in path.read_text(encoding="ascii").splitlines():
        if line.startswith("s "):
            status = line
        elif line.startswith("v "):
            positive.update(x for x in map(int, line[2:].split()) if x > 0)
    assert status == "s SATISFIABLE", status
    colors = [-1] * N
    for v in core:
        selected = [c for c in range(K) if color_var(v, c) in positive]
        assert len(selected) == 1
        colors[v] = selected[0]
    mask = sum(
        (1 << i) for i in range(len(DEGREE_FOUR)) if blocked_var(i) in positive
    )
    return colors, mask


def encode_coloring(colors: list[int], core: list[int]) -> str:
    assert all(0 <= colors[v] < K for v in core)
    return "".join(str(colors[v]) for v in core)


def decode_coloring(text: str, core: list[int]) -> list[int]:
    assert len(text) == len(core)
    colors = [-1] * N
    for v, symbol in zip(core, text, strict=True):
        assert symbol in "0123"
        colors[v] = int(symbol)
    return colors


def actual_mask(colors: list[int], adj: list[set[int]]) -> int:
    return sum(
        (1 << i)
        for i, v in enumerate(DEGREE_FOUR)
        if len({colors[x] for x in adj[v]}) == K
    )


def verify_coloring(
    colors: list[int], edges: list[tuple[int, int]], adj: list[set[int]], mask: int
) -> None:
    removed = set(DEGREE_FOUR)
    for u, v in edges:
        if u not in removed and v not in removed:
            assert colors[u] != colors[v], (u, v)
    assert actual_mask(colors, adj) == mask


def generate(args: argparse.Namespace) -> None:
    edges, adj = load_graph(args.edges)
    base = base_clauses(edges, adj)
    core = [v for v in range(N) if v not in set(DEGREE_FOUR)]
    scratch = args.scratch
    scratch.mkdir(parents=True, exist_ok=True)
    witnesses: dict[str, str] = {}
    for mask in ALLOWED_MASKS:
        cnf = scratch / f"witness_{mask}.cnf"
        sol = scratch / f"witness_{mask}.sol"
        write_dimacs(cnf, base + exact_mask_clauses(mask))
        run = subprocess.run(
            [str(args.cadical), "-q", "-w", str(sol), str(cnf)],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            check=False,
        )
        assert run.returncode == 10, (mask, run.returncode, run.stdout)
        colors, solver_mask = parse_solution(sol, core)
        assert solver_mask == mask
        verify_coloring(colors, edges, adj, mask)
        witnesses[str(mask)] = encode_coloring(colors, core)

    classification_clauses = base + [exclude_mask_clause(m) for m in ALLOWED_MASKS]
    write_dimacs(args.cnf, classification_clauses)
    neighborhood_edges = {
        str(v): [
            [x, y]
            for x, y in itertools.combinations(sorted(adj[v]), 2)
            if y in adj[x]
        ]
        for v in DEGREE_FOUR
    }
    certificate = {
        "format": FORMAT,
        "claim": (
            "The blocked subsets across all proper 4-colorings of the Parts-509 "
            "core obtained by deleting its six degree-4 vertices are exactly "
            "the six singletons and three antipodal pairs."
        ),
        "vertices": N,
        "edges": len(edges),
        "edge_sha256": EXPECTED_EDGE_SHA256,
        "core_vertices": len(core),
        "core_edges": sum(u not in DEGREE_FOUR and v not in DEGREE_FOUR for u, v in edges),
        "degree_four_vertices": list(DEGREE_FOUR),
        "neighborhoods": {str(v): sorted(adj[v]) for v in DEGREE_FOUR},
        "neighborhood_induced_edges": neighborhood_edges,
        "allowed_masks": list(ALLOWED_MASKS),
        "allowed_blocked_sets": {
            str(mask): [DEGREE_FOUR[i] for i in range(6) if mask & (1 << i)]
            for mask in ALLOWED_MASKS
        },
        "core_colorings": witnesses,
        "pinned_triangle": list(PINNED_TRIANGLE),
        "cnf_variables": N * K + len(DEGREE_FOUR),
        "cnf_clauses": len(classification_clauses),
        "cnf_sha256": hashlib.sha256(args.cnf.read_bytes()).hexdigest(),
        "solver": subprocess.run(
            [str(args.cadical), "--version"], capture_output=True, text=True, check=True
        ).stdout.strip(),
    }
    args.certificate.write_text(
        json.dumps(certificate, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    verify_certificate(args.edges, args.certificate)
    print(f"allowed_masks={','.join(map(str, ALLOWED_MASKS))}")
    print(f"sat_witnesses={len(witnesses)}")
    print(f"classification_cnf_variables={certificate['cnf_variables']}")
    print(f"classification_cnf_clauses={certificate['cnf_clauses']}")
    print(f"classification_cnf_sha256={certificate['cnf_sha256']}")


def verify_certificate(edge_path: Path, certificate_path: Path) -> None:
    edges, adj = load_graph(edge_path)
    cert = json.loads(certificate_path.read_text(encoding="utf-8"))
    assert cert["format"] == FORMAT
    assert cert["edge_sha256"] == EXPECTED_EDGE_SHA256
    assert tuple(cert["degree_four_vertices"]) == DEGREE_FOUR
    assert tuple(cert["allowed_masks"]) == ALLOWED_MASKS
    core = [v for v in range(N) if v not in set(DEGREE_FOUR)]
    for key, text in cert["core_colorings"].items():
        mask = int(key)
        assert mask in ALLOWED_MASKS
        colors = decode_coloring(text, core)
        verify_coloring(colors, edges, adj, mask)
    assert set(map(int, cert["core_colorings"])) == set(ALLOWED_MASKS)
    print("edge_manifest_verified=true")
    print("degree_four_vertices_verified=6")
    print("core_coloring_witnesses_verified=9")
    print("allowed_blocked_signatures=6_singletons_plus_3_antipodal_pairs")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--edges",
        type=Path,
        default=Path(
            "../hadwiger_nelson_parts509_degree10_replacements/edges.json"
        ),
    )
    sub = parser.add_subparsers(dest="command", required=True)
    gen = sub.add_parser("generate")
    gen.add_argument("--cadical", type=Path, required=True)
    gen.add_argument("--scratch", type=Path, required=True)
    gen.add_argument("--certificate", type=Path, default=Path("certificate.json"))
    gen.add_argument("--cnf", type=Path, default=Path("classification.cnf"))
    verify = sub.add_parser("verify")
    verify.add_argument("certificate", type=Path, nargs="?", default=Path("certificate.json"))
    args = parser.parse_args()
    if args.command == "generate":
        generate(args)
    else:
        verify_certificate(args.edges, args.certificate)


if __name__ == "__main__":
    main()
