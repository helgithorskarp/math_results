#!/usr/bin/env python3
"""Serial same-author source/record validation; adapted from own9868, not independent review."""
import argparse
import copy
import hashlib
import json
import os
from pathlib import Path
import resource
import shutil
import subprocess
import sys
import tempfile
import time

ROOT = Path(__file__).resolve().parent
THREAD_NAMES = ["OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS",
                "BLIS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "NUMEXPR_NUM_THREADS"]
ENV = dict(os.environ, **{name: "1" for name in THREAD_NAMES})

def run(where, optimized=False, expected=None, export=None):
    cmd = [sys.executable, "-I", "-B"] + (["-O"] if optimized else []) + [str(where / "verify.py")]
    if expected is not None:
        cmd += ["--expected", str(expected)]
    if export is not None:
        cmd += ["--export", str(export)]
    start = time.perf_counter()
    r = subprocess.run(cmd, cwd=where, env=ENV, text=True, capture_output=True, timeout=45)
    return r, time.perf_counter() - start

def require(ok, message):
    if not ok:
        raise ValueError(message)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--seal", action="store_true", help="author-only regenerate frozen source census")
    args = parser.parse_args()
    if args.seal:
        names = [".gitignore", "verify.py", "validate.py", "PROOF.md", "README.md", "LITERATURE.md", "EXPECTED.json"]
        m = {"schema": 1, "sha256": {n: hashlib.sha256((ROOT / n).read_bytes()).hexdigest() for n in names}}
        (ROOT / "MANIFEST.json").write_text(json.dumps(m, indent=2) + "\n")
    base = json.loads((ROOT / "EXPECTED.json").read_text())
    positives = []
    rejects = []
    pins = []
    with tempfile.TemporaryDirectory(prefix="sendov-polar-phase-author-") as name:
        temp = Path(name)
        records = []
        for optimized in [False, True]:
            export = temp / ("whole-O.json" if optimized else "whole-normal.json")
            r, elapsed = run(ROOT, optimized, export=export)
            require(r.returncode == 0, "whole positive checker failed: " + r.stderr)
            records.append(export.read_bytes())
            positives.append({"optimized": optimized, "seconds": elapsed, "whole_output": json.loads(r.stdout)})
        require(records[0] == records[1], "entire normal/optimized records differ")
        isolated = temp / "isolated"
        isolated.mkdir()
        for filename in names if args.seal else json.loads((ROOT / "MANIFEST.json").read_text())["sha256"]:
            shutil.copy2(ROOT / filename, isolated / filename)
        shutil.copy2(ROOT / "MANIFEST.json", isolated / "MANIFEST.json")
        for optimized in [False, True]:
            export = temp / ("isolated-O.json" if optimized else "isolated-normal.json")
            r, elapsed = run(isolated, optimized, export=export)
            require(r.returncode == 0, "isolated verification failed: " + r.stderr)
            require(export.read_bytes() == records[0], "entire isolated record differs")
            positives.append({"optimized": optimized, "isolated": True, "seconds": elapsed,
                              "whole_output": json.loads(r.stdout)})
        modifications = []
        def damage(label, callback):
            v = copy.deepcopy(base)
            callback(v)
            modifications.append((label, json.dumps(v)))
        damage("missing_face", lambda v: v["whole_faces"].pop())
        damage("last_polar_coefficient", lambda v: v["polar_certificates"]["mean"]["whole_polynomial"].__setitem__(-1, "0"))
        damage("full_polar_route", lambda v: v["whole_polar"]["whole_tail"].pop())
        damage("last_face_coefficient", lambda v: v["whole_faces"][3]["whole_residual"].__setitem__(-1, "0"))
        damage("last_first_Newton_order", lambda v: v["first_whole_Newton_stream"].pop("7"))
        damage("last_second_Newton_coefficient", lambda v: v["second_whole_Newton_stream"]["7"].__setitem__(-1, "0"))
        damage("wrong_receiving_endpoint", lambda v: v.__setitem__("eta_endpoint", "1/16000"))
        damage("merge_two_distinct_radii", lambda v: v["complete_constants"].__setitem__("second_path_rho", "1/20"))
        damage("missing_cube_zero", lambda v: v["whole_cube_field"].pop(2))
        damage("wrong_principal_pair_sign", lambda v: v["whole_cube_field"][6]["full_pair_coefficient"].__setitem__(0, "-1/6"))
        damage("wrong_retained_square", lambda v: v["whole_mean_square"]["expanded_rhs"][0].__setitem__(2, "0"))
        damage("changed_complete_gradient", lambda v: v["whole_literal_controls"][2]["all_eight_gradients"][1].__setitem__(0, "0"))
        damage("missing_hessian_row", lambda v: v["whole_literal_controls"][2]["whole_ordered_hessian"].pop())
        damage("wrong_strict_margin", lambda v: v["all_full_window_margins"].__setitem__("actual_absolute_energy_h1over320", "0"))
        damage("missing_rejected_target33", lambda v: v["rejected_mathematical_budgets"].pop("first33eta_target"))
        damage("integer_boolean", lambda v: v["whole_faces"][0].__setitem__("m", True))
        damage("integer_float", lambda v: v["whole_faces"][0].__setitem__("m", 1.0))
        damage("extra_field", lambda v: v.__setitem__("extra", []))
        modifications += [("duplicate_key", '{"agent":"six-sendov-1","agent":"six-sendov-1"}'),
                          ("nonfinite", '{"agent":NaN}'), ("truncated", '{"agent":')]
        for optimized in [False, True]:
            for label, value in modifications:
                fixture = temp / (label + ".json")
                fixture.write_text(value)
                r, _ = run(ROOT, optimized, expected=fixture)
                require(r.returncode != 0, "damaged external record accepted " + label)
                rejects.append({"label": label, "optimized": optimized, "returncode": r.returncode})
            r, _ = run(ROOT, optimized, expected=temp / "absent.json")
            require(r.returncode != 0, "absent record accepted")
            rejects.append({"label": "absent", "optimized": optimized, "returncode": r.returncode})
        for filename in ["verify.py", "PROOF.md"]:
            for optimized in [False, True]:
                copied = temp / (filename.replace(".", "-") + ("-O" if optimized else "-normal"))
                shutil.copytree(ROOT, copied, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
                with (copied / filename).open("a") as f:
                    f.write("\n# deliberate frozen-source damage\n")
                r, _ = run(copied, optimized)
                require(r.returncode != 0, "copied source pin damage accepted")
                pins.append({"file": filename, "optimized": optimized, "returncode": r.returncode})
    receipt = {"agent": "six-sendov-1", "role": "researcher",
               "status": "ordinary unformalized author proof; independently unreviewed",
               "python": sys.version.split()[0], "third_party_packages": [],
               "native_threads": {n: 1 for n in THREAD_NAMES}, "serial_math_children": True,
               "child_guard_seconds": 45, "peak_child_rss_kib": resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,
               "positive": positives, "external_fixture_rejections": rejects,
               "copied_source_pin_rejections": pins,
               "manifest_sha256": hashlib.sha256((ROOT / "MANIFEST.json").read_bytes()).hexdigest()}
    (ROOT / "VALIDATION.json").write_text(json.dumps(receipt, indent=2) + "\n")
    print(json.dumps({"status": "PASS", "whole_record_sha256": positives[0]["whole_output"]["whole_record_sha256"],
                      "external_fixture_rejections": len(rejects), "copied_source_pin_rejections": len(pins),
                      "peak_child_rss_kib": receipt["peak_child_rss_kib"]}))

if __name__ == "__main__":
    main()
