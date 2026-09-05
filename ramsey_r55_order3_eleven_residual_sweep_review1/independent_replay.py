#!/usr/bin/env python3
"""Independent one-worker replay of all 34 claimed residual-core exclusions.

The 45 reported timeout cases make no mathematical assertion and are not
rerun.  This script imports no module from the reviewed sweep.  It uses the
previously accepted complete r=4 parent generator, constructs each cube from
the literal cycle-pair ordering, obtains a fresh Kissat proof, and requires a
complete drat-trim replay before recording an exclusion.
"""

import argparse
from hashlib import sha256
from itertools import combinations
import json
import os
from pathlib import Path
import re
import resource
import subprocess
import sys
import time


HERE = Path(__file__).resolve().parent
REPO = HERE.parent
SWEEP = REPO / "ramsey_r55_order3_eleven_residual_sweep"
PARENT_SOURCE = REPO / "ramsey_r55_order3_eleven_cycle_obstruction"
CLASSIFICATION = REPO / "ramsey_r55_order3_eleven_blue_k4_exclusion" / "classification.json"
PUBLISHED_RESULT = SWEEP / "result.json"
PUBLISHED_VERIFICATION = SWEEP / "verification.json"
PUBLISHED_CASES = SWEEP / "cases.json"

PARENT_SHA256 = "c8f355b256de55727b18efcbd47ef9e777ac2b3b4ae69e09676fcddd51afa05f"
CLASSIFICATION_SHA256 = "429289f6e84bbb8ec58fb007024c6b65a55096b4bbe606402d711157c4abc957"
RESULT_SHA256 = "aa6fe619507d058d69aadf36f5ef92ec7bc073f5cfab2d1e99b3191d8b2e658c"
VERIFICATION_SHA256 = "5a942552a2113a5e6a0b728cef862dce6316c6aae9b1fd2a4a79b58ca6bc21fc"
CASES_SHA256 = "b14870da74f34b18f326b649be79452d05ff6517dcf21a86af47b7caad3c3a65"
PARENT_GENERATOR_SHA256 = "e97e44491220a8d0d288912930d5f1795c8a4c86802ce66f5fc6cf374655b95b"
PARENT_AUDITOR_SHA256 = "23df18de05fca300e1f20759be822e9d58a924c42a38be764beb8546939f7946"

CLAIMED_EXCLUDED = (
    11, 13, 25, 32, 34, 41, 48, 50, 66, 70, 76, 77, 80, 81, 84, 108,
    111, 113, 134, 141, 142, 146, 148, 149, 150, 151, 152, 163, 166,
    171, 174, 175, 187, 189,
)


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def info(path):
    value = sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            value.update(block)
    return {"bytes": path.stat().st_size, "sha256": value.hexdigest()}


def atomic(path, value):
    temporary = path.with_suffix(path.suffix + ".partial")
    with temporary.open("w", encoding="utf-8") as stream:
        json.dump(value, stream, indent=2, sort_keys=True)
        stream.write("\n")
        stream.flush()
        os.fsync(stream.fileno())
    os.replace(temporary, path)


def case_manifest_sha256(rows):
    """Digest proof-relevant fields, excluding machine-dependent timings."""
    manifest = [
        {
            "bits": row["bits"],
            "formula": row["formula"],
            "index": row["index"],
            "labeled": row["labeled"],
            "proof": row["proof"],
            "rat_core_lemmas": row["replay"]["rat_core_lemmas"],
        }
        for row in rows
    ]
    encoded = json.dumps(manifest, sort_keys=True, separators=(",", ":")).encode("ascii")
    return sha256(encoded).hexdigest()


def core_variables():
    """Derive the 18 core variables from cycle-pair/difference order."""
    starts = {pair: 3 * position + 1
              for position, pair in enumerate(combinations(range(11), 2))}
    result = []
    for pair in combinations(range(4), 2):
        result.extend(range(starts[pair], starts[pair] + 3))
    require(result == [1, 2, 3, 4, 5, 6, 7, 8, 9,
                       31, 32, 33, 34, 35, 36, 58, 59, 60],
            "core variable derivation")
    return tuple(result)


