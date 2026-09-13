#!/usr/bin/env python3
"""Semantic rejection controls for the independent dominating-triple audit."""

from __future__ import annotations

import copy
import json
from pathlib import Path

import independent_audit as audit


HERE = Path(__file__).resolve().parent


def reject(label, phrase, action):
    try:
        action()
    except ValueError as error:
        audit.need(phrase in str(error), f"{label} reached wrong check: {error}")
        return label
    raise ValueError(f"invalid control passed: {label}")


def main():
    base = json.loads((audit.TARGET / "certificate.json").read_text())
    rejected = []

    bad = copy.deepcopy(base)
    bad["pair_order_4"][0] = [0, 2]
    rejected.append(reject(
        "corrupt four-point pair order",
        "four-point pair order",
        lambda: audit.audit_certificate(bad),
    ))

    bad = copy.deepcopy(base)
    bad["distinct_parity_conflict_graphs_4"] += 1
    rejected.append(reject(
        "corrupt conflict-graph count",
        "conflict graph census",
        lambda: audit.audit_certificate(bad),
    ))

    bad = copy.deepcopy(base)
    bad["unsat_no_triple"].pop()
    rejected.append(reject(
        "omit four-point exception",
        "four-point abstract exceptions",
        lambda: audit.audit_certificate(bad),
    ))

    bad = copy.deepcopy(base)
    bad["unsat_one_triple"][0]["a_mask"] ^= 1
    rejected.append(reject(
        "corrupt triple exception",
        "triple abstract exceptions",
        lambda: audit.audit_certificate(bad),
    ))

    rejected.append(reject(
        "monochromatic two-centre patch",
        "two-centre patch colouring",
        lambda: audit.audit_two_centre_patch(colors=(0,) * 12),
    ))

    result = {"verified": True, "rejected": rejected}
    audit.need(result == json.loads((HERE / "EXPECTED_CONTROLS.json").read_text()),
               "expected control output")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
