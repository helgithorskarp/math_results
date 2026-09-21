#!/usr/bin/env python3
"""Independent exact audit of the core-branch line-graph signature bound.

CPython 3.11+, standard library only.  This checker imports no target code or
output.  It uses characteristic polynomials and Cramer determinants rather
than symmetric-congruence pivots.  Finite checks corroborate the proof; the
universal inequalities are proved in REVIEW.md.
"""

import argparse
from collections import Counter, defaultdict
from fractions import Fraction
from hashlib import sha256
from heapq import heapify, heappop, heappush
from itertools import combinations, product
import json
from pathlib import Path


def require(condition, message):
    if not condition:
        raise ValueError(message)


def matrix_product(left, right):
    rows = len(left)
    inner = len(right)
    columns = len(right[0]) if right else 0
    return [[sum(left[i][k] * right[k][j] for k in range(inner))
             for j in range(columns)] for i in range(rows)]


def characteristic_polynomial(matrix):
    """Faddeev--LeVerrier coefficients of det(xI-A), exactly."""
    size = len(matrix)
    require(all(len(row) == size for row in matrix), "matrix is not square")
    a = [[Fraction(entry) for entry in row] for row in matrix]
    block = [[Fraction(int(i == j)) for j in range(size)] for i in range(size)]
    coefficients = [Fraction(1)]
    for step in range(1, size + 1):
        multiplied = matrix_product(a, block)
        coefficient = -sum(multiplied[i][i] for i in range(size)) / step
        coefficients.append(coefficient)
        if step < size:
            for i in range(size):
                multiplied[i][i] += coefficient
            block = multiplied
    return coefficients


def sign_variations(values):
    signs = [1 if value > 0 else -1 for value in values if value]
    return sum(signs[i] != signs[i - 1] for i in range(1, len(signs)))


def inertia_from_charpoly(matrix):
    """Descartes is exact because a symmetric matrix has only real roots."""
    coefficients = characteristic_polynomial(matrix)
    degree = len(coefficients) - 1
    positive = sign_variations(coefficients)
    reflected = [coefficient * ((-1) ** (degree - index))
                 for index, coefficient in enumerate(coefficients)]
    negative = sign_variations(reflected)
    return positive, degree - positive - negative, negative


def signature(matrix):
    positive, _, negative = inertia_from_charpoly(matrix)
    return positive - negative


def bareiss_determinant(matrix):
    size = len(matrix)
    require(all(len(row) == size for row in matrix), "matrix is not square")
    if size == 0:
        return 1
    a = [[int(entry) for entry in row] for row in matrix]
    sign = 1
    previous = 1
    for column in range(size - 1):
        if a[column][column] == 0:
            pivot = next((row for row in range(column + 1, size)
                          if a[row][column]), None)
            if pivot is None:
                return 0
            a[column], a[pivot] = a[pivot], a[column]
            sign = -sign
        current = a[column][column]
        for row in range(column + 1, size):
            for j in range(column + 1, size):
                numerator = a[row][j] * current - a[row][column] * a[column][j]
                require(numerator % previous == 0, "Bareiss division was not exact")
                a[row][j] = numerator // previous
            a[row][column] = 0
        previous = current
    return sign * a[-1][-1]


def adjacency(number, edges):
    result = [set() for _ in range(number)]
    for u, v in edges:
        require(0 <= u < v < number and v not in result[u], "not a simple graph")
        result[u].add(v)
        result[v].add(u)
    return result


def connected(adjacency_sets):
    if not adjacency_sets:
        return False
    seen = {0}
    stack = [0]
    while stack:
        vertex = stack.pop()
        for neighbor in adjacency_sets[vertex] - seen:
            seen.add(neighbor)
            stack.append(neighbor)
    return len(seen) == len(adjacency_sets)


def two_core(adjacency_sets):
    active = set(range(len(adjacency_sets)))
    degree = [len(neighbors) for neighbors in adjacency_sets]
    stack = [vertex for vertex, value in enumerate(degree) if value < 2]
    while stack:
        vertex = stack.pop()
        if vertex not in active:
            continue
        active.remove(vertex)
        for neighbor in adjacency_sets[vertex]:
            if neighbor in active:
                degree[neighbor] -= 1
                if degree[neighbor] == 1:
                    stack.append(neighbor)
    return frozenset(active)


