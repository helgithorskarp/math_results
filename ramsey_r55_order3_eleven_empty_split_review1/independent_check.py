#!/usr/bin/env python3
"""Clean-room checker for the z=1 versus z>=2 eleven-cycle split.

No module from the reviewed empty-split contribution is imported.  The code
derives the equality ordering from bit tuples, checks split completeness on
every relevant signature profile, reconstructs primary edge-orbit bindings,
audits every new DIMACS unit, and replays the two claimed DRAT refutations.
"""

from argparse import ArgumentParser
from collections import Counter
from hashlib import sha256
from itertools import combinations, product
from json import dump
from pathlib import Path
import re
import subprocess


TARGET_REF = "bafkreiehgdsqcps5lzvuqrv6j4vmvub5fxbocm3ib3htgcobp4khx4sjjq"
CORE_WORDS = {11: "100110110", 13: "110110101"}
EXPECTED = {
    "base11.cnf": (24873705, "edcb237d03e46805495c5151f4589d44543f0450c30564108bbefb7dea2905e1"),
    "base13.cnf": (24873704, "3e795444d8ce43c10c52f20f382b0f981605f47223fc24204a22e8553c132236"),
    "c11_one.cnf": (24873882, "66a189985febad0f8e08e988cc79aef498a740cf37cfbdf99c7956248a9a5c5d"),
    "c11_many.cnf": (24873726, "ec5b3113a2a1bb845cf0d22857aa728c937eb629e2730a0d47ba69413a32b96d"),
    "c13_one.cnf": (24873881, "e6fa2416d82fecdfbf09b26c1bd81639bd7d97cea248bae8d33661b474223477"),
    "c13_many.cnf": (24873725, "57e6219d14e7eefd43881657cfac7d3c06b79127095ced6dee1df257e2d0f99e"),
    "c11_one.drat": (11698808, "1cb1b979acbcac3f377cbcde81cd4b2dc781383e8356a99b017fb841b6cb5160"),
    "c13_one.drat": (11651203, "e3876f1d2a86fe86b30c6106cacb23ea4b3a24ea2c2422c4c4d9fb5b77291d61"),
    "drat-trim": (51352, "9c09fe813af0b52f58d923837a1bc3ca5e6017987c1e9530d62fa5b4f018412a"),
}


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def file_info(path):
    h = sha256()
    size = 0
    with path.open("rb") as stream:
        while block := stream.read(1 << 20):
            size += len(block)
            h.update(block)
    return {"bytes": size, "sha256": h.hexdigest()}


def check_info(path, label):
    actual = file_info(path)
    size, digest = EXPECTED[label]
    require(actual == {"bytes": size, "sha256": digest}, f"file identity: {label}")
    return actual


def same_file(left, right):
    with left.open("rb") as a, right.open("rb") as b:
        while True:
            x, y = a.read(1 << 20), b.read(1 << 20)
            if x != y:
                return False
            if not x:
                return True


def weak_compositions():
    """All eight-bin weak compositions of ten, via stars and bars."""
    for bars in combinations(range(17), 7):
        cuts = (-1,) + bars + (17,)
        yield tuple(cuts[i + 1] - cuts[i] - 1 for i in range(8))


def bits(mask):
    return tuple(int(bool(mask & (1 << i))) for i in range(3))


def equality_rows():
    rows = [bits(0)]
    rows.extend(bits(1 << i) for i in range(3) for _ in range(2))
    rows.extend(bits((1 << i) | (1 << j)) for i, j in combinations(range(3), 2))
    return tuple(sorted(rows))


def profile_rows(counts):
    return tuple(sorted(bits(mask) for mask, count in enumerate(counts) for _ in range(count)))


