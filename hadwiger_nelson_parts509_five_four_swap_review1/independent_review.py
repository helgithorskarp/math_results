#!/usr/bin/env python3
"""Independent exact audit of the sealed Parts-509 swap-pool witnesses.

This checker imports no code from the package under review.  It reconstructs
the 677 embedded points in K = Q(sqrt(3),sqrt(5),sqrt(11)), enumerates every
unit-distance pair exactly after a sound finite-field rejection screen,
compares the resulting induced graph with the committed ambient edge list,
and checks every advertised four-colouring witness on that complete graph.
"""
from __future__ import annotations

import base64
import hashlib
import json
import time
from collections import Counter
from fractions import Fraction
from pathlib import Path

import numpy as np
import sympy
from sympy import QQ, Rational, sqrt, sympify


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
CRITICAL = ROOT / "hadwiger_nelson_parts509_criticality"
SWAP = ROOT / "hadwiger_nelson_parts509_swap_closure"
PAIR = ROOT / "hadwiger_nelson_parts509_pair_closure"
BUDGET = ROOT / "hadwiger_nelson_parts509_s_replacement_budget"
INTERFACE = ROOT / "hadwiger_nelson_parts509_interface_lemma"
TARGET = ROOT / "hadwiger_nelson_parts509_five_four_swap_search"

RADICALS = [
    sympy.Integer(1), sqrt(3), sqrt(5), sqrt(15),
    sqrt(11), sqrt(33), sqrt(55), sqrt(165),
]


