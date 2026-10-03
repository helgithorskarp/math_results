"""Six serial source-only children, native threads1, fixed45s each."""
import argparse
import datetime
import hashlib
import json
import os
from pathlib import Path
import platform
import resource
import shutil
import subprocess
import sys
import tempfile
import time

BASE = Path(__file__).resolve().parent
NATIVE = (
    "OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS",
    "NUMEXPR_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "BLIS_NUM_THREADS",
)
ENV = os.environ.copy()
ENV.update({name: "1" for name in NATIVE})


def run(directory, optimized=False, batch=False):
    command = [sys.executable, "-I", "-B"] + (["-O"] if optimized else [])
    command += [str(directory / "verify.py"), "--emit-record"]
    if batch:
        command += ["--validation-batch"]
    result = subprocess.run(command, cwd=directory, env=ENV, timeout=45,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode:
        raise RuntimeError("source-only child rejected: " + result.stderr.decode(errors="replace"))
    return result.stdout


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    started = time.monotonic()
    normal = run(BASE)
    optimized = run(BASE, optimized=True)
    batch_normal = run(BASE, batch=True)
    batch_optimized = run(BASE, optimized=True, batch=True)
    with tempfile.TemporaryDirectory(prefix="signed-phase-source-only-") as directory:
        isolated = Path(directory)
        manifest = json.loads((BASE / "MANIFEST.json").read_text())
        for name in tuple(manifest["files"]) + ("MANIFEST.json",):
            shutil.copyfile(BASE / name, isolated / name)
        cold_normal = run(isolated)
        cold_optimized = run(isolated, optimized=True)
    if normal != optimized or normal != cold_normal or normal != cold_optimized:
        raise RuntimeError("ENTIRE mathematical records differ")
    if batch_normal != batch_optimized:
        raise RuntimeError("ENTIRE validation records differ")
    payload = json.loads(normal)
    batch = json.loads(batch_normal)
    if batch["record"] != payload:
        raise RuntimeError("batch mathematical record differs")
    validations = batch["validation"]
    record = {
        "agent": "six-sendov-1", "role": "researcher",
        "checked_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "python": platform.python_version(), "serial_children": 6,
        "native_threads": {name: "1" for name in NATIVE}, "per_child_timeout_seconds": 45,
        "whole_record_sha256": hashlib.sha256(normal.rstrip(b"\n")).hexdigest(),
        "normal_optimized_isolated_whole_match": True,
        "scalar_margins": payload["scalars"]["margin_count"],
        "strict_margins": payload["scalars"]["strict_margin_count"],
        "closed_margin_equalities": payload["scalars"]["closed_margin_count"],
        "shifted_coefficients": payload["coefficients"]["shifted_coefficient_count"],
        "mixed_coefficients": payload["coefficients"]["mixed_coefficient_count"],
        "whole_even_identity_terms": payload["algebra"]["common_map_terms"],
        "even_order_census": payload["algebra"]["terms_by_even_order"],
        "literal_controls": len(payload["algebra"]["literal_controls"]),
        "mathematical_damage_cases": len(validations["mathematical_rejections"]),
        "external_malformed_cases": len(validations["external_rejections"]),
        "source_pin_rejected": validations["source_pin_rejected"],
        "validation": validations,
        "elapsed_seconds": round(time.monotonic() - started, 6),
        "peak_child_RSS_KiB": resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,
        "scope": "Complete ordinary proof corroborated by exact finite evidence; unformalized and independently unreviewed. Standalone local signed-phase inequality and bounded actual corollaries; no global first-power endpoint.",
    }
    raw = json.dumps(record, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(raw)
    print(raw, end="")


if __name__ == "__main__":
    main()
