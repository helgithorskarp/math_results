#!/usr/bin/env python3
"""Independent exact checker using denominator-clearing Ramanujan traces."""

import argparse
from collections import Counter, defaultdict
from itertools import combinations, product
import hashlib
import json
from fractions import Fraction
from math import gcd
from pathlib import Path

HERE = Path(__file__).resolve().parent
N = 30
KS = (2, 3, 4, 5, 8, 9, 14)
TERMINAL_ADDRESSES = (
    (2, 0), (3, 2), (3, 0), (8, 1),
    (4, 0), (9, 7), (9, 0), (14, 13),
)


def require(condition, message):
    if not condition:
        raise ValueError(message)


def dump(obj):
    return json.dumps(obj, sort_keys=True, separators=(",", ":")) + "\n"


def digest(obj):
    return hashlib.sha256(dump(obj).encode()).hexdigest()


def mobius(n):
    parity = 0
    p = 2
    while p * p <= n:
        if n % p == 0:
            n //= p
            parity += 1
            if n % p == 0:
                return 0
        p += 1
    return (-1) ** (parity + (n > 1))


RAMANUJAN = tuple(sum(d * mobius(N // d) for d in range(1, N + 1)
                       if N % d == 0 and k % d == 0)
                   for k in range(N))


def add(a, b, scale=1):
    return tuple(x + scale * y for x, y in zip(a, b))


def monomial(j, scale=1):
    answer = [0] * N
    answer[j % N] = scale
    return tuple(answer)


def multiply(a, b):
    answer = [0] * N
    for j, x in enumerate(a):
        if x:
            for k, y in enumerate(b):
                if y:
                    answer[(j + k) % N] += x * y
    return tuple(answer)


def conjugate(a):
    return tuple(a[-j % N] for j in range(N))


def trace(a):
    return tuple(sum(c * RAMANUJAN[(j - k) % N]
                     for j, c in enumerate(a) if c)
                 for k in range(N))


def is_zero(a):
    return not any(trace(a))


def address_fraction(address):
    k, j = address
    if k == 0:
        return (0,) * N, monomial(0)
    return monomial(j), add(monomial(0), monomial(k), -1)


def difference(a, b):
    an, ad = address_fraction(a)
    bn, bd = address_fraction(b)
    return add(multiply(an, bd), multiply(bn, ad), -1), multiply(ad, bd)


def coincident(a, b):
    numerator, _ = difference(a, b)
    return is_zero(numerator)


def unit_distance(a, b):
    numerator, denominator = difference(a, b)
    squared_numerator = multiply(numerator, conjugate(numerator))
    squared_denominator = multiply(denominator, conjugate(denominator))
    return is_zero(add(squared_numerator, squared_denominator, -1))


def geometry():
    addresses = [(0, 0)] + [(k, j) for k in KS for j in range(N)]
    require(len(addresses) == 211, "address count")
    for a, b in combinations(addresses, 2):
        require(not coincident(a, b), "unexpected physical collision")
    edges = [(a, b) for a, b in combinations(range(len(addresses)), 2)
             if unit_distance(addresses[a], addresses[b])]
    index = {address: j for j, address in enumerate(addresses)}
    terminals = tuple(index[address] for address in TERMINAL_ADDRESSES)
    return addresses, edges, terminals


def adjacency(vertex_count, edges):
    answer = [set() for _ in range(vertex_count)]
    for a, b in edges:
        require(0 <= a < b < vertex_count and b not in answer[a], "edge domain")
        answer[a].add(b)
        answer[b].add(a)
    return answer


def check_word(word, colours, adj, pins=None):
    require(type(word) is str and len(word) == len(adj)
            and set(word) <= set(map(str, range(colours))), "colour word shape")
    values = tuple(map(int, word))
    require(all(values[a] != values[b] for a in range(len(adj)) for b in adj[a]
                if a < b), "improper colour word")
    if pins is not None:
        require(all(values[v] == c for v, c in pins), "terminal pin mismatch")
    return values


def canonical_patterns(terminal_edges):
    answer = []
    for word in product(range(4), repeat=8):
        if word[0] != 0:
            continue
        if any(word[j] > 1 + max(word[:j], default=-1) for j in range(8)):
            continue
        if any(word[a] == word[b] for a, b in terminal_edges):
            continue
        answer.append("".join(map(str, word)))
    return answer


def incidence(addresses, edges):
    rows = defaultdict(Counter)
    for a, b in edges:
        ka, ja = addresses[a]
        kb, jb = addresses[b]
        if ka > kb:
            ka, kb, ja, jb = kb, ka, jb, ja
        offset = jb if ka == 0 else (jb - ja) % N
        rows[(ka, kb)][offset] += 1
    return [[list(key), [[offset, count] for offset, count in sorted(counts.items())]]
            for key, counts in sorted(rows.items())]


def decode_coordinates(rows):
    require(type(rows) is list and len(rows) == 211, "coordinate rows")
    answer = []
    for row in rows:
        require(type(row) is list and len(row) == 8, "coordinate degree")
        decoded = []
        for pair in row:
            require(type(pair) is list and len(pair) == 2
                    and all(type(x) is int for x in pair) and pair[1] > 0,
                    "coordinate rational")
            numerator, denominator = pair
            require(gcd(abs(numerator), denominator) == 1, "unreduced rational")
            decoded.append(Fraction(numerator, denominator))
        answer.append(tuple(decoded))
    return answer


def verify(certificate, expected):
    require(type(certificate) is dict and set(certificate) == {
        "version", "source", "coordinates", "three_colour_word", "terminal_rows"
    }, "certificate fields")
    require(certificate["version"] == 1
            and certificate["source"] == "reciprocal_chord_cage_30",
            "certificate identity")
    coordinates = decode_coordinates(certificate["coordinates"])
    addresses, edges, terminals = geometry()
    for address, coordinate in zip(addresses, coordinates):
        numerator, denominator = address_fraction(address)
        coordinate_poly = tuple(coordinate) + (Fraction(0),) * (N - len(coordinate))
        require(is_zero(add(multiply(coordinate_poly, denominator), numerator, -1)),
                "coordinate/address mismatch")
    adj = adjacency(len(addresses), edges)
    degree_histogram = [list(row) for row in sorted(Counter(map(len, adj)).items())]
    terminal_edges = [(a, b) for a, b in combinations(range(8), 2)
                      if terminals[b] in adj[terminals[a]]]
    require(terminal_edges == [(0, 1), (2, 3), (4, 5), (6, 7)],
            "terminal graph")
    check_word(certificate["three_colour_word"], 3, adj)
    triangle = [0, 91, 96]
    require(all(triangle[(j + 1) % 3] in adj[triangle[j]] for j in range(3)),
            "three-colour lower witness")
    required_patterns = canonical_patterns(terminal_edges)
    rows = certificate["terminal_rows"]
    require(type(rows) is list and all(type(row) is dict
            and set(row) == {"pattern", "word"} for row in rows),
            "terminal row shape")
    require([row["pattern"] for row in rows] == required_patterns,
            "complete canonical terminal-pattern census")
    for row in rows:
        pattern = row["pattern"]
        require(len(pattern) == 8 and set(pattern) <= set("0123"), "pattern shape")
        check_word(row["word"], 4, adj,
                   list(zip(terminals, map(int, pattern))))
    report = {
        "vertices": len(addresses),
        "edges": len(edges),
        "degree_histogram": degree_histogram,
        "terminal_indices": list(terminals),
        "terminal_edges": [list(edge) for edge in terminal_edges],
        "canonical_bare_patterns": len(required_patterns),
        "canonical_extending_patterns": len(rows),
        "canonical_forbidden_patterns": len(required_patterns) - len(rows),
        "named_bare_patterns": 12 ** 4,
        "named_extending_patterns": 12 ** 4,
        "chromatic_number": 3,
        "coordinate_sha256": digest(certificate["coordinates"]),
        "address_sha256": digest(addresses),
        "edge_sha256": digest(edges),
        "incidence_sha256": digest(incidence(addresses, edges)),
        "pattern_sha256": digest(required_patterns),
        "witness_sha256": digest(rows),
        "three_colour_sha256": hashlib.sha256(
            certificate["three_colour_word"].encode()).hexdigest(),
    }
    require(report == expected, "expected report mismatch")
    return report


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--certificate", type=Path,
                        default=HERE / "certificate.json")
    parser.add_argument("--expected", type=Path, default=HERE / "expected.json")
    args = parser.parse_args()
    certificate = json.loads(args.certificate.read_text())
    expected = json.loads(args.expected.read_text())
    print(dump(verify(certificate, expected)), end="")


if __name__ == "__main__":
    main()