def shifted_signless(adjacency_sets, vertices=None, diagonal_addition=None):
    if vertices is None:
        vertices = tuple(range(len(adjacency_sets)))
    vertices = tuple(vertices)
    if diagonal_addition is None:
        diagonal_addition = {}
    matrix = [[Fraction(0) for _ in vertices] for _ in vertices]
    for i, vertex in enumerate(vertices):
        matrix[i][i] = Fraction(len(adjacency_sets[vertex]) - 2) + diagonal_addition.get(vertex, 0)
        for j, other in enumerate(vertices[:i]):
            if other in adjacency_sets[vertex]:
                matrix[i][j] = matrix[j][i] = 1
    return matrix


def line_adjacency(edges):
    matrix = [[0 for _ in edges] for _ in edges]
    for i, edge in enumerate(edges):
        for j, other in enumerate(edges[:i]):
            if set(edge).intersection(other):
                matrix[i][j] = matrix[j][i] = 1
    return matrix


def prufer_edges(sequence, number):
    if number == 1:
        return ()
    degrees = [1] * number
    for vertex in sequence:
        degrees[vertex] += 1
    leaves = [vertex for vertex, degree in enumerate(degrees) if degree == 1]
    heapify(leaves)
    edges = []
    for vertex in sequence:
        leaf = heappop(leaves)
        edges.append(tuple(sorted((leaf, vertex))))
        degrees[leaf] -= 1
        degrees[vertex] -= 1
        if degrees[vertex] == 1:
            heappush(leaves, vertex)
    edges.append(tuple(sorted((heappop(leaves), heappop(leaves)))))
    return tuple(sorted(edges))


def rooted_matrix(number, edges, root=0):
    graph = adjacency(number, edges)
    matrix = shifted_signless(graph)
    matrix[root][root] += 1
    return [[int(entry) for entry in row] for row in matrix]


def direct_rooted_state(number, edges, root=0):
    matrix = rooted_matrix(number, edges, root)
    determinant = bareiss_determinant(matrix)
    require(determinant != 0, "rooted matrix is singular")
    minor = [[matrix[i][j] for j in range(number) if j != root]
             for i in range(number) if i != root]
    response = Fraction(bareiss_determinant(minor), determinant)
    return signature(matrix), response


def audit_labeled_rooted_trees(max_order=7):
    counts = []
    total = zero_signature = negative_minus_one = 0
    digest = sha256()
    for number in range(1, max_order + 1):
        count = 0
        sequences = product(range(number), repeat=max(0, number - 2))
        for sequence in sequences:
            edges = prufer_edges(sequence, number)
            sigma, rho = direct_rooted_state(number, edges)
            require(rho.numerator % 2 and rho.denominator % 2,
                    "root response violates odd/odd parity")
            require(sigma <= 0, "rooted-tree signature is positive")
            if sigma == 0:
                require(rho == 1, "zero signature does not force response one")
                zero_signature += 1
            if sigma == -1 and rho < 0:
                require(rho == -1, "negative response at signature -1 is not -1")
                negative_minus_one += 1
            digest.update(json.dumps([number, sequence, sigma,
                                      rho.numerator, rho.denominator],
                                     separators=(",", ":")).encode())
            count += 1
        counts.append(count)
        total += count
    return {
        "orders": [1, max_order],
        "counts": counts,
        "total": total,
        "zero_signature_states": zero_signature,
        "negative_response_signature_minus_one": negative_minus_one,
        "record_digest": digest.hexdigest(),
    }


def attached_tree_data(adjacency_sets, core):
    outside = set(range(len(adjacency_sets))) - set(core)
    corrections = {vertex: Fraction(0) for vertex in core}
    tau = 0
    while outside:
        start = min(outside)
        component = {start}
        stack = [start]
        while stack:
            vertex = stack.pop()
            for neighbor in adjacency_sets[vertex] & outside:
                if neighbor not in component:
                    component.add(neighbor)
                    stack.append(neighbor)
        outside -= component
        boundary = [(vertex, neighbor) for vertex in component
                    for neighbor in adjacency_sets[vertex] if neighbor in core]
        require(len(boundary) == 1, "outside component has wrong core boundary")
        root, core_vertex = boundary[0]
        order = [root] + sorted(component - {root})
        index = {vertex: i for i, vertex in enumerate(order)}
        tree_edges = []
        for vertex in component:
            for neighbor in adjacency_sets[vertex] & component:
                if vertex < neighbor:
                    tree_edges.append(tuple(sorted((index[vertex], index[neighbor]))))
        require(len(tree_edges) == len(component) - 1, "outside component is not a tree")
        sigma, rho = direct_rooted_state(len(component), tuple(sorted(tree_edges)), 0)
        tau += sigma
        corrections[core_vertex] += 1 - rho
    return tau, corrections


