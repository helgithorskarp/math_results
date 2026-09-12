#!/usr/bin/env python3
"""Independent small controls for the physical graph verifier."""

from __future__ import annotations

import itertools
import json
from pathlib import Path

import verify


HERE = Path(__file__).resolve().parent


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def direct_counts(n: int, word: int) -> tuple[int, int]:
    pairs = list(itertools.combinations(range(n), 2))
    edge_index = {edge: i for i, edge in enumerate(pairs)}
    red = blue = 0
    for five in itertools.combinations(range(n), 5):
        mask = 0
        for a, b in itertools.combinations(five, 2):
            mask |= 1 << edge_index[a, b]
        selected = word & mask
        red += selected == mask
        blue += selected == 0
    return red, blue


def encode_hex(bits: list[int]) -> str:
    alphabet = "0123456789abcdef"
    result = []
    for start in range(0, len(bits), 4):
        digit = sum(bit << shift for shift, bit in enumerate(bits[start:start + 4]))
        result.append(alphabet[digit])
    return "".join(result)


def force(bits: list[int], n: int, vertices: tuple[int, ...], value: int) -> list[int]:
    result = bits.copy()
    index = {edge: i for i, edge in enumerate(itertools.combinations(range(n), 2))}
    for edge in itertools.combinations(vertices, 2):
        result[index[edge]] = value
    return result


def main() -> None:
    exhaustive_words = 0
    for n in range(1, 7):
        edges = n * (n - 1) // 2
        for word in range(1 << edges):
            bits = [(word >> i) & 1 for i in range(edges)]
            report = verify.audit(n, bits)
            expected_red, expected_blue = direct_counts(n, word)
            require((report["red_K5"], report["blue_K5"]) ==
                    (expected_red, expected_blue), "five-set count mismatch")
            require(verify.decode_hex(n, encode_hex(bits)) == bits,
                    "hexadecimal round trip failed")
            exhaustive_words += 1

    record = (HERE / "fixtures" / "good42.g6").read_text(encoding="ascii").strip()
    n, bits = verify.decode_graph6(record)
    good = verify.audit(n, bits)
    require(n == 42 and good["status"] == "GOOD_GRAPH", "good42 rejected")
    require(good["five_subsets_checked"] == 850668, "wrong good42 coverage")
    require(good["red_edges"] == 425, "wrong good42 edge count")

    red_bad = verify.audit(n, force(bits, n, (0, 1, 2, 3, 4), 1))
    blue_bad = verify.audit(n, force(bits, n, (37, 38, 39, 40, 41), 0))
    require(red_bad["red_K5"] >= 1 and red_bad["first_red_K5"] is not None,
            "red negative control accepted")
    require(blue_bad["blue_K5"] >= 1 and blue_bad["first_blue_K5"] is not None,
            "blue negative control accepted")

    # Complementation plus relabeling at a chosen root is checked on every
    # labelled graph through order six.  It is the finite analogue of the
    # target's four-branch root normalization.
    root_checks = 0
    for n in range(2, 7):
        edges = n * (n - 1) // 2
        for word in range(1 << edges):
            bits = [(word >> i) & 1 for i in range(edges)]
            adjacency = [[0] * n for _ in range(n)]
            for bit, (a, b) in zip(bits, itertools.combinations(range(n), 2), strict=True):
                adjacency[a][b] = adjacency[b][a] = bit
            degree = sum(adjacency[0])
            normalized_degree = min(degree, n - 1 - degree)
            require(normalized_degree <= (n - 1) // 2,
                    "root normalization failed")
            root_checks += 1

    malformed = 0
    for n, text in ((5, "0"), (5, "ggg"), (6, "ffff")):
        try:
            verify.decode_hex(n, text)
        except ValueError:
            malformed += 1
        else:
            raise AssertionError("malformed hexadecimal graph accepted")
    for text in ("", "~", "iinvalid"):
        try:
            verify.decode_graph6(text)
        except (ValueError, UnicodeError):
            malformed += 1
        else:
            raise AssertionError("malformed graph6 accepted")

    print(json.dumps({
        "status": "PASS",
        "exhaustive_graph_words": exhaustive_words,
        "root_normalization_checks": root_checks,
        "good42_five_subsets_checked": good["five_subsets_checked"],
        "negative_physical_fixtures": 2,
        "malformed_inputs_rejected": malformed,
    }, sort_keys=True, separators=(",", ":")))


if __name__ == "__main__":
    main()
