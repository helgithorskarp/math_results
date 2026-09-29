#!/usr/bin/env python3
"""Independent, standard-library audit of a 536-word and its 537 extension."""
import argparse
import json
from pathlib import Path


def read_word(path, length):
    word = path.read_text().strip()
    if len(word) != length or any(c not in "123456" for c in word):
        raise ValueError(f"{path}: expected {length} digits in 1,...,6")
    return word


def bad_triples(word):
    n = len(word)
    return [(x, y, x + y) for x in range(1, n + 1)
            for y in range(x, n - x + 1)
            if word[x - 1] == word[y - 1] == word[x + y - 1]]


def pair_counts(word):
    if len(word) != 536:
        raise ValueError("reflected pairs require a 536-word")
    return [sum(word[x - 1] == word[536 - x] == str(c)
                for x in range(1, 269)) for c in range(1, 7)]


def audit(path):
    word = read_word(path, 536)
    bad = bad_triples(word)
    counts = pair_counts(word)
    if bad:
        raise AssertionError(f"{path}: {len(bad)} bad triples, first {bad[0]}")
    for colour in range(1, 7):
        extension_bad = bad_triples(word + str(colour))
        if len(extension_bad) != counts[colour - 1]:
            raise AssertionError("reflected-pair formula failed")
        if any(z != 537 for _, _, z in extension_bad):
            raise AssertionError("old triple appeared on extension")
    return {"word": path.name, "length": 536, "bad_triples": 0,
            "extension_bad_triples_by_colour": counts}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("word", type=Path)
    args = parser.parse_args()
    print(json.dumps(audit(args.word), sort_keys=True))
