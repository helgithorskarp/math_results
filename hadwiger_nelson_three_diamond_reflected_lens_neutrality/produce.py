#!/usr/bin/env python3
"""Produce the exact reflected-terminal-lens interaction certificate."""

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
    """a+b*s+c*y+d*s*y, with s^2=3 and y^2=2-s/2."""

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
        p0, p1 = a * e + 3 * b * f, a * f + b * e
        q0, q1 = c * g + 3 * d * h, c * h + d * g
        return K((
            p0 + 2 * q0 - Fraction(3, 2) * q1,
            p1 + 2 * q1 - Fraction(1, 2) * q0,
            a * g + 3 * b * h + c * e + 3 * d * f,
            a * h + b * g + c * f + d * e,
        ))

    def scale(self, q: int | Fraction) -> "K":
        return K(tuple(Fraction(q) * x for x in self.c))  # type: ignore[arg-type]


Z, O = K.scalar(0), K.scalar(1)
S = K((Fraction(0), Fraction(1), Fraction(0), Fraction(0)))
Y = K((Fraction(0), Fraction(0), Fraction(1), Fraction(0)))
Point = tuple[K, K]
CORE_NAMES = ("P1", "P2", "X0", "Y0", "X1", "Y1", "X2", "Y2")
TERMINALS = (2, 3, 4, 5, 6, 7)


def dist2(p: Point, q: Point) -> K:
    dx, dy = p[0] - q[0], p[1] - q[1]
    return dx * dx + dy * dy


def full_source() -> tuple[list[tuple[str, Point]], tuple[Point, Point]]:
    caps = [
        (Z, Z),
        ((O + S).scale(Fraction(1, 2)), Y),
        ((O - S).scale(Fraction(1, 2)), Y),
        (O, Z),
    ]
    full = [(f"P{i}", p) for i, p in enumerate(caps)]
    for i, (p, q) in enumerate(zip(caps, caps[1:])):
        dx, dy = q[0] - p[0], q[1] - p[1]
        mid = ((p[0] + q[0]).scale(Fraction(1, 2)), (p[1] + q[1]).scale(Fraction(1, 2)))
        off = ((-dy * S).scale(Fraction(1, 6)), (dx * S).scale(Fraction(1, 6)))
        full.append((f"X{i}", (mid[0] + off[0], mid[1] + off[1])))
        full.append((f"Y{i}", (mid[0] - off[0], mid[1] - off[1])))
    by_name = dict(full)
    out = [(name, by_name[name]) for name in CORE_NAMES]
    for centre, left, right in (("P1", ("X0", "Y0"), ("X1", "Y1")),
                                ("P2", ("X1", "Y1"), ("X2", "Y2"))):
        for a in left:
            for b in right:
                out.append((f"R{centre[-1]}_{a}_{b}",
                            (by_name[a][0] + by_name[b][0] - by_name[centre][0],
                             by_name[a][1] + by_name[b][1] - by_name[centre][1])))
    return out, (by_name["P0"], by_name["P3"])


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
        left = [v for v, c in enumerate(word) if c < 0]
        if not left:
            return True
        v = max(left, key=lambda z: (len({word[w] for w in adj[z] if word[w] >= 0}), len(adj[z]), -z))
        forbidden = {word[w] for w in adj[v] if word[w] >= 0}
        for c in range(k):
            if c not in forbidden:
                word[v] = c
                if visit():
                    return True
        word[v] = -1
        return False

    return tuple(word) if visit() else None


def relation_formula(values: tuple[int, ...]) -> bool:
    if any(values[2 * i] == values[2 * i + 1] for i in range(3)):
        return False
    e0, e1, e2 = ({values[2 * i], values[2 * i + 1]} for i in range(3))
    return bool(e0 & e1) and bool(e1 & e2)


def canonical(values: tuple[int, ...]) -> str:
    rename: dict[int, int] = {}
    return "".join(str(rename.setdefault(x, len(rename))) for x in values)


def ftext(x: Fraction) -> str:
    return str(x.numerator) if x.denominator == 1 else f"{x.numerator}/{x.denominator}"


def vector(x: K) -> list[str]:
    return [ftext(c) for c in x.c]


def digest(value: object) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def build() -> dict[str, object]:
    named, deleted_caps = full_source()
    if len(named) != 16 or len({p for _, p in named}) != 16:
        raise RuntimeError("unexpected collision")
    points = [p for _, p in named]
    if any(points[i] in deleted_caps for i in range(8, 16)):
        raise RuntimeError("deleted cap reintroduced")
    if any(dist2(points[i], points[j]) in (Z, O) for i in range(8, 16) for j in (0, 1)):
        raise RuntimeError("added-to-internal contact")
    edges = [(u, v) for u, v in itertools.combinations(range(16), 2) if dist2(points[u], points[v]) == O]
    adj = adjacency(16, edges)
    three = colour(adj, 3)
    if three is None or colour(adj, 2) is not None:
        raise RuntimeError("unexpected chromatic number")
    input_patterns: set[str] = set()
    output_patterns: set[str] = set()
    witnesses: dict[str, str] = {}
    named_input = named_output = 0
    for assignment in itertools.product(range(4), repeat=6):
        if not relation_formula(assignment):
            continue
        named_input += 1
        pattern = canonical(assignment)
        input_patterns.add(pattern)
        witness = colour(adj, 4, dict(zip(TERMINALS, assignment)))
        if witness is not None:
            named_output += 1
            output_patterns.add(pattern)
            witnesses.setdefault(pattern, "".join(map(str, witness)))
    point_rows = [{"label": label, "x": vector(p[0]), "y": vector(p[1])} for label, p in named]
    edge_rows = [list(edge) for edge in edges]
    return {
        "format": "hn-three-diamond-reflected-lens-neutrality-v1",
        "parent_review_source_commit": "1193ec46a7c0368ae16da8b88a781508d34d4a2f",
        "field": {"basis": ["1", "s", "y", "s*y"], "relations": ["s^2=3", "y^2=(4-s)/2"]},
        "points": point_rows,
        "point_rows_sha256": digest(point_rows),
        "edges": edge_rows,
        "edge_rows_sha256": digest(edge_rows),
        "chromatic": {"number": 3, "triangle": [0, 2, 3], "three_colouring": "".join(map(str, three))},
        "interaction_boundary": {
            "added_vertices": list(range(8, 16)),
            "retained_internal_vertices": [0, 1],
            "added_internal_contacts": 0,
            "deleted_cap_collisions": 0,
            "formal_addresses": 16,
            "distinct_points": 16,
        },
        "relation": {
            "terminals": list(TERMINALS),
            "terminal_labels": [named[i][0] for i in TERMINALS],
            "input_formula": "palette(E0) intersects palette(E1) and palette(E1) intersects palette(E2)",
            "canonical_input_patterns": sorted(input_patterns),
            "canonical_output_patterns": sorted(output_patterns),
            "canonical_witnesses": dict(sorted(witnesses.items())),
            "named_input_assignments": named_input,
            "named_output_assignments": named_output,
            "newly_forbidden_assignments": named_input - named_output,
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, default=Path(__file__).with_name("certificate.json"))
    args = parser.parse_args()
    args.out.write_text(json.dumps(build(), indent=2, sort_keys=True) + "\n")


if __name__ == "__main__":
    main()
