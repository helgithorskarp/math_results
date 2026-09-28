"""Regenerate and independently verify all ten block-trade DRAT proofs."""

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


def check_case(offset, expected, cadical, drat_trim):
    with tempfile.TemporaryDirectory(prefix=f"schur-block-{offset}-") as temp:
        cnf = Path(temp) / "case.cnf"
        proof = Path(temp) / "case.drat"
        dimensions = write_cnf(cnf, offset)
        audited = audit_cnf(cnf, offset)
        assert dimensions == audited
        assert dimensions == {key: expected[key] for key in dimensions}
        assert sha256(cnf) == expected["cnf_sha256"]

        solved = subprocess.run(
            [str(cadical), "-q", "--no-binary", str(cnf), str(proof)],
            text=True, capture_output=True, check=False,
        )
        if solved.returncode != 20 or "s UNSATISFIABLE" not in solved.stdout:
            raise RuntimeError(f"offset {offset}: solver failed: {solved.stdout} {solved.stderr}")
        checked = subprocess.run(
            [str(drat_trim), str(cnf), str(proof)],
            text=True, capture_output=True, check=False,
        )
        if checked.returncode != 0 or "s VERIFIED" not in checked.stdout:
            raise RuntimeError(f"offset {offset}: proof rejected: {checked.stdout} {checked.stderr}")
        same_proof = (proof.stat().st_size == expected["proof_bytes"]
                      and sha256(proof) == expected["proof_sha256"])
        print(f"VERIFIED offset={offset} drat=yes "
              f"reference_proof_match={'yes' if same_proof else 'no'} "
              f"proof_bytes={proof.stat().st_size}", flush=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--cadical", type=Path, required=True)
    parser.add_argument("--drat-trim", type=Path, required=True)
    parser.add_argument("--offset", type=int, action="append", choices=range(1, 11),
                        help="check selected offset(s), default all ten")
    args = parser.parse_args()
    expected = {row["offset"]: row for row in json.loads((HERE / "expected.json").read_text())}
    assert set(expected) == set(range(1, 11))
    selected = args.offset or list(range(1, 11))
    for offset in selected:
        check_case(offset, expected[offset], args.cadical, args.drat_trim)
    print(f"PASS block_offsets_unsat={len(selected)} drat_verified={len(selected)}")
