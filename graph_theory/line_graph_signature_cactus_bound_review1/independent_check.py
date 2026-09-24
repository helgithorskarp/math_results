#!/usr/bin/env python3
"""Independent exact audit for the sharp cactus line-graph signature bound.

This standard-library checker imports no code from the reviewed package.
It uses exact rational congruence, definition-level graph matrices, a
different cactus generator, and transition tests stated directly in terms
of the charged response invariant.
"""

from fractions import Fraction
from itertools import combinations, product
import hashlib
import json
import random


TARGET_REF = "bafkreifjkblukdlkejmx6xqonhwi2thsq34q7acbpcvejth2rrjqcnzxe4"
TARGET_COMMIT = "8422a9e7e4b9c6c2ae90ec8d1c912c4ba9d1124d"


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def graph(order, edges):
    normalized = tuple(sorted(tuple(sorted(edge)) for edge in edges))
    require(order >= 1, "positive graph order required")
    require(len(normalized) == len(set(normalized)), "duplicate edge")
    require(all(0 <= u < v < order for u, v in normalized), "invalid simple edge")
    return order, normalized


def adjacency(g):
    rows = [set() for _ in range(g[0])]
    for u, v in g[1]:
        rows[u].add(v)
        rows[v].add(u)
    return rows


def connected(g):
    rows = adjacency(g)
    seen = {0}
    todo = [0]
    while todo:
        for vertex in rows[todo.pop()]:
            if vertex not in seen:
                seen.add(vertex)
                todo.append(vertex)
    return len(seen) == g[0]


def cyclomatic(g):
    require(connected(g), "connected graph required")
    return len(g[1]) - g[0] + 1


def blocks(g):
    """Return edge-biconnected blocks by an independently written DFS."""
    require(connected(g), "block decomposition requires connectivity")
    rows = adjacency(g)
    discovery = [-1] * g[0]
    low = [0] * g[0]
    stack = []
    result = []
    clock = 0

    def visit(vertex, parent):
        nonlocal clock
        discovery[vertex] = low[vertex] = clock
        clock += 1
        for other in sorted(rows[vertex]):
            edge = tuple(sorted((vertex, other)))
            if discovery[other] < 0:
                stack.append(edge)
                visit(other, vertex)
                low[vertex] = min(low[vertex], low[other])
                if low[other] >= discovery[vertex]:
                    block = []
                    while True:
                        item = stack.pop()
                        block.append(item)
                        if item == edge:
                            break
                    result.append(tuple(sorted(block)))
            elif other != parent and discovery[other] < discovery[vertex]:
                stack.append(edge)
                low[vertex] = min(low[vertex], discovery[other])

    visit(0, -1)
    require(not stack, "unfinished block stack")
    return tuple(sorted(result))


def is_cactus(g):
    if not connected(g):
        return False
    for block in blocks(g):
        if len(block) == 1:
            continue
        degrees = {}
        for u, v in block:
            degrees[u] = degrees.get(u, 0) + 1
            degrees[v] = degrees.get(v, 0) + 1
        if len(block) != len(degrees) or any(value != 2 for value in degrees.values()):
            return False
    return True


def cycle_vertices(g):
    return {vertex for block in blocks(g) if len(block) > 1
            for edge in block for vertex in edge}


def shifted_matrix(g, root=None):
    matrix = [[0] * g[0] for _ in range(g[0])]
    for vertex in range(g[0]):
        matrix[vertex][vertex] = -2 + int(vertex == root)
    for u, v in g[1]:
        matrix[u][u] += 1
        matrix[v][v] += 1
        matrix[u][v] = matrix[v][u] = 1
    return matrix


def line_matrix(g):
    sets = [set(edge) for edge in g[1]]
    return [[int(i != j and bool(left & right)) for j, right in enumerate(sets)]
            for i, left in enumerate(sets)]


