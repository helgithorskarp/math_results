#!/usr/bin/env python3
"""Generate and verify compact criticality data for rotation-scan exceptions.

The two alternate isomorphism classes use explicit 4-colourings of every
one-vertex deletion.  Their non-4-colourability is certified separately by
regenerable DRAT proofs; this module writes the canonical CNFs under a caller-
chosen /scratch path and records proof hashes after external checking.
"""

from __future__ import annotations

import argparse
import base64
import hashlib
import json
import subprocess
import sys
from functools import lru_cache
from pathlib import Path
from typing import Iterable, Sequence

from pysat.solvers import Solver


HERE = Path(__file__).resolve().parent
CRITICALITY = HERE.parent / "hadwiger_nelson_parts509_criticality"
ASYMMETRY = HERE.parent / "hadwiger_nelson_parts509_asymmetry"
sys.path[:0] = [str(CRITICALITY), str(ASYMMETRY)]

from parts509 import build_edges, parse_points, triangle_avoiding  # noqa: E402
from refinement_certificate import (  # noqa: E402
    canonical_hash,
    make_adjacency,
    refine,
)


FORMAT = "parts509-rotation-criticality-v1"
N = 509
L_SIZE = 374
ALTERNATE_REPRESENTATIVES = (108, 109)
ALL_REPRESENTATIVES = (108, 109, 690)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for block in iter(lambda: source.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def unpack_coloring(packed: str, n: int = N) -> list[int]:
    raw = base64.b64decode(packed, validate=True)
    if len(raw) != (n + 3) // 4:
        raise ValueError("packed colouring has the wrong length")
    colors = [(raw[i // 4] >> (2 * (i % 4))) & 3 for i in range(n)]
    if n % 4 and raw[-1] >> (2 * (n % 4)):
        raise ValueError("nonzero padding bits")
    return colors


def pack_coloring(colors: Sequence[int]) -> str:
    data = bytearray((len(colors) + 3) // 4)
    for i, color in enumerate(colors):
        data[i // 4] |= color << (2 * (i % 4))
    return base64.b64encode(data).decode("ascii")


def pack_five_coloring(colors: Sequence[int]) -> str:
    if len(colors) != N or any(not (0 <= color < 5) for color in colors):
        raise ValueError("invalid five-colouring")
    return base64.b64encode(bytes(colors)).decode("ascii")


def unpack_five_coloring(packed: str) -> list[int]:
    colors = list(base64.b64decode(packed, validate=True))
    if len(colors) != N or any(not (0 <= color < 5) for color in colors):
        raise ValueError("invalid five-colouring data")
    return colors


@lru_cache(maxsize=None)
def strict_edges(points_path: Path) -> tuple[tuple[int, int], ...]:
    return tuple(build_edges(parse_points(points_path)))


def graph_edges(points_path: Path, scan: dict, event_index: int) -> list[tuple[int, int]]:
    strict = strict_edges(points_path)
    edges = [(u, v) for u, v in strict if v < L_SIZE or u >= L_SIZE]
    edges += [tuple(map(int, edge)) for edge in scan["invariant_cross_edges"]]
    edges += [
        tuple(map(int, edge))
        for edge in scan["events"][event_index]["event_cross_edges"]
    ]
    if len(edges) != len(set(edges)):
        raise ValueError("duplicate edge in reconstructed graph")
    return sorted(edges)


def activated_clauses(edges: Iterable[tuple[int, int]]) -> list[list[int]]:
    clauses = [
        [-(4 * N + vertex + 1)] + [4 * vertex + color + 1 for color in range(4)]
        for vertex in range(N)
    ]
    clauses.extend(
        [-4 * u - color - 1, -4 * v - color - 1]
        for u, v in edges
        for color in range(4)
    )
    return clauses


def ordinary_clauses(edges: Iterable[tuple[int, int]], colors: int) -> list[list[int]]:
    clauses = [
        [colors * vertex + color + 1 for color in range(colors)]
        for vertex in range(N)
    ]
    clauses.extend(
        [-colors * u - color - 1, -colors * v - color - 1]
        for u, v in edges
        for color in range(colors)
    )
    return clauses


def model_coloring(
    model: Sequence[int], colors: int, allow_uncolored: int | None = None
) -> list[int]:
    positive = {literal for literal in model if literal > 0}
    result = []
    for vertex in range(N):
        available = [
            color
            for color in range(colors)
            if colors * vertex + color + 1 in positive
        ]
        if not available:
            if vertex == allow_uncolored:
                result.append(0)
                continue
            raise AssertionError(f"model leaves vertex {vertex} uncoloured")
        result.append(available[0])
    return result


def check_coloring(
    colors: Sequence[int], edges: Iterable[tuple[int, int]], deleted: int | None = None
) -> None:
    if len(colors) != N or any(not (0 <= color < 4) for color in colors):
        raise ValueError("invalid four-colouring data")
    for u, v in edges:
        if u != deleted and v != deleted and colors[u] == colors[v]:
            raise ValueError(f"monochromatic edge {(u, v)} with deletion {deleted}")


def canonical_data(edges: list[tuple[int, int]]) -> tuple[dict, dict[int, int]]:
    adjacency = make_adjacency(set(range(N)), set(edges))
    colors, counts = refine(adjacency)
    return (
        {
            "refinement_cell_counts": counts,
            "canonical_edge_sha256": canonical_hash(adjacency, colors),
        },
        colors,
    )


def canonical_summary(edges: list[tuple[int, int]]) -> dict:
    return canonical_data(edges)[0]


def generate(scan_path: Path, points_path: Path, output_path: Path) -> None:
    scan = json.loads(scan_path.read_text())
    records = []
    for event_index in ALL_REPRESENTATIVES:
        edges = graph_edges(points_path, scan, event_index)
        summary = {
            "event_index": event_index,
            "edges": len(edges),
            **canonical_summary(edges),
        }
        with Solver(name="cadical195", bootstrap_with=ordinary_clauses(edges, 5)) as solver:
            if not solver.solve():
                raise AssertionError("expected a five-colouring")
            summary["five_coloring"] = pack_five_coloring(
                model_coloring(solver.get_model(), 5)
            )

        if event_index in ALTERNATE_REPRESENTATIVES:
            witnesses = []
            clauses = activated_clauses(edges)
            with Solver(name="cadical195", bootstrap_with=clauses) as solver:
                for deleted in range(N):
                    triangle = triangle_avoiding(N, edges, deleted)
                    assumptions = [
                        4 * N + vertex + 1 for vertex in range(N) if vertex != deleted
                    ]
                    assumptions += [4 * triangle[color] + color + 1 for color in range(3)]
                    if not solver.solve(assumptions=assumptions):
                        raise AssertionError(
                            f"event {event_index}, deletion {deleted} is not 4-colourable"
                        )
                    coloring = model_coloring(
                        solver.get_model(), 4, allow_uncolored=deleted
                    )
                    check_coloring(coloring, edges, deleted)
                    witnesses.append(pack_coloring(coloring))
                    if (deleted + 1) % 100 == 0:
                        print(f"event {event_index}: {deleted + 1}/{N} deletions")
            summary["deletion_four_colorings"] = witnesses
        else:
            summary["criticality_dependency"] = (
                "hadwiger_nelson_parts509_criticality/certificate.json"
            )
        records.append(summary)

    # Group all six SAT-negative rotations by a discrete-refinement canonical hash.
    classes: dict[str, list[tuple[int, list[tuple[int, int]], dict[int, int]]]] = {}
    for event_index in scan["counts"]["uncolorable_event_indices"]:
        edges = graph_edges(points_path, scan, event_index)
        graph_summary, colors = canonical_data(edges)
        graph_hash = graph_summary["canonical_edge_sha256"]
        classes.setdefault(graph_hash, []).append((event_index, edges, colors))

    isomorphism_classes = []
    for graph_hash, members in sorted(classes.items(), key=lambda item: min(x[0] for x in item[1])):
        members.sort(key=lambda item: item[0])
        representative_index, representative_edges, representative_colors = members[0]
        inverse_representative = {color: vertex for vertex, color in representative_colors.items()}
        isomorphisms = {}
        for event_index, edges, colors in members[1:]:
            mapping = [inverse_representative[colors[vertex]] for vertex in range(N)]
            mapped_edges = {
                (min(mapping[u], mapping[v]), max(mapping[u], mapping[v])) for u, v in edges
            }
            if mapped_edges != set(representative_edges):
                raise AssertionError("equal canonical hashes did not give an exact isomorphism")
            isomorphisms[str(event_index)] = mapping
        isomorphism_classes.append(
            {
                "canonical_edge_sha256": graph_hash,
                "representative_event_index": representative_index,
                "event_indices": [member[0] for member in members],
                "isomorphisms_to_representative": isomorphisms,
            }
        )

    document = {
        "format": FORMAT,
        "scan_sha256": sha256(scan_path),
        "isomorphism_classes": isomorphism_classes,
        "representatives": records,
        "drat": {},
    }
    output_path.write_text(json.dumps(document, separators=(",", ":")) + "\n")
    print(f"wrote {output_path}")


def verify(scan_path: Path, points_path: Path, certificate_path: Path) -> None:
    scan = json.loads(scan_path.read_text())
    certificate = json.loads(certificate_path.read_text())
    if certificate.get("format") != FORMAT or certificate.get("scan_sha256") != sha256(scan_path):
        raise ValueError("format or scan hash mismatch")
    for record in certificate["representatives"]:
        event_index = int(record["event_index"])
        edges = graph_edges(points_path, scan, event_index)
        expected = canonical_summary(edges)
        if record["edges"] != len(edges) or any(record[key] != value for key, value in expected.items()):
            raise ValueError(f"graph summary mismatch for event {event_index}")
        five = unpack_five_coloring(record["five_coloring"])
        if any(five[u] == five[v] for u, v in edges):
            raise ValueError(f"bad five-colouring for event {event_index}")
        if event_index in ALTERNATE_REPRESENTATIVES:
            witnesses = record.get("deletion_four_colorings", [])
            if len(witnesses) != N:
                raise ValueError("wrong deletion witness count")
            for deleted, packed in enumerate(witnesses):
                check_coloring(unpack_coloring(packed), edges, deleted)
    print("criticality_witnesses_verified=true")


def write_dimacs(scan_path: Path, points_path: Path, event_index: int, output: Path) -> None:
    if not str(output.resolve()).startswith("/scratch/"):
        raise ValueError("solver inputs must be written under /scratch")
    scan = json.loads(scan_path.read_text())
    edges = graph_edges(points_path, scan, event_index)
    clauses = ordinary_clauses(edges, 4)
    # Sound symmetry breaking on a surviving triangle.
    triangle = triangle_avoiding(N, edges, -1)
    clauses += [[4 * triangle[color] + color + 1] for color in range(3)]
    with output.open("w") as target:
        target.write(f"p cnf {4 * N} {len(clauses)}\n")
        for clause in clauses:
            target.write(" ".join(map(str, clause)) + " 0\n")
    print(f"cnf={output} sha256={sha256(output)} clauses={len(clauses)} triangle={triangle}")


def bind_proofs(
    certificate_path: Path,
    checker: Path,
    files: Sequence[tuple[int, Path, Path]],
) -> None:
    document = json.loads(certificate_path.read_text())
    if document.get("format") != FORMAT:
        raise ValueError("criticality certificate format mismatch")
    try:
        checker_commit = subprocess.run(
            ["git", "-C", str(checker.parent), "rev-parse", "HEAD"],
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip()
    except subprocess.CalledProcessError:
        checker_commit = "not-a-git-checkout"
    records = {}
    for event_index, cnf, proof in files:
        for path in (cnf, proof):
            if not str(path.resolve()).startswith("/scratch/"):
                raise ValueError("CNF and proof files must remain under /scratch")
        completed = subprocess.run(
            [str(checker), str(cnf), str(proof)],
            capture_output=True,
            text=True,
        )
        transcript = (completed.stdout + completed.stderr).replace("\r", "\n")
        if completed.returncode != 0 or "s VERIFIED" not in transcript:
            raise RuntimeError(f"proof check failed for event {event_index}:\n{transcript}")
        summary = [
            line.strip()
            for line in transcript.splitlines()
            if any(
                marker in line
                for marker in (
                    "clauses in core",
                    "lemmas in core",
                    "RAT lemmas in core",
                    "s VERIFIED",
                )
            )
        ]
        records[str(event_index)] = {
            "cnf_sha256": sha256(cnf),
            "cnf_bytes": cnf.stat().st_size,
            "proof_sha256": sha256(proof),
            "proof_bytes": proof.stat().st_size,
            "checker_summary": summary,
        }
    document["drat"] = {
        "checker": "drat-trim",
        "checker_git_commit": checker_commit,
        "proofs": records,
    }
    certificate_path.write_text(json.dumps(document, separators=(",", ":")) + "\n")
    print(f"proofs_bound_and_verified=true checker_commit={checker_commit}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=("generate", "verify", "cnf", "bind"))
    parser.add_argument("scan", type=Path)
    parser.add_argument(
        "--points", type=Path, default=CRITICALITY / "parts509.vtx"
    )
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--event", type=int)
    parser.add_argument("--checker", type=Path)
    parser.add_argument("--cnf108", type=Path)
    parser.add_argument("--proof108", type=Path)
    parser.add_argument("--cnf109", type=Path)
    parser.add_argument("--proof109", type=Path)
    args = parser.parse_args()
    if args.mode == "generate":
        generate(args.scan, args.points, args.output)
    elif args.mode == "verify":
        verify(args.scan, args.points, args.output)
    elif args.mode == "cnf":
        if args.event is None:
            parser.error("cnf mode requires --event")
        write_dimacs(args.scan, args.points, args.event, args.output)
    else:
        required = (args.checker, args.cnf108, args.proof108, args.cnf109, args.proof109)
        if any(path is None for path in required):
            parser.error("bind mode requires --checker and both --cnf/--proof path pairs")
        bind_proofs(
            args.output,
            args.checker,
            ((108, args.cnf108, args.proof108), (109, args.cnf109, args.proof109)),
        )


if __name__ == "__main__":
    main()
