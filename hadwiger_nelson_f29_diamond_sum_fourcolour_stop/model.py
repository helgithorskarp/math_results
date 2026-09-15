#!/usr/bin/env python3
"""Exact geometry and finite colouring routines for the F29/diamond sum."""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction as Q
from itertools import combinations
import hashlib
import json


@dataclass(frozen=True)
class K:
    """a+b*sqrt(3)+c*sqrt(11)+d*sqrt(33)."""

    c: tuple[Q, Q, Q, Q]

    def __add__(self, other: "K") -> "K":
        return K(tuple(a + b for a, b in zip(self.c, other.c)))

    def __neg__(self) -> "K":
        return K(tuple(-a for a in self.c))

    def __sub__(self, other: "K") -> "K":
        return self + (-other)

    def __mul__(self, other: "K") -> "K":
        out = [Q(0)] * 4
        for i, a in enumerate(self.c):
            for j, b in enumerate(other.c):
                mask = i ^ j
                factor = (3 if i & j & 1 else 1) * (11 if i & j & 2 else 1)
                out[mask] += a * b * factor
        return K(tuple(out))

    def scale(self, q: Q | int) -> "K":
        return K(tuple(Q(q) * a for a in self.c))


K0 = K((Q(0),) * 4)
K1 = K((Q(1), Q(0), Q(0), Q(0)))
KS = K((Q(0), Q(1), Q(0), Q(0)))


@dataclass(frozen=True)
class L:
    """A+B*y over K, where y^2=(4-sqrt(3))/2."""

    a: K
    b: K

    def __add__(self, other: "L") -> "L":
        return L(self.a + other.a, self.b + other.b)

    def __neg__(self) -> "L":
        return L(-self.a, -self.b)

    def __sub__(self, other: "L") -> "L":
        return self + (-other)

    def __mul__(self, other: "L") -> "L":
        y2 = K1.scale(2) - KS.scale(Q(1, 2))
        return L(self.a * other.a + self.b * other.b * y2,
                 self.a * other.b + self.b * other.a)

    def scale(self, q: Q | int) -> "L":
        return L(self.a.scale(q), self.b.scale(q))


L0 = L(K0, K0)
L1 = L(K1, K0)
LS = L(KS, K0)
LY = L(K0, K1)
Point = tuple[L, L]


def point_add(p: Point, q: Point) -> Point:
    return p[0] + q[0], p[1] + q[1]


def point_mul(p: Point, q: Point) -> Point:
    return p[0] * q[0] - p[1] * q[1], p[0] * q[1] + p[1] * q[0]


def point_conj(p: Point) -> Point:
    return p[0], -p[1]


def point_scale(p: Point, q: Q | int) -> Point:
    return p[0].scale(q), p[1].scale(q)


def dist2(p: Point, q: Point) -> L:
    dx, dy = p[0] - q[0], p[1] - q[1]
    return dx * dx + dy * dy


def flat(x: L) -> tuple[str, ...]:
    return tuple(str(q) for q in x.a.c + x.b.c)


def digest(value) -> str:
    raw = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(raw).hexdigest()


def f29_points() -> list[Point]:
    """Reconstruct the selected 29 points from the seven Polymath16 cosets."""
    keep = (0, 5, 6, 9, 12, 13, 16, 17, 18, 19, 20, 22, 24, 25, 26,
            27, 28, 30, 31, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42)
    omega = (L1.scale(Q(1, 2)), LS.scale(Q(1, 2)))
    sqrt33 = L(K((Q(0), Q(0), Q(0), Q(1))), K0)
    eta = (sqrt33.scale(Q(1, 6)), LS.scale(Q(1, 6)))
    one = (L1, L0)
    zero = (L0, L0)
    powers = [one]
    for _ in range(5):
        powers.append(point_mul(powers[-1], omega))
    assert point_mul(powers[-1], omega) == one
    assert point_mul(eta, point_conj(eta)) == one
    eta_w2 = point_mul(eta, powers[2])
    seeds = [
        one,
        point_add(eta, point_scale(point_conj(eta), -1)),
        point_add(eta, point_scale(point_mul(point_conj(eta), omega), -1)),
        eta,
        point_add(one, eta_w2),
        point_conj(eta),
        point_add(one, point_conj(eta_w2)),
    ]
    pool = {point_mul(a, b) for a in seeds for b in powers}
    assert len(pool) == 42 and zero not in pool

    def native_key(p: Point):
        x, yy = p
        assert x.b == K0 and yy.b == K0
        assert x.a.c[1] == x.a.c[2] == yy.a.c[0] == yy.a.c[3] == 0
        return x.a.c[0], x.a.c[3], yy.a.c[1], yy.a.c[2]

    full = [zero] + sorted(pool, key=native_key)
    return [full[i] for i in keep]


