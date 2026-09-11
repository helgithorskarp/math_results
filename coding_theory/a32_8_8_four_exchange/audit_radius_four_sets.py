#!/usr/bin/env python3
"""Independent Python audit of the complete radius-four removal-set cover."""

from __future__ import annotations

import argparse
import resource
import sys
import time
from itertools import combinations
from pathlib import Path


def load_supports(path: Path) -> dict[tuple[int, ...], int]:
    result: dict[tuple[int, ...], int] = {}
    lines = path.read_text(encoding="ascii").splitlines()
    if not lines or lines[0] != "word_hex\tblocker_count\tblockers_zero_based":
        raise AssertionError("unexpected low-candidate header")
    for line in lines[1:]:
        _, count_text, blocker_text = line.split("\t")
        support = tuple(map(int, blocker_text.split(",")))
        if len(support) != int(count_text) or not 1 <= len(support) <= 4:
            raise AssertionError("invalid blocker support")
        result[support] = result.get(support, 0) + 1
    if sum(result.values()) != 6051:
        raise AssertionError("expected 6051 candidates")
    return result


def pack_quad(values: set[int] | tuple[int, ...] | list[int]) -> int:
    ordered = sorted(values)
    if len(ordered) != 4 or len(set(ordered)) != 4:
        raise AssertionError("not a four-set")
    return ordered[0] | ordered[1] << 11 | ordered[2] << 22 | ordered[3] << 33


def main() -> None:
    started = time.monotonic()
    parser = argparse.ArgumentParser()
    parser.add_argument("low4", type=Path)
    args = parser.parse_args()
    support_counts = load_supports(args.low4)
    singletons = sorted(support[0] for support in support_counts if len(support) == 1)
    pairs = sorted(support for support in support_counts if len(support) == 2)
    triples = sorted(support for support in support_counts if len(support) == 3)
    quads = sorted(support for support in support_counts if len(support) == 4)
    active = sorted({blocker for support in support_counts for blocker in support})

    removals = {pack_quad(support) for support in quads}
    for triple in triples:
        triple_set = set(triple)
        for blocker in active:
            if blocker not in triple_set:
                removals.add(pack_quad((*triple, blocker)))
    after_triples = len(removals)

    for first_index, first in enumerate(pairs):
        first_set = set(first)
        for second in pairs[first_index + 1 :]:
            union = first_set | set(second)
            if len(union) == 4:
                removals.add(pack_quad(union))
            elif len(union) == 3:
                for blocker in active:
                    if blocker not in union:
                        removals.add(pack_quad((*union, blocker)))
            else:
                raise AssertionError("distinct pair supports have union smaller than three")
    after_pair_pairs = len(removals)

    for pair in pairs:
        pair_set = set(pair)
        for first, second in combinations(singletons, 2):
            union = pair_set | {first, second}
            if len(union) == 4:
                removals.add(pack_quad(union))

    observed = (
        len(singletons),
        len(pairs),
        len(triples),
        len(quads),
        len(active),
        after_triples,
        after_pair_pairs,
        len(removals),
    )
    expected = (116, 543, 1479, 3632, 1366, 2_018_499, 3_883_999, 7_359_226)
    if observed != expected:
        raise AssertionError(f"unexpected removal-cover counts: {observed}")
    labels = (
        "singleton_supports",
        "pair_supports",
        "triple_supports",
        "quadruple_supports",
        "active_blockers",
        "removal_sets_after_triples",
        "removal_sets_after_pair_pairs",
        "radius_four_removal_sets",
    )
    for label, value in zip(labels, observed):
        print(f"{label}={value}")
    print("independent_removal_cover_audit=PASS")
    print(f"elapsed_seconds={time.monotonic() - started:.6f}", file=sys.stderr)
    print(f"peak_rss_kib={resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}", file=sys.stderr)


if __name__ == "__main__":
    main()
