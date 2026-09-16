#!/usr/bin/env python3
"""Negative controls for the exact O'Donnell-core verifier."""

import copy
import json

import verify


BASE = copy.deepcopy(verify.CERT)


def rejected(name, mutate):
    trial = copy.deepcopy(BASE)
    mutate(trial)
    verify.CERT = trial
    try:
        verify.verify()
    except ValueError:
        return name
    raise AssertionError(f"negative control accepted: {name}")


checks = []
checks.append(rejected("monochromatic three-word",
                       lambda c: c.__setitem__("three_colouring", [0] * 171)))
checks.append(rejected("deleted physical unit edge",
                       lambda c: c["edges"].pop()))


def corrupt_coordinate(c):
    c["physical_coordinates"][0][0][0] = "1/7"


checks.append(rejected("corrupted physical coordinate", corrupt_coordinate))
checks.append(rejected("false chromatic label",
                       lambda c: c.__setitem__("chromatic_number", 4)))
verify.CERT = BASE
print(json.dumps({"negative_controls_rejected": checks}, indent=2, sort_keys=True))
