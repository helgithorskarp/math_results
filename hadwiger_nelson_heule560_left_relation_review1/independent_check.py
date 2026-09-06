#!/usr/bin/env python3
"""Independent exact audit of the H560 left-selector relation.

No target Python module is imported.  Geometry is reconstructed with dense
coefficient vectors, the selector lattice is rebuilt from certificate
antichains, and the combined negative CNF is encoded afresh.
"""

from collections import Counter
from fractions import Fraction
from hashlib import sha256
from itertools import combinations
import json
from math import comb, gcd
from pathlib import Path


HERE = Path(__file__).resolve().parent
REPO = HERE.parent
TARGET = REPO / "hadwiger_nelson_heule560_left_relation"
RAD = (1, 3, 5, 15, 11, 33, 55, 165)
RAD_INDEX = {radicand: index for index, radicand in enumerate(RAD)}
UNIT_SCALED = (96 * 96,) + (0,) * 7
PINNED = {
    "plan.json": "0640e6d33b4a47c010dbba7496d618e0fcd2788d4ac46e5c1faba52f80b31c49",
    "certificate.json": "e3c01e8694b4e27afe22ea633a2acbc77dae5d4268a8d0da59d7ce83f42c3a42",
    "proof_manifest.json": "fd33662c86ac6aac5f7375a4916e4b9a1a105de675dd9edb11907f7a4ac0c127",
    "expected.json": "b6e5c27cb32ed578b33742a4cb4820a01812629c234821edb27037551276572c",
}


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def scaled_point(row):
    require(len(row) == 2 and all(len(axis) == 8 for axis in row), "coordinate shape")
    axes = []
    for axis in row:
        values = []
        for coefficient in axis:
            scaled = 96 * Fraction(coefficient)
            require(scaled.denominator == 1, "coordinate is not integral at scale 96")
            values.append(scaled.numerator)
        axes.append(tuple(values))
    return tuple(axes)


def multiply_slot(i, j):
    overlap = gcd(RAD[i], RAD[j])
    reduced = RAD[i] * RAD[j] // (overlap * overlap)
    return RAD_INDEX[reduced], overlap


MUL = tuple(tuple(multiply_slot(i, j) for j in range(8)) for i in range(8))


def square_axis(axis):
    result = [0] * 8
    for i, left in enumerate(axis):
        if not left:
            continue
        for j in range(i, 8):
            right = axis[j]
            if not right:
                continue
            slot, scalar = MUL[i][j]
            result[slot] += scalar * left * right * (1 if i == j else 2)
    return result


def squared_distance(left, right):
    total = [0] * 8
    for left_axis, right_axis in zip(left, right):
        squared = square_axis(tuple(a - b for a, b in zip(left_axis, right_axis)))
        for index, value in enumerate(squared):
            total[index] += value
    return tuple(total)


