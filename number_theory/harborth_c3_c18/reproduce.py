#!/usr/bin/env python3
"""Regenerate all three CNFs, solve, independently check, and audit semantics."""
import argparse
import hashlib
import json
import platform
import resource
import subprocess
import time
from pathlib import Path
from encode import build
from audit import run as semantic_audit


def sha(path):
    digest=hashlib.sha256()
    with Path(path).open("rb") as source:
        for chunk in iter(lambda:source.read(1<<20),b""):digest.update(chunk)
    return digest.hexdigest()


def invoke(command,log,seconds):
    started=time.monotonic()
    with log.open("w") as out:
        result=subprocess.run(command,stdout=out,stderr=subprocess.STDOUT,
                              timeout=seconds)
    return result.returncode,round(time.monotonic()-started,6)


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--kissat",type=Path,required=True)
    parser.add_argument("--drat-trim",type=Path,required=True)
    parser.add_argument("--work",type=Path,required=True)
    parser.add_argument("--seconds",type=int,default=300,
                        help="solver limit per case; incomplete runs fail")
    args=parser.parse_args()
    if args.seconds<=0:raise ValueError("positive time limit required")
    args.kissat=args.kissat.resolve();args.drat_trim=args.drat_trim.resolve()
    args.work=args.work.resolve();args.work.mkdir(parents=True,exist_ok=True)
    expected=json.loads(Path(__file__).with_name("expected.json").read_text())
    started=time.monotonic()
    audit=semantic_audit()
    (args.work/"audit.json").write_text(json.dumps(audit,indent=2,sort_keys=True)+"\n")
    if audit!=expected["semantic_audit"]:raise ValueError("semantic audit mismatch")
    results=[]
    for case in expected["cases"]:
        a,b=case["total"];name=f"case{a}{b}"
        cnf,meta,_,_=build(total=(a,b))
        cnf_file=args.work/(name+".cnf");proof_file=args.work/(name+".drat")
        cnf.write(cnf_file)
        if sha(cnf_file)!=case["cnf_sha256"]:raise ValueError("CNF hash mismatch")
        for field in ["variables","clauses","forbidden_complements"]:
            if meta[field]!=case[field]:raise ValueError("instance size mismatch")
        solve_log=args.work/(name+".solve.log")
        code,solve_time=invoke([str(args.kissat),f"--time={args.seconds}",
                               str(cnf_file),str(proof_file)],solve_log,args.seconds+30)
        if code!=20 or "s UNSATISFIABLE" not in solve_log.read_text():
            raise RuntimeError(f"{name} not proved UNSAT; exit{code}; inspect{solve_log}")
        check_log=args.work/(name+".check.log")
        code,check_time=invoke([str(args.drat_trim),str(cnf_file),str(proof_file)],
                               check_log,max(300,args.seconds*3))
        if code!=0 or "s VERIFIED" not in check_log.read_text():
            raise RuntimeError(f"{name} certificate failed; exit{code}; inspect{check_log}")
        row={"total":[a,b],"cnf_sha256":sha(cnf_file),"proof_sha256":sha(proof_file),
             "proof_bytes":proof_file.stat().st_size,"solver_exit":20,"checker_exit":0,
             "checker_status":"VERIFIED","solver_seconds":solve_time,
             "checker_seconds":check_time,
             "matches_recorded_proof":sha(proof_file)==case["proof_sha256"]}
        results.append(row)
        # Persist only completed cases, so an interrupted run is unambiguous.
        (args.work/"completed_cases.json").write_text(json.dumps(results,indent=2)+"\n")
        print(json.dumps(row),flush=True)
    report={"status":"VERIFIED_g_C3_C18_EQUALS_21","lower":21,"upper":21,
            "cases":results,"covered_totals":54,
            "semantic_audit_sha256":sha(args.work/"audit.json"),
            "python":platform.python_version(),
            "solver_version":subprocess.check_output([str(args.kissat),"--version"],text=True).strip(),
            "solver_binary_sha256":sha(args.kissat),"checker_binary_sha256":sha(args.drat_trim),
            "elapsed_seconds":round(time.monotonic()-started,6),
            "children_peak_rss_kib":resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,
            "formal_proof_assistant":False}
    (args.work/"verified.json").write_text(json.dumps(report,indent=2)+"\n")
    print(report["status"],flush=True)


if __name__=="__main__":
    main()
