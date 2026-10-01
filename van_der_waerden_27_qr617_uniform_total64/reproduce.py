#!/usr/bin/env python3
"""Generate48 primitives and audit all114 partitions serially, each capped90s."""
import argparse
import datetime
import hashlib
import json
import os
import resource
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOTS = [1, 618, 1235, 1852, 2469, 3086]
CHILDREN = [286, 571, 856, 1141, 1426, 1711]
BUDGETS = [[30,33], [31,32], [32,31], [33,30]]
TASKS = [("root", r) for r in ROOTS] + [("controls", r) for r in ROOTS]
TASKS += [("split", None), ("coverage", None)]
BASIC = ["Boolean_endpoint", "wrong_endpoint", "wrong_root", "swapped_original_budget",
         "enlarged_original_budget", "extra_initial_hypothesis", "supplied_parent_state",
         "false_terminal", "incomplete_terminal"]
SPLIT = ["missing_child", "duplicate_child", "Boolean_child", "child_outside_full_petal",
         "nonmandatory_split", "wrong_child_budget", "wrong_child_root",
         "extra_child_hypothesis", "supplied_child_state"]


def require(condition, message):
    if not condition:
        raise ValueError(message)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--output-dir", type=Path, required=True)
    p.add_argument("--resume", action="store_true")
    a = p.parse_args()
    work = a.output_dir.resolve()
    require(not work.is_relative_to(HERE.parent.resolve()), "Generated proof data must stay outside the repository")
    if work.exists() and not a.resume:
        p.error("Choose a fresh output directory or explicitly resume checked completed jobs")
    work.mkdir(parents=True, exist_ok=True)
    jobs, proofs, parts = [work / n for n in ("jobs", "proofs", "partitions")]
    for directory in (jobs, proofs, parts):
        directory.mkdir(exist_ok=True)
    pins = {path.name: hashlib.sha256(path.read_bytes()).hexdigest()
            for path in sorted(HERE.glob("*.py"))}
    pins.update({name: hashlib.sha256((HERE/name).read_bytes()).hexdigest()
                 for name in ("expected.json", "provenance.json")})
    pin_path = work / "source-pins.json"
    if pin_path.exists():
        require(json.loads(pin_path.read_text()) == pins, "Saved computation used different source")
    else:
        pin_path.write_text(json.dumps(pins, indent=2)+"\n")
    expected = json.loads((HERE/"expected.json").read_text())
    env = os.environ.copy()
    env.update({key: "1" for key in ["OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS",
        "NUMEXPR_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "BLIS_NUM_THREADS", "OMP_THREAD_LIMIT", "NUMBA_NUM_THREADS"]})
    start = time.monotonic()
    completed = []

    def run_stage(token, command):
        record = jobs / (token+".json")
        if record.exists():
            saved = json.loads(record.read_text())
            require(a.resume and saved["status"] == "FINISHED" and saved["returncode"] == 0 and
                    saved["command"] == command and saved["cap_seconds"] == 90,
                    "Interrupted or failed saved job: no automatic retry")
            completed.append(token)
            return
        row = {"agent": "six-vdw-2", "role": "researcher", "token": token,
               "command": command, "status": "STARTED", "returncode": None,
               "threads": 1, "cap_seconds": 90}
        record.write_text(json.dumps(row, indent=2)+"\n")
        begin = time.monotonic()
        with (jobs/(token+".log")).open("w") as stdout, (jobs/(token+".err")).open("w") as stderr:
            try:
                result = subprocess.run(command, env=env, stdout=stdout, stderr=stderr, timeout=90)
                row.update(status="FINISHED", returncode=result.returncode)
            except subprocess.TimeoutExpired:
                row.update(status="TIME_LIMIT")
        row.update(seconds=round(time.monotonic()-begin,3),
                   max_child_rss_kib=resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,
                   finished_utc=datetime.datetime.now(datetime.timezone.utc).isoformat())
        record.write_text(json.dumps(row, indent=2)+"\n")
        require(row["status"] == "FINISHED" and row["returncode"] == 0,
                "Bounded job failed or timed out; preserve progress, no exclusion or automatic retry")
        completed.append(token)
        print(json.dumps({"completed": token, "seconds": row["seconds"], "clean_exit": True}), flush=True)

    for B in BUDGETS:
        for root in ROOTS:
            token = f"generate-{B[0]}-{B[1]}-root{root}-parent"
            command = [sys.executable, str(HERE/"generate.py"), "--output", str(proofs),
                       "--budget", *map(str,B), "--root", str(root), "--seconds", "90"]
            run_stage(token, command)
            if root == 1:
                for child in CHILDREN:
                    run_stage(f"generate-{B[0]}-{B[1]}-root1-child{child}", command+["--child",str(child)])
    expected_names = {row["file"] for box in expected["boxes"] for row in box["certificates"]}
    require({p.name for p in proofs.glob("tree-*.json")} == expected_names, "Incomplete full forest file coverage")
    for box in expected["boxes"]:
        for row in box["certificates"]:
            raw = (proofs/row["file"]).read_bytes()
            require(len(raw) == row["bytes"] and hashlib.sha256(raw).hexdigest() == row["sha256"],
                    "Fresh certificate differs from the expected complete proof")
    for mode in ("normal", "optimized"):
        interpreter = [sys.executable]+(["-O"] if mode == "optimized" else [])
        for B in BUDGETS:
            for task, root in TASKS:
                token = f"{mode}-{B[0]}-{B[1]}-{task}"+("" if root is None else f"-{root}")
                command = interpreter+[str(HERE/"verify.py"),str(proofs),"--budget",*map(str,B),
                                       "--task",task,"--output",str(parts/(token+".json"))]
                if root is not None:
                    command += ["--root",str(root)]
                run_stage(token,command)
        token = mode+"-arithmetic"
        run_stage(token,interpreter+[str(HERE/"verify.py"),str(proofs),"--task","arithmetic",
                                    "--output",str(parts/(token+".json"))])
    require(len(completed) == len(set(completed)) == 162, "Missing or duplicate primitive/partition coverage")
    all_names = [f"{mode}-{B[0]}-{B[1]}-{task}"+("" if r is None else f"-{r}")+".json"
                 for mode in ("normal","optimized") for B in BUDGETS for task,r in TASKS]
    all_names += [mode+"-arithmetic.json" for mode in ("normal","optimized")]
    require({p.name for p in parts.glob("*.json")} == set(all_names), "Wrong complete partition file coverage")
    box_results = []
    for B in BUDGETS:
        expected_controls = [(r,n) for r in ROOTS for n in BASIC]+[(1,n) for n in SPLIT]
        expected_controls += [(r,"missing_mandatory_root") for r in ROOTS]+[(None,"unexpected_root")]
        require(len(expected_controls) == len(set(expected_controls)) == 70, "Invalid meaningful control specification")
        loaded = {}
        for task, root in TASKS:
            suffix = f"-{B[0]}-{B[1]}-{task}"+("" if root is None else f"-{root}")
            paths = [parts/(mode+suffix+".json") for mode in ("normal","optimized")]
            require(paths[0].read_bytes() == paths[1].read_bytes(), "Mode partition bytes differ")
            part = json.loads(paths[0].read_text())
            require((part["endpoint"],part["budget"],part["task"],part["root"]) == (0,B,task,root),
                    "Wrong partition quantifiers")
            for mode in ("normal","optimized"):
                log = json.loads((jobs/(mode+suffix+".log")).read_text())
                require((log["budget"],log["task"],log["root"],log["optimized_flag"]) ==
                        (B,task,root,1 if mode == "optimized" else 0), "Wrong interpreter mode or partition")
            loaded[(task,root)] = part["result"]
        root_parts = [loaded[("root",r)] for r in ROOTS]
        controls = [x for r in ROOTS for x in loaded[("controls",r)]["rejected"]]
        controls += loaded[("split",None)]["rejected"]+loaded[("coverage",None)]["rejected"]
        require([(x.get("root"),x["name"]) for x in controls] == expected_controls, "Incomplete exact corruption-control coverage")
        box = next(x for x in expected["boxes"] if x["budget"] == B)
        require([x["certificate"] for x in root_parts] == box["certificates"] and
                [x["root_result"] for x in root_parts] == box["verification"]["root_results"] and
                [x["parent_state"] for x in root_parts] == box["parent_states"], "Full root/certificate/state results differ")
        box_results.append({"budget":B,"root_results": [x["root_result"] for x in root_parts],
                            "corruption_controls_rejected":len(controls)})
    require((parts/"normal-arithmetic.json").read_bytes() == (parts/"optimized-arithmetic.json").read_bytes(),
            "Mode arithmetic bytes differ")
    for mode in ("normal","optimized"):
        require(json.loads((jobs/(mode+"-arithmetic.log")).read_text())["optimized_flag"] ==
                (1 if mode == "optimized" else 0), "Wrong arithmetic interpreter mode")
    summary = {"agent":"six-vdw-2","role":"researcher","status":"UNIFORM64_COMPLETE_FRESH_REPRODUCTION_PASSED",
               "generation_primitives":48,"validation_partitions":114,"root_cases":24,"nodes":48,"splits":4,"closed_leaves":44,
               "controls_per_mode":280,"full_parent_state_regressions":24,"certificate_bytes":expected["certificate_bytes"],
               "all_certificate_bytes_match":True,"all_mode_partition_bytes_identical":True,
               "class_bounds_both_endpoints":[30,1818],"total_bounds_both_endpoints":[64,3632],
               "arithmetic":json.loads((parts/"normal-arithmetic.json").read_text())["result"],
               "threads":1,"primitive_and_validation_caps_seconds":90,"seconds":round(time.monotonic()-start,3),
               "peak_child_rss_kib":resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,
               "length3704_witness_or_new_W_bound_asserted":False}
    (work/"summary.json").write_text(json.dumps(summary,indent=2)+"\n")
    print(json.dumps({k:v for k,v in summary.items() if k != "arithmetic"}),flush=True)


if __name__ == "__main__":
    main()
