#!/usr/bin/env python3
"""Exact model for the frozen L10,1 directed-edge-star closure."""

from collections import deque
from dataclasses import dataclass
from fractions import Fraction as Q
from itertools import combinations


@dataclass(frozen=True, order=True)
class K:
    """An element of Q(sqrt(3),sqrt(11)) in basis 1,a,b,ab."""

    q: Q = Q(0)
    a: Q = Q(0)
    b: Q = Q(0)
    c: Q = Q(0)

    def __add__(self, other):
        other = as_k(other)
        return K(self.q + other.q, self.a + other.a,
                 self.b + other.b, self.c + other.c)

    __radd__ = __add__

    def __neg__(self):
        return K(-self.q, -self.a, -self.b, -self.c)

    def __sub__(self, other):
        return self + (-as_k(other))

    def __rsub__(self, other):
        return as_k(other) - self

    def __mul__(self, other):
        other = as_k(other)
        x0, x1, x2, x3 = self.q, self.a, self.b, self.c
        y0, y1, y2, y3 = other.q, other.a, other.b, other.c
        return K(
            x0*y0 + 3*x1*y1 + 11*x2*y2 + 33*x3*y3,
            x0*y1 + x1*y0 + 11*x2*y3 + 11*x3*y2,
            x0*y2 + x2*y0 + 3*x1*y3 + 3*x3*y1,
            x0*y3 + x3*y0 + x1*y2 + x2*y1,
        )

    __rmul__ = __mul__

    def __truediv__(self, n):
        n = Q(n)
        return K(self.q/n, self.a/n, self.b/n, self.c/n)

    def encode(self):
        return [fraction_text(x) for x in (self.q, self.a, self.b, self.c)]


def as_k(x):
    return x if isinstance(x, K) else K(Q(x))


def fraction_text(x):
    return str(x.numerator) if x.denominator == 1 else f"{x.numerator}/{x.denominator}"


@dataclass(frozen=True, order=True)
class Point:
    x: K
    y: K

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y)

    def encode(self):
        return [self.x.encode(), self.y.encode()]


def complex_multiply(z, w):
    return Point(z.x*w.x - z.y*w.y, z.x*w.y + z.y*w.x)


def norm_squared(z):
    return z.x*z.x + z.y*z.y


ZERO = K()
ONE = K(Q(1))
SQRT3 = K(a=Q(1))
SQRT11 = K(b=Q(1))
SQRT33 = K(c=Q(1))


def source_points():
    """Return the frozen exact ten-point support in insertion order A,...,J."""
    a, b, c = SQRT3, SQRT11, SQRT33
    return {
        "A": Point(ZERO, ZERO),
        "B": Point(ONE, ZERO),
        "C": Point(c/6, a/6),
        "D": Point(ONE+c/6, a/6),
        "E": Point(K(Q(1, 2))+c/6, 2*a/3),
        "F": Point(K(Q(1, 2)), a/2),
        "G": Point(K(Q(1, 2)), -a/2),
        "H": Point(K(Q(1, 2))+c/6, -a/3),
        "I": Point((K(11)+c)/12, (a+b)/12),
        "J": Point((ONE+c)/12, (a-b)/12),
    }


FIGURE_EDGES = {tuple(sorted(e)) for e in
                "AB AC CD DB CE ED EF FA AG BG HC HG IJ JF FI IH HJ".split()}


def complete_edges(points):
    return [(i, j) for i, j in combinations(range(len(points)), 2)
            if norm_squared(points[i]-points[j]) == ONE]


def build():
    source = source_points()
    names = list(source)
    source_list = [source[x] for x in names]
    source_edges = complete_edges(source_list)
    source_named_edges = {
        tuple(sorted((names[i], names[j]))) for i, j in source_edges
    }
    if not FIGURE_EDGES <= source_named_edges:
        raise AssertionError("a displayed source edge is not unit")

    placements = []
    point_set = set()
    for i, j in source_edges:
        for u_index, v_index in ((i, j), (j, i)):
            u, v = source_list[u_index], source_list[v_index]
            direction = v-u
            image = tuple(u + complex_multiply(direction, z) for z in source_list)
            placements.append((names[u_index]+names[v_index], image))
            point_set.update(image)

    points = sorted(point_set)
    edges = complete_edges(points)
    return {
        "source_names": names,
        "source_points": source_list,
        "source_edges": source_edges,
        "source_named_edges": source_named_edges,
        "source_incidental_edges": source_named_edges-FIGURE_EDGES,
        "placements": placements,
        "points": points,
        "edges": edges,
    }


def adjacency(vertex_count, edges):
    adj = [set() for _ in range(vertex_count)]
    for u, v in edges:
        adj[u].add(v)
        adj[v].add(u)
    return adj


def find_coloring(adj, color_count):
    """Deterministic DSATUR search; return one word or None."""
    n = len(adj)
    colors = [-1]*n
    saturation = [set() for _ in range(n)]
    uncolored = set(range(n))

    def recurse():
        if not uncolored:
            return True
        v = max(uncolored, key=lambda x: (len(saturation[x]), len(adj[x]), -x))
        used = set(colors)-{-1}
        for color in range(min(color_count, len(used)+1)):
            if color in saturation[v]:
                continue
            colors[v] = color
            uncolored.remove(v)
            touched = []
            for w in adj[v]:
                if colors[w] < 0 and color not in saturation[w]:
                    saturation[w].add(color)
                    touched.append(w)
            if recurse():
                return True
            for w in touched:
                saturation[w].remove(color)
            uncolored.add(v)
            colors[v] = -1
        return False

    return tuple(colors) if recurse() else None


def graph_cuts(adj):
    n = len(adj)
    discovery = [-1]*n
    low = [0]*n
    timer = 0
    articulations = set()
    bridges = []

    def dfs(v, parent=-1):
        nonlocal timer
        discovery[v] = low[v] = timer
        timer += 1
        children = 0
        for w in adj[v]:
            if w == parent:
                continue
            if discovery[w] >= 0:
                low[v] = min(low[v], discovery[w])
            else:
                dfs(w, v)
                low[v] = min(low[v], low[w])
                children += 1
                if low[w] > discovery[v]:
                    bridges.append(tuple(sorted((v, w))))
                if parent >= 0 and low[w] >= discovery[v]:
                    articulations.add(v)
        if parent < 0 and children > 1:
            articulations.add(v)

    if n:
        dfs(0)
    return sum(x >= 0 for x in discovery), articulations, sorted(bridges)


def core_size(adj, minimum_degree):
    alive = set(range(len(adj)))
    degree = [len(x) for x in adj]
    queue = deque(i for i, d in enumerate(degree) if d < minimum_degree)
    while queue:
        v = queue.popleft()
        if v not in alive:
            continue
        alive.remove(v)
        for w in adj[v]:
            if w in alive:
                degree[w] -= 1
                if degree[w] < minimum_degree:
                    queue.append(w)
    return len(alive)


def proper_coloring(word, edges, color_count):
    return (len(word) > 0 and all(isinstance(x, int) and 0 <= x < color_count for x in word)
            and all(word[u] != word[v] for u, v in edges))
