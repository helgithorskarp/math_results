#!/usr/bin/env python3
"""Native-checker semantic controls, parser negatives, and saved-prefix replay."""
import argparse
from hashlib import sha256
import json
from pathlib import Path
import subprocess
import tempfile
import time
from fast_check import check
from physical import catalog, require


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("checker", type=Path)
    parser.add_argument("--run", type=Path)
    parser.add_argument("--prefix", type=int, default=0)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    binary = args.checker.resolve()
    semantic = json.loads(subprocess.check_output([str(binary), "--controls"], text=True))
    require(semantic["status"] == "PASS", "Semantic controls failed")
    square = "p cnf 2 4\n1 2 0\n1 -2 0\n-1 2 0\n-1 -2 0\n"
    # SAT inputs must not be refuted, even after deletions or new-pivot additions.
    negatives = [
        ("p cnf 1 1\n1 0\n", "0\n"),
        (square, "0\n"),
        (square, "1 0\n"),
        (square, "1 0\n0\n1 0\n"),
        (square, "1 1 0\n0\n"),
        (square, "1 -1 0\n0\n"),
        (square, "1 0 junk\n0\n"),
        (square, "1 0 0\n0\n"),
        (square, "1000001 0\n0\n"),
        ("p cnf 1 2\n1 0\n", "0\n"),
        ("p cnf 1 junk\n", "0\n"),
        ("p cnf 1\n", "0\n"),
        ("p cnf 1 1\n2 0\n", "0\n"),
        ("p cnf 1 1\n1 1 0\n", "0\n"),
        ("p cnf 1 1\n1 -1 0\n", "0\n"),
        ("p cnf 1 1\n1 0\n", "2 0\nd 1 0\n0\n"),
    ]
    positives = [
        (square, "1 0\n0\n"),
        (square, "1 0\n1 0\nd 1 0\n0\n"),
        (square, "3 0\n1 0\n0\n"),
        (square, "d 3 0\n1 0\n0\n"),
        ("p cnf 1 1\n0\n", "0\n"),
    ]
    with tempfile.TemporaryDirectory(prefix="r55-drat-controls-") as directory:
        core, proof = Path(directory)/"core.cnf", Path(directory)/"proof.drat"
        for expect, cases in [(False, negatives), (True, positives)]:
            for i, (cnf, trace) in enumerate(cases):
                core.write_text(cnf)
                proof.write_text(trace)
                result = subprocess.run([str(binary), str(core), str(proof)], capture_output=True, text=True)
                require((result.returncode == 0) == expect,
                        f"Proof control {expect}/{i}: {result.returncode} {result.stderr}")
    replay = []
    records = catalog(Path(__file__).with_name("r55_42some.g6"))
    require(0 <= args.prefix <= len(records), "Prefix out of bounds")
    for index in range(args.prefix):
        require(args.run is not None, "Prefix replay needs --run")
        folder = args.run/f"parent{index:03d}"
        previous = json.loads((folder/"result.json").read_text())
        require(previous["parent"] == index and previous["seed"] == records[index], "Input mismatch")
        start = time.monotonic()
        report = check(records[index], folder/"core.cnf", folder/"trimmed.drat", binary)
        elapsed = time.monotonic()-start
        require(report == previous["certificate"], f"Reference mismatch at {index}")
        replay.append({"parent": index, "seconds": elapsed,
                       "certificate_sha256": sha256(json.dumps(report, sort_keys=True).encode()).hexdigest()})
    report = {"status": "PASS", "semantic": semantic, "negative_controls": len(negatives),
              "positive_controls": len(positives), "checker_sha256": sha256(binary.read_bytes()).hexdigest(),
              "replayed": len(replay), "seconds": sum(r["seconds"] for r in replay), "cases": replay}
    text = json.dumps(report, indent=2)+"\n"
    if args.output:
        args.output.write_text(text)
    print(text, end="")


if __name__ == "__main__":
    main()
