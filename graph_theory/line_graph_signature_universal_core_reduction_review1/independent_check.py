#!/usr/bin/env python3
"""Independent exact audit of the universal subcubic-core reduction.

Standard-library Python only.  This file deliberately imports no code from
the reviewed package.  All matrices are rebuilt from graph definitions and
all inertia calculations use exact rational congruence elimination.
"""

from fractions import Fraction
from itertools import combinations, product
import json


TARGET_COMMIT = "c8a497851df1f30ed0acdddc8975b2339276ad5b"
TARGET_REF = "bafkreifbhuv5cqeoh2qwk2xtqhrxspbjsqz3e3a4sz2qz6ibt67ufmnmhu"


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


class Polynomial:
    """Tiny exact polynomial ring over Q, used only for the split identity."""

    def __init__(self, terms=None):
        self.terms = {m: Fraction(c) for m, c in (terms or {}).items() if c}

    @staticmethod
    def constant(value):
        return Polynomial({(): Fraction(value)}) if value else Polynomial()

    @staticmethod
    def variable(name):
        return Polynomial({(name,): Fraction(1)})

    def __add__(self, other):
        other = as_polynomial(other)
        result = dict(self.terms)
        for monomial, coefficient in other.terms.items():
            result[monomial] = result.get(monomial, Fraction(0)) + coefficient
            if not result[monomial]:
                del result[monomial]
        return Polynomial(result)

    __radd__ = __add__

    def __neg__(self):
        return Polynomial({m: -c for m, c in self.terms.items()})

    def __sub__(self, other):
        return self + (-as_polynomial(other))

    def __rsub__(self, other):
        return as_polynomial(other) - self

    def __mul__(self, other):
        other = as_polynomial(other)
        result = {}
        for left, a in self.terms.items():
            for right, b in other.terms.items():
                monomial = tuple(sorted(left + right))
                result[monomial] = result.get(monomial, Fraction(0)) + a * b
        return Polynomial(result)

    __rmul__ = __mul__

    def __truediv__(self, denominator):
        denominator = Fraction(denominator)
        require(denominator != 0, "zero polynomial denominator")
        return Polynomial({m: c / denominator for m, c in self.terms.items()})

    def __eq__(self, other):
        return self.terms == as_polynomial(other).terms


def as_polynomial(value):
    return value if isinstance(value, Polynomial) else Polynomial.constant(value)


def verify_universal_split_polynomial():
    # F and G stand for the arbitrary scalars f^T z and g^T z; z^T B z is
    # common to both sides and can be omitted.  Thus this is dimension-free.
    alpha, beta, x, y, t, aa, bb, ff, gg = [
        Polynomial.variable(name)
        for name in ("alpha", "beta", "x", "y", "t", "A", "B0", "F", "G")
    ]
    u = x
    w = x + y
    r = t - beta * x - gg - beta * y / 2
    p = aa - r
    q = bb - x
    path = 2 * u * p + 2 * p * q + 2 * q * r + 2 * r * w
    transformed = alpha * u * u + beta * w * w + 2 * u * ff + 2 * w * gg + path
    expected = (alpha + beta) * x * x + 2 * x * (ff + gg) + 2 * aa * bb + 2 * y * t
    require(transformed == expected, "universal split polynomial failed")
    return {"coefficient_domain": "Q[alpha,beta,x,y,t,A,B0,F,G]", "identity": True}


def graph(order, edges):
    normalized = tuple(sorted(tuple(sorted(edge)) for edge in edges))
    require(order >= 1, "positive order required")
    require(len(normalized) == len(set(normalized)), "duplicate edge")
    require(all(0 <= u < v < order for u, v in normalized), "invalid simple edge")
    return order, normalized


def neighbors(g):
    order, edges = g
    rows = [set() for _ in range(order)]
    for u, v in edges:
        rows[u].add(v)
        rows[v].add(u)
    return rows


def connected(g):
    rows = neighbors(g)
    seen = {0}
    stack = [0]
    while stack:
        for vertex in rows[stack.pop()]:
            if vertex not in seen:
                seen.add(vertex)
                stack.append(vertex)
    return len(seen) == g[0]


def cyclomatic(g):
    require(connected(g), "connected graph required")
    return len(g[1]) - g[0] + 1


