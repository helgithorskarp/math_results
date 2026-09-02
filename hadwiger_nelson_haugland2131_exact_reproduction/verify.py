#!/usr/bin/env python3
"""Solver-free replay plus optional DRAT audit for the Haugland graph."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from itertools import combinations
from pathlib import Path

from pysat.formula import CNF

import reconstruct
import sat_cert


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def exact_edges_base(points, edges, one) -> None:
    seen: set[tuple[int, int]] = set()
    for u, v in edges:
        if not 0 <= u < v < len(points) or (u, v) in seen:
            raise AssertionError(f"invalid or duplicate edge {(u, v)}")
        seen.add((u, v))
        dx = points[u][0] - points[v][0]
        dy = points[u][1] - points[v][1]
        if dx * dx + dy * dy != one:
            raise AssertionError(f"non-unit declared edge {(u, v)}")


def exact_edges_extended(points, edges, zero, one) -> None:
    seen: set[tuple[int, int]] = set()
    for u, v in edges:
        if not 0 <= u < v < len(points) or (u, v) in seen:
            raise AssertionError(f"invalid or duplicate edge {(u, v)}")
        seen.add((u, v))
        dx = reconstruct.pair_sub(points[u][0], points[v][0])
        dy = reconstruct.pair_sub(points[u][1], points[v][1])
        norm = reconstruct.pair_add(
            reconstruct.pair_square(dx), reconstruct.pair_square(dy)
        )
        if norm != (one, zero):
            raise AssertionError(f"non-unit declared edge {(u, v)}")


def contains_moser_spindle(n: int, edges: list[tuple[int, int]]) -> bool:
    """Exhaustively seek the two K4-e arms in the Hajós description."""
    adjacency = [set() for _ in range(n)]
    edge_set = set(edges)
    for u, v in edges:
        adjacency[u].add(v)
        adjacency[v].add(u)

    for shared in range(n):
        arms: set[tuple[int, int, int]] = set()
        for left, right in combinations(sorted(adjacency[shared]), 2):
            if (min(left, right), max(left, right)) not in edge_set:
                continue
            for tip in adjacency[left] & adjacency[right]:
                if tip not in {shared, left, right}:
                    arms.add((tip, left, right))
        arms_list = sorted(arms)
        for i, (tip1, left1, right1) in enumerate(arms_list):
            first = {tip1, left1, right1}
            for tip2, left2, right2 in arms_list[i + 1 :]:
                if first & {tip2, left2, right2}:
                    continue
                if tip2 in adjacency[tip1]:
                    return True
    return False


def expected_g1_cnf(payload: dict, g1_points, sqrt3) -> tuple[CNF, tuple[int, int, int]]:
    endpoint_a, _ = payload["G1_endpoints"]
    cnf, triangle, lex_pairs = sat_cert.endpoint_forcing_cnf(
        payload, g1_points, sqrt3
    )
    if triangle[0] != endpoint_a:
        raise AssertionError("canonical triangle must start at endpoint A")
    if len(lex_pairs) != sat_cert.LEX_PAIR_COUNT:
        raise AssertionError("lex-pair count mismatch")
    return cnf, triangle


def verify_structural_bridge(
    g1_points, g1_edges, g2_points, g3_points, g3_edges, field
) -> dict[str, int]:
    zero, one, r = field.zero, field.one, field.sqrt3

    def ext(x, y):
        return (reconstruct.promote(x, zero), reconstruct.promote(y, zero))

    p = ext(-one, zero)
    q = ext(zero, zero)
    s = ext(one, zero)
    a = ext(-one / 2, r / 2)
    b = ext(one / 2, r / 2)
    sprime = (
        (3 * one / 4, zero),
        (zero, r / 4),  # (sqrt(15)/4) = (sqrt(3)/4) sqrt(5)
    )
    index = {point: vertex for vertex, point in enumerate(g3_points)}
    named = {name: index[point] for name, point in {"p": p, "q": q, "s": s, "a": a, "b": b, "sprime": sprime}.items()}
    edge_set = set(g3_edges)
    required = [
        ("p", "q"),
        ("q", "s"),
        ("p", "a"),
        ("a", "q"),
        ("q", "b"),
        ("b", "s"),
        ("a", "b"),
        ("s", "sprime"),
    ]
    for left, right in required:
        edge = tuple(sorted((named[left], named[right])))
        if edge not in edge_set:
            raise AssertionError(f"missing structural unit edge {left}-{right}: {edge}")

    # Build exactly the portion of G2 used by the K5-e argument: two isometric
    # G1 copies plus the seven unit edges among p,q,s,a,b.  Then check this
    # entire forcing subgraph in both final copies, not only its named points.
    g2_index = {point: vertex for vertex, point in enumerate(g2_points)}

    def transform_g1(point, copy):
        x, y = point
        if copy == 1:
            return ((x + r * y) / 2 - one, (-r * x + y) / 2)
        return ((x - r * y) / 2 + one, (r * x + y) / 2)

    required_g2_edges: set[tuple[int, int]] = set()
    for copy in (1, 2):
        mapping = [g2_index[transform_g1(point, copy)] for point in g1_points]
        required_g2_edges.update(
            tuple(sorted((mapping[u], mapping[v]))) for u, v in g1_edges
        )
    base_named_points = {"p": (-one, zero), "q": (zero, zero), "s": (one, zero), "a": (-one / 2, r / 2), "b": (one / 2, r / 2)}
    base_named = {name: g2_index[point] for name, point in base_named_points.items()}
    for left, right in required[:-1]:
        required_g2_edges.add(tuple(sorted((base_named[left], base_named[right]))))

    def final_transform(point, copy):
        x, y = point
        if copy == 0:
            return ext(x, y)
        return (
            ((7 * (x + one)) / 8 - one, -(r * y) / 8),
            (7 * y / 8, r * (x + one) / 8),
        )

    edge_set = set(g3_edges)
    for copy in (0, 1):
        mapping = [index[final_transform(point, copy)] for point in g2_points]
        for u, v in required_g2_edges:
            edge = tuple(sorted((mapping[u], mapping[v])))
            if edge not in edge_set:
                raise AssertionError(f"forcing subgraph edge absent from G3: {edge}")

    # The two G1 copies force p != b and s != a.  The seven first-stage
    # unit edges therefore give K5 minus p-s on {p,q,s,a,b}; four colours
    # force p=s.  The rotated G2 copy forces p=sprime, contradicting s-sprime.
    return named


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("graph", type=Path)
    parser.add_argument("certificate", type=Path)
    parser.add_argument("--cnf", type=Path)
    parser.add_argument("--proof", type=Path)
    parser.add_argument("--drat-trim", type=Path)
    args = parser.parse_args()

    payload = json.loads(args.graph.read_text())
    certificate = json.loads(args.certificate.read_text())
    field = reconstruct.Cyclotomic84()
    vectors = field.unit_vectors()
    floats = field.float_vectors()

    g1, f1 = reconstruct.build_g1(payload["paths"], vectors, floats, field)
    g1_edges = [tuple(edge) for edge in payload["G1_edges"]]
    if len(g1) != 740 or len(g1_edges) != 3985:
        raise AssertionError("G1 count mismatch")
    if payload["G1_endpoints"] != [g1.index((field.zero, field.zero)), g1.index((field.zero, field.sqrt3))]:
        raise AssertionError("G1 endpoint mismatch")
    exact_edges_base(g1, g1_edges, field.one)

    g2, f2 = reconstruct.build_g2(g1, f1, field)
    g3, _ = reconstruct.build_g3(g2, f2, field)
    g3_edges = [tuple(edge) for edge in payload["G3_edges"]]
    if len(g2) != 1066 or len(g3) != 2131 or len(g3_edges) != 12530:
        raise AssertionError("G2/G3 count mismatch")
    exact_edges_extended(g3, g3_edges, field.zero, field.one)

    colouring = certificate["five_colouring"]
    if len(colouring) != len(g3):
        raise AssertionError("5-colouring length mismatch")
    sat_cert.check_colouring(colouring, g3_edges, 5)
    if certificate.get("G1_halfturn_colour_involution") != list(
        sat_cert.COLOUR_INVOLUTION
    ) or certificate.get("G1_prefix_lex_pairs") != sat_cert.LEX_PAIR_COUNT:
        raise AssertionError("certificate symmetry metadata mismatch")
    if contains_moser_spindle(len(g3), g3_edges):
        raise AssertionError("declared graph contains a Moser spindle subgraph")
    named = verify_structural_bridge(g1, g1_edges, g2, g3, g3_edges, field)

    expected_cnf, triangle = expected_g1_cnf(payload, g1, field.sqrt3)
    if args.cnf:
        supplied = CNF(from_file=args.cnf)
        if supplied.nv != expected_cnf.nv or supplied.clauses != expected_cnf.clauses:
            raise AssertionError("supplied CNF differs from canonical reconstruction")
        print(f"cnf_sha256={sha256(args.cnf)}")
    if args.proof:
        if not args.cnf or not args.drat_trim:
            raise ValueError("--proof requires --cnf and --drat-trim")
        print(f"proof_sha256={sha256(args.proof)}")
        completed = subprocess.run(
            [str(args.drat_trim), str(args.cnf), str(args.proof)],
            check=False,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
        print(completed.stdout, end="")
        if completed.returncode != 0 or "s VERIFIED" not in completed.stdout:
            raise AssertionError("drat-trim did not verify the proof")

    print(
        "all_checks=true "
        f"G1_unit_edges={len(g1_edges)} G3_unit_edges={len(g3_edges)} "
        f"five_colouring=true moser_spindle_free=true triangle_pin={triangle} "
        f"structural_vertices={named}"
    )


if __name__ == "__main__":
    main()
