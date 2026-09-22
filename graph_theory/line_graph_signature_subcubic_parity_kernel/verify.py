#!/usr/bin/env python3
"""Exact audit of the parity-kernel reduction for subcubic 2-cores.

Only standard-library exact arithmetic is used.  The universal result is the
proof in THEOREM.md; this program audits extraction, the reduced matrices,
their inertia, the signed-component rank formula, and modulo-four stability.
"""

from __future__ import annotations

import hashlib
import itertools
import json
from fractions import Fraction
from typing import Iterable, Sequence

Edge = tuple[int, int]
Path = tuple[int, int, int]
Matrix = list[list[int | Fraction]]


def inertia(matrix: Sequence[Sequence[int | Fraction]]) -> tuple[int, int, int]:
    """Exact symmetric inertia by congruence using 1x1 and 2x2 pivots."""
    a = [[Fraction(x) for x in row] for row in matrix]
    if any(len(row) != len(a) for row in a):
        raise ValueError("matrix must be square")
    if any(a[i][j] != a[j][i] for i in range(len(a)) for j in range(len(a))):
        raise ValueError("matrix must be symmetric")
    positive = negative = zero = 0
    while a:
        n = len(a)
        pivot = next((i for i in range(n) if a[i][i] != 0), None)
        if pivot is not None:
            if pivot:
                a[0], a[pivot] = a[pivot], a[0]
                for row in a:
                    row[0], row[pivot] = row[pivot], row[0]
            value = a[0][0]
            positive += int(value > 0)
            negative += int(value < 0)
            a = [
                [a[i][j] - a[i][0] * a[0][j] / value for j in range(1, n)]
                for i in range(1, n)
            ]
            continue
        off_diagonal = next(
            ((i, j) for i in range(n) for j in range(i + 1, n) if a[i][j] != 0),
            None,
        )
        if off_diagonal is None:
            zero += n
            break
        i, j = off_diagonal
        order = [i, j] + [k for k in range(n) if k not in (i, j)]
        a = [[a[u][v] for v in order] for u in order]
        value = a[0][1]
        positive += 1
        negative += 1
        a = [
            [
                a[u][v]
                - (a[u][0] * a[1][v] + a[u][1] * a[0][v]) / value
                for v in range(2, n)
            ]
            for u in range(2, n)
        ]
    return positive, zero, negative


def signature(matrix: Sequence[Sequence[int | Fraction]]) -> int:
    positive, _, negative = inertia(matrix)
    return positive - negative


def matrix_rank(matrix: Sequence[Sequence[int | Fraction]]) -> int:
    rows = [[Fraction(x) for x in row] for row in matrix]
    if not rows:
        return 0
    columns = len(rows[0])
    if any(len(row) != columns for row in rows):
        raise ValueError("ragged matrix")
    rank = 0
    for column in range(columns):
        pivot = next((i for i in range(rank, len(rows)) if rows[i][column]), None)
        if pivot is None:
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        value = rows[rank][column]
        rows[rank] = [x / value for x in rows[rank]]
        for i in range(len(rows)):
            if i != rank and rows[i][column]:
                factor = rows[i][column]
                rows[i] = [x - factor * y for x, y in zip(rows[i], rows[rank])]
        rank += 1
        if rank == len(rows):
            break
    return rank


def nullspace(matrix: Sequence[Sequence[int | Fraction]], columns: int) -> Matrix:
    """Return a matrix whose columns form a basis of the right kernel."""
    rows = [[Fraction(x) for x in row] for row in matrix]
    if any(len(row) != columns for row in rows):
        raise ValueError("wrong column count")
    pivot_columns: list[int] = []
    rank = 0
    for column in range(columns):
        pivot = next((i for i in range(rank, len(rows)) if rows[i][column]), None)
        if pivot is None:
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        value = rows[rank][column]
        rows[rank] = [x / value for x in rows[rank]]
        for i in range(len(rows)):
            if i != rank and rows[i][column]:
                factor = rows[i][column]
                rows[i] = [x - factor * y for x, y in zip(rows[i], rows[rank])]
        pivot_columns.append(column)
        rank += 1
    free = [j for j in range(columns) if j not in pivot_columns]
    vectors: list[list[Fraction]] = []
    for free_column in free:
        vector = [Fraction(0) for _ in range(columns)]
        vector[free_column] = 1
        for i, pivot_column in enumerate(pivot_columns):
            vector[pivot_column] = -rows[i][free_column]
        vectors.append(vector)
    return [[vectors[j][i] for j in range(len(vectors))] for i in range(columns)]


