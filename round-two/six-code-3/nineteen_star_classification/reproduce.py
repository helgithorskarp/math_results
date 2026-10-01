"""Sequential full reproduction; generated comparison data stay in workspace scratch."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import resource
import subprocess
import sys
import time

HERE = Path(__file__).resolve().parent


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--work", type=Path, default=HERE/".work")
    parser.add_argument("--record", type=Path)
    args = parser.parse_args()
    work = args.work.resolve()
    work.mkdir(parents=True, exist_ok=True)
    env = dict(os.environ)
    for name in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS"):
        env[name] = "1"
    commands = [["-B", "produce.py", "--work", str(work)],
                ["-B", "verify.py", "--compare", str(work/"producer-carriers.json")],
                ["-B", "-O", "verify.py"], ["-B", "-O", "controls.py"]]
    records = []
    for command in commands:
        started = time.monotonic()
        completed = subprocess.run([sys.executable]+command, cwd=HERE, env=env,
                                   capture_output=True, text=True, timeout=60, check=True)
        if completed.stderr:
            raise RuntimeError("unexpected diagnostic: "+completed.stderr)
        result = json.loads(completed.stdout)
        if result.get("status") != "COMPLETE":
            raise RuntimeError("incomplete child")
        records.append({"command": command, "seconds": time.monotonic()-started,
                        "result": result})
    if records[0]["result"]["manifest_sha256"] != records[1]["result"]["manifest_sha256"] \
            or records[1]["result"]["manifest_sha256"] != records[2]["result"]["manifest_sha256"]:
        raise RuntimeError("normal/optimized source output disagreement")
    evidence = {"agent": "six-code-3", "role": "researcher", "status": "COMPLETE",
                "python": sys.version, "child_peak_rss_kib": resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,
                "threads": 1, "commands": records,
                "expected_bytes": (HERE/"expected.json").stat().st_size,
                "expected_sha256": hashlib.sha256((HERE/"expected.json").read_bytes()).hexdigest()}
    if args.record:
        args.record.write_text(json.dumps(evidence, sort_keys=True, indent=2)+"\n")
    print(json.dumps({"status": "COMPLETE", "children": len(records),
                      "seconds": sum(r["seconds"] for r in records),
                      "child_peak_rss_kib": evidence["child_peak_rss_kib"],
                      "manifest_sha256": evidence["expected_sha256"]}, sort_keys=True))


if __name__ == "__main__":
    main()
