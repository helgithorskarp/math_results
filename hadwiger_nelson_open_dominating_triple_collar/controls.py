#!/usr/bin/env python3
"""Mutation controls: every named semantic corruption must be rejected."""

from __future__ import annotations

import copy
import json
from pathlib import Path

from verify import CheckError, verify_certificate


def main() -> None:
    source = Path(__file__).with_name("certificate.json")
    base = json.loads(source.read_text())
    mutations = []

    def add(name, mutate):
        value = copy.deepcopy(base)
        mutate(value)
        mutations.append((name, value))

    add("wrong_threshold_polynomial", lambda d: d["threshold"].__setitem__("squared_minimal_polynomial", [1, -8, 9]))
    add("wrong_orbit_chord", lambda d: d["circle_orbit"]["squared_chords"].__setitem__(1, 2))
    add("wrong_fixture_coordinate", lambda d: d["open_fixture"]["centres"][2]["y"].__setitem__(3, 2))
    add("wrong_fixture_norm", lambda d: d["open_fixture"]["pair_squared_distances"].__setitem__(0, 7))
    add("wide_cap", lambda d: d["cap_fixture"].__setitem__("cap_diameter_squared_upper_bound", [1, 1]))
    add("overlapping_palettes", lambda d: d["palette"].__setitem__("third_circle_colours", [1, 3]))

    rejected = []
    for name, value in mutations:
        try:
            verify_certificate(value)
        except (CheckError, KeyError, TypeError, ValueError, ZeroDivisionError):
            rejected.append(name)
        else:
            raise SystemExit(f"mutation accepted: {name}")
    result = {"malformed_certificate_rejections": len(rejected), "rejected": rejected, "status": "PASS"}
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
