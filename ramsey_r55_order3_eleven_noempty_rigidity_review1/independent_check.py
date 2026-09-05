#!/usr/bin/env python3
"""Independent hand-reduction, literal-obstruction, formula and replay audit.

No module from the reviewed no-empty package is imported.  The code relies on
the hand implications rather than repeating its 39,105-profile enumerators.
"""
from itertools import combinations
from pathlib import Path
import argparse
import hashlib
import json
import re


BASE_HASH = "f3a99ee8b211cfcf134f26670ada6fcdce9dc765b92dce3812a5bfdb16f971eb"
PAIR_MASKS = (3, 5, 6, 9, 10, 12)


def need(condition, message):
    if not condition:
        raise ValueError(message)


def digest(path):
    h = hashlib.sha256()
    with path.open("rb") as stream:
        while block := stream.read(1 << 20):
            h.update(block)
    return {"bytes": path.stat().st_size, "sha256": h.hexdigest()}


def core_red_edges(bits):
    pairs = list(combinations(range(4), 2))
    red = set()
    for a, b in combinations(range(12), 2):
        i, s = divmod(a, 3)
        j, t = divmod(b, 3)
        if i == j or bits[3 * pairs.index((i, j)) + (t - s) % 3] == "1":
            red.add((a, b))
    return red


