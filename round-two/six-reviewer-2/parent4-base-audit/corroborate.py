"""Optional late native corroboration. Never imported by the independent proof."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import struct
import subprocess
import sys
from grid import need

ROOT = Path(__file__).resolve().parent


def run(target, own_scratch, scratch):
    target = Path(target).resolve()
    own_scratch = Path(own_scratch).resolve()
    scratch = Path(scratch).resolve()
    need(scratch != ROOT and ROOT not in scratch.parents, "outputs outside public source")
    scratch.mkdir(parents=True, exist_ok=True)
    inputs = json.loads((ROOT / "AUTHOR-INPUTS.json").read_text())
    for f, v in inputs["files"].items():
        need(hashlib.sha256((target / f).read_bytes()).hexdigest() == v["sha256"],
             "unmodified native input closure " + f)
    expected = json.loads((ROOT / "EXPECTED.json").read_text())
    native = json.loads((target / "certificate.json").read_text())
    env = dict(os.environ)
    for name in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS",
                 "NUMEXPR_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "BLIS_NUM_THREADS"):
        env[name] = "1"
    compared = []
    for optimized in (False, True):
        for stage in range(1, 5):
            stem = str(stage) + ("-O" if optimized else "-normal")
            out, rows = scratch / (stem + ".json"), scratch / (stem + ".bin")
            cmd = [sys.executable, "-B"] + (["-O"] if optimized else [])
            cmd += [str(ROOT / "capture.py"), str(target / "generate.py"),
                    str(target / "certificate.json"), str(stage), str(out), str(rows)]
            p = subprocess.run(cmd, cwd=ROOT, env=env, capture_output=True,
                               text=True, timeout=20)
            need(p.returncode == 0 and not p.stderr, "native capture incomplete " + p.stderr)
            need(json.loads(out.read_text()) == native["stages"][stage - 1],
                 "entire native generated certificate")
            own = (own_scratch / ("canonical" + str(stage) + ".bin")).read_bytes()
            raw = rows.read_bytes()
            e = expected["stages"][stage - 1]["canonical_original"]
            need(hashlib.sha256(own).hexdigest() == e["row_sha256"],
                 "bind whole pre-native independent row stream")
            left = list(struct.iter_unpack("<38H", own))
            right = list(struct.iter_unpack("<38H", raw))
            need(len(left) == len(right) == e["count"], "every native/own row present")
            for i, (a, b) in enumerate(zip(left, right)):
                need(a == b, "actual field-by-field native row mismatch " + str((stage, i)))
            need(raw == own, "whole row stream equality")
            compared.append({"stage": stage, "optimized": optimized,
                "rows": len(left), "all_38_field_values": len(left) * 38,
                "entire_row_sha256": hashlib.sha256(raw).hexdigest(),
                "entire_native_stage_certificate_matches": True})
    return {"agent": "six-reviewer-2", "role": "independent mathematical reviewer",
            "late_native_code_only": True, "independent_proof_imports_native": False,
            "instrumentation": "one binary row write appended after unchanged native digest update; all native arithmetic and output statements retained",
            "native_guard_seconds": 20, "serial_threads": 1,
            "all_12_native_input_files_unchanged": True, "comparisons": compared}


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--target", required=True)
    p.add_argument("--own-scratch", required=True)
    p.add_argument("--scratch", required=True)
    p.add_argument("--out", required=True)
    a = p.parse_args()
    raw = (json.dumps(run(a.target, a.own_scratch, a.scratch), sort_keys=True,
                      separators=(",", ":")) + "\n").encode()
    Path(a.out).write_bytes(raw)
    print(json.dumps({"all_eight_whole_comparisons_pass": True,
                      "entire_comparison_sha256": hashlib.sha256(raw).hexdigest()}))
