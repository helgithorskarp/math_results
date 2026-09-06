#!/usr/bin/env python3
"""One bounded, sequential, restartable decision for each catalog-switch family."""
import argparse
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path
import resource
import signal
import subprocess
import time
from physical import catalog, decode, require
from check import check

stop_requested = False


def request_stop(signum, frame):
    global stop_requested
    stop_requested = True


def save(path, value):
    temporary = path.with_suffix(path.suffix+".tmp")
    temporary.write_text(json.dumps(value, indent=2)+"\n")
    temporary.replace(path)


def run(command, log, timeout):
    start = time.monotonic()
    before = resource.getrusage(resource.RUSAGE_CHILDREN)
    with log.open("w") as output:
        process = subprocess.Popen(list(map(str, command)), stdout=output, stderr=subprocess.STDOUT)
        expired = False
        try:
            code = process.wait(timeout=timeout)
        except subprocess.TimeoutExpired:
            expired = True
            process.terminate()
            try:
                code = process.wait(timeout=10)
            except subprocess.TimeoutExpired:
                process.kill()
                code = process.wait()
    after = resource.getrusage(resource.RUSAGE_CHILDREN)
    return {"command": list(map(str, command)), "exit_code": code, "wall_timeout": expired,
            "wall_seconds": time.monotonic()-start, "user_seconds": after.ru_utime-before.ru_utime,
            "system_seconds": after.ru_stime-before.ru_stime,
            "children_max_rss_KiB": after.ru_maxrss}


def model(record, log):
    graph = decode(record)
    n = len(graph)
    values = {}
    for line in log.read_text().splitlines():
        if line.startswith("v "):
            for literal in map(int, line.split()[1:]):
                if literal:
                    require(1<=abs(literal)<=2*n-1 and abs(literal) not in values, "Bad model literal")
                    values[abs(literal)] = int(literal > 0)
    require(set(values)==set(range(1,2*n)), "Incomplete model")
    spin = {0:0, **{v:values[v] for v in range(1,n)}}
    red = {(u,v): graph[u][v]^spin[u]^spin[v] if v<n else values[n+u]
           for u,v in combinations(range(n+1),2)}
    defects=[0,0]
    for vertices in combinations(range(n+1),5):
        colors={red[edge] for edge in combinations(vertices,2)}
        if len(colors)==1:
            defects[colors.pop()] += 1
    require(defects==[0,0], f"Invalid decoded graph {defects}")
    return {"vertices": n+1, "red_edges":[list(e) for e,bit in red.items() if bit],
            "blue_K5":0,"red_K5":0}


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("folder",type=Path)
    parser.add_argument("--catalog",type=Path,default=Path(__file__).with_name("r55_42some.g6"))
    parser.add_argument("--generator",type=Path,required=True)
    parser.add_argument("--kissat",type=Path,required=True)
    parser.add_argument("--drat-trim",type=Path,required=True)
    args=parser.parse_args()
    records=catalog(args.catalog)
    args.folder.mkdir(parents=True,exist_ok=True)
    signal.signal(signal.SIGTERM, request_stop)
    signal.signal(signal.SIGINT, request_stop)
    completed=[]
    total_start=time.monotonic()
    for index,record in enumerate(records):
        if stop_requested or (args.folder/"STOP").exists():
            save(args.folder/"stopped.json",{"status":"STOPPED_AT_CASE_BOUNDARY","next_parent":index})
            print(json.dumps({"status":"STOPPED_AT_CASE_BOUNDARY","next_parent":index}),flush=True)
            return
        folder=args.folder/f"parent{index:03d}"
        folder.mkdir(exist_ok=True)
        checkpoint=folder/"result.json"
        if checkpoint.exists():
            saved=json.loads(checkpoint.read_text())
            require(saved["parent"]==index and saved["seed"]==record, "Saved input mismatch")
            require(saved["status"]=="CHECKED_SWITCH_EXTENSION_EXCLUSION", "Unresolved prior case; no retry")
            require(check(record,folder/"core.cnf",folder/"trimmed.drat")==saved["certificate"],
                    "Saved proof no longer verifies")
            completed.append(saved)
            continue
        require(not (folder/"solver.log").exists(), "Interrupted solver invocation: inspect before resuming")
        result={"parent":index,"seed":record,"status":"STARTED"}
        if not (folder/"family.cnf").exists():
            result["generation"]=run([args.generator.resolve(),args.catalog.resolve(),index,folder/"family.cnf"],
                                     folder/"generation.log",60)
            require(result["generation"]["exit_code"]==0,"Generation failed")
        result["cnf_sha256"]=sha256((folder/"family.cnf").read_bytes()).hexdigest()
        result["solver"]=run([args.kissat.resolve(),"--time=30","--no-binary",folder/"family.cnf",folder/"proof.drat"],
                             folder/"solver.log",45)
        code=result["solver"]["exit_code"]
        if code==10 and not result["solver"]["wall_timeout"]:
            save(folder/"target.json",model(record,folder/"solver.log"))
            result["status"]="DIRECTLY_CHECKED_TARGET"
        elif code==20 and not result["solver"]["wall_timeout"]:
            require("s UNSATISFIABLE" in (folder/"solver.log").read_text(), "Missing UNSAT status")
            result["status"]="UNSAT_PROOF_PENDING"
            save(checkpoint,result)
            result["proof_check"]=run([args.drat_trim.resolve(),folder/"family.cnf",folder/"proof.drat",
                                       "-c",folder/"core.cnf","-l",folder/"trimmed.drat"],folder/"proof_check.log",300)
            require(result["proof_check"]["exit_code"]==0 and
                    "s VERIFIED" in (folder/"proof_check.log").read_text(),"Unverified proof")
            start=time.monotonic()
            result["certificate"]=check(record,folder/"core.cnf",folder/"trimmed.drat")
            result["direct_check_seconds"]=time.monotonic()-start
            result["status"]="CHECKED_SWITCH_EXTENSION_EXCLUSION"
        else:
            result["status"]="NO_CONCLUSION"
        result["files"]={p.name:{"bytes":p.stat().st_size,"sha256":sha256(p.read_bytes()).hexdigest()}
                         for p in sorted(folder.iterdir()) if p.is_file() and p.name!="result.json"}
        save(checkpoint,result)
        completed.append(result)
        save(args.folder/"progress.json",{"checked":sum(r["status"]=="CHECKED_SWITCH_EXTENSION_EXCLUSION" for r in completed),
                                          "last_parent":index,"status":result["status"],
                                          "elapsed_seconds":time.monotonic()-total_start})
        print(json.dumps({"parent":index,"status":result["status"],"solver_seconds":result["solver"]["wall_seconds"],
                          "certificate_clauses":result.get("certificate",{}).get("core_clauses")}),flush=True)
        if result["status"]!="CHECKED_SWITCH_EXTENSION_EXCLUSION":
            return
    require(len(completed)==328,"Incomplete catalog")
    save(args.folder/"completed.json",{"status":"CHECKED_ENTIRE_CATALOG_SWITCH_EXTENSION_UNION",
                                      "parents":328,"elapsed_seconds":time.monotonic()-total_start})


if __name__=="__main__":
    main()