def complement_data(bits):
    red = core_red_edges(bits)
    need(all(0 < sum(edge in red for edge in combinations(five, 2)) < 10
             for five in combinations(range(12), 5)), "invalid local core")
    good = []
    witnesses = {}
    for omitted in range(4):
        vertices = [v for v in range(12) if v // 3 != omitted]
        has_blue_triangle = any(
            all(edge not in red for edge in combinations(triple, 2))
            for triple in combinations(vertices, 3)
        )
        if not has_blue_triangle:
            good.append(omitted)
            red_four = next((four for four in combinations(vertices, 4)
                             if all(edge in red for edge in combinations(four, 2))), None)
            need(red_four is not None, "blue-free complement has no displayed red K4")
            witnesses[omitted] = list(red_four)
    return red, good, witnesses


def hand_closure(cores):
    histogram = {}
    closed = []
    deductions = []
    for row in cores:
        red, good, witnesses = complement_data(row["bits"])
        need(good == row["good"], f"complement classification c{row['index']}")
        need(row["singletons"] == [1 + int(i in good) for i in range(4)],
             f"singleton counts c{row['index']}")
        saved_witnesses = {entry["omitted"]: entry["red_k4"] for entry in row["red_k4_witnesses"]}
        need(saved_witnesses == witnesses, f"red K4 witnesses c{row['index']}")
        g = len(good)
        histogram[str(g)] = histogram.get(str(g), 0) + 1
        if g == 1:
            a = good[0]
            others = [i for i in range(4) if i != a]
            # Omitting b gives x_a+y_ab=2, so y_ab=0 because x_a=2.
            x_a = 1 + int(a in good)
            zero_pairs = {sum(1 << i for i in (a, b)): 2 - x_a for b in others}
            need(x_a == 2 and set(zero_pairs.values()) == {0}, "g=1 zero pairs")
            # For each triple containing a, omit one of its non-a indices and
            # use its already-zero complementary pair in y_jk+t_ijk=1.
            triples = {}
            for triple_tuple in combinations(range(4), 3):
                if a not in triple_tuple:
                    continue
                omitted = next(i for i in triple_tuple if i != a)
                pair_tuple = tuple(i for i in triple_tuple if i != omitted)
                pair_mask = sum(1 << i for i in pair_tuple)
                triples[sum(1 << i for i in triple_tuple)] = 1 - zero_pairs[pair_mask]
            need(len(zero_pairs) == len(triples) == 3, "g=1 deduction")
            need(set(triples.values()) == {1} and x_a + sum(triples.values()) == 5,
                 "g=1 incidence contradiction")
            deductions.append({"index": row["index"], "case": "one",
                               "singleton": a, "zero_pair_masks": sorted(zero_pairs),
                               "forced_triple_masks": sorted(triples),
                               "incidence_lower_bound": 5})
            closed.append(row["index"])
        elif g == 2:
            a, b = good
            c, d = [i for i in range(4) if i not in good]
            # Omitting c: x_a+y_ac=2 gives y_ac=0.  Omitting d:
            # y_ac+t_acd=1 gives t_acd=1.  The red K4 on complement b
            # simultaneously forces t_acd=0.
            pair = (1 << a) | (1 << c)
            triple = (1 << a) | (1 << c) | (1 << d)
            y_ac = 2 - (1 + int(a in good))
            projected_triple = 1 - y_ac
            red_k4_triple = 0
            need(triple == 15 ^ (1 << b), "g=2 complementary triple")
            need(y_ac == 0 and projected_triple == 1 and red_k4_triple == 0,
                 "g=2 equality contradiction")
            deductions.append({"index": row["index"], "case": "two",
                               "zero_pair_mask": pair,
                               "contradictory_triple_mask": triple,
                               "red_k4": witnesses[b]})
            closed.append(row["index"])
        else:
            need(g == 4 and row["index"] == 194, "unexpected complement type")
    need(histogram == {"1": 7, "2": 18, "4": 1}, "complement histogram")
    need(len(closed) == 25, "hand-closed core count")
    return histogram, closed, deductions


def expected_profiles():
    return sorted(sorted([1, 1, 2, 2, 4, 4, 8, 8, p, q])
                  for p, q in combinations(PAIR_MASKS, 2))


def check_literal_obstructions(certificate, classification):
    need(certificate["core"] == 194 and certificate["bits"] == "100110110110110100",
         "certificate core")
    core = next(row for row in classification["cores"] if row["index"] == 194)
    profiles = expected_profiles()
    need(core["profiles"] == profiles and len(profiles) == 15, "profile cover")
    red = core_red_edges(core["bits"])
    constructed = []
    for number, (record, profile) in enumerate(zip(certificate["cases"], profiles)):
        need(record["index"] == number and sorted(record["fixed_masks"]) == profile,
             f"certificate profile {number}")
        masks = record["fixed_masks"]
        pair = min(mask for mask in masks if mask.bit_count() == 2)
        i = min(j for j in range(4) if pair >> j & 1)
        fixed = [12 + position for position, mask in enumerate(masks)
                 if mask in (1 << i, pair)]
        need(len(fixed) == 3, f"three fixed vertices {number}")
        outside = [j for j in range(4) if not (pair >> j & 1)]
        blue_edge = next(((a, b)
                          for a in range(3 * outside[0], 3 * outside[0] + 3)
                          for b in range(3 * outside[1], 3 * outside[1] + 3)
                          if tuple(sorted((a, b))) not in red), None)
        need(blue_edge is not None, f"blue cross edge {number}")
        five = sorted(fixed + list(blue_edge))
        # Fixed-fixed edges are forced blue by the internally red triangle Ci.
        forced = {tuple(sorted(edge)) for edge in combinations(fixed, 2)}
        for edge in combinations(five, 2):
            edge = tuple(sorted(edge))
            if edge in forced or edge == tuple(sorted(blue_edge)):
                continue
            a, b = edge
            fixed_vertex = b if b >= 12 else a
            core_vertex = a if a < 12 else b
            need(not (masks[fixed_vertex - 12] >> (core_vertex // 3) & 1),
                 f"nonblue attachment in obstruction {number}")
        need(record["blue_k5"] == five, f"published blue K5 {number}")
        published_forced = {tuple(sorted(entry["edge"])) for entry in record["forced_blue"]}
        need(published_forced == forced, f"published forced edges {number}")
        constructed.append(five)
    return {"profiles": 15, "constructed_blue_k5": len(constructed),
            "forced_fixed_edges": 45}


def check_formula(base, formula, case):
    words = sorted(tuple(bool(mask >> i & 1) for i in range(4)) for mask in case["masks"])
    units = []
    for fixed, word in zip(range(33, 43), words):
        for cycle, bit in enumerate(word):
            variable = 211 + 11 * (fixed - 33) + cycle
            units.append(variable if bit else -variable)
    with base.open() as source, formula.open() as target:
        need(source.readline() == "p cnf 34320 616138\n", "base header")
        need(target.readline() == "p cnf 34320 616178\n", "formula header")
        for line in source:
            need(target.readline() == line, "complete base mismatch")
        for unit in units:
            need(target.readline() == f"{unit} 0\n", "signature unit mismatch")
        need(target.read() == "", "formula suffix")


def proof_record(work, published):
    index = published["index"]
    proof = work / f"p{index:02}.review1.drat"
    replay = work / f"p{index:02}.review1.replay.log"
    proof_info = digest(proof)
    need(proof_info == published["proof"], f"proof identity p{index:02}")
    text = replay.read_text(errors="replace")
    need("s VERIFIED" in text, f"proof replay p{index:02}")
    hit = re.search(r"(\d+) RAT lemmas in core", text)
    need(hit is not None and int(hit.group(1)) == 0, f"zero RAT p{index:02}")
    return {"index": index, "proof": proof_info, "verified": True, "rat_core_lemmas": 0}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--work", type=Path, required=True)
    parser.add_argument("--kissat", type=Path, required=True)
    parser.add_argument("--drat-trim", type=Path, required=True)
    parser.add_argument("--report", type=Path, required=True)
    args = parser.parse_args()
    source = args.source.resolve()
    work = args.work.resolve()
    classification = json.loads((source / "classification.json").read_text())
    certificate = json.loads((source / "local_obstructions.json").read_text())
    result = json.loads((source / "result.json").read_text())
    propagation = json.loads((source.parent / "ramsey_r55_order3_eleven_anchor_propagation" / "result.json").read_text())
    residual = [row for row in propagation["cases"] if row["status"] == "open"]
    need([row["index"] for row in classification["cores"]] ==
         [row["index"] for row in residual], "26-core inherited boundary")
    need(all(all(row[key] == old[key] for key in ("index", "bits", "labeled"))
             for row, old in zip(classification["cores"], residual)), "core identities")
    need(sum(row["labeled"] for row in residual) == 16605, "residual labels")
    histogram, closed, deductions = hand_closure(classification["cores"])
    local = check_literal_obstructions(certificate, classification)

    base = work / "inherited" / "c194.cnf"
    need(digest(base)["sha256"] == BASE_HASH, "strengthened base identity")
    need(result["excluded"] == list(range(15)) and result["open"] == [], "published outcome")
    replays = []
    for case in result["cases"]:
        formula = work / f"p{case['index']:02}.cnf"
        need(digest(formula) == case["formula"], f"formula identity p{case['index']:02}")
        check_formula(base, formula, case)
        replays.append(proof_record(work, case))
    need(sum(row["proof"]["bytes"] for row in replays) == 822857, "proof byte total")
    deduction_hash = hashlib.sha256(
        json.dumps(deductions, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()
    unique_proofs = []
    for proof_hash in sorted({row["proof"]["sha256"] for row in replays}):
        matches = [row for row in replays if row["proof"]["sha256"] == proof_hash]
        unique_proofs.append({"sha256": proof_hash, "bytes": matches[0]["proof"]["bytes"],
                              "case_count": len(matches)})

    report = {
        "format": "r55-order3-eleven-noempty-rigidity-review1-v1",
        "all_checks_passed": True,
        "residual_cores_checked": 26,
        "residual_labeled_cores": 16605,
        "complement_histogram": histogram,
        "hand_closed_by_projection": closed,
        "hand_deduction_records": len(deductions),
        "hand_deduction_sha256": deduction_hash,
        "core194_profiles": 15,
        "local_obstructions": local,
        "strengthened_base": digest(base),
        "complete_formulas_checked": 15,
        "fresh_proof_replays": len(replays),
        "unique_proofs": unique_proofs,
        "proof_bytes": 822857,
        "rat_core_lemmas": 0,
        "reviewer_kissat": digest(args.kissat),
        "reviewer_drat_trim": digest(args.drat_trim),
        "new_whole_core_exclusions": 0,
        "forced_empty_signature_on_each_residual_core": True,
        "entire_branch_conclusion_conditional_on_inherited_171_exclusions": True,
        "target_graph_claimed": False,
    }
    args.report.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    print("PASS 26 hand reductions, 15 literal obstructions, formulas and fresh DRAT replays")


if __name__ == "__main__":
    main()