def transpose(matrix: Sequence[Sequence[int | Fraction]]) -> Matrix:
    if not matrix:
        return []
    return [list(column) for column in zip(*matrix)]


def multiply(a: Sequence[Sequence[int | Fraction]], b: Sequence[Sequence[int | Fraction]]) -> Matrix:
    if not a:
        return []
    inner = len(a[0])
    if len(b) != inner:
        raise ValueError("dimension mismatch")
    columns = len(b[0]) if b else 0
    return [
        [sum((Fraction(a[i][k]) * Fraction(b[k][j]) for k in range(inner)), Fraction(0))
         for j in range(columns)]
        for i in range(len(a))
    ]


def adjacency(order: int, edges: Iterable[Edge]) -> list[set[int]]:
    graph = [set() for _ in range(order)]
    for u, v in edges:
        if not (0 <= u < v < order) or v in graph[u]:
            raise ValueError("edges must be distinct ordered pairs")
        graph[u].add(v)
        graph[v].add(u)
    return graph


def edge_list(graph: Sequence[set[int]]) -> tuple[Edge, ...]:
    return tuple((u, v) for u in range(len(graph)) for v in graph[u] if u < v)


def connected(graph: Sequence[set[int]]) -> bool:
    if not graph:
        return False
    seen = {0}
    stack = [0]
    while stack:
        vertex = stack.pop()
        for neighbor in graph[vertex] - seen:
            seen.add(neighbor)
            stack.append(neighbor)
    return len(seen) == len(graph)


def shifted_signless(graph: Sequence[set[int]]) -> Matrix:
    matrix: Matrix = [[0 for _ in graph] for _ in graph]
    for vertex, neighbors in enumerate(graph):
        matrix[vertex][vertex] = len(neighbors) - 2
        for neighbor in neighbors:
            matrix[vertex][neighbor] = 1
    return matrix


def line_adjacency(graph: Sequence[set[int]]) -> Matrix:
    edges = edge_list(graph)
    matrix: Matrix = [[0 for _ in edges] for _ in edges]
    for i, edge in enumerate(edges):
        for j, other in enumerate(edges[:i]):
            if set(edge) & set(other):
                matrix[i][j] = matrix[j][i] = 1
    return matrix


def validate_core(graph: Sequence[set[int]]) -> None:
    if not connected(graph):
        raise ValueError("graph must be connected")
    degrees = [len(neighbors) for neighbors in graph]
    if not degrees or min(degrees) < 2 or max(degrees) > 3:
        raise ValueError("graph must have minimum degree 2 and maximum degree 3")
    if all(degree == 2 for degree in degrees):
        raise ValueError("a cycle has no branch kernel")


def branch_paths(graph: Sequence[set[int]]) -> tuple[tuple[int, ...], tuple[Path, ...]]:
    """Extract maximal degree-two paths between degree-three vertices."""
    validate_core(graph)
    branch = tuple(vertex for vertex, neighbors in enumerate(graph) if len(neighbors) == 3)
    branch_set = set(branch)
    branch_index = {vertex: i for i, vertex in enumerate(branch)}
    used: set[Edge] = set()
    paths: list[Path] = []
    for start in branch:
        for first in sorted(graph[start]):
            first_edge = (min(start, first), max(start, first))
            if first_edge in used:
                continue
            used.add(first_edge)
            previous, current = start, first
            length = 1
            while current not in branch_set:
                choices = graph[current] - {previous}
                if len(choices) != 1:
                    raise AssertionError("degree-two path traversal failed")
                following = next(iter(choices))
                edge = (min(current, following), max(current, following))
                if edge in used:
                    raise AssertionError("path closed without reaching a branch vertex")
                used.add(edge)
                previous, current = current, following
                length += 1
            u, v = branch_index[start], branch_index[current]
            if v < u:
                u, v = v, u
            paths.append((u, v, length))
    if used != set(edge_list(graph)):
        raise AssertionError("not every core edge was assigned to a branch path")
    return branch, tuple(sorted(paths))


