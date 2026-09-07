"""Exact existence/uniqueness certificate for the pinned 17-point seed."""
import json
from fractions import Fraction as F
from itertools import combinations
from pathlib import Path
from intervals import I, squared_distance

HERE = Path(__file__).resolve().parent
RADIUS = F(1, 10**18)


def require(test, message):
    if not test:
        raise ValueError(message)


def inverse(matrix):
    n = len(matrix)
    a = [list(row) + [F(i == j) for j in range(n)] for i, row in enumerate(matrix)]
    for j in range(n):
        k = next((k for k in range(j, n) if a[k][j]), None)
        require(k is not None, 'singular midpoint Jacobian')
        a[j], a[k] = a[k], a[j]
        pivot = a[j][j]
        a[j] = [x / pivot for x in a[j]]
        for k in range(n):
            if k != j and a[k][j]:
                scale = a[k][j]
                a[k] = [x - scale * y for x, y in zip(a[k], a[j])]
    return [row[n:] for row in a]


def dot(a, b):
    return sum((x * y for x, y in zip(a, b)), F(0))


def three_colour_search(edges):
    """Direct exhaustive DSATUR; pinned edge removes colour-name symmetry."""
    neighbours = [set() for _ in range(17)]
    for u, v in edges:
        neighbours[u].add(v)
        neighbours[v].add(u)
    colours = [-1] * 17
    colours[10], colours[16] = 0, 1
    nodes = 0

    def visit():
        nonlocal nodes
        nodes += 1
        left = [v for v in range(17) if colours[v] < 0]
        if not left:
            return True
        forbidden = {v: {colours[w] for w in neighbours[v] if colours[w] >= 0} for v in left}
        v = max(left, key=lambda v: (len(forbidden[v]), len(neighbours[v]), -v))
        for c in range(3):
            if c not in forbidden[v]:
                colours[v] = c
                if visit():
                    return True
        colours[v] = -1
        return False

    require(not visit(), 'seed unexpectedly three-colourable')
    return nodes


def certify(midpoint=None, edges=None, radius=RADIUS):
    if midpoint is None:
        midpoint = [[F(s) for s in row] for row in json.loads((HERE / 'seed_midpoint.json').read_text())]
    if edges is None:
        edges = [tuple(e) for e in json.loads((HERE / 'seed_edges.json').read_text())]
    require(len(midpoint) == 17 and all(len(row) == 2 for row in midpoint), 'midpoint shape')
    require(midpoint[10] == [F(-1), F(0)] and midpoint[16] == [F(0), F(0)], 'pinned edge')
    require(radius > 0, 'positive radius')
    require(len(edges) == len(set(edges)) == 31, '31 distinct edges required')
    require(all(0 <= u < v < 17 for u, v in edges) and (10, 16) in edges, 'edge labels')
    variables = [(v, d) for v in range(17) if v not in (10, 16) for d in range(2)]
    index = {x: i for i, x in enumerate(variables)}
    equations = [e for e in edges if e != (10, 16)]
    residuals, jacobian = [], []
    for u, v in equations:
        delta = [midpoint[u][d] - midpoint[v][d] for d in range(2)]
        residuals.append(dot(delta, delta) - 1)
        row = [F(0)] * 30
        for d in range(2):
            if (u, d) in index:
                row[index[u, d]] = 2 * delta[d]
            if (v, d) in index:
                row[index[v, d]] = -2 * delta[d]
        jacobian.append(row)
    inv = inverse(jacobian)
    # Check the inverse identity independently of elimination's internal state.
    for i in range(30):
        for j in range(30):
            require(dot(inv[i], [row[j] for row in jacobian]) == (i == j), 'inverse identity')
    norm_inv = max(sum(abs(x) for x in row) for row in inv)
    correction = max(abs(dot(row, residuals)) for row in inv)
    require(norm_inv < 20 and correction < F(1,10**24), 'documented root bounds')
    # Each Jacobian row has at most 4 nonzero entries, each varying by <=4r.
    lipschitz = 16 * radius * norm_inv
    require(lipschitz < 1, 'contraction bound')
    require(correction + lipschitz * radius < radius, 'root self-mapping bound')
    points = []
    for v, row in enumerate(midpoint):
        r = F(0) if v in (10, 16) else radius
        points.append(tuple(I(I.rational(x-r).lo, I.rational(x+r).hi) for x in row))
    edge_set = set(edges)
    for u, v in combinations(range(17), 2):
        d = squared_distance(points[u], points[v])
        require(d.lo > 0, 'seed points not certified distinct')
        if (u, v) not in edge_set:
            require(not d.contains(1), 'seed nonedge not excluded')
    require(not any((a,b) in edge_set and (a,c) in edge_set and (b,c) in edge_set
                    for a,b,c in combinations(range(17),3)), 'seed triangle')
    nodes = three_colour_search(edges)
    # Compact outward scalar bounds; the assertions above use exact Fractions.
    def ceil_scaled(x, scale):
        return -((-x.numerator * scale) // x.denominator)
    report = dict(vertices=17, edges=31, free_variables=30,
                  radius=str(radius), inverse_norm_ceiling=ceil_scaled(norm_inv, 1),
                  correction_upper_units_1e_minus_24=ceil_scaled(correction,10**24),
                  lipschitz_upper_units_1e_minus_12=ceil_scaled(lipschitz,10**12),
                  three_colour_exhaustion_nodes=nodes, triangle_free=True,
                  faithful=True, exact_unique_root=True)
    return points, report


if __name__ == '__main__':
    print(json.dumps(certify()[1], sort_keys=True, indent=2))
