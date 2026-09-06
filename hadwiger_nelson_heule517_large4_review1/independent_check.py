#!/usr/bin/env python3
"""Clean-room exact review of the H517 four-large/five-small closure.

The checker imports no reviewed module.  It reconstructs the 517-point graph
in Q(sqrt(3),sqrt(5),sqrt(11)), decodes every positive witness used from the
134-small through four-large stages, and independently enumerates each finite
cover needed for the target-order corollary.
"""

from __future__ import annotations

import argparse
from fractions import Fraction
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path


RADICANDS = (3, 5, 11)


class ReviewFailure(RuntimeError):
    pass


def need(condition, message):
    if not condition:
        raise ReviewFailure(message)


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def field_product(left, right):
    """Multiply in the squarefree mask basis for sqrt(3),sqrt(5),sqrt(11)."""
    need(len(left) == len(right) == 8, "field coefficient width")
    out = [0] * 8
    for i, a in enumerate(left):
        if not a:
            continue
        for j, b in enumerate(right):
            if not b:
                continue
            common = i & j
            coefficient = a * b
            for bit, radicand in enumerate(RADICANDS):
                if common & (1 << bit):
                    coefficient *= radicand
            out[i ^ j] += coefficient
    return tuple(out)


def squared_distance(a, b):
    dx = tuple(x - y for x, y in zip(a[0], b[0]))
    dy = tuple(x - y for x, y in zip(a[1], b[1]))
    return tuple(x + y for x, y in zip(field_product(dx, dx), field_product(dy, dy)))


def scaled_point(raw, denominator=96):
    need(isinstance(raw, list) and len(raw) == 2, "point axes")
    axes = []
    for axis in raw:
        need(isinstance(axis, list) and len(axis) == 8, "point basis width")
        values = [Fraction(x) * denominator for x in axis]
        need(all(x.denominator == 1 for x in values), "point denominator")
        axes.append(tuple(int(x) for x in values))
    return tuple(axes)


def reconstruct_graph(repository):
    old = load(repository / "hadwiger_nelson_parts509_heule_union_minimum/certificate_H510.json")
    labels = [v for v in range(553) if "510" in old["provenance"][v]]
    need(len(labels) == 510 and labels == sorted(set(labels)), "H510 label set")
    candidates = load(repository / "hadwiger_nelson_heule510_completion_frontier/fresh_candidates.json")
    added = [row for row in candidates if row["degree"] >= 7]
    need([row["centre_index"] for row in added] == [327, 439, 671, 1040, 1074, 1377, 1383],
         "completion stratum")
    points = [scaled_point(old["coordinates"][str(v)]) for v in labels]
    points += [scaled_point(row["coordinates"]) for row in added]
    need(len(points) == len(set(points)) == 517, "H517 distinct support")

    unit = (96 * 96,) + (0,) * 7
    edges = [(i, j) for i, j in combinations(range(517), 2)
             if squared_distance(points[i], points[j]) == unit]
    edge_raw = "".join(f"{i},{j}\n" for i, j in edges).encode("ascii")
    large = {v for v, point in enumerate(points)
             if all(point[axis][basis] == 0 for axis in (0, 1) for basis in (2, 3, 6, 7))}
    small = set(range(517)) - large
    le = sum(i in large and j in large for i, j in edges)
    se = sum(i in small and j in small for i, j in edges)
    cross = len(edges) - le - se
    need((len(large), len(small), len(edges), le, se, cross) == (375, 142, 2555, 1920, 605, 30),
         "H517 graph and block counts")
    return old, labels, points, edges, large, small, sha256(edge_raw).hexdigest()


