#!/usr/bin/env python3
"""Independent exact review of the frozen H516 coupled-edge exchange.

This checker imports neither target executable.  It reconstructs the archived
H632 coordinate table from four pinned inputs, decides every squared distance
in Q(sqrt(3),sqrt(5),sqrt(11)), replays the geometric selector, checks both the
published and a freshly found four-colouring, and verifies the Moser lower
bound inside the retained 506-point core.
"""

import argparse
import hashlib
import itertools
import json
from fractions import Fraction
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
TARGET = ROOT / "hadwiger_nelson_h516_coupled_edge_exchange_stop"
DENOMINATOR = 96
RADICANDS = (1, 3, 5, 15, 11, 33, 55, 165)
REMOVED = (102, 109, 293, 296, 299, 302, 305, 308, 569, 578)
ADDED = (399, 576)

INPUTS = {
    "hadwiger_nelson_h516_degree4_surgeries/SOURCE.json":
        "3f60fe94c7cd3d9c70b7cc52124fa185d4b46d54bb59b21bca0c45d2b181fd51",
    "hadwiger_nelson_heule510_completion_frontier/fresh_candidates.json":
        "89345930e1bea184ce2457b0e14a015bcd9a2901cfc609a6468cf050234a8317",
    "hadwiger_nelson_heule632_minimize/certificate.json":
        "3a22660e40329c0aef34e108b91747f529adb046cf687df5b05b3531ca17e35b",
    "hadwiger_nelson_parts509_heule_union_minimum/certificate_H510.json":
        "bc8e0f5f5ec7fa5f2376cc77ba0e65f6023b340cf48990370d5eda575d30ae79",
}

TARGET_HASHES = {
    "ARCHITECTURE.json": "cdaa97ac81cf3842fbf762f0a392a7809b28df69086c0aa23950e9445b468d81",
    "PROVENANCE.json": "24c942961aad8990e8faa047528fe632afc4dac829023fd94feca88d74007700",
    "README.md": "0ef4a121753361c6671ea779ea685b8d9ef77329d4598f8ee699fa9fe87d3749",
    "certificate.json": "ad0d6ed39a1c40d0b3233025b907709947412ad4fc6159fb1d443ee0b38da986",
    "edges.csv": "c6b4b06b5883d1d8d94693413ff3314148130f3255044f6ecee707ab0fc5d646",
    "h632.csv": "5bc6df88afed13c6ccff2154c749fc1f5e74a9892b6b13f79ab08bbc49cd2e17",
    "points.csv": "9a68a448527fafd9ea02b31eee6f2b97e2f0430595b29984aa5c79f6ce97c121",
    "reproduce.py": "b4c54106aef03486ffba7e4fabcd9a35f46f411c9dad80f9c997f8a29e7b71df",
    "verify.py": "40ee6f68d1142ca8b096a7bab1ac60e77f0d4912d8911fcb6bf4c1efc4f5484a",
}


class ReviewFailure(RuntimeError):
    pass


def need(condition, message):
    if not condition:
        raise ReviewFailure(message)


def sha256_bytes(blob):
    return hashlib.sha256(blob).hexdigest()


def sha256_path(path):
    return sha256_bytes(path.read_bytes())


def read_json(path):
    return json.loads(path.read_text())


def scaled_axis(axis):
    values = [DENOMINATOR * Fraction(value) for value in axis]
    need(all(value.denominator == 1 for value in values), "coordinate denominator")
    return tuple(int(value) for value in values)


def scaled_point(point):
    need(len(point) == 2 and all(len(axis) == 8 for axis in point), "coordinate shape")
    return scaled_axis(point[0]) + scaled_axis(point[1])


def parse_csv_points(path):
    rows = [tuple(map(int, line.split(","))) for line in path.read_text().splitlines()]
    need(all(len(row) == 16 for row in rows), "CSV coordinate shape")
    return rows


