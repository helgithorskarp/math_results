"""Exercise public replay across type boundaries and reject incomplete evidence."""
import argparse
import csv
import hashlib
import json
from pathlib import Path
import subprocess
import sys

HERE = Path(__file__).resolve().parent


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--drat-trim", type=Path, required=True)
    args = parser.parse_args()
    out = args.out.resolve()
    out.mkdir(parents=True, exist_ok=True)
    checker = args.drat_trim.resolve()
    with (HERE/"certificates.csv").open(newline="") as source:
        manifest = list(csv.DictReader(source))
    verified = []
    hash_matches = 0
    for start, stop in ((0,1), (88,89), (163,165), (1415,1417), (4331,4332)):
        directory = out/f"replay-{start}-{stop}"
        command = [sys.executable, str(HERE/"replay.py"), "--out", str(directory),
                   "--drat-trim", str(checker), "--start", str(start), "--stop", str(stop)]
        subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        result = json.loads((directory/"replay.json").read_text())
        if result["complete_family"] or result["verified"] != stop-start:
            raise RuntimeError("incorrect partial replay status")
        for record in result["cases"]:
            if record["status"] != "UNSAT_DRAT_VERIFIED":
                raise RuntimeError("unchecked replay case")
            verified.append(record["index"])
            hash_matches += record["proof_sha256"] == manifest[record["index"]]["proof_sha256"]

    limited = subprocess.run(
        [sys.executable, str(HERE/"replay.py"), "--out", str(out/"unknown"),
         "--drat-trim", str(checker), "--start", "88", "--stop", "89", "--conflicts", "1"],
        capture_output=True, text=True)
    if limited.returncode == 0 or "UNKNOWN in case 88" not in limited.stderr:
        raise RuntimeError("the budget-one UNKNOWN control did not fail as required")
    if (out/"unknown/replay.json").exists():
        raise RuntimeError("UNKNOWN run left a misleading completion record")

    empty = out/"empty.drat"
    empty.write_bytes(b"")
    failed = subprocess.run([str(checker), str(out/"replay-0-1/case_0000.cnf"), str(empty)],
                            capture_output=True, text=True)
    if failed.returncode == 0 or "s VERIFIED" in failed.stdout:
        raise RuntimeError("empty proof was incorrectly accepted")
    result = {"status":"DIRECT72_PIPELINE_CONTROLS_PASSED", "replayed_indices":verified,
              "proof_hashes_equal_original":hash_matches, "unknown_rejected":True,
              "empty_proof_rejected":True, "partial_runs_marked_incomplete":True,
              "checker_sha256":hashlib.sha256(checker.read_bytes()).hexdigest()}
    (out/"pipeline-controls.json").write_text(json.dumps(result, indent=2)+"\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
