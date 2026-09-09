#!/usr/bin/env python3
"""Reproduce the compact 238-source theorem without a SAT solver."""
from hashlib import sha256
from pathlib import Path
import argparse
import json
import subprocess
import sys
import time

HERE = Path(__file__).resolve().parent
SOURCE = (HERE.parent / "ramsey_r55_cyclic43_q13_boundary_certificate" /
          "objective-twelve-component-fast.json")


def need(condition, message):
    if not condition:
        raise ValueError(message)


def run(command, log):
    started = time.monotonic()
    with log.open("x") as output:
        process = subprocess.run(command, stdout=output, stderr=subprocess.STDOUT,
                                 check=False)
    need(process.returncode == 0, f"command failed, see {log}")
    return time.monotonic() - started


def deterministic(report):
    result = dict(report)
    result.pop("verification_seconds", None)
    return result


def verify_sha256s():
    checked = 0
    for line in (HERE / "SHA256SUMS").read_text().splitlines():
        expected, name = line.split("  ", 1)
        path = HERE / name
        need(path.is_file(), f"missing manifest file {name}")
        need(sha256(path.read_bytes()).hexdigest() == expected,
             f"hash mismatch for {name}")
        checked += 1
    return checked


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    output = args.output.resolve()
    need(not output.exists(), "output directory must not exist")
    output.mkdir(parents=True)
    expected = json.loads((HERE / "EXPECTED.json").read_text())
    common = [str(HERE / "check_certificate.py"), str(SOURCE),
              str(HERE / "cores.dimacs"), str(HERE / "proofs.drat"), "--quiet"]
    normal_json = output / "normal.json"
    optimized_json = output / "optimized.json"
    normal_seconds = run([sys.executable, "-B", *common,
                          "--output", str(normal_json)], output / "normal.log")
    optimized_seconds = run([sys.executable, "-B", "-O", *common,
                             "--output", str(optimized_json)], output / "optimized.log")
    normal = deterministic(json.loads(normal_json.read_text()))
    optimized = deterministic(json.loads(optimized_json.read_text()))
    need(normal == optimized == expected, "normal/optimized/expected mismatch")
    controls_seconds = run([sys.executable, "-B", str(HERE / "controls.py")],
                           output / "controls.log")
    controls_opt_seconds = run([sys.executable, "-B", "-O",
                                str(HERE / "controls.py")],
                               output / "controls-optimized.log")
    controls = json.loads((output / "controls.log").read_text())
    controls_opt = json.loads((output / "controls-optimized.log").read_text())
    need(controls == controls_opt and
         controls["status"] == "VERIFIED_CERTIFICATE_CONTROLS",
         "certificate controls mismatch")
    census = json.loads((HERE / "census.json").read_text())
    need(census["status"] == expected["status"] and
         census["source_count"] == expected["source_count"], "census headline")
    result = {
        "status": "REPRODUCED_CYCLIC43_238_SEIDEL_CLASS_EXCLUSION",
        "manifest_files_checked": verify_sha256s(),
        "source_count": expected["source_count"],
        "physical_core_clauses": expected["physical_core_clauses"],
        "rup_additions": expected["proof_totals"]["rup_additions"],
        "normal_seconds": normal_seconds,
        "optimized_seconds": optimized_seconds,
        "controls_seconds": controls_seconds,
        "controls_optimized_seconds": controls_opt_seconds,
    }
    (output / "result.json").write_text(json.dumps(result, indent=2,
                                                    sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