def reconstruct_h632():
    loaded = {}
    for relative, expected in INPUTS.items():
        path = ROOT / relative
        need(sha256_path(path) == expected, "pinned input bytes: " + relative)
        loaded[relative] = read_json(path)

    old = loaded["hadwiger_nelson_parts509_heule_union_minimum/certificate_H510.json"]
    fresh = loaded["hadwiger_nelson_heule510_completion_frontier/fresh_candidates.json"]
    old_labels = [
        label for label in sorted(map(int, old["coordinates"]))
        if "510" in old["provenance"][label]
    ]
    rows = [scaled_point(old["coordinates"][str(label)]) for label in old_labels]
    rows.extend(scaled_point(item["coordinates"]) for item in fresh)
    need(len(old_labels) == 510 and len(fresh) == 122 and len(rows) == 632,
         "H632 source census")
    need(len(set(rows)) == 632, "H632 physical collisions")
    return rows, loaded


def field_square(axis):
    """Square in the tensor basis indexed by subsets of (3,5,11)."""
    result = [0] * 8
    for left, a in enumerate(axis):
        if a == 0:
            continue
        for right, b in enumerate(axis):
            if b:
                result[left ^ right] += a * b * RADICANDS[left & right]
    return result


def unit_distance(left, right):
    dx = tuple(a - b for a, b in zip(left[:8], right[:8]))
    dy = tuple(a - b for a, b in zip(left[8:], right[8:]))
    value = tuple(a + b for a, b in zip(field_square(dx), field_square(dy)))
    return value == (DENOMINATOR * DENOMINATOR, 0, 0, 0, 0, 0, 0, 0)


def exact_squared_distance(left, right):
    dx = tuple(a - b for a, b in zip(left[:8], right[:8]))
    dy = tuple(a - b for a, b in zip(left[8:], right[8:]))
    return tuple(a + b for a, b in zip(field_square(dx), field_square(dy)))


def complete_edges(points):
    return [
        (left, right)
        for left, right in itertools.combinations(range(len(points)), 2)
        if unit_distance(points[left], points[right])
    ]


def edge_bytes(edges):
    return "".join(f"{left},{right}\n" for left, right in edges).encode()


def adjacency(order, edges):
    graph = [set() for _ in range(order)]
    for left, right in edges:
        graph[left].add(right)
        graph[right].add(left)
    return graph


def validate_word(word, order, edges):
    need(isinstance(word, str) and len(word) == order, "colour word length")
    need(set(word) <= set("0123"), "colour word alphabet")
    need(all(word[left] != word[right] for left, right in edges), "monochromatic edge")


def fresh_four_colouring(order, edges):
    """Deterministic DSATUR search; no target word or SAT solver is used."""
    graph = adjacency(order, edges)
    degrees = list(map(len, graph))
    colours = [-1] * order
    masks = [0] * order
    start = max(range(order), key=lambda vertex: (degrees[vertex], vertex))
    colours[start] = 0
    for other in graph[start]:
        masks[other] |= 1
    nodes = 0
    backtracks = 0

    def search(done, maximum):
        nonlocal nodes, backtracks
        nodes += 1
        if done == order:
            return True
        vertex = max(
            (item for item in range(order) if colours[item] < 0),
            key=lambda item: (masks[item].bit_count(), degrees[item], item),
        )
        available = [
            colour for colour in range(min(3, maximum + 1) + 1)
            if not masks[vertex] & (1 << colour)
        ]
        available.sort(key=lambda colour: (
            sum(colours[other] < 0 and not masks[other] & (1 << colour)
                for other in graph[vertex]),
            colour,
        ))
        for colour in available:
            bit = 1 << colour
            colours[vertex] = colour
            changed = []
            conflict = False
            for other in graph[vertex]:
                if colours[other] < 0 and not masks[other] & bit:
                    masks[other] |= bit
                    changed.append(other)
                    if masks[other] == 15:
                        conflict = True
            if not conflict and search(done + 1, max(maximum, colour)):
                return True
            for other in changed:
                masks[other] ^= bit
            colours[vertex] = -1
            backtracks += 1
        return False

    need(search(1, 0), "fresh four-colour search")
    word = "".join(map(str, colours))
    validate_word(word, order, edges)
    need(set(word) == set("0123"), "fresh word uses four colours")
    return word, nodes, backtracks, start


