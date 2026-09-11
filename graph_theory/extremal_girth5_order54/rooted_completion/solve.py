"""Run a bounded exact graph-completion search; UNKNOWN is not a refutation."""

import argparse, hashlib, json, resource, time
from pathlib import Path
from pysat.solvers import Solver
from model import target, decode, verify


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--z", type=int, choices=(9, 10, 11), required=True)
    p.add_argument("--a", type=int, required=True)
    p.add_argument("--c", type=int, required=True)
    p.add_argument("--solver", choices=("g4", "cadical195"), default="g4")
    p.add_argument("--conflicts", type=int, default=200000)
    p.add_argument("--output", type=Path, required=True)
    p.add_argument("--gap", action="store_true")
    p.add_argument("--structure", action="store_true")
    args = p.parse_args()
    if args.conflicts <= 0:
        raise ValueError("Conflict limit must be positive")
    args.output.mkdir(parents=True, exist_ok=False)
    t = time.perf_counter()
    cnf, data = target(args.z, args.a, args.c)
    if args.gap:
        from gap import add_energy

        add_energy(cnf, data)
    if args.structure:
        from high_structure import add_structure

        add_structure(cnf, data, args.z)
    formula = args.output / "formula.cnf"
    cnf.to_file(str(formula))
    r = dict(
        z=args.z,
        a=args.a,
        c=args.c,
        solver=args.solver,
        budget=args.conflicts,
        gap=args.gap,
        structure=args.structure,
        variables=cnf.nv,
        clauses=len(cnf.clauses),
        build_seconds=time.perf_counter() - t,
        formula_sha256=hashlib.sha256(formula.read_bytes()).hexdigest(),
    )
    (args.output / "started.json").write_text(json.dumps(r, indent=2) + "\n")
    print(json.dumps(r), flush=True)
    t = time.perf_counter()
    with Solver(name=args.solver, bootstrap_with=cnf, with_proof=True) as solver:
        solver.conf_budget(args.conflicts)
        ans = solver.solve_limited(expect_interrupt=True)
        r.update(
            status="UNSAT" if ans is False else "SAT" if ans else "UNKNOWN",
            solve_seconds=time.perf_counter() - t,
            statistics=solver.accum_stats(),
            peak_self_rss_KiB=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
        )
        if ans is False:
            (args.output / "proof.drup").write_text(
                "\n".join(solver.get_proof()) + "\n"
            )
        elif ans:
            edges = decode(data, solver.get_model())
            r["verification"] = verify(
                54, edges, {6: args.z + 4, 7: 50 - 2 * args.z, 8: args.z}
            )
            (args.output / "witness.json").write_text(
                json.dumps(dict(n=54, edges=edges), indent=2) + "\n"
            )
    (args.output / "result.json").write_text(json.dumps(r, indent=2) + "\n")
    print(json.dumps(r), flush=True)


if __name__ == "__main__":
    main()
