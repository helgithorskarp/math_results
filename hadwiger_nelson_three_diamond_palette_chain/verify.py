#!/usr/bin/env python3
"""Definition-level independent verifier for the three-diamond certificate."""

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
    """a+b*s with s^2=3."""

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

    def scale(self, x: int | Fraction) -> "R":
        return R(Fraction(x) * self.a, Fraction(x) * self.b)


@dataclass(frozen=True)
class E:
    """A+B*y over Q(s), with y^2=2-s/2."""

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

    def scale(self, x: int | Fraction) -> "E":
        return E(self.a.scale(x), self.b.scale(x))


ZERO, ONE = E.scalar(0), E.scalar(1)
S = E(R(Fraction(0), Fraction(1)), R.scalar(0))
Y = E(R.scalar(0), R.scalar(1))
Point = tuple[E, E]


def norm_difference(p: Point, q: Point) -> E:
    dx, dy = p[0] - q[0], p[1] - q[1]
    return dx * dx + dy * dy


def reconstruct() -> list[tuple[str, Point]]:
    caps = [
        (ZERO, ZERO),
        ((ONE + S).scale(Fraction(1, 2)), Y),
        ((ONE - S).scale(Fraction(1, 2)), Y),
        (ONE, ZERO),
    ]
    out = [(f"P{i}", p) for i, p in enumerate(caps)]
    for i, (p, q) in enumerate(zip(caps, caps[1:])):
        dx, dy = q[0] - p[0], q[1] - p[1]
        mid = ((p[0] + q[0]).scale(Fraction(1, 2)), (p[1] + q[1]).scale(Fraction(1, 2)))
        offset = ((-dy * S).scale(Fraction(1, 6)), (dx * S).scale(Fraction(1, 6)))
        out.append((f"X{i}", (mid[0] + offset[0], mid[1] + offset[1])))
        out.append((f"Y{i}", (mid[0] - offset[0], mid[1] - offset[1])))
    return out


def parse_element(row: object) -> E:
    if not isinstance(row, list) or len(row) != 4 or not all(isinstance(x, str) for x in row):
        raise ValueError("bad field element")
    a, b, c, d = map(Fraction, row)
    return E(R(a, b), R(c, d))


