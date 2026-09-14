#!/usr/bin/env python3
"""Negative controls for the three-diamond verifier."""

from __future__ import annotations

import copy
import importlib.util
import json
import sys
from pathlib import Path


HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("three_diamond_verify", HERE / "verify.py")
if spec is None or spec.loader is None:
    raise RuntimeError("cannot load verifier")
module = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = module
spec.loader.exec_module(module)


def main() -> None:
    original = json.loads((HERE / "certificate.json").read_text())
    mutations = []

    bad = copy.deepcopy(original)
    bad["format"] = "wrong"
    mutations.append(("format", bad))

    bad = copy.deepcopy(original)
    bad["points"][0]["x"][0] = "1"
    mutations.append(("coordinate", bad))

    bad = copy.deepcopy(original)
    bad["point_rows_sha256"] = "0" * 64
    mutations.append(("point hash", bad))

    bad = copy.deepcopy(original)
    bad["edges"] = bad["edges"][:-1]
    mutations.append(("missing edge", bad))

    bad = copy.deepcopy(original)
    bad["edge_rows_sha256"] = "0" * 64
    mutations.append(("edge hash", bad))

    bad = copy.deepcopy(original)
    bad["chromatic"]["four_colouring"] = "0" * 10
    mutations.append(("colouring", bad))

    bad = copy.deepcopy(original)
    bad["relation"]["canonical_extendible_patterns"] = bad["relation"]["canonical_extendible_patterns"][:-1]
    mutations.append(("relation", bad))

    bad = copy.deepcopy(original)
    key = next(iter(bad["relation"]["canonical_witnesses"]))
    bad["relation"]["canonical_witnesses"][key] = "0" * 10
    mutations.append(("witness", bad))

    accepted = []
    for label, cert in mutations:
        try:
            module.verify(cert)
        except (TypeError, ValueError):
            continue
        accepted.append(label)
    if accepted:
        raise SystemExit("negative controls accepted: " + ", ".join(accepted))
    print(f"PASS: verifier rejected all {len(mutations)} malformed certificates")


if __name__ == "__main__":
    main()
