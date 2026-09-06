#!/usr/bin/env python3
"""Independent exact review of the whole H514 deletion closure.

The checker imports no executable code from the reviewed contribution.  It
reconstructs H514 over Q(sqrt(3),sqrt(5),sqrt(11)), independently decodes the
positive-colouring library from raw certificate recipes, checks every retained
unit-edge inequality, and exhausts all 2^11 subsets of the free vertices.
"""

from __future__ import annotations

import argparse
from collections import Counter
from fractions import Fraction
from hashlib import sha256
from itertools import combinations
import json
import os
from pathlib import Path
import sys


DENOMINATOR = 96
RADICANDS = (3, 5, 11)
EXPECTED_CENTRES = [170, 436, 1239, 1527]
EXPECTED_EDGE_HASH = "6e174788901829d3d2aa3089e26e296372f1d33141666e2cb2b5624d5078a89e"
EXPECTED_FREE = [152, 214, 344, 433, 439, 497, 500, 510, 511, 512, 513]
EXPECTED_EXCEPTIONS = [
    [152, 214, 433, 497, 500, 512],
    [152, 214, 433, 497, 512, 513],
    [152, 433, 497, 500, 510, 512],
    [152, 433, 497, 510, 512, 513],
]


class ReviewFailure(RuntimeError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ReviewFailure(message)


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def file_record(path: Path) -> dict[str, int | str]:
    raw = path.read_bytes()
    return {"bytes": len(raw), "sha256": sha256(raw).hexdigest()}


def atomic_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".tmp")
    with temporary.open("w", encoding="utf-8") as stream:
        json.dump(value, stream, indent=2, sort_keys=True)
        stream.write("\n")
        stream.flush()
        os.fsync(stream.fileno())
    os.replace(temporary, path)


def verify_sha256s(directory: Path) -> dict[str, dict[str, int | str]]:
    records = {}
    lines = (directory / "SHA256SUMS").read_text(encoding="ascii").splitlines()
    for line in lines:
        expected, name = line.split(maxsplit=1)
        record = file_record(directory / name)
        require(record["sha256"] == expected, "source hash: " + name)
        records[name] = record
    return records


def verify_manifest(repository: Path, path: Path) -> int:
    manifest = load(path)
    for name, expected in manifest.items():
        require(file_record(repository / name)["sha256"] == expected,
                "manifest input hash: " + name)
    return len(manifest)


def scaled_axis(raw: list[object]) -> tuple[int, ...]:
    require(isinstance(raw, list) and len(raw) == 8, "radical axis width")
    values = [Fraction(value) * DENOMINATOR for value in raw]
    require(all(value.denominator == 1 for value in values),
            "coordinate denominator divides 96")
    return tuple(int(value) for value in values)


def scaled_point(raw: list[list[object]]) -> tuple[tuple[int, ...], tuple[int, ...]]:
    require(isinstance(raw, list) and len(raw) == 2, "point has two axes")
    return scaled_axis(raw[0]), scaled_axis(raw[1])


def ring_product(left: tuple[int, ...], right: tuple[int, ...]) -> tuple[int, ...]:
    """Multiply coefficient vectors in Q(sqrt(3),sqrt(5),sqrt(11))."""
    require(len(left) == len(right) == 8, "radical coefficient width")
    result = [0] * 8
    for left_mask, left_value in enumerate(left):
        for right_mask, right_value in enumerate(right):
            square_factor = 1
            overlap = left_mask & right_mask
            for bit, radicand in enumerate(RADICANDS):
                if overlap & (1 << bit):
                    square_factor *= radicand
            result[left_mask ^ right_mask] += left_value * right_value * square_factor
    return tuple(result)


def exact_squared_distance(left, right) -> tuple[int, ...]:
    differences = [
        tuple(a - b for a, b in zip(left[axis], right[axis]))
        for axis in (0, 1)
    ]
    squares = [ring_product(delta, delta) for delta in differences]
    return tuple(a + b for a, b in zip(squares[0], squares[1]))


