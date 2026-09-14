#!/usr/bin/env python3
"""Independent definition-level checker for the reflected-lens interaction."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path


@dataclass(frozen=True)
class R:
    a: Fraction
    b: Fraction

    @staticmethod
    def scalar(x: int | Fraction) -> "R":
        return R(Fraction(x), Fraction(0))

    def __add__(self, other: "R") -> "R":
        return R(self.a + other.a, self.b + other.b)

    def __neg__(self) -> "R":
        return R(-self.a, -self.b)

    def __sub__(self, other: "R") -> "R":
        return self + (-other)

    def __mul__(self, other: "R") -> "R":
        return R(self.a * other.a + 3 * self.b * other.b, self.a * other.b + self.b * other.a)

    def scale(self, q: int | Fraction) -> "R":
        return R(Fraction(q) * self.a, Fraction(q) * self.b)


@dataclass(frozen=True)
class E:
    a: R
    b: R

    @staticmethod
    def scalar(x: int | Fraction) -> "E":
        return E(R.scalar(x), R.scalar(0))

    def __add__(self, other: "E") -> "E":
        return E(self.a + other.a, self.b + other.b)

    def __neg__(self) -> "E":
        return E(-self.a, -self.b)

    def __sub__(self, other: "E") -> "E":
        return self + (-other)

    def __mul__(self, other: "E") -> "E":
        q = R(Fraction(2), Fraction(-1, 2))
        return E(self.a * other.a + self.b * other.b * q, self.a * other.b + self.b * other.a)

    def scale(self, q: int | Fraction) -> "E":
        return E(self.a.scale(q), self.b.scale(q))


Z, O = E.scalar(0), E.scalar(1)
S = E(R(Fraction(0), Fraction(1)), R.scalar(0))
Y = E(R.scalar(0), R.scalar(1))
Point = tuple[E, E]
NAMES = ("P1", "P2", "X0", "Y0", "X1", "Y1", "X2", "Y2")
TERMINALS = (2, 3, 4, 5, 6, 7)


def dist2(p: Point, q: Point) -> E:
    dx, dy = p[0] - q[0], p[1] - q[1]
    return dx * dx + dy * dy


def reconstruct() -> tuple[list[tuple[str, Point]], tuple[Point, Point]]:
    caps = [
        (Z, Z), ((O + S).scale(Fraction(1, 2)), Y),
        ((O - S).scale(Fraction(1, 2)), Y), (O, Z),
    ]
    original = {f"P{i}": p for i, p in enumerate(caps)}
    for i, (p, q) in enumerate(zip(caps, caps[1:])):
        dx, dy = q[0] - p[0], q[1] - p[1]
        mid = ((p[0] + q[0]).scale(Fraction(1, 2)), (p[1] + q[1]).scale(Fraction(1, 2)))
        off = ((-dy * S).scale(Fraction(1, 6)), (dx * S).scale(Fraction(1, 6)))
        original[f"X{i}"] = (mid[0] + off[0], mid[1] + off[1])
        original[f"Y{i}"] = (mid[0] - off[0], mid[1] - off[1])
    out = [(name, original[name]) for name in NAMES]
    for centre, left, right in (("P1", ("X0", "Y0"), ("X1", "Y1")),
                                ("P2", ("X1", "Y1"), ("X2", "Y2"))):
        for a in left:
            for b in right:
                out.append((f"R{centre[-1]}_{a}_{b}",
                            (original[a][0] + original[b][0] - original[centre][0],
                             original[a][1] + original[b][1] - original[centre][1])))
    return out, (original["P0"], original["P3"])


def parse_element(row: object) -> E:
    if not isinstance(row, list) or len(row) != 4 or not all(isinstance(x, str) for x in row):
        raise ValueError("bad field row")
    a, b, c, d = map(Fraction, row)
    return E(R(a, b), R(c, d))


def digest(value: object) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def adjacency(n: int, edges: list[tuple[int, int]]) -> list[set[int]]:
    out = [set() for _ in range(n)]
    for u, v in edges:
        out[u].add(v)
        out[v].add(u)
    return out


def extension(adj: list[set[int]], k: int, fixed: dict[int, int]) -> tuple[int, ...] | None:
    word = [-1] * len(adj)
    for v, c in fixed.items():
        if not 0 <= v < len(adj) or not 0 <= c < k:
            return None
        word[v] = c
    if any(word[u] >= 0 and word[u] == word[v] for u in range(len(adj)) for v in adj[u]):
        return None

    def visit() -> bool:
        options = [v for v, c in enumerate(word) if c < 0]
        if not options:
            return True
        v = max(options, key=lambda z: (len({word[w] for w in adj[z] if word[w] >= 0}), len(adj[z])))
        forbidden = {word[w] for w in adj[v] if word[w] >= 0}
        for c in range(k - 1, -1, -1):
            if c not in forbidden:
                word[v] = c
                if visit():
                    return True
        word[v] = -1
        return False

    return tuple(word) if visit() else None


def formula(values: tuple[int, ...]) -> bool:
    if any(values[2 * i] == values[2 * i + 1] for i in range(3)):
        return False
    e0, e1, e2 = ({values[2 * i], values[2 * i + 1]} for i in range(3))
    return bool(e0 & e1) and bool(e1 & e2)


def canonical(values: tuple[int, ...]) -> str:
    rename: dict[int, int] = {}
    return "".join(str(rename.setdefault(x, len(rename))) for x in values)


def check_word(text: object, edges: list[tuple[int, int]], k: int) -> tuple[int, ...]:
    if not isinstance(text, str) or len(text) != 16 or any(c not in "0123"[:k] for c in text):
        raise ValueError("bad colour word")
    word = tuple(map(int, text))
    if any(word[u] == word[v] for u, v in edges):
        raise ValueError("improper colour word")
    return word


def verify(cert: dict[str, object]) -> dict[str, object]:
    if cert.get("format") != "hn-three-diamond-reflected-lens-neutrality-v1":
        raise ValueError("bad format")
    expected, deleted = reconstruct()
    if len(expected) != 16 or len({p for _, p in expected}) != 16:
        raise ValueError("exact collision")
    rows = cert.get("points")
    if not isinstance(rows, list) or len(rows) != 16:
        raise ValueError("bad points")
    points = []
    for row, (label, point) in zip(rows, expected):
        if not isinstance(row, dict) or row.get("label") != label:
            raise ValueError("label mismatch")
        got = (parse_element(row.get("x")), parse_element(row.get("y")))
        if got != point:
            raise ValueError("coordinate mismatch")
        points.append(got)
    if cert.get("point_rows_sha256") != digest(rows):
        raise ValueError("point hash mismatch")
    if any(points[i] in deleted for i in range(8, 16)):
        raise ValueError("deleted cap collision")
    if any(dist2(points[i], points[j]) in (Z, O) for i in range(8, 16) for j in (0, 1)):
        raise ValueError("forbidden internal contact")
    exact_edges = [(u, v) for u, v in itertools.combinations(range(16), 2) if dist2(points[u], points[v]) == O]
    edge_rows = cert.get("edges")
    if not isinstance(edge_rows, list):
        raise ValueError("bad edges")
    edges = [tuple(row) for row in edge_rows]
    if edges != exact_edges or len(edges) != 35:
        raise ValueError("incomplete unit graph")
    if cert.get("edge_rows_sha256") != digest(edge_rows):
        raise ValueError("edge hash mismatch")
    adj = adjacency(16, edges)
    chromatic = cert.get("chromatic")
    if not isinstance(chromatic, dict) or chromatic.get("number") != 3 or chromatic.get("triangle") != [0, 2, 3]:
        raise ValueError("bad chromatic data")
    if not all(tuple(sorted(e)) in edges for e in itertools.combinations((0, 2, 3), 2)):
        raise ValueError("missing triangle")
    check_word(chromatic.get("three_colouring"), edges, 3)
    if extension(adj, 2, {}) is not None:
        raise ValueError("unexpected two-colouring")
    boundary = cert.get("interaction_boundary")
    if not isinstance(boundary, dict) or boundary.get("added_internal_contacts") != 0 or boundary.get("deleted_cap_collisions") != 0:
        raise ValueError("bad interaction boundary")

    relation = cert.get("relation")
    if not isinstance(relation, dict) or relation.get("terminals") != list(TERMINALS):
        raise ValueError("bad relation")
    input_patterns: set[str] = set()
    output_patterns: set[str] = set()
    named_input = named_output = 0
    for assignment in itertools.product(range(4), repeat=6):
        if not formula(assignment):
            continue
        named_input += 1
        pat = canonical(assignment)
        input_patterns.add(pat)
        if extension(adj, 4, dict(zip(TERMINALS, assignment))) is not None:
            named_output += 1
            output_patterns.add(pat)
    if input_patterns != output_patterns:
        raise ValueError("interaction strengthened relation")
    if relation.get("canonical_input_patterns") != sorted(input_patterns) or relation.get("canonical_output_patterns") != sorted(output_patterns):
        raise ValueError("pattern rows mismatch")
    if (relation.get("named_input_assignments"), relation.get("named_output_assignments"), relation.get("newly_forbidden_assignments")) != (named_input, named_output, 0):
        raise ValueError("named counts mismatch")
    witnesses = relation.get("canonical_witnesses")
    if not isinstance(witnesses, dict) or set(witnesses) != output_patterns:
        raise ValueError("witness keys mismatch")
    for pattern, text in witnesses.items():
        word = check_word(text, edges, 4)
        if canonical(tuple(word[v] for v in TERMINALS)) != pattern:
            raise ValueError("witness terminal mismatch")
    return {
        "status": "VERIFIED_REFLECTED_LENS_INTERACTION_NEUTRALITY",
        "points": 16,
        "edges": 35,
        "chromatic_number": 3,
        "all_pairs": 120,
        "added_vertices": 8,
        "added_internal_contacts": 0,
        "deleted_cap_collisions": 0,
        "canonical_input_patterns": len(input_patterns),
        "canonical_output_patterns": len(output_patterns),
        "named_input_assignments": named_input,
        "named_output_assignments": named_output,
        "newly_forbidden_assignments": 0,
        "point_rows_sha256": cert["point_rows_sha256"],
        "edge_rows_sha256": cert["edge_rows_sha256"],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certificate", type=Path, default=Path(__file__).with_name("certificate.json"))
    parser.add_argument("--check-expected", action="store_true")
    args = parser.parse_args()
    report = verify(json.loads(args.certificate.read_text()))
    if args.check_expected:
        expected = json.loads(Path(__file__).with_name("expected.json").read_text())
        if report != expected:
            raise SystemExit("expected report mismatch")
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
