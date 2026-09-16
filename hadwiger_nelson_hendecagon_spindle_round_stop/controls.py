#!/usr/bin/env python3
"""Negative controls for the exact field model and literal witnesses."""

import copy
import json
from pathlib import Path

from model import ONE, PHI66, Q, check_word, construction, qpower
from verify import VerificationError, compute, validate_certificate


HERE = Path(__file__).resolve().parent


def reject(certificate, context):
    try:
        validate_certificate(certificate, context)
    except (VerificationError, ValueError):
        return
    raise RuntimeError("corrupted certificate was accepted")


def main():
    # Field/order and conjugation controls.
    assert qpower(66) == ONE
    assert sum(PHI66[k] * qpower(k) for k in range(21)) == 0
    assert Q * Q.conjugate() == ONE

    _, context = compute()
    certificate = json.loads((HERE / "certificate.json").read_text())

    bad = copy.deepcopy(certificate)
    bad["schema"] = "wrong"
    reject(bad, context)

    bad = copy.deepcopy(certificate)
    bad["source_extensions"][0]["source_word"] = "0101222"
    reject(bad, context)

    bad = copy.deepcopy(certificate)
    word = list(bad["source_extensions"][0]["extension"])
    word[0] = word[1]
    bad["source_extensions"][0]["extension"] = "".join(word)
    reject(bad, context)

    points, edges, _, _ = construction()
    word = certificate["source_extensions"][0]["extension"][:-1]
    try:
        check_word(word, len(points), edges)
    except ValueError:
        pass
    else:
        raise RuntimeError("short colouring was accepted")
    print("CONTROLS_OK")


if __name__ == "__main__":
    main()

