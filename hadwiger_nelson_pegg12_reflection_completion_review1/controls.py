#!/usr/bin/env python3
"""Independent algebra, reflection, relation, and certificate controls."""

from itertools import combinations
import json

import verify


def require(condition, message):
    if not condition:
        raise ValueError(message)


def rejected(function):
    try:
        function()
    except (KeyError, TypeError, ValueError):
        return True
    return False


def direct_compatible(data, base_word, reflected_word, removed_edges=()):
    removed = set(removed_edges)
    values = tuple(map(int, base_word))
    for left, right in data["overlaps"]:
        if values[left] != reflected_word[right]:
            return False
    for physical, pairs in data["cross_by_edge"].items():
        if physical in removed:
            continue
        for left, right in pairs:
            if values[left] == reflected_word[right]:
                return False
    return True


def main():
    # Conjugate-norm inversion controls use elements not appearing as target
    # reflection denominators as well as the two quadratic generators.
    samples = (
        verify.ONE,
        verify.fadd(verify.rat(2), verify.R3),
        verify.fsub(verify.R11, verify.R3),
        verify.fadd(verify.fsub(verify.rat(1), verify.R11), verify.fscale(verify.R33, 2)),
    )
    for sample in samples:
        require(verify.fmul(sample, verify.finverse(sample)) == verify.ONE, "inverse control")
    require(verify.fmul(verify.R3, verify.R3) == verify.rat(3), "sqrt3 square")
    require(verify.fmul(verify.R11, verify.R11) == verify.rat(11), "sqrt11 square")
    require(verify.fmul(verify.R3, verify.R11) == verify.R33, "mixed radical")

    source = verify.source_points()
    source_edges = verify.complete_edges(source)
    reflection_controls = 0
    distance_controls = 0
    for left, right in combinations(range(12), 2):
        reflected = tuple(verify.reflect(point, source[left], source[right]) for point in source)
        for old, image in zip(source, reflected):
            require(verify.reflect(image, source[left], source[right]) == old, "reflection involution")
            reflection_controls += 1
        for first, second in combinations(range(12), 2):
            require(
                verify.squared_distance(reflected[first], reflected[second])
                == verify.squared_distance(source[first], source[second]),
                "distance preservation",
            )
            distance_controls += 1

    canonical = verify.canonical_words(12, source_edges, 4)
    labelled = verify.labelled_words(canonical)
    bitsets, all_bits = verify.colour_bitsets(labelled)
    data = verify.axis_data((0, 6), source_edges)
    relation_controls = 0
    for word in (canonical[0], "011022011203", "012021021301", canonical[-1]):
        bitset_indices = {
            index
            for index in range(len(labelled))
            if verify.compatible_bits(data, word, bitsets, all_bits) & (1 << index)
        }
        direct_indices = {
            index for index, reflected in enumerate(labelled) if direct_compatible(data, word, reflected)
        }
        require(bitset_indices == direct_indices, "bitset/direct relation mismatch")
        relation_controls += len(labelled)

    certificate = json.loads((verify.TARGET / "certificate.json").read_text())
    full_points, full_edges, _, _ = verify.reflected_union(tuple(map(tuple, certificate["full_axes"])))
    good = certificate["full_four_word"]
    verify.check_word(good, len(full_points), full_edges)
    malformed_rejected = 0
    require(rejected(lambda: verify.check_word(good[:-1], len(full_points), full_edges)), "short word accepted")
    malformed_rejected += 1
    bad = good[:7] + "4" + good[8:]
    require(rejected(lambda: verify.check_word(bad, len(full_points), full_edges)), "bad symbol accepted")
    malformed_rejected += 1
    first, second = full_edges[0]
    bad = list(good)
    bad[second] = bad[first]
    require(rejected(lambda: verify.check_word("".join(bad), len(full_points), full_edges)),
            "monochromatic edge accepted")
    malformed_rejected += 1

    result = {
        "all_controls_passed": True,
        "distance_preservation_controls": distance_controls,
        "field_inverse_controls": len(samples),
        "malformed_colour_words_rejected": malformed_rejected,
        "reflection_involution_controls": reflection_controls,
        "relation_entry_controls": relation_controls,
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
