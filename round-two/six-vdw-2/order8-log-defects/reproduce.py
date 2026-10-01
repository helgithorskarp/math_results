"""Serial, capped regeneration and exact replay of the order-eight defect cut."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import resource
import subprocess
import sys
import time
import urllib.request

from audit import audit, counter_controls
from check_rup_lrat import verify

ROOT = Path(__file__).resolve().parent


def require(condition, message):
    if not condition:
        raise ValueError(message)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--work", type=Path, required=True)
    ap.add_argument("--resume", action="store_true")
    ap.add_argument("--drat-source", type=Path)
    args = ap.parse_args()
    began = time.monotonic()
    work = args.work.resolve()
    expected = json.loads((ROOT/"expected.json").read_text())
    env = dict(os.environ, OMP_NUM_THREADS="1", OPENBLAS_NUM_THREADS="1",
               MKL_NUM_THREADS="1", NUMEXPR_NUM_THREADS="1")
    pins = {p.name: sha(p) for p in ROOT.iterdir()
            if p.is_file() and p.suffix in (".py", ".json", ".txt")}
    require(pins["check_rup_lrat.py"] == expected["reused_checker"]["sha256"], "changed reused checker")
    if args.resume:
        require((work/"pins.json").is_file(), "no complete input checkpoint")
        require(json.loads((work/"pins.json").read_text()) == pins, "source pins changed")
    else:
        require(not work.exists() or not any(work.iterdir()), "use a fresh work directory")
        work.mkdir(parents=True, exist_ok=True)
        (work/"pins.json").write_text(json.dumps(pins, sort_keys=True, indent=2)+"\n")
    timings = {}
    def run(label, command, limit=30):
        start = time.monotonic()
        try:
            result = subprocess.run(list(map(str, command)), env=env,
                                    capture_output=True, text=True, timeout=limit)
        except subprocess.TimeoutExpired as error:
            raise ValueError(f"{label}: timeout; no mathematical exclusion") from error
        timings[label] = time.monotonic()-start
        require(result.returncode == 0,
                f"{label}: failed; no mathematical exclusion: {result.stderr[-2000:]}")
        return result.stdout
    cnf = work/"order8-defect11.cnf"
    metadata = json.loads(run("encode", [sys.executable, ROOT/"encode.py", cnf, "--bound", 11]))
    require(metadata["cnf_sha256"] == expected["cnf_sha256"], "different exact instance")
    direct = audit(cnf, 11)
    for key in ("variables", "clauses", "field_edges", "direct_retained_APs", "direct_zero_APs_removed"):
        require(direct[key] == expected[key], "different exact coverage: "+key)
    require(counter_controls()["exhaustive_counter_inputs"] == expected["counter_inputs_checked"], "different counter coverage")
    source = work/"drat-trim.c"
    if args.drat_source:
        source.write_bytes(args.drat_source.read_bytes())
    elif not source.exists():
        source.write_bytes(urllib.request.urlopen(expected["converter"]["url"], timeout=20).read())
    require(sha(source) == expected["converter"]["sha256"], "unrecognized converter source")
    converter = work/"drat-trim"
    run("compile_converter", ["gcc", "-O2", "-std=gnu99", source, "-o", converter])
    drat, lrat = cnf.with_suffix(".drat"), cnf.with_suffix(".lrat")
    solved = cnf.with_suffix(".solve.json")
    if args.resume and solved.exists():
        record = json.loads(solved.read_text())
        require(record["status"] == "UNSAT_PENDING_CHECK" and record["cnf_sha256"] == sha(cnf), "incomplete solver checkpoint")
        require(drat.exists() and record["drat_sha256"] == sha(drat), "incomplete proof checkpoint")
    else:
        require(not drat.exists(), "unmarked partial proof; use a fresh stem")
        record = json.loads(run("solve", [sys.executable, ROOT/"solve.py", cnf]))
        require(record["status"] == "UNSAT_PENDING_CHECK", "no complete candidate proof")
    converted = work/"conversion.complete.json"
    if args.resume and converted.exists():
        record2 = json.loads(converted.read_text())
        require(record2 == {"drat_sha256": sha(drat), "lrat_sha256": sha(lrat)}, "changed converted proof")
    else:
        require(not lrat.exists(), "unmarked partial conversion; use a fresh stem")
        output = run("convert", [converter, cnf, drat, "-t", 25, "-L", lrat])
        require("s VERIFIED" in output, "conversion unsuccessful")
        converted.write_text(json.dumps({"drat_sha256": sha(drat), "lrat_sha256": sha(lrat)}, indent=2)+"\n")
    # These checks always replay, even when expensive proposal stages resume.
    exact = verify(cnf, lrat)
    optimized = json.loads(run("optimized_check", [sys.executable, "-O", ROOT/"check_rup_lrat.py", cnf, lrat]))
    require(all(exact[k] == optimized[k] for k in exact), "optimized checker differs")
    controls = json.loads(run("controls", [sys.executable, ROOT/"controls.py", cnf, lrat, "--work", work/"controls"]))
    optimized_controls = json.loads(run("optimized_controls", [sys.executable, "-O", ROOT/"controls.py", cnf, lrat, "--work", work/"controls-O"]))
    require(controls == optimized_controls, "optimized controls differ")
    incomplete = work/"one-conflict.cnf"
    if args.resume and incomplete.with_suffix(".solve.json").exists():
        require(json.loads(incomplete.with_suffix(".solve.json").read_text())["status"] == "UNKNOWN", "bad budget checkpoint")
    else:
        incomplete.write_bytes(cnf.read_bytes())
        limited = json.loads(run("one_conflict_control", [sys.executable, ROOT/"solve.py", incomplete, "--conflicts", 1]))
        require(limited["status"] == "UNKNOWN", "one-conflict control did not stop")
    require(not incomplete.with_suffix(".drat").exists(), "incomplete solver emitted exclusion proof")
    result = {"agent": "six-vdw-2", "role": "researcher", "status": expected["status"],
              "equal_pair_floor": 13, "multiplicative_equal_pair_floor": 104,
              "excluded_labeled_templates": expected["excluded_labeled_templates"],
              "encoding": direct, "RUP": exact, "controls": controls,
              "reference_RUP_byte_match": exact["proof_sha256"] == expected["reference_RUP"]["proof_sha256"],
              "one_conflict_UNKNOWN": True, "threads": 1, "CPU_jobs_at_once": 1,
              "seconds": time.monotonic()-began, "stage_seconds": timings,
              "maxrss_parent_kib": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
              "maxrss_child_kib": resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,
              "Python": sys.version, "source_pins": pins}
    (work/"result.json").write_text(json.dumps(result, sort_keys=True, indent=2)+"\n")
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
