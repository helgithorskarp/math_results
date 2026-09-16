#!/usr/bin/env python3
"""Small controls for the candidate verifier and exhaustive colour checker."""
import argparse
import json
from pathlib import Path

import verify


def rejected(call):
    try:
        call()
    except ValueError:
        return True
    return False


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, type=Path)
    args = parser.parse_args()
    result = verify.verify(args.input)
    expected = json.loads((verify.HERE / "expected.json").read_text())
    verify.need(result == expected, "expected mismatch")

    triangle = [(0, 1), (0, 2), (1, 2)]
    k4 = triangle + [(0, 3), (1, 3), (2, 3)]
    tri_word, tri_nodes, _ = verify.three_colour_search(range(3), triangle)
    k4_word, k4_nodes, _ = verify.three_colour_search(range(4), k4)
    verify.need(tri_word is not None and k4_word is None, "small colour control")
    verify.need(rejected(lambda: verify.check_word("00", [(0, 1)], "0123")), "bad word accepted")
    verify.need(rejected(lambda: verify.check_word("04", [], "0123")), "bad alphabet accepted")
    print(
        json.dumps(
            {
                "verified": True,
                "expected_replay": True,
                "triangle_three_colourable": True,
                "triangle_search_nodes": tri_nodes,
                "k4_three_colourable": False,
                "k4_search_nodes": k4_nodes,
                "malformed_words_rejected": 2
            },
            indent=2,
            sort_keys=True,
        )
    )