def vertex_matrix(g):
    order, edges = g
    matrix = [[0] * order for _ in range(order)]
    for vertex in range(order):
        matrix[vertex][vertex] = -2
    for u, v in edges:
        matrix[u][u] += 1
        matrix[v][v] += 1
        matrix[u][v] = matrix[v][u] = 1
    return matrix


def line_matrix(g):
    edge_sets = [set(edge) for edge in g[1]]
    return [
        [int(i != j and bool(left & right)) for j, right in enumerate(edge_sets)]
        for i, left in enumerate(edge_sets)
    ]


def inertia(matrix):
    """Exact inertia by rebuilding a Schur complement at each pivot."""
    size = len(matrix)
    require(all(len(row) == size for row in matrix), "square matrix required")
    require(all(matrix[i][j] == matrix[j][i] for i in range(size) for j in range(i)),
            "symmetric matrix required")
    current = [[Fraction(entry) for entry in row] for row in matrix]
    positive = zero = negative = 0
    while current:
        size = len(current)
        diagonal = next((i for i in range(size) if current[i][i]), None)
        if diagonal is not None:
            order = [diagonal] + [i for i in range(size) if i != diagonal]
            current = [[current[i][j] for j in order] for i in order]
            pivot = current[0][0]
            positive += int(pivot > 0)
            negative += int(pivot < 0)
            current = [
                [current[i][j] - current[i][0] * current[0][j] / pivot
                 for j in range(1, size)]
                for i in range(1, size)
            ]
            continue
        pair = next(((i, j) for i in range(size) for j in range(i + 1, size)
                     if current[i][j]), None)
        if pair is None:
            zero += size
            break
        first, second = pair
        order = [first, second] + [i for i in range(size) if i not in pair]
        current = [[current[i][j] for j in order] for i in order]
        pivot = current[0][1]
        positive += 1
        negative += 1
        current = [
            [current[i][j] -
             (current[i][0] * current[1][j] + current[i][1] * current[0][j]) / pivot
             for j in range(2, size)]
            for i in range(2, size)
        ]
    return positive, zero, negative


def add_inertia(left, right):
    return tuple(a + b for a, b in zip(left, right))


def line_inertia_from_vertex(g):
    result = list(inertia(vertex_matrix(g)))
    result[2] += cyclomatic(g) - 1
    require(result[2] >= 0, "invalid incidence inertia conversion")
    return tuple(result)


def split_vertex(g, vertex, left):
    order, edges = g
    rows = neighbors(g)
    left = set(left)
    require(left and left < rows[vertex], "proper nonempty split required")
    right_endpoint = order
    rewritten = []
    for u, v in edges:
        if vertex not in (u, v):
            rewritten.append((u, v))
            continue
        other = v if u == vertex else u
        rewritten.append((vertex if other in left else right_endpoint, other))
    rewritten += [
        (vertex, order + 1), (order + 1, order + 2),
        (order + 2, order + 3), (order + 3, right_endpoint),
    ]
    return graph(order + 4, rewritten)


MODULE_EDGES = (
    (0, 1), (1, 2), (2, 3), (0, 3),
    (4, 5), (5, 6), (6, 7), (7, 8), (4, 8),
    (0, 4), (1, 9),
)


def attach_module(g, vertex):
    order, edges = g
    labels = list(range(order, order + 9)) + [vertex]
    attached = list(edges) + [(labels[u], labels[v]) for u, v in MODULE_EDGES]
    return graph(order + 9, attached)


def to_core(g):
    require(g[0] >= 2 and connected(g), "nontrivial connected input required")
    current = g
    splits = 0
    while True:
        rows = neighbors(current)
        vertex = next((i for i, row in enumerate(rows) if len(row) >= 4), None)
        if vertex is None:
            break
        current = split_vertex(current, vertex, sorted(rows[vertex])[:2])
        splits += 1
    leaves = [i for i, row in enumerate(neighbors(current)) if len(row) == 1]
    for vertex in leaves:
        current = attach_module(current, vertex)
    return current, splits, len(leaves)


def path_graph(order):
    return graph(order, [(i, i + 1) for i in range(order - 1)])


def cycle_graph(order):
    return graph(order, [(i, (i + 1) % order) for i in range(order)])


