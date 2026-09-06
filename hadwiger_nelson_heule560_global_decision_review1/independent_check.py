#!/usr/bin/env python3
"""Independent audit of the bounded H560 global-decision certificate.

The target producer and verifier are not imported.  Exact H632 geometry is
reconstructed through the earlier reviewer's pinned quadratic-tower checker,
which is independent of the target's sparse-radical implementation.  This
script rebuilds the right-interface CNF, checks all positive and deletion
witnesses, audits the residual cylinder exhaustively, and can produce a fresh
DRAT/LRAT chain with a different solver seed.
"""

import argparse
from collections import Counter
import hashlib
import importlib.util
from itertools import combinations
import json
from math import comb
from pathlib import Path
import resource
import subprocess
import sys

sys.dont_write_bytecode = True

HERE = Path(__file__).resolve().parent
REPO = HERE.parent
TARGET = REPO / "hadwiger_nelson_heule560_global_decision"
TARGET_COMMIT = "bff36887d06f5fdbf017380148419da5ce8f0935"
TARGET_MANIFEST_SHA256 = "168f04d6f86b41effbe047555dd9b56b8e82e698328bd1ace80d402630efcef4"
GEOMETRY_CHECKER = REPO / "hadwiger_nelson_heule560_left_relation_review1" / "independent_check.py"
GEOMETRY_CHECKER_SHA256 = "1d57c4dc5d81035fea15b3ad6b82b3a336459043781b96412b2f1402c3c9da2e"
ERASED = {510, 512, 513, 520, 521, 523, 524, 535}
EXPECTED_ORACLE_SHA256 = "4682363b5c0afd715b028e2214191f2710260a5c74c29cf89934ad538df6465e"
EXPECTED_NEGATIVE_SHA256 = "bde148aa4dc1d8e1ce8a378f2168a79f19fe84d028cb4b9fd8a9cf49649ef832"


class ReviewFailure(RuntimeError):
    pass


def require(condition, message):
    if not condition:
        raise ReviewFailure(message)


def file_sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def verify_sources():
    require(file_sha256(TARGET / "SHA256SUMS") == TARGET_MANIFEST_SHA256,
            "target manifest identity")
    listed = {}
    for line in (TARGET / "SHA256SUMS").read_text(encoding="ascii").splitlines():
        digest, relative = line.split(maxsplit=1)
        listed[relative] = digest
        require(file_sha256(REPO / relative) == digest, "target file identity: " + relative)
    require(len(listed) == 12 and file_sha256(GEOMETRY_CHECKER) == GEOMETRY_CHECKER_SHA256,
            "target file set or reused geometry checker identity")
    return {"target_commit": TARGET_COMMIT, "target_files": len(listed),
            "target_manifest_sha256": TARGET_MANIFEST_SHA256,
            "geometry_checker_sha256": GEOMETRY_CHECKER_SHA256}


def load_geometry_checker():
    spec = importlib.util.spec_from_file_location("reviewed_left_geometry", GEOMETRY_CHECKER)
    require(spec is not None and spec.loader is not None, "cannot load reviewed geometry checker")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def prepare_geometry():
    reviewer = load_geometry_checker()
    left_plan = json.loads((REPO / "hadwiger_nelson_heule560_left_relation" / "plan.json").read_text())
    geometry = reviewer.reconstruct_geometry(left_plan)
    mandatory = geometry["mandatory"]
    original_optional = geometry["optional"]
    large = geometry["large"]
    small = geometry["small"]
    separator = geometry["separator"]
    right = sorted(small | set(separator))
    optional = sorted((small & original_optional) | {310})
    right_edges = [(left, right_vertex) for left, right_vertex in geometry["edges"]
                   if left in set(right) and right_vertex in set(right)]
    require(large & original_optional == ERASED | {310}, "left optional decomposition")
    require(len(mandatory) == 492 and len(original_optional) == 68, "M492/U68 partition")
    require(len(right) == 196 and len(right_edges) == 806 and len(separator) == 19,
            "right block dimensions")
    require(len(optional) == 60 and set(optional) == original_optional - ERASED,
            "G552 selector domain")
    parent = geometry["parent"]
    states = [row["state"] for row in parent["blocks"]["mandatory"]["states"]]
    full_states = {row["state"] for row in parent["blocks"]["full"]["states"]}
    require(len(states) == len(set(states)) == 72 and len(full_states) == 20,
            "imported separator relations")
    return {
        "mandatory": mandatory,
        "original_optional": original_optional,
        "large": large,
        "right": right,
        "right_edges": right_edges,
        "optional": optional,
        "separator": separator,
        "states": states,
        "full_states": full_states,
        "parent": parent,
        "edges": geometry["edges"],
    }


