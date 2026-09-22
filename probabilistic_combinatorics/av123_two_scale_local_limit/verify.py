"""Finite exact audits supporting PROOF.md; not an asymptotic proof by data."""

import argparse
from collections import Counter
import hashlib
import json
from math import comb
from pathlib import Path

from counts import (ballot, catalan, distance_count, joint_count,
                    position_excedance_count)
from literal_audit import build_observations, path_counts


def require(condition, message):
    if not condition:
        raise ValueError(message)


def canonical(obj):
    return json.dumps(obj, sort_keys=True, separators=(",", ":")).encode()


def audit():
    object_rows = []
    histogram_digest = hashlib.sha256()
    identity_checks = cells = 0
    for n, total, observed in build_observations():
        require(total == catalan(n), (n, "Catalan total"))
        predicted = Counter()
        for d in range(1, n//2+1):
            for x in range(d):
                for y in range(d):
                    number = joint_count(n, d, x, y)
                    if number:
                        require((n-d+1+x-y) % 2 == 0, "position parity")
                        require((n-d-1+x+y) % 2 == 0, "excedance parity")
                        a = (n-d+1+x-y)//2
                        e = (n-d-1+x+y)//2
                        predicted[d, x, y, a, e] = number
        require(predicted == observed, (n, "literal joint count mismatch"))
        for (d, x, y, a, e), number in observed.items():
            require(2*a == n-d+1+x-y, "position identity")
            require(2*e == n-d-1+x+y, "excedance identity")
            require(position_excedance_count(n, d, a, e) == number,
                    "position/excedance decoding")
            identity_checks += 3
        cells += len(observed)
        histogram_digest.update(canonical([n, sorted(observed.items())]))
        object_rows.append({"n": n, "avoiders": total,
                            "two_fixed": sum(observed.values()),
                            "nonzero_joint_cells": len(observed)})

    ballot_checks = ratio_checks = log_concavity_checks = 0
    for length in range(151):
        direct = path_counts(length)
        for t in range(-2, length+3):
            expected = direct[t] if 0 <= t < len(direct) else 0
            require(ballot(length, t) == expected, "ballot/path mismatch")
            ballot_checks += 1
        for t in range(length % 2, length-1, 2):
            a, b = ballot(length, t), ballot(length, t+2)
            require(b*(t+1)*(length+t+4) == a*(t+3)*(length-t),
                    "ballot adjacent ratio")
            ratio_checks += 1
            if t+4 <= length:
                c = ballot(length, t+4)
                require(b*b >= a*c, "ballot log concavity")
                log_concavity_checks += 1

    maximum_checks = rational_product_checks = 0
    for n in range(2, 121):
        for d in range(1, n//2+1):
            m, length = d-1, n-d-1
            delta = (length-m) % 2
            maximum = ballot(length, m+delta)*ballot(length, m-delta)
            for s in range(length % 2, 2*m+1, 2):
                g = ballot(length, s)*ballot(length, 2*m-s)
                require(g <= maximum, (n, d, s, "central maximum"))
                maximum_checks += 1
                if 0 <= s <= length and 0 <= 2*m-s <= length:
                    k = s-m
                    product = (comb(length, (length-s)//2)
                               *comb(length, (length-2*m+s)//2))
                    require(g*(n*n-k*k) == 4*(d*d-k*k)*product,
                            "exact rational product (20)")
                    rational_product_checks += 1

    lattice_checks = vandermonde_checks = 0
    for n in range(2, 41):
        for d in range(1, n//2+1):
            m, length = d-1, n-d-1
            total = 0
            hk_points = set()
            for x in range(m+1):
                for y in range(m+1):
                    total += joint_count(n, d, x, y)
                    if (x+y-length) % 2 == 0:
                        h, k = x-y, x+y-m
                        require(h % 2 == length % 2 and k % 2 == n % 2,
                                "wrong h,k parity")
                        require((m+k+h)//2 == x and (m+k-h)//2 == y,
                                "lattice inverse")
                        hk_points.add((h, k))
                        lattice_checks += 1
            expected_hk = {(h, k) for h in range(-m, m+1)
                           for k in range(-m, m+1)
                           if h % 2 == length % 2 and k % 2 == n % 2
                           and abs(h)+abs(k) <= m}
            require(hk_points == expected_hk, "extra lattice constraint")
            require(total == distance_count(n, d), "Vandermonde distance sum")
            vandermonde_checks += 1

    parity_checks = 0
    for m in range(1, 101):
        for parity in (0, 1):
            total = sum(comb(2*m, s) for s in range(parity, 2*m+1, 2))
            require(total == 2**(2*m-1), "parity normalization")
            parity_checks += 1
    # Explicit controls for unsupported, empty, and parity-forbidden inputs.
    zero_controls = [joint_count(1, 1, 0, 0), joint_count(8, 5, 0, 0),
                     joint_count(8, 2, -1, 0), joint_count(8, 2, 0, 2),
                     joint_count(9, 1, 0, 0), ballot(10, 3), ballot(0, 1),
                     position_excedance_count(8, 2, 0, 3),
                     position_excedance_count(8, 2, 8, 3)]
    require(not any(zero_controls), "zero-domain control")

    return {"status": "ALL_EXACT_CHECKS_PASSED",
            "literal_permutation_maximum": 9, "insertion_maximum": 12,
            "objects": object_rows, "nonzero_joint_cells": cells,
            "histogram_sha256": histogram_digest.hexdigest(),
            "identity_checks": identity_checks,
            "ballot_path_checks": ballot_checks,
            "ballot_ratio_checks": ratio_checks,
            "ballot_log_concavity_checks": log_concavity_checks,
            "central_maximum_checks": maximum_checks,
            "rational_product_checks": rational_product_checks,
            "lattice_point_checks": lattice_checks,
            "vandermonde_distance_checks": vandermonde_checks,
            "parity_normalization_checks": parity_checks,
            "zero_domain_controls": len(zero_controls)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check-expected", action="store_true")
    parser.add_argument("--write-expected", action="store_true")
    args = parser.parse_args()
    result = audit()
    result["record_sha256"] = hashlib.sha256(canonical(result)).hexdigest()
    path = Path(__file__).with_name("expected.json")
    if args.check_expected:
        require(json.loads(path.read_text()) == result, "expected record differs")
    if args.write_expected:
        path.write_text(json.dumps(result, indent=2)+"\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
