#!/usr/bin/env python3
"""Exact signature-population derivation of the degree-stratified bound."""
import json

ORDER = 43
OUTSIDE = 39


def rows():
    answer = []
    for degree in range(18, 25):
        required = 4 * (degree - 3)
        feasible = []
        for n0 in range(OUTSIDE + 1):
            for n1 in range(OUTSIDE - n0 + 1):
                for n2 in range(OUTSIDE - n0 - n1 + 1):
                    n3 = OUTSIDE - n0 - n1 - n2
                    if n3 <= 16 and n1 + 2 * n2 + 3 * n3 >= required:
                        feasible.append((n0, n1, n2, n3))
        maximum = max(row[0] for row in feasible)
        extremal = [list(row) for row in feasible if row[0] == maximum]
        answer.append({
            "minimum_color_degree": degree,
            "required_same_color_incidence": required,
            "maximum_three_contact_vertices": 16,
            "feasible_signature_populations": len(feasible),
            "maximum_noncontacts": maximum,
            "minimum_contacts": OUTSIDE - maximum,
            "extremal_populations": extremal,
        })
    return answer


def run():
    data = rows()
    expected = [53 - 2 * d for d in range(18, 25)]
    if [row["maximum_noncontacts"] for row in data] != expected:
        raise ValueError("sharp signature bound")
    return {
        "status": "VERIFIED_K4_SIGNATURE_DEGREE_STRATA",
        "order": ORDER,
        "outside_vertices": OUTSIDE,
        "degree_window": [18, 24],
        "unconditional_minimum_contacts": 22,
        "h3899_minimum_contacts": 19,
        "contact_gain": 3,
        "rows": data,
        "target43_found": False,
        "tasks_decided": 0,
    }


if __name__ == "__main__":
    print(json.dumps(run(), indent=2, sort_keys=True))