def build_core(branch_count: int, paths: Sequence[Path]) -> list[set[int]]:
    """Build a simple subcubic core from a cubic pseudokernel and lengths."""
    if branch_count <= 0:
        raise ValueError("positive branch count required")
    incidences = [0] * branch_count
    graph = [set() for _ in range(branch_count)]
    for u, v, length in paths:
        if not (0 <= u <= v < branch_count) or length < 1:
            raise ValueError("invalid path")
        incidences[u] += 1
        incidences[v] += 1
        if u == v and length < 3:
            raise ValueError("a simple loop path needs length at least three")
        internal = list(range(len(graph), len(graph) + length - 1))
        graph.extend(set() for _ in internal)
        route = [u] + internal + [v]
        for x, y in zip(route, route[1:]):
            if x == y or y in graph[x]:
                raise ValueError("construction is not simple")
            graph[x].add(y)
            graph[y].add(x)
    if any(value != 3 for value in incidences):
        raise ValueError("kernel must be cubic, counting a loop twice")
    validate_core(graph)
    return graph


def reduction(paths: Sequence[Path], branch_count: int) -> dict[str, object]:
    """Construct P, V, Z and the restricted parity-kernel form."""
    p: Matrix = [[int(i == j) for j in range(branch_count)] for i in range(branch_count)]
    v_rows: Matrix = []
    q = 0
    even_paths = 0
    for u, v, length in paths:
        q += (length - 1) // 2
        residue = length % 4
        if length % 2:
            sign = 1 if residue == 1 else -1
            if u == v:
                p[u][u] += 2 * sign
            else:
                p[u][v] += sign
                p[v][u] += sign
            continue
        even_paths += 1
        row = [0] * branch_count
        row[u] += 1
        row[v] += -1 if residue == 0 else 1
        v_rows.append(row)
    rank = matrix_rank(v_rows)
    z = nullspace(v_rows, branch_count)
    if z and z[0]:
        restricted = multiply(transpose(z), multiply(p, z))
    else:
        restricted = []
    return {
        "P": p,
        "V": v_rows,
        "Z": z,
        "R": restricted,
        "q": q,
        "t": even_paths,
        "rank": rank,
    }


def balanced_even_components(paths: Sequence[Path], branch_count: int) -> int:
    """Dimension of the signed even-path constraint kernel."""
    neighbors: list[list[tuple[int, int]]] = [[] for _ in range(branch_count)]
    forced_zero = [False] * branch_count
    for u, v, length in paths:
        if length % 2:
            continue
        relation = 1 if length % 4 == 0 else -1  # x_v = relation*x_u
        if u == v:
            if relation == -1:
                forced_zero[u] = True
            continue
        neighbors[u].append((v, relation))
        neighbors[v].append((u, relation))
    seen: set[int] = set()
    balanced = 0
    for root in range(branch_count):
        if root in seen:
            continue
        signs = {root: 1}
        stack = [root]
        consistent = not forced_zero[root]
        seen.add(root)
        while stack:
            vertex = stack.pop()
            if forced_zero[vertex]:
                consistent = False
            for neighbor, relation in neighbors[vertex]:
                expected = relation * signs[vertex]
                if neighbor in signs:
                    consistent &= signs[neighbor] == expected
                else:
                    signs[neighbor] = expected
                    seen.add(neighbor)
                    stack.append(neighbor)
        balanced += int(consistent)
    return balanced


