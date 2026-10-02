#!/usr/bin/env python3
"""Replay the primary 21-point incumbent; not a new construction."""
from pathlib import Path
import hashlib
import json
import sys
import urllib.request

URL = "https://raw.githubusercontent.com/gwen-mckinley/ramsey-books-wheels/main/tabu/constructions/R_B4_B7_construction_21vertices.txt"


def replay(raw):
    # The source appends search metadata after its leading JSON matrix.
    matrix, _ = json.JSONDecoder().raw_decode(raw.decode().lstrip())
    n = len(matrix)
    if n != 21 or any(len(row) != n for row in matrix):
        raise ValueError("primary matrix dimensions")
    if any(matrix[i][j] not in (0,1) or matrix[i][j] != matrix[j][i]
           for i in range(n) for j in range(n)):
        raise ValueError("primary matrix color or symmetry")
    pages = [[],[]]
    for i in range(n):
        for j in range(i+1,n):
            color = matrix[i][j]  # off-diagonal zero=red, one=blue
            pages[color].append(sum(k != i and k != j and
                matrix[i][k] == color and matrix[j][k] == color for k in range(n)))
    counts = (len(pages[0]),len(pages[1]),max(pages[0]),max(pages[1]))
    if counts != (93,117,3,6):
        raise ValueError("primary incumbent changed or failed")
    digest = hashlib.sha256(raw).hexdigest()
    if digest != "3b648b66a5990d0b6ed945ce80d3f546e90f2b233f924775bb02ac2418558a55":
        raise ValueError("primary raw-byte identity differs")
    return {"source":URL,"raw_sha256":digest,"n":n,"red_edges":counts[0],
            "blue_edges":counts[1],"max_red_pages":counts[2],"max_blue_pages":counts[3]}


if __name__ == "__main__":
    if len(sys.argv) > 2:
        raise SystemExit("usage: baseline.py [downloaded-primary-file]")
    raw = Path(sys.argv[1]).read_bytes() if len(sys.argv) == 2 else urllib.request.urlopen(URL,timeout=20).read()
    print(json.dumps(replay(raw),separators=(",", ":")))