def complete_graph(order):
    return graph(order, combinations(range(order), 2))


def star_graph(leaves):
    return graph(leaves + 1, [(0, i) for i in range(1, leaves + 1)])


def complete_bipartite(left, right):
    return graph(left + right, [(u, left + v) for u in range(left) for v in range(right)])


def audit_module():
    module = graph(10, MODULE_EDGES)
    matrix = line_matrix(module)
    root = module[1].index((1, 9))
    values = {(0, 1): Fraction(1, 2), (1, 2): Fraction(1, 2),
              (2, 3): Fraction(-1, 2), (0, 3): Fraction(-1, 2)}
    response = [values.get(edge, Fraction(0)) for edge in module[1]]
    product_vector = [sum(Fraction(x) * y for x, y in zip(row, response)) for row in matrix]
    require(product_vector == [Fraction(int(i == root)) for i in range(11)],
            "module inverse-column certificate")
    require(response[root] == 0, "module root response is not zero")
    module_inertia = inertia(matrix)
    require(module_inertia == (6, 0, 5), "module inertia")

    hosts = [path_graph(2), path_graph(4), cycle_graph(4), complete_graph(4), star_graph(5)]
    attachment_cases = 0
    for host in hosts:
        old = inertia(line_matrix(host))
        for vertex in range(host[0]):
            enlarged = attach_module(host, vertex)
            require(inertia(line_matrix(enlarged)) == add_inertia(old, module_inertia),
                    "literal module attachment inertia")
            attachment_cases += 1
    return {"inertia": module_inertia, "root_inverse_entry": "0",
            "literal_host_vertex_attachments": attachment_cases}


def audit_splits():
    hosts = [star_graph(d) for d in range(2, 10)]
    hosts += [complete_graph(n) for n in range(4, 9)]
    # This port has irregular edges among its neighbors.
    hosts.append(graph(9, [(0, i) for i in range(1, 9)] +
                       [(1, 2), (2, 3), (3, 4), (4, 5), (1, 5), (6, 7)]))
    exact_cases = direct_line_cases = 0
    for host in hosts:
        old_vertex = inertia(vertex_matrix(host))
        old_line = inertia(line_matrix(host))
        row = sorted(neighbors(host)[0])
        # Complementary cuts give the same mathematical partition; retain the
        # first port to select exactly one orientation of each partition.
        for bits in range(1, 1 << len(row)):
            left = [v for i, v in enumerate(row) if bits >> i & 1]
            if row[0] not in left or len(left) == len(row):
                continue
            enlarged = split_vertex(host, 0, left)
            require(inertia(vertex_matrix(enlarged)) == add_inertia(old_vertex, (2, 0, 2)),
                    "split shifted-matrix inertia")
            exact_cases += 1
            if exact_cases % 19 == 0 or len(row) <= 3:
                require(inertia(line_matrix(enlarged)) == add_inertia(old_line, (2, 0, 2)),
                        "split line-graph inertia")
                direct_line_cases += 1
    return {"oriented_partition_representatives": exact_cases,
            "literal_line_graph_cases": direct_line_cases}


