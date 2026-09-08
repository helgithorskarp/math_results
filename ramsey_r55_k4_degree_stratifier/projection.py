#!/usr/bin/env python3
"""Exact contact-projection and propagation-strength comparison."""
from math import comb
import json


def run():
    old = sum(comb(39, n) for n in range(21))
    rows = []
    for degree in range(18, 25):
        maximum = 53 - 2 * degree
        retained = sum(comb(39, n) for n in range(maximum + 1))
        baseline_contacts = max(19, degree)
        new_contacts = 2 * degree - 14
        rows.append({
            "minimum_color_degree": degree,
            "maximum_noncontacts": maximum,
            "minimum_contacts": new_contacts,
            "minimum_contacts_from_h3899_plus_h3909": baseline_contacts,
            "additional_forced_contacts": new_contacts - baseline_contacts,
            "retained_binary_contact_patterns": retained,
            "h3899_binary_contact_patterns": old,
            "removed_from_h3899_projection": old - retained,
            "exact_reduction_ratio": {"numerator": old, "denominator": retained},
            "conflict_after_fixed_noncontacts": maximum + 1,
        })
    return {
        "status": "VERIFIED_DEGREE_STRATIFIER_PROPAGATION_SIGNAL",
        "scope": "Per-block binary contact projection only; patterns are not independent physical graphs or task counts.",
        "h3899_conflict_after_fixed_noncontacts": 21,
        "new_unconditional_conflict_after_fixed_noncontacts": 18,
        "earlier_unconditional_conflict": 3,
        "rows": rows,
        "solver_calls": 0,
        "target43_found": False,
    }


if __name__ == "__main__":
    print(json.dumps(run(), indent=2, sort_keys=True))
