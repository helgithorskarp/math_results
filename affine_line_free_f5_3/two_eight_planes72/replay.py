"""Regenerate UNSAT proofs and check them in a separate DRAT-trim process."""
import argparse
import ctypes
import hashlib
import json
from pathlib import Path
import subprocess
import time

from pysat.solvers import Solver
from model import decode_and_check, generate

HERE = Path(__file__).resolve().parent


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--drat-trim", type=Path, required=True)
    parser.add_argument("--start", type=int, default=0)
    parser.add_argument("--stop", type=int, default=164)
    parser.add_argument("--conflicts", type=int, default=300000)
    args = parser.parse_args()
    if not 0 <= args.start < args.stop <= 164 or args.conflicts <= 0:
        parser.error("invalid case interval or conflict budget")
    out = args.out.resolve()
    out.mkdir(parents=True, exist_ok=True)
    checker = args.drat_trim.resolve()
    representatives = json.loads((HERE/"orbits.json").read_text())
    expected = json.loads((HERE/"certificates.json").read_text())["cases"]
    libc = ctypes.CDLL(None)
    libc.fflush.argtypes = [ctypes.c_void_p]
    libc.fflush.restype = ctypes.c_int
    results = []
    for i in range(args.start, args.stop):
        word = representatives[i]["weights"]
        formula, gauge = generate(word)
        cnf, proof, log = (out/f"case_{i:03d}.{suffix}" for suffix in ("cnf", "drat", "check.log"))
        formula.to_file(str(cnf))
        if digest(cnf) != expected[i]["cnf_sha256"]:
            raise RuntimeError(f"CNF hash mismatch in case {i}")
        start = time.monotonic()
        with Solver(name="cadical195", bootstrap_with=formula.clauses, with_proof=True) as solver:
            solver.conf_budget(args.conflicts)
            answer = solver.solve_limited()
            if answer is True:
                witness = decode_and_check(word, solver.get_model())
                (out/f"counterexample_{i:03d}.json").write_text(json.dumps(witness)+"\n")
                raise RuntimeError(f"SAT witness in case {i}; claimed exclusion fails")
            if answer is None:
                raise RuntimeError(f"UNKNOWN in case {i}; increase the budget, no exclusion established")
            # PySAT 1.9.dev15 does not flush the native stream in get_proof().
            # Its binary-to-text helper also failed on one valid trace. Preserve
            # the flushed raw binary stream, and let DRAT-trim parse it directly.
            if libc.fflush(None) != 0:
                raise RuntimeError("native proof stream flush failed")
            solver.solver.prfile.seek(0)
            proof.write_bytes(solver.solver.prfile.read())
            stats = solver.accum_stats()
        with log.open("w") as output:
            checked = subprocess.run([str(checker), str(cnf), str(proof)],
                                     stdout=output, stderr=subprocess.STDOUT)
        if checked.returncode != 0 or "s VERIFIED" not in log.read_text():
            raise RuntimeError(f"independent proof check failed in case {i}")
        record = {"index": i, "status": False, "verified": True, "gauge": gauge,
                  "cnf_sha256": digest(cnf), "proof_sha256": digest(proof),
                  "proof_format": "binary DRAT", "proof_bytes": proof.stat().st_size,
                  "seconds_total": time.monotonic()-start, "stats": stats}
        (out/f"case_{i:03d}.json").write_text(json.dumps(record, indent=2)+"\n")
        results.append(record)
        print(json.dumps({"case": i, "status": "DRAT_VERIFIED"}), flush=True)
    summary = {"start": args.start, "stop": args.stop, "verified": len(results),
               "complete_family": args.start == 0 and args.stop == 164,
               "checker_sha256": digest(checker), "cases": results}
    (out/"replay.json").write_text(json.dumps(summary, indent=2)+"\n")


if __name__ == "__main__":
    main()
