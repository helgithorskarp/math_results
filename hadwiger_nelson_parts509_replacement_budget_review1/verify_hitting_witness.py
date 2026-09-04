#!/usr/bin/env python3
"""Check the reviewer's size-90 hitting set against the published family.

This is deliberately solver-free.  It imports no target module and derives the
distinct and inclusion-minimal families directly from certificate.json.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path


HERE = Path(__file__).resolve().parent
DEFAULT_CERTIFICATE = (
    HERE.parent / "hadwiger_nelson_parts509_s_replacement_budget" / "certificate.json"
)


def minimal_family(rows: list[dict[str, object]]) -> list[frozenset[int]]:
    distinct = sorted(
        {frozenset(map(int, row["D"])) for row in rows},
        key=lambda item: (len(item), tuple(sorted(item))),
    )
    minimal: list[frozenset[int]] = []
    for candidate in distinct:
        if not any(earlier < candidate for earlier in minimal if len(earlier) < len(candidate)):
            minimal.append(candidate)
    return minimal


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certificate", type=Path, default=DEFAULT_CERTIFICATE)
    parser.add_argument("--witness", type=Path, default=HERE / "hitting_set_90.txt")
    args = parser.parse_args()

    certificate = json.loads(args.certificate.read_text())
    s_vertices = list(map(int, certificate["S"]))
    assert s_vertices == list(range(374, 509))
    rows = certificate["killing_sets"]
    distinct = {frozenset(map(int, row["D"])) for row in rows}
    minimal = minimal_family(rows)
    assert len(rows) == len(distinct) == 3575
    assert len(minimal) == certificate["solver_bound"]["minimal_sets"] == 2852

    forced = sorted(next(iter(item)) for item in minimal if len(item) == 1)
    pairs = [item for item in minimal if len(item) == 2]
    assert len(forced) == 30
    assert len(pairs) == 125
    assert len(set().union(*pairs)) == 78

    witness_values = [int(value) for value in args.witness.read_text().split()]
    witness = frozenset(witness_values)
    assert len(witness_values) == len(witness) == 90
    assert witness <= set(s_vertices)
    assert all(item & witness for item in distinct)

    canonical = " ".join(map(str, sorted(witness))) + "\n"
    digest = hashlib.sha256(canonical.encode()).hexdigest()
    assert digest == "3253baae849fe5dd1eb7c04a60fa05dbec61f26098fb4ed627c052f77bd61d76"
    histogram = dict(sorted(Counter(map(len, minimal)).items()))
    print(f"rows={len(rows)} distinct={len(distinct)} minimal={len(minimal)}")
    print(f"minimal_size_histogram={histogram}")
    print(f"forced_singletons={len(forced)} minimal_pairs={len(pairs)} pair_vertices=78")
    print(f"hitting_set_size={len(witness)} sha256={digest}")
    print("witness_check=true")


if __name__ == "__main__":
    main()
