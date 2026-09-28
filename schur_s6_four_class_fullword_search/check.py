"""Independently count all classical Schur triples in a 537-digit word."""
import argparse
from pathlib import Path


def violations(path):
    word = Path(path).read_text(encoding="ascii").strip()
    assert len(word) == 537 and set(word) == set("123456")
    colours = [0] + list(map(int, word))
    bad = []
    triples = 0
    doubling = 0
    for x in range(1, 538):
        for y in range(x, 538 - x):
            z = x + y
            triples += 1
            if x == y:
                doubling += 1
            if colours[x] == colours[y] == colours[z]:
                bad.append((x, y, z))
    assert triples == 72092 and doubling == 268
    return bad


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("word", type=Path)
    args = parser.parse_args()
    bad = violations(args.word)
    print(f"triples=72092 doubling=268 defects={len(bad)} bad={bad}")
