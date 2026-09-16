"""Exact frozen two-frame address patch in Q(zeta_42,sqrt(5))."""

from __future__ import annotations

from fractions import Fraction as Q
from hashlib import sha256
import importlib.util
from pathlib import Path

HERE = Path(__file__).resolve().parent
GEOMETRY = HERE.parent / "hadwiger_nelson_heptagon_difference_lifts/geometry.py"
GEOMETRY_SHA256 = "67599414c9cabc9e1e9f0100907c3c039200deea4ffd935cb6ba09d67c57ef07"


def require(condition, message):
    if not condition:
        raise ValueError(message)


require(sha256(GEOMETRY.read_bytes()).hexdigest() == GEOMETRY_SHA256, "pinned heptagon geometry")
_spec = importlib.util.spec_from_file_location("hn_heptagon_geometry_two_frame", GEOMETRY)
F = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(F)


def eadd(x, y):
    return F.add(x[0], y[0]), F.add(x[1], y[1])


def esub(x, y):
    return F.sub(x[0], y[0]), F.sub(x[1], y[1])


def emul(x, y):
    return (
        F.add(F.mul(x[0], y[0]), F.scale(F.mul(x[1], y[1]), 5)),
        F.add(F.mul(x[0], y[1]), F.mul(x[1], y[0])),
    )


def econj(x):
    return F.conj(x[0]), F.conj(x[1])


def enorm(x):
    return emul(x, econj(x))


def embed(x):
    return x, F.ZERO


I_SQRT3 = F.sub(F.scale(F.POW[7], 2), F.ONE)
ALPHA = F.scale(F.ONE, Q(7, 8)), F.scale(I_SQRT3, Q(1, 8))
EONE = F.ONE, F.ZERO
EZERO = F.ZERO, F.ZERO


def rotate(x):
    return emul(ALPHA, embed(x))


def construction():
    host = F.host()
    normalized = [F.sub(x, host[0]) for x in host]
    patch = sorted({F.add(x, y) for x in normalized for y in normalized})
    require(len(host) == 21 and len(patch) == 231 and F.ZERO in patch, "source or patch order")
    translation = esub(esub(embed(patch[197]), rotate(patch[230])), embed(F.ONE))
    frame_a = [embed(x) for x in patch]
    frame_b = [eadd(rotate(x), translation) for x in patch]
    require(not (set(frame_a) & set(frame_b)), "frames must be disjoint")
    points = frame_a + frame_b
    require(len(points) == len(set(points)) == 462, "collision-merged order")
    return normalized, patch, translation, points


def eval_k(value, prime, root):
    total = 0
    power = 1
    for coefficient in value:
        total = (total + coefficient.numerator * pow(coefficient.denominator, -1, prime) * power) % prime
        power = power * root % prime
    return total


def modular_point(point, prime=1009, zeta84=527):
    root = zeta84 * zeta84 % prime
    a, b = point
    return (
        eval_k(a, prime, root),
        eval_k(b, prime, root),
        eval_k(F.conj(a), prime, root),
        eval_k(F.conj(b), prime, root),
    )


def complete_edges(points):
    """No-false-negative modular sieve followed by exact decisions."""
    prime, sqrt5 = 1009, 244
    require(pow(527, 84, prime) == 1 and pow(527, 42, prime) != 1, "zeta specialization")
    require(sqrt5 * sqrt5 % prime == 5, "sqrt5 specialization")
    modular = [modular_point(point, prime) for point in points]
    survivors = exact_rejects = 0
    edges = []
    for u in range(len(points)):
        a, b, ac, bc = modular[u]
        for v in range(u + 1, len(points)):
            c, d, cc, dc = modular[v]
            x, y = (a - c) % prime, (b - d) % prime
            xc, yc = (ac - cc) % prime, (bc - dc) % prime
            if (x * xc + 5 * y * yc) % prime != 1 or (x * yc + y * xc) % prime != 0:
                continue
            survivors += 1
            if enorm(esub(points[u], points[v])) == EONE:
                edges.append((u, v))
            else:
                exact_rejects += 1
    return edges, survivors, exact_rejects


def coordinate_line(point):
    def element(value):
        return ",".join(f"{x.numerator}/{x.denominator}" for x in value)
    return element(point[0]) + ";" + element(point[1]) + "\n"


def coordinate_hash(points):
    digest = sha256()
    for point in points:
        digest.update(coordinate_line(point).encode("ascii"))
    return digest.hexdigest()


def edge_hash(edges):
    return sha256("".join(f"{u} {v}\n" for u, v in edges).encode("ascii")).hexdigest()


def components(vertices, edges, removed=frozenset()):
    selected = set(vertices) - set(removed)
    adjacency = {v: set() for v in selected}
    for u, v in edges:
        if u in selected and v in selected:
            adjacency[u].add(v)
            adjacency[v].add(u)
    result = []
    while selected:
        root = min(selected)
        selected.remove(root)
        stack = [root]
        block = []
        while stack:
            u = stack.pop()
            block.append(u)
            found = adjacency[u] & selected
            selected.difference_update(found)
            stack.extend(found)
        result.append(sorted(block))
    return sorted(result, key=lambda block: (-len(block), block))
