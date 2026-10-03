"""Resumable serial source-only replay, one bounded intensive child at a time.

Outputs and logs are excluded from publication. Each child retains original
60s/2000000-state guards and has a60s external process timeout. A partial or
failed run supplies no bound. Separate cold normal/optimized copies generate
all required mathematical inputs themselves, then compare entire records.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import time
from operations import check_operations


def need(ok, message):
    if not ok:
        raise ValueError(message)


def encoded(value):
    return (json.dumps(value, sort_keys=True, separators=(",", ":")) + "\n").encode()


def read(path):
    return json.loads(path.read_bytes())


def pin(path):
    raw = path.read_bytes()
    return {"bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest()}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=("normal", "optimized"), required=True)
    parser.add_argument("--work", type=Path, required=True)
    parser.add_argument("--normal", type=Path)
    parser.add_argument("--resume", action="store_true")
    parser.add_argument("--max-stages", type=int, default=0)
    args = parser.parse_args()
    need(args.max_stages >= 0, "nonnegative stage boundary allowance")
    check_operations()
    original = Path(__file__).resolve().parent
    work = args.work.resolve()
    need(args.resume == work.exists(), "fresh replay directory or explicit resume")
    files = sorted(p.name for p in original.iterdir() if p.is_file() and (p.suffix in (".py", ".json") or p.name == "baseline69.txt") and p.name not in ("VALIDATION.json", "SOURCE_MANIFEST.json"))
    frozen = {name:pin(original/name) for name in files}
    if not args.resume:
        work.mkdir(parents=True)
        (work / "source").mkdir()
        for name in files:
            shutil.copyfile(original/name, work/"source"/name)
        plan = {"agent":"six-code-2","role":"researcher","mode":args.mode,"sources_and_fixtures":frozen,"original_math_seconds":60,"original_math_states":2000000,"external_child_seconds":60,"native_threads":1,"serial_children":1,"private_generated_inputs":[]}
        (work/"FROZEN_PLAN.json").write_bytes(encoded(plan))
        journal = {"agent":"six-code-2","role":"researcher","mode":args.mode,"status":"RUNNING_SOURCE_ONLY_SERIAL_REPLAY","stages":[]}
    else:
        plan = read(work/"FROZEN_PLAN.json")
        journal = read(work/"JOURNAL.json")
        need(plan["sources_and_fixtures"] == frozen and plan["mode"] == args.mode and
             journal["status"] in ("STOPPED_AT_SUCCESSFUL_STAGE_BOUNDARY","STOPPED_BEFORE_CHILD_OPERATIONS_BARRIER"), "only completed stage-boundary replay can resume")
    local = work/"source"
    need((args.mode == "optimized") == (args.normal is not None), "optimized requires completed normal reference; normal has no generated input reference")
    normal = args.normal.resolve() if args.normal is not None else None
    if normal is not None:
        need(read(normal/"JOURNAL.json")["status"] == "COMPLETE_SOURCE_ONLY_FOUR_FAMILIES" and
             read(normal/"FROZEN_PLAN.json")["sources_and_fixtures"] == frozen, "normal completed with identical source/fixtures")
    spec = read(local/"SPEC.json")
    stages = []
    for case in spec["cases"]:
        key = case["key"]; root=work/key
        parent=local/"PARENT.json"; control=local/case["control_file"]; cover_spec=local/case["cover_spec"]
        stages.extend([
            (key+"-caps","caps.py",["--parent",parent,"--q",case["q"],"--extra-empty-parents",*case["extras"],"--work",root/"carrier"]),
            (key+"-graph","graph.py",["--parent",parent,"--carrier",root/"carrier/CORES.json","--control69",control,"--work",root/"graph"]),
            (key+"-colors","colors.py",["--graph",root/"graph/GRAPH.json","--work",root/"colors"]),
            (key+"-audit","audit_h6.py",["--parent",parent,"--carrier",root/"carrier/CORES.json","--graph",root/"graph/GRAPH.json","--colors",root/"colors/COLORS.json","--producer-summary",root/"graph/SUMMARY.json","--witness-dir",root/"graph","--baseline69",local/"baseline69.txt","--control69",control,"--control-a",case["control_a"],"--control-R",case["control_R"],"--work",root/"point-audit"]),
            (key+"-cover","cover.py",["--parent",parent,"--spec",cover_spec,"--work",root/"cover"]),
            (key+"-cover-audit","audit_cover.py",["--parent",parent,"--spec",cover_spec,"--cover",root/"cover/COVER.json","--witness",root/"graph/WITNESS69.json","--known-seeds",local/"SEED_PAIRS.json","--work",root/"point-cover-audit"]),
        ])
    roots = [work/c["key"] for c in spec["cases"]]
    case_args = [item for root in roots for item in ("--case-root",root)]
    stages.extend([
        ("labels","hole_labels.py",["--parent",local/"PARENT.json",*case_args,"--work",work/"labels"]),
        ("links","unlabeled_links.py",["--parent",local/"PARENT.json",*case_args,"--labels",work/"labels/CERTIFICATES.json","--work",work/"links"]),
        ("domain","domain.py",[*case_args,"--work",work/"domain"]),
        ("whole-check","check_outputs.py",["--source",local,"--root",work,"--work",work/"whole-check"]),
    ])
    completed = len(journal["stages"])
    need([s[0] for s in stages[:completed]] == [s["stage"] for s in journal["stages"]], "completed exact stage prefix")
    environment = dict(os.environ)
    for key in ("OMP_NUM_THREADS","OPENBLAS_NUM_THREADS","MKL_NUM_THREADS","NUMEXPR_NUM_THREADS","BLIS_NUM_THREADS","VECLIB_MAXIMUM_THREADS"):
        environment[key]="1"
    environment["PYTHONDONTWRITEBYTECODE"]="1"
    interpreter = [sys.executable,"-B"] + (["-O"] if args.mode == "optimized" else [])

    def save():
        (work/"JOURNAL.json").write_bytes(encoded(journal))

    def check_sources():
        need({n:pin(original/n) for n in files} == frozen and {n:pin(local/n) for n in files} == frozen, "whole frozen source/fixture bytes changed")

    save()
    for offset, (name, script, arguments) in enumerate(stages[completed:]):
        if args.max_stages and offset >= args.max_stages:
            journal["status"]="STOPPED_AT_SUCCESSFUL_STAGE_BOUNDARY";save();print(json.dumps({"status":journal["status"],"completed_stages":len(journal["stages"])},sort_keys=True));return
        try:
            check_operations();check_sources()
        except Exception:
            journal["status"]="STOPPED_BEFORE_CHILD_OPERATIONS_BARRIER";save();raise
        argv = interpreter+[str(local/script),*map(str,arguments)]
        print(json.dumps({"starting":name,"mode":args.mode},sort_keys=True),flush=True)
        begin=time.monotonic();code=None;timeout=False
        with (work/(name+".stdout.txt")).open("wb") as out, (work/(name+".stderr.txt")).open("wb") as err:
            try:
                code=subprocess.run(argv,cwd=local,env=environment,stdout=out,stderr=err,timeout=60).returncode
            except subprocess.TimeoutExpired:
                timeout=True
        row={"stage":name,"script":script,"seconds":time.monotonic()-begin,"returncode":code,"timeout":timeout,"stdout":pin(work/(name+".stdout.txt")),"stderr":pin(work/(name+".stderr.txt"))}
        journal["stages"].append(row)
        if code!=0 or timeout or row["stderr"]["bytes"]:
            journal["status"]="FAILED_OR_INCOMPLETE_NO_ABSENCE";save();raise RuntimeError("Stopped incomplete child: "+name)
        check_sources();save()
        print(json.dumps({"completed":name,"mode":args.mode,"seconds":row["seconds"]},sort_keys=True),flush=True)
    check_sources();check_operations()
    if normal is not None:
        need((work/"whole-check/EXACT_RESULT.json").read_bytes() == (normal/"whole-check/EXACT_RESULT.json").read_bytes(), "entire cold normal/optimized mathematical record differs")
    journal["status"]="COMPLETE_SOURCE_ONLY_FOUR_FAMILIES"
    journal["whole_exact_result"]=pin(work/"whole-check/EXACT_RESULT.json")
    journal["normal_optimized_whole_equal"]=(True if normal is not None else None)
    save()
    print(json.dumps({"status":journal["status"],"mode":args.mode,"stages":len(stages),"whole_exact_result":journal["whole_exact_result"]},sort_keys=True),flush=True)


if __name__ == "__main__":
    main()
