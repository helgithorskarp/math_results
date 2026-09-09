#!/usr/bin/env python3
"""Focused corruption controls for exact algebra and certificate decoding."""
from copy import deepcopy
from fractions import Fraction as Q
from pathlib import Path
from tempfile import TemporaryDirectory
import json

import verify as V


HERE = Path(__file__).resolve().parent


def need(condition, message):
    if not condition:
        raise ValueError(message)


def low_level_controls():
    # Sturm coverage must reject an omitted real root.
    polynomial = [Q(-2), Q(0), Q(1)]
    V.check_intervals(polynomial, [["-2", "-1"], ["1", "2"]])
    try:
        V.check_intervals(polynomial, [["1", "2"]])
    except ValueError:
        pass
    else:
        raise RuntimeError("accepted incomplete Sturm coverage")

    # A shared zero of two residues must not be called excluded.
    modulus = [Q(-2), Q(0), Q(1)]
    need(not V.no_common_root(modulus, modulus), "common-root control")
    need(V.no_common_root(modulus, [Q(1), Q(1)]), "coprime-residue control")
    return ["incomplete Sturm coverage", "shared residue root"]


def certificate_controls():
    original = json.loads((HERE / "certificate.json").read_text())
    corruptions = []
    altered = deepcopy(original)
    altered["pair_rows"][0]["relation_a"][0] = "2"
    corruptions.append(("wrong shape relation", altered))
    altered = deepcopy(original)
    altered["pair_rows"][0]["components"][0]["intervals"].pop()
    corruptions.append(("missing real embedding", altered))
    altered = deepcopy(original)
    altered["pair_rows"][5]["components"][0]["failure_factor_ids"][0] = 989
    corruptions.append(("wrong failure witness", altered))

    rejected = []
    with TemporaryDirectory(prefix="hn-viability-controls-") as directory:
        directory = Path(directory)
        for index, (name, certificate) in enumerate(corruptions):
            path = directory / f"corruption-{index}.json"
            path.write_text(json.dumps(certificate, separators=(",", ":")) + "\n")
            try:
                V.run(path)
            except ValueError:
                rejected.append(name)
            else:
                raise RuntimeError("accepted corruption: " + name)
    return rejected


if __name__ == "__main__":
    print(json.dumps({"low_level_controls": low_level_controls(),
                      "rejected_certificate_corruptions": certificate_controls()},
                     indent=2, sort_keys=True))
