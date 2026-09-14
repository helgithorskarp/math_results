#!/usr/bin/env python3
"""Normalize a target-generated field-rows.json for entrywise comparison."""

from hashlib import sha256
import json
from pathlib import Path
import sys

if len(sys.argv) != 2:
    raise SystemExit("usage: target_rows_digest.py field-rows.json")
rows = json.loads(Path(sys.argv[1]).read_text())
normalized = [
    {
        "trace": row["trace"],
        "norm": row["norm"],
        "edges": row["edges"],
        "D": row["D"],
        "valuation_plus": row["plus"]["valuation"],
        "valuation_minus": row["minus"]["valuation"],
        "embeds_plus": row["embeds_plus"],
        "embeds_minus": row["embeds_minus"],
    }
    for row in rows
]
normalized.sort(key=lambda row: (row["trace"], row["norm"], row["D"], row["edges"]))
packed = json.dumps(normalized, sort_keys=True, separators=(",", ":")).encode()
print(len(normalized), sha256(packed).hexdigest())
