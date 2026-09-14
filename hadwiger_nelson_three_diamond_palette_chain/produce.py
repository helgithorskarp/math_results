#!/usr/bin/env python3
"""Produce the exact closed three-diamond-chain certificate."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path


@dataclass(frozen=True)
class K:
    """a+b*s+c*y+d*s*y, where s^2=3 and y^2=(4-s)/2."""

    c: tuple[Fraction, Fraction, Fraction, Fraction]

    @staticmethod
    def scalar(x: int | Fraction) -> "K":
        return K((Fraction(x), Fraction(0), Fraction(0), Fraction(0)))

    def __add__(self, other: "K") -> "K":
        return K(tuple(a + b for a, b in zip(self.c, other.c)))  # type: ignore[arg-type]

    def __neg__(self) -> "K":
        return K(tuple(-a for a in self.c))  # type: ignore[arg-type]

    def __sub__(self, other: "K") -> "K":
        return self + (-other)

    def __mul__(self, other: "K") -> "K":
        a, b, c, d = self.c
        e, f, g, h = other.c
        # Multiply as (a+bs)+(c+ds)y, reducing s^2=3 and
        # y^2=2-s/2.
        ac0, ac1 = a * e + 3 * b * f, a * f + b * e
        bd0, bd1 = c * g + 3 * d * h, c * h + d * g
        real0 = ac0 + 2 * bd0 - Fraction(3, 2) * bd1
        real1 = ac1 + 2 * bd1 - Fraction(1, 2) * bd0
        y0 = a * g + 3 * b * h + c * e + 3 * d * f
        y1 = a * h + b * g + c * f + d * e
        return K((real0, real1, y0, y1))

    def scale(self, x: int | Fraction) -> "K":
        return K(tuple(Fraction(x) * a for a in self.c))  # type: ignore[arg-type]


ZERO, ONE = K.scalar(0), K.scalar(1)
S = K((Fraction(0), Fraction(1), Fraction(0), Fraction(0)))
Y = K((Fraction(0), Fraction(0), Fraction(1), Fraction(0)))
Point = tuple[K, K]


def dist2(p: Point, q: Point) -> K:
    dx, dy = p[0] - q[0], p[1] - q[1]
    return dx * dx + dy * dy


def points() -> list[tuple[str, Point]]:
    caps = [
        (ZERO, ZERO),
        ((ONE + S).scale(Fraction(1, 2)), Y),
        ((ONE - S).scale(Fraction(1, 2)), Y),
        (ONE, ZERO),
    ]
    out = [(f"P{i}", p) for i, p in enumerate(caps)]
    for i in range(3):
        p, q = caps[i], caps[i + 1]
        dx, dy = q[0] - p[0], q[1] - p[1]
        mid = ((p[0] + q[0]).scale(Fraction(1, 2)), (p[1] + q[1]).scale(Fraction(1, 2)))
        off = ((-dy * S).scale(Fraction(1, 6)), (dx * S).scale(Fraction(1, 6)))
        out.extend([
            (f"X{i}", (mid[0] + off[0], mid[1] + off[1])),
            (f"Y{i}", (mid[0] - off[0], mid[1] - off[1])),
        ])
    return out


def adjacency(n: int, edges: list[tuple[int, int]]) -> list[set[int]]:
    adj = [set() for _ in range(n)]
    for u, v in edges:
        adj[u].add(v)
        adj[v].add(u)
    return adj


def colour(adj: list[set[int]], k: int, fixed: dict[int, int] | None = None) -> tuple[int, ...] | None:
    word = [-1] * len(adj)
    for v, c in (fixed or {}).items():
        word[v] = c
    if any(word[u] >= 0 and word[u] == word[v] for u in range(len(adj)) for v in adj[u]):
        return None

    def visit() -> bool:
        remaining = [v for v, c in enumerate(word) if c < 0]
        if not remaining:
            return True
        v = max(remaining, key=lambda z: (len({word[w] for w in adj[z] if word[w] >= 0}), len(adj[z]), -z))
        forbidden = {word[w] for w in adj[v] if word[w] >= 0}
        for c in range(k):
            if c not in forbidden:
                word[v] = c
                if visit():
                    return True
        word[v] = -1
        return False

    return tuple(word) if visit() else None


def canonical(values: tuple[int, ...]) -> str:
    rename: dict[int, int] = {}
    return "".join(str(rename.setdefault(x, len(rename))) for x in values)


def ftext(x: Fraction) -> str:
    return str(x.numerator) if x.denominator == 1 else f"{x.numerator}/{x.denominator}"


def vector(x: K) -> list[str]:
    return [ftext(c) for c in x.c]


def digest(rows: object) -> str:
    raw = json.dumps(rows, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(raw).hexdigest()


def build() -> dict[str, object]:
    named = points()
    if len(named) != 10 or len({p for _, p in named}) != 10:
        raise RuntimeError("unexpected collision")
    pts = [p for _, p in named]
    edges = [(u, v) for u, v in itertools.combinations(range(10), 2) if dist2(pts[u], pts[v]) == ONE]
    adj = adjacency(10, edges)
    four = colour(adj, 4)
    if four is None or colour(adj, 3) is not None:
        raise RuntimeError("unexpected chromatic number")
    terminals = (4, 5, 6, 7, 8, 9)
    bare: set[str] = set()
    allowed: set[str] = set()
    witnesses: dict[str, str] = {}
    named_bare = named_allowed = 0
    for assignment in itertools.product(range(4), repeat=6):
        if any(assignment[2 * i] == assignment[2 * i + 1] for i in range(3)):
            continue
        named_bare += 1
        pat = canonical(assignment)
        bare.add(pat)
        witness = colour(adj, 4, dict(zip(terminals, assignment)))
        if witness is not None:
            named_allowed += 1
            allowed.add(pat)
            witnesses.setdefault(pat, "".join(map(str, witness)))
    point_rows = [{"label": label, "x": vector(p[0]), "y": vector(p[1])} for label, p in named]
    edge_rows = [list(edge) for edge in edges]
    return {
        "format": "hn-three-diamond-palette-chain-v1",
        "field": {"basis": ["1", "s", "y", "s*y"], "relations": ["s^2=3", "y^2=(4-s)/2"]},
        "points": point_rows,
        "point_rows_sha256": digest(point_rows),
        "edges": edge_rows,
        "edge_rows_sha256": digest(edge_rows),
        "chromatic": {
            "number": 4,
            "diamonds": [[0, 1, 4, 5], [1, 2, 6, 7], [2, 3, 8, 9]],
            "closing_edge": [0, 3],
            "four_colouring": "".join(map(str, four)),
        },
        "relation": {
            "terminals": list(terminals),
            "terminal_labels": [named[v][0] for v in terminals],
            "bare_terminal_edges": [[4, 5], [6, 7], [8, 9]],
            "formula": "palette(X0,Y0) intersects palette(X1,Y1) and palette(X1,Y1) intersects palette(X2,Y2)",
            "canonical_bare_patterns": sorted(bare),
            "canonical_extendible_patterns": sorted(allowed),
            "canonical_witnesses": dict(sorted(witnesses.items())),
            "named_bare_assignments": named_bare,
            "named_extendible_assignments": named_allowed,
            "named_forbidden_assignments": named_bare - named_allowed,
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, default=Path(__file__).with_name("certificate.json"))
    args = parser.parse_args()
    args.out.write_text(json.dumps(build(), indent=2, sort_keys=True) + "\n")


if __name__ == "__main__":
    main()
