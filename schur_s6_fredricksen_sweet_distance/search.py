"""Deterministically find disjoint blocker witnesses for the 536 baseline.

The search is a heuristic for finding a certificate.  check.py proves the
certificate's implication independently of this program or its random choices.
"""

from __future__ import annotations

import argparse
import json
import random
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
NEEDED = {2: 8, 4: 13, 5: 19, 6: 16}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--trials", type=int, default=1000)
    parser.add_argument("--output", type=Path, default=HERE / "certificate.json")
    args = parser.parse_args()
    if args.trials < 1:
        parser.error("--trials must be positive")

    encoded = (HERE / "baseline.txt").read_text(encoding="ascii").strip()
    if len(encoded) != 536 or set(encoded) != set("123456"):
        raise ValueError("invalid baseline")
    color = [0] + [int(x) for x in encoded]
    witnesses: dict[tuple[int, int], list[tuple[tuple[int, ...], tuple[int, int, int]]]] = defaultdict(list)
    for x in range(1, 537):
        for y in range(x, 537 - x):
            triple = (x, y, x + y)
            for v in set(triple):
                support = tuple(sorted(set(triple) - {v}))
                if len({color[u] for u in support}) != 1:
                    continue
                d = color[support[0]]
                if d != color[v]:
                    witnesses[v, d].append((support, triple))

    target_pairs = {c: [] for c in range(1, 7)}
    for x in range(1, 269):
        y = 537 - x
        if color[x] == color[y]:
            target_pairs[color[x]].append((x, y))

    selected_by_color: dict[str, list[dict]] = {str(c): [] for c in range(1, 7)}
    for c, needed in NEEDED.items():
        candidates = [p for p in target_pairs[c]
                      if all(witnesses[v, d] for v in p
                             for d in range(1, 7) if d != c)]
        rng = random.Random(20260928 + c)
        best: list[dict] = []
        for _ in range(args.trials):
            order = candidates[:]
            rng.shuffle(order)
            used: set[int] = set()
            selected: list[dict] = []
            for pair in order:
                if not all(any(not (set(support) & used)
                               for support, _ in witnesses[v, d])
                           for v in pair for d in range(1, 7) if d != c):
                    continue
                local: set[int] = set()
                entries = []
                for v in pair:
                    for d in range(1, 7):
                        if d == c:
                            continue
                        options = [(s, t) for s, t in witnesses[v, d]
                                   if not (set(s) & used)]
                        cheapest = min(len(set(s) - local) for s, _ in options)
                        options = [(s, t) for s, t in options
                                   if len(set(s) - local) == cheapest]
                        support, triple = rng.choice(options[:20])
                        local.update(support)
                        entries.append({"endpoint": v, "new_color": d,
                                        "triple": list(triple)})
                used.update(local)
                selected.append({"pair": list(pair), "witnesses": entries})
            if len(selected) > len(best):
                best = selected
        if len(best) < needed:
            raise RuntimeError(f"found only {len(best)} disjoint pairs for color {c}")
        selected_by_color[str(c)] = best[:needed]

    certificate = {
        "target": 537,
        "claimed_min_distance": 51,
        "selected_by_color": selected_by_color,
    }
    args.output.write_text(json.dumps(certificate, separators=(",", ":")) + "\n",
                           encoding="utf-8")
    print("selected_counts=" + ",".join(
        str(len(selected_by_color[str(c)])) for c in range(1, 7)))


if __name__ == "__main__":
    main()
