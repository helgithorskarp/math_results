#!/usr/bin/env python3
"""Find a torsion countermodel to the paper's rational row-span test.

This is exploratory/production code using only exact arithmetic.  It follows
the tree transition in the Zenodo ``treeSearch.py`` source and stops at the
first node which NumPy's intended characteristic-zero rank test would prune,
but whose accumulated relations admit pairwise distinct nonzero labels in an
elementary abelian p-group.
"""

from __future__ import annotations

import argparse
from collections import deque
from fractions import Fraction
from itertools import combinations
from typing import Iterable, Sequence


Vector = tuple[int, ...]


def rref_q(rows: Sequence[Vector]) -> tuple[list[list[Fraction]], list[int]]:
    """Return reduced rows and pivot columns over Q."""
    if not rows:
        return [], []
    matrix = [[Fraction(x) for x in row] for row in rows]
    width = len(matrix[0])
    rank = 0
    pivot_cols: list[int] = []
    for col in range(width):
        pivot = next((r for r in range(rank, len(matrix)) if matrix[r][col]), None)
        if pivot is None:
            continue
        matrix[rank], matrix[pivot] = matrix[pivot], matrix[rank]
        scale = matrix[rank][col]
        matrix[rank] = [x / scale for x in matrix[rank]]
        for r in range(len(matrix)):
            if r != rank and matrix[r][col]:
                scale = matrix[r][col]
                matrix[r] = [x - scale * y for x, y in zip(matrix[r], matrix[rank])]
        pivot_cols.append(col)
        rank += 1
    return matrix[:rank], pivot_cols


def rref_mod_p(rows: Sequence[Vector], prime: int) -> tuple[list[list[int]], list[int]]:
    """Return reduced rows and pivot columns over F_p."""
    if not rows:
        return [], []
    matrix = [[x % prime for x in row] for row in rows]
    width = len(matrix[0])
    rank = 0
    pivot_cols: list[int] = []
    for col in range(width):
        pivot = next((r for r in range(rank, len(matrix)) if matrix[r][col]), None)
        if pivot is None:
            continue
        matrix[rank], matrix[pivot] = matrix[pivot], matrix[rank]
        inv = pow(matrix[rank][col], -1, prime)
        matrix[rank] = [(x * inv) % prime for x in matrix[rank]]
        for r in range(len(matrix)):
            if r != rank and matrix[r][col]:
                scale = matrix[r][col]
                matrix[r] = [(x - scale * y) % prime for x, y in zip(matrix[r], matrix[rank])]
        pivot_cols.append(col)
        rank += 1
    return matrix[:rank], pivot_cols


def characteristic_zero_rank(rows: Sequence[Vector]) -> int:
    return len(rref_q(rows)[1])


def rank_mod_p(rows: Sequence[Vector], prime: int) -> int:
    return len(rref_mod_p(rows, prime)[1])


def in_rref_q(rows: Sequence[Sequence[Fraction]], pivots: Sequence[int], vector: Vector) -> bool:
    remainder = [Fraction(x) for x in vector]
    for row, pivot in zip(rows, pivots):
        scale = remainder[pivot]
        if scale:
            remainder = [x - scale * y for x, y in zip(remainder, row)]
    return not any(remainder)


def in_rref_mod_p(
    rows: Sequence[Sequence[int]], pivots: Sequence[int], vector: Vector, prime: int
) -> bool:
    remainder = [x % prime for x in vector]
    for row, pivot in zip(rows, pivots):
        scale = remainder[pivot]
        if scale:
            remainder = [(x - scale * y) % prime for x, y in zip(remainder, row)]
    return not any(remainder)


def in_span_q(rows: Sequence[Vector], vector: Vector) -> bool:
    reduced, pivots = rref_q(rows)
    return in_rref_q(reduced, pivots, vector)


def in_span_mod_p(rows: Sequence[Vector], vector: Vector, prime: int) -> bool:
    reduced, pivots = rref_mod_p(rows, prime)
    return in_rref_mod_p(reduced, pivots, vector, prime)


def standard_targets(n: int) -> list[Vector]:
    targets: list[Vector] = []
    for i in range(n):
        targets.append(tuple(int(j == i) for j in range(n)))
    for i, j in combinations(range(n), 2):
        targets.append(tuple(int(k == i) - int(k == j) for k in range(n)))
    return targets


def compression_targets(n: int, mode: str) -> list[Vector]:
    """Reproduce the two ``initial_cons`` generators in the archived code."""
    if mode == "none":
        return []
    targets: list[Vector] = []
    for length in range(2, n):
        for start in range(n - length + 1):
            vector = tuple(
                int(start <= position < start + length) for position in range(n)
            )
            if mode == "zero" and vector[-2] == vector[-1]:
                targets.append(vector)
            elif mode == "nonzero" and vector[-1] == 0:
                targets.append(vector)
    return targets


def nullspace_mod_p(rows: Sequence[Vector], prime: int) -> list[Vector]:
    """Return a deterministic row basis of {x: Cx=0} over F_p."""
    if not rows:
        n = 0
        return []
    n = len(rows[0])
    matrix, pivot_cols = rref_mod_p(rows, prime)
    return nullspace_from_rref_mod_p(matrix, pivot_cols, n, prime)


def nullspace_from_rref_mod_p(
    matrix: Sequence[Sequence[int]],
    pivot_cols: Sequence[int],
    n: int,
    prime: int,
) -> list[Vector]:
    free_cols = [col for col in range(n) if col not in pivot_cols]
    basis: list[Vector] = []
    for free in free_cols:
        vector = [0] * n
        vector[free] = 1
        for r, pivot_col in enumerate(pivot_cols):
            vector[pivot_col] = (-matrix[r][free]) % prime
        basis.append(tuple(vector))
    return basis


