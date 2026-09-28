"""Replay the deterministic multiplier-seed local-search scan.

The returned strings are checked directly against x+y=z. A near-colouring is
only a search seed; the independent check.py certifies the committed fixtures.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import tempfile
from concurrent.futures import ProcessPoolExecutor, as_completed
from math import gcd
from pathlib import Path

HERE = Path(__file__).resolve().parent


def canonical(values: list[int]) -> list[int]:
    names: dict[int, int] = {}
    answer = []
    for value in values:
        if value not in names:
            names[value] = len(names) + 1
        answer.append(names[value])
    return answer


def violations(encoded: str) -> list[tuple[int, int, int]]:
    colour = [0] + [int(char) for char in encoded]
    n = len(encoded)
    return [(x, y, x + y)
            for x in range(1, n + 1)
            for y in range(x, n - x + 1)
            if colour[x] == colour[y] == colour[x + y]]


def trial(args: tuple[int, list[int], str, str]) -> tuple[int, int, str]:
    m, baseline, binary, directory = args
    inverse = pow(m, -1, 537)
    transformed = canonical([baseline[(inverse * x) % 537] for x in range(1, 537)])
    prefix = "".join(map(str, transformed))
    if violations(prefix):
        raise ValueError(f"multiplier {m} did not preserve the baseline")
    blocked = [sum(transformed[x - 1] == transformed[537 - x - 1] == c
                   for x in range(1, 269)) for c in range(1, 7)]
    last_colour = min(range(1, 7), key=lambda c: blocked[c - 1])
    source = Path(directory) / f"seed-{m}.txt"
    source.write_text(prefix + str(last_colour) + "\n", encoding="ascii")

    result = subprocess.run(
        [binary, str(source), "537", str(m), "5", "20000", "5", "5", "5"],
        capture_output=True, text=True, timeout=60, check=True,
    )
    final = next(line for line in result.stdout.splitlines() if line.startswith("FINAL "))
    score = int(final.split("best=")[1])
    colouring = result.stdout.split("BEST_COLOR ")[1].splitlines()[0]
    if len(colouring) != 537 or set(colouring) != set("123456"):
        raise ValueError(f"malformed search output for multiplier {m}")
    if len(violations(colouring)) != score:
        raise ValueError(f"search score disagrees with direct check for {m}")
    return m, score, colouring


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--binary", type=Path, required=True)
    parser.add_argument("--workers", type=int, default=4)
    args = parser.parse_args()
    if not 1 <= args.workers <= 16:
        parser.error("--workers must be between 1 and 16")
    binary = str(args.binary.resolve(strict=True))
    encoded = (HERE / "baseline.txt").read_text(encoding="ascii").strip()
    if len(encoded) != 536 or set(encoded) != set("123456"):
        raise ValueError("invalid baseline")
    baseline = [0] + [int(char) for char in encoded]
    expected = {row["multiplier"]: row["colors"] for row in
                json.loads((HERE / "fixtures.json").read_text(encoding="utf-8"))}
    multipliers = [m for m in range(1, 537) if gcd(m, 537) == 1]
    observed: dict[int, tuple[int, str]] = {}
    with tempfile.TemporaryDirectory(prefix="schur-s6-seeds-") as directory:
        with ProcessPoolExecutor(max_workers=args.workers) as pool:
            futures = {pool.submit(trial, (m, baseline, binary, directory)): m
                       for m in multipliers}
            for future in as_completed(futures):
                m, score, colouring = future.result()
                observed[m] = (score, colouring)
                if score == 0:
                    print(f"VERIFIED_537_COLOURING multiplier={m} colours={colouring}",
                          flush=True)

    winners = sorted(m for m, (score, _) in observed.items() if score == 1)
    if winners != [190, 347, 359]:
        raise ValueError(f"unexpected one-violation multipliers: {winners}")
    for m, colouring in expected.items():
        if observed[m] != (1, colouring):
            raise ValueError(f"fixture for multiplier {m} was not reproduced")
    best = min(score for score, _ in observed.values())
    print(f"PASS units={len(observed)} min_violations={best} "
          f"min_multipliers={','.join(map(str, winners))} "
          f"two_violation_starts={sum(score == 2 for score, _ in observed.values())}")


if __name__ == "__main__":
    main()
