#!/usr/bin/env python3
"""Regenerate and independently audit the formula; never run a solver."""
from pathlib import Path
import argparse
import hashlib
import json
import subprocess
import sys
import tempfile

HERE = Path(__file__).resolve().parent
SOURCE = HERE.parent / "ramsey_r55_k4_expansion_interface"
SOURCE_MANIFEST = "18273dc7ca8a1a7e693a05a98a31df0c3c4b0b250efcf172f87bf97a61e1b78c"
TASK = "bo1-q7-r7-c000000"


def need(ok, message):
    if not ok:
        raise ValueError(message)


def digest(path):
    value = hashlib.sha256()
    with Path(path).open("rb") as stream:
        while chunk := stream.read(1024 * 1024):
            value.update(chunk)
    return value.hexdigest()


def source_identity():
    raw = (SOURCE / "SHA256SUMS").read_bytes()
    need(hashlib.sha256(raw).hexdigest() == SOURCE_MANIFEST, "interface source manifest")
    lines = raw.decode().splitlines()
    need(len(lines) == 16, "interface source entry count")
    for line in lines:
        wanted, name = line.split("  ", 1)
        need(digest(SOURCE / name) == wanted, "interface source identity " + name)
    return len(lines)


def package_identity():
    count = 0
    for line in (HERE / "SHA256SUMS").read_text().splitlines():
        wanted, name = line.split("  ", 1)
        need(digest(HERE / name) == wanted, "boundary package identity " + name)
        count += 1
    return count


def command(optimized, script, *arguments):
    answer = [sys.executable]
    if optimized:
        answer.append("-O")
    answer.extend(["-B", str(script), *map(str, arguments)])
    return answer


def run(cache):
    source_entries = source_identity()
    expected = json.loads((HERE / "FORMULA_AUDIT.json").read_text())
    with tempfile.TemporaryDirectory(prefix="r55-k4e-q7r7-") as raw:
        cnf = Path(raw) / "formula.cnf"
        produced = subprocess.run(command(False, SOURCE / "augment.py", cache,
                                  "--task", TASK, "--triangles", "--cnf", cnf),
                                  check=True, text=True, stdout=subprocess.PIPE).stdout
        producer = json.loads(produced)
        for key in ("variables", "clauses", "bytes", "max_width", "sha256",
                    "ordered_variables", "ordered_clauses", "expansion_variables",
                    "expansion_clauses"):
            need(producer[key] == expected[key], "producer field " + key)
        need(digest(cnf) == expected["sha256"], "generated formula identity")
        audits = []
        for optimized in (False, True):
            checked = subprocess.run(command(optimized, SOURCE / "audit.py",
                                     "--cache", cache, "--task", TASK,
                                     "--triangles", "--cnf", cnf), check=True,
                                     text=True, stdout=subprocess.PIPE).stdout
            record = json.loads(checked)
            need(record == expected, "independent full literal audit")
            audits.append(record)
    compact = []
    for optimized in (False, True):
        checked = subprocess.run(command(optimized, HERE / "compact_check.py"),
                                 check=True, text=True, stdout=subprocess.PIPE).stdout
        compact.append(json.loads(checked))
    need(compact[0] == compact[1], "normal/-O compact result")
    return {
        "status": "REPRODUCED_K4_EXPANSION_Q7R7_UNKNOWN_BOUNDARY",
        "source_manifest_entries": source_entries,
        "package_manifest_entries": package_identity(),
        "normal_and_optimized_literal_audits_match": audits[0] == audits[1],
        "normal_and_optimized_compact_checks_match": compact[0] == compact[1],
        "formula_sha256": expected["sha256"],
        "solver_status": "UNKNOWN",
        "solver_calls": 0,
        "target43_found": False
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("cache", type=Path)
    args = parser.parse_args()
    print(json.dumps(run(args.cache), sort_keys=True))