def column_labels(nullspace_basis: Sequence[Vector]) -> list[Vector]:
    n = len(nullspace_basis[0])
    return [tuple(row[i] for row in nullspace_basis) for i in range(n)]


def terminal_targets_from_labels(
    labels: Sequence[Vector], compression: Sequence[Vector], prime: int
) -> list[Vector]:
    """Return all standard/compression targets annihilating the nullspace."""
    n = len(labels)
    dimension = len(labels[0]) if labels else 0
    zero = (0,) * dimension
    targets: list[Vector] = []
    for i, label in enumerate(labels):
        if label == zero:
            targets.append(tuple(int(j == i) for j in range(n)))
    for i, j in combinations(range(n), 2):
        if labels[i] == labels[j]:
            targets.append(tuple(int(k == i) - int(k == j) for k in range(n)))
    for target in compression:
        value = tuple(
            sum(target[i] * labels[i][coordinate] for i in range(n)) % prime
            for coordinate in range(dimension)
        )
        if value == zero:
            targets.append(target)
    return targets


def children(ordering: Vector, constraints: tuple[Vector, ...]) -> Iterable[tuple[Vector, tuple[Vector, ...], tuple[int, int]]]:
    """Reproduce SearchNode.generate_children from the archived source."""
    n = len(ordering)
    for i in range(n - 1):
        for j in range(i + 1, n):
            if j - i > n // 2:
                continue
            row = [0] * n
            for k in range(i, j + 1):
                row[ordering[k] - 1] = 1
            row_tuple = tuple(row)
            if row_tuple in constraints:
                continue
            new_order = list(ordering)
            if i >= 1:
                new_order[i], new_order[i - 1] = new_order[i - 1], new_order[i]
            else:
                new_order[j], new_order[j + 1] = new_order[j + 1], new_order[j]
            yield tuple(new_order), (*constraints, row_tuple), (i, j)


def find_countermodel(
    n: int,
    max_nodes: int,
    primes: Sequence[int],
    mode: str,
    strategy: str,
) -> dict[str, object]:
    standard = standard_targets(n)
    compression = compression_targets(n, mode)
    targets = standard + compression
    root = (tuple(range(1, n + 1)), tuple(), tuple())
    queue = deque([root])
    explored = 0
    while queue:
        ordering, constraints, path = queue.popleft() if strategy == "bfs" else queue.pop()
        explored += 1
        if explored > max_nodes:
            raise RuntimeError(f"node cap reached: {max_nodes}")
        # Exact characteristic-zero screening.  Every square minor has rows of
        # Euclidean norm at most sqrt(n), hence absolute determinant at most
        # n^(n/2) by Hadamard.  The prime is larger than this bound for n <= 25,
        # so reduction modulo it preserves every relevant rank exactly.
        screen_prime = 2_305_843_009_213_693_951  # 2^61 - 1, prime
        if n**n >= screen_prime**2:
            raise ValueError("exact modular Q-rank screen is certified only for n <= 25")
        screen_rows, screen_pivots = rref_mod_p(constraints, screen_prime)
        screen_basis = nullspace_from_rref_mod_p(
            screen_rows, screen_pivots, n, screen_prime
        )
        screen_labels = column_labels(screen_basis) if screen_basis else [()] * n
        rational_targets = terminal_targets_from_labels(
            screen_labels, compression, screen_prime
        )
        if rational_targets:
            for prime in primes:
                basis = nullspace_mod_p(constraints, prime)
                labels = column_labels(basis) if basis else []
                zero = (0,) * len(basis)
                labels_are_a_set = (
                    len(labels) == n
                    and zero not in labels
                    and len(set(labels)) == n
                )
                compression_is_nonzero = labels_are_a_set and all(
                    any(
                        sum(target[i] * labels[i][coordinate] for i in range(n))
                        % prime
                        for coordinate in range(len(basis))
                    )
                    for target in compression
                )
                if compression_is_nonzero:
                    assert all(any(x for x in label) for label in labels)
                    assert len(set(labels)) == n
                    assert all(
                        all(sum(c * x for c, x in zip(row, basis_coordinate)) % prime == 0 for basis_coordinate in basis)
                        for row in constraints
                    )
                    return {
                        "n": n,
                        "mode": mode,
                        "explored_nodes": explored,
                        "path": path,
                        "ordering": ordering,
                        "constraints": constraints,
                        "prime": prime,
                        "nullspace_basis": basis,
                        "labels": labels,
                        "rational_targets": rational_targets,
                    }
            continue
        for new_order, new_constraints, interval in children(ordering, constraints):
            queue.append((new_order, new_constraints, (*path, interval)))
    raise RuntimeError("tree exhausted without a false-positive certificate")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--n", type=int, default=6)
    parser.add_argument("--max-nodes", type=int, default=1_000_000)
    parser.add_argument("--mode", choices=("none", "zero", "nonzero"), default="none")
    parser.add_argument("--strategy", choices=("bfs", "dfs"), default="bfs")
    parser.add_argument(
        "--primes",
        default="2,3,5,7,11,13,17,19,23,29,31,37,41,43,47,53,59,61,67,71,73,79,83,89,97",
        help="comma-separated prime characteristics in which to seek a countermodel",
    )
    args = parser.parse_args()
    primes = tuple(int(value) for value in args.primes.split(","))
    result = find_countermodel(
        args.n,
        args.max_nodes,
        primes,
        args.mode,
        args.strategy,
    )
    for key, value in result.items():
        print(f"{key}={value}")


if __name__ == "__main__":
    main()
