#!/usr/bin/env python3
"""Independent controls for the E477 translation-union review."""

from copy import deepcopy
from itertools import combinations
from json import dumps
from math import gcd

import verify as V


RADICANDS = (1, 3, 11, 33)
RINDEX = {value: index for index, value in enumerate(RADICANDS)}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def multiply(left, right):
    output = [0, 0, 0, 0]
    for i, first in enumerate(left):
        for j, second in enumerate(right):
            common = gcd(RADICANDS[i], RADICANDS[j])
            radicand = RADICANDS[i] * RADICANDS[j] // (common * common)
            output[RINDEX[radicand]] += common * first * second
    return tuple(output)


def generic_unit(left, right):
    a, b, c, d = V.sub(left, right)
    x = (0, a, b, 0)
    y = (c, 0, 0, d)
    norm = tuple(first + second for first, second in zip(multiply(x, x), multiply(y, y)))
    return norm == (1296, 0, 0, 0)


def rejected(certificate, data):
    try:
        V.validate(certificate, data)
    except (ValueError, KeyError, TypeError):
        return True
    return False


def main():
    data = V.reconstruct()
    baseline = V.validate(deepcopy(data["target_certificate"]), data)
    source_generic_agreements = 0
    for left, right in combinations(data["source_rows"], 2):
        require(V.unit(left, right) == generic_unit(left, right),
                "source direct/generic unit disagreement")
        source_generic_agreements += 1
    union_generic_agreements = 0
    for left, right in combinations(data["physical_rows"], 2):
        require(V.unit(left, right) == generic_unit(left, right),
                "union direct/generic unit disagreement")
        union_generic_agreements += 1

    # On a hand-checkable one-dimensional toy set, difference multiplicity and
    # literal translated-set intersection agree for every nonzero candidate.
    toy = frozenset((value, 0, 0, 0) for value in (0, 1, 3, 4))
    toy_candidates = {V.sub(right, left) for left in toy for right in toy if left != right}
    toy_controls = 0
    for translation in toy_candidates:
        multiplicity = sum(V.sub(right, left) == translation for left in toy for right in toy)
        intersection = sum(V.add(left, translation) in toy for left in toy)
        require(multiplicity == intersection, "translation autocorrelation identity")
        toy_controls += 1

    corruptions = []
    wrong = deepcopy(data["target_certificate"])
    wrong["selected_translation"][0] += 1
    corruptions.append(wrong)
    wrong = deepcopy(data["target_certificate"])
    wrong["translation_overlap_maximum"] -= 1
    corruptions.append(wrong)
    wrong = deepcopy(data["target_certificate"])
    left, right = data["edges"][0]
    word = list(wrong["four_colouring"])
    word[right] = word[left]
    wrong["four_colouring"] = "".join(word)
    corruptions.append(wrong)
    wrong = deepcopy(data["target_certificate"])
    wrong["point_sha256"] = "0" * 64
    corruptions.append(wrong)
    wrong = deepcopy(data["target_certificate"])
    wrong["moser_source_labels"][0] = wrong["moser_source_labels"][1]
    corruptions.append(wrong)
    wrong = deepcopy(data["target_certificate"])
    wrong["input_sha256"]["certificate.json"] = "0" * 64
    corruptions.append(wrong)
    require(all(rejected(certificate, data) for certificate in corruptions),
            "accepted corrupted certificate")

    print(dumps({
        "all_controls_passed": True,
        "baseline_verdict": baseline["verdict"],
        "corruptions_rejected": len(corruptions),
        "source_direct_generic_pair_agreements": source_generic_agreements,
        "translation_autocorrelation_toy_controls": toy_controls,
        "union_direct_generic_pair_agreements": union_generic_agreements,
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
