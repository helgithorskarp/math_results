#!/usr/bin/env python3
"""Definition-level audit of the Parts-509 degree-7-pool certificate.

This checker deliberately does not import the reviewed implementation.  It
tests every one of the C(585, 2) point pairs in the exact multiquadratic field
Q(sqrt(3), sqrt(5), sqrt(11)); there is no floating-point rejection screen.
It then replays every supplied four-colouring and checks a concrete
58-element hitting set.  The *lower* bound 58 is not established here: that
requires the separately documented optimization/proof computation.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from collections import Counter
from fractions import Fraction
from pathlib import Path


PRIMES = (3, 5, 11)
EXPECTED_CERTIFICATE_SHA256 = (
    "41a47be8d0568be7e1497f16a45c17d433e31e01fb62877856189fbf1ad53729"
)
EXPECTED_HITTING_SET = {
    13, 14, 15, 23, 24, 25, 27, 70, 75, 112, 121, 125, 126, 127, 128,
    129, 132, 133, 147, 185, 218, 252, 350, 369, 371, 392, 393, 412,
    413, 414, 415, 416, 431, 433, 455, 457, 472, 473, 477, 479, 495,
    510, 511, 513, 515, 518, 520, 521, 523, 526, 527, 528, 545, 551,
    563, 566, 578, 579,
}


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def parse_coefficients(values: list[str]) -> tuple[Fraction, ...]:
    if len(values) != 8:
        raise AssertionError("a field element must have eight coefficients")
    return tuple(Fraction(value) for value in values)


def scaled_coordinates(
    document: dict[str, object], vertices: list[int]
) -> tuple[int, dict[int, tuple[tuple[int, ...], tuple[int, ...]]]]:
    rational = {
        vertex: (
            parse_coefficients(document["coordinates"][str(vertex)][0]),
            parse_coefficients(document["coordinates"][str(vertex)][1]),
        )
        for vertex in vertices
    }
    scale = 1
    for point in rational.values():
        for coordinate in point:
            for coefficient in coordinate:
                scale = math.lcm(scale, coefficient.denominator)
    integer = {
        vertex: tuple(
            tuple(coefficient.numerator * (scale // coefficient.denominator)
                  for coefficient in coordinate)
            for coordinate in point
        )
        for vertex, point in rational.items()
    }
    return scale, integer


def square_in_field(values: tuple[int, ...]) -> list[int]:
    """Return coefficients of the square in the fixed radical basis."""
    result = [0] * 8
    nonzero = [(mask, value) for mask, value in enumerate(values) if value]
    for left_index, (left_mask, left) in enumerate(nonzero):
        for right_index in range(left_index, len(nonzero)):
            right_mask, right = nonzero[right_index]
            coefficient = left * right
            if right_index != left_index:
                coefficient *= 2
            common = left_mask & right_mask
            for bit, prime in enumerate(PRIMES):
                if (common >> bit) & 1:
                    coefficient *= prime
            result[left_mask ^ right_mask] += coefficient
    return result


def unit_distance(
    left: tuple[tuple[int, ...], tuple[int, ...]],
    right: tuple[tuple[int, ...], tuple[int, ...]],
    scale_squared: int,
) -> bool:
    dx = tuple(a - b for a, b in zip(left[0], right[0]))
    dy = tuple(a - b for a, b in zip(left[1], right[1]))
    squared_x = square_in_field(dx)
    squared_y = square_in_field(dy)
    distance = [a + b for a, b in zip(squared_x, squared_y)]
    return distance[0] == scale_squared and all(value == 0 for value in distance[1:])


def edge_digest(edges: list[tuple[int, int]]) -> str:
    payload = "".join(f"{left} {right}\n" for left, right in edges).encode()
    return hashlib.sha256(payload).hexdigest()


def proper_colouring(
    witness: str,
    vertices: list[int],
    edges: list[tuple[int, int]],
    deleted: set[int],
) -> bool:
    survivors = [vertex for vertex in vertices if vertex not in deleted]
    if len(witness) != len(survivors) or set(witness) > set("0123"):
        return False
    colour = dict(zip(survivors, witness, strict=True))
    return all(
        left in deleted or right in deleted or colour[left] != colour[right]
        for left, right in edges
    )


def decision_opb_hash(
    free: list[int], family: list[frozenset[int]], pool: list[int]
) -> str:
    """Rebuild the published budget-57, at-least-four-pool OPB instance."""
    variable = {vertex: index + 1 for index, vertex in enumerate(free)}
    minimal = [
        deletion for deletion in family
        if not any(other < deletion for other in family)
    ]
    lines = [
        " ".join(f"+1 x{variable[vertex]}" for vertex in sorted(deletion))
        + " >= 1 ;"
        for deletion in minimal
    ]
    lines.append(
        " ".join(f"+1 x{variable[vertex]}" for vertex in pool) + " >= 4 ;"
    )
    lines.append(
        " ".join(f"-1 x{variable[vertex]}" for vertex in free) + " >= -57 ;"
    )
    header = (
        f"* #variable= {len(free)} #constraint= {len(lines)} "
        "#equal= 0 intsize= 8\n"
    )
    return hashlib.sha256((header + "\n".join(lines) + "\n").encode()).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("certificate", type=Path)
    args = parser.parse_args()

    certificate_hash = digest(args.certificate)
    if certificate_hash != EXPECTED_CERTIFICATE_SHA256:
        raise AssertionError("unexpected certificate SHA-256")
    document = json.loads(args.certificate.read_text())
    vertices = document["vertices"]
    if vertices != sorted(set(vertices)) or len(vertices) != 585:
        raise AssertionError("expected 585 distinct, ordered ambient vertices")

    scale, coordinates = scaled_coordinates(document, vertices)
    if len(set(coordinates.values())) != len(vertices):
        raise AssertionError("duplicate exact coordinates")
    edges: list[tuple[int, int]] = []
    for left_index, left in enumerate(vertices):
        for right in vertices[left_index + 1:]:
            if unit_distance(coordinates[left], coordinates[right], scale * scale):
                edges.append((left, right))
    if len(edges) != 3083:
        raise AssertionError(f"expected 3083 unit edges, found {len(edges)}")

    forced = document["forced"]
    free = document["free"]
    pool = document["pool_free"]
    if sorted(forced + free) != vertices or set(forced) & set(free):
        raise AssertionError("forced/free partition is malformed")
    if len(forced) != 451 or len(free) != 134:
        raise AssertionError("unexpected forced/free sizes")
    if pool != document["pool"] or set(pool) != {vertex for vertex in free if vertex >= 509}:
        raise AssertionError("pool/free metadata mismatch")

    for vertex in forced:
        witness = document["forced_witness"].get(str(vertex))
        if witness is None or not proper_colouring(witness, vertices, edges, {vertex}):
            raise AssertionError(f"invalid forced-vertex witness for {vertex}")

    free_set = set(free)
    family: list[frozenset[int]] = []
    for row in document["family"]:
        deletion = frozenset(row["D"])
        if not deletion or not deletion <= free_set or len(deletion) != len(row["D"]):
            raise AssertionError("malformed killing set")
        if not proper_colouring(row["witness"], vertices, edges, set(deletion)):
            raise AssertionError(f"invalid killing-set witness {sorted(deletion)}")
        family.append(deletion)
    if len(family) != 425 or len(set(family)) != 425:
        raise AssertionError("expected 425 distinct killing sets")
    minimal = [D for D in family if not any(E < D for E in family)]
    if len(minimal) != 337:
        raise AssertionError("expected 337 inclusion-minimal killing sets")

    if len(EXPECTED_HITTING_SET) != 58:
        raise AssertionError("malformed compact hitting-set witness")
    if not EXPECTED_HITTING_SET <= free_set:
        raise AssertionError("hitting-set witness contains a non-free vertex")
    if len(EXPECTED_HITTING_SET & set(pool)) != 17:
        raise AssertionError("unexpected pool count in hitting-set witness")
    if any(not EXPECTED_HITTING_SET & deletion for deletion in family):
        raise AssertionError("the compact 58-set does not hit the certified family")
    if (
        document["min_points"] != 4
        or document["minimum_hitting_set"] != 58
        or document["target"] != 58
    ):
        raise AssertionError("unexpected recorded optimization target")

    sizes = Counter(map(len, minimal))
    opb_hash = decision_opb_hash(free, family, pool)
    expected_opb_hash = "03dfd3601258be7899c607696b96bf9b0ddba77784db404cca045e7b8dfdda9d"
    if opb_hash != expected_opb_hash:
        raise AssertionError("independently rebuilt OPB hash mismatch")

    print("PASS exact all-pairs audit of the Parts-509 degree-7-pool certificate")
    print(
        f"vertices={len(vertices)} exact_pair_tests={len(vertices) * (len(vertices)-1) // 2} "
        f"unit_edges={len(edges)} coordinate_scale={scale}"
    )
    print(
        f"forced_witnesses={len(forced)} killing_witnesses={len(family)} "
        f"minimal_killing_sets={len(minimal)} minimal_size_histogram={dict(sorted(sizes.items()))}"
    )
    print(
        "hitting_set_witness_size=58 pool_vertices_in_witness=17 "
        "recorded_lower_bound=58 lower_bound_checked_here=false"
    )
    print(f"edge_list_sha256={edge_digest(edges)}")
    print(f"decision_opb_sha256={opb_hash}")
    print(f"certificate_sha256={certificate_hash}")


if __name__ == "__main__":
    main()
