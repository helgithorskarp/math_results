#!/usr/bin/env python3
"""Independent checker for the Core194 empty-blue-pair lemma and case split.

This file imports no module from the reviewed contribution.  It reconstructs
the physical primary-variable map, exhaustively checks the local graph claim,
checks the literal fixtures and certificate, parses the full inherited CNF,
and independently emits the two claimed child formulas.
"""
from itertools import combinations, product
from pathlib import Path
import argparse
import hashlib
import json
import shutil


WORD = "100110110110110100"
BASE = {
    "bytes": 24_968_424,
    "sha256": "214cbdad727ec3f48e97e62246134b341719277981119bd6b89baa5475b2dbb4",
}
CHILDREN = {
    "blue": {
        "bytes": 24_968_511,
        "sha256": "21b9a5e9d4b4ddb9e91388abf6bc45d87488f356adbcbc70fb60d752ad5f13e1",
        "clauses": 617_945,
    },
    "red": {
        "bytes": 24_968_430,
        "sha256": "941df55fb7a26c64b1e72dfdff819d3cad15409a5eb83521a57ac2e353562224",
        "clauses": 617_937,
    },
}
SOURCE_FILES = {
    "SHA256SUMS": "df0d660b46bc1d71449f4aa3f6671e317a3536fb564d246511052ed9ca3aedd8",
    "certificate.json": "2d79294b8ac0d5079b14e1afde77d9cdc5889dc732b51e56d637f946385d1746",
    "cases.json": "96c37b92fe77aac389398d82430ac5ecdda018ecbe47689e6efb53f4d3434752",
    "blue_pair14.edges": "3101276f4d277e534e73d95f7ac5f5803daf999449df3678e08846e255552a4a",
    "red_pair15.edges": "9ba40ea39112b462cf9d169cb29adf760a1012811c9d5229fb2c3a5709b3acd0",
    "result.json": "8cc1a431546b7d5ba1f9fc819dcc48e7728b6647466036c6850535ba199b39a9",
    "boundary.json": "50434529beb914e06cfbdd14d1d480e70082d9d0603805e80d88cb7203ca9149",
}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def file_info(path):
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while block := stream.read(1 << 20):
            digest.update(block)
    return {"bytes": path.stat().st_size, "sha256": digest.hexdigest()}


def check_source(target):
    observed = {}
    for name, expected in SOURCE_FILES.items():
        got = file_info(target / name)["sha256"]
        require(got == expected, f"reviewed source drift: {name}")
        observed[name] = got
    return observed