def read_claim():
    pins = ((CLASSIFICATION, CLASSIFICATION_SHA256), (PUBLISHED_RESULT, RESULT_SHA256),
            (PUBLISHED_VERIFICATION, VERIFICATION_SHA256), (PUBLISHED_CASES, CASES_SHA256),
            (PARENT_SOURCE / "generate.py", PARENT_GENERATOR_SHA256),
            (PARENT_SOURCE / "check_formula.cpp", PARENT_AUDITOR_SHA256))
    for path, expected in pins:
        require(info(path)["sha256"] == expected, ("source hash", path.name))

    classification = json.loads(CLASSIFICATION.read_text())
    retained = classification["retained"]
    require(classification["retained_classes"] == len(retained) == 79, "retained class count")
    require(classification["retained_labeled"] == sum(row["labeled"] for row in retained) == 51_696,
            "retained labeled count")
    require([row["index"] for row in retained] == sorted({row["index"] for row in retained}),
            "retained ordering")
    require(all(len(row["bits"]) == 18 and set(row["bits"]) <= {"0", "1"} for row in retained),
            "retained bit words")
    require(json.loads(PUBLISHED_CASES.read_text()) == retained, "published case list")
    by_index = {row["index"]: row for row in retained}
    require(set(CLAIMED_EXCLUDED) < set(by_index), "excluded list is not a proper residual subset")
    open_indices = tuple(index for index in by_index if index not in CLAIMED_EXCLUDED)
    require(len(open_indices) == 45, "open complement count")
    require(sum(by_index[i]["labeled"] for i in CLAIMED_EXCLUDED) == 21_942,
            "excluded labeled count")
    require(sum(by_index[i]["labeled"] for i in open_indices) == 29_754,
            "open labeled count")

    published = json.loads(PUBLISHED_RESULT.read_text())
    verification = json.loads(PUBLISHED_VERIFICATION.read_text())
    require(published["complete"] and not published["target_graph"], "published sweep status")
    require(tuple(published["excluded"]) == CLAIMED_EXCLUDED and
            tuple(published["open"]) == open_indices, "published outcome partition")
    require(verification["verified"] and verification["proof_replays"] == 34,
            "published verification status")
    require(tuple(verification["excluded"]) == CLAIMED_EXCLUDED and
            tuple(verification["open"]) == open_indices, "verification outcome partition")
    require(len(published["cases"]) == len(verification["cases"]) == 79,
            "published per-case coverage")
    published_by_index = {row["index"]: row for row in published["cases"]}
    verified_by_index = {row["index"]: row for row in verification["cases"]}
    require(set(published_by_index) == set(verified_by_index) == set(by_index),
            "per-case index coverage")
    for index, case in by_index.items():
        first = published_by_index[index]
        second = verified_by_index[index]
        require(first["bits"] == case["bits"], ("published bits", index))
        require(first["formula"] == second["formula"], ("two-pass formula identity", index))
        require(first["status"] == second["status"], ("two-pass status", index))
        if index in CLAIMED_EXCLUDED:
            require(first["solver_code"] == 20 and first["replay"]["verified"] and
                    second["replay"]["verified"], ("published proof obligation", index))
        else:
            require(first["solver_code"] == 0 and first["status"] == "open",
                    ("published open semantics", index))
    return by_index, open_indices, published_by_index


def parse_parent(parent):
    require(info(parent) == {"bytes": 24_892_619, "sha256": PARENT_SHA256},
            "complete parent identity")
    clauses = 0
    maximum = 0
    with parent.open("rb") as stream:
        require(stream.readline() == b"p cnf 34280 615920\n", "parent DIMACS header")
        for line in stream:
            words = line.split()
            require(words and words[-1] == b"0", ("parent clause terminator", clauses))
            literals = tuple(map(int, words[:-1]))
            require(literals and len(literals) == len(set(literals)),
                    ("empty or repeated parent literal", clauses))
            require(not any(-literal in literals for literal in literals),
                    ("tautological parent clause", clauses))
            maximum = max(maximum, *(abs(literal) for literal in literals))
            clauses += 1
    require(clauses == 615_920 and maximum == 34_280, "parent DIMACS dimensions")


def prepare(work):
    parent = work / "parent.cnf"
    if not parent.exists():
        generated = subprocess.run(
            [sys.executable, "-B", str(PARENT_SOURCE / "generate.py"),
             "--red-cycles", "4", "--output", str(parent)],
            capture_output=True, text=True, check=True)
        metadata = json.loads(generated.stdout)
        require(metadata["sha256"] == PARENT_SHA256, "parent generator output")
    parse_parent(parent)
    auditor = work / "check_formula"
    subprocess.run(["g++", "-std=c++17", "-O2", "-Wall", "-Wextra", "-Wpedantic",
                    "-Werror", str(PARENT_SOURCE / "check_formula.cpp"), "-o", str(auditor)],
                   check=True)
    checked = subprocess.run([str(auditor), "4", str(parent)], capture_output=True, text=True)
    require(checked.returncode == 0 and "FORMULA_AUDIT" in checked.stdout and
            " PASS" in checked.stdout, "independent inherited parent audit")
    return parent, checked.stdout.strip()


