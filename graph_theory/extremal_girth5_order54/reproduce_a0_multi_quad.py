#!/usr/bin/env python3
"""Regenerate and independently check the complete multi-quad exclusion."""
import argparse, hashlib, json, platform, resource, subprocess, time
from pathlib import Path
from pysat.solvers import Solver
from a0_multi_quad_sat import build, cases, case_name, proof_stage
from a0_unit_check import unit_contradiction

HERE = Path(__file__).resolve().parent

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def check_proof(checker, formula, proof, log, clauses):
    with log.open("w") as out:
        run = subprocess.run([str(checker), str(formula), str(proof)],
                             stdout=out, stderr=subprocess.STDOUT)
    text = log.read_text()
    ordinary = run.returncode == 0 and "s VERIFIED" in text
    # This pinned drat-trim leaves sts=ERROR on parse-time UNSAT and exits 1.
    # Never accept that exit code without a separate exact contradiction.
    trivial = (run.returncode == 1 and "c trivial UNSAT" in text
               and "s VERIFIED" in text)
    independent = unit_contradiction(clauses) if trivial else None
    return ordinary or (trivial and independent), run.returncode, independent

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--work", type=Path, required=True)
    ap.add_argument("--checker", type=Path, required=True)
    ap.add_argument("--case", help="Exact multiquad_INDEX_ORBIT name; default all 357.")
    ap.add_argument("--replay", type=Path, help="Directory of existing named .drup traces.")
    ap.add_argument("--conflicts", type=int, default=0, help="0 means unlimited; UNKNOWN fails.")
    args = ap.parse_args()
    work, checker = args.work.resolve(), args.checker.resolve()
    if work == HERE or HERE in work.parents:
        raise ValueError("Generated outputs must be outside the source tree.")
    if args.conflicts < 0:
        raise ValueError("Negative conflict limit.")
    work.mkdir(parents=True, exist_ok=True)
    selected = [c for c in cases() if args.case is None or case_name(c) == args.case]
    if not selected:
        raise ValueError("Unknown case.")
    records = []
    expected_path = HERE / "a0_multi_quad_expected.json"
    expected = ({r["name"]: r for r in json.loads(expected_path.read_text())["refutations"]}
                if expected_path.exists() else {})
    for case in selected:
        name = case_name(case)
        formula = work / (name + ".cnf")
        trace = work / (name + ".drup")
        if formula.exists() or trace.exists():
            raise FileExistsError(name)
        start = time.monotonic()
        cnf, data = build(*case, stage=proof_stage(case))
        cnf.to_file(str(formula))
        build_seconds = time.monotonic() - start
        solve_seconds = None
        stats = None
        if args.replay:
            trace = args.replay.resolve() / (name + ".drup")
            if not trace.is_file():
                raise FileNotFoundError(trace)
        else:
            start = time.monotonic()
            with Solver(name="g4", bootstrap_with=cnf, with_proof=True) as solver:
                if args.conflicts:
                    solver.conf_budget(args.conflicts)
                    answer = solver.solve_limited(expect_interrupt=True)
                else:
                    answer = solver.solve()
                stats = solver.accum_stats()
                solve_seconds = time.monotonic() - start
                if answer is not False:
                    record = {"case": case, "status": "SAT" if answer else "UNKNOWN"}
                    if answer:
                        model = set(solver.get_model())
                        record["selected_vertices"] = [
                            (i, d, sorted(B), j)
                            for i, (d, B, j) in enumerate(data["vertices"])
                            if data["X"][i] in model]
                        record["selected_edges"] = [
                            uv for uv, e in data.get("E", {}).items() if e in model]
                    (work / (name + "_nonrefutation.json")).write_text(
                        json.dumps(record, indent=2) + "\n")
                    raise RuntimeError("Nonrefutation preserved; coverage incomplete.")
                trace.write_text("\n".join(solver.get_proof()) + "\n")
        start = time.monotonic()
        verified, code, unit = check_proof(
            checker, formula, trace, work / (name + "_check.log"), cnf.clauses)
        record = dict(
            case=list(case), name=name, stage=proof_stage(case),
            variables=cnf.nv, clauses=len(cnf.clauses),
            slots=len(data["vertices"]), edge_variables=len(data.get("E", {})),
            formula_sha256=sha(formula), trace_sha256=sha(trace),
            trace_bytes=trace.stat().st_size, verified=verified,
            checker_returncode=code, independent_unit_contradiction=unit,
            build_seconds=build_seconds, solve_seconds=solve_seconds,
            check_seconds=time.monotonic()-start, statistics=stats)
        records.append(record)
        with (work / "progress.jsonl").open("a") as out:
            out.write(json.dumps(record) + "\n")
        print(json.dumps({"case": case, "verified": verified}), flush=True)
        if not verified:
            raise RuntimeError("Certificate verification failed.")
        if expected:
            for field in ("stage", "variables", "clauses", "slots",
                          "edge_variables", "formula_sha256"):
                if record[field] != expected[name][field]:
                    raise ValueError("Expected formula mismatch: " + name + " " + field)
    result = dict(complete_cover=len(selected) == len(list(cases())),
                  python=platform.python_version(), checker_sha256=sha(checker),
                  peak_self_rss_KiB=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
                  peak_child_rss_KiB=resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,
                  replay=args.replay is not None, records=records)
    (work / "result.json").write_text(json.dumps(result, indent=2) + "\n")
    return result

if __name__ == "__main__":
    main()
