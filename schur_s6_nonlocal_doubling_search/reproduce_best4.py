"""Replay the bounded run that generated best4.txt, then check it directly."""

import argparse
import subprocess
from pathlib import Path

from check import violations

HERE = Path(__file__).resolve().parent


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--binary", type=Path, required=True)
    args = parser.parse_args()
    result = subprocess.run(
        [str(args.binary.resolve(strict=True)), str(HERE / "seed_359.txt"),
         "10359", "100", "50000", "18", "5", "5", "4"],
        check=True, capture_output=True, text=True)
    lines = result.stdout.splitlines()
    final = next(line for line in lines if line.startswith("FINAL "))
    word = next(line.split(" ", 1)[1]
                for line in lines if line.startswith("BEST_COLOR "))
    expected = (HERE / "best4.txt").read_text(encoding="ascii").strip()
    if word != expected or "defects=4 direct=4" not in final:
        raise ValueError("bounded replay differs from published candidate")
    count, bad = violations(word)
    if count != 72092 or len(bad) != 4 or any(x == y for x, y, _ in bad):
        raise ValueError("independent Schur check failed")
    print("PASS replay_steps=5000000 candidate_defects=4 "
          "doubling_defects=0 exact_word_match=yes")


if __name__ == "__main__":
    main()
