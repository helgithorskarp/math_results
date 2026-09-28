"""Replay the five-million-step run from the public two-defect 537 seed."""
import argparse
import subprocess
from pathlib import Path

from check_best3 import defects

HERE = Path(__file__).resolve().parent


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--binary", type=Path, required=True)
    args = parser.parse_args()
    result = subprocess.run(
        [str(args.binary.resolve(strict=True)), str(HERE / "external_two.txt"),
         "20260929", "100", "50000", "18", "5", "5", "4"],
        check=True, capture_output=True, text=True)
    lines = result.stdout.splitlines()
    final = next(line for line in lines if line.startswith("FINAL "))
    word = next(line.split(" ", 1)[1]
                for line in lines if line.startswith("BEST_COLOR "))
    expected = (HERE / "best3.txt").read_text(encoding="ascii").strip()
    if word != expected or "defects=3 direct=3" not in final:
        raise ValueError("replay differs from published 537 word")
    c = [0] + [int(d) for d in word]
    bad = defects(c)
    if len(bad) != 3 or any(x == y for x, y, _, _ in bad):
        raise ValueError("direct triple check failed")
    print("PASS replay_steps=5000000 candidate_defects=3 "
          "doubling_defects=0 exact_word_match=yes")


if __name__ == "__main__":
    main()
