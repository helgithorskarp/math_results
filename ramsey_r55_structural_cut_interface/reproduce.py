#!/usr/bin/env python3
"""Replay compact certificates in normal and assertion-disabled Python."""
import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("out", type=Path)
    args = parser.parse_args()
    here = Path(__file__).resolve().parent
    manifest = json.loads((here / "MANIFEST.json").read_text())
    files = {p.name for p in here.iterdir() if p.is_file() and p.name != "MANIFEST.json"}
    if files != set(manifest):
        raise ValueError("package file set differs from manifest")
    for name, info in manifest.items():
        data = (here / name).read_bytes()
        if len(data) != info["bytes"] or hashlib.sha256(data).hexdigest() != info["sha256"]:
            raise ValueError(f"hash mismatch: {name}")
    args.out.mkdir(parents=True, exist_ok=True)
    expected = json.loads((here / "EXPECTED.json").read_text())
    controls = []
    for mode in ([], ["-O"]):
        tag = "optimized" if mode else "normal"
        dest = args.out / tag
        dest.mkdir(exist_ok=True)
        base = [sys.executable, *mode, "-B"]
        def run(script, *parameters):
            r = subprocess.run([*base, str(here / script), *map(str, parameters)],
                               capture_output=True, text=True, check=True)
            (dest / (script + ".stdout")).write_text(r.stdout)
            return r.stdout
        run("build.py", dest)
        for name in ("TEMPLATE.json",):
            if json.loads((dest / name).read_text()) != json.loads((here / name).read_text()):
                raise ValueError("rebuilt template differs")
        solver = json.loads((here / "SOLVER.json").read_text())
        if hashlib.sha256((dest / "input.cnf").read_bytes()).hexdigest() != solver["input_sha256"]:
            raise ValueError("rebuilt DIMACS differs")
        cut = dest / "cut.json"
        run("interface.py", "--vertices", ",".join(map(str, range(19))), "--color", 1, "--out", cut)
        receipt = dest / "verified.json"
        run("verify.py", here, cut, "--out", receipt)
        if json.loads(receipt.read_text()) != expected:
            raise ValueError("verification receipt differs")
        controls.append(json.loads(run("controls.py")))
    if controls[0] != controls[1] or controls[0]["status"] != "CONTROLS_PASS":
        raise ValueError("control outputs differ")
    print(json.dumps({"status": "REPRODUCED_GLOBAL_STRUCTURAL_CUT_INTERFACE",
                      "normal_and_optimized": True, "controls": controls[0],
                      "count_gate_gt_2_to_750": True, "solver_calls": 0}, sort_keys=True))


if __name__ == "__main__":
    main()
