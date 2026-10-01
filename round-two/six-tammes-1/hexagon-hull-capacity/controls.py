#!/usr/bin/env python3
"""Adverse controls for finite obligations and their scalar bridges.

Rejection of a proposed wider parameter here means this certificate fails;
it does not prove that the wider geometric statement is false.
"""
from copy import deepcopy
from pathlib import Path
import json
import check

BASE = Path(__file__).resolve().parent


def main():
    original = json.loads((BASE/"certificate.json").read_text())
    data = (BASE/"coordinates.txt").read_bytes()
    cases = []
    for name, key, value in [
        ("larger_displacement_requires_a_new_certificate", "epsilon", "1/20"),
        ("false_smaller_vertex_norm_bound", "vertex_norm_squared_bound", "4/5"),
        ("invalid_cap_normalization_bridge", "unit_cap_cosine_lower", "9/10"),
        ("invalid_pair_separation_bridge", "packing_cosine_max", "7/10")]:
        cert = deepcopy(original)
        cert[key] = value
        cases.append((name, cert, data))
    cert = deepcopy(original)
    cert["patterns"][0]["support_pairs"][0] = [0, 4]
    cases.append(("non_supporting_diagonal", cert, data))
    cases.append(("corrupted_coordinate_input", deepcopy(original), data+b"0\n"))
    results = []
    for name, cert, candidate_data in cases:
        try:
            check.verify(cert, candidate_data)
        except ValueError as exc:
            results.append({"control": name, "result": "rejected",
                            "reason": str(exc)})
        else:
            raise ValueError("adverse control was accepted: "+name)
    output = {"status": "six_adverse_certificate_controls_rejected",
              "controls": results}
    path = BASE/"CONTROLS_EXPECTED.json"
    if path.exists() and output != json.loads(path.read_text()):
        raise ValueError("control expected-output mismatch")
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
