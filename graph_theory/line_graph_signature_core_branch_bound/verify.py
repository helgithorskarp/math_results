#!/usr/bin/env python3
"""Exact audit for the core-branch line-graph signature theorem.

The universal proof is in THEOREM.md.  This program checks its finite
interfaces using only standard-library exact rational arithmetic.
"""

from __future__ import annotations

import hashlib
import itertools
import json
from collections import Counter, defaultdict
from fractions import Fraction
from functools import lru_cache
from typing import Iterable, Sequence

Matrix = list[list[int | Fraction]]
Edge = tuple[int, int]
RootedForm = tuple["RootedForm", ...]


def inertia(matrix: Sequence[Sequence[int | Fraction]]) -> tuple[int, int, int]:
    """Exact inertia by symmetric congruence with 1x1/2x2 pivots."""
    a = [[Fraction(x) for x in row] for row in matrix]
    assert all(len(row) == len(a) for row in a)
    assert all(a[i][j] == a[j][i] for i in range(len(a)) for j in range(len(a)))
    pos = neg = zero = 0
    while a:
        n = len(a)
        pivot = next((i for i in range(n) if a[i][i] != 0), None)
        if pivot is not None:
            if pivot != 0:
                a[0], a[pivot] = a[pivot], a[0]
                for row in a:
                    row[0], row[pivot] = row[pivot], row[0]
            d = a[0][0]
            pos += int(d > 0)
            neg += int(d < 0)
            a = [
                [a[i][j] - a[i][0] * a[0][j] / d for j in range(1, n)]
                for i in range(1, n)
            ]
            continue

        off = next(
            ((i, j) for i in range(n) for j in range(i + 1, n) if a[i][j] != 0),
            None,
        )
        if off is None:
            zero += n
            break
        i, j = off
        order = [i, j] + [k for k in range(n) if k not in (i, j)]
        a = [[a[u][v] for v in order] for u in order]
        d = a[0][1]
        pos += 1
        neg += 1
        a = [
            [a[u][v] - (a[u][0] * a[1][v] + a[u][1] * a[0][v]) / d
             for v in range(2, n)]
            for u in range(2, n)
        ]
    return pos, zero, neg


def signature(matrix: Sequence[Sequence[int | Fraction]]) -> int:
    pos, _, neg = inertia(matrix)
    return pos - neg


def graph6_decode(code: str) -> tuple[int, tuple[Edge, ...]]:
    """Decode the small-n graph6 form used by both sharp witnesses."""
    values = [ord(char) - 63 for char in code.strip()]
    assert values and 0 <= values[0] <= 62
    n = values[0]
    bits = [bit for value in values[1:] for bit in ((value >> k) & 1 for k in range(5, -1, -1))]
    edges: list[Edge] = []
    cursor = 0
    for v in range(1, n):
        for u in range(v):
            if bits[cursor]:
                edges.append((u, v))
            cursor += 1
    return n, tuple(edges)


def adjacency(n: int, edges: Iterable[Edge]) -> list[set[int]]:
    adj = [set() for _ in range(n)]
    for u, v in edges:
        assert 0 <= u < v < n and v not in adj[u]
        adj[u].add(v)
        adj[v].add(u)
    return adj


def is_connected(adj: Sequence[set[int]]) -> bool:
    if not adj:
        return False
    seen = {0}
    stack = [0]
    while stack:
        v = stack.pop()
        for w in adj[v] - seen:
            seen.add(w)
            stack.append(w)
    return len(seen) == len(adj)


def two_core(adj: Sequence[set[int]]) -> frozenset[int]:
    active = set(range(len(adj)))
    degree = [len(neighbors) for neighbors in adj]
    stack = [v for v, d in enumerate(degree) if d < 2]
    while stack:
        v = stack.pop()
        if v not in active:
            continue
        active.remove(v)
        for w in adj[v]:
            if w in active:
                degree[w] -= 1
                if degree[w] == 1:
                    stack.append(w)
    return frozenset(active)


def shifted_signless(adj: Sequence[set[int]], vertices: Sequence[int] | None = None) -> Matrix:
    if vertices is None:
        vertices = tuple(range(len(adj)))
    vertices = tuple(vertices)
    matrix: Matrix = [[0 for _ in vertices] for _ in vertices]
    for i, u in enumerate(vertices):
        matrix[i][i] = len(adj[u]) - 2
        for j, v in enumerate(vertices[:i]):
            if v in adj[u]:
                matrix[i][j] = matrix[j][i] = 1
    return matrix


