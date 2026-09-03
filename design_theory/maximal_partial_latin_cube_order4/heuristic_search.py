#!/usr/bin/env python3
"""Seeded non-proof witness search for a requested code size."""

from __future__ import annotations

import argparse
import itertools
import json
import math
import random
from pathlib import Path


Word = tuple[int, ...]


def distance(left: Word, right: Word) -> int:
    return sum(a != b for a, b in zip(left, right, strict=True))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--order", type=int, default=4)
    parser.add_argument("--dimension", type=int, default=4)
    parser.add_argument("--size", type=int, default=29)
    parser.add_argument("--seed", type=int, default=20260903)
    parser.add_argument("--restarts", type=int, default=100)
    parser.add_argument("--steps", type=int, default=200_000)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--initial", type=Path)
    parser.add_argument("--independent-only", action="store_true")
    args = parser.parse_args()

    universe = list(itertools.product(range(args.order), repeat=args.dimension))
    n = len(universe)
    adjacency: list[int] = []
    balls: list[int] = []
    for word in universe:
        adjacent = 0
        ball = 0
        for index, other in enumerate(universe):
            d = distance(word, other)
            if d == 1:
                adjacent |= 1 << index
            if d <= 1:
                ball |= 1 << index
        adjacency.append(adjacent)
        balls.append(ball)
    full = (1 << n) - 1

    initial: list[int] | None = None
    if args.initial:
        payload = json.loads(args.initial.read_text(encoding="utf-8"))
        index = {word: i for i, word in enumerate(universe)}
        initial = [index[tuple(map(int, word))] for word in payload["selected_words"]]

    def score(state: list[int]) -> tuple[int, int, int]:
        mask = sum(1 << word for word in state)
        conflicts = sum((adjacency[word] & mask).bit_count() for word in state) // 2
        covered = 0
        for word in state:
            covered |= balls[word]
        uncovered = (full ^ covered).bit_count()
        return 20 * conflicts + uncovered, conflicts, uncovered

    rng = random.Random(args.seed)
    best: tuple[int, int, int] | None = None
    for restart in range(args.restarts):
        if args.independent_only:
            while True:
                state = []
                shuffled = list(range(n))
                rng.shuffle(shuffled)
                for word in shuffled:
                    mask = sum(1 << chosen for chosen in state)
                    if not adjacency[word] & mask:
                        state.append(word)
                        if len(state) == args.size:
                            break
                if len(state) == args.size:
                    break
        elif initial is not None and restart == 0:
            state = initial.copy()
            while len(state) < args.size:
                candidate = rng.randrange(n)
                if candidate not in state:
                    state.append(candidate)
            while len(state) > args.size:
                state.pop(rng.randrange(len(state)))
        else:
            state = rng.sample(range(n), args.size)
        current = score(state)
        present = set(state)
        for step in range(args.steps):
            if current[1:] == (0, 0):
                payload = {
                    "dimension": args.dimension,
                    "interpretation": "[layer, row, column, symbol] with coordinates numbered 0 through 3",
                    "order": args.order,
                    "search": {"restart": restart, "seed": args.seed, "step": step},
                    "selected_words": [list(universe[word]) for word in sorted(state)],
                }
                args.output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
                print(json.dumps({"status": "FOUND", **payload["search"]}))
                return
            remove_position = rng.randrange(args.size)
            removed = state[remove_position]
            if args.independent_only:
                remaining_mask = sum(1 << word for i, word in enumerate(state) if i != remove_position)
                choices = [
                    word
                    for word in range(n)
                    if word not in present and not adjacency[word] & remaining_mask
                ]
                if not choices:
                    continue
                inserted = rng.choice(choices)
            else:
                while True:
                    inserted = rng.randrange(n)
                    if inserted not in present:
                        break
            state[remove_position] = inserted
            candidate_score = score(state)
            initial_temperature = 3.0 if args.independent_only else 8.0
            temperature = max(0.2, initial_temperature * (1.0 - (step % 20_000) / 20_000))
            delta = candidate_score[0] - current[0]
            if delta <= 0 or rng.random() < math.exp(-delta / temperature):
                present.remove(removed)
                present.add(inserted)
                current = candidate_score
            else:
                state[remove_position] = removed
            if best is None or current < best:
                best = current
                print(json.dumps({"best": best, "restart": restart, "step": step}), flush=True)
    raise SystemExit(f"no witness found; best score was {best}")


if __name__ == "__main__":
    main()
