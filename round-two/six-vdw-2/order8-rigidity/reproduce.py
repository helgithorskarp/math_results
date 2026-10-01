"""Serial capped regeneration and independent replay of all seventeen cases."""
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

from audit import audit_cover
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
    require([c["length"] for c in expected["cases"]] == list(range(2, 19)), "incomplete expected cover")
    env = dict(os.environ, OMP_NUM_THREADS="1", OPENBLAS_NUM_THREADS="1",
               MKL_NUM_THREADS="1", NUMEXPR_NUM_THREADS="1")
    pins = {p.name: sha(p) for p in ROOT.iterdir()
            if p.is_file() and p.suffix in (".py", ".json", ".txt")}
    require(pins["check_rup_lrat.py"] == expected["reused_checker"]["sha256"], "changed reused checker")
    if args.resume:
        require((work/"pins.json").is_file(), "no input checkpoint")
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

    for reference in expected["cases"]:
        length = reference["length"]
        cnf = work/f"run-{length}.cnf"
        metadata = json.loads(run(f"encode_{length}",
                                  [sys.executable, ROOT/"encode.py", cnf, "--length", length]))
        require(metadata["cnf_sha256"] == reference["cnf_sha256"], "different exact case instance")
    # One direct definition-level traversal, followed by every case comparison.
    audited = json.loads(json.dumps(audit_cover(work)))
    optimized_audit = json.loads(run("optimized_audit", [sys.executable, "-O", ROOT/"audit.py", work]))
    require(audited == optimized_audit, "optimized encoding audit differs")
    for key in ("field_edges", "direct_retained_APs", "direct_zero_APs_removed", "critical_AP", "controls"):
        require(audited[key] == expected[key], "different exact reduction coverage: "+key)
    source = work/"drat-trim.c"
    if args.drat_source:
        source.write_bytes(args.drat_source.read_bytes())
    elif not source.exists():
        source.write_bytes(urllib.request.urlopen(expected["converter"]["url"], timeout=20).read())
    require(sha(source) == expected["converter"]["sha256"], "unrecognized converter source")
    converter = work/"drat-trim"
    run("compile_converter", ["gcc", "-O2", "-std=gnu99", source, "-o", converter])
    checked = []
    for reference in expected["cases"]:
        length = reference["length"]
        cnf = work/f"run-{length}.cnf"
        drat, lrat, solved = (cnf.with_suffix(s) for s in (".drat", ".lrat", ".solve.json"))
        if args.resume and solved.exists():
            record = json.loads(solved.read_text())
            require(record["status"] == "UNSAT_PENDING_CHECK" and record["cnf_sha256"] == sha(cnf),
                    "incomplete solver checkpoint")
            require(drat.exists() and record["drat_sha256"] == sha(drat), "incomplete proof checkpoint")
        else:
            require(not drat.exists(), "unmarked partial solver trace; use a fresh stem")
            record = json.loads(run(f"solve_{length}", [sys.executable, ROOT/"solve.py", cnf]))
            require(record["status"] == "UNSAT_PENDING_CHECK", "no complete candidate proof")
        converted = work/f"run-{length}.conversion.complete.json"
        if args.resume and converted.exists():
            require(lrat.exists(), "missing converted proof")
            record2 = json.loads(converted.read_text())
            require(record2 == {"drat_sha256": sha(drat), "lrat_sha256": sha(lrat)}, "changed converted trace")
        else:
            require(not lrat.exists(), "unmarked partial conversion; use a fresh stem")
            output = run(f"convert_{length}", [converter, cnf, drat, "-t", 25, "-L", lrat])
            require("s VERIFIED" in output, "conversion unsuccessful")
            converted.write_text(json.dumps({"drat_sha256": sha(drat), "lrat_sha256": sha(lrat)}, indent=2)+"\n")
        # Independent verification always replays, including on resume.
        exact = verify(cnf, lrat)
        optimized = json.loads(run(f"optimized_replay_{length}",
                                   [sys.executable, "-O", ROOT/"check_rup_lrat.py", cnf, lrat]))
        require(all(exact[k] == optimized[k] for k in exact), "optimized proof checker differs")
        checked.append({"length": length, "solve": record, "RUP": exact,
                        "reference_RUP_byte_match": exact["proof_sha256"] == reference["proof_sha256"]})
        (work/"checked-cases.json").write_text(json.dumps(checked, sort_keys=True, indent=2)+"\n")
        print(json.dumps({"case": length, "status": "EXACT_CASE_REFUTATION_REPLAYED",
                          "additions": exact["checked_additions"]}), flush=True)
    require([c["length"] for c in checked] == list(range(2, 19)), "incomplete exact case cover")
    hard_cnf, hard_proof = work/"run-3.cnf", work/"run-3.lrat"
    controls = json.loads(run("controls", [sys.executable, ROOT/"controls.py", hard_cnf, hard_proof,
                                           "--work", work/"controls"]))
    optimized_controls = json.loads(run("optimized_controls",
        [sys.executable, "-O", ROOT/"controls.py", hard_cnf, hard_proof, "--work", work/"controls-O"]))
    require(controls == optimized_controls, "optimized corruption controls differ")
    incomplete = work/"one-conflict.cnf"
    if args.resume and incomplete.with_suffix(".solve.json").exists():
        limited = json.loads(incomplete.with_suffix(".solve.json").read_text())
        require(limited["cnf_sha256"] == sha(hard_cnf), "changed budget-control input")
    else:
        incomplete.write_bytes(hard_cnf.read_bytes())
        limited = json.loads(run("one_conflict_control",
            [sys.executable, ROOT/"solve.py", incomplete, "--conflicts", 1]))
    require(limited["status"] == "UNKNOWN", "one-conflict control did not stop")
    require(not incomplete.with_suffix(".drat").exists(), "incomplete solver emitted exclusion trace")
    result = {"agent": "six-vdw-2", "role": "researcher", "status": expected["status"],
              "H8_invariant_AP_free_patterns": 0, "excluded_labeled_patterns": 2**77,
              "encoding": audited, "checked_cases": checked, "controls": controls,
              "one_conflict_UNKNOWN": True, "threads": 1, "CPU_jobs_at_once": 1,
              "seconds": time.monotonic()-began, "stage_seconds": timings,
              "maxrss_parent_kib": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
              "maxrss_child_kib": resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,
              "Python": sys.version, "source_pins": pins}
    (work/"result.json").write_text(json.dumps(result, sort_keys=True, indent=2)+"\n")
    print(json.dumps({k: v for k, v in result.items() if k not in ("checked_cases", "source_pins", "stage_seconds")},
                     sort_keys=True))


if __name__ == "__main__":
    main()
