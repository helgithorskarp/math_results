#!/usr/bin/env python3
"""Independent exact verifier for the Petersen reflection-closure checkpoint.

This file imports no producer code and uses a Laurent-polynomial divisibility
test rather than arithmetic in the producer's quotient field.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import itertools
import json
from fractions import Fraction
from pathlib import Path


PHI20 = [Fraction(1), 0, -1, 0, 1, 0, -1, 0, 1]


def require(ok, message):
    if not ok:
        raise ValueError(message)


def parse_q(text):
    require(isinstance(text, str), "coefficient must be a string")
    try:
        q = Fraction(text)
    except Exception as exc:
        raise ValueError("invalid rational coefficient") from exc
    require(str(q.numerator) == text or f"{q.numerator}/{q.denominator}" == text,
            "coefficient is not canonical")
    return q


def parse_point(row):
    require(isinstance(row, list) and len(row) == 8, "point row must have length eight")
    return tuple(parse_q(x) for x in row)


def point_word(point):
    return [str(q.numerator) if q.denominator == 1 else f"{q.numerator}/{q.denominator}" for q in point]


def add(a, b):
    return tuple(x + y for x, y in zip(a, b))


def sub(a, b):
    return tuple(x - y for x, y in zip(a, b))


def norm_minus_one_laurent(a):
    """Coefficients of a(x)*a(x^-1)-1, exponents -7,...,7."""
    out = {e: Fraction(0) for e in range(-7, 8)}
    for i, x in enumerate(a):
        if x:
            for j, y in enumerate(a):
                if y:
                    out[i - j] += x * y
    out[0] -= 1
    return [out[e] for e in range(-7, 8)]


def divisible_by_phi20(poly):
    """Divide a degree-at-most-14 polynomial by monic Phi_20 exactly."""
    p = list(poly)
    require(len(p) == 15, "unexpected Laurent shift length")
    for k in range(14, 7, -1):
        q = p[k]
        if q:
            shift = k - 8
            for j, c in enumerate(PHI20):
                p[shift + j] -= q * c
    return all(x == 0 for x in p)


def is_unit_delta(a):
    # Multiplication by x^7 shifts Laurent exponents -7,...,7 to 0,...,14.
    return divisible_by_phi20(norm_minus_one_laurent(a))


def strict_edges(points):
    return [
        (i, j)
        for i in range(len(points))
        for j in range(i + 1, len(points))
        if is_unit_delta(sub(points[i], points[j]))
    ]


def reflect_round(points):
    edges = strict_edges(points)
    neighbours = [[] for _ in points]
    for u, v in edges:
        neighbours[u].append(v)
        neighbours[v].append(u)
    out = set(points)
    wedges = 0
    for r, ns in enumerate(neighbours):
        for p, q in itertools.combinations(ns, 2):
            x = sub(add(points[p], points[q]), points[r])
            require(is_unit_delta(sub(x, points[p])), "bad reflected p contact")
            require(is_unit_delta(sub(x, points[q])), "bad reflected q contact")
            out.add(x)
            wedges += 1
    return sorted(out), edges, wedges


def stream_hash(rows):
    raw = json.dumps(rows, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(raw).hexdigest()


def petersen_edges():
    out = set()
    for k in range(5):
        out.add(tuple(sorted((k, (k + 1) % 5))))
        out.add(tuple(sorted((5 + k, 5 + (k + 2) % 5))))
        out.add((k, 5 + k))
    return sorted(out)


def bare_patterns(terminal_edges):
    word = [0] * 10
    out = set()

    def rec(pos, used):
        if pos == 10:
            pattern = "".join(map(str, word))
            if all(word[u] != word[v] for u, v in terminal_edges):
                out.add(pattern)
            return
        for colour in range(min(used + 1, 4)):
            word[pos] = colour
            rec(pos + 1, max(used, colour + 1))

    rec(1, 1)
    return out


def exhaustive_k_colour(points_count, edges, k):
    adjacency = [set() for _ in range(points_count)]
    for u, v in edges:
        adjacency[u].add(v)
        adjacency[v].add(u)
    domains = [(1 << k) - 1] * points_count
    nodes = 0

    def propagate(current, stack):
        while stack:
            v = stack.pop()
            mask = current[v]
            if mask == 0 or mask & (mask - 1):
                continue
            for w in adjacency[v]:
                if current[w] & mask:
                    new = current[w] & ~mask
                    if new == 0:
                        return False
                    if new != current[w]:
                        current[w] = new
                        if not new & (new - 1):
                            stack.append(w)
        return True

    def search(current):
        nonlocal nodes
        nodes += 1
        choices = [v for v, mask in enumerate(current) if mask & (mask - 1)]
        if not choices:
            return current
        v = min(
            choices,
            key=lambda x: (
                current[x].bit_count(),
                -len({current[w] for w in adjacency[x] if not current[w] & (current[w] - 1)}),
                -len(adjacency[x]),
                x,
            ),
        )
        for bit in (1 << c for c in range(k)):
            if current[v] & bit:
                child = current.copy()
                child[v] = bit
                if propagate(child, [v]):
                    result = search(child)
                    if result is not None:
                        return result
        return None

    # On a graph with an edge, colour permutation permits this pinning.
    require(edges, "colour test requires an edge")
    u, v = edges[0]
    domains[u] = 1
    domains[v] = 2
    if not propagate(domains, [u, v]):
        return None, nodes
    return search(domains), nodes


def validate_certificate(data, points, edges, base, terminals, terminal_edges):
    require(data.get("schema") == "hn-petersen-reflection-v1", "wrong schema")
    require(data.get("terminals") == terminals, "wrong terminal indices")
    require(data.get("terminal_edges") == [list(e) for e in terminal_edges], "wrong terminal edges")
    require(data.get("point_hash") == stream_hash([point_word(p) for p in points]), "wrong point hash")
    require(data.get("edge_hash") == stream_hash([list(e) for e in edges]), "wrong edge hash")

    expected = bare_patterns(terminal_edges)
    rows = data.get("witnesses")
    require(isinstance(rows, list), "witnesses must be a list")
    actual = {}
    colour_checks = 0
    for row in rows:
        require(isinstance(row, list) and len(row) == 2, "bad witness row")
        pattern, word = row
        require(isinstance(pattern, str) and pattern in expected, "invalid terminal pattern")
        require(pattern not in actual, "duplicate terminal pattern")
        require(isinstance(word, str) and len(word) == len(points), "bad colour word length")
        require(set(word) <= set("0123"), "bad colour symbol")
        colours = [ord(x) - ord("0") for x in word]
        for u, v in edges:
            require(colours[u] != colours[v], "monochromatic certificate edge")
            colour_checks += 1
        require("".join(word[terminals[i]] for i in range(10)) == pattern,
                "word does not realize terminal pattern")
        actual[pattern] = word
    require(set(actual) == expected, "terminal relation coverage is incomplete")
    return len(expected), colour_checks


def verify(data, controls=False):
    base_rows = data.get("base_points")
    require(isinstance(base_rows, list) and len(base_rows) == 10, "need ten base points")
    base = [parse_point(row) for row in base_rows]
    require(len(set(base)) == 10, "base points are not distinct")
    require(strict_edges(base) == petersen_edges(), "base strict graph is not Petersen")

    points = sorted(base)
    computed_rounds = []
    supports = []
    for round_index in range(3):
        supports.append(points)
        nxt, round_edges, wedges = reflect_round(points)
        computed_rounds.append({
            "round": round_index,
            "vertices": len(points),
            "edges": len(round_edges),
            "wedges": wedges,
            "next_vertices": len(nxt),
        })
        if round_index < 2:
            points = nxt
    require(data.get("rounds") == computed_rounds, "wrong round census")
    edges = strict_edges(points)

    index = {p: i for i, p in enumerate(points)}
    terminals = [index[p] for p in base]
    terminal_index = {v: i for i, v in enumerate(terminals)}
    terminal_edges = sorted(
        (min(terminal_index[u], terminal_index[v]), max(terminal_index[u], terminal_index[v]))
        for u, v in edges
        if u in terminal_index and v in terminal_index
    )
    relation_size, colour_checks = validate_certificate(
        data, points, edges, base, terminals, terminal_edges
    )

    three_word, three_nodes = exhaustive_k_colour(len(points), edges, 3)
    require(three_word is None, "closure unexpectedly has a three-colouring")
    base_three, _ = exhaustive_k_colour(10, strict_edges(base), 3)
    require(base_three is not None, "Petersen control should be three-colourable")
    first_edges = strict_edges(supports[1])
    first_three, _ = exhaustive_k_colour(len(supports[1]), first_edges, 3)
    require(first_three is not None, "first closure should be three-colourable")

    adjacency = [set() for _ in points]
    for u, v in edges:
        adjacency[u].add(v)
        adjacency[v].add(u)
    triangles = sum(len(adjacency[u] & adjacency[v]) for u, v in edges) // 3
    require(triangles == 0, "expected triangle-free closure")

    controls_checked = 0
    if controls:
        mutations = []
        bad = copy.deepcopy(data)
        bad["point_hash"] = "0" * 64
        mutations.append(bad)
        bad = copy.deepcopy(data)
        bad["edge_hash"] = "0" * 64
        mutations.append(bad)
        bad = copy.deepcopy(data)
        bad["terminals"][0], bad["terminals"][1] = bad["terminals"][1], bad["terminals"][0]
        mutations.append(bad)
        bad = copy.deepcopy(data)
        bad["witnesses"].pop()
        mutations.append(bad)
        bad = copy.deepcopy(data)
        pattern, word = bad["witnesses"][0]
        u, v = edges[0]
        chars = list(word)
        chars[v] = chars[u]
        bad["witnesses"][0] = [pattern, "".join(chars)]
        mutations.append(bad)
        bad = copy.deepcopy(data)
        bad["witnesses"].append(copy.deepcopy(bad["witnesses"][0]))
        mutations.append(bad)
        for bad in mutations:
            try:
                validate_certificate(bad, points, edges, base, terminals, terminal_edges)
            except ValueError:
                controls_checked += 1
            else:
                raise ValueError("corrupted certificate was accepted")

    return {
        "status": "VERIFIED_PETERSEN_REFLECTION_CLOSURE",
        "rounds": computed_rounds,
        "final_vertices": len(points),
        "final_edges": len(edges),
        "triangles": triangles,
        "chromatic_number": 4,
        "three_colour_search_nodes": three_nodes,
        "bare_terminal_patterns": relation_size,
        "realized_terminal_patterns": relation_size,
        "forbidden_terminal_patterns": 0,
        "colour_words_checked": relation_size,
        "colour_edge_checks": colour_checks,
        "controls_checked": controls_checked,
        "point_hash": data["point_hash"],
        "edge_hash": data["edge_hash"],
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--certificate", type=Path, default=Path("certificate.json"))
    ap.add_argument("--check-expected", action="store_true")
    ap.add_argument("--controls", action="store_true")
    args = ap.parse_args()
    data = json.loads(args.certificate.read_text())
    result = verify(data, controls=args.controls)
    if args.check_expected:
        expected = json.loads(Path("expected.json").read_text())
        require(result == expected, "result does not match expected.json")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
