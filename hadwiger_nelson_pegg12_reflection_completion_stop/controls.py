#!/usr/bin/env python3
"""Small negative and algebra controls for the reflection verifier."""

from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path

from model import K, ONE, R3, R11, R33, check_word, inverse, reflected_union


HERE = Path(__file__).resolve().parent


def rejected(fn):
    try:
        fn()
    except (AssertionError, ValueError):
        return True
    return False


def main():
    samples = [ONE, 2 + R3, R11 - R3, 1 + 2 * R3 - R11 + R33]
    assert all(x * inverse(x) == ONE for x in samples)
    # The multiplication basis must encode both quadratic relations.
    assert R3 * R3 == K.rational(3)
    assert R11 * R11 == K.rational(11)
    assert R3 * R11 == R33

    cert = json.loads((HERE / "certificate.json").read_text())
    axes = tuple(map(tuple, cert["full_axes"]))
    points, edges, _, _ = reflected_union(axes)
    good = cert["full_four_word"]
    assert check_word(good, len(points), edges)

    bad_symbol = good[:10] + "4" + good[11:]
    assert rejected(lambda: check_word(bad_symbol, len(points), edges))
    a, b = edges[0]
    altered = list(good)
    altered[b] = altered[a]
    assert rejected(lambda: check_word("".join(altered), len(points), edges))
    assert rejected(lambda: check_word(good[:-1], len(points), edges))
    print("VERIFIED_PEGG12_REFLECTION_CONTROLS")


if __name__ == "__main__":
    main()