def selected(mask, optional):
    require(type(mask) is int and 0 <= mask < (1 << len(optional)), "selector mask domain")
    return {vertex for index, vertex in enumerate(optional) if mask & (1 << index)}


def parse_colouring(row, geometry):
    chosen = selected(row["mask"], geometry["optional"])
    support = geometry["mandatory"] | chosen
    right_support = support & set(geometry["right"])
    text = row["colouring"]
    require(type(text) is str and len(text) == len(geometry["right"]) and set(text) <= set("0123."),
            "right colouring encoding")
    colours = {vertex: colour for vertex, colour in zip(geometry["right"], text) if colour != "."}
    require(set(colours) == right_support, "right colouring support")
    state = row["state"]
    require(type(state) is str and len(state) == 19 and set(state) <= set("0123"),
            "boundary word encoding")
    require("".join(colours[vertex] for vertex in geometry["separator"]) == state,
            "right colouring boundary")
    allowed = geometry["full_states"] if 310 in chosen else set(geometry["states"])
    require(state in allowed, "boundary state is not available on the left")
    right_checks = 0
    for left, right in geometry["right_edges"]:
        if left in right_support and right in right_support:
            require(colours[left] != colours[right], "monochromatic right edge")
            right_checks += 1

    block_name = "full" if 310 in chosen else "mandatory"
    block = geometry["parent"]["blocks"][block_name]
    left_row = next(candidate for candidate in block["states"] if candidate["state"] == state)
    joined = {vertex: colour for vertex, colour in zip(block["vertices"], left_row["colouring"])
              if vertex in support}
    require(all(joined[vertex] == colours[vertex] for vertex in geometry["separator"]),
            "left/right boundary mismatch")
    joined.update(colours)
    require(set(joined) == support, "glued colouring support")
    whole_checks = 0
    for left, right in geometry["edges"]:
        if left in support and right in support:
            require(joined[left] != joined[right], "monochromatic glued edge")
            whole_checks += 1
    return chosen, right_checks, whole_checks


def build_formula(geometry, negative_rows):
    right = geometry["right"]
    position = {vertex: index for index, vertex in enumerate(right)}

    def colour_var(vertex, colour):
        return 4 * position[vertex] + colour + 1

    selectors = {vertex: 4 * len(right) + index + 1
                 for index, vertex in enumerate(geometry["optional"])}
    after_selectors = 4 * len(right) + len(selectors)
    clauses = []
    for vertex in right:
        colours = [colour_var(vertex, colour) for colour in range(4)]
        clauses.append(colours)
        clauses.extend([-left, -right_var] for left, right_var in combinations(colours, 2))
    for left, right_vertex in geometry["right_edges"]:
        guards = [-selectors[vertex] for vertex in (left, right_vertex) if vertex in selectors]
        for colour in range(4):
            clauses.append(guards + [-colour_var(left, colour), -colour_var(right_vertex, colour)])

    gates = [after_selectors + index + 1 for index in range(len(geometry["states"]))]
    clauses.append(gates)
    for gate, state in zip(gates, geometry["states"]):
        clauses.extend([[-gate, colour_var(vertex, int(colour))]
                        for vertex, colour in zip(geometry["separator"], state)])
        if state not in geometry["full_states"]:
            clauses.append([-selectors[310], -gate])
    variable_count = after_selectors + len(gates)

    if negative_rows is not None:
        case_gates = [variable_count + index + 1 for index in range(len(negative_rows))]
        clauses.append(case_gates)
        for gate, row in zip(case_gates, negative_rows):
            chosen = selected(row["mask"], geometry["optional"])
            clauses.extend([[-gate, selectors[vertex]] for vertex in geometry["optional"]
                            if vertex in chosen])
        variable_count += len(case_gates)

    raw = (f"p cnf {variable_count} {len(clauses)}\n" +
           "".join(" ".join(map(str, clause)) + " 0\n" for clause in clauses)).encode("ascii")
    return raw, variable_count, len(clauses)


