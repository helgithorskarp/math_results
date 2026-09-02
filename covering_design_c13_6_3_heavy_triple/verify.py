#!/usr/bin/env python3
"""Definition-level verification of the upper cover and reduction arithmetic."""

from __future__ import annotations

import argparse
import collections
import itertools
import json
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cover", type=Path, default=Path("upper_cover.json"))
    parser.add_argument("--orbits", type=Path, default=Path("orbit_representatives.json"))
    args = parser.parse_args()
    payload = json.loads(args.cover.read_text())
    blocks = [tuple(block) for block in payload["blocks"]]
    assert len(blocks) == len(set(blocks)) == 21
    assert all(len(block) == 6 and tuple(sorted(block)) == block for block in blocks)
    assert all(1 <= point <= 13 for block in blocks for point in block)
    multiplicity = collections.Counter()
    for block in blocks:
        multiplicity.update(itertools.combinations(block, 3))
    triples = set(itertools.combinations(range(1, 14), 3))
    assert set(multiplicity) == triples
    distribution = collections.Counter(multiplicity.values())
    assert distribution == {1: 188, 2: 73, 3: 14, 4: 11}
    reduced = collections.Counter()
    for block in blocks[:-1]:
        reduced.update(itertools.combinations(block, 3))
    assert set(reduced) != triples

    # Arithmetic forced for a hypothetical 20-block cover.
    degrees = [10] * 3 + [9] * 10
    assert sum(degrees) == 20 * 6 == 120
    total_block_pair_intersection = sum(d * (d - 1) // 2 for d in degrees)
    assert total_block_pair_intersection == 495
    block_pairs = 20 * 19 // 2
    assert total_block_pair_intersection - 2 * block_pairs == 115
    triple_incidence_excess = 20 * 20 - len(triples)
    assert triple_incidence_excess == 114
    assert total_block_pair_intersection - 2 * block_pairs > triple_incidence_excess

    orbits = json.loads(args.orbits.read_text())
    assert orbits["counts_by_a"] == [177, 103, 44, 12]
    assert orbits["total_orbits"] == 336
    print(json.dumps({
        "upper_cover_blocks": len(blocks),
        "covered_triples": len(multiplicity),
        "upper_cover_multiplicity_distribution": dict(sorted(distribution.items())),
        "hypothetical_20_degree_profile": degrees,
        "hypothetical_20_block_pair_intersection_sum": total_block_pair_intersection,
        "forced_repeated_triple_pair_lower_bound": 115,
        "triple_incidence_excess": triple_incidence_excess,
        "orbit_counts_by_a": orbits["counts_by_a"],
        "total_orbits": orbits["total_orbits"]
    }, sort_keys=True))


if __name__ == "__main__":
    main()
