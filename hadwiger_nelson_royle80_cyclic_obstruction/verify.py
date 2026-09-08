#!/usr/bin/env python3
"""Exact verifier for the Royle-80 C20-equivariant plane obstruction."""

from __future__ import annotations

import argparse
from collections import deque
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import sys


HERE = Path(__file__).resolve().parent
N = 80
R = 4
S = 20
EXPECTED_ROWS = {
    "0": [1, 19, 32, -35, -32, -27, -23, -1],
    "1": [1, 16, 23, 27, 35, -19, -16, -1],
    "2": [1, 5, 13, 19, 32, -32, -23, -1],
    "3": [1, 16, 23, -19, -16, -13, -5, -1],
}
EXPECTED_TYPES = {
    (0, 0, 8),
    (0, 1, 0),
    (0, 1, 11),
    (0, 1, 13),
    (0, 1, 14),
    (0, 3, 4),
    (0, 3, 19),
    (1, 1, 4),
    (1, 2, 0),
    (1, 2, 15),
    (2, 2, 8),
    (2, 3, 0),
    (2, 3, 1),
    (2, 3, 3),
    (2, 3, 14),
    (3, 3, 4),
}
KEY_TYPES = [(0, 0, 8), (1, 1, 4), (0, 1, 0), (0, 1, 11)]
PRIMITIVE_K = [1, 3, 7, 9, 11, 13, 17, 19]


