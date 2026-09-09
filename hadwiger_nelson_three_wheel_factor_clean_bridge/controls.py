#!/usr/bin/env python3
"""Corruption and arithmetic controls for the factor-clean bridge."""
from copy import deepcopy
from pathlib import Path
import json

import inputs
import verify


HERE = Path(__file__).resolve().parent


def main():
    expected, _ = verify.compute()
    published = json.loads((HERE / "certificate.json").read_text())
    verify.check_certificate(published, expected)
    mutations = []
    changed = deepcopy(published)
    changed["rows"].pop()
    mutations.append(("missing survivor row", changed))
    changed = deepcopy(published)
    changed["rows"][0]["nonunit_factor_ids"].pop()
    mutations.append(("missing nonunit factor", changed))
    changed = deepcopy(published)
    changed["rows"][0]["zero_factor_ids"].pop()
    mutations.append(("missing zero factor", changed))
    changed = deepcopy(published)
    changed["rows"][0]["proper_h4085_word_indices"].append(13)
    mutations.append(("false proper word", changed))
    changed = deepcopy(published)
    changed["rows"][0]["unit_edge_sha256"] = "0" * 64
    mutations.append(("wrong graph hash", changed))
    changed = deepcopy(published)
    changed["minimum_component_uniform_word_cover_size"] = 3
    mutations.append(("false three-word cover", changed))
    rejected = []
    for name, changed in mutations:
        try:
            verify.check_certificate(changed, expected)
        except ValueError:
            rejected.append(name)
        else:
            raise ValueError("accepted corruption: " + name)

    inputs.need(verify.polynomial_gcd([Q for Q in (0, -1, 1)], [-1, 1])
                == [-1, 1], "shared-root gcd control")
    inputs.need(verify.polynomial_gcd([1, 0, 1], [-1, 1]) == [1],
                "coprime gcd control")
    print(json.dumps({
        "status": "ALL_CONTROLS_PASSED",
        "certificate_corruptions_rejected": rejected,
        "low_level_controls": ["shared-root gcd", "coprime gcd"],
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
