#!/usr/bin/env python3
"""Generate and check edge-deletion colorings for the Parts-509 reduced graph.

The certificate contains one explicit four-coloring of H-e for every edge e.
Generation uses an incremental SAT solver.  Verification is solver-free: it
decodes each coloring and checks every retained edge directly.

Generated certificates, progress files, and solver output should first be
written under /scratch.  Only the compact final certificate belongs in git.
"""

from __future__ import annotations

import argparse
import base64
import hashlib
import json
import time
from pathlib import Path
from typing import Iterable, Sequence


FORMAT = "parts509-reduced-edge-criticality-v1"
N_VERTICES = 509
N_COLORS = 4
SYMMETRY_CONFLICT_BUDGET = 20_000
SEED_CONFLICT_BUDGET = 5_000
CORE_GUIDED_ROUNDS = 16
ROW_BYTES = (2 * N_VERTICES + 7) // 8
PACKING = (
    "one fixed-width 128-byte row per edge in edge-list order; within each row, "
    "four 2-bit colors per byte, low bits first, vertices in increasing order; "
    "the six unused high bits of the last byte are zero"
)
TRIANGLE_PATTERNS = (
    (0, 1, 2),
    (1, 0, 2),
    (1, 2, 0),
    (1, 2, 3),
)

Edge = tuple[int, int]


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for block in iter(lambda: source.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def edge_sha256(edges: Iterable[Edge]) -> str:
    digest = hashlib.sha256()
    for u, v in edges:
        digest.update(f"{u} {v}\n".encode())
    return digest.hexdigest()


def load_edges(path: Path) -> list[Edge]:
    document = json.loads(path.read_text())
    edges = [tuple(map(int, edge)) for edge in document["edges"]]
    if len(edges) != 2259:
        raise ValueError(f"expected 2259 edges, got {len(edges)}")
    if any(not (0 <= u < v < N_VERTICES) for u, v in edges):
        raise ValueError("edge list contains a malformed edge")
    if len(set(edges)) != len(edges):
        raise ValueError("edge list contains duplicates")
    if edges != sorted(edges):
        raise ValueError("edge list is not in canonical lexicographic order")
    used = {vertex for edge in edges for vertex in edge}
    if used != set(range(N_VERTICES)):
        missing = sorted(set(range(N_VERTICES)) - used)
        raise ValueError(f"edge list has isolated vertices: {missing}")
    return edges


def color_var(vertex: int, color: int) -> int:
    return N_COLORS * vertex + color + 1


def selector_var(edge_index: int) -> int:
    return N_COLORS * N_VERTICES + edge_index + 1


def pack_row(colors: Sequence[int]) -> bytes:
    if len(colors) != N_VERTICES or any(color not in range(N_COLORS) for color in colors):
        raise ValueError("invalid coloring row")
    packed = bytearray(ROW_BYTES)
    for vertex, color in enumerate(colors):
        packed[vertex // 4] |= color << (2 * (vertex % 4))
    return bytes(packed)


def unpack_row(packed: bytes) -> list[int]:
    if len(packed) != ROW_BYTES:
        raise ValueError("invalid packed row length")
    if packed[-1] & 0b11111100:
        raise ValueError("nonzero padding bits in packed row")
    return [
        (packed[vertex // 4] >> (2 * (vertex % 4))) & 3
        for vertex in range(N_VERTICES)
    ]


def load_vertex_deletion_seeds(path: Path | None) -> list[list[int]] | None:
    if path is None:
        return None
    certificate = json.loads(path.read_text())
    payload = base64.b64decode(certificate["deletion_colorings_base64"], validate=True)
    if hashlib.sha256(payload).hexdigest() != certificate.get(
        "packed_deletion_colorings_sha256"
    ):
        raise ValueError("vertex-deletion seed payload hash mismatch")
    row_bytes = (N_VERTICES - 1) // 4
    if len(payload) != N_VERTICES * row_bytes:
        raise ValueError("vertex-deletion seed payload length mismatch")
    rows = []
    for deleted in range(N_VERTICES):
        block = payload[deleted * row_bytes : (deleted + 1) * row_bytes]
        retained = [
            (byte >> shift) & 3
            for byte in block
            for shift in (0, 2, 4, 6)
        ]
        iterator = iter(retained)
        rows.append(
            [
                -1 if vertex == deleted else next(iterator)
                for vertex in range(N_VERTICES)
            ]
        )
    return rows


def normalized_seed_colors(seed: Sequence[int], deleted: int, other: int) -> list[int]:
    common = seed[other]
    permutation = list(range(N_COLORS))
    permutation[0], permutation[common] = permutation[common], permutation[0]
    return [
        0 if vertex == deleted else permutation[seed[vertex]]
        for vertex in range(N_VERTICES)
    ]


def seed_phases(seed: Sequence[int], deleted: int, other: int) -> list[int]:
    colors = normalized_seed_colors(seed, deleted, other)
    return [
        color_var(vertex, color) if colors[vertex] == color else -color_var(vertex, color)
        for vertex in range(N_VERTICES)
        for color in range(N_COLORS)
    ]


def validate_edge_deletion_coloring(
    edges: Sequence[Edge], deleted_index: int, colors: Sequence[int]
) -> None:
    if len(colors) != N_VERTICES or any(color not in range(N_COLORS) for color in colors):
        raise ValueError(f"edge {deleted_index}: malformed coloring")
    deleted = edges[deleted_index]
    if colors[deleted[0]] != colors[deleted[1]]:
        raise ValueError(f"edge {deleted_index}: deleted endpoints do not share a color")
    if set(colors) != set(range(N_COLORS)):
        raise ValueError(f"edge {deleted_index}: coloring does not use all four colors")
    for edge_index, (u, v) in enumerate(edges):
        if edge_index != deleted_index and colors[u] == colors[v]:
            raise ValueError(
                f"edge {deleted_index}: retained edge {edge_index}={(u, v)} is monochromatic"
            )


def extract_colors(model: Sequence[int]) -> list[int]:
    positive = {literal for literal in model if literal > 0}
    colors = []
    for vertex in range(N_VERTICES):
        selected = [
            color
            for color in range(N_COLORS)
            if color_var(vertex, color) in positive
        ]
        if not selected:
            raise RuntimeError(f"solver model assigns no color to vertex {vertex}")
        # At-most-one clauses are unnecessary.  Edge exclusions make the sets
        # of selected colors at adjacent vertices disjoint, so choosing the
        # least selected color at every vertex is a proper ordinary coloring.
        colors.append(min(selected))
    return colors


def build_solver(edges: Sequence[Edge], solver_name: str):
    from pysat.solvers import Solver

    solver = Solver(name=solver_name)
    for vertex in range(N_VERTICES):
        variables = [color_var(vertex, color) for color in range(N_COLORS)]
        solver.add_clause(variables)
    for edge_index, (u, v) in enumerate(edges):
        selector = selector_var(edge_index)
        for color in range(N_COLORS):
            solver.add_clause(
                [selector, -color_var(u, color), -color_var(v, color)]
            )
    return solver


def find_triangles(edges: Sequence[Edge]) -> list[tuple[int, int, int]]:
    neighbors = [set() for _ in range(N_VERTICES)]
    for u, v in edges:
        neighbors[u].add(v)
        neighbors[v].add(u)
    triangles = []
    for u, v in edges:
        for w in sorted(neighbors[u] & neighbors[v]):
            if v < w:
                triangles.append((u, v, w))
    if not triangles:
        raise ValueError("graph contains no triangle for color symmetry breaking")
    return triangles


def symmetry_pin_cases(
    edges: Sequence[Edge],
    edge_index: int,
    triangles: Sequence[tuple[int, int, int]],
) -> list[list[int]]:
    """Return complete color-symmetry representatives for one deletion.

    The endpoints of the deleted edge have already been pinned to color zero.
    A surviving triangle either contains color zero at one of its three vertices
    or uses the other three colors.  For speed, choose a triangle having the fewest
    locally compatible patterns under adjacency to the deleted endpoints.
    """

    deleted = edges[edge_index]
    u, v = deleted
    edge_set = set(edges)
    best_cases: list[list[int]] | None = None
    for triangle in triangles:
        triangle_edges = {
            tuple(sorted((triangle[first], triangle[second])))
            for first in range(3)
            for second in range(first + 1, 3)
        }
        if deleted in triangle_edges:
            continue
        cases = []
        for pattern in TRIANGLE_PATTERNS:
            if any(
                vertex in (u, v) and pattern[position] != 0
                for position, vertex in enumerate(triangle)
            ):
                continue
            if any(
                pattern[position] == 0
                and any(
                    tuple(sorted((endpoint, vertex))) in edge_set
                    and tuple(sorted((endpoint, vertex))) != deleted
                    for endpoint in (u, v)
                    if endpoint != vertex
                )
                for position, vertex in enumerate(triangle)
            ):
                continue
            cases.append(
                [
                    color_var(vertex, pattern[position])
                    for position, vertex in enumerate(triangle)
                ]
            )
        if cases and (best_cases is None or len(cases) < len(best_cases)):
            best_cases = cases
            if len(best_cases) == 1:
                break
    if best_cases is None:
        raise RuntimeError("no surviving symmetry triangle has a compatible color case")
    return best_cases


def save_progress(path: Path, edge_hash: str, rows: Sequence[bytes]) -> None:
    payload = b"".join(rows)
    progress = {
        "format": FORMAT + "-partial",
        "edge_sha256": edge_hash,
        "completed_rows": len(rows),
        "packed_sha256": hashlib.sha256(payload).hexdigest(),
        "rows_base64": base64.b64encode(payload).decode("ascii"),
    }
    path.write_text(json.dumps(progress, sort_keys=True) + "\n")


def load_progress(path: Path, edge_hash: str) -> list[bytes]:
    if not path.exists():
        return []
    progress = json.loads(path.read_text())
    if progress.get("format") != FORMAT + "-partial":
        raise ValueError("unknown progress format")
    if progress.get("edge_sha256") != edge_hash:
        raise ValueError("progress edge hash mismatch")
    payload = base64.b64decode(progress["rows_base64"], validate=True)
    if hashlib.sha256(payload).hexdigest() != progress.get("packed_sha256"):
        raise ValueError("progress payload hash mismatch")
    if len(payload) % ROW_BYTES:
        raise ValueError("partial payload has a truncated row")
    rows = [payload[offset : offset + ROW_BYTES] for offset in range(0, len(payload), ROW_BYTES)]
    if len(rows) != progress.get("completed_rows"):
        raise ValueError("progress row-count mismatch")
    return rows


def solve_edge_deletion(
    solver,
    edges: Sequence[Edge],
    edge_index: int,
    triangles: Sequence[tuple[int, int, int]],
    vertex_deletion_seeds: Sequence[Sequence[int]] | None,
) -> list[int]:
    selector_assumptions = [-selector_var(index) for index in range(len(edges))]
    selector_assumptions[edge_index] = -selector_assumptions[edge_index]
    u, v = edges[edge_index]
    selector_assumptions.extend([color_var(u, 0), color_var(v, 0)])
    if vertex_deletion_seeds is not None:
        for deleted, other in ((u, v), (v, u)):
            candidate = normalized_seed_colors(
                vertex_deletion_seeds[deleted], deleted, other
            )
            try:
                validate_edge_deletion_coloring(edges, edge_index, candidate)
                return candidate
            except ValueError:
                pass
            fixed = {
                color_var(vertex, candidate[vertex])
                for vertex in range(N_VERTICES)
                if vertex not in (u, v)
            }
            for _ in range(CORE_GUIDED_ROUNDS):
                solver.conf_budget(SEED_CONFLICT_BUDGET)
                result = solver.solve_limited(
                    assumptions=selector_assumptions + sorted(fixed)
                )
                if result is True:
                    colors = extract_colors(solver.get_model())
                    validate_edge_deletion_coloring(edges, edge_index, colors)
                    return colors
                if result is None:
                    break
                core = set(solver.get_core() or ())
                relax = fixed & core
                if not relax:
                    break
                fixed -= relax
            solver.set_phases(
                seed_phases(vertex_deletion_seeds[deleted], deleted, other)
            )
            solver.conf_budget(SEED_CONFLICT_BUDGET)
            result = solver.solve_limited(assumptions=selector_assumptions)
            if result is True:
                colors = extract_colors(solver.get_model())
                validate_edge_deletion_coloring(edges, edge_index, colors)
                return colors
    for symmetry_pins in symmetry_pin_cases(edges, edge_index, triangles):
        solver.conf_budget(SYMMETRY_CONFLICT_BUDGET)
        result = solver.solve_limited(
            assumptions=selector_assumptions + symmetry_pins
        )
        if result is True:
            colors = extract_colors(solver.get_model())
            validate_edge_deletion_coloring(edges, edge_index, colors)
            return colors
    # A triangle representative is only a speed heuristic.  The endpoint pins
    # alone are complete for the requested endpoint-equal witness, so fall back
    # to that instance without a conflict budget.
    solver.conf_budget(-1)
    if solver.solve(assumptions=selector_assumptions):
        colors = extract_colors(solver.get_model())
        validate_edge_deletion_coloring(edges, edge_index, colors)
        return colors
    raise RuntimeError(
        f"H-edge[{edge_index}]={edges[edge_index]} is not four-colorable; "
        "the upstream edge-criticality claim fails or the encoding is wrong"
    )


def command_generate(
    edge_path: Path,
    certificate_path: Path,
    progress_path: Path,
    solver_name: str,
    limit: int | None,
    seed_path: Path | None,
) -> None:
    import pysat

    edges = load_edges(edge_path)
    triangles = find_triangles(edges)
    vertex_deletion_seeds = load_vertex_deletion_seeds(seed_path)
    edge_hash = edge_sha256(edges)
    rows = load_progress(progress_path, edge_hash)
    for edge_index, row in enumerate(rows):
        validate_edge_deletion_coloring(edges, edge_index, unpack_row(row))
    stop = len(edges) if limit is None else min(len(edges), len(rows) + limit)
    started = time.monotonic()

    with build_solver(edges, solver_name) as solver:
        for edge_index in range(len(rows), stop):
            try:
                colors = solve_edge_deletion(
                    solver, edges, edge_index, triangles, vertex_deletion_seeds
                )
            except RuntimeError:
                save_progress(progress_path, edge_hash, rows)
                raise
            rows.append(pack_row(colors))
            if len(rows) % 25 == 0 or len(rows) == stop:
                save_progress(progress_path, edge_hash, rows)
                elapsed = time.monotonic() - started
                print(
                    json.dumps(
                        {
                            "completed": len(rows),
                            "elapsed_seconds_this_run": round(elapsed, 3),
                            "total": len(edges),
                        },
                        sort_keys=True,
                    ),
                    flush=True,
                )

    if len(rows) != len(edges):
        print(f"partial generation stopped at {len(rows)} of {len(edges)} rows")
        return

    payload = b"".join(rows)
    certificate = {
        "claim": "For every edge e of H, the graph H-e has an explicit proper four-coloring whose endpoints on e have the same color.",
        "edge_file_sha256": file_sha256(edge_path),
        "edge_row_order": "lexicographic edge order, exactly as stored in the edge file",
        "edge_sha256": edge_hash,
        "edges": len(edges),
        "format": FORMAT,
        "generator": f"PySAT {pysat.__version__}, solver {solver_name}",
        "packed_edge_deletion_colorings_sha256": hashlib.sha256(payload).hexdigest(),
        "packing": PACKING,
        "rows_base64": base64.b64encode(payload).decode("ascii"),
        "vertices": N_VERTICES,
    }
    certificate_path.write_text(json.dumps(certificate, indent=2, sort_keys=True) + "\n")
    print(
        json.dumps(
            {
                "certificate": str(certificate_path),
                "certificate_sha256": file_sha256(certificate_path),
                "edge_deletion_colorings": len(rows),
                "packed_bytes": len(payload),
            },
            indent=2,
            sort_keys=True,
        )
    )


def save_segment(
    path: Path,
    edge_hash: str,
    start_index: int,
    stop_index: int,
    solver_name: str,
    rows: Sequence[bytes],
) -> None:
    payload = b"".join(rows)
    document = {
        "format": FORMAT + "-segment",
        "edge_sha256": edge_hash,
        "start_index": start_index,
        "stop_index": stop_index,
        "completed_rows": len(rows),
        "solver": solver_name,
        "packed_sha256": hashlib.sha256(payload).hexdigest(),
        "rows_base64": base64.b64encode(payload).decode("ascii"),
    }
    path.write_text(json.dumps(document, sort_keys=True) + "\n")


def load_segment(
    path: Path, edge_hash: str, start_index: int, stop_index: int
) -> list[bytes]:
    if not path.exists():
        return []
    document = json.loads(path.read_text())
    if document.get("format") != FORMAT + "-segment":
        raise ValueError(f"{path}: unknown segment format")
    if document.get("edge_sha256") != edge_hash:
        raise ValueError(f"{path}: segment edge hash mismatch")
    if document.get("start_index") != start_index or document.get("stop_index") != stop_index:
        raise ValueError(f"{path}: segment range mismatch")
    payload = base64.b64decode(document["rows_base64"], validate=True)
    if hashlib.sha256(payload).hexdigest() != document.get("packed_sha256"):
        raise ValueError(f"{path}: segment payload hash mismatch")
    if len(payload) % ROW_BYTES:
        raise ValueError(f"{path}: truncated segment row")
    rows = [payload[offset : offset + ROW_BYTES] for offset in range(0, len(payload), ROW_BYTES)]
    if len(rows) != document.get("completed_rows"):
        raise ValueError(f"{path}: segment row-count mismatch")
    return rows


def command_generate_segment(
    edge_path: Path,
    segment_path: Path,
    start_index: int,
    stop_index: int,
    solver_name: str,
    seed_path: Path | None,
) -> None:
    edges = load_edges(edge_path)
    triangles = find_triangles(edges)
    vertex_deletion_seeds = load_vertex_deletion_seeds(seed_path)
    if not (0 <= start_index < stop_index <= len(edges)):
        raise ValueError("invalid segment range")
    edge_hash = edge_sha256(edges)
    rows = load_segment(segment_path, edge_hash, start_index, stop_index)
    for offset, row in enumerate(rows):
        validate_edge_deletion_coloring(edges, start_index + offset, unpack_row(row))
    started = time.monotonic()
    with build_solver(edges, solver_name) as solver:
        for edge_index in range(start_index + len(rows), stop_index):
            try:
                colors = solve_edge_deletion(
                    solver, edges, edge_index, triangles, vertex_deletion_seeds
                )
            except RuntimeError:
                save_segment(
                    segment_path, edge_hash, start_index, stop_index, solver_name, rows
                )
                raise
            rows.append(pack_row(colors))
            if len(rows) % 25 == 0 or start_index + len(rows) == stop_index:
                save_segment(
                    segment_path, edge_hash, start_index, stop_index, solver_name, rows
                )
                print(
                    json.dumps(
                        {
                            "completed_global_index": start_index + len(rows),
                            "completed_rows": len(rows),
                            "elapsed_seconds_this_run": round(time.monotonic() - started, 3),
                            "range": [start_index, stop_index],
                        },
                        sort_keys=True,
                    ),
                    flush=True,
                )


def read_merge_segment(path: Path, edge_hash: str) -> tuple[int, list[bytes], str]:
    document = json.loads(path.read_text())
    if document.get("edge_sha256") != edge_hash:
        raise ValueError(f"{path}: edge hash mismatch")
    if document.get("format") == FORMAT + "-partial":
        start_index = 0
        generator = "prefix progress generated by PySAT/CaDiCaL"
    elif document.get("format") == FORMAT + "-segment":
        start_index = int(document["start_index"])
        generator = f"PySAT solver {document.get('solver')}"
    else:
        raise ValueError(f"{path}: unsupported merge input format")
    payload = base64.b64decode(document["rows_base64"], validate=True)
    if hashlib.sha256(payload).hexdigest() != document.get("packed_sha256"):
        raise ValueError(f"{path}: payload hash mismatch")
    if len(payload) % ROW_BYTES:
        raise ValueError(f"{path}: truncated row")
    rows = [payload[offset : offset + ROW_BYTES] for offset in range(0, len(payload), ROW_BYTES)]
    if len(rows) != document.get("completed_rows"):
        raise ValueError(f"{path}: row-count mismatch")
    return start_index, rows, generator


def command_merge(edge_path: Path, certificate_path: Path, segment_paths: Sequence[Path]) -> None:
    edges = load_edges(edge_path)
    edge_hash = edge_sha256(edges)
    pieces = sorted(
        (read_merge_segment(path, edge_hash) for path in segment_paths),
        key=lambda piece: piece[0],
    )
    rows: list[bytes] = []
    generators = []
    for start_index, piece_rows, generator in pieces:
        if start_index != len(rows):
            raise ValueError(
                f"segment coverage gap or overlap: expected start {len(rows)}, got {start_index}"
            )
        rows.extend(piece_rows)
        generators.append(generator)
    if len(rows) != len(edges):
        raise ValueError(f"merged {len(rows)} rows, expected {len(edges)}")
    for edge_index, row in enumerate(rows):
        validate_edge_deletion_coloring(edges, edge_index, unpack_row(row))
    payload = b"".join(rows)
    certificate = {
        "claim": "For every edge e of H, the graph H-e has an explicit proper four-coloring whose endpoints on e have the same color.",
        "edge_file_sha256": file_sha256(edge_path),
        "edge_row_order": "lexicographic edge order, exactly as stored in the edge file",
        "edge_sha256": edge_hash,
        "edges": len(edges),
        "format": FORMAT,
        "generator": "; ".join(generators),
        "packed_edge_deletion_colorings_sha256": hashlib.sha256(payload).hexdigest(),
        "packing": PACKING,
        "rows_base64": base64.b64encode(payload).decode("ascii"),
        "vertices": N_VERTICES,
    }
    certificate_path.write_text(json.dumps(certificate, indent=2, sort_keys=True) + "\n")
    print(
        json.dumps(
            {
                "certificate": str(certificate_path),
                "certificate_sha256": file_sha256(certificate_path),
                "edge_deletion_colorings": len(rows),
                "packed_bytes": len(payload),
            },
            indent=2,
            sort_keys=True,
        )
    )


def command_verify(edge_path: Path, certificate_path: Path) -> None:
    edges = load_edges(edge_path)
    certificate = json.loads(certificate_path.read_text())
    if certificate.get("format") != FORMAT:
        raise ValueError("unknown certificate format")
    expected = {
        "edge_file_sha256": file_sha256(edge_path),
        "edge_sha256": edge_sha256(edges),
        "edges": len(edges),
        "packing": PACKING,
        "vertices": N_VERTICES,
    }
    for key, value in expected.items():
        if certificate.get(key) != value:
            raise ValueError(f"certificate {key} mismatch")
    payload = base64.b64decode(certificate["rows_base64"], validate=True)
    if len(payload) != len(edges) * ROW_BYTES:
        raise ValueError("packed certificate length mismatch")
    if hashlib.sha256(payload).hexdigest() != certificate.get(
        "packed_edge_deletion_colorings_sha256"
    ):
        raise ValueError("packed certificate hash mismatch")
    endpoint_equalities = 0
    for edge_index in range(len(edges)):
        offset = edge_index * ROW_BYTES
        colors = unpack_row(payload[offset : offset + ROW_BYTES])
        validate_edge_deletion_coloring(edges, edge_index, colors)
        endpoint_equalities += 1
    print(
        json.dumps(
            {
                "all_checks": True,
                "certificate_sha256": file_sha256(certificate_path),
                "edge_deletion_colorings_verified": len(edges),
                "edge_file_sha256": file_sha256(edge_path),
                "edge_sha256": edge_sha256(edges),
                "endpoint_equality_checks": endpoint_equalities,
                "retained_edge_inequality_checks": len(edges) * (len(edges) - 1),
                "trust_boundary": (
                    "This solver-free command proves four-colorability of every H-e. "
                    "The conclusion that H is 5-chromatic and hence edge-critical "
                    "also requires the separately audited UNSAT certificate for H."
                ),
            },
            indent=2,
            sort_keys=True,
        )
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    generate = subparsers.add_parser("generate")
    generate.add_argument("edges", type=Path)
    generate.add_argument("certificate", type=Path)
    generate.add_argument("--progress", type=Path, required=True)
    generate.add_argument("--solver", default="cadical195")
    generate.add_argument("--limit", type=int)
    generate.add_argument("--vertex-deletion-certificate", type=Path)

    segment = subparsers.add_parser("generate-segment")
    segment.add_argument("edges", type=Path)
    segment.add_argument("segment", type=Path)
    segment.add_argument("start_index", type=int)
    segment.add_argument("stop_index", type=int)
    segment.add_argument("--solver", default="cadical195")
    segment.add_argument("--vertex-deletion-certificate", type=Path)

    merge = subparsers.add_parser("merge")
    merge.add_argument("edges", type=Path)
    merge.add_argument("certificate", type=Path)
    merge.add_argument("segments", nargs="+", type=Path)

    verify = subparsers.add_parser("verify")
    verify.add_argument("edges", type=Path)
    verify.add_argument("certificate", type=Path)
    return parser


def main() -> None:
    args = build_parser().parse_args()
    if args.command == "generate":
        command_generate(
            args.edges,
            args.certificate,
            args.progress,
            args.solver,
            args.limit,
            args.vertex_deletion_certificate,
        )
    elif args.command == "generate-segment":
        command_generate_segment(
            args.edges,
            args.segment,
            args.start_index,
            args.stop_index,
            args.solver,
            args.vertex_deletion_certificate,
        )
    elif args.command == "merge":
        command_merge(args.edges, args.certificate, args.segments)
    elif args.command == "verify":
        command_verify(args.edges, args.certificate)


if __name__ == "__main__":
    main()
