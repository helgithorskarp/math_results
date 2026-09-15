#!/usr/bin/env python3
"""Build the exact all-golden-edge unit-lens completion of Parts's 16 points.

Coordinates are elements of Q(zeta_5), stored in the power basis
1,zeta,zeta^2,zeta^3.  A stored point p represents the physical point q*p,
where q=1/|1-zeta|.  Thus a physical unit edge is characterized exactly by
N(p-r)=N(1-zeta).
"""

from collections import Counter, defaultdict, deque
from fractions import Fraction as F
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent

ZERO = (F(0),) * 4
ONE = (F(1), F(0), F(0), F(0))
ZETA = (F(0), F(1), F(0), F(0))


def add(a, b):
    return tuple(x + y for x, y in zip(a, b))


def neg(a):
    return tuple(-x for x in a)


def sub(a, b):
    return add(a, neg(b))


def mul(a, b):
    """Multiply modulo 1+x+x^2+x^3+x^4."""
    coefficients = [F(0)] * 7
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            coefficients[i + j] += x * y
    for degree in range(6, 3, -1):
        value = coefficients[degree]
        for offset in range(1, 5):
            coefficients[degree - offset] -= value
    return tuple(coefficients[:4])


def power(a, exponent):
    result = ONE
    while exponent:
        if exponent & 1:
            result = mul(result, a)
        a = mul(a, a)
        exponent //= 2
    return result


def conjugate(a):
    c0, c1, c2, c3 = a
    return (c0 - c1, -c1, -c1 + c3, -c1 + c2)


def norm(a):
    return mul(a, conjugate(a))


def inverse(a):
    columns = [mul(a, power(ZETA, exponent)) for exponent in range(4)]
    matrix = [
        [columns[column][row] for column in range(4)] + [ONE[row]]
        for row in range(4)
    ]
    for column in range(4):
        pivot = next(row for row in range(column, 4) if matrix[row][column])
        matrix[column], matrix[pivot] = matrix[pivot], matrix[column]
        value = matrix[column][column]
        matrix[column] = [entry / value for entry in matrix[column]]
        for row in range(4):
            if row == column:
                continue
            value = matrix[row][column]
            if value:
                matrix[row] = [
                    entry - value * pivot_entry
                    for entry, pivot_entry in zip(matrix[row], matrix[column])
                ]
    answer = tuple(matrix[row][4] for row in range(4))
    assert mul(a, answer) == ONE
    return answer


PHI = (F(0), F(0), F(-1), F(-1))
PHI_SQUARED = add(PHI, ONE)
UNIT_NORM = norm(sub(ONE, ZETA))
GOLDEN_NORM = mul(PHI_SQUARED, UNIT_NORM)

SOURCE_ROWS = (
    (0, 0, 0, 0, 5), (1, 0, 0, 0, 4),
    (0, 0, 0, 1, 4), (1, 0, 0, 1, 3),
    (0, 1, 0, 0, 4), (0, 0, 1, 0, 4),
    (1, 0, 1, 0, 3), (0, 1, 0, 1, 3),
    (1, 1, 0, 0, 3), (0, 0, 1, 1, 3),
    (1, 1, 0, 1, 2), (1, 0, 1, 1, 2),
    (0, 1, 1, 0, 3), (1, 1, 1, 0, 2),
    (0, 1, 1, 1, 2), (1, 1, 1, 1, 1),
)

POWERS = tuple(power(ZETA, exponent) for exponent in range(5))
SOURCE = tuple(
    tuple(
        sum(F(coefficient) * POWERS[exponent][coordinate]
            for exponent, coefficient in enumerate(row))
        for coordinate in range(4)
    )
    for row in SOURCE_ROWS
)


def distance_edges(points, target_norm):
    return tuple(
        (left, right)
        for left, right in combinations(range(len(points)), 2)
        if norm(sub(points[right], points[left])) == target_norm
    )


