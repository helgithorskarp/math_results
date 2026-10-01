"""Serial release/sanitizer/resume checks for the optional heuristic."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import resource
import subprocess
import time
import audit621 as check


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--work", type=Path, required=True)
    args = p.parse_args()
    work = args.work.resolve()
    work.mkdir(parents=True, exist_ok=False)
    source = Path(__file__).resolve().parent / "search621.cpp"
    env = dict(os.environ)
    env.update({name: "1" for name in
                ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS")})
    env.update(ASAN_OPTIONS="detect_leaks=1:halt_on_error=1",
               UBSAN_OPTIONS="halt_on_error=1:print_stacktrace=1")
    started = time.monotonic()

    def run(command, label, success=True):
        with (work / (label + ".log")).open("w") as stream:
            proc = subprocess.run(command, stdout=stream, stderr=subprocess.STDOUT,
                                  env=env, timeout=30, check=False)
        check.require((proc.returncode == 0) == success, f"unexpected status: {label}")

    release, sanitized = work / "release", work / "sanitized"
    common = ["g++", "-std=c++17", "-Wall", "-Wextra", "-Wconversion", "-pedantic"]
    run(common + ["-O2", str(source), "-o", str(release)], "compile-release")
    run(common + ["-O1", "-g", "-fsanitize=address,undefined", "-fno-omit-frame-pointer",
                  str(source), "-o", str(sanitized)], "compile-sanitized")
    whole, split, san = [work / name for name in ("whole", "split", "san")]
    run([str(release), str(whole), "250", "20"], "whole")
    run([str(release), str(split), "100", "20"], "split-first")
    run([str(release), str(split), "150", "20"], "split-second")
    run([str(sanitized), str(san), "250", "20"], "sanitized")
    check.require(whole.read_bytes() == split.read_bytes() == san.read_bytes(),
                  "resume or sanitizer checkpoint mismatch")
    words = [Path(str(path) + ".best.bits").read_bytes() for path in (whole, split, san)]
    check.require(words[0] == words[1] == words[2], "best-word mismatch")
    cost = int(whole.read_text().split()[2])
    pairs = check.cyclic_count(list(map(int, words[0].decode().strip())))
    check.require(pairs == 2 * cost, "direct cyclic cost mismatch")
    rejected = 0
    for i, invalid in enumerate(("bad\n", "VDW621SEARCH2 0 0\n",
                                 whole.read_text() + " extra\n")):
        target = work / ("bad-" + str(i))
        target.write_text(invalid)
        run([str(release), str(target), "1", "10"], "reject-" + str(i), success=False)
        rejected += 1
    result = {"status": "HEURISTIC_SANITIZER_RESUME_AND_COST_CHECKS_PASSED",
              "moves": 250, "best_half_count": cost, "cyclic_pairs": pairs,
              "word_sha256": hashlib.sha256(words[0]).hexdigest(),
              "checkpoint_sha256": hashlib.sha256(whole.read_bytes()).hexdigest(),
              "rejected_checkpoints": rejected,
              "elapsed_seconds": round(time.monotonic() - started, 6),
              "child_max_rss_kib": resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss}
    (work / "result.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, sort_keys=True), flush=True)


if __name__ == "__main__":
    main()
