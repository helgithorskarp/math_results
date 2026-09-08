"""Exact four-coordinate graph and spindle, with no forcing-gadget premises."""
import hashlib
import json
from itertools import combinations
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def require(condition, message):
    if not condition:
        raise ValueError(message)


def read(name):
    return json.loads((ROOT / name).read_text())


def rows():
    data = read('coordinates.json')
    require(type(data) is list and all(type(p) is list and len(p) == 4 and
            all(type(x) is int for x in p) for p in data), 'coordinate format')
    result = list(map(tuple, data))
    require(result == sorted(set(result)), 'coordinate order or collision')
    require((0, 0, 0, 0) in result and (0, 0, 96, 0) in result, 'missing terminal')
    return result


def norm(p):
    a, b, c, d = p
    return 3*a*a+11*b*b+c*c+33*d*d, 2*(a*b+c*d)


def half_edges(points):
    return [(i, j) for i, j in combinations(range(len(points)), 2)
            if norm(tuple(x-y for x, y in zip(points[i], points[j]))) == (1296, 0)]


def cross(p, q):
    """Whether p and Rq are unit-separated, without floating-point rotations."""
    a, b, c, d = p
    A, B, C, D = q
    n0, n1 = norm(p)
    m0, m1 = norm(q)
    dot0 = 3*a*A+11*b*B+c*C+33*d*D
    dot1 = a*B+b*A+c*D+d*C
    cross3 = c*A+11*d*B-a*C-11*b*D
    cross11 = c*B+3*d*A-b*C-3*a*D
    return (cross3 == cross11 == 0 and
            64*(n0+m0)-119*dot0 == 82944 and 64*(n1+m1)-119*dot1 == 0)


def spindle(points):
    n = len(points)
    origin = points.index((0, 0, 0, 0))
    labels = {origin: origin}
    for i in range(n):
        if i != origin:
            labels[i] = n+len(labels)-1
    edges = set(half_edges(points))
    edges.update(tuple(sorted((labels[a], labels[b]))) for a, b in list(edges))
    cross_edges = {(i, labels[j]) for i, p in enumerate(points)
                   for j, q in enumerate(points) if j != origin and cross(p, q)}
    edges.update(cross_edges)
    return sorted(edges), labels, sorted(cross_edges)


def cnf(n, edges, pins):
    clauses = []
    for v in range(n):
        clauses.append([4*v+c+1 for c in range(4)])
        clauses.extend([-(4*v+c+1), -(4*v+d+1)] for c, d in combinations(range(4), 2))
    for u, v in edges:
        clauses.extend([-(4*u+c+1), -(4*v+c+1)] for c in range(4))
    clauses.extend([[4*pins[0]+1], [4*pins[1]+2]])
    return clauses


def dimacs(n, clauses):
    return f'p cnf {4*n} {len(clauses)}\n' + ''.join(' '.join(map(str, c))+' 0\n' for c in clauses)


def digest(value):
    return hashlib.sha256(json.dumps(value, separators=(',', ':')).encode()).hexdigest()
