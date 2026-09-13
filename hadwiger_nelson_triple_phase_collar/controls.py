#!/usr/bin/env python3
"""Mutation controls: every named corruption must be rejected."""

from __future__ import annotations

import copy
import json
from pathlib import Path

from verify import CheckError, verify_certificate


def main() -> None:
    base = json.loads(Path(__file__).with_name("certificate.json").read_text())
    mutations = []

    def add(name, mutate):
        value = copy.deepcopy(base)
        mutate(value)
        mutations.append((name, value))

    add("wrong_threshold", lambda d: d["threshold"].__setitem__("distance", [2, 1, 0, 0, 1]))
    add("wrong_gap_factor", lambda d: d["monotonicity"]["cosine_gap_factorization"].__setitem__("scalar", 2))
    add("wrong_orbit_chord", lambda d: d["circle_orbit"]["squared_chords"].__setitem__(1, 2))
    add("wrong_fixture_coordinate", lambda d: d["interior_fixture"]["centres"][2].__setitem__("y", [0, 5, 0, 0, 4]))
    add("nonunit_cross_direction", lambda d: d["cross_triple_fixture"]["directions"][0].__setitem__("x", [3, 0, 0, 0, 4]))
    add("wrong_cross_product", lambda d: d["cross_triple_fixture"].__setitem__("product", {"x": [0, 0, 0, 0, 1], "y": [0, 0, 0, 0, 1]}))
    add("broken_sharp_triangle", lambda d: d["sharp_triangle"]["points"][2].__setitem__("x", [1, 1, 0, 0, 1]))
    add("overlapping_palettes", lambda d: d["palette"].__setitem__("third_circle_colours", [1, 3]))

    rejected = []
    for name, value in mutations:
        try:
            verify_certificate(value)
        except (CheckError, KeyError, TypeError, ValueError, ZeroDivisionError):
            rejected.append(name)
        else:
            raise SystemExit(f"mutation accepted: {name}")
    print(json.dumps({"malformed_certificate_rejections": len(rejected), "rejected": rejected, "status": "PASS"}, sort_keys=True))


if __name__ == "__main__":
    main()
