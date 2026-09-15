#!/usr/bin/env python3
"""Fast semantic corruption controls for the triangle-gluing checker."""
from __future__ import annotations

import copy
import json
from pathlib import Path

import verify

HERE = Path(__file__).resolve().parent


def rejected(certificate, label):
    try:
        verify.verify(certificate)
    except (ValueError, TypeError):
        return
    raise RuntimeError(f"control accepted: {label}")


def main():
    source = json.loads((HERE / "certificate.json").read_text())

    damaged = copy.deepcopy(source)
    damaged["family"] = "wrong family"
    rejected(damaged, "family")

    damaged = copy.deepcopy(source)
    damaged["rows"].pop()
    rejected(damaged, "missing placement")

    damaged = copy.deepcopy(source)
    damaged["permutation_order"][0] = [0, 2, 1]
    rejected(damaged, "permutation order")

    damaged = copy.deepcopy(source)
    damaged["rows"][0][3] = "!"
    rejected(damaged, "malformed colour word")

    print(json.dumps({"verified": True, "rejected_corruptions": 4}, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
