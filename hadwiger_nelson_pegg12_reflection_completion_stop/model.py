"""Exact Q(sqrt(3),sqrt(11)) model for the Pegg UD12-2 reflection test."""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from functools import lru_cache
from hashlib import sha256
from itertools import combinations


Q = Fraction


@dataclass(frozen=True, slots=True)
class K:
    """Element of Q(sqrt(3),sqrt(11)) in the basis 1,r3,r11,r33."""

    c: tuple[Q, Q, Q, Q]

    @staticmethod
    def rational(x: int | Q) -> "K":
        return K((Q(x), Q(0), Q(0), Q(0)))

    @staticmethod
    def basis(mask: int) -> "K":
        a = [Q(0)] * 4
        a[mask] = Q(1)
        return K(tuple(a))

    def __add__(self, other: "K" | int) -> "K":
        other = as_k(other)
        return K(tuple(a + b for a, b in zip(self.c, other.c)))

    __radd__ = __add__

    def __neg__(self) -> "K":
        return K(tuple(-a for a in self.c))

    def __sub__(self, other: "K" | int) -> "K":
        return self + (-as_k(other))

    def __rsub__(self, other: "K" | int) -> "K":
        return as_k(other) - self

    def __mul__(self, other: "K" | int | Q) -> "K":
        other = as_k(other)
        out = [Q(0)] * 4
        for i, a in enumerate(self.c):
            for j, b in enumerate(other.c):
                factor = 1
                common = i & j
                if common & 1:
                    factor *= 3
                if common & 2:
                    factor *= 11
                out[i ^ j] += a * b * factor
        return K(tuple(out))

    __rmul__ = __mul__

    def __truediv__(self, other: "K" | int | Q) -> "K":
        return self * inverse(as_k(other))

    def __bool__(self) -> bool:
        return any(self.c)


def as_k(x: K | int | Q) -> K:
    return x if isinstance(x, K) else K.rational(Q(x))


@lru_cache(maxsize=None)
def inverse(x: K) -> K:
    if not x:
        raise ZeroDivisionError
    basis = [K.basis(i) for i in range(4)]
    # Column j is x*basis[j].  Solve M y = 1 by exact elimination.
    rows = [[(x * basis[j]).c[i] for j in range(4)] for i in range(4)]
    rhs = [Q(1), Q(0), Q(0), Q(0)]
    for col in range(4):
        pivot = next(r for r in range(col, 4) if rows[r][col])
        rows[col], rows[pivot] = rows[pivot], rows[col]
        rhs[col], rhs[pivot] = rhs[pivot], rhs[col]
        scale = rows[col][col]
        rows[col] = [v / scale for v in rows[col]]
        rhs[col] /= scale
        for r in range(4):
            if r == col or not rows[r][col]:
                continue
            scale = rows[r][col]
            rows[r] = [a - scale * b for a, b in zip(rows[r], rows[col])]
            rhs[r] -= scale * rhs[col]
    return K(tuple(rhs))


ZERO = K.rational(0)
ONE = K.rational(1)
R3 = K.basis(1)
R11 = K.basis(2)
R33 = K.basis(3)
Point = tuple[K, K]


@lru_cache(maxsize=1)
def source_points() -> tuple[Point, ...]:
    """The symmetric exact realization of Pegg/Shibuya {UnitDistance,{12,2}}."""

    a = (R33 - 3) / 12
    y = (R3 + 3 * R11) / 12
    s = R3 / 6
    half = ONE / 2
    return (
        (ZERO, ZERO),
        (ONE, ZERO),
        (-a, y),
        (ONE + a, y),
        (half - a, y - s),
        (half + a, y - s),
        (half, -s),
        (-a, y - 2 * s),
        (ONE + a, y - 2 * s),
        (half - a, y + s),
        (half + a, y + s),
        (half, s),
    )


def squared_distance(p: Point, q: Point) -> K:
    dx = p[0] - q[0]
    dy = p[1] - q[1]
    return dx * dx + dy * dy


def reflect(z: Point, p: Point, q: Point) -> Point:
    """Reflect z in the line through the distinct exact points p,q."""

    dx, dy = q[0] - p[0], q[1] - p[1]
    d2 = dx * dx + dy * dy
    a = (dx * dx - dy * dy) / d2
    b = 2 * dx * dy / d2
    wx, wy = z[0] - p[0], z[1] - p[1]
    return (p[0] + a * wx + b * wy, p[1] + b * wx - a * wy)


def complete_edges(points: tuple[Point, ...]) -> tuple[tuple[int, int], ...]:
    return tuple(
        (i, j)
        for i, j in combinations(range(len(points)), 2)
        if squared_distance(points[i], points[j]) == ONE
    )


def merge_points(groups: list[tuple[Point, tuple[str, int, int]]]):
    points: list[Point] = []
    labels: list[list[tuple[str, int, int]]] = []
    index: dict[Point, int] = {}
    mapping: list[int] = []
    for point, label in groups:
        if point not in index:
            index[point] = len(points)
            points.append(point)
            labels.append([])
        k = index[point]
        labels[k].append(label)
        mapping.append(k)
    return tuple(points), tuple(tuple(x) for x in labels), tuple(mapping)


