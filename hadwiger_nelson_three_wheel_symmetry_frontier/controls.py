#!/usr/bin/env python3
"""Targeted corruption controls for the symmetry certificate."""
from copy import deepcopy
import json

import verify as V


def expect_rejection(name, action, rejected):
    try:
        action()
    except (KeyError, TypeError, ValueError):
        rejected.append(name)
    else:
        raise ValueError("accepted corruption: " + name)


def run():
    certificate = json.loads((V.HERE / "certificate.json").read_text())
    source, factors, active, source_rows, cover = V.source_state()
    alignment = V.alignment_ids(factors)
    domain_ids = sorted(active - alignment)
    safe = alignment | (set(range(len(factors))) - active)
    permutations, word_maps = V.generator_data(certificate, factors, domain_ids, safe)
    group = V.group_closure(permutations)
    rejected = []

    bad = deepcopy(certificate)
    bad["generators"]["swap"]["identities"].pop()
    expect_rejection("missing generator identity", lambda: V.generator_data(bad, factors, domain_ids, safe), rejected)

    bad = deepcopy(certificate)
    original = bad["generators"]["swap"]["identities"][0]["target"]
    bad["generators"]["swap"]["identities"][0]["target"] = next(i for i in domain_ids if i != original)
    expect_rejection("wrong generator target", lambda: V.generator_data(bad, factors, domain_ids, safe), rejected)

    bad = deepcopy(certificate)
    bad["generators"]["conjugate"]["identities"][0]["extras"].append([domain_ids[0], 1])
    expect_rejection("unsafe extra factor", lambda: V.generator_data(bad, factors, domain_ids, safe), rejected)

    bad = deepcopy(certificate)
    bad["pair_orbit_representatives"].pop()
    data = {"factors": factors, "pair_orbit_representatives": bad["pair_orbit_representatives"]}
    expect_rejection(
        "missing pair orbit representative",
        lambda: V.pair_quotient(data, source_rows, cover, domain_ids, alignment, group),
        rejected,
    )

    bad = deepcopy(certificate)
    bad["collision_orbit_representatives"][0]["x_coefficients"][0] = "0"
    expect_rejection("wrong collision coordinate", lambda: V.collision_check(bad), rejected)

    bad = deepcopy(certificate)
    bad["alignment_collision_types"][0]["solutions"].pop()
    expect_rejection("missing alignment collision root", lambda: V.collision_check(bad), rejected)

    return {"status": "ALL_CORRUPTIONS_REJECTED", "rejected": rejected}


if __name__ == "__main__":
    print(json.dumps(run(), indent=2, sort_keys=True))