def digest_rows(rows):
    digest = sha256()
    for row in rows:
        digest.update((" ".join(map(str, row)) + "\n").encode())
    return digest.hexdigest()


def canonical_address(address):
    return ":".join(map(str, address))


def build():
    source_unit_edges = distance_edges(SOURCE, UNIT_NORM)
    source_golden_edges = distance_edges(SOURCE, GOLDEN_NORM)
    assert len(source_unit_edges) == len(source_golden_edges) == 28

    # If |b-a|=phi, the two intersections of the unit circles about a,b are
    # a + phi^-1 exp(+-pi*i/5)(b-a).  In Q(zeta_5), exp(pi*i/5)=-zeta^3
    # and exp(-pi*i/5)=-zeta^2.
    inverse_phi = inverse(PHI)
    multipliers = (
        ("plus", mul(inverse_phi, neg(power(ZETA, 3)))),
        ("minus", mul(inverse_phi, neg(power(ZETA, 2)))),
    )

    points = []
    index = {}
    addresses = defaultdict(list)

    def insert(point, address):
        if point not in index:
            index[point] = len(points)
            points.append(point)
        addresses[index[point]].append(address)
        return index[point]

    for source_index, point in enumerate(SOURCE):
        insert(point, ("source", source_index))

    prescribed = set(source_unit_edges)
    for left, right in source_golden_edges:
        difference = sub(SOURCE[right], SOURCE[left])
        for sign, multiplier in multipliers:
            point = add(SOURCE[left], mul(multiplier, difference))
            lens_index = insert(point, ("lens", left, right, sign))
            assert norm(sub(point, SOURCE[left])) == UNIT_NORM
            assert norm(sub(point, SOURCE[right])) == UNIT_NORM
            prescribed.add(tuple(sorted((left, lens_index))))
            prescribed.add(tuple(sorted((right, lens_index))))

    all_edges = set(distance_edges(points, UNIT_NORM))
    assert prescribed <= all_edges
    assert len(points) == 40
    assert len(all_edges) == 92
    assert len(prescribed) == 76

    return {
        "points": tuple(points),
        "edges": tuple(sorted(all_edges)),
        "source_unit_edges": source_unit_edges,
        "source_golden_edges": source_golden_edges,
        "prescribed_edges": tuple(sorted(prescribed)),
        "addresses": tuple(
            tuple(canonical_address(address) for address in addresses[i])
            for i in range(len(points))
        ),
        "multipliers": multipliers,
    }


def colour_graph(vertices, edges, colours):
    adjacency = [set() for _ in range(vertices)]
    for left, right in edges:
        adjacency[left].add(right)
        adjacency[right].add(left)
    row = [-1] * vertices
    nodes = 0

    def search(done):
        nonlocal nodes
        nodes += 1
        if done == vertices:
            return True
        candidates = []
        for vertex in range(vertices):
            if row[vertex] >= 0:
                continue
            used = {row[neighbour] for neighbour in adjacency[vertex]
                    if row[neighbour] >= 0}
            candidates.append((len(used), len(adjacency[vertex]), -vertex,
                               vertex, used))
        _sat, _degree, _negative_vertex, vertex, used = max(candidates)
        for colour in range(colours):
            if colour not in used:
                row[vertex] = colour
                if search(done + 1):
                    return True
        row[vertex] = -1
        return False

    answer = tuple(row) if search(0) else None
    return answer, nodes