def reconstruct_geometry(plan):
    for relative, expected in plan["input_files"].items():
        require(digest(REPO / relative) == expected, f"imported input hash: {relative}")

    old = json.loads((REPO / "hadwiger_nelson_parts509_heule_union_minimum/certificate_H510.json").read_text())
    labels = [v for v in sorted(map(int, old["coordinates"])) if "510" in old["provenance"][v]]
    fresh = json.loads((REPO / "hadwiger_nelson_heule510_completion_frontier/fresh_candidates.json").read_text())
    points = [scaled_point(old["coordinates"][str(v)]) for v in labels]
    points.extend(scaled_point(row["coordinates"]) for row in fresh)
    require(len(labels) == 510 and len(points) == 632 and len(set(points)) == 632,
            "host point domain")

    host_edges = []
    for u in range(632):
        for v in range(u + 1, 632):
            if squared_distance(points[u], points[v]) == UNIT_SCALED:
                host_edges.append((u, v))
    require(len(host_edges) == 3112, "host exact edge count")

    boundary = json.loads((REPO / "hadwiger_nelson_heule632_minimize/boundary.json").read_text())
    mandatory = set(boundary["mandatory_vertices"])
    optional = set(boundary["optional_vertices"])
    vertices = mandatory | optional
    require(len(mandatory) == 492 and len(optional) == 68 and len(vertices) == 560,
            "H560 partition")
    large = {
        v for v in vertices
        if all(all(not coefficient or RAD[index] % 5 for index, coefficient in enumerate(axis))
               for axis in points[v])
    }
    small = vertices - large
    edges = [(u, v) for u, v in host_edges if u in vertices and v in vertices]
    cross = [(u, v) if u in large else (v, u) for u, v in edges if (u in large) != (v in large)]
    separator = sorted({u for u, _ in cross})
    left_optional = sorted(large & optional)
    require(len(large) == 383 and len(separator) == 19 and len(cross) == 33,
            "large-block separator")
    require(left_optional == plan["optional_order"], "left optional order")

    parent = json.loads((REPO / "hadwiger_nelson_heule560_separator/certificate.json").read_text())
    require(parent["separator"] == separator, "parent separator differs")
    require(parent["blocks"]["full"]["vertices"] == sorted(large), "parent full block differs")
    require(parent["blocks"]["mandatory"]["vertices"] == sorted(large & mandatory),
            "parent mandatory block differs")
    return {
        "points": points,
        "host_edges": host_edges,
        "edges": edges,
        "mandatory": mandatory,
        "optional": optional,
        "large": large,
        "small": small,
        "separator": separator,
        "left_optional": left_optional,
        "parent": parent,
    }


def mask_vertices(mask, optional):
    require(isinstance(mask, int) and 0 <= mask < 1 << len(optional), "selector mask")
    return {vertex for bit, vertex in enumerate(optional) if mask & (1 << bit)}


def check_colouring(text, ordered_vertices, support, edges, separator, state):
    require(len(text) == len(ordered_vertices) and set(text) <= set("0123."), "colour string")
    colour = {vertex: symbol for vertex, symbol in zip(ordered_vertices, text) if symbol != "."}
    require(set(colour) == support, "colour support")
    require("".join(colour[vertex] for vertex in separator) == state, "boundary state")
    checked = 0
    for u, v in edges:
        if u in support and v in support:
            require(colour[u] != colour[v], "monochromatic exact unit edge")
            checked += 1
    return checked


def reconstruct_cnf(geometry, cases):
    vertices = sorted(geometry["large"])
    optional = geometry["left_optional"]
    position = {vertex: index for index, vertex in enumerate(vertices)}

    def colour_var(vertex, colour):
        return 4 * position[vertex] + colour + 1

    selector = {vertex: 4 * len(vertices) + bit + 1 for bit, vertex in enumerate(optional)}
    clauses = []
    for vertex in vertices:
        colours = [colour_var(vertex, colour) for colour in range(4)]
        clauses.append(colours)
        clauses.extend((-left, -right) for left, right in combinations(colours, 2))
    for u, v in geometry["edges"]:
        if u not in position or v not in position:
            continue
        guards = []
        if u in selector:
            guards.append(-selector[u])
        if v in selector:
            guards.append(-selector[v])
        for colour in range(4):
            clauses.append(tuple(guards + [-colour_var(u, colour), -colour_var(v, colour)]))

    top = 4 * len(vertices) + len(optional)
    clauses.append(tuple(top + case + 1 for case in range(len(cases))))
    for case, (state, mask) in enumerate(cases):
        gate = top + case + 1
        for index, vertex in enumerate(geometry["separator"]):
            clauses.append((-gate, colour_var(vertex, int(state[index]))))
        selected = mask_vertices(mask, optional)
        for vertex in optional:
            if vertex in selected:
                clauses.append((-gate, selector[vertex]))

    variables = top + len(cases)
    payload = bytearray(f"p cnf {variables} {len(clauses)}\n", "ascii")
    for clause in clauses:
        payload.extend((" ".join(map(str, clause)) + " 0\n").encode("ascii"))
    return bytes(payload), variables, len(clauses)