def witness_data(repository, old, labels, large, small):
    prior = load(repository / "hadwiger_nelson_heule517_family_pilot/certificate.json")["rows"]
    small133 = load(repository / "hadwiger_nelson_heule517_small_pilot/certificate.json")["rows"]
    small134 = load(repository / "hadwiger_nelson_heule517_small134/certificate.json")
    profiles = load(repository / "hadwiger_nelson_heule517_joint_interface/certificate.json")["rows"]
    large2 = load(repository / "hadwiger_nelson_heule517_large2_pilot/certificate.json")["rows"]
    large3 = load(repository / "hadwiger_nelson_heule517_large3/certificate.json")["rows"]
    large4 = load(repository / "hadwiger_nelson_heule517_large4/certificate.json")["rows"]
    ls, ss = sorted(large), sorted(small)

    def decode_prior(row):
        source = row.get("source")
        if source == "native":
            return row["colouring"]
        if source == "forced":
            omitted = [row["index"]]
            text = old["forced_witness"][str(row["index"])]
        else:
            need(source == "family", "prior source kind")
            record = old["family"][row["index"]]
            omitted, text = record["D"], record["witness"]
        retained = sorted(set(range(553)) - set(omitted))
        need(len(retained) == len(text), "prior source witness length")
        colours = dict(zip(retained, text))
        return "".join(colours.get(v, ".") for v in labels) + row["extra"]

    def decode_small(row):
        if row["kind"] == "seed":
            need(type(row["row"]) is int and 0 <= row["row"] < len(prior), "small seed index")
            source = prior[row["row"]]
            need(row["D"] == source["D"], "small seed omissions")
            return decode_prior(source)
        need(row["kind"] == "case" and type(row["case"]) is int
             and 0 <= row["case"] < len(profiles), "small profile index")
        left, right = profiles[row["case"]]["colouring"], row["colouring"]
        need(len(left) == 375 and len(right) == 142, "block colouring widths")
        out = ["."] * 517
        for v, c in zip(ls, left):
            out[v] = c
        for v, c in zip(ss, right):
            out[v] = c
        return "".join(out)

    final_small = []
    for kind, index in small134["final_rows"]:
        pool = small133 if kind == "initial" else small134["new_rows"]
        need(kind in ("initial", "new") and type(index) is int and 0 <= index < len(pool),
             "small134 recipe")
        final_small.append(pool[index])
    need((len(prior), len(small133), len(small134["new_rows"]), len(final_small),
          len(large2), len(large3), len(large4)) == (526, 206, 16, 202, 86, 108, 33),
         "witness family sizes")
    return {
        "prior": [(row, decode_prior(row)) for row in prior],
        "small": [(row, decode_small(row)) for row in final_small],
        "large2": [(row, row["colouring"]) for row in large2],
        "large3": [(row, row["colouring"]) for row in large3],
        "large4": [(row, row["colouring"]) for row in large4],
    }


def verify_witnesses(groups, edges):
    result = {}
    stream = sha256()
    for name, rows in groups.items():
        checks = 0
        seen = set()
        for index, (row, colouring) in enumerate(rows):
            omitted = row["D"]
            need(omitted == sorted(set(omitted)) and omitted, f"{name} omission set")
            need(len(colouring) == 517 and set(colouring) <= set(".0123"),
                 f"{name} colouring domain")
            need(omitted == [v for v, c in enumerate(colouring) if c == "."],
                 f"{name} omission markers")
            need(all(colouring[u] == "." or colouring[v] == "." or colouring[u] != colouring[v]
                     for u, v in edges), f"{name} improper colouring")
            checks += sum(colouring[u] != "." and colouring[v] != "." for u, v in edges)
            cut = tuple(omitted)
            need(cut not in seen, f"{name} duplicate cut")
            seen.add(cut)
            stream.update(f"{name}:{index}:{','.join(map(str, omitted))}:{colouring}\n".encode("ascii"))
        result[name] = {"rows": len(rows), "retained_edge_checks": checks}
    result["witness_stream_sha256"] = stream.hexdigest()
    return result


def inclusion_antichain(cuts):
    minimal = []
    for cut in sorted(cuts, key=lambda d: (len(d), tuple(sorted(d)))):
        if not any(old <= cut for old in minimal):
            minimal.append(cut)
    return minimal