def inertia(matrix):
    """Exact inertia by repeated scalar or two-coordinate Schur complements."""
    size = len(matrix)
    require(all(len(row) == size for row in matrix), "square matrix required")
    require(all(matrix[i][j] == matrix[j][i] for i in range(size) for j in range(i)),
            "symmetric matrix required")
    current = [[Fraction(entry) for entry in row] for row in matrix]
    positive = zero = negative = 0
    while current:
        size = len(current)
        pivot_index = next((i for i in range(size) if current[i][i]), None)
        if pivot_index is not None:
            order = [pivot_index] + [i for i in range(size) if i != pivot_index]
            current = [[current[i][j] for j in order] for i in order]
            pivot = current[0][0]
            positive += int(pivot > 0)
            negative += int(pivot < 0)
            current = [[current[i][j] - current[i][0] * current[0][j] / pivot
                        for j in range(1, size)] for i in range(1, size)]
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


def response(matrix, root=0):
    """Return e_root^T x for Ax=e_root, or None when e_root is not in im A."""
    size = len(matrix)
    augmented = [[Fraction(value) for value in row] + [Fraction(i == root)]
                 for i, row in enumerate(matrix)]
    pivot_columns = []
    row = 0
    for column in range(size):
        found = next((i for i in range(row, size) if augmented[i][column]), None)
        if found is None:
            continue
        augmented[row], augmented[found] = augmented[found], augmented[row]
        pivot = augmented[row][column]
        augmented[row] = [value / pivot for value in augmented[row]]
        for i in range(size):
            if i != row and augmented[i][column]:
                factor = augmented[i][column]
                augmented[i] = [x - factor * y
                                for x, y in zip(augmented[i], augmented[row])]
        pivot_columns.append(column)
        row += 1
    if any(not any(row[:size]) and row[size] for row in augmented):
        return None
    solution = [Fraction(0)] * size
    for i, column in enumerate(pivot_columns):
        solution[column] = augmented[i][size]
    require(all(sum(Fraction(matrix[i][j]) * solution[j] for j in range(size)) ==
                Fraction(i == root) for i in range(size)), "root response solve failed")
    return solution[root]


def signature(values):
    return values[0] - values[2]


def digest_update(digest, value):
    digest.update(json.dumps(value, sort_keys=True, separators=(",", ":")).encode() + b"\n")


def check_cactus_bound(g, literal_line=False):
    require(is_cactus(g), "generated graph is not a cactus")
    c = cyclomatic(g)
    vertex_inertia = inertia(shifted_matrix(g))
    line_signature = signature(vertex_inertia) - c + 1
    require(2 * line_signature <= c + 1, "cactus bound failed")
    if literal_line:
        direct = inertia(line_matrix(g))
        require(signature(direct) == line_signature, "incidence/line signature mismatch")
        require(direct == (vertex_inertia[0], vertex_inertia[1],
                           vertex_inertia[2] + c - 1), "full line inertia mismatch")
    return vertex_inertia, line_signature


def attach_leaf(g, vertex):
    return graph(g[0] + 1, list(g[1]) + [(vertex, g[0])])


def attach_cycle(g, vertex, length):
    require(length >= 3, "cycle too short")
    route = [vertex] + list(range(g[0], g[0] + length - 1)) + [vertex]
    return graph(g[0] + length - 1, list(g[1]) + list(zip(route, route[1:])))


MODULE = ((0, 1), (1, 2), (2, 3), (0, 3),
          (4, 5), (5, 6), (6, 7), (7, 8), (4, 8), (0, 4), (1, 9))


def attach_module(g, vertex):
    labels = list(range(g[0], g[0] + 9)) + [vertex]
    return graph(g[0] + 9, list(g[1]) + [(labels[u], labels[v]) for u, v in MODULE])