def rotate(v):
    return v if v >= 33 else 3 * (v // 3) + (v + 1) % 3


def primary_map():
    """Recover all 320 primary meanings from edge orbits, not submitted code."""
    unused = set(combinations(range(43), 2))
    moving, fixed, incidence = [], [], []
    while unused:
        edge = min(unused)
        orbit = {edge}
        image = tuple(sorted(map(rotate, edge)))
        while image != edge:
            orbit.add(image)
            image = tuple(sorted(map(rotate, image)))
        unused -= orbit
        a, b = min(orbit)
        if b < 33 and a // 3 != b // 3:
            moving.append((min(orbit), orbit))
        elif a >= 33:
            fixed.append((min(orbit), orbit))
        elif b >= 33:
            incidence.append((min(orbit), orbit))
    moving.sort(key=lambda row: (row[0][0] // 3, row[0][1] // 3,
                                 (row[0][1] - row[0][0]) % 3))
    fixed.sort()
    incidence.sort(key=lambda row: (row[0][1], row[0][0] // 3))
    orbits = moving + fixed + incidence
    require([len(moving), len(fixed), len(incidence)] == [165, 45, 110],
            "unexpected orbit-type counts")
    answer = {edge: index for index, (_, orbit) in enumerate(orbits, 1)
              for edge in orbit}
    # The 33 within-cycle edges are fixed red and hence have no primary.
    require(len(answer) == 870 and max(answer.values()) == 320,
            "incomplete edge-to-primary map")
    return answer


def core_red_edges(ids):
    core_ids = list(range(1, 10)) + list(range(31, 37)) + list(range(58, 61))
    red_primary = {index for index, bit in zip(core_ids, WORD) if bit == "1"}
    return {
        edge for edge in combinations(range(12), 2)
        if edge[0] // 3 == edge[1] // 3 or ids[edge] in red_primary
    }


def monochromatic_fives(vertices, red):
    rows = []
    for subset in combinations(vertices, 5):
        colors = {edge in red for edge in combinations(subset, 2)}
        if len(colors) == 1:
            rows.append(("red" if True in colors else "blue", subset))
    return rows


def exhaustive_local(target, ids):
    """Check all sixteen possible uniform signatures of a third fixed point."""
    core = core_red_edges(ids)
    cert = json.loads((target / "certificate.json").read_text())
    require(cert["index"] == 194 and cert["bits"] == WORD,
            "certificate identifies another core")
    require(cert["empty_pair"] == [12, 13] and cert["third_fixed"] == 14,
            "certificate uses other local vertices")
    submitted = cert["forbidden_common_blue_signatures"]
    require([row["mask"] for row in submitted] == list(range(16)),
            "certificate does not cover each signature exactly once")

    classes = {"blue": 0, "red": 0}
    total_fives = 0
    submitted_pairs = 0
    derived = []
    for mask, row in enumerate(submitted):
        red = set(core)
        red.update((a, 14) for a in range(12) if mask & (1 << (a // 3)))
        witnesses = monochromatic_fives(range(15), red)
        total_fives += len(list(combinations(range(15), 5)))
        require(witnesses, f"signature {mask} has no obstruction")
        colors = {color for color, _ in witnesses}
        expected_color = "red" if mask.bit_count() >= 3 else "blue"
        require(expected_color in colors,
                f"signature {mask} lacks its structural obstruction")
        classes[expected_color] += 1

        vertices = tuple(row["vertices"])
        require(len(vertices) == 5 and len(set(vertices)) == 5,
                f"malformed certificate witness {mask}")
        require((row["color"], vertices) in witnesses,
                f"certificate witness {mask} is not monochromatic")
        require(row["color"] == expected_color,
                f"certificate witness {mask} has wrong structural color")
        submitted_pairs += len(list(combinations(vertices, 2)))
        derived.append({"mask": mask, "color": expected_color,
                        "lexicographic_witness": list(next(q for c, q in witnesses
                                                           if c == expected_color))})

    require(classes == {"blue": 11, "red": 5}, "wrong signature partition")
    encoded = json.dumps(derived, sort_keys=True, separators=(",", ":")).encode()
    k4_by_omitted_triangle = {
        str(omitted): next(row["lexicographic_witness"][:4] for row in derived
                           if row["mask"] == 15 - (1 << omitted))
        for omitted in range(4)
    }
    return {
        "signatures_exhausted": 16,
        "five_vertex_subsets_examined": total_fives,
        "obstruction_classes": classes,
        "submitted_witness_pairs_checked": submitted_pairs,
        "derived_witness_table_sha256": hashlib.sha256(encoded).hexdigest(),
        "red_k4_by_omitted_triangle": k4_by_omitted_triangle,
    }


def read_fixture(path):
    lines = path.read_text().splitlines()
    require(lines, "empty fixture")
    n = int(lines[0])
    edges = [tuple(map(int, line.split())) for line in lines[1:]]
    require(len(edges) == len(set(edges)), "duplicate fixture edge")
    require(all(0 <= a < b < n for a, b in edges), "invalid fixture edge")
    return n, set(edges)


def check_fixture(path, expected_n, pair_red, ids):
    n, red = read_fixture(path)
    require(n == expected_n, "wrong fixture order")
    require({edge for edge in red if edge[1] < 12} == core_red_edges(ids),
            "fixture changes Core194")
    require(all((a, f) not in red for a in range(12) for f in range(12, n)),
            "fixture fixed vertex is not empty")
    require(((12, 13) in red) == pair_red, "wrong empty-pair color")
    mono = monochromatic_fives(range(n), red)
    require(not mono, "fixture contains a monochromatic K5")
    common = [w for w in range(n) if w not in (12, 13)
              and tuple(sorted((12, w))) not in red
              and tuple(sorted((13, w))) not in red]
    expected_common = list(range(12)) + ([] if n == 14 else [14])
    require(common == expected_common, "wrong literal common-blue neighborhood")
    def local_rotate(v):
        return v if v >= 12 else 3 * (v // 3) + (v + 1) % 3
    for edge in combinations(range(n), 2):
        image = tuple(sorted(map(local_rotate, edge)))
        require((edge in red) == (image in red), "fixture breaks core rotation")
    return {
        "vertices": n,
        "red_edges": len(red),
        "five_vertex_subsets_checked": len(list(combinations(range(n), 5))),
        "common_blue_neighbors_of_pair": common,
        "pair_color": "red" if pair_red else "blue",
    }


def expected_tail(case, ids):
    pair = ids[(33, 34)]
    if case == "red":
        return [(pair,)]
    return [(-pair,)] + [(ids[(33, f)], ids[(34, f)]) for f in range(35, 43)]


def scan_base(base, ids):
    require(file_info(base) == BASE, "inherited multiple-empty base identity differs")
    empty_units = {(-ids[(3 * cycle, fixed)],) for fixed in (33, 34)
                   for cycle in range(4)}
    moving_guards = {(ids[(33, 34)], ids[(3 * cycle, 33)], ids[(3 * cycle, 34)])
                     for cycle in range(4, 11)}
    units_found, guards_found = set(), set()
    clauses = 0
    with base.open() as stream:
        require(stream.readline().strip() == "p cnf 34320 617936", "wrong base header")
        for line in stream:
            literals = tuple(map(int, line.split()))
            require(literals and literals[-1] == 0, "malformed DIMACS clause")
            clause = literals[:-1]
            clauses += 1
            if clause in empty_units:
                units_found.add(clause)
            if clause in moving_guards:
                guards_found.add(clause)
    require(clauses == 617_936, "base clause count differs")
    require(units_found == empty_units, "missing empty-signature units")
    require(guards_found == moving_guards, "missing blue-cycle guard clauses")
    return {
        "variables": 34_320,
        "clauses_parsed": clauses,
        "empty_units_found": sorted(row[0] for row in units_found),
        "moving_cycle_guards_found": len(guards_found),
        "identity": BASE,
    }


def make_child(base, output, case, ids):
    tail = expected_tail(case, ids)
    with base.open("rb") as source, output.open("wb") as child:
        require(source.readline() == b"p cnf 34320 617936\n", "base header differs")
        child.write(f"p cnf 34320 {617_936 + len(tail)}\n".encode())
        shutil.copyfileobj(source, child)
        for clause in tail:
            child.write((" ".join(map(str, clause)) + " 0\n").encode())
    observed = file_info(output)
    require(observed == {k: CHILDREN[case][k] for k in ("bytes", "sha256")},
            f"{case} child identity differs")
    return {"tail": [list(row) for row in tail], "formula": observed,
            "variables": 34_320, "clauses": CHILDREN[case]["clauses"]}


def exhaustive_partition():
    blue = red = overlap = missed = 0
    for pair_red, contacts in product((False, True), product((False, True), repeat=16)):
        premise = pair_red or all(contacts[2 * k] or contacts[2 * k + 1]
                                  for k in range(8))
        in_red = pair_red
        in_blue = not pair_red and all(contacts[2 * k] or contacts[2 * k + 1]
                                       for k in range(8))
        require((in_red or in_blue) == premise,
                "children do not exhaust guarded assignments")
        overlap += in_red and in_blue
        missed += premise and not (in_red or in_blue)
        red += in_red
        blue += in_blue
    require((blue, red, overlap, missed) == (3 ** 8, 2 ** 16, 0, 0),
            "incorrect case truth table")
    return {"assignments_checked": 2 ** 17, "blue_child": blue,
            "red_child": red, "overlap": overlap, "missed": missed}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--target", type=Path, required=True)
    parser.add_argument("--base", type=Path, required=True)
    parser.add_argument("--work", type=Path, required=True)
    parser.add_argument("--report", type=Path, required=True)
    args = parser.parse_args()
    args.work.mkdir(parents=True, exist_ok=True)
    ids = primary_map()
    cases = json.loads((args.target / "cases.json").read_text())
    require(cases == [{"id": "blue", "index": 194, "pair_red": False},
                      {"id": "red", "index": 194, "pair_red": True}],
            "cases are not the complete literal pair-color split")
    require(ids[(33, 34)] == 166, "pair variable is not primary 166")

    local = exhaustive_local(args.target, ids)
    fixtures = {
        "blue_guarded": check_fixture(args.target / "blue_pair14.edges", 14, False, ids),
        "red_guard_counterexample": check_fixture(args.target / "red_pair15.edges", 15, True, ids),
    }
    base = scan_base(args.base, ids)
    children = {case: make_child(args.base, args.work / f"{case}.cnf", case, ids)
                for case in ("blue", "red")}
    answer = {
        "reviewed_source": check_source(args.target),
        "primary_orbits": {"moving": 165, "fixed": 45, "incidence": 110,
                            "total": 320, "empty_pair_primary": 166},
        "local_lemma": local,
        "fixtures": fixtures,
        "full_formula_base": base,
        "children": children,
        "guarded_partition": exhaustive_partition(),
        "exact_common_blue_neighbors": {
            "red_core_vertices": 12,
            "other_fixed_excluded_by_local_lemma": 8,
            "blue_cycle_vertices_excluded_by_blue_K5": 21,
            "total": 12,
        },
        "solver_claims_reproduced": False,
        "solver_scope_note": "Both submitted child solves are UNKNOWN and have no proving force.",
    }
    args.report.write_text(json.dumps(answer, indent=2, sort_keys=True) + "\n")
    print("PASS independent Core194 empty-pair lemma and complete formula split")


if __name__ == "__main__":
    main()