def audit_relation(certificate, geometry, manifest):
    optional = geometry["left_optional"]
    separator = geometry["separator"]
    ordered_left = sorted(geometry["large"])
    mandatory_left = geometry["large"] & geometry["mandatory"]
    require(certificate["optional_order"] == optional and certificate["separator"] == separator,
            "certificate labeling")
    require(certificate["record_improvement"] is False and
            certificate["whole560_family_closed"] is False, "scope flags")

    parent_mandatory = geometry["parent"]["blocks"]["mandatory"]["states"]
    parent_full_rows = geometry["parent"]["blocks"]["full"]["states"]
    parent_states = [row["state"] for row in parent_mandatory]
    full = {row["state"]: row for row in parent_full_rows}
    require(parent_states == sorted(set(parent_states)) and len(parent_states) == 72 and len(full) == 20,
            "parent state sets")
    require([row["state"] for row in certificate["rows"]] == parent_states, "target state domain")

    all_subsets = [mask_vertices(mask, optional) for mask in range(512)]
    table = []
    cases = []
    positive_checks = minimality_checks = maximality_checks = 0
    for row in certificate["rows"]:
        state = row["state"]
        inherited = state in full
        require(row["inherited_full"] is inherited, "inherited-state tag")
        if inherited:
            positive_checks += check_colouring(
                full[state]["colouring"], ordered_left, set(ordered_left),
                geometry["edges"], separator, state)
            require("positive_covers" not in row and "negative_masks" not in row,
                    "inherited row carries new antichains")
            table.append([True] * 512)
            continue

        positive_masks = [cover["mask"] for cover in row["positive_covers"]]
        negative_masks = row["negative_masks"]
        require(positive_masks == sorted(set(positive_masks)) and
                negative_masks == sorted(set(negative_masks)), "noncanonical antichain")
        positive_sets = [mask_vertices(mask, optional) for mask in positive_masks]
        negative_sets = [mask_vertices(mask, optional) for mask in negative_masks]
        require(all(not (a <= b or b <= a) for a, b in combinations(positive_sets, 2)),
                "positive masks are not an antichain")
        require(all(not (a <= b or b <= a) for a, b in combinations(negative_sets, 2)),
                "negative masks are not an antichain")

        for cover, support_optional in zip(row["positive_covers"], positive_sets):
            positive_checks += check_colouring(
                cover["colouring"], ordered_left, mandatory_left | support_optional,
                geometry["edges"], separator, state)
        truth = []
        for subset in all_subsets:
            good = any(subset <= cover for cover in positive_sets)
            bad = any(forbidden <= subset for forbidden in negative_sets)
            require(good != bad, "selector lattice is not completely partitioned")
            truth.append(good)
        for forbidden in negative_sets:
            for vertex in forbidden:
                require(any(forbidden - {vertex} <= cover for cover in positive_sets),
                        "negative mask is not minimal")
                minimality_checks += 1
        for cover in positive_sets:
            for vertex in set(optional) - cover:
                require(any(forbidden <= cover | {vertex} for forbidden in negative_sets),
                        "positive mask is not maximal")
                maximality_checks += 1
        cases.extend((state, mask) for mask in negative_masks)
        table.append(truth)

    relevant = []
    for bit, vertex in enumerate(optional):
        if any(row[mask] != row[mask ^ (1 << bit)] for row in table for mask in range(512)):
            relevant.append(vertex)
    require(relevant == [310], "relation depends on more than vertex 310")
    for state, truth in zip(parent_states, table):
        for mask, subset in enumerate(all_subsets):
            require(truth[mask] == (state in full or 310 not in subset), "one-switch formula")

    stream = "".join("".join("1" if value else "0" for value in row) + "\n" for row in table).encode()
    cnf, variables, clauses = reconstruct_cnf(geometry, cases)
    require(sha256(stream).hexdigest() ==
            "1458e9587a41c25a713cc821be1591a09b44b9b1bd443f5f13fcfa0accfa4ab9",
            "truth table hash")
    require(sha256(cnf).hexdigest() == manifest["cnf_sha256"] and len(cnf) == manifest["cnf_bytes"],
            "independent CNF identity")
    require((len(cases), variables, clauses) ==
            (manifest["cases"], manifest["variables"], manifest["clauses"]), "CNF dimensions")

    relation_words = ["".join("1" if row[mask] else "0" for row in table) for mask in range(512)]
    classes = Counter(relation_words)
    state_counts = Counter(sum(row[mask] for row in table) for mask in range(512))
    return {
        "states": len(table),
        "masks": 512,
        "state_mask_pairs": len(table) * 512,
        "true_pairs": sum(sum(row) for row in table),
        "false_pairs": len(table) * 512 - sum(sum(row) for row in table),
        "positive_unit_edge_checks": positive_checks,
        "negative_cases": len(cases),
        "minimality_checks": minimality_checks,
        "maximality_checks": maximality_checks,
        "relevant_optional_vertices": relevant,
        "irrelevant_optional_vertices": sorted(set(optional) - set(relevant)),
        "distinct_boundary_relations": len(classes),
        "equivalence_class_sizes": sorted(classes.values()),
        "state_count_census": {str(key): value for key, value in sorted(state_counts.items())},
        "table_sha256": sha256(stream).hexdigest(),
        "negative_cnf_sha256": sha256(cnf).hexdigest(),
        "negative_cnf_variables": variables,
        "negative_cnf_clauses": clauses,
        "negative_cnf_bytes": len(cnf),
    }


