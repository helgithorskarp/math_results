#!/usr/bin/env python3
"""Serial cold replays, complete byte comparisons and adverse controls."""
from pathlib import Path
import argparse
import hashlib
import json
import os
import subprocess
import sys
import time
import urllib.request
try:
    import resource
except ImportError:
    resource = None
from baseline import URL,replay

HERE = Path(__file__).resolve().parent


def canonical(value):
    return json.dumps(value,separators=(",", ":"))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--scratch",type=Path,default=HERE/".scratch")
    parser.add_argument("--baseline",type=Path)
    args = parser.parse_args()
    args.scratch.mkdir(parents=True,exist_ok=True)
    raw = args.baseline.read_bytes() if args.baseline else urllib.request.urlopen(URL,timeout=20).read()
    primary = replay(raw)
    expected = json.loads((HERE/"EXPECTED.json").read_text())
    env = os.environ.copy()
    for key in ("OPENBLAS_NUM_THREADS","OMP_NUM_THREADS","MKL_NUM_THREADS",
                "NUMEXPR_NUM_THREADS","VECLIB_MAXIMUM_THREADS","BLIS_NUM_THREADS"):
        env[key] = "1"
    jobs = [("derive-normal",["derive.py","--emit"],False),
            ("derive-optimized",["derive.py","--emit"],True),
            ("verify-normal",["verify.py","--emit"],False),
            ("verify-optimized",["verify.py","--emit"],True),
            ("self-normal",["verify.py","--self-test"],False),
            ("self-optimized",["verify.py","--self-test"],True)]
    runs = []
    whole = None
    start = time.monotonic()
    for name,arguments,optimized in jobs:
        command = [sys.executable]+(["-O"] if optimized else [])+[str(HERE/arguments[0]),*arguments[1:]]
        output = args.scratch/(name+".json")
        errors = args.scratch/(name+"-stderr.txt")
        begin = time.monotonic()
        with output.open("wb") as out,errors.open("wb") as err:
            try:
                child = subprocess.run(command,stdout=out,stderr=err,env=env,timeout=90)
            except subprocess.TimeoutExpired:
                raise RuntimeError(name+": fixed 90s child guard; no exclusion follows")
        if child.returncode:
            raise RuntimeError(name+": child failed, see "+str(errors))
        content = output.read_bytes()
        value = json.loads(content)
        if name.startswith(("derive-","verify-")):
            if whole is None:
                whole = content
                summary = {key:item for key,item in value.items() if key != "domains"}
                summary["red_book_witnesses"] = value["domains"]["red_books"]
                if canonical(summary) != canonical(expected):
                    raise ValueError("fresh whole producer differs from frozen compact summary")
            elif content != whole:
                raise ValueError("complete fresh mathematical records differ byte-for-byte")
        elif value != {"six_point_subset_pairs":4096,"SX_orbit_transports":1440,
                       "known_red_book_witnesses":192,"rejected_damages":16}:
            raise ValueError("adverse/transport controls differ")
        measurement = {"name":name,"command":command,"exit_code":child.returncode,
                       "elapsed_seconds":round(time.monotonic()-begin,6),
                       "output_bytes":len(content),"output_sha256":hashlib.sha256(content).hexdigest(),
                       "cumulative_peak_child_RSS_KiB":resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss if resource else None}
        runs.append(measurement)
        checkpoint = {"agent":"six-books-1","role":"researcher","primary_baseline":primary,
                      "threads":1,"one_intensive_child_at_a_time":True,"child_guard_seconds":90,
                      "complete_jobs":len(runs),"planned_jobs":len(jobs),"runs":runs,
                      "completed":len(runs)==len(jobs),
                      "whole_mathematical_bytes":len(whole),"whole_mathematical_sha256":hashlib.sha256(whole).hexdigest(),
                      "elapsed_seconds":round(time.monotonic()-start,6)}
        (args.scratch/"validation.json").write_text(json.dumps(checkpoint,indent=2)+"\n")
        print(canonical(measurement),flush=True)
    print(canonical({"completed":True,"counts":expected["counts"],
                     "whole_mathematical_bytes":len(whole),"whole_mathematical_sha256":hashlib.sha256(whole).hexdigest()}),flush=True)


if __name__ == "__main__":
    main()
