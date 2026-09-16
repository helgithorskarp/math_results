#!/usr/bin/env python3
"""Negative controls: the verifier must reject three semantic corruptions."""

import copy
import json
from pathlib import Path

from verify import verify_certificate


ROOT = Path(__file__).resolve().parent


def rejected(data, expected):
    try:
        verify_certificate(data, expected)
    except (AssertionError, KeyError, IndexError, TypeError, ValueError):
        return True
    return False


def main():
    original = json.loads((ROOT/"certificate.json").read_text())
    expected = json.loads((ROOT/"EXPECTED.json").read_text())

    bad_color = copy.deepcopy(original)
    u, v = bad_color["unit_edges"][0]
    bad_color["four_word"][v] = bad_color["four_word"][u]

    missing_edge = copy.deepcopy(original)
    missing_edge["unit_edges"].pop()

    moved_point = copy.deepcopy(original)
    moved_point["points"][0][0][0] = "1/97"

    outcomes = {
        "bad_coloring_rejected": rejected(bad_color, expected),
        "missing_edge_rejected": rejected(missing_edge, expected),
        "moved_point_rejected": rejected(moved_point, expected),
    }
    if not all(outcomes.values()):
        raise SystemExit("a semantic corruption was accepted")
    print(json.dumps(outcomes, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
