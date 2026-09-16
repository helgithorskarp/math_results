#!/usr/bin/env python3
"""Adversarial controls for the independent EI19 first-lens review."""

import copy
import json
from fractions import Fraction

import independent_check as review


def rejects(action):
    try:
        action()
    except review.ReviewFailure:
        return True
    return False


def arithmetic_controls():
    fixtures = [
        Fraction(0), Fraction(1), Fraction(2), Fraction(2, 3),
        Fraction((review.SQRT_SCALE - 1) ** 2, review.SQRT_SCALE ** 2),
        Fraction(review.SQRT_SCALE ** 2 + 1, review.SQRT_SCALE ** 2),
        Fraction(10**100 + 12345, 10**99 + 7),
    ]
    for value in fixtures:
        lower = review.sqrt_lower(value)
        upper = review.sqrt_upper(value)
        review.need(lower * lower <= value <= upper * upper,
                    "square-root enclosure control")
        review.need(upper - lower <= Fraction(1, review.SQRT_SCALE),
                    "square-root width control")

    first = review.Interval(Fraction(-3, 7), Fraction(5, 11))
    second = review.Interval(Fraction(-2, 5), Fraction(7, 13))
    first_samples = (first.lo, (first.lo + first.hi) / 2, first.hi)
    second_samples = (second.lo, (second.lo + second.hi) / 2, second.hi)
    product = first * second
    difference = first - second
    squared = first.square()
    for left in first_samples:
        review.need(squared.lo <= left * left <= squared.hi,
                    "square containment control")
        for right in second_samples:
            review.need(product.lo <= left * right <= product.hi,
                        "product containment control")
            review.need(difference.lo <= left - right <= difference.hi,
                        "difference containment control")
    return len(fixtures), len(first_samples) * len(second_samples)


def main():
    baseline = review.verify()
    certificate = json.loads(review.SOURCE_CERT.read_text())
    _, centres, edges, radius, denominator = review.audit_source(certificate)
    points, _, _ = review.first_lens_closure(
        review.source_boxes(centres, radius, denominator)
    )
    word = (review.TARGET / "four_word.txt").read_text().strip()

    corruptions = []

    altered = copy.deepcopy(certificate)
    altered["schema"] = "wrong"
    corruptions.append(("source schema", rejects(lambda: review.audit_source(altered))))

    altered = copy.deepcopy(certificate)
    altered["centre_numerators"][0][0] = 1
    corruptions.append(("source anchor", rejects(lambda: review.audit_source(altered))))

    altered = copy.deepcopy(certificate)
    altered["edge_equations"].pop()
    corruptions.append(("source edge census", rejects(lambda: review.audit_source(altered))))

    characters = list(word)
    characters[1] = characters[0]
    corruptions.append((
        "unit-edge colour collision",
        rejects(lambda: review.validate_word(points, "".join(characters))),
    ))

    corruptions.append((
        "word alphabet",
        rejects(lambda: review.validate_word(points, "x" + word[1:])),
    ))

    _, deletion_word, _ = review.three_colour(edges, omitted=0)
    edge = next((item for item in edges if 0 not in item))
    characters = list(deletion_word)
    characters[edge[1]] = characters[edge[0]]
    corruptions.append((
        "vertex-deletion witness",
        rejects(lambda: review.check_graph_word("".join(characters), edges, omitted=0)),
    ))

    corruptions.append((
        "reversed interval",
        rejects(lambda: review.Interval(Fraction(1), Fraction(0))),
    ))
    corruptions.append((
        "negative square root",
        rejects(lambda: review.sqrt_lower(Fraction(-1))),
    ))

    review.need(all(result for _, result in corruptions), "a corruption was accepted")
    sqrt_fixtures, arithmetic_samples = arithmetic_controls()
    report = {
        "status": "ALL INDEPENDENT REVIEW CONTROLS PASS",
        "baseline_status": baseline["status"],
        "corruptions_rejected": len(corruptions),
        "corruption_names": [name for name, _ in corruptions],
        "sqrt_fixtures_checked": sqrt_fixtures,
        "arithmetic_sample_pairs_checked": arithmetic_samples,
    }
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
