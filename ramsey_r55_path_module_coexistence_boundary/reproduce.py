"""Regenerate and check the complete coexistence control in new scratch space."""

import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import time


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("work", type=Path)
    args = parser.parse_args()
    work = args.work.resolve()
    work.mkdir(parents=True, exist_ok=False)
    source = Path(__file__).resolve().parent
    if source == work or source in work.parents:
        raise ValueError("Use scratch space outside the source directory")
    origin = json.loads((source / "CONTROL_ORIGIN.json").read_text())
    graph = source / "control43.edges"
    if hashlib.sha256(graph.read_bytes()).hexdigest() != origin["sha256"]:
        raise ValueError("The unchanged input graph has the wrong hash")
    started = time.monotonic()
    compiler = subprocess.check_output(["g++", "--version"], text=True).splitlines()[0]
    subprocess.run(["g++", "-std=c++17", "-O2", "-Wall", "-Wextra",
                    "-Wconversion", "-Wshadow", "-pedantic", str(source / "audit.cpp"),
                    "-o", str(work / "audit")], check=True)
    native = subprocess.run([str(work / "audit"), str(graph), str(work / "cover.bin")],
                            capture_output=True, text=True, check=True)
    (work / "native.json").write_text(native.stdout)
    subprocess.run([sys.executable, "-B", str(source / "check.py"), "--graph", str(graph),
                    "--cover", str(work / "cover.bin"), "--native", str(work / "native.json"),
                    "--output", str(work / "checked.json")], check=True)
    if (work / "checked.json").read_bytes() != (source / "EXPECTED.json").read_bytes():
        raise ValueError("The full checked output differs from EXPECTED.json")
    result = {"status": "REPRODUCED_PATH_MODULE_COEXISTENCE_BOUNDARY",
              "seconds": time.monotonic() - started, "compiler": compiler,
              "python": sys.version, "first_gate_met": False,
              "new_good43_decisions": 0,
              "cover_sha256": hashlib.sha256((work / "cover.bin").read_bytes()).hexdigest(),
              "expected_sha256": hashlib.sha256((source / "EXPECTED.json").read_bytes()).hexdigest()}
    (work / "REPLAY.json").write_text(json.dumps(result, indent=2) + "\n")
    print(result["status"])


if __name__ == "__main__":
    main()
