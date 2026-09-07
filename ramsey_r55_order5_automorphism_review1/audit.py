#!/usr/bin/env python3
"""Audit the retained evidence for the (5,5,42) order-5 exclusion.

This checker does not attempt the reported 51-hour SAT computation.  It checks
the committed cube/refinement/log metadata and then exercises the committed
final verifier with (a) fabricated VERIFIED records and no proofs and (b) no
records and no proofs.  Acceptance in case (a) demonstrates exactly which part
of the published final check is an imported trust assertion.
"""

import argparse
import collections
import hashlib
import itertools
import json
import lzma
import os
from pathlib import Path
import subprocess
import sys
import tempfile


SOURCE_COMMIT = "7fdf9ce2ee71c32bb6617a37251e3f61e388c69c"
TARGET_REF = "bafkreidhhbjq6oq77k3zzq5ur6b5pp55tisztn6he2x3d37r4hkko5imaa"
FORMULA_SHA256 = "0b47e92e573989d7406e26d8b261edd7665937912d213eb8e9423099492b7845"

# Paths are relative to graph-ramsey-theory at the reviewed commit.
PINNED_FILES = {
    "r55-42-no-order-5-automorphism/README.md":
        "6aa4cd4dd8c1a80b52d29ecd368656b508222f439bb99fa0f7e219ee0ed1b4e6",
    "r55-42-no-order-5-automorphism/c2_5_8_L3r3.icnf":
        "9e7a9285ca2e601e32b3646ab1469b7b08c8f7e220cfe4fc3b9447f800f24e8e",
    "r55-42-no-order-5-automorphism/c2_5_8_L3r_map.json":
        "77658935ce74b05360a9eb59a17aa921a9469dbd6eee134e76936584e23c20b1",
    "r55-42-no-order-5-automorphism/c2_5_8_L3r2_map.json":
        "3cfdc502c7b7ab32f0eeb1317ec433c294d6dd859d6f51a8e6f608bc0a90da58",
    "r55-42-no-order-5-automorphism/c2_5_8_L3r3_map.json":
        "93f3c6cd633f31a0f3b1b59ac3cf056d40448cb2b74aaa9ed3bdc1a83a81ba68",
    "r55-42-no-order-5-automorphism/level3_p5.json":
        "5032d9ed9fb24adb67391eb0f1d0886cdcca760086cc916263bd30a8bba7f2bf",
    "r55-42-no-order-5-automorphism/logs/results.jsonl.xz":
        "95d95ed71fad0f60ca8a6ced9b416678b29162c8742d964c9f0ce14e8d8dd891",
    "r55-42-no-order-5-automorphism/logs/verify_full.log":
        "3cdbafb8cefdb32bd54c3bd83045a1c24042f0d50ed17d2d1eb54e38764b98a8",
    "r55-42-order3-cube-and-conquer/cnc_p.py":
        "f26e9212101ff70122db0b4c7016bd4a6376be352486910a99cf110009fae430",
    "r55-42-order3-cube-and-conquer/run_lrat_p.py":
        "fdcdba39ab1ad8cd44cf40f40352fcd193afb040765d2eaffa0f09e30aabc781",
    "r55-42-order3-cube-and-conquer/verify_cnc_p.py":
        "04c9969eed1f0473c870e903bd872ce24c08d92e89084cbe57bbad6e28f8df1f",
    "r55-42-prime-order-automorphisms/encode.py":
        "79a774cd7145da2cb0b4ead2e34764bf17837bcb3dbdc3a2d5ebe9887280914a",
    "r55-42-prime-order-automorphisms/hybrid.py":
        "47cd8e06df784d05d8c864bd06eb96d4f1e68dd75476c6ddbc042eff35d5564d",
    "r55-42-prime-order-automorphisms/verify.py":
        "5a1041f0c038d7785ae27244ec59d7616cdc365ccda1afe068c4d62f3fc39cd0",
    "r55-42-prime-order-automorphisms/verify_hybrid.py":
        "413088c22eac0c3376cbc9f1219da3664c7cebf710981dc598c60afd0e48e2c2",
    "r55-42-fixed-vertex-lex-leader/symF.py":
        "8b612b0230832118778c90959d630f5318c130cb9c4797e060c8a1a595ebd6f1",
    "r55-42-fixed-vertex-lex-leader/verify_symF.py":
        "d3ff348773e1a88ecf64663f20226ffd25ab0d735ba468072be35fd674055ab9",
}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for block in iter(lambda: source.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def run_command(arguments, cwd, env=None, expected=0):
    result = subprocess.run(arguments, cwd=cwd, env=env, text=True,
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    require(result.returncode == expected,
            f"unexpected exit {result.returncode} (wanted {expected}):\n{result.stdout}")
    return result.stdout


def parse_cubes(path):
    cubes = []
    for number, line in enumerate(path.read_text().splitlines(), 1):
        require(line.startswith("a ") and line.endswith(" 0"),
                f"malformed cube line {number}")
        cube = tuple(map(int, line.split()[1:-1]))
        require(cube and len({abs(literal) for literal in cube}) == len(cube),
                f"duplicate or empty cube line {number}")
        cubes.append(cube)
    require(len(set(cubes)) == len(cubes), "duplicate final cube")
    return tuple(cubes)


def collapse(cubes, map_path):
    data = json.loads(map_path.read_text())
    require(type(data) is dict and type(data.get("split_vars")) is list
            and type(data.get("cubes")) is list, "refinement-map shape")
    split_variables = tuple(data["split_vars"])
    require(split_variables
            and len(set(split_variables)) == len(split_variables)
            and all(type(value) is int and value > 0 for value in split_variables),
            "split variables")
    records = data["cubes"]
    require(len(records) == len(cubes), "map/cube length mismatch")
    parents = {}
    for cube, record in zip(cubes, records):
        require(type(record) is dict and set(record) == {"parent", "added"},
                "refinement record fields")
        parent = record["parent"]
        added = tuple(record["added"])
        require(type(parent) is int and parent >= 0, "parent index")
        if added:
            require(cube[-len(added):] == added, "added literals are not suffix")
            base = cube[:-len(added)]
        else:
            base = cube
        previous = parents.setdefault(parent, {"cube": base, "added": set()})
        require(previous["cube"] == base, "inconsistent parent cube")
        if added:
            require(tuple(sorted(map(abs, added))) == tuple(sorted(split_variables)),
                    "wrong split-variable set")
            previous["added"].add(added)
    require(sorted(parents) == list(range(len(parents))),
            "nonconsecutive parent indices")
    full_split = {
        tuple(sign * variable for sign, variable in zip(signs, split_variables))
        for signs in itertools.product((1, -1), repeat=len(split_variables))
    }
    refined = 0
    for parent in parents.values():
        if parent["added"]:
            require(parent["added"] == full_split, "incomplete binary refinement")
            refined += 1
        require(not ({abs(literal) for literal in parent["cube"]}
                     & set(split_variables)), "parent already fixes split variable")
    return tuple(parents[index]["cube"] for index in range(len(parents))), {
        "children": len(cubes),
        "parents": len(parents),
        "refined_parents": refined,
        "split_variables": list(split_variables),
    }


def inspect_records(log_path, cubes):
    with lzma.open(log_path, "rt") as source:
        records = [json.loads(line) for line in source]
    statuses = collections.Counter(record.get("status") for record in records)
    require(statuses == {"UNSAT-VERIFIED": 16872, "TIMEOUT": 16},
            "unexpected status census")
    require({record.get("cube") for record in records} == set(range(len(cubes))),
            "record cube-index coverage")
    last = {}
    for record in records:
        last[record.get("cube")] = record
    require(all(last[index].get("status") == "UNSAT-VERIFIED"
                and tuple(last[index].get("cube_lits", ())) == cubes[index]
                for index in range(len(cubes))), "last records do not cover cubes")
    verified = [record for record in records
                if record.get("status") == "UNSAT-VERIFIED"]
    require(len(verified) == len(cubes), "verified-record count")
    require(all(tuple(record.get("cube_lits", ())) == cubes[record["cube"]]
                for record in verified), "verified cube literals")
    require(len({tuple(record["cube_lits"]) for record in verified}) == len(cubes),
            "verified literal uniqueness")
    require(all(type(record.get("lrat_bytes")) is int
                and record["lrat_bytes"] > 0 for record in verified),
            "recorded proof size")
    require(all(type(record.get("lrat_sha256")) is str
                and len(record["lrat_sha256"]) == 64
                and all(character in "0123456789abcdef"
                        for character in record["lrat_sha256"])
                for record in verified), "recorded proof digest")
    return records, verified, statuses


def build_formula(area, target, scratch):
    prime = area / "r55-42-prime-order-automorphisms"
    lex = area / "r55-42-fixed-vertex-lex-leader"
    cnc = area / "r55-42-order3-cube-and-conquer"
    python = sys.executable
    run_command([python, "-B", str(prime / "hybrid.py"), "42", "2", "5", "8",
                 "f2_p5_k8.cnf"], scratch)
    run_command([python, "-B", str(lex / "symF.py"), "f2_p5_k8.cnf",
                 "h2_5_8_symF.cnf", "42", "2", "5", "8"], scratch)
    run_command([python, "-B", str(cnc / "cnc_p.py"), "h2_5_8_symF.cnf",
                 str(target / "level3_p5.json"), "2", "5", "8", "c2_5_8_L3"],
                scratch)
    formula = scratch / "c2_5_8_L3.cnf"
    require(sha256(formula) == FORMULA_SHA256, "regenerated formula digest")
    header = formula.open().readline().split()
    require(header == ["p", "cnf", "2426", "360550"], "formula header")
    return formula, scratch / "c2_5_8_L3.icnf"


def exercise_verifier(area, target, scratch, cubes, formula):
    cnc = area / "r55-42-order3-cube-and-conquer"
    lex = area / "r55-42-fixed-vertex-lex-leader"
    verifier = cnc / "verify_cnc_p.py"
    fake_log = scratch / "fabricated_results.jsonl"
    with fake_log.open("w") as destination:
        for cube in cubes:
            # Deliberately omit cube index, proof size, proof hash, and proof.
            destination.write(json.dumps({
                "status": "UNSAT-VERIFIED",
                "cube_lits": list(cube),
            }, sort_keys=True) + "\n")
    empty_log = scratch / "empty_results.jsonl"
    empty_log.write_text("")
    manifest = scratch / "empty_manifest.json"
    manifest.write_text("{}\n")
    certdir = scratch / "empty_certificates"
    certdir.mkdir()
    maps = ",".join(str(target / name) for name in (
        "c2_5_8_L3r_map.json", "c2_5_8_L3r2_map.json",
        "c2_5_8_L3r3_map.json"))
    common = [sys.executable, "-B", str(verifier), "2", "5", "8", "3",
              str(target / "c2_5_8_L3r3.icnf"), str(formula), str(manifest),
              str(certdir), "--refine", maps, "--jobs", "1"]

    clean_environment = dict(os.environ)
    clean_environment.pop("PYTHONPATH", None)
    clean_environment["PYTHONDONTWRITEBYTECODE"] = "1"
    unassisted = subprocess.run(common + ["--verified", str(fake_log),
                                          "--skip-complete"],
                                 cwd=scratch, env=clean_environment, text=True,
                                 stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    require(unassisted.returncode != 0
            and "No module named 'verify_symF'" in unassisted.stdout,
            "clean README-style verifier call unexpectedly worked")

    repaired_environment = dict(clean_environment)
    repaired_environment["PYTHONPATH"] = str(lex)
    fake_output = run_command(common + ["--verified", str(fake_log)], scratch,
                              repaired_environment, expected=0)
    require("16872 cubes recorded VERIFIED by earlier replay sweeps" in fake_output,
            "fabricated record count not accepted")
    require("completeness: 185848 labelled" in fake_output,
            "canonical-prefix completeness did not replay")
    require("certificates: 16872 VERIFIED earlier" in fake_output
            and "RESULT: all checks passed" in fake_output,
            "fabricated statuses were not accepted as a full result")

    empty_output = run_command(common + ["--verified", str(empty_log),
                                         "--skip-complete"], scratch,
                               repaired_environment, expected=1)
    require("certificates: 16872 missing" in empty_output
            and "RESULT: incomplete (missing certificates)" in empty_output,
            "missing-certificate negative control")
    return sha256(fake_log), unassisted.returncode


def audit(source, scratch_root):
    source = source.resolve()
    commit = run_command(["git", "rev-parse", "HEAD"], source).strip()
    require(commit == SOURCE_COMMIT, "source checkout is not the reviewed commit")
    area = source / "graph-ramsey-theory"
    for relative, digest in PINNED_FILES.items():
        path = area / relative
        require(path.is_file() and sha256(path) == digest,
                f"pinned source mismatch: {relative}")
    target = area / "r55-42-no-order-5-automorphism"

    cubes = parse_cubes(target / "c2_5_8_L3r3.icnf")
    require(len(cubes) == 16872, "final cube count")
    parents = cubes
    reverse_stats = []
    for name in ("c2_5_8_L3r3_map.json", "c2_5_8_L3r2_map.json",
                 "c2_5_8_L3r_map.json"):
        parents, stats = collapse(parents, target / name)
        reverse_stats.append(stats)
    require(len(parents) == 256, "initial parent count")

    records, verified, statuses = inspect_records(
        target / "logs" / "results.jsonl.xz", cubes)
    proof_files = tuple(target.rglob("*.lrat")) + tuple(target.rglob("*.lrat.xz"))
    require(not proof_files, "unexpected retained LRAT proof")

    scratch_root.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="order5-audit-", dir=scratch_root) as temporary:
        scratch = Path(temporary)
        formula, initial_cubes = build_formula(area, target, scratch)
        require(parse_cubes(initial_cubes) == parents,
                "regenerated initial cubes differ from collapsed parents")
        fake_hash, unassisted_exit = exercise_verifier(
            area, target, scratch, cubes, formula)

    chronological = list(reversed(reverse_stats))
    return {
        "verdict": "not_accepted_without_retained_or_regenerated_unsat_certificates",
        "mathematical_claim_refuted": False,
        "target_contribution": TARGET_REF,
        "reviewed_source_commit": SOURCE_COMMIT,
        "pinned_source_files": len(PINNED_FILES),
        "formula_variables": 2426,
        "formula_clauses": 360550,
        "formula_sha256": FORMULA_SHA256,
        "initial_canonical_cubes": len(parents),
        "refinement_chain": [256] + [stage["children"] for stage in chronological],
        "refined_parent_counts": [stage["refined_parents"] for stage in chronological],
        "split_variables": [stage["split_variables"] for stage in chronological],
        "final_cubes": len(cubes),
        "published_log_lines": len(records),
        "published_log_statuses": dict(sorted(statuses.items())),
        "published_verified_status_records": len(verified),
        "recorded_lrat_bytes": sum(record["lrat_bytes"] for record in verified),
        "largest_recorded_lrat_bytes": max(record["lrat_bytes"] for record in verified),
        "recorded_lrat_sha256_fields": sum(
            bool(record.get("lrat_sha256")) for record in verified),
        "retained_lrat_files": len(proof_files),
        "lrat_replays_performed_by_review": 0,
        "fabricated_record_fields": ["cube_lits", "status"],
        "fabricated_records": len(cubes),
        "fabricated_log_sha256": fake_hash,
        "target_verifier_fabricated_log_exit": 0,
        "target_verifier_fabricated_log_result": "RESULT: all checks passed",
        "target_verifier_empty_log_exit": 1,
        "target_verifier_empty_log_result": "RESULT: incomplete (missing certificates)",
        "readme_style_clean_import_exit": unassisted_exit,
        "readme_style_clean_import_error": "No module named 'verify_symF'",
        "replayed_non_unsat_prefix": (
            "formula regeneration; independently checked refinements; "
            "target-checker canonical-prefix completeness"
        ),
        "unreplayed_load_bearing_step": "UNSAT of every one of the 16872 final cubes",
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", required=True, type=Path,
                        help="discovery-net-notes checkout at the reviewed commit")
    parser.add_argument("--scratch-root", required=True, type=Path)
    parser.add_argument("--expected", type=Path)
    arguments = parser.parse_args()
    report = audit(arguments.source, arguments.scratch_root)
    if arguments.expected:
        require(report == json.loads(arguments.expected.read_text()),
                "expected report mismatch")
    print(json.dumps(report, indent=2, sort_keys=True))
