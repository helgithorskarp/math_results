#!/usr/bin/env python3
"""Recompute the exact target specification."""

from __future__ import annotations

import json
from pathlib import Path

import factorization


def main() -> None:
    expected = json.loads(Path(__file__).with_name("expected_target.json").read_text(
        encoding="utf-8"))
    actual = factorization.target_spec()
    if actual != expected:
        print(json.dumps(actual, indent=2, sort_keys=True))
        raise SystemExit("target specification differs")
    print("TARGET_SPEC status=PASS branches=3 physical_edges=903 free_variables=861 "
          "inner_cross_variables=432,437,440")


if __name__ == "__main__":
    main()
