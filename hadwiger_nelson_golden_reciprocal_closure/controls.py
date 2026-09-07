#!/usr/bin/env python3
"""Cross-representation, enumeration, and certificate rejection controls."""

import json
from pathlib import Path

import model
import verify

HERE = Path(__file__).resolve().parent


def to_nested(a):
    c0, c1, c2, c3 = a
    return (
        (c0 - (c1 + c2 + c3) / 4, (c1 - c2 - c3) / 4),
        (c1 / 4 - c2 / 8 + c3 / 8, c2 / 8 - c3 / 8),
    )


def main():
    if model.power(model.ZETA, 5) != model.ONE:
        raise AssertionError("cyclotomic fifth-root identity failed")
    if model.add(model.PHI, model.ONE) != model.mul(model.PHI, model.PHI):
        raise AssertionError("golden-ratio identity failed")

    pair_checks = 0
    for left in range(len(model.SOURCE)):
        for right in range(left + 1, len(model.SOURCE)):
            difference = model.sub(model.SOURCE[right], model.SOURCE[left])
            nested = to_nested(difference)
            if to_nested(model.conjugate(difference)) != verify.cconjugate(nested):
                raise AssertionError("conjugation representations disagree")
            if to_nested(model.norm(difference))[0] != verify.cnorm(nested):
                raise AssertionError("norm representations disagree")
            if to_nested(model.inverse(difference)) != verify.cinverse(nested):
                raise AssertionError("inverse representations disagree")
            pair_checks += 1

    producer_groups = {}
    verifier_groups = {}
    copy_checks = 0
    for name, scale_squared in (
            ("down", model.INVERSE_PHI_SQUARED), ("up", model.PHI_SQUARED)):
        producer_groups[name] = model.enumerate_copies(scale_squared)
        verifier_groups[name] = verify.enumerate_copies(name)
        producer_sets = tuple(sorted(
            tuple(sorted(model.canonical_key(point) for point in copy[-1]))
            for copy in producer_groups[name][1]
        ))
        verifier_sets = tuple(point_set for point_set, _points
                              in verifier_groups[name][1])
        if producer_groups[name][0] != verifier_groups[name][0]:
            raise AssertionError("raw specification counts disagree")
        if producer_sets != verifier_sets:
            raise AssertionError("copy point sets disagree entry by entry")
        source_keys = {model.canonical_key(point) for point in model.SOURCE}
        if any(len(set(point_set) & source_keys) < 2 for point_set in producer_sets):
            raise AssertionError("enumerated copy violates coincidence condition")
        copy_checks += len(producer_sets)

    point_map = {verify.point_key(point): point for point in verify.SOURCE}
    for _raw, copies in verifier_groups.values():
        for _point_set, points in copies:
            for point in points:
                point_map.setdefault(verify.point_key(point), point)
    keys = tuple(sorted(point_map))
    edges = verify.distance_edges(keys)
    certificate = json.loads((HERE / "certificate.json").read_text())
    word = certificate["full_closure"]["four_colouring"]
    colours = tuple(int(value) for value in word)
    if not verify.valid_colouring(len(keys), edges, colours, 4):
        raise AssertionError("published colouring failed the control graph")

    rejected = []
    left, right = edges[0]
    bad = list(colours)
    bad[right] = bad[left]
    if verify.valid_colouring(len(keys), edges, tuple(bad), 4):
        raise AssertionError("monochromatic-edge control was accepted")
    rejected.append("monochromatic edge")
    if verify.valid_colouring(len(keys), edges, colours[:-1], 4):
        raise AssertionError("truncated-colouring control was accepted")
    rejected.append("truncated colouring")
    if verify.valid_colouring(len(keys), edges, colours[:-1] + (4,), 4):
        raise AssertionError("out-of-range-colour control was accepted")
    rejected.append("out-of-range colour")

    result = {
        "status": "controls passed",
        "cross_representation_pair_checks": pair_checks,
        "entrywise_copy_point_set_checks": copy_checks,
        "closure_vertices": len(keys),
        "closure_edges": len(edges),
        "rejected_colour_controls": rejected,
        "floating_point_operations": 0,
    }
    (HERE / "CONTROLS.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
