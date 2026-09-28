"""Regenerate and verify the noninjective decadal-map DRAT certificate."""

import argparse
import hashlib
import json
import subprocess
import tempfile
from pathlib import Path

from audit import check as audit_cnf
from encode import write_cnf

HERE = Path(__file__).resolve().parent


def sha256(path):
    digest = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def verify(args):
    expected = json.loads((HERE / "expected.json").read_text(encoding="ascii"))
    with tempfile.TemporaryDirectory(prefix="schur-decadal-maps-") as temp:
        cnf = Path(temp) / "case.cnf"
        proof = Path(temp) / "case.drat"
        dimensions = write_cnf(cnf)
        assert dimensions == audit_cnf(cnf)
        assert dimensions == {key: expected[key] for key in dimensions}
        assert cnf.stat().st_size == expected["cnf_bytes"]
        assert sha256(cnf) == expected["cnf_sha256"]

        solved = subprocess.run(
            [str(args.cadical), "-q", "--sat", "--seed=20260928", "-t", "300",
             str(cnf), str(proof)],
            text=True, capture_output=True, check=False,
        )
        if solved.returncode != 20 or "s UNSATISFIABLE" not in solved.stdout:
            raise RuntimeError(f"solver did not prove UNSAT: {solved.stdout} {solved.stderr}")
        checked = subprocess.run(
            [str(args.drat_trim), str(cnf), str(proof)],
            text=True, capture_output=True, check=False,
        )
        if checked.returncode != 0 or "s VERIFIED" not in checked.stdout:
            raise RuntimeError(f"DRAT checker rejected proof: {checked.stdout} {checked.stderr}")
        exact = (proof.stat().st_size == expected["reference_proof_bytes"]
                 and sha256(proof) == expected["reference_proof_sha256"])
        print("PASS noninjective_decadal_maps_unsat=yes drat_verified=yes "
              f"reference_proof_match={'yes' if exact else 'no'} "
              f"proof_bytes={proof.stat().st_size}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--cadical", type=Path, required=True)
    parser.add_argument("--drat-trim", type=Path, required=True)
    verify(parser.parse_args())
