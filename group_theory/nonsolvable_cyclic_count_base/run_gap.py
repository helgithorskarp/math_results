#!/usr/bin/env python3
"""Run the exact GAP exporter with a 512-MiB heap and compact cost record."""
import argparse
import hashlib
import json
from pathlib import Path
import resource
import shutil
import subprocess
import sys
import time


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--gap", default="gap", help="GAP kernel/executable")
    parser.add_argument("--root", help="Optional GAP root for a local extraction")
    args = parser.parse_args()
    directory = Path(__file__).resolve().parent
    executable = shutil.which(args.gap) or args.gap
    command = [executable, "-A", "-b", "-q", "-m", "64m", "-o", "512m",
               "--quitonbreak"]
    if args.root:
        command.extend(["-l", args.root])
    command.append("export_base.g")
    start = time.monotonic()
    with (directory / "gap-run-private.txt").open("w") as output:
        result = subprocess.run(command, cwd=directory, stdout=output,
                                stderr=subprocess.STDOUT, check=False)
    cost = resource.getrusage(resource.RUSAGE_CHILDREN)
    summary = dict(exit_code=result.returncode,
                   wall_seconds=round(time.monotonic()-start,3),
                   user_seconds=round(cost.ru_utime,3),
                   system_seconds=round(cost.ru_stime,3),
                   max_rss_kib=cost.ru_maxrss,
                   python_version=sys.version.split()[0],
                   native_threads=1, gap_heap_limit="512m")
    evidence = directory / "evidence.json"
    if result.returncode == 0:
        json.loads(evidence.read_text())  # Reject a truncated/non-JSON export.
        summary["evidence_sha256"] = hashlib.sha256(evidence.read_bytes()).hexdigest()
    (directory / "run_summary.json").write_text(json.dumps(summary,indent=2)+"\n")
    print(json.dumps(summary))
    if result.returncode:
        raise SystemExit(result.returncode)


if __name__ == "__main__":
    main()
