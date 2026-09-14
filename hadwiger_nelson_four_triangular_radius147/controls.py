#!/usr/bin/env python3
"""Positive controls for the compressed four-cycle obstruction test."""

from collections import defaultdict
import json
from math import isqrt

import verify


def require(condition, message):
    if not condition:
        raise ValueError(message)


def patch(limit):
    bound = isqrt(4 * limit // 3)
    return {(a, b) for a in range(-bound, bound + 1)
            for b in range(-bound, bound + 1)
            if a * a + a * b + b * b <= limit}


def norm(point):
    a, b = point
    return a * a + a * b + b * b


def main():
    buckets = defaultdict(lambda: {"sign": {}, "zero": {}})
    require(verify.insert_path(buckets, "target", "sign", 0, "a") is None,
            "first synthetic path unexpectedly conflicts")
    require(verify.insert_path(buckets, "target", "sign", 0, "b") is None,
            "same-label synthetic path unexpectedly conflicts")
    require(verify.insert_path(buckets, "target", "sign", 1, "c") == "a",
            "opposite-label synthetic square was not detected")

    # At P36 the preceding verifier explicitly reconstructs and colours every
    # one of 8,100 normalized C4 placements.  The compressed census must agree
    # with that independently implemented full enumeration.
    fast = verify.scan(36)
    verify.exact.LIMIT = 36
    explicit = verify.exact.certify()
    require(fast["normalized_active_triangles"] ==
            explicit["normalized_active_triangles"] == 186,
            "P36 triangle controls disagree")
    require(explicit["normalized_four_cycles"] == 8100,
            "P36 explicit C4 control changed")
    require(fast["inconsistent_triangles"] == 0 and
            fast["opposite_parity_target_channels"] == 0,
            "compressed P36 control reports a false obstruction")
    require(fast["channel_label_states"] == fast["channel_target_buckets"],
            "compressed P36 control has a dual-label bucket")

    # Exact geometric bridge to the record-relevant corollary: recentering a
    # P36 copy at any one of its vertices puts it inside P144, hence P147.
    p36, p37, p147, p148 = (patch(limit) for limit in (36, 37, 147, 148))
    differences = {(z[0] - a[0], z[1] - a[1])
                   for z in p36 for a in p36}
    require(max(map(norm, differences)) == 144,
            "P36 difference hull does not have exact radius 144")
    require(differences <= p147,
            "a recentered P36 patch escapes P147")
    require((len(p36), len(p37), len(p147), len(p148)) ==
            (127, 139, 535, 547), "patch cardinality boundary changed")

    report = {
        "verified": True,
        "synthetic_opposite_label_detected": True,
        "p36_explicit_triangles": explicit["normalized_active_triangles"],
        "p36_explicit_four_cycles": explicit["normalized_four_cycles"],
        "p36_fast_two_edge_products": fast["two_edge_products"],
        "p36_fast_opposite_parity_target_channels":
            fast["opposite_parity_target_channels"],
        "p36_difference_hull_maximum_norm": max(map(norm, differences)),
        "p36_difference_hull_points": len(differences),
        "patch_cardinalities": {
            "P36": len(p36),
            "P37": len(p37),
            "P147": len(p147),
            "P148": len(p148),
        },
    }
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