def core_shifted(adj: Sequence[set[int]], core: frozenset[int], subset: Iterable[int]) -> Matrix:
    vertices = tuple(sorted(subset))
    matrix: Matrix = [[0 for _ in vertices] for _ in vertices]
    core_degree = {u: len(adj[u] & core) for u in core}
    for i, u in enumerate(vertices):
        matrix[i][i] = core_degree[u] - 2
        for j, v in enumerate(vertices[:i]):
            if v in adj[u]:
                matrix[i][j] = matrix[j][i] = 1
    return matrix


def line_adjacency(n: int, edges: Sequence[Edge]) -> Matrix:
    del n
    matrix: Matrix = [[0 for _ in edges] for _ in edges]
    for i, edge in enumerate(edges):
        for j, other in enumerate(edges[:i]):
            if set(edge) & set(other):
                matrix[i][j] = matrix[j][i] = 1
    return matrix


def graph_properties(n: int, edges: Sequence[Edge]) -> dict[str, int | tuple[int, int, int]]:
    adj = adjacency(n, edges)
    assert is_connected(adj)
    core = two_core(adj)
    c = len(edges) - n + 1
    branch = sum(len(adj[v] & core) >= 3 for v in core)
    m_inertia = inertia(shifted_signless(adj))
    line_inertia = inertia(line_adjacency(n, edges))
    m_sig = m_inertia[0] - m_inertia[2]
    line_sig = line_inertia[0] - line_inertia[2]
    assert line_sig == m_sig - c + 1
    return {
        "n": n,
        "m": len(edges),
        "c": c,
        "b": branch,
        "m_inertia": m_inertia,
        "line_inertia": line_inertia,
        "line_signature": line_sig,
    }


def all_edges(n: int) -> tuple[Edge, ...]:
    return tuple((u, v) for v in range(1, n) for u in range(v))


def audit_graphs(max_n: int = 6, principal_max_n: int = 5) -> dict[str, object]:
    connected = relevant = equality = principal = 0
    by_c: Counter[int] = Counter()
    max_slack: dict[int, int] = defaultdict(lambda: -10**9)
    for n in range(1, max_n + 1):
        possible = all_edges(n)
        for mask in range(1 << len(possible)):
            edges = tuple(edge for i, edge in enumerate(possible) if (mask >> i) & 1)
            adj = adjacency(n, edges)
            if not is_connected(adj):
                continue
            connected += 1
            c = len(edges) - n + 1
            if c < 2:
                continue
            relevant += 1
            core = two_core(adj)
            branch_set = {v for v in core if len(adj[v] & core) >= 3}
            b = len(branch_set)
            m_sig = signature(shifted_signless(adj))
            line_sig = signature(line_adjacency(n, edges))
            assert line_sig == m_sig - c + 1
            assert m_sig <= b
            assert line_sig <= b - c + 1 <= c - 1
            equality += int(line_sig == b - c + 1)
            by_c[c] += 1
            max_slack[c] = max(max_slack[c], line_sig - (b - c + 1))

            if n <= principal_max_n:
                vertices = tuple(sorted(core))
                for subset_mask in range(1 << len(vertices)):
                    subset = tuple(v for i, v in enumerate(vertices) if (subset_mask >> i) & 1)
                    lhs = signature(core_shifted(adj, core, subset))
                    rhs = len(set(subset) & branch_set)
                    assert lhs <= rhs
                    principal += 1
    return {
        "max_n": max_n,
        "connected": connected,
        "c_ge_2": relevant,
        "branch_bound_equalities": equality,
        "principal_checks": principal,
        "counts_by_c": dict(sorted(by_c.items())),
        "max_signed_slack_by_c": dict(sorted(max_slack.items())),
    }


def integer_partitions(total: int, minimum: int = 1) -> Iterable[tuple[int, ...]]:
    if total == 0:
        yield ()
        return
    for first in range(minimum, total + 1):
        for rest in integer_partitions(total - first, first):
            yield (first,) + rest


def rooted_forms(max_n: int) -> dict[int, tuple[RootedForm, ...]]:
    forms: dict[int, tuple[RootedForm, ...]] = {1: ((),)}
    for n in range(2, max_n + 1):
        generated: list[RootedForm] = []
        for partition in integer_partitions(n - 1):
            counts = Counter(partition)
            choices = [
                tuple(itertools.combinations_with_replacement(forms[size], count))
                for size, count in sorted(counts.items())
            ]
            for selected in itertools.product(*choices):
                generated.append(tuple(sorted(itertools.chain.from_iterable(selected))))
        forms[n] = tuple(sorted(generated))
        assert len(forms[n]) == len(set(forms[n]))
    return forms


@lru_cache(maxsize=None)
def rooted_state(form: RootedForm) -> tuple[int, Fraction]:
    states = [rooted_state(child) for child in form]
    a = Fraction(len(form) - 1) - sum((rho for _, rho in states), Fraction(0))
    assert a != 0
    sigma = sum(value for value, _ in states) + (1 if a > 0 else -1)
    return sigma, 1 / a