def reflected_union(axes: tuple[tuple[int, int], ...]):
    base = source_points()
    groups: list[tuple[Point, tuple[str, int, int]]] = [
        (p, ("B", 0, i)) for i, p in enumerate(base)
    ]
    for copy, (i, j) in enumerate(axes, 1):
        groups.extend(
            (reflect(z, base[i], base[j]), ("R", copy, k))
            for k, z in enumerate(base)
        )
    points, labels, raw_mapping = merge_points(groups)
    maps = [raw_mapping[0:12]]
    for copy in range(len(axes)):
        maps.append(raw_mapping[12 * (copy + 1) : 12 * (copy + 2)])
    return points, complete_edges(points), labels, tuple(maps)


POSITIVE_AXES = (
    (0, 6), (0, 11), (1, 6), (1, 11),
    (2, 5), (2, 7), (2, 9), (2, 11),
    (3, 4), (3, 8), (3, 10), (3, 11),
    (4, 6), (4, 7), (4, 9),
    (5, 6), (5, 8), (5, 10),
)


@lru_cache(maxsize=1)
def source_edges() -> tuple[tuple[int, int], ...]:
    return complete_edges(source_points())


def edge_hash(edges: tuple[tuple[int, int], ...]) -> str:
    data = "".join(f"{a} {b}\n" for a, b in edges).encode()
    return sha256(data).hexdigest()


def coordinate_hash(points: tuple[Point, ...]) -> str:
    rows = []
    for x, y in points:
        coeffs = x.c + y.c
        rows.append(" ".join(f"{v.numerator}/{v.denominator}" for v in coeffs) + "\n")
    return sha256("".join(rows).encode()).hexdigest()


def check_word(word: str, n: int, edges: tuple[tuple[int, int], ...], k: int = 4):
    assert len(word) == n
    colors = tuple(int(x) for x in word)
    assert all(0 <= x < k for x in colors)
    assert all(colors[a] != colors[b] for a, b in edges)
    return colors


def canonical_word(word) -> str:
    rename: dict[int, int] = {}
    out = []
    for value in word:
        value = int(value)
        if value not in rename:
            rename[value] = len(rename)
        out.append(str(rename[value]))
    return "".join(out)


@lru_cache(maxsize=1)
def all_source_four_colorings() -> tuple[str, ...]:
    edges = source_edges()
    adj = [set() for _ in range(12)]
    for a, b in edges:
        adj[a].add(b)
        adj[b].add(a)
    order = sorted(range(12), key=lambda v: (-len(adj[v]), v))
    color = [-1] * 12
    words: set[str] = set()

    def visit(depth: int):
        if depth == 12:
            words.add(canonical_word(color))
            return
        v = order[depth]
        used = {color[w] for w in adj[v] if color[w] >= 0}
        for c in range(4):
            if c not in used:
                color[v] = c
                visit(depth + 1)
        color[v] = -1

    visit(0)
    return tuple(sorted(words))


def find_coloring(n: int, edges, k: int, pins: dict[int, int] | None = None):
    """Deterministic exhaustive DSATUR search; None is a replayable negative."""

    adj = [set() for _ in range(n)]
    for a, b in edges:
        adj[a].add(b)
        adj[b].add(a)
    color = [-1] * n
    if pins:
        for v, c in pins.items():
            if color[v] not in (-1, c):
                return None
            color[v] = c
        if any(color[a] == color[b] >= 0 for a, b in edges):
            return None

    def search():
        uncolored = [v for v in range(n) if color[v] < 0]
        if not uncolored:
            return tuple(color)
        v = max(
            uncolored,
            key=lambda x: (len({color[w] for w in adj[x] if color[w] >= 0}), len(adj[x]), -x),
        )
        forbidden = {color[w] for w in adj[v] if color[w] >= 0}
        for c in range(k):
            if c in forbidden:
                continue
            color[v] = c
            answer = search()
            if answer is not None:
                return answer
        color[v] = -1
        return None

    return search()


def is_connected_after(n: int, edges, removed=()) -> bool:
    removed = set(removed)
    vertices = [v for v in range(n) if v not in removed]
    if len(vertices) <= 1:
        return True
    adj = [[] for _ in range(n)]
    for a, b in edges:
        if a not in removed and b not in removed:
            adj[a].append(b)
            adj[b].append(a)
    seen = {vertices[0]}
    stack = [vertices[0]]
    while stack:
        v = stack.pop()
        for w in adj[v]:
            if w not in seen:
                seen.add(w)
                stack.append(w)
    return len(seen) == len(vertices)


def vertex_connectivity(n: int, edges, limit=5):
    for size in range(1, min(limit, n - 1) + 1):
        for cut in combinations(range(n), size):
            if not is_connected_after(n, edges, cut):
                return size, cut
    return None, None