def path_matrix(diagonal, cycle=False):
    size = len(diagonal)
    matrix = [[Fraction(0)] * size for _ in range(size)]
    for i, value in enumerate(diagonal):
        matrix[i][i] = Fraction(value)
    for i in range(size - 1):
        matrix[i][i + 1] = matrix[i + 1][i] = 1
    if cycle:
        require(size >= 3, "cycle matrix too short")
        matrix[0][-1] = matrix[-1][0] = 1
    return matrix


def audit_weighted_lemmas():
    digest = hashlib.sha256()
    paths = cycles = charged = 0
    for size in range(1, 6):
        for weights in product(range(4), repeat=size):
            values = inertia(path_matrix(weights))
            require(2 * signature(values) <= sum(weights) + 1, "weighted path lemma")
            digest_update(digest, ["path", weights, values])
            paths += 1
            if size >= 3:
                values = inertia(path_matrix(weights, cycle=True))
                require(2 * signature(values) <= sum(weights) + 2, "weighted cycle lemma")
                digest_update(digest, ["cycle", weights, values])
                cycles += 1
    rng = random.Random(918273645)
    for case in range(1200):
        size = rng.randrange(1, 18)
        charges = [rng.randrange(7) for _ in range(size)]
        diagonal = [rng.randrange(-15, charge + 1) if charge <= 2
                    else rng.randrange(-30, 31) for charge in charges]
        values = inertia(path_matrix(diagonal))
        require(2 * signature(values) <= sum(charges) + 1, "charged path lemma")
        digest_update(digest, ["charged_path", charges, diagonal, values])
        charged += 1
        if size >= 3:
            values = inertia(path_matrix(diagonal, cycle=True))
            require(2 * signature(values) <= sum(charges) + 2, "charged cycle lemma")
            if any(charge >= 3 for charge in charges):
                require(2 * signature(values) <= sum(charges),
                        "charged cycle deletion strengthening")
            digest_update(digest, ["charged_cycle", charges, diagonal, values])
            charged += 1
    return {"weights_0_through_3_paths": paths,
            "weights_0_through_3_cycles": cycles,
            "charged_random_path_cycle_cases": charged,
            "entrywise_sha256": digest.hexdigest()}


def validate_state(charge, rho):
    require(charge >= 0, "negative state charge")
    if rho is None:
        require(charge >= 1, "zero-charge pole")
    elif charge <= 2:
        require(rho >= 1 - charge, "response boundary failed")


STATE_PALETTE = (
    (0, Fraction(1)), (0, Fraction(3, 2)), (0, Fraction(7)),
    (1, Fraction(0)), (1, Fraction(1, 4)), (1, Fraction(4)),
    (2, Fraction(-1)), (2, Fraction(-1, 2)), (2, Fraction(0)), (2, Fraction(5)),
    (3, Fraction(-12)), (3, Fraction(-1)), (3, Fraction(0)), (3, Fraction(9)),
    (4, Fraction(-20)), (4, Fraction(2)), (5, Fraction(30)),
    (1, None), (2, None), (5, None),
)


def bridge_transition(children):
    total = sum(charge for charge, _ in children)
    if any(rho is None for _, rho in children):
        output = (total, Fraction(0))
    else:
        pivot = len(children) - 1 - sum((rho for _, rho in children), Fraction(0))
        if pivot > 0:
            output = (total - 2, 1 / pivot)
        elif pivot < 0:
            output = (total + 2, 1 / pivot)
        else:
            output = (total, None)
    validate_state(*output)
    return output


ABSENT = "absent"


def cycle_transition(children):
    size = len(children) + 1
    matrix = [[Fraction(0)] * size for _ in range(size)]
    matrix[0][0] = 1
    for i in range(size):
        matrix[i][(i + 1) % size] = 1
        matrix[(i + 1) % size][i] = 1
    total = 0
    poles = set()
    for i, child in enumerate(children, 1):
        if child == ABSENT:
            continue
        charge, rho = child
        total += charge
        if rho is None:
            poles.add(i)
        else:
            matrix[i][i] += 1 - rho
    keep = [i for i in range(size) if i not in poles]
    reduced = [[matrix[i][j] for j in keep] for i in keep]
    out_charge = 3 + total - 2 * signature(inertia(reduced))
    out_rho = response(reduced)
    validate_state(out_charge, out_rho)
    return out_charge, out_rho


