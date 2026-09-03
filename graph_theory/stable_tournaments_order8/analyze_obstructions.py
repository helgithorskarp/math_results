#!/usr/bin/env python3
"""Report elementary invariants of the 96 order-eight m=2 tournament classes."""

from __future__ import annotations

import argparse
import collections
import itertools
import re
from pathlib import Path

N = 8
PAIRS = [(i, j) for i in range(N) for j in range(i + 1, N)]
FAIL_RE = re.compile(r"^FAIL (?P<index>\d+) tournament=(?P<tournament>\d+)$")


def matrix(mask: int) -> list[list[int]]:
    result = [[0] * N for _ in range(N)]
    for bit, (i, j) in enumerate(PAIRS):
        result[i][j] = (mask >> bit) & 1
        result[j][i] = 1 - result[i][j]
    return result


def relabel(old: list[list[int]], permutation: tuple[int, ...]) -> int:
    return sum(old[permutation[i]][permutation[j]] << bit for bit, (i, j) in enumerate(PAIRS))


def strongly_connected(adjacency: list[list[int]]) -> bool:
    for start in range(N):
        seen = {start}
        frontier = [start]
        while frontier:
            vertex = frontier.pop()
            for target in range(N):
                if adjacency[vertex][target] and target not in seen:
                    seen.add(target)
                    frontier.append(target)
        if len(seen) != N:
            return False
    return True


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("certificate", type=Path)
    args = parser.parse_args()
    records: list[tuple[int, int]] = []
    for line in args.certificate.read_text(encoding="ascii").splitlines():
        match = FAIL_RE.fullmatch(line)
        if match:
            records.append((int(match["index"]), int(match["tournament"])))
    if len(records) != 96:
        raise ValueError(f"expected 96 obstructions, got {len(records)}")

    permutations = list(itertools.permutations(range(N)))
    score_counter: collections.Counter[tuple[int, ...]] = collections.Counter()
    automorphism_counter: collections.Counter[int] = collections.Counter()
    strong_count = 0
    for _, tournament in records:
        adjacency = matrix(tournament)
        scores = tuple(sorted(map(sum, adjacency)))
        score_counter[scores] += 1
        strong_count += strongly_connected(adjacency)
        automorphisms = sum(relabel(adjacency, permutation) == tournament for permutation in permutations)
        automorphism_counter[automorphisms] += 1

    print(f"m2_classes={len(records)} strongly_connected={strong_count}")
    print("score_sequences")
    for scores, count in sorted(score_counter.items()):
        print(f"{','.join(map(str, scores))}\t{count}")
    print("automorphism_group_orders")
    for order, count in sorted(automorphism_counter.items()):
        print(f"{order}\t{count}")
    first_index, first_tournament = records[0]
    first_matrix = matrix(first_tournament)
    print(f"first_obstruction class={first_index} mask={first_tournament}")
    print("first_score_sequence=" + ",".join(map(str, sorted(map(sum, first_matrix)))))
    for row in first_matrix:
        print("".join(map(str, row)))


if __name__ == "__main__":
    main()