def audit_full_reductions():
    cases = {
        "edge": path_graph(2),
        "path6": path_graph(6),
        "cycle3": cycle_graph(3),
        "cycle4": cycle_graph(4),
        "cycle5": cycle_graph(5),
        "cycle6": cycle_graph(6),
        "star3": star_graph(3),
        "star4": star_graph(4),
        "star6": star_graph(6),
        "K4": complete_graph(4),
        "K5": complete_graph(5),
        "K6": complete_graph(6),
        "K2,4": complete_bipartite(2, 4),
        "K3,4": complete_bipartite(3, 4),
        "branched_tree": graph(8, [(0, 1), (0, 2), (0, 3), (1, 4),
                                    (1, 5), (3, 6), (6, 7)]),
    }
    direct_outputs = 0
    maximum_order = maximum_edges = 0
    for name, original in cases.items():
        rows = neighbors(original)
        leaves = sum(len(row) == 1 for row in rows)
        excess = sum(max(len(row) - 3, 0) for row in rows)
        old_vertex = inertia(vertex_matrix(original))
        old_line = inertia(line_matrix(original))
        require(old_line == line_inertia_from_vertex(original),
                f"input incidence identity: {name}")
        core, splits, caps = to_core(original)
        require((splits, caps) == (excess, leaves), f"move counts: {name}")
        require(core[0] == original[0] + 4 * excess + 9 * leaves,
                f"vertex count: {name}")
        require(len(core[1]) == len(original[1]) + 4 * excess + 11 * leaves,
                f"edge count: {name}")
        require(cyclomatic(core) == cyclomatic(original) + 2 * leaves,
                f"cyclomatic count: {name}")
        require(set(map(len, neighbors(core))) <= {2, 3}, f"core degrees: {name}")
        new_vertex = inertia(vertex_matrix(core))
        require(new_vertex == add_inertia(old_vertex,
                                          (2 * excess + 6 * leaves, 0,
                                           2 * excess + 3 * leaves)),
                f"shifted-matrix inertia: {name}")
        new_line = line_inertia_from_vertex(core)
        require(new_line == add_inertia(old_line,
                                        (2 * excess + 6 * leaves, 0,
                                         2 * excess + 5 * leaves)),
                f"line-graph inertia formula: {name}")
        old_slack = 2 * (old_line[0] - old_line[2]) - cyclomatic(original) - 1
        new_slack = 2 * (new_line[0] - new_line[2]) - cyclomatic(core) - 1
        require(old_slack == new_slack, f"slack preservation: {name}")
        if len(core[1]) <= 55:
            require(inertia(line_matrix(core)) == new_line,
                    f"literal output line graph: {name}")
            direct_outputs += 1
        maximum_order = max(maximum_order, core[0])
        maximum_edges = max(maximum_edges, len(core[1]))
    return {"named_adversarial_inputs": len(cases),
            "literal_output_line_graphs": direct_outputs,
            "maximum_output_order": maximum_order,
            "maximum_output_edges": maximum_edges}


def nullspace(rows, width):
    reduced = [[Fraction(value) for value in row] for row in rows]
    pivot_columns = []
    pivot_row = 0
    for column in range(width):
        found = next((row for row in range(pivot_row, len(reduced))
                      if reduced[row][column]), None)
        if found is None:
            continue
        reduced[pivot_row], reduced[found] = reduced[found], reduced[pivot_row]
        scale = reduced[pivot_row][column]
        reduced[pivot_row] = [value / scale for value in reduced[pivot_row]]
        for row in range(len(reduced)):
            if row != pivot_row and reduced[row][column]:
                factor = reduced[row][column]
                reduced[row] = [x - factor * y
                                for x, y in zip(reduced[row], reduced[pivot_row])]
        pivot_columns.append(column)
        pivot_row += 1
    free = [column for column in range(width) if column not in pivot_columns]
    basis = []
    for column in free:
        vector = [Fraction(0)] * width
        vector[column] = 1
        for row, pivot in enumerate(pivot_columns):
            vector[pivot] = -reduced[row][column]
        basis.append(vector)
    return basis, len(pivot_columns)


def realize_kernel(branches, paths):
    degrees = [0] * branches
    edges = []
    order = branches
    for u, v, length in paths:
        require(length >= (3 if u == v else 2), "simple realization length")
        degrees[u] += 1
        degrees[v] += 1
        route = [u] + list(range(order, order + length - 1)) + [v]
        order += length - 1
        edges += list(zip(route, route[1:]))
    require(all(degree == 3 for degree in degrees), "noncubic pseudokernel")
    return graph(order, edges)


def parity_prediction(branches, paths):
    p = [[int(i == j) for j in range(branches)] for i in range(branches)]
    constraints = []
    q = 0
    for u, v, length in paths:
        q += (length - 1) // 2
        residue = length % 4
        if residue in (1, 3):
            sign = 1 if residue == 1 else -1
            p[u][v] += sign
            p[v][u] += sign
        else:
            row = [0] * branches
            row[u] += 1
            row[v] += -1 if residue == 0 else 1
            constraints.append(row)
    basis, rank = nullspace(constraints, branches)
    restricted = [[sum(basis[u][i] * p[i][j] * basis[v][j]
                       for i in range(branches) for j in range(branches))
                   for v in range(len(basis))] for u in range(len(basis))]
    small = inertia(restricted)
    return add_inertia(small, (q + rank, len(constraints) - rank, q + rank)), small