def serialize_state(state):
    charge, rho = state
    return [charge, None if rho is None else str(rho)]


def audit_transitions():
    digest = hashlib.sha256()
    bridges = cycles = 0
    for arity in range(3):
        for children in product(STATE_PALETTE, repeat=arity):
            output = bridge_transition(children)
            digest_update(digest, ["bridge", [serialize_state(x) for x in children],
                                   serialize_state(output)])
            bridges += 1
    boundary = (ABSENT, (0, Fraction(1)), (1, Fraction(0)), (2, Fraction(-1)),
                (3, Fraction(-12)), (3, Fraction(9)), (1, None), (2, None),
                (5, None))
    for length in range(3, 5):
        for children in product(boundary, repeat=length - 1):
            output = cycle_transition(children)
            encoded = [x if x == ABSENT else serialize_state(x) for x in children]
            digest_update(digest, ["cycle", encoded, serialize_state(output)])
            cycles += 1
    rng = random.Random(2718281828)
    for _ in range(4000):
        arity = rng.randrange(4, 9)
        children = [STATE_PALETTE[rng.randrange(len(STATE_PALETTE))]
                    for _ in range(arity)]
        output = bridge_transition(children)
        digest_update(digest, ["bridge_sample", [serialize_state(x) for x in children],
                               serialize_state(output)])
        bridges += 1
    cycle_choices = (ABSENT,) + STATE_PALETTE
    for _ in range(4000):
        length = rng.randrange(3, 14)
        children = [cycle_choices[rng.randrange(len(cycle_choices))]
                    for _ in range(length - 1)]
        output = cycle_transition(children)
        encoded = [x if x == ABSENT else serialize_state(x) for x in children]
        digest_update(digest, ["cycle_sample", encoded, serialize_state(output)])
        cycles += 1
    return {"bridge_transitions": bridges, "cycle_transitions": cycles,
            "entrywise_sha256": digest.hexdigest()}


def prufer_tree(order, sequence):
    degrees = [1] * order
    for vertex in sequence:
        degrees[vertex] += 1
    edges = []
    for vertex in sequence:
        leaf = next(i for i, degree in enumerate(degrees) if degree == 1)
        edges.append((leaf, vertex))
        degrees[leaf] -= 1
        degrees[vertex] -= 1
    leaves = [i for i, degree in enumerate(degrees) if degree == 1]
    edges.append(tuple(leaves))
    return graph(order, edges)


def audit_seventh_order_trees():
    digest = hashlib.sha256()
    count = literal = 0
    for sequence in product(range(7), repeat=5):
        tree = prufer_tree(7, sequence)
        values, line_signature = check_cactus_bound(tree, literal_line=count % 997 == 0)
        require(line_signature <= 0, "tree line signature is positive")
        literal += count % 997 == 0
        digest_update(digest, [sequence, values, line_signature])
        count += 1
    require(count == 7 ** 5, "Pruefer coverage count")
    return {"all_labelled_trees_order_7": count, "literal_line_graphs": literal,
            "entrywise_sha256": digest.hexdigest()}