def need(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def edge(u: int, v: int) -> tuple[int, int]:
    need(u != v, "loop in LCF data")
    return (u, v) if u < v else (v, u)


def reconstruct(rows: dict[str, list[int]]) -> set[tuple[int, int]]:
    edges = set()
    for i in range(R):
        for j in range(S):
            u = i + R * j
            for t in rows[str(i)]:
                need(isinstance(t, int), "nonintegral LCF entry")
                edges.add(edge(u, (u + t) % N))
    return edges


def edge_type(u: int, v: int) -> tuple[int, int, int]:
    i, j = u % R, u // R
    ip, jp = v % R, v // R
    forward = (i, ip, (jp - j) % S)
    reverse = (ip, i, (j - jp) % S)
    return min(forward, reverse)


def graph_girth(adjacency: list[set[int]]) -> int:
    best = N + 1
    for root in range(N):
        distance = [-1] * N
        parent = [-1] * N
        distance[root] = 0
        queue = deque([root])
        while queue:
            u = queue.popleft()
            for v in adjacency[u]:
                if distance[v] < 0:
                    distance[v] = distance[u] + 1
                    parent[v] = u
                    queue.append(v)
                elif parent[u] != v:
                    best = min(best, distance[u] + distance[v] + 1)
    return best


# An element (a,b) denotes a + b*sqrt(5), with a,b rational.
Q5 = tuple[Fraction, Fraction]


def qadd(x: Q5, y: Q5) -> Q5:
    return (x[0] + y[0], x[1] + y[1])


def qneg(x: Q5) -> Q5:
    return (-x[0], -x[1])


def qmul(x: Q5, y: Q5) -> Q5:
    return (x[0] * y[0] + 5 * x[1] * y[1],
            x[0] * y[1] + x[1] * y[0])


def qinv(x: Q5) -> Q5:
    denominator = x[0] * x[0] - 5 * x[1] * x[1]
    need(denominator != 0, "division by zero in Q(sqrt(5))")
    return (x[0] / denominator, -x[1] / denominator)


def qscale(c: int | Fraction, x: Q5) -> Q5:
    return (c * x[0], c * x[1])


def qstr(x: Q5) -> str:
    def f(y: Fraction) -> str:
        return str(y.numerator) if y.denominator == 1 else f"{y.numerator}/{y.denominator}"
    if x[1] == 0:
        return f(x[0])
    sign = "+" if x[1] > 0 else "-"
    return f"{f(x[0])}{sign}{f(abs(x[1]))}*sqrt(5)"


def fifth_cosine(residue: int) -> Q5:
    residue %= 20
    if residue in (4, 16):
        return (Fraction(-1, 4), Fraction(1, 4))
    if residue in (8, 12):
        return (Fraction(-1, 4), Fraction(-1, 4))
    raise ValueError(f"unexpected cosine residue {residue}")


def radius_square(cosine: Q5) -> Q5:
    one_minus = qadd((Fraction(1), Fraction(0)), qneg(cosine))
    return qinv(qscale(2, one_minus))


def canonical_digest(items: list[object]) -> str:
    data = json.dumps(items, separators=(",", ":"), sort_keys=True).encode()
    return hashlib.sha256(data).hexdigest()


def verify(certificate_path: Path) -> dict[str, object]:
    certificate = json.loads(certificate_path.read_text())
    lcf = certificate["lcf"]
    need(lcf["r"] == R and lcf["s"] == S, "wrong LCF dimensions")
    need(lcf["rows"] == EXPECTED_ROWS, "LCF table differs from the pinned source")
    need(certificate["semiregular_automorphism"]["order"] == S,
         "wrong automorphism order")
    need([tuple(x) for x in certificate["required_edge_orbits"]] == KEY_TYPES,
         "the four proof edge orbits changed")

    edges = reconstruct(lcf["rows"])
    need(len(edges) == 320, "wrong edge count")
    adjacency = [set() for _ in range(N)]
    for u, v in edges:
        adjacency[u].add(v)
        adjacency[v].add(u)
    need({len(a) for a in adjacency} == {8}, "graph is not 8-regular")
    girth = graph_girth(adjacency)
    need(girth == 5, "graph does not have girth 5")

    shifted = {edge((u + R) % N, (v + R) % N) for u, v in edges}
    need(shifted == edges, "v -> v+4 is not an automorphism")
    types = {edge_type(u, v) for u, v in edges}
    need(types == EXPECTED_TYPES, "unexpected edge-orbit decomposition")
    orbit_counts = {t: 0 for t in types}
    for u, v in edges:
        orbit_counts[edge_type(u, v)] += 1
    need(set(orbit_counts.values()) == {20}, "edge orbit does not have length 20")
    need(all(t in types for t in KEY_TYPES), "a proof edge orbit is absent")

    colouring = certificate["five_colouring"]
    need(len(colouring) == N, "wrong colouring length")
    need(all(type(c) is int and 0 <= c < 5 for c in colouring),
         "colour outside 0,...,4")
    need(set(colouring) == set(range(5)), "colour certificate does not use five colours")
    need(all(colouring[u] != colouring[v] for u, v in edges),
         "improper five-colouring")

    radius_pairs = {}
    for k in PRIMITIVE_K:
        need(__import__("math").gcd(k, 20) == 1, "nonprimitive rotation exponent")
        r0_squared = radius_square(fifth_cosine(8 * k))
        r1_squared = radius_square(fifth_cosine(4 * k))
        need(qadd(r0_squared, r1_squared) == (Fraction(1), Fraction(0)),
             "radius-square sum identity failed")
        # Two perpendicularities whose phases differ by 11*k*pi/10
        # could coexist only if 10 divides 11*k.
        need((11 * k) % 10 != 0, "phase contradiction disappeared")
        radius_pairs[str(k)] = [qstr(r0_squared), qstr(r1_squared)]

    edge_list = [list(e) for e in sorted(edges)]
    type_list = [list(t) for t in sorted(types)]
    return {
        "status": "VERIFIED_ROYLE80_C20_EQUIVARIANT_OBSTRUCTION",
        "vertices": N,
        "edges": len(edges),
        "degree": 8,
        "girth": girth,
        "edge_orbits": len(types),
        "edge_orbit_size": 20,
        "key_edge_orbits": [list(t) for t in KEY_TYPES],
        "primitive_rotation_exponents": PRIMITIVE_K,
        "radius_square_pairs": radius_pairs,
        "phase_condition": "10 does not divide 11*k for every gcd(k,20)=1",
        "five_colouring_verified": True,
        "edge_list_sha256": canonical_digest(edge_list),
        "edge_orbits_sha256": canonical_digest(type_list),
        "five_colouring_sha256": canonical_digest(colouring),
        "scope": "no injective edge-preserving plane realization equivariant under v->v+4",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("certificate", nargs="?", type=Path,
                        default=HERE / "certificate.json")
    parser.add_argument("--skip-expected", action="store_true")
    args = parser.parse_args()
    result = verify(args.certificate)
    if not args.skip_expected:
        expected = json.loads((HERE / "EXPECTED.json").read_text())
        need(result == expected, "verification receipt differs from EXPECTED.json")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    try:
        main()
    except (KeyError, TypeError, ValueError, json.JSONDecodeError) as error:
        print(f"verification failed: {error}", file=sys.stderr)
        raise SystemExit(1)