def check_moser(witness, edges):
    need(len(witness) == len(set(witness)) == 7, "Moser witness vertices")
    origin, tip, a, b, second, d, e = witness
    required = {
        tuple(sorted(pair)) for pair in (
            (origin, a), (origin, b), (tip, a), (tip, b), (a, b),
            (origin, d), (origin, e), (second, d), (second, e), (d, e),
            (tip, second),
        )
    }
    need(required <= set(edges), "Moser witness edges")
    return sorted(required)


def construct_report():
    for name, expected in TARGET_HASHES.items():
        need(sha256_path(TARGET / name) == expected, "target bytes: " + name)

    h632, inputs = reconstruct_h632()
    need(tuple(parse_csv_points(TARGET / "h632.csv")) == tuple(h632),
         "archived H632 reconstruction")
    h632_edges = complete_edges(h632)
    need(len(h632_edges) == 3112, "H632 complete edge census")
    h632_graph = adjacency(632, h632_edges)

    source = inputs["hadwiger_nelson_h516_degree4_surgeries/SOURCE.json"]
    base = set(source["labels"])
    host = set(inputs["hadwiger_nelson_heule632_minimize/certificate.json"]["retained"])
    need(len(base) == 516 and len(host) == 560 and base <= host, "nested source sets")
    need([h632[label] for label in source["labels"]] ==
         [tuple(axis[0] + axis[1]) for axis in source["coordinates"]],
         "H516 coordinates")
    base_edges = [edge for edge in h632_edges if edge[0] in base and edge[1] in base]
    need(base_edges == [tuple(edge) for edge in source["edges"]] and len(base_edges) == 2538,
         "H516 complete edge graph")
    degree_four = sorted(label for label in base if len(h632_graph[label] & base) == 4)
    need(degree_four == list(REMOVED) == source["degree4"], "all degree-four vertices")
    need(exact_squared_distance(h632[293], h632[299]) ==
         (9 * DENOMINATOR * DENOMINATOR, 0, 0, 0, 0, 0, 0, 0),
         "distributed-deletion distance")

    retained = base - set(REMOVED)
    eligible = [
        (left, right) for left, right in h632_edges
        if left not in host and right not in host
        and len(h632_graph[left] & retained) >= 3
        and len(h632_graph[right] & retained) >= 3
    ]
    need(eligible and eligible[0] == ADDED, "lexicographically first selected pair")
    labels = sorted(retained | set(ADDED))
    need(len(labels) == 508 and not set(ADDED) & host, "final physical support")
    points = [h632[label] for label in labels]
    need(tuple(parse_csv_points(TARGET / "points.csv")) == tuple(points), "final point stream")
    final_edges = complete_edges(points)
    supplied_edges = [tuple(map(int, line.split(",")))
                      for line in (TARGET / "edges.csv").read_text().splitlines()]
    need(final_edges == supplied_edges and len(final_edges) == 2506, "complete final edge stream")

    old_indices = {index for index, label in enumerate(labels) if label in retained}
    added_indices = {label: labels.index(label) for label in ADDED}
    old_old = [(u, v) for u, v in final_edges if u in old_indices and v in old_indices]
    old_new = [(u, v) for u, v in final_edges if (u in old_indices) != (v in old_indices)]
    new_new = [(u, v) for u, v in final_edges if u not in old_indices and v not in old_indices]
    need((len(old_old), len(old_new), len(new_new)) == (2498, 7, 1), "edge split")
    contacts = {
        str(label): sorted(h632_graph[label] & retained) for label in ADDED
    }
    need(contacts == {"399": [346, 392, 421, 441], "576": [393, 421, 431]},
         "added-point contacts")

    certificate = read_json(TARGET / "certificate.json")
    need(certificate["labels"] == labels, "certificate label map")
    validate_word(certificate["four_word"], 508, final_edges)
    moser_edges = check_moser(certificate["moser_witness"], final_edges)
    moser_labels = [labels[index] for index in certificate["moser_witness"]]
    need(set(moser_labels) <= retained and not set(moser_labels) & set(ADDED),
         "Moser witness lies in H506")

    fresh_word, nodes, backtracks, start = fresh_four_colouring(508, final_edges)
    need(fresh_word != certificate["four_word"], "fresh word independent of supplied word")

    supplied_by_label = dict(zip(labels, certificate["four_word"]))
    nested = []
    for additions in ((), (399,), (576,), ADDED):
        support = sorted(retained | set(additions))
        support_set = set(support)
        edges = [(u, v) for u, v in h632_edges if u in support_set and v in support_set]
        need(all(supplied_by_label[u] != supplied_by_label[v] for u, v in edges),
             "nested four-colouring")
        need(set(moser_labels) <= support_set, "nested Moser lower bound")
        nested.append({"additions": list(additions), "vertices": len(support), "unit_edges": len(edges)})
    need(nested == [
        {"additions": [], "vertices": 506, "unit_edges": 2498},
        {"additions": [399], "vertices": 507, "unit_edges": 2502},
        {"additions": [576], "vertices": 507, "unit_edges": 2501},
        {"additions": [399, 576], "vertices": 508, "unit_edges": 2506},
    ], "nested support census")

    # Corruption controls exercise the two principal certificate boundaries.
    bad_word = list(certificate["four_word"])
    bad_word[final_edges[0][1]] = bad_word[final_edges[0][0]]
    try:
        validate_word("".join(bad_word), 508, final_edges)
    except ReviewFailure:
        word_control = True
    else:
        word_control = False
    need(word_control, "monochromatic-word control")
    missing_edge_control = final_edges[:-1] != supplied_edges
    need(missing_edge_control, "edge-omission control")

    return {
        "status": "ACCEPT_AND_STRENGTHEN_EXACT_FOUR",
        "reviewed_target_commit": "bcb699cc9890480c93c24716155a7fb5f4b5cea1",
        "h632_vertices": 632,
        "h632_pairs_checked": 632 * 631 // 2,
        "h632_unit_edges": len(h632_edges),
        "h516_vertices": len(base),
        "h516_unit_edges": len(base_edges),
        "degree_four_vertices": degree_four,
        "eligible_external_pairs": len(eligible),
        "eligible_external_pairs_first_five": [list(edge) for edge in eligible[:5]],
        "selected_pair": list(ADDED),
        "selected_pair_outside_h560": True,
        "added_indices": {str(label): index for label, index in added_indices.items()},
        "new_old_contacts": contacts,
        "final_vertices": len(points),
        "final_pairs_checked": len(points) * (len(points) - 1) // 2,
        "final_unit_edges": len(final_edges),
        "old_old_edges": len(old_old),
        "old_new_edges": len(old_new),
        "new_new_edges": len(new_new),
        "point_sha256": sha256_path(TARGET / "points.csv"),
        "edge_sha256": sha256_bytes(edge_bytes(final_edges)),
        "supplied_four_word_sha256": sha256_bytes(certificate["four_word"].encode()),
        "fresh_four_word_sha256": sha256_bytes(fresh_word.encode()),
        "fresh_four_search_nodes": nodes,
        "fresh_four_search_backtracks": backtracks,
        "fresh_four_search_start": start,
        "moser_witness_indices": certificate["moser_witness"],
        "moser_witness_labels": moser_labels,
        "moser_witness_edges": [list(edge) for edge in moser_edges],
        "moser_entirely_in_retained_h506": True,
        "nested_exact_four_graphs": nested,
        "controls_rejected": ["monochromatic supplied word", "omitted final edge"],
        "record_candidate": False,
        "scope": "one frozen physical two-point exchange; no family closure",
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--check-expected", action="store_true")
    arguments = parser.parse_args()
    report = construct_report()
    if arguments.check_expected:
        need(report == read_json(HERE / "EXPECTED.json"), "EXPECTED.json mismatch")
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
