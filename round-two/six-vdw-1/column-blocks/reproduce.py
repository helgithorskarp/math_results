"""Source-only validation of the exact ordinary-column repair kernel.

All generated executables, checkpoints and expanded tables stay in scratch.
Children run sequentially with one solver/BLAS/OpenMP thread. No solver
verdict or search timeout is used as an exclusion.
"""
import argparse
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import resource
import subprocess
import sys
import time

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def require(ok, message):
    if not ok:
        raise ValueError(message)


def reproduce(scratch):
    require(not scratch.exists() or not any(scratch.iterdir()), "scratch must be absent or empty")
    scratch.mkdir(parents=True, exist_ok=True)
    env = os.environ.copy()
    for name in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS"):
        env[name] = "1"
    begin = time.monotonic()

    def run(args, tag, timeout=55):
        result = subprocess.run(list(map(str, args)), text=True, capture_output=True,
                                env=env, timeout=timeout)
        (scratch / (tag + ".log")).write_text(result.stdout + result.stderr)
        require(result.returncode == 0, f"{tag} failed: {result.stderr[-2000:]}")
        return result.stdout

    flags = ["g++", "-std=c++17", "-Wall", "-Wextra", "-Wconversion", "-pedantic"]
    for name, source in (("kernel", HERE / "validate_kernel.cpp"), ("repair", ROOT / "repair3704.cpp")):
        run(flags + ["-O2", source, "-o", scratch / name], "compile-" + name)
        run(flags + ["-O1", "-g", "-fsanitize=address,undefined", "-fno-omit-frame-pointer",
                     source, "-o", scratch / (name + "-san")], "compile-san-" + name)
    fixtures = run([scratch / "kernel"], "kernel")
    require(run([scratch / "kernel-san"], "kernel-san") == fixtures, "sanitized kernel differs")
    fixture_path = scratch / "kernel-fixtures.json"
    fixture_path.write_text(fixtures)
    checks = []
    for optimized in (False, True):
        prefix = [sys.executable] + (["-O"] if optimized else [])
        checks.append(json.loads(run(prefix + [HERE / "validate_kernel.py", fixture_path],
                                     "kernel-check-" + str(optimized))))
    require(checks[0] == checks[1], "normal/optimized kernel checks differ")
    geometry = json.loads(run([sys.executable, HERE / "geometry_controls.py"], "geometry"))
    require(json.loads(run([sys.executable, "-O", HERE / "geometry_controls.py"], "geometry-O")) == geometry,
            "normal/optimized geometry controls differ")
    spec = importlib.util.spec_from_file_location("independent_kernel_check", HERE / "validate_kernel.py")
    checker = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(checker)
    corruptions = 0
    for kind in ("score", "feasible", "count"):
        data = json.loads(fixtures)
        if kind == "score":
            next(x for x in data if x["feasible"])["minimum"][1] += 1
        elif kind == "feasible":
            next(x for x in data if not x["feasible"])["feasible"] = True
        else:
            data.pop()
        corrupt = scratch / ("corrupt-" + kind + ".json")
        corrupt.write_text(json.dumps(data))
        try:
            checker.check(corrupt)
        except ValueError:
            corruptions += 1
        else:
            raise ValueError("corrupt kernel evidence accepted")
    seed = HERE / "fixture-invalid747.bits"
    seed_hash = hashlib.sha256(seed.read_bytes()).hexdigest()
    require(seed_hash == "3e9e467b6a58dbd1e2f0c48d0bedcbaf2a1fd1c40b316e3091787caf5a32d552",
            "wrong invalid fixture bytes")
    final_fixture_checks = []
    for optimized in (False, True):
        prefix = [sys.executable] + (["-O"] if optimized else [])
        final_fixture_checks.append(json.loads(run(prefix + [ROOT / "audit_repair.py", "--word",
                                         HERE / "fixture-invalid526.bits"], "fixture526-" + str(optimized))))
    require(final_fixture_checks[0] == final_fixture_checks[1] and
            final_fixture_checks[0]["word"]["monochromatic_windows"] == 526 and
            final_fixture_checks[0]["word_sha256"] == "584629f61ab417648b7c00b94f6a8f71acfa70ec65a3af2549f17e41fe455fc2",
            "wrong invalid526 fixture")

    def search(path, steps, tag, start=False, sanitized=False, seconds=45):
        args = [scratch / ("repair-san" if sanitized else "repair"), path, steps, seconds, 3704]
        if start:
            args.append(seed)
        return run(args, tag)

    suffixes = ("", ".best.bits", ".gains", ".pairs", ".block.json")

    def same(first, second, extra=()):
        for suffix in suffixes + extra:
            require(Path(str(first) + suffix).read_bytes() == Path(str(second) + suffix).read_bytes(),
                    "restart or sanitizer bytes differ: " + suffix)

    whole, split = scratch / "whole", scratch / "split"
    search(whole, 200, "whole", start=True)
    search(split, 100, "split-first", start=True)
    search(split, 100, "split-second")
    same(whole, split)
    ten, ten_san = scratch / "ten", scratch / "ten-san"
    search(ten, 10, "ten", start=True)
    search(ten_san, 10, "ten-san", start=True, sanitized=True)
    same(ten, ten_san)
    whole_sweep, split_sweep = scratch / "whole-sweep", scratch / "split-sweep"
    search(whole_sweep, "sweep", "sweep-whole", start=True)
    search(split_sweep, "sweep", "sweep-partial", start=True, seconds=0.001)
    partial = json.loads(Path(str(split_sweep) + ".sweep.json").read_text())
    require(not partial["complete"] and partial["after_cost"] == 747, "partial sweep changed frozen word")
    search(split_sweep, "sweep", "sweep-resume")
    same(whole_sweep, split_sweep, (".sweep-state", ".sweep.json"))
    curve = [747]
    curve.append(json.loads(Path(str(whole_sweep) + ".sweep.json").read_text())["after_cost"])
    for step in range(2, 6):
        search(whole_sweep, "sweep", "descent-" + str(step))
        report = json.loads(Path(str(whole_sweep) + ".sweep.json").read_text())
        require(report["complete"] and report["column_pairs_visited"] == 188805, "incomplete benchmark sweep")
        curve.append(report["after_cost"])
    require(curve == [747, 681, 634, 607, 592, 576], "unexpected frozen-fixture descent")
    audits = []
    for optimized in (False, True):
        args = [sys.executable] + (["-O"] if optimized else [])
        audits.append(json.loads(run(args + [ROOT / "audit_repair.py", whole_sweep],
                                      "interval-audit-" + str(optimized))))
    require(audits[0] == audits[1], "normal/optimized definition-level audits differ")
    require(audits[0]["best"]["monochromatic_windows"] == 576 and
            audits[0]["best_word_sha256"] == "6f786146aa13e8ce34dcbac61ce522557d35bd538da23d8f8516d6934ce8f04d",
            "wrong benchmark final word")
    result = {"kernel": checks[0], "geometry": geometry, "corruption_rejections": corruptions,
              "exact_restart_checks": ["200_vs_100_plus_100", "complete_vs_partial_resumed_sweep"],
              "sanitizers": ["kernel", "ten_move_search"], "curve": curve,
              "fixture_sha256": seed_hash, "final_audit": audits[0],
              "extra_invalid_fixture": final_fixture_checks[0]}
    canonical = json.dumps(result, sort_keys=True, separators=(",", ":")).encode()
    result["canonical_result_sha256"] = hashlib.sha256(canonical).hexdigest()
    expected = HERE / "expected.json"
    if expected.exists():
        require(result == json.loads(expected.read_text()), "expected result mismatch")
    (scratch / "result.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    metrics = {"elapsed_seconds": round(time.monotonic() - begin, 6),
               "peak_child_rss_kib": resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss}
    (scratch / "metrics.json").write_text(json.dumps(metrics, indent=2) + "\n")
    print(json.dumps({"status": "SOURCE_ONLY_REPRODUCTION_PASSED",
                      "canonical_result_sha256": result["canonical_result_sha256"], **metrics}, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--scratch", type=Path, required=True)
    args = parser.parse_args()
    reproduce(args.scratch.resolve())
