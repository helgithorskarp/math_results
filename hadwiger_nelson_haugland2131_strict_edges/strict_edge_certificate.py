#!/usr/bin/env python3
"""Certify every unit pair in Haugland's G1, G2, and G3 exactly.

The finite-field evaluation is only a one-sided sieve: an exact unit pair
always survives it.  Every surviving pair is then checked in characteristic
zero in the same algebraic field used to reconstruct the points.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from itertools import combinations
from pathlib import Path
from typing import Any, Callable

import sympy as sp


RECONSTRUCTION_DIRECTORY = "hadwiger_nelson_haugland2131_exact_reproduction"


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def edge_hash(edges: list[tuple[int, int]]) -> str:
    payload = "".join(f"{u} {v}\n" for u, v in edges).encode()
    return hashlib.sha256(payload).hexdigest()


def coefficient_text(coefficient: Any) -> str:
    numerator = int(coefficient.numerator)
    denominator = int(coefficient.denominator)
    return str(numerator) if denominator == 1 else f"{numerator}/{denominator}"


def anp_text(element: Any) -> str:
    coefficients = list(reversed(element.to_list()))
    coefficients.extend([0] * (24 - len(coefficients)))
    if len(coefficients) != 24:
        raise AssertionError("unexpected algebraic-field degree")
    return ",".join(coefficient_text(value) for value in coefficients)


def coordinate_hash(points: list[Any], extended: bool) -> str:
    digest = hashlib.sha256()
    for x, y in points:
        elements = (x[0], x[1], y[0], y[1]) if extended else (x, y)
        digest.update((";".join(anp_text(value) for value in elements) + "\n").encode())
    return digest.hexdigest()


def load_reconstruct():
    sibling = Path(__file__).resolve().parent.parent / RECONSTRUCTION_DIRECTORY
    sys.path.insert(0, str(sibling))
    import reconstruct  # type: ignore[import-not-found]

    return reconstruct


def evaluate_anp(element: Any, prime: int, generator_image: int) -> int:
    """Evaluate a SymPy ANP at a chosen root modulo ``prime``."""
    value = 0
    for coefficient in element.to_list():
        numerator = int(coefficient.numerator)
        denominator = int(coefficient.denominator)
        if denominator % prime == 0:
            raise AssertionError("specialization divides a coordinate denominator")
        value = (
            value * generator_image
            + numerator * pow(denominator, -1, prime)
        ) % prime
    return value


def check_specialization(field: Any, prime: int, zeta_image: int) -> None:
    if not sp.isprime(prime):
        raise AssertionError("sieve modulus is not prime")
    if pow(zeta_image, 84, prime) != 1:
        raise AssertionError("zeta image is not an 84th root of unity")
    for divisor in (2, 3, 7):
        if pow(zeta_image, 84 // divisor, prime) == 1:
            raise AssertionError("zeta image does not have exact order 84")
    modulus_value = 0
    for coefficient in field.field.mod.to_list():
        modulus_value = (
            modulus_value * zeta_image + int(coefficient.numerator)
        ) % prime
    if modulus_value != 0:
        raise AssertionError("zeta image is not a root of the defining polynomial")
    if evaluate_anp(field.zeta, prime, zeta_image) != zeta_image:
        raise AssertionError("algebraic generator does not map to the chosen root")
    if evaluate_anp(field.one, prime, zeta_image) != 1:
        raise AssertionError("specialization does not preserve one")


def base_images(points: list[Any], prime: int, zeta_image: int) -> list[tuple[int, int]]:
    return [
        (
            evaluate_anp(x, prime, zeta_image),
            evaluate_anp(y, prime, zeta_image),
        )
        for x, y in points
    ]


def extended_images(
    points: list[Any], prime: int, zeta_image: int, sqrt5_image: int
) -> list[tuple[int, int]]:
    if sqrt5_image * sqrt5_image % prime != 5 % prime:
        raise AssertionError("sqrt(5) image has the wrong square")

    def evaluate_pair(pair: tuple[Any, Any]) -> int:
        return (
            evaluate_anp(pair[0], prime, zeta_image)
            + sqrt5_image * evaluate_anp(pair[1], prime, zeta_image)
        ) % prime

    return [(evaluate_pair(x), evaluate_pair(y)) for x, y in points]


def sieve_candidates(images: list[tuple[int, int]], prime: int) -> list[tuple[int, int]]:
    candidates: list[tuple[int, int]] = []
    for u, v in combinations(range(len(images)), 2):
        dx = images[u][0] - images[v][0]
        dy = images[u][1] - images[v][1]
        if (dx * dx + dy * dy - 1) % prime == 0:
            candidates.append((u, v))
    return candidates


def confirm_base(
    points: list[Any], candidates: list[tuple[int, int]], one: Any
) -> list[tuple[int, int]]:
    edges: list[tuple[int, int]] = []
    for u, v in candidates:
        dx = points[u][0] - points[v][0]
        dy = points[u][1] - points[v][1]
        if dx * dx + dy * dy == one:
            edges.append((u, v))
    return edges


def confirm_extended(
    reconstruct: Any,
    points: list[Any],
    candidates: list[tuple[int, int]],
    zero: Any,
    one: Any,
) -> list[tuple[int, int]]:
    edges: list[tuple[int, int]] = []
    for u, v in candidates:
        dx = reconstruct.pair_sub(points[u][0], points[v][0])
        dy = reconstruct.pair_sub(points[u][1], points[v][1])
        norm = reconstruct.pair_add(
            reconstruct.pair_square(dx), reconstruct.pair_square(dy)
        )
        if norm == (one, zero):
            edges.append((u, v))
    return edges


def certify_graph(
    name: str,
    points: list[Any],
    image_builder: Callable[[list[Any]], list[tuple[int, int]]],
    confirmer: Callable[[list[Any], list[tuple[int, int]]], list[tuple[int, int]]],
    prime: int,
    coordinate_sha256: str,
) -> tuple[dict[str, Any], list[tuple[int, int]]]:
    candidates = sieve_candidates(image_builder(points), prime)
    edges = confirmer(points, candidates)
    if edges != sorted(edges):
        raise AssertionError(f"{name} edges are not canonical")
    result = {
        "vertices": len(points),
        "pairs_checked": len(points) * (len(points) - 1) // 2,
        "sieve_survivors": len(candidates),
        "strict_unit_edges": len(edges),
        "edge_sha256": edge_hash(edges),
        "coordinate_sha256": coordinate_sha256,
    }
    return result, edges


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("graph", type=Path)
    parser.add_argument("certificate", type=Path)
    args = parser.parse_args()

    certificate = json.loads(args.certificate.read_text())
    if sha256_file(args.graph) != certificate["input_graph_sha256"]:
        raise AssertionError("input graph hash mismatch")
    payload = json.loads(args.graph.read_text())

    reconstruct = load_reconstruct()
    field = reconstruct.Cyclotomic84()
    vectors = field.unit_vectors()
    float_vectors = field.float_vectors()
    g1, f1 = reconstruct.build_g1(payload["paths"], vectors, float_vectors, field)
    g2, f2 = reconstruct.build_g2(g1, f1, field)
    g3, _ = reconstruct.build_g3(g2, f2, field)

    parameters = certificate["primary_specialization"]
    prime = parameters["prime"]
    zeta_image = parameters["zeta_image"]
    sqrt5_image = parameters["sqrt5_image"]
    check_specialization(field, prime, zeta_image)

    base_builder = lambda points: base_images(points, prime, zeta_image)
    g1_result, g1_edges = certify_graph(
        "G1",
        g1,
        base_builder,
        lambda points, candidates: confirm_base(points, candidates, field.one),
        prime,
        coordinate_hash(g1, False),
    )
    g2_result, _ = certify_graph(
        "G2",
        g2,
        base_builder,
        lambda points, candidates: confirm_base(points, candidates, field.one),
        prime,
        coordinate_hash(g2, False),
    )
    g3_result, g3_edges = certify_graph(
        "G3",
        g3,
        lambda points: extended_images(
            points, prime, zeta_image, sqrt5_image
        ),
        lambda points, candidates: confirm_extended(
            reconstruct, points, candidates, field.zero, field.one
        ),
        prime,
        coordinate_hash(g3, True),
    )
    results = {"G1": g1_result, "G2": g2_result, "G3": g3_result}
    if results != certificate["primary_results"]:
        raise AssertionError(
            "strict-edge results differ from certificate:\n"
            + json.dumps(results, indent=2, sort_keys=True)
        )

    declared_g1 = [tuple(edge) for edge in payload["G1_edges"]]
    declared_g3 = [tuple(edge) for edge in payload["G3_edges"]]
    if g1_edges != declared_g1 or g3_edges != declared_g3:
        raise AssertionError("strict edge set differs from the committed edge set")
    for name, result in results.items():
        if list(payload["graph_counts"][name]) != [
            result["vertices"],
            result["strict_unit_edges"],
        ]:
            raise AssertionError(f"{name} graph count mismatch")

    summaries = " ".join(
        f"{name}_pairs={result['pairs_checked']} "
        f"{name}_survivors={result['sieve_survivors']} "
        f"{name}_strict_edges={result['strict_unit_edges']} "
        f"{name}_edge_sha256={result['edge_sha256']} "
        f"{name}_coordinate_sha256={result['coordinate_sha256']}"
        for name, result in results.items()
    )
    print(f"primary_all_checks=true prime={prime} {summaries}")


if __name__ == "__main__":
    main()
