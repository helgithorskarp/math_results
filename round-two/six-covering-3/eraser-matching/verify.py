"""Sequential source-only replay, with bounded children and frozen evidence."""

import argparse
import hashlib
import json
import os
from pathlib import Path
import resource
import subprocess
import sys
import tempfile
import time


def require(condition, message):
    if not condition:
        raise ValueError(message)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--scratch", type=Path)
    args = parser.parse_args()
    src = Path(__file__).resolve().parent
    expected = json.loads((src / "expected.json").read_text())
    env = os.environ.copy()
    env.update({"PYTHONDONTWRITEBYTECODE": "1", "OPENBLAS_NUM_THREADS": "1",
                "OMP_NUM_THREADS": "1", "MKL_NUM_THREADS": "1", "NUMEXPR_NUM_THREADS": "1"})
    start = time.monotonic()
    children = []

    def run(name, command, guard=20):
        began = time.monotonic()
        result = subprocess.run(command, env=env, capture_output=True, text=True, timeout=guard)
        require(result.returncode == 0, name + " failed: " + result.stderr[:2000])
        require(not result.stderr, name + " unexpected stderr: " + result.stderr[:2000])
        children.append({"name": name, "seconds": round(time.monotonic() - began, 3)})
        return result.stdout

    py = sys.executable
    produced = run("producer", [py, "-B", str(src / "produce.py")])
    frozen = (src / "certificate.json").read_text()
    require(produced == frozen, "producer bytes differ from frozen certificate")
    optimized = run("producer-optimized", [py, "-O", "-B", str(src / "produce.py")])
    require(optimized == frozen, "optimized producer bytes differ")
    for flags, suffix in [(["-B"], "normal"), (["-O", "-B"], "optimized")]:
        checked = json.loads(run("literal-python-" + suffix, [py] + flags + [str(src / "check.py")]))
        require(checked == expected["python"], "Python expected mismatch: " + suffix)
        controls = json.loads(run("controls-" + suffix, [py] + flags + [str(src / "controls.py")]))
        require(controls == expected["controls"], "control expected mismatch: " + suffix)
    if args.scratch is not None:
        args.scratch.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="eraser-build-", dir=args.scratch) as temp:
        for label, optimization in [
                ("release", ["-O2"]),
                ("sanitizers", ["-O1", "-g", "-fsanitize=address,undefined", "-fno-omit-frame-pointer"])]:
            target = Path(temp) / ("literal-" + label)
            compile_args = ["g++", "-std=c++20"] + optimization + [
                "-Wall", "-Wextra", "-Wpedantic", "-Wconversion", "-Wshadow", "-Werror",
                str(src / "literal_gap.cpp"), "-o", str(target)]
            run("compile-" + label, compile_args, 30)
            literal = json.loads(run("literal-cpp-" + label, [str(target)]))
            require(literal == expected["literal"], "literal expected mismatch: " + label)
    print(json.dumps({"complete": True, "agent": "six-covering-3", "role": "researcher",
                      "certificate_sha256": hashlib.sha256(frozen.encode()).hexdigest(),
                      "evidence": expected, "children": children,
                      "seconds": round(time.monotonic() - start, 3),
                      "maximum_child_rss_kib": resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,
                      "python": sys.version.split()[0]}, sort_keys=True))


if __name__ == "__main__":
    main()
