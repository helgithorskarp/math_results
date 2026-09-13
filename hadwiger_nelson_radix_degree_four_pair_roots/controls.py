#!/usr/bin/env python3
"""Negative controls for certificate binding and colouring replay."""

from __future__ import annotations

import argparse
import copy
import json
import tempfile
from pathlib import Path

import verify


HERE = Path(__file__).resolve().parent


def must_fail(residual, value, directory, label):
    path = Path(directory) / f"{label}.json"
    path.write_text(json.dumps(value, sort_keys=True, separators=(",", ":")) + "\n")
    try:
        verify.verify(residual, path)
    except ValueError:
        return
    raise ValueError(f"negative control unexpectedly passed: {label}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--residual", type=Path, required=True)
    parser.add_argument("--certificate", type=Path, default=HERE / "certificate.json")
    args = parser.parse_args()
    baseline = json.loads(args.certificate.read_text())
    verify.verify(args.residual, args.certificate)
    with tempfile.TemporaryDirectory(prefix="hn-degree4-controls-") as directory:
        bad_digest = copy.deepcopy(baseline)
        bad_digest["source_residual_sha256"] = "0" * 64
        must_fail(args.residual, bad_digest, directory, "source-digest")

        bad_decomposition = copy.deepcopy(baseline)
        bad_decomposition["pair_components"][0]["real_component_keys"] = []
        must_fail(args.residual, bad_decomposition, directory, "decomposition")

        bad_colour = copy.deepcopy(baseline)
        row = next(row for row in bad_colour["components"] if row["three_colouring"] is not None)
        row["three_colouring"] = [0] * 243
        must_fail(args.residual, bad_colour, directory, "colour-word")
    print("PASS: baseline and 3 negative controls")
