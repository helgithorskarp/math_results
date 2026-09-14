#!/usr/bin/env python3
"""Produce the exact square six-lens source certificate."""

from __future__ import annotations

import argparse
import hashlib
import json
from dataclasses import dataclass
from fractions import Fraction
from itertools import combinations
from pathlib import Path


@dataclass(frozen=True)
class K:
    """Eight-coefficient basis q^e s^f, q^4=3, s^2=2."""

    c: tuple[Fraction, ...]

    def __post_init__(self) -> None:
        if len(self.c) != 8:
            raise ValueError("expected eight coefficients")

    @staticmethod
    def scalar(x: int | Fraction) -> "K":
        return K((Fraction(x),) + (Fraction(0),) * 7)

    def __add__(self, other: "K") -> "K":
        return K(tuple(a + b for a, b in zip(self.c, other.c)))

    def __neg__(self) -> "K":
        return K(tuple(-a for a in self.c))

    def __sub__(self, other: "K") -> "K":
        return self + (-other)

    def __mul__(self, other: "K") -> "K":
        out = [Fraction(0) for _ in range(8)]
        for i, ai in enumerate(self.c):
            if not ai:
                continue
            fi, ei = divmod(i, 4)
            for j, bj in enumerate(other.c):
                if not bj:
                    continue
                fj, ej = divmod(j, 4)
                e, f = ei + ej, fi + fj
                factor = Fraction(1)
                if e >= 4:
                    e -= 4
                    factor *= 3
                if f >= 2:
                    f -= 2
                    factor *= 2
                out[4 * f + e] += ai * bj * factor
        return K(tuple(out))

    def scale(self, x: int | Fraction) -> "K":
        return K(tuple(Fraction(x) * a for a in self.c))


ZERO = K.scalar(0)
ONE = K.scalar(1)
Q = K((Fraction(0), Fraction(1)) + (Fraction(0),) * 6)
S = K((Fraction(0),) * 4 + (Fraction(1),) + (Fraction(0),) * 3)
Point = tuple[K, K]


def dist2(p: Point, q: Point) -> K:
    dx, dy = p[0] - q[0], p[1] - q[1]
    return dx * dx + dy * dy


def source_points() -> list[tuple[str, Point]]:
    sqrt3 = Q * Q
    a = (S * sqrt3 - S).scale(Fraction(1, 2))
    hs = (S * sqrt3 + S).scale(Fraction(1, 4))
    ah, qh = a.scale(Fraction(1, 2)), Q.scale(Fraction(1, 2))
    return [
        ("C0", (-ah, -ah)),
        ("C1", (ah, -ah)),
        ("C2", (ah, ah)),
        ("C3", (-ah, ah)),
        ("L01+", (ZERO, -ah + hs)),
        ("L01-", (ZERO, -ah - hs)),
        ("L02+", (-qh, qh)),
        ("L02-", (qh, -qh)),
        ("L03+", (-ah - hs, ZERO)),
        ("L03-", (-ah + hs, ZERO)),
        ("L12+", (ah - hs, ZERO)),
        ("L12-", (ah + hs, ZERO)),
        ("L13+", (-qh, -qh)),
        ("L13-", (qh, qh)),
        ("L23+", (ZERO, ah - hs)),
        ("L23-", (ZERO, ah + hs)),
    ]


def adjacency(n: int, edges: list[tuple[int, int]]) -> list[set[int]]:
    adj = [set() for _ in range(n)]
    for u, v in edges:
        adj[u].add(v)
        adj[v].add(u)
    return adj


def colouring(adj: list[set[int]], k: int, pre: dict[int, int] | None = None) -> tuple[int, ...] | None:
    color = [-1] * len(adj)
    for v, c in (pre or {}).items():
        color[v] = c
    if any(color[u] >= 0 and color[u] == color[v] for u in range(len(adj)) for v in adj[u]):
        return None

    def choose() -> int | None:
        uncoloured = [v for v, c in enumerate(color) if c < 0]
        if not uncoloured:
            return None
        return max(
            uncoloured,
            key=lambda v: (len({color[w] for w in adj[v] if color[w] >= 0}), len(adj[v]), -v),
        )

    def visit() -> bool:
        v = choose()
        if v is None:
            return True
        forbidden = {color[w] for w in adj[v] if color[w] >= 0}
        for c in range(k):
            if c not in forbidden:
                color[v] = c
                if visit():
                    return True
                color[v] = -1
        return False

    return tuple(color) if visit() else None


def patterns() -> list[tuple[int, ...]]:
    words = [(0,)]
    for _ in range(3):
        words = [w + (x,) for w in words for x in range(max(w) + 2)]
    return words


def fraction_text(x: Fraction) -> str:
    return str(x.numerator) if x.denominator == 1 else f"{x.numerator}/{x.denominator}"


def vector(x: K) -> list[str]:
    return [fraction_text(c) for c in x.c]


def digest(rows: object) -> str:
    raw = json.dumps(rows, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(raw).hexdigest()


def build() -> dict[str, object]:
    named = source_points()
    if len({p for _, p in named}) != 16:
        raise AssertionError("unexpected collision")
    pts = [p for _, p in named]
    edges = [(i, j) for i, j in combinations(range(16), 2) if dist2(pts[i], pts[j]) == ONE]
    adj = adjacency(16, edges)
    three = colouring(adj, 3)
    if three is None:
        raise AssertionError("missing three-colouring")
    pats = patterns()
    witnesses: dict[str, str] = {}
    for pattern in pats:
        word = colouring(adj, 4, dict(enumerate(pattern)))
        if word is None:
            raise AssertionError(pattern)
        witnesses["".join(map(str, pattern))] = "".join(map(str, word))
    point_rows = [
        {"label": label, "x": vector(point[0]), "y": vector(point[1])}
        for label, point in named
    ]
    edge_rows = [[u, v] for u, v in edges]
    return {
        "format": "hn-square-six-lens-neutrality-v1",
        "claim": "The frozen 16-point strict unit graph is three-chromatic and every four-colour assignment on its four square centres extends.",
        "field": {
            "basis_order": ["1", "q", "q^2", "q^3", "s", "s*q", "s*q^2", "s*q^3"],
            "relations": ["q^4=3", "s^2=2"],
        },
        "parameter": {"side": "a=s*(q^2-1)/2", "side_squared": "2-q^2"},
        "terminals": [0, 1, 2, 3],
        "points": point_rows,
        "edges": edge_rows,
        "point_rows_sha256": digest(point_rows),
        "edge_rows_sha256": digest(edge_rows),
        "chromatic": {
            "number": 3,
            "triangle": [0, 4, 9],
            "three_colouring": "".join(map(str, three)),
        },
        "relation": {
            "bare_terminal_edges": [],
            "canonical_bare_patterns": ["".join(map(str, p)) for p in pats],
            "canonical_extendible_patterns": ["".join(map(str, p)) for p in pats],
            "canonical_witnesses": witnesses,
            "named_bare_assignments": 256,
            "named_extendible_assignments": 256,
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, default=Path("certificate.json"))
    args = parser.parse_args()
    args.out.write_text(json.dumps(build(), indent=2, sort_keys=True) + "\n")
    print("PRODUCED_SQUARE_SIX_LENS_CERTIFICATE")


if __name__ == "__main__":
    main()