def generated_cacti():
    rng = random.Random(202609245911)
    result = []
    for index in range(100):
        g = graph(1, [])
        for step in range(5 + index % 6):
            vertex = 0 if (index + step) % 5 == 0 else rng.randrange(g[0])
            if rng.randrange(4) == 0:
                g = attach_leaf(g, vertex)
            else:
                g = attach_cycle(g, vertex, 3 + rng.randrange(7))
        for _ in range(index % 4):
            g = attach_leaf(g, 0)
        result.append(g)
    # Deterministic high-articulation bouquets and long block chains.
    for count in range(1, 8):
        bouquet = graph(1, [])
        chain = graph(1, [])
        tip = 0
        for i in range(count):
            length = 3 + (2 * i + count) % 7
            bouquet = attach_cycle(bouquet, 0, length)
            old_order = chain[0]
            chain = attach_cycle(chain, tip, length)
            tip = old_order + length - 2
        for _ in range(count // 2):
            bouquet = attach_leaf(bouquet, 0)
            chain = attach_leaf(chain, tip)
        result.extend((bouquet, chain))
    return result


def audit_adversarial_cacti():
    digest = hashlib.sha256()
    cases = generated_cacti()
    literal = maximum_order = maximum_edges = 0
    for index, g in enumerate(cases):
        values, line_signature = check_cactus_bound(g, literal_line=index % 16 == 0)
        literal += index % 16 == 0
        maximum_order = max(maximum_order, g[0])
        maximum_edges = max(maximum_edges, len(g[1]))
        digest_update(digest, [index, g[0], g[1], values, line_signature])
    return {"generated_cases": len(cases), "literal_line_graphs": literal,
            "maximum_order": maximum_order, "maximum_edges": maximum_edges,
            "entrywise_sha256": digest.hexdigest()}, cases


def random_subcubic_cactus(rng, steps):
    g = graph(1, [])
    for _ in range(steps):
        rows = adjacency(g)
        cycle_ports = [i for i, row in enumerate(rows) if len(row) <= 1]
        leaf_ports = [i for i, row in enumerate(rows) if len(row) <= 2]
        if cycle_ports and rng.randrange(3):
            g = attach_cycle(g, cycle_ports[rng.randrange(len(cycle_ports))],
                             3 + rng.randrange(6))
        elif leaf_ports:
            g = attach_leaf(g, leaf_ports[rng.randrange(len(leaf_ports))])
        else:
            break
    return g


def audit_direct_rooted_states():
    rng = random.Random(1414213562)
    digest = hashlib.sha256()
    graphs = roots = poles = singular = 0
    for index in range(70):
        g = random_subcubic_cactus(rng, 4 + index % 7)
        rows = adjacency(g)
        on_cycle = cycle_vertices(g)
        eligible = [i for i in range(g[0]) if i not in on_cycle or len(rows[i]) == 2]
        chosen = eligible if len(eligible) <= 4 else [eligible[i * (len(eligible) - 1) // 3]
                                                     for i in range(4)]
        for root in chosen:
            matrix = shifted_matrix(g, root)
            values = inertia(matrix)
            rho = response(matrix, root)
            charge = 3 * cyclomatic(g) - 2 * signature(values)
            validate_state(charge, rho)
            poles += rho is None
            singular += values[1] > 0
            digest_update(digest, [index, root, g[0], g[1], values, charge,
                                   None if rho is None else str(rho)])
            roots += 1
        graphs += 1
    return {"subcubic_cacti": graphs, "eligible_root_checks": roots,
            "pole_roots": poles, "singular_rooted_matrices": singular,
            "entrywise_sha256": digest.hexdigest()}


def components_without_vertex(g, deleted):
    rows = adjacency(g)
    remaining = set(range(g[0])) - {deleted}
    labels = {}
    component = 0
    while remaining:
        start = min(remaining)
        seen = {start}
        todo = [start]
        remaining.remove(start)
        while todo:
            for vertex in rows[todo.pop()] - {deleted}:
                if vertex not in seen:
                    seen.add(vertex)
                    remaining.remove(vertex)
                    todo.append(vertex)
        for vertex in seen:
            labels[vertex] = component
        component += 1
    return labels


def split_group(g, vertex):
    row = sorted(adjacency(g)[vertex])
    labels = components_without_vertex(g, vertex)
    same_cycle = next(((u, v) for u, v in combinations(row, 2)
                       if labels[u] == labels[v]), None)
    return same_cycle if same_cycle is not None else tuple(row[:2])


def split_vertex(g, vertex, group):
    group = set(group)
    order = g[0]
    second, p, q, r = order, order + 1, order + 2, order + 3
    edges = []
    for u, v in g[1]:
        if vertex not in (u, v):
            edges.append((u, v))
        else:
            other = v if u == vertex else u
            edges.append((vertex if other in group else second, other))
    edges += [(vertex, p), (p, q), (q, r), (r, second)]
    return graph(order + 4, edges)


def audit_degree_reduction():
    digest = hashlib.sha256()
    inputs = moves = outputs = 0
    fixtures = []
    for degree in range(4, 9):
        fixtures.append(graph(degree + 1, [(0, vertex) for vertex in range(1, degree + 1)]))
    for count in range(2, 6):
        bouquet = graph(1, [])
        for index in range(count):
            bouquet = attach_cycle(bouquet, 0, 3 + index % 3)
        fixtures.append(bouquet)
    mixed = attach_cycle(attach_cycle(attach_cycle(graph(1, []), 0, 3), 0, 4), 0, 5)
    for _ in range(4):
        mixed = attach_leaf(mixed, 0)
    fixtures.append(mixed)
    for index, original in enumerate(fixtures):
        current = original
        old_c = cyclomatic(current)
        while max(map(len, adjacency(current))) >= 4:
            rows = adjacency(current)
            vertex = next(i for i, row in enumerate(rows) if len(row) >= 4)
            group = split_group(current, vertex)
            old_inertia = inertia(shifted_matrix(current))
            enlarged = split_vertex(current, vertex, group)
            new_inertia = inertia(shifted_matrix(enlarged))
            require(new_inertia == (old_inertia[0] + 2, old_inertia[1],
                                    old_inertia[2] + 2), "split inertia increment")
            require(is_cactus(enlarged), "split did not preserve cactus")
            require(cyclomatic(enlarged) == old_c, "split changed cyclomatic number")
            digest_update(digest, [index, vertex, group, current[0], current[1],
                                   old_inertia, new_inertia])
            current = enlarged
            moves += 1
        cycle_occurrences = {}
        for block in blocks(current):
            if len(block) > 1:
                for edge in block:
                    for vertex in edge:
                        cycle_occurrences[vertex] = cycle_occurrences.get(vertex, 0) + 1
        require(all(count == 2 for count in cycle_occurrences.values()),
                "subcubic cycles are not vertex-disjoint")
        check_cactus_bound(current, literal_line=False)
        inputs += 1
        outputs += 1
    return {"high_degree_inputs": inputs, "exact_split_moves": moves,
            "subcubic_outputs": outputs, "entrywise_sha256": digest.hexdigest()}


def audit_sharpness():
    digest = hashlib.sha256()
    count = 0
    for parity in (0, 1):
        g = graph(1, []) if parity == 0 else attach_cycle(graph(1, []), 0, 5)
        for step in range(7):
            values = inertia(line_matrix(g))
            line_signature = signature(values)
            require(line_signature == (cyclomatic(g) + 1) // 2, "sharp witness")
            digest_update(digest, [cyclomatic(g), g[0], len(g[1]), values])
            count += 1
            g = attach_module(g, (2 * step + parity) % g[0])
    return {"witnesses": count, "cyclomatic_range": [0, 13],
            "entrywise_sha256": digest.hexdigest()}


def main():
    adversarial, _ = audit_adversarial_cacti()
    output = {
        "target": {"artifact_ref": TARGET_REF, "commit": TARGET_COMMIT},
        "arithmetic": "Python integers and fractions.Fraction; no floating point",
        "weighted_lemmas": audit_weighted_lemmas(),
        "abstract_transitions": audit_transitions(),
        "all_order_seven_trees": audit_seventh_order_trees(),
        "adversarial_cacti": adversarial,
        "direct_rooted_states": audit_direct_rooted_states(),
        "degree_reduction": audit_degree_reduction(),
        "sharpness": audit_sharpness(),
    }
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
