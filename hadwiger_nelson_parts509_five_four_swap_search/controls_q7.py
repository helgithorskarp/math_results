#!/usr/bin/env python3
"""Mutation controls for the q=7 positive-evidence verifier."""
from __future__ import annotations

import json
import tempfile
from pathlib import Path

from certlib import pack_colours, unpack_colours
from verify_q7_frontier import HERE, PAIR, verify


def must_fail(data, label):
    with tempfile.TemporaryDirectory(prefix="parts-q7-control-") as directory:
        path = Path(directory) / "mutated.json"
        path.write_text(json.dumps(data))
        try:
            verify(path)
        except ValueError:
            print(f"PASS {label}")
            return
    raise AssertionError(f"mutation escaped verification: {label}")


def main():
    original = json.loads((HERE / "q7_frontier_certificate.json").read_text())

    wrong_order = json.loads(json.dumps(original))
    wrong_order["candidate"]["S_deleted"].pop()
    must_fail(wrong_order, "candidate_order")

    bad_padding = json.loads(json.dumps(original))
    packed = bad_padding["candidate"]["verified_compatible_colourings"][0]
    # There are 134 selected pool colours, hence two unused two-bit slots.
    import base64
    raw = bytearray(base64.b64decode(packed["colouring_selected_pool_2bit"]))
    raw[-1] |= 0b11000000
    packed["colouring_selected_pool_2bit"] = base64.b64encode(raw).decode()
    must_fail(bad_padding, "packed_padding")

    monochromatic = json.loads(json.dumps(original))
    candidate = monochromatic["candidate"]
    selected = ((set(range(374, 509)) - set(candidate["S_deleted"])) |
                set(candidate["Q5_added"]))
    entry = candidate["verified_compatible_colourings"][0]
    word = list(unpack_colours(entry["colouring_selected_pool_2bit"], 134))
    pool_vertices = sorted(selected)
    pool_index = {v: i for i, v in enumerate(pool_vertices)}
    interface = json.loads((HERE.parent /
        "hadwiger_nelson_parts509_interface_lemma/interface_L.json").read_text())
    colours = {v: interface["classes"][entry["class_index"]]
               ["witness_colouring_L"][v] for v in range(374)}
    colours.update(zip(pool_vertices, word))
    ambient = json.loads((PAIR / "ambient_w3_edges.json").read_text())
    for a, b in ambient["edges"]:
        if a in selected and b in (set(range(374)) | selected):
            word[pool_index[a]] = colours[b]
            break
        if b in selected and a in (set(range(374)) | selected):
            word[pool_index[b]] = colours[a]
            break
    else:
        raise AssertionError("no mutable candidate edge")
    entry["colouring_selected_pool_2bit"] = pack_colours("".join(word))
    must_fail(monochromatic, "candidate_monochromatic_edge")
    print("ALL_Q7_MUTATION_CONTROLS_PASSED")


if __name__ == "__main__":
    main()
