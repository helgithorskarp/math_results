#!/usr/bin/env python3
"""Serial same-author source/record validation; not independent review."""
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
    cmd = [sys.executable, "-B"] + (["-O"] if optimized else []) + [str(where / "verify.py")]
    if expected is not None:
        cmd += ["--expected", str(expected)]
    if export is not None:
        cmd += ["--export", str(export)]
    start = time.perf_counter()
    r = subprocess.run(cmd, env=ENV, text=True, capture_output=True, timeout=45)
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
    with tempfile.TemporaryDirectory(prefix="sendov-signed-author-") as name:
        temp = Path(name)
        records = []
        for optimized in [False, True]:
            export = temp / ("whole-O.json" if optimized else "whole-normal.json")
            r, elapsed = run(ROOT, optimized, export=export)
            require(r.returncode == 0, "whole positive checker failed: " + r.stderr)
            records.append(export.read_bytes())
            positives.append({"optimized": optimized, "seconds": elapsed, "whole_output": json.loads(r.stdout)})
        require(records[0] == records[1], "entire normal/optimized records differ")
        modifications = []
        def damage(label, callback):
            v = copy.deepcopy(base)
            callback(v)
            modifications.append((label, json.dumps(v)))
        damage("missing_face", lambda v: v["whole_faces"].pop())
        damage("changed_tensor_entry", lambda v: v["whole_faces"][0]["bernstein"][0].__setitem__(0, "0"))
        damage("truncated_full_tensor", lambda v: v["whole_faces"][0]["bernstein"].pop())
        damage("changed_whole_power", lambda v: v["whole_faces"][0]["power_a_u"][0].__setitem__(2, "0"))
        damage("changed_phase_coefficient", lambda v: v["phase_coefficients"].__setitem__("deficit", "0"))
        damage("missing_final_taylor_order", lambda v: v["complete_complex_taylor_coefficients"][0].pop())
        damage("wrong_a_endpoint", lambda v: v["a_interval"].__setitem__(0, "1"))
        damage("missing_hessian_row", lambda v: v["whole_literal_controls"][2]["ordered_hessian"].pop())
        damage("changed_complete_gradient", lambda v: v["whole_literal_controls"][2]["gradient"][1].__setitem__(0, "0"))
        damage("wrong_strict_margin", lambda v: v["strict_margins"].__setitem__("complex_hessian", "0"))
        damage("missing_rejected_budget", lambda v: v["rejected_mathematical_budgets"].pop("global_nonpositive_gradient"))
        damage("integer_boolean", lambda v: v["whole_faces"][0].__setitem__("order", True))
        damage("integer_float", lambda v: v["whole_faces"][0].__setitem__("order", 1.0))
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
