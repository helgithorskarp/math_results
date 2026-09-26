#!/usr/bin/env python3
"""Exact prefix-cone construction and monotone-matching certificate.

The existing verify.py supplies the unchanged group, coefficient construction,
complete branching enumeration and matching routine. The new theorem uses
ordered weights of arbitrary ratios, not the old fixed-base coefficient cones.
independent_ordered_check.py imports neither constructor.
"""
from pathlib import Path
import argparse
import hashlib
import json
import verify as base


def encoded(value):
    return (json.dumps(value, indent=2, sort_keys=True) + "\n").encode()


def prefix_order(points):
    data = base.basis(points)
    prefix = [[[sum(data[g][i][k] for i in range(r + 1))
                for k in range(len(base.KEYS))] for r in range(4)]
              for g in range(base.N)]
    up = []
    for g in range(base.N):
        mask = 0
        for h in range(base.N):
            if all(b >= a for lower, upper in zip(prefix[g], prefix[h])
                   for a, b in zip(lower, upper)):
                mask |= 1 << h
        up.append(mask)
    base.audit_order(up)
    return up


def construction():
    orders = {"A": prefix_order(base.A), "B": prefix_order(base.B)}
    cert = {
        "schema": "square-cone-ordered-weights-v1",
        "group_size": 48,
        "group_order": "lexicographic (permutation of (0,1,2), signs in (-1,1)^3)",
        "group_action": "(g x)_i = signs_i * x_(perm_i)",
        "points_A": base.A,
        "points_B": base.B,
        "weight_order_A": [0, 1, 2, 3],
        "weight_order_B": [0, 1, 2, 3],
        "weight_condition": "q_0 >= q_1 >= q_2 >= q_3 >= 0, independently in each cluster",
        "prefix_generators": [[1] * k + [0] * (4-k) for k in range(1, 5)],
        "clearing_monomial_powers": [1, 2, 3],
        "coefficient_degree_box": [2, 4, 6],
        "orders": orders,
    }
    sets = base.upper_sets(orders["A"])
    digest = hashlib.sha256()
    total_edges = nonempty = 0
    for s in sets:
        matching = base.monotone_matching(s, orders["B"])
        total_edges += len(matching)
        nonempty += bool(matching)
        digest.update((str(s) + ":" + str(matching) + "\n").encode())

    # A reversed B order must not certify the same universal correlation.
    reverse_b = [sum(1 << j for j in range(48) if orders["B"][j] >> i & 1)
                 for i in range(48)]
    rejected = False
    for s in sets:
        try:
            base.monotone_matching(s, reverse_b)
        except RuntimeError:
            rejected = True
            break
    base.require(rejected, "Invalid reversed order was accepted")

    # The same support map is a contraction at every positive ray scale.
    cross_dots = [sum(a*b for a, b in zip(x, y)) for x in base.A for y in base.B]
    base.require(min(cross_dots) == 0 and max(cross_dots) == 2,
                 "Wrong cross-ray geometry")
    record = {
        "status": "ORDERED_WEIGHT_ORBIT_MATCHINGS_PASS",
        "certificate_sha256": hashlib.sha256(encoded(cert)).hexdigest(),
        "ordered_pairs": {name: sum(row.bit_count() for row in up)
                          for name, up in orders.items()},
        "A_upper_sets": len(sets),
        "nonempty_matchings": nonempty,
        "matching_edges": total_edges,
        "matching_digest": digest.hexdigest(),
        "reversed_order_control_rejected": rejected,
        "cross_dot_values": sorted(set(cross_dots)),
        "all_weight_ratios_allowed": True,
        "trust_boundary": "Exact finite computation plus the analytic ordered-weight and ball-union transfer in ORDERED_WEIGHTS.md; not independent peer review or formalization.",
    }
    return cert, record


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--certificate", action="store_true")
    args = parser.parse_args()
    cert, record = construction()
    here = Path(__file__).resolve().parent
    if args.check:
        base.require(encoded(cert) == (here / "ORDERED_CERTIFICATE.json").read_bytes(),
                     "Ordered-weight certificate differs")
        base.require(encoded(record) == (here / "ORDERED_EXPECTED.json").read_bytes(),
                     "Ordered-weight audit differs")
        print(record["status"], hashlib.sha256(encoded(record)).hexdigest())
    else:
        print(encoded(cert if args.certificate else record).decode(), end="")


if __name__ == "__main__":
    main()
