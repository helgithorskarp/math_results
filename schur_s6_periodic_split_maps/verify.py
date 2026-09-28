"""Regenerate and independently check periodic-split DRAT proofs."""

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
    cases = expected["cases"]
    assert cases
    selected = args.cases if args.cases else sorted(cases)
    for key in selected:
        reference = cases[key]
        period, offset = map(int, key.split("-"))
        assert (reference["period"], reference["offset"]) == (period, offset)
        with tempfile.TemporaryDirectory(prefix=f"schur-periodic-{key}-") as temp:
            cnf = Path(temp) / "case.cnf"
            proof = Path(temp) / "case.drat"
            dimensions = write_cnf(period, offset, cnf)
            assert dimensions == audit_cnf(period, offset, cnf)
            assert dimensions == {key: reference[key] for key in dimensions}
            assert cnf.stat().st_size == reference["cnf_bytes"]
            assert sha256(cnf) == reference["cnf_sha256"]

            solved = subprocess.run(
                [str(args.cadical), "-q", "--sat", "--seed=20260928",
                 "-t", str(args.timeout), str(cnf), str(proof)],
                text=True, capture_output=True, check=False,
            )
            if solved.returncode != 20 or "s UNSATISFIABLE" not in solved.stdout:
                raise RuntimeError(f"case {key}: solver did not prove UNSAT: "
                                   f"{solved.stdout} {solved.stderr}")
            checked = subprocess.run(
                [str(args.drat_trim), str(cnf), str(proof)],
                text=True, capture_output=True, check=False,
            )
            if checked.returncode != 0 or "s VERIFIED" not in checked.stdout:
                raise RuntimeError(f"case {key}: checker rejected proof: "
                                   f"{checked.stdout} {checked.stderr}")
            exact = (proof.stat().st_size == reference["reference_proof_bytes"]
                     and sha256(proof) == reference["reference_proof_sha256"])
            print(f"PASS case={key} unsat=yes drat_verified=yes "
                  f"reference_proof_match={'yes' if exact else 'no'} "
                  f"proof_bytes={proof.stat().st_size}", flush=True)

    print(f"PASS all_requested_cases={len(selected)}", flush=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--cadical", type=Path, required=True)
    parser.add_argument("--drat-trim", type=Path, required=True)
    parser.add_argument("--cases", nargs="*")
    parser.add_argument("--timeout", type=int, default=600)
    verify(parser.parse_args())