def need(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def split_pair(body: str) -> tuple[str, str]:
    expression = body.replace("Sqrt[", "sqrt(").replace("]", ")")
    depth = 0
    for index, char in enumerate(expression):
        if char == "(":
            depth += 1
        elif char == ")":
            depth -= 1
        elif char == "," and depth == 0:
            return expression[:index], expression[index + 1:]
    raise ValueError("coordinate pair does not split")


def decode_colours(encoded: str, length: int) -> list[int]:
    raw = base64.b64decode(encoded, validate=True)
    need(len(raw) == (length + 3) // 4, "wrong packed-colouring length")
    colours = [(raw[i // 4] >> (2 * (i % 4))) & 3 for i in range(length)]
    if length % 4:
        need(raw[-1] >> (2 * (length % 4)) == 0,
             "nonzero packed-colouring padding")
    return colours


def sqrt_mod(number: int, prime: int) -> int:
    need(pow(number, (prime - 1) // 2, prime) == 1,
         "radicand is not a quadratic residue")
    if prime % 4 == 3:
        root = pow(number, (prime + 1) // 4, prime)
    else:
        odd, exponent = prime - 1, 0
        while odd % 2 == 0:
            odd //= 2
            exponent += 1
        nonresidue = 2
        while pow(nonresidue, (prime - 1) // 2, prime) != prime - 1:
            nonresidue += 1
        m = exponent
        c = pow(nonresidue, odd, prime)
        t = pow(number, odd, prime)
        root = pow(number, (odd + 1) // 2, prime)
        while t != 1:
            i, square = 0, t
            while square != 1:
                square = square * square % prime
                i += 1
            factor = pow(c, 1 << (m - i - 1), prime)
            m, c = i, factor * factor % prime
            t, root = t * c % prime, root * factor % prime
    need(root * root % prime == number % prime, "modular square root failed")
    return root


def screening_primes(count: int) -> list[int]:
    primes = []
    candidate = (1 << 31) - 1
    while len(primes) < count:
        if (sympy.isprime(candidate)
                and all(pow(a, (candidate - 1) // 2, candidate) == 1
                        for a in (3, 5, 11))):
            primes.append(candidate)
        candidate -= 2
    return primes


def main() -> None:
    started = time.time()
    source_paths = {
        "parts509.vtx": CRITICAL / "parts509.vtx",
        "completion_points.json": SWAP / "completion_points.json",
        "ambient_w3_edges.json": PAIR / "ambient_w3_edges.json",
        "pool_S.json": BUDGET / "pool_S.json",
        "interface_L.json": INTERFACE / "interface_L.json",
        "certificate.json": TARGET / "certificate.json",
    }
    for path in source_paths.values():
        need(path.is_file(), f"missing source {path}")

    pool_data = json.loads(source_paths["pool_S.json"].read_text())
    certificate = json.loads(source_paths["certificate.json"].read_text())
    pool = sorted(pool_data["W_S"])
    q5 = sorted(pool_data["Q5"])
    fixed_l = list(range(374))
    labels = sorted(set(fixed_l) | set(pool))
    need(len(pool) == 303 and len(q5) == 168 and len(labels) == 677,
         "unexpected sealed-pool dimensions")
    need(certificate["pool"] == pool and certificate["Q5"] == q5,
         "certificate and sealed pool disagree")
    need(certificate["S"] == list(range(374, 509)),
         "Parts S labels disagree")
    need(set(pool) == set(range(374, 509)) | set(q5),
         "pool is not the disjoint union S union Q5")

    field = QQ.algebraic_field(sqrt(3), sqrt(5), sqrt(11))
    expressions = []
    for line in source_paths["parts509.vtx"].read_text().splitlines():
        if line.strip():
            x_text, y_text = split_pair(line.strip()[1:-1])
            expressions.append((sympify(x_text), sympify(y_text)))
    need(len(expressions) == 509, "wrong number of Parts vertices")
    parts = [
        (field.from_sympy(sympy.sqrtdenest(x)),
         field.from_sympy(sympy.sqrtdenest(y)))
        for x, y in expressions
    ]
    need(len(set(parts)) == 509, "repeated Parts point")

    completions_data = json.loads(
        source_paths["completion_points.json"].read_text())

    def from_coefficients(values: list[str]):
        expression = sum(
            Rational(Fraction(value).numerator, Fraction(value).denominator)
            * radical
            for value, radical in zip(values, RADICALS)
        )
        return field.from_sympy(expression)

    completions = [
        (from_coefficients(row["x"]), from_coefficients(row["y"]))
        for row in completions_data["points"]
    ]
    need(len(completions) == 1158 and len(set(completions)) == 1158,
         "wrong or repeated completion points")
    need(not (set(parts) & set(completions)),
         "completion point duplicates a Parts vertex")

    points = {
        label: (parts[label] if label < 509 else completions[label - 509])
        for label in labels
    }
    need(len(set(points.values())) == 677, "repeated point in sealed pool")

    basis = [field.from_sympy(radical) for radical in RADICALS]

    def power_vector(element) -> list[Fraction]:
        values = [Fraction(int(c.numerator), int(c.denominator))
                  for c in element.to_list()]
        return [Fraction(0)] * (8 - len(values)) + values

    basis_matrix = sympy.Matrix([
        [Rational(c.numerator, c.denominator) for c in power_vector(element)]
        for element in basis
    ]).T
    inverse_basis = basis_matrix.inv()

    def radical_vector(element) -> list[Fraction]:
        vector = inverse_basis * sympy.Matrix([
            Rational(c.numerator, c.denominator)
            for c in power_vector(element)
        ])
        result = [Fraction(int(value.p), int(value.q)) for value in vector]
        rebuilt = sum((field.from_sympy(
            Rational(value.numerator, value.denominator)) * radical
            for value, radical in zip(result, basis)), field.zero)
        need(rebuilt == element, "radical vector does not rebuild coordinate")
        return result

    vectors = [
        (radical_vector(points[label][0]), radical_vector(points[label][1]))
        for label in labels
    ]

    def modular_images(prime: int) -> np.ndarray:
        root3, root5, root11 = (
            sqrt_mod(3, prime), sqrt_mod(5, prime), sqrt_mod(11, prime))
        radical_images = [
            1, root3, root5, root3 * root5 % prime, root11,
            root3 * root11 % prime, root5 * root11 % prime,
            root3 * root5 * root11 % prime,
        ]

        def image(vector: list[Fraction]) -> int:
            total = 0
            for coefficient, radical_image in zip(vector, radical_images):
                need(coefficient.denominator % prime != 0,
                     "screening prime divides a denominator")
                total += (coefficient.numerator
                          * pow(coefficient.denominator, -1, prime)
                          * radical_image)
            return total % prime

        return np.array([[image(x), image(y)] for x, y in vectors],
                        dtype=np.int64)

    candidates = None
    primes = screening_primes(2)
    for prime in primes:
        images = modular_images(prime)
        dx = (images[:, None, 0] - images[None, :, 0]) % prime
        dy = (images[:, None, 1] - images[None, :, 1]) % prime
        squared = (dx * dx % prime + dy * dy % prime) % prime
        current = np.triu(squared == 1, 1)
        candidates = current if candidates is None else candidates & current

    one = field.one

    def is_unit(i: int, j: int) -> bool:
        first, second = points[labels[i]], points[labels[j]]
        dx, dy = first[0] - second[0], first[1] - second[1]
        return dx * dx + dy * dy == one

    exact_edges = []
    rows, columns = np.nonzero(candidates)
    for i, j in zip(rows.tolist(), columns.tolist()):
        if is_unit(i, j):
            exact_edges.append((labels[i], labels[j]))
    exact_edges.sort()

    ambient = json.loads(source_paths["ambient_w3_edges.json"].read_text())
    label_set = set(labels)
    ambient_edges = sorted(
        (a, b) for a, b in ambient["edges"]
        if a in label_set and b in label_set
    )
    need(exact_edges == ambient_edges,
         "exact induced unit graph differs from ambient edge list")
    edge_sha = hashlib.sha256("".join(
        f"{a} {b}\n" for a, b in exact_edges).encode()).hexdigest()

    interface = json.loads(source_paths["interface_L.json"].read_text())
    l_words = [row["witness_colouring_L"] for row in interface["classes"]]
    need(len(l_words) == 20 and all(len(word) == 374 for word in l_words),
         "wrong L-interface witness shape")
    l_edges = [(a, b) for a, b in exact_edges if b < 374]
    need(all(all(word[a] != word[b] for a, b in l_edges)
             for word in l_words), "improper L witness")

    killing_rows = certificate["killing_sets"]
    seen = set()
    provenance = Counter()
    edge_checks = 0
    deletion_sizes = Counter()
    pool_set = set(pool)
    for number, row in enumerate(killing_rows):
        deleted = tuple(row["D"])
        need(deleted and deleted == tuple(sorted(set(deleted))),
             f"invalid killing set at row {number}")
        need(set(deleted) <= pool_set and deleted not in seen,
             f"duplicate or out-of-pool killing set at row {number}")
        seen.add(deleted)
        deletion_sizes[len(deleted)] += 1
        class_index = row["class_index"]
        need(type(class_index) is int and 0 <= class_index < len(l_words),
             f"invalid interface class at row {number}")
        selected = [label for label in pool if label not in set(deleted)]
        packed = decode_colours(row["colouring_U_minus_D_2bit"], len(selected))
        colours = {label: packed[i] for i, label in enumerate(selected)}
        l_word = l_words[class_index]
        for a, b in exact_edges:
            if a < 374 and b < 374:
                continue
            if a < 374:
                if b in colours:
                    edge_checks += 1
                    need(int(l_word[a]) != colours[b],
                         f"monochromatic cross edge in row {number}")
            elif a in colours and b in colours:
                edge_checks += 1
                need(colours[a] != colours[b],
                     f"monochromatic pool edge in row {number}")
        provenance[row["provenance"]] += 1

    need(dict(provenance) == certificate["killing_set_provenance_counts"],
         "killing-set provenance counts differ")
    need(edge_checks == 7_907_307, "unexpected witness edge-check count")

    edge_types = Counter()
    for a, b in exact_edges:
        if b < 374:
            edge_types["L-L"] += 1
        elif a < 374:
            edge_types["L-U"] += 1
        else:
            edge_types["U-U"] += 1

    result = {
        "status": "INDEPENDENT_EXACT_GEOMETRY_AND_WITNESSES_VERIFIED",
        "field": "Q(sqrt(3),sqrt(5),sqrt(11))",
        "embedded_points": len(labels),
        "fixed_L_points": len(fixed_l),
        "pool_points": len(pool),
        "Q5_points": len(q5),
        "screening_primes": primes,
        "screen_candidates": int(candidates.sum()),
        "exact_edges": len(exact_edges),
        "edge_types": dict(edge_types),
        "induced_edge_sha256": edge_sha,
        "interface_classes": len(l_words),
        "killing_sets": len(killing_rows),
        "deletion_size_histogram": {
            str(size): count for size, count in sorted(deletion_sizes.items())
        },
        "witness_edge_checks": edge_checks,
        "source_sha256": {
            name: sha256(path) for name, path in source_paths.items()
        },
        "seconds": round(time.time() - started, 3),
    }
    expected = json.loads((HERE / "GEOMETRY_WITNESS_RESULT.json").read_text())
    need({key: value for key, value in result.items() if key != "seconds"}
         == {key: value for key, value in expected.items() if key != "seconds"},
         "result differs from committed geometry/witness receipt")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    try:
        main()
    except (ValueError, KeyError, TypeError, json.JSONDecodeError) as error:
        print(f"independent review failed: {error}")
        raise SystemExit(1)