def small134_cover(small_cuts, small):
    forced = {next(iter(d)) for d in small_cuts if len(d) == 1}
    need(len(forced) == 120 and forced <= small, "small134 singleton forcing")
    free = sorted(small - forced)
    residual = [sum(1 << v for v in d) for d in small_cuts if not d & forced]
    count = 0
    for omitted in combinations(free, 8):
        mask = sum(1 << v for v in omitted)
        need(any(mask & cut == cut for cut in residual), "uncovered small134 omission")
        count += 1
    need((len(free), count) == (22, 319770), "small134 cover count")
    return {"forced_small": len(forced), "free_small": free, "eight_sets_checked": count,
            "remaining_cases": 0}


def block_family_cover(initial_cuts, new_cuts, large, small, small_omissions, large_omissions,
                       expected_small_cases, expected_candidates):
    forced = {next(iter(d)) for d in initial_cuts if len(d) == 1}
    free_small = sorted(small - forced)
    pure_small = [sum(1 << v for v in d) for d in initial_cuts if d <= small]
    pieces = [(d & small, d & large) for d in initial_cuts]
    new_masks = [sum(1 << v for v in d) for d in new_cuts]
    all_small = survivors = candidates = 0
    for omitted_small in combinations(free_small, small_omissions):
        all_small += 1
        smask = sum(1 << v for v in omitted_small)
        if any(smask & cut == cut for cut in pure_small):
            continue
        survivors += 1
        os = set(omitted_small)
        relevant = [dl for ds, dl in pieces if ds <= os]
        need(relevant and all(relevant), "surviving small case has empty large cut")
        forced_large = set().union(*(d for d in relevant if len(d) == 1))
        blockers = [sum(1 << v for v in d) for d in relevant if len(d) >= 2]
        for omitted_large in combinations(sorted(large - forced_large), large_omissions):
            lmask = sum(1 << v for v in omitted_large)
            if any(lmask & cut == cut for cut in blockers):
                continue
            candidates += 1
            whole = smask | lmask
            need(any(whole & cut == cut for cut in new_masks),
                 "uncovered blockwise deletion candidate")
    need((survivors, candidates) == (expected_small_cases, expected_candidates),
         "block family census")
    return {
        "small_omission_sets_checked": all_small,
        "surviving_small_cases": survivors,
        "large_candidates_checked": candidates,
        "remaining_candidates": 0,
    }


