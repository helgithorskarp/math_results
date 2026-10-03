"""Actual semantic repaired-digest probes and complete small coefficient oracles."""
import ast
import collections
import copy
import hashlib
import itertools
import json
import math
import os
import resource
import subprocess
import time
from pathlib import Path


def need(ok, why):
    if not ok:
        raise ValueError(why)


def canon(x):
    return json.dumps(x, sort_keys=True, separators=(",", ":")).encode()


def load_function(path, name, extra):
    module = ast.parse(path.read_text())
    node = next(n for n in module.body if isinstance(n, ast.FunctionDef) and n.name == name)
    ns = {"collections": collections, "math": math, "need": need, **extra}
    exec(compile(ast.Module(body=[node], type_ignores=[]), str(path), "exec"), ns)
    return ns[name]


def toy_checks(h):
    grouped = load_function(h/"character617-size24-row-budget.py", "coefficients", {})
    individual = load_function(h/"check-character617-size24-row-budget.py", "individual_product", {})
    increment = load_function(h/"character617-size24-row-completion.py", "increment", {})
    coefficients = 0
    for size in range(5, 9):
        for scores in itertools.product((14, 20, 26), repeat=size):
            literal = collections.Counter(sum(scores[i] for i in subset)
                                          for subset in itertools.combinations(range(size), 5)
                                          if sum(scores[i] for i in subset) <= 100)
            expected = sorted([list(x) for x in literal.items()])
            need(grouped(scores) == individual(scores) == expected, "complete actual five-factor toy oracle")
            coefficients += 1
    for matrix in range(4096):
        planes = [0]*4
        for row in range(3):
            increment(planes, sum(1 << col for col in range(4) if (matrix >> (4*row+col)) & 1))
        for col in range(4):
            observed = sum((1 << j) for j in range(4) if (planes[j] >> col) & 1)
            expected = sum((matrix >> (4*row+col)) & 1 for row in range(3))
            need(observed == expected, "complete three-row four-column bit-add oracle")
    return {"five_row_coefficient_fixtures": coefficients, "bit_add_fixtures": 4096,
            "status": "COMPLETE_EXHAUSTIVE_SMALL_ORACLES"}


