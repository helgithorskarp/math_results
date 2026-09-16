#!/usr/bin/env python3
"""Boundary and mutation controls for the equality-pair gate."""

import copy
import json
from pathlib import Path

import verify


HERE = Path(__file__).resolve().parent


def rejected(cert):
    try:
        verify.verify(cert)
    except (AssertionError, KeyError, TypeError, ValueError):
        return True
    return False


cert = json.loads((HERE / "certificate.json").read_text())
base = verify.verify(cert)

mutations = 0
for k in range(8):
    bad = copy.deepcopy(cert)
    del bad["words"][k]
    assert rejected(bad)
    mutations += 1

bad = copy.deepcopy(cert)
bad["source_ids"][20] = bad["source_ids"][19]
assert rejected(bad)
mutations += 1

bad = copy.deepcopy(cert)
word = list(bad["words"][0])
word[1] = word[0]
bad["words"][0] = "".join(word)
assert rejected(bad)
mutations += 1

bad = copy.deepcopy(cert)
bad["words"][0] = "4" + bad["words"][0][1:]
assert rejected(bad)
mutations += 1

assert verify.sign_quadratic(1, 0) == 1
assert verify.sign_quadratic(-1, 0) == -1
assert verify.sign_quadratic(0, 1) == 1
assert verify.sign_quadratic(0, -1) == -1
assert verify.sign_quadratic(6, -1) == 1
assert verify.sign_quadratic(5, -1) == -1
assert verify.sign_quadratic(-6, 1) == -1
assert verify.sign_quadratic(-5, 1) == 1

print(json.dumps({
    "status": "CONTROLS_OK",
    "valid_status": base["status"],
    "rejected_mutations": mutations,
    "sign_controls": 8,
}, indent=2, sort_keys=True))