def primary_map():
    """Recover every unordered-pair orbit under the order-three action."""
    def rotate(v):
        return 3 * (v // 3) + (v % 3 + 1) % 3 if v < 33 else v

    member_to_rep = {}
    representatives = set()
    for pair in combinations(range(43), 2):
        if pair[1] < 33 and pair[0] // 3 == pair[1] // 3:
            continue
        orbit = []
        moved = pair
        while moved not in orbit:
            orbit.append(moved)
            moved = tuple(sorted((rotate(moved[0]), rotate(moved[1]))))
        representative = min(orbit)
        representatives.add(representative)
        for member in orbit:
            member_to_rep[member] = representative

    moving = sorted(rep for rep in representatives if rep[1] < 33)
    fixed = sorted(rep for rep in representatives if rep[0] >= 33)
    links = sorted((rep for rep in representatives if rep[0] < 33 <= rep[1]),
                   key=lambda rep: (rep[1], rep[0]))
    require((len(moving), len(fixed), len(links)) == (165, 45, 110), "orbit categories")
    ids = {rep: i + 1 for i, rep in enumerate(moving + fixed + links)}
    result = {member: ids[rep] for member, rep in member_to_rep.items()}
    require(len(ids) == 320, "primary variable count")
    return result


def attachment(pair_id, fixed_vertex, triangle):
    return pair_id[tuple(sorted((fixed_vertex, 3 * triangle)))]


def split_units(pair_id, branch):
    if branch == "many":
        return tuple(-attachment(pair_id, 34, i) for i in range(3))
    require(branch == "one", "unknown branch")
    return tuple(attachment(pair_id, 33 + row, i) if bit else
                 -attachment(pair_id, 33 + row, i)
                 for row, row_bits in enumerate(equality_rows()) if row
                 for i, bit in enumerate(row_bits))


def arithmetic_and_split(pair_id):
    eq_rows = equality_rows()
    eq_masks = [sum(bit << i for i, bit in enumerate(row)) for row in eq_rows]
    require(eq_masks == [0, 4, 4, 2, 2, 6, 1, 1, 5, 3], "lexicographic equality order")
    require(eq_masks != sorted(eq_masks), "numeric mask order must differ")
    one_units = split_units(pair_id, "one")
    many_units = split_units(pair_id, "many")
    require(one_units == (-222, -223, 224, -233, -234, 235, -244, 245, -246,
                          -255, 256, -257, -266, 267, 268, 277, -278, -279,
                          288, -289, -290, 299, -300, 301, 310, 311, -312),
            "equality unit bindings")
    require(many_units == (-222, -223, -224), "many-empty unit bindings")

    total = basic = stronger = one_count = many_count = 0
    equality_profiles = []
    truth_counts = Counter()
    for counts in weak_compositions():
        total += 1
        incidences = [sum(counts[mask] for mask in range(8) if mask & (1 << i))
                      for i in range(3)]
        if max(incidences) > 4 or max(counts[1], counts[2], counts[4]) > 2:
            continue
        basic += 1
        require(counts[0] >= 1, "basic inequalities allowed ten nonempty signatures")
        rows = profile_rows(counts)
        values = {attachment(pair_id, 33 + row, i): value
                  for row, row_bits in enumerate(rows) for i, value in enumerate(row_bits)}
        one_true = all(values[abs(lit)] == int(lit > 0) for lit in one_units)
        many_true = all(values[abs(lit)] == int(lit > 0) for lit in many_units)
        require(one_true == (counts[0] == 1), "equality branch is not equivalent to z=1")
        require(many_true == (counts[0] >= 2), "many branch is not equivalent to z>=2")
        require(one_true != many_true, "branches do not form a disjoint cover")
        truth_counts[(one_true, many_true)] += 1
        if one_true:
            equality_profiles.append(counts)
        if any(counts[1 << i] + counts[(1 << i) | (1 << j)] > 3
               for i in range(3) for j in range(3) if i != j):
            continue
        stronger += 1
        one_count += one_true
        many_count += many_true

    require(total == 19448 and basic == 928, "basic arithmetic census")
    require((stronger, one_count, many_count) == (778, 1, 777), "strong split census")
    require(equality_profiles == [(1, 2, 2, 1, 2, 1, 1, 0)], "unique equality profile")

    signatures11 = list(product((0, 1), repeat=11))
    require(all(signatures11[i][:3] <= signatures11[i + 1][:3]
                for i in range(len(signatures11) - 1)), "full ordering does not order prefixes")
    return {
        "profiles": total,
        "basic_profiles": basic,
        "stronger_profiles": stronger,
        "one_profiles": one_count,
        "many_profiles": many_count,
        "unique_equality_profile": list(equality_profiles[0]),
        "equality_prefix_masks_in_row_order": eq_masks,
        "equality_units": list(one_units),
        "many_units": list(many_units),
        "basic_split_truth_counts": {"one": truth_counts[(True, False)],
                                     "many": truth_counts[(False, True)]},
        "full_eleven_bit_signatures": len(signatures11),
        "numeric_mask_order_rejected": True,
    }


def parse_header(line, path):
    fields = line.decode("ascii").split()
    require(len(fields) == 4 and fields[:2] == ["p", "cnf"], f"header: {path}")
    return int(fields[2]), int(fields[3])


def audit_formula(base_path, full_path, units):
    with base_path.open("rb") as base, full_path.open("rb") as full:
        base_vars, base_clauses = parse_header(base.readline(), base_path)
        full_vars, full_clauses = parse_header(full.readline(), full_path)
        require((base_vars, base_clauses) == (34268, 617204), "signature-base dimensions")
        require((full_vars, full_clauses) == (34268, 617204 + len(units)), "split dimensions")
        for index in range(base_clauses):
            require(base.readline() == full.readline(), f"base-prefix clause {index + 1}")
        require(base.read() == b"", "extra base data")
        for lit in units:
            require(full.readline() == f"{lit} 0\n".encode(), "wrong appended unit")
        require(full.read() == b"", "extra split-formula data")
    return {"variables": full_vars, "clauses": full_clauses,
            "base_prefix_clauses": base_clauses, "appended_units": len(units),
            "complete_prefix": True}


def replay(drat_trim, formula, proof, log_path, expected_rat):
    with log_path.open("wb") as output:
        result = subprocess.run([str(drat_trim), str(formula), str(proof)],
                                stdout=output, stderr=subprocess.STDOUT)
    text = log_path.read_text(errors="replace").replace("\r", "")
    match = re.search(r"(\d+) RAT lemmas in core", text)
    require(result.returncode == 0 and "s VERIFIED" in text, f"DRAT replay failed: {formula.name}")
    require(match and int(match.group(1)) == expected_rat, f"RAT count: {formula.name}")
    return {"verified": True, "exit_code": result.returncode,
            "rat_core_lemmas": int(match.group(1))}


def main():
    parser = ArgumentParser()
    parser.add_argument("--proof-work", required=True, type=Path)
    parser.add_argument("--reviewed-signature-work", required=True, type=Path,
                        help="proof workspace used by the accepted signature-bound review")
    parser.add_argument("--drat-trim", required=True, type=Path)
    parser.add_argument("--work", required=True, type=Path)
    parser.add_argument("--report", required=True, type=Path)
    parser.add_argument("--skip-proofs", action="store_true")
    args = parser.parse_args()
    args.work.mkdir(parents=True, exist_ok=True)

    pair_id = primary_map()
    report = {
        "format": "r55-order3-k11-empty-split-review1-v1",
        "target_artifact": TARGET_REF,
        "arithmetic_split": arithmetic_and_split(pair_id),
        "primary_orbits": 320,
        "bases": {},
        "cases": [],
    }
    for core in (11, 13):
        base = args.proof_work / f"base{core}.cnf"
        reviewed = args.reviewed_signature_work / f"c{core}.cnf"
        info = check_info(base, f"base{core}.cnf")
        require(same_file(base, reviewed), f"base {core} differs from accepted-review instance")
        report["bases"][str(core)] = {"formula": info,
                                      "byte_identical_to_accepted_review_instance": True,
                                      "core_words": CORE_WORDS[core]}

        for branch in ("one", "many"):
            name = f"c{core}_{branch}"
            formula = args.proof_work / f"{name}.cnf"
            units = split_units(pair_id, branch)
            row = {"name": name, "core": core, "branch": branch,
                   "formula": check_info(formula, f"{name}.cnf"),
                   "audit": audit_formula(base, formula, units)}
            if branch == "one":
                proof = args.proof_work / f"{name}.drat"
                row["proof"] = check_info(proof, f"{name}.drat")
                if not args.skip_proofs:
                    row["replay"] = replay(args.drat_trim, formula, proof,
                                           args.work / f"{name}.replay.log",
                                           {11: 86, 13: 89}[core])
                row["status"] = "excluded" if row.get("replay", {}).get("verified") else "unchecked"
            else:
                row["status"] = "open_not_certified"
            report["cases"].append(row)

    report["drat_trim"] = check_info(args.drat_trim, "drat-trim")
    report["excluded"] = [row["name"] for row in report["cases"] if row["status"] == "excluded"]
    report["open_not_certified"] = [row["name"] for row in report["cases"]
                                    if row["status"] == "open_not_certified"]
    report["conclusion"] = "z>=2" if report["excluded"] == ["c11_one", "c13_one"] else "not established"
    report["target_graph_claimed"] = False
    report["all_checks_passed"] = report["conclusion"] == "z>=2"
    args.report.parent.mkdir(parents=True, exist_ok=True)
    with args.report.open("w") as stream:
        dump(report, stream, indent=2, sort_keys=True)
        stream.write("\n")
    print("PASS split completeness, exact formula tails" +
          (", and two serial DRAT replays" if not args.skip_proofs else " (proof replays skipped)"))


if __name__ == "__main__":
    main()
