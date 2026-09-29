"""Definition-level checker for a complete six-colouring of [1,537]."""
import argparse
from pathlib import Path


def defects(word):
    if len(word) != 537 or any(c not in "123456" for c in word):
        raise ValueError("expected 537 digits in 1,...,6")
    return [(x, y, x + y) for x in range(1, 538)
            for y in range(x, 538 - x)
            if word[x - 1] == word[y - 1] == word[x + y - 1]]


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("word", type=Path)
    args = parser.parse_args()
    word = args.word.read_text().strip()
    bad = defects(word)
    print(f"length={len(word)} bad_count={len(bad)} bad={bad[:10]}")
    if bad:
        raise SystemExit(1)
