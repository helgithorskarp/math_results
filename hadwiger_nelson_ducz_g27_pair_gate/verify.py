#!/usr/bin/env python3
"""Definition-level checker for the G_27 chromatic and pair gate."""

from itertools import combinations
import argparse
import json
from pathlib import Path

from geometry import EDGES, ONE, POINTS, W1, W3, W13, add, edge_sha256, multiply


WORDS = (
    "000201201202100210212020122",
    "100201201202100210212020122",
    "001201201202100210212020122",
    "010201201202100210212020122",
    "000301201202100210212020122",
    "000201221202100210212020122",
    "000201201212100210212020122",
    "011001201000121220001202100",
    "000201201202100213212020122",
    "000102101202100210212020122",
    "000201201202300210212020122",
    "000201201202100210212010311",
    "000201201203100210212020122",
    "000201201202100210312020122",
    "000201201202100210202320122",
    "000201201202101220021003102",
    "000201201202100210212030122",
)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def proper(word: str) -> bool:
    return len(word) == 27 and set(word) <= set("0123") and all(
        word[a] != word[b] for a, b in EDGES)


def check_words(words: tuple[str, ...]) -> None:
    require(len(words) == 17, "word count")
    require(all(proper(w) for w in words), "improper saved word")
    require(set(words[0]) == set("012"), "first word is not a proper three-colouring")
    signatures = [tuple(w[v] for w in words) for v in range(27)]
    require(len(set(signatures)) == 27, "colour signatures do not separate all points")


def result() -> dict:
    require(len(POINTS) == len(set(POINTS)) == 27, "coordinate collision")
    # Independent sanity check for the manually expanded omega_1*omega_3.
    complex_product = (
        add(multiply(W1[0], W3[0]), tuple(-x for x in multiply(W1[1], W3[1]))),
        add(multiply(W1[0], W3[1]), multiply(W1[1], W3[0])),
    )
    require(complex_product == W13, "basis product")
    require(len(EDGES) == 49, "complete edge count")
    require(edge_sha256() == "e23da734060870131917024d0e2b397ac2353e495d235aa8470704183f6d4dde",
            "edge stream hash")
    check_words(WORDS)
    edge_set = set(EDGES)
    require({(3, 5), (3, 13), (5, 13)} <= edge_set, "triangle witness")
    degrees = [0] * 27
    for a, b in EDGES:
        degrees[a] += 1
        degrees[b] += 1
    require(sum(degrees) == 98, "handshake")
    return {
        "verified": True,
        "vertices": 27,
        "complete_unit_edges": 49,
        "chromatic_number": 3,
        "triangle_witness_zero_based": [3, 5, 13],
        "proper_three_colouring": WORDS[0],
        "proper_four_colour_separating_words": len(WORDS),
        "all_distinct_pairs_separated": True,
        "forced_equal_pairs": 0,
        "edge_stream_sha256": edge_sha256(),
        "degree_sequence": sorted(degrees),
    }


def controls() -> None:
    bad = list(WORDS)
    a, b = EDGES[0]
    w = list(bad[0])
    w[b] = w[a]
    bad[0] = "".join(w)
    rejected = False
    try:
        check_words(tuple(bad))
    except ValueError:
        rejected = True
    require(rejected, "corrupt edge word was accepted")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check-expected", action="store_true")
    parser.add_argument("--controls", action="store_true")
    args = parser.parse_args()
    out = result()
    if args.controls:
        controls()
        out["controls"] = "passed"
    text = json.dumps(out, sort_keys=True, separators=(",", ":"))
    if args.check_expected:
        expected = (Path(__file__).with_name("EXPECTED.json").read_text().strip())
        require(text == expected, "EXPECTED.json mismatch")
    print(text)


if __name__ == "__main__":
    main()