def diamond_core_points() -> list[Point]:
    """The reviewed eight-point core in order P1,P2,X0,Y0,X1,Y1,X2,Y2."""
    caps = [
        (L0, L0),
        ((L1 + LS).scale(Q(1, 2)), LY),
        ((L1 - LS).scale(Q(1, 2)), LY),
        (L1, L0),
    ]
    full = list(caps)
    for left, right in zip(caps, caps[1:]):
        dx, dy = right[0] - left[0], right[1] - left[1]
        midpoint = ((left[0] + right[0]).scale(Q(1, 2)),
                    (left[1] + right[1]).scale(Q(1, 2)))
        offset = ((-dy * LS).scale(Q(1, 6)), (dx * LS).scale(Q(1, 6)))
        full.extend((point_add(midpoint, offset),
                     point_add(midpoint, point_scale(offset, -1))))
    return [full[i] for i in (1, 2, 4, 5, 6, 7, 8, 9)]


def edges(points: list[Point]) -> list[tuple[int, int]]:
    return [(a, b) for a, b in combinations(range(len(points)), 2)
            if dist2(points[a], points[b]) == L1]


def adjacency(n: int, es: list[tuple[int, int]]) -> list[set[int]]:
    adj = [set() for _ in range(n)]
    for a, b in es:
        adj[a].add(b)
        adj[b].add(a)
    return adj


def colour(adj: list[set[int]], colours: int,
           allowed: list[set[int]] | None = None) -> tuple[int, ...] | None:
    word = [-1] * len(adj)
    domains = [set(range(colours)) if allowed is None else set(allowed[i])
               for i in range(len(adj))]

    def visit(done: int) -> bool:
        if done == len(adj):
            return True
        v = min((i for i, c in enumerate(word) if c < 0),
                key=lambda i: (len(domains[i]), -len(adj[i]), i))
        for c in sorted(domains[v]):
            if any(word[w] == c for w in adj[v]):
                continue
            word[v] = c
            changed = []
            bad = False
            for w in adj[v]:
                if word[w] < 0 and c in domains[w]:
                    domains[w].remove(c)
                    changed.append(w)
                    if not domains[w]:
                        bad = True
                        break
            if not bad and visit(done + 1):
                return True
            for w in changed:
                domains[w].add(c)
            word[v] = -1
        return False

    return tuple(word) if visit(0) else None


def build_geometry():
    f29 = f29_points()
    core = diamond_core_points()
    f_edges = edges(f29)
    d_edges = edges(core)
    assert (len(f29), len(f_edges), len(core), len(d_edges)) == (29, 75, 8, 11)

    addresses = [(i, j, point_add(p, q))
                 for i, p in enumerate(f29) for j, q in enumerate(core)]
    physical = sorted({p for _, _, p in addresses}, key=lambda p: (flat(p[0]), flat(p[1])))
    index = {p: i for i, p in enumerate(physical)}
    address_map = [[i, j, index[p]] for i, j, p in addresses]
    es = edges(physical)

    inherited = set()
    for j in range(len(core)):
        for a, b in f_edges:
            inherited.add(tuple(sorted((index[point_add(f29[a], core[j])],
                                        index[point_add(f29[b], core[j])]))))
    for i in range(len(f29)):
        for a, b in d_edges:
            inherited.add(tuple(sorted((index[point_add(f29[i], core[a])],
                                        index[point_add(f29[i], core[b])]))))
    assert inherited <= set(es)
    return f29, core, physical, es, inherited, address_map