def residue_length(u, v, residue, extra=0):
    base = {0: 4, 1: 5, 2: 6 if u == v else 2, 3: 3}[residue]
    return base + 4 * extra


def audit_parity_dependency():
    kernels = [
        (2, [(0, 1), (0, 1), (0, 1)]),
        (2, [(0, 0), (0, 1), (1, 1)]),
        (4, list(combinations(range(4), 2))),
        (4, [(0, 0), (0, 1), (1, 2), (1, 2), (2, 3), (3, 3)]),
    ]
    checked = line_checked = 0
    for index, (branches, edges) in enumerate(kernels):
        if len(edges) == 3:
            assignments = list(product(range(4), repeat=3))
        else:
            assignments = [tuple((seed * (i + 1) + i * i + index) % 4
                                 for i in range(len(edges))) for seed in range(64)]
        for case, residues in enumerate(assignments):
            paths = [(u, v, residue_length(u, v, residue,
                                           extra=int((case + i) % 17 == 0)))
                     for i, ((u, v), residue) in enumerate(zip(edges, residues))]
            realized = realize_kernel(branches, paths)
            predicted, restricted = parity_prediction(branches, paths)
            actual = inertia(vertex_matrix(realized))
            require(actual == predicted, "parity-kernel shifted inertia")
            c = cyclomatic(realized)
            line_signature = line_inertia_from_vertex(realized)
            require(line_signature[0] - line_signature[2] ==
                    restricted[0] - restricted[2] - c + 1,
                    "parity-kernel line signature")
            if case % 23 == 0:
                require(inertia(line_matrix(realized)) == line_signature,
                        "literal parity-kernel line graph")
                line_checked += 1
            require(realized[0] <= 15 * c - 14 + 4 * len(edges),
                    "long-path sanity bound")
            checked += 1
    return {"loop_parallel_and_K4_cases": checked,
            "literal_line_graph_cases": line_checked}


def four_subdivide(g, edge):
    order, edges = g
    edge = tuple(sorted(edge))
    require(edge in edges, "subdivision edge absent")
    u, v = edge
    route = [u, order, order + 1, order + 2, order + 3, v]
    return graph(order + 4, [item for item in edges if item != edge] +
                 list(zip(route, route[1:])))


def audit_four_subdivision():
    hosts = [path_graph(5), cycle_graph(3), cycle_graph(4), complete_graph(4), star_graph(4)]
    cases = 0
    for host in hosts:
        old_vertex = inertia(vertex_matrix(host))
        old_line = inertia(line_matrix(host))
        for edge in host[1]:
            enlarged = four_subdivide(host, edge)
            require(inertia(vertex_matrix(enlarged)) == add_inertia(old_vertex, (2, 0, 2)),
                    "four-subdivision shifted inertia")
            require(inertia(line_matrix(enlarged)) == add_inertia(old_line, (2, 0, 2)),
                    "four-subdivision line inertia")
            cases += 1
    # The internal P4 block has the claimed response entries.
    p4 = [[int(abs(i - j) == 1) for j in range(4)] for i in range(4)]
    inverse_first = [Fraction(0), Fraction(1), Fraction(0), Fraction(-1)]
    require([sum(Fraction(x) * y for x, y in zip(row, inverse_first)) for row in p4] ==
            [Fraction(1), Fraction(0), Fraction(0), Fraction(0)], "P4 inverse column")
    require(inverse_first[0] == 0 and inverse_first[3] == -1, "P4 endpoint response")
    return {"all_edges_of_five_hosts": cases, "P4_endpoint_diagonal": "0",
            "P4_endpoint_cross": "-1"}


def main():
    output = {
        "target": {"artifact_ref": TARGET_REF, "commit": TARGET_COMMIT},
        "arithmetic": "Python integers and fractions.Fraction; no floating point",
        "universal_split": verify_universal_split_polynomial(),
        "module": audit_module(),
        "split_instances": audit_splits(),
        "full_reductions": audit_full_reductions(),
        "parity_dependency": audit_parity_dependency(),
        "four_subdivision": audit_four_subdivision(),
    }
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
