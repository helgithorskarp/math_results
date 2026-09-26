"""Generate and independently check every direct 71-point lifting proof.

Ranges are half open. Every completed case is written atomically; resumes
check all saved input/proof hashes. A partial range never certifies the full
family. Use audit.py to join disjoint ranges and check complete coverage.
"""
import argparse
import ctypes
import json
from pathlib import Path
import subprocess
import time

from pysat.solvers import Solver
from evidence import (COUNT, DOMAIN_SHA256, VERIFIED, atomic_json, audit_record,
                      case_files, cnf_bytes, digest, load_domain)
from point_model import decode_and_check, generate


def check_proof(checker, cnf, proof, log):
    with log.open("w") as stream:
        result = subprocess.run([str(checker), str(cnf), str(proof)],
                                stdout=stream, stderr=subprocess.STDOUT)
    if result.returncode != 0 or "s VERIFIED" not in log.read_text():
        raise ValueError("independent DRAT proof check failed")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--domain", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--drat-trim", type=Path, required=True)
    parser.add_argument("--start", type=int, default=0)
    parser.add_argument("--stop", type=int, default=COUNT)
    parser.add_argument("--conflicts", type=int, default=500000)
    parser.add_argument("--recheck-existing", action="store_true")
    args = parser.parse_args()
    if not 0 <= args.start < args.stop <= COUNT or args.conflicts <= 0:
        parser.error("invalid interval or conflict budget")
    domain = load_domain(args.domain)
    out = args.out.resolve()
    out.mkdir(parents=True, exist_ok=True)
    checker = args.drat_trim.resolve()
    checker_hash = digest(checker)
    libc = ctypes.CDLL(None)
    libc.fflush.argtypes = [ctypes.c_void_p]
    libc.fflush.restype = ctypes.c_int
    begun = time.monotonic()
    verified = reused = 0
    for index in range(args.start, args.stop):
        representative = domain[index]
        cnf, proof, log, path = case_files(out, index)
        cnf.parent.mkdir(parents=True, exist_ok=True)
        if path.exists():
            record = audit_record(out, index, representative)
            if args.recheck_existing:
                check_proof(checker, cnf, proof, log)
                record["checker_sha256"] = checker_hash
                atomic_json(path, record)
            verified += 1
            reused += 1
            continue
        formula, gauge = generate(representative["weights"])
        if formula.nv != 125 or sum(map(int, representative["weights"])) != 71:
            raise ValueError("incorrect formula cardinality or variable domain")
        cnf.write_bytes(cnf_bytes(formula))
        started = time.monotonic()
        with Solver(name="cadical195", bootstrap_with=formula.clauses,
                    with_proof=True) as solver:
            solver.conf_budget(args.conflicts)
            answer = solver.solve_limited()
            stats = solver.accum_stats()
            solver_seconds = time.monotonic() - started
            if answer is True:
                points = decode_and_check(representative["weights"], solver.get_model())
                if len(points) != 71:
                    raise ValueError("incorrect witness cardinality")
                atomic_json(out / f"WITNESS71_{index}.json",
                            {"status": "SAT_71_POINT_WITNESS", "index": index,
                             "points": points, "weights": representative["weights"]})
                raise RuntimeError(f"SAT witness at {index}; exclusion fails")
            if answer is None:
                atomic_json(out / f"UNKNOWN_{index}.json",
                            {"index": index, "status": "UNKNOWN", "stats": stats})
                raise RuntimeError(f"UNKNOWN at {index}; no exclusion established")
            # PySAT's convenience decoder need not retain the complete native
            # binary stream. Flush and copy that stream before deleting solver.
            if libc.fflush(None) != 0:
                raise RuntimeError("native proof-stream flush failed")
            solver.solver.prfile.seek(0)
            proof.write_bytes(solver.solver.prfile.read())
        check_proof(checker, cnf, proof, log)
        record = {
            "index": index, "type": representative["type"],
            "weights": representative["weights"], "gauge": list(gauge),
            "variables": formula.nv, "clauses": len(formula.clauses),
            "input_catalogue_sha256": DOMAIN_SHA256,
            "cnf_sha256": digest(cnf), "proof_sha256": digest(proof),
            "proof_bytes": proof.stat().st_size, "status": VERIFIED,
            "checker_sha256": checker_hash, "stats": stats,
            "solver_seconds": solver_seconds, "total_seconds": time.monotonic() - started,
            "conflict_limit": args.conflicts,
        }
        atomic_json(path, record)
        verified += 1
        if verified % 100 == 0:
            print(json.dumps({"through": index, "verified": verified,
                              "seconds": time.monotonic() - begun}), flush=True)
    result = {
        "status": "COMPLETE_RANGE_DRAT_VERIFIED", "start": args.start,
        "stop": args.stop, "verified": verified, "reused_records": reused,
        "complete_family": args.start == 0 and args.stop == COUNT,
        "input_catalogue_sha256": DOMAIN_SHA256, "checker_sha256": checker_hash,
        "seconds": time.monotonic() - begun,
    }
    atomic_json(out / f"replay_{args.start}_{args.stop}.json", result)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