def predicted_inertia(paths: Sequence[Path], branch_count: int) -> tuple[int, int, int]:
    data = reduction(paths, branch_count)
    positive, zero, negative = inertia(data["R"])
    q = int(data["q"])
    rank = int(data["rank"])
    null_even = int(data["t"]) - rank
    return q + rank + positive, null_even + zero, q + rank + negative


def audit_one(graph: Sequence[set[int]], check_line_graph: bool = False) -> dict[str, int]:
    branch, paths = branch_paths(graph)
    direct = inertia(shifted_signless(graph))
    predicted = predicted_inertia(paths, len(branch))
    if direct != predicted:
        raise AssertionError((paths, direct, predicted))
    data = reduction(paths, len(branch))
    beta = balanced_even_components(paths, len(branch))
    if beta != len(branch) - int(data["rank"]):
        raise AssertionError("signed-component/rank identity failed")
    reduced_signature = signature(data["R"])
    if direct[0] - direct[2] != reduced_signature:
        raise AssertionError("signature did not survive the reduction")
    cyclomatic = sum(map(len, graph)) // 2 - len(graph) + 1
    if len(branch) != 2 * cyclomatic - 2:
        raise AssertionError("branch/cyclomatic identity failed")
    if reduced_signature > beta:
        raise AssertionError("dimension bound failed")
    if check_line_graph:
        line_signature = signature(line_adjacency(graph))
        if line_signature != reduced_signature - cyclomatic + 1:
            raise AssertionError("line-graph transfer failed")
    return {
        "order": len(graph),
        "paths": len(paths),
        "branch": len(branch),
        "cyclomatic": cyclomatic,
        "beta": beta,
        "signature": reduced_signature,
    }


def graph6_decode(code: str) -> list[set[int]]:
    values = [ord(char) - 63 for char in code.strip()]
    if not values or not 0 <= values[0] <= 62:
        raise ValueError("only small graph6 records are supported")
    order = values[0]
    bits = [bit for value in values[1:] for bit in ((value >> k) & 1 for k in range(5, -1, -1))]
    edges: list[Edge] = []
    cursor = 0
    for v in range(1, order):
        for u in range(v):
            if bits[cursor]:
                edges.append((u, v))
            cursor += 1
    return adjacency(order, edges)


def audit_small_graphs(max_order: int = 6) -> dict[str, object]:
    tested = line_checked = rank_class = 0
    by_order: dict[int, int] = {}
    beta_histogram: dict[int, int] = {}
    for order in range(4, max_order + 1):
        possible = tuple((u, v) for v in range(1, order) for u in range(v))
        count = 0
        for mask in range(1 << len(possible)):
            degrees = [0] * order
            edges: list[Edge] = []
            invalid = False
            for i, (u, v) in enumerate(possible):
                if (mask >> i) & 1:
                    degrees[u] += 1
                    degrees[v] += 1
                    if degrees[u] > 3 or degrees[v] > 3:
                        invalid = True
                        break
                    edges.append((u, v))
            if invalid or min(degrees) < 2 or max(degrees) > 3:
                continue
            graph = adjacency(order, edges)
            if not connected(graph) or all(degree == 2 for degree in degrees):
                continue
            check_line = order <= 5 or count < 128
            stats = audit_one(graph, check_line_graph=check_line)
            tested += 1
            line_checked += int(check_line)
            count += 1
            beta = stats["beta"]
            beta_histogram[beta] = beta_histogram.get(beta, 0) + 1
            threshold = (3 * stats["cyclomatic"] - 1) // 2
            rank_class += int(beta <= threshold)
        by_order[order] = count
    return {
        "max_order": max_order,
        "tested": tested,
        "line_graph_checks": line_checked,
        "rank_class": rank_class,
        "by_order": by_order,
        "beta_histogram": dict(sorted(beta_histogram.items())),
    }


KERNELS: dict[str, tuple[int, tuple[tuple[int, int], ...]]] = {
    "three_parallel": (2, ((0, 1), (0, 1), (0, 1))),
    "two_loops_bridge": (2, ((0, 0), (0, 1), (1, 1))),
    "k4": (4, ((0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3))),
    "prism": (6, ((0, 1), (1, 2), (0, 2), (3, 4), (4, 5), (3, 5), (0, 3), (1, 4), (2, 5))),
    "k33": (6, tuple((u, v) for u in range(3) for v in range(3, 6))),
}


