#!/usr/bin/env python3
"""Definition-level checks for the four realizable point-degree patterns."""

from __future__ import annotations

import itertools
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
POINTS = tuple(range(12))


def verify(a: int, blocks: list[list[int]]) -> dict[str, object]:
    expected = (5,) * a + (4,) * (9 - 2 * a) + (3,) * (3 + a)
    normalized = [tuple(sorted(block)) for block in blocks]
    assert len(normalized) == 9
    assert len(set(normalized)) == 9
    assert all(len(block) == 5 and set(block) <= set(POINTS) for block in normalized)
    assert all(any(first in block and second in block for block in normalized)
               for first, second in itertools.combinations(POINTS, 2))
    degrees = tuple(sum(point in block for block in normalized) for point in POINTS)
    assert degrees == expected, (a, degrees, expected)
    multiplicities = [sum(first in block and second in block for block in normalized)
                      for first, second in itertools.combinations(POINTS, 2)]
    histogram = {value: multiplicities.count(value) for value in sorted(set(multiplicities))}
    return {"a": a, "degrees": degrees, "pair_multiplicities": histogram}


def main() -> None:
    payload = json.loads((ROOT / "witnesses.json").read_text())
    summary = [verify(a, payload[str(a)]) for a in range(4)]
    print(json.dumps(summary, sort_keys=True))
    print("witness_audit=PASS")


if __name__ == "__main__":
    main()
