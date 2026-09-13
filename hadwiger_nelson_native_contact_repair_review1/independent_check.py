#!/usr/bin/env python3
"""Clean-room audit of the native-contact HN construction.

This checker imports no code from the reviewed package.  It reconstructs the
two physical hosts from the pinned 159-row source, enumerates every strict
unit edge, checks all positive colour certificates, and independently emits
the selected graph's four-colour CNF.  A finite-field homomorphism is used
only as a safe all-pairs sieve; every surviving pair is decided again by
generic exact multiplication in Q(sqrt(3),sqrt(5),sqrt(11)).

With --record, SymPy's general algebraic-number field implementation is used
to reparse the separate Mathematica Parts-509 coordinate file and discover
the exact displayed-coordinate overlap.  This is deliberately separate from
the standard-library geometry proof.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPOSITORY = HERE.parent
TARGET = REPOSITORY / "hadwiger_nelson_native_contact_repair"
SEED = REPOSITORY / "hadwiger_nelson_nonmono159_214_lowden2" / "points159.tsv"
PARTS = REPOSITORY / "hadwiger_nelson_parts509_criticality" / "parts509.vtx"

PINS = {
    TARGET / "certificate.json": "55f29fcb4f21b3dfd00c1b9cb6c0c13a823764e688dd16a0f709163f2308e290",
    SEED: "4f72fa06d18434472ce77cebe38880333694ec04b94945ede073a4a1c6d5bc02",
    PARTS: "770a585a6c1e1222355322707479cb826e9ada560279da904ef89c15c99ff0b5",
}

# Coefficient index m denotes the squarefree radical with prime mask m.
PRIMES = (3, 5, 11)
RADICAND = tuple(math.prod(PRIMES[k] for k in range(3) if m & (1 << k)) for m in range(8))
ZERO = (0,) * 8
ONE_12 = (144,) + (0,) * 7
ONE_96 = (96 * 96,) + (0,) * 7
Point = tuple[tuple[int, ...], tuple[int, ...]]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for block in iter(lambda: source.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def digest_json(value: object) -> str:
    return hashlib.sha256(json.dumps(value, separators=(",", ":")).encode()).hexdigest()


def add(a: tuple[int, ...], b: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(x + y for x, y in zip(a, b))


def sub(a: tuple[int, ...], b: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(x - y for x, y in zip(a, b))


def scale(a: tuple[int, ...], coefficient: int) -> tuple[int, ...]:
    return tuple(coefficient * x for x in a)


def multiply(a: tuple[int, ...], b: tuple[int, ...]) -> tuple[int, ...]:
    """Generic multiplication in the eight-element squarefree basis."""
    out = [0] * 8
    for i, x in enumerate(a):
        if not x:
            continue
        for j, y in enumerate(b):
            if y:
                out[i ^ j] += x * y * RADICAND[i & j]
    return tuple(out)


def norm(point: Point) -> tuple[int, ...]:
    x, y = point
    return add(multiply(x, x), multiply(y, y))


def point_add(a: Point, b: Point) -> Point:
    return add(a[0], b[0]), add(a[1], b[1])


def point_sub(a: Point, b: Point) -> Point:
    return sub(a[0], b[0]), sub(a[1], b[1])


def point_scale(a: Point, coefficient: int) -> Point:
    return scale(a[0], coefficient), scale(a[1], coefficient)


def read_seed() -> list[Point]:
    rows = []
    for line in SEED.read_text().splitlines():
        if line and not line.startswith("#"):
            row = tuple(map(int, line.split()))
            require(len(row) == 16, "seed row width")
            rows.append((row[:8], row[8:]))
    require(len(rows) == 159 and len(set(rows)) == 159, "seed cardinality")
    require(all(all(x[k] == 0 for k in (1, 2, 3, 4, 6, 7)) for x, _ in rows), "seed x subspace")
    require(all(all(y[k] == 0 for k in (0, 2, 3, 5, 6, 7)) for _, y in rows), "seed y subspace")
    return rows


def sign_a_plus_b_sqrt33(a: int, b: int) -> int:
    if b == 0:
        return (a > 0) - (a < 0)
    if a == 0 or (a > 0) == (b > 0):
        return (b > 0) - (b < 0)
    comparison = a * a - 33 * b * b
    require(comparison != 0, "impossible rational equality to nonzero sqrt(33)")
    return ((a > 0) - (a < 0)) * ((comparison > 0) - (comparison < 0))


def within_radius_two(point: Point) -> bool:
    value = list(norm(point))
    value[0] -= 4 * 12 * 12
    require(all(value[k] == 0 for k in range(8) if k not in (0, 5)), "radius field")
    return sign_a_plus_b_sqrt33(value[0], value[5]) <= 0


def flatten(point: Point) -> tuple[int, ...]:
    x, y = point
    require(all(x[k] == 0 for k in (1, 3, 4, 6)), "host x subspace")
    require(all(y[k] == 0 for k in (0, 2, 5, 7)), "host y subspace")
    return x[0], x[2], x[5], x[7], y[1], y[3], y[4], y[6]


def generate_host(truncated: bool) -> list[Point]:
    seed = read_seed()
    directions: set[Point] = set()
    for i, a in enumerate(seed):
        for b in seed[:i]:
            difference = point_sub(a, b)
            if norm(difference) == ONE_12:
                directions.add(difference)
                directions.add(point_scale(difference, -1))
    require(len(directions) == 30, "oriented direction count")
    enlarged = set(seed)
    enlarged.update(point_add(a, direction) for a in seed for direction in directions)
    if truncated:
        enlarged = {point for point in enlarged if within_radius_two(point)}
    ordered = sorted(enlarged, key=lambda p: (p[0][0], p[0][5], p[1][1], p[1][4]))
    require(len(ordered) == (1525 if truncated else 1960), "one-copy host count")

    sqrt15 = (0, 0, 0, 1, 0, 0, 0, 0)
    native = [(scale(x, 8), scale(y, 8)) for x, y in ordered]
    rotated = [
        (sub(scale(x, 7), multiply(sqrt15, y)), add(multiply(sqrt15, x), scale(y, 7)))
        for x, y in ordered
    ]
    points = list(dict.fromkeys(native + rotated))
    require(len(points) == (3049 if truncated else 3919), "two-copy host count")
    require(len({flatten(point) for point in points}) == len(points), "physical point uniqueness")
    return points


# One exact field homomorphism into F_p.  It can create false positives but
# cannot discard an exact unit pair.  All survivors are checked in the field.
SIEVE_PRIME = 1_000_081
SIEVE_ROOTS = (35_512, 183_365, 29_480)


def prime_by_trial_division(number: int) -> bool:
    if number < 2:
        return False
    for divisor in range(2, math.isqrt(number) + 1):
        if number % divisor == 0:
            return False
    return True


def field_evaluations() -> tuple[int, ...]:
    require(prime_by_trial_division(SIEVE_PRIME), "sieve modulus is not prime")
    require(all(root * root % SIEVE_PRIME == radicand for root, radicand in zip(SIEVE_ROOTS, PRIMES)), "bad sieve roots")
    values = []
    for mask in range(8):
        values.append(math.prod(SIEVE_ROOTS[k] for k in range(3) if mask & (1 << k)) % SIEVE_PRIME)
    return tuple(values)


def strict_edges(points: list[Point]) -> tuple[list[tuple[int, int]], int]:
    basis_values = field_evaluations()
    residues = [
        (
            sum(coefficient * basis_values[k] for k, coefficient in enumerate(x)) % SIEVE_PRIME,
            sum(coefficient * basis_values[k] for k, coefficient in enumerate(y)) % SIEVE_PRIME,
        )
        for x, y in points
    ]
    edges = []
    survivors = 0
    modulus = SIEVE_PRIME
    target = 96 * 96 % modulus
    for i, point in enumerate(points):
        xi, yi = residues[i]
        for j in range(i):
            xj, yj = residues[j]
            dx = xi - xj
            dy = yi - yj
            if (dx * dx + dy * dy) % modulus != target:
                continue
            survivors += 1
            if norm(point_sub(point, points[j])) == ONE_96:
                edges.append((j, i))
    return edges, survivors


def colour(edges: list[tuple[int, int]], word: str, vertices: int, colours: int) -> None:
    require(isinstance(word, str) and len(word) == vertices, "colour-word length")
    require(all(character in "0123456"[:colours] for character in word), "colour-word alphabet")
    require(all(word[a] != word[b] for a, b in edges), "monochromatic edge")


def subset_edges(edges: list[tuple[int, int]], vertices: list[int]) -> list[tuple[int, int]]:
    index = {vertex: i for i, vertex in enumerate(vertices)}
    return [(index[a], index[b]) for a, b in edges if a in index and b in index]


def encode_four_colouring(vertices: int, edges: list[tuple[int, int]]) -> tuple[str, tuple[int, int, int]]:
    clauses: list[list[int]] = []
    adjacency = [set() for _ in range(vertices)]
    for vertex in range(vertices):
        variables = [4 * vertex + colour_index + 1 for colour_index in range(4)]
        clauses.append(variables)
        for high in range(4):
            for low in range(high):
                clauses.append([-variables[high], -variables[low]])
    for a, b in edges:
        adjacency[a].add(b)
        adjacency[b].add(a)
        for colour_index in range(4):
            clauses.append([-(4 * a + colour_index + 1), -(4 * b + colour_index + 1)])
    triangle = next(
        (a, b, c)
        for a, b in edges
        for c in sorted(adjacency[a] & adjacency[b])
        if c > b
    )
    clauses.extend([[4 * vertex + colour_index + 1] for colour_index, vertex in enumerate(triangle)])
    text = f"p cnf {4 * vertices} {len(clauses)}\n" + "".join(
        " ".join(map(str, clause)) + " 0\n" for clause in clauses
    )
    return text, triangle


def split_pair(body: str) -> tuple[str, str]:
    depth = 0
    for index, character in enumerate(body):
        if character == "(":
            depth += 1
        elif character == ")":
            depth -= 1
        elif character == "," and depth == 0:
            return body[:index], body[index + 1 :]
    raise ValueError("cannot split Mathematica coordinate")


def check_record_overlap(compact_full: list[tuple[int, ...]], certificate: dict) -> dict:
    """Discover the displayed overlap through SymPy's ANP representation."""
    import sympy

    roots = [sympy.sqrt(p) for p in PRIMES]
    field = sympy.QQ.algebraic_field(*roots)
    require(field.ext.minpoly.degree() == 8, "unexpected number-field degree")
    basis_expr = []
    for mask in range(8):
        expression = sympy.Integer(1)
        for k in range(3):
            if mask & (1 << k):
                expression *= roots[k]
        basis_expr.append(expression)
    basis = [field.from_sympy(expression) for expression in basis_expr]

    def host_element(coefficients: tuple[int, ...], masks: tuple[int, ...]):
        result = field.zero
        for coefficient, mask in zip(coefficients, masks):
            result += field.convert(sympy.Rational(coefficient, 96)) * basis[mask]
        return result

    host = {}
    for index, point in enumerate(compact_full):
        x = host_element(point[:4], (0, 2, 5, 7))
        y = host_element(point[4:], (1, 3, 4, 6))
        require((x, y) not in host, "duplicate algebraic host point")
        host[(x, y)] = index

    parsed = []
    for line in PARTS.read_text().splitlines():
        if not line.strip():
            continue
        translated = line.strip()[1:-1].replace("Sqrt[", "sqrt(").replace("]", ")")
        x_text, y_text = split_pair(translated)
        x = field.from_sympy(sympy.sqrtdenest(sympy.sympify(x_text)))
        y = field.from_sympy(sympy.sqrtdenest(sympy.sympify(y_text)))
        parsed.append((x, y))
    require(len(parsed) == 509 and len(set(parsed)) == 509, "Parts source cardinality")
    mapping = {str(index): host[point] for index, point in enumerate(parsed) if point in host}
    missing = [index for index, point in enumerate(parsed) if point not in host]
    require(mapping == certificate["record_map"], "record map mismatch")
    require(missing == certificate["missing_original_indices"], "missing record labels mismatch")
    return {"matched_vertices": len(mapping), "missing_original_indices": missing, "field_degree": 8}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--work", type=Path, required=True)
    parser.add_argument("--record", action="store_true", help="also run the independent SymPy overlap check")
    parser.add_argument("--check-expected", action="store_true")
    args = parser.parse_args()
    require(not args.check_expected or args.record, "--check-expected requires --record")
    args.work.mkdir(parents=True, exist_ok=True)
    start = time.monotonic()

    for path, expected_hash in PINS.items():
        require(file_sha256(path) == expected_hash, f"source pin: {path.name}")
    certificate = json.loads((TARGET / "certificate.json").read_text())

    radius = generate_host(True)
    radius_edges, radius_survivors = strict_edges(radius)
    compact_radius = [flatten(point) for point in radius]
    colour(radius_edges, certificate["radius_two_five_word"], len(radius), 5)

    selected = certificate["selected_radius_two_ids"]
    require(selected == sorted(set(selected)) and all(type(v) is int and 0 <= v < len(radius) for v in selected), "selected IDs")
    selected_edges = subset_edges(radius_edges, selected)
    selected_word = "".join(certificate["radius_two_five_word"][v] for v in selected)
    colour(selected_edges, selected_word, len(selected), 5)
    selected_cnf, selected_triangle = encode_four_colouring(len(selected), selected_edges)
    (args.work / "independent-selected.cnf").write_text(selected_cnf)

    fixed = set(certificate["radius_two_fixed_482"])
    require(len(fixed) == 482 and fixed <= set(range(len(radius))), "482-point base")
    adjacency = [set() for _ in radius]
    for a, b in radius_edges:
        adjacency[a].add(b)
        adjacency[b].add(a)
    pool = sorted(fixed | {v for v in range(len(radius)) if len(adjacency[v] & fixed) >= 2})
    pool_edges = subset_edges(radius_edges, pool)
    colour(pool_edges, certificate["radius_two_two_neighbor_pool_word"], len(pool), 4)

    full = generate_host(False)
    full_edges, full_survivors = strict_edges(full)
    compact_full = [flatten(point) for point in full]
    colour(full_edges, certificate["untruncated_five_word"], len(full), 5)
    require(set(radius) <= set(full), "radius host containment")

    base = certificate["untruncated_fixed_503"]
    require(base == sorted(set(base)) and len(base) == 503, "503-point base")
    require(sorted(certificate["record_map"].values()) == base, "record-map image")
    require(sorted(map(int, certificate["record_map"])) == sorted(set(range(509)) - set(certificate["missing_original_indices"])), "record-map domain")
    control = certificate["subrecord_control"]["vertices"]
    require(control == sorted(set(control)) and set(base) <= set(control) and len(control) == 507, "507-point control")
    control_edges = subset_edges(full_edges, control)
    colour(control_edges, certificate["subrecord_control"]["word"], len(control), 4)

    # Definition-level negative controls.
    require(norm(((96,) + (0,) * 7, ZERO)) == ONE_96, "unit basis control")
    require(norm((ZERO, ZERO)) != ONE_96, "zero is not a unit displacement")
    damaged = list(certificate["radius_two_five_word"])
    a, b = radius_edges[0]
    damaged[a] = damaged[b]
    try:
        colour(radius_edges, "".join(damaged), len(radius), 5)
    except ValueError:
        pass
    else:
        raise ValueError("damaged colour certificate accepted")

    record_result = check_record_overlap(compact_full, certificate) if args.record else None
    result = {
        "status": "INDEPENDENT EXACT CONSTRUCTION CHECK PASSED",
        "target_commit": "c44e047d60d44b60b5878f13a9293ef33aac3bc5",
        "python": f"{sys.version_info.major}.{sys.version_info.minor}",
        "radius_two": {
            "vertices": len(radius),
            "edges": len(radius_edges),
            "sieve_survivors": radius_survivors,
            "points_sha256": digest_json(compact_radius),
            "edges_sha256": digest_json(radius_edges),
        },
        "selected": {
            "vertices": len(selected),
            "edges": len(selected_edges),
            "ids_sha256": digest_json(selected),
            "triangle": list(selected_triangle),
            "cnf_sha256": hashlib.sha256(selected_cnf.encode()).hexdigest(),
            "five_colouring": True,
        },
        "untruncated": {
            "vertices": len(full),
            "edges": len(full_edges),
            "sieve_survivors": full_survivors,
            "points_sha256": digest_json(compact_full),
            "edges_sha256": digest_json(full_edges),
            "five_colouring": True,
        },
        "two_neighbor_pool": {"vertices": len(pool), "edges": len(pool_edges), "four_colourable": True},
        "subrecord_control": {"vertices": len(control), "edges": len(control_edges), "four_colourable": True},
        "record_overlap": record_result,
        "all_pairs_sieved": len(radius) * (len(radius) - 1) // 2 + len(full) * (len(full) - 1) // 2,
        "seconds": time.monotonic() - start,
    }
    if args.check_expected:
        expected = json.loads((HERE / "EXPECTED.json").read_text())
        observed = json.loads(json.dumps(result))
        observed.pop("seconds")
        require(observed == expected, "independent expected output mismatch")
    (args.work / "independent-output.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
