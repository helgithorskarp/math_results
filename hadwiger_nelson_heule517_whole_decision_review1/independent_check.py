#!/usr/bin/env python3
"""Independent positive-certificate review of the whole H517 closure.

No module from the reviewed contribution or its preceding reviewer checker is
imported.  The script reconstructs the exact 517-point graph, decodes all 963
positive colourings from their original compact sources, and proves the final
cover by enumerating every subset of the 21 free vertices rather than only the
nine-subsets enumerated by the submission.
"""

from __future__ import annotations

import argparse
from fractions import Fraction
from hashlib import sha256
from itertools import combinations
import json
import os
from pathlib import Path
import sys


RADICANDS = (3, 5, 11)
DENOMINATOR = 96
EXPECTED_COMPLETIONS = [327, 439, 671, 1040, 1074, 1377, 1383]
EXPECTED_EDGE_HASH = "93bec44c9bc6e2514ed4d4b75985267561f63751eaa7132ec5cdd271af85e456"


class ReviewFailure(RuntimeError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ReviewFailure(message)


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def digest(path: Path) -> dict[str, int | str]:
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


def scaled_axis(raw: list[object]) -> tuple[int, ...]:
    require(isinstance(raw, list) and len(raw) == 8, "radical-basis axis width")
    scaled = [Fraction(value) * DENOMINATOR for value in raw]
    require(all(value.denominator == 1 for value in scaled), "coordinate denominator divides 96")
    return tuple(int(value) for value in scaled)


def scaled_point(raw: list[list[object]]) -> tuple[tuple[int, ...], tuple[int, ...]]:
    require(isinstance(raw, list) and len(raw) == 2, "point has two axes")
    return scaled_axis(raw[0]), scaled_axis(raw[1])


def ring_product(left: tuple[int, ...], right: tuple[int, ...]) -> tuple[int, ...]:
    """Exact multiplication in Q(sqrt(3),sqrt(5),sqrt(11)), scaled externally."""
    require(len(left) == len(right) == 8, "radical-basis coefficient width")
    result = [0] * 8
    for left_mask, left_value in enumerate(left):
        for right_mask, right_value in enumerate(right):
            overlap = left_mask & right_mask
            square_factor = 1
            for bit, radicand in enumerate(RADICANDS):
                if overlap & (1 << bit):
                    square_factor *= radicand
            result[left_mask ^ right_mask] += left_value * right_value * square_factor
    return tuple(result)


def exact_squared_distance(left, right) -> tuple[int, ...]:
    delta_x = tuple(a - b for a, b in zip(left[0], right[0]))
    delta_y = tuple(a - b for a, b in zip(left[1], right[1]))
    x2 = ring_product(delta_x, delta_x)
    y2 = ring_product(delta_y, delta_y)
    return tuple(a + b for a, b in zip(x2, y2))


def reconstruct_graph(repository: Path):
    source = load(repository / "hadwiger_nelson_parts509_heule_union_minimum/certificate_H510.json")
    labels = [index for index, provenance in enumerate(source["provenance"]) if "510" in provenance]
    require(len(labels) == 510 and labels == sorted(set(labels)), "exact H510 increasing labels")

    candidates = load(repository / "hadwiger_nelson_heule510_completion_frontier/fresh_candidates.json")
    completions = [row for row in candidates if row["degree"] >= 7]
    require([row["centre_index"] for row in completions] == EXPECTED_COMPLETIONS,
            "exact seven completion centres")
    points = [scaled_point(source["coordinates"][str(label)]) for label in labels]
    points.extend(scaled_point(row["coordinates"]) for row in completions)
    require(len(points) == len(set(points)) == 517, "517 distinct exact points")

    unit = (DENOMINATOR * DENOMINATOR,) + (0,) * 7
    edges = []
    for left, right in combinations(range(517), 2):
        if exact_squared_distance(points[left], points[right]) == unit:
            edges.append((left, right))
    edge_stream = "".join(f"{left},{right}\n" for left, right in edges).encode("ascii")

    large = {
        vertex
        for vertex, point in enumerate(points)
        if all(point[axis][basis] == 0 for axis in (0, 1) for basis in (2, 3, 6, 7))
    }
    small = set(range(517)) - large
    large_edges = sum(left in large and right in large for left, right in edges)
    small_edges = sum(left in small and right in small for left, right in edges)
    cross_edges = len(edges) - large_edges - small_edges
    require((len(large), len(small), len(edges), large_edges, small_edges, cross_edges)
            == (375, 142, 2555, 1920, 605, 30), "exact H517 graph and block counts")
    require(sha256(edge_stream).hexdigest() == EXPECTED_EDGE_HASH, "ordered unit-edge identity")
    return source, labels, edges, large, small


def prior_decoder(source, labels, row) -> str:
    kind = row.get("source")
    if kind == "native":
        return row["colouring"]
    if kind == "forced":
        omitted = [row["index"]]
        text = source["forced_witness"][str(row["index"])]
    else:
        require(kind == "family", "recognized inherited witness source")
        family_row = source["family"][row["index"]]
        omitted = family_row["D"]
        text = family_row["witness"]
    retained = [vertex for vertex in range(553) if vertex not in set(omitted)]
    require(len(retained) == len(text), "ambient witness width")
    colour = dict(zip(retained, text))
    return "".join(colour.get(label, ".") for label in labels) + row["extra"]


def inherited_witnesses(repository: Path, source, labels, large, small):
    prior = load(repository / "hadwiger_nelson_heule517_family_pilot/certificate.json")["rows"]
    small_pilot = load(repository / "hadwiger_nelson_heule517_small_pilot/certificate.json")["rows"]
    small134 = load(repository / "hadwiger_nelson_heule517_small134/certificate.json")
    profiles = load(repository / "hadwiger_nelson_heule517_joint_interface/certificate.json")["rows"]
    large2 = load(repository / "hadwiger_nelson_heule517_large2_pilot/certificate.json")["rows"]
    large3 = load(repository / "hadwiger_nelson_heule517_large3/certificate.json")["rows"]
    large4 = load(repository / "hadwiger_nelson_heule517_large4/certificate.json")["rows"]
    large_order = sorted(large)
    small_order = sorted(small)

    def decode_small(row) -> str:
        if row["kind"] == "seed":
            index = row["row"]
            require(type(index) is int and 0 <= index < len(prior), "small seed index")
            require(row["D"] == prior[index]["D"], "small seed omission identity")
            return prior_decoder(source, labels, prior[index])
        require(row["kind"] == "case", "small case kind")
        index = row["case"]
        require(type(index) is int and 0 <= index < len(profiles), "small profile index")
        left = profiles[index]["colouring"]
        right = row["colouring"]
        require(len(left) == 375 and len(right) == 142, "large/small colouring widths")
        full = ["."] * 517
        for vertex, colour in zip(large_order, left):
            full[vertex] = colour
        for vertex, colour in zip(small_order, right):
            full[vertex] = colour
        return "".join(full)

    final_small = []
    for origin, index in small134["final_rows"]:
        require(origin in ("initial", "new"), "small134 recipe source")
        pool = small_pilot if origin == "initial" else small134["new_rows"]
        require(type(index) is int and 0 <= index < len(pool), "small134 recipe index")
        final_small.append(pool[index])

    require((len(prior), len(small_pilot), len(small134["new_rows"]), len(final_small),
             len(large2), len(large3), len(large4)) == (526, 206, 16, 202, 86, 108, 33),
            "inherited certificate family sizes")
    return {
        "prior": [(row, prior_decoder(source, labels, row)) for row in prior],
        "small": [(row, decode_small(row)) for row in final_small],
        "large2": [(row, row["colouring"]) for row in large2],
        "large3": [(row, row["colouring"]) for row in large3],
        "large4": [(row, row["colouring"]) for row in large4],
    }


def check_witness(row, colouring: str, edges: list[tuple[int, int]]) -> int:
    omissions = row["D"]
    require(omissions and omissions == sorted(set(omissions)), "nonempty sorted omission set")
    require(len(colouring) == 517 and set(colouring) <= set(".0123"), "colouring domain")
    require(omissions == [vertex for vertex, colour in enumerate(colouring) if colour == "."],
            "dots equal the claimed omission set")
    retained_checks = 0
    for left, right in edges:
        if colouring[left] == "." or colouring[right] == ".":
            continue
        retained_checks += 1
        require(colouring[left] != colouring[right], "monochromatic unit edge")
    return retained_checks


def verify_groups(groups, edges):
    result = {}
    for name, rows in groups.items():
        cuts = set()
        retained_checks = 0
        for row, colouring in rows:
            retained_checks += check_witness(row, colouring, edges)
            cut = tuple(row["D"])
            require(cut not in cuts, f"duplicate omission set within {name}")
            cuts.add(cut)
        result[name] = {"rows": len(rows), "retained_edge_checks": retained_checks}
    return result


def minimal_antichain(cuts: set[frozenset[int]]) -> list[frozenset[int]]:
    answer = []
    for cut in sorted(cuts, key=lambda item: (len(item), tuple(sorted(item)))):
        if not any(old <= cut for old in answer):
            answer.append(cut)
    return answer


def avoiding_histogram(universe_size: int, forbidden_masks: list[int]) -> list[int]:
    """Exhaust all subsets, counting those containing no certified cut."""
    histogram = [0] * (universe_size + 1)
    for subset in range(1 << universe_size):
        if all(subset & forbidden != forbidden for forbidden in forbidden_masks):
            histogram[subset.bit_count()] += 1
    return histogram


def rejection_controls(new_rows, edges) -> list[str]:
    rejected = []

    def reject(name, function):
        try:
            function()
        except ReviewFailure:
            rejected.append(name)
        else:
            raise ReviewFailure("accepted malformed control " + name)

    row = new_rows[0]
    colouring = row["colouring"]
    left, right = next(
        (left, right) for left, right in edges
        if colouring[left] != "." and colouring[right] != "."
    )
    corrupted = colouring[:right] + colouring[left] + colouring[right + 1:]
    reject("monochromatic_unit_edge", lambda: check_witness(row, corrupted, edges))
    reject("incorrect_omission_set", lambda: check_witness({**row, "D": []}, colouring, edges))

    toy = avoiding_histogram(3, [1])
    require(toy == [1, 2, 1, 0], "incomplete toy cover exposes an avoiding pair")
    rejected.append("incomplete_hypergraph_cover")
    return rejected


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repository", required=True, type=Path)
    parser.add_argument("--target", type=Path)
    parser.add_argument("--report", required=True, type=Path)
    args = parser.parse_args()
    repository = args.repository.resolve()
    target = (args.target or repository / "hadwiger_nelson_heule517_whole_decision").resolve()

    submitted_sums = {}
    for line in (target / "SHA256SUMS").read_text(encoding="ascii").splitlines():
        expected, name = line.split(maxsplit=1)
        observed = digest(target / name)
        require(observed["sha256"] == expected, "submitted source hash " + name)
        submitted_sums[name] = observed

    source, labels, edges, large, small = reconstruct_graph(repository)
    groups = inherited_witnesses(repository, source, labels, large, small)
    inherited_checks = verify_groups(groups, edges)
    require(sum(item["rows"] for item in inherited_checks.values()) == 955,
            "exact 955 inherited colourings")

    new_rows = load(target / "certificate.json")["rows"]
    require(len(new_rows) == 8 and len({row["native_index"] for row in new_rows}) == 8,
            "eight distinct retained native witnesses")
    new_edge_checks = sum(check_witness(row, row["colouring"], edges) for row in new_rows)
    require([row["D"] for row in new_rows]
            == [[130], [194], [254], [285], [395], [470], [192, 245], [332, 338]],
            "exact new omission sets")

    all_cuts = {
        frozenset(row["D"])
        for rows in groups.values()
        for row, _ in rows
    }
    all_cuts.update(frozenset(row["D"]) for row in new_rows)
    antichain = minimal_antichain(all_cuts)
    forced = {next(iter(cut)) for cut in antichain if len(cut) == 1}
    free = sorted(set(range(517)) - forced)
    non_singleton = [cut for cut in antichain if len(cut) > 1]
    require((len(antichain), len(forced), len(forced & large), len(forced & small), len(free),
             len(non_singleton)) == (538, 496, 367, 129, 21, 42),
            "combined minimal-cut structure")
    require(all(cut <= set(free) for cut in non_singleton), "non-singleton cuts live on free vertices")

    position = {vertex: index for index, vertex in enumerate(free)}
    cut_masks = [sum(1 << position[vertex] for vertex in cut) for cut in non_singleton]
    histogram = avoiding_histogram(len(free), cut_masks)
    require(sum(histogram) == 8142, "number of cut-avoiding free subsets")
    require(histogram == [1, 21, 177, 773, 1888, 2596, 1920, 679, 87] + [0] * 13,
            "complete cut-avoiding subset histogram")
    maximum_avoiding = max(index for index, count in enumerate(histogram) if count)
    require(maximum_avoiding == 8, "every nine free omissions contain a certified cut")

    cut_size_histogram = {
        str(size): sum(len(cut) == size for cut in antichain)
        for size in sorted({len(cut) for cut in antichain})
    }
    published = load(target / "verification.json")
    require((published["unit_edges"], published["inherited_colourings"], published["new_colourings"],
             published["final_antichain"], published["forced_vertices"], published["free_vertices"],
             published["non_singleton_cuts"], published["nine_sets_checked"],
             published["uncovered_nine_sets"])
            == (len(edges), 955, len(new_rows), len(antichain), len(forced), free,
                len(non_singleton), 293930, 0), "independent result matches submitted summary")

    controls = rejection_controls(new_rows, edges)
    result = {
        "all_checks_passed": True,
        "scope": "every at-most-508-vertex subgraph of the fixed exact H517 support is four-colourable",
        "python": sys.version.split()[0],
        "reviewed_source": submitted_sums,
        "graph": {
            "vertices": 517,
            "exact_pairs_checked": 133386,
            "unit_edges": len(edges),
            "edge_stream_sha256": EXPECTED_EDGE_HASH,
            "large_vertices": len(large),
            "small_vertices": len(small),
            "large_edges": 1920,
            "small_edges": 605,
            "cross_edges": 30,
        },
        "positive_witnesses": {
            "inherited": inherited_checks,
            "inherited_total": 955,
            "inherited_retained_edge_checks": sum(item["retained_edge_checks"] for item in inherited_checks.values()),
            "new": len(new_rows),
            "new_retained_edge_checks": new_edge_checks,
            "new_omission_sets": [row["D"] for row in new_rows],
        },
        "cover": {
            "minimal_cuts": len(antichain),
            "cut_size_histogram": cut_size_histogram,
            "forced_vertices": len(forced),
            "forced_large": len(forced & large),
            "forced_small": len(forced & small),
            "free_vertices": free,
            "non_singleton_cuts": len(non_singleton),
            "all_free_subsets_checked": 1 << len(free),
            "cut_avoiding_subset_histogram": histogram,
            "maximum_cut_avoiding_omissions": maximum_avoiding,
        },
        "negative_controls_rejected": controls,
        "conclusion": {
            "fixed_support_closed": True,
            "unrestricted_at_most508_family_closed": True,
            "record_improvement": False,
            "new_five_chromatic_graph": False,
            "other_supports_excluded": False,
            "negative_solver_proof_required": False,
        },
        "trust_boundary": [
            "exact source coordinates and independence of the radical basis",
            "ordinary CPython integer and Fraction arithmetic and faithful JSON decoding",
            "completeness of the explicit finite loops and the elementary restriction argument",
            "SHA-256 for source and edge-stream identity",
        ],
    }
    atomic_json(args.report, result)
    print(json.dumps({
        "all_checks_passed": True,
        "unit_edges": len(edges),
        "positive_colourings": 955 + len(new_rows),
        "free_vertices": len(free),
        "all_free_subsets_checked": 1 << len(free),
        "maximum_cut_avoiding_omissions": maximum_avoiding,
        "fixed_support_closed": True,
    }, sort_keys=True))


if __name__ == "__main__":
    main()