def main():
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--toy", action="store_true")
    ap.add_argument("--output", type=Path)
    args = ap.parse_args()
    h = Path(__file__).resolve().parent
    if args.toy:
        need(args.output is not None and not args.output.exists(), "preserve complete toy output")
        result = toy_checks(h)
        args.output.write_text(json.dumps(result, sort_keys=True)+"\n")
        print(json.dumps(result))
        return
    work = h/"character617-pass30-controls"
    work.mkdir(exist_ok=True)
    need(not (work/"run.json").exists() and not (work/"failed.json").exists(), "preserve complete run or failure")
    env = os.environ.copy()
    for name in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS",
                 "VECLIB_MAXIMUM_THREADS", "BLIS_NUM_THREADS"):
        env[name] = "1"
    row_source = json.loads((h/"character617-size24-row-budget-checks/producer/range-0000.json").read_text())
    complete_source = json.loads((h/"character617-size24-row-completion-checks/producer/batch-000.json").read_text())
    short = next(r for r in complete_source["records"] if r["row_choices"] == 4)
    complete_source["records"] = [short]
    complete_source["selected_core_indices"] = [short["core_index"]]
    complete_source["row_choices"] = short["row_choices"]
    complete_source["remaining_row_choices"] = short["remaining_row_choices"]
    complete_source["records_sha256"] = hashlib.sha256(canon(complete_source["records"])).hexdigest()
    selection = work/"selection.json"
    selection.write_text(json.dumps(complete_source["selected_core_indices"])+"\n")
    children = []

    def run(name, mode, command, expect, reason=None):
        need(not any(Path("/scratch/research-team-sol61-six-20260929/state", k).exists()
                     for k in ("PAUSED", "PAUSED.json", "HANDOVER.json")), "Operations barrier")
        begin = time.monotonic()
        command = [str(h/"solver-env/bin/python")]+(["-O"] if mode == "optimized" else [])+command
        record = {"name": name, "mode": mode, "guard_seconds": 20, "threads": 1,
                  "command": command, "expected": expect, "expected_reason": reason}
        try:
            p = subprocess.run(command, env=env, capture_output=True, text=True, timeout=20)
            good = ((p.returncode == 0) if expect == "PASS" else (p.returncode != 0 and reason in p.stderr))
            record.update(exit_code=p.returncode, stdout=p.stdout, stderr=p.stderr,
                          status="EXPECTED_CONTROL_COMPLETED" if good else "UNEXPECTED_CONTROL_RESULT")
        except subprocess.TimeoutExpired:
            record["status"] = "TIMEOUT_INCOMPLETE_NO_EXCLUSION"
        record.update(seconds=time.monotonic()-begin,
                      peak_child_rss_kib=resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss)
        children.append(record)
        (work/"execution.json").write_text(json.dumps(children, indent=2)+"\n")
        if record["status"] != "EXPECTED_CONTROL_COMPLETED":
            (work/"failed.json").write_text(json.dumps(record, indent=2)+"\n")
            raise SystemExit("Preserve first failed control; no identical retry")

    damages = []
    for kind, source, mutations in (
        ("row", row_source, [
            ("wrong_score", lambda d: d["records"][0]["scores"][0].__setitem__(1, 0), "every actual row score"),
            ("omit_physical_row", lambda d: d["records"][0]["scores"].pop(), "every actual row score"),
            ("duplicate_physical_row", lambda d: d["records"][0]["scores"].__setitem__(1, d["records"][0]["scores"][0]), "every actual row score"),
            ("wrong_coefficient", lambda d: next(r for r in d["records"] if r["row_choices"])["row_coefficients"][0].__setitem__(1, 0), "every actual row score"),
            ("omit_core", lambda d: d["records"].pop(), "entire declared core range"),
            ("wrong_entire_common", lambda d: d["records"][0]["C"].pop(), "every actual row score"),
            ("wrong_budget", lambda d: d.__setitem__("scaled_budget", 101), "actual relaxation premises"),
        ]),
        ("completion", complete_source, [
            ("wrong_exact_minimum", lambda d: d["records"][0]["answers"][0].__setitem__(5, 20), "exact whole relaxed column minimum"),
            ("omit_row_tuple", lambda d: d["records"][0]["answers"].pop(), "legality, uniqueness"),
            ("duplicate_row_tuple", lambda d: d["records"][0]["answers"].__setitem__(1, d["records"][0]["answers"][0]), "strict tuple ordering"),
            ("illegal_row_tuple", lambda d: d["records"][0]["answers"][0].__setitem__(0, 0), "five physical distinct added rows"),
            ("wrong_conditional_summary", lambda d: d["records"][0].__setitem__("conditional_minimum", 20), "whole actual row/minimum transcript"),
            ("wrong_entire_common", lambda d: d["records"][0]["C"].pop(), "whole actual row/minimum transcript"),
            ("wrong_budget", lambda d: d.__setitem__("missing_budget", 21), "actual conditional minimum premises"),
        ]),
    ):
        good = work/f"{kind}-positive.json"
        good.write_text(json.dumps(source, sort_keys=True)+"\n")
        for name, mutate, reason in mutations:
            d = copy.deepcopy(source)
            mutate(d)
            d["records_sha256"] = hashlib.sha256(canon(d["records"])).hexdigest()
            p = work/f"{kind}-{name}.json"
            p.write_text(json.dumps(d, sort_keys=True)+"\n")
            damages.append((kind, name, p, reason))
    for mode in ("normal", "optimized"):
        toy = work/f"{mode}-toy.json"
        run("toy", mode, [str(Path(__file__).resolve()), "--toy", "--output", str(toy)], "PASS")
        for kind in ("row", "completion"):
            inputs = [("positive", work/f"{kind}-positive.json", None)]+[(name, p, reason) for k, name, p, reason in damages if k == kind]
            for name, p, reason in inputs:
                output = work/f"{mode}-{kind}-{name}-checked.json"
                if kind == "row":
                    cmd = [str(h/"check-character617-size24-row-budget.py"), "--domain", str(h/"character617-size24-capacity-checks/normal/checked.json")]
                else:
                    cmd = [str(h/"check-character617-size24-row-completion.py"), "--domain", str(h/"character617-size24-row-budget-checks/checked.json"),
                           "--selection", str(selection)]
                cmd += ["--input", str(p), "--output", str(output)]
                run(kind+"-"+name, mode, cmd, "PASS" if reason is None else "REJECT", reason)
    for name in ("toy", "row-positive-checked", "completion-positive-checked"):
        need((work/f"normal-{name}.json").read_bytes() == (work/f"optimized-{name}.json").read_bytes(), "whole positive-mode equality")
    result = {"agent": "six-vdw-3", "role": "researcher", "children": len(children),
              "semantic_damages_per_mode": len(damages), "whole_positive_pairs": 3,
              "guard_seconds": 20, "threads": 1, "seconds": sum(r["seconds"] for r in children),
              "maximum_child_seconds": max(r["seconds"] for r in children),
              "peak_child_rss_kib": max(r["peak_child_rss_kib"] for r in children),
              "status": "COMPLETE_ACTUAL_SEMANTIC_AND_EXHAUSTIVE_SMALL_CONTROLS"}
    (work/"run.json").write_text(json.dumps(result, indent=2)+"\n")
    print(json.dumps(result))


if __name__ == "__main__":
    main()
