#!/usr/bin/env python3
"""Regenerate and compare the independent h3909 review evidence."""

import argparse
import hashlib
import json
import subprocess
import sys
import tempfile
from pathlib import Path


HERE = Path(__file__).resolve().parent
SOURCE = HERE.parent / "ramsey_r55_maximal_vertex_connectivity"
MANIFEST_SHA256 = "a9ea0aeb000182d0f1e3ff5f8bd1763230669b29dd7587785ed77336c6d572d0"


def need(ok, message):
    if not ok:
        raise ValueError(message)


def run(argv):
    result = subprocess.run(argv, capture_output=True, check=True)
    if result.stderr:
        raise ValueError(("unexpected stderr", argv, result.stderr.decode()))
    return result.stdout


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("scratch", type=Path,
                        help="existing directory for regenerated temporary streams")
    args = parser.parse_args()
    need(args.scratch.is_dir(), "scratch directory does not exist")
    need(hashlib.sha256((SOURCE / "SHA256SUMS").read_bytes()).hexdigest() ==
         MANIFEST_SHA256, "reviewed source manifest differs")

    with tempfile.TemporaryDirectory(prefix="h3909-review-", dir=args.scratch) as temp:
        temp = Path(temp)
        producer = temp / "producer"
        run([sys.executable, "-B", str(SOURCE / "enumerate.py"), str(producer)])
        stream = producer / "witnesses.jsonl"
        stream_bytes = stream.read_bytes()
        results = []
        for backend in ("cadical195", "minisat22"):
            output = run([
                sys.executable, "-B", str(HERE / "independent_sat_check.py"),
                str(SOURCE), "--producer-stream", str(stream), "--solver", backend,
            ])
            results.append(json.loads(output))

    stripped = []
    for result in results:
        result = dict(result)
        result.pop("solver")
        stripped.append(result)
    need(stripped[0] == stripped[1], "SAT backend results differ")
    receipt = {
        "status": "REPRODUCED_INDEPENDENT_REVIEW_H3909",
        "reviewed_manifest_sha256": MANIFEST_SHA256,
        "producer_stream_records": stream_bytes.count(b"\n"),
        "producer_stream_sha256": hashlib.sha256(stream_bytes).hexdigest(),
        "backends": ["cadical195", "minisat22"],
        "finite_hinge": stripped[0],
    }
    expected = json.loads((HERE / "EXPECTED.json").read_text())
    need(receipt == expected, "review receipt differs from EXPECTED.json")
    print(json.dumps(receipt, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
