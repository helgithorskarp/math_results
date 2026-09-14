#!/usr/bin/env python3
"""Mutation and algebra controls for the E457 field obstruction."""

from __future__ import annotations

import copy
import json
import tempfile
from pathlib import Path

import verify


def reject(core, label):
    with tempfile.TemporaryDirectory() as directory:
        path = Path(directory) / "core.json"
        path.write_text(json.dumps(core))
        try:
            verify.verify(path, check_hashes=False)
        except (ValueError, KeyError, TypeError):
            return label
    raise RuntimeError(f"accepted malformed control: {label}")


def main():
    original = json.loads(verify.CORE.read_text())
    controls = []
    bad = copy.deepcopy(original)
    bad["schema"] = "wrong"
    controls.append(reject(bad, "schema"))
    bad = copy.deepcopy(original)
    bad["points"][1] = [0, 0, 95, 0]
    controls.append(reject(bad, "endpoint"))
    bad = copy.deepcopy(original)
    bad["points"][2] = bad["points"][3]
    controls.append(reject(bad, "collision"))
    bad = copy.deepcopy(original)
    bad["points"] = bad["points"][:-1]
    controls.append(reject(bad, "point_count"))

    probes = [
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1],
        [7, -3, 11, 5],
        [-12, 9, -4, 17],
    ]
    if not all(verify.source_norm(row) == verify.e_norm(verify.rotate_to_e(row))
               for row in probes):
        raise RuntimeError("norm identity control failed")
    print(json.dumps({
        "verified": True,
        "malformed_controls_rejected": controls,
        "norm_identity_probes": len(probes),
    }, sort_keys=True, separators=(",", ":")))


if __name__ == "__main__":
    main()
