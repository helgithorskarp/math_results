#!/usr/bin/env python3
import json
from pathlib import Path

from exact_model import exact_certificate


HERE = Path(__file__).resolve().parent
expected = json.loads((HERE / "certificate.json").read_text())
actual = exact_certificate()
if actual != expected:
    raise SystemExit("certificate mismatch; run produce.py and compare")
print(json.dumps({
    "status": "verified",
    "m1_vertices": actual["m1_vertices"],
    "m2_vertices": actual["m2_vertices"],
    "shells": len(actual["shells"]),
    "maximal_budget_pairs": [
        [row["left_vertices"], row["right_vertices"]]
        for row in actual["maximal_budget_pairs"]
    ],
    "largest_prefix_vertices": actual["largest_relevant_prefix_vertices"],
    "largest_prefix_edges": len(actual["largest_relevant_prefix_unit_edges"]),
    "largest_prefix_bipartite": True,
    "conclusion": actual["conclusion"],
}, indent=2))
