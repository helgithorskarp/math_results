#!/usr/bin/env python3
"""Boundary and malformed-certificate controls for the E477 review."""

from copy import deepcopy
from itertools import combinations
import json
from pathlib import Path

import verify


HERE = Path(__file__).resolve().parent


def require(condition, message):
    if not condition:
        raise ValueError(message)


def rejects(certificate):
    try:
        verify.verify(certificate)
    except (KeyError, TypeError, ValueError):
        return True
    return False


def main():
    certificate = json.loads((HERE / "certificate.json").read_text())
    baseline = verify.verify(certificate)

    # Exhaust the abstract one-edge/two-list boundary independently of the
    # verifier's assignment loop.
    mask_controls = 0
    for left_mask in range(16):
        for right_mask in range(16):
            for edge in (False, True):
                direct = any(
                    left_mask & (1 << left) and right_mask & (1 << right) and (not edge or left != right)
                    for left in range(4)
                    for right in range(4)
                )
                formula = bool(left_mask and right_mask) and (
                    not edge
                    or left_mask & (left_mask - 1)
                    or right_mask & (right_mask - 1)
                    or left_mask != right_mask
                )
                require(bool(formula) == direct, "mask boundary mismatch")
                mask_controls += 1

    # The producer's shortcut unit predicate must agree entry-by-entry with
    # the verifier's generic radical arithmetic.
    equal = json.loads((verify.SOURCE / "certificate.json").read_text())["equal"]
    rows = equal["points"]
    points = [verify.point(row) for row in rows]
    geometry_controls = 0
    for left, right in combinations(range(477), 2):
        a, b, c, d = (x - y for x, y in zip(rows[left], rows[right]))
        shortcut = 3 * a * a + 11 * b * b + c * c + 33 * d * d == 1296 and a * b + c * d == 0
        require(shortcut == verify.unit(points[left], points[right]), "unit predicate mismatch")
        geometry_controls += 1

    malformed_rejected = 0
    bad = deepcopy(certificate)
    bad["core_colourings"][0] = "4" + bad["core_colourings"][0][1:]
    require(rejects(bad), "invalid colour accepted")
    malformed_rejected += 1
    bad = deepcopy(certificate)
    bad["core_vertices"][0] = 2
    require(rejects(bad), "bad core accepted")
    malformed_rejected += 1
    bad = deepcopy(certificate)
    bad["optional_vertices"] = bad["optional_vertices"][:-1]
    require(rejects(bad), "bad optional set accepted")
    malformed_rejected += 1

    # The greedy bank is irredundant: deleting any one word exposes an
    # uncovered singleton or pair.  Each such damaged input must be rejected.
    removal_controls = 0
    for index in range(len(certificate["core_colourings"])):
        bad = deepcopy(certificate)
        del bad["core_colourings"][index]
        require(rejects(bad), "redundant certificate word unexpectedly accepted")
        removal_controls += 1

    result = {
        "all_controls_passed": True,
        "baseline_status": baseline["status"],
        "geometry_pair_controls": geometry_controls,
        "mask_boundary_controls": mask_controls,
        "malformed_certificates_rejected": malformed_rejected,
        "single_word_removal_certificates_rejected": removal_controls,
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
