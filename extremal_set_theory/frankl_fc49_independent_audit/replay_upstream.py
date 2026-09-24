#!/usr/bin/env python3
"""Replay the pinned upstream classification and emit a compact audit summary.

The upstream checkout and generated output are external inputs, not bundled
here. This always runs the verifier; a saved PASS report alone is not accepted.
"""
import argparse
import hashlib
import json
from pathlib import Path
import platform
import re
import resource
import subprocess
import sys
import time

UPSTREAM_COMMIT = "17002022f9bb033fb6b40e7b5d1484e78ceb0ac2"


def require(condition, message):
    if not condition:
        raise ValueError(message)


def command(*args):
    return subprocess.check_output([str(x) for x in args], text=True).strip()


def source_digest(source):
    require(command("git", "-C", source, "rev-parse", "HEAD") == UPSTREAM_COMMIT,
            "Wrong upstream commit")
    subprocess.run(["git", "-C", str(source), "diff", "--exit-code", "HEAD"], check=True,
                   stdout=subprocess.DEVNULL)
    paths = command("git", "-C", source, "ls-files").splitlines()
    digest = hashlib.sha256()
    total = 0
    for name in sorted(paths):
        content = (source / name).read_bytes()
        total += len(content)
        digest.update(name.encode() + b"\0" + hashlib.sha256(content).digest())
    return {"commit": UPSTREAM_COMMIT, "tracked_files": len(paths),
            "tracked_bytes": total, "path_content_manifest_sha256": digest.hexdigest()}


def summarize(source):
    root = source / "fc49"
    report = json.loads((root / "run/verification_report.json").read_text())
    foundation = json.loads((root / "foundation/verification_report.json").read_text())
    require(report["status"] == foundation["status"] == "PASS", "Incomplete upstream run")
    counters = dict(nodes=0, leaves=0, conflicts=0)
    positives = 0
    for record in foundation["witnesses"] + report["new_certificate_replays"]:
        if record["status"] != "FC":
            continue
        text = record.get("integer_replay", record.get("replay", ""))
        match = re.fullmatch(r"status 0 nodes (\d+) leaves (\d+) conflicts (\d+) depth \d+ seconds \S+", text)
        require(match is not None, "Malformed successful tree replay")
        for k, v in zip(counters, match.groups()):
            counters[k] += int(v)
        positives += 1
    require(positives == 3954 and counters["nodes"] == 26456004, "Wrong tree totals")
    enumerations = {}
    for mode, text in report["enumeration16"].items():
        match = re.fullmatch(r"DONE cases (\d+) visits (\d+) leaves (\d+) pruned7 (\d+) pruned8 (\d+) pruneddeg (\d+)", text)
        require(match is not None, "Incomplete final traversal")
        enumerations[mode] = dict(zip(("cases", "visits", "survivors", "pruned7", "pruned8", "pruneddeg"),
                                     map(int, match.groups())))
        require(enumerations[mode]["cases"] == 68 and enumerations[mode]["survivors"] == 0,
                "A final traversal has a survivor or missing base")
    require(set(enumerations) == {"normal", "no7", "nodegree"}, "Missing traversal")
    return {"status": "PASS", "theorem": "FC(4,9)=16 (upstream replay)",
            "records": report["records"], "positive_records": positives,
            "negative_records": report["negative_records"], "positive_tree_totals": counters,
            "boundary_counts": report["boundary_counts"], "enumerations": enumerations,
            "lower15_dual_sum": report["lower15_dual_sum"]}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", type=Path, required=True)
    ap.add_argument("--output", type=Path, required=True)
    ap.add_argument("--workers", type=int, default=4)
    args = ap.parse_args()
    require(args.workers > 0, "workers must be positive")
    require(sys.flags.optimize == 0, "Upstream requires assertions enabled")
    source = args.source.resolve()
    provenance = source_digest(source)
    started = time.monotonic()
    subprocess.run([sys.executable, "fc49/verify.py", "--workers", str(args.workers)],
                   cwd=source, check=True)
    require(source_digest(source) == provenance, "Upstream tracked input changed during replay")
    result = summarize(source)
    peak_rss = resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss
    if sys.platform == "darwin":
        peak_rss //= 1024
    result.update(upstream=provenance, python=platform.python_version(),
                  compiler=command("g++", "--version").splitlines()[0], workers=args.workers,
                  seconds=time.monotonic() - started,
                  child_peak_rss_kib=peak_rss)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