def rejection_controls(edges, example):
    failures = 0
    colouring = example[1]
    omitted = example[0]["D"]
    bad = colouring.replace(".", "0", 1)
    try:
        need(omitted == [v for v, c in enumerate(bad) if c == "."], "missing dot")
    except ReviewFailure:
        failures += 1
    bad = list(colouring)
    for u, v in edges:
        if colouring[u] != "." and colouring[v] != ".":
            bad[v] = bad[u]
            break
    try:
        need(all(bad[u] == "." or bad[v] == "." or bad[u] != bad[v] for u, v in edges),
             "monochromatic mutation")
    except ReviewFailure:
        failures += 1
    # A tiny incomplete positive-cut family must leave its sole avoiding pair.
    toy = [frozenset((0,))]
    uncovered = [o for o in combinations(range(3), 2) if not any(d <= set(o) for d in toy)]
    need(uncovered == [(1, 2)], "toy incomplete-cover control")
    failures += 1
    need(failures == 3, "rejection controls")
    return failures


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--repository", required=True, type=Path)
    parser.add_argument("--report", required=True, type=Path)
    args = parser.parse_args()
    repository = args.repository.resolve()

    target = repository / "hadwiger_nelson_heule517_large4"
    manifest = load(target / "manifest.json")
    observed = {name: digest(repository / name) for name in manifest}
    need(observed == manifest, "target manifest inputs")
    old, labels, points, edges, large, small, edge_hash = reconstruct_graph(repository)
    groups = witness_data(repository, old, labels, large, small)
    witness_checks = verify_witnesses(groups, edges)

    cuts = {name: [frozenset(row["D"]) for row, _ in rows] for name, rows in groups.items()}
    need(all(d <= small for d in cuts["small"]), "small certificate has a large omission")
    need(len(inclusion_antichain(cuts["prior"] + cuts["small"] + cuts["large2"] + cuts["large3"])) == 584,
         "initial large4 antichain")

    small_report = small134_cover(cuts["small"], small)
    large2_report = block_family_cover(cuts["prior"] + cuts["small"], cuts["large2"],
                                       large, small, 7, 2, 167, 870215)
    large3_report = block_family_cover(cuts["prior"] + cuts["small"] + cuts["large2"],
                                       cuts["large3"], large, small, 6, 3, 38, 749066)
    initial4 = cuts["prior"] + cuts["small"] + cuts["large2"] + cuts["large3"]
    large4_report = block_family_cover(initial4, cuts["large4"], large, small,
                                       5, 4, 94, 31695)

    initially_forced = {next(iter(d)) for d in initial4 if len(d) == 1}
    finally_forced = initially_forced | {next(iter(d)) for d in cuts["large4"] if len(d) == 1}
    need((len(initially_forced), len(initially_forced & large), len(initially_forced & small))
         == (467, 340, 127), "initial mandatory vertices")
    need((len(finally_forced), len(finally_forced & large), len(finally_forced & small))
         == (490, 362, 128), "final mandatory vertices")
    free_vertices = sorted(set(range(517)) - finally_forced)
    need(len(free_vertices) == 27, "final free vertex count")
    controls = rejection_controls(edges, groups["large4"][0])

    result = {
        "all_checks_passed": True,
        "verdict": "ACCEPTED",
        "reviewed_source_commit": "fe8f1593bcfec80c71adfc55f60b28d58428d70d",
        "scope": "fixed H517 four-large/five-small deletion family and its stated target-order corollary",
        "target_graph_claimed": False,
        "geometry": {
            "basis": "1,sqrt(3),sqrt(5),sqrt(15),sqrt(11),sqrt(33),sqrt(55),sqrt(165)",
            "denominator": 96,
            "vertices": len(points),
            "large_vertices": len(large),
            "small_vertices": len(small),
            "unordered_pair_checks": len(points) * (len(points) - 1) // 2,
            "unit_edges": len(edges),
            "edge_stream_sha256": edge_hash,
        },
        "positive_witnesses": witness_checks,
        "small134_dependency": small_report,
        "two_large_dependency": large2_report,
        "three_large_dependency": large3_report,
        "four_large_target": large4_report,
        "target_order_deduction": {
            "cases": [
                "at most 134 small: small134 positive cover",
                "135 small: at most 373 large, two-large positive cover",
                "136 small: at most 372 large, three-large positive cover",
                "137 small: at most 371 large, four-large positive cover",
            ],
            "nonfour_subgraph_on_at_most_508_needs_at_least_small": 138,
            "and_has_at_most_large": 370,
            "unrestricted_at_most_508_family_closed": False,
        },
        "mandatory_vertices": {
            "before_large4": len(initially_forced),
            "after_large4": len(finally_forced),
            "large": len(finally_forced & large),
            "small": len(finally_forced & small),
            "possible_omission_vertices": free_vertices,
        },
        "rejection_controls": controls,
        "negative_solver_result_used": False,
        "native_solver_used": False,
        "trust_boundary": [
            "exact multiquadratic source coordinates and basis independence",
            "CPython integer, Fraction, JSON and SHA-256 behavior",
            "finite-loop and witness-decoding correctness",
        ],
        "manifest_inputs": observed,
    }
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print("PASS exact H517 geometry, 955 positive witnesses, and all four cover levels")


if __name__ == "__main__":
    main()
