#!/usr/bin/env python3
"""Independent small census and deliberate certificate-corruption controls."""
import argparse
import json
from collections import Counter

from census import five_classes, labelled_downsets, partition, profile_canonical
from verify import (EXCEPTION, TWELVE_PARTITION, characteristic_polynomial,
                    check_partition, decode, exact_ldl_psd, exceptional_matrix)


def antichain_downsets(n):
    """Include/exclude recursion on maximal antichains, not ideal sections."""
    total = 1 << n
    comparable = [sum(1 << b for b in range(total)
                      if a & b in (a, b)) for a in range(total)]
    closures = [sum(1 << b for b in range(total) if a & b == b)
                for a in range(total)]

    def visit(available, downclosure):
        if not available:
            yield downclosure
            return
        low = available & -available
        a = low.bit_length() - 1
        yield from visit(available ^ low, downclosure)
        yield from visit(available & ~comparable[a], downclosure | closures[a])

    return visit((1 << total) - 1, 0)


def expect_rejection(call):
    try:
        call()
    except (AssertionError, ValueError):
        return
    raise AssertionError("corrupted certificate was accepted")


def run(six_expected=None):
    for n in range(6):
        antichains = list(antichain_downsets(n))
        if len(set(antichains)) != len(antichains):
            raise AssertionError("duplicate antichain downclosures")
        if set(antichains) != set(labelled_downsets(n)):
            raise AssertionError("entry-level census methods disagree")
        # Compare the two canonicalization mechanisms on every labeled
        # five-element family, not just the aggregate number of classes.
        reference = five_classes(n)
        reference_orbit = {}
        from itertools import permutations
        for family, orbit in reference:
            sets = decode(family, n)
            images = set()
            for p in permutations(range(n)):
                image = sum(1 << sum(1 << p[i] for i in range(n) if a >> i & 1)
                            for a in sets)
                images.add(image)
            if len(images) != orbit:
                raise AssertionError("reference orbit reconstruction failed")
            keys = {profile_canonical(image, n) for image in images}
            if len(keys) != 1 or next(iter(keys))[1] != orbit:
                raise AssertionError("profile canonicalization is not invariant")
            reference_orbit[next(iter(keys))[0]] = orbit
        if len(reference_orbit) != len(reference):
            raise AssertionError("distinct classes merged by profiles")
        for family, _ in reference:
            bins, _ = partition(family, n)
            if bins is None:
                raise AssertionError("small partition absent")
            check_partition(family, bins, n)
    check_partition(EXCEPTION, TWELVE_PARTITION, 6, target=12)
    bad_bins = [list(block) for block in TWELVE_PARTITION]
    bad_bins[0].append(bad_bins[1][0])
    expect_rejection(lambda: check_partition(EXCEPTION, bad_bins, 6, target=12))
    expect_rejection(lambda: check_partition(1 << 3, [[3]], 2))
    _, w, _ = exceptional_matrix()
    expect_rejection(lambda: exact_ldl_psd([[-1]]))
    expect_rejection(lambda: exact_ldl_psd([[0, 1], [1, 0]]))
    if exact_ldl_psd([[1, 1], [1, 1]]) != 1:
        raise AssertionError("singular PSD control failed")
    corrupted = [row[:] for row in w]
    corrupted[0][0] = -1
    expect_rejection(lambda: exact_ldl_psd(corrupted))
    for matrix, psd in [([[1, 1], [1, 1]], True), ([[0, 1], [1, 0]], False)]:
        coefficients = characteristic_polynomial(matrix)
        if all((-1) ** i * c >= 0 for i, c in enumerate(coefficients)) != psd:
            raise AssertionError("characteristic-polynomial sign control failed")
    print("PASS: antichain/section equality through n=5; entry-level orbit checks;")
    print("all small partitions; exceptional 12-partition; corrupted certificate rejection.")
    if six_expected:
        with open(six_expected, encoding="utf-8") as handle:
            expected = json.load(handle)
        count = total = 0
        histogram = Counter()
        for family in antichain_downsets(6):
            count += 1
            total += family
            histogram[family.bit_count()] += 1
        if count != expected["labelled_downsets"]:
            raise AssertionError("six-element independent count differs")
        if total != expected["labeled_family_mask_sum"]:
            raise AssertionError("six-element independent mask sum differs")
        if {str(k): v for k, v in histogram.items()} != expected["labeled_size_histogram"]:
            raise AssertionError("six-element independent size distribution differs")
        print(f"PASS: independent antichain stream of all {count} labeled six-element downsets;")
        print("exact full size distribution and family-mask sum match orbit reconstruction.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--six-antichains", metavar="RESULTS_JSON",
                        help="also stream all 7,828,354 labeled six-element downsets")
    run(parser.parse_args().six_antichains)
