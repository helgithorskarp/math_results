"""Replay eight bounded nonlocal searches and check every returned word."""

import argparse
import subprocess
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path

HERE = Path(__file__).resolve().parent
JOBS = [
    ("seed_359.txt", 30001, 12, 0, 5, 5),
    ("seed_359.txt", 30002, 40, 1, 3, 10),
    ("seed_359.txt", 30003, 30, 5, 15, 7),
    ("seed_359.txt", 30004, 80, 10, 30, 3),
    ("best4.txt", 30005, 20, 0, 10, 2),
    ("best4.txt", 30006, 30, 2, 5, 15),
    ("best4.txt", 30007, 100, 10, 5, 5),
    ("best4.txt", 30008, 20, 3, 20, 20),
]
EXPECTED = {30001: (4, 58), 30002: (4, 78), 30003: (6, 57),
            30004: (5, 79), 30005: (4, 0), 30006: (4, 0),
            30007: (4, 0), 30008: (4, 0)}


def score(word: str) -> int:
    colour = [0] + [int(d) for d in word]
    return sum(colour[x] == colour[y] == colour[x + y]
               for x in range(1, 538) for y in range(x, 538 - x))


def run(binary: str, job: tuple) -> tuple[int, int, int, str]:
    filename, seed, kick, global_noise, local_noise, tabu = job
    source = (HERE / filename).read_text(encoding="ascii").strip()
    result = subprocess.run(
        [binary, str(HERE / filename), str(seed), "40", "50000", str(kick),
         str(global_noise), str(local_noise), str(tabu)],
        check=True, capture_output=True, text=True)
    lines = result.stdout.splitlines()
    final = next(line for line in lines if line.startswith("FINAL "))
    claimed = int(final.split("defects=")[1].split()[0])
    word = next(line.split(" ", 1)[1]
                for line in lines if line.startswith("BEST_COLOR "))
    if len(word) != 537 or set(word) != set("123456"):
        raise ValueError(f"malformed word from seed {seed}")
    actual = score(word)  # Includes x=y; independent of the C++ scoring code.
    if claimed != actual:
        raise ValueError(f"score mismatch for seed {seed}: {claimed} vs {actual}")
    return seed, actual, sum(a != b for a, b in zip(source, word)), word


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--binary", type=Path, required=True)
    parser.add_argument("--workers", type=int, default=8)
    args = parser.parse_args()
    if not 1 <= args.workers <= 16:
        parser.error("workers must be between 1 and 16")
    binary = str(args.binary.resolve(strict=True))
    rows = []
    with ProcessPoolExecutor(max_workers=args.workers) as pool:
        futures = [pool.submit(run, binary, job) for job in JOBS]
        for future in as_completed(futures):
            row = future.result()
            rows.append(row)
            if row[1] == 0:
                print(f"VERIFIED_537_COLOURING seed={row[0]} word={row[3]}",
                      flush=True)
    rows.sort()
    observed = {seed: (defects, distance) for seed, defects, distance, _ in rows}
    if observed != EXPECTED:
        raise ValueError(f"bounded sweep changed: {observed}")
    for seed, defects, distance, _ in rows:
        print(f"seed={seed} defects={defects} distance={distance}")
    print("PASS trials=8 steps=16000000 minimum_defects=4")


if __name__ == "__main__":
    main()
