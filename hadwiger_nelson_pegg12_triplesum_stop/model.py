"""Exact model for the frozen Pegg12 commutative triple-sum gate."""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from functools import lru_cache
from hashlib import sha256
from itertools import combinations, combinations_with_replacement


Q = Fraction


@dataclass(frozen=True, slots=True)
class K:
    """Element of Q(sqrt(3),sqrt(11)) in basis 1,r3,r11,r33."""

    c: tuple[Q, Q, Q, Q]

    @staticmethod
    def rational(x: int | Q) -> "K":
        return K((Q(x), Q(0), Q(0), Q(0)))

    @staticmethod
    def basis(mask: int) -> "K":
        out = [Q(0)] * 4
        out[mask] = Q(1)
        return K(tuple(out))

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
    rows = [[(x * basis[j]).c[i] for j in range(4)] for i in range(4)]
    rhs = [Q(1), Q(0), Q(0), Q(0)]
    for col in range(4):
        pivot = next(r for r in range(col, 4) if rows[r][col])
        rows[col], rows[pivot] = rows[pivot], rows[col]
        rhs[col], rhs[pivot] = rhs[pivot], rhs[col]
        scale = rows[col][col]
        rows[col] = [v / scale for v in rows[col]]
        rhs[col] /= scale
        for row in range(4):
            if row == col or not rows[row][col]:
                continue
            scale = rows[row][col]
            rows[row] = [a - scale * b for a, b in zip(rows[row], rows[col])]
            rhs[row] -= scale * rhs[col]
    return K(tuple(rhs))


ZERO = K.rational(0)
ONE = K.rational(1)
R3 = K.basis(1)
R11 = K.basis(2)
R33 = K.basis(3)
Point = tuple[K, K]


@lru_cache(maxsize=1)
def source_points() -> tuple[Point, ...]:
    """Symmetric exact realization of Pegg/Shibuya UD12-2."""

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
    dx, dy = p[0] - q[0], p[1] - q[1]
    return dx * dx + dy * dy


def complete_edges(points: tuple[Point, ...]) -> tuple[tuple[int, int], ...]:
    return tuple(
        (i, j)
        for i, j in combinations(range(len(points)), 2)
        if squared_distance(points[i], points[j]) == ONE
    )


@lru_cache(maxsize=1)
def source_edges() -> tuple[tuple[int, int], ...]:
    return complete_edges(source_points())


def add3(a: Point, b: Point, c: Point) -> Point:
    return (a[0] + b[0] + c[0], a[1] + b[1] + c[1])


@lru_cache(maxsize=1)
def triple_sum():
    """Collision-merged P+P+P, complete edges, labels, and source fibre."""

    source = source_points()
    labels_by_point: dict[Point, list[tuple[int, int, int]]] = {}
    for address in combinations_with_replacement(range(12), 3):
        point = add3(*(source[i] for i in address))
        labels_by_point.setdefault(point, []).append(address)
    points = tuple(sorted(labels_by_point, key=lambda p: (p[0].c, p[1].c)))
    index = {point: i for i, point in enumerate(points)}
    labels = tuple(tuple(labels_by_point[point]) for point in points)
    fibre = tuple(index[add3(source[0], source[0], point)] for point in source)
    return points, complete_edges(points), labels, fibre


def inherited_edges(points: tuple[Point, ...]) -> tuple[tuple[int, int], ...]:
    """Edges inherited from any of the 78 translated source fibres."""

    source = source_points()
    index = {point: i for i, point in enumerate(points)}
    edges = set()
    for i, j in combinations_with_replacement(range(12), 2):
        fibre = tuple(index[add3(source[i], source[j], point)] for point in source)
        for a, b in source_edges():
            edges.add(tuple(sorted((fibre[a], fibre[b]))))
    return tuple(sorted(edges))


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
    adjacency = [set() for _ in range(12)]
    for a, b in edges:
        adjacency[a].add(b)
        adjacency[b].add(a)
    order = sorted(range(12), key=lambda v: (-len(adjacency[v]), v))
    colors = [-1] * 12
    words: set[str] = set()

    def visit(depth: int):
        if depth == 12:
            words.add(canonical_word(colors))
            return
        vertex = order[depth]
        forbidden = {colors[w] for w in adjacency[vertex] if colors[w] >= 0}
        for color in range(4):
            if color not in forbidden:
                colors[vertex] = color
                visit(depth + 1)
        colors[vertex] = -1

    visit(0)
    return tuple(sorted(words))


def find_coloring(n: int, edges, k: int, pins: dict[int, int] | None = None):
    """Deterministic exhaustive DSATUR search; None is an exhaustive negative."""

    adjacency = [set() for _ in range(n)]
    for a, b in edges:
        adjacency[a].add(b)
        adjacency[b].add(a)
    colors = [-1] * n
    if pins:
        for vertex, color in pins.items():
            if colors[vertex] not in (-1, color):
                return None
            colors[vertex] = color
        if any(colors[a] == colors[b] >= 0 for a, b in edges):
            return None

    def search():
        uncolored = [v for v in range(n) if colors[v] < 0]
        if not uncolored:
            return tuple(colors)
        vertex = max(
            uncolored,
            key=lambda v: (
                len({colors[w] for w in adjacency[v] if colors[w] >= 0}),
                len(adjacency[v]),
                -v,
            ),
        )
        forbidden = {colors[w] for w in adjacency[vertex] if colors[w] >= 0}
        for color in range(k):
            if color in forbidden:
                continue
            colors[vertex] = color
            answer = search()
            if answer is not None:
                return answer
        colors[vertex] = -1
        return None

    return search()


def check_word(word: str, n: int, edges, k: int = 4):
    if len(word) != n:
        raise ValueError("wrong word length")
    colors = tuple(map(int, word))
    if not all(0 <= color < k for color in colors):
        raise ValueError("colour outside range")
    if not all(colors[a] != colors[b] for a, b in edges):
        raise ValueError("word is improper")
    return colors


def coordinate_hash(points: tuple[Point, ...]) -> str:
    rows = []
    for x, y in points:
        rows.append(" ".join(f"{v.numerator}/{v.denominator}" for v in x.c + y.c) + "\n")
    return sha256("".join(rows).encode()).hexdigest()


def edge_hash(edges) -> str:
    return sha256("".join(f"{a} {b}\n" for a, b in edges).encode()).hexdigest()


def word_hash(words) -> str:
    return sha256("".join(word + "\n" for word in words).encode()).hexdigest()