def reconstruct_h514(repository: Path):
    old = load(repository / "hadwiger_nelson_parts509_heule_union_minimum/certificate_H510.json")
    labels = [index for index, provenance in enumerate(old["provenance"]) if "510" in provenance]
    require(len(labels) == 510 and labels == sorted(set(labels)), "exact increasing H510 labels")
    base = [scaled_point(old["coordinates"][str(label)]) for label in labels]
    large = {
        vertex for vertex, point in enumerate(base)
        if all(point[axis][basis] == 0 for axis in (0, 1) for basis in (2, 3, 6, 7))
    }
    require(len(large) == 375, "H510 large block")

    pool = load(repository / "hadwiger_nelson_heule510_completion_frontier/fresh_candidates.json")
    require(len(pool) == 122, "complete candidate pool")
    unit = (DENOMINATOR * DENOMINATOR,) + (0,) * 7
    selected = []
    classification = Counter()
    candidate_pair_checks = 0
    for row in pool:
        point = scaled_point(row["coordinates"])
        neighbours = []
        for vertex, old_point in enumerate(base):
            candidate_pair_checks += 1
            if exact_squared_distance(point, old_point) == unit:
                neighbours.append(vertex)
        require(neighbours == row["neighbors"] and len(neighbours) == row["degree"],
                "candidate neighbourhood recomputation")
        large_degree = len(set(neighbours) & large)
        small_degree = len(neighbours) - large_degree
        classification[large_degree, small_degree] += 1
        if large_degree and small_degree:
            selected.append(row)
    require([row["centre_index"] for row in selected] == EXPECTED_CENTRES,
            "the four mixed completion centres")

    points = base + [scaled_point(row["coordinates"]) for row in selected]
    require(len(points) == len(set(points)) == 514, "514 distinct exact points")
    edges = []
    for left, right in combinations(range(514), 2):
        if exact_squared_distance(points[left], points[right]) == unit:
            edges.append((left, right))
    edge_bytes = "".join(f"{left},{right}\n" for left, right in edges).encode("ascii")
    require(len(edges) == 2526, "complete H514 unit-edge count")
    require(sha256(edge_bytes).hexdigest() == EXPECTED_EDGE_HASH,
            "canonical ordered H514 edge identity")
    require([edge for edge in edges if edge[0] >= 510]
            == [(510, 511), (511, 512), (512, 513)], "induced completion path")
    attachments = [
        [left for left, right in edges if right == 510 + offset and left < 510]
        for offset in range(4)
    ]
    require(attachments == [row["neighbors"] for row in selected],
            "complete old-to-new attachments")
    return old, labels, large, edges, {
        "candidate_pair_checks": candidate_pair_checks,
        "candidate_classification": [
            {"large_degree": key[0], "small_degree": key[1], "centres": count}
            for key, count in sorted(classification.items())
        ],
        "selected_centres": EXPECTED_CENTRES,
        "selected_attachments": attachments,
        "edge_stream_sha256": sha256(edge_bytes).hexdigest(),
    }


def decode_ambient(old, labels, row) -> str:
    """Decode one H510-family witness directly from its original U553 recipe."""
    source_kind = row.get("source")
    if source_kind == "native":
        return row["colouring"]
    if source_kind == "forced":
        omissions = [row["index"]]
        text = old["forced_witness"][str(row["index"])]
    else:
        require(source_kind == "family", "recognized ambient recipe kind")
        family_row = old["family"][row["index"]]
        omissions = family_row["D"]
        text = family_row["witness"]
    retained = [vertex for vertex in range(553) if vertex not in set(omissions)]
    require(len(retained) == len(text), "ambient witness width")
    colour_by_label = dict(zip(retained, text))
    return "".join(colour_by_label.get(label, ".") for label in labels) + row["extra"]