def assignment(index: int, edge_count: int) -> tuple[int, ...]:
    """Deterministic mixed-residue lengths in 1..8."""
    values: list[int] = []
    state = index + 1
    for edge in range(edge_count):
        state = (1103515245 * state + 12345 + 97 * edge) & 0x7FFFFFFF
        values.append(1 + (state % 8))
    return tuple(values)


def audit_structured(cases_per_kernel: int = 48) -> dict[str, object]:
    tested = periodic = line_checked = periodic_line_checked = 0
    by_kernel: dict[str, int] = {}
    witness_records: dict[str, object] = {}
    for name, (branch_count, kernel_edges) in KERNELS.items():
        count = 0
        for index in range(cases_per_kernel):
            lengths = list(assignment(index, len(kernel_edges)))
            for i, (u, v) in enumerate(kernel_edges):
                if u == v and lengths[i] < 3:
                    lengths[i] += 4
            paths = tuple((u, v, length) for (u, v), length in zip(kernel_edges, lengths))
            try:
                graph = build_core(branch_count, paths)
            except ValueError:
                continue
            stats = audit_one(graph, check_line_graph=(index < 12))
            line_checked += int(index < 12)
            tested += 1
            count += 1
            lifted = list(paths)
            chosen = index % len(lifted)
            u, v, length = lifted[chosen]
            lifted[chosen] = (u, v, length + 4)
            lifted_graph = build_core(branch_count, lifted)
            base_inertia = inertia(shifted_signless(graph))
            lifted_inertia = inertia(shifted_signless(lifted_graph))
            if lifted_inertia != (base_inertia[0] + 2, base_inertia[1], base_inertia[2] + 2):
                raise AssertionError("four-subdivision inertia law failed")
            if index < 12:
                if signature(line_adjacency(graph)) != signature(line_adjacency(lifted_graph)):
                    raise AssertionError("four-subdivision line-signature law failed")
                periodic_line_checked += 1
            periodic += 1
            if index == 0:
                witness_records[name] = {"lengths": lengths, **stats}
        by_kernel[name] = count
    for code in ("Jl?GGCHa??_", "Ml_GGCHO??_@?@?C_"):
        graph = graph6_decode(code)
        core_vertices = set(range(len(graph)))
        changed = True
        while changed:
            changed = False
            for vertex in tuple(core_vertices):
                if len(graph[vertex] & core_vertices) < 2:
                    core_vertices.remove(vertex)
                    changed = True
        relabel = {vertex: i for i, vertex in enumerate(sorted(core_vertices))}
        core_edges = [
            (relabel[u], relabel[v])
            for u, v in edge_list(graph)
            if u in core_vertices and v in core_vertices
        ]
        core = adjacency(len(core_vertices), core_edges)
        witness_records[code] = audit_one(core, check_line_graph=True)
    return {
        "cases_per_kernel": cases_per_kernel,
        "tested": tested,
        "periodicity_checks": periodic,
        "line_graph_checks": line_checked + periodic_line_checked + 2,
        "by_kernel": by_kernel,
        "witnesses": witness_records,
    }


def run_audit(max_order: int = 6, cases_per_kernel: int = 48) -> dict[str, object]:
    small = audit_small_graphs(max_order)
    structured = audit_structured(cases_per_kernel)
    record: dict[str, object] = {
        "arithmetic": "exact integers and fractions",
        "small_graphs": small,
        "structured": structured,
    }
    canonical = json.dumps(record, sort_keys=True, separators=(",", ":"))
    record["record_sha256"] = hashlib.sha256(canonical.encode()).hexdigest()
    return record


def main() -> None:
    record = run_audit()
    print(json.dumps(record, indent=2, sort_keys=True))
    print("VERIFIED")


if __name__ == "__main__":
    main()
