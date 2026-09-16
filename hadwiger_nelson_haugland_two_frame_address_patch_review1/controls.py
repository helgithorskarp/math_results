#!/usr/bin/env python3
"""Negative and sensitivity controls for the independent two-frame review."""

import argparse
import copy
import json
from pathlib import Path

import independent_check as review


HERE = Path(__file__).resolve().parent


def must_reject(function, message):
    try:
        function()
    except review.ReviewFailure:
        return
    raise review.ReviewFailure("control was accepted: " + message)


def run(repository: Path):
    target = repository / review.TARGET_NAME
    certificate = json.loads((target / "certificate.json").read_text())
    host, normalized, patch, _, points = review.construct_support()
    edges, _, _ = review.complete_edges(points)
    review.validate_certificate(certificate, points, edges)

    corruptions = []

    def changed(key, value):
        result = copy.deepcopy(certificate)
        result[key] = value
        return result

    corruptions.append(("version", changed("version", 2)))
    corruptions.append(("anchors", changed("anchors", [230, 197])))
    corruptions.append(("coordinate hash", changed("coordinate_sha256", "0" * 64)))
    corruptions.append(("edge hash", changed("edge_sha256", "f" * 64)))
    bad_word = list(certificate["four_word"])
    left, right = edges[0]
    bad_word[right] = bad_word[left]
    corruptions.append(("monochromatic word", changed("four_word", "".join(bad_word))))
    corruptions.append(("short word", changed("four_word", certificate["four_word"][:-1])))
    for message, bad in corruptions:
        must_reject(lambda bad=bad: review.validate_certificate(bad, points, edges), message)

    bad_sieves = (
        (1428, 1274, 336),
        (1429, 1275, 336),
        (1429, 1274, 337),
    )
    for parameters in bad_sieves:
        must_reject(lambda parameters=parameters: review.validate_sieve(*parameters),
                    "invalid finite-field image")

    source_edges = set(review.source_pattern_edges())
    deletion_counts = []
    for offset, step in ((0, 1), (7, 2), (14, 3)):
        cycle = {
            tuple(sorted((offset + index, offset + (index + step) % 7)))
            for index in range(7)
        }
        deletion_counts.append(review.normalized_triangle_colourings(tuple(sorted(source_edges - cycle))))
    review.need(deletion_counts == [84, 84, 84], "source colouring sensitivity")

    bypass_edges = sorted(set(edges) | {(0, 231)})
    bypass_articulations, _ = review.articulation_data(462, bypass_edges)
    review.need(461 not in bypass_articulations, "articulation bypass control")
    single_contact = sorted(set(edges) - (set(review.EXPECTED_CROSS) - {review.EXPECTED_CROSS[0]}))
    _, single_bridges = review.articulation_data(462, single_contact)
    review.need(list(review.EXPECTED_CROSS[0]) in [list(edge) for edge in single_bridges],
                "single-contact bridge control")

    return {
        "status": "PASS",
        "certificate_corruptions_rejected": len(corruptions),
        "invalid_sieves_rejected": len(bad_sieves),
        "source_cycle_deletion_colouring_counts": deletion_counts,
        "articulation_bypass_detected": True,
        "single_contact_bridge_detected": True,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("repository", nargs="?", type=Path, default=HERE.parent)
    parser.add_argument("--check-expected", action="store_true")
    args = parser.parse_args()
    result = run(args.repository.resolve())
    if args.check_expected:
        review.need(result == json.loads((HERE / "CONTROLS_EXPECTED.json").read_text()),
                    "expected control result")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
