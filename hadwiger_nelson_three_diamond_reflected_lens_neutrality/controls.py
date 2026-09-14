#!/usr/bin/env python3
"""Negative controls for the reflected-lens verifier."""

from __future__ import annotations

import copy
import importlib.util
import json
import sys
from pathlib import Path


HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("reflected_lens_verify", HERE / "verify.py")
if spec is None or spec.loader is None:
    raise RuntimeError("cannot load verifier")
module = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = module
spec.loader.exec_module(module)


def main() -> None:
    original = json.loads((HERE / "certificate.json").read_text())
    mutations = []
    for label, edit in (
        ("format", lambda c: c.__setitem__("format", "wrong")),
        ("point hash", lambda c: c.__setitem__("point_rows_sha256", "0" * 64)),
        ("edge hash", lambda c: c.__setitem__("edge_rows_sha256", "0" * 64)),
        ("coordinate", lambda c: c["points"][8]["x"].__setitem__(0, "1")),
        ("edge", lambda c: c["edges"].pop()),
        ("colour", lambda c: c["chromatic"].__setitem__("three_colouring", "0" * 16)),
        ("relation", lambda c: c["relation"]["canonical_output_patterns"].pop()),
        ("boundary", lambda c: c["interaction_boundary"].__setitem__("added_internal_contacts", 1)),
    ):
        bad = copy.deepcopy(original)
        edit(bad)
        mutations.append((label, bad))
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
