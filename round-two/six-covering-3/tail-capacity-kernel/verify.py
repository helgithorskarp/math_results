"""Six serial bounded standard-library replay children; no solver required."""
import argparse
from hashlib import sha256
import json
import os
from pathlib import Path
import resource
import subprocess
import sys
import time


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--scratch", type=Path, required=True)
    args = ap.parse_args()
    args.scratch.mkdir(parents=True, exist_ok=True)
    here = Path(__file__).resolve().parent
    manifest = json.loads((here / "manifest.json").read_text())
    for name, expected in manifest["files"].items():
        data = (here / name).read_bytes()
        if len(data) != expected["bytes"] or sha256(data).hexdigest() != expected["sha256"]:
            raise ValueError("source integrity failed: "+name)
    env = dict(os.environ, OPENBLAS_NUM_THREADS="1", OMP_NUM_THREADS="1",
               MKL_NUM_THREADS="1", NUMEXPR_NUM_THREADS="1", PYTHONDONTWRITEBYTECODE="1")
    start = time.monotonic(); rows = []; decoded = {}
    for script in ("check.py", "audit.py", "controls.py"):
        for optimized in (False, True):
            flags = ["-B"] + (["-O"] if optimized else [])
            p = subprocess.run([sys.executable, *flags, str(here / script)],
                               env=env, capture_output=True, text=True, timeout=20)
            name = script[:-3]+("-O" if optimized else "-normal")
            (args.scratch / (name+".stdout.json")).write_text(p.stdout)
            (args.scratch / (name+".stderr.txt")).write_text(p.stderr)
            if p.returncode:
                raise RuntimeError(name+" failed: "+p.stderr)
            decoded[name] = json.loads(p.stdout)
            rows.append({"child": name, "stdout_sha256": sha256(p.stdout.encode()).hexdigest()})
        if decoded[script[:-3]+"-normal"] != decoded[script[:-3]+"-O"]:
            raise ValueError("normal/optimized mathematical records differ")
    if decoded["check-normal"] != decoded["audit-normal"]:
        raise ValueError("cofactor and physical original-period evidence differ")
    result = {"agent": "six-covering-3", "role": "researcher", "status": "PASSED",
              "serial_children": rows, "seconds": round(time.monotonic()-start, 6),
              "max_child_RSS_KiB": resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,
              "per_child_guard_seconds": 20, "numerical_solver_dependency": False,
              "evidence": decoded["check-normal"], "controls": decoded["controls-normal"]}
    (args.scratch / "verification.json").write_text(json.dumps(result, indent=2)+"\n")
    print(json.dumps({k: v for k, v in result.items() if k not in ("serial_children", "evidence")}, sort_keys=True))


if __name__ == "__main__":
    main()
