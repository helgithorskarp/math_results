#!/usr/bin/env python3
"""Mutation controls for the exact lens-orbit certificate."""

from __future__ import annotations

import copy
import json
from pathlib import Path

from verify import verify_certificate


HERE = Path(__file__).resolve().parent


def rejected(data: dict[str, object]) -> bool:
    try:
        verify_certificate(data)
    except (KeyError, TypeError, ValueError):
        return True
    return False


def main() -> None:
    base = json.loads((HERE / "certificate.json").read_text(encoding="utf-8"))
    mutations = []

    data = copy.deepcopy(base)
    data["centres"][2][1] = 4
    mutations.append(data)

    data = copy.deepcopy(base)
    data["lenses"][0]["intersections"][0][0] = 0
    mutations.append(data)

    data = copy.deepcopy(base)
    data["points"].pop()
    mutations.append(data)

    data = copy.deepcopy(base)
    data["edges"].pop()
    mutations.append(data)

    data = copy.deepcopy(base)
    data["three_colouring"] = "0" + data["three_colouring"][1:]
    mutations.append(data)

    data = copy.deepcopy(base)
    data["centre_relation_witnesses"].pop("012")
    mutations.append(data)

    data = copy.deepcopy(base)
    data["centre_relation_witnesses"]["000"] = "0" * len(data["points"])
    mutations.append(data)

    data = copy.deepcopy(base)
    data["hashes"]["edges"] = "0" * 64
    mutations.append(data)

    if not all(rejected(data) for data in mutations):
        raise SystemExit("a malformed certificate was accepted")
    print(json.dumps({"controls_rejected": len(mutations), "verified": True}, sort_keys=True))


if __name__ == "__main__":
    main()
