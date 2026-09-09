#!/usr/bin/env python3
"""Small-space and malformed-certificate controls for the five-cover theorem."""

from copy import deepcopy
from itertools import combinations, product
import importlib.util
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location("five_pencil_control_verifier", HERE / "verify.py")
V = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(V)


def reject(certificate, mutation):
    changed = deepcopy(certificate)
    mutation(changed)
    try:
        V.precheck_certificate(changed)
    except (KeyError, TypeError, ValueError):
        return
    raise ValueError("malformed certificate accepted")


def main():
    words = tuple(product(range(4), repeat=2))
    normals = sorted(
        {
            V.projective(normal, 0)[0]
            for normal in words
            if any(normal)
        }
    )
    lines = [(normal, constant) for normal in normals for constant in range(4)]
    masks = {
        line: sum(
            1 << index
            for index, word in enumerate(words)
            if V.dot(line[0], word) == line[1]
        )
        for line in lines
    }
    full = (1 << len(words)) - 1
    covers = [
        family
        for family in combinations(lines, 5)
        if __import__("functools").reduce(
            int.__or__, (masks[line] for line in family), 0
        )
        == full
    ]
    profiles = {}
    for family in covers:
        multiplicities = {}
        for normal, _ in family:
            multiplicities[normal] = multiplicities.get(normal, 0) + 1
        profile = tuple(sorted(multiplicities.values(), reverse=True))
        profiles[profile] = profiles.get(profile, 0) + 1
    if len(covers) != 96 or profiles != {(4, 1): 80, (1, 1, 1, 1, 1): 16}:
        raise ValueError("AG(2,4) exhaustive five-line control")

    certificate = json.loads((HERE / "certificate.json").read_text())
    V.precheck_certificate(certificate)
    mutations = [
        lambda item: item.__setitem__("schema", "corrupt"),
        lambda item: item["affine_cover_classification"].__setitem__("abstract_five_covers", 1),
        lambda item: item["affine_cover_classification"]["pencils_by_missing_type_count"].__setitem__("0", 1),
        lambda item: item["curve_lift_frontier"].__setitem__("removed_by_h4167_pairs", 1),
        lambda item: item["curve_lift_frontier"].__setitem__("pencils_empty_after_triples", 1),
        lambda item: item["pair_frontier"].__setitem__("requires_at_least_six_pair_orbits", 1),
        lambda item: item["pair_frontier"].__setitem__("classification_D3_invariant", False),
        lambda item: item.__setitem__("record_improvement", True),
    ]
    for mutation in mutations:
        reject(certificate, mutation)
    print(json.dumps({
        "status": "CONTROLS_PASSED",
        "AG_2_4_five_line_subsets_checked": 15504,
        "AG_2_4_cover_count": len(covers),
        "AG_2_4_cover_profiles": {str(key): value for key, value in sorted(profiles.items())},
        "malformed_certificates_rejected": len(mutations),
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