def relabeled_core(adjacency_sets, core):
    vertices = sorted(core)
    index = {vertex: i for i, vertex in enumerate(vertices)}
    edges = tuple((index[u], index[v]) for u in vertices
                  for v in adjacency_sets[u] if u < v and v in core)
    return len(vertices), edges


def audit_connected_graphs(max_order=6):
    connected_count = relevant = reduction_checks = 0
    strict_refinements = positive_branch_corrections = excess_payments = 0
    conjecture_certificates = refined_equalities = 0
    correction_histogram = Counter()
    cyclomatic_histogram = Counter()
    unique_cores = set()
    for number in range(1, max_order + 1):
        possible = tuple(combinations(range(number), 2))
        for bits in range(1 << len(possible)):
            edges = tuple(edge for index, edge in enumerate(possible)
                          if bits & (1 << index))
            graph = adjacency(number, edges)
            if not connected(graph):
                continue
            connected_count += 1
            cyclomatic = len(edges) - number + 1
            if cyclomatic < 2:
                continue
            relevant += 1
            cyclomatic_histogram[cyclomatic] += 1
            core = two_core(graph)
            require(core, "relevant graph has empty 2-core")
            core_vertices = sorted(core)
            core_degrees = {vertex: len(graph[vertex] & core) for vertex in core}
            branch = {vertex for vertex in core if core_degrees[vertex] >= 3}
            eta = sum(max(core_degrees[vertex] - 3, 0) for vertex in core)
            require(len(branch) == 2 * cyclomatic - 2 - eta,
                    "branch/excess identity failed")
            tau, corrections = attached_tree_data(graph, core)
            positive = {vertex for vertex in core if corrections[vertex] > 0}
            payment = -tau - len(positive)
            require(payment >= 0, "tree signature does not pay for correction")
            full_signature = signature(shifted_signless(graph))
            core_graph = [neighbors & core for neighbors in graph]
            core_matrix = shifted_signless(core_graph, core_vertices, corrections)
            require(full_signature == tau + signature(core_matrix),
                    "2-core Schur signature identity failed")
            branch_positive = len(branch & positive)
            refined_bound = len(branch) - branch_positive - payment
            require(full_signature <= refined_bound,
                    "attachment-sensitive branch bound failed")
            line_signature = full_signature - cyclomatic + 1
            correction = eta + branch_positive + payment
            require(line_signature <= cyclomatic - 1 - correction,
                    "refined line-signature bound failed")
            reduction_checks += 1
            correction_histogram[correction] += 1
            strict_refinements += int(correction > 0)
            positive_branch_corrections += int(branch_positive > 0)
            excess_payments += int(payment > 0)
            conjecture_certificates += int(correction >= cyclomatic // 2 - 1)
            refined_equalities += int(line_signature == cyclomatic - 1 - correction)
            unique_cores.add(relabeled_core(graph, core))
    return {
        "orders": [1, max_order],
        "connected_graphs": connected_count,
        "graphs_with_cyclomatic_at_least_two": relevant,
        "schur_reductions_checked": reduction_checks,
        "cyclomatic_histogram": dict(sorted(cyclomatic_histogram.items())),
        "correction_histogram": dict(sorted(correction_histogram.items())),
        "strict_refinements": strict_refinements,
        "positive_branch_correction_graphs": positive_branch_corrections,
        "excess_payment_graphs": excess_payments,
        "sharp_conjecture_certificates": conjecture_certificates,
        "refined_bound_equalities": refined_equalities,
        "unique_cores": unique_cores,
    }


def audit_principal_reduction(unique_cores):
    structural = signature_checks = 0
    by_order = Counter()
    for number, edges in sorted(unique_cores):
        graph = adjacency(number, edges)
        degrees = [len(neighbors) for neighbors in graph]
        branch = {vertex for vertex, degree in enumerate(degrees) if degree >= 3}
        for mask in range(1 << number):
            chosen = {vertex for vertex in range(number) if mask & (1 << vertex)}
            low = chosen - branch
            unseen = set(low)
            while unseen:
                start = min(unseen)
                component = {start}
                stack = [start]
                while stack:
                    vertex = stack.pop()
                    for neighbor in graph[vertex] & low:
                        if neighbor not in component:
                            component.add(neighbor)
                            stack.append(neighbor)
                unseen -= component
                edge_count = sum(len(graph[vertex] & component)
                                 for vertex in component) // 2
                require(edge_count < len(component),
                        "degree-two induced subgraph contains a cycle")
                require(all(len(graph[vertex] & component) <= 2
                            for vertex in component),
                        "low-degree component is not a path")
            structural += 1
            by_order[number] += 1
            if number <= 5:
                matrix = shifted_signless(graph, sorted(chosen))
                require(signature(matrix) <= len(chosen & branch),
                        "principal branch-signature inequality failed")
                signature_checks += 1
    return {
        "unique_cores": len(unique_cores),
        "structural_subset_checks": structural,
        "structural_checks_by_core_order": dict(sorted(by_order.items())),
        "charpoly_principal_checks_through_order_five": signature_checks,
    }


def graph6_decode(code):
    values = [ord(character) - 63 for character in code]
    require(values and 0 <= values[0] <= 62, "unsupported graph6 header")
    number = values[0]
    bits = [bit for value in values[1:]
            for bit in ((value >> shift) & 1 for shift in range(5, -1, -1))]
    edges = []
    cursor = 0
    for v in range(1, number):
        for u in range(v):
            if bits[cursor]:
                edges.append((u, v))
            cursor += 1
    return number, tuple(edges)


def cycle(number):
    return tuple(sorted((min(i, (i + 1) % number), max(i, (i + 1) % number))
                        for i in range(number)))


def audit_boundary_and_witnesses():
    cycle_five = cycle(5)
    cycle_graph = adjacency(5, cycle_five)
    cycle_signature = signature(shifted_signless(cycle_graph))
    require(cycle_signature == 1, "C5 boundary control failed")

    witnesses = {}
    for name, code, expected in (
            ("c2", "Jl?GGCHa??_", 1),
            ("c3", "Ml_GGCHO??_@?@?C_", 2)):
        number, edges = graph6_decode(code)
        direct = signature(line_adjacency(edges))
        graph = adjacency(number, edges)
        cyclomatic = len(edges) - number + 1
        translated = signature(shifted_signless(graph)) - cyclomatic + 1
        require(direct == translated == expected, "sharp witness failed")
        witnesses[name] = {
            "order": number,
            "size": len(edges),
            "cyclomatic": cyclomatic,
            "line_signature": direct,
        }
    return {
        "excluded_C5": {
            "cyclomatic": 1,
            "branch_vertices": 0,
            "shifted_signless_signature": cycle_signature,
        },
        "sharp_witnesses": witnesses,
    }


def run():
    rooted = audit_labeled_rooted_trees()
    graph_audit = audit_connected_graphs()
    unique_cores = graph_audit.pop("unique_cores")
    principal = audit_principal_reduction(unique_cores)
    boundaries = audit_boundary_and_witnesses()
    return {
        "status": "VERIFIED",
        "rooted_labeled_tree_audit": rooted,
        "connected_graph_audit": graph_audit,
        "principal_reduction_audit": principal,
        "boundary_and_witness_audit": boundaries,
        "trust_boundary": (
            "finite exact corroboration only; the universal Schur, payment, "
            "interlacing, and refinement arguments are audited in REVIEW.md"
        ),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--emit", action="store_true",
                        help="emit output without checking expected.json")
    arguments = parser.parse_args()
    result = run()
    encoded = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if not arguments.emit:
        expected = json.loads(Path(__file__).with_name("expected.json").read_text())
        require(json.loads(encoded) == expected, "expected output mismatch")
    print(encoded, end="")


if __name__ == "__main__":
    main()
