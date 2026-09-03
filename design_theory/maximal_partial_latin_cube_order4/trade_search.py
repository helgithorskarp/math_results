#!/usr/bin/env python3
"""Deterministically search for a small cardinality-changing code trade."""

from __future__ import annotations

import argparse
import itertools
import json
from pathlib import Path


Word = tuple[int, ...]


def distance(left: Word, right: Word) -> int:
    return sum(a != b for a, b in zip(left, right, strict=True))


def find_trade(
    selected: set[Word], q: int, dimension: int, max_removed: int, size_change: int
) -> tuple[tuple[Word, ...], tuple[Word, ...]] | None:
    universe = list(itertools.product(range(q), repeat=dimension))
    ordered_selected = sorted(selected)
    word_index = {word: index for index, word in enumerate(universe)}
    selected_index = {word: index for index, word in enumerate(ordered_selected)}
    selected_ids = [word_index[word] for word in ordered_selected]
    outside_ids = [index for index, word in enumerate(universe) if word not in selected]
    full_coverage = (1 << len(universe)) - 1

    balls: list[int] = []
    for word in universe:
        ball = 0
        for index, other in enumerate(universe):
            if distance(word, other) <= 1:
                ball |= 1 << index
        balls.append(ball)
    selected_conflicts: dict[int, int] = {}
    for word_id in outside_ids:
        mask = 0
        for codeword in ordered_selected:
            if distance(universe[word_id], codeword) == 1:
                mask |= 1 << selected_index[codeword]
        selected_conflicts[word_id] = mask
    compatible: list[int] = []
    for word in universe:
        mask = 0
        for index, other in enumerate(universe):
            if distance(word, other) >= 2:
                mask |= 1 << index
        compatible.append(mask)

    for removed_count in range(1, max_removed + 1):
        for removed_positions in itertools.combinations(range(len(ordered_selected)), removed_count):
            removed_mask = sum(1 << position for position in removed_positions)
            eligible = [word_id for word_id in outside_ids if not selected_conflicts[word_id] & ~removed_mask]
            required = removed_count + size_change
            if required < 0 or len(eligible) < required:
                continue
            base_coverage = 0
            for position, word_id in enumerate(selected_ids):
                if not (removed_mask >> position) & 1:
                    base_coverage |= balls[word_id]

            def extend(
                start: int, inserted: list[int], allowed: int, coverage: int
            ) -> tuple[int, ...] | None:
                if len(inserted) == required:
                    return tuple(inserted) if coverage == full_coverage else None
                needed = required - len(inserted)
                for index in range(start, len(eligible) - needed + 1):
                    word_id = eligible[index]
                    if (allowed >> word_id) & 1:
                        result = extend(
                            index + 1,
                            inserted + [word_id],
                            allowed & compatible[word_id],
                            coverage | balls[word_id],
                        )
                        if result is not None:
                            return result
                return None

            inserted_ids = extend(0, [], full_coverage, base_coverage)
            if inserted_ids is not None:
                removed = tuple(ordered_selected[position] for position in removed_positions)
                inserted = tuple(universe[word_id] for word_id in inserted_ids)
                return removed, inserted
        print(json.dumps({"removed_count_completed": removed_count}), flush=True)
    return None


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("certificate", type=Path)
    parser.add_argument("--max-removed", type=int, default=5)
    parser.add_argument("--size-change", type=int, default=1)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    payload = json.loads(args.certificate.read_text(encoding="utf-8"))
    q = int(payload["order"])
    dimension = int(payload["dimension"])
    selected = {tuple(map(int, word)) for word in payload["selected_words"]}
    result = find_trade(selected, q, dimension, args.max_removed, args.size_change)
    if result is None:
        raise SystemExit("no trade found through the requested removal size")
    removed, inserted = result
    traded = sorted((selected - set(removed)) | set(inserted))
    output = {
        "dimension": dimension,
        "interpretation": payload.get("interpretation"),
        "order": q,
        "selected_words": [list(word) for word in traded],
        "trade": {
            "removed": [list(word) for word in removed],
            "inserted": [list(word) for word in inserted],
        },
    }
    args.output.write_text(json.dumps(output, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"removed": removed, "inserted": inserted, "new_size": len(traded)}, default=list))


if __name__ == "__main__":
    main()
