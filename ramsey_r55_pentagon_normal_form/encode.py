#!/usr/bin/env python3
"""Emit the complete physical Ramsey formula; do not run a solver."""
import argparse
import hashlib
import json
import shutil
import tempfile
from collections import Counter
from pathlib import Path
import frame


def encode(path, n=43, cycles=5, joined=True):
    counts = Counter()
    lengths = Counter()
    nv = len(frame.variables(n, cycles, joined))
    path = Path(path)
    with tempfile.TemporaryFile(mode="w+b") as body:
        for color, clause in frame.clauses(n, cycles, joined):
            body.write((" ".join(map(str, clause)) + (" " if clause else "") + "0\n").encode())
            counts[color] += 1
            lengths[len(clause)] += 1
        body.seek(0)
        with path.open("wb") as out:
            out.write(f"p cnf {nv} {sum(counts.values())}\n".encode())
            shutil.copyfileobj(body, out)
    with path.open("rb") as source:
        digest = hashlib.file_digest(source, "sha256").hexdigest()
    return {"status": "EMITTED_COMPLETE_FRAME_CNF", "n": n, "cycles": cycles,
            "joined": joined, "fixed_pairs": len(frame.pins(n, cycles, joined)),
            "variables": nv, "clauses": sum(counts.values()),
            "red_clauses": counts[1], "blue_clauses": counts[0],
            "length_histogram": {str(k): v for k, v in sorted(lengths.items())},
            "bytes": path.stat().st_size, "sha256": digest}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    print(json.dumps(encode(args.output), sort_keys=True))
