"""Serial source-only reproduction, independent checking, and seed census."""
import argparse
import json
import os
from pathlib import Path
import resource
import subprocess
import sys
import time


def require(ok, message):
    if not ok:
        raise ValueError(message)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--work", type=Path, required=True)
    args = parser.parse_args()
    work = args.work.resolve()
    work.mkdir(parents=True, exist_ok=False)
    source = Path(__file__).resolve().parent
    env = dict(os.environ)
    env.update({k: "1" for k in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS")})
    env.update(ASAN_OPTIONS="detect_leaks=1:halt_on_error=1", UBSAN_OPTIONS="halt_on_error=1:print_stacktrace=1")
    started = time.monotonic()

    def run(command, label):
        with (work / (label + ".log")).open("w") as stream:
            result = subprocess.run(command, stdout=stream, stderr=subprocess.STDOUT,
                                    timeout=55, env=env, check=False)
        require(result.returncode == 0, f"nonzero/operational failure: {label}; no exclusion inferred")

    common = ["g++", "-std=c++17", "-Wall", "-Wextra", "-Wconversion", "-pedantic"]
    native, sanitized = work / "native", work / "sanitized"
    run(common + ["-O2", str(source / "enumerate.cpp"), "-o", str(native)], "compile-native")
    run(common + ["-O1", "-g", "-fsanitize=address,undefined", "-fno-omit-frame-pointer",
                  str(source / "enumerate.cpp"), "-o", str(sanitized)], "compile-sanitized")
    run([str(native)], "native")
    run([str(sanitized)], "sanitized")
    require((work / "native.log").read_bytes() == (work / "sanitized.log").read_bytes(), "sanitizer output mismatch")
    checked, optimized = work / "checked.json", work / "optimized.json"
    run([sys.executable, str(source / "check.py"), str(work / "native.log"), "--output", str(checked)], "check")
    run([sys.executable, "-O", str(source / "check.py"), str(work / "native.log"), "--output", str(optimized)], "optimized")
    require(checked.read_bytes() == optimized.read_bytes(), "optimized checker disagreement")
    run([sys.executable, str(source / "probe_seeds.py"), str(checked), "--word", str(work / "seed.bits")], "seeds")
    result = {"check": json.loads(checked.read_text()), "seeds": json.loads((work / "seeds.log").read_text())}
    require(result == json.loads((source / "expected.json").read_text()), "pinned expected result mismatch")
    summary = {"status": "SOURCE_ONLY_CLASSIFICATION_PRODUCT_EXCLUSION_AND_SEEDS_PASSED",
               "u_assignments": 4194304, "v9_assignments": 256, "v27_assignments": 5038848,
               "result_sha256": result["check"]["result_sha256"],
               "elapsed_seconds": round(time.monotonic() - started, 6),
               "child_peak_rss_kib": resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss}
    (work / "summary.json").write_text(json.dumps(summary, sort_keys=True, indent=2) + "\n")
    print(json.dumps(summary, sort_keys=True), flush=True)


if __name__ == "__main__":
    main()