def build_h517_source_strings(repository: Path, old, labels, large) -> list[str]:
    """Reimplement the historical recipe stack that numbers 963 source rows."""
    prior = load(repository / "hadwiger_nelson_heule517_family_pilot/certificate.json")["rows"]
    small_pilot = load(repository / "hadwiger_nelson_heule517_small_pilot/certificate.json")["rows"]
    small134 = load(repository / "hadwiger_nelson_heule517_small134/certificate.json")
    profiles = load(repository / "hadwiger_nelson_heule517_joint_interface/certificate.json")["rows"]
    large2 = load(repository / "hadwiger_nelson_heule517_large2_pilot/certificate.json")["rows"]
    large3 = load(repository / "hadwiger_nelson_heule517_large3/certificate.json")["rows"]
    large4 = load(repository / "hadwiger_nelson_heule517_large4/certificate.json")["rows"]
    large_order = sorted(large)
    small_order = sorted(set(range(517)) - large)

    def decode_small(row) -> str:
        if row["kind"] == "seed":
            index = row["row"]
            require(type(index) is int and 0 <= index < len(prior), "small seed index")
            require(row["D"] == prior[index]["D"], "small seed omissions")
            return decode_ambient(old, labels, prior[index])
        require(row["kind"] == "case", "small case kind")
        index = row["case"]
        require(type(index) is int and 0 <= index < len(profiles), "joint-profile index")
        left = profiles[index]["colouring"]
        right = row["colouring"]
        require(len(left) == 375 and len(right) == 142, "block-colouring widths")
        full = ["."] * 517
        for vertex, colour in zip(large_order, left):
            full[vertex] = colour
        for vertex, colour in zip(small_order, right):
            full[vertex] = colour
        return "".join(full)

    final_small = []
    for origin, index in small134["final_rows"]:
        require(origin in ("initial", "new"), "small134 source name")
        pool = small_pilot if origin == "initial" else small134["new_rows"]
        require(type(index) is int and 0 <= index < len(pool), "small134 recipe index")
        final_small.append(pool[index])
    require((len(prior), len(small_pilot), len(small134["new_rows"]), len(final_small),
             len(large2), len(large3), len(large4)) == (526, 206, 16, 202, 86, 108, 33),
            "historical certificate-family sizes")

    source = [decode_ambient(old, labels, row) for row in prior]
    source.extend(decode_small(row) for row in final_small)
    source.extend(row["colouring"] for row in large2)
    source.extend(row["colouring"] for row in large3)
    source.extend(row["colouring"] for row in large4)
    source.extend(
        row["colouring"]
        for row in load(repository / "hadwiger_nelson_heule517_whole_decision/certificate.json")["rows"]
    )
    require(len(source) == 963, "exact source-string numbering")
    require(all(len(colouring) == 517 and set(colouring) <= set(".0123") for colouring in source),
            "source-string width and alphabet")
    return source


def decode_transport(recipe, source: list[str]) -> str:
    require(isinstance(recipe, list) and len(recipe) == 3, "transport recipe shape")
    index, tail, fills = recipe
    require(type(index) is int and 0 <= index < len(source), "transport source index")
    require(isinstance(tail, str) and len(tail) == 4 and set(tail) <= set(".0123"),
            "transport H514 tail")
    colouring = list(source[index][:510] + tail)
    restored = set()
    for item in fills:
        require(isinstance(item, list) and len(item) == 2, "fill recipe shape")
        vertex, colour = item
        require(type(vertex) is int and 0 <= vertex < 510 and vertex not in restored,
                "unique old fill vertex")
        require(colouring[vertex] == "." and colour in "0123", "valid omitted-vertex fill")
        colouring[vertex] = colour
        restored.add(vertex)
    return "".join(colouring)


def check_colouring(colouring: str, omissions: list[int], edges: list[tuple[int, int]]) -> int:
    require(len(colouring) == 514 and set(colouring) <= set(".0123"), "colouring domain")
    require(omissions == sorted(set(omissions)), "canonical nonempty omissions")
    require(omissions == [vertex for vertex, colour in enumerate(colouring) if colour == "."],
            "dots equal omission set")
    checks = 0
    for left, right in edges:
        if colouring[left] == "." or colouring[right] == ".":
            continue
        checks += 1
        require(colouring[left] != colouring[right], "monochromatic unit edge")
    return checks