def rooted_matrix(form: RootedForm) -> Matrix:
    """Construct C_T directly, with the root at coordinate zero."""
    edges: list[Edge] = []
    next_vertex = 1

    def add_children(parent: int, children: RootedForm) -> None:
        nonlocal next_vertex
        for child in children:
            vertex = next_vertex
            next_vertex += 1
            edges.append((min(parent, vertex), max(parent, vertex)))
            add_children(vertex, child)

    add_children(0, form)
    adj = adjacency(next_vertex, edges)
    matrix = shifted_signless(adj)
    matrix[0][0] += 1
    return matrix


def inverse_entry_00(matrix: Sequence[Sequence[int | Fraction]]) -> Fraction:
    """Return the (0,0) entry of an exact inverse by Gauss-Jordan elimination."""
    n = len(matrix)
    augmented = [
        [Fraction(x) for x in row] + [Fraction(int(i == j)) for j in range(n)]
        for i, row in enumerate(matrix)
    ]
    for column in range(n):
        pivot = next(row for row in range(column, n) if augmented[row][column] != 0)
        augmented[column], augmented[pivot] = augmented[pivot], augmented[column]
        value = augmented[column][column]
        augmented[column] = [x / value for x in augmented[column]]
        for row in range(n):
            if row == column or augmented[row][column] == 0:
                continue
            multiple = augmented[row][column]
            augmented[row] = [
                x - multiple * y for x, y in zip(augmented[row], augmented[column])
            ]
    return augmented[0][n]


def audit_rooted_trees(max_n: int = 12) -> dict[str, object]:
    forms = rooted_forms(max_n)
    zero_states = negative_response_minus_one = direct_checks = 0
    digest_rows: list[tuple[int, str, int, int, int]] = []
    for n in range(1, max_n + 1):
        for form in forms[n]:
            sigma, rho = rooted_state(form)
            assert rho.numerator % 2 and rho.denominator % 2
            assert sigma <= 0
            if sigma == 0:
                zero_states += 1
                assert rho == 1
            if sigma == -1 and rho < 0:
                negative_response_minus_one += 1
                assert rho == -1
            if n <= 9:
                matrix = rooted_matrix(form)
                assert signature(matrix) == sigma
                assert inverse_entry_00(matrix) == rho
                direct_checks += 1
            digest_rows.append((n, repr(form), sigma, rho.numerator, rho.denominator))
    digest = hashlib.sha256(json.dumps(digest_rows, separators=(",", ":")).encode()).hexdigest()
    return {
        "max_n": max_n,
        "counts": [len(forms[n]) for n in range(1, max_n + 1)],
        "total": sum(len(forms[n]) for n in range(1, max_n + 1)),
        "zero_states": zero_states,
        "negative_response_minus_one": negative_response_minus_one,
        "direct_matrix_checks": direct_checks,
        "state_digest": digest,
    }


def audit_witnesses() -> dict[str, object]:
    expected = {
        "c2": ("Jl?GGCHa??_", 2, 1, 2),
        "c3": ("Ml_GGCHO??_@?@?C_", 3, 2, 4),
    }
    result: dict[str, object] = {}
    for name, (code, c, line_sig, branch) in expected.items():
        n, edges = graph6_decode(code)
        props = graph_properties(n, edges)
        assert props["c"] == c
        assert props["line_signature"] == line_sig
        assert props["b"] == branch
        assert line_sig == branch - c + 1
        result[name] = {"graph6": code, **props}
    return result


def main() -> None:
    rooted = audit_rooted_trees()
    graphs = audit_graphs()
    witnesses = audit_witnesses()
    result = {"rooted_trees": rooted, "graphs": graphs, "witnesses": witnesses}
    certificate = hashlib.sha256(
        json.dumps(result, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()
    print("rooted_tree_counts=" + ",".join(map(str, rooted["counts"])))
    print(
        f"rooted_tree_total={rooted['total']} zero_states={rooted['zero_states']} "
        f"direct_matrix_checks={rooted['direct_matrix_checks']}"
    )
    print(
        f"connected_graphs={graphs['connected']} c_ge_2={graphs['c_ge_2']} "
        f"principal_checks={graphs['principal_checks']}"
    )
    print(f"branch_bound_equalities={graphs['branch_bound_equalities']}")
    for name, props in witnesses.items():
        print(
            f"{name}: n={props['n']} m={props['m']} c={props['c']} b={props['b']} "
            f"line_inertia={props['line_inertia']} signature={props['line_signature']}"
        )
    print(f"certificate_sha256={certificate}")
    print("VERIFIED")


if __name__ == "__main__":
    main()
