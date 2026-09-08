#!/usr/bin/env python3
"""Full source and independent reproduction of the ACCEPT review for h3927."""

import argparse
import hashlib
import io
import json
import os
import resource
import subprocess
import sys
import tarfile
from pathlib import Path


HERE = Path(__file__).resolve().parent
SOURCE_COMMIT = "35a4c0957ceca369cce1f6729a2fe534d9d04264"
SOURCE_DIRECTORY = "hadwiger_nelson_vnd_case10_verified_gate"
SOURCE_MANIFEST_SHA256 = "b7a0a5049c2b54c3b4f96638c8b60ea58d63729288327efb01c54f3e60ad9262"
LRAT_SHA256 = "e83e851c0e8f70b0e909085ba81c582438290983e451f33a6b5c851aa4ff136d"
CNF_SHA256 = "aa4305ebd561a52e89fe77738deee93c53f0c062a7715b879a51d0ada69b3bef"


def need(condition, message):
    if not condition:
        raise ValueError(message)


def digest(path):
    value = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            value.update(block)
    return value.hexdigest()


def memory_limit():
    ceiling = 8 * (1 << 30)
    resource.setrlimit(resource.RLIMIT_AS, (ceiling, ceiling))


def run(command, cwd, environment=None, limited=False):
    result = subprocess.run(
        [str(item) for item in command], cwd=cwd, env=environment,
        capture_output=True, text=True, check=True,
        preexec_fn=memory_limit if limited else None,
    )
    need(not result.stderr, "unexpected stderr: " + " ".join(map(str, command)))
    return result.stdout


def run_json(command, cwd, environment=None, limited=False):
    return json.loads(run(command, cwd, environment, limited))


def compile_cpp(source, output, sanitized=False):
    flags = ["-std=c++17", "-Wall", "-Wextra", "-Wconversion", "-pedantic"]
    if sanitized:
        flags += ["-O1", "-g", "-fsanitize=address,undefined",
                  "-fno-omit-frame-pointer"]
    else:
        flags += ["-O3"]
    run(["g++", *flags, source, "-o", output], HERE)


