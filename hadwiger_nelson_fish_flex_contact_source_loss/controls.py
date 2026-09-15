#!/usr/bin/env python3
"""Negative controls: corrupt mathematical data and require rejection."""

from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path
from tempfile import TemporaryDirectory

from verify import verify


HERE = Path(__file__).resolve().parent


def rejected(call):
    try:
        call()
    except (KeyError, TypeError, ValueError):
        return
    raise RuntimeError("corrupted certificate was accepted")


def main():
    original = json.loads((HERE/"geometry_certificate.json").read_text())
    changes = []

    def add(name, mutate):
        value = deepcopy(original)
        mutate(value)
        changes.append((name, value))

    add("zero inverse", lambda c: c.__setitem__(
        "inverse_numerators", [[0]*42 for _ in range(42)]))
    add("move midpoint", lambda c: c["midpoint_numerators"][3].__setitem__(
        0, c["midpoint_numerators"][3][0]+c["midpoint_denominator"]))
    add("delete source edge", lambda c: c["source_edges"].pop())
    add("macroscopic radius", lambda c: c.__setitem__("radius_denominator", 1))
    add("wrong target", lambda c: c.__setitem__("target_contact", [9, 16]))
    add("improper blocked word", lambda c: c.__setitem__(
        "source_blocked_word", "0"*23))
    add("unblocked word", lambda c: c.__setitem__(
        "source_blocked_word", c["surviving_complete_word"]))
    add("improper survivor", lambda c: c.__setitem__(
        "surviving_complete_word", "0"*23))

    with TemporaryDirectory() as temporary:
        path = Path(temporary)/"corrupt.json"
        for _, value in changes:
            path.write_text(json.dumps(value))
            rejected(lambda: verify(path))
    print(json.dumps({"status": "CONTROLS PASS",
                      "mathematical_corruptions_rejected": len(changes),
                      "hash_rejection_used": False}, sort_keys=True))


if __name__ == "__main__":
    main()
