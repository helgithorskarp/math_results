#!/usr/bin/env python3
"""Positive and negative controls for the Pegg12 triple-sum certificate."""

from __future__ import annotations

import copy
import json
from pathlib import Path

from model import ONE, R3, R11, R33
from verify import VerificationError, compute, require, validate_certificate


HERE = Path(__file__).resolve().parent


def must_reject(certificate, context):
    try:
        validate_certificate(certificate, context)
    except (VerificationError, AssertionError, ValueError):
        return
    raise AssertionError("corrupted certificate was accepted")


def main():
    require(R3 * R3 == 3 * ONE, "sqrt(3) control failed")
    require(R11 * R11 == 11 * ONE, "sqrt(11) control failed")
    require(R33 == R3 * R11, "sqrt(33) control failed")

    expected = json.loads((HERE / "expected.json").read_text())
    certificate = json.loads((HERE / "certificate.json").read_text())
    actual, context = compute()
    require(actual == expected, "expected output control failed")
    validate_certificate(certificate, context)

    bad = copy.deepcopy(certificate)
    bad["schema"] = "wrong"
    must_reject(bad, context)

    bad = copy.deepcopy(certificate)
    bad["first_surviving_source_word"] = "0" * 12
    must_reject(bad, context)

    bad = copy.deepcopy(certificate)
    bad["four_color_word"] = bad["four_color_word"][:-1]
    must_reject(bad, context)

    bad = copy.deepcopy(certificate)
    word = list(bad["four_color_word"])
    word[0] = word[1]
    bad["four_color_word"] = "".join(word)
    must_reject(bad, context)
    print("CONTROLS_PASS")


if __name__ == "__main__":
    main()
