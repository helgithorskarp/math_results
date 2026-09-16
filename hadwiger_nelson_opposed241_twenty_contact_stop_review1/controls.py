#!/usr/bin/env python3
"""Arithmetic, graph, and malformed-certificate controls for the review."""

import copy
import json

import independent_check as review


def rejects(action):
    try:
        action()
    except (review.ReviewFailure, ValueError, KeyError, IndexError, TypeError):
        return True
    return False


def arithmetic_controls():
    # Exhaustively check associativity on all triples of basis monomials.
    basis = [review.element(**{f"e{index}": 1}) for index in range(8)]
    checked = 0
    for first in basis:
        for second in basis:
            for third in basis:
                review.need(
                    review.multiply(review.multiply(first, second), third) ==
                    review.multiply(first, review.multiply(second, third)),
                    "basis associativity control",
                )
                checked += 1
    review.need(review.multiply(review.TROOT, review.TROOT) == review.T,
                "t square control")
    review.need(review.multiply(review.A, review.B) == review.C,
                "radical product control")
    return checked + 2


def graph_controls():
    _, path = review.graph_structure(4, [(0, 1), (1, 2), (2, 3)])
    review.need(path["components"] == 1 and
                path["articulation_vertices"] == 2 and path["bridges"] == 3,
                "path control")
    _, cycle = review.graph_structure(4, [(0, 1), (1, 2), (2, 3), (0, 3)])
    review.need(cycle["components"] == 1 and
                cycle["articulation_vertices"] == 0 and cycle["bridges"] == 0,
                "cycle control")
    cross = review.cross_structure([(0, 3), (1, 3), (2, 4)], {0, 1, 2}, {3, 4})
    review.need(cross["components"] == 2 and
                cross["length_two_paths"] == 1 and
                cross["isolated_edges"] == 1 and
                cross["maximum_matching"] == 2,
                "cross forest control")
    return 3


def main():
    review.check_pins()
    data = review.reconstruct()
    certificate = json.loads((review.TARGET / "certificate.json").read_text())
    review.validate_submitted_certificate(certificate, data)

    corruptions = []

    altered = copy.deepcopy(certificate)
    altered["schema"] = "wrong"
    corruptions.append(("schema", rejects(
        lambda: review.validate_submitted_certificate(altered, data))))

    altered = copy.deepcopy(certificate)
    altered["rotation_contact_source_indices"] = [45, 64]
    corruptions.append(("rotation indices", rejects(
        lambda: review.validate_submitted_certificate(altered, data))))

    altered = copy.deepcopy(certificate)
    altered["rotation_branch"] = "negative_t"
    corruptions.append(("rotation branch", rejects(
        lambda: review.validate_submitted_certificate(altered, data))))

    altered = copy.deepcopy(certificate)
    altered["cross_edges"][0][0] += 1
    corruptions.append(("cross contact", rejects(
        lambda: review.validate_submitted_certificate(altered, data))))

    altered = copy.deepcopy(certificate)
    altered["point_sha256"] = "0" * 64
    corruptions.append(("point hash", rejects(
        lambda: review.validate_submitted_certificate(altered, data))))

    altered = copy.deepcopy(certificate)
    altered["edge_sha256"] = "0" * 64
    corruptions.append(("edge hash", rejects(
        lambda: review.validate_submitted_certificate(altered, data))))

    altered = copy.deepcopy(certificate)
    first, second = data["edges"][0]
    word = list(altered["proper4"])
    word[second] = word[first]
    altered["proper4"] = "".join(word)
    corruptions.append(("monochromatic edge", rejects(
        lambda: review.validate_submitted_certificate(altered, data))))

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
