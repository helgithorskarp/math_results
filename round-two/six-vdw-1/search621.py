"""Bounded construction probes; an unchecked UNSAT is not a theorem.

Run one child/skeleton at a time, with an external timeout. A SAT proposal is
decoded and checked by the independent integer-AP checker before writing it.
"""
import argparse
import hashlib
import json
import resource
import time
from pathlib import Path
import fiber621 as enc
import audit621 as check


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--skeleton", required=True,
                   choices=[name for name, tau in enc.skeletons()])
    p.add_argument("--conflicts", type=int, default=5000)
    p.add_argument("--output", type=Path, required=True)
    args = p.parse_args()
    if not 1 <= args.conflicts <= 10000:
        raise ValueError("conflict cap must be between 1 and 10000")
    began = time.monotonic()
    tau = dict(enc.skeletons())[args.skeleton]
    weighted = enc.edges(tau)
    direct = check.direct_edges(tau)
    check.require(weighted == direct, "literal constraint dictionary mismatch")
    result = {"author": "six-vdw-1", "role": "researcher", "period": 621,
              "skeleton": args.skeleton, "skeleton_values": tau,
              "edges": len(weighted), "static_weight": sum(weighted.values()),
              "dictionary_sha256": check.dictionary_digest(weighted),
              "conflict_cap": args.conflicts}
    from pysat.solvers import Solver
    import pysat
    result["python_sat_version"] = pysat.__version__
    with Solver(name="cadical195", bootstrap_with=enc.clauses(weighted),
                with_proof=True) as solver:
        solver.conf_budget(args.conflicts)
        status = solver.solve_limited()
        result["solver_statistics"] = solver.accum_stats()
        if status is True:
            model = solver.get_model()
            assignment = {abs(literal): int(literal > 0) for literal in model}
            u = [assignment[x + 1] for x in range(207)]
            word = enc.decode(tau, u)
            check.require(check.cyclic_count(word) == 0, "invalid cyclic SAT proposal")
            bits = "".join(map(str, word)) * 6
            result["integer_check"] = check.check_coloring(bits, 3726)
            result["status"] = "EXACTLY_CHECKED_WITNESS"
            result["orientation"] = u
            witness = args.output.with_suffix(".bits")
            witness.write_text(bits + "\n")
            result["witness_sha256"] = hashlib.sha256(witness.read_bytes()).hexdigest()
        elif status is False:
            proof = solver.get_proof()
            proof_path = args.output.with_suffix(".drup")
            proof_path.write_text("\n".join(proof) + "\n")
            result["status"] = "UNVERIFIED_SOLVER_UNSAT"
            result["proof_lines"] = len(proof)
            result["proof_sha256"] = hashlib.sha256(proof_path.read_bytes()).hexdigest()
            # Proof checking is a separate obligation; no exclusion is claimed.
        else:
            result["status"] = "UNKNOWN"
    result["elapsed_seconds"] = round(time.monotonic() - began, 6)
    result["max_rss_kib"] = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({key: result[key] for key in
                      ("skeleton", "status", "edges", "elapsed_seconds", "max_rss_kib")},
                     sort_keys=True), flush=True)


if __name__ == "__main__":
    main()