def audit_family_consequence(geometry):
    erased = {510, 512, 513, 520, 521, 523, 524, 535}
    retained = (geometry["mandatory"] | geometry["optional"]) - erased
    retained_edges = [(u, v) for u, v in geometry["edges"] if u in retained and v in retained]
    old = json.loads((REPO / "hadwiger_nelson_heule632_minimize/certificate.json").read_text())
    colouring = old["five_colouring"]
    require(len(colouring) == 632, "inherited five-colouring length")
    require(all(colouring[u] != colouring[v] for u, v in retained_edges),
            "inherited five-colouring is improper on G552")
    require(len(retained) == 552 and len(retained_edges) == 2726, "G552 order or size")
    without_310 = comb(59, 16)
    with_310 = comb(59, 15)
    require(without_310 + with_310 == comb(60, 16), "two-case support partition")
    return {
        "reduced_support_vertices": len(retained),
        "reduced_support_edges": len(retained_edges),
        "inherited_five_colour_edge_checks": len(retained_edges),
        "remaining_optional_vertices": 60,
        "original_exact_508_support_count": comb(68, 16),
        "canonical_exact_508_support_count": comb(60, 16),
        "without_310_exact_508_support_count": without_310,
        "with_310_exact_508_support_count": with_310,
    }


def main():
    for filename, expected in PINNED.items():
        require(digest(TARGET / filename) == expected, f"target file hash: {filename}")
    plan = json.loads((TARGET / "plan.json").read_text())
    certificate = json.loads((TARGET / "certificate.json").read_text())
    manifest = json.loads((TARGET / "proof_manifest.json").read_text())
    geometry = reconstruct_geometry(plan)
    result = {
        "status": "INDEPENDENTLY_VERIFIED_SCOPED_INTERMEDIATE_RESULT",
        "geometry": {
            "host_vertices": len(geometry["points"]),
            "host_pairs_checked": 632 * 631 // 2,
            "host_unit_edges": len(geometry["host_edges"]),
            "h560_vertices": len(geometry["mandatory"] | geometry["optional"]),
            "large_block_vertices": len(geometry["large"]),
            "separator_vertices": len(geometry["separator"]),
            "cross_edges": sum((u in geometry["large"]) != (v in geometry["large"])
                               for u, v in geometry["edges"]),
        },
        "relation": audit_relation(certificate, geometry, manifest),
        "family_consequence": audit_family_consequence(geometry),
        "proof_boundary": {
            "drat_sha256": manifest["proof_sha256"],
            "drat_bytes": manifest["proof_bytes"],
            "drat_replay_in_this_script": False,
        },
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
