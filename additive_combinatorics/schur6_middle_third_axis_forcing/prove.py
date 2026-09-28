"""Regenerate the target CNF and a DRAT proof, then check the proof.

Requires external CaDiCaL and DRAT-trim executables. Temporary CNF, proof and
logs are removed after checking. The output contains compact provenance.
"""
import argparse
import hashlib
import json
import shutil
import subprocess
import tempfile
import time
from pathlib import Path

from model import dimacs


def sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def executable(name):
    found = shutil.which(name)
    if found is None:
        raise FileNotFoundError(name)
    return str(Path(found).resolve())


def run(cadical, drat_trim, timeout):
    expected = json.loads(Path(__file__).with_name("expected.json").read_text())["certificate"]
    data = dimacs()
    digest = hashlib.sha256(data).hexdigest()
    if digest != expected["cnf_sha256"] or len(data) != expected["cnf_bytes"]:
        raise RuntimeError("generated CNF differs from the audited instance")
    cadical, drat_trim = executable(cadical), executable(drat_trim)
    with tempfile.TemporaryDirectory(prefix="schur-middle-axis-") as name:
        folder = Path(name)
        cnf, proof = folder / "instance.cnf", folder / "proof.drat"
        cnf.write_bytes(data)
        start = time.monotonic()
        # Wait for the solver process to exit before reading the proof file.
        # This avoids accepting an incompletely flushed C stdio stream.
        result = subprocess.run([cadical, "-q", str(cnf), str(proof)],
                                capture_output=True, text=True, timeout=timeout)
        solver_seconds = time.monotonic() - start
        if result.returncode != 20 or "s UNSATISFIABLE" not in result.stdout:
            raise RuntimeError(("solver did not prove UNSAT", result.returncode,
                                result.stdout, result.stderr))
        proof_digest, proof_bytes = sha256(proof), proof.stat().st_size
        start = time.monotonic()
        checked = subprocess.run([drat_trim, str(cnf), str(proof), "-i", "-t", str(timeout)],
                                 capture_output=True, text=True, timeout=timeout + 10)
        checker_seconds = time.monotonic() - start
        if checked.returncode != 0 or "s VERIFIED" not in checked.stdout:
            raise RuntimeError(("proof not verified", checked.returncode,
                                checked.stdout, checked.stderr))
    return {
        "status": "DRAT_VERIFIED",
        "cnf_sha256": digest,
        "proof_sha256": proof_digest,
        "proof_bytes": proof_bytes,
        "matches_reference_proof": proof_digest == expected["proof_sha256"],
        "solver_seconds": round(solver_seconds, 3),
        "checker_seconds": round(checker_seconds, 3),
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--cadical", default="cadical")
    parser.add_argument("--drat-trim", default="drat-trim")
    parser.add_argument("--timeout", type=int, default=600,
                        help="maximum seconds for each external tool")
    args = parser.parse_args()
    print(json.dumps(run(args.cadical, args.drat_trim, args.timeout), indent=2))