def load_positive_library(repository: Path, edges, old, labels, large):
    source = build_h517_source_strings(repository, old, labels, large)
    interface = load(repository / "hadwiger_nelson_heule514_interface/certificate.json")
    require(len(interface["transport"]) == 491 and len(interface["native"]) == 25,
            "H514 interface library sizes")
    initial_colours = [decode_transport(recipe, source) for recipe in interface["transport"]]
    initial_colours.extend(row["colouring"] for row in interface["native"])
    initial = sorted(
        (([vertex for vertex, colour in enumerate(text) if colour == "."], text)
         for text in initial_colours),
        key=lambda item: (len(item[0]), item[0]),
    )
    rows = [
        {"group": "interface", "index": index, "D": omissions, "colouring": colouring}
        for index, (omissions, colouring) in enumerate(initial)
    ]
    profile = load(repository / "hadwiger_nelson_heule514_profile_pilot/certificate.json")
    whole = load(repository / "hadwiger_nelson_heule514_whole_decision/certificate.json")
    require(len(profile) == 15 and len(whole) == 13, "supplemental certificate sizes")
    require([row["index"] for row in profile] == list(range(15)), "profile row numbering")
    require([row["index"] for row in whole] == list(range(13)), "whole row numbering")
    rows.extend({"group": "profile", "index": row["index"], "D": row["D"],
                 "colouring": row["colouring"]} for row in profile)
    rows.extend({"group": "whole", "index": row["index"], "D": row["D"],
                 "colouring": row["colouring"]} for row in whole)

    edge_checks = 0
    for row in rows:
        require(row["D"], "positive witness has a nonempty cut")
        edge_checks += check_colouring(row["colouring"], row["D"], edges)
    cuts = [frozenset(row["D"]) for row in rows]
    require(len(rows) == len(set(cuts)) == 544, "544 distinct positive cuts")
    return rows, edge_checks


def greedy_restore(seed: str, omissions: set[int], removed: list[int], adjacency):
    live = set(range(514)) - omissions - set(removed)
    colouring = [seed[vertex] if vertex in live else "." for vertex in range(514)]
    choices = []
    for vertex in reversed(removed):
        neighbour_colours = {colouring[other] for other in adjacency[vertex]
                             if colouring[other] != "."}
        require(len(neighbour_colours) <= 3, "reverse restoration has at most three colours")
        choice = min(set("0123") - neighbour_colours)
        colouring[vertex] = choice
        choices.append({"vertex": vertex, "forbidden": sorted(neighbour_colours), "chosen": choice})
    return "".join(colouring), choices


