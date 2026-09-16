#!/usr/bin/env python3
"""Adversarial controls for the independent H630 replacement review."""

import copy
import csv
import json

import independent_check as review


def rejects(action):
    try:
        action()
    except (review.ReviewFailure, ValueError, KeyError, IndexError):
        return True
    return False


def arithmetic_controls():
    root2 = (0, 1, 0, 0, 0, 0, 0, 0)
    root3 = (0, 0, 1, 0, 0, 0, 0, 0)
    root11 = (0, 0, 0, 0, 1, 0, 0, 0)
    review.need(review.tower_square(root2, review.NEW_PRIMES) == (2,) + (0,) * 7,
                "sqrt2 square control")
    review.need(review.tower_square(root3, review.NEW_PRIMES) == (3,) + (0,) * 7,
                "sqrt3 square control")
    review.need(review.tower_square(root11, review.NEW_PRIMES) == (11,) + (0,) * 7,
                "sqrt11 square control")
    product = review.tower_product(root2, root3, review.NEW_PRIMES)
    review.need(product == (0, 0, 0, 1, 0, 0, 0, 0),
                "sqrt6 product control")
    q = review.disk_point(1, 0)
    zero = (0,) * 16
    anchor = [0] * 16
    anchor[0], anchor[10] = 96, 32
    review.need(review.squared_distance(q, zero, review.NEW_PRIMES) == review.UNIT and
                review.squared_distance(q, tuple(anchor), review.NEW_PRIMES) == review.UNIT,
                "two-anchor disk control")
    return 5


def graph_controls():
    path = [{1}, {0, 2}, {1, 3}, {2}]
    result = review.graph_structure(range(4), path)
    review.need(result == {
        "components": 1,
        "largest_component": 4,
        "articulation_vertices": 2,
        "bridges": 3,
    }, "path structure control")
    cycle = [{1, 3}, {0, 2}, {1, 3}, {0, 2}]
    result = review.graph_structure(range(4), cycle)
    review.need(result == {
        "components": 1,
        "largest_component": 4,
        "articulation_vertices": 0,
        "bridges": 0,
    }, "cycle structure control")
    return 2


def main():
    baseline = review.verify()
    certificate = json.loads((review.TARGET / "certificate.json").read_text())
    edges = [tuple(map(int, row)) for row in
             csv.reader((review.TARGET / "edges.csv").open())]
    graph = review.adjacency(508, edges)
    retained = set(certificate["old_to_final"].values())
    reverse = {value: int(key) for key, value in certificate["old_to_final"].items()}
    _, moser_sets = review.enumerate_induced_moser_spindles(graph, retained, reverse)
    data = {
        "retained_labels": certificate["retained_labels"],
        "removed_labels": certificate["removed_labels"],
        "old_to_final": certificate["old_to_final"],
        "disk_to_final": certificate["disk_to_final"],
        "edge_split": certificate["edge_split"],
        "old_new_edges": certificate["old_new_edges"],
        "point_sha256": certificate["point_sha256"],
        "edge_sha256": certificate["edge_sha256"],
        "architecture_sha256": certificate["architecture_sha256"],
        "edges": edges,
        "moser_sets": moser_sets,
    }
    review.validate_certificate(certificate, data)

    corruptions = []
    altered = copy.deepcopy(certificate)
    word = list(altered["four_word"])
    word[edges[0][1]] = word[edges[0][0]]
    altered["four_word"] = "".join(word)
    corruptions.append(("monochromatic unit edge",
                        rejects(lambda: review.validate_certificate(altered, data))))

    altered = copy.deepcopy(certificate)
    altered["vertices"] = 507
    corruptions.append(("wrong physical order",
                        rejects(lambda: review.validate_certificate(altered, data))))

    altered = copy.deepcopy(certificate)
    altered["old_to_final"].pop(next(iter(altered["old_to_final"])))
    corruptions.append(("wrong retained map",
                        rejects(lambda: review.validate_certificate(altered, data))))

    altered = copy.deepcopy(certificate)
    altered["disk_to_final"][0]["m"] += 1
    corruptions.append(("wrong disk address",
                        rejects(lambda: review.validate_certificate(altered, data))))

    altered = copy.deepcopy(certificate)
    altered["edge_sha256"] = "0" * 64
    corruptions.append(("wrong edge identity",
                        rejects(lambda: review.validate_certificate(altered, data))))

    altered = copy.deepcopy(certificate)
    altered["moser_witness"][0] = altered["moser_witness"][1]
    corruptions.append(("colliding Moser roles",
                        rejects(lambda: review.validate_certificate(altered, data))))

    altered = copy.deepcopy(certificate)
    altered["status"] = "RECORD"
    corruptions.append(("false claim status",
                        rejects(lambda: review.validate_certificate(altered, data))))

    corruptions.append(("malformed coordinate row",
                        rejects(lambda: review.scaled_point([["0"] * 8]))))

    review.need(all(result for _, result in corruptions), "a corruption was accepted")
    report = {
        "status": "ALL INDEPENDENT REVIEW CONTROLS PASS",
        "baseline_status": baseline["status"],
        "corruptions_rejected": len(corruptions),
        "corruption_names": [name for name, _ in corruptions],
        "arithmetic_controls": arithmetic_controls(),
        "graph_structure_controls": graph_controls(),
    }
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