def encoding_controls():
    edge_guard_checks = gate_checks = case_checks = 0
    # Guarded inequality: for every endpoint activation pattern and colour
    # pair, each of four clauses is equivalent to inactive edge or inequality.
    for selected_left in (False, True):
        for selected_right in (False, True):
            for colour_left in range(4):
                for colour_right in range(4):
                    clause_values = []
                    for tested_colour in range(4):
                        clause_values.append((not selected_left) or (not selected_right) or
                                             colour_left != tested_colour or colour_right != tested_colour)
                    require(all(clause_values) ==
                            ((not selected_left) or (not selected_right) or colour_left != colour_right),
                            "guarded edge clauses differ from induced-edge semantics")
                    edge_guard_checks += 4
    for selector_310 in (False, True):
        for gate in (False, True):
            clause = (not selector_310) or (not gate)
            require(clause == (not (selector_310 and gate)), "P20 gate restriction differs")
            gate_checks += 1
    # A true case gate requires its mask but leaves every other selector free.
    masks = ({0}, {1, 2})
    for selector_bits in range(8):
        chosen = {index for index in range(3) if selector_bits & (1 << index)}
        formula_has_gate = False
        for gate_bits in range(1, 4):
            gate_assignment_satisfies = all(
                not (gate_bits & (1 << index)) or mask <= chosen
                for index, mask in enumerate(masks)
            )
            formula_has_gate |= gate_assignment_satisfies
            case_checks += 1
        direct = any(mask <= chosen for mask in masks)
        require(formula_has_gate == direct, "case-gate semantics differs")
    return {"guarded_edge_clause_checks": edge_guard_checks,
            "p20_gate_truth_checks": gate_checks,
            "case_gate_truth_checks": case_checks}


def audit_certificate(certificate, geometry):
    require(certificate["optional_order"] == geometry["optional"] and
            certificate["right_vertices"] == geometry["right"] and
            certificate["separator"] == geometry["separator"], "certificate label orders")
    require(certificate["record_improvement"] is False and
            certificate["whole560_family_closed"] is False, "certificate scope flags")
    positives = certificate["positive_covers"]
    negatives = certificate["negative_cores"]
    positive_sets = [selected(row["mask"], geometry["optional"]) for row in positives]
    negative_sets = [selected(row["mask"], geometry["optional"]) for row in negatives]
    require(len(positives) == len({row["mask"] for row in positives}) == 35,
            "positive cover uniqueness/count")
    require(len(negatives) == len({row["mask"] for row in negatives}) == 80,
            "negative support uniqueness/count")
    require(all(not (left <= right or right <= left) for left, right in combinations(positive_sets, 2)),
            "positive rows are not an antichain")
    require(all(not (left <= right or right <= left) for left, right in combinations(negative_sets, 2)),
            "negative rows are not an antichain")
    require(not any(negative <= positive for negative in negative_sets for positive in positive_sets),
            "positive and negative cones overlap")

    right_checks = whole_checks = 0
    for row in positives:
        _, right_count, whole_count = parse_colouring(row, geometry)
        right_checks += right_count
        whole_checks += whole_count

    singleton_complements = sorted(next(iter(set(geometry["optional"]) - cover))
                                   for cover in positive_sets if len(cover) == 59)
    require(singleton_complements == [310, 393, 578], "forced singleton complements")
    require(any(cover == set(geometry["optional"]) - {310} for cover in positive_sets),
            "missing 310-absent whole-family cover")

    five_colouring = json.loads((REPO / "hadwiger_nelson_heule632_minimize" / "certificate.json").read_text())["five_colouring"]
    require(len(five_colouring) == 632 and set(five_colouring) <= set("01234."),
            "inherited five-colouring encoding")
    five_checks = 0
    for support_optional in negative_sets:
        support = geometry["mandatory"] | support_optional
        require(all(five_colouring[vertex] in "01234" for vertex in support),
                "missing inherited five-colour entry")
        for left, right in geometry["edges"]:
            if left in support and right in support:
                require(five_colouring[left] != five_colouring[right], "monochromatic inherited five-colour edge")
                five_checks += 1

    minimal_index = certificate["minimality_evidence_core_index"]
    require(minimal_index == 52 and len(negative_sets[minimal_index]) == min(map(len, negative_sets)) == 24,
            "critical-support evidence index/size")
    minimal_row = negatives[minimal_index]
    expected_critical_optional = {
        310, 358, 361, 362, 393, 406, 407, 409, 416, 431, 434, 454,
        498, 500, 539, 569, 578, 586, 596, 609, 610, 612, 613, 615,
    }
    require(negative_sets[minimal_index] == expected_critical_optional,
            "claimed 516-vertex optional support differs")
    deletion_rows = minimal_row["deletion_witnesses"]
    require([row["removed"] for row in deletion_rows] == sorted(negative_sets[minimal_index]),
            "optional deletion witness domain")
    deletion_right_checks = deletion_whole_checks = 0
    for row in deletion_rows:
        chosen, right_count, whole_count = parse_colouring(row, geometry)
        require(chosen == negative_sets[minimal_index] - {row["removed"]},
                "optional deletion witness support")
        deletion_right_checks += right_count
        deletion_whole_checks += whole_count

    oracle, oracle_variables, oracle_clauses = build_formula(geometry, None)
    combined, combined_variables, combined_clauses = build_formula(geometry, negatives)
    require(hashlib.sha256(oracle).hexdigest() == EXPECTED_ORACLE_SHA256 and
            (oracle_variables, oracle_clauses) == (916, 6017), "oracle CNF identity/dimensions")
    require(hashlib.sha256(combined).hexdigest() == EXPECTED_NEGATIVE_SHA256 and
            (combined_variables, combined_clauses) == (996, 8226), "negative CNF identity/dimensions")

    return {
        "positive_covers": len(positives),
        "positive_cover_sizes": dict(sorted(Counter(map(len, positive_sets)).items())),
        "negative_supports": len(negatives),
        "negative_support_sizes": dict(sorted(Counter(map(len, negative_sets)).items())),
        "positive_right_edge_checks": right_checks,
        "positive_whole_edge_checks": whole_checks,
        "negative_five_colour_edge_checks": five_checks,
        "forced_selectors": singleton_complements,
        "whole_310_absent_case_closed": True,
        "critical_support_index": minimal_index,
        "critical_support_vertices": 492 + len(negative_sets[minimal_index]),
        "optional_deletion_witnesses": len(deletion_rows),
        "mandatory_deletion_witnesses_imported_from_reviewed_parent": 492,
        "deletion_right_edge_checks": deletion_right_checks,
        "deletion_whole_edge_checks": deletion_whole_checks,
        "oracle_variables": oracle_variables,
        "oracle_clauses": oracle_clauses,
        "oracle_sha256": hashlib.sha256(oracle).hexdigest(),
        "negative_variables": combined_variables,
        "negative_clauses": combined_clauses,
        "negative_sha256": hashlib.sha256(combined).hexdigest(),
    }, combined, positive_sets, negative_sets


