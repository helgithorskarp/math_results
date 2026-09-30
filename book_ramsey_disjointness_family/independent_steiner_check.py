#!/usr/bin/env python3
"""Edge-first count of every bad spine, independent of the deletion-first run."""
from collections import Counter
from hashlib import sha256
from itertools import combinations
from pathlib import Path
import json

HERE = Path(__file__).resolve().parent


def main():
    blocks = [set(b) for b in json.loads((HERE / "steiner_blocks.json").read_text())]
    assert len(blocks) == 26 and all(len(b) == 3 and b <= set(range(13)) for b in blocks)
    assert len({tuple(sorted(b)) for b in blocks}) == 26
    assert all(sum({x, y} <= b for b in blocks) == 1 for x, y in combinations(range(13), 2))
    deletion_sets = list(combinations(range(26), 4))
    counts = {d: 0 for d in deletion_sets}
    edges = 0
    for i, j in combinations(range(26), 2):
        if not blocks[i] & blocks[j]:
            continue
        edges += 1
        common = [k for k in range(26) if k != i and k != j
                  and blocks[k] & blocks[i] and blocks[k] & blocks[j]]
        assert len(common) == 8
        outside = [k for k in range(26) if k not in common and k != i and k != j]
        assert len(outside) == 16
        # Retaining this spine leaves >=7 pages precisely when the four
        # deletions contain zero or one of its original eight pages.
        for d in combinations(outside, 4):
            counts[d] += 1
        for page in common:
            for other in combinations(outside, 3):
                counts[tuple(sorted((page, *other)))] += 1
    assert edges == 195
    vector = [counts[d] for d in deletion_sets]
    assert all(0 <= x <= 195 for x in vector)
    hist = dict(sorted(Counter(vector).items()))
    digest = sha256(bytes(vector)).hexdigest()
    expected = json.loads((HERE / "expected.json").read_text())["cyclic_STS13"]
    assert digest == expected["ordered_counts_sha256"]
    assert {str(k): v for k, v in hist.items()} == expected["bad_spine_histogram"]
    assert min(vector) == 39 and vector.count(39) == 13
    # Literal entry-level comparison, not merely matching aggregate totals.
    from verify import deletion_counts
    _, deletion_first_vector = deletion_counts(return_vector=True)
    assert vector == deletion_first_vector
    print(json.dumps({"algorithm": "spine-first exact incidence enumeration",
                      "sets_checked": len(vector), "minimum": min(vector),
                      "minimizers": vector.count(min(vector)),
                      "ordered_counts_sha256": digest}, indent=2))


if __name__ == "__main__":
    main()
