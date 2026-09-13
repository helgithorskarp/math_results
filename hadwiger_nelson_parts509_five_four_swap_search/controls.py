#!/usr/bin/env python3
"""Mutation controls for the compact certificate checker."""
from __future__ import annotations

import copy
import json
import tempfile
from pathlib import Path

from verify import HERE, verify


def main():
    source = json.loads((HERE / "certificate.json").read_text())
    mutations = []

    bad = copy.deepcopy(source)
    bad["killing_sets"][0]["D"] = []
    mutations.append(("empty_killing_set", bad))

    bad = copy.deepcopy(source)
    bad["killing_sets"][0]["class_index"] = 20
    mutations.append(("bad_interface_class", bad))

    bad = copy.deepcopy(source)
    bad["killing_sets"][0]["colouring_U_minus_D_2bit"] = "not-base64!"
    mutations.append(("bad_colour_payload", bad))

    bad = copy.deepcopy(source)
    bad["pool"][0] = -1
    mutations.append(("changed_pool", bad))

    bad = copy.deepcopy(source)
    bad["selectors"]["5"]["sha256"] = "0" * 64
    mutations.append(("changed_selector_hash", bad))

    with tempfile.TemporaryDirectory(prefix="parts-pool-controls-") as tmp:
        for name, certificate in mutations:
            path = Path(tmp) / f"{name}.json"
            path.write_text(json.dumps(certificate))
            try:
                verify(path)
            except ValueError:
                print(f"rejected {name}")
            else:
                raise AssertionError(f"accepted mutation: {name}")
    print("ALL_MUTATION_CONTROLS_REJECTED")


if __name__ == "__main__":
    main()