def rejection_controls(rows, edges) -> list[str]:
    rejected = []

    def reject(name, function):
        try:
            function()
        except ReviewFailure:
            rejected.append(name)
        else:
            raise ReviewFailure("accepted malformed control: " + name)

    row = rows[0]
    reject("truncated_colouring", lambda: check_colouring(row["colouring"][:-1], row["D"], edges))
    reject("incorrect_omission_set", lambda: check_colouring(row["colouring"], [], edges))
    left, right = next((left, right) for left, right in edges
                       if row["colouring"][left] != "." and row["colouring"][right] != ".")
    corrupt = row["colouring"][:right] + row["colouring"][left] + row["colouring"][right + 1:]
    reject("monochromatic_unit_edge", lambda: check_colouring(corrupt, row["D"], edges))
    return rejected


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repository", required=True, type=Path)
    parser.add_argument("--target", type=Path)
    parser.add_argument("--report", required=True, type=Path)
    args = parser.parse_args()
    repository = args.repository.resolve()
    target = (args.target or repository / "hadwiger_nelson_heule514_whole_decision").resolve()

    reviewed_source = verify_sha256s(target)
    target_manifest_inputs = verify_manifest(repository, target / "manifest.json")
    interface_manifest_inputs = verify_manifest(
        repository, repository / "hadwiger_nelson_heule514_interface/manifest.json")

    old, labels, large, edges, graph_details = reconstruct_h514(repository)
    rows, positive_edge_checks = load_positive_library(repository, edges, old, labels, large)
    forced = {next(iter(row["D"])) for row in rows if len(row["D"]) == 1}
    free = sorted(set(range(514)) - forced)
    cuts = [frozenset(row["D"]) for row in rows]
    minimal_cuts = [cut for cut in cuts if not any(other < cut for other in cuts)]
    non_singletons = [cut for cut in minimal_cuts if len(cut) > 1]
    require(len(forced) == 503 and free == EXPECTED_FREE, "503 forced and exact 11 free vertices")
    require(len(minimal_cuts) == 514 and len(non_singletons) == 11
            and all(len(cut) == 2 and cut <= set(free) for cut in non_singletons),
            "minimal antichain is 503 singletons and 11 free-vertex pairs")

    position = {vertex: index for index, vertex in enumerate(free)}
    cut_masks = [sum(1 << position[vertex] for vertex in cut) for cut in non_singletons]
    avoiding_histogram = [0] * (len(free) + 1)
    avoiding_subsets = []
    for subset_mask in range(1 << len(free)):
        if all(subset_mask & cut_mask != cut_mask for cut_mask in cut_masks):
            omissions = [free[index] for index in range(len(free)) if subset_mask & (1 << index)]
            avoiding_histogram[len(omissions)] += 1
            if len(omissions) >= 6:
                avoiding_subsets.append(omissions)
    require(sorted(avoiding_subsets) == EXPECTED_EXCEPTIONS,
            "the witness hypergraph leaves exactly four six-omission exceptions: "
            + repr(avoiding_subsets))
    avoiding_subsets = sorted(avoiding_subsets)

    adjacency = [set() for _ in range(514)]
    for left, right in edges:
        adjacency[left].add(right)
        adjacency[right].add(left)
    seed_rows = [row for row in rows if row["D"] == [299]]
    require(len(seed_rows) == 1, "unique singleton-299 seed")
    seed = seed_rows[0]
    exception_colours = {}
    exception_records = []
    for omission_list in EXPECTED_EXCEPTIONS:
        omissions = set(omission_list)
        degrees = {str(vertex): len(adjacency[vertex] - omissions) for vertex in (299, 302)}
        require(all(value <= 3 for value in degrees.values()), "simultaneous low-degree pair")
        colouring, choices = greedy_restore(seed["colouring"], omissions, [299, 302], adjacency)
        check_colouring(colouring, omission_list, edges)
        exception_colours[frozenset(omissions)] = colouring
        exception_records.append({
            "omitted": omission_list,
            "degrees_before_removal": degrees,
            "restoration_order": [302, 299],
            "restoration_choices": choices,
            "seed": {"group": seed["group"], "index": seed["index"], "D": seed["D"]},
        })

    six_cases = 0
    six_direct = 0
    six_peeled = 0
    six_edge_checks = 0
    for omissions_tuple in combinations(free, 6):
        six_cases += 1
        omissions = set(omissions_tuple)
        direct = next((row for row in rows if set(row["D"]) <= omissions), None)
        if direct is not None:
            six_direct += 1
            colouring = "".join("." if vertex in omissions else direct["colouring"][vertex]
                                 for vertex in range(514))
        else:
            six_peeled += 1
            colouring = exception_colours[frozenset(omissions)]
        six_edge_checks += check_colouring(colouring, list(omissions_tuple), edges)
    require((six_cases, six_direct, six_peeled, six_edge_checks)
            == (462, 458, 4, 1146726), "all 462 exact six-omission colourings")

    # Stronger than the submission's six-set loop: explicitly construct and
    # check a colouring for every free-vertex subset of size at least six.
    all_subset_edge_checks = 0
    at_most_508_patterns = 0
    for subset_mask in range(1 << len(free)):
        omissions = {free[index] for index in range(len(free)) if subset_mask & (1 << index)}
        if len(omissions) < 6:
            continue
        at_most_508_patterns += 1
        direct = next((row for row in rows if set(row["D"]) <= omissions), None)
        if direct is not None:
            base = direct["colouring"]
        else:
            exceptional = next((cut for cut in exception_colours if cut <= omissions), None)
            require(exceptional is not None, "non-direct subset contains a checked exception")
            base = exception_colours[exceptional]
        colouring = "".join("." if vertex in omissions else base[vertex]
                             for vertex in range(514))
        all_subset_edge_checks += check_colouring(colouring, sorted(omissions), edges)
    require(at_most_508_patterns == 1024, "all free omission patterns of size at least six")

    direct_summary = load(target / "direct_certificate.json")
    require((direct_summary["forced_vertices"], direct_summary["free_vertices"],
             direct_summary["cases"], direct_summary["directly_covered"],
             direct_summary["peeling_cases"])
            == (len(forced), free, six_cases, six_direct, six_peeled),
            "independent counts match submitted direct certificate")
    require([row["omitted"] for row in direct_summary["peeling_witnesses"]]
            == EXPECTED_EXCEPTIONS, "submitted exceptional supports")
    submitted = load(target / "standalone_verification.json")
    require((submitted["vertices"], submitted["unit_edges"],
             submitted["positive_witnesses_checked"], submitted["positive_edge_checks"],
             submitted["direct_whole_support"]["target_edge_checks"])
            == (514, len(edges), len(rows), positive_edge_checks, six_edge_checks),
            "independent totals match submitted standalone report")

    result = {
        "all_checks_passed": True,
        "scope": "every at-most-508-vertex subgraph of the fixed exact H514 unit-distance graph is four-colourable",
        "python": sys.version.split()[0],
        "reviewed_source_commit": "ee698e3de7f3b4e32e8655b6df54f1f1c898d152",
        "reviewed_source": reviewed_source,
        "pinned_manifest_inputs": {
            "target": target_manifest_inputs,
            "interface": interface_manifest_inputs,
        },
        "graph": {
            "vertices": 514,
            "exact_graph_pairs_checked": 514 * 513 // 2,
            "unit_edges": len(edges),
            **graph_details,
        },
        "positive_library": {
            "source_strings_redecoded": 963,
            "interface_colourings": 516,
            "profile_colourings": 15,
            "whole_colourings": 13,
            "total_colourings_checked": len(rows),
            "retained_edge_checks": positive_edge_checks,
            "raw_distinct_cuts": len(cuts),
            "minimal_cuts": len(minimal_cuts),
            "cut_size_histogram": {
                str(size): sum(len(cut) == size for cut in minimal_cuts)
                for size in sorted({len(cut) for cut in minimal_cuts})
            },
            "forced_vertices": len(forced),
            "free_vertices": free,
            "non_singleton_cuts": len(non_singletons),
            "minimal_non_singleton_cuts": sorted(sorted(cut) for cut in non_singletons),
        },
        "cover": {
            "all_free_subsets_checked": 1 << len(free),
            "cut_avoiding_subset_histogram": avoiding_histogram,
            "non_direct_subsets_of_size_at_least_six": avoiding_subsets,
            "six_omission_cases": six_cases,
            "six_direct": six_direct,
            "six_degree_peeled": six_peeled,
            "six_case_retained_edge_checks": six_edge_checks,
            "all_size_at_least_six_patterns_coloured": at_most_508_patterns,
            "all_size_at_least_six_retained_edge_checks": all_subset_edge_checks,
            "exception_records": exception_records,
        },
        "negative_controls_rejected": rejection_controls(rows, edges),
        "conclusion": {
            "fixed_H514_deletion_family_closed_through_508": True,
            "edge_deleted_subgraphs_included_by_restriction": True,
            "new_sub509_five_chromatic_graph": False,
            "record_improvement": False,
            "other_geometric_supports_excluded": False,
            "solver_or_negative_certificate_required": False,
        },
        "trust_boundary": [
            "the pinned raw coordinates and the standard linear independence of the eight squarefree radical basis elements",
            "the pinned positive colouring strings and transport recipes; every resulting H514 colouring is nevertheless checked edge by edge",
            "ordinary CPython integer/Fraction arithmetic, JSON decoding, and exhaustive finite-loop execution",
            "SHA-256 collision resistance for source and graph-stream identity",
        ],
    }
    atomic_json(args.report, result)
    print(json.dumps({
        "all_checks_passed": True,
        "unit_edges": len(edges),
        "positive_colourings": len(rows),
        "free_vertices": len(free),
        "all_free_subsets_checked": 1 << len(free),
        "six_cases": six_cases,
        "exceptions": six_peeled,
        "fixed_H514_closed_through_508": True,
    }, sort_keys=True))


if __name__ == "__main__":
    main()
