#!/usr/bin/env python3
"""Mutation controls for the Parts574 indispensability certificate."""
from __future__ import annotations

import base64
import json
import tempfile
from pathlib import Path

from verify import HERE, GEOMETRY, PARENT, compute, load_module, unpack


def pack(word):
    raw = bytearray((len(word) + 3) // 4)
    for i, character in enumerate(word):
        raw[i // 4] |= int(character) << (2 * (i % 4))
    return base64.b64encode(raw).decode()


def must_fail(data, label):
    with tempfile.TemporaryDirectory(prefix="parts574-L-control-") as directory:
        path = Path(directory) / "mutated.json"
        path.write_text(json.dumps(data))
        try:
            compute(path)
        except ValueError:
            print(f"PASS {label}")
            return
    raise AssertionError(f"mutation escaped verification: {label}")


def main():
    original = json.loads((HERE / "certificate.json").read_text())

    missing = json.loads(json.dumps(original))
    missing["L_deletion_colourings"].pop()
    must_fail(missing, "missing_deletion_row")

    padding = json.loads(json.dumps(original))
    entry = padding["L_deletion_colourings"][0]
    raw = bytearray(base64.b64decode(entry["colouring_2bit"]))
    raw[-1] |= 0b11000000
    entry["colouring_2bit"] = base64.b64encode(raw).decode()
    must_fail(padding, "packed_padding")

    monochromatic = json.loads(json.dumps(original))
    entry = monochromatic["L_deletion_colourings"][0]
    parent = json.loads((PARENT / "certificate.json").read_text())
    labels = list(range(374)) + parent["pool_labels"]
    active = [v for v in labels if v != entry["removed"]]
    word = list(unpack(entry["colouring_2bit"], 573))
    position = {v: i for i, v in enumerate(active)}
    colours = dict(zip(active, word))
    geometry = load_module("control_geometry", GEOMETRY)
    _, _, _, _, all_edges = geometry.read_geometry()
    label_set = set(labels)
    for a, b in all_edges:
        if a in position and b in position and a in label_set and b in label_set:
            word[position[a]] = colours[b]
            break
    else:
        raise AssertionError("no active edge for control")
    entry["colouring_2bit"] = pack("".join(word))
    must_fail(monochromatic, "monochromatic_edge")
    print("ALL_PARTS574_L_CONTROLS_PASSED")


if __name__ == "__main__":
    main()