def digest(rows: object) -> str:
    raw = json.dumps(rows, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(raw).hexdigest()


def adjacency(n: int, edges: list[tuple[int, int]]) -> list[set[int]]:
    adj = [set() for _ in range(n)]
    for u, v in edges:
        adj[u].add(v)
        adj[v].add(u)
    return adj


def extension(adj: list[set[int]], k: int, fixed: dict[int, int]) -> tuple[int, ...] | None:
    word = [-1] * len(adj)
    for v, c in fixed.items():
        if not 0 <= v < len(adj) or not 0 <= c < k:
            return None
        word[v] = c
    if any(word[u] >= 0 and word[u] == word[v] for u in range(len(adj)) for v in adj[u]):
        return None

    def search() -> bool:
        best = -1
        score = (-1, -1)
        for v, c in enumerate(word):
            if c < 0:
                current = (len({word[w] for w in adj[v] if word[w] >= 0}), len(adj[v]))
                if current > score:
                    best, score = v, current
        if best < 0:
            return True
        forbidden = {word[w] for w in adj[best] if word[w] >= 0}
        for c in range(k - 1, -1, -1):
            if c not in forbidden:
                word[best] = c
                if search():
                    return True
        word[best] = -1
        return False

    return tuple(word) if search() else None


def check_word(text: object, edges: list[tuple[int, int]], k: int) -> tuple[int, ...]:
    if not isinstance(text, str) or len(text) != 10 or any(c not in "0123"[:k] for c in text):
        raise ValueError("bad colour word")
    word = tuple(map(int, text))
    if any(word[u] == word[v] for u, v in edges):
        raise ValueError("improper colour word")
    return word


def canonical(values: tuple[int, ...]) -> str:
    rename: dict[int, int] = {}
    out = []
    for x in values:
        if x not in rename:
            rename[x] = len(rename)
        out.append(rename[x])
    return "".join(map(str, out))


def formula(values: tuple[int, ...]) -> bool:
    e0, e1, e2 = ({values[2 * i], values[2 * i + 1]} for i in range(3))
    return bool(e0 & e1) and bool(e1 & e2)


def verify(cert: dict[str, object]) -> dict[str, object]:
    if cert.get("format") != "hn-three-diamond-palette-chain-v1":
        raise ValueError("bad format")
    expected = reconstruct()
    if len(expected) != 10 or len({p for _, p in expected}) != 10:
        raise ValueError("coordinate collision")
    rows = cert.get("points")
    if not isinstance(rows, list) or len(rows) != 10:
        raise ValueError("bad point rows")
    parsed: list[Point] = []
    for row, (label, point) in zip(rows, expected):
        if not isinstance(row, dict) or row.get("label") != label:
            raise ValueError("point label mismatch")
        got = (parse_element(row.get("x")), parse_element(row.get("y")))
        if got != point:
            raise ValueError("point coordinate mismatch")
        parsed.append(got)
    if cert.get("point_rows_sha256") != digest(rows):
        raise ValueError("point hash mismatch")
    exact_edges = [(u, v) for u, v in itertools.combinations(range(10), 2) if norm_difference(parsed[u], parsed[v]) == ONE]
    edge_rows = cert.get("edges")
    if not isinstance(edge_rows, list):
        raise ValueError("bad edge rows")
    edges = [tuple(row) for row in edge_rows]
    if edges != exact_edges or len(edges) != 16:
        raise ValueError("incomplete or incorrect unit graph")
    if cert.get("edge_rows_sha256") != digest(edge_rows):
        raise ValueError("edge hash mismatch")
    adj = adjacency(10, edges)

    chromatic = cert.get("chromatic")
    if not isinstance(chromatic, dict) or chromatic.get("number") != 4:
        raise ValueError("bad chromatic block")
    diamonds = chromatic.get("diamonds")
    if diamonds != [[0, 1, 4, 5], [1, 2, 6, 7], [2, 3, 8, 9]] or chromatic.get("closing_edge") != [0, 3]:
        raise ValueError("bad structural lower-bound data")
    for a, b, x, y in diamonds:
        required = {(min(u, v), max(u, v)) for u, v in [(a, x), (a, y), (b, x), (b, y), (x, y)]}
        if not required.issubset(edges) or (a, b) in edges:
            raise ValueError("bad diamond")
    if (0, 3) not in edges or extension(adj, 3, {}) is not None:
        raise ValueError("three-colour lower bound failed")
    check_word(chromatic.get("four_colouring"), edges, 4)

    relation = cert.get("relation")
    if not isinstance(relation, dict):
        raise ValueError("bad relation block")
    terminals = (4, 5, 6, 7, 8, 9)
    if relation.get("terminals") != list(terminals) or relation.get("bare_terminal_edges") != [[4, 5], [6, 7], [8, 9]]:
        raise ValueError("bad terminal definition")
    witnesses = relation.get("canonical_witnesses")
    if not isinstance(witnesses, dict):
        raise ValueError("bad witnesses")
    bare_named = allowed_named = 0
    bare_canonical: set[str] = set()
    allowed_canonical: set[str] = set()
    for assignment in itertools.product(range(4), repeat=6):
        if any(assignment[2 * i] == assignment[2 * i + 1] for i in range(3)):
            continue
        bare_named += 1
        pat = canonical(assignment)
        bare_canonical.add(pat)
        got = extension(adj, 4, dict(zip(terminals, assignment))) is not None
        if got != formula(assignment):
            raise ValueError("formula mismatch")
        if got:
            allowed_named += 1
            allowed_canonical.add(pat)
    if relation.get("canonical_bare_patterns") != sorted(bare_canonical):
        raise ValueError("bad bare relation")
    if relation.get("canonical_extendible_patterns") != sorted(allowed_canonical):
        raise ValueError("bad extendible relation")
    if set(witnesses) != allowed_canonical:
        raise ValueError("incomplete witness keys")
    for pattern, text in witnesses.items():
        word = check_word(text, edges, 4)
        if canonical(tuple(word[v] for v in terminals)) != pattern:
            raise ValueError("terminal witness mismatch")
    forbidden_named = bare_named - allowed_named
    if (relation.get("named_bare_assignments"), relation.get("named_extendible_assignments"), relation.get("named_forbidden_assignments")) != (bare_named, allowed_named, forbidden_named):
        raise ValueError("bad relation counts")
    return {
        "status": "VERIFIED_THREE_DIAMOND_PALETTE_CHAIN",
        "points": 10,
        "edges": 16,
        "chromatic_number": 4,
        "terminal_edges": 3,
        "canonical_bare_patterns": len(bare_canonical),
        "canonical_extendible_patterns": len(allowed_canonical),
        "canonical_forbidden_patterns": len(bare_canonical - allowed_canonical),
        "named_bare_assignments": bare_named,
        "named_extendible_assignments": allowed_named,
        "named_forbidden_assignments": forbidden_named,
        "relation_formula_exact": True,
        "point_rows_sha256": cert["point_rows_sha256"],
        "edge_rows_sha256": cert["edge_rows_sha256"],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certificate", type=Path, default=Path(__file__).with_name("certificate.json"))
    parser.add_argument("--check-expected", action="store_true")
    args = parser.parse_args()
    cert = json.loads(args.certificate.read_text())
    report = verify(cert)
    if args.check_expected:
        expected = json.loads(Path(__file__).with_name("expected.json").read_text())
        if report != expected:
            raise SystemExit("expected report mismatch")
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
