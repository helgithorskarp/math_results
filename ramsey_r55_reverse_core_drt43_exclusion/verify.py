#!/usr/bin/env python3
"""Independent exact checker for the fixed reverse-core DRT43 exclusion."""
from __future__ import annotations

import itertools
import json
import math
import pathlib
import sys

N = 21
PRIME = 1_000_033  # Different from the C++ enumerator's prime.


def is_prime(value: int) -> bool:
    return value >= 2 and all(value % divisor for divisor in range(2, math.isqrt(value) + 1))


def read_core(path: pathlib.Path) -> tuple[list[list[bool]], int]:
    tokens = path.read_text(encoding="ascii").split()
    if len(tokens) < 2:
        raise ValueError("missing header")
    nv, declared = map(int, tokens[:2])
    if (nv, declared) != (21, 98) or (len(tokens) - 2) != 2 * declared:
        raise ValueError("bad header or edge count")
    graph = [[False] * N for _ in range(N)]
    for k in range(declared):
        u, v = map(int, tokens[2 + 2 * k : 4 + 2 * k])
        if not (0 <= u < v < N) or graph[u][v]:
            raise ValueError("malformed or duplicate edge")
        graph[u][v] = graph[v][u] = True
    return graph, declared


def matmul(a: list[list[int]], b: list[list[int]], p: int) -> list[list[int]]:
    return [[sum(a[i][k] * b[k][j] for k in range(N)) % p
             for j in range(N)] for i in range(N)]


def inverse(matrix: list[list[int]], p: int) -> tuple[list[list[int]], int]:
    a = [[x % p for x in row] + [int(i == j) for j in range(N)]
         for i, row in enumerate(matrix)]
    rank = 0
    for column in range(N):
        pivot = next((i for i in range(rank, N) if a[i][column]), None)
        if pivot is None:
            continue
        a[rank], a[pivot] = a[pivot], a[rank]
        scale = pow(a[rank][column], p - 2, p)
        a[rank] = [(x * scale) % p for x in a[rank]]
        for i in range(N):
            if i == rank or not a[i][column]:
                continue
            q = a[i][column]
            a[i] = [(x - q * y) % p for x, y in zip(a[i], a[rank])]
        rank += 1
    if rank != N:
        raise ValueError(f"Krylov rank {rank}, expected {N}")
    return [row[N:] for row in a], rank


def clique_count(graph: list[list[bool]], size: int, color: bool) -> int:
    return sum(all(graph[u][v] == color for u, v in itertools.combinations(s, 2))
               for s in itertools.combinations(range(N), size))


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit("usage: verify.py core.edges")
    if not is_prime(PRIME):
        raise ValueError("configured modulus is not prime")
    graph, edge_count = read_core(pathlib.Path(sys.argv[1]))
    tournament = [[False] * N for _ in range(N)]
    a_int = [[0] * N for _ in range(N)]
    for i in range(N):
        for j in range(N):
            if i == j:
                continue
            tournament[i][j] = graph[i][j] if i < j else not graph[i][j]
            a_int[i][j] = 1 if tournament[i][j] else -1
    outdegrees = [sum(row) for row in tournament]
    if outdegrees != [10] * N:
        raise ValueError("the tournament core is not regular")

    a = [[x % PRIME for x in row] for row in a_int]
    identity = [[int(i == j) for j in range(N)] for i in range(N)]
    powers = [identity]
    for _ in range(1, N):
        powers.append(matmul(powers[-1], a, PRIME))
    krylov = [[powers[k][0][j] for j in range(N)] for k in range(N)]
    inv_k, rank = inverse(krylov, PRIME)

    # A commuting B with first row b obeys K B = [b A^k]_k.
    # Precompute only rows 1..20 because row zero is b itself.
    forms: list[list[int]] = []
    for i in range(1, N):
        for j in range(N):
            forms.append([
                sum(inv_k[i][k] * powers[k][t][j] for k in range(N)) % PRIME
                for t in range(N)
            ])

    tested = 0
    modular_rows: list[tuple[tuple[int, ...], list[list[int]]]] = []
    all_positions = range(N)
    for plus_tuple in itertools.combinations(all_positions, 11):
        tested += 1
        plus = set(plus_tuple)
        rows = [[1 if j in plus else -1 for j in all_positions]]
        flat: list[int] = []
        survives = True
        for coefficients in forms:
            residue = (-sum(coefficients) + 2 * sum(coefficients[j] for j in plus_tuple)) % PRIME
            if residue == 1:
                flat.append(1)
            elif residue == PRIME - 1:
                flat.append(-1)
            else:
                survives = False
                break
        if survives:
            rows.extend([flat[k * N:(k + 1) * N] for k in range(N - 1)])
            modular_rows.append((plus_tuple, rows))

    exact: list[dict[str, object]] = []
    for _, b in modular_rows:
        if any(sum(a_int[i][k] * b[k][j] for k in range(N)) !=
               sum(b[i][k] * a_int[k][j] for k in range(N))
               for i in range(N) for j in range(N)):
            continue
        if [sum(row) for row in b] != [1] * N:
            continue
        if [sum(b[i][j] for i in range(N)) for j in range(N)] != [1] * N:
            continue
        plus_a = all(b[i][j] == (1 if i == j else a_int[i][j])
                     for i in range(N) for j in range(N))
        minus_a = all(b[i][j] == (1 if i == j else -a_int[i][j])
                      for i in range(N) for j in range(N))
        mismatches = 0
        for i in range(N):
            for j in range(N):
                bbt = sum(b[i][k] * b[j][k] for k in range(N))
                aat = sum(a_int[i][k] * a_int[j][k] for k in range(N))
                required = (43 if i == j else 0) - 2 - aat
                mismatches += bbt != required
        exact.append({
            "first_row": "".join("1" if x == 1 else "0" for x in b[0]),
            "kind": "I_plus_A" if plus_a else "I_minus_A" if minus_a else "other",
            "gram_mismatch_ordered_entries": mismatches,
        })

    exact.sort(key=lambda item: str(item["first_row"]))
    result = {
        "status": "INDEPENDENTLY_CHECKED_REVERSE_CORE_DRT43_EXCLUSION",
        "core_vertices": N,
        "core_forward_edges": edge_count,
        "core_tournament_outdegrees": sorted(set(outdegrees)),
        "core_forward_k4": clique_count(graph, 4, True),
        "core_forward_independent5": clique_count(graph, 5, False),
        "prime": PRIME,
        "krylov_rank": rank,
        "first_rows_expected": math.comb(N, 11),
        "first_rows_tested": tested,
        "modular_sign_matrices": len(modular_rows),
        "exact_commuting_sign_matrices": len(exact),
        "candidates": exact,
        "gram_valid_matrices": sum(item["gram_mismatch_ordered_entries"] == 0 for item in exact),
        "target_graph_established": False,
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
