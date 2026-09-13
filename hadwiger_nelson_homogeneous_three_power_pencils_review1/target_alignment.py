#!/usr/bin/env python3
"""Bridge the clean-room objects to the reviewed package entry by entry."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
from itertools import combinations, product
from pathlib import Path

import independent_audit as audit


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
TARGET = ROOT / "hadwiger_nelson_homogeneous_three_power_pencils"


def load_target_exact():
    specification = importlib.util.spec_from_file_location(
        "reviewed_three_power_exact", TARGET / "exact.py"
    )
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


def run(residual_path):
    target_exact = load_target_exact()
    equation_checks = 0
    norm_checks = 0
    for signs in product((-1, 1), repeat=5):
        independent_equations, independent_norms = audit.equations(signs)
        target_equations, target_norms = target_exact.equations(signs)
        audit.need(independent_equations == target_equations, "target defining equations")
        audit.need(independent_norms == tuple(target_norms), "target radius polynomials")
        equation_checks += len(independent_equations)
        norm_checks += len(independent_norms)

    normalization = audit.finite_normalization_audit()
    pencils = normalization.pop("pencils")
    all_a5 = []
    for support in combinations(range(4), 3):
        for pencil in pencils:
            embedded = []
            for normal in pencil:
                vector = [0] * 4
                for position, value in zip(support, normal):
                    vector[position] = value
                embedded.append([vector, 0])
            all_a5.append(sorted(embedded))
    all_a5.sort()
    residual = json.loads(Path(residual_path).read_text())
    selected = []
    for index, pencil in enumerate(residual["remaining_pencil_signatures"]):
        support = {
            j
            for normal, constant in pencil
            for j, value in enumerate(normal)
            if value
        }
        if all(constant == 0 for normal, constant in pencil) and len(support) == 3:
            selected.append([index, pencil])

    target_interface_path = TARGET / "A5_INTERFACE.json"
    target_interface = json.loads(target_interface_path.read_text())
    audit.need(all_a5 == target_interface["all_a5_pencils"], "target full A5 interface")
    audit.need(
        selected == target_interface["remaining_h4195_index_pencil"],
        "target residual interface",
    )
    certificate_path = TARGET / "certificate.json"
    return {
        "status": "PASS",
        "sign_cases": 32,
        "defining_polynomials_compared": equation_checks,
        "radius_polynomials_compared": norm_checks,
        "a5_pencils_compared_entrywise": len(all_a5),
        "residual_pencils_compared_entrywise": len(selected),
        "target_certificate_sha256": hashlib.sha256(certificate_path.read_bytes()).hexdigest(),
        "target_interface_sha256": hashlib.sha256(target_interface_path.read_bytes()).hexdigest(),
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--residual", type=Path, required=True)
    parser.add_argument("--check-expected", action="store_true")
    arguments = parser.parse_args()
    result = run(arguments.residual)
    if arguments.check_expected:
        expected = json.loads(HERE.joinpath("EXPECTED_ALIGNMENT.json").read_text())
        audit.need(result == expected, "alignment output mismatch")
    print(json.dumps(result, indent=2, sort_keys=True))
