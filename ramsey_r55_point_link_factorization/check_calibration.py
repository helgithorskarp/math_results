#!/usr/bin/env python3
"""Definition-check the positive point-link good42 calibration."""

from __future__ import annotations

import json
from pathlib import Path

import factorization


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def main() -> None:
    text = Path(__file__).with_name("calibration_good42.hex").read_text(
        encoding="ascii").strip()
    report = factorization.audit(42, factorization.decode_hex(42, text), 0)
    require(report["factorization_identity"], "factorization identity failed")
    require(report["status"] == "GOOD_GRAPH", "calibration graph is not good42")
    require(report["root_degree"] == 19, "wrong root degree")
    require(min(report["degrees"]) == 19 and max(report["degrees"]) == 22,
            "wrong degree range")
    require(report["red_edges"] == 427, "wrong edge count")
    require(report["active_cross_clauses"] == 59934, "wrong cross clause count")
    print(json.dumps({
        "status": "VERIFIED_GOOD42_POINT_LINK_CALIBRATION",
        "five_subsets_checked": 850668,
        "red_edges": report["red_edges"],
        "active_cross_clauses": report["active_cross_clauses"],
        "red_K5": report["direct_red_K5"],
        "blue_K5": report["direct_blue_K5"],
    }, sort_keys=True, separators=(",", ":")))


if __name__ == "__main__":
    main()