def make_formula(parent, output, bits):
    variables = core_variables()
    require(len(bits) == 18 and set(bits) <= {"0", "1"}, "core bit word")
    with parent.open("rb") as source, output.open("wb") as target:
        require(source.readline() == b"p cnf 34280 615920\n", "parent header during cube")
        target.write(b"p cnf 34280 615938\n")
        for block in iter(lambda: source.read(1 << 20), b""):
            target.write(block)
        for variable, bit in zip(variables, bits, strict=True):
            target.write(f"{variable if bit == '1' else -variable} 0\n".encode("ascii"))
    return info(output)


def replay(drat, formula, proof, log, seconds):
    before = time.monotonic()
    with log.open("w", encoding="utf-8") as stream:
        result = subprocess.run([str(drat), str(formula), str(proof), "-t", str(seconds)],
                                stdout=stream, stderr=subprocess.STDOUT, timeout=seconds + 60)
    output = log.read_text(errors="replace")
    require(result.returncode == 0 and "s VERIFIED" in output, "DRAT proof replay")
    match = re.search(r"(\d+) RAT lemmas in core", output)
    require(match, "missing RAT-core statistic")
    return {"verified": True, "exit_code": result.returncode,
            "rat_core_lemmas": int(match.group(1)),
            "seconds": round(time.monotonic() - before, 6)}


def case_contract(index, case, published, formula):
    require(formula == published["formula"], ("published formula identity", index))
    return {"index": index, "bits": case["bits"], "labeled": case["labeled"],
            "formula": formula, "published_formula": published["formula"]}


def run_case(work, parent, kissat, drat, solve_seconds, replay_seconds,
             index, case, published, resume):
    stem = f"c{index:03}"
    formula, proof = work / (stem + ".cnf"), work / (stem + ".drat")
    solve_log, replay_log = work / (stem + ".solve.log"), work / (stem + ".replay.log")
    checkpoint = work / (stem + ".json")
    formula_info = make_formula(parent, formula, case["bits"])
    base = case_contract(index, case, published, formula_info)
    if resume and checkpoint.exists():
        old = json.loads(checkpoint.read_text())
        require(old["index"] == index and old["bits"] == case["bits"] and
                old["formula"] == formula_info, ("changed checkpoint", index))
        if old.get("status") == "excluded" and old.get("replay", {}).get("verified"):
            require(info(proof) == old["proof"], ("changed retained proof", index))
            checked_again = replay(drat, formula, proof, replay_log, replay_seconds)
            require(checked_again["rat_core_lemmas"] == old["replay"]["rat_core_lemmas"],
                    ("changed retained replay", index))
            old["checkpoint_replay"] = checked_again
            atomic(checkpoint, old)
            return old

    before = time.monotonic()
    with solve_log.open("w", encoding="utf-8") as stream:
        solved = subprocess.run([str(kissat), f"--time={solve_seconds}", str(formula), str(proof)],
                                stdout=stream, stderr=subprocess.STDOUT,
                                timeout=solve_seconds + 60)
    row = dict(base, solver_exit_code=solved.returncode,
               solve_seconds=round(time.monotonic() - before, 6), proof=info(proof))
    if solved.returncode != 20:
        row["status"] = "not_reproduced"
        atomic(checkpoint, row)
        raise RuntimeError(("claimed exclusion did not regenerate", index, solved.returncode))
    row["replay"] = replay(drat, formula, proof, replay_log, replay_seconds)
    row["status"] = "excluded"
    atomic(checkpoint, row)
    return row


