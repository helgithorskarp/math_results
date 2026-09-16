#!/usr/bin/env python3
"""Arithmetic, graph, and malformed-certificate controls for the review."""

import copy
import json
from fractions import Fraction as F
from itertools import product

import independent_check as review


def rejects(action):
    try:
        action()
    except (review.ReviewFailure, ValueError, KeyError, IndexError, TypeError):
        return True
    return False


def arithmetic_controls():
    basis = [tuple(F(index == coordinate) for coordinate in range(4))
             for index in range(4)]
    associativity = 0
    for first in basis:
        for second in basis:
            for third in basis:
                review.need(
                    review.multiply(review.multiply(first, second), third) ==
                    review.multiply(first, review.multiply(second, third)),
                    "basis associativity control",
                )
                associativity += 1

    norm_checks = 0
    for row in product(range(-2, 3), repeat=4):
        value = tuple(F(coefficient) for coefficient in row)
        product_norm = review.scale(2, review.multiply(value, review.conjugate(value)))
        review.need(product_norm == review.real_element(*review.norm_pair(value)),
                    "Gram norm control")
        norm_checks += 1

    residues, values = review.residue_theorem()
    review.need(len(residues) == len(values) == 10 and 0 not in values,
                "residue theorem control")
    review.need(review.multiply(review.ZETA,
                 review.multiply(review.ZETA,
                 review.multiply(review.ZETA,
                 review.multiply(review.ZETA, review.ZETA)))) == review.ONE,
                "fifth-root control")
    return {
        "basis_associativity": associativity,
        "gram_norm_checks": norm_checks,
        "residue_rows": len(residues),
        "root_relation": 1,
    }


def graph_controls():
    _, path = review.graph_structure(4, [(0, 1), (1, 2), (2, 3)])
    review.need(path["components"] == 1 and
                path["articulation_vertices"] == 2 and path["bridges"] == 3,
                "path control")
    _, cycle = review.graph_structure(5, [(0, 1), (1, 2), (2, 3),
                                          (3, 4), (0, 4)])
    review.need(cycle["components"] == 1 and
                cycle["articulation_vertices"] == 0 and cycle["bridges"] == 0,
                "cycle control")
    return 2


def main():
    review.check_pins()
    data = review.reconstruct()
    certificate = json.loads((review.TARGET / "certificate.json").read_text())
    review.validate_certificate(certificate, data)

    corruptions = []

    altered = copy.deepcopy(certificate)
    altered["architecture_sha256"] = "0" * 64
    corruptions.append(("architecture identity", rejects(
        lambda: review.validate_certificate(altered, data))))

    altered = copy.deepcopy(certificate)
    altered["vertices"] = 461
    corruptions.append(("physical order", rejects(
        lambda: review.validate_certificate(altered, data))))

    altered = copy.deepcopy(certificate)
    altered["generated_anchored_copies"] = 160
    corruptions.append(("generated-anchor count", rejects(
        lambda: review.validate_certificate(altered, data))))

    altered = copy.deepcopy(certificate)
    altered["terminal_unique_corner_index"] = 0
    corruptions.append(("terminal corner", rejects(
        lambda: review.validate_certificate(altered, data))))

    altered = copy.deepcopy(certificate)
    altered["outside_closed_overlay_points"] = 0
    corruptions.append(("overlay containment", rejects(
        lambda: review.validate_certificate(altered, data))))

    altered = copy.deepcopy(certificate)
    altered["point_sha256"] = "0" * 64
    corruptions.append(("point identity", rejects(
        lambda: review.validate_certificate(altered, data))))

    altered = copy.deepcopy(certificate)
    first, second = data["edges"][0]
    word = list(altered["four_word"])
    word[second] = word[first]
    altered["four_word"] = "".join(word)
    corruptions.append(("monochromatic unit edge", rejects(
        lambda: review.validate_certificate(altered, data))))

    altered = copy.deepcopy(certificate)
    altered["golden_source_constraints_violated"] = []
    corruptions.append(("concealed source failure", rejects(
        lambda: review.validate_certificate(altered, data))))

    altered = copy.deepcopy(certificate)
    altered["record_candidate"] = True
    corruptions.append(("false record status", rejects(
        lambda: review.validate_certificate(altered, data))))

    review.need(all(outcome for _, outcome in corruptions),
                "malformed certificate accepted")
    result = {
        "status": "ALL INDEPENDENT REVIEW CONTROLS PASS",
        "baseline_points": len(data["points"]),
        "baseline_edges": len(data["edges"]),
        "arithmetic_controls": arithmetic_controls(),
        "graph_controls": graph_controls(),
        "malformed_certificates_rejected": len(corruptions),
        "corruption_names": [name for name, _ in corruptions],
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
