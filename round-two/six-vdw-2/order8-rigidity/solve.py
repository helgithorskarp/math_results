"""Bounded untrusted SAT proposal; only checked RUP establishes an exclusion."""
import argparse
import ctypes
import hashlib
import json
from pathlib import Path
import time


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cnf", type=Path)
    ap.add_argument("--conflicts", type=int, default=50000)
    args = ap.parse_args()
    if not 1 <= args.conflicts <= 50000:
        raise ValueError("conflict budget outside authorized source bounds")
    for suffix in (".drat", ".solve.json"):
        if args.cnf.with_suffix(suffix).exists():
            raise ValueError("use a fresh solver stem; refusing stale output")
    from pysat.formula import CNF
    from pysat.solvers import Solver
    began = time.monotonic()
    cnf = CNF(from_file=str(args.cnf))
    with Solver(name="cadical195", bootstrap_with=cnf.clauses, with_proof=True) as solver:
        solver.conf_budget(args.conflicts)
        answer = solver.solve_limited()
        stats = solver.accum_stats()
        if answer is False:
            # PySAT's native proof stream must be flushed before reading it.
            libc = ctypes.CDLL(None)
            libc.fflush.argtypes = [ctypes.c_void_p]
            libc.fflush.restype = ctypes.c_int
            if libc.fflush(None) != 0:
                raise RuntimeError("proof stream flush failed")
            proof = "\n".join(solver.get_proof())+"\n"
            args.cnf.with_suffix(".drat").write_text(proof)
        elif answer is True:
            model = {abs(v): v > 0 for v in solver.get_model()}
            if not all(any(model[abs(v)] == (v > 0) for v in c) for c in cnf.clauses):
                raise RuntimeError("invalid satisfying assignment")
    record = {"status": {False: "UNSAT_PENDING_CHECK", True: "SAT", None: "UNKNOWN"}[answer],
              "solver": "cadical195", "conflict_budget": args.conflicts,
              "stats": stats, "seconds": time.monotonic()-began,
              "cnf_sha256": hashlib.sha256(args.cnf.read_bytes()).hexdigest()}
    if answer is False:
        record.update(proof_bytes=len(proof.encode()),
                      drat_sha256=hashlib.sha256(proof.encode()).hexdigest())
    args.cnf.with_suffix(".solve.json").write_text(json.dumps(record, indent=2)+"\n")
    print(json.dumps(record, sort_keys=True))


if __name__ == "__main__":
    main()