def negative_control(work, drat, formula, replay_seconds):
    bogus = work / "unsupported-empty.drat"
    bogus.write_text("0\n", encoding="ascii")
    log = work / "unsupported-empty.log"
    with log.open("w", encoding="utf-8") as stream:
        result = subprocess.run([str(drat), str(formula), str(bogus), "-t", str(replay_seconds)],
                                stdout=stream, stderr=subprocess.STDOUT,
                                timeout=replay_seconds + 60)
    output = log.read_text(errors="replace")
    require(result.returncode != 0 or "s VERIFIED" not in output,
            "checker accepted unsupported empty clause")
    return True


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--work", type=Path, required=True)
    parser.add_argument("--kissat", type=Path, required=True)
    parser.add_argument("--drat-trim", type=Path, required=True)
    parser.add_argument("--solve-seconds", type=int, default=60)
    parser.add_argument("--replay-seconds", type=int, default=300)
    parser.add_argument("--resume", action="store_true")
    args = parser.parse_args()
    work = args.work.resolve()
    require(not work.is_relative_to(REPO) and args.solve_seconds > 0 and args.replay_seconds > 0,
            "external work directory and positive limits required")
    work.mkdir(parents=True, exist_ok=True)
    kissat, drat = args.kissat.resolve(), args.drat_trim.resolve()
    by_index, open_indices, published = read_claim()
    contract = {
        "format": "r55-k11-r4-residual-independent-review1-v1",
        "python": sys.version.split()[0],
        "workers": 1,
        "solve_seconds": args.solve_seconds,
        "replay_seconds": args.replay_seconds,
        "kissat": info(kissat),
        "drat_trim": info(drat),
        "classification_sha256": CLASSIFICATION_SHA256,
        "published_result_sha256": RESULT_SHA256,
        "published_verification_sha256": VERIFICATION_SHA256,
        "parent_sha256": PARENT_SHA256,
    }
    contract_path = work / "contract.json"
    if contract_path.exists():
        require(args.resume and json.loads(contract_path.read_text()) == contract,
                "existing work or changed contract")
    atomic(contract_path, contract)
    started = time.monotonic()
    parent, parent_audit = prepare(work)
    rows = []
    for ordinal, index in enumerate(CLAIMED_EXCLUDED, 1):
        if (work / "STOP").exists():
            break
        row = run_case(work, parent, kissat, drat, args.solve_seconds,
                       args.replay_seconds, index, by_index[index], published[index], args.resume)
        rows.append(row)
        report = {
            "status": "RUNNING" if ordinal < len(CLAIMED_EXCLUDED) else "VERIFIED",
            "complete": ordinal == len(CLAIMED_EXCLUDED),
            "claimed_exclusions": list(CLAIMED_EXCLUDED),
            "verified_exclusions": [item["index"] for item in rows],
            "reported_open_not_rerun": list(open_indices),
            "cases": rows,
            "parent_audit": parent_audit,
            "contract": contract,
            "elapsed_seconds": round(time.monotonic() - started, 6),
            "maximum_child_rss_kib": resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,
        }
        atomic(work / "report.json", report)
        print(json.dumps({"ordinal": ordinal, "index": index,
                          "solve_seconds": row["solve_seconds"],
                          "replay_seconds": row["replay"]["seconds"],
                          "proof_bytes": row["proof"]["bytes"]}), flush=True)
    require(len(rows) == len(CLAIMED_EXCLUDED), "run stopped before all claimed exclusions")
    first_formula = work / f"c{CLAIMED_EXCLUDED[0]:03}.cnf"
    control = negative_control(work, drat, first_formula, args.replay_seconds)
    final = json.loads((work / "report.json").read_text())
    final.update({
        "status": "ALL 34 CLAIMED EXCLUSIONS INDEPENDENTLY REGENERATED AND VERIFIED",
        "complete": True,
        "proof_replays": len(rows),
        "formula_hashes_match_published": all(row["formula"] == row["published_formula"] for row in rows),
        "proof_hashes_match_published": all(
            row["proof"] == published[row["index"]]["proof"] for row in rows
        ),
        "all_proofs_replayed_this_invocation": all(
            (row.get("checkpoint_replay") or row["replay"])["verified"] for row in rows
        ),
        "case_manifest_sha256": case_manifest_sha256(rows),
        "fresh_proof_bytes": sum(row["proof"]["bytes"] for row in rows),
        "fresh_rat_core_lemmas": sum(row["replay"]["rat_core_lemmas"] for row in rows),
        "unsupported_empty_proof_rejected": control,
        "excluded_classes": 34,
        "excluded_labeled_cores": 21_942,
        "open_classes": 45,
        "open_labeled_cores": 29_754,
        "combined_excluded_classes": 152,
        "combined_excluded_labeled_cores": 85_789,
        "record_improvement": False,
        "elapsed_seconds": round(time.monotonic() - started, 6),
        "maximum_child_rss_kib": resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,
    })
    atomic(work / "report.json", final)
    print("FINISHED " + json.dumps({key: final[key] for key in
          ("status", "proof_replays", "fresh_proof_bytes", "fresh_rat_core_lemmas",
           "case_manifest_sha256", "elapsed_seconds", "maximum_child_rss_kib")},
          sort_keys=True), flush=True)


if __name__ == "__main__":
    main()