def extract_source(root, destination):
    resolved = run(["git", "rev-parse", SOURCE_COMMIT + "^{commit}"], root).strip()
    need(resolved == SOURCE_COMMIT, "reviewed source commit unavailable")
    archive = subprocess.run(
        ["git", "archive", "--format=tar", SOURCE_COMMIT, SOURCE_DIRECTORY],
        cwd=root, capture_output=True, check=True,
    ).stdout
    with tarfile.open(fileobj=io.BytesIO(archive), mode="r:") as bundle:
        bundle.extractall(destination)
    source = destination / SOURCE_DIRECTORY
    manifest = source / "SHA256SUMS"
    need(digest(manifest) == SOURCE_MANIFEST_SHA256, "source manifest identity")
    count = 0
    for line in manifest.read_text().splitlines():
        wanted, name = line.split("  ", 1)
        need("/" not in name and name not in (".", ".."), "source manifest path")
        need(digest(source / name) == wanted, "source file identity " + name)
        count += 1
    need(count == 28, "source manifest count")
    return source, count


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("root", type=Path, help="math_results checkout root")
    parser.add_argument("work", type=Path, help="new scratch directory")
    parser.add_argument("lrat", type=Path, help="the 926441080-byte pinned LRAT")
    parser.add_argument("--python", type=Path, default=Path(sys.executable),
                        help="Python with python-flint 0.8.0 installed")
    args = parser.parse_args()
    root = args.root.resolve()
    work = args.work.resolve()
    lrat = args.lrat.resolve()
    # Preserve a virtual-environment launcher rather than resolving its symlink
    # to the base interpreter (which would lose the environment's packages).
    python = args.python.absolute()
    need(not work.exists(), "work directory must be new")
    need(lrat.stat().st_size == 926441080 and digest(lrat) == LRAT_SHA256,
         "LRAT identity")
    work.mkdir(parents=True)
    source, manifest_entries = extract_source(root, work / "snapshot")
    source_work = work / "source_work"
    environment = dict(os.environ, VND_WORKDIR=str(source_work))

    replay = run([python, "-B", source / "reproduce.py", "--work", source_work],
                 source, environment)
    need("VERIFIED_VND_CASE10_EXACT_STRICT_GEOMETRY_AND_CNF" in replay.splitlines(),
         "source geometry/CNF replay")
    need(digest(source_work / "gate.cnf") == CNF_SHA256, "source replay CNF")
    os.symlink(lrat, source_work / "gate.lrat")
    source_proof = run_json(
        [python, "-B", source / "check_proof.py", "--work", source_work,
         "--checkers", work, "--lrat-only"], source, environment, limited=True
    )
    need(source_proof["status"] == "VERIFIED_VND_CASE10_FULL_LRAT_REFUTATION",
         "source LRAT checker")

    normal = work / "independent_normal"
    optimized = work / "independent_optimized"
    prepare = [HERE / "independent_audit.py", "prepare", source_work]
    normal_prepare = run_json([python, "-B", *prepare, normal], HERE)
    optimized_prepare = run_json([python, "-O", "-B", *prepare, optimized], HERE)
    need(normal_prepare == optimized_prepare, "independent coordinate modes")
    need((normal / "review_residues.tsv").read_bytes() ==
         (optimized / "review_residues.tsv").read_bytes(), "residue modes")

    sieve = normal / "review_sieve"
    sieve_sanitized = normal / "review_sieve_sanitized"
    compile_cpp(HERE / "review_sieve.cpp", sieve)
    compile_cpp(HERE / "review_sieve.cpp", sieve_sanitized, sanitized=True)
    pilot = normal / "pilot.bin"
    pilot_sanitized = normal / "pilot_sanitized.bin"
    pilot_report = run_json(
        [sieve, normal / "review_residues.tsv", 2000, pilot], HERE
    )
    sanitized_report = run_json(
        [sieve_sanitized, normal / "review_residues.tsv", 2000,
         pilot_sanitized], HERE
    )
    need(pilot_report == sanitized_report and pilot.read_bytes() ==
         pilot_sanitized.read_bytes(), "sieve sanitizer pilot")
    sieve_report = run_json(
        [sieve, normal / "review_residues.tsv", 64513,
         normal / "review_sieve.bin"], HERE
    )
    (normal / "review_sieve.json").write_text(
        json.dumps(sieve_report, separators=(",", ":")) + "\n"
    )
    finish = [HERE / "independent_audit.py", "finish", source_work, normal]
    normal_finish = run_json([python, "-B", *finish], HERE)
    optimized_finish = run_json([python, "-O", "-B", *finish], HERE)
    need(normal_finish == optimized_finish, "independent finish modes")

    checker = normal / "review_lrat"
    checker_sanitized = normal / "review_lrat_sanitized"
    compile_cpp(HERE / "review_lrat.cpp", checker)
    compile_cpp(HERE / "review_lrat.cpp", checker_sanitized, sanitized=True)
    controls = run_json(
        [python, "-B", HERE / "checker_controls.py", normal / "lrat_controls",
         checker, checker_sanitized], HERE
    )
    proof_lines = run([checker, source_work / "gate.cnf", lrat], HERE,
                      limited=True).splitlines()
    need(len(proof_lines) == 2 and
         proof_lines[0] == "VERIFIED_INDEPENDENT_RUP_LRAT",
         "independent LRAT acceptance")
    proof = json.loads(proof_lines[1])

    receipt = {
        "status": "REPRODUCED_ACCEPT_REVIEW_H3927",
        "reviewed_source_commit": SOURCE_COMMIT,
        "source_manifest_sha256": SOURCE_MANIFEST_SHA256,
        "manifest_entries": manifest_entries,
        "upstream_source_commit": "e3714d0a156f6ed151d4521debb2b89ce4f1075c",
        "source_replay_verified": True,
        "source_LRAT_checker_verified": source_proof["verified"],
        "independent_coordinate_modes_equal": True,
        "points": normal_prepare["vertices"],
        "declared_edges_exactly_unit": normal_prepare["declared_edges"],
        "review_residues_sha256": normal_prepare["review_residues_sha256"],
        "all_pairs_audited": normal_finish["all_pairs_audited"],
        "independent_sieve_prime": normal_finish["independent_sieve_prime"],
        "independent_strict_edges": normal_finish["strict_unit_edges"],
        "independent_strict_sieve_false_positives":
            normal_finish["independent_sieve_false_positives"],
        "strict_sieve_sha256": normal_finish["survivor_sha256"],
        "variables": normal_finish["variables"],
        "clauses": normal_finish["clauses"],
        "CNF_sha256": normal_finish["CNF_sha256"],
        "LRAT_bytes": lrat.stat().st_size,
        "LRAT_sha256": LRAT_SHA256,
        "independent_LRAT_verified": True,
        "independent_LRAT_additions": proof["additions"],
        "independent_LRAT_deletions": proof["deletions"],
        "independent_LRAT_deletion_records": proof["deletion_records"],
        "independent_LRAT_hints_used": proof["hints_used"],
        "truth_table_LRAT_controls":
            controls["truth_table_instances_and_hint_orders"],
        "non_four_colourability_verified": True,
        "physical_core_extracted": False,
        "target_508_found": False,
    }
    expected = json.loads((HERE / "EXPECTED.json").read_text())
    need(receipt == expected, "final receipt mismatch")
    print(json.dumps(receipt, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
