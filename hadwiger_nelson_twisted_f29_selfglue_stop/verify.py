#!/usr/bin/env python3
"""Independent exact checker for the frozen twisted F29 self-gluing."""

from __future__ import annotations

from fractions import Fraction
import hashlib
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
RADS = (1, 3, 11, 33, 35, 105, 385, 1155)
RIDX = {r: i for i, r in enumerate(RADS)}
N = (4, 5, 6, 7, 9, 10, 12, 14, 15, 17, 18, 22, 25, 28)


def ensure(condition, message="verification failed"):
    if not condition:
        raise ValueError(message)


def reduce_rad(n: int) -> tuple[int, int]:
    square = 1
    rest = n
    p = 2
    while p * p <= rest:
        exponent = 0
        while rest % p == 0:
            rest //= p
            exponent += 1
        square *= p ** (exponent // 2)
        if exponent % 2:
            rest *= p
            rest //= p
        p += 1
    # The loop above has intentionally retained the squarefree residue only
    # through division.  Recompute it from n and the extracted square part.
    return square, n // (square * square)


class A:
    __slots__ = ("v",)

    def __init__(self, values=()):
        if isinstance(values, (int, Fraction)):
            values = {1: Fraction(values)}
        out = [Fraction(0)] * 8
        if isinstance(values, dict):
            for rad, coeff in values.items():
                out[RIDX[rad]] += Fraction(coeff)
        else:
            for i, coeff in enumerate(values):
                out[i] = Fraction(coeff)
        self.v = tuple(out)

    def __hash__(self):
        return hash(self.v)

    def __eq__(self, other):
        return isinstance(other, A) and self.v == other.v

    def __add__(self, other):
        return A(a + b for a, b in zip(self.v, other.v))

    def __sub__(self, other):
        return A(a - b for a, b in zip(self.v, other.v))

    def __neg__(self):
        return A(-a for a in self.v)

    def __mul__(self, other):
        out = {r: Fraction(0) for r in RADS}
        for i, x in enumerate(self.v):
            if not x:
                continue
            for j, y in enumerate(other.v):
                if not y:
                    continue
                factor, rad = reduce_rad(RADS[i] * RADS[j])
                ensure(rad in RIDX, "field basis is not closed")
                out[rad] += x * y * factor
        return A(out)

    def scale(self, q):
        return A(x * Fraction(q) for x in self.v)

    def row(self):
        return [[x.numerator, x.denominator] for x in self.v]


ZERO = A(0)
ONE = A(1)
Q = A({35: Fraction(1, 5)})


def padd(p, q):
    return p[0] + q[0], p[1] + q[1]


def psub(p, q):
    return p[0] - q[0], p[1] - q[1]


def phalf(p):
    return p[0].scale(Fraction(1, 2)), p[1].scale(Fraction(1, 2))


def n2(p):
    return p[0] * p[0] + p[1] * p[1]


def iq(p):
    return -(Q * p[1]), Q * p[0]


def load_source(path=HERE / "source_points.tsv"):
    out = []
    for line in path.read_text().splitlines():
        if not line or line.startswith("#"):
            continue
        label, a, b, c, d = map(int, line.split())
        ensure(label == len(out), "noncanonical source labels")
        x = A({1: Fraction(a, 12), 33: Fraction(b, 12)})
        y = A({3: Fraction(c, 12), 11: Fraction(d, 12)})
        out.append((x, y))
    ensure(len(out) == 29, "wrong source order")
    return out


def all_edges(points):
    return [
        [i, j]
        for i in range(len(points))
        for j in range(i + 1, len(points))
        if n2(psub(points[i], points[j])) == ONE
    ]


def build_geometry():
    source = load_source()
    s = padd(source[4], source[1])
    ensure(n2(s) == A(Fraction(5, 3)), "wrong role-sum norm")
    ensure(Q * Q == A(Fraction(7, 5)), "wrong intersection radical")
    w = padd(phalf(s), phalf(iq(s)))
    ensure(n2(w) == ONE and n2(psub(s, w)) == ONE, "invalid unit-circle intersection")
    # A nonzero sqrt(35)-containing coefficient certifies w is outside the
    # displayed source field, under the standard multiquadratic basis.
    ensure(any(w[c].v[i] for c in (0, 1) for i in range(4, 8)), "frame stayed in source field")
    second = [psub(w, p) for p in source]
    points = []
    index = {}
    maps = [[], []]
    for copy, rows in enumerate((source, second)):
        for p in rows:
            if p not in index:
                index[p] = len(points)
                points.append(p)
            maps[copy].append(index[p])
    return source, w, points, maps


def canonical_words(length, k=4):
    word = [0] * length

    def visit(pos, largest):
        if pos == length:
            yield tuple(word)
            return
        for colour in range(min(k - 1, largest + 1) + 1):
            word[pos] = colour
            yield from visit(pos + 1, max(largest, colour))

    word[0] = 0
    yield from visit(1, 0)


def find_colouring(n, edges, k, pins=None, allowed=None):
    adj = [set() for _ in range(n)]
    for a, b in edges:
        adj[a].add(b)
        adj[b].add(a)
    colour = [-1] * n
    pins = {} if pins is None else dict(pins)
    allowed = {} if allowed is None else {v: set(s) for v, s in allowed.items()}
    for v, c in pins.items():
        if c not in allowed.get(v, set(range(k))):
            return None
        colour[v] = c
    if any(colour[a] >= 0 and colour[a] == colour[b] for a, b in edges):
        return None

    def visit(done):
        if done == n:
            return True
        best = -1
        key = (-10**9, -1, -1)
        for v in range(n):
            if colour[v] >= 0:
                continue
            forbidden = {colour[u] for u in adj[v] if colour[u] >= 0}
            choices = allowed.get(v, set(range(k))) - forbidden
            candidate = (-len(choices), len(forbidden), len(adj[v]))
            if candidate > key:
                key, best = candidate, v
        forbidden = {colour[u] for u in adj[best] if colour[u] >= 0}
        choices = sorted(allowed.get(best, set(range(k))) - forbidden)
        for c in choices:
            colour[best] = c
            if visit(done + 1):
                return True
            colour[best] = -1
        return False

    return colour.copy() if visit(sum(c >= 0 for c in colour)) else None


def sha_rows(rows):
    blob = json.dumps(rows, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(blob).hexdigest()


def check_word(word, n, edges, pins=None):
    ensure(isinstance(word, str) and len(word) == n, "bad colour-word length")
    colours = [int(c) for c in word]
    ensure(set(colours) <= {0, 1, 2, 3}, "bad colour alphabet")
    ensure(all(colours[a] != colours[b] for a, b in edges), "improper colour word")
    if pins:
        ensure(all(colours[v] == c for v, c in pins.items()), "wrong pinned interface pattern")
    return colours


def verify_data(data):
    source, w, points, maps = build_geometry()
    source_edges = all_edges(source)
    edges = all_edges(points)
    ensure(len(source_edges) == data["source_edges"] == 75, "wrong source edge count")
    ensure(len(points) == data["physical_vertices"] == 58, "wrong physical order")
    ensure(len(edges) == data["complete_edges"] == 171, "wrong complete edge count")
    ensure(len(set(points)) == len(points), "unmerged collision")
    ensure(maps[0] == list(range(29)) and maps[1] == list(range(29, 58)), "unexpected collision map")
    ensure(data["collisions"] == [], "certificate claims a collision")

    internal = {
        tuple(sorted((maps[c][a], maps[c][b])))
        for c in (0, 1)
        for a, b in source_edges
    }
    extras = [e for e in edges if tuple(e) not in internal]
    ensure(len(internal) == data["internal_edge_union"] == 150, "wrong internal edge union")
    ensure(extras == data["extra_edge_rows"], "wrong cross-edge stream")
    ensure(len(extras) == data["extra_edges"] == 21, "wrong cross-edge count")
    ensure(data["prescribed_edge_rows"] == [[0, 29], [1, 33], [4, 30]], "wrong prescribed contacts")
    ensure(all(e in edges for e in data["prescribed_edge_rows"]), "missing prescribed contact")

    point_rows = [[x.row(), y.row()] for x, y in points]
    ensure(sha_rows(point_rows) == data["points_sha256"], "point hash mismatch")
    ensure(sha_rows(edges) == data["edges_sha256"], "edge hash mismatch")
    ensure([w[0].row(), w[1].row()] == data["w"], "frame coordinate mismatch")

    # Direct finite checks of the inherited forcing feature and chi(F29)=4.
    ensure(find_colouring(29, source_edges, 3) is None, "source unexpectedly three-colourable")
    source_minus_centre = [[a, b] for a, b in source_edges if a and b]
    ensure(find_colouring(
        29, source_minus_centre, 4, pins={0: 0, 4: 0},
        allowed={v: {0, 1} for v in N},
    ) is None, "source palette obstruction failed")

    whole = check_word(data["four_colour_word"], 58, edges)
    ensure(data["three_colourable"] is False, "wrong three-colour flag")
    ensure(data["four_colourable"] is True, "wrong four-colour flag")
    ensure([sorted({whole[maps[c][v]] for v in N}) for c in (0, 1)] == [[1, 2, 3], [0, 2, 3]], "wrong terminal palettes")

    terminals = [maps[0][0], maps[1][0], maps[0][4], maps[0][1], maps[1][4], maps[1][1]]
    ensure(terminals == data["active_interface_rows"], "wrong active interface")
    eset = {tuple(e) for e in edges}
    terminal_edges = [
        [a, b] for a in range(6) for b in range(a + 1, 6)
        if tuple(sorted((terminals[a], terminals[b]))) in eset
    ]
    ensure(terminal_edges == data["active_interface_edges"], "wrong active-interface edges")
    bare = []
    for pattern in canonical_words(6):
        if all(pattern[a] != pattern[b] for a, b in terminal_edges):
            bare.append("".join(map(str, pattern)))
    witnesses = data["active_interface_extension_words"]
    ensure(sorted(witnesses) == sorted(bare), "interface relation is not neutral")
    for pattern, word in witnesses.items():
        check_word(word, 58, edges, {terminals[i]: int(pattern[i]) for i in range(6)})
    ensure(len(bare) == data["active_interface_bare_patterns"] == 23, "wrong bare-pattern count")
    ensure(len(witnesses) == data["active_interface_extended_patterns"] == 23, "wrong extension count")
    ensure(data["active_interface_neutral"] is True, "wrong neutrality flag")

    return {
        "status": "VERIFIED_TWISTED_F29_SELFGLUE_FOURCOLOUR_STOP",
        "source_vertices": 29,
        "source_edges": 75,
        "physical_vertices": 58,
        "complete_edges": 171,
        "cross_edges": 21,
        "interface_patterns": 23,
        "interface_neutral": True,
        "chromatic_number": 4,
        "outside_source_field": True,
        "points_sha256": data["points_sha256"],
        "edges_sha256": data["edges_sha256"],
    }


def main():
    data = json.loads((HERE / "certificate.json").read_text())
    result = verify_data(data)
    expected = json.loads((HERE / "EXPECTED.json").read_text())
    ensure(result == expected, "headline result mismatch")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