def audit_residual(residual, geometry, positive_sets, negative_sets):
    old_path = REPO / residual["old_cover_file"]
    require(file_sha256(old_path) == residual["old_cover_sha256"], "old cover file identity")
    old_rows = json.loads(old_path.read_text())["maximal_extending_cover_colourings"]
    old_sets = []
    old_edge_checks = 0
    for row in old_rows:
        omitted = set(row["omitted_optional"])
        support = geometry["mandatory"] | (geometry["original_optional"] - omitted)
        text = row["colouring"]
        require(len(text) == 632 and set(text) <= set("0123."), "old cover colouring encoding")
        colours = {vertex: text[vertex] for vertex in support}
        require(all(colour in "0123" for colour in colours.values()), "old cover colouring support")
        for left, right in geometry["edges"]:
            if left in support and right in support:
                require(colours[left] != colours[right], "monochromatic old-cover edge")
                old_edge_checks += 1
        old_sets.append(set(geometry["optional"]) - omitted)

    required = set(residual["required_vertices"])
    require(len(required) == 12 and required <= set(geometry["optional"]), "residual cylinder base")
    require(not any(required <= cover for cover in positive_sets + old_sets),
            "residual base lies in a certified positive cone")
    require(all(len(negative) > 16 for negative in negative_sets),
            "a negative cone reaches exact-16 support")
    require(residual["target_size"] == 16 and residual["cylinder_count"] == comb(48, 4) == 194580,
            "residual binomial count")

    optional = geometry["optional"]
    position = {vertex: index for index, vertex in enumerate(optional)}
    required_mask = sum(1 << position[vertex] for vertex in required)
    remaining = [vertex for vertex in optional if vertex not in required]
    positive_masks = [sum(1 << position[v] for v in cover) for cover in positive_sets + old_sets]
    negative_masks = [sum(1 << position[v] for v in support) for support in negative_sets]
    count = 0
    for extra in combinations(remaining, 4):
        mask = required_mask | sum(1 << position[vertex] for vertex in extra)
        require(mask.bit_count() == 16, "residual support cardinality")
        require(not any(mask & ~cover == 0 for cover in positive_masks),
                "enumerated residual support lies below a positive cover")
        require(not any(core & ~mask == 0 for core in negative_masks),
                "enumerated residual support lies above a negative support")
        count += 1
    require(count == residual["cylinder_count"], "exhaustive residual cylinder count")
    return {"required_vertices": sorted(required),
            "old_covers_checked": len(old_sets),
            "old_cover_edge_checks": old_edge_checks,
            "exact_508_residual_supports_exhausted": count,
            "meaning": "outside_the_published_positive_and_negative_cones_only"}


