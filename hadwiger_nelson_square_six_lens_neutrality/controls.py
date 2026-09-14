#!/usr/bin/env python3
"""Mutation controls for verify.py."""

from __future__ import annotations

import copy
import json
from pathlib import Path

from verify import verify_certificate


def rejected(cert: dict, mutate) -> None:
    bad = copy.deepcopy(cert)
    mutate(bad)
    try:
        verify_certificate(bad)
    except (KeyError, TypeError, ValueError):
        return
    raise AssertionError("corruption was accepted")


def main() -> None:
    cert = json.loads(Path(__file__).with_name("certificate.json").read_text())
    rejected(cert, lambda x: x.__setitem__("format", "wrong"))
    rejected(cert, lambda x: x["points"][0]["x"].__setitem__(0, "1"))
    rejected(cert, lambda x: x["edges"].pop())
    rejected(cert, lambda x: x["edges"].append([0, 1]))
    rejected(cert, lambda x: x["chromatic"].__setitem__("three_colouring", "0" * 16))
    rejected(cert, lambda x: x["relation"]["canonical_extendible_patterns"].pop())
    rejected(cert, lambda x: x["relation"]["canonical_witnesses"].__setitem__("0000", "0" * 16))
    print("REJECTED_7_SQUARE_SIX_LENS_CORRUPTIONS")


if __name__ == "__main__":
    main()
