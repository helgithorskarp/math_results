#!/usr/bin/env python3
"""Definition-level independent checker for the square six-lens certificate."""

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
    """Quartics a0+a1*q+a2*q^2+a3*q^3 with q^4=3."""

    c: tuple[Fraction, Fraction, Fraction, Fraction]

    @staticmethod
    def scalar(x: int | Fraction) -> "R":
        return R((Fraction(x), Fraction(0), Fraction(0), Fraction(0)))

    def __add__(self, other: "R") -> "R":
        return R(tuple(a + b for a, b in zip(self.c, other.c)))  # type: ignore[arg-type]

    def __neg__(self) -> "R":
        return R(tuple(-a for a in self.c))  # type: ignore[arg-type]

    def __sub__(self, other: "R") -> "R":
        return self + (-other)

    def __mul__(self, other: "R") -> "R":
        raw = [Fraction(0) for _ in range(7)]
        for i, a in enumerate(self.c):
            for j, b in enumerate(other.c):
                raw[i + j] += a * b
        for degree in range(6, 3, -1):
            raw[degree - 4] += 3 * raw[degree]
        return R(tuple(raw[:4]))  # type: ignore[arg-type]

    def scale(self, x: int | Fraction) -> "R":
        return R(tuple(Fraction(x) * a for a in self.c))  # type: ignore[arg-type]


@dataclass(frozen=True)
class E:
    """A+B*s over R, with s^2=2."""

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
        return E(self.a * other.a + (self.b * other.b).scale(2), self.a * other.b + self.b * other.a)

    def scale(self, x: int | Fraction) -> "E":
        return E(self.a.scale(x), self.b.scale(x))


Z, O = E.scalar(0), E.scalar(1)
q = E(R((Fraction(0), Fraction(1), Fraction(0), Fraction(0))), R.scalar(0))
s = E(R.scalar(0), R.scalar(1))
Point = tuple[E, E]


def norm_difference(p: Point, r: Point) -> E:
    x, y = p[0] - r[0], p[1] - r[1]
    return x * x + y * y


def reconstruct() -> list[tuple[str, Point]]:
    root3 = q * q
    a = (s * root3 - s).scale(Fraction(1, 2))
    h = (s * root3 + s).scale(Fraction(1, 4))
    ah, qh = a.scale(Fraction(1, 2)), q.scale(Fraction(1, 2))
    return [
        ("C0", (-ah, -ah)), ("C1", (ah, -ah)), ("C2", (ah, ah)), ("C3", (-ah, ah)),
        ("L01+", (Z, -ah + h)), ("L01-", (Z, -ah - h)),
        ("L02+", (-qh, qh)), ("L02-", (qh, -qh)),
        ("L03+", (-ah - h, Z)), ("L03-", (-ah + h, Z)),
        ("L12+", (ah - h, Z)), ("L12-", (ah + h, Z)),
        ("L13+", (-qh, -qh)), ("L13-", (qh, qh)),
        ("L23+", (Z, ah - h)), ("L23-", (Z, ah + h)),
    ]


def parse_fraction(text: str) -> Fraction:
    return Fraction(text)


def parse_element(values: list[str]) -> E:
    if len(values) != 8:
        raise ValueError("bad coordinate width")
    vals = [parse_fraction(x) for x in values]
    return E(R(tuple(vals[:4])), R(tuple(vals[4:])))  # type: ignore[arg-type]


