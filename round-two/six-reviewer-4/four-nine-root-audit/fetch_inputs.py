#!/usr/bin/env python3
"""Fetch only two public, exact hash-pinned proof inputs to a chosen directory."""
import argparse, hashlib
from pathlib import Path
from urllib.request import urlopen

INPUTS = (
    ("certificate.json", "https://raw.githubusercontent.com/helgithorskarp/math_results/4674720842bee9238370fd4a6543c10da96b510b/round-two/six-books-3/four-nine108/certificate.json", "1eb55ea5963ecbba0deaa1414bcbdb4aa500e9fa0ce9e2a81f6bb77684428330"),
    ("primary21.txt", "https://raw.githubusercontent.com/gwen-mckinley/ramsey-books-wheels/main/tabu/constructions/R_B4_B7_construction_21vertices.txt", "3b648b66a5990d0b6ed945ce80d3f546e90f2b233f924775bb02ac2418558a55"),
)

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("directory", type=Path)
    args = p.parse_args()
    args.directory.mkdir(parents=True, exist_ok=True)
    for filename, url, expected in INPUTS:
        with urlopen(url, timeout=30) as response:
            raw = response.read()
        if hashlib.sha256(raw).hexdigest() != expected:
            raise ValueError("Public proof input changed: " + filename)
        (args.directory/filename).write_bytes(raw)
        print(filename, len(raw), expected)
