#!/usr/bin/env python3
"""Negative controls for the independent T375--G79--G49 review."""

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
    source_dir = repository / review.SOURCE_NAME
    target_dir = repository / review.TARGET_NAME
    host, complement, union, _ = review.reconstruct_geometry(source_dir)
    complement_edges, _ = review.complete_edges(complement)
    union_edges, _ = review.complete_edges(union)
    original = review.read_json(target_dir / "certificate.json")
    review.validate_certificate(original, host, complement, union, complement_edges, union_edges)
    review.validate_moser(complement_edges)

    mutations = []

    def altered(path, value):
        certificate = copy.deepcopy(original)
        target = certificate
        for key in path[:-1]:
            target = target[key]
        target[path[-1]] = value
        return certificate

    mutations.append(("schema", altered(("schema",), "wrong-schema")))
    mutations.append(("complement count", altered(("complement_points",), 125)))
    mutations.append(("complement edge hash", altered(("complement_edge_sha256",), "0" * 64)))
    mutations.append(("union point hash", altered(("union_point_sha256",), "f" * 64)))
    bad_word = copy.deepcopy(original["complement_colour_word"])
    left, right = complement_edges[0]
    bad_word[right] = bad_word[left]
    mutations.append(("monochromatic word", altered(("complement_colour_word",), bad_word)))
    bad_map = copy.deepcopy(original["complement_to_union"])
    bad_map[3] = bad_map[4]
    mutations.append(("embedding", altered(("complement_to_union",), bad_map)))
    mutations.append(("cross contacts", altered(("extra_cross_edges",), original["extra_cross_edges"][:-1])))
    mutations.append(("field support", altered(("outside_native_field_indices",), original["outside_native_field_indices"][:-1])))
    mutations.append(("pin word", altered(("pins",), [0, 0, 0])))
    mutations.append(("record flag", altered(("record_candidate",), True)))

    for message, certificate in mutations:
        must_reject(
            lambda certificate=certificate: review.validate_certificate(
                certificate, host, complement, union, complement_edges, union_edges
            ),
            message,
        )

    invalid_roots = list(review.SIEVES[0][1])
    invalid_roots[0] += 1
    must_reject(lambda: review.sieve_weights(review.SIEVES[0][0], invalid_roots), "invalid sieve root")

    complete = set(complement_edges)
    witness_edges = [
        tuple(sorted((review.MOSER_VERTICES[left], review.MOSER_VERTICES[right])))
        for left, right in review.MOSER_PATTERN_EDGES
    ]
    for edge in witness_edges:
        reduced = sorted(complete - {edge})
        must_reject(lambda reduced=reduced: review.validate_moser(reduced), "deleted Moser edge")

    critical_deletions = 0
    for index in range(len(review.MOSER_PATTERN_EDGES)):
        reduced_pattern = (review.MOSER_PATTERN_EDGES[:index] +
                           review.MOSER_PATTERN_EDGES[index + 1:])
        if review.proper_colourings(7, reduced_pattern, 3) > 0:
            critical_deletions += 1
    review.need(critical_deletions == 11, "Moser edge-critical controls")

    return {
        "status": "PASS",
        "corruptions_rejected": len(mutations),
        "invalid_sieve_roots_rejected": 1,
        "moser_witness_deletions_rejected": len(witness_edges),
        "moser_edge_deletions_three_colourable": critical_deletions,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("repository", nargs="?", type=Path, default=HERE.parent)
    parser.add_argument("--check-expected", action="store_true")
    args = parser.parse_args()
    result = run(args.repository.resolve())
    if args.check_expected:
        review.need(result == review.read_json(HERE / "CONTROLS_EXPECTED.json"),
                    "expected control result")
    print(json.dumps(result, sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
