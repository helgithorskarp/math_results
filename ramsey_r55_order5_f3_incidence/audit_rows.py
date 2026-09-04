#!/usr/bin/env python3
"""Independent row-set enumeration; no canonicalization code is imported.

Fix the first red row to {0,1,2,3} by a permutation of the eight columns.
Enumerate both other four-subsets and every fixed triangle. Use direct
set intersections, including both colors, then normalize the minority edge.
"""
from itertools import combinations, product
from collections import Counter
import json
from pathlib import Path


def main():
    universe = frozenset(range(8))
    rows = [frozenset(s) for s in combinations(range(8), 4)]
    pairs = ((0, 1), (0, 2), (1, 2))
    passing = Counter()
    tested = 0
    for row1, row2 in product(rows, repeat=2):
        red = (frozenset(range(4)), row1, row2)
        blue = tuple(universe - r for r in red)
        for edges in product((0, 1), repeat=3):
            tested += 1
            neighborhoods = (blue, red)
            if any(len(neighborhoods[c][i] & neighborhoods[c][j]) > 2
                   for c in (0, 1) for i, j in pairs):
                continue
            if all(e == edges[0] for e in edges):
                color_rows = neighborhoods[edges[0]]
                if color_rows[0] & color_rows[1] & color_rows[2]:
                    continue
            if any(len(neighborhoods[c][i] & neighborhoods[c][j] &
                       neighborhoods[1-c][3-i-j]) > 1
                   for (i, j), c in zip(pairs, edges)):
                continue
            assert sum(edges) in (1, 2), "unexpected monochromatic survivor"
            minority = 1 if sum(edges) == 1 else 0
            x, y = pairs[edges.index(minority)]
            z = 3-x-y
            color_rows = neighborhoods[minority]
            multiplicities = Counter()
            for col in range(8):
                value = sum((col in color_rows[v]) << i
                            for i, v in enumerate((x, y, z)))
                multiplicities[value] += 1
            h = multiplicities[7]
            assert h in (0, 1)
            expected = (1, 1, 1, 1, h, 2-h, 2-h, h)
            assert tuple(multiplicities[v] for v in range(8)) == expected
            passing[h] += 1
    reference = json.loads(Path(__file__).with_name("result.json").read_text())
    assert sum(passing.values()) * len(rows) == reference["counts"][
        "surviving_fully_labeled_matrices"]
    assert tested == 70 * 70 * 8 == 39200
    assert dict(passing) == {0: 864, 1: 3456}
    print(f"ROW_AUDIT tested={tested} survivors={sum(passing.values())} "
          f"h0={passing[0]} h1={passing[1]}")
    print("PASS: every admissible ordered incidence matrix has the proved form")


if __name__ == "__main__":
    main()