def digest(rows: object) -> str:
    raw = json.dumps(rows, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(raw).hexdigest()


def check_word(word: str, edges: list[tuple[int, int]], colors: int) -> None:
    if len(word) != 16 or any(c not in "0123"[:colors] for c in word):
        raise ValueError("bad colour word")
    if any(word[u] == word[v] for u, v in edges):
        raise ValueError("improper colour word")


def canonical(values: tuple[int, ...]) -> str:
    rename: dict[int, int] = {}
    out = []
    for x in values:
        if x not in rename:
            rename[x] = len(rename)
        out.append(rename[x])
    return "".join(map(str, out))


def canonical_patterns() -> list[str]:
    return sorted({canonical(values) for values in itertools.product(range(4), repeat=4)})


def verify_certificate(cert: dict[str, object]) -> dict[str, object]:
    if cert.get("format") != "hn-square-six-lens-neutrality-v1":
        raise ValueError("bad format")
    expected = reconstruct()
    if len({p for _, p in expected}) != 16:
        raise ValueError("reconstructed collision")
    rows = cert.get("points")
    if not isinstance(rows, list) or len(rows) != 16:
        raise ValueError("bad points")
    parsed: list[Point] = []
    for row, (label, point) in zip(rows, expected):
        if not isinstance(row, dict) or row.get("label") != label:
            raise ValueError("point label mismatch")
        got = (parse_element(row["x"]), parse_element(row["y"]))
        if got != point:
            raise ValueError("point coordinate mismatch")
        parsed.append(got)
    if cert.get("point_rows_sha256") != digest(rows):
        raise ValueError("point hash mismatch")
    exact_edges = [
        (u, v)
        for u in range(16)
        for v in range(u + 1, 16)
        if norm_difference(parsed[u], parsed[v]) == O
    ]
    edge_rows = cert.get("edges")
    if not isinstance(edge_rows, list):
        raise ValueError("bad edges")
    edges = [tuple(row) for row in edge_rows]
    if edges != exact_edges or len(edges) != 28:
        raise ValueError("incomplete or incorrect unit graph")
    if cert.get("edge_rows_sha256") != digest(edge_rows):
        raise ValueError("edge hash mismatch")
    chromatic = cert.get("chromatic")
    if not isinstance(chromatic, dict) or chromatic.get("number") != 3:
        raise ValueError("bad chromatic block")
    triangle = tuple(chromatic.get("triangle", []))
    if len(triangle) != 3 or any(tuple(sorted(edge)) not in edges for edge in itertools.combinations(triangle, 2)):
        raise ValueError("bad triangle lower bound")
    check_word(chromatic.get("three_colouring", ""), edges, 3)
    relation = cert.get("relation")
    if not isinstance(relation, dict) or relation.get("bare_terminal_edges") != []:
        raise ValueError("bad terminal graph")
    pats = canonical_patterns()
    if relation.get("canonical_bare_patterns") != pats or relation.get("canonical_extendible_patterns") != pats:
        raise ValueError("incomplete canonical relation")
    witnesses = relation.get("canonical_witnesses")
    if not isinstance(witnesses, dict) or sorted(witnesses) != pats:
        raise ValueError("bad witness keys")
    for pattern in pats:
        word = witnesses[pattern]
        check_word(word, edges, 4)
        if word[:4] != pattern:
            raise ValueError("witness terminal mismatch")
    # Construct and check a concrete extension for every named assignment.
    named_checked = 0
    for assignment in itertools.product(range(4), repeat=4):
        pattern = canonical(assignment)
        base_word = witnesses[pattern]
        image: dict[int, int] = {}
        for c, x in zip(map(int, pattern), assignment):
            image[c] = x
        unused = [x for x in range(4) if x not in image.values()]
        for c in range(4):
            if c not in image:
                image[c] = unused.pop(0)
        word = "".join(str(image[int(c)]) for c in base_word)
        check_word(word, edges, 4)
        if tuple(map(int, word[:4])) != assignment:
            raise ValueError("named witness mismatch")
        named_checked += 1
    if relation.get("named_bare_assignments") != named_checked or relation.get("named_extendible_assignments") != named_checked:
        raise ValueError("bad named relation counts")
    degrees = sorted((sum(u == v or w == v for u, w in edges) for v in range(16)), reverse=True)
    extra_cycle = [(4, 9), (4, 10), (9, 14), (10, 14)]
    if any(edge not in edges for edge in extra_cycle):
        raise ValueError("missing inner lens cycle")
    return {
        "status": "VERIFIED_SQUARE_SIX_LENS_NEUTRALITY",
        "points": 16,
        "edges": 28,
        "chromatic_number": 3,
        "degree_sequence": degrees,
        "canonical_terminal_patterns": 15,
        "named_terminal_assignments": named_checked,
        "forbidden_terminal_patterns": 0,
        "inner_lens_cycle": [list(edge) for edge in extra_cycle],
        "point_rows_sha256": cert["point_rows_sha256"],
        "edge_rows_sha256": cert["edge_rows_sha256"],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certificate", type=Path, default=Path(__file__).with_name("certificate.json"))
    parser.add_argument("--check-expected", action="store_true")
    args = parser.parse_args()
    cert = json.loads(args.certificate.read_text())
    report = verify_certificate(cert)
    if args.check_expected:
        expected = json.loads(Path(__file__).with_name("expected.json").read_text())
        if report != expected:
            raise SystemExit("expected report mismatch")
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