def shortest_odd_closed_walk(vertices, edges):
    adjacency = [set() for _ in range(vertices)]
    for left, right in edges:
        adjacency[left].add(right)
        adjacency[right].add(left)
    best = None
    for start in range(vertices):
        distance = [[-1, -1] for _ in range(vertices)]
        parent = [[None, None] for _ in range(vertices)]
        distance[start][0] = 0
        queue = deque([(start, 0)])
        while queue:
            vertex, parity = queue.popleft()
            for neighbour in adjacency[vertex]:
                new_parity = parity ^ 1
                if distance[neighbour][new_parity] < 0:
                    distance[neighbour][new_parity] = distance[vertex][parity] + 1
                    parent[neighbour][new_parity] = (vertex, parity)
                    queue.append((neighbour, new_parity))
        if distance[start][1] >= 0 and (
                best is None or distance[start][1] < best[0]):
            walk = []
            state = (start, 1)
            while state is not None:
                walk.append(state[0])
                state = parent[state[0]][state[1]]
            best = (distance[start][1], tuple(reversed(walk)))
    assert best is not None
    return best[1]


def main():
    graph = build()
    points = graph["points"]
    edges = graph["edges"]
    two_colouring, two_nodes = colour_graph(len(points), edges, 2)
    three_colouring, three_nodes = colour_graph(len(points), edges, 3)
    assert two_colouring is None
    assert three_colouring is not None
    assert all(three_colouring[left] != three_colouring[right]
               for left, right in edges)
    odd_cycle = shortest_odd_closed_walk(len(points), edges)
    assert len(odd_cycle) == 6 and odd_cycle[0] == odd_cycle[-1]
    assert all(tuple(sorted(pair)) in set(edges)
               for pair in zip(odd_cycle, odd_cycle[1:]))

    address_multiplicities = Counter(map(len, graph["addresses"]))
    triangle_count = sum(
        {(a, b), (a, c), (b, c)} <= set(edges)
        for a, b, c in combinations(range(len(points)), 3)
    )
    certificate = {
        "claim_scope": "fixed all-golden-edge two-lens completion only",
        "candidate_status": False,
        "record_progress": False,
        "coordinate_model": (
            "point (a,b,c,d) means q*(a+b*zeta+c*zeta^2+d*zeta^3), "
            "zeta=exp(2*pi*i/5), q=1/|1-zeta|"
        ),
        "source_vertices": 16,
        "source_unit_edges": [list(edge) for edge in graph["source_unit_edges"]],
        "source_golden_edges": [list(edge) for edge in graph["source_golden_edges"]],
        "raw_addresses": 72,
        "raw_lens_addresses": 56,
        "distinct_points": len(points),
        "new_distinct_points": len(points) - 16,
        "distinct_lens_locations": sum(
            any(address.startswith("lens:") for address in row)
            for row in graph["addresses"]
        ),
        "source_lens_collision_locations": sum(
            any(address.startswith("source:") for address in row)
            and any(address.startswith("lens:") for address in row)
            for row in graph["addresses"]
        ),
        "address_multiplicity_histogram": {
            str(key): address_multiplicities[key]
            for key in sorted(address_multiplicities)
        },
        "complete_unit_edges": len(edges),
        "prescribed_distinct_edges": len(graph["prescribed_edges"]),
        "incidental_unit_edges": len(set(edges) - set(graph["prescribed_edges"])),
        "triangle_count": triangle_count,
        "chromatic_number": 3,
        "two_colour_search_nodes": two_nodes,
        "three_colour_search_nodes": three_nodes,
        "odd_cycle": list(odd_cycle),
        "three_colouring": list(three_colouring),
        "coordinates_power_basis": [list(map(int, point)) for point in points],
        "addresses": [list(row) for row in graph["addresses"]],
        "unit_edges": [list(edge) for edge in edges],
        "point_sha256": digest_rows(points),
        "edge_sha256": digest_rows(edges),
    }
    path = HERE / "certificate.json"
    path.write_text(json.dumps(certificate, indent=2, sort_keys=True) + "\n")
    summary = {key: certificate[key] for key in (
        "claim_scope", "candidate_status", "record_progress", "raw_addresses",
        "distinct_points", "complete_unit_edges", "prescribed_distinct_edges",
        "incidental_unit_edges", "triangle_count", "chromatic_number",
        "odd_cycle", "point_sha256", "edge_sha256",
    )}
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