def limits():
    resource.setrlimit(resource.RLIMIT_AS, (4 * 1024**3, 4 * 1024**3))
    resource.setrlimit(resource.RLIMIT_FSIZE, (512 * 1024**2, 512 * 1024**2))


def run_native_chain(cnf_raw, work, kissat, drat_trim, lrat_check):
    require(work is not None and not work.exists(), "fresh --work directory required")
    work.mkdir(parents=True)
    cnf = work / "negative.cnf"
    proof = work / "review-seed29.drat"
    lrat = work / "review-seed29.lrat"
    cnf.write_bytes(cnf_raw)
    with (work / "kissat.log").open("wb") as log:
        solved = subprocess.run([str(kissat), "--seed=29", "--conflicts=4000000", "--time=180",
                                 str(cnf), str(proof)], stdout=log, stderr=subprocess.STDOUT,
                                timeout=200, preexec_fn=limits)
    require(solved.returncode == 20, "reviewer Kissat did not prove UNSAT")
    with (work / "drat-trim.log").open("wb") as log:
        checked = subprocess.run([str(drat_trim), str(cnf), str(proof), "-L", str(lrat)],
                                 stdout=log, stderr=subprocess.STDOUT, timeout=200, preexec_fn=limits)
    require(checked.returncode == 0 and b"s VERIFIED" in (work / "drat-trim.log").read_bytes().splitlines(),
            "drat-trim did not verify/generate LRAT")
    with (work / "lrat-check.log").open("wb") as log:
        checked = subprocess.run([str(lrat_check), str(cnf), str(lrat)],
                                 stdout=log, stderr=subprocess.STDOUT, timeout=200, preexec_fn=limits)
    require(checked.returncode == 0 and b"c VERIFIED" in (work / "lrat-check.log").read_bytes().splitlines(),
            "lrat-check did not verify")
    return {
        "review_seed": 29,
        "kissat_sha256": file_sha256(kissat),
        "drat_trim_sha256": file_sha256(drat_trim),
        "lrat_check_sha256": file_sha256(lrat_check),
        "review_drat_bytes": proof.stat().st_size,
        "review_drat_sha256": file_sha256(proof),
        "review_lrat_bytes": lrat.stat().st_size,
        "review_lrat_sha256": file_sha256(lrat),
        "drat_trim_verified": True,
        "lrat_check_verified": True,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--prove", action="store_true")
    parser.add_argument("--work", type=Path)
    parser.add_argument("--kissat", type=Path)
    parser.add_argument("--drat-trim", type=Path)
    parser.add_argument("--lrat-check", type=Path)
    args = parser.parse_args()
    if args.prove:
        require(all((args.work, args.kissat, args.drat_trim, args.lrat_check)),
                "--prove requires --work and all three native tools")

    report = {
        "status": "INDEPENDENTLY_VERIFIED_SCOPED_GLOBAL_DECISION",
        "source": verify_sources(),
        "encoding_controls": encoding_controls(),
    }
    geometry = prepare_geometry()
    certificate = json.loads((TARGET / "certificate.json").read_text())
    certificate_report, combined, positives, negatives = audit_certificate(certificate, geometry)
    report["certificate"] = certificate_report
    residual = json.loads((TARGET / "residual.json").read_text())
    report["residual"] = audit_residual(residual, geometry, positives, negatives)
    report["scope"] = {
        "record_improvement": False,
        "whole_family_closed": False,
        "target_exact_508_support_found": False,
        "timed_pilot_replayed": False,
    }
    if args.prove:
        report["native_review_proof"] = run_native_chain(
            combined, args.work, args.kissat, args.drat_trim, args.lrat_check)
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
