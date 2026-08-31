#!/usr/bin/env python3
"""Verify and classify minimum locating-dominating codes in Q_6.

The direct checker uses only the Python standard library.  The exhaustive
classification additionally uses python-sat (PySAT).
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import math
import time
from collections import Counter


DIMENSION = 6
VERTEX_COUNT = 1 << DIMENSION
OPTIMUM_SIZE = 16

# The construction independently checked in the sibling contribution
# q6_locating_dominating_16, in integer/lexicographic binary notation.
REFERENCE_CODE = frozenset(
    {
        0,
        5,
        11,
        14,
        18,
        23,
        25,
        28,
        34,
        36,
        41,
        47,
        51,
        53,
        56,
        62,
    }
)
CANONICAL_CODE = (
    0,
    3,
    5,
    10,
    20,
    27,
    29,
    30,
    38,
    41,
    44,
    47,
    49,
    50,
    55,
    56,
)


def closed_neighborhood(vertex: int) -> frozenset[int]:
    """Return the radius-one closed neighborhood of ``vertex`` in Q_6."""
    return frozenset(
        {vertex, *(vertex ^ (1 << coordinate) for coordinate in range(DIMENSION))}
    )


NEIGHBORHOODS = tuple(closed_neighborhood(vertex) for vertex in range(VERTEX_COUNT))


def verify_locating_dominating(code: frozenset[int]) -> Counter[int]:
    """Directly check domination and distinct non-codeword signatures."""
    assert len(code) == OPTIMUM_SIZE
    signatures: dict[frozenset[int], int] = {}
    distribution: Counter[int] = Counter()
    for vertex in range(VERTEX_COUNT):
        if vertex in code:
            continue
        signature = frozenset(code & NEIGHBORHOODS[vertex])
        assert signature, f"undominated vertex {vertex:06b}"
        assert signature not in signatures, (
            f"equal signatures at {signatures.get(signature):06b} and {vertex:06b}"
        )
        signatures[signature] = vertex
        distribution[len(signature)] += 1
    assert len(signatures) == VERTEX_COUNT - OPTIMUM_SIZE
    return distribution


def pair_distance_distribution(code: frozenset[int]) -> Counter[int]:
    """Count unordered codeword pairs by Hamming distance."""
    return Counter(
        (first ^ second).bit_count()
        for first, second in itertools.combinations(sorted(code), 2)
    )


def permute_word(word: int, permutation: tuple[int, ...]) -> int:
    """Apply a permutation of the six coordinate positions."""
    image = 0
    for source, destination in enumerate(permutation):
        image |= ((word >> source) & 1) << destination
    return image


def automorphism_orbit(code: frozenset[int]) -> set[tuple[int, ...]]:
    """Return the orbit under all translations and coordinate permutations."""
    images: set[tuple[int, ...]] = set()
    for permutation in itertools.permutations(range(DIMENSION)):
        permuted = tuple(permute_word(word, permutation) for word in code)
        for translation in range(VERTEX_COUNT):
            images.add(tuple(sorted(word ^ translation for word in permuted)))
    return images


def build_classification_cnf(reference_orbit: set[tuple[int, ...]]):
    """Build the exact-size-16 CNF after blocking the known orbit.

    Variable ``vertex + 1`` says that ``vertex`` is a codeword.  The first
    family of clauses enforces domination.  For u < v, the second family is

        x_u OR x_v OR OR_{w in N[u] symmetric_difference N[v]} x_w.

    If u and v are both non-codewords, it says precisely that their signatures
    differ.  If either is a codeword, the clause is inactive.  We normalize by
    requiring vertex zero to be a codeword; vertex transitivity makes this
    lossless for every nonempty code.
    """
    from pysat.card import CardEnc, EncType
    from pysat.formula import CNF

    cnf = CNF()
    for vertex in range(VERTEX_COUNT):
        cnf.append([word + 1 for word in sorted(NEIGHBORHOODS[vertex])])

    for first in range(VERTEX_COUNT):
        for second in range(first + 1, VERTEX_COUNT):
            witnesses = sorted(NEIGHBORHOODS[first] ^ NEIGHBORHOODS[second])
            cnf.append([first + 1, second + 1, *(word + 1 for word in witnesses)])

    cardinality = CardEnc.equals(
        lits=list(range(1, VERTEX_COUNT + 1)),
        bound=OPTIMUM_SIZE,
        top_id=cnf.nv,
        encoding=EncType.totalizer,
    )
    cnf.extend(cardinality.clauses)
    cnf.append([1])

    normalized_images = sorted(image for image in reference_orbit if 0 in image)
    for image in normalized_images:
        # Exact cardinality 16 makes this clause block exactly this image.
        cnf.append([-(vertex + 1) for vertex in image])
    return cnf, normalized_images


def dimacs_bytes(cnf) -> bytes:
    """Return a deterministic DIMACS serialization for hashing/reproduction."""
    lines = [f"p cnf {cnf.nv} {len(cnf.clauses)}"]
    lines.extend(" ".join(map(str, clause)) + " 0" for clause in cnf.clauses)
    return ("\n".join(lines) + "\n").encode("ascii")


def classify(solvers: list[str], cnf_output: str | None) -> None:
    """Prove by exhaustive SAT search that no second orbit exists."""
    import pysat
    from pysat.solvers import Solver

    distribution = verify_locating_dominating(REFERENCE_CODE)
    distances = pair_distance_distribution(REFERENCE_CODE)
    assert distances == Counter({2: 32, 3: 48, 4: 24, 5: 16})
    orbit = automorphism_orbit(REFERENCE_CODE)
    assert min(orbit) == CANONICAL_CODE
    group_order = VERTEX_COUNT * math.factorial(DIMENSION)
    assert group_order % len(orbit) == 0
    stabilizer_order = group_order // len(orbit)
    cnf, normalized_images = build_classification_cnf(orbit)
    payload = dimacs_bytes(cnf)
    digest = hashlib.sha256(payload).hexdigest()

    if cnf_output is not None:
        with open(cnf_output, "wb") as output:
            output.write(payload)

    print(f"PySAT version: {pysat.__version__}")
    print(f"reference code size: {len(REFERENCE_CODE)}")
    print(
        "signature-size distribution: "
        + " ".join(f"{size}:{distribution[size]}" for size in sorted(distribution))
    )
    print(
        "unordered pair-distance distribution: "
        + " ".join(f"{distance}:{distances[distance]}" for distance in sorted(distances))
    )
    print(f"automorphism group order: {group_order}")
    print(f"reference orbit size: {len(orbit)}")
    print(f"reference stabilizer order: {stabilizer_order}")
    print(f"orbit images containing 000000: {len(normalized_images)}")
    print(f"classification CNF: {cnf.nv} variables, {len(cnf.clauses)} clauses")
    print(f"classification CNF SHA-256: {digest}")

    blocker_count = len(normalized_images)
    base_clauses = cnf.clauses[:-blocker_count]
    blocker_clauses = cnf.clauses[-blocker_count:]
    for solver_name in solvers:
        started = time.monotonic()
        with Solver(name=solver_name, bootstrap_with=base_clauses) as solver:
            assert solver.solve(), f"{solver_name} rejected the unblocked base CNF"
            positive = {literal for literal in solver.get_model() if literal > 0}
            candidate = tuple(
                vertex for vertex in range(VERTEX_COUNT) if vertex + 1 in positive
            )
            assert candidate in orbit, (
                f"{solver_name} found a size-16 code outside the reference orbit "
                "before orbit blocking"
            )
            warmup_elapsed = time.monotonic() - started
            for clause in blocker_clauses:
                solver.add_clause(clause)
            residual_started = time.monotonic()
            satisfiable = solver.solve()
            residual_elapsed = time.monotonic() - residual_started
        print(
            f"{solver_name}: base SAT in {warmup_elapsed:.3f} seconds; "
            f"orbit-blocked residual {'SAT' if satisfiable else 'UNSAT'} in "
            f"{residual_elapsed:.3f} seconds"
        )
        assert not satisfiable, f"{solver_name} found a second orbit"

    print("classified: exactly one optimum Q_6 code up to automorphism")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--classify",
        action="store_true",
        help="run the exhaustive PySAT classification",
    )
    parser.add_argument(
        "--solvers",
        nargs="+",
        default=["cadical195", "glucose42"],
        help="PySAT solver backends used for independent UNSAT runs",
    )
    parser.add_argument(
        "--write-cnf",
        metavar="PATH",
        help="write the deterministic classification CNF (use a scratch path)",
    )
    args = parser.parse_args()

    distribution = verify_locating_dominating(REFERENCE_CODE)
    distances = pair_distance_distribution(REFERENCE_CODE)
    assert distances == Counter({2: 32, 3: 48, 4: 24, 5: 16})
    print(f"direct verification passed for {len(REFERENCE_CODE)} codewords")
    print(
        "signature-size distribution: "
        + " ".join(f"{size}:{distribution[size]}" for size in sorted(distribution))
    )
    print(
        "unordered pair-distance distribution: "
        + " ".join(f"{distance}:{distances[distance]}" for distance in sorted(distances))
    )
    if args.classify:
        classify(args.solvers, args.write_cnf)


if __name__ == "__main__":
    main()
